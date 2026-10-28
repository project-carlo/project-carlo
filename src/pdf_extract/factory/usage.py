"""The accounts' usage: which can take a new job, and when one next can (§5, step 1).

Each account is a Claude Code config directory signed in with `claude /login`. Its usage
comes from the endpoint Claude Code reads, with that login's OAuth token. A rate-limit
error from a worker is the backstop whatever the endpoint said.
"""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.factory.config import Account, Config

USAGE_URL = "https://api.anthropic.com/api/oauth/usage"
WEEK = timedelta(days=7)
FIVE_HOURS = timedelta(hours=5)


class UsageError(RuntimeError):
    """The endpoint failed or answered something unexpected: the dispatcher pauses."""


@dataclass(frozen=True)
class Usage:
    five_hour: float  # percent used
    five_hour_resets: datetime
    seven_day: float
    seven_day_resets: datetime
    # The whole response, scrubbed: model-specific and extra windows the fields above drop.
    raw: dict[str, Any] | None = field(default=None, compare=False)


@dataclass(frozen=True)
class Standing:
    account: Account
    usage: Usage
    five_hour_allowed: float
    weekly_allowed: float  # the paced weekly cap today
    eligible: bool
    headroom: float
    eligible_at: datetime  # when it can next take a job, if not now


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


def account_plan(account: Account) -> str | None:
    """The account's plan: its login's subscription and rate-limit tier, else local.yaml's."""
    try:
        oauth = json.loads((account.config_dir / ".credentials.json").read_text(
            encoding="utf-8"))["claudeAiOauth"]
        parts = [str(oauth[k]) for k in ("subscriptionType", "rateLimitTier") if oauth.get(k)]
    except (OSError, ValueError, KeyError, TypeError):
        parts = []
    return "/".join(parts) or account.plan


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
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        raise UsageError(f"{account.name}: usage endpoint failed: {exc}") from None
    return parse_usage(body)


def standing(account: Account, usage: Usage, config: Config, at: datetime) -> Standing:
    week_start = usage.seven_day_resets - WEEK
    days_in = max(0, min(6, math.floor((at - week_start) / timedelta(days=1))))
    weekly_allowed = config.weekly_cap * (days_in + 1) / 7
    five_ok = usage.five_hour < config.five_hour_cap
    week_ok = usage.seven_day < weekly_allowed
    headroom = min(config.five_hour_cap - usage.five_hour, weekly_allowed - usage.seven_day)
    waits = [at]
    if not five_ok:
        waits.append(usage.five_hour_resets)
    if not week_ok:
        # The paced cap rises each day; past the full cap, only the reset helps.
        next_day = week_start + timedelta(days=days_in + 1)
        full = usage.seven_day >= config.weekly_cap
        waits.append(usage.seven_day_resets if full or days_in >= 6 else next_day)
    return Standing(account, usage, config.five_hour_cap, weekly_allowed, five_ok and week_ok,
                    headroom, max(waits))


Fetch = Callable[[Account], Usage]


def standings(config: Config, fetch: Fetch = fetch_usage,
              at: datetime | None = None) -> list[Standing]:
    at = at or datetime.now(UTC)
    return [standing(a, fetch(a), config, at) for a in config.accounts]


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
