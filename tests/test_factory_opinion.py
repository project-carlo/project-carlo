"""The dispatcher's second opinion on each seed (docs/seed-second-opinion-plan.md, Phase 2):
asked in the background when a seed Run starts, revealed once a seed's gates pass, and
the differences sent back to the drafter as their own attempt. luna is a fake."""

from __future__ import annotations

import json
import shutil
import sqlite3
from concurrent.futures import Executor, Future
from datetime import timedelta
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.factory import report
from pdf_extract.factory.backup import backup_ledger
from pdf_extract.factory.ledger import DONE, IN_REVIEW, SEED, SENT_BACK, Ledger
from pdf_extract.factory.metrics import report as metrics
from pdf_extract.factory.opinions import ASKING, FAILED, Opinions
from pdf_extract.factory.workers import StubAction, WorkerRequest
from pdf_extract.labeling.demo import build_demo
from pdf_extract.seeding import second_opinion as so
from tests.test_factory import (
    BATCHES,
    META,
    ROSTER,
    D,
    Env,
    church_record,
    done,
    drive,
    git,
    parish_record,
)
from tests.test_factory import env as factory_env  # noqa: F401
from tests.test_seed_second_opinion import HF, NEW, OLD, PARISH, FakeCaller, reply, weekly

MARKER = "src/pdf_extract/seeding/second_opinion.py"


@pytest.fixture
def env(request: pytest.FixtureRequest) -> Env:
    return request.getfixturevalue("factory_env")


class Inline(Executor):
    """Runs each call as it is submitted, so a test needn't wait for threads."""

    def submit(self, fn, /, *args, **kwargs):  # type: ignore[override]
        future: Future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except BaseException as exc:  # pragma: no cover
            future.set_exception(exc)
        return future


class Held(Executor):
    """Keeps each call until `release`: one still in flight."""

    def __init__(self) -> None:
        self.held: list[Any] = []

    def submit(self, fn, /, *args, **kwargs):  # type: ignore[override]
        self.held.append((fn, args, kwargs))
        return Future()

    def release(self) -> None:
        while self.held:
            fn, args, kwargs = self.held.pop(0)
            fn(*args, **kwargs)


def opinion_run(env: Env, *, marker: bool = True) -> Any:
    """A seed Run of the demo parish, with the demo database as the dispatcher's."""
    demo = build_demo(env.tmp / "demo")
    shutil.copy(demo["db_path"], env.tmp / "parish_events.db")
    files = {
        f"data/dioceses/{D}/diocese.md": META,
        f"data/dioceses/{D}/batches.json": json.dumps(BATCHES),
        f"data/dioceses/{D}/rosters/directory.json": json.dumps(ROSTER),
        f"data/dioceses/{D}/parishes/{PARISH}.md": parish_record(),
        f"data/dioceses/{D}/churches/{PARISH}.md": church_record(PARISH, "directory:3"),
    }
    if marker:
        files[MARKER] = "# the Run's seed CLI reads a second opinion\n"
    files[".gitignore"] = "scratch/\ndata/factory/\ndata/*.db\n"  # as the repo's own
    env.commit_main(files, "mapped")
    (env.repo / "factory" / "queue.json").write_text("[]")
    env.demo_seed = (demo["seeds_dir"] / f"{PARISH}.json").read_text()  # type: ignore[attr-defined]
    run_id = env.ledger.add_run(diocese=D, kind=SEED, worktrees_dir=env.config.worktrees_dir,
                                parishes=[PARISH])
    return env.ledger.run(run_id)


def opinions(env: Env, caller: FakeCaller, executor: Executor | None = None,
             stored=lambda parish, h: True) -> Opinions:
    return Opinions(env.ledger, env.config, db_path=env.tmp / "parish_events.db",
                    caller=lambda: caller, read_pdf=lambda parish, h: b"%PDF-" + h.encode(),
                    stored=stored, executor=executor or Inline())


def seed_path(run: Any) -> Path:
    return Path(run["worktree"]) / "data" / "seeds" / f"{PARISH}.json"


