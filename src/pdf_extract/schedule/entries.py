"""One schedule entry's content: reading it, checking it, its identity and its hash.

An entry is immutable (`schedule_entry`): a change to a slot is a new entry.
Its `hash` covers every column, so identical content is stored once and an
entry id names its content. Its `identity_key` says which slot it is:

- weekly: church, event type, weekday, start time, weeks and season
- specific_date: church, event type, date, start time
- continuous: church and event type (Adoration), and its valid_from/valid_until
  when it has them: a church has at most one 24-hour chapel at a time

End time, cancelled and note are not part of identity. `slot_key` groups
recurrence variants at the same weekday and time; `conflicts_with` checks
whether two variants can occur together. A modify names its target by entry
id, so it can still change qualifiers (or move a slot).

Entries arrive in the labels' form (times as "h:MM AM", weeks of the month as
a list with `exclude_weeks`, the season as an object, the church by slug), from
the model's answer, a hand edit or a seed. `parse_entry` checks one and turns it into an `Entry`;
`Entry.view` turns it back.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from datetime import date
from hashlib import sha256
from typing import Any

from pdf_extract.bulletin_week import parse_iso_date
from pdf_extract.model import (
    ACCESS_KINDS,
    CONTINUOUS,
    DAYS,
    ENTRY_KINDS,
    EVENT_TYPES,
    continuous_access_errors,
    private_detail,
)
from pdf_extract.model import ENTRY_KEYS as LABEL_ENTRY_KEYS
from pdf_extract.schedule.qualifiers import (
    QualifierError,
    columns_to_season,
    mask_excludes_weeks,
    mask_to_weeks,
    recurrence_mask,
    season_to_columns,
    weeks_to_mask,
)
from pdf_extract.timeparse import minutes_to_time, time_to_minutes

# Rejection reasons an entry itself can earn (see `policy`).
UNKNOWN_CHURCH = "unknown_church"
INVALID_ENTRY = "invalid_entry"

# The keys an entry may carry: the labels' form plus the dates it holds between.
ENTRY_KEYS = frozenset({*LABEL_ENTRY_KEYS, "valid_from", "valid_until"})


@dataclass(frozen=True)
class Entry:
    """A `schedule_entry` row's content, column for column (no id, hash or identity)."""

    church_id: int
    event_type: str
    event_kind: str
    day_of_week: str | None
    date: str | None
    start_time: int | None  # null for a continuous chapel only
    end_time: int | None
    cancelled: int
    weeks_of_month: int  # the mask, exclusion bit and all (`qualifiers.weeks_to_mask`)
    season_start_month: int | None
    season_start_day: int | None
    season_end_month: int | None
    season_end_day: int | None
    note: str | None
    valid_from: str | None = None
    valid_until: str | None = None
    # A continuous chapel's access (`model.ACCESS_KINDS`) and unlocked hours; null otherwise.
    access: str | None = None
    open_from: int | None = None
    open_until: int | None = None

    @property
    def hash(self) -> str:
        # Unset bounds and access are left out, so entries written before they
        # existed keep their hashes.
        content = [getattr(self, name) for name in ENTRY_COLUMNS
                   if (self.bounded or name not in BOUND_COLUMNS)
                   and (self.access is not None or name not in ACCESS_COLUMNS)]
        return sha256(json.dumps(content).encode("utf-8")).hexdigest()

    @property
    def bounded(self) -> bool:
        return self.valid_from is not None or self.valid_until is not None

    @property
    def slot_key(self) -> str:
        """The unqualified slot, shared by disjoint recurrence variants."""
        if self.continuous:
            return f"{self.church_id}|{self.event_type}|{self.event_kind}"
        anchor = self.day_of_week if self.event_kind == "weekly" else self.date
        return f"{self.church_id}|{self.event_type}|{self.event_kind}|{anchor}|{self.start_time}"

    @property
    def identity_key(self) -> str:
        if self.continuous:
            if not self.bounded:
                return self.slot_key
            return f"{self.slot_key}|{self.valid_from or ''}|{self.valid_until or ''}"
        if not self.weekly:
            return self.slot_key
        qualifiers = (self.weeks_of_month, self.season_start_month, self.season_start_day,
                      self.season_end_month, self.season_end_day)
        key = self.slot_key + "|" + "|".join(str(value or 0) for value in qualifiers)
        if self.bounded:
            key += f"|{self.valid_from or ''}|{self.valid_until or ''}"
        return key

    def conflicts_with(self, other: Entry) -> bool:
        """Whether entries duplicate a pattern or claim the same occurrence.

        Dated overrides and weekly entries retain their separate identities.
        End times and notes never make overlapping recurrences distinct slots.
        """
        if self.slot_key != other.slot_key:
            return False
        if not self.recurring or self.identity_key == other.identity_key:
            return True
        if max(self.valid_from or '0001-01-01', other.valid_from or '0001-01-01') > min(
            self.valid_until or '9999-12-31', other.valid_until or '9999-12-31',
        ):
            return False
        # A church's chapel is one chapel: two versions overlapping in time conflict.
        return self.continuous or bool(self._recurrence_mask() & other._recurrence_mask())

    def _recurrence_mask(self) -> int:
        return recurrence_mask(
            self.weeks_of_month, self.season_start_month, self.season_start_day,
            self.season_end_month, self.season_end_day,
        )

    @property
    def weekly(self) -> bool:
        return self.event_kind == "weekly"

    @property
    def continuous(self) -> bool:
        return self.event_kind == CONTINUOUS

    @property
    def recurring(self) -> bool:
        """Weekly or continuous: an entry that repeats, and may hold valid_from/valid_until."""
        return self.weekly or self.continuous

    def dated_before(self, day: date) -> bool:
        """Whether this is a dated entry for a day before `day`."""
        return not self.weekly and self.date is not None and self.date < day.isoformat()

    def expired_before(self, day: date) -> bool:
        """Whether this is a dated entry before `day` or a recurring one that ended before it."""
        return self.dated_before(day) or (
            self.recurring and self.valid_until is not None and self.valid_until < day.isoformat()
        )

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
        if self.continuous:
            out.update(
                access=self.access,
                open_from=minutes_to_time(self.open_from),
                open_until=minutes_to_time(self.open_until),
            )
            if self.bounded:
                out.update(valid_from=self.valid_from, valid_until=self.valid_until)
        elif self.weekly:
            out.update(
                day_of_week=self.day_of_week,
                weeks_of_month=mask_to_weeks(self.weeks_of_month),
                exclude_weeks=mask_excludes_weeks(self.weeks_of_month),
                season=self.season(),
            )
            if self.bounded:
                out.update(valid_from=self.valid_from, valid_until=self.valid_until)
        else:
            out.update(date=self.date, cancelled=bool(self.cancelled))
        return out

    def view(self, entry_id: int) -> dict[str, Any]:
        """The entry as the view shows it: the labels' form under its id, church aside."""
        out = self.labels_form("")
        del out["church_slug"]
        return {"id": entry_id, **out}


