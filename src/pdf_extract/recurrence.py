"""Promote repeatedly-dated events to weekly ones.

Bulletins are often ambiguous about whether a listing is a one-off or a
standing weekly slot ("Adoration Wednesday at 7:00 PM" printed under this
week's calendar). The extractor has to guess, and when it guesses "one-off" it
files the slot under `single_events` with a single calendar date, so the
frontend shows it as a dated event that disappears the moment it passes.

The tell is that a genuinely weekly slot keeps reappearing: the same church,
the same event type, the same weekday and start time, exactly one week later,
bulletin after bulletin. `data/event_history.json` accumulates every occurrence
the pipeline has extracted, and `promote_recurring_events` rewrites a dated
event as a weekly one once matching occurrences show up in each of the
`MIN_PRIOR_WEEKS` weeks immediately before it.

Weekly extractions count towards that chain as much as dated ones. The
extractor is not consistent from week to week — on the current corpus, 173 of
1488 slots have been filed both ways at some point — so a slot that alternates
would otherwise never accumulate two consecutive dated sightings and would
never be promoted, even after the bulletin had listed it in its weekly
schedule for two months. A weekly row carries no date, so it is credited to
the week its bulletin covers: the first matching weekday on or after the
bulletin's published date.

The history file is the pipeline's only memory of past bulletins: `events.json`
is compacted down to the latest bulletin per parish on every run, so the
evidence would otherwise be gone by the time the repeat arrives.
"""

from __future__ import annotations

