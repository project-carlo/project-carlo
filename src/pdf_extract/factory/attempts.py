"""One attempt of a job: start a worker on it, record what came back. What it used
(tokens, quota readings) goes to `metrics`, which never stops a job.

What the next attempt is told is the job's pending prompt (`ledger.pending` lists the
kinds).

An attempt that hits a usage limit or crashes is settled here. The engine acts on the
rest: a crash past `max_crashes` blocks the Run, a partial end continues or is exhausted,
and a finished attempt goes to the gates.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.factory import git, render
from pdf_extract.factory.accounts import Accounts
from pdf_extract.factory.config import Config
from pdf_extract.factory.handoff import handoff_path
from pdf_extract.factory.ledger import (
    QUEUED,
    RUNNING,
    WAITING_USAGE,
    Ledger,
    now,
    pending,
    stamp,
)
from pdf_extract.factory.metrics import attempt_meta
from pdf_extract.factory.metrics.readings import Readings
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.spec import StageSpec
from pdf_extract.factory.workers import (
    CRASH,
    PARTIAL,
    TIMEOUT,
    USAGE,
    Worker,
    WorkerRequest,
    copy_transcript,
    prompt_body,
)


@dataclass
class Ended:
    """An attempt the engine acts on next. `outcome` is CRASH (past `max_crashes`),
    PARTIAL, TIMEOUT or OK; `why` says why for the first three."""

    job: Any
    outcome: str
    why: str = ""


class Attempts:
    def __init__(self, ledger: Ledger, config: Config, *, worker: Worker, accounts: Accounts,
                 readings: Readings, clock: Callable[[], datetime], runs_dir: Path) -> None:
        self.ledger, self.config, self.worker = ledger, config, worker
        self.accounts, self.readings = accounts, readings
        self.clock, self.runs_dir = clock, runs_dir
        attempt_meta.code_commit()  # the commit this code was loaded from, read at start

    def recover(self) -> None:
        """A job still marked running when the dispatcher starts crashed with it."""
        for row in self.ledger.all("SELECT id FROM job WHERE status = ?", RUNNING):
            self.ledger.set_job(row["id"], status=QUEUED, pending_prompt=pending("resume"))

    def run(self, run: Any, job: Any, spec: StageSpec, worktree: Path) -> Outcome | Ended:
        if job["resumes_job"] and job["account"] is None:
            original = self.ledger.job(job["resumes_job"])
            if original["account"] and original["run_id"] == run["id"]:
                # Its session can only be resumed from the account that stores it.
                self.ledger.set_job(job["id"], account=original["account"])
                job = self.ledger.job(job["id"])
        # What a first message points to, read before the usage check so a missing one costs
        # no reading. A missing read is a FactoryError: the job waits and tries again
        # (merging main again, until it has started), so a fix to the spec on main heals it;
        # after a few failures the Run blocks.
        reads = render.read_files(spec, render.worktree_text(worktree), run["id"], job["name"])
        account, reading, waiting = self.accounts.pick(job)
        if waiting is not None:
            return waiting
        job = self.ledger.job(job["id"])
        values = render.job_values(self.ledger, run, job)
        before = json.loads(job["pending_prompt"] or "null") or {}
        kind, prompt, session = render.next_prompt(self.ledger, run, job, spec, values)
        if kind in ("start", "fresh"):
            files = reads | render.input_files(self.ledger, run, job)
            for rel, text in files.items():
                (worktree / rel).parent.mkdir(parents=True, exist_ok=True)
                (worktree / rel).write_text(text, encoding="utf-8")
        if before.get("kind") not in ("resume", "continue"):
            # A send-back or an answer needs a new handoff: the old one mustn't pass again.
            handoff_path(worktree, run["id"], job["name"]).unlink(missing_ok=True)
        commit_sha = git.head(worktree)
        started = stamp(self.clock)
        with self.ledger.tx():
            attempt_id = self.ledger.add_attempt(job["id"], kind, prompt,
                                                 account.name if account else None, commit_sha,
                                                 at=started)
            if kind in ("start", "fresh"):
                self._claim_leads(run, job)
        if reading is not None:  # the selection's reading of this account is its before
            self.ledger.link_usage(reading, "before", attempt_id, job["id"])
        self.ledger.set_job(job["id"], status=RUNNING, started_at=job["started_at"] or now(),
                            account=job["account"] or (account.name if account else None),
                            commit_sha=job["commit_sha"] or commit_sha, wait_until=None,
                            session_id=session or job["session_id"])
        steps = iter(range(1, 1_000_000))
        request = WorkerRequest(
            job_id=job["id"], run_id=run["id"], job_name=job["name"], stage=job["stage"],
            spec=spec, worktree=worktree, account=account, prompt=prompt,
            system_append=prompt_body(worktree, spec.prompt), values=values, session_id=session,
            on_step=lambda k, name, detail: self.ledger.add_step(attempt_id, next(steps), k,
                                                                 name, detail),
            on_rate_limit=lambda info: self.readings.rate_limit(attempt_id, info),
        )
        result = self.worker.run(request)
        finished = stamp(self.clock)
        after = self.readings.after(account)
        transcript = copy_transcript(result, self.runs_dir / run["id"] / job["name"])
        self.ledger.finish_attempt(attempt_id, outcome=result.outcome, error=result.error,
                                   cost_usd=result.cost_usd, turns=result.turns,
                                   session_id=result.session_id, finished_at=finished,
                                   transcript=str(transcript) if transcript else None)
        attempt_meta.record(self.ledger, attempt_id, run, job, spec, worktree, account, result,
                            transcript, session, started, finished)
        after(attempt_id, job["id"])
        job = self.ledger.job(job["id"])
        self.ledger.set_job(job["id"], cost_usd=job["cost_usd"] + result.cost_usd,
                            turns=job["turns"] + result.turns,
                            session_id=result.session_id or job["session_id"])
        job = self.ledger.job(job["id"])
        if result.outcome == USAGE:
            until = result.resets_at or self.clock() + timedelta(minutes=30)
            # With a session, it continues where it stopped. Without one, the next attempt
            # starts fresh and still needs what this one was told (problems, an answer).
            then = pending("continue") if job["session_id"] else job["pending_prompt"]
            self.ledger.set_job(job["id"], status=WAITING_USAGE, wait_until=until.isoformat(),
                                pending_prompt=then)
            return Outcome("waiting", f"job {job['id']} hit a usage limit", until)
        if result.outcome == CRASH:
            then = pending("resume")
            if session and result.turns == 0:
                # The session couldn't be resumed: a fresh worker gets the files on disk,
                # and what this attempt was told (problems to fix, an answer) again.
                self.ledger.set_job(job["id"], session_id=None)
                then = job["pending_prompt"] or then
            crashes = job["crashes"] + 1
            self.ledger.set_job(job["id"], crashes=crashes)
            if crashes >= self.config.max_crashes:
                return Ended(job, CRASH, f"The worker crashed {crashes} times: {result.error}")
            self.ledger.set_job(job["id"], status=QUEUED, pending_prompt=then)
            return Outcome("ran", f"job {job['id']} crashed; resuming")
        if result.outcome in (PARTIAL, TIMEOUT):
            return Ended(job, result.outcome, f"the session ended early ({result.outcome})")
        return Ended(job, result.outcome)

    def _claim_leads(self, run: Any, job: Any) -> None:
        """The leads the attempt's input shows become the job's when the attempt starts: a
        later job's input leaves them out, and reconcile lists only those no job took."""
        for lead in render.leads_shown(self.ledger, run, job):
            self.ledger.run_sql("UPDATE lead SET used_by = ? WHERE id = ?", job["id"], lead["id"])
