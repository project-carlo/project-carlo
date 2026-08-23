"""Promote repeatedly-dated events to weekly ones.

Bulletins are often ambiguous about whether a listing is a one-off or a
standing weekly slot ("Adoration Wednesday at 7:00 PM" printed under this
week's calendar). The extractor has to guess, and when it guesses "one-off" it
files the slot under `single_events` with a single calendar date, so the
frontend shows it as a dated event that disappears the moment it passes.

The tell is that a genuinely weekly slot keeps reappearing: the same church,
the same event type, the same weekday and start time, exactly one week later,
bulletin after bulletin. `data/event_history.json` accumulates every dated
occurrence the pipeline has extracted, and `promote_recurring_events` rewrites
a dated event as a weekly one once matching occurrences show up in each of the
`MIN_PRIOR_WEEKS` weeks immediately before it.

The history file is the pipeline's only memory of past bulletins: `events.json`
is compacted down to the latest bulletin per parish on every run, so the
evidence would otherwise be gone by the time the repeat arrives.
"""

from __future__ import annotations

import json
import logging
import subprocess
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.storage import (
    EVENT_HISTORY_PATH,
    EVENTS_PATH,
    load_json_list,
    save_json_list,
)
from pdf_extract.timeparse import normalize_event_date, time_to_minutes

LOGGER = logging.getLogger(__name__)

# How many consecutive earlier weeks must contain the same slot before a dated
# event is treated as weekly. 2 means "printed on this weekday at this time for
# each of the past two weeks as well", i.e. three sightings a week apart.
MIN_PRIOR_WEEKS = 2

# How far back the chain of preceding weeks is followed. Only a cap on the
# work: the chain stops at the first week with no matching sighting, because a
# gap is exactly what separates a weekly slot from a fortnightly or monthly one
# (parishes really do rotate an 11:00 AM Mass between churches week to week).
LOOKBACK_WEEKS = 8

# Occurrences older than this are dropped from event_history.json; they can no
# longer contribute to any future match.
HISTORY_RETENTION_WEEKS = 26

WEEKDAY_NAMES = (
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
)
_WEEKDAY_INDEX = {name.lower(): idx for idx, name in enumerate(WEEKDAY_NAMES)}

# (church_slug, event_type, weekday index, start time in minutes). End time is
# deliberately excluded: bulletins print "9:00 AM" one week and "9:00-10:00 AM"
# the next for the same slot.
SlotKey = tuple[str, str, int, int]


# ── History records ─────────────────────────────────────────────────────────
def load_history(path: Path = EVENT_HISTORY_PATH) -> list[dict[str, Any]]:
    records = load_json_list(path)
    return [r for r in records if isinstance(r, dict)]


def save_history(history: list[dict[str, Any]], path: Path = EVENT_HISTORY_PATH) -> None:
    save_json_list(path, history)


def observation_from_row(row: dict[str, Any]) -> dict[str, Any] | None:
    """Turn an events.json row into a history record, or None if unusable.

    Only uncancelled specific-date events with a parseable date and start time
    are evidence of recurrence: weekly rows are already weekly, and a
    cancellation is dated by nature.
    """
    if not isinstance(row, dict):
        return None
    if row.get("event_kind") != "specific_date" or row.get("cancelled"):
        return None
    church_slug = row.get("church_slug")
    event_type = row.get("event_type")
    if not isinstance(church_slug, str) or not isinstance(event_type, str):
        return None
    if not church_slug or not event_type:
        return None
    iso_date = normalize_event_date(row.get("date"))
    start_minutes = time_to_minutes(row.get("start_time"))
    if iso_date is None or start_minutes is None:
        return None
    return {
        "church_slug": church_slug,
        "event_type": event_type,
        "date": iso_date,
        "start_time": start_minutes,
    }


def _record_key(record: dict[str, Any]) -> tuple[str, str, str, int] | None:
    church_slug = record.get("church_slug")
    event_type = record.get("event_type")
    iso_date = record.get("date")
    start_time = record.get("start_time")
    if not isinstance(church_slug, str) or not isinstance(event_type, str):
        return None
    if not isinstance(iso_date, str) or not isinstance(start_time, int):
        return None
    return (iso_date, church_slug, event_type, start_time)


