"""The onboarding factory's dispatcher, end to end with stub workers (docs/factory-spec.md).

Each test builds a git repo with a bare `origin`, so worktrees, commits, pushes and
merges are real. Workers are stubs, GitHub is files (`LocalForge`), and the commands a
gate runs are faked.
"""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
import subprocess
import threading
import time
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.blobstore import BlobStoreError
from pdf_extract.factory import dispatcher as dispatcher_mod
from pdf_extract.factory import forge as forge_mod
from pdf_extract.factory import playbook, readiness, render, report
from pdf_extract.factory.backfill import backfill
from pdf_extract.factory.config import Account, Config, FactoryError, load_config
from pdf_extract.factory.dispatcher import Dispatcher
from pdf_extract.factory.forge import LocalForge
from pdf_extract.factory.handoff import read_handoff
from pdf_extract.factory.ledger import (
    ACTIVE,
    BLOCKED,
    DONE,
    IN_REVIEW,
    MAP,
    MERGED,
    PENDING,
    RUNNING,
    SEED,
    WAITING_USAGE,
    Ledger,
)
from pdf_extract.factory.quota import (
    IMMEDIATE,
    INCONSISTENT,
    MISSING,
    RESET,
    SETTLED,
    SHARED,
    Analysis,
    Measure,
    Reading,
    Span,
    combine,
)
from pdf_extract.factory.stages import in_scope
from pdf_extract.factory.tokens import from_result, parse_transcript
from pdf_extract.factory.usage import (
    Standing,
    Usage,
    UsageError,
    account_plan,
    choose,
    parse_usage,
    standing,
)
from pdf_extract.factory.workers import (
    OK,
    USAGE,
    StubAction,
    StubWorker,
    WorkerRequest,
    WorkerResult,
)

ROOT = Path(__file__).resolve().parents[1]
D = "testd"

META = """\
---
name: Diocese of Testd
state: DE
status: exploring
---
The test diocese.

## Sources

### Bulletin publishers here

- Parishes Online prints most bulletins.

## Rules settled for this diocese

## Log
"""
ROSTER = {"name": "directory", "title": "Directory", "fetched": "2026-10-01", "entries": [
    {"id": "1", "name": "St. Ann", "city": "Dover"},
    {"id": "2", "name": "St. Bede", "city": "Dover"},
    {"id": "3", "name": "St. Clare", "city": "Lewes"},
]}
BATCHES = {"version": 1, "diocese": D, "first_batch": "b2", "batches": [
    {"id": "b1", "name": "Dover", "why": "one town", "entries": ["directory:1", "directory:2"]},
    {"id": "b2", "name": "Lewes", "why": "typical", "entries": ["directory:3"]},
], "excluded": []}


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                          text=True).stdout


def survey_files() -> dict[str, str]:
    return {
        "data/dioceses/{diocese}/diocese.md": META,
        "data/dioceses/{diocese}/rosters/directory.json": json.dumps(ROSTER),
        "data/dioceses/{diocese}/batches.json": json.dumps(BATCHES),
    }


def parish_record(roster: str) -> str:
    return (f"---\nname: Parish\nbulletin_provider: parishes_online\nprovider_id: x\n"
            f"roster: ['{roster}']\n---\nNotes.\n")


def seed_file(parish: str, status: str = "needs_review") -> str:
    entry = {"church": "c", "day": "sunday", "start": "09:00"}
    return json.dumps({"parish_slug": parish, "status": status, "slots": [{
        "id": "s1", "status": "needs_human", "question": "Is the 9:00 Mass weekly?",
        "options": [{"label": "Include", "entry": entry, "leaning": True},
                    {"label": "Leave out", "entry": None, "leaning": False}]}]})


def done(summary: str = "ok", **extra: Any) -> dict[str, Any]:
    return {"status": "done", "summary": summary, **extra}


class Env:
    def __init__(self, tmp: Path) -> None:
        self.tmp = tmp
        self.remote = tmp / "remote.git"
        self.repo = tmp / "repo"
        self.forge = LocalForge(tmp / "forge")
        self.ledger = Ledger(tmp / "ledger.db")
        self.config = Config(worktrees_dir=tmp / "wt", setup=[], owner="owner")
        self.now = datetime(2026, 11, 2, 12, tzinfo=UTC)
        self.commands_run: list[str] = []
        self.failing: dict[str, int] = {}  # command substring -> failures left

    def clock(self) -> datetime:
        return self.now

    def commands(self, command: str, cwd: Path) -> tuple[bool, str]:
        self.commands_run.append(command)
        for needle, left in list(self.failing.items()):
            if needle in command and left > 0:
                self.failing[needle] = left - 1
                return False, f"{needle} failed on purpose"
        if command.startswith("pnpm seed approve"):
            parts = command.split()
            parish, reviewer = parts[3], parts[parts.index("--reviewer") + 1]
            path = cwd / "data" / "seeds" / f"{parish}.json"
            seed = json.loads(path.read_text())
            if seed["status"] == "approved":  # as `seed approve` refuses
                return False, f"Already approved by {seed['reviewer']}"
            seed |= {"status": "approved", "reviewer": reviewer}
            path.write_text(json.dumps(seed))
        if "diocese coverage" in command:
            return True, json.dumps({"diocese": D, "rosters": [
                {"roster": "directory", "title": "Directory", "accounted_for": "3/3 (100%)",
                 "modelled": "3/3"}]})
        return True, "ok"

    def dispatcher(self, script: Callable[[WorkerRequest, int], StubAction], **kw: Any):
        self.worker = StubWorker(script)
        return Dispatcher(self.ledger, self.config, repo=self.repo, worker=self.worker,
                          forge=self.forge, clock=self.clock, commands=self.commands,
                          db_path=self.tmp / "parish_events.db", runs_dir=self.tmp / "runs",
                          queue_path=self.repo / "factory" / "queue.json", **kw)

    def answer(self, number: int, body: str | None, author: str = "owner") -> None:
        path = self.forge.folder / "issues" / f"{number}.json"
        data = json.loads(path.read_text())
        data["state"] = "CLOSED"
        if body is not None:
            data["comments"].append({"author": author, "body": body})
        path.write_text(json.dumps(data))

    def commit_main(self, files: dict[str, str], message: str) -> None:
        for rel, content in files.items():
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", message)
        git(self.repo, "push", "-q", "origin", "main")


@pytest.fixture
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Env:
    e = Env(tmp_path)
    git(tmp_path, "init", "-q", "--bare", "-b", "main", str(e.remote))
    e.repo.mkdir()
    git(e.repo, "init", "-q", "-b", "main")
    git(e.repo, "config", "user.email", "factory@example.com")
    git(e.repo, "config", "user.name", "Factory")
    shutil.copytree(ROOT / "factory", e.repo / "factory")
    (e.repo / "factory" / "queue.json").write_text(json.dumps([{"diocese": D, "notes": "Test"}]))
    (e.repo / ".gitignore").write_text("scratch/\ndata/factory/\n")
    (e.repo / "data").mkdir()
    (e.repo / "data" / "parishes.csv").write_text("slug\n")
    git(e.repo, "add", "-A")
    git(e.repo, "commit", "-qm", "init")
    git(e.repo, "remote", "add", "origin", str(e.remote))
    git(e.repo, "push", "-q", "-u", "origin", "main")
    for wt in (e.tmp / "wt",):
        wt.mkdir()
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Factory")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "factory@example.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "Factory")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "factory@example.com")
    monkeypatch.chdir(e.repo)
    return e


def drive(d: Dispatcher, limit: int = 60) -> list[str]:
    """Tick until the dispatcher has nothing to do; the outcomes, in order."""
    seen = []
    for _ in range(limit):
        outcome = d.tick()
        seen.append(f"{outcome.action}: {outcome.detail}")
        if outcome.action in ("idle", "waiting", "paused"):
            return seen
    raise AssertionError("the dispatcher never went idle:\n" + "\n".join(seen[-10:]))


def map_script(**overrides: Callable[[WorkerRequest, int], StubAction]):
    """A map Run where every stage succeeds; `overrides` replace a stage's behaviour."""
    def script(req: WorkerRequest, attempt: int) -> StubAction:
        if req.stage in overrides:
            return overrides[req.stage](req, attempt)
        if req.stage == "survey":
            return StubAction(files=survey_files(), handoff=done("surveyed"))
        if req.stage == "survey-review":
            return StubAction(handoff=done(verdict="approve",
                                           rules=["Campus Masses are left out."]))
        if req.stage == "map":
            return StubAction(
                files={"data/dioceses/{diocese}/parishes/p-{job}.md": parish_record("x:1")},
                handoff=done(lessons=[f"Lesson from {req.job_name}"],
                             leads=[{"touches": "b1", "note": "St. Ann may share St. Bede's"}]))
        return StubAction(handoff=done())
    return script


def map_run(env: Env) -> Any:
    return next(r for r in env.ledger.runs() if r["kind"] == MAP)


# ── A map Run end to end ─────────────────────────────────────────────────────
def test_map_run_end_to_end(env: Env) -> None:
    d = env.dispatcher(map_script())
    drive(d)
    run = map_run(env)
    assert run["status"] == IN_REVIEW
    stages = [j["stage"] for j in env.ledger.jobs(run["id"])]
    assert stages == ["survey", "survey-review", "map", "map", "reconcile", "promote", "pr"]
    # first_batch first, then the file's order.
    maps = [json.loads(j["input"])["batch"] for j in env.ledger.jobs(run["id"], "map")]
    assert maps == ["b2", "b1"]
    # Every job committed and pushed with its trailer.
    log = git(env.repo, "log", f"origin/{run['branch']}", "--format=%B")
    assert f"Factory-Job: {run['id']}/001-survey" in log
    assert f"Factory-Job: {run['id']}/003-map" in log
    meta = Path(run["worktree"]) / "data" / "dioceses" / D / "diocese.md"
    rules = playbook.bullets(meta, playbook.RULES)
    assert rules and rules[0].startswith("Campus Masses are left out.")
    assert playbook.bullets(meta, playbook.NEW_LESSONS) == [
        "Lesson from 003-map", "Lesson from 004-map"]
    # The first batch's lead about b1 reached b1's job input.
    b1 = env.ledger.jobs(run["id"], "map")[1]
    assert "St. Ann may share" in env.ledger.all(
        "SELECT prompt FROM attempt WHERE job_id = ?", b1["id"])[0]["prompt"]
    assert any("diocese promote testd" in c for c in env.commands_run)
    pr = next((env.forge.folder / "prs").glob("*.md")).read_text()
    assert "Directory: 3/3 (100%) accounted for" in pr
    assert run["pr_url"] and run["head_sha"] == git(Path(run["worktree"]), "rev-parse",
                                                    "HEAD").strip()


def test_integrate_runs_when_new_lessons_pass_the_threshold(env: Env) -> None:
    env.config.lessons_before_integrate = 1

    def mapping(req: WorkerRequest, attempt: int) -> StubAction:
        return StubAction(handoff=done(lessons=[f"{req.job_name} one", f"{req.job_name} two"]))

    def integrating(req: WorkerRequest, attempt: int) -> StubAction:
        meta = req.worktree / "data" / "dioceses" / D / "diocese.md"
        text = meta.read_text()
        kept = "\n".join(line for line in text.splitlines() if not line.startswith("- 0"))
        return StubAction(files={"data/dioceses/{diocese}/diocese.md": kept + "\n"},
                          handoff=done())

    d = env.dispatcher(map_script(map=mapping, integrate=integrating))
    drive(d)
    stages = [j["stage"] for j in env.ledger.jobs(map_run(env)["id"])]
    assert stages == ["survey", "survey-review", "map", "integrate", "map", "integrate",
                      "reconcile", "promote", "pr"]


# ── Send-backs, scope, retries ───────────────────────────────────────────────
def test_a_failing_gate_sends_the_job_back_to_its_session(env: Env) -> None:
    env.failing["diocese validate"] = 1  # the survey's validate passes the second time
    d = env.dispatcher(map_script())
    drive(d)
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    assert survey["send_backs"] == 1
    attempts = env.ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", survey["id"])
    assert [a["kind"] for a in attempts] == ["start", "send_back"]
    assert "failed on purpose" in attempts[1]["prompt"]
    resumed = [r for r in env.worker.calls if r.job_id == survey["id"]][1]
    assert resumed.session_id == f"stub-{survey['id']}"


