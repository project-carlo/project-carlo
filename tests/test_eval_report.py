"""`eval report`: tiered matching of predictions against labels, and the written report."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import runner
from pdf_extract.classifiers import get_classifier
from pdf_extract.evals.report import (
    build_report,
    field_accuracy,
    match_events,
    render_markdown,
    score_optional,
    score_records,
    write_report,
)
from pdf_extract.evals.run import version_dir_name
from pdf_extract.labeling.labels import empty_label

HASH_A, HASH_B, HASH_C = "a" * 64, "b" * 64, "c" * 64


def _ev(**overrides: Any) -> dict[str, Any]:
    event = {
        "church_slug": "st-mary", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "10:00", "end_time": None,
        "cancelled": False, "weeks_of_month": [], "season": None, "page_number": 1,
        "note": None, "origin": "human", "optional": None,
    }
    return event | overrides


def _dated(**overrides: Any) -> dict[str, Any]:
    # 2026-10-04 is a Sunday.
    return _ev(event_kind="specific_date", day_of_week=None, date="2026-10-04") | overrides


def _tiers(labels, preds) -> list[tuple[str, int | None, int | None]]:
    """(tier, label index, pred index) for each record."""
    out = []
    for r in match_events(labels, preds):
        li = next((i for i, e in enumerate(labels) if e is r["label"]), None)
        pi = next((i for i, e in enumerate(preds) if e is r["pred"]), None)
        out.append((r["tier"], li, pi))
    return sorted(out, key=lambda t: (t[1] is None, t[1], t[2]))


def test_exact_and_core_tiers():
    labels = [_ev(), _ev(start_time="08:00", end_time="09:00")]
    preds = [_ev(note="Spanish", page_number=3), _ev(start_time="08:00", weeks_of_month=["first"])]
    assert _tiers(labels, preds) == [("exact", 0, 0), ("core", 1, 1)]


def test_wrong_time_pairs_closest_start_first():
    labels = [_ev(start_time="08:00"), _ev(start_time="11:00")]
    preds = [_ev(start_time="11:30"), _ev(start_time="08:15")]
    assert _tiers(labels, preds) == [("wrong_time", 0, 1), ("wrong_time", 1, 0)]


def test_weekly_vs_dated_needs_same_weekday_and_start():
    labels = [_ev(), _ev(day_of_week="Saturday", start_time="16:00")]
    preds = [_dated(), _dated(date="2026-10-03", start_time="17:00")]  # a Saturday, other time
    assert _tiers(labels, preds) == [
        ("weekly_vs_dated", 0, 0), ("missed", 1, None), ("spurious", None, 1),
    ]


def test_wrong_church_and_type_are_found_before_wrong_time_and_never_count():
    labels = [_ev(), _ev(event_type="confession", day_of_week="Saturday", start_time="15:00")]
    preds = [
        _ev(start_time="12:00"),                       # same church, other time
        _ev(church_slug="st-joseph"),                  # same time, other church
        _ev(event_type="adoration", day_of_week="Saturday", start_time="15:00"),
    ]
    assert _tiers(labels, preds) == [
        ("wrong_church", 0, 1), ("wrong_type", 1, 2), ("spurious", None, 0),
    ]
    score = score_records(match_events(labels, preds))
    assert score["levels"]["any_time"]["found"] == 0
    assert score["rates"]["wrong_church"] == 0.5 and score["rates"]["wrong_type"] == 0.5


def test_cancelled_must_agree():
    assert _tiers([_dated(cancelled=True)], [_dated()]) == [
        ("missed", 0, None), ("spurious", None, 0),
    ]


def test_levels_precision_recall_f1():
    labels = [_ev(), _ev(start_time="08:00", end_time="09:00"), _ev(start_time="12:00"),
              _ev(day_of_week="Monday")]
    preds = [_ev(), _ev(start_time="08:00"), _ev(start_time="12:30")]
    score = score_records(match_events(labels, preds))
    assert score["outcomes"]["exact"] == 1 and score["outcomes"]["core"] == 1
    assert score["outcomes"]["wrong_time"] == 1 and score["outcomes"]["missed"] == 1
    assert score["levels"]["strict"] == {
        "found": 1, "found_predicted": 1, "precision": 1 / 3, "recall": 1 / 4, "f1": 2 / 7,
    }
    assert score["levels"]["loose"]["f1"] == 4 / 7
    assert score["levels"]["any_time"]["f1"] == 6 / 7
    assert score_records([])["levels"]["strict"]["f1"] == 1.0


def test_one_weekly_prediction_covers_every_dated_label_of_its_slot():
    # 2026-10-04, 10-11 and 10-18 are Sundays; 10-10 is a Saturday.
    labels = [
        _dated(), _dated(date="2026-10-11"), _dated(date="2026-10-18"),
        _dated(date="2026-10-10"),                               # other weekday
        _dated(date="2026-10-11", start_time="12:00"),           # other time
    ]
    preds = [_ev()]
    assert _tiers(labels, preds) == [
        ("weekly_vs_dated", 0, 0), ("weekly_vs_dated", 1, 0), ("weekly_vs_dated", 2, 0),
        ("missed", 3, None), ("missed", 4, None),
    ]
    score = score_records(match_events(labels, preds))
    loose = score["levels"]["loose"]
    assert score["label_events"] == 5 and score["predicted_events"] == 1
    assert loose["found"] == 3 and loose["found_predicted"] == 1
    assert loose["recall"] == 3 / 5 and loose["precision"] == 1.0
    assert loose["f1"] == 4 / 6
    assert score["levels"]["core"]["found"] == 0 and score["spurious"] == 0


def test_weekly_label_still_pairs_with_one_dated_prediction():
    labels = [_ev()]
    preds = [_dated(), _dated(date="2026-10-11")]
    assert _tiers(labels, preds) == [("weekly_vs_dated", 0, 0), ("spurious", None, 1)]


def test_weekly_prediction_paired_exactly_does_not_cover_dated_labels():
    labels = [_ev(), _dated()]
    preds = [_ev()]
    assert _tiers(labels, preds) == [("exact", 0, 0), ("missed", 1, None)]


def test_covering_weekly_prediction_covers_optional_dated_labels_too():
    labels = [_dated(), _dated(date="2026-10-11", optional="include")]
    preds = [_ev()]
    records = match_events(labels, preds)
    assert _tiers(labels, preds) == [("weekly_vs_dated", 0, 0), ("optional", 1, 0)]
    assert score_optional(records)["preferred"] == 1
    assert score_records(records)["predicted_events"] == 1


def test_bulletin_is_perfect_at_loose_when_a_weekly_prediction_covers_its_dates(tmp_path: Path):
    labels_dir, out_dir = tmp_path / "labels", tmp_path / "eval"
    _label(labels_dir, HASH_A, "done", [_dated(), _dated(date="2026-10-11")])
    _pred(out_dir, HASH_A, [_ev()])
    report = build_report(out_dir, labels_dir)
    assert report["bulletin_level"]["perfect"] == {
        "strict": 0, "core": 0, "loose": 1, "any_time": 1,
    }
    assert report["by_event_kind"]["weekly"]["predicted_events"] == 1
    assert report["by_event_kind"]["specific_date"]["levels"]["loose"]["recall"] == 1.0


def test_optional_events_are_paired_last_and_left_out_of_the_scores():
    labels = [
        _ev(optional="include"),                          # also matches the required 10:00
        _ev(),
        _ev(start_time="12:00", optional="include"),      # left out by the classifier
        _ev(start_time="17:00", optional="exclude"),      # predicted at 17:15
        _ev(start_time="19:00", optional="exclude"),      # left out, as preferred
    ]
    preds = [_ev(), _ev(start_time="17:15"), _ev(note="second")]
    records = match_events(labels, preds)
    # The required 10:00 is paired first; the optional one takes the other 10:00.
    assert _tiers(labels, preds) == [
        ("optional", 0, 2), ("exact", 1, 0), ("optional", 2, None), ("optional", 3, 1),
        ("optional", 4, None),
    ]
    assert [r["found_as"] for r in records if r["tier"] == "optional"] == [
        "exact", None, "wrong_time", None,
    ]
    score = score_records(records)
    assert score["label_events"] == 1 and score["predicted_events"] == 1
    assert score["levels"]["strict"]["f1"] == 1.0 and score["spurious"] == 0
    optional = score_optional(records)
    assert optional["events"] == 4 and optional["preferred"] == 2 and optional["rate"] == 0.5
    assert optional["by_preference"] == {
        "include": {"events": 2, "preferred": 1, "rate": 0.5},
        "exclude": {"events": 2, "preferred": 1, "rate": 0.5},
    }


def test_optional_events_never_count_as_missed_or_spurious_in_the_report(tmp_path: Path):
    labels_dir, out_dir = tmp_path / "labels", tmp_path / "eval"
    _label(labels_dir, HASH_A, "done", [
        _ev(), _ev(day_of_week="Friday", optional="include"),
        _ev(day_of_week="Saturday", optional="exclude"),
    ])
    _pred(out_dir, HASH_A, [_ev(), _ev(day_of_week="Saturday")])
    report = build_report(out_dir, labels_dir)
    assert report["overall"]["label_events"] == 1 and report["overall"]["predicted_events"] == 1
    assert report["overall"]["levels"]["strict"]["f1"] == 1.0
    assert report["bulletin_level"]["perfect"]["strict"] == 1
    assert report["optional"]["preferred"] == 0 and report["optional"]["events"] == 2
    assert set(report["by_event_type"]) == {"mass"}
    assert report["by_event_type"]["mass"]["label_events"] == 1

    markdown = render_markdown(report)
    assert "## Optional events" in markdown
    assert "| include | 1 | 0/1 (0.0%) |" in markdown
    assert "**optional, prefer include**: left out" in markdown
    assert "**optional, prefer exclude**" in markdown


def test_field_accuracy_outcomes():
    labels = [
        _ev(end_time="11:00", weeks_of_month=["first"], note="Latin"),
        _ev(start_time="08:00", season={"start_month": 10, "start_day": None,
                                        "end_month": 6, "end_day": None}),
    ]
    preds = [
        _ev(end_time="11:30", weeks_of_month=["first"]),
        _ev(start_time="08:00", end_time="09:00", note="  "),
    ]
    fields = field_accuracy(match_events(labels, preds))
    assert fields["end_time"] == {
        "pairs": 2, "accuracy": 0.0, "both_empty": 0, "match": 0, "different": 1,
        "missing": 0, "extra": 1,
    }
    assert fields["weeks_of_month"]["match"] == 1 and fields["weeks_of_month"]["both_empty"] == 1
    assert fields["season"]["missing"] == 1 and fields["season"]["accuracy"] == 0.5
    assert fields["note"]["missing"] == 1 and fields["note"]["both_empty"] == 1


# ── Whole report over files on disk ─────────────────────────────────────────
def _write(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def _label(labels_dir: Path, content_hash: str, status: str, events, **extra) -> None:
    label = empty_label("st-mary-parish", content_hash, "https://x/b.pdf")
    _write(labels_dir / "st-mary-parish" / f"{content_hash}.json",
           label | {"status": status, "events": events} | extra)


def _pred(out_dir: Path, content_hash: str, events, **extra) -> None:
    _write(out_dir / "predictions" / "st-mary-parish" / f"{content_hash[:12]}.json", {
        "content_hash": content_hash,
        "classifier": "fake", "classifier_version": "fake-v1", "published_date": None,
        "wrong_bulletin": False, "usage": {"input_tokens": 100}, "seconds": 2.0,
        "from_cache": False, "events": events,
    } | extra)


@pytest.fixture
def files(tmp_path: Path):
    labels_dir, out_dir = tmp_path / "labels", tmp_path / "eval"
    _label(labels_dir, HASH_A, "done", [_ev(), _ev(day_of_week="Saturday", start_time="16:00")],
           published_date="2026-10-04")
    _label(labels_dir, HASH_B, "done", [_ev(event_type="confession")])
    _label(labels_dir, HASH_C, "skipped", [_ev()])
    _pred(out_dir, HASH_A, [_ev(), _dated(date="2026-10-03", start_time="16:00")],
          published_date="2026-10-04")
    _pred(out_dir, HASH_C, [])
    return labels_dir, out_dir


def test_build_report_skips_skipped_and_lists_unpredicted(files):
    labels_dir, out_dir = files
    report = build_report(out_dir, labels_dir)
    assert [b["content_hash"] for b in report["bulletins"]] == [HASH_A]
    assert report["unpredicted"] == [{"parish_slug": "st-mary-parish", "content_hash": HASH_B}]
    assert report["overall"]["levels"]["strict"]["f1"] == 0.5
    assert report["overall"]["levels"]["loose"]["f1"] == 1.0
    kinds = report["by_event_kind"]
    assert kinds["weekly"]["levels"]["loose"]["recall"] == 1.0
    assert kinds["weekly"]["levels"]["loose"]["precision"] == 1.0
    assert kinds["specific_date"]["levels"]["loose"]["precision"] == 1.0
    assert kinds["specific_date"]["levels"]["loose"]["recall"] is None
    bl = report["bulletin_level"]
    assert bl["perfect"] == {"strict": 0, "core": 0, "loose": 1, "any_time": 1}
    assert bl["published_date"]["accuracy"] == 1.0
    assert report["cost"]["usage"] == {"input_tokens": 100}

    markdown = render_markdown(report)
    assert "# Eval report: fake" in markdown
    assert "**weekly_vs_dated**" in markdown and "no prediction" in markdown


def test_write_report_writes_next_to_predictions(files, tmp_path, monkeypatch):
    labels_dir, out_dir = files
    monkeypatch.setattr(runner, "RUNS_DIR", tmp_path / "runs")
    with pytest.raises(FileNotFoundError):
        write_report(classifier_name="gemini-flash", version="v1", labels_dir=labels_dir)

    target = runner.run_dir("gemini-flash") / "eval" / version_dir_name("gemini-flash", "v1")
    target.parent.mkdir(parents=True)
    out_dir.rename(target)
    summary = write_report(classifier_name="gemini-flash", version="v1", labels_dir=labels_dir)
    assert Path(summary["report_md"]).read_text().startswith("# Eval report")
    assert json.loads(Path(summary["report_json"]).read_text())["bulletins"]
    assert summary["f1"] == {"strict": 0.5, "core": 0.5, "loose": 1.0, "any_time": 1.0}

    # The directory name the "versions with output" list prints works as --version too.
    by_dir = write_report(classifier_name="gemini-flash", version=target.name,
                          labels_dir=labels_dir)
    assert by_dir["report_md"] == summary["report_md"]


def test_report_finds_a_run_made_with_another_model(files, tmp_path, monkeypatch):
    labels_dir, out_dir = files
    monkeypatch.setattr(runner, "RUNS_DIR", tmp_path / "runs")
    options = {"model": "gpt-6.1-sol", "pdf_as_images": True}
    version = get_classifier("gpt-6-luna", **options).version
    target = runner.run_dir("gpt-6.1-sol") / "eval" / version_dir_name("gpt-6.1-sol", version)
    target.parent.mkdir(parents=True)
    out_dir.rename(target)

    summary = write_report(classifier_name="gpt-6-luna", classifier_options=options,
                           labels_dir=labels_dir)
    assert Path(summary["report_md"]).parent == target