import json
import logging
import subprocess
from collections.abc import Set as AbstractSet
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.storage import (
    BULLETINS_METADATA_PATH,
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

# Occurrences older than this are dropped from event_history.json; past the
# lookback window they can no longer contribute to any match.
HISTORY_RETENTION_WEEKS = 12

WEEKDAY_NAMES = (
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
)
_WEEKDAY_INDEX = {name.lower(): idx for idx, name in enumerate(WEEKDAY_NAMES)}

# (church_slug, event_type, start time in minutes). The weekday is not part of
# the key: occurrences are matched at exact seven-day offsets, which can only
# ever line up on the same weekday. End time is excluded too, because bulletins
# print "9:00 AM" one week and "9:00-10:00 AM" the next for the same slot.
SlotKey = tuple[str, str, int]

# slot -> the dates that slot was seen on.
History = dict[SlotKey, set[date]]


# ── History file ────────────────────────────────────────────────────────────
def load_history(path: Path = EVENT_HISTORY_PATH) -> History:
    """Read event_history.json into slot -> dates.

    Records are grouped by slot on disk rather than stored one per occurrence:
    with weekly sightings included this file covers every event in the corpus
    every week, and the grouped form keeps it a few hundred KB instead of a few
    MB of near-identical rows.
    """
    history: History = {}
    for record in load_json_list(path):
        if not isinstance(record, dict):
            continue
        key = _slot_key(
            record.get("church_slug"), record.get("event_type"), record.get("start_time"),
        )
        if key is None:
            continue
        dates = record.get("dates")
        if not isinstance(dates, list):
            continue
        parsed = {d for d in (_parse_date(value) for value in dates) if d is not None}
        if parsed:
            history.setdefault(key, set()).update(parsed)
    return history


def save_history(history: History, path: Path = EVENT_HISTORY_PATH) -> None:
    records = [
        {
            "church_slug": church_slug,
            "event_type": event_type,
            "start_time": start_time,
            "dates": [d.isoformat() for d in sorted(dates)],
        }
        for (church_slug, event_type, start_time), dates in sorted(history.items())
        if dates
    ]
    save_json_list(path, records)


def _slot_key(church_slug: Any, event_type: Any, start_time: Any) -> SlotKey | None:
    if not isinstance(church_slug, str) or not church_slug:
        return None
    if not isinstance(event_type, str) or not event_type:
        return None
    if not isinstance(start_time, int) or isinstance(start_time, bool):
        return None
    return (church_slug, event_type, start_time)


def _parse_date(value: Any) -> date | None:
    iso = normalize_event_date(value) if isinstance(value, str) else None
    return date.fromisoformat(iso) if iso else None


# ── Recording occurrences ───────────────────────────────────────────────────
def bulletin_reference_date(entry: dict[str, Any]) -> date | None:
    """The date a bulletin's week starts from, for crediting its weekly rows.

    Prefers the issue date the extractor read off the bulletin itself. When
    that is missing the fetch date stands in, snapped to the nearest Sunday.
    The raw fetch date cannot be used as-is: it lands anywhere from the day
    before publication to three days after, and for a Sunday weekly row that is
    the difference between crediting the bulletin's own Sunday and the next
    one — a whole week. Since 58 of the corpus's 59 parishes have some
    bulletins with an issue date and some without, an unsnapped fallback breaks
    those parishes' chains wherever the two kinds meet.

    Snapping to the *nearest* Sunday rather than the preceding one matters:
    bulletins are fetched on the Saturday before publication as often as on the
    Monday after, and rounding a Saturday backwards would land a full week
    early.
    """
    published = _parse_date(entry.get("published_date"))
    if published is not None:
        return published
    fetched_at = entry.get("fetched_at")
    if not isinstance(fetched_at, str) or not fetched_at:
        return None
    fetched = _parse_date(fetched_at[:10])
    return None if fetched is None else _nearest_sunday(fetched)


def _nearest_sunday(day: date) -> date:
    """The Sunday of the week `day` belongs to, rounding Thursday forwards."""
    forward = (6 - day.weekday()) % 7
    return day + timedelta(days=forward) if forward <= 3 else day - timedelta(days=7 - forward)


def occurrence_from_row(
    row: dict[str, Any], *, bulletin_date: date | None,
) -> tuple[SlotKey, date] | None:
    """Turn an events.json row into a (slot, date) occurrence, or None.

    Dated rows are credited to their own date. Weekly rows are credited to the
    first matching weekday on or after `bulletin_date`, i.e. the occurrence the
    bulletin was actually announcing. Cancellations are never evidence of
    recurrence.
    """
    if not isinstance(row, dict) or row.get("cancelled"):
        return None
    key = _slot_key(
        row.get("church_slug"),
        row.get("event_type"),
        time_to_minutes(row.get("start_time")),
    )
    if key is None:
        return None

    kind = row.get("event_kind")
    if kind == "specific_date":
        occurred = _parse_date(row.get("date"))
        return (key, occurred) if occurred else None
    if kind == "weekly":
        if bulletin_date is None:
            return None
        day_of_week = row.get("day_of_week")
        if not isinstance(day_of_week, str):
            return None
        weekday = _WEEKDAY_INDEX.get(day_of_week.strip().lower())
        if weekday is None:
            return None
        offset = (weekday - bulletin_date.weekday()) % 7
        return (key, bulletin_date + timedelta(days=offset))
    return None


def record_observations(
    history: History, rows: list[dict[str, Any]], *, bulletin_date: date | None,
) -> int:
    """Add the occurrences in `rows` to `history` in place.

    Occurrences already on file (seen in an earlier run, or listed twice in one
    bulletin) are ignored. Returns the number added.
    """
    added = 0
    for row in rows:
        occurrence = occurrence_from_row(row, bulletin_date=bulletin_date)
        if occurrence is None:
            continue
        key, occurred = occurrence
        dates = history.setdefault(key, set())
        if occurred not in dates:
            dates.add(occurred)
            added += 1
    return added


def prune_history(
    history: History,
    *,
    today: date | None = None,
    retention_weeks: int = HISTORY_RETENTION_WEEKS,
) -> int:
    """Drop occurrences too old to affect any future match. Returns dates removed.

    The cutoff runs back from today, or from the newest occurrence on file when
    that is older — so a corpus replayed or backfilled long after the fact keeps
    its most recent weeks instead of being wiped. It deliberately does not run
    back from the newest occurrence when that is in the *future*: bulletins
    announce events months ahead, and anchoring on those would prune away the
    recent weeks the whole chain depends on. Future occurrences themselves are
    always kept.
    """
    newest = max((max(dates) for dates in history.values() if dates), default=None)
    if newest is None:
        history.clear()
        return 0
    anchor = min(newest, today if today is not None else date.today())
    cutoff = anchor - timedelta(weeks=retention_weeks)

    removed = 0
    for key in list(history):
        dates = history[key]
        kept = {d for d in dates if d >= cutoff}
        removed += len(dates) - len(kept)
        if kept:
            history[key] = kept
        else:
            del history[key]
    return removed


# ── Promotion ───────────────────────────────────────────────────────────────
def consecutive_prior_weeks(
    history: History,
    key: SlotKey,
    event_date: date,
    *,
    exclude: AbstractSet[date] = frozenset(),
) -> int:
    """Count unbroken weeks before `event_date` that also saw this slot.

    Counting stops at the first missing week: a slot seen two and four weeks
    ago but not one or three weeks ago is fortnightly, not weekly.

    `exclude` drops dates that must not count as independent evidence — see
    `promote_recurring_events`, which passes the bulletin's own sightings.
    """
    seen = history.get(key)
    if not seen:
        return 0
    weeks = 0
    for weeks_back in range(1, LOOKBACK_WEEKS + 1):
        candidate = event_date - timedelta(weeks=weeks_back)
        if candidate not in seen or candidate in exclude:
            break
        weeks += 1
    return weeks


def _weekly_slot(row: dict[str, Any]) -> tuple[SlotKey, int] | None:
    """Slot and weekday of an already-weekly row, used to avoid a duplicate.

    Cancelled weekly rows count: the slot is still spoken for, and adding a
    second, live weekly row beside the cancellation would leave the parish
    contradicting itself about the same weekday and time.
    """
    if row.get("event_kind") != "weekly":
        return None
    key = _slot_key(
        row.get("church_slug"),
        row.get("event_type"),
        time_to_minutes(row.get("start_time")),
    )
    day_of_week = row.get("day_of_week")
    if key is None or not isinstance(day_of_week, str):
        return None
    weekday = _WEEKDAY_INDEX.get(day_of_week.strip().lower())
    return None if weekday is None else (key, weekday)


def _promote(row: dict[str, Any], weekday: int) -> dict[str, Any]:
    promoted = dict(row)
    promoted["event_kind"] = "weekly"
    promoted["day_of_week"] = WEEKDAY_NAMES[weekday]
    promoted["date"] = None
    return promoted


def promote_recurring_events(
    rows: list[dict[str, Any]], history: History,
) -> tuple[list[dict[str, Any]], int]:
    """Rewrite dated rows that repeat weekly as weekly rows.

    A row is promoted when the same church, event type, weekday and start time
    appear in `history` in each of the MIN_PRIOR_WEEKS weeks immediately before
    it. A promoted row that duplicates a weekly row already present in `rows`
    is dropped instead, so the parish does not gain two copies of the slot.

    A bulletin's own dated rows are not evidence for that same bulletin. One
    that prints a slot on three consecutive dates — a six-week Lenten fish fry,
    a summer novena — describes a finite series, not a standing weekly slot,
    and without this it would promote itself to an open-ended weekly on first
    sight. Evidence has to come from a week this bulletin did not itself list.

    Returns the rewritten rows and the number of dated rows promoted (including
    ones dropped as duplicates).
    """
    weekly_slots = {slot for slot in (_weekly_slot(r) for r in rows) if slot is not None}

    own_dates: dict[SlotKey, set[date]] = {}
    for row in rows:
        if row.get("event_kind") != "specific_date":
            continue
        occurrence = occurrence_from_row(row, bulletin_date=None)
        if occurrence is not None:
            own_dates.setdefault(occurrence[0], set()).add(occurrence[1])

    out: list[dict[str, Any]] = []
    promoted_count = 0
    for row in rows:
        occurrence = (
            occurrence_from_row(row, bulletin_date=None)
            if row.get("event_kind") == "specific_date"
            else None
        )
        if occurrence is None:
            out.append(row)
            continue
        key, event_date = occurrence
        prior = consecutive_prior_weeks(
            history, key, event_date, exclude=own_dates.get(key, frozenset()),
        )
        if prior < MIN_PRIOR_WEEKS:
            out.append(row)
            continue

        promoted_count += 1
        weekday = event_date.weekday()
        if (key, weekday) in weekly_slots:
            LOGGER.info(
                "Dropping dated %s at %s on %s: already a weekly slot",
                key[1], key[0], event_date,
            )
            continue
        weekly_slots.add((key, weekday))
        LOGGER.info(
            "Promoting dated %s at %s on %s to weekly (%s %s)",
            key[1], key[0], event_date, WEEKDAY_NAMES[weekday], row.get("start_time"),
        )
        out.append(_promote(row, weekday))
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
    metadata_path: Path = BULLETINS_METADATA_PATH,
    limit: int | None = None,
) -> dict[str, int]:
    """Seed event_history.json from past committed revisions of events.json.

    The weekly pipeline commits a fresh events.json every run, so git already
    holds the sightings the history file was never around to record. Without
    this the detector needs MIN_PRIOR_WEEKS of new runs before it can promote
    anything.
    """
    history = load_history(history_path)
    reference_dates = _reference_dates_by_source_url(metadata_path)

    revisions = _git_revisions(events_path, limit=limit)
    scanned = 0
    added = 0
    for revision in revisions:
        rows = _git_show_json(revision, events_path)
        if rows is None:
            continue
        scanned += 1
        added += _record_by_bulletin(history, rows, reference_dates)

    # The working copy may be ahead of the last commit.
    added += _record_by_bulletin(history, load_json_list(events_path), reference_dates)

    prune_history(history)
    save_history(history, history_path)
    occurrences = sum(len(dates) for dates in history.values())
    LOGGER.info(
        "Backfilled event history from %d revisions of %s: %d new occurrences "
        "(%d occurrences across %d slots)",
        scanned, events_path, added, occurrences, len(history),
    )
    return {
        "revisions": scanned,
        "added": added,
        "occurrences": occurrences,
        "slots": len(history),
    }


def _reference_dates_by_source_url(metadata_path: Path) -> dict[str, date]:
    """Map each bulletin's source URL to the date its week starts from."""
    reference_dates: dict[str, date] = {}
    for entry in load_json_list(metadata_path):
        if not isinstance(entry, dict):
            continue
        source_url = entry.get("source_url")
        reference = bulletin_reference_date(entry)
        if isinstance(source_url, str) and source_url and reference is not None:
            reference_dates[source_url] = reference
    return reference_dates


def _record_by_bulletin(
    history: History, rows: list[dict[str, Any]], reference_dates: dict[str, date],
) -> int:
    """Record rows a bulletin at a time, so each gets its own reference date."""
    by_bulletin: dict[Any, list[dict[str, Any]]] = {}
    for row in rows:
        if isinstance(row, dict):
            by_bulletin.setdefault(row.get("bulletin_source_url"), []).append(row)
    added = 0
    for source_url, bulletin_rows in by_bulletin.items():
        reference = reference_dates.get(source_url) if isinstance(source_url, str) else None
        added += record_observations(history, bulletin_rows, bulletin_date=reference)
    return added


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
