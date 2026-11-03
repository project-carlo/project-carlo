"""The accounts' usage: which can take a new job, and when one next can (docs/factory.md,
Usage).

Each account is a Claude Code config directory signed in with `claude /login`. Its usage
comes from the endpoint Claude Code reads, with that login's OAuth token. A rate-limit
error from a worker is the backstop whatever the endpoint said.

Every reading goes through one `Poller`, which the usage check and the quota readings
share: a reading of an account taken in the last `usage_min_interval_seconds` is handed
out again rather than asked for, an account is never asked twice in that interval, and a
429 cools down only the account it came from, for as long as its `Retry-After` says.
"""

from __future__ import annotations

import dataclasses
import email.utils
import json
import math
import os
import re
import subprocess
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pdf_extract.factory.config import Account, Config, JobUsage

if TYPE_CHECKING:
    from pdf_extract.factory.ledger import Ledger

USAGE_URL = "https://api.anthropic.com/api/oauth/usage"
WEEK = timedelta(days=7)
FIVE_HOURS = timedelta(hours=5)


class UsageError(RuntimeError):
    """The endpoint failed or answered something unexpected: the dispatcher pauses, or for
    a 429 (`status`) waits out a cooldown and tries again."""

    def __init__(self, message: str, status: int | None = None,
                 retry_after: float | None = None) -> None:
        super().__init__(message)
        self.status = status  # the endpoint's HTTP status, when it answered with an error
        self.retry_after = retry_after  # seconds, from its Retry-After header


class Cooldown(UsageError):
    """The account's usage endpoint answered 429: nothing asks it again until `until`."""

    def __init__(self, account: str, until: datetime, reason: str) -> None:
        super().__init__(f"{account}: usage check cooldown until {until.isoformat()}: "
                         f"{reason}", status=429)
        self.account, self.until, self.reason = account, until, reason


class TooSoon(UsageError):
    """A fresh reading was asked for within `usage_min_interval_seconds` of the last
    request to the account, by a reading that doesn't wait."""


@dataclass(frozen=True)
class Usage:
    five_hour: float  # percent used
    five_hour_resets: datetime
    seven_day: float
    seven_day_resets: datetime
    # The whole response, scrubbed: model-specific and extra windows the fields above drop.
    raw: dict[str, Any] | None = field(default=None, compare=False)
    # When it was read (set by the Poller), so a shared reading keeps its own time.
    at: datetime | None = field(default=None, compare=False)


@dataclass(frozen=True)
class Standing:
    account: Account
    usage: Usage
    five_hour_allowed: float
    weekly_allowed: float  # the paced weekly cap today
    eligible: bool
    headroom: float
    eligible_at: datetime  # when it can next take a job, if not now


def taken(usage: Usage, clock: Callable[[], datetime]) -> str:
    """When a reading was taken, for its ledger row: a shared one keeps its own time."""
    return (usage.at or clock()).isoformat(timespec="microseconds")


def _parse_time(value: Any, unused: timedelta, at: datetime) -> datetime:
    """A window's reset time. A window with no usage yet has none: it would start now."""
    if value is None:
        return at + unused
    when = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return when if when.tzinfo else when.replace(tzinfo=UTC)


# Keys never stored from a response, should one ever carry them.
_SECRET_KEY = re.compile(r"token$|^token|authori[sz]ation|credential|secret|password|cookie|"
                         r"api_?key|bearer", re.I)


def scrub(value: Any) -> Any:
    """A response without anything that looks like a credential."""
    if isinstance(value, dict):
        return {k: scrub(v) for k, v in value.items() if not _SECRET_KEY.search(str(k))}
    if isinstance(value, list):
        return [scrub(v) for v in value]
    if isinstance(value, str) and re.match(r"(Bearer |sk-ant-)", value):
        return "[removed]"
    return value


def parse_usage(body: Any, at: datetime | None = None) -> Usage:
    at = at or datetime.now(UTC)
    try:
        five, week = body["five_hour"], body["seven_day"]
        return Usage(float(five["utilization"] or 0),
                     _parse_time(five["resets_at"], FIVE_HOURS, at),
                     float(week["utilization"] or 0), _parse_time(week["resets_at"], WEEK, at),
                     raw=scrub(body))
    except (KeyError, TypeError, ValueError) as exc:
        raise UsageError(f"unexpected usage response: {exc!r}") from None


