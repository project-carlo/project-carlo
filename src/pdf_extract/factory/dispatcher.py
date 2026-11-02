"""The dispatcher: the loop that runs the factory, and what it is made of (§5).

Each tick checks the pause and the usage cooldown, does the housekeeping, then takes one
job a step on. The parts, each in its own module:

- `engine`: one job, from picking it to its gates, send-backs and what follows them.
- `attempts`: one attempt of a job: starting its worker and recording what came back.
- `accounts`: the account each attempt runs on, and the quota readings.
- `answers`: issues for blocking flags, and what the owner's answers do.
- `housekeeping`: readings, issues, merged Runs, seed readiness and backups between jobs.
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
from pdf_extract.factory.engine import Engine, main_queue
from pdf_extract.factory.forge import Forge
from pdf_extract.factory.housekeeping import Housekeeping
from pdf_extract.factory.ledger import Ledger
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.usage import Fetch, fetch_usage
from pdf_extract.factory.workers import Worker

__all__ = ["Dispatcher", "Outcome", "main_queue", "run_command"]

LOGGER = logging.getLogger(__name__)


def run_command(command: str, cwd: Path, timeout: int = 3600) -> tuple[bool, str]:
    try:
        proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout)
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
        commands: Callable[[str, Path], tuple[bool, str]] = run_command,
        db_path: Path = Path("data") / "parish_events.db",
        runs_dir: Path = RUNS_DIR,
        queue_path: Path | None = None,
        pull_data: Callable[[], None] | None = None,
        backup: Callable[[], str] | None = None,
        push: bool = True,
    ) -> None:
        self.ledger, self.config, self.clock = ledger, config, clock
        self.accounts = Accounts(ledger, config, fetch_usage, clock)
        self.answers = Answers(ledger, config, forge)
        self.attempts = Attempts(ledger, config, worker=worker, accounts=self.accounts,
                                 clock=clock, runs_dir=runs_dir)
        self.engine = Engine(ledger, config, repo=repo, forge=forge, attempts=self.attempts,
                             answers=self.answers, clock=clock, commands=commands,
                             db_path=db_path, queue_path=queue_path, push=push)
        self.housekeeping = Housekeeping(ledger, config, repo=repo, forge=forge,
                                         accounts=self.accounts, answers=self.answers,
                                         clock=clock, db_path=db_path, runs_dir=runs_dir,
                                         pull_data=pull_data, backup=backup)

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
