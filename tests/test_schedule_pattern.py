"""Recurrence qualifiers: weeks of the month, and partial-year season ranges."""

from __future__ import annotations

import json
from datetime import date

import pytest

from pdf_extract.pattern_backfill import backfill_patterns, derive_pattern
from pdf_extract.recurrence import occurrence_from_row
from pdf_extract.runner import flatten_extracted_events
from pdf_extract.schedule_extraction import SchedulePayload, reconstruct_events
from pdf_extract.schedule_pattern import (
    NO_SEASON,
    Season,
    date_in_season,
    normalize_day,
    normalize_month,
    normalize_season,
    normalize_weeks_of_month,
    weeks_of_month_to_text,
)


# ── Normalisation ───────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, []),
        ([], []),
        (["first"], ["first"]),
        (["1st"], ["first"]),
        ([1], ["first"]),
        ("first,third", ["first", "third"]),
        (["Last"], ["last"]),
        # Canonical order, whatever order the bulletin listed them in.
        (["4th", "2nd"], ["second", "fourth"]),
        # Duplicates collapse; unreadable entries are dropped, not guessed at.
        (["first", "FIRST", "occasionally"], ["first"]),
    ],
)
def test_normalize_weeks_of_month(raw: object, expected: list[str]) -> None:
    assert normalize_weeks_of_month(raw) == expected


def test_weeks_of_month_to_text() -> None:
    assert weeks_of_month_to_text(["first", "third"]) == "first,third"
    assert weeks_of_month_to_text([]) is None


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("October", 10), ("october", 10), ("Oct", 10), ("Sept", 9), ("Sep", 9),
        (6, 6), ("6", 6), (0, None), (13, None), ("Smarch", None), (None, None),
        (True, None),
    ],
)
def test_normalize_month(raw: object, expected: int | None) -> None:
    assert normalize_month(raw) == expected


@pytest.mark.parametrize(
    ("raw", "month", "expected"),
    [
        (4, 6, 4), ("4", 6, 4), ("4th", 6, 4), (31, 1, 31),
        # February keeps its leap day: a boundary is a position in every year.
        (29, 2, 29), (30, 2, None),
        (31, 9, None), (0, 6, None), (None, 6, None), (True, 6, None),
        # A day without a month has nothing to refine.
        (4, None, None),
    ],
)
def test_normalize_day(raw: object, month: int | None, expected: int | None) -> None:
    assert normalize_day(raw, month) == expected


def test_half_stated_season_is_no_season() -> None:
    """Without both ends the slot stays year-round rather than half-hidden."""
    assert normalize_season("October", None, None) == NO_SEASON
    assert normalize_season(None, None, "June") == NO_SEASON
    assert normalize_season("October", None, "June", None) == Season(10, None, 6, None)


def test_season_keeps_the_days_a_bulletin_stated() -> None:
    assert normalize_season("June", "4", "September", 10) == Season(6, 4, 9, 10)


def test_an_impossible_day_falls_back_to_its_whole_month() -> None:
    assert normalize_season("February", 30, "April", 31) == Season(2, None, 4, None)


@pytest.mark.parametrize(
    ("month", "day", "expected"),
    [(9, 30, False), (10, 1, True), (12, 31, True), (1, 1, True),
     (6, 30, True), (7, 1, False)],
)
def test_season_wrapping_the_new_year(month: int, day: int, expected: bool) -> None:
    """October through June covers the turn of the year, not the middle of it."""
    season = normalize_season("October", None, "June", None)
    assert date_in_season(month, day, season) is expected


@pytest.mark.parametrize(
    ("month", "day", "expected"),
    [(5, 31, False), (6, 1, True), (8, 31, True), (9, 1, False)],
)
def test_season_within_one_year(month: int, day: int, expected: bool) -> None:
    season = normalize_season("June", None, "August", None)
    assert date_in_season(month, day, season) is expected