def _token(account: Account) -> str:
    path = account.config_dir / ".credentials.json"
    for attempt in range(2):
        try:
            oauth = json.loads(path.read_text(encoding="utf-8"))["claudeAiOauth"]
        except (OSError, ValueError, KeyError) as exc:
            raise UsageError(f"{account.name}: no Claude login in {path} ({exc}); "
                             f"run CLAUDE_CONFIG_DIR={account.config_dir} claude /login") from None
        if oauth.get("expiresAt", 0) / 1000 > time.time() + 60:
            return str(oauth["accessToken"])
        if attempt == 0:
            # Claude Code refreshes an expired login when it starts.
            try:
                subprocess.run(["claude", "auth", "status"], capture_output=True, timeout=60,
                               env={**os.environ, "CLAUDE_CONFIG_DIR": str(account.config_dir)})
            except (OSError, subprocess.SubprocessError):
                pass  # still expired below: the error says how to sign in again
    raise UsageError(f"{account.name}: the Claude login has expired; "
                     f"run CLAUDE_CONFIG_DIR={account.config_dir} claude /login")


def fetch_usage(account: Account) -> Usage:
    request = urllib.request.Request(USAGE_URL, headers={
        "Authorization": f"Bearer {_token(account)}",
        "anthropic-beta": "oauth-2025-04-20",
        "User-Agent": "project-carlo-factory",
    })
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        raise UsageError(f"{account.name}: usage endpoint failed: {exc}", status=exc.code,
                         retry_after=retry_after(exc.headers)) from None
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise UsageError(f"{account.name}: usage endpoint failed: {exc}") from None
    return parse_usage(body)


def retry_after(headers: Any, at: datetime | None = None) -> float | None:
    """A Retry-After header in seconds: either seconds or an HTTP date. None if absent or
    unreadable."""
    value = headers.get("Retry-After") if headers is not None else None
    if value is None:
        return None
    value = str(value).strip()
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        when = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when.tzinfo is None:
        when = when.replace(tzinfo=UTC)
    return max(0.0, (when - (at or datetime.now(UTC))).total_seconds())


COOLDOWNS = "usage_cooldowns"  # the ledger key: account -> {reason, since, until}


class Poller:
    """The one way the factory reads usage: shared readings, spaced requests and a
    cooldown per account (module docstring).

    The quota's after reading calls it from a background thread, so it only touches the
    ledger in `sync`, which the dispatcher calls from its own thread each tick: it saves
    the cooldowns this process changed and loads the rest (`resume` clears them).
    """

    def __init__(self, ledger: Ledger, config: Config, fetch: Fetch,
                 clock: Callable[[], datetime],
                 sleep: Callable[[float], None] = time.sleep) -> None:
        self.ledger, self.config, self.fetch = ledger, config, fetch
        self.clock, self.sleep = clock, sleep
        self._lock = threading.Lock()
        self._account_locks: dict[str, threading.Lock] = {}
        self._last: dict[str, Usage] = {}  # the latest reading of each account
        self._asked: dict[str, datetime] = {}  # when each account was last asked
        self._cooldowns: dict[str, dict[str, str]] = {}
        self._changed: dict[str, dict[str, str] | None] = {}  # not yet in the ledger
        self.sync()

    @property
    def interval(self) -> timedelta:
        return timedelta(seconds=self.config.usage_min_interval_seconds)

    def sync(self) -> None:
        with self._lock:
            saved = dict(self.ledger.get(COOLDOWNS) or {})
            if self._changed:
                for name, value in self._changed.items():
                    if value is None:
                        saved.pop(name, None)
                    else:
                        saved[name] = value
                self.ledger.set(COOLDOWNS, saved or None)
                self._changed = {}
            self._cooldowns = saved

    def cooling(self, account: str) -> Cooldown | None:
        """The account's cooldown, if it is cooling down now."""
        with self._lock:
            entry = self._cooldowns.get(account)
        if entry is None:
            return None
        until = datetime.fromisoformat(entry["until"])
        return Cooldown(account, until, entry["reason"]) if until > self.clock() else None

    def read(self, account: Account, *, since: datetime | None = None,
             wait: bool = True) -> Usage:
        """A reading of `account` taken at or after `since` (by default, one interval ago):
        the last one if it is recent enough, else a new request. A request within an
        interval of the last one waits the rest of it, or with `wait` False raises
        TooSoon. An account cooling down raises Cooldown without asking."""
        with self._lock:
            lock = self._account_locks.setdefault(account.name, threading.Lock())
        with lock:  # one request per account at a time; the others share its answer
            cooldown = self.cooling(account.name)
            if cooldown is not None:
                raise cooldown
            at = self.clock()
            since = at - self.interval if since is None else since
            last = self._last.get(account.name)
            if last is not None and last.at is not None and last.at >= since:
                return last
            asked = self._asked.get(account.name)
            if asked is not None and at - asked < self.interval:
                left = (self.interval - (at - asked)).total_seconds()
                if not wait:
                    raise TooSoon(f"{account.name}: asked {(at - asked).total_seconds():.0f}s "
                                  f"ago; the next request in {left:.0f}s")
                self.sleep(left)
            self._asked[account.name] = self.clock()
            try:
                usage = self.fetch(account)
            except UsageError as exc:
                if exc.status == 429:
                    raise self._cool_down(account.name, exc) from None
                raise
            usage = dataclasses.replace(usage, at=usage.at or self.clock())
            self._last[account.name] = usage
            self._set_cooldown(account.name, None)
            return usage

    def _cool_down(self, name: str, exc: UsageError) -> Cooldown:
        """Wait what the endpoint's Retry-After asks, or `usage_cooldown_minutes` without
        one, then try again (another 429 waits again)."""
        at = self.clock()
        wait = (timedelta(seconds=exc.retry_after) if exc.retry_after is not None
                else timedelta(minutes=self.config.usage_cooldown_minutes))
        until = at + max(wait, self.interval)
        with self._lock:
            since = (self._cooldowns.get(name) or {}).get("since", at.isoformat())
        reason = str(exc)
        self._set_cooldown(name, {"reason": reason, "since": since,
                                  "until": until.isoformat()})
        return Cooldown(name, until, reason)

    def _set_cooldown(self, name: str, value: dict[str, str] | None) -> None:
        with self._lock:
            if value is None and name not in self._cooldowns:
                return
            if value is None:
                self._cooldowns.pop(name, None)
            else:
                self._cooldowns[name] = value
            self._changed[name] = value


