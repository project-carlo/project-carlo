"""Weeks of the month and seasons, between the labels' forms and the database's.

The labels (`labeling/labels.py`), the view sent to the model, the model's
answer and the snapshot all use the labels' forms: weeks of the month as a
list such as `["first", "third"]`, and a season as
`{"start_month": 5, "start_day": None, "end_month": 10, "end_day": None}`.
An exclusion is the list plus `exclude_weeks` true (`["last"]` excluded:
every week except the last). `schedule_entry` stores the weeks as one mask
(bit 0 first ... bit 5 last, 0 = every week; bit 6 set when the listed weeks
are the ones left out), always in `labels.canonical_weeks`' form, and the
season as four integer columns. These are the only functions that translate
between the two.

`describe_schedule_pattern` words the qualifiers for people ("First Friday of
the month, October through June"), as the web app's
`apps/web/src/lib/schedulePattern.ts` does.
"""

from __future__ import annotations

from calendar import monthrange
from datetime import date
from functools import lru_cache
from typing import Any

from pdf_extract.labeling.labels import (
    DAYS_IN_MONTH,
    SEASON_KEYS,
    WEEKS_OF_MONTH,
    canonical_weeks,
    weeks_never_happen,
)

MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
_MONTH_NUMBER = {name.lower(): i for i, name in enumerate(MONTHS, start=1)}

# The mask bit that says the listed weeks are the ones the slot skips.
EXCLUDE_WEEKS_BIT = 1 << len(WEEKS_OF_MONTH)
_WEEK_BITS = EXCLUDE_WEEKS_BIT - 1

SEASON_COLUMNS = ("season_start_month", "season_start_day", "season_end_month", "season_end_day")


class QualifierError(ValueError):
    """A weeks-of-the-month list or season that can't be stored."""


def weeks_to_mask(weeks: Any, exclude: Any = False) -> int:
    """`["first", "third"]` -> 0b101; `["last"]` excluded -> 0b1100000.

    The selection is stored in its canonical form, so an exclusion the
    remaining weeks can say is stored as them. Raises QualifierError for
    anything else, and for an exclusion that leaves no week.
    """
    if weeks is None:
        weeks = []
    if not isinstance(weeks, list):
        raise QualifierError("weeks_of_month must be a list")
    if exclude is None:
        exclude = False
    if not isinstance(exclude, bool):
        raise QualifierError("exclude_weeks must be true or false")
    tokens = []
    for week in weeks:
        token = week.strip().lower() if isinstance(week, str) else week
        if token not in WEEKS_OF_MONTH:
            raise QualifierError(f"unknown week of the month {week!r}")
        if token in tokens:
            raise QualifierError(f"week of the month {week!r} listed twice")
        tokens.append(token)
    if weeks_never_happen(tokens, exclude):
        raise QualifierError("exclude_weeks leaves out every week")
    listed, excluded = canonical_weeks(tokens, exclude)
    mask = sum(1 << WEEKS_OF_MONTH.index(week) for week in listed)
    return mask | EXCLUDE_WEEKS_BIT if excluded else mask


def mask_to_weeks(mask: int) -> list[str]:
    """0b101 -> `["first", "third"]`, in the labels' order (the exclusion bit aside)."""
    return [week for i, week in enumerate(WEEKS_OF_MONTH) if mask & (1 << i)]


def mask_excludes_weeks(mask: int) -> bool:
    """Whether the mask's weeks are the ones the slot skips."""
    return bool(mask & EXCLUDE_WEEKS_BIT) and bool(mask & _WEEK_BITS)


def _in_season(
    month: int, day: int, start_month: int | None, start_day: int | None,
    end_month: int | None, end_day: int | None,
) -> bool:
    start = (start_month, start_day or 1) if start_month else (1, 1)
    end = (end_month, end_day or DAYS_IN_MONTH[end_month - 1]) if end_month else (12, 31)
    point = (month, day)
    return start <= point <= end if start <= end else point >= start or point <= end