ENTRY_COLUMNS = tuple(f.name for f in fields(Entry))
BOUND_COLUMNS = ("valid_from", "valid_until")
ACCESS_COLUMNS = ("access", "open_from", "open_until")


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
    if kind not in ENTRY_KINDS:
        raise EntryError(INVALID_ENTRY, f"event_kind must be one of {', '.join(ENTRY_KINDS)}")
    note = raw.get("note")
    if note is not None and not isinstance(note, str):
        raise EntryError(INVALID_ENTRY, "note must be text or null")
    private = private_detail(note) if isinstance(note, str) else None
    if private:
        raise EntryError(INVALID_ENTRY, f"note {private}")
    bounds = _bounds(raw, kind)
    if kind == CONTINUOUS:
        return _parse_continuous(raw, churches[slug], note, bounds)
    for name in ("access", "open_from", "open_until"):
        if raw.get(name) is not None:
            raise EntryError(INVALID_ENTRY, f"{name} is for a continuous chapel only")

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
        note=_note(note),
        **bounds,
    )


def _note(note: str | None) -> str | None:
    return note.strip() or None if isinstance(note, str) else None


def _bounds(raw: dict[str, Any], kind: str) -> dict[str, str | None]:
    bounds = {}
    for name in ("valid_from", "valid_until"):
        value = raw.get(name)
        parsed = parse_iso_date(value) if isinstance(value, str) else None
        if value is not None and (kind == "specific_date" or parsed is None):
            raise EntryError(
                INVALID_ENTRY, f"{name} must be a weekly or continuous YYYY-MM-DD date or null",
            )
        bounds[name] = parsed.isoformat() if parsed else None
    if bounds['valid_from'] and bounds['valid_until'] and (
        bounds['valid_from'] > bounds['valid_until']
    ):
        raise EntryError(INVALID_ENTRY, "valid_until must not precede valid_from")
    return bounds


def _parse_continuous(
    raw: dict[str, Any], church_id: int, note: str | None, bounds: dict[str, str | None],
) -> Entry:
    """A `continuous` entry: an Adoration chapel open every day, around the clock."""
    if raw.get("event_type") != "adoration":
        raise EntryError(INVALID_ENTRY, "a continuous entry is Adoration only")
    for name in ("day_of_week", "date", "start_time", "end_time", "season"):
        value = raw.get(name)
        if value is not None and not (isinstance(value, str) and not value.strip()):
            raise EntryError(INVALID_ENTRY, f"a continuous entry has no {name}")
    if raw.get("cancelled") or raw.get("weeks_of_month") or raw.get("exclude_weeks"):
        raise EntryError(
            INVALID_ENTRY, "a continuous entry has no cancellation or weeks of the month",
        )
    access = raw.get("access")
    if access not in ACCESS_KINDS:
        raise EntryError(INVALID_ENTRY, f"access must be one of {', '.join(ACCESS_KINDS)}")
    open_from = _time(raw.get("open_from"), "open_from", required=False)
    open_until = _time(raw.get("open_until"), "open_until", required=False)
    hours = [None if m is None else f"{m // 60:02d}:{m % 60:02d}" for m in (open_from, open_until)]
    problems = continuous_access_errors(access, *hours, "entry")
    if problems:
        raise EntryError(INVALID_ENTRY, problems[0].removeprefix("entry: ").removeprefix("entry."))
    return Entry(
        church_id=church_id,
        event_type="adoration",
        event_kind=CONTINUOUS,
        day_of_week=None,
        date=None,
        start_time=None,
        end_time=None,
        cancelled=0,
        weeks_of_month=0,
        season_start_month=None,
        season_start_day=None,
        season_end_month=None,
        season_end_day=None,
        note=_note(note),
        access=access,
        open_from=open_from,
        open_until=open_until,
        **bounds,
    )
