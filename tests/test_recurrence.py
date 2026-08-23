"""Tests for promoting repeatedly-dated events to weekly ones."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.recurrence import (
    HISTORY_RETENTION_WEEKS,
    LOOKBACK_WEEKS,
    MIN_PRIOR_WEEKS,
    History,
    apply_recurrence,
    bulletin_reference_date,
    load_history,
    occurrence_from_row,
    promote_recurring_events,
    prune_history,
    record_observations,
    save_history,
)
from pdf_extract.storage import save_json_list

BASE_DATE = date(2026, 8, 19)  # a Wednesday


def _dated_row(
    event_date: date,
    *,
    church_slug: str = "st-mary-anytown",
    event_type: str = "adoration",
    start_time: str = "7:00 PM",
    **overrides: Any,
) -> dict[str, Any]:
    row = {
        "church_slug": church_slug,
        "bulletin_source_url": "https://example.org/bulletin.pdf",
        "event_type": event_type,
        "event_kind": "specific_date",
        "day_of_week": None,
        "date": event_date.isoformat(),
        "start_time": start_time,
        "end_time": None,
        "cancelled": False,
        "page_number": 1,
        "note": None,
    }
    row.update(overrides)
    return row


def _weekly_row(day_of_week: str, **overrides: Any) -> dict[str, Any]:
    row = {
        "church_slug": "st-mary-anytown",
        "bulletin_source_url": "https://example.org/bulletin.pdf",
        "event_type": "adoration",
        "event_kind": "weekly",
        "day_of_week": day_of_week,
        "date": None,
        "start_time": "7:00 PM",
        "end_time": None,
        "cancelled": False,
        "page_number": 1,
        "note": None,
    }
    row.update(overrides)
    return row


def _history_for(weeks_back: list[int], **row_kwargs: Any) -> History:
    """History holding the slot as a dated sighting in each of `weeks_back`."""
    history: History = {}
    rows = [_dated_row(BASE_DATE - timedelta(weeks=w), **row_kwargs) for w in weeks_back]
    record_observations(history, rows, bulletin_date=None)
    return history


def _weekly_history_for(weeks_back: list[int], day_of_week: str = "Wednesday") -> History:
    """History holding the slot as a *weekly* sighting in each of `weeks_back`.

    Each sighting comes from its own bulletin, published the Sunday before the
    week it covers, exactly as the pipeline would record it.
    """
    history: History = {}
    for weeks in weeks_back:
        covered = BASE_DATE - timedelta(weeks=weeks)
        published = covered - timedelta(days=covered.weekday() + 1)  # the Sunday before
        record_observations(
            history, [_weekly_row(day_of_week)], bulletin_date=published,
        )
    return history


# ── Occurrences ─────────────────────────────────────────────────────────────
def test_dated_row_is_credited_to_its_own_date() -> None:
    occurrence = occurrence_from_row(
        _dated_row(BASE_DATE, start_time="7:00 p.m."), bulletin_date=None
    )
    assert occurrence == (("st-mary-anytown", "adoration", 1140), BASE_DATE)


def test_weekly_row_is_credited_to_the_week_its_bulletin_covers() -> None:
    published = date(2026, 8, 16)  # the Sunday before BASE_DATE
    occurrence = occurrence_from_row(_weekly_row("Wednesday"), bulletin_date=published)
    assert occurrence == (("st-mary-anytown", "adoration", 1140), BASE_DATE)

    # A weekday on the publication day itself belongs to that same week.
    occurrence = occurrence_from_row(_weekly_row("Sunday"), bulletin_date=published)
    assert occurrence == (("st-mary-anytown", "adoration", 1140), published)


def test_weekly_row_without_a_bulletin_date_is_not_recorded() -> None:
    assert occurrence_from_row(_weekly_row("Wednesday"), bulletin_date=None) is None


def test_occurrence_skips_cancelled_and_unparseable_rows() -> None:
    assert occurrence_from_row(_dated_row(BASE_DATE, cancelled=True), bulletin_date=None) is None
    assert occurrence_from_row(
        _weekly_row("Wednesday", cancelled=True), bulletin_date=BASE_DATE
    ) is None
    assert occurrence_from_row(
        _dated_row(BASE_DATE, start_time="whenever"), bulletin_date=None
    ) is None
    assert occurrence_from_row(
        _dated_row(BASE_DATE, date="sometime soon"), bulletin_date=None
    ) is None
    assert occurrence_from_row(_weekly_row("Caturday"), bulletin_date=BASE_DATE) is None


def test_record_observations_dedupes_repeated_sightings() -> None:
    history: History = {}
    rows = [_dated_row(BASE_DATE), _dated_row(BASE_DATE)]
    assert record_observations(history, rows, bulletin_date=None) == 1
    assert record_observations(history, rows, bulletin_date=None) == 0
    assert history == {("st-mary-anytown", "adoration", 1140): {BASE_DATE}}


def test_bulletin_reference_date_prefers_published_over_fetched() -> None:
    assert bulletin_reference_date(
        {"published_date": "2026-08-16", "fetched_at": "2026-08-19T04:00:00Z"}
    ) == date(2026, 8, 16)
    assert bulletin_reference_date({"published_date": None, "fetched_at": None}) is None


def test_bulletin_reference_date_snaps_the_fetch_fallback_to_its_sunday() -> None:
    # An issue date is nearly always a Sunday, and the fetch lands anywhere
    # from the Saturday before to the Wednesday after. Without snapping, the
    # same parish's Sunday slot would be credited to two different weeks
    # depending on whether the extractor happened to read the issue date.
    sunday = date(2026, 8, 16)
    for fetched in ("2026-08-15", "2026-08-16", "2026-08-17", "2026-08-19"):
        assert bulletin_reference_date(
            {"published_date": None, "fetched_at": f"{fetched}T04:00:00Z"}
        ) == sunday, fetched


def test_bulletin_reference_date_survives_an_unparseable_fetch() -> None:
    assert bulletin_reference_date(
        {"published_date": None, "fetched_at": "not-a-date"}
    ) is None


# ── Promotion ───────────────────────────────────────────────────────────────
def test_promotes_after_two_prior_weeks() -> None:
    history = _history_for([1, 2])
    rows = [_dated_row(BASE_DATE)]
    promoted_rows, promoted = promote_recurring_events(rows, history)

    assert promoted == 1
    assert promoted_rows[0]["event_kind"] == "weekly"
    assert promoted_rows[0]["day_of_week"] == "Wednesday"
    assert promoted_rows[0]["date"] is None
    # Everything else about the row is preserved.
    assert promoted_rows[0]["start_time"] == "7:00 PM"
    assert promoted_rows[0]["page_number"] == 1


def test_promotes_when_the_prior_weeks_were_extracted_as_weekly() -> None:
    # The bulletin listed this slot in its weekly schedule for the past two
    # weeks and filed it as a one-off this week. The earlier weekly sightings
    # are the strongest possible evidence that this week's date is the error.
    history = _weekly_history_for([1, 2])
    _, promoted = promote_recurring_events([_dated_row(BASE_DATE)], history)
    assert promoted == 1


def test_promotes_across_a_mix_of_weekly_and_dated_prior_weeks() -> None:
    history = _weekly_history_for([2])
    record_observations(
        history, [_dated_row(BASE_DATE - timedelta(weeks=1))], bulletin_date=None,
    )
    _, promoted = promote_recurring_events([_dated_row(BASE_DATE)], history)
    assert promoted == 1


def test_a_weekly_sighting_on_a_different_weekday_does_not_count() -> None:
    history = _weekly_history_for([1, 2], day_of_week="Thursday")
    _, promoted = promote_recurring_events([_dated_row(BASE_DATE)], history)
    assert promoted == 0


def test_does_not_promote_with_only_one_prior_week() -> None:
    history = _history_for([1])
    rows = [_dated_row(BASE_DATE)]
    promoted_rows, promoted = promote_recurring_events(rows, history)

    assert promoted == 0
    assert promoted_rows == rows


def test_does_not_promote_a_fortnightly_slot() -> None:
    # Seen 2, 4 and 6 weeks back but never in the week just gone: a slot the
    # parish runs every other week, not a weekly one.
    history = _history_for([2, 4, 6])
    _, promoted = promote_recurring_events([_dated_row(BASE_DATE)], history)
    assert promoted == 0


def test_a_gap_breaks_the_chain() -> None:
    history = _history_for([1, 3, 4])  # week 2 missing
    _, promoted = promote_recurring_events([_dated_row(BASE_DATE)], history)
    assert promoted == 0


def test_a_longer_unbroken_chain_still_promotes() -> None:
    history = _history_for(list(range(1, LOOKBACK_WEEKS + 1)))
    _, promoted = promote_recurring_events([_dated_row(BASE_DATE)], history)
    assert promoted == 1


def test_does_not_promote_a_different_weekday_or_time() -> None:
    history = _history_for([1, 2])

    # Same slot, but this occurrence is a Thursday rather than a Wednesday.
    thursday = BASE_DATE + timedelta(days=1)
    _, promoted = promote_recurring_events([_dated_row(thursday)], history)
    assert promoted == 0

    _, promoted = promote_recurring_events(
        [_dated_row(BASE_DATE, start_time="6:00 PM")], history
    )
    assert promoted == 0


def test_does_not_promote_across_churches_or_event_types() -> None:
    history = _history_for([1, 2])
    _, promoted = promote_recurring_events(
        [_dated_row(BASE_DATE, church_slug="st-joseph-anytown")], history
    )
    assert promoted == 0
    _, promoted = promote_recurring_events(
        [_dated_row(BASE_DATE, event_type="mass")], history
    )
    assert promoted == 0


def test_cancelled_dated_events_are_left_alone() -> None:
    history = _history_for([1, 2])
    rows = [_dated_row(BASE_DATE, cancelled=True)]
    promoted_rows, promoted = promote_recurring_events(rows, history)
    assert promoted == 0
    assert promoted_rows[0]["event_kind"] == "specific_date"


def test_promotion_drops_a_duplicate_of_an_existing_weekly_slot() -> None:
    history = _history_for([1, 2])
    rows = [_weekly_row("Wednesday"), _dated_row(BASE_DATE)]
    promoted_rows, promoted = promote_recurring_events(rows, history)

    assert promoted == 1
    assert promoted_rows == [_weekly_row("Wednesday")]


def test_promotion_is_idempotent() -> None:
    history = _history_for([1, 2])
    once, _ = promote_recurring_events([_dated_row(BASE_DATE)], history)
    twice, promoted = promote_recurring_events(once, history)
    assert promoted == 0
    assert twice == once


def test_weekly_rows_and_other_dated_rows_pass_through_untouched() -> None:
    history = _history_for([1, 2])
    weekly = _weekly_row("Sunday", event_type="mass")
    one_off = _dated_row(BASE_DATE, event_type="mass", start_time="10:00 AM")
    promoted_rows, promoted = promote_recurring_events([weekly, one_off], history)

    assert promoted == 0
    assert promoted_rows == [weekly, one_off]


def test_a_bulletin_cannot_promote_a_slot_on_its_own_listings() -> None:
    # One bulletin printing a six-week series on three consecutive dates
    # describes a finite run, not a standing weekly slot.
    history: History = {}
    rows = [
        _dated_row(BASE_DATE - timedelta(weeks=w), event_type="fish_fry")
        for w in (2, 1, 0)
    ]
    record_observations(history, rows, bulletin_date=None)
    promoted_rows, promoted = promote_recurring_events(rows, history)

    assert promoted == 0
    assert promoted_rows == rows


def test_earlier_bulletins_still_promote_a_slot_this_bulletin_also_lists() -> None:
    # The exclusion is limited to the weeks this bulletin printed itself: a
    # chain from earlier bulletins must still count.
    history = _history_for([1, 2])
    rows = [_dated_row(BASE_DATE), _dated_row(BASE_DATE + timedelta(weeks=1))]
    _, promoted = promote_recurring_events(rows, history)
    assert promoted == 1


def test_promotion_drops_a_duplicate_of_a_cancelled_weekly_slot() -> None:
    # The slot is spoken for either way; a live weekly row beside the
    # cancellation would have the parish contradicting itself.
    history = _history_for([1, 2])
    cancelled = _weekly_row("Wednesday", cancelled=True)
    promoted_rows, promoted = promote_recurring_events(
        [cancelled, _dated_row(BASE_DATE)], history,
    )
    assert promoted == 1
    assert promoted_rows == [cancelled]


# ── History maintenance ─────────────────────────────────────────────────────
def test_prune_history_drops_expired_occurrences() -> None:
    history = _history_for([0, 1, HISTORY_RETENTION_WEEKS + 1])
    removed = prune_history(history, today=BASE_DATE)

    assert removed == 1
    assert history == {
        ("st-mary-anytown", "adoration", 1140): {
            BASE_DATE, BASE_DATE - timedelta(weeks=1),
        }
    }


def test_prune_history_drops_slots_left_with_no_dates() -> None:
    history = _history_for([0])  # a current slot, so the cutoff sits at today
    record_observations(
        history,
        [
            _dated_row(BASE_DATE - timedelta(weeks=w), event_type="mass")
            for w in (HISTORY_RETENTION_WEEKS + 1, HISTORY_RETENTION_WEEKS + 2)
        ],
        bulletin_date=None,
    )
    assert prune_history(history, today=BASE_DATE) == 2
    assert list(history) == [("st-mary-anytown", "adoration", 1140)]


def test_prune_history_keeps_recent_rows_when_the_corpus_is_old() -> None:
    # Replaying a corpus long after the fact must not wipe it: the cutoff falls
    # back to the newest occurrence when that is older than today.
    history = _history_for([0, 1])
    assert prune_history(history, today=BASE_DATE + timedelta(weeks=52)) == 0
    assert len(history[("st-mary-anytown", "adoration", 1140)]) == 2


def test_prune_history_is_not_dragged_forward_by_future_dated_events() -> None:
    # Bulletins announce events months out. Anchoring the cutoff on those would
    # prune away the recent weeks every chain depends on.
    history = _history_for([0, 1])
    record_observations(
        history,
        [_dated_row(BASE_DATE + timedelta(weeks=HISTORY_RETENTION_WEEKS + 4))],
        bulletin_date=None,
    )
    assert prune_history(history, today=BASE_DATE) == 0
    assert len(history[("st-mary-anytown", "adoration", 1140)]) == 3


def test_history_round_trips_through_disk(tmp_path: Path) -> None:
    path = tmp_path / "event_history.json"
    history = _history_for([1, 2])
    history[("st-mary-anytown", "mass", 540)] = {BASE_DATE}
    save_history(history, path)
    assert load_history(path) == history


def test_history_is_grouped_by_slot_on_disk(tmp_path: Path) -> None:
    path = tmp_path / "event_history.json"
    save_history(_history_for([1, 2]), path)
    records = json.loads(path.read_text(encoding="utf-8"))
    assert records == [
        {
            "church_slug": "st-mary-anytown",
            "event_type": "adoration",
            "start_time": 1140,
            "dates": ["2026-08-05", "2026-08-12"],
        }
    ]


# ── apply_recurrence over events.json ───────────────────────────────────────
def test_apply_recurrence_rewrites_the_events_file(tmp_path: Path) -> None:
    events_path = tmp_path / "events.json"
    history_path = tmp_path / "event_history.json"
    save_json_list(events_path, [_dated_row(BASE_DATE)])
    save_history(_history_for([1, 2]), history_path)

    result = apply_recurrence(
        events_path=events_path,
        history_path=history_path,
        metadata_path=tmp_path / "metadata.json",
        today=BASE_DATE,
    )

    assert result == {"events": 1, "promoted": 1, "recorded": 1}
    written = json.loads(events_path.read_text(encoding="utf-8"))
    assert written[0]["event_kind"] == "weekly"
    assert written[0]["day_of_week"] == "Wednesday"


def test_apply_recurrence_dedupes_only_within_a_bulletin(tmp_path: Path) -> None:
    events_path = tmp_path / "events.json"
    history_path = tmp_path / "event_history.json"
    # The same slug/time in two parishes' bulletins must not collapse together.
    other_bulletin = {"bulletin_source_url": "https://example.org/other.pdf"}
    save_json_list(
        events_path,
        [_dated_row(BASE_DATE), _dated_row(BASE_DATE, **other_bulletin)],
    )
    save_history(_history_for([1, 2]), history_path)

    result = apply_recurrence(
        events_path=events_path,
        history_path=history_path,
        metadata_path=tmp_path / "metadata.json",
        today=BASE_DATE,
    )

    assert result == {"events": 2, "promoted": 2, "recorded": 1}


def test_apply_recurrence_leaves_the_file_alone_when_nothing_promotes(
    tmp_path: Path,
) -> None:
    events_path = tmp_path / "events.json"
    history_path = tmp_path / "event_history.json"
    save_json_list(events_path, [_dated_row(BASE_DATE)])
    save_history(_history_for([1]), history_path)
    before = events_path.read_text(encoding="utf-8")

    result = apply_recurrence(
        events_path=events_path,
        history_path=history_path,
        metadata_path=tmp_path / "metadata.json",
        today=BASE_DATE,
    )

    assert result == {"events": 1, "promoted": 0, "recorded": 1}
    assert events_path.read_text(encoding="utf-8") == before


def test_apply_recurrence_records_sightings_before_it_clears_their_dates(
    tmp_path: Path,
) -> None:
    """Promotion clears a row's `date`, so the sighting has to be filed first.

    events.json is the only place an unrecorded sighting exists; promoting
    without recording destroys it, leaving a hole in the chain that breaks the
    slot back to a dated event the following week.
    """
    events_path = tmp_path / "events.json"
    history_path = tmp_path / "event_history.json"
    metadata_path = tmp_path / "metadata.json"
    save_json_list(events_path, [_dated_row(BASE_DATE)])
    save_history(_history_for([1, 2]), history_path)

    apply_recurrence(
        events_path=events_path,
        history_path=history_path,
        metadata_path=metadata_path,
        today=BASE_DATE,
    )

    slot = ("st-mary-anytown", "adoration", 1140)
    assert BASE_DATE in load_history(history_path)[slot]

    # With its own week on file, next week's bulletin still sees an unbroken chain.
    save_json_list(events_path, [_dated_row(BASE_DATE + timedelta(weeks=1))])
    result = apply_recurrence(
        events_path=events_path,
        history_path=history_path,
        metadata_path=metadata_path,
        today=BASE_DATE,
    )
    assert result["promoted"] == 1


def test_prune_history_tolerates_slots_holding_no_dates() -> None:
    history: History = {("st-mary-anytown", "adoration", 1140): set()}
    assert prune_history(history, today=BASE_DATE) == 0
    assert history == {}


def test_thresholds_are_the_documented_defaults() -> None:
    assert MIN_PRIOR_WEEKS == 2
    assert LOOKBACK_WEEKS >= MIN_PRIOR_WEEKS