def draft(env: Env, resolve=None):
    """The drafter: writes the demo seed, and answers an opinion prompt with `resolve`."""
    def script(req: WorkerRequest, attempt: int) -> StubAction:
        if req.stage == "seed":
            path = req.worktree / "data" / "seeds" / f"{PARISH}.json"
            if attempt == 1:
                return StubAction(files={f"data/seeds/{PARISH}.json": env.demo_seed},
                                  handoff=done("drafted"))
            seed = json.loads(path.read_text())
            if resolve is not None:
                seed = resolve(seed)
            return StubAction(files={f"data/seeds/{PARISH}.json": json.dumps(seed, indent=2)},
                              handoff=done("resolved"))
        if req.stage == "seed-review":
            return StubAction(handoff=done(seeds=[
                {"parish": p, "verdict": "approve"} for p in req.values["parishes"].split()]))
        return StubAction(handoff=done())
    return script


def keep_all(seed: dict[str, Any]) -> dict[str, Any]:
    for d in so.unresolved(seed):
        seed = so.keep(seed, d["id"], [{"source": "agent", "bulletin": NEW[:8], "page": 2,
                                        "said": "Tue-Fri 8:00 AM"}],
                       "R1: the newest schedule box prints 8:00.")
    return seed


def to_830(seed: dict[str, Any]) -> dict[str, Any]:
    for s in seed["slots"]:
        if s["id"] in ("s12", "s13", "s14", "s15"):
            s["entry"]["start_time"] = "08:30"
    return so.refresh(seed)


def rows(env: Env) -> list[sqlite3.Row]:
    return env.ledger.all("SELECT * FROM seed_opinion ORDER BY id")


def seed_job(env: Env, run: Any) -> Any:
    return env.ledger.jobs(run["id"], "seed")[0]


def pr_text(env: Env) -> str:
    return next((env.forge.folder / "prs").glob("*.md")).read_text()


# ── The ledger ──────────────────────────────────────────────────────────────
def test_an_old_ledger_gains_the_seed_opinion_table(tmp_path: Path) -> None:
    path = tmp_path / "old.db"
    Ledger(path).close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE seed_opinion")
    conn.commit()
    conn.close()
    ledger = Ledger(path)
    cols = {r["name"] for r in ledger.all("PRAGMA table_info(seed_opinion)")}
    assert {"run_id", "parish", "status", "request_key", "reply", "cost_usd", "revealed_at",
            "entries_sha256", "drafter_newest", "stats"} <= cols


# ── Asking ──────────────────────────────────────────────────────────────────
def test_a_seed_run_asks_once_per_parish_and_reuses_a_stored_reply(env: Env) -> None:
    run = opinion_run(env)
    caller = FakeCaller(reply())
    held = Held()
    ops = opinions(env, caller, held)
    d = env.dispatcher(draft(env), opinions=ops)
    d.engine.pick()  # the Run's first pick fires its parishes' calls
    d.engine.pick()
    [row] = rows(env)
    assert row["parish"] == PARISH and row["status"] == "queued" and len(held.held) == 1
    held.release()  # in the background
    [row] = rows(env)
    assert row["status"] == DONE and len(caller.calls) == 1 and row["cost_usd"] > 0
    assert [b["content_hash"] for b in json.loads(row["bulletins"])] == [NEW, OLD]
    assert row["today"] == "2026-09-25" and row["request_key"] and row["revealed_at"] is None
    # Another request for the same bulletins, churches and day takes the stored reply.
    again = ops.ask(run["id"], PARISH, json.loads(env.demo_seed),
                    {"content_hash": NEW, "fetched_at": "2026-09-25T21:00:00Z"})
    held.release()
    again = ops.row(again["id"])
    assert again["status"] == DONE and again["reused_from"] == row["id"]
    assert again["cost_usd"] == 0 and len(caller.calls) == 1


