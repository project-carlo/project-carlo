"""`python -m pdf_extract factory ...` (`pnpm factory ...`): the onboarding factory.

  status                       Runs, the running job, usage, what waits on you
  queue                        the dioceses waiting for a map Run (factory/queue.json)
  run [--once] [--stub FILE]   the dispatcher; --stub plays canned workers, with issues
                               and PRs as files under data/factory/stub/ and no pushes
  pause [REASON]               stop starting jobs (the running one finishes)
  resume [--override-caps]     start again; --override-caps ignores the usage caps
  retry <job>                  run a blocked or failed job again from where it stopped
  inspect <job> [--prompt]     everything about a job, for a foreman review
  inspect --stage S [--last N] a stage's recent jobs
  cost [--stage]               cost by Run, or by stage
  backup                       back the ledger up to R2 now

A job is its number or `<run>/<name>` (`wilmington-map-1/004-map`). Run it from the
dispatcher's own checkout; see docs/factory-spec.md.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pdf_extract.factory import report
from pdf_extract.factory.backup import backup_ledger
from pdf_extract.factory.config import (
    DATA,
    LEDGER_PATH,
    RUNS_DIR,
    FactoryError,
    load_config,
)
from pdf_extract.factory.ledger import (
    ACTIVE,
    BLOCKED,
    FAILED,
    JOB_BLOCKED,
    OPEN,
    QUEUED,
    SETTLED,
    Ledger,
    now,
)

Result = dict[str, Any]


def _ledger() -> Ledger:
    return Ledger(LEDGER_PATH)


def _status(args: argparse.Namespace) -> Result:
    return report.status(_ledger())


def _queue(args: argparse.Namespace) -> Result:
    from pdf_extract.factory.dispatcher import main_queue

    return report.queue(_ledger(), main_queue(_repo(), load_config().upstream))


def _pause(args: argparse.Namespace) -> Result:
    ledger = _ledger()
    ledger.set("paused", {"reason": args.reason or "paused by the owner", "at": now()})
    ledger.set("override_caps", False)
    return {"paused": True}


def _resume(args: argparse.Namespace) -> Result:
    ledger = _ledger()
    ledger.set("paused", None)
    ledger.set("override_caps", bool(args.override_caps))
    return {"paused": False, "override_caps": bool(args.override_caps)}


def _retry(args: argparse.Namespace) -> Result:
    ledger = _ledger()
    try:
        job = report.find_job(ledger, args.job)
    except KeyError:
        raise FactoryError(f"no job {args.job}") from None
    if job["status"] not in (JOB_BLOCKED, FAILED):
        raise FactoryError(f"job {job['id']} is {job['status']}; only blocked or failed jobs "
                           "are retried")
    ledger.clear_actions(job["id"])
    ledger.set_job(job["id"], status=QUEUED, send_backs=0, continues=0, finished_at=None,
                   pending_prompt=json.dumps({"kind": "resume", "prompt": None}))
    for flag in ledger.all("SELECT * FROM flag WHERE job_id = ? AND status = ?", job["id"], OPEN):
        ledger.run_sql("UPDATE flag SET status = ?, answer = ? WHERE id = ?", SETTLED,
                       "retried by the owner", flag["id"])
    run = ledger.run(job["run_id"])
    if run["status"] == BLOCKED and not [f for f in ledger.flags(run["id"], OPEN)
                                         if f["scope"] == "run"]:
        ledger.set_run(run["id"], status=ACTIVE, blocked_reason=None)
    return {"job": job["id"], "status": QUEUED, "run": run["id"]}


def _inspect(args: argparse.Namespace) -> Result:
    ledger = _ledger()
    if args.stage:
        args.render = report.text_recent
        return report.recent(ledger, args.stage, args.last)
    if not args.job:
        raise FactoryError("name a job, or --stage")
    try:
        job = report.find_job(ledger, args.job)
    except KeyError:
        raise FactoryError(f"no job {args.job}") from None
    if args.prompt:
        first = ledger.one("SELECT prompt FROM attempt WHERE job_id = ? ORDER BY n LIMIT 1",
                           job["id"])
        args.render = lambda r: r["prompt"]
        return {"prompt": first["prompt"] if first else None}
    return report.inspect(ledger, job, RUNS_DIR)


def _cost(args: argparse.Namespace) -> Result:
    return report.cost(_ledger(), args.stage)


def _backup(args: argparse.Namespace) -> Result:
    return {"backup": backup_ledger(LEDGER_PATH, load_config().backup_prefix)}


def _repo() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if out.returncode != 0:
        raise FactoryError("run the dispatcher from its git checkout")
    return Path(out.stdout.strip())


def _run(args: argparse.Namespace) -> Result:
    from pdf_extract.factory import forge
    from pdf_extract.factory.dispatcher import Dispatcher, run_command
    from pdf_extract.factory.workers import SdkWorker, StubWorker, scenario_script

    # The dispatcher's log is what it did, tick by tick.
    logging.getLogger("pdf_extract.factory").setLevel(logging.INFO)
    # Each Run worktree has its own .venv; `uv run` would warn about this one's.
    os.environ.pop("VIRTUAL_ENV", None)
    config = load_config()
    ledger = _ledger()
    stub = args.stub is not None
    if stub:
        worker: Any = StubWorker(scenario_script(Path(args.stub)))
        the_forge: Any = forge.LocalForge(DATA / "stub")
        config.accounts = []
        config.owner = config.owner or "owner"
    else:
        if not config.accounts:
            raise FactoryError("no accounts: list them in data/factory/local.yaml "
                               "(factory/local.example.yaml)")
        worker = SdkWorker()
        the_forge = forge.GhForge(Path.cwd())
        config.owner = config.owner or forge.owner_login()

    def pull() -> None:
        ok, out = run_command("pnpm data:pull", Path.cwd())
        if not ok:
            raise FactoryError(f"pnpm data:pull failed: {out[-500:]}")

    dispatcher = Dispatcher(
        ledger, config, repo=_repo(), worker=worker, forge=the_forge,
        pull_data=None if stub else pull,
        backup=None if stub else (lambda: backup_ledger(LEDGER_PATH, config.backup_prefix)),
        push=not (stub or args.no_push),
    )
    if args.once:
        outcome = dispatcher.tick()
        return {"action": outcome.action, "detail": outcome.detail,
                "wait_until": outcome.wait_until.isoformat() if outcome.wait_until else None}
    dispatcher.run_forever()
    return {}


def _text(r: Result) -> str:
    return json.dumps(r, indent=1)


def add_factory_parser(
    subparsers: argparse._SubParsersAction,
    add_common_args: Callable[[argparse.ArgumentParser], None],
) -> None:
    parser = subparsers.add_parser(
        "factory", help="The onboarding factory (docs/factory-spec.md)",
        description=__doc__, usage="%(prog)s <command> ...",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.set_defaults(help_parser=parser)
    sub = parser.add_subparsers(dest="factory_command", metavar="<command>",
                                help=argparse.SUPPRESS)

    def leaf(name: str, handler, render=_text) -> argparse.ArgumentParser:
        p = sub.add_parser(name, description=handler.__doc__)
        p.set_defaults(handler=handler, render=render)
        p.add_argument("--json", action="store_true", help="Print the JSON result")
        add_common_args(p)
        return p

    leaf("status", _status, report.text_status)
    leaf("queue", _queue, report.text_queue)
    p = leaf("run", _run)
    p.add_argument("--once", action="store_true", help="One tick, then stop")
    p.add_argument("--stub", metavar="FILE", help="Stub workers from a scenario JSON file")
    p.add_argument("--no-push", action="store_true", help="Commit but don't push")
    p = leaf("pause", _pause)
    p.add_argument("reason", nargs="?")
    p = leaf("resume", _resume)
    p.add_argument("--override-caps", action="store_true")
    p = leaf("retry", _retry)
    p.add_argument("job")
    p = leaf("inspect", _inspect, report.text_inspect)
    p.add_argument("job", nargs="?")
    p.add_argument("--prompt", action="store_true", help="Print the job input it started from")
    p.add_argument("--stage", help="List a stage's recent jobs instead")
    p.add_argument("--last", type=int, default=10)
    p = leaf("cost", _cost, report.text_cost)
    p.add_argument("--stage", action="store_true", help="By stage instead of by Run")
    leaf("backup", _backup)
