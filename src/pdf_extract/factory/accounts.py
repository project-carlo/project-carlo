"""Which account a job's next attempt runs on, against the caps (§5), and the quota readings.

A failing usage check pauses the factory; a 429 from the usage endpoint is a cooldown
instead, which ends by itself. The readings are for measuring, not choosing: one before
each attempt (the selection's), one after it, a settled one once the account has been idle
a while, and a periodic one of every account.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from pdf_extract.factory.config import Account, Config
from pdf_extract.factory.ledger import WAITING_USAGE, Ledger, now
from pdf_extract.factory.outcome import Outcome
from pdf_extract.factory.usage import Fetch, UsageError, choose, next_eligible, scrub, standings

LOGGER = logging.getLogger(__name__)
# How long an attempt's gates wait for its after reading (seconds); usually under one.
AFTER_READING_WAIT = 10


def stamp(clock: Callable[[], datetime]) -> str:
    return clock().isoformat(timespec="microseconds")


class Accounts:
    def __init__(self, ledger: Ledger, config: Config, fetch_usage: Fetch,
                 clock: Callable[[], datetime]) -> None:
        self.ledger, self.config = ledger, config
        self.fetch_usage, self.clock = fetch_usage, clock

    def _stamp(self) -> str:
        return stamp(self.clock)

    # ── Choosing ────────────────────────────────────────────────────────────
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
        taken = self._stamp()
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

    # ── Readings ────────────────────────────────────────────────────────────
    def after_reading(self, account: Account) -> Callable[[int, int], None]:
        """Start the reading after an attempt in the background, so a slow endpoint or an
        expired login doesn't hold up the attempt's gates. The returned function records it
        for the attempt, waiting at most AFTER_READING_WAIT; a late one is dropped."""
        got: dict[str, Any] = {}

        def fetch() -> None:
            try:
                got["usage"] = self.fetch_usage(account)
                got["at"] = self._stamp()
            except Exception as exc:  # recorded as a warning below
                got["error"] = exc

        thread = threading.Thread(target=fetch, name=f"after-reading-{account.name}",
                                  daemon=True)
        thread.start()

        def record(attempt_id: int, job_id: int) -> None:
            thread.join(AFTER_READING_WAIT)
            if thread.is_alive():
                LOGGER.warning("after quota reading of %s took over %ss: skipped",
                               account.name, AFTER_READING_WAIT)
            elif "error" in got:
                LOGGER.warning("after quota reading of %s failed: %s", account.name,
                               got["error"])
            else:
                self.ledger.add_usage(account.name, got["at"], got["usage"], "after",
                                      attempt_id, job_id)
        return record

    def rate_limit(self, attempt_id: int, info: dict[str, Any]) -> None:
        """An SDK rate-limit event, kept without credentials. Called from inside the
        worker's message loop: a failure to record it is logged, never raised."""
        try:
            self.ledger.add_rate_limit_event(attempt_id, scrub(info), self._stamp())
        except Exception:
            LOGGER.exception("attempt %s: recording a rate-limit event failed", attempt_id)

    def _reading(self, account: Account, source: str, attempt_id: int | None = None,
                 job_id: int | None = None) -> None:
        """A quota reading for measuring, not choosing: a failure is logged, nothing more."""
        try:
            usage = self.fetch_usage(account)
        except (UsageError, OSError) as exc:
            LOGGER.warning("%s quota reading of %s failed: %s", source, account.name, exc)
            return
        self.ledger.add_usage(account.name, self._stamp(), usage, source, attempt_id, job_id)

    def sample_quota(self) -> None:
        """A settled reading of each account idle `quota_settle_seconds` since its last
        attempt (once per attempt), and one of every account each `quota_sample_minutes`."""
        if not self.config.accounts:
            return
        at = self.clock()
        settle = timedelta(seconds=self.config.quota_settle_seconds)
        for a in self.config.accounts:
            last = self.ledger.one("SELECT id, job_id, finished_at FROM attempt WHERE "
                                   "account = ? AND finished_at IS NOT NULL ORDER BY "
                                   "finished_at DESC, id DESC LIMIT 1", a.name)
            if last is None:
                continue
            # Not for an attempt long finished (the dispatcher was down or paused).
            finished = datetime.fromisoformat(last["finished_at"])
            if not finished + settle <= at <= finished + settle + timedelta(hours=1):
                continue
            if not self.ledger.one("SELECT 1 FROM usage WHERE source = 'settled' AND "
                                   "attempt_id = ?", last["id"]):
                self._reading(a, "settled", last["id"], last["job_id"])
        if self.ledger.due("quota_sampled", timedelta(minutes=self.config.quota_sample_minutes),
                           at):
            for a in self.config.accounts:
                self._reading(a, "periodic")
