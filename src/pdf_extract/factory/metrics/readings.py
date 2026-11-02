"""Quota readings for measuring, not choosing (docs/factory-quota.md).

The reading `accounts` takes to choose an account becomes the attempt's `before`. The
rest are here: an `after` reading once the worker returns, a `settled` one once the
account has been idle `quota_settle_seconds`, a `periodic` one of every account each
`quota_sample_minutes`, and the SDK's rate-limit events. A failing reading is logged and
never stops a job.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any

from pdf_extract.factory.config import Account, Config
from pdf_extract.factory.ledger import Ledger, stamp
from pdf_extract.factory.usage import Fetch, UsageError, scrub

LOGGER = logging.getLogger(__name__)
# How long an attempt's gates wait for its after reading (seconds); usually under one.
AFTER_READING_WAIT = 10

Record = Callable[[int, int], None]


class Readings:
    def __init__(self, ledger: Ledger, config: Config, fetch_usage: Fetch,
                 clock: Callable[[], datetime]) -> None:
        self.ledger, self.config = ledger, config
        self.fetch_usage, self.clock = fetch_usage, clock

    def after(self, account: Account | None) -> Record:
        """Start the reading after an attempt in the background, so a slow endpoint or an
        expired login doesn't hold up the attempt's gates. The returned function records it
        for the attempt, waiting at most AFTER_READING_WAIT; a late one is dropped. It never
        raises. Without an account (stub runs) there is nothing to read."""
        if account is None:
            return lambda attempt_id, job_id: None
        got: dict[str, Any] = {}

        def fetch() -> None:
            try:
                got["usage"] = self.fetch_usage(account)
                got["at"] = stamp(self.clock)
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
                try:
                    self.ledger.add_usage(account.name, got["at"], got["usage"], "after",
                                          attempt_id, job_id)
                except Exception:
                    LOGGER.exception("attempt %s: recording its after reading failed",
                                     attempt_id)
        return record

    def rate_limit(self, attempt_id: int, info: dict[str, Any]) -> None:
        """An SDK rate-limit event, kept without credentials. Called from inside the
        worker's message loop: a failure to record it is logged, never raised."""
        try:
            self.ledger.add_rate_limit_event(attempt_id, scrub(info), stamp(self.clock))
        except Exception:
            LOGGER.exception("attempt %s: recording a rate-limit event failed", attempt_id)

    def _reading(self, account: Account, source: str, attempt_id: int | None = None,
                 job_id: int | None = None) -> None:
        try:
            usage = self.fetch_usage(account)
        except (UsageError, OSError) as exc:
            LOGGER.warning("%s quota reading of %s failed: %s", source, account.name, exc)
            return
        self.ledger.add_usage(account.name, stamp(self.clock), usage, source, attempt_id,
                              job_id)

    def sample(self) -> None:
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
