"""Scoring classifier runs against human ground truth."""

from __future__ import annotations

from labelapp import events as ev
from labelapp import store
from labelapp.corpus import Run
from labelapp.score import attribute_errors, score_run

URL = "https://example.org/bulletin.pdf"


def _ev(**overrides):
    base = {
        "church_slug": "st-mary",
        "bulletin_source_url": URL,
        "event_type": "mass",
        "event_kind": "weekly",
        "day_of_week": "Sunday",
        "date": None,
        "start_time": "9:00 AM",
        "end_time": None,
        "cancelled": False,
        "page_number": 1,
        "note": None,
    }
    base.update(overrides)
    return base


def _key(event):
    from pdf_extract.compare import event_key

    return event_key(event)


def _run(rows: list[dict], *, name: str = "a") -> Run:
    return Run(name=name, covered={URL}, events_by_bulletin={URL: rows})


def _label(accepted: list[dict], rejected: list[dict] | None = None, *, status=store.STATUS_COMPLETE):
    return {
        URL: store.normalize_label(
            {
                "bulletin_source_url": URL,
                "parish_slug": "st-mary-parish",
                "status": status,
                "events": accepted,
                "rejected": rejected or [],
            }
        )
    }


def test_perfect_run_scores_one():
    rows = [_ev(start_time="9:00 AM"), _ev(start_time="11:00 AM")]
    result = score_run(_run(rows), _label([dict(row) for row in rows]))

    assert (result["precision"], result["recall"], result["f1"]) == (1.0, 1.0, 1.0)
    assert result["false_positives"] == 0
    assert result["false_negatives"] == 0


def test_extra_and_missing_events_are_counted():
    predicted = [_ev(start_time="9:00 AM"), _ev(start_time="7:00 AM")]
    truth = [_ev(start_time="9:00 AM"), _ev(start_time="5:00 PM")]
    result = score_run(_run(predicted), _label(truth))

    assert result["true_positives"] == 1
    assert result["false_positives"] == 1
    assert result["false_negatives"] == 1
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5


def test_recall_only_counts_bulletins_marked_complete():
    """A partly labeled bulletin cannot say what a model missed, because nobody
    has yet asserted the accepted set is exhaustive."""
    rows = [_ev()]
    result = score_run(
        _run(rows), _label([dict(rows[0])], status=store.STATUS_IN_PROGRESS)
    )

    assert result["scored_bulletins"] == 0
    assert result["recall"] is None
    assert result["partial_bulletins"] == 1


def test_partial_labels_still_contribute_precision():
    predicted = [_ev(start_time="9:00 AM"), _ev(start_time="7:00 AM")]
    labels = _label(
        [_ev(start_time="9:00 AM")],
        [_ev(start_time="7:00 AM")],
        status=store.STATUS_IN_PROGRESS,
    )
    decided = score_run(_run(predicted), labels)["decided_only"]

    assert decided["candidates_ruled_on"] == 2
    assert decided["accepted"] == 1
    assert decided["precision"] == 0.5


def test_bulletins_the_run_never_saw_are_skipped():
    other = Run(name="a", covered=set(), events_by_bulletin={})
    result = score_run(other, _label([_ev()]))

    assert result["scored_bulletins"] == 0
    assert result["precision"] is None


def test_near_misses_are_attributed_to_the_field_they_turn_on():
    """Reading a real slot slightly wrong is a different failure from inventing
    an event, and the two call for different fixes."""
    predicted = [_ev(end_time="9:45 AM")]
    truth = [_ev(end_time=None)]
    attribution = score_run(_run(predicted), _label(truth))["error_attribution"]

    assert attribution["near_miss_by_field"] == {ev.FIELD_END: 1}
    assert attribution["spurious"] == []
    assert attribution["missed"] == []


def test_an_invented_event_is_not_dressed_up_as_a_near_miss():
    predicted = [_ev(church_slug="st-jude", event_type="adoration", start_time="6:00 AM")]
    truth = [_ev()]
    attribution = score_run(_run(predicted), _label(truth))["error_attribution"]

    assert attribution["near_miss_by_field"] == {}
    assert len(attribution["spurious"]) == 1
    assert len(attribution["missed"]) == 1


def test_reading_a_slot_as_dated_instead_of_weekly_is_not_an_error():
    """Nobody labels that axis — `pdf_extract.recurrence` settles it from history
    across bulletins — so scoring a run on it would be scoring a coin toss."""
    predicted = [_ev(event_kind="specific_date", day_of_week=None, date="2026-03-08")]
    result = score_run(_run(predicted), _label([_ev()]))

    assert (result["precision"], result["recall"]) == (1.0, 1.0)
    assert result["false_positives"] == 0
    assert result["false_negatives"] == 0
    assert result["when_variants_excused"] == 1
    assert result["error_attribution"]["near_miss_by_field"] == {}


def test_a_date_on_the_wrong_weekday_is_still_an_error():
    """Only weekly-vs-dated is unanswerable. 2026-03-10 is a Tuesday, so this is
    a date read wrong, and it stays on the books as one."""
    predicted = [_ev(event_kind="specific_date", day_of_week=None, date="2026-03-10")]
    result = score_run(_run(predicted), _label([_ev()]))

    assert result["false_positives"] == 1
    assert result["false_negatives"] == 1
    assert result["when_variants_excused"] == 0
    assert result["error_attribution"]["near_miss_by_field"] == {ev.FIELD_WHEN: 1}


def test_a_dated_prediction_of_a_rejected_slot_still_counts_as_ruled_on():
    """A slot the labeler threw out is a false positive however it was filed."""
    predicted = [_ev(event_kind="specific_date", day_of_week=None, date="2026-03-08")]
    labels = _label([], [_ev()], status=store.STATUS_IN_PROGRESS)
    decided = score_run(_run(predicted), labels)["decided_only"]

    assert decided["candidates_ruled_on"] == 1
    assert decided["accepted"] == 0


def test_near_misses_sort_without_tripping_over_null_columns():
    """Event keys carry None in the nullable columns, so the per-bulletin report
    must not order them by raw tuple comparison."""
    predicted = [_ev(start_time="7:00 AM"), _ev(start_time="7:00 AM", end_time="7:45 AM")]
    truth = [_ev(start_time="5:00 PM")]
    result = score_run(_run(predicted), _label(truth))

    assert result["per_bulletin"][0]["false_positives"] == 2


def test_each_false_positive_is_paired_at_most_once():
    """Two predictions one field from the same truth row cannot both be excused
    as the same near miss."""
    attribution = attribute_errors(
        false_positives=[
            _key(_ev(start_time="9:15 AM")),
            _key(_ev(start_time="9:30 AM")),
        ],
        false_negatives=[_key(_ev())],
    )
    assert sum(attribution["near_miss_by_field"].values()) == 1
    assert len(attribution["spurious"]) == 1


