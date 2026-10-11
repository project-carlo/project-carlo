from __future__ import annotations

import hashlib
import json
from io import BytesIO
from pathlib import Path
from random import Random

import pytest
from pypdf import PdfWriter

from scripts import pdf_detail_followup_features as sidecar


def features(text_chars=100, coverage=0.0):
    return {
        "pages": [
            {
                "page_number": 1,
                "text_chars": text_chars,
                "image_coverage_fraction_estimate": coverage,
                "text_like_component_count": 200,
                "ink_density": 0.1,
                "text_like_height_median_low_detail_px": 4,
                "line_pitch_low_detail_px": 8,
                "errors": [],
            }
        ],
    }


@pytest.fixture
def cohort(tmp_path):
    rows = []
    for position, slug in enumerate(("alpha", "alpha", "beta", "gamma"), start=1):
        source = tmp_path / f"frozen-{position}.pdf"
        data = f"synthetic PDF {position}".encode()
        source.write_bytes(data)
        rows.append(
            {
                "parish_slug": slug,
                "content_hash": f"{position:064x}",
                "pdf_path": str(source),
                "pdf_sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    # Distinct leading prefixes, since filenames intentionally use hash12.
    for position, row in enumerate(rows, start=1):
        row["content_hash"] = f"{position:x}" * 64
    path = tmp_path / "cohort.json"
    sidecar.write_json(path, {"bulletins": rows})
    return path, rows


def analysis_inputs(tmp_path, cohort, labels=None):
    path, rows = cohort
    feature_path = tmp_path / "features.json"
    review_path = tmp_path / "manual_review.json"
    sidecar.write_json(
        feature_path,
        {
            "bulletins": [
                {**row, "status": "ok", "features": features(0, 0.9) if index == 0 else features()}
                for index, row in enumerate(rows)
            ]
        },
    )
    labels = labels if labels is not None else [True, False, False, None]
    reviews = [
        {
            "parish_slug": row["parish_slug"],
            "content_hash": row["content_hash"],
            "observed_supported_advantage": value,
            "observed_raster_advantage": value,
            "verdict": "reviewed",
        }
        for row, value in zip(rows, labels)
        if value is not None
    ]
    sidecar.write_json(review_path, {"bulletins": reviews})
    return path, feature_path, review_path, tmp_path / "feature_analysis.json"


def test_exact_frozen_bytes_resume_multiple_hashes_and_settings(cohort, tmp_path, monkeypatch):
    path, rows = cohort
    calls = []

    def extract(data, **settings):
        calls.append((data, settings))
        return features()

    monkeypatch.setattr(sidecar, "extract_pdf_features", extract)
    first = sidecar.extract_features(path, tmp_path, workers=2)
    assert first["counts"] == {"documents": 4, "ok": 4, "errors": 0, "resumed": 0}
    assert {data for data, _ in calls} == {
        f"synthetic PDF {position}".encode() for position in range(1, 5)
    }
    assert first["walltime_seconds"] >= 0
    for row in rows:
        stored = tmp_path / "features" / row["parish_slug"] / f"{row['content_hash'][:12]}.json"
        assert sidecar.read_json(stored)["scan_risk_routing"]["detail"] == "low"
    second = sidecar.extract_features(path, tmp_path)
    assert second["counts"]["resumed"] == 4
    assert len(calls) == 4
    sidecar.extract_features(path, tmp_path, dpi=120)
    assert len(calls) == 8
    assert sidecar.read_json(tmp_path / "features.json")["settings"]["dpi"] == 120


def test_changed_frozen_pdf_cannot_resume_or_extract(cohort, tmp_path, monkeypatch):
    path, rows = cohort
    calls = []
    monkeypatch.setattr(
        sidecar, "extract_pdf_features", lambda data, **settings: calls.append(data) or features()
    )
    sidecar.extract_features(path, tmp_path)
    Path(rows[0]["pdf_path"]).write_bytes(b"modified after freezing")
    result = sidecar.extract_features(path, tmp_path)
    assert result["counts"]["errors"] == 1
    assert result["counts"]["resumed"] == 3
    assert len(calls) == 4
    assert "SHA256 mismatch" in result["bulletins"][0]["error"]
    assert "features" not in result["bulletins"][0]


def test_corrupt_and_failed_cache_are_retried(cohort, tmp_path, monkeypatch):
    path, rows = cohort
    monkeypatch.setattr(sidecar, "extract_pdf_features", lambda *args, **kwargs: features())
    sidecar.extract_features(path, tmp_path)
    destination = tmp_path / "features" / "alpha" / f"{rows[0]['content_hash'][:12]}.json"
    destination.write_text("broken json")
    assert sidecar.extract_features(path, tmp_path)["counts"]["resumed"] == 3
    sidecar.write_json(destination, {"status": "error"})
    assert sidecar.extract_features(path, tmp_path)["counts"]["resumed"] == 3


def test_prefix_collision_and_unsafe_identity_rejected(cohort, tmp_path):
    path, rows = cohort
    rows[1]["content_hash"] = rows[0]["content_hash"][:12] + "b" * 52
    sidecar.write_json(path, {"bulletins": rows})
    with pytest.raises(ValueError, match="collision"):
        sidecar.extract_features(path, tmp_path)
    with pytest.raises(ValueError, match="Unsafe"):
        sidecar.identity({"parish_slug": "../escape", "content_hash": "a" * 64})
    with pytest.raises(ValueError, match="Duplicate"):
        sidecar.indexed([rows[0], rows[0]])


@pytest.mark.parametrize("workers", [0, 9])
def test_worker_bound(cohort, tmp_path, workers):
    with pytest.raises(ValueError, match="workers"):
        sidecar.extract_features(cohort[0], tmp_path, workers=workers)


def test_real_synthetic_pdf_uses_existing_pdfium_lock(cohort, tmp_path, monkeypatch):
    from pdf_extract import pdf_detail
    from pdf_extract.classifiers.openai_responses import _PDFIUM_LOCK

    path, rows = cohort
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    buffer = BytesIO()
    writer.write(buffer)
    data = buffer.getvalue()
    for row in rows:
        Path(row["pdf_path"]).write_bytes(data)
        row["pdf_sha256"] = hashlib.sha256(data).hexdigest()
    sidecar.write_json(path, {"bulletins": rows})
    document = pdf_detail.pdfium.PdfDocument
    checked = []

    def locked_document(*args, **kwargs):
        assert _PDFIUM_LOCK.locked()
        checked.append(True)
        return document(*args, **kwargs)

    monkeypatch.setattr(pdf_detail.pdfium, "PdfDocument", locked_document)
    result = sidecar.extract_features(path, tmp_path, workers=2, max_render_pixels=10_000)
    assert result["counts"]["ok"] == len(checked) == 4


@pytest.mark.parametrize("value", [None, 0, 1, "false", "true"])
def test_only_explicit_booleans_are_labels(value):
    assert sidecar.reviewed_truth({"verdict": "reviewed", "target": value}, "target") is None


@pytest.mark.parametrize("verdict", [None, "", "unknown", "ambiguous", "inconclusive", "pending"])
def test_unclear_verdict_is_unknown(verdict):
    assert sidecar.reviewed_truth({"verdict": verdict, "target": False}, "target") is None


def test_cost_sensitivity_and_confusion():
    truth = [True] + [False] * 7
    vectors = [{"scan_fraction": 0.5}] * len(truth)
    assert sidecar.fit_threshold(vectors, truth, 5) == {"feature": "constant", "high": False}
    assert sidecar.fit_threshold(vectors, truth, 10) == {"feature": "constant", "high": True}
    metrics = sidecar.confusion([True, True, False, False], [True, False, True, False])
    assert (metrics["tp"], metrics["fn"], metrics["fp"], metrics["tn"]) == (1, 1, 1, 1)
    assert metrics["weighted_loss_fn5_fp1"] == 6
    assert metrics["weighted_loss_fn10_fp1"] == 11
    assert sidecar.confusion([], [])["recall"] is None


def test_explicit_no_relative_change_is_reviewed_negative_not_source_accuracy():
    review = {"review_status": "no_relative_change", "target": False}
    assert sidecar.reviewed_truth(review, "target") is False
    assert sidecar.reviewed_truth({**review, "target": None}, "target") is None
    assert sidecar.reviewed_truth({**review, "target": True}, "target") is None
    assert (
        sidecar.reviewed_truth(
            {"review_status": "unknown", "verdict": "reviewed", "target": False}, "target"
        )
        is None
    )


def test_amended_cohort_resume_adds_only_new_bulletin(cohort, tmp_path, monkeypatch):
    path, rows = cohort
    calls = []
    monkeypatch.setattr(
        sidecar, "extract_pdf_features", lambda data, **settings: calls.append(data) or features()
    )
    sidecar.extract_features(path, tmp_path)
    source = tmp_path / "amended.pdf"
    source.write_bytes(b"amended frozen PDF")
    rows.append(
        {
            "parish_slug": "alpha",
            "content_hash": "a" * 64,
            "pdf_path": str(source),
            "pdf_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        }
    )
    sidecar.write_json(path, {"bulletins": rows})
    result = sidecar.extract_features(path, tmp_path)
    assert result["counts"] == {"documents": 5, "ok": 5, "errors": 0, "resumed": 4}
    assert len(calls) == 5


def test_threshold_separates_synthetic_feature():
    vectors = [{"scan_fraction": value} for value in (0, 0.1, 0.8, 1)]
    rule = sidecar.fit_threshold(vectors, [False, False, True, True])
    assert [sidecar.predict(rule, values) for values in vectors] == [False, False, True, True]


@pytest.mark.parametrize("fn_weight", [5, 10])
def test_fast_threshold_search_matches_exhaustive_search(fn_weight):
    random = Random(123)
    for _ in range(15):
        vectors = [
            {"scan_fraction": random.randrange(5), "components": random.randrange(10)}
            for _ in range(20)
        ]
        truth = [bool(random.randrange(2)) for _ in vectors]
        candidates = [{"feature": "constant", "high": False}, {"feature": "constant", "high": True}]
        for feature in vectors[0]:
            values = sorted({row[feature] for row in vectors})
            thresholds = [
                *values,
                *[left + (right - left) / 2 for left, right in zip(values, values[1:])],
            ]
            candidates.extend(
                {"feature": feature, "operator": operator, "threshold": threshold}
                for operator in ("<=", ">=")
                for threshold in thresholds
            )

        def rank(rule):
            metrics = sidecar.confusion(truth, [sidecar.predict(rule, row) for row in vectors])
            return (
                fn_weight * metrics["fn"] + metrics["fp"],
                metrics["fn"],
                metrics["fp"],
                rule["feature"] != "constant",
                json.dumps(rule, sort_keys=True),
            )

        assert sidecar.fit_threshold(vectors, truth, fn_weight) == min(candidates, key=rank)


def test_grouped_loo_excludes_all_bulletins_of_held_out_parish(cohort, tmp_path):
    inputs = analysis_inputs(tmp_path, cohort)
    result = sidecar.analyze(*inputs)
    target = result["targets"][sidecar.TARGETS[0]]
    assert target["counts"]["unknown"] == 1
    assert target["counts"]["reviewed_negative"] == 2
    alpha = next(fold for fold in target["folds"] if fold["held_out_parish"] == "alpha")
    assert alpha["training_parishes"] == ["beta"]
    assert alpha["training_documents"] == 1
    assert alpha["test_documents"] == 2
    for fold in target["folds"]:
        assert fold["held_out_parish"] not in fold["training_parishes"]
    reviews = sidecar.read_json(inputs[2])
    for row in reviews["bulletins"]:
        if row["parish_slug"] == "alpha":
            row[sidecar.TARGETS[0]] = not row[sidecar.TARGETS[0]]
    sidecar.write_json(inputs[2], reviews)
    mutated = sidecar.analyze(*inputs)
    new_alpha = next(
        fold
        for fold in mutated["targets"][sidecar.TARGETS[0]]["folds"]
        if fold["held_out_parish"] == "alpha"
    )
    assert new_alpha["rules"] == alpha["rules"]


def test_eval_parish_never_trains_even_its_other_hash(cohort, tmp_path):
    path, rows = cohort
    rows[0]["split"] = "test"
    sidecar.write_json(path, {"bulletins": rows})
    inputs = analysis_inputs(tmp_path, cohort, [True, False, False, True])
    result = sidecar.analyze(*inputs)
    assert result["protected_parishes"] == ["alpha"]
    for target in result["targets"].values():
        assert all("alpha" not in fold["training_parishes"] for fold in target["folds"])
    with pytest.raises(ValueError, match="eval/test"):
        sidecar.analyze(*inputs, train_parishes=["alpha"])


def test_fixed_train_pool_held_out_feature_and_target_cannot_change_rule(cohort, tmp_path):
    inputs = analysis_inputs(tmp_path, cohort, [True, False, False, True])
    result = sidecar.analyze(*inputs, train_parishes=["beta", "gamma"])
    before = result["targets"][sidecar.TARGETS[0]]["folds"][0]["rules"]
    data = sidecar.read_json(inputs[1])
    for row in data["bulletins"]:
        if row["parish_slug"] == "alpha":
            row["features"] = features(999_999, 0.6)
    sidecar.write_json(inputs[1], data)
    reviews = sidecar.read_json(inputs[2])
    for row in reviews["bulletins"]:
        if row["parish_slug"] == "alpha":
            row[sidecar.TARGETS[0]] = False
    sidecar.write_json(inputs[2], reviews)
    changed = sidecar.analyze(*inputs, train_parishes=["beta", "gamma"])
    assert changed["targets"][sidecar.TARGETS[0]]["folds"][0]["rules"] == before
    assert {
        row["parish_slug"] for row in changed["targets"][sidecar.TARGETS[0]]["predictions"]
    } == {"alpha"}


def test_no_training_and_failed_features_counted_not_imputed(cohort, tmp_path):
    inputs = analysis_inputs(tmp_path, cohort, [True, False, None, None])
    data = sidecar.read_json(inputs[1])
    data["bulletins"][0]["status"] = "error"
    sidecar.write_json(inputs[1], data)
    result = sidecar.analyze(*inputs)
    target = result["targets"][sidecar.TARGETS[0]]
    assert target["counts"]["unknown"] == 2
    assert target["counts"]["reviewed_feature_errors"] == 1
    assert target["counts"]["model_evaluated"] == 0
    assert target["folds"][0]["status"] == "no_training_data"
    assert target["predictions"][0]["threshold_fn5"] is None


def test_analysis_provenance_and_unknown_review_identity_rejected(cohort, tmp_path):
    inputs = analysis_inputs(tmp_path, cohort)
    data = sidecar.read_json(inputs[1])
    data["bulletins"][0]["pdf_sha256"] = "f" * 64
    sidecar.write_json(inputs[1], data)
    with pytest.raises(ValueError, match="provenance"):
        sidecar.analyze(*inputs)
    inputs = analysis_inputs(tmp_path, cohort)
    data = sidecar.read_json(inputs[2])
    data["bulletins"][0]["content_hash"] = "e" * 64
    sidecar.write_json(inputs[2], data)
    with pytest.raises(ValueError, match="identities"):
        sidecar.analyze(*inputs)


def test_cli_actions_on_synthetic_inputs(cohort, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sidecar, "extract_pdf_features", lambda *args, **kwargs: features())
    assert sidecar.main(["features", "--cohort", str(cohort[0])]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] == 4
    analysis_inputs(tmp_path, cohort)
    assert sidecar.main(["model", "--cohort", str(cohort[0])]) == 0
    assert json.loads(capsys.readouterr().out)[sidecar.TARGETS[0]]["unknown"] == 1
