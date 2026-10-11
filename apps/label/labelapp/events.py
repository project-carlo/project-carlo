"""Event identity, logical-field diffing, and display helpers.

Identity is `pdf_extract.compare.event_key` — the same tuple the classifier
comparison uses — so a label written here scores directly against a run.

On top of that, events are diffed by *logical* field rather than by raw column.
`event_kind`, `day_of_week` and `date` collapse into a single `when` field
because they always move together: the extractor filing a standing Sunday slot
under one calendar date changes three columns at once, and a reader comparing
two readings is looking at one difference, not three.

Within `when`, the weekly-vs-dated axis is treated as undetermined rather than
as a disagreement. Whether a listing is a standing slot or a one-off is rarely
decidable from a single bulletin, and the pipeline already answers it elsewhere:
`pdf_extract.recurrence` promotes a dated event to weekly once the same slot
turns up in the preceding weeks of `data/event_history.json`. `is_when_variant`
identifies that pair so `labelapp.candidates` can fold it into one candidate and
`labelapp.score` can decline to score it.
"""

from __future__ import annotations

import json
from datetime import date as date_cls
from hashlib import sha1
from typing import Any

from pdf_extract.compare import EventKey, event_key

# Logical fields, in the order they read on a card.
FIELD_CHURCH = "church"
FIELD_TYPE = "type"
FIELD_WHEN = "when"
FIELD_START = "start"
FIELD_END = "end"
FIELD_CANCELLED = "cancelled"

FIELD_LABELS: dict[str, str] = {
    FIELD_CHURCH: "church",
    FIELD_TYPE: "event type",
    FIELD_WHEN: "day or date",
    FIELD_START: "start time",
    FIELD_END: "end time",
    FIELD_CANCELLED: "cancelled",
}

# The columns a ground-truth event carries. Anything else on a candidate dict
# (sources, page numbers, notes) is commentary and never part of identity.
EVENT_FIELDS = (
    "church_slug",
    "event_type",
    "event_kind",
    "day_of_week",
    "date",
    "start_time",
    "end_time",
    "cancelled",
)

_WEEKDAY_NAMES = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


def key_id(key: EventKey) -> str:
    """Stable short id for an event key.

    A pure function of the key itself, so verdicts recorded today still line up
    after another classifier joins the comparison and the candidate list grows.
    """
    payload = json.dumps(list(key), ensure_ascii=False, sort_keys=True)
    return sha1(payload.encode("utf-8")).hexdigest()[:16]


def event_id(event: dict[str, Any]) -> str:
    return key_id(event_key(event))


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    """Reduce an event dict to the identity columns, with consistent types."""
    kind = str(event.get("event_kind") or "")
    day_of_week = event.get("day_of_week")
    date_value = event.get("date")
    return {
        "church_slug": str(event.get("church_slug") or ""),
        "event_type": str(event.get("event_type") or ""),
        "event_kind": kind,
        "day_of_week": day_of_week if isinstance(day_of_week, str) and day_of_week else None,
        "date": date_value if isinstance(date_value, str) and date_value else None,
        "start_time": str(event.get("start_time") or ""),
        "end_time": event.get("end_time") if isinstance(event.get("end_time"), str) else None,
        "cancelled": bool(event.get("cancelled", False)),
    }


def logical_fields(event: dict[str, Any]) -> dict[str, Any]:
    """Project an event onto the fields a human actually decides between."""
    normalized = normalize_event(event)
    return {
        FIELD_CHURCH: normalized["church_slug"],
        FIELD_TYPE: normalized["event_type"],
        FIELD_WHEN: (
            normalized["event_kind"],
            normalized["day_of_week"],
            normalized["date"],
        ),
        FIELD_START: normalized["start_time"],
        FIELD_END: normalized["end_time"],
        FIELD_CANCELLED: normalized["cancelled"],
    }


def differing_fields(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    """Logical field names on which two events disagree."""
    fields_a = logical_fields(a)
    fields_b = logical_fields(b)
    return [name for name, value in fields_a.items() if value != fields_b[name]]


def weekday_of(date_value: str | None) -> str | None:
    """Weekday name for a `YYYY-MM-DD` string, or None if it will not parse."""
    if not isinstance(date_value, str):
        return None
    try:
        parsed = date_cls.fromisoformat(date_value.strip())
    except ValueError:
        return None
    return _WEEKDAY_NAMES[parsed.weekday()]


def when_slot_key(event: dict[str, Any]) -> tuple[Any, ...] | None:
    """Identity of the schedule slot an event fills, ignoring weekly-vs-dated.

    The `when` axis collapses to the weekday both readings share, so a standing
    Sunday slot and a Mass dated to a Sunday produce the same key. None when no
    weekday can be resolved — a weekly row with no day, or a date that will not
    parse — because there is then nothing to line the two readings up on.
    """
    normalized = normalize_event(event)
    if normalized["event_kind"] == "weekly":
        weekday = normalized["day_of_week"]
    else:
        weekday = weekday_of(normalized["date"])
    if not weekday:
        return None
    return (
        normalized["church_slug"],
        normalized["event_type"],
        weekday,
        normalized["start_time"],
        normalized["end_time"],
        normalized["cancelled"],
    )


def is_when_variant(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Whether two events are one slot filed as weekly by one reading and as a
    single date on that same weekday by the other.

    This is the extractor's most common split, and not one a labeler can settle:
    "Adoration Wednesday at 7:00 PM" printed under this week's calendar reads
    both ways from a single bulletin. `pdf_extract.recurrence` settles it from
    history instead, so everything here treats the two readings as the same slot.
    """
    kinds = {normalize_event(a)["event_kind"], normalize_event(b)["event_kind"]}
    if kinds != {"weekly", "specific_date"}:
        return False
    slot = when_slot_key(a)
    return slot is not None and slot == when_slot_key(b)


def describe_when(event: dict[str, Any]) -> str:
    """Human-readable schedule phrase, e.g. `Weekly Sunday` or `2026-03-08 (Sun)`."""
    normalized = normalize_event(event)
    if normalized["event_kind"] == "weekly":
        return f"Weekly {normalized['day_of_week'] or '?'}"
    date_value = normalized["date"]
    if not date_value:
        return "Undated"
    weekday = weekday_of(date_value)
    return f"{date_value} ({weekday[:3]})" if weekday else date_value


def describe_event(event: dict[str, Any]) -> str:
    """One-line summary used in logs, the CLI report, and card fallbacks."""
    normalized = normalize_event(event)
    parts = [
        normalized["church_slug"],
        normalized["event_type"],
        describe_when(normalized),
        normalized["start_time"],
    ]
    if normalized["end_time"]:
        parts.append(f"– {normalized['end_time']}")
    if normalized["cancelled"]:
        parts.append("CANCELLED")
    return " · ".join(part for part in parts if part)
