"""Recurrence qualifiers: weeks of the month, and partial-year season ranges."""

from __future__ import annotations

from datetime import date

import pytest

from pdf_extract.recurrence import occurrence_from_row
from pdf_extract.runner import flatten_extracted_events
from pdf_extract.schedule_extraction import (
    EVENTS_SYSTEM_PROMPT,
    SCHEMA_VERSION,
    WEEKLY_QUALIFIER_PROMPT,
    SchedulePayload,
    WeeklySlot,
    reconstruct_events,
)
from pdf_extract.schedule_pattern import (
    NO_SEASON,
    Season,
    date_in_season,
    date_matches_pattern,
    date_matches_weeks,
    describe_schedule_pattern,
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


# ── Date matching ───────────────────────────────────────────────────────────
# September 2026: Fridays fall on the 4th, 11th, 18th and 25th.
_SEPTEMBER_FRIDAYS = [date(2026, 9, day) for day in (4, 11, 18, 25)]


def test_empty_weeks_match_every_date() -> None:
    assert all(date_matches_weeks(day, []) for day in _SEPTEMBER_FRIDAYS)


def test_first_week_matches_only_the_first_occurrence() -> None:
    assert [date_matches_weeks(day, ["first"]) for day in _SEPTEMBER_FRIDAYS] == [
        True, False, False, False,
    ]


def test_weeks_count_weekday_occurrences_not_calendar_weeks() -> None:
    """The 4th is the first Friday even though it sits in a partial week."""
    assert date_matches_weeks(date(2026, 9, 11), ["second"]) is True


def test_last_is_not_fourth() -> None:
    """October 2026 has five Fridays: 2, 9, 16, 23, 30."""
    assert date_matches_weeks(date(2026, 10, 23), ["last"]) is False
    assert date_matches_weeks(date(2026, 10, 30), ["last"]) is True
    assert date_matches_weeks(date(2026, 10, 23), ["fourth"]) is True


def test_several_named_weeks_match_any_of_them() -> None:
    assert [
        date_matches_weeks(day, ["second", "fourth"]) for day in _SEPTEMBER_FRIDAYS
    ] == [False, True, False, True]


def test_date_matches_pattern_requires_week_and_season() -> None:
    season = normalize_season("October", None, "June", None)
    # First Friday of October, in season.
    assert date_matches_pattern(date(2026, 10, 2), ["first"], season) is True
    # First Friday of September, out of season.
    assert date_matches_pattern(date(2026, 9, 4), ["first"], season) is False
    # In season, but the third Friday.
    assert date_matches_pattern(date(2026, 10, 16), ["first"], season) is False


# ── Display copy ────────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    ("weeks", "season", "day", "expected"),
    [
        ([], NO_SEASON, "Friday", None),
        (["first"], NO_SEASON, "Friday", "First Friday of the month"),
        (["second", "fourth"], NO_SEASON, "saturday",
         "Second and fourth Saturdays of the month"),
        ([], normalize_season("October", None, "June", None), "Tuesday",
         "October through June"),
        ([], normalize_season("June", 4, "September", 10), "Thursday",
         "June 4 through September 10"),
        ([], normalize_season("January", None, "April", None), "Wednesday",
         "January through April"),
        (["first"], normalize_season("October", None, "June", None), "Friday",
         "First Friday of the month, October through June"),
    ],
)
def test_describe_schedule_pattern_matches_the_bulletin_grain(
    weeks: list[str], season: Season, day: str, expected: str | None,
) -> None:
    assert describe_schedule_pattern(weeks, season, day) == expected


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


# ── Qualifier prompt (the quality lever) ────────────────────────────────────
def test_qualifier_policy_lives_in_its_own_prompt_block() -> None:
    """A reviewer can read the qualifier rules without the rest of the extractor."""
    assert WEEKLY_QUALIFIER_PROMPT.strip().startswith("# Weekly schedule qualifiers")
    assert WEEKLY_QUALIFIER_PROMPT in EVENTS_SYSTEM_PROMPT
    head, _, _ = EVENTS_SYSTEM_PROMPT.partition("# Weekly schedule qualifiers")
    assert "weeks_of_month" not in head
    assert "season_start_month" not in head


def test_a_wording_only_prompt_change_invalidates_cached_extractions() -> None:
    """Classifiers fold SCHEMA_VERSION into the cache key; bump it with the prompt."""
    assert SCHEMA_VERSION >= 4


@pytest.mark.parametrize(
    "needle",
    [
        "still belongs in `weekly_schedule`",
        "Empty means every week",
        "Set both months or neither",
        "Do not invent the 1st or the 30th",
        "summer is June through August",
        "school-year schedule is September through June",
        "does not run in July or August is September through June",
        "Do not restate in `note`",
        "language",
        "benediction",
        "every Saturday except the first",
        "First Friday",
        "1st and 3rd Saturdays",
        "October through June",
        "June 4 through September 10",
    ],
)
def test_qualifier_prompt_states_the_hard_case_policy(needle: str) -> None:
    """The isolated block, not implicit model judgment, decides these cases."""
    assert needle in WEEKLY_QUALIFIER_PROMPT


def test_weekly_slot_field_descriptions_steer_the_same_policy() -> None:
    fields = WeeklySlot.model_fields
    assert "every week" in fields["weeks_of_month"].description
    assert "last` is not `fourth" in fields["weeks_of_month"].description
    assert "both null" in fields["season_start_month"].description
    assert "Do not invent the 1st" in fields["season_start_day"].description
    assert "Do not invent the 30th" in fields["season_end_day"].description
    assert "Do not restate" in fields["note"].description
