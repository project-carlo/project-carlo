"""Grouping model output into the decisions a labeler is asked to make."""

from __future__ import annotations

from labelapp import events as ev
from labelapp.candidates import build_candidates, build_review, group_candidates
from labelapp.corpus import Bulletin, Run

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
        "page_number": 2,
        "note": None,
    }
    base.update(overrides)
    return base


def _run(name: str, rows: list[dict]) -> Run:
    return Run(name=name, covered={URL}, events_by_bulletin={URL: rows})


def _group(runs: dict[str, Run]):
    order = list(runs)
    candidates, covering = build_candidates(URL, runs, order)
    return group_candidates(candidates), covering


def test_events_every_run_proposed_are_agreed():
    row = _ev()
    groups, covering = _group({"a": _run("a", [row]), "b": _run("b", [dict(row)])})

    assert covering == ["a", "b"]
    assert [c.sources for c in groups["agreed"]] == [["a", "b"]]
    assert groups["conflicts"] == []
    assert groups["singletons"] == []


def test_agreement_ignores_page_number_and_note():
    groups, _ = _group(
        {
            "a": _run("a", [_ev(page_number=1, note="Latin")]),
            "b": _run("b", [_ev(page_number=9, note=None)]),
        }
    )
    assert len(groups["agreed"]) == 1
    assert groups["agreed"][0].notes == [{"run": "a", "note": "Latin"}]


def test_weekly_versus_dated_is_one_conflict_on_the_when_field():
    """The extractor filing a standing slot under a date moves three columns at
    once; the labeler should still see a single question."""
    groups, _ = _group(
        {
            "a": _run("a", [_ev()]),
            "b": _run(
                "b",
                [_ev(event_kind="specific_date", day_of_week=None, date="2026-03-08")],
            ),
        }
    )
    assert len(groups["conflicts"]) == 1
    conflict = groups["conflicts"][0]
    assert conflict.fields == [ev.FIELD_WHEN]
    assert len(conflict.variants) == 2


def test_end_time_disagreement_is_a_conflict():
    groups, _ = _group(
        {
            "a": _run("a", [_ev(event_type="confession", end_time=None)]),
            "b": _run("b", [_ev(event_type="confession", end_time="9:45 AM")]),
        }
    )
    assert [c.fields for c in groups["conflicts"]] == [[ev.FIELD_END]]


def test_events_from_one_run_are_never_variants_of_each_other():
    """Two slots the same run listed separately are two events, not two readings
    of one. Without this, a whole daily schedule collapses into one card."""
    a_rows = [_ev(day_of_week="Tuesday"), _ev(day_of_week="Thursday")]
    groups, _ = _group({"a": _run("a", a_rows), "b": _run("b", [dict(a_rows[0])])})

    # Tuesday is agreed; Thursday is a's alone and must not be paired against it.
    assert [c.event["day_of_week"] for c in groups["agreed"]] == ["Tuesday"]
    assert groups["conflicts"] == []
    assert [c.event["day_of_week"] for c in groups["singletons"]] == ["Thursday"]


def test_different_weekdays_are_not_treated_as_one_slot():
    """Only a weekly slot and a date falling on that same weekday are two
    readings of one thing. Different weekdays are different Masses, and there is
    no right answer to pick between them."""
    groups, _ = _group(
        {
            "a": _run("a", [_ev(day_of_week="Tuesday")]),
            "b": _run("b", [_ev(day_of_week="Thursday")]),
        }
    )
    assert groups["conflicts"] == []
    assert len(groups["singletons"]) == 2


def test_a_date_on_a_different_weekday_is_not_a_variant():
    groups, _ = _group(
        {
            "a": _run("a", [_ev(day_of_week="Sunday")]),
            # 2026-03-10 is a Tuesday, so this is not the Sunday slot re-filed.
            "b": _run(
                "b",
                [_ev(event_kind="specific_date", day_of_week=None, date="2026-03-10")],
            ),
        }
    )
    assert groups["conflicts"] == []
    assert len(groups["singletons"]) == 2


