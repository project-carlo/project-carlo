"""The shape of a recurring slot: which weeks of the month, and which part of the year.

Bulletins qualify a weekly line in two ways a plain (weekday, time) pair cannot
carry: a slot that only runs for part of the year ("Confessions Tuesdays,
October through June") and one that only falls on certain weeks of the month
("First Friday devotions"). Until these had fields of their own the extractor
could only put them in `note` — free text nothing downstream reads — so the
frontend advertised an October-to-June confession slot in September, and listed
First Friday devotions as if they happened every Friday.

This module is the single place that decides what those two qualifiers mean. It
normalises the loose strings the LLM returns and answers whether a month falls
inside a season range. `pdf_extract.db` writes the normalised values into the
`event` table, and `apps/web/src/lib/schedulePattern.ts` mirrors the same rules
in the browser.
"""

from __future__ import annotations

import re
from typing import Any

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


def normalize_season(start: Any, end: Any) -> tuple[int | None, int | None]:
    """Canonicalise a season range; a half-stated range is no range at all.

    "Runs from October" without an end month leaves the slot year-round rather
    than inventing a December cutoff and hiding it for half the year.
    """
    start_month = normalize_month(start)
    end_month = normalize_month(end)
    if start_month is None or end_month is None:
        return None, None
    return start_month, end_month


def month_in_season(month: int, start: int | None, end: int | None) -> bool:
    """Whether `month` falls inside an inclusive season range.

    A range that wraps the new year (October through June) is the common case
    for a parish schedule tied to the school year, so `start > end` reads as
    "start month to December, then January to end month".
    """
    if start is None or end is None:
        return True
    if start <= end:
        return start <= month <= end
    return month >= start or month <= end
