from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest


@pytest.fixture
def fit_module(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "scripts"))
    return importlib.import_module("pdf_detail_fit")


def test_study_key_ignores_notes_and_page_numbers():
    from scripts.pdf_detail_study import event_key

    original = {"church_slug": "church", "event_type": "mass", "start_time": "09:00"}
    annotated = {**original, "note": "Different wording", "page_number": 3}
    assert event_key(original) == event_key(annotated)
    assert event_key(original) != event_key({**original, "start_time": "10:00"})


def test_confusion_penalizes_missed_benefits(fit_module):
    metrics = fit_module.confusion([True, True, False, False], [True, False, True, False])
    assert (metrics["tp"], metrics["fn"], metrics["fp"], metrics["tn"]) == (1, 1, 1, 1)
    assert metrics["weighted_loss_fn5_fp1"] == 6
    assert metrics["recall"] == metrics["precision"] == 0.5


def test_stump_separates_simple_feature(fit_module):
    vectors = [{"scan_fraction": value} for value in (0, 0.1, 0.8, 1)]
    rule = fit_module.fit_stump(vectors, [False, False, True, True])
    assert [fit_module.predict(rule, values) for values in vectors] == [False, False, True, True]
    assert rule["feature"] == "scan_fraction"


def test_stump_with_no_confirmed_benefits_prefers_low(fit_module):
    vectors = [{"scan_fraction": value} for value in (0, 1)]
    rule = fit_module.fit_stump(vectors, [False, False])
    assert rule == {"feature": "constant", "high": False}


def test_subset_prepare_selects_exact_hash_and_snapshots_label(tmp_path, monkeypatch):
    from scripts.pdf_detail_study import prepare

    monkeypatch.chdir(tmp_path)
    cohort = tmp_path / "gemini"
    content_hash = "a" * 64
    for slug in ("selected", "excluded"):
        prediction = cohort / "predictions" / slug / "prediction.json"
        prediction.parent.mkdir(parents=True)
        prediction.write_text(json.dumps({"parish_slug": slug, "content_hash": content_hash}))
        label = tmp_path / "data/labels" / slug / f"{content_hash}.json"
        label.parent.mkdir(parents=True)
        label.write_text(json.dumps({"status": "done", "events": []}))
    output = tmp_path / "study"
    labels = prepare(cohort, output, ["selected"])
    assert len(list(labels.glob("*/*.json"))) == 1
    manifest = json.loads((output / "cohort.json").read_text())
    assert manifest["bulletins"][0]["parish_slug"] == "selected"
    assert manifest["bulletins"][0]["content_hash"] == content_hash
    source = tmp_path / "data/labels/selected" / f"{content_hash}.json"
    source.write_text("changed")
    assert json.loads((labels / "selected" / source.name).read_text())["status"] == "done"
