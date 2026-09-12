"""The shape of a recurring slot: which weeks of the month, and which part of the year.

Bulletins qualify a weekly line in two ways a plain (weekday, time) pair cannot
carry: a slot that only runs for part of the year ("Confessions Tuesdays,
October through June") and one that only falls on certain weeks of the month
("First Friday devotions"). Until these had fields of their own the extractor
could only put them in `note` — free text nothing downstream reads — so the
frontend advertised an October-to-June confession slot in September, and listed
First Friday devotions as if they happened every Friday.

A season is held to the day, not just the month, because bulletins state it that
way: "Summer Masses, June 4 through September 10" starts on a Thursday in the
first week of June and nothing before it. A boundary with no day is not a
missing value but a coarser statement of the same thing: "January to April" runs
the whole of both months, and reads back to the parish in the words it used,
without a January 1st or an April 30th it never printed.

This module is the single place that decides what those qualifiers mean. It
normalises the loose strings the LLM returns, answers whether a date matches
the pattern, and describes the pattern back at the grain it was filled in at.
`pdf_extract.db` writes the normalised values into the `event` table, and
`apps/web/src/lib/schedulePattern.ts` mirrors the same rules in the browser.
"""

from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Any, NamedTuple

# Which occurrences of a weekday within a month a slot falls on. "last" is kept
# distinct from "fourth": a five-Friday month has a fourth Friday and a
# different last one, and bulletins mean the later date when they say "last".
WEEKS_OF_MONTH: tuple[str, ...] = (
    "first", "second", "third", "fourth", "fifth", "last",
)

MONTH_NAMES: tuple[str, ...] = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)

# February is given 29 days: a season boundary is a recurring calendar position,
# not a date in one particular year, and "Adoration through February 29" is a
# real thing for a parish to print in a leap year.
DAYS_IN_MONTH: tuple[int, ...] = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

_WEEK_ALIASES: dict[str, str] = {}
for _index, _week in enumerate(WEEKS_OF_MONTH[:5], start=1):
    _WEEK_ALIASES[_week] = _week
    _WEEK_ALIASES[str(_index)] = _week
    _WEEK_ALIASES[f"{_index}st"] = _week
    _WEEK_ALIASES[f"{_index}nd"] = _week
    _WEEK_ALIASES[f"{_index}rd"] = _week
    _WEEK_ALIASES[f"{_index}th"] = _week
_WEEK_ALIASES["last"] = "last"
_WEEK_ALIASES["final"] = "last"

_MONTH_INDEX: dict[str, int] = {}
for _index, _name in enumerate(MONTH_NAMES, start=1):
    _MONTH_INDEX[_name.lower()] = _index
    _MONTH_INDEX[_name.lower()[:3]] = _index
# Not reachable from the three-letter rule, and the abbreviation parishes use most.
_MONTH_INDEX["sept"] = 9

_WEEK_ORDER = {week: idx for idx, week in enumerate(WEEKS_OF_MONTH)}
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
_NON_DIGIT_RE = re.compile(r"[^0-9]")


def normalize_week_of_month(value: Any) -> str | None:
    """Map one loose ordinal ("1st", "First", 1) to its canonical token."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        value = str(value)
    if not isinstance(value, str):
        return None
    return _WEEK_ALIASES.get(_NON_ALNUM_RE.sub("", value.strip().lower()))


def normalize_weeks_of_month(value: Any) -> list[str]:
    """Canonicalise the weeks a slot falls on; empty list means every week.

    Accepts what the LLM and the stored forms both produce: a list of ordinals,
    a comma-separated string, or nothing. Unrecognised entries are dropped
    rather than guessed at — a slot with no readable qualifier is a weekly slot,
    which is what it was before this field existed.
    """
    if value is None:
        return []
    items: list[Any]
    if isinstance(value, str):
        items = value.split(",")
    elif isinstance(value, (list, tuple)):
        items = list(value)
    else:
        items = [value]

    weeks: list[str] = []
    for item in items:
        week = normalize_week_of_month(item)
        if week is not None and week not in weeks:
            weeks.append(week)
    return sorted(weeks, key=lambda week: _WEEK_ORDER[week])


def weeks_of_month_to_text(weeks: list[str]) -> str | None:
    """Render canonical weeks for the `event.weeks_of_month` column."""
    return ",".join(weeks) if weeks else None


def normalize_month(value: Any) -> int | None:
    """Parse a month name, abbreviation, or 1-12 number into a month number."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if 1 <= value <= 12 else None
    if not isinstance(value, str):
        return None
    raw = value.strip().lower()
    if not raw:
        return None
    if raw.isdigit():
        number = int(raw)
        return number if 1 <= number <= 12 else None
    # Tolerate "October through June" style fragments arriving with punctuation.
    return _MONTH_INDEX.get(_NON_ALNUM_RE.sub("", raw))


def normalize_day(value: Any, month: int | None) -> int | None:
    """Parse a day of the month, dropped when it cannot fall in `month`.

    A day is only ever a refinement of the month beside it: dropping an
    unreadable or impossible one ("February 30") leaves the boundary at the
    whole month, which is the coarser but still correct reading.
    """
    if month is None or isinstance(value, bool):
        return None
    if isinstance(value, str):
        digits = _NON_DIGIT_RE.sub("", value)  # Tolerate "4th".
        if not digits:
            return None
        value = int(digits)
    if not isinstance(value, int):
        return None
    return value if 1 <= value <= DAYS_IN_MONTH[month - 1] else None


