"""Which account a job's next attempt runs on, against the caps (docs/factory.md, Usage).

A failing usage check pauses the factory; a 429 from the usage endpoint is a cooldown
instead, which ends by itself. Each check's reading is kept, and the chosen account's
becomes the attempt's `before` reading; the other readings are `metrics.readings`.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from pdf_extract.factory.config import Account, Config
from pdf_extract.factory.ledger import WAITING_USAGE, Ledger, now, stamp
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.usage import Fetch, UsageError, choose, next_eligible, standings


class Accounts:
    def __init__(self, ledger: Ledger, config: Config, fetch_usage: Fetch,
                 clock: Callable[[], datetime]) -> None:
        self.ledger, self.config = ledger, config
        self.fetch_usage, self.clock = fetch_usage, clock

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
        try:
            rows = standings(self.config, self.fetch_usage, self.clock())
        except UsageError as exc:
            if exc.status == 429:
                return None, None, self._cool_down(exc)
            self.ledger.set("paused", {"reason": f"usage check failed: {exc}", "at": now()})
            return None, None, Outcome("paused", str(exc))
        if self.ledger.get("usage_cooldown"):
            self.ledger.set("usage_cooldown", None)
        taken = stamp(self.clock)
        ids = {s.account.name: self.ledger.add_usage(s.account.name, taken, s.usage, "select")
               for s in rows}
        rows = [s for s in rows if s.account.name not in held]
        if override:
            pick = next((s for s in rows if only is None or s.account.name == only), None)
        else:
            pick = choose(rows, only=only)
        if pick is None:
            # The soonest of an account under its caps again and a calibration gap ending.
            soonest = [t for t in (next_eligible(rows, only=only), until) if t is not None]
            until = min(soonest, default=self.clock() + timedelta(minutes=30))
            self.ledger.set_job(job["id"], status=WAITING_USAGE, wait_until=until.isoformat())
            return None, None, Outcome("waiting", f"no account under its caps until {until}",
                                       until)
        return pick.account, ids[pick.account.name], None

    def _cool_down(self, exc: UsageError) -> Outcome:
        """The endpoint is rate limiting the factory: wait `usage_cooldown_minutes`, then try
        again (another 429 waits again). Kept apart from `paused`, which only the owner clears."""
        at = self.clock()
        until = at + timedelta(minutes=self.config.usage_cooldown_minutes)
        since = (self.ledger.get("usage_cooldown") or {}).get("since", at.isoformat())
        self.ledger.set("usage_cooldown", {"reason": f"usage check failed: {exc}",
                                           "since": since, "until": until.isoformat()})
        return Outcome("waiting", f"usage check cooldown until {until.isoformat()}: {exc}",
                       until)

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