def _in_weeks(day: int, month_days: int, weeks: int) -> bool:
    selected = weeks & _WEEK_BITS
    week_bits = 1 << ((day - 1) // 7)
    if day + 7 > month_days:
        week_bits |= 1 << 5  # last, which can also be fourth or fifth
    listed = bool(selected & week_bits)
    return not selected or (not listed if mask_excludes_weeks(weeks) else listed)


def recurrence_includes_date(
    day: date, weeks: int, start_month: int | None, start_day: int | None,
    end_month: int | None, end_day: int | None,
) -> bool:
    """Whether a weekly pattern's qualifiers include this calendar date.

    Callers match the weekday separately. Seasons include both endpoints and
    may cross New Year; an omitted day covers the whole boundary month. Last
    means the date's weekday will not occur again in its actual month/year.
    """
    return _in_season(day.month, day.day, start_month, start_day, end_month, end_day) and (
        _in_weeks(day.day, monthrange(day.year, day.month)[1], weeks)
    )


@lru_cache(maxsize=1024)
def recurrence_mask(
    weeks: int, start_month: int | None, start_day: int | None,
    end_month: int | None, end_day: int | None,
) -> int:
    """Possible month-days of a weekly pattern, for testing recurrence overlap.

    Each bit is a (month, month length, day) combination. February is checked
    at both lengths: its last weekday may be the fourth in one and fifth in
    the other. Any month-day can fall on the entry's weekday in some year;
    callers compare only entries with the same weekday. Seasons are inclusive
    and may cross New Year. This avoids choosing an arbitrary reference year.
    """
    result = 0
    bit = 0
    for month, length in enumerate(DAYS_IN_MONTH, start=1):
        for days in ((28, 29) if month == 2 else (length,)):
            for day in range(1, days + 1):
                if _in_season(month, day, start_month, start_day, end_month, end_day) and (
                    _in_weeks(day, days, weeks)
                ):
                    result |= 1 << bit
                bit += 1
    return result


def _month(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if 1 <= value <= 12 else None
    if isinstance(value, str):
        return _MONTH_NUMBER.get(value.strip().lower())
    return None


def season_to_columns(season: Any) -> tuple[int | None, int | None, int | None, int | None]:
    """A season object as (start_month, start_day, end_month, end_day); all None for none.

    Months may be numbers or English month names. Each day must be null or a
    day of its month (`labels.DAYS_IN_MONTH`, so February 29 is allowed).
    """
    if season is None:
        return (None, None, None, None)
    if not isinstance(season, dict):
        raise QualifierError("season must be null or an object")
    unknown = sorted(set(season) - set(SEASON_KEYS))
    if unknown:
        raise QualifierError(f"season has unknown keys {', '.join(unknown)}")
    out: list[int | None] = []
    for edge in ("start", "end"):
        month = _month(season.get(f"{edge}_month"))
        if month is None:
            raise QualifierError(f"season {edge}_month must be a month")
        day = season.get(f"{edge}_day")
        if day is not None and (
            isinstance(day, bool) or not isinstance(day, int)
            or not 1 <= day <= DAYS_IN_MONTH[month - 1]
        ):
            raise QualifierError(f"season {edge}_day must be null or a day of month {month}")
        out += [month, day]
    return (out[0], out[1], out[2], out[3])


def columns_to_season(
    start_month: int | None, start_day: int | None, end_month: int | None, end_day: int | None,
) -> dict[str, int | None] | None:
    """The four season columns as a season object, or None for no season."""
    if start_month is None or end_month is None:
        return None
    return {
        "start_month": start_month,
        "start_day": start_day,
        "end_month": end_month,
        "end_day": end_day,
    }


def _join_with_and(parts: list[str]) -> str:
    if len(parts) <= 1:
        return parts[0] if parts else ""
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return f"{', '.join(parts[:-1])}, and {parts[-1]}"


def describe_weeks_of_month(
    weeks: list[str], day_of_week: str | None, exclude: bool = False,
) -> str | None:
    """"First Friday of the month", "First and third Fridays of the month".

    An exclusion reads "Every Sunday except the last".
    """
    ordered = [week for week in WEEKS_OF_MONTH if week in weeks]
    if not ordered:
        return None
    day = day_of_week.strip() if isinstance(day_of_week, str) else ""
    if exclude:
        return f"Every {day.capitalize() or 'week'} except the {_join_with_and(ordered)}"
    if not day:
        return f"{_join_with_and([w.capitalize() for w in ordered])} week of the month"
    ordinals = [week.capitalize() if i == 0 else week for i, week in enumerate(ordered)]
    plural = "s" if len(ordered) > 1 else ""
    return f"{_join_with_and(ordinals)} {day.capitalize()}{plural} of the month"


def describe_season(season: dict[str, int | None] | None) -> str | None:
    """"October through June", or "June 4 through September 10" once the bulletin dated it.

    A boundary carries a day only where the parish printed one, so a range
    given in whole months is described in whole months.
    """
    if season is None:
        return None
    ends = []
    for edge in ("start", "end"):
        month, day = season[f"{edge}_month"], season[f"{edge}_day"]
        name = MONTHS[month - 1]
        ends.append(name if day is None else f"{name} {day}")
    return f"{ends[0]} through {ends[1]}"


def describe_schedule_pattern(
    weeks: list[str],
    season: dict[str, int | None] | None,
    day_of_week: str | None,
    exclude: bool = False,
) -> str | None:
    """The whole qualifier as one phrase, or None for a plain weekly slot."""
    parts = [
        part for part in (
            describe_weeks_of_month(weeks, day_of_week, exclude), describe_season(season),
        )
        if part is not None
    ]
    return ", ".join(parts) if parts else None
