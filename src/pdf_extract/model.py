"""The schedule's vocabulary, shared by every part of the pipeline.

An event is a Mass, Confession or Adoration, weekly or on one date. A weekly
event can be limited to some weeks of the month (`weeks_of_month`, the same
tokens and ranges `schedule_pattern` uses) and to a season. `weeks_of_month`
lists the weeks an event happens on, or, with `exclude_weeks` true, the weeks
it doesn't: "every Sunday except the last" is `["last"]` excluded, which no
list of the weeks that remain can say.

A schedule entry is one event written down this way (`ENTRY_KEYS`,
`validate_entry`). A seed (`pdf_extract.seeding`) holds entries in this shape,
and a label event (`pdf_extract.labeling.labels`) is an entry plus the keys
that describe one reading of one bulletin.

This module sits at the bottom of the package: it imports nothing from
`pdf_extract` but `timeparse`, so the schedule, the seeds, the labeler and the
evals can all import it without importing each other.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, date, datetime, time
from hashlib import sha256
from typing import Any

from pdf_extract.timeparse import normalize_event_date, time_to_minutes

EVENT_TYPES = ("mass", "confession", "adoration")
EVENT_KINDS = ("weekly", "specific_date")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
WEEKS_OF_MONTH = ("first", "second", "third", "fourth", "fifth", "last")
# The ordinals a month can have of a weekday; "last" is the fourth or the fifth.
ORDINAL_WEEKS = WEEKS_OF_MONTH[:5]

# February has 29: a season boundary recurs every year, leap years included.
DAYS_IN_MONTH = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
SEASON_KEYS = ("start_month", "start_day", "end_month", "end_day")

ENTRY_KEYS = (
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "weeks_of_month", "exclude_weeks", "season", "note",
)
# Keys an entry written before they existed may lack; a missing one reads as
# false.
ENTRY_KEYS_ADDED_LATER = ("exclude_weeks",)

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ── Weeks of the month ──────────────────────────────────────────────────────
def canonical_weeks(weeks: Any, exclude: Any) -> tuple[list[str], bool]:
    """The one way to write a weeks-of-the-month selection, in the labels' order.

    An exclusion that leaves out no "last" is the list of the weeks that
    remain ("every week except the first" is second to fifth). One that leaves
    out "last" stays an exclusion, without "fifth" (a fifth weekday is always
    the last). Excluding nothing is every week, and a selection that leaves no
    week (`weeks_never_happen`) is kept as given. Unknown tokens are dropped.
    """
    listed = set(weeks) if isinstance(weeks, list) else set()
    ordered = [w for w in WEEKS_OF_MONTH if w in listed]
    if exclude is not True or not ordered:
        return ordered, False
    if weeks_never_happen(ordered, True):
        return ordered, True
    if "last" not in listed:
        return [w for w in ORDINAL_WEEKS if w not in listed], False
    return [w for w in ordered if w != "fifth"], True


def weeks_never_happen(weeks: Any, exclude: Any) -> bool:
    """Whether a selection leaves no week at all: every ordinal, or the first four and the last, excluded."""
    listed = set(weeks) if isinstance(weeks, list) else set()
    return exclude is True and set(ORDINAL_WEEKS[:4]) <= listed and bool({"fifth", "last"} & listed)


# ── Identifiers ─────────────────────────────────────────────────────────────
def is_valid_slug(value: Any) -> bool:
    return isinstance(value, str) and len(value) <= 120 and bool(_SLUG_RE.match(value))


def is_valid_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_HASH_RE.match(value))


# ── Validation ──────────────────────────────────────────────────────────────
def is_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or not _DATE_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def check_keys(
    obj: dict[str, Any], expected: tuple[str, ...], where: str, *, may_lack: tuple[str, ...] = (),
) -> list[str]:
    """The keys `obj` is missing or has beyond `expected`, as error messages."""
    errors = []
    missing = [k for k in expected if k not in obj and k not in may_lack]
    extra = sorted(k for k in obj if k not in expected)
    if missing:
        errors.append(f"{where}: missing {', '.join(missing)}")
    if extra:
        errors.append(f"{where}: unknown {', '.join(extra)}")
    return errors


def _validate_season(season: Any, where: str) -> list[str]:
    if season is None:
        return []
    if not isinstance(season, dict):
        return [f"{where}.season must be null or an object"]
    errors = check_keys(season, SEASON_KEYS, f"{where}.season")
    if errors:
        return errors
    for edge in ("start", "end"):
        month = season[f"{edge}_month"]
        day = season[f"{edge}_day"]
        if not is_int(month) or not 1 <= month <= 12:
            errors.append(f"{where}.season.{edge}_month must be 1-12")
            continue
        if day is not None and (not is_int(day) or not 1 <= day <= DAYS_IN_MONTH[month - 1]):
            errors.append(f"{where}.season.{edge}_day must be null or a day of month {month}")
    return errors


def entry_value_errors(entry: dict[str, Any], where: str) -> list[str]:
    """Every reason the values of `entry`, whose keys are already checked, are not an entry's."""
    errors = []
    if not is_valid_slug(entry["church_slug"]):
        errors.append(f"{where}.church_slug must be a church slug")
    if entry["event_type"] not in EVENT_TYPES:
        errors.append(f"{where}.event_type must be one of {', '.join(EVENT_TYPES)}")
    kind = entry["event_kind"]
    if kind not in EVENT_KINDS:
        errors.append(f"{where}.event_kind must be one of {', '.join(EVENT_KINDS)}")
    elif kind == "weekly":
        if entry["day_of_week"] not in DAYS:
            errors.append(f"{where}.day_of_week must be a weekday name for a weekly event")
        if entry["date"] is not None:
            errors.append(f"{where}.date must be null for a weekly event")
    else:
        if entry["day_of_week"] is not None:
            errors.append(f"{where}.day_of_week must be null for a dated event")
        if not is_iso_date(entry["date"]):
            errors.append(f"{where}.date must be YYYY-MM-DD for a dated event")

    if not isinstance(entry["start_time"], str) or not _TIME_RE.match(entry["start_time"]):
        errors.append(f"{where}.start_time must be HH:MM (24-hour)")
    end = entry["end_time"]
    if end is not None and (not isinstance(end, str) or not _TIME_RE.match(end)):
        errors.append(f"{where}.end_time must be null or HH:MM (24-hour)")
    if not isinstance(entry["cancelled"], bool):
        errors.append(f"{where}.cancelled must be true or false")

    weeks = entry["weeks_of_month"]
    if not isinstance(weeks, list) or any(w not in WEEKS_OF_MONTH for w in weeks):
        errors.append(f"{where}.weeks_of_month must be a list of {', '.join(WEEKS_OF_MONTH)}")
    elif len(set(weeks)) != len(weeks):
        errors.append(f"{where}.weeks_of_month has duplicates")
    elif weeks and kind == "specific_date":
        errors.append(f"{where}.weeks_of_month applies to weekly events only")
    exclude = entry.get("exclude_weeks", False)
    if not isinstance(exclude, bool):
        errors.append(f"{where}.exclude_weeks must be true or false")
    elif exclude and not weeks:
        errors.append(f"{where}.exclude_weeks needs the weeks it leaves out in weeks_of_month")
    elif exclude and weeks_never_happen(weeks, exclude):
        errors.append(f"{where}.exclude_weeks leaves out every week")
    errors.extend(_validate_season(entry["season"], where))
    if entry["season"] is not None and kind == "specific_date":
        errors.append(f"{where}.season applies to weekly events only")

    if entry["note"] is not None and not isinstance(entry["note"], str):
        errors.append(f"{where}.note must be null or a string")
    return errors


