"""Which week a bulletin is for, and which of a parish's bulletins is current.

A bulletin's week comes from its own issue date, the one the extractor reads
off it (`published_date`). The address it was fetched from is no guide: on
the 2026-09 corpus a fifth of the addresses carry no date `parse_date` can
read, and Discover Mass hands out a new address for the same PDF on every
request. Nor is the fetch time: an issue is posted anywhere from two weeks
early to a month late.

Every date is rounded to the Sunday of its week (`nearest_sunday`), because a
bulletin can carry its Saturday vigil's date or the Sunday's, and a weekly run
lands anywhere from the Saturday before to the Monday after.

`week_order_sql` is the same ordering in SQL, for the queries that pick each
parish's current bulletin (`storage.latest_bulletin_order`). The two must
agree, which is why a date is read only as a real YYYY-MM-DD day: SQLite's
`date()` reads no other format, and rolls an impossible day like 02-30 into
the next month.

A bulletin the extractor took for another parish's (`wrong_bulletin`) ranks
behind every other: its date says nothing about this parish.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

# An issue date further ahead of its fetch than this is a misreading (the
# wrong year, a date from an event listing), not a bulletin posted early. The
# earliest posting seen is 13 days ahead. Without the cap, one misread date
# would stay the parish's "newest" bulletin until real time caught up with it.
MAX_DAYS_AHEAD_OF_FETCH = 21

# A stored issue date is trusted to skip next week's fetch only when the
# bulletin was fetched within this many days of it. On the 2026-09 corpus, 92%
# of dated bulletins fall within it; the rest were posted early or late, or
# misread, and are simply fetched again.
TRUSTED_DATE_DAYS = 4

# A parish whose newest bulletin is at least this much older than the run's
# Sunday has missed two weeks in a row.
STALE_BULLETIN_AGE_DAYS = 14


def nearest_sunday(day: date) -> date:
    """The Sunday of the week `day` belongs to, rounding Thursday forwards."""
    forward = (6 - day.weekday()) % 7
    return day + timedelta(days=forward) if forward <= 3 else day - timedelta(days=7 - forward)


_ISO_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def parse_iso_date(value: Any) -> date | None:
    """`value` as a date if it is a real day written YYYY-MM-DD, else None."""
    if not isinstance(value, str) or not _ISO_DATE_RE.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _fetched_day(entry: dict[str, Any]) -> date | None:
    fetched_at = entry.get("fetched_at")
    if not isinstance(fetched_at, str) or not fetched_at:
        return None
    return parse_iso_date(fetched_at[:10])


def bulletin_reference_date(entry: dict[str, Any]) -> date | None:
    """The date a bulletin's week starts from, for crediting its weekly rows.

    Prefers the issue date the extractor read off the bulletin itself. When
    that is missing (or dated implausibly far past the fetch) the fetch date
    stands in, snapped to the nearest Sunday. The raw fetch date cannot be used
    as-is: it lands anywhere from the day before publication to three days
    after, and for a Sunday weekly row that is the difference between crediting
    the bulletin's own Sunday and the next one — a whole week. Since 58 of the
    corpus's 59 parishes have some bulletins with an issue date and some
    without, an unsnapped fallback breaks those parishes' chains wherever the
    two kinds meet.

    Snapping to the *nearest* Sunday rather than the preceding one matters:
    bulletins are fetched on the Saturday before publication as often as on the
    Monday after, and rounding a Saturday backwards would land a full week
    early.
    """
    fetched = _fetched_day(entry)
    published = parse_iso_date(entry.get("published_date"))
    if published is not None and (
        fetched is None or published <= fetched + timedelta(days=MAX_DAYS_AHEAD_OF_FETCH)
    ):
        return published
    return None if fetched is None else nearest_sunday(fetched)


def bulletin_week(entry: dict[str, Any]) -> date | None:
    """The Sunday of the week a bulletin is for, or None if it has no date at all."""
    reference = bulletin_reference_date(entry)
    return None if reference is None else nearest_sunday(reference)


def _iso_date_sql(expr: str) -> str:
    """`expr` if it is a real day written YYYY-MM-DD, else NULL: `parse_iso_date`."""
    return f"CASE WHEN date({expr}) = {expr} THEN {expr} END"


def week_order_sql(alias: str = "") -> str:
    """`bulletin_week` as an SQL expression ('' for no date), for ORDER BY."""
    col = f"{alias}." if alias else ""
    fetched = _iso_date_sql(f"substr({col}fetched_at, 1, 10)")
    published_date = _iso_date_sql(f"{col}published_date")
    published = (
        f"CASE WHEN {fetched} IS NULL"
        f" OR {published_date} <= date({fetched}, '+{MAX_DAYS_AHEAD_OF_FETCH} days')"
        f" THEN {published_date} END"
    )
    # SQLite's 'weekday 0' moves forward to a Sunday, so going back three days
    # first lands Monday to Wednesday on the Sunday before, as nearest_sunday does.
    return (
        f"COALESCE(date({published}, '-3 days', 'weekday 0'),"
        f" date({fetched}, '-3 days', 'weekday 0'), '')"
    )


def _currency_key(entry: dict[str, Any]) -> tuple[bool, str, str, str, int]:
    week = bulletin_week(entry)
    return (
        not entry.get("wrong_bulletin"),
        week.isoformat() if week else "",
        str(entry.get("fetched_at") or ""),
        str(entry.get("processed_at") or ""),
        int(entry.get("id") or 0),
    )


def newest_bulletin(entries: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    """The bulletin for the latest week, the latest fetched of that week's.

    The ordering `storage.latest_bulletin_order` puts first: a second issue of
    the same week (a correction) displaces the first, and an old issue a site
    falls back to never displaces a newer one, however recently it was fetched.
    A bulletin flagged `wrong_bulletin` comes first only when there is no other.
    """
    return max(entries, key=_currency_key, default=None)


def has_bulletin_for(entry: dict[str, Any] | None, sunday: date) -> bool:
    """Whether `entry` is, by a date we can trust, the bulletin for `sunday`'s week.

    Only the extractor's date counts, and only when the bulletin was fetched
    around that date and the extractor took it for the parish's bulletin.
    """
    if entry is None or entry.get("wrong_bulletin"):
        return False
    published = parse_iso_date(entry.get("published_date"))
    fetched = _fetched_day(entry)
    if published is None or fetched is None:
        return False
    if abs((fetched - published).days) > TRUSTED_DATE_DAYS:
        return False
    return nearest_sunday(published) == sunday


@dataclass(frozen=True)
class Placement:
    """Where a newly processed bulletin's week falls among the parish's others."""

    kind: str
    """NEWER, CORRECTION, REPEATED_WEEK or OLDER."""

    week: date
    others: tuple[dict[str, Any], ...] = ()
    """For a repeated week, the week's earlier bulletins; for an older one,
    the newest bulletin it falls behind."""


NEWER = "newer"
CORRECTION = "correction"
REPEATED_WEEK = "repeated_week"
OLDER = "older"


def place_bulletin(
    entry: dict[str, Any], parish_bulletins: Iterable[dict[str, Any]],
) -> Placement | None:
    """How `entry`'s issue date compares with the parish's other processed bulletins.

    None when the extractor read no date, so there is nothing to compare.
    Bulletins the extractor rejected as the wrong PDF are left out: their dates
    say nothing about this parish.
    """
    if parse_iso_date(entry.get("published_date")) is None:
        return None
    week = bulletin_week(entry)
    if week is None:
        return None
    others = [
        other for other in parish_bulletins
        if other.get("id") != entry.get("id") and other.get("processed_at")
        and not other.get("wrong_bulletin") and bulletin_week(other) is not None
    ]
    newest = newest_bulletin(others)
    if newest is None or week > bulletin_week(newest):
        return Placement(NEWER, week)
    if week < bulletin_week(newest):
        return Placement(OLDER, week, (newest,))
    same_week = tuple(other for other in others if bulletin_week(other) == week)
    return Placement(CORRECTION if len(same_week) == 1 else REPEATED_WEEK, week, same_week)


def stale_parishes(
    bulletins: Iterable[dict[str, Any]], slugs: Iterable[str], *, today: date | None = None,
) -> dict[str, dict[str, Any] | None]:
    """Parish slug -> its newest bulletin, for those of `slugs` without a recent one.

    A parish with no bulletin at all maps to None. Judged by the bulletins'
    weeks, so a site that keeps serving an old issue is stale however often it
    was fetched. A bulletin flagged `wrong_bulletin` is not the parish's, so it
    keeps no parish fresh.
    """
    by_slug: dict[str, list[dict[str, Any]]] = {}
    for entry in bulletins:
        if entry.get("wrong_bulletin"):
            continue
        by_slug.setdefault(entry.get("parish_slug") or "", []).append(entry)
    sunday = nearest_sunday(today or date.today())
    stale: dict[str, dict[str, Any] | None] = {}
    for slug in slugs:
        newest = newest_bulletin(by_slug.get(slug, []))
        week = None if newest is None else bulletin_week(newest)
        if week is None or (sunday - week).days >= STALE_BULLETIN_AGE_DAYS:
            stale[slug] = newest
    return stale