@pytest.mark.parametrize(
    ("month", "day", "expected"),
    [(6, 3, False), (6, 4, True), (7, 15, True), (9, 10, True), (9, 11, False)],
)
def test_dated_season_runs_to_the_day(month: int, day: int, expected: bool) -> None:
    """"June 4 through September 10" does not start on the 1st of June."""
    season = normalize_season("June", 4, "September", 10)
    assert date_in_season(month, day, season) is expected


@pytest.mark.parametrize(
    ("month", "day", "expected"),
    [(10, 14, False), (10, 15, True), (2, 1, True), (4, 20, True), (4, 21, False)],
)
def test_dated_season_wrapping_the_new_year(
    month: int, day: int, expected: bool,
) -> None:
    season = normalize_season("October", 15, "April", 20)
    assert date_in_season(month, day, season) is expected


def test_no_season_means_every_day() -> None:
    assert all(date_in_season(month, 1, NO_SEASON) for month in range(1, 13))


# ── Extraction ──────────────────────────────────────────────────────────────
def _weekly_payload(**slot: object) -> dict:
    return {
        "weekly_schedule": {
            "confessions": [
                {
                    "church_slug": "holy-trinity",
                    "day_of_week": "Tuesday",
                    "start_time": "4:30 PM",
                    **slot,
                },
            ],
        },
    }


def test_extraction_canonicalises_the_qualifiers() -> None:
    payload = SchedulePayload.model_validate(
        _weekly_payload(
            season_start_month="October",
            season_end_month="June",
        )
    )
    event = reconstruct_events(payload)["events"][0]
    assert event["season_start_month"] == 10
    assert event["season_end_month"] == 6
    # No days, because the bulletin named none; the range is a whole-month one.
    assert event["season_start_day"] is None
    assert event["season_end_day"] is None
    assert event["weeks_of_month"] == []


def test_extraction_keeps_a_dated_range() -> None:
    payload = SchedulePayload.model_validate(
        _weekly_payload(
            season_start_month="June", season_start_day=4,
            season_end_month="September", season_end_day=10,
        )
    )
    event = reconstruct_events(payload)["events"][0]
    assert event["season_start_day"] == 4
    assert event["season_end_day"] == 10


def test_lenient_path_carries_the_qualifiers() -> None:
    """A response Pydantic rejects still keeps the qualifiers it did state."""
    event = reconstruct_events(_weekly_payload(weeks_of_month=["1st"]))["events"][0]
    assert event["weeks_of_month"] == ["first"]


def test_dated_slots_carry_no_qualifiers() -> None:
    """Only a recurring slot can be qualified; a date is already specific."""
    payload = SchedulePayload.model_validate(
        {"single_events": {"masses": [
            {"church_slug": "st-mary", "date": "2026-09-04", "start_time": "8:00 AM"},
        ]}}
    )
    event = reconstruct_events(payload)["events"][0]
    assert event["weeks_of_month"] == []
    assert event["season_start_month"] is None


def test_events_json_omits_the_qualifiers_when_unset() -> None:
    """Most slots carry neither, and events.json is rewritten every week."""
    entry = {"source_url": "https://example.test/b.pdf"}
    plain, qualified = flatten_extracted_events(entry, {"events": [
        {"church_slug": "a", "type": "mass", "kind": "weekly",
         "day_of_week": "Sunday", "start_time": "9:00 AM"},
        {"church_slug": "b", "type": "adoration", "kind": "weekly",
         "day_of_week": "Friday", "start_time": "7:00 PM",
         "weeks_of_month": ["first"], "season_start_month": 10,
         "season_end_month": 6},
    ]})
    assert "weeks_of_month" not in plain
    assert "season_start_month" not in plain
    assert qualified["weeks_of_month"] == ["first"]
    assert qualified["season_start_month"] == 10
    assert qualified["season_end_month"] == 6
    # Days the bulletin never named stay off the row rather than arriving null.
    assert "season_start_day" not in qualified
    assert "season_end_day" not in qualified


