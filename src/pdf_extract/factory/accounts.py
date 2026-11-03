"""Which account a job's next attempt runs on, against the caps (docs/factory.md, Usage).

A failing usage check pauses the factory. A 429 from an account's usage endpoint cools
down only that account (usage.Poller), which ends by itself: the job goes to another
account meanwhile, or waits for the soonest cooldown to end. Each check's reading is
kept, and the chosen account's becomes the attempt's `before` reading; the other readings
are `metrics.readings`.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from pdf_extract.factory.config import Account, Config, JobUsage
from pdf_extract.factory.ledger import RUNNING, WAITING_USAGE, Ledger, now
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.usage import (
    Cooldown,
    Poller,
    Usage,
    UsageError,
    choose,
    next_eligible,
    standing,
    taken,
)


class Accounts:
    def __init__(self, ledger: Ledger, config: Config, poller: Poller,
                 clock: Callable[[], datetime]) -> None:
        self.ledger, self.config = ledger, config
        self.poller, self.clock = poller, clock

    def pick(self, job: Any) -> tuple[Account | None, int | None, Outcome | None]:
        """The account for the job's next attempt, and the id of its reading taken now."""
        if not self.config.accounts:
            return None, None, None  # stub runs and tests: no usage to check
        override = self.ledger.get("override_caps", False)
        only = job["account"]
        held = self._calibration_holds()
        open_ = [a for a in self.config.accounts if a.name not in held
                 and (only is None or a.name == only)]
        until = min((t for name, t in held.items() if only is None or name == only),
                    default=None)
        if not open_ and until is not None:
            return None, None, Outcome("waiting", f"calibration gap until {until}", until)
        read, cooling = self._readings(only)
        if read is None:
            return None, None, cooling  # another failure: the factory is paused
        need = self.config.job_usage_for(job["stage"])
        reserved, at = self._reserved(job), self.clock()
        rows = [standing(a, usage, self.config, at, need + reserved.get(a.name, JobUsage()))
                for a, usage in read]
        ids = {s.account.name: self.ledger.add_usage(s.account.name, taken(s.usage, self.clock),
                                                     s.usage, "select")
               for s in rows}
        rows = [s for s in rows if s.account.name not in held]
        if override:
            pick = next((s for s in rows if only is None or s.account.name == only), None)
        else:
            pick = choose(rows, only=only)
        if pick is not None:
            return pick.account, ids[pick.account.name], None
        if cooling and not rows:
            # Every account is cooling down (or in its gap): no reading says when to look
            # again but the cooldowns themselves.
            until = min([*cooling.values(), *held.values()])
            what = ", ".join(f"{name} until {t.isoformat()}" for name, t in cooling.items())
            return None, None, Outcome("waiting", f"usage check cooldown: {what}", until)
        # The soonest of an account under its caps again, a calibration gap or a cooldown
        # ending.
        soonest = [t for t in (next_eligible(rows, only=only), until, *cooling.values())
                   if t is not None]
        until = min(soonest, default=self.clock() + timedelta(minutes=30))
        self.ledger.set_job(job["id"], status=WAITING_USAGE, wait_until=until.isoformat())
        return None, None, Outcome("waiting", f"no account has room for a {job['stage']} "
                                   f"job under its caps until {until}", until)

    def _readings(self, only: str | None) -> tuple[Any, Any]:
        """Each account's reading (the job's own account only, if it has one) and the
        accounts cooling down, with when each ends. Any other failure pauses the factory:
        None and the outcome."""
        read: list[tuple[Account, Usage]] = []
        cooling: dict[str, datetime] = {}
        for account in self.config.accounts:
            if only is not None and account.name != only:
                continue
            try:
                read.append((account, self.poller.read(account)))
            except Cooldown as exc:
                cooling[account.name] = exc.until
            except UsageError as exc:
                self.ledger.set("paused", {"reason": f"usage check failed: {exc}", "at": now()})
                return None, Outcome("paused", str(exc))
        return read, cooling

    def _reserved(self, job: Any) -> dict[str, JobUsage]:
        """What the other jobs running on each account are expected to use, so jobs run in
        parallel don't all count the same room. The meter already shows part of it, so
        this errs on the safe side. With one job at a time, nothing else is running."""
        out: dict[str, JobUsage] = {}
        for row in self.ledger.all("SELECT stage, account FROM job WHERE status = ? AND "
                                   "account IS NOT NULL AND id != ?", RUNNING, job["id"]):
            out[row["account"]] = (out.get(row["account"], JobUsage())
                                   + self.config.job_usage_for(row["stage"]))
        return out

    def _last_finished(self, account: str) -> datetime | None:
        row = self.ledger.one("SELECT MAX(finished_at) AS at FROM attempt WHERE account = ?",
                              account)
        return datetime.fromisoformat(row["at"]) if row and row["at"] else None

    def _calibration_holds(self) -> dict[str, datetime]:
        """Accounts still in their calibration gap after their last attempt, and until when.
        With `calibration_gap_seconds` 0 (the default) nothing waits."""
        gap = timedelta(seconds=self.config.calibration_gap_seconds)
        if not gap:
            return {}
        at, held = self.clock(), {}
        for a in self.config.accounts:
            last = self._last_finished(a.name)
            if last is not None and at < last + gap:
                held[a.name] = last + gap
        return held
