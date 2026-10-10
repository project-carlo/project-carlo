"""Weeks of the month and seasons, between the labels' forms and the database's.

The labels (`labeling/labels.py`), the view sent to the model, the model's
answer and the snapshot all use the labels' forms: weeks of the month as a
list such as `["first", "third"]`, and a season as
`{"start_month": 5, "start_day": None, "end_month": 10, "end_day": None}`.
`schedule_entry` stores the weeks as a 6-bit mask (bit 0 first ... bit 5 last,
0 = every week) and the season as four integer columns. These are the only
functions that translate between the two.
"""

from __future__ import annotations

from typing import Any

from pdf_extract.labeling.labels import DAYS_IN_MONTH, SEASON_KEYS, WEEKS_OF_MONTH

MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)
_MONTH_NUMBER = {name.lower(): i for i, name in enumerate(MONTHS, start=1)}

SEASON_COLUMNS = ("season_start_month", "season_start_day", "season_end_month", "season_end_day")


class QualifierError(ValueError):
    """A weeks-of-the-month list or season that can't be stored."""


def weeks_to_mask(weeks: Any) -> int:
    """`["first", "third"]` -> 0b101. Raises QualifierError for anything else."""
    if weeks is None:
        return 0
    if not isinstance(weeks, list):
        raise QualifierError("weeks_of_month must be a list")
    mask = 0
    for week in weeks:
        token = week.strip().lower() if isinstance(week, str) else week
        if token not in WEEKS_OF_MONTH:
            raise QualifierError(f"unknown week of the month {week!r}")
        bit = 1 << WEEKS_OF_MONTH.index(token)
        if mask & bit:
            raise QualifierError(f"week of the month {week!r} listed twice")
        mask |= bit
    return mask


def mask_to_weeks(mask: int) -> list[str]:
    """0b101 -> `["first", "third"]`, in the labels' order."""
    return [week for i, week in enumerate(WEEKS_OF_MONTH) if mask & (1 << i)]


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