def validate_entry(entry: Any, where: str) -> list[str]:
    """Every reason `entry` is not a schedule entry (empty when it is one)."""
    if not isinstance(entry, dict):
        return [f"{where} must be an object"]
    errors = check_keys(entry, ENTRY_KEYS, where, may_lack=ENTRY_KEYS_ADDED_LATER)
    if errors:
        return errors
    return entry_value_errors(entry, where)


# ── Canonical forms ─────────────────────────────────────────────────────────
def sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    """Sorted keys, no whitespace: the same value always hashes the same."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def normalize_as_of(value: str) -> str:
    """A seed's `as_of` in the form `fetched_at` is stored in, so the two compare as text.

    Takes an ISO time (`Z` or an offset; none means UTC) or a date, which
    means the end of that day: everything fetched that day is in the seed.
    """
    text = value.strip()
    try:
        if len(text) == 10:
            moment = datetime.combine(date.fromisoformat(text), time(23, 59, 59), UTC)
        else:
            moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=UTC)
    except ValueError as exc:
        raise ValueError(f"as_of must be an ISO date or time, not {value!r}") from exc
    return moment.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ── A classifier's flat events ──────────────────────────────────────────────
def _hhmm(raw: Any) -> str | None:
    minutes = time_to_minutes(raw) if isinstance(raw, str) else None
    return None if minutes is None else f"{minutes // 60:02d}:{minutes % 60:02d}"


def _day(raw: Any) -> str | None:
    if not isinstance(raw, str) or len(raw.strip()) < 2:
        return None
    prefix = raw.strip().lower()[:3]
    return next((d for d in DAYS if d.lower().startswith(prefix)), None)


def _weeks(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    weeks = {str(w).strip().lower() for w in raw}
    return [w for w in WEEKS_OF_MONTH if w in weeks]


def _season(ev: dict[str, Any]) -> dict[str, int | None] | None:
    """A season from the flat `season_*` fields the pipeline adds in schema v2, if any."""
    start, end = ev.get("season_start_month"), ev.get("season_end_month")
    if not (isinstance(start, int) and isinstance(end, int)):
        return None
    if not (1 <= start <= 12 and 1 <= end <= 12):
        return None
    start_day, end_day = ev.get("season_start_day"), ev.get("season_end_day")
    return {
        "start_month": start,
        "start_day": start_day if isinstance(start_day, int) else None,
        "end_month": end,
        "end_day": end_day if isinstance(end_day, int) else None,
    }


def gemini_rows(events: list[Any]) -> list[dict[str, Any]]:
    """Gemini's flat events in the label's row shape, keeping the raw strings.

    `problems` lists what could not be read (an unparseable time, say), so the
    labeler sees it instead of the row silently vanishing.
    """
    out = []
    for i, ev in enumerate(events):
        if not isinstance(ev, dict):
            continue
        event_type = ev.get("type", ev.get("event_type"))
        kind = ev.get("kind", ev.get("event_kind"))
        weekly = kind == "weekly"
        weeks, exclude_weeks = canonical_weeks(
            _weeks(ev.get("weeks_of_month")), ev.get("exclude_weeks") is True,
        ) if weekly else ([], False)
        row = {
            "id": f"g{i}",
            "church_slug": ev.get("church_slug") if isinstance(ev.get("church_slug"), str) else "",
            "event_type": event_type if event_type in EVENT_TYPES else None,
            "event_kind": kind if kind in EVENT_KINDS else None,
            "day_of_week": _day(ev.get("day_of_week")) if weekly else None,
            "date": None if weekly else normalize_event_date(ev.get("date")),
            "start_time": _hhmm(ev.get("start_time")),
            "end_time": _hhmm(ev.get("end_time")),
            "cancelled": bool(ev.get("cancelled", False)),
            "weeks_of_month": weeks,
            "exclude_weeks": exclude_weeks,
            "season": _season(ev) if weekly else None,
            "page_number": ev.get("page_number") if isinstance(ev.get("page_number"), int) else None,
            "note": ev.get("note") if isinstance(ev.get("note"), str) and ev["note"].strip() else None,
            "raw": {
                k: ev.get(k) for k in ("day_of_week", "date", "start_time", "end_time")
                if ev.get(k) is not None
            },
        }
        problems = []
        if row["event_type"] is None:
            problems.append(f"unknown type {event_type!r}")
        if row["event_kind"] is None:
            problems.append(f"unknown kind {kind!r}")
        elif weekly and row["day_of_week"] is None:
            problems.append(f"unreadable day {ev.get('day_of_week')!r}")
        elif not weekly and row["date"] is None:
            problems.append(f"unreadable date {ev.get('date')!r}")
        if row["start_time"] is None:
            problems.append(f"unreadable start time {ev.get('start_time')!r}")
        if ev.get("end_time") and row["end_time"] is None:
            problems.append(f"unreadable end time {ev.get('end_time')!r}")
        row["problems"] = problems
        out.append(row)
    return out