def test_events_json_keeps_the_days_a_bulletin_did_name() -> None:
    entry = {"source_url": "https://example.test/b.pdf"}
    (row,) = flatten_extracted_events(entry, {"events": [
        {"church_slug": "a", "type": "mass", "kind": "weekly",
         "day_of_week": "Thursday", "start_time": "8:30 AM",
         "season_start_month": 6, "season_start_day": 4,
         "season_end_month": 9, "season_end_day": 10},
    ]})
    assert row["season_start_day"] == 4
    assert row["season_end_day"] == 10


# ── Recurrence evidence ─────────────────────────────────────────────────────
def _weekly_row(**extra: object) -> dict:
    return {
        "church_slug": "st-ambrose",
        "event_type": "adoration",
        "event_kind": "weekly",
        "day_of_week": "Friday",
        "start_time": "7:00 PM",
        **extra,
    }


def test_plain_weekly_row_is_credited_to_its_bulletin_week() -> None:
    occurrence = occurrence_from_row(
        _weekly_row(), bulletin_date=date(2026, 9, 6),
    )
    assert occurrence is not None
    assert occurrence[1] == date(2026, 9, 11)


def test_monthly_row_is_not_evidence_of_a_weekly_slot() -> None:
    """Crediting a first-Friday slot every week would invent three sightings."""
    assert occurrence_from_row(
        _weekly_row(weeks_of_month=["first"]), bulletin_date=date(2026, 9, 6),
    ) is None


def test_out_of_season_row_is_not_evidence() -> None:
    """A September bulletin listing an October-to-June slot saw nothing yet."""
    assert occurrence_from_row(
        _weekly_row(season_start_month=10, season_end_month=6),
        bulletin_date=date(2026, 9, 6),
    ) is None


def test_in_season_row_is_still_evidence() -> None:
    occurrence = occurrence_from_row(
        _weekly_row(season_start_month=10, season_end_month=6),
        bulletin_date=date(2026, 10, 4),
    )
    assert occurrence is not None
    assert occurrence[1] == date(2026, 10, 9)


def test_a_season_that_starts_mid_month_is_read_to_the_day() -> None:
    """A slot starting October 15 saw nothing on the Friday of October 9."""
    row = _weekly_row(
        season_start_month=10, season_start_day=15,
        season_end_month=6, season_end_day=1,
    )
    assert occurrence_from_row(row, bulletin_date=date(2026, 10, 4)) is None
    assert occurrence_from_row(row, bulletin_date=date(2026, 10, 18)) is not None


# ── Backfill from notes ─────────────────────────────────────────────────────
@pytest.mark.parametrize(
    ("note", "day", "expected"),
    [
        ("First Fridays after 8:30 AM Mass", "Friday",
         {"weeks_of_month": ["first"], "note": "after 8:30 AM Mass"}),
        ("Last Thursdays after 8:30 AM Mass", "Thursday",
         {"weeks_of_month": ["last"], "note": "after 8:30 AM Mass"}),
        ("1st, 2nd, and 4th weeks of the month", "Wednesday",
         {"weeks_of_month": ["first", "second", "fourth"], "note": None}),
        ("Spanish, 2nd & 4th Saturdays", "Saturday",
         {"weeks_of_month": ["second", "fourth"], "note": "Spanish"}),
        ("Healing Mass, First Monday of the month", "Monday",
         {"weeks_of_month": ["first"], "note": "Healing Mass"}),
        # A note left saying only what the row already says is dropped.
        ("First Saturday Mass", "Saturday",
         {"weeks_of_month": ["first"], "note": None}),
        ("First Friday of the month; ends with benediction", "Friday",
         {"weeks_of_month": ["first"], "note": "ends with benediction"}),
        # A season named in whole months keeps no days, so it is described
        # back in the whole months the bulletin printed.
        ("October through June", "Tuesday",
         {"season_start_month": 10, "season_end_month": 6, "note": None}),
        ("June 4 - September 10", "Thursday",
         {"season_start_month": 6, "season_start_day": 4,
          "season_end_month": 9, "season_end_day": 10, "note": None}),
        ("Sept. 8 to May 30, Latin", "Sunday",
         {"season_start_month": 9, "season_start_day": 8,
          "season_end_month": 5, "season_end_day": 30, "note": "Latin"}),
        # The year beside a month is not a day of it.
        ("October through June 2027", "Tuesday",
         {"season_start_month": 10, "season_end_month": 6, "note": "2027"}),
        # Both qualifiers at once.
        ("1st Saturdays, June 1 through August 31", "Saturday",
         {"weeks_of_month": ["first"], "season_start_month": 6,
          "season_start_day": 1, "season_end_month": 8, "season_end_day": 31,
          "note": None}),
    ],
)
def test_derive_pattern_reads_a_stated_schedule(
    note: str, day: str, expected: dict,
) -> None:
    assert derive_pattern(note, day) == expected


