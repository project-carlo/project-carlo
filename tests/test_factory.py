"""The onboarding factory's dispatcher, end to end with stub workers (docs/factory-spec.md).

Each test builds a git repo with a bare `origin`, so worktrees, commits, pushes and
merges are real. Workers are stubs, GitHub is files (`LocalForge`), and the commands a
gate runs are faked.
"""

from __future__ import annotations

import json
import shutil
import sqlite3
import subprocess
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.factory import forge as forge_mod
from pdf_extract.factory import playbook, readiness, report
from pdf_extract.factory.config import Account, Config
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
from pdf_extract.factory.stages import in_scope
from pdf_extract.factory.usage import Usage, choose, standing
from pdf_extract.factory.workers import OK, USAGE, StubAction, StubWorker, WorkerRequest

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
    shutil.copytree(ROOT / ".claude" / "agents", e.repo / ".claude" / "agents")
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
    drive(d)
    follow = env.ledger.run(follow["id"])
    assert [j["stage"] for j in env.ledger.jobs(follow["id"])] == ["map", "promote", "pr"]
    assert follow["status"] == IN_REVIEW
    first = env.ledger.one("SELECT * FROM attempt a JOIN job j ON j.id = a.job_id "
                           "WHERE j.run_id = ?", follow["id"])
    # Another worktree can't resume the old session: a fresh worker gets the answer.
    assert first["kind"] == "start" and "It is open; map it." in first["prompt"]


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


# ── Merging main ─────────────────────────────────────────────────────────────
def test_main_is_merged_at_the_start_of_each_stage(env: Env) -> None:
    d = env.dispatcher(map_script())
    d.tick()  # survey
    env.commit_main({"README.md": "new spec\n"}, "spec change")
    d.tick()  # survey-review: a new stage, so main is merged first
    run = map_run(env)
    assert (Path(run["worktree"]) / "README.md").read_text() == "new spec\n"


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
    assert "data/seeds/st-clare.json" in git(wt, "ls-files", "data/seeds")
    assert "seed st-clare, parked" in git(wt, "log", "--format=%s")
    assert not git(wt, "status", "--porcelain")


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
    run_id = env.ledger.add_run(diocese=D, kind=MAP, worktrees_dir=env.tmp / "wt", status=MERGED)
    folder = env.tmp / "wt" / run_id / "data" / "dioceses" / D / "parishes"
    folder.mkdir(parents=True)
    for p in parishes:
        (folder / f"{p}.md").write_text(parish_record("directory:1"))
    (folder / "gone.md").write_text("---\nname: Gone\nbulletin_provider: no_bulletin\n---\n")
    env.ledger.set_run(run_id, merged_at=merged_at.isoformat())


def test_readiness_starts_the_first_seed_run_at_80_percent(env: Env) -> None:
    parishes = [f"p{i}" for i in range(10)]
    merged_map(env, parishes, env.now)
    db = env.tmp / "db.sqlite"
    make_db(db, {p: (2 if i < 7 else 1) for i, p in enumerate(parishes)})
    r = readiness.assess(env.ledger, env.config, D, db, env.now)
    assert r is not None and r.start == [] and len(r.seedable) == 10  # 70%: not yet
    db.unlink()
    make_db(db, {p: (2 if i < 8 else 0) for i, p in enumerate(parishes)})
    r = readiness.assess(env.ledger, env.config, D, db, env.now)
    assert r.start == parishes[:8]


def test_follow_up_seed_run_waits_for_all_or_six_weeks(env: Env) -> None:
    parishes = ["a", "b", "c"]
    merged_map(env, parishes, env.now)
    env.ledger.add_run(diocese=D, kind=SEED, worktrees_dir=env.tmp / "wt", status=MERGED,
                       parishes=["a"])
    db = env.tmp / "db.sqlite"
    make_db(db, {"a": 3, "b": 2, "c": 0})
    r = readiness.assess(env.ledger, env.config, D, db, env.now + timedelta(weeks=1))
    assert r.start == [] and r.not_ready == ["c"]
    r = readiness.assess(env.ledger, env.config, D, db, env.now + timedelta(weeks=6, hours=1))
    assert r.start == ["b"] and r.overdue == ["c"]


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
    assert read_handoff(path, "seed-review")[1]  # a rule-covered question is a send-back


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