def test_conflicts_stay_pairwise_instead_of_chaining():
    """Three one-field-apart candidates from two runs must not merge into one
    oversized decision when they are not all mutually compatible."""
    groups, _ = _group(
        {
            "a": _run("a", [_ev(start_time="9:00 AM"), _ev(start_time="11:00 AM")]),
            "b": _run("b", [_ev(start_time="10:00 AM")]),
        }
    )
    assert all(len(conflict.variants) == 2 for conflict in groups["conflicts"])


def test_a_lone_dated_duplicate_carries_the_agreed_weekly_slot_as_context():
    """The extractor's signature error: one model re-files a standing Sunday Mass
    under a single date. Nothing disputes the dated row, so it lands as a
    singleton — and it is only obviously wrong next to the weekly slot it
    duplicates, so that slot rides along on the card."""
    agreed = _ev(day_of_week="Sunday", start_time="8:00 AM")
    dated = _ev(
        event_kind="specific_date",
        day_of_week=None,
        date="2026-03-08",  # a Sunday
        start_time="8:00 AM",
    )
    groups, _ = _group({"a": _run("a", [agreed]), "b": _run("b", [dict(agreed), dated])})

    assert groups["conflicts"] == []
    singleton = groups["singletons"][0]
    assert singleton.event["date"] == "2026-03-08"
    assert [c.event["day_of_week"] for c in singleton.context] == ["Sunday"]


def test_conflict_context_is_limited_to_the_disputed_field():
    """An agreed event that differs on some other axis is a neighbour, not
    evidence, and would only add noise to the card."""
    groups, _ = _group(
        {
            "a": _run(
                "a",
                [
                    _ev(start_time="8:00 AM", end_time="8:30 AM"),
                    _ev(start_time="11:00 AM"),
                ],
            ),
            "b": _run(
                "b",
                [
                    _ev(start_time="8:00 AM", end_time="8:30 AM"),
                    _ev(start_time="11:00 AM", end_time="11:45 AM"),
                ],
            ),
        }
    )
    conflict = groups["conflicts"][0]
    assert conflict.fields == [ev.FIELD_END]
    # The agreed 8:00 Mass differs from the disputed 11:00 one by start time,
    # not by the end time under discussion.
    assert conflict.context == []


def test_agreement_is_measured_only_against_runs_that_saw_the_bulletin():
    """A run that has not reached a bulletin yet neither agrees nor dissents."""
    behind = Run(name="b", covered=set(), events_by_bulletin={})
    groups, covering = _group({"a": _run("a", [_ev()]), "b": behind})

    assert covering == ["a"]
    assert len(groups["agreed"]) == 1
    assert groups["singletons"] == []


def test_a_run_serving_zero_events_still_counts_as_dissent():
    """`bulletins.json` records bulletins served with no events; that is a real
    prediction, not a gap, so everything the other run found is disputed."""
    empty = Run(name="b", covered={URL}, events_by_bulletin={URL: []})
    groups, covering = _group({"a": _run("a", [_ev()]), "b": empty})

    assert covering == ["a", "b"]
    assert groups["agreed"] == []
    assert [c.sources for c in groups["singletons"]] == [["a"]]


def test_review_reports_counts_and_wrong_bulletin_flags():
    flagged = Run(
        name="b",
        covered={URL},
        events_by_bulletin={URL: [_ev()]},
        wrong_bulletin={URL},
    )
    bulletin = Bulletin(
        source_url=URL,
        parish_slug="st-mary-parish",
        content_hash="abc",
        pdf_path=None,
        published_date="2026-03-08",
        fetched_at="2026-03-09T00:00:00Z",
    )
    review = build_review(bulletin, {"a": _run("a", [_ev()]), "b": flagged}, ["a", "b"])

    assert review["candidate_count"] == 1
    assert review["agreed_count"] == 1
    assert review["disputed_count"] == 0
    assert review["wrong_bulletin_runs"] == ["b"]
    assert review["has_pdf"] is False