def _threshold(cap: float, need: float) -> float:
    """The usage below which a job needing `need` points can start under `cap`. A job
    needing the whole cap or more starts only from an unused window."""
    return max(cap - need, min(cap, 1))


def standing(account: Account, usage: Usage, config: Config, at: datetime,
             need: JobUsage = JobUsage()) -> Standing:
    """Whether the account can take a job expected to use `need` (with what jobs already
    running on it are expected to use) and stay under both caps, and if not, when to look
    again."""
    week_start = usage.seven_day_resets - WEEK
    days_in = max(0, min(6, math.floor((at - week_start) / timedelta(days=1))))
    weekly_allowed = config.weekly_cap * (days_in + 1) / 7
    five_below = _threshold(config.five_hour_cap, need.five_hour)
    week_below = _threshold(weekly_allowed, need.weekly)
    five_ok = usage.five_hour < five_below
    week_ok = usage.seven_day < week_below
    headroom = min(five_below - usage.five_hour, week_below - usage.seven_day)
    waits = [at]
    if not five_ok:
        waits.append(usage.five_hour_resets)
    if not week_ok:
        # The paced cap rises each day; past the full cap, only the reset helps.
        next_day = week_start + timedelta(days=days_in + 1)
        full = usage.seven_day >= _threshold(config.weekly_cap, need.weekly)
        waits.append(usage.seven_day_resets if full or days_in >= 6 else next_day)
    return Standing(account, usage, config.five_hour_cap, weekly_allowed, five_ok and week_ok,
                    headroom, max(waits))


Fetch = Callable[[Account], Usage]


def standings(config: Config, fetch: Fetch = fetch_usage, at: datetime | None = None,
              need: JobUsage = JobUsage(),
              reserved: dict[str, JobUsage] | None = None) -> list[Standing]:
    """Each account's standing for a job expected to use `need`, with `reserved` what jobs
    already running on each account are expected to use still."""
    at = at or datetime.now(UTC)
    reserved = reserved or {}
    return [standing(a, fetch(a), config, at, need + reserved.get(a.name, JobUsage()))
            for a in config.accounts]


def choose(rows: list[Standing], *, only: str | None = None) -> Standing | None:
    """The eligible account whose weekly window resets soonest (or the job's own account).

    Whatever an account hasn't used by its weekly reset is lost, so the one resetting first
    is drained first. Between accounts resetting at the same time, the most headroom wins.
    """
    eligible = [s for s in rows if s.eligible and (only is None or s.account.name == only)]
    return min(eligible, key=lambda s: (s.usage.seven_day_resets, -s.headroom), default=None)


def next_eligible(rows: list[Standing], *, only: str | None = None) -> datetime | None:
    times = [s.eligible_at for s in rows if only is None or s.account.name == only]
    return min(times, default=None)


def account_path(config: Config, name: str) -> Path:
    for a in config.accounts:
        if a.name == name:
            return a.config_dir
    raise UsageError(f"no account named {name} in data/factory/local.yaml")
