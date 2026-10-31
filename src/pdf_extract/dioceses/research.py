"""Structured research attempts and the actions that could change their outcome.

These are observations, not evidence that a bulletin does not exist. A blocked
request and a search with no result must never turn into the same claim.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

OUTCOMES = frozenset({
    "found", "not-found", "access-blocked", "unsupported-format", "not-published",
})
BULLETIN_STATUSES = (OUTCOMES - {"found"}) | {"available"}
FIELDS = {"method", "url", "checked", "outcome", "next_action", "retry_when", "revisit_after"}


def _date(value: Any) -> dt.date | None:
    if not isinstance(value, str) or len(value) != 10:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def errors(attempts: Any, *, today: str) -> list[str]:
    """Return errors without trusting a hand-edited record's types."""
    if not isinstance(attempts, list):
        return ["research must be a list of attempts"]
    out = []
    for i, attempt in enumerate(attempts, 1):
        where = f"research #{i}"
        if not isinstance(attempt, Mapping):
            out.append(f"{where} must be an object")
            continue
        for field in attempt:
            if field not in FIELDS:
                out.append(f"{where}: unknown field {field!r}")
        for field in ("method", "outcome", "next_action", "retry_when", "url"):
            value = attempt.get(field)
            if value is not None and not isinstance(value, str):
                out.append(f"{where}: {field} must be text")
        if not isinstance(attempt.get("method"), str) or not attempt["method"].strip():
            out.append(f"{where}: method is required")
        outcome = attempt.get("outcome")
        if not isinstance(outcome, str) or outcome not in OUTCOMES:
            out.append(f"{where}: outcome must be one of {', '.join(sorted(OUTCOMES))}")
        if not _date(attempt.get("checked")):
            out.append(f"{where}: checked must be a date like 2026-09-06")
        elif attempt["checked"] > today:
            out.append(f"{where}: checked is in the future")
        if "revisit_after" in attempt and attempt["revisit_after"] is not None:
            revisit = _date(attempt["revisit_after"])
            if not revisit:
                out.append(f"{where}: revisit_after must be a date like 2026-09-06")
            elif _date(attempt.get("checked")) and attempt["revisit_after"] < attempt["checked"]:
                out.append(f"{where}: revisit_after cannot precede checked")
        if outcome != "found":
            for field in ("next_action", "retry_when"):
                if not isinstance(attempt.get(field), str) or not attempt[field].strip():
                    out.append(f"{where}: {field} is required for an unresolved outcome")
        if isinstance(attempt.get("url"), str) and attempt["url"]:
            try:
                url = urlsplit(attempt["url"])
                valid_url = url.scheme in ("https", "http") and bool(url.netloc)
            except ValueError:
                valid_url = False
            if not valid_url:
                out.append(f"{where}: url must start with http:// or https://")
    return out


def pending(record: Mapping[str, Any], *, today: str) -> list[dict[str, Any]]:
    """Latest attempt per method/URL; a later success retires that failed check.

    Dependency triggers have no due date. They remain visible, without implying
    that repeating the same request today will help. Preserve distinct channels.
    """
    latest: dict[tuple[str, str], dict[str, Any]] = {}
    attempts = record.get("research")
    for attempt in attempts if isinstance(attempts, list) else []:
        if not isinstance(attempt, dict) or not _date(attempt.get("checked")):
            continue
        key = (str(attempt.get("method", "")), str(attempt.get("url", "")))
        if key not in latest or attempt["checked"] >= latest[key]["checked"]:
            latest[key] = attempt
    out = []
    for attempt in latest.values():
        if attempt.get("outcome") == "found":
            continue
        after = attempt.get("revisit_after")
        state = "waiting-for-trigger"
        if _date(after):
            state = "due" if after <= today else "scheduled"
        out.append({**attempt, "state": state})
    return sorted(out, key=lambda a: (a.get("checked", ""), str(a.get("method", ""))))
