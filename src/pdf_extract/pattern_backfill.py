"""Recover recurrence qualifiers from the notes older extractions left behind.

Before `weeks_of_month` and the season months existed, the extractor had nowhere
to put "First Friday of the month" or "October through June" except `note` —
free text nothing downstream reads. So the frontend offered a first-Friday
devotion every Friday, and an October-to-June confession slot in September.

New extractions fill the fields directly. This reads the same statement back out
of the notes already on file, so the corpus does not have to wait for every
parish to publish its next bulletin.

Deliberately narrow. It acts only on notes that state the pattern outright, and
only on weekly rows, which are the only ones that recur. It never guesses at
"Summer Mass" or "Resumes in September", where the months the parish means are
not on the page, and it refuses any note carrying an exclusion ("Except 1st
Saturday of the month") — reading that as a first-Saturday-only slot would
invert its meaning. Anything it cannot read is left exactly as it is, and the
row goes on behaving as it does today.

The phrase it reads is removed from the note, since the fields now carry it and
the frontend renders them itself — with one exception. A season keeps the words
the parish printed, verbatim, in `season_note`: a bulletin that said "October
through June" is quoted back that way rather than paraphrased as the exact days
underneath. Weeks of the month need no such record, since "First Friday of the
month" reads back the same either way.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

from pdf_extract.schedule_pattern import (
    MONTH_NAMES,
    clean_note,
    normalize_day,
    normalize_month,
    normalize_weeks_of_month,
)
from pdf_extract.storage import EVENTS_PATH, load_json_list, save_json_list

LOGGER = logging.getLogger(__name__)

# An exclusion anywhere in the note disqualifies the whole note: "Except 1st
# Saturday of the month" names the one week the slot does *not* run, and the
# fields have no way to say that.
_EXCLUSION_RE = re.compile(r"(?i)\b(?:except|excluding|other than|apart from|no|not)\b")

_ORDINAL = r"(?:first|second|third|fourth|fifth|last|1st|2nd|3rd|4th|5th)"
_SEPARATOR = r"(?:\s*[,&+]\s*(?:and\s+)?|\s+and\s+|\s+or\s+)"
_ORDINAL_LIST = rf"{_ORDINAL}(?:{_SEPARATOR}{_ORDINAL})*"
_ORDINAL_TOKEN_RE = re.compile(_ORDINAL, re.I)

# Longest first so "September" is not cut short to "Sep" with "tember" left in
# the note. A trailing period is consumed but not captured; `normalize_month`
# reads the abbreviations.
_MONTH = "|".join(sorted(
    {*MONTH_NAMES, *(name[:3] for name in MONTH_NAMES), "Sept"},
    key=len, reverse=True,
))
# The day is optional and never swallows part of a year: "October through June"
# leaves both days unset, "June 4 - September 10" fills them in, and "October
# through June 2027" keeps its hands off the 2027.
_DAY = r"(?:\s+(\d{1,2})(?!\d)(?:st|nd|rd|th)?)?"
_MONTH_DAY = rf"\b({_MONTH})\b\.?{_DAY}"
_SEASON_RE = re.compile(
    rf"{_MONTH_DAY}\s*(?:through|thru|to|until|–|—|-)\s*{_MONTH_DAY}",
    re.I,
)

# A note trimmed down to nothing but the service it describes is saying no more
# than the row itself already does.
_LEADING_NOUN_RE = re.compile(
    r"^(?:mass|masses|adoration|exposition|holy hour|devotions?|confessions?|"
    r"benediction|rosary)\b",
    re.I,
)
_EDGE_PUNCTUATION = " \t,;:.·-–—"


def _weeks_pattern(day_of_week: str) -> re.Pattern[str]:
    """Ordinals qualifying this row's own weekday, or the weeks of the month.

    Anchoring on the row's weekday is what keeps "First Friday" on a Friday row
    apart from a stray mention of some other day's schedule.
    """
    day = re.escape(day_of_week.strip())
    return re.compile(
        rf"\b({_ORDINAL_LIST})\s+(?:{day}s?|weeks?)"
        r"(?:\s+of\s+the\s+month)?(?:\s+only)?",
        re.I,
    )


def _tidy(note: str) -> str | None:
    """Clean up what is left of a note once a matched phrase is cut out."""
    text = re.sub(r"\s+", " ", note).strip(_EDGE_PUNCTUATION)
    text = _LEADING_NOUN_RE.sub("", text, count=1).strip(_EDGE_PUNCTUATION)
    return text or None


def derive_pattern(note: str | None, day_of_week: Any) -> dict[str, Any] | None:
    """Read a note's recurrence qualifiers, or None when it states none.

    Returns the fields to set on the row, including the rewritten `note` with
    the phrase they replace removed.
    """
    if not isinstance(note, str) or not note.strip():
        return None
    if _EXCLUSION_RE.search(note):
        return None

    remaining = note
    derived: dict[str, Any] = {}

    if isinstance(day_of_week, str) and day_of_week.strip():
        match = _weeks_pattern(day_of_week).search(remaining)
        if match:
            weeks = normalize_weeks_of_month(_ORDINAL_TOKEN_RE.findall(match.group(1)))
            if weeks:
                derived["weeks_of_month"] = weeks
                remaining = remaining[: match.start()] + " " + remaining[match.end():]

    match = _SEASON_RE.search(remaining)
    if match:
        start_month = normalize_month(match.group(1))
        end_month = normalize_month(match.group(3))
        if start_month is not None and end_month is not None:
            start_day = normalize_day(match.group(2), start_month)
            end_day = normalize_day(match.group(4), end_month)
            derived["season_start_month"] = start_month
            if start_day is not None:
                derived["season_start_day"] = start_day
            derived["season_end_month"] = end_month
            if end_day is not None:
                derived["season_end_day"] = end_day
            # The words the parish printed, kept as printed: this is what the
            # frontend shows, so a note that ranged whole months is not read
            # back to anyone as a pair of exact dates it never named.
            derived["season_note"] = clean_note(match.group(0))
            remaining = remaining[: match.start()] + " " + remaining[match.end():]

    if not derived:
        return None
    derived["note"] = _tidy(remaining)
    return derived


def backfill_patterns(
    events_path: Path = EVENTS_PATH, *, dry_run: bool = False,
) -> dict[str, int]:
    """Fill in weeks-of-month and season months across data/events.json.

    Rows that already carry either qualifier are left alone: the extractor's own
    reading of the bulletin outranks a second-hand one taken off a note.
    """
    events = load_json_list(events_path)
    monthly = 0
    seasonal = 0

    for row in events:
        if not isinstance(row, dict) or row.get("event_kind") != "weekly":
            continue
        if row.get("weeks_of_month") or row.get("season_start_month") is not None:
            continue
        derived = derive_pattern(row.get("note"), row.get("day_of_week"))
        if derived is None:
            continue
        if "weeks_of_month" in derived:
            monthly += 1
        if "season_start_month" in derived:
            seasonal += 1
        LOGGER.info(
            "%s %s %s %s: %r -> %s",
            row.get("church_slug"), row.get("event_type"), row.get("day_of_week"),
            row.get("start_time"), row.get("note"), derived,
        )
        row.update(derived)

    changed = monthly + seasonal
    if changed and not dry_run:
        save_json_list(events_path, events)

    result = {
        "events": len(events),
        "monthly": monthly,
        "seasonal": seasonal,
        "dry_run": int(dry_run),
    }
    LOGGER.info("Pattern backfill: %s", result)
    return result
