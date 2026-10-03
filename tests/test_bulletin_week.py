"""Tests for telling which week a bulletin is for, and which bulletin is current."""

from __future__ import annotations

import sqlite3
from datetime import date, timedelta

import pytest

from pdf_extract.bulletin_week import (
    CORRECTION,
    NEWER,
    OLDER,
    REPEATED_WEEK,
    bulletin_week,
    has_bulletin_for,
    nearest_sunday,
    newest_bulletin,
    place_bulletin,
    stale_parishes,
    week_order_sql,
)
from pdf_extract.storage import latest_bulletin_order

SUNDAY = date(2026, 10, 4)


def _bulletin(
    id: int, *, published: str | None, fetched: str | None, processed: bool = True, **extra,
) -> dict:
    return {
        "id": id,
        "parish_slug": "p",
        "published_date": published,
        "fetched_at": None if fetched is None else f"{fetched}T09:00:00Z",
        "processed_at": "2026-10-04T10:00:00Z" if processed else None,
        **extra,
    }


def test_nearest_sunday_rounds_thursday_forwards() -> None:
    days = [SUNDAY + timedelta(days=offset) for offset in range(-3, 4)]
    assert [nearest_sunday(day) for day in days] == [SUNDAY] * 7
    assert nearest_sunday(SUNDAY - timedelta(days=4)) == SUNDAY - timedelta(days=7)


def test_bulletin_week_reads_the_issue_date_and_rounds_a_vigil_date() -> None:
    assert bulletin_week(_bulletin(1, published="2026-10-03", fetched="2026-10-05")) == SUNDAY
    # Without an issue date, the fetch date stands in.
    assert bulletin_week(_bulletin(1, published=None, fetched="2026-10-06")) == SUNDAY
    assert bulletin_week(_bulletin(1, published=None, fetched=None)) is None


def test_bulletin_week_ignores_a_date_far_past_the_fetch() -> None:
    # A misread year would otherwise outrank every real bulletin for a year.
    assert bulletin_week(_bulletin(1, published="2027-10-03", fetched="2026-10-03")) == SUNDAY
    # Posted two weeks early is real.
    early = _bulletin(1, published="2026-10-18", fetched="2026-10-05")
    assert bulletin_week(early) == date(2026, 10, 18)


@pytest.mark.parametrize("published", [
    None, "2026-09-27", "2026-10-03", "2027-01-01", "junk",
    # Dates SQLite's date() misreads or cannot read: neither side reads them.
    "10/04/2026", "September 27, 2026", "2026-02-30", " 2026-10-04", "2026-10-4",
])
@pytest.mark.parametrize("fetched", [None, "2026-09-30", "2026-10-01", "2026-10-03", "junk"])
def test_week_order_sql_agrees_with_bulletin_week(published, fetched) -> None:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE bulletin (published_date TEXT, fetched_at TEXT)")
    fetched_at = None if fetched is None else f"{fetched}T09:00:00Z"
    conn.execute("INSERT INTO bulletin VALUES (?, ?)", (published, fetched_at))
    [sql_week] = conn.execute(f"SELECT {week_order_sql()} FROM bulletin").fetchone()
    python_week = bulletin_week({"published_date": published, "fetched_at": fetched_at})
    assert sql_week == (python_week.isoformat() if python_week else "")


def test_newest_bulletin_lets_a_correction_but_not_an_old_issue_displace_the_current() -> None:
    current = _bulletin(1, published="2026-10-04", fetched="2026-10-03")
    correction = _bulletin(2, published="2026-10-03", fetched="2026-10-05")
    old_issue = _bulletin(3, published="2026-09-20", fetched="2026-10-06")
    assert newest_bulletin([current, old_issue]) is current
    assert newest_bulletin([current, correction, old_issue]) is correction
    assert newest_bulletin([]) is None


def test_newest_bulletin_puts_a_wrong_bulletin_behind_every_other() -> None:
    real = _bulletin(1, published="2026-09-27", fetched="2026-09-26")
    wrong = _bulletin(2, published="2026-10-04", fetched="2026-10-03", wrong_bulletin=1)
    assert newest_bulletin([real, wrong]) is real
    assert newest_bulletin([wrong]) is wrong