def test_a_call_cut_off_by_a_restart_is_asked_again_once(env: Env) -> None:
    run = opinion_run(env)
    caller = FakeCaller(reply())
    ops = opinions(env, caller, Held())
    env.dispatcher(draft(env), opinions=ops).engine.pick()
    [row] = rows(env)
    # The dispatcher stopped mid-call: a new one finds the row asking.
    env.ledger.run_sql("UPDATE seed_opinion SET status = ?, attempts = 1 WHERE id = ?",
                       ASKING, row["id"])
    restarted = opinions(env, caller)
    restarted.fire(env.ledger.run(run["id"]))
    assert restarted.row(row["id"])["status"] == DONE and len(caller.calls) == 1
    env.ledger.run_sql("UPDATE seed_opinion SET status = ?, attempts = 2, reply = NULL "
                       "WHERE id = ?", ASKING, row["id"])
    opinions(env, caller).fire(env.ledger.run(run["id"]))
    assert ops.row(row["id"])["status"] == FAILED and len(caller.calls) == 1


# ── Reveal ──────────────────────────────────────────────────────────────────
def test_no_differences_go_on_to_commit(env: Env) -> None:
    run = opinion_run(env)
    d = env.dispatcher(draft(env), opinions=opinions(env, FakeCaller(reply(weekday="08:00"))))
    drive(d)
    job = seed_job(env, run)
    assert job["status"] == DONE and job["send_backs"] == 0
    assert [a["kind"] for a in env.ledger.all("SELECT kind FROM attempt WHERE job_id = ?",
                                              job["id"])] == ["start"]
    seed = json.loads(seed_path(run).read_text())
    assert seed["second_opinion"]["differences"] == []
    assert any(s["source"] == "c1" for s in seed["slots"][0]["sources"])
    [row] = rows(env)
    assert row["revealed_at"] and row["job_id"] == job["id"]
    assert row["entries_sha256"] == seed["second_opinion"]["entries_sha256"]
    assert json.loads(row["stats"])["differences"] == 0
    # The seed's commit has it: the reviewer sees what the second reader read.
    wt = Path(run["worktree"])
    sha = git(wt, "log", "--format=%H", "--grep=: seed b2 (", "-1").strip()
    committed = json.loads(git(wt, "show", f"{sha}:data/seeds/{PARISH}.json"))
    assert committed["status"] == "needs_review" and "second_opinion" in committed


def test_differences_go_back_to_the_same_session_and_are_no_send_back(env: Env) -> None:
    env.config.max_send_backs = 0  # an opinion attempt doesn't spend one
    run = opinion_run(env)
    d = env.dispatcher(draft(env, keep_all),
                       opinions=opinions(env, FakeCaller(reply(weekday="08:30"))))
    gate_envs: list[tuple[str, dict[str, str]]] = []

    def commands(command: str, cwd: Path, secrets: dict[str, str] | None = None):
        gate_envs.append((command, dict(secrets or {})))
        return env.commands(command, cwd, secrets)

    d.engine.commands = commands
    outcome = d.tick()
    assert "differences from the second opinion" in outcome.detail
    job = seed_job(env, run)
    assert job["status"] == SENT_BACK and job["send_backs"] == 0
    assert json.loads(job["pending_prompt"])["kind"] == "opinion"
    drive(d)
    job = env.ledger.job(job["id"])
    attempts = env.ledger.all("SELECT * FROM attempt WHERE job_id = ? ORDER BY n", job["id"])
    assert [a["kind"] for a in attempts] == ["start", "opinion"]
    assert attempts[1]["session_id"] == attempts[0]["session_id"]
    prompt = attempts[1]["prompt"]
    assert "second reader, not an authority" in prompt and "d1 differs: start time" in prompt
    assert "“Tue-Fri 8:30 AM”" in prompt and f"pnpm seed opinion keep {PARISH}" in prompt
    assert job["status"] == DONE and job["send_backs"] == 0
    # Its gates ran again on what it handed back, with the hash the dispatcher kept.
    checks = [g for g in env.ledger.all("SELECT * FROM gate WHERE job_id = ?", job["id"])
              if g["name"].startswith("pnpm seed check")]
    assert len(checks) == 2
    seed = json.loads(seed_path(run).read_text())
    sha = seed["second_opinion"]["entries_sha256"]
    seed_checks = [e for c, e in gate_envs if c.startswith("pnpm seed check")][:2]
    assert so.OPINION_SHA_ENV not in seed_checks[0]  # nothing revealed yet
    assert seed_checks[1][so.OPINION_SHA_ENV] == f"{PARISH}={sha}"
    st = json.loads(rows(env)[0]["stats"])
    assert st["kept"] == 1 and st["unresolved"] == 0


