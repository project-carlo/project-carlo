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
    month_in_season,
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


def test_half_stated_season_is_no_season() -> None:
    """Without both ends the slot stays year-round rather than half-hidden."""
    assert normalize_season("October", None) == (None, None)
    assert normalize_season(None, "June") == (None, None)
    assert normalize_season("October", "June") == (10, 6)


@pytest.mark.parametrize(
    ("month", "expected"),
    [(9, False), (10, True), (12, True), (1, True), (6, True), (7, False)],
)
def test_season_wrapping_the_new_year(month: int, expected: bool) -> None:
    """October through June covers the turn of the year, not the middle of it."""
    assert month_in_season(month, 10, 6) is expected


@pytest.mark.parametrize(
    ("month", "expected"), [(5, False), (6, True), (8, True), (9, False)],
)
def test_season_within_one_year(month: int, expected: bool) -> None:
    assert month_in_season(month, 6, 8) is expected


def test_no_season_means_every_month() -> None:
    assert all(month_in_season(month, None, None) for month in range(1, 13))


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
        _weekly_payload(season_start_month="October", season_end_month="June")
    )
    event = reconstruct_events(payload)["events"][0]
    assert event["season_start_month"] == 10
    assert event["season_end_month"] == 6
    assert event["weeks_of_month"] == []


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
        ("October through June", "Tuesday",
         {"season_start_month": 10, "season_end_month": 6, "note": None}),
        ("June 4 - September 10", "Thursday",
         {"season_start_month": 6, "season_end_month": 9, "note": None}),
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