def record_observations(history: list[dict[str, Any]], rows: list[dict[str, Any]]) -> int:
    """Add the dated occurrences in `rows` to `history` in place.

    Duplicate occurrences (the same slot on the same date, seen in an earlier
    run or twice in one bulletin) are ignored. Returns the number added.
    """
    known = {key for key in (_record_key(r) for r in history) if key is not None}
    added = 0
    for row in rows:
        record = observation_from_row(row)
        if record is None:
            continue
        key = _record_key(record)
        if key is None or key in known:
            continue
        known.add(key)
        history.append(record)
        added += 1
    if added:
        history.sort(key=lambda r: _record_key(r) or ("", "", "", 0))
    return added


def prune_history(
    history: list[dict[str, Any]],
    *,
    today: date | None = None,
    retention_weeks: int = HISTORY_RETENTION_WEEKS,
) -> int:
    """Drop occurrences too old to affect any future match. Returns rows removed.

    The cutoff is measured back from the newest occurrence on file rather than
    from the wall clock, so a corpus that is replayed or backfilled long after
    the fact keeps its most recent weeks instead of being wiped. Pass `today`
    to push the cutoff forward to the current date as well.
    """
    if not history:
        return 0
    dates = [d for d in (_parse_date(r.get("date")) for r in history) if d is not None]
    if not dates:
        return 0
    anchor = max(dates)
    if today is not None:
        anchor = max(anchor, today)
    cutoff = anchor - timedelta(weeks=retention_weeks)

    kept = []
    for record in history:
        record_date = _parse_date(record.get("date"))
        if record_date is not None and record_date >= cutoff:
            kept.append(record)
    removed = len(history) - len(kept)
    if removed:
        history[:] = kept
    return removed


def _parse_date(value: Any) -> date | None:
    iso = normalize_event_date(value) if isinstance(value, str) else None
    if iso is None:
        return None
    return date.fromisoformat(iso)


# ── Promotion ───────────────────────────────────────────────────────────────
def build_slot_index(history: list[dict[str, Any]]) -> dict[SlotKey, set[date]]:
    """Index history as slot -> set of dates that slot was seen on."""
    index: dict[SlotKey, set[date]] = {}
    for record in history:
        record_date = _parse_date(record.get("date"))
        start_time = record.get("start_time")
        church_slug = record.get("church_slug")
        event_type = record.get("event_type")
        if record_date is None or not isinstance(start_time, int):
            continue
        if not isinstance(church_slug, str) or not isinstance(event_type, str):
            continue
        key: SlotKey = (church_slug, event_type, record_date.weekday(), start_time)
        index.setdefault(key, set()).add(record_date)
    return index


def consecutive_prior_weeks(
    index: dict[SlotKey, set[date]], key: SlotKey, event_date: date,
) -> int:
    """Count unbroken weeks before `event_date` that also saw this slot.

    Counting stops at the first missing week: a slot seen two and four weeks
    ago but not one or three weeks ago is fortnightly, not weekly.
    """
    seen = index.get(key)
    if not seen:
        return 0
    weeks = 0
    for weeks_back in range(1, LOOKBACK_WEEKS + 1):
        if event_date - timedelta(weeks=weeks_back) not in seen:
            break
        weeks += 1
    return weeks


def _weekly_key(row: dict[str, Any]) -> SlotKey | None:
    """Slot key for an already-weekly row, used to avoid promoting a duplicate."""
    if row.get("event_kind") != "weekly" or row.get("cancelled"):
        return None
    church_slug = row.get("church_slug")
    event_type = row.get("event_type")
    day_of_week = row.get("day_of_week")
    if not isinstance(church_slug, str) or not isinstance(event_type, str):
        return None
    if not isinstance(day_of_week, str):
        return None
    weekday = _WEEKDAY_INDEX.get(day_of_week.strip().lower())
    if weekday is None:
        return None
    start_minutes = time_to_minutes(row.get("start_time"))
    if start_minutes is None:
        return None
    return (church_slug, event_type, weekday, start_minutes)


def _promote(row: dict[str, Any], weekday: int) -> dict[str, Any]:
    promoted = dict(row)
    promoted["event_kind"] = "weekly"
    promoted["day_of_week"] = WEEKDAY_NAMES[weekday]
    promoted["date"] = None
    return promoted


