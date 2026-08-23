"""Tests for promoting repeatedly-dated events to weekly ones."""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.recurrence import (
    HISTORY_RETENTION_WEEKS,
    LOOKBACK_WEEKS,
    MIN_PRIOR_WEEKS,
    apply_recurrence,
    load_history,
    observation_from_row,
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


def _history_for(weeks_back: list[int], **row_kwargs: Any) -> list[dict[str, Any]]:
    history: list[dict[str, Any]] = []
    rows = [_dated_row(BASE_DATE - timedelta(weeks=w), **row_kwargs) for w in weeks_back]
    record_observations(history, rows)
    return history


# ── Observations ────────────────────────────────────────────────────────────
def test_observation_normalises_date_and_time() -> None:
    record = observation_from_row(_dated_row(BASE_DATE, start_time="7:00 p.m."))
    assert record == {
        "church_slug": "st-mary-anytown",
        "event_type": "adoration",
        "date": "2026-08-19",
        "start_time": 1140,
    }


def test_observation_skips_weekly_cancelled_and_unparseable_rows() -> None:
    assert observation_from_row(_weekly_row("Wednesday")) is None
    assert observation_from_row(_dated_row(BASE_DATE, cancelled=True)) is None
    assert observation_from_row(_dated_row(BASE_DATE, start_time="whenever")) is None
    assert observation_from_row(_dated_row(BASE_DATE, date="sometime soon")) is None


def test_record_observations_dedupes_repeated_sightings() -> None:
    history: list[dict[str, Any]] = []
    rows = [_dated_row(BASE_DATE), _dated_row(BASE_DATE), _weekly_row("Sunday")]
    assert record_observations(history, rows) == 1
    assert record_observations(history, rows) == 0
    assert len(history) == 1


def test_record_observations_keeps_history_sorted_by_date() -> None:
    history: list[dict[str, Any]] = []
    record_observations(history, [_dated_row(BASE_DATE)])
    record_observations(history, [_dated_row(BASE_DATE - timedelta(weeks=1))])
    assert [r["date"] for r in history] == ["2026-08-12", "2026-08-19"]


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


# ── History maintenance ─────────────────────────────────────────────────────
def test_prune_history_drops_expired_occurrences() -> None:
    history = _history_for([0, 1, HISTORY_RETENTION_WEEKS + 1])
    removed = prune_history(history, today=BASE_DATE)

    assert removed == 1
    assert [r["date"] for r in history] == ["2026-08-12", "2026-08-19"]


def test_prune_history_keeps_recent_rows_when_the_corpus_is_old() -> None:
    # Anchored on the newest occurrence, so replaying an old corpus long after
    # the fact does not wipe it.
    history = _history_for([0, 1])
    assert prune_history(history) == 0
    assert len(history) == 2


def test_prune_history_can_be_anchored_on_today_instead() -> None:
    history = _history_for([0, 1])
    removed = prune_history(history, today=BASE_DATE + timedelta(weeks=52))
    assert removed == 2
    assert history == []


def test_history_round_trips_through_disk(tmp_path: Path) -> None:
    path = tmp_path / "event_history.json"
    history = _history_for([1, 2])
    save_history(history, path)
    assert load_history(path) == history


# ── apply_recurrence over events.json ───────────────────────────────────────
def test_apply_recurrence_rewrites_the_events_file(tmp_path: Path) -> None:
    events_path = tmp_path / "events.json"
    history_path = tmp_path / "event_history.json"
    save_json_list(events_path, [_dated_row(BASE_DATE)])
    save_history(_history_for([1, 2]), history_path)

    result = apply_recurrence(events_path=events_path, history_path=history_path)

    assert result == {"events": 1, "promoted": 1}
    written = load_history(events_path)
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

    result = apply_recurrence(events_path=events_path, history_path=history_path)

    assert result == {"events": 2, "promoted": 2}


def test_apply_recurrence_leaves_the_file_alone_when_nothing_promotes(
    tmp_path: Path,
) -> None:
    events_path = tmp_path / "events.json"
    history_path = tmp_path / "event_history.json"
    save_json_list(events_path, [_dated_row(BASE_DATE)])
    save_history(_history_for([1]), history_path)
    before = events_path.read_text(encoding="utf-8")

    result = apply_recurrence(events_path=events_path, history_path=history_path)

    assert result == {"events": 1, "promoted": 0}
    assert events_path.read_text(encoding="utf-8") == before


def test_thresholds_are_the_documented_defaults() -> None:
    assert MIN_PRIOR_WEEKS == 2
    assert LOOKBACK_WEEKS >= MIN_PRIOR_WEEKS