def test_latest_bulletin_order_agrees_with_newest_bulletin() -> None:
    bulletins = [
        _bulletin(1, published="2026-09-27", fetched="2026-09-26", wrong_bulletin=0),
        _bulletin(2, published="2026-10-04", fetched="2026-10-03", wrong_bulletin=1),
        _bulletin(3, published=None, fetched="2026-09-19", wrong_bulletin=0),
        _bulletin(4, published="10/04/2026", fetched="2026-09-25", wrong_bulletin=0),
    ]
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE bulletin (id INTEGER, published_date TEXT, fetched_at TEXT,"
        " processed_at TEXT, wrong_bulletin INTEGER)"
    )
    conn.executemany(
        "INSERT INTO bulletin VALUES (:id, :published_date, :fetched_at, :processed_at,"
        " :wrong_bulletin)",
        bulletins,
    )
    sql_order = [
        row[0] for row in conn.execute(
            f"SELECT id FROM bulletin ORDER BY {latest_bulletin_order()}"
        )
    ]
    assert sql_order[0] == newest_bulletin(bulletins)["id"] == 1
    assert sql_order[-1] == 2


def test_has_bulletin_for_trusts_only_a_plausible_extracted_date() -> None:
    assert has_bulletin_for(_bulletin(1, published="2026-10-04", fetched="2026-10-03"), SUNDAY)
    assert has_bulletin_for(_bulletin(1, published="2026-10-03", fetched="2026-10-05"), SUNDAY)
    assert not has_bulletin_for(_bulletin(1, published="2026-09-27", fetched="2026-09-26"), SUNDAY)
    assert not has_bulletin_for(_bulletin(1, published=None, fetched="2026-10-03"), SUNDAY)
    assert not has_bulletin_for(_bulletin(1, published="2026-10-04", fetched="2026-09-21"), SUNDAY)
    assert not has_bulletin_for(
        _bulletin(1, published="2026-10-04", fetched="2026-10-03", wrong_bulletin=1), SUNDAY,
    )
    assert not has_bulletin_for(None, SUNDAY)


def test_place_bulletin() -> None:
    week_before = _bulletin(1, published="2026-09-27", fetched="2026-09-26")
    this_week = _bulletin(2, published="2026-10-04", fetched="2026-10-03")
    correction = _bulletin(3, published="2026-10-04", fetched="2026-10-04")

    new = _bulletin(9, published="2026-10-04", fetched="2026-10-03")
    assert place_bulletin(new, [week_before, new]).kind == NEWER

    placement = place_bulletin(new, [week_before, this_week, new])
    assert placement.kind == CORRECTION
    assert placement.others == (this_week,)

    placement = place_bulletin(new, [week_before, this_week, correction, new])
    assert placement.kind == REPEATED_WEEK
    assert placement.others == (this_week, correction)

    old = _bulletin(9, published="2026-09-20", fetched="2026-10-05")
    placement = place_bulletin(old, [week_before, this_week, old])
    assert (placement.kind, placement.others) == (OLDER, (this_week,))

    assert place_bulletin(_bulletin(9, published=None, fetched="2026-10-03"), [this_week]) is None


def test_place_bulletin_ignores_unprocessed_and_wrong_bulletins() -> None:
    unprocessed = _bulletin(1, published=None, fetched="2026-10-03", processed=False)
    wrong = _bulletin(2, published="2026-10-11", fetched="2026-10-03", wrong_bulletin=1)
    new = _bulletin(9, published="2026-10-04", fetched="2026-10-03")
    assert place_bulletin(new, [unprocessed, wrong, new]).kind == NEWER


def test_stale_parishes_judges_by_the_bulletins_week() -> None:
    bulletins = [
        _bulletin(1, published="2026-09-27", fetched="2026-09-26") | {"parish_slug": "behind"},
        # Fetched this week, but an issue from a month ago.
        _bulletin(2, published="2026-09-06", fetched="2026-10-03") | {"parish_slug": "old"},
        _bulletin(3, published="2026-09-20", fetched="2026-09-19") | {"parish_slug": "stuck"},
    ]
    stale = stale_parishes(bulletins, ["behind", "old", "stuck", "never"], today=SUNDAY)
    assert sorted(stale) == ["never", "old", "stuck"]
    # Another parish's bulletin keeps no parish fresh.
    wrong = _bulletin(4, published="2026-10-04", fetched="2026-10-03", wrong_bulletin=1)
    assert stale_parishes([wrong], ["p"], today=SUNDAY) == {"p": None}
    assert stale["never"] is None
    assert stale["old"]["id"] == 2