def promote_recurring_events(
    rows: list[dict[str, Any]], history: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], int]:
    """Rewrite dated rows that repeat weekly as weekly rows.

    A row is promoted when the same church, event type, weekday and start time
    appear in `history` in each of the MIN_PRIOR_WEEKS weeks immediately before
    it. A promoted row that duplicates a weekly row already present in
    `rows` is dropped instead, so the parish does not gain two copies of the
    same slot.

    Returns the rewritten rows and the number of dated rows promoted (including
    ones dropped as duplicates).
    """
    index = build_slot_index(history)
    weekly_keys = {key for key in (_weekly_key(r) for r in rows) if key is not None}

    out: list[dict[str, Any]] = []
    promoted_count = 0
    for row in rows:
        observation = observation_from_row(row)
        if observation is None:
            out.append(row)
            continue
        event_date = date.fromisoformat(observation["date"])
        key: SlotKey = (
            observation["church_slug"],
            observation["event_type"],
            event_date.weekday(),
            observation["start_time"],
        )
        if consecutive_prior_weeks(index, key, event_date) < MIN_PRIOR_WEEKS:
            out.append(row)
            continue

        promoted_count += 1
        if key in weekly_keys:
            LOGGER.info(
                "Dropping dated %s at %s on %s: already a weekly slot",
                observation["event_type"], observation["church_slug"], observation["date"],
            )
            continue
        weekly_keys.add(key)
        LOGGER.info(
            "Promoting dated %s at %s on %s to weekly (%s %s)",
            observation["event_type"], observation["church_slug"], observation["date"],
            WEEKDAY_NAMES[event_date.weekday()], row.get("start_time"),
        )
        out.append(_promote(row, event_date.weekday()))
    return out, promoted_count


# ── Pipeline entry points ───────────────────────────────────────────────────
def apply_recurrence(
    events_path: Path = EVENTS_PATH, history_path: Path = EVENT_HISTORY_PATH,
) -> dict[str, int]:
    """Re-run promotion over the current events.json.

    `process` already promotes each bulletin as it merges it, so this is for
    applying a backfilled history (or a changed threshold) to events that were
    processed before the evidence existed.
    """
    events = load_json_list(events_path)
    history = load_history(history_path)
    if not events:
        LOGGER.info("No events at %s, nothing to promote", events_path)
        return {"events": 0, "promoted": 0}

    # Promotion dedupes against weekly rows for the same parish only, so group
    # by bulletin: rows from different bulletins never describe the same slot.
    by_bulletin: dict[Any, list[dict[str, Any]]] = {}
    for row in events:
        by_bulletin.setdefault(row.get("bulletin_source_url"), []).append(row)

    promoted_total = 0
    out: list[dict[str, Any]] = []
    for rows in by_bulletin.values():
        promoted_rows, promoted = promote_recurring_events(rows, history)
        promoted_total += promoted
        out.extend(promoted_rows)

    if promoted_total:
        save_json_list(events_path, out)
    LOGGER.info("Recurrence apply: %d of %d events promoted to weekly", promoted_total, len(events))
    return {"events": len(out), "promoted": promoted_total}


def backfill_history_from_git(
    *,
    events_path: Path = EVENTS_PATH,
    history_path: Path = EVENT_HISTORY_PATH,
    limit: int | None = None,
) -> dict[str, int]:
    """Seed event_history.json from past committed revisions of events.json.

    The weekly pipeline commits a fresh events.json every run, so git already
    holds the sightings the history file was never around to record. Without
    this the detector needs MIN_PRIOR_WEEKS of new runs before it can promote
    anything.
    """
    history = load_history(history_path)
    before = len(history)

    revisions = _git_revisions(events_path, limit=limit)
    scanned = 0
    for revision in revisions:
        rows = _git_show_json(revision, events_path)
        if rows is None:
            continue
        scanned += 1
        record_observations(history, rows)

    # The working copy may be ahead of the last commit.
    record_observations(history, load_json_list(events_path))

    prune_history(history)
    save_history(history, history_path)
    added = len(history) - before
    LOGGER.info(
        "Backfilled event history from %d revisions of %s: %d new occurrences (%d total)",
        scanned, events_path, added, len(history),
    )
    return {"revisions": scanned, "added": added, "occurrences": len(history)}


def _git_revisions(path: Path, *, limit: int | None = None) -> list[str]:
    args = ["git", "log", "--format=%H"]
    if limit is not None:
        args.append(f"--max-count={limit}")
    args += ["--", path.as_posix()]
    completed = subprocess.run(args, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"git log failed: {completed.stderr.strip()}")
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def _git_show_json(revision: str, path: Path) -> list[dict[str, Any]] | None:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path.as_posix()}"],
        capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0:
        LOGGER.debug("Skipping %s: %s not readable at that revision", revision, path)
        return None
    try:
        rows = json.loads(completed.stdout)
    except json.JSONDecodeError:
        LOGGER.warning("Skipping %s: %s is not valid JSON at that revision", revision, path)
        return None
    if not isinstance(rows, list):
        return None
    return [r for r in rows if isinstance(r, dict)]