class Season(NamedTuple):
    """The part of the year a slot runs.

    The months and days are inclusive bounds; a missing day means the boundary
    sits at the edge of its month, which is how a bulletin naming only months
    reads.
    """

    start_month: int | None = None
    start_day: int | None = None
    end_month: int | None = None
    end_day: int | None = None

    @property
    def is_set(self) -> bool:
        """Whether this season actually bounds anything."""
        return self.start_month is not None and self.end_month is not None


NO_SEASON = Season()


def normalize_season(
    start_month: Any,
    start_day: Any = None,
    end_month: Any = None,
    end_day: Any = None,
) -> Season:
    """Canonicalise a season range; a half-stated range is no range at all.

    "Runs from October" without an end month leaves the slot year-round rather
    than inventing a December cutoff and hiding it for half the year.
    """
    start = normalize_month(start_month)
    end = normalize_month(end_month)
    if start is None or end is None:
        return NO_SEASON
    return Season(
        start_month=start,
        start_day=normalize_day(start_day, start),
        end_month=end,
        end_day=normalize_day(end_day, end),
    )


def date_in_season(month: int, day: int, season: Season) -> bool:
    """Whether the (month, day) position falls inside an inclusive season range.

    A range that wraps the new year (October through June) is the common case
    for a parish schedule tied to the school year, so a start later in the
    calendar than the end reads as "start to New Year's Eve, then New Year's Day
    to end". A boundary stated without a day covers its whole month, which is
    what "January to April" means when the bulletin names no dates.
    """
    if not season.is_set:
        return True
    start = (season.start_month, season.start_day or 1)
    end = (season.end_month, season.end_day or DAYS_IN_MONTH[season.end_month - 1])
    position = (month, day)
    if start <= end:
        return start <= position <= end
    return position >= start or position <= end


def _ordinal_of_month(when: date) -> int:
    """Which occurrence of its weekday within the month `when` is, 1-5."""
    return (when.day - 1) // 7 + 1


def _is_last_of_month(when: date) -> bool:
    """Whether `when` is the last occurrence of its weekday in the month."""
    return (when + timedelta(days=7)).month != when.month


def date_matches_weeks(when: date, weeks: list[str]) -> bool:
    """Whether `when` is one of the weeks of the month this slot falls on.

    "last" stays distinct from "fourth": a month with five Fridays has a fourth
    Friday and a different last one, and a bulletin that says "last Friday"
    means the later date.
    """
    if not weeks:
        return True
    ordinal = WEEKS_OF_MONTH[_ordinal_of_month(when) - 1]
    if ordinal != "last" and ordinal in weeks:
        return True
    return "last" in weeks and _is_last_of_month(when)


def date_matches_pattern(when: date, weeks: list[str], season: Season) -> bool:
    """Whether this slot actually happens on `when`, weeks and season both."""
    return date_matches_weeks(when, weeks) and date_in_season(
        when.month, when.day, season,
    )


def _title_case_week(week: str) -> str:
    return week[:1].upper() + week[1:]


def _join_with_and(parts: list[str]) -> str:
    if len(parts) <= 1:
        return parts[0] if parts else ""
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return f"{', '.join(parts[:-1])}, and {parts[-1]}"


def describe_weeks_of_month(weeks: list[str], day_of_week: str | None) -> str | None:
    """"First Friday of the month", "First and third Fridays of the month"."""
    if not weeks:
        return None
    day = day_of_week.strip() if isinstance(day_of_week, str) else ""
    if not day:
        return f"{_join_with_and([_title_case_week(week) for week in weeks])} week of the month"
    day_label = day[:1].upper() + day[1:].lower()
    ordinals = [
        _title_case_week(week) if index == 0 else week
        for index, week in enumerate(weeks)
    ]
    plural = "s" if len(weeks) > 1 else ""
    return f"{_join_with_and(ordinals)} {day_label}{plural} of the month"


def _describe_boundary(month: int, day: int | None) -> str:
    """"October", or "June 4" once the bulletin has dated the boundary."""
    name = MONTH_NAMES[month - 1]
    return name if day is None else f"{name} {day}"


def describe_season(season: Season) -> str | None:
    """When the slot runs, at the grain the bulletin stated it.

    A boundary carries a day only where the parish printed one, so a range given
    in whole months is described in whole months — "January through April", not
    the January 1st and April 30th filtering reads underneath it.
    """
    start, end = season.start_month, season.end_month
    if start is None or end is None:
        return None
    return (
        f"{_describe_boundary(start, season.start_day)} through "
        f"{_describe_boundary(end, season.end_day)}"
    )


def describe_schedule_pattern(
    weeks: list[str], season: Season, day_of_week: str | None,
) -> str | None:
    """The whole qualifier as one phrase, or None for a plain weekly slot."""
    parts = [
        part for part in (
            describe_weeks_of_month(weeks, day_of_week),
            describe_season(season),
        ) if part is not None
    ]
    return ", ".join(parts) if parts else None