def test_out_of_scope_changes_are_reverted_and_sent_back(env: Env) -> None:
    def mapping(req: WorkerRequest, attempt: int) -> StubAction:
        files = {"data/dioceses/{diocese}/parishes/p.md": parish_record("x:1")}
        if attempt == 1:
            files["data/parishes.csv"] = "slug\nsneaky\n"
        return StubAction(files=files, handoff=done())

    d = env.dispatcher(map_script(map=mapping))
    drive(d)
    run = map_run(env)
    first = env.ledger.jobs(run["id"], "map")[0]
    assert first["send_backs"] == 1
    gate = env.ledger.one("SELECT * FROM gate WHERE job_id = ? AND name = 'diff-scope' "
                          "ORDER BY id LIMIT 1", first["id"])
    assert not gate["passed"] and "data/parishes.csv" in gate["output"]
    assert (Path(run["worktree"]) / "data" / "parishes.csv").read_text() == "slug\n"


def test_past_its_send_backs_a_job_blocks_the_run(env: Env) -> None:
    env.failing["diocese batches validate"] = 99
    d = env.dispatcher(map_script())
    out = drive(d)
    run = map_run(env)
    assert run["status"] == BLOCKED
    assert out[-1].startswith("idle")
    flag = env.ledger.flags(run["id"])[0]
    assert flag["scope"] == "run" and flag["issue_number"] == 1
    issue = json.loads((env.forge.folder / "issues" / "1.json").read_text())
    assert "factory" in issue["labels"] and f"run:{D}" in issue["labels"]
    assert "stage:survey" in issue["labels"]


def test_a_missing_handoff_is_sent_back(env: Env) -> None:
    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        return StubAction(files=survey_files(), handoff=None if attempt == 1 else done())

    d = env.dispatcher(map_script(survey=surveying))
    drive(d)
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    assert survey["send_backs"] == 1 and survey["status"] == DONE


def test_partial_is_continued_once(env: Env) -> None:
    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        status = "partial" if attempt == 1 else "done"
        return StubAction(files=survey_files(), handoff={"status": status, "summary": "s"})

    d = env.dispatcher(map_script(survey=surveying))
    drive(d)
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    kinds = [a["kind"] for a in env.ledger.all(
        "SELECT kind FROM attempt WHERE job_id = ? ORDER BY n", survey["id"])]
    assert kinds == ["start", "continue"] and survey["continues"] == 1


def test_the_number_of_continues_is_a_setting(env: Env) -> None:
    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        status = "partial" if attempt < 3 else "done"
        return StubAction(files=survey_files(), handoff={"status": status, "summary": "s"})

    env.config.max_continues = 2
    d = env.dispatcher(map_script(survey=surveying))
    drive(d)
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    assert survey["continues"] == 2 and survey["status"] == DONE


def test_a_crash_resumes_the_session_and_a_restart_resumes_a_running_job(env: Env) -> None:
    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 1:
            return StubAction(outcome="crash")
        return StubAction(files=survey_files(), handoff=done())

    d = env.dispatcher(map_script(survey=surveying))
    d.tick()
    d.tick()
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    assert [a["kind"] for a in env.ledger.all(
        "SELECT kind FROM attempt WHERE job_id = ?", survey["id"])] == ["start", "resume"]
    # A dispatcher killed mid-job leaves it `running`; the next one resumes it.
    review = env.ledger.add_job(survey["run_id"], "survey-review", {"survey_job": survey["id"]})
    env.ledger.set_job(review, status=RUNNING, session_id="lost-session")
    d2 = env.dispatcher(map_script())
    d2._recover()
    drive(d2)
    assert env.ledger.job(review)["status"] == DONE
    assert env.worker.calls[0].session_id == "lost-session"


def test_usage_limit_waits_then_resumes_the_same_session(env: Env) -> None:
    resets = env.now + timedelta(hours=1)

    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 1:
            return StubAction(outcome=USAGE, resets_at=resets)
        return StubAction(files=survey_files(), handoff=done())

    d = env.dispatcher(map_script(survey=surveying))
    out = drive(d)
    assert out[-1].startswith("waiting")
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    assert survey["status"] == WAITING_USAGE
    assert d.tick().action == "waiting"
    env.now = resets + timedelta(minutes=1)
    drive(d)
    assert env.ledger.job(survey["id"])["status"] == DONE
    assert env.worker.calls[1].session_id == f"stub-{survey['id']}"


def test_survey_review_send_back_resumes_the_survey(env: Env) -> None:
    def reviewing(req: WorkerRequest, attempt: int) -> StubAction:
        if req.job_name == "002-survey-review":
            return StubAction(handoff=done(verdict="send_back", problems=["Split b1"]))
        return StubAction(handoff=done(verdict="approve"))

    d = env.dispatcher(map_script(**{"survey-review": reviewing}))
    drive(d)
    run = map_run(env)
    stages = [j["stage"] for j in env.ledger.jobs(run["id"])][:3]
    assert stages == ["survey", "survey-review", "survey-review"]
    survey = env.ledger.jobs(run["id"], "survey")[0]
    assert survey["send_backs"] == 1
    prompts = [a["prompt"] for a in env.ledger.all(
        "SELECT prompt FROM attempt WHERE job_id = ? ORDER BY n", survey["id"])]
    assert "Split b1" in prompts[1]
    second_review = env.ledger.jobs(run["id"], "survey-review")[1]
    first_prompt = env.ledger.one("SELECT prompt FROM attempt WHERE job_id = ?",
                                  second_review["id"])["prompt"]
    assert "Split b1" in first_prompt  # the re-review sees what the first one asked for


# ── Flags, issues and answers ────────────────────────────────────────────────
def parking_map(req: WorkerRequest, attempt: int) -> StubAction:
    data = req.values
    if req.job_name == "003-map":
        return StubAction(handoff=done(flags=[{
            "severity": "blocking", "scope": "parish", "subject": "directory:3",
            "question": "Is St. Clare closed?", "evidence": ["https://x 2026-10-01"],
            "suggestion": "Exclude it as closed."}]))
    return StubAction(handoff=done(summary=f"mapped {data['job']}"))


def test_a_parked_parish_is_resumed_with_the_owners_answer(env: Env) -> None:
    d = env.dispatcher(map_script(map=parking_map))
    drive(d)
    run = map_run(env)
    assert run["status"] == IN_REVIEW  # the rest of the Run carried on
    flag = env.ledger.flags(run["id"])[0]
    assert flag["status"] == "open" and flag["issue_number"] == 1
    assert "Parked parishes" in next((env.forge.folder / "prs").glob("*.md")).read_text()


def test_answers_while_the_run_is_active_requeue_the_job(env: Env) -> None:
    d = env.dispatcher(map_script(map=parking_map))
    for _ in range(4):  # survey, survey-review, map b2 (parks directory:3), map b1
        d.tick()
    run = map_run(env)
    env.answer(1, None)  # closed with no answer: reopened, nothing changes
    d.poll_issues()
    issue = env.forge.issue(1)
    assert issue.state == "OPEN" and "without an answer" in issue.comments[-1].body
    env.answer(1, "/accept")
    d.poll_issues()
    requeued = env.ledger.jobs(run["id"], "map")[-1]
    data = json.loads(requeued["input"])
    assert data["answer"] == "Exclude it as closed." and data["entries"] == ["directory:3"]
    drive(d)
    attempt = env.ledger.one("SELECT * FROM attempt WHERE job_id = ?", requeued["id"])
    assert attempt["kind"] == "answer" and "Exclude it as closed." in attempt["prompt"]
    first = env.ledger.jobs(run["id"], "map")[0]
    call = next(c for c in env.worker.calls if c.job_id == requeued["id"])
    assert call.session_id == f"stub-{first['id']}"  # it resumed the parking job's session
    # It ran before reconcile.
    stages = [j["stage"] for j in env.ledger.jobs(run["id"])]
    assert stages.index("reconcile") > stages.index("map", 4)


def test_only_the_owners_comments_answer(env: Env) -> None:
    issue = forge_mod.Issue(1, "CLOSED", [
        forge_mod.Comment("owner", "Keep it open"),
        forge_mod.Comment("owner", f"{forge_mod.MARKER}\nreopened"),
        forge_mod.Comment("someone", "Exclude it"),
    ])
    assert forge_mod.answer(issue, "owner", "sugg") == "Keep it open"
    issue.comments.append(forge_mod.Comment("Owner", "/accept and date it 2024"))
    assert forge_mod.answer(issue, "owner", "sugg") == "sugg\n\nand date it 2024"
    assert forge_mod.answer(forge_mod.Issue(2, "CLOSED"), "owner", "s") is None


def test_answers_after_the_pr_opened_go_to_a_follow_up_run(env: Env) -> None:
    d = env.dispatcher(map_script(map=parking_map))
    drive(d)
    run = map_run(env)
    env.answer(1, "It is open; map it.")
    d.poll_issues()
    follow = next(r for r in env.ledger.runs() if r["follow_up_of"] == run["id"])
    assert follow["status"] == PENDING and follow["id"] == f"{D}-map-2"
    assert drive(d)[-1].startswith("idle")  # waits for the first PR to merge
    git(Path(run["worktree"]), "push", "-q", "origin", "HEAD:main")
    git(env.repo, "fetch", "-q", "origin")
    d.check_merged()
    assert env.ledger.run(run["id"])["status"] == MERGED
    # Its worktree and local branch are gone; its scratch was kept for foreman reviews.
    assert not Path(run["worktree"]).exists()
    assert not git(env.repo, "branch", "--list", run["branch"]).strip()
    assert (env.tmp / "runs" / run["id"] / "scratch" / "001-survey" / "handoff.json").exists()
    drive(d)
    follow = env.ledger.run(follow["id"])
    assert [j["stage"] for j in env.ledger.jobs(follow["id"])] == ["map", "promote", "pr"]
    assert follow["status"] == IN_REVIEW
    first = env.ledger.one("SELECT * FROM attempt a JOIN job j ON j.id = a.job_id "
                           "WHERE j.run_id = ?", follow["id"])
    # Another worktree can't resume the old session: a fresh worker gets the answer.
    assert first["kind"] == "start" and "It is open; map it." in first["prompt"]


def test_a_squash_merged_pr_counts_as_merged(env: Env) -> None:
    d = env.dispatcher(map_script())
    drive(d)
    run = map_run(env)
    d.check_merged()
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW
    env.forge.merge_pr(run["pr_url"])  # squashed: the Run's commits aren't in main
    d.check_merged()
    assert env.ledger.run(run["id"])["status"] == MERGED


def test_github_failing_partway_waits_and_tries_again(env: Env) -> None:
    open_pr = env.forge.open_pr
    calls = []

    def flaky(*args: Any) -> str:
        calls.append(args)
        if len(calls) == 1:
            raise FactoryError("gh pr create: connection reset")
        return open_pr(*args)

    env.forge.open_pr = flaky  # type: ignore[method-assign]
    d = env.dispatcher(map_script())
    out = drive(d)
    assert out[-1].startswith("waiting") and "connection reset" in out[-1]
    drive(d)
    run = map_run(env)
    assert run["status"] == IN_REVIEW and len(calls) == 2


def test_github_failing_again_and_again_blocks_the_run(env: Env) -> None:
    open_pr = env.forge.open_pr

    def down(*args: Any) -> str:
        raise FactoryError("gh: authentication expired")

    env.forge.open_pr = down  # type: ignore[method-assign]
    d = env.dispatcher(map_script())
    drive(d)
    assert d.tick().action == "waiting"
    out = d.tick()
    assert out.action == "blocked" and "failed 3 times" in out.detail
    assert map_run(env)["status"] == BLOCKED
    # Once it's fixed and the issue closed, the job carries on where it stopped.
    env.forge.open_pr = open_pr  # type: ignore[method-assign]
    env.answer(1, "Signed in to gh again.")
    d.poll_issues()
    drive(d)
    assert map_run(env)["status"] == IN_REVIEW
    assert len(env.ledger.jobs(map_run(env)["id"], "pr")) == 1


