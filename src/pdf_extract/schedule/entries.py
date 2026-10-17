"""One schedule entry's content: reading it, checking it, its identity and its hash.

An entry is immutable (`schedule_entry`): a change to a slot is a new entry.
Its `hash` covers every column, so identical content is stored once and an
entry id names its content. Its `identity_key` says which slot it is:

- weekly: church, event type, weekday, start time
- specific_date: church, event type, date, start time

End time, weeks of the month (and whether they are excluded), season,
cancelled and note are not part of identity, so changing any of them is a
modify of the same slot.

Entries arrive in the labels' form (times as "h:MM AM", weeks of the month as
a list with `exclude_weeks`, the season as an object, the church by slug), from
the model's answer, a hand edit or a seed. `parse_entry` checks one and turns it into an `Entry`;
`Entry.view` turns it back.
"""

from __future__ import annotations

import json
from dataclasses import astuple, dataclass, fields
from datetime import date
from hashlib import sha256
from typing import Any

from pdf_extract.bulletin_week import parse_iso_date
from pdf_extract.labeling.labels import DAYS, EVENT_KINDS, EVENT_TYPES
from pdf_extract.schedule.qualifiers import (
    QualifierError,
    columns_to_season,
    mask_excludes_weeks,
    mask_to_weeks,
    season_to_columns,
    weeks_to_mask,
)
from pdf_extract.timeparse import minutes_to_time, time_to_minutes

# Rejection reasons an entry itself can earn (see `policy`).
UNKNOWN_CHURCH = "unknown_church"
INVALID_ENTRY = "invalid_entry"

# The keys an entry may carry in the labels' form.
ENTRY_KEYS = frozenset({
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "weeks_of_month", "exclude_weeks", "season", "note",
})


@dataclass(frozen=True)
class Entry:
    """A `schedule_entry` row's content, column for column (no id, hash or identity)."""

    church_id: int
    event_type: str
    event_kind: str
    day_of_week: str | None
    date: str | None
    start_time: int
    end_time: int | None
    cancelled: int
    weeks_of_month: int  # the mask, exclusion bit and all (`qualifiers.weeks_to_mask`)
    season_start_month: int | None
    season_start_day: int | None
    season_end_month: int | None
    season_end_day: int | None
    note: str | None

    @property
    def hash(self) -> str:
        return sha256(json.dumps(astuple(self)).encode("utf-8")).hexdigest()

    @property
    def identity_key(self) -> str:
        anchor = self.day_of_week if self.event_kind == "weekly" else self.date
        return f"{self.church_id}|{self.event_type}|{self.event_kind}|{anchor}|{self.start_time}"

    @property
    def weekly(self) -> bool:
        return self.event_kind == "weekly"

    def dated_before(self, day: date) -> bool:
        """Whether this is a dated entry for a day before `day`."""
        return not self.weekly and self.date is not None and self.date < day.isoformat()

    def season(self) -> dict[str, int | None] | None:
        return columns_to_season(
            self.season_start_month, self.season_start_day,
            self.season_end_month, self.season_end_day,
        )

    def labels_form(self, church_slug: str) -> dict[str, Any]:
        """The entry as the model writes one (and a hand edit or seed gives one)."""
        out: dict[str, Any] = {
            "church_slug": church_slug,
            "event_type": self.event_type,
            "event_kind": self.event_kind,
            "start_time": minutes_to_time(self.start_time),
            "end_time": minutes_to_time(self.end_time),
            "note": self.note,
        }
        if self.weekly:
            out.update(
                day_of_week=self.day_of_week,
                weeks_of_month=mask_to_weeks(self.weeks_of_month),
                exclude_weeks=mask_excludes_weeks(self.weeks_of_month),
                season=self.season(),
            )
        else:
            out.update(date=self.date, cancelled=bool(self.cancelled))
        return out

    def view(self, entry_id: int) -> dict[str, Any]:
        """The entry as the view shows it: the labels' form under its id, church aside."""
        out = self.labels_form("")
        del out["church_slug"]
        return {"id": entry_id, **out}


ENTRY_COLUMNS = tuple(f.name for f in fields(Entry))


def entry_from_row(row: Any) -> Entry:
    """An Entry from a `schedule_entry` row (anything indexable by column name)."""
    return Entry(**{name: row[name] for name in ENTRY_COLUMNS})