def test_a_newer_bulletin_the_drafter_read_is_asked_about_again(env: Env) -> None:
    run = opinion_run(env)
    caller = FakeCaller(reply(weekday="08:00"))
    # When the Run started, the newest bulletin's PDF wasn't stored yet.
    late = {NEW}
    ops = opinions(env, caller, stored=lambda parish, h: h not in late)
    d = env.dispatcher(draft(env), opinions=ops)
    d.engine.pick()
    [first] = rows(env)
    assert first["status"] == "skipped"  # one bulletin: too few
    late.clear()
    env.ledger.run_sql("UPDATE seed_opinion SET status = 'done', bulletins = ?, reply = ? "
                       "WHERE id = ?", json.dumps([{"content_hash": OLD,
                                                    "fetched_at": "2026-09-18T21:00:00Z",
                                                    "published_date": "2026-09-20"}]),
                       json.dumps({"text": reply()}), first["id"])
    drive(d)
    second = rows(env)[-1]
    assert len(rows(env)) == 2 and second["drafter_newest"] == NEW and len(caller.calls) == 1
    assert [b["content_hash"] for b in json.loads(second["bulletins"])] == [NEW, OLD]
    assert second["revealed_at"] and rows(env)[0]["revealed_at"] is None
    seed = json.loads(seed_path(run).read_text())
    assert seed["second_opinion"]["bulletins"][0]["content_hash"] == NEW
    assert seed_job(env, run)["status"] == DONE


def test_luna_unreachable_goes_on_without_it_and_the_pr_says_so(env: Env) -> None:
    run = opinion_run(env)
    caller = FakeCaller(error=ConnectionError("api.openai.com unreachable"))
    d = env.dispatcher(draft(env), opinions=opinions(env, caller))
    drive(d)
    assert seed_job(env, run)["status"] == DONE
    # Asked at the Run's start, then once more on the drafter's bulletins.
    assert [r["status"] for r in rows(env)] == [FAILED, FAILED] and len(caller.calls) == 2
    assert "second_opinion" not in json.loads(seed_path(run).read_text())
    assert env.ledger.run(run["id"])["status"] == IN_REVIEW
    pr = pr_text(env)
    assert "## Second opinion" in pr and "### Seeds without a second opinion" in pr
    assert f"`{PARISH}`: ConnectionError: api.openai.com unreachable" in pr


def test_a_slow_opinion_is_waited_for_then_gone_without(env: Env) -> None:
    run = opinion_run(env)
    held = Held()
    d = env.dispatcher(draft(env), opinions=opinions(env, FakeCaller(reply()), held))
    outcome = d.tick()
    assert outcome.action == "waiting" and "second opinion" in outcome.detail
    job = seed_job(env, run)
    assert env.ledger.job(job["id"])["status"] == "gating"
    gates = len(env.ledger.all("SELECT * FROM gate WHERE job_id = ?", job["id"]))
    assert d.tick().action == "waiting"
    # Waiting doesn't run the gates again.
    assert len(env.ledger.all("SELECT * FROM gate WHERE job_id = ?", job["id"])) == gates
    env.now += timedelta(minutes=env.config.opinion_timeout_minutes + 1)
    drive(d)
    assert env.ledger.job(job["id"])["status"] == DONE
    assert "second_opinion" not in json.loads(seed_path(run).read_text())
    assert "no reply within 20 minutes" in pr_text(env)