@pytest.mark.parametrize(
    ("note", "day"),
    [
        # An exclusion names the week the slot does *not* run, which the fields
        # cannot express; reading it as first-Saturday-only inverts it.
        ("Except 1st Saturday of the month", "Saturday"),
        ("Except second Tuesdays", "Tuesday"),
        ("Except summer", "Sunday"),
        # The months a parish means by "summer" are not on the page.
        ("Summer Mass", "Sunday"),
        ("Resumes in September", "Monday"),
        # An ordinal about some other weekday is not this row's schedule.
        ("First Friday devotions follow", "Sunday"),
        ("Includes Rosary", "Monday"),
        (None, "Monday"),
        ("", "Monday"),
    ],
)
def test_derive_pattern_leaves_unclear_notes_alone(note: str | None, day: str) -> None:
    assert derive_pattern(note, day) is None


def test_backfill_updates_only_weekly_rows_without_qualifiers(tmp_path) -> None:
    events_path = tmp_path / "events.json"
    events_path.write_text(json.dumps([
        {"church_slug": "holy-trinity", "event_kind": "weekly",
         "day_of_week": "Tuesday", "start_time": "4:30 PM",
         "note": "October through June"},
        # A dated row's note describes that one date, not a recurrence.
        {"church_slug": "holy-family", "event_kind": "specific_date",
         "date": "2026-09-04", "start_time": "9:30 AM", "note": "First Friday"},
        # The extractor's own reading outranks a second-hand one off a note.
        {"church_slug": "st-ambrose", "event_kind": "weekly",
         "day_of_week": "Friday", "start_time": "11:00 AM",
         "note": "1st Fridays", "weeks_of_month": ["second"]},
    ]), encoding="utf-8")

    result = backfill_patterns(events_path)
    assert result == {"events": 3, "monthly": 0, "seasonal": 1, "dry_run": 0}

    rows = json.loads(events_path.read_text(encoding="utf-8"))
    assert rows[0]["season_start_month"] == 10
    assert rows[0]["season_end_month"] == 6
    # No day either side, because the bulletin named neither.
    assert "season_start_day" not in rows[0]
    assert "season_end_day" not in rows[0]
    assert rows[0]["note"] is None
    assert "weeks_of_month" not in rows[1]
    assert rows[1]["note"] == "First Friday"
    assert rows[2]["weeks_of_month"] == ["second"]


def test_backfill_dry_run_writes_nothing(tmp_path) -> None:
    events_path = tmp_path / "events.json"
    original = json.dumps([
        {"church_slug": "holy-trinity", "event_kind": "weekly",
         "day_of_week": "Tuesday", "start_time": "4:30 PM",
         "note": "October through June"},
    ])
    events_path.write_text(original, encoding="utf-8")

    result = backfill_patterns(events_path, dry_run=True)
    assert result["seasonal"] == 1
    assert events_path.read_text(encoding="utf-8") == original
