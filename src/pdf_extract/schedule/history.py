"""Which week each of a parish's update calls is for, and its high-water mark.

A call's week is `bulletin_week` of the issue date the model read, with the
existing cap on dates implausibly far past the fetch. A call that read no date,
or an implausible one, is undated: it is applied but never moves the mark.

The parish's high-water mark is the newest week among its earlier calls that
succeeded, weren't a wrong bulletin or stale, and were dated, and never older
than the week of the newest dated bulletin (not a wrong bulletin) fetched on or
before its latest seed's `as_of`. A call older than the mark is stale.

The history is worked out again from the calls each time, in call order, so
nothing about it needs storing: a stale call is one whose week was older than
the mark when it was made.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import date

from pdf_extract.bulletin_week import MAX_DAYS_AHEAD_OF_FETCH, nearest_sunday, parse_iso_date

SUCCEEDED = ("ok", "lenient")


def call_week(published_date: str | None, fetched_at: str | None) -> date | None:
    """The Sunday of the week a call is for, or None when it is undated.

    Undated: no date read, or one more than `MAX_DAYS_AHEAD_OF_FETCH` past the
    fetch. `bulletin_week` would fall back to the fetch date there, but that is
    only a guess, and a wrong guess would make the next dated bulletin stale.
    """
    published = parse_iso_date(published_date)
    if published is None:
        return None
    fetched = parse_iso_date((fetched_at or "")[:10])
    if fetched is not None and (published - fetched).days > MAX_DAYS_AHEAD_OF_FETCH:
        return None
    return nearest_sunday(published)


def seed_mark(conn: sqlite3.Connection, parish_id: int, as_of: str | None) -> date | None:
    """The week of the newest dated bulletin fetched on or before the seed's `as_of`."""
    if as_of is None:
        return None
    rows = conn.execute(
        """SELECT published_date, fetched_at FROM bulletin
           WHERE parish_id = ? AND COALESCE(wrong_bulletin, 0) = 0
             AND published_date IS NOT NULL AND fetched_at IS NOT NULL AND fetched_at <= ?""",
        (parish_id, as_of),
    ).fetchall()
    weeks = [w for r in rows if (w := call_week(r["published_date"], r["fetched_at"]))]
    return max(weeks, default=None)


@dataclass(frozen=True)
class CallPlace:
    """Where one successful call falls in its parish's history."""

    llm_call_id: int
    bulletin_id: int
    week: date | None
    """None: undated."""
    wrong_bulletin: bool
    stale: bool
    same_week_before: int
    """How many earlier counted calls were for the same week (1: a correction)."""
    mark_before: date | None


def place_call(
    *,
    week: date | None,
    wrong_bulletin: bool,
    mark: date | None,
    counted_weeks: list[date],
) -> tuple[bool, int]:
    """(stale, earlier calls for the same week) for a call given the history before it."""
    if wrong_bulletin or week is None:
        return False, 0
    if mark is not None and week < mark:
        return True, 0
    return False, sum(1 for w in counted_weeks if w == week)


@dataclass
class History:
    """A parish's successful calls placed in order, and where the next call would fall."""

    places: list[CallPlace]
    mark: date | None
    """The high-water mark for the next call."""
    counted_weeks: list[date]
    """The weeks of the bulletins counted so far: each seed's newest dated bulletin,
    and every call that succeeded, was dated, and wasn't a wrong bulletin or stale."""


def parish_history(conn: sqlite3.Connection, parish_id: int) -> History:
    """Every successful call of the parish placed in order, and the mark after them.

    Each call is placed against the seed it was made under (the latest seed
    revision at or before the call's base revision), so a later seed doesn't
    change how an earlier call was placed. A seed's newest dated bulletin
    counts as that week's first bulletin, so the next one for the same week is
    a correction.
    """
    seeds = conn.execute(
        """SELECT revision, as_of FROM schedule_revision
           WHERE parish_id = ? AND source_kind = 'seed' ORDER BY revision""",
        (parish_id,),
    ).fetchall()
    floors = [(s["revision"], seed_mark(conn, parish_id, s["as_of"])) for s in seeds]
    applied_seeds = 0
    mark: date | None = None
    counted: list[date] = []

    def apply_seeds(up_to_revision: int | None) -> None:
        nonlocal applied_seeds, mark
        while applied_seeds < len(floors) and (
            up_to_revision is None or floors[applied_seeds][0] <= up_to_revision
        ):
            floor = floors[applied_seeds][1]
            applied_seeds += 1
            if floor is not None:
                counted.append(floor)
                mark = floor if mark is None else max(mark, floor)

    places: list[CallPlace] = []
    rows = conn.execute(
        f"""SELECT c.id, c.bulletin_id, c.published_date, c.wrong_bulletin, c.base_revision,
                   b.fetched_at
            FROM llm_call c JOIN bulletin b ON b.id = c.bulletin_id
            WHERE c.parish_id = ? AND c.status IN ({", ".join("?" * len(SUCCEEDED))})
            ORDER BY c.id""",
        (parish_id, *SUCCEEDED),
    ).fetchall()
    for row in rows:
        apply_seeds(row["base_revision"])
        week = call_week(row["published_date"], row["fetched_at"])
        wrong = bool(row["wrong_bulletin"])
        stale, same_week = place_call(
            week=week, wrong_bulletin=wrong, mark=mark, counted_weeks=counted,
        )
        places.append(CallPlace(
            llm_call_id=row["id"], bulletin_id=row["bulletin_id"], week=week,
            wrong_bulletin=wrong, stale=stale, same_week_before=same_week, mark_before=mark,
        ))
        if week is not None and not wrong and not stale:
            counted.append(week)
            mark = week if mark is None else max(mark, week)
    apply_seeds(None)
    return History(places, mark, counted)