def test_a_parish_flag_from_a_stage_that_cant_park_is_sent_back(tmp_path: Path) -> None:
    path = tmp_path / "h.json"
    path.write_text(json.dumps({"status": "done", "summary": "s", "verdict": "approve",
                                "flags": [{"severity": "blocking", "scope": "parish",
                                           "subject": "directory:3", "question": "q"}]}))
    assert "only map and seed" in read_handoff(path, "survey-review")[1][0]
    data = json.loads(path.read_text())
    del data["verdict"]
    path.write_text(json.dumps(data))
    assert not read_handoff(path, "map")[1]  # a map job parks the parish


OPEN_RECORD = ("---\nname: Chapel\nrevisit: Ask the parish office\nrevisit_after: 2027-01-31\n"
               "roster: []\nevidence: []\n---\nNotes.\n")
GAP = ("fetch_gap:\n  kind: solutio-file-403\n  seen: 2026-10-21\n"
       "  note: \"Solutio /file links\\n  answer 403.\"\n")


def test_reconcile_settles_earlier_flags_and_the_pr_lists_the_rest(env: Env) -> None:
    def mapping(req: WorkerRequest, attempt: int) -> StubAction:
        parish = parish_record("x:1")
        if req.job_name == "003-map":
            parish = parish.replace("---\nNotes", GAP + "---\nNotes")
        return StubAction(
            files={"data/dioceses/{diocese}/parishes/p-{job}.md": parish,
                   "data/dioceses/{diocese}/open/chapel-{job}.md": OPEN_RECORD},
            handoff=done(flags=[{"severity": "advisory", "scope": "parish",
                                 "subject": f"p-{req.job_name}",
                                 "question": f"Merge p-{req.job_name} into St. Ann?"}]))

    shown: list[int] = []

    def reconciling(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 1:
            shown.extend(int(i) for i in re.findall(r"\[#(\d+)\]", req.prompt))
            return StubAction(handoff=done(settled=[{"flag": 999, "how": "?"}]))
        return StubAction(handoff=done(
            settled=[{"flag": shown[0], "how": "Merged;\none masthead."}],
            flags=[{"severity": "advisory", "scope": "parish", "subject": "p-004-map",
                    "question": "Kept apart: two mastheads."}]))

    d = env.dispatcher(map_script(map=mapping, reconcile=reconciling))
    drive(d)
    run = map_run(env)
    first, second, own = env.ledger.flags(run["id"])
    assert shown == [first["id"], second["id"]]
    reconcile = env.ledger.jobs(run["id"], "reconcile")[0]
    assert reconcile["send_backs"] == 1  # flag 999 isn't one of its Run's
    assert (first["status"], first["answer"], first["settled_by"]) == (
        "settled", "Merged;\none masthead.", reconcile["id"])
    assert second["status"] == "listed"
    # A fresh input (after a resume or a retry) leaves out the flags it raised itself,
    # which it can't settle.
    again = render.stage_input(env.ledger, run, reconcile, {})
    assert f"[#{second['id']}]" in again and f"[#{own['id']}]" not in again

    pr = next((env.forge.folder / "prs").glob("*.md")).read_text()
    open_section = pr.split("## Left open")[1].split("##")[0]
    assert "- `chapel-003-map` Chapel: Ask the parish office (after 2027-01-31)" in open_section
    assert "`solutio-file-403` (1): `p-003-map`. Solutio /file links answer 403." in pr
    flags = pr.split("## Advisory flags")[1].split("## Parked")[0]
    listed, collapsed = flags.split("<details>")
    assert "Merge p-004-map into St. Ann?" in listed and "p-003-map" not in listed
    assert ("Merge p-003-map into St. Ann? **Settled by 005-reconcile:** Merged; one "
            "masthead.") in collapsed


def test_a_run_level_flag_blocks_until_answered(env: Env) -> None:
    def reconciling(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 1:
            return StubAction(handoff={"status": "blocked", "summary": "s", "flags": [{
                "severity": "blocking", "scope": "run", "subject": "testd-map-1",
                "question": "Two batches claim St. Bede"}]})
        return StubAction(handoff=done())

    d = env.dispatcher(map_script(reconcile=reconciling))
    drive(d)
    run = map_run(env)
    assert run["status"] == BLOCKED
    env.answer(1, "St. Bede belongs to b1.")
    d.poll_issues()
    drive(d)
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW
    reconcile = env.ledger.jobs(run["id"], "reconcile")[0]
    kinds = [a["kind"] for a in env.ledger.all(
        "SELECT kind FROM attempt WHERE job_id = ? ORDER BY n", reconcile["id"])]
    assert kinds == ["start", "answer"]


def test_every_answer_to_a_jobs_run_level_flags_reaches_it(env: Env) -> None:
    def reconciling(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 1:
            return StubAction(handoff={"status": "blocked", "summary": "s", "flags": [
                {"severity": "blocking", "scope": "run", "subject": "testd-map-1",
                 "question": "Two batches claim St. Bede"},
                {"severity": "blocking", "scope": "run", "subject": "testd-map-1",
                 "question": "Is the roster's St. Clare the Lewes one?"}]})
        return StubAction(handoff=done())

    d = env.dispatcher(map_script(reconcile=reconciling))
    drive(d)
    run = map_run(env)
    env.answer(1, "St. Bede belongs to b1.")
    d.poll_issues()
    assert env.ledger.run(run["id"])["status"] == BLOCKED  # the other issue is still open
    env.answer(2, "Yes, Lewes.")
    d.poll_issues()
    drive(d)
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW
    reconcile = env.ledger.jobs(run["id"], "reconcile")[0]
    answer = env.ledger.one("SELECT prompt FROM attempt WHERE job_id = ? AND kind = 'answer'",
                            reconcile["id"])["prompt"]
    assert "St. Bede belongs to b1." in answer and "Yes, Lewes." in answer


def test_a_run_level_flag_raised_again_after_its_answer_is_asked_again(env: Env) -> None:
    flag = {"severity": "blocking", "scope": "run", "subject": "testd-map-1",
            "question": "Two batches claim St. Bede"}

    def reconciling(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt <= 2:
            return StubAction(handoff={"status": "blocked", "summary": "s", "flags": [flag]})
        return StubAction(handoff=done())

    d = env.dispatcher(map_script(reconcile=reconciling))
    drive(d)
    run = map_run(env)
    env.answer(1, "St. Bede belongs to b1.")
    d.poll_issues()
    drive(d)
    # The same question again is a new issue, not a Run blocked with nothing to answer.
    assert env.ledger.run(run["id"])["status"] == BLOCKED
    assert [f["issue_number"] for f in env.ledger.flags(run["id"], "open")] == [2]
    env.answer(2, "Still b1.")
    d.poll_issues()
    drive(d)
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW
    assert len(env.ledger.jobs(run["id"], "reconcile")) == 1


def test_an_answered_job_needs_a_new_handoff(env: Env) -> None:
    def reconciling(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 1:
            return StubAction(handoff={"status": "blocked", "summary": "s", "flags": [{
                "severity": "blocking", "scope": "run", "subject": "testd-map-1",
                "question": "Two batches claim St. Bede"}]})
        if attempt == 2:
            return StubAction()  # ends without writing a handoff
        return StubAction(handoff=done())

    d = env.dispatcher(map_script(reconcile=reconciling))
    drive(d)
    run = map_run(env)
    env.answer(1, "St. Bede belongs to b1.")
    d.poll_issues()
    drive(d)
    reconcile = env.ledger.jobs(run["id"], "reconcile")[0]
    assert reconcile["send_backs"] == 1  # the first handoff didn't count again
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW


def test_an_issue_github_refused_is_opened_on_a_later_poll(env: Env) -> None:
    opened = env.forge.open_issue
    refusals = [1]

    def flaky(title: str, body: str, labels: list[str]) -> int:
        if refusals and refusals.pop():
            raise FactoryError("gh issue: HTTP 502")
        return opened(title, body, labels)

    env.forge.open_issue = flaky  # type: ignore[method-assign]
    env.failing["batches validate"] = 99
    d = env.dispatcher(map_script())
    drive(d)
    run = map_run(env)
    assert run["status"] == BLOCKED
    flag = env.ledger.flags(run["id"], "open")[0]
    assert flag["issue_number"] is None
    d.poll_issues()
    assert env.ledger.flags(run["id"], "open")[0]["issue_number"] == 1


def test_crashes_count_again_once_the_owner_unblocks_the_job(env: Env) -> None:
    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt <= 4:
            return StubAction(outcome="crash")
        return StubAction(files=survey_files(), handoff=done())

    d = env.dispatcher(map_script(survey=surveying))
    drive(d)
    run = map_run(env)
    assert run["status"] == BLOCKED and "crashed 3 times" in run["blocked_reason"]
    env.answer(1, "The SDK is fixed; go again.")
    d.poll_issues()
    drive(d)
    survey = env.ledger.jobs(run["id"], "survey")[0]
    assert survey["status"] == DONE
    attempts = env.ledger.all("SELECT kind, prompt FROM attempt WHERE job_id = ? ORDER BY n",
                              survey["id"])
    assert [a["kind"] for a in attempts] == ["start", "resume", "fresh", "answer", "fresh"]
    # The answer's session couldn't be resumed: the fresh worker gets the whole job input.
    assert attempts[-1]["prompt"].startswith("# Factory job")
    assert "The SDK is fixed" in attempts[-1]["prompt"]


def test_a_failed_worktree_setup_runs_again(env: Env) -> None:
    env.config.setup = ["uv sync"]
    env.failing["uv sync"] = 1
    d = env.dispatcher(map_script())
    drive(d)
    run = map_run(env)
    assert run["status"] == BLOCKED
    env.answer(1, "Fixed the lockfile.")
    d.poll_issues()
    drive(d)
    assert env.commands_run.count("uv sync") == 2
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW


def test_a_failing_backup_does_not_stop_the_dispatcher(env: Env) -> None:
    def backup() -> str:
        raise BlobStoreError("R2 unreachable")

    env.config.backup_hour = 0
    d = env.dispatcher(map_script(), backup=backup)
    drive(d)
    assert env.ledger.run(map_run(env)["id"])["status"] == IN_REVIEW
    assert env.ledger.get("backed_up")  # tried again tomorrow, not every tick


# ── Merging main ─────────────────────────────────────────────────────────────
def test_main_is_merged_at_the_start_of_each_stage(env: Env) -> None:
    d = env.dispatcher(map_script())
    d.tick()  # survey
    env.commit_main({"README.md": "new spec\n"}, "spec change")
    d.tick()  # survey-review: a new stage, so main is merged first
    run = map_run(env)
    assert (Path(run["worktree"]) / "README.md").read_text() == "new spec\n"


def test_a_stage_runs_with_the_spec_main_had_when_it_started(env: Env) -> None:
    d = env.dispatcher(map_script())
    d.tick()  # survey
    spec = env.repo / "factory" / "stages" / "survey-review.yaml"
    text = spec.read_text().replace("max_turns: 80", "max_turns: 7")
    env.commit_main({"factory/stages/survey-review.yaml": text + "reads: [README.md]\n"},
                    "spec change")
    d.tick()  # survey-review: main is merged before its spec is read
    request = env.worker.calls[-1]
    assert request.stage == "survey-review"
    assert request.spec.max_turns == 7 and request.spec.reads == ["README.md"]


def test_a_merge_conflict_blocks_the_run(env: Env) -> None:
    d = env.dispatcher(map_script())
    d.tick()  # the survey writes diocese.md
    env.commit_main({f"data/dioceses/{D}/diocese.md": "conflicting\n"}, "conflict")
    out = d.tick()
    assert out.action == "blocked" and "conflicts in" in out.detail
    assert map_run(env)["status"] == BLOCKED


def test_csv_conflicts_take_mains_version_and_promote_again(env: Env) -> None:
    def promote_then_conflict(req: WorkerRequest, attempt: int) -> StubAction:
        return StubAction(handoff=done())

    d = env.dispatcher(map_script())
    for _ in range(5):  # survey .. reconcile
        d.tick()
    run = map_run(env)
    (Path(run["worktree"]) / "data" / "parishes.csv").write_text("slug\nours\n")
    git(Path(run["worktree"]), "commit", "-qam", "promoted")
    env.commit_main({"data/parishes.csv": "slug\ntheirs\n"}, "another diocese")
    d.tick()  # promote: merges main, conflict in parishes.csv
    assert "diocese promote testd" in " ".join(env.commands_run)
    assert map_run(env)["status"] in (ACTIVE, IN_REVIEW)
    assert "theirs" in (Path(run["worktree"]) / "data" / "parishes.csv").read_text()


# ── Seed Runs ────────────────────────────────────────────────────────────────
def seed_env(env: Env) -> Any:
    env.commit_main({
        f"data/dioceses/{D}/diocese.md": META,
        f"data/dioceses/{D}/batches.json": json.dumps(BATCHES),
        f"data/dioceses/{D}/rosters/directory.json": json.dumps(ROSTER),
        f"data/dioceses/{D}/parishes/st-ann.md": parish_record("directory:1"),
        f"data/dioceses/{D}/parishes/st-clare.md": parish_record("directory:3"),
    }, "mapped")
    (env.repo / "factory" / "queue.json").write_text("[]")
    run_id = env.ledger.add_run(diocese=D, kind=SEED, worktrees_dir=env.config.worktrees_dir,
                                parishes=["st-ann", "st-clare"])
    return env.ledger.run(run_id)


def seed_script(req: WorkerRequest, attempt: int) -> StubAction:
    if req.stage == "seed":
        return StubAction(files={"data/seeds/{parish}.json": seed_file(req.values["parish"])},
                          handoff=done(lessons=["Seed lesson"]))
    if req.stage == "seed-review":
        seeds = []
        for parish in req.values["parishes"].split():
            if parish == "st-ann" and req.job_name == "004-seed-review":
                seeds.append({"parish": parish, "verdict": "send_back",
                              "problems": ["R12 covers s1: settle it"]})
            else:
                seeds.append({"parish": parish, "verdict": "approve", "answers": [{
                    "slot": "s1", "question": "Is the 9:00 Mass weekly?", "choice": 1,
                    "basis": "judgment", "why": "Only printed once."}]})
        return StubAction(handoff=done(seeds=seeds))
    return StubAction(handoff=done())


def test_seed_run_reviews_approves_and_records_decisions(env: Env) -> None:
    run = seed_env(env)
    d = env.dispatcher(seed_script)
    drive(d)
    run = env.ledger.run(run["id"])
    stages = [(j["stage"], json.loads(j["input"]).get("parish") or
               json.loads(j["input"]).get("parishes")) for j in env.ledger.jobs(run["id"])]
    # b2 (st-clare) first, then b1 (st-ann), whose seed is sent back once and re-reviewed.
    assert stages == [("seed", "st-clare"), ("seed-review", ["st-clare"]), ("seed", "st-ann"),
                      ("seed-review", ["st-ann"]), ("seed-review", ["st-ann"]), ("pr", None)]
    wt = Path(run["worktree"])
    for parish in ("st-ann", "st-clare"):
        seed = json.loads((wt / "data" / "seeds" / f"{parish}.json").read_text())
        assert seed["status"] == "approved"
        assert seed["reviewer"].startswith("agent:seed-review@")
    ann = env.ledger.jobs(run["id"], "seed")[1]
    assert ann["send_backs"] == 1
    assert "R12 covers s1" in env.ledger.all(
        "SELECT prompt FROM attempt WHERE job_id = ? ORDER BY n", ann["id"])[1]["prompt"]
    rereview = env.ledger.jobs(run["id"], "seed-review")[-1]
    assert "sent back for: R12 covers s1" in env.ledger.one(
        "SELECT prompt FROM attempt WHERE job_id = ?", rereview["id"])["prompt"]
    decisions = env.ledger.all("SELECT * FROM decision WHERE run_id = ?", run["id"])
    assert {d["parish"] for d in decisions} == {"st-ann", "st-clare"}
    assert all(d["against_lean"] == 1 and d["lean"] == "Include" for d in decisions)
    precedents = playbook.bullets(wt / "data" / "dioceses" / D / "diocese.md",
                                  playbook.PRECEDENTS)
    assert len(precedents) == 2 and "Leave out" in precedents[0]
    # Seed lessons stay in the ledger, out of diocese.md.
    assert not playbook.bullets(wt / "data" / "dioceses" / D / "diocese.md",
                                playbook.NEW_LESSONS)
    pr = next((env.forge.folder / "prs").glob("*.md")).read_text()
    assert "**against the lean**" in pr and "**approved** (2)" in pr
    approve = [c for c in env.commands_run if c.startswith("pnpm seed approve st-ann")][0]
    answers = json.loads((wt / approve.split("--answers ")[1]).read_text())
    assert answers[0]["slot"] == "s1" and answers[0]["choice"] == 1


def test_seed_verdicts_applied_again_keep_their_approvals(env: Env) -> None:
    run = seed_env(env)
    d = env.dispatcher(seed_script)
    drive(d)
    review = env.ledger.jobs(run["id"], "seed-review")[0]  # approved st-clare
    handoff, _ = read_handoff(Path(run["worktree"]) / "scratch" / run["id"] / review["name"]
                              / "handoff.json", "seed-review")
    approvals = len([c for c in env.commands_run if c.startswith("pnpm seed approve")])
    # A resumed review, a retry or a restart applies them again.
    assert d._seed_verdicts(env.ledger.run(run["id"]), review, Path(run["worktree"]),
                            handoff) == ["st-clare"]
    assert len([c for c in env.commands_run if c.startswith("pnpm seed approve")]) == approvals
    clare = env.ledger.jobs(run["id"], "seed")[0]
    assert env.ledger.job(clare["id"])["status"] == DONE
    assert len(env.ledger.all("SELECT * FROM verdict WHERE job_id = ?", review["id"])) == 1
    assert len(env.ledger.all("SELECT * FROM decision WHERE job_id = ?", review["id"])) == 1


def test_seed_review_must_cover_every_parish(env: Env) -> None:
    run = seed_env(env)

    def script(req: WorkerRequest, attempt: int) -> StubAction:
        if req.stage == "seed-review" and attempt == 1:
            return StubAction(handoff=done(seeds=[]))
        return seed_script(req, attempt)

    d = env.dispatcher(script)
    drive(d)
    review = env.ledger.jobs(run["id"], "seed-review")[0]
    assert review["send_backs"] == 1
    gate = env.ledger.one("SELECT * FROM gate WHERE job_id = ? AND name = 'handoff'",
                          review["id"])
    assert gate is not None


def test_a_seed_past_its_send_backs_is_parked(env: Env) -> None:
    env.failing["pnpm seed check st-clare"] = 99
    run = seed_env(env)
    d = env.dispatcher(seed_script)
    drive(d)
    run = env.ledger.run(run["id"])
    parked = env.ledger.parked(run["id"])
    assert [f["subject"] for f in parked] == ["st-clare"]
    assert run["status"] == IN_REVIEW  # st-ann was still seeded and reviewed
    # The parked draft was committed as it stood, so st-ann's job wasn't blamed for it.
    ann = next(j for j in env.ledger.jobs(run["id"], "seed")
               if json.loads(j["input"])["parish"] == "st-ann")
    assert ann["send_backs"] == 0
    wt = Path(run["worktree"])
    assert "seed st-clare, parked" in git(wt, "log", "--format=%s")
    assert not git(wt, "status", "--porcelain")
    # Only approved seeds go to main: the PR leaves the parked draft out.
    assert git(wt, "ls-files", "data/seeds").split() == ["data/seeds/st-ann.json"]
    pr = next((env.forge.folder / "prs").glob("*.md")).read_text()
    assert "st-clare (not approved: left out of this PR)" in pr


def test_seed_review_decides_instead_of_flagging_and_lists_every_decision(env: Env) -> None:
    run = seed_env(env)

    def script(req: WorkerRequest, attempt: int) -> StubAction:
        if req.stage == "seed-review" and req.values["parishes"] == "st-clare" and attempt == 1:
            return StubAction(handoff=done(seeds=[], flags=[{
                "severity": "blocking", "scope": "parish", "subject": "st-clare",
                "question": "Is the 9:00 Mass weekly?"}]))
        if req.stage == "seed-review":
            seeds = [{"parish": p, "verdict": "approve", "answers": [{
                "slot": "s1", "question": "Is the 9:00 Mass weekly?", "choice": 0,
                "basis": "rule" if p == "st-ann" else "judgment",
                "why": "R12" if p == "st-ann" else "Printed every week."}]}
                for p in req.values["parishes"].split()]
            return StubAction(handoff=done(seeds=seeds))
        return seed_script(req, attempt)

    d = env.dispatcher(script)
    drive(d)
    review = env.ledger.jobs(run["id"], "seed-review")[0]
    assert review["send_backs"] == 1 and not env.ledger.parked(run["id"])
    gate = env.ledger.one("SELECT output FROM gate WHERE job_id = ? AND name = 'handoff' "
                          "AND passed = 0", review["id"])
    assert "decides every question" in gate["output"]
    assert not list((env.forge.folder / "issues").glob("*.json"))
    pr = next((env.forge.folder / "prs").glob("*.md")).read_text()
    assert "### By judgment" in pr and "### By a rule the drafter missed" in pr
    assert "`st-ann` s1" in pr and "R12" in pr
    # Only judgments become precedents.
    precedents = playbook.bullets(Path(run["worktree"]) / "data" / "dioceses" / D / "diocese.md",
                                  playbook.PRECEDENTS)
    assert len(precedents) == 1 and "st-clare" in precedents[0]


def test_a_seed_that_parks_itself_is_not_held_to_seed_check(env: Env) -> None:
    env.failing["pnpm seed check st-clare"] = 99  # an unfinished draft fails the check
    run = seed_env(env)

    def script(req: WorkerRequest, attempt: int) -> StubAction:
        if req.stage == "seed" and req.values["parish"] == "st-clare":
            return StubAction(
                files={"data/seeds/{parish}.json": seed_file("st-clare", "drafting")},
                handoff={"status": "blocked", "summary": "s", "flags": [{
                    "severity": "blocking", "scope": "parish", "subject": "st-clare",
                    "question": "The bulletin lists two 9:00 Masses; which church?"}]})
        return seed_script(req, attempt)

    d = env.dispatcher(script)
    drive(d)
    clare = env.ledger.jobs(run["id"], "seed")[0]
    assert clare["status"] == DONE and clare["send_backs"] == 0
    assert [f["subject"] for f in env.ledger.parked(run["id"])] == ["st-clare"]
    assert len(list((env.forge.folder / "issues").glob("*.json"))) == 1


def test_approvals_that_fail_their_check_are_kept_for_the_resumed_review(env: Env) -> None:
    run = seed_env(env)
    d = env.dispatcher(seed_script)
    d.tick()  # st-clare's seed
    env.failing["pnpm seed check st-clare"] = 1  # the approved seed fails its check once
    out = d.tick()  # its review approves it, then the check fails
    assert out.action == "blocked"
    wt = Path(run["worktree"])
    assert "approvals, check failing" in git(wt, "log", "-1", "--format=%s")
    assert not git(wt, "status", "--porcelain")
    env.answer(1, "Fixed the seed by hand.")
    d.poll_issues()
    drive(d)
    review = env.ledger.jobs(run["id"], "seed-review")[0]
    assert env.ledger.job(review["id"])["send_backs"] == 0  # not blamed for the approvals
    assert not env.ledger.all("SELECT * FROM gate WHERE job_id = ? AND name = 'diff-scope' "
                              "AND passed = 0", review["id"])
    seed = json.loads((wt / "data" / "seeds" / "st-clare.json").read_text())
    assert seed["status"] == "approved"
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW


def test_an_approved_seed_is_not_drafted_again(env: Env) -> None:
    env.commit_main({"data/seeds/st-clare.json": seed_file("st-clare", "approved")},
                    "st-clare approved")
    run = seed_env(env)
    d = env.dispatcher(seed_script)
    drive(d)
    parishes = {json.loads(j["input"]).get("parish") for j in env.ledger.jobs(run["id"], "seed")}
    assert parishes == {"st-ann"}


# ── Readiness (§11) ──────────────────────────────────────────────────────────
def make_db(path: Path, counts: dict[str, int]) -> None:
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE parish (id INTEGER PRIMARY KEY, slug TEXT)")
    conn.execute("CREATE TABLE bulletin (id INTEGER PRIMARY KEY, parish_id INT, content_hash TEXT)")
    for i, (slug, n) in enumerate(counts.items(), 1):
        conn.execute("INSERT INTO parish VALUES (?, ?)", (i, slug))
        for k in range(n):
            conn.execute("INSERT INTO bulletin (parish_id, content_hash) VALUES (?, ?)",
                         (i, f"{slug}{k}"))
    conn.commit()
    conn.close()


def merged_map(env: Env, parishes: list[str], merged_at: datetime) -> None:
    """A merged map Run: its records are in main, and its worktree is gone."""
    run_id = env.ledger.add_run(diocese=D, kind=MAP, worktrees_dir=env.tmp / "wt", status=MERGED)
    folder = f"data/dioceses/{D}/parishes"
    env.commit_main({**{f"{folder}/{p}.md": parish_record("directory:1") for p in parishes},
                     f"{folder}/gone.md": "---\nname: Gone\nbulletin_provider: no_bulletin\n---\n"},
                    "mapped")
    env.ledger.set_run(run_id, merged_at=merged_at.isoformat())


def test_readiness_starts_the_first_seed_run_at_80_percent(env: Env) -> None:
    parishes = [f"p{i}" for i in range(10)]
    merged_map(env, parishes, env.now)
    db = env.tmp / "db.sqlite"
    make_db(db, {p: (2 if i < 7 else 1) for i, p in enumerate(parishes)})
    r = readiness.assess(env.ledger, env.config, D, db, env.now, repo=env.repo)
    assert r is not None and r.start == [] and len(r.seedable) == 10  # 70%: not yet
    db.unlink()
    make_db(db, {p: (2 if i < 8 else 0) for i, p in enumerate(parishes)})
    r = readiness.assess(env.ledger, env.config, D, db, env.now, repo=env.repo)
    assert r.start == parishes[:8]


def test_follow_up_seed_run_waits_for_all_or_six_weeks(env: Env) -> None:
    parishes = ["a", "b", "c"]
    merged_map(env, parishes, env.now)
    env.ledger.add_run(diocese=D, kind=SEED, worktrees_dir=env.tmp / "wt", status=MERGED,
                       parishes=["a"])
    db = env.tmp / "db.sqlite"
    make_db(db, {"a": 3, "b": 2, "c": 0})
    r = readiness.assess(env.ledger, env.config, D, db, repo=env.repo,
                         at=env.now + timedelta(weeks=1))
    assert r.start == [] and r.not_ready == ["c"]
    r = readiness.assess(env.ledger, env.config, D, db, repo=env.repo,
                         at=env.now + timedelta(weeks=6, hours=1))
    assert r.start == ["b"] and r.overdue == ["c"]


def test_first_seed_run_starts_after_six_weeks_even_short_of_80_percent(env: Env) -> None:
    parishes = [f"p{i}" for i in range(10)]
    merged_map(env, parishes, env.now)
    db = env.tmp / "db.sqlite"
    make_db(db, {p: (2 if i < 5 else 0) for i, p in enumerate(parishes)})
    r = readiness.assess(env.ledger, env.config, D, db, repo=env.repo,
                         at=env.now + timedelta(weeks=5))
    assert r is not None and r.start == [] and r.overdue == []
    r = readiness.assess(env.ledger, env.config, D, db, repo=env.repo,
                         at=env.now + timedelta(weeks=6, hours=1))
    assert r.start == parishes[:5] and r.overdue == parishes[5:]


def test_check_readiness_creates_a_pending_seed_run_and_overdue_issues(env: Env) -> None:
    merged_map(env, ["a", "b"], env.now - timedelta(weeks=7))
    env.ledger.add_run(diocese=D, kind=SEED, worktrees_dir=env.tmp / "wt", status=MERGED,
                       parishes=[])
    make_db(env.tmp / "parish_events.db", {"a": 2, "b": 0})
    d = env.dispatcher(seed_script)
    d.check_readiness()
    d.check_readiness()
    seed_runs = [r for r in env.ledger.runs(PENDING) if r["kind"] == SEED]
    assert len(seed_runs) == 1 and json.loads(seed_runs[0]["parishes"]) == ["a"]
    assert len(list((env.forge.folder / "issues").glob("*.json"))) == 1


def test_a_parish_waiting_on_a_collector_isnt_seeded_until_its_gap_is_cleared(env: Env) -> None:
    merged_map(env, ["a", "b"], env.now - timedelta(weeks=7))
    path = f"data/dioceses/{D}/parishes/g.md"
    gap = parish_record("directory:1").replace("---\nNotes", GAP + "---\nNotes")
    env.commit_main({path: gap}, "g waits on a collector")
    env.ledger.add_run(diocese=D, kind=SEED, worktrees_dir=env.tmp / "wt", status=MERGED,
                       parishes=[])
    make_db(env.tmp / "parish_events.db", {"a": 2, "b": 2, "g": 0})
    d = env.dispatcher(seed_script)
    d.check_readiness()
    run = next(r for r in env.ledger.runs(PENDING) if r["kind"] == SEED)
    assert json.loads(run["parishes"]) == ["a", "b"]
    assert "1 wait on a collector" in run["notes"]
    assert not list((env.forge.folder / "issues").glob("*.json"))  # g isn't overdue
    env.commit_main({path: parish_record("directory:1")}, "collector landed")
    r = readiness.assess(env.ledger, env.config, D, env.tmp / "parish_events.db", env.now,
                         repo=env.repo)
    assert r is not None and "g" in r.seedable and r.fetch_gaps == []


# ── Units ────────────────────────────────────────────────────────────────────
def test_usage_caps_and_weekly_pacing() -> None:
    config = Config(five_hour_cap=75, weekly_cap=70)
    account = Account("a", Path("/x"))
    resets = datetime(2026, 11, 7, tzinfo=UTC)
    at = resets - timedelta(days=7) + timedelta(hours=1)  # day 0 of the week: cap 10%
    s = standing(account, Usage(10, at + timedelta(hours=2), 9, resets), config, at)
    assert s.eligible and s.weekly_allowed == pytest.approx(10)
    s = standing(account, Usage(10, at + timedelta(hours=2), 11, resets), config, at)
    assert not s.eligible and s.eligible_at == resets - timedelta(days=6)  # tomorrow
    s = standing(account, Usage(80, at + timedelta(hours=2), 1, resets), config, at)
    assert not s.eligible and s.eligible_at == at + timedelta(hours=2)
    late = resets - timedelta(hours=1)  # day 6: the full cap
    s = standing(account, Usage(0, late, 71, resets), config, late)
    assert not s.eligible and s.eligible_at == resets
    rows = [standing(Account(n, Path("/x")), Usage(u, late, 10, resets), config, late)
            for n, u in (("a", 50), ("b", 20))]
    assert choose(rows).account.name == "b"
    assert choose(rows, only="a").account.name == "a"


def test_choose_prefers_the_account_resetting_soonest() -> None:
    config = Config(five_hour_cap=75, weekly_cap=100)
    at = datetime(2026, 11, 5, tzinfo=UTC)

    def row(name: str, five: float, week: float, resets_in: timedelta) -> Standing:
        return standing(Account(name, Path("/x")), Usage(five, at + timedelta(hours=2), week,
                                                         at + resets_in), config, at)

    # "b" has less headroom but resets first: its unused allowance would be lost.
    rows = [row("a", 0, 10, timedelta(days=3)), row("b", 60, 50, timedelta(hours=6))]
    assert choose(rows).account.name == "b"
    # An account over its caps is skipped however soon it resets.
    rows = [row("a", 0, 10, timedelta(days=3)), row("b", 80, 50, timedelta(hours=6))]
    assert choose(rows).account.name == "a"
    assert choose(rows, only="b") is None


@pytest.mark.parametrize("source", ["defaults", "repository"])
@pytest.mark.parametrize("day", range(1, 8))
def test_full_weekly_budget_is_paced_across_all_seven_days(
    source: str, day: int, tmp_path: Path,
) -> None:
    config = Config() if source == "defaults" else load_config(local_path=tmp_path / "absent.yaml")
    account = Account("a", Path("/x"))
    resets = datetime(2026, 11, 7, 3, 30, tzinfo=UTC)
    start = resets - timedelta(days=7)
    at = start + timedelta(days=day - 1)
    allowed = 100 * day / 7

    s = standing(account, Usage(0, at + timedelta(hours=5), allowed - 0.01, resets), config, at)
    assert s.weekly_allowed == pytest.approx(allowed)
    assert s.eligible

    s = standing(account, Usage(0, at + timedelta(hours=5), allowed, resets), config, at)
    assert not s.eligible
    assert s.eligible_at == start + timedelta(days=day)

    if day > 1:
        # The new allowance becomes available exactly at the account's day boundary.
        before = at - timedelta(microseconds=1)
        s = standing(account, Usage(0, at + timedelta(hours=5), allowed - 0.01, resets),
                     config, before)
        assert not s.eligible
        assert s.eligible_at == at


def test_an_unused_usage_window_has_no_reset_time() -> None:
    at = datetime(2026, 11, 2, tzinfo=UTC)
    usage = parse_usage({"five_hour": {"utilization": 0, "resets_at": None},
                         "seven_day": {"utilization": None, "resets_at": None}}, at)
    assert usage.five_hour == 0 and usage.five_hour_resets == at + timedelta(hours=5)
    assert usage.seven_day_resets == at + timedelta(days=7)
    assert standing(Account("a", Path("/x")), usage, Config(), at).eligible


def test_a_job_that_waited_on_usage_merges_main_first(env: Env) -> None:
    env.config.accounts = [Account("a", Path("/x"))]
    week = env.now + timedelta(days=3)
    usage = {"five_hour": 90.0}
    d = env.dispatcher(map_script(), fetch_usage=lambda a: Usage(
        usage["five_hour"], env.now + timedelta(hours=1), 1, week))
    assert d.tick().action == "waiting"  # the survey, before its first attempt
    env.commit_main({"README.md": "new spec\n"}, "spec change")
    usage["five_hour"] = 1.0
    env.now += timedelta(hours=2)
    assert d.tick().action == "ran"
    assert (Path(map_run(env)["worktree"]) / "README.md").read_text() == "new spec\n"


def test_a_usage_limit_without_a_session_keeps_what_the_job_was_told(env: Env) -> None:
    class NoSession(StubWorker):
        """A worker whose session never started (the CLI died before its first message)."""

        def run(self, request: WorkerRequest) -> WorkerResult:
            result = super().run(request)
            result.session_id = None
            return result

    def surveying(req: WorkerRequest, attempt: int) -> StubAction:
        if attempt == 2:
            return StubAction(outcome=USAGE, resets_at=env.now + timedelta(hours=1))
        return StubAction(files=survey_files(), handoff=done())

    env.failing["diocese validate"] = 1  # attempt 1 is sent back
    d = env.dispatcher(map_script(survey=surveying))
    d.worker = env.worker = NoSession(map_script(survey=surveying))
    drive(d)
    env.now += timedelta(hours=2)
    drive(d)
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    prompts = [a["prompt"] for a in env.ledger.all(
        "SELECT prompt FROM attempt WHERE job_id = ? ORDER BY n", survey["id"])]
    assert len(prompts) == 3 and "failed on purpose" in prompts[2]


def test_accounts_out_of_headroom_wait(env: Env) -> None:
    env.config.accounts = [Account("a", Path("/x"))]
    resets = env.now + timedelta(hours=3)
    d = env.dispatcher(map_script(),
                       fetch_usage=lambda a: Usage(90, resets, 1, env.now + timedelta(days=3)))
    out = d.tick()
    assert out.action == "waiting" and out.wait_until == resets
    env.ledger.set("override_caps", True)
    assert d.tick().action == "ran"


def test_playbook_appends_once_under_its_heading(tmp_path: Path) -> None:
    meta = tmp_path / "diocese.md"
    meta.write_text(META)
    assert playbook.append(meta, playbook.NEW_LESSONS, ["A  lesson", "B"]) == ["A lesson", "B"]
    assert playbook.append(meta, playbook.NEW_LESSONS, ["B", "C"]) == ["C"]
    assert playbook.bullets(meta, playbook.NEW_LESSONS) == ["A lesson", "B", "C"]
    text = meta.read_text()
    assert text.index("## New lessons") < text.index("## Rules settled")
    playbook.append(meta, playbook.PRECEDENTS, ["P"])
    assert text.index("## Log") > 0 and meta.read_text().index("## Seeding precedents") \
        < meta.read_text().index("## Log")
    # Bulletin publishers' bullet stays put.
    assert playbook.bullets(meta, playbook.PUBLISHERS) == ["Parishes Online prints most bulletins."]


def test_handoff_validation(tmp_path: Path) -> None:
    path = tmp_path / "h.json"
    path.write_text(json.dumps({"status": "done", "summary": "s", "extra": 1}))
    assert read_handoff(path, "map")[1]
    path.write_text(json.dumps({"status": "blocked", "summary": "s"}))
    assert "blocking flag" in read_handoff(path, "map")[1][0]
    path.write_text(json.dumps({"status": "done", "summary": "s", "verdict": "send_back"}))
    assert "problems" in read_handoff(path, "survey-review")[1][0]
    path.write_text(json.dumps({"status": "done", "summary": "s", "seeds": [
        {"parish": "p", "verdict": "approve", "answers": [
            {"slot": "s1", "choice": "edited", "basis": "judgment", "why": "w"}]}]}))
    assert "edited needs an entry" in read_handoff(path, "seed-review")[1][0]
    path.write_text(json.dumps({"status": "done", "summary": "s", "seeds": [
        {"parish": "p", "verdict": "approve", "answers": [
            {"slot": "s1", "choice": 0, "basis": "rule", "why": "w"}]}]}))
    assert not read_handoff(path, "seed-review")[1]  # a rule-covered question is answered
    path.write_text(json.dumps({"status": "blocked", "summary": "s", "seeds": [], "flags": [{
        "severity": "blocking", "scope": "parish", "subject": "p", "question": "q"}]}))
    assert "decides every question" in read_handoff(path, "seed-review")[1][0]
    path.write_text(json.dumps({"status": "done", "summary": "s", "settled": [
        {"flag": 1, "how": "merged"}, {"flag": 1, "how": "again"}]}))
    assert "settle each flag once" in read_handoff(path, "reconcile")[1][0]
    path.write_text(json.dumps({"status": "done", "summary": "s", "settled": [
        {"flag": 1, "how": "merged"}]}))
    assert not read_handoff(path, "reconcile")[1]
    assert read_handoff(path, "map")[1]  # only reconcile settles flags


def test_runs_take_their_branch_prefix(tmp_path: Path) -> None:
    ledger = Ledger(tmp_path / "ledger.db")
    stub = ledger.add_run(diocese=D, kind=MAP, worktrees_dir=tmp_path,
                          branch_prefix="factory-stub/")
    assert ledger.run(stub)["branch"] == f"factory-stub/{D}-map-1"
    real = ledger.add_run(diocese=D, kind=SEED, worktrees_dir=tmp_path)
    assert ledger.run(real)["branch"] == f"factory/{D}-seed-1"


def test_write_globs() -> None:
    globs = ["data/dioceses/testd/**", "data/seeds/st-ann.json"]
    assert in_scope("data/dioceses/testd/parishes/a.md", globs)
    assert in_scope("data/seeds/st-ann.json", globs)
    assert not in_scope("data/seeds/st-bede.json", globs)
    assert not in_scope("data/dioceses/other/diocese.md", globs)
    assert not in_scope("data/parishes.csv", globs)


def test_stage_specs_load_and_cover_every_stage() -> None:
    from pdf_extract.factory.stages import STAGES, load_stage

    for stage in STAGES:
        spec = load_stage(stage, ROOT)
        if spec.is_agent:
            assert (ROOT / spec.prompt).exists(), spec.prompt
            assert spec.writes and spec.model


def test_stage_specs_accept_reads_and_deny(tmp_path: Path) -> None:
    from pdf_extract.factory.stages import load_stage

    (tmp_path / "factory" / "stages").mkdir(parents=True)
    spec = (ROOT / "factory" / "stages" / "map.yaml").read_text()
    (tmp_path / "factory" / "stages" / "map.yaml").write_text(
        spec + "reads: [data/dioceses/README.md#Fields]\ndeny: [Bash(pnpm seed extract:*)]\n")
    loaded = load_stage("map", tmp_path)
    assert loaded.reads == ["data/dioceses/README.md#Fields"]
    assert loaded.deny == ["Bash(pnpm seed extract:*)"]
    assert load_stage("map", ROOT).reads == [] and load_stage("map", ROOT).deny == []


def test_the_committed_config_is_the_defaults(tmp_path: Path) -> None:
    assert load_config(ROOT / "factory" / "config.yaml", tmp_path / "none.yaml") == Config()


def test_inspect_shows_attempts_gates_and_reviews(env: Env) -> None:
    env.failing["diocese validate"] = 1
    d = env.dispatcher(map_script())
    drive(d)
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    r = report.inspect(env.ledger, report.find_job(env.ledger, f"{D}-map-1/001-survey"),
                       env.tmp / "runs")
    assert r["job"] == survey["id"] and len(r["attempts"]) == 2
    assert any(not g["passed"] for g in r["gates"])
    assert r["reviewed_by"][0]["verdict"] == "approve"
    assert "send_back" in report.text_inspect(r)
    assert report.cost(env.ledger, by_stage=True)["rows"]
    assert "testd-map-1" in report.text_status(report.status(env.ledger))


def test_stub_worker_ok_constant() -> None:
    assert OK == "ok"


# ── Quota: attribution, tokens, readings, backfill ───────────────────────────
T0 = datetime(2026, 11, 2, 12, tzinfo=UTC)
FIVE_RESETS = T0 + timedelta(hours=4)
WEEK_RESETS = T0 + timedelta(days=3)
SETTLE = timedelta(seconds=150)


def reading(rid: int, minutes: float, five: float, week: float = 20, *,
            five_resets: datetime = FIVE_RESETS, account: str = "a") -> Reading:
    return Reading(rid, account, T0 + timedelta(minutes=minutes),
                   {"five_hour": five, "seven_day": week},
                   {"five_hour": five_resets, "seven_day": WEEK_RESETS})


def span(sid: int, start: float, end: float | None, account: str = "a") -> Span:
    return Span(sid, sid, account, T0 + timedelta(minutes=start),
                None if end is None else T0 + timedelta(minutes=end))


def test_back_to_back_attempts_share_their_measurement() -> None:
    # B starts 5 s after A ends, and the meter rises during B: no exact share for either.
    spans = [span(1, 0, 10), span(2, 10.1, 20)]
    reads = [reading(1, -0.01, 10), reading(2, 10.05, 12), reading(3, 24, 21)]
    an = Analysis(spans, reads, SETTLE)
    a, b = an.measure(spans[0], "five_hour"), an.measure(spans[1], "five_hour")
    assert a.label == b.label == SHARED and a.group == b.group == [1, 2]
    assert (a.group_low, a.group_high) == (10, 12)  # 21 - 10 ± 1, settled
    assert a.low == 1 and a.high == 12  # A's early reading: at least 12 - 10 - 1
    assert b.low == 0 and b.high == 12
    # One job running both: the group's upper bound counts once, not once per attempt.
    job = combine([a, b])
    assert (job["label"], job["low"], job["high"]) == (SHARED, 1, 12)
    totals = {(w["window"]): w for w in an.window_totals()}
    assert totals["five_hour"]["shared"] == 11 and totals["five_hour"]["unexplained"] == 10


def test_an_idle_gap_gives_a_settled_range_and_zero_is_below_one() -> None:
    spans = [span(1, 0, 10)]
    an = Analysis(spans, [reading(1, 0, 10, 20), reading(2, 13, 15, 20)], SETTLE)
    five, week = an.measure(spans[0], "five_hour"), an.measure(spans[0], "seven_day")
    assert (five.label, five.low, five.high) == (SETTLED, 4, 6)
    assert (week.label, week.low, week.high) == (SETTLED, 0, 1) and week.as_dict()["text"] == "<1"
    # Read sooner than the meter settles: a minimum only.
    early = Analysis(spans, [reading(1, 0, 10), reading(2, 10.5, 15)], SETTLE)
    m = early.measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high) == (IMMEDIATE, 4, None)
    assert combine([m])["text"] == "≥4"


def test_a_reset_during_a_job_is_a_minimum_and_jitter_is_not_a_reset() -> None:
    spans = [span(1, 0, 10)]
    before = reading(1, 0, 70, five_resets=T0 + timedelta(minutes=5))
    after = reading(2, 13, 4, five_resets=T0 + timedelta(hours=5, minutes=5))
    m = Analysis(spans, [before, after], SETTLE).measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high) == (RESET, 3, None)
    jitter = reading(2, 13, 72, five_resets=FIVE_RESETS + timedelta(seconds=0.6))
    m = Analysis(spans, [reading(1, 0, 70), jitter], SETTLE).measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high) == (SETTLED, 1, 3)


def test_missing_or_inconsistent_readings_give_no_number() -> None:
    spans = [span(1, 0, 10)]
    for reads in ([reading(2, 13, 15)], [reading(1, 0, 10)]):
        m = Analysis(spans, reads, SETTLE).measure(spans[0], "five_hour")
        assert m.label == MISSING and m.low is None and m.high is None
    fell = Analysis(spans, [reading(1, 0, 10), reading(2, 13, 8)], SETTLE)
    m = fell.measure(spans[0], "five_hour")
    assert m.label == INCONSISTENT and m.low is None
    assert combine([m])["low"] is None


def test_a_meter_rising_while_idle_flags_nearby_attempts() -> None:
    spans = [span(1, 0, 10)]
    reads = [reading(1, -60, 5), reading(2, -30, 9), reading(3, 0, 9), reading(4, 13, 12)]
    an = Analysis(spans, reads, SETTLE)
    assert an.measure(spans[0], "five_hour").outside_use
    assert an.rises[0]["points"] == 4
    quiet = Analysis(spans, [reading(1, -60, 9), reading(3, 0, 9), reading(4, 13, 12)], SETTLE)
    assert not quiet.measure(spans[0], "five_hour").outside_use


def test_historical_readings_are_a_minimum_at_best() -> None:
    spans = [span(1, 0, 10)]
    reads = [reading(1, 0, 10), reading(2, 13, 15)]
    m = Analysis(spans, reads, SETTLE, approximate={1}).measure(spans[0], "five_hour")
    assert (m.label, m.low, m.high, m.approximate) == (IMMEDIATE, 4, None, True)


def assistant(mid: str, at: str, model: str = "claude-opus-5-5", out: int = 100,
              thinking: int = 40, five: int = 0, hour: int = 50) -> str:
    return json.dumps({"type": "assistant", "timestamp": at, "version": "2.1.310",
                       "entrypoint": "sdk-py", "sessionId": "s1", "message": {
                           "id": mid, "model": model, "usage": {
                               "input_tokens": 3, "output_tokens": out,
                               "output_tokens_details": {"thinking_tokens": thinking},
                               "cache_read_input_tokens": 1000,
                               "cache_creation_input_tokens": five + hour,
                               "cache_creation": {"ephemeral_5m_input_tokens": five,
                                                  "ephemeral_1h_input_tokens": hour}}}})


def cost_state(start: datetime) -> str:
    return json.dumps({"type": "cost-state", "startTime": start.timestamp() * 1000,
                       "modelUsage": {"claude-haiku-5-5": {
                           "inputTokens": 2000, "outputTokens": 20, "thinkingTokens": 0,
                           "cacheReadInputTokens": 0, "cacheCreationInputTokens": 0}}})


TRANSCRIPT = [
    # Attempt 1 (12:00): m1 recorded three times, m2 once, and its cost-state.
    assistant("m1", "2026-11-02T12:00:05Z"), assistant("m1", "2026-11-02T12:00:05Z"),
    assistant("m1", "2026-11-02T12:00:06Z"), assistant("m2", "2026-11-02T12:01:00Z", five=7),
    cost_state(T0), "not json",
    # Attempt 2 (13:00), resuming the session in the same file.
    assistant("m3", "2026-11-02T13:00:05Z", out=10, thinking=0, hour=0),
    assistant("m3", "2026-11-02T13:00:05Z", out=10, thinking=0, hour=0),
]


def test_transcript_tokens_count_each_message_once() -> None:
    first = parse_transcript(TRANSCRIPT, since=T0)
    assert first.messages == 3 and first.duplicates == 3  # m1, m2, m3
    one = parse_transcript(TRANSCRIPT[:6], since=T0)
    assert (one.messages, one.duplicates) == (2, 2)
    assert one.output == 200 + 20 and one.thinking == 80  # thinking not added to output
    assert (one.cache_write_5m, one.cache_write_1h) == (7, 100)
    assert one.per_model["claude-haiku-5-5"]["input"] == 2000  # the side call
    assert one.input == 6 + 2000 and one.model == "claude-opus-5-5"
    assert one.cli_version == "2.1.310" and one.entrypoint == "sdk-py"
    # The resumed attempt counts only its own messages, by time or by ids already counted.
    later = parse_transcript(TRANSCRIPT, since=T0 + timedelta(hours=1))
    assert (later.messages, later.output, later.cache_write_1h) == (1, 10, 0)
    assert "claude-haiku-5-5" not in later.per_model  # attempt 1's cost-state
    again = parse_transcript(TRANSCRIPT, seen=one.message_ids)
    assert again.messages == 1 and again.per_model["claude-opus-5-5"]["output"] == 10


def test_result_tokens_keep_the_cache_ttl_and_side_models() -> None:
    t = from_result(
        {"input_tokens": 5, "output_tokens": 90, "cache_creation_input_tokens": 30,
         "cache_creation": {"ephemeral_5m_input_tokens": 10, "ephemeral_1h_input_tokens": 20},
         "output_tokens_details": {"thinking_tokens": 40}},
        {"claude-opus-5-5": {"inputTokens": 5, "outputTokens": 90,
                             "cacheCreationInputTokens": 30, "cacheReadInputTokens": 9},
         "claude-haiku-5-5": {"inputTokens": 100, "outputTokens": 2}})
    assert (t.output, t.thinking, t.cache_write_5m, t.cache_write_1h) == (92, 40, 10, 20)
    assert t.input == 105 and t.model == "claude-opus-5-5" and not t.gaps


def test_raw_usage_is_kept_without_credentials(tmp_path: Path) -> None:
    body = {"five_hour": {"utilization": 22, "resets_at": "2026-11-02T16:00:00Z"},
            "seven_day": {"utilization": 28, "resets_at": "2026-11-05T16:00:00Z"},
            "seven_day_opus": {"utilization": 3, "resets_at": None},
            "extra_usage": {"is_enabled": False, "access_token": "tok-123"},
            "Authorization": "Bearer abc", "note": "Bearer xyz"}
    usage = parse_usage(body)
    ledger = Ledger(tmp_path / "l.db")
    ledger.add_usage("a", T0.isoformat(), usage, "periodic")
    raw = ledger.one("SELECT raw FROM usage")["raw"]
    assert "seven_day_opus" in raw and "is_enabled" in raw
    assert "tok-123" not in raw and "abc" not in raw and "xyz" not in raw
    # The plan: the login's, else local.yaml's.
    login = tmp_path / "acct"
    login.mkdir()
    (login / ".credentials.json").write_text(json.dumps({"claudeAiOauth": {
        "accessToken": "secret", "subscriptionType": "pro", "rateLimitTier": "default_pro"}}))
    assert account_plan(Account("a", login)) == "pro/default_pro"
    assert account_plan(Account("b", tmp_path / "none", "max")) == "max"
    local = tmp_path / "local.yaml"
    local.write_text("accounts: [{name: a, config_dir: /x, plan: pro}]\n"
                     "calibration_gap_seconds: 200\n")
    config = load_config(tmp_path / "missing.yaml", local)
    assert config.accounts[0].plan == "pro" and config.calibration_gap_seconds == 200
    assert config.quota_settle_seconds == 150


def test_an_old_ledger_gains_the_quota_columns(tmp_path: Path) -> None:
    path = tmp_path / "old.db"
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE usage (id INTEGER PRIMARY KEY, account TEXT NOT NULL, at TEXT "
                 "NOT NULL, five_hour REAL, five_hour_resets TEXT, seven_day REAL, "
                 "seven_day_resets TEXT)")
    conn.execute("INSERT INTO usage (account, at, five_hour) VALUES ('a', 'x', 1)")
    conn.commit()
    conn.close()
    ledger = Ledger(path)
    row = ledger.one("SELECT * FROM usage")
    assert row["source"] == "select" and row["attempt_id"] is None and row["raw"] is None
    Ledger(path)  # opening it again changes nothing
    assert ledger.one("SELECT COUNT(*) AS n FROM attempt_meta")["n"] == 0


class Meter:
    """A fake usage endpoint whose meter the stub workers move."""

    def __init__(self) -> None:
        self.five, self.week, self.fail = 10.0, 20.0, 0
        self.status: int | None = None  # the HTTP status a failing call reports
        self.calls = 0

    def __call__(self, account: Account) -> Usage:
        self.calls += 1
        if self.fail:
            self.fail -= 1
            raise UsageError("endpoint down", status=self.status)
        return Usage(self.five, FIVE_RESETS, self.week, WEEK_RESETS,
                     raw={"five_hour": {"utilization": self.five}})


def metered(env: Env, gap: int = 0) -> tuple[Meter, Callable[..., Any]]:
    env.config.accounts = [Account("a", env.tmp / "acct", "pro")]
    env.config.calibration_gap_seconds = gap
    meter = Meter()

    def spend(points: float, minutes: float, then: StubAction, fail: int = 0):
        def stage(req: WorkerRequest, attempt: int) -> StubAction:
            meter.five += points
            env.now += timedelta(minutes=minutes)
            meter.fail = fail
            return then
        return stage
    return meter, spend


def quota_of(env: Env, attempt_id: int, window: str = "five_hour") -> Measure:
    an, spans = report.analysis(env.ledger)
    return an.measure(spans[attempt_id], window)


def test_readings_before_after_and_settled_are_linked_to_attempts(env: Env) -> None:
    meter, spend = metered(env)
    survey = StubAction(files=survey_files(), handoff=done("surveyed"), rate_limits=[{
        "type": "five_hour", "status": "allowed_warning", "utilization": 0.81,
        "resets_at": FIVE_RESETS.isoformat(), "raw": {"surpassedThreshold": 0.8}}],
        usage={"output_tokens": 50, "output_tokens_details": {"thinking_tokens": 20}},
        model_usage={"claude-opus-5-5": {"inputTokens": 3, "outputTokens": 50}})
    review = StubAction(handoff=done(verdict="approve"))
    d = env.dispatcher(map_script(survey=spend(5, 10, survey),
                                  **{"survey-review": spend(3, 2, review)}), fetch_usage=meter)
    seen = drive(d)
    assert not any(s.startswith("waiting") for s in seen)  # no gap: nothing waits
    rows = env.ledger.all("SELECT * FROM usage WHERE attempt_id IS NOT NULL ORDER BY id")
    assert [(r["attempt_id"], r["source"]) for r in rows][:3] == [
        (1, "before"), (1, "after"), (2, "before")]
    assert rows[0]["five_hour"] == 10 and rows[1]["five_hour"] == 15
    assert rows[2]["at"] == rows[1]["at"]  # the next job started at once
    first, second = quota_of(env, 1), quota_of(env, 2)
    assert first.label == second.label == SHARED and 1 in first.group and 2 in first.group
    env.now += timedelta(seconds=200)
    d.tick()
    last = env.ledger.one("SELECT MAX(id) AS id FROM attempt")["id"]
    settled = env.ledger.all("SELECT * FROM usage WHERE source = 'settled'")
    assert [r["attempt_id"] for r in settled] == [last]
    d.tick()
    assert len(env.ledger.all("SELECT * FROM usage WHERE source = 'settled'")) == 1
    first = quota_of(env, 1)
    assert (first.group_low, first.group_high) == (7, 9) and first.low == 4
    meta = report.attempt_meta(env.ledger, 1)
    assert meta["requested_model"] and meta["effort"] and meta["config_hash"]
    assert (meta["output_tokens"], meta["thinking_tokens"], meta["plan"]) == (50, 20, "pro")
    assert meta["work_units"] == 1 and meta["source"] == "live"
    r = report.inspect(env.ledger, report.find_job(env.ledger, f"{D}-map-1/001-survey"),
                       env.tmp / "runs")
    a = r["attempts"][0]
    assert a["rate_limits"]["events"] == 1 and a["rate_limits"]["last_utilization"] == 0.81
    assert a["quota"]["five_hour"]["label"] == SHARED
    text = report.text_inspect(r)
    assert "shared" in text and "utilization 0.81" in text and "before #" in text
    maps = [m for m in env.ledger.jobs(map_run(env)["id"], "map")]
    units = [report.attempt_meta(env.ledger, env.ledger.one(
        "SELECT id FROM attempt WHERE job_id = ?", m["id"])["id"])["work_units"] for m in maps]
    assert units == [1, 2]  # b2 (first_batch) has one entry, b1 two
    q = report.quota(env.ledger)
    row = next(x for x in q["rows"] if x["key"] == "survey")
    assert row["five_hour"]["samples"] == 0 and row["five_hour"]["uncertain"]["jobs"] == 1
    assert "diagnostic" in report.text_quota(q)
    assert report.quota(env.ledger, by="model", tz="America/New_York")["rows"]
    assert "5h shared" in report.text_recent(report.recent(env.ledger, "survey", 5))
    w = report.windows(env.ledger)
    assert any(x["window"] == "five_hour" and x["shared"] == 8 for x in w["windows"])


def test_a_calibration_gap_holds_the_next_job_for_a_settled_reading(env: Env) -> None:
    meter, spend = metered(env, gap=200)
    survey = StubAction(files=survey_files(), handoff=done("surveyed"))
    d = env.dispatcher(map_script(survey=spend(5, 10, survey)), fetch_usage=meter)
    out = drive(d)
    assert out[-1].startswith("waiting: calibration gap")
    assert len(env.ledger.all("SELECT * FROM attempt")) == 1
    env.now += timedelta(seconds=100)
    assert d.tick().action == "waiting"
    env.now += timedelta(seconds=100)
    assert d.tick().action == "ran"  # the settled reading first, then the next job
    settled = env.ledger.one("SELECT * FROM usage WHERE source = 'settled'")
    assert settled["attempt_id"] == 1 and settled["five_hour"] == 15
    m = quota_of(env, 1)
    assert (m.label, m.low, m.high) == (SETTLED, 4, 6)
    q = report.quota(env.ledger)
    row = next(x for x in q["rows"] if x["key"] == "survey")
    assert row["five_hour"]["samples"] == 1 and row["five_hour"]["per_unit"]["median"] == 5


def test_a_failed_after_reading_does_not_stop_the_job(env: Env) -> None:
    meter, spend = metered(env)
    survey = StubAction(files=survey_files(), handoff=done("surveyed"))
    d = env.dispatcher(map_script(survey=spend(5, 10, survey, fail=1)), fetch_usage=meter)
    assert d.tick().action == "ran"
    assert env.ledger.get("paused") is None
    assert env.ledger.jobs(map_run(env)["id"], "survey")[0]["status"] == DONE
    assert not env.ledger.all("SELECT * FROM usage WHERE source = 'after'")
    assert quota_of(env, 1).label in (SHARED, MISSING)


def failing_usage_check(env: Env, status: int, fail: int = 1) -> Meter:
    """An endpoint failing the next job's usage check (the periodic reading already taken)."""
    meter, _ = metered(env)
    meter.fail, meter.status = fail, status
    env.ledger.set("quota_sampled", env.now.isoformat())
    return meter


COOLDOWN = timedelta(minutes=Config().usage_cooldown_minutes)


def test_a_usage_check_429_cools_down_then_retries_and_resumes(env: Env) -> None:
    meter = failing_usage_check(env, 429, 2)
    d = env.dispatcher(map_script(), fetch_usage=meter)
    first = d.tick()
    assert first.action == "waiting" and "cooldown" in first.detail
    assert first.wait_until == env.now + COOLDOWN
    assert env.ledger.get("paused") is None
    since = env.ledger.get("usage_cooldown")["since"]
    status = report.text_status(report.status(env.ledger))
    assert "USAGE CHECK COOLDOWN: usage check failed: endpoint down" in status
    assert f"next retry {first.wait_until.isoformat()[:16]}" in status
    # Nothing reads the endpoint during the cooldown.
    calls = meter.calls
    env.now += timedelta(minutes=29)
    assert d.tick().action == "waiting"
    assert meter.calls == calls
    # After 30 minutes it tries again; another 429 waits another 30 minutes.
    env.now += timedelta(minutes=1)
    second = d.tick()
    assert second.action == "waiting" and meter.calls == calls + 1
    assert second.wait_until == env.now + COOLDOWN
    assert env.ledger.get("usage_cooldown")["since"] == since
    assert env.ledger.jobs(map_run(env)["id"], "survey")[0]["status"] != DONE
    # The next check succeeds: the cooldown clears and queued work resumes.
    env.now = second.wait_until
    assert d.tick().action == "ran"
    assert env.ledger.get("usage_cooldown") is None
    assert env.ledger.jobs(map_run(env)["id"], "survey")[0]["status"] == DONE
    assert "COOLDOWN" not in report.text_status(report.status(env.ledger))


def test_after_a_usage_check_cooldown_the_caps_still_hold(env: Env) -> None:
    meter = failing_usage_check(env, 429, 1)
    d = env.dispatcher(map_script(), fetch_usage=meter)
    assert d.tick().action == "waiting"
    meter.five = env.config.five_hour_cap + 5  # over the 5-hour cap once it answers
    env.now += COOLDOWN
    out = d.tick()
    assert out.action == "waiting" and "no account under its caps" in out.detail
    assert env.ledger.get("usage_cooldown") is None
    survey = env.ledger.jobs(map_run(env)["id"], "survey")[0]
    assert survey["status"] == WAITING_USAGE and not env.ledger.all("SELECT * FROM attempt")


def test_a_cooldown_never_lifts_the_owners_pause(env: Env) -> None:
    meter = failing_usage_check(env, 429, 1)
    d = env.dispatcher(map_script(), fetch_usage=meter)
    assert d.tick().action == "waiting"
    env.ledger.set("paused", {"reason": "paused by the owner", "at": "now"})
    env.now += COOLDOWN * 3
    calls = meter.calls
    out = d.tick()
    assert (out.action, out.detail) == ("paused", "paused by the owner")
    assert meter.calls == calls
    assert env.ledger.get("paused")["reason"] == "paused by the owner"


def test_resume_retries_the_usage_check_at_once(env: Env,
                                               monkeypatch: pytest.MonkeyPatch) -> None:
    import argparse

    from pdf_extract.factory import cli

    meter = failing_usage_check(env, 429)
    d = env.dispatcher(map_script(), fetch_usage=meter)
    assert d.tick().action == "waiting"
    monkeypatch.setattr(cli, "_ledger", lambda args: env.ledger)
    cli._resume(argparse.Namespace(override_caps=False))
    assert env.ledger.get("usage_cooldown") is None
    assert d.tick().action == "ran"


def test_other_usage_check_failures_still_pause(env: Env) -> None:
    meter = failing_usage_check(env, 500, 1)
    d = env.dispatcher(map_script(), fetch_usage=meter)
    assert d.tick().action == "paused"
    env.now += COOLDOWN * 3
    assert d.tick().action == "paused"
    assert env.ledger.get("usage_cooldown") is None
    assert "endpoint down" in env.ledger.get("paused")["reason"]


def test_fetch_usage_reports_the_http_status(tmp_path: Path,
                                            monkeypatch: pytest.MonkeyPatch) -> None:
    import urllib.error

    from pdf_extract.factory import usage as usage_mod

    def too_many(request: Any, timeout: int) -> Any:
        raise urllib.error.HTTPError(usage_mod.USAGE_URL, 429, "Too Many Requests", {}, None)

    monkeypatch.setattr(usage_mod, "_token", lambda account: "t")
    monkeypatch.setattr(usage_mod.urllib.request, "urlopen", too_many)
    with pytest.raises(UsageError) as caught:
        usage_mod.fetch_usage(Account("second", tmp_path, "pro"))
    assert caught.value.status == 429
    assert str(caught.value) == ("second: usage endpoint failed: HTTP Error 429: "
                                 "Too Many Requests")


def test_backfill_recovers_tokens_and_lists_gaps(tmp_path: Path) -> None:
    ledger = Ledger(tmp_path / "factory.db")
    run_id = ledger.add_run(diocese=D, kind=MAP, worktrees_dir=tmp_path)
    job = ledger.add_job(run_id, "map", {"batch": "b1"})
    ledger.set_job(job, status=DONE, account="a")
    rel = "data/factory/runs/x/003-map/s1.jsonl"
    (tmp_path / rel).parent.mkdir(parents=True)
    (tmp_path / rel).write_text("\n".join(TRANSCRIPT[:6]) + "\n")
    attempt = ledger.add_attempt(job, "start", "p", "a", "abc", at=T0.isoformat())
    ledger.finish_attempt(attempt, outcome="ok", session_id="s1", transcript=rel,
                          finished_at=(T0 + timedelta(minutes=10)).isoformat())
    ledger.add_step(attempt, 1, "rate_limit", "five_hour", "allowed")
    for minutes, five in ((-0.01, 10), (10.2, 14), (20, 16)):
        ledger.add_usage("a", (T0 + timedelta(minutes=minutes)).isoformat(),
                         Usage(five, FIVE_RESETS, 20, WEEK_RESETS), "select")
    files = {"abc:factory/stages/map.yaml": "stage: map\nmodel: claude-sonnet-5-5\neffort: "
             "high\nprompt: factory/prompts/map.md\nskills: [explore-diocese]\n",
             "abc:factory/prompts/map.md": "Map.",
             f"abc:data/dioceses/{D}/batches.json": json.dumps(BATCHES)}
    config = Config(accounts=[Account("a", tmp_path / "acct", "pro")])
    r = backfill(ledger, config, files.get, root=tmp_path)
    assert len(r["attempts"]) == 1 and r["linked"] == 2
    meta = report.attempt_meta(ledger, attempt)
    assert meta["source"] == "backfill" and meta["approximate"] == 1
    assert (meta["requested_model"], meta["effort"]) == ("claude-sonnet-5-5", "high")
    assert meta["output_tokens"] == 220 and meta["messages"] == 2
    assert meta["duplicate_records"] == 2 and meta["work_units"] == 2
    assert meta["cli_version"] == "2.1.310" and meta["config_hash"]
    gaps = " ".join(meta["gaps"])
    assert "SDK version" in gaps and "rate-limit events" in gaps and "plan read" in gaps
    assert "no settled reading" not in gaps  # the reading at 20 min came after idling
    sources = [r["source"] for r in ledger.all("SELECT source FROM usage ORDER BY id")]
    assert sources == ["before", "after", "select"]
    # Never settled from historical readings: a minimum, marked approximate.
    m = Analysis([Span.from_row(ledger.one("SELECT * FROM attempt"))],
                 [Reading.from_row(x) for x in ledger.all("SELECT * FROM usage")], SETTLE,
                 approximate={attempt}).measure(span(attempt, 0, 10), "five_hour")
    assert (m.label, m.low, m.high) == (IMMEDIATE, 5, None)
    again = backfill(ledger, config, files.get, root=tmp_path)
    assert again == {"attempts": [], "linked": 0}
    # Without its spec or transcript, it says so.
    other = ledger.add_attempt(job, "resume", "p", "a", "zzz", at=T0.isoformat())
    ledger.finish_attempt(other, outcome="crash", finished_at=T0.isoformat())
    backfill(ledger, config, files.get, root=tmp_path)
    gaps = " ".join(report.attempt_meta(ledger, other)["gaps"])
    assert "no transcript" in gaps and "stage spec" in gaps


def test_backfill_gives_a_resumed_session_each_attempt_its_own_tokens(tmp_path: Path) -> None:
    ledger = Ledger(tmp_path / "factory.db")
    run_id = ledger.add_run(diocese=D, kind=MAP, worktrees_dir=tmp_path)
    job = ledger.add_job(run_id, "survey", {})
    rel = "s1.jsonl"
    (tmp_path / rel).write_text("\n".join(TRANSCRIPT) + "\n")
    ids = []
    for kind, start in (("start", T0), ("resume", T0 + timedelta(hours=1))):
        a = ledger.add_attempt(job, kind, "p", "a", None, at=start.isoformat())
        ledger.finish_attempt(a, outcome="ok", session_id="s1", transcript=rel,
                              finished_at=(start + timedelta(minutes=10)).isoformat())
        ids.append(a)
    backfill(ledger, Config(accounts=[Account("a", tmp_path / "acct")]), {}.get, root=tmp_path)
    first, second = (report.attempt_meta(ledger, a) for a in ids)
    assert (first["messages"], first["output_tokens"]) == (2, 220)  # m1, m2 only
    assert (second["messages"], second["output_tokens"]) == (1, 10)  # m3
    assert second["resumed_from"] == ids[0]


def test_a_calibration_gap_ends_the_wait_when_the_other_account_is_over_its_caps(
        env: Env) -> None:
    meter, spend = metered(env, gap=200)
    env.config.accounts.append(Account("b", env.tmp / "acct-b"))

    def fetch(account: Account) -> Usage:
        return meter(account) if account.name == "a" else Usage(
            99, FIVE_RESETS, 20, WEEK_RESETS)
    survey = StubAction(files=survey_files(), handoff=done("surveyed"))
    d = env.dispatcher(map_script(survey=spend(5, 10, survey)), fetch_usage=fetch)
    assert drive(d)[-1].startswith("waiting")
    waiting = env.ledger.one("SELECT wait_until FROM job WHERE status = ?", WAITING_USAGE)
    finished = env.ledger.one("SELECT finished_at FROM attempt WHERE id = 1")["finished_at"]
    # Account a is free once its gap ends, long before b's five-hour window resets.
    assert datetime.fromisoformat(waiting["wait_until"]) == \
        datetime.fromisoformat(finished) + timedelta(seconds=200)


def test_rate_limit_events_are_scrubbed_and_never_stop_the_attempt(
        env: Env, monkeypatch: pytest.MonkeyPatch) -> None:
    meter, spend = metered(env)
    event = {"type": "five_hour", "status": "allowed_warning", "utilization": 0.9,
             "raw": {"access_token": "tok-123", "surpassedThreshold": 0.8}}
    survey = StubAction(files=survey_files(), handoff=done("surveyed"),
                        rate_limits=[event, event])
    d = env.dispatcher(map_script(survey=spend(5, 10, survey)), fetch_usage=meter)
    real = env.ledger.add_rate_limit_event
    calls = []

    def flaky(*args: Any, **kwargs: Any) -> None:
        calls.append(1)
        if len(calls) == 1:
            raise sqlite3.OperationalError("database is locked")
        real(*args, **kwargs)
    monkeypatch.setattr(env.ledger, "add_rate_limit_event", flaky)
    assert d.tick().action == "ran"
    assert env.ledger.one("SELECT outcome FROM attempt WHERE id = 1")["outcome"] == OK
    rows = env.ledger.all("SELECT raw FROM rate_limit_event")
    assert len(rows) == 1 and "tok-123" not in rows[0]["raw"]
    assert "surpassedThreshold" in rows[0]["raw"]


def test_a_slow_after_reading_does_not_hold_up_the_gates(
        env: Env, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(dispatcher_mod, "AFTER_READING_WAIT", 0.2)
    meter, spend = metered(env)
    release = threading.Event()

    def slow(account: Account) -> Usage:
        if threading.current_thread() is not threading.main_thread():  # the after reading
            release.wait(5)
        return meter(account)
    survey = StubAction(files=survey_files(), handoff=done("surveyed"))
    d = env.dispatcher(map_script(survey=spend(5, 10, survey)), fetch_usage=slow)
    started = time.monotonic()
    assert d.tick().action == "ran"
    assert time.monotonic() - started < 3
    release.set()
    assert env.ledger.jobs(map_run(env)["id"], "survey")[0]["status"] == DONE
    assert not env.ledger.all("SELECT * FROM usage WHERE source = 'after'")


def test_an_unknown_time_zone_is_a_clear_error(tmp_path: Path) -> None:
    with pytest.raises(FactoryError, match="unknown time zone 'US/Eastrn'"):
        report.quota(Ledger(tmp_path / "l.db"), by="hour", tz="US/Eastrn")