class EntryError(ValueError):
    """An entry that can't be stored. `reason` is the policy's rejection code."""

    def __init__(self, reason: str, message: str) -> None:
        super().__init__(message)
        self.reason = reason


def _day_of_week(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    wanted = value.strip().lower()
    return next((d for d in DAYS if d.lower() == wanted), None)


def _time(value: Any, name: str, *, required: bool) -> int | None:
    if value is None or (isinstance(value, str) and not value.strip()):
        if required:
            raise EntryError(INVALID_ENTRY, f"{name} is required")
        return None
    minutes = time_to_minutes(value) if isinstance(value, str) else None
    if minutes is None or not 0 <= minutes <= 1439:
        raise EntryError(INVALID_ENTRY, f"unreadable {name} {value!r}")
    return minutes


def parse_entry(raw: Any, churches: dict[str, int]) -> Entry:
    """Check an entry in the labels' form and return it as an Entry.

    `churches` maps the slugs of the parish's churches (retired ones left out)
    to their ids. Raises EntryError with reason `unknown_church` for a church
    outside it, and `invalid_entry` for anything else wrong: a weekly entry
    with a date, a season day its month doesn't have, an unreadable time...
    """
    if not isinstance(raw, dict):
        raise EntryError(INVALID_ENTRY, "entry must be an object")
    # The policy checks the church before the entry itself.
    slug = raw.get("church_slug")
    if not isinstance(slug, str) or slug not in churches:
        raise EntryError(UNKNOWN_CHURCH, f"church {slug!r} is not one of the parish's")
    unknown = sorted(set(raw) - ENTRY_KEYS)
    if unknown:
        raise EntryError(INVALID_ENTRY, f"unknown keys {', '.join(unknown)}")

    event_type = raw.get("event_type")
    if event_type not in EVENT_TYPES:
        raise EntryError(INVALID_ENTRY, f"event_type must be one of {', '.join(EVENT_TYPES)}")
    kind = raw.get("event_kind")
    if kind not in EVENT_KINDS:
        raise EntryError(INVALID_ENTRY, f"event_kind must be one of {', '.join(EVENT_KINDS)}")

    day_of_week = _day_of_week(raw.get("day_of_week"))
    cancelled = raw.get("cancelled") or False
    if not isinstance(cancelled, bool):
        raise EntryError(INVALID_ENTRY, "cancelled must be true or false")
    try:
        weeks = weeks_to_mask(raw.get("weeks_of_month") or [], raw.get("exclude_weeks") or False)
        season = season_to_columns(raw.get("season"))
    except QualifierError as exc:
        raise EntryError(INVALID_ENTRY, str(exc)) from exc

    if kind == "weekly":
        if day_of_week is None:
            raise EntryError(INVALID_ENTRY, "a weekly entry needs a day_of_week")
        if raw.get("date") is not None:
            raise EntryError(INVALID_ENTRY, "a weekly entry has no date")
        if cancelled:
            raise EntryError(
                INVALID_ENTRY, "a weekly entry can't be cancelled; cancel one date instead",
            )
        entry_date = None
    else:
        parsed = parse_iso_date(raw.get("date"))
        if parsed is None:
            raise EntryError(INVALID_ENTRY, f"a dated entry needs a YYYY-MM-DD date, not {raw.get('date')!r}")
        # A weekday that agrees with the date says nothing more; one that
        # disagrees means the entry is not what it seems.
        if raw.get("day_of_week") is not None and day_of_week != DAYS[parsed.weekday()]:
            raise EntryError(INVALID_ENTRY, "a dated entry has no day_of_week")
        if weeks or season[0] is not None:
            raise EntryError(
                INVALID_ENTRY, "weeks_of_month, exclude_weeks and season are for weekly entries",
            )
        entry_date, day_of_week = parsed.isoformat(), None

    note = raw.get("note")
    if note is not None and not isinstance(note, str):
        raise EntryError(INVALID_ENTRY, "note must be text or null")
    return Entry(
        church_id=churches[slug],
        event_type=event_type,
        event_kind=kind,
        day_of_week=day_of_week,
        date=entry_date,
        start_time=_time(raw.get("start_time"), "start_time", required=True),
        end_time=_time(raw.get("end_time"), "end_time", required=False),
        cancelled=int(cancelled),
        weeks_of_month=weeks,
        season_start_month=season[0],
        season_start_day=season[1],
        season_end_month=season[2],
        season_end_day=season[3],
        note=note.strip() or None if isinstance(note, str) else None,
    )