def test_a_run_whose_checkout_predates_it_gets_none(env: Env) -> None:
    run = opinion_run(env, marker=False)
    caller = FakeCaller(reply(weekday="08:30"))
    d = env.dispatcher(draft(env), opinions=opinions(env, caller))
    drive(d)
    assert seed_job(env, run)["status"] == DONE and not rows(env) and not caller.calls
    assert "second_opinion" not in json.loads(seed_path(run).read_text())
    assert "## Second opinion" not in pr_text(env)


# ── End to end ──────────────────────────────────────────────────────────────
def test_reveal_opinion_resolution_review_and_the_pr(env: Env) -> None:
    run = opinion_run(env)
    caller = FakeCaller(reply(weekday="08:30", extra_masses=[
        weekly(HF, "Sunday", "12:00", quote="Sunday Noon Mass")]))

    def resolve(seed: dict[str, Any]) -> dict[str, Any]:
        # Changes the weekday Masses as the bulletin shows; keeps its Sundays.
        return keep_all(to_830(seed))

    ops = opinions(env, caller)
    d = env.dispatcher(draft(env, resolve), opinions=ops)
    drive(d)
    run = env.ledger.run(run["id"])
    assert run["status"] == IN_REVIEW and len(caller.calls) == 1
    job = seed_job(env, run)
    assert job["status"] == DONE and job["send_backs"] == 0
    seed = json.loads(seed_path(run).read_text())
    assert seed["status"] == "approved"
    hows = sorted((d["kind"], d["resolution"]["how"])
                  for d in seed["second_opinion"]["differences"])
    assert hows == [("differs", "changed"), ("missing", "kept")]
    pr = pr_text(env)
    assert "| parishes | compared | differences | changed | asked | kept | cost |" in pr
    assert "| 1 | 1 | 2 | 1 | 0 | 1 | $" in pr
    assert "### Kept against the second opinion" in pr
    assert f"`{PARISH}` d2 (missing): gpt-6-luna read mass Sun 12:00" in pr
    assert "**Kept:** dbb914e7 p2 “Tue-Fri 8:00 AM”. R1:" in pr
    # Foremen see it per job and per stage.
    inspected = report.text_inspect(report.inspect(env.ledger, job, env.tmp / "runs"))
    assert f"second opinion {PARISH}: done, 2 bulletins" in inspected
    assert "2 differences: 1 changed, 0 asked, 1 kept, 0 open" in inspected
    recent = metrics.recent(env.ledger, "seed", 5)
    assert recent["opinion"]["kept_share"] == 0.5 and recent["opinion"]["changed_share"] == 0.5
    assert "changed 50%, asked 0%, kept 50%" in metrics.text_recent(recent)


# ── Hidden until revealed ───────────────────────────────────────────────────
def test_the_backup_leaves_out_replies_not_yet_revealed(env: Env) -> None:
    run = opinion_run(env)
    ops = opinions(env, FakeCaller(reply()))
    env.dispatcher(draft(env), opinions=ops).engine.pick()
    env.ledger.run_sql("INSERT INTO seed_opinion (run_id, parish, status, reply, revealed_at, "
                       "created_at) VALUES (?, 'other', 'done', '{\"text\": \"shown\"}', "
                       "'2026-11-01', '2026-11-01')", run["id"])
    out = backup_ledger(env.ledger.path, "factory/backups/", {}, out_dir=env.tmp / "backups")
    copy = sqlite3.connect(out.split(" ")[0])
    got = copy.execute("SELECT parish, status, reply FROM seed_opinion ORDER BY id").fetchall()
    assert got == [(PARISH, "queued", None), ("other", "done", '{"text": "shown"}')]
    raw = Path(out.split(" ")[0]).read_bytes()
    assert b"Sat 4:00 PM Vigil" not in raw  # not left in a free page either
    copy.close()
    assert rows(env)[0]["reply"] is not None  # the ledger itself keeps it


@pytest.mark.parametrize("stage", ["seed"])
def test_the_seed_prompt_still_renders(env: Env, stage: str) -> None:
    run = opinion_run(env)
    preview = report.preview(env.ledger, stage, run["id"], repo=env.repo,
                             lessons_before_integrate=15)
    assert preview["kind"] == "start" and f"seed `{PARISH}`" in preview["first_message"]
