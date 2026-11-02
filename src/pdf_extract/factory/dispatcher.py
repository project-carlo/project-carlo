"""The dispatcher: the loop that runs the factory, and what it is made of (docs/factory.md).

Each tick checks the pause and the usage cooldown, does the housekeeping, then takes one
job a step on. The parts, each in its own module:

- `engine`: one job, from picking it to its gates, send-backs and what follows them.
- `attempts`: one attempt of a job: starting its worker and recording what came back.
- `accounts`: the account each attempt runs on, against the caps.
- `answers`: issues for blocking flags, and what the owner's answers do.
- `housekeeping`: readings, issues, merged Runs, seed readiness and backups between jobs.
- `metrics.readings`: the quota readings for measuring. The rest of `metrics` (tokens,
  attempt metadata, the reports) is called from these parts, never the other way round.
"""

from __future__ import annotations

import logging
import subprocess
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from pdf_extract.factory.accounts import Accounts
from pdf_extract.factory.answers import Answers
from pdf_extract.factory.attempts import Attempts
from pdf_extract.factory.config import RUNS_DIR, Config
from pdf_extract.factory.engine import Engine
from pdf_extract.factory.forge import Forge
from pdf_extract.factory.housekeeping import Housekeeping
from pdf_extract.factory.ledger import Ledger
from pdf_extract.factory.metrics.readings import Readings
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.secrets import Secrets, command_env
from pdf_extract.factory.usage import Fetch, fetch_usage
from pdf_extract.factory.workers import Worker

LOGGER = logging.getLogger(__name__)


def run_command(command: str, cwd: Path, secrets: dict[str, str] | None = None,
                timeout: int = 3600) -> tuple[bool, str]:
    """A shell command, with the dispatcher's environment scrubbed of secrets plus
    `secrets`, and without reading a `.env` (secrets.command_env)."""
    try:
        proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout, env=command_env(secrets))
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    return proc.returncode == 0, (proc.stdout + proc.stderr)[-6000:]


class Dispatcher:
    def __init__(
        self,
        ledger: Ledger,
        config: Config,
        *,
        repo: Path,
        worker: Worker,
        forge: Forge,
        fetch_usage: Fetch = fetch_usage,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        commands: Callable[..., tuple[bool, str]] = run_command,
        secrets: Secrets | None = None,
        db_path: Path = Path("data") / "parish_events.db",
        runs_dir: Path = RUNS_DIR,
        queue_path: Path | None = None,
        pull_data: Callable[[], None] | None = None,
        backup: Callable[[], str] | None = None,
        cleanup: Callable[[], None] | None = None,
        sandbox_dir: Path | None = None,
        push: bool = True,
    ) -> None:
        self.ledger, self.config, self.clock = ledger, config, clock
        self.accounts = Accounts(ledger, config, fetch_usage, clock)
        self.readings = Readings(ledger, config, fetch_usage, clock)
        self.answers = Answers(ledger, config, forge)
        secrets = secrets or {}
        self.attempts = Attempts(ledger, config, worker=worker, accounts=self.accounts,
                                 readings=self.readings, clock=clock, runs_dir=runs_dir,
                                 secrets=secrets, cleanup=cleanup)
        self.engine = Engine(ledger, config, repo=repo, forge=forge, attempts=self.attempts,
                             answers=self.answers, clock=clock, commands=commands,
                             secrets=secrets, db_path=db_path, queue_path=queue_path,
                             push=push)
        # Sandboxed workers' workspaces, one per Run, go when the Run is retired.
        self.housekeeping = Housekeeping(ledger, config, repo=repo, forge=forge,
                                         readings=self.readings, answers=self.answers,
                                         clock=clock, db_path=db_path, runs_dir=runs_dir,
                                         pull_data=pull_data, backup=backup,
                                         sandbox_dir=sandbox_dir)

    def run_forever(self) -> None:
        self.attempts.recover()
        while True:
            outcome = self.tick()
            LOGGER.info("%s %s", outcome.action, outcome.detail)
            if outcome.action == "ran":
                continue
            pause = self.config.tick_seconds
            if outcome.wait_until is not None:
                pause = max(5, min(pause, (outcome.wait_until - self.clock()).total_seconds()))
            time.sleep(pause)

    def tick(self) -> Outcome:
        paused = self.ledger.get("paused")
        if paused:
            return Outcome("paused", paused.get("reason", ""))
        cooldown = self.ledger.get("usage_cooldown")
        if cooldown:
            # Nothing reads the endpoint until the cooldown ends, housekeeping's readings
            # included; then the next job's usage check tries it again.
            until = datetime.fromisoformat(cooldown["until"])
            if until > self.clock():
                return Outcome("waiting", f"usage check cooldown until {cooldown['until']}: "
                                          f"{cooldown.get('reason', '')}", until)
        self.housekeeping.run()
        job = self.engine.pick()
        if job is None:
            if cooldown:  # no usage check to retry: the periodic readings take over again
                self.ledger.set("usage_cooldown", None)
            return Outcome("idle")
        return self.engine.run_job(job)
