"""Frozen PDF features and parish-held-out threshold models; no API calls/reports.

Use actions features, analysis (or model). Relative frozen PDF paths resolve from
the working directory. No latest-bulletin substitution or evaluation-set fitting.
Analysis defaults to grouped leave-one-parish-out. Repeated --train-parish selects
a fixed training pool instead; all other parishes are held out. Any parish with an
eval/test split is excluded from training entirely. Missing/ambiguous labels are
UNKNOWN; explicit boolean false with review_status=no_relative_change is a valid
relative-advantage negative, not a claim about source accuracy. No model is fitted
until reviewed targets are supplied. Outputs are JSON artifacts, not reports.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
import uuid
from bisect import bisect_left, bisect_right
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from pdf_extract.pdf_detail import extract_pdf_features, route_scan_risk

DEFAULT_COHORT = Path("data/runs/pdf-detail-full/eval/2026-10-09/cohort.json")
TARGETS = ("observed_supported_advantage", "observed_raster_advantage")
UNKNOWN_VERDICTS = {"unknown", "unreviewed", "pending", "unclear", "ambiguous", "inconclusive"}
SCHEMA_VERSION = 1


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_text(
            json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def identity(row: dict) -> tuple[str, str]:
    slug, content_hash = row["parish_slug"], row["content_hash"]
    if not isinstance(slug, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", slug):
        raise ValueError("Unsafe parish_slug")
    if not isinstance(content_hash, str) or not re.fullmatch(r"[a-fA-F0-9]{12,64}", content_hash):
        raise ValueError("content_hash must contain 12-64 hexadecimal characters")
    return slug, content_hash


def indexed(rows: list[dict]) -> dict[tuple[str, str], dict]:
    result = {}
    for row in rows:
        key = identity(row)
        if key in result:
            raise ValueError(f"Duplicate bulletin: {key}")
        result[key] = row
    return result


def extract_features(
    cohort: Path,
    output: Path,
    *,
    workers: int = 2,
    dpi: float = 100,
    max_render_pixels: int = 2_000_000,
    max_pages: int | None = None,
) -> dict:
    """Extract verified bytes; the existing extractor owns the shared PDFium lock."""
    if not 1 <= workers <= 8:
        raise ValueError("workers must be between 1 and 8")
    if not math.isfinite(dpi) or dpi <= 0 or max_render_pixels < 4:
        raise ValueError("Invalid render settings")
    if max_pages is not None and max_pages < 1:
        raise ValueError("max_pages must be positive")
    started = time.perf_counter()
    rows = list(indexed(read_json(cohort)["bulletins"]).values())
    destinations = set()
    for row in rows:
        slug, content_hash = identity(row)
        destination = (slug.lower(), content_hash[:12].lower())
        if destination in destinations:
            raise ValueError(f"Truncated hash/path collision: {destination}")
        destinations.add(destination)
        if not re.fullmatch(r"[a-fA-F0-9]{64}", row.get("pdf_sha256", "")):
            raise ValueError("Every frozen PDF needs a full pdf_sha256")
    settings = {"dpi": dpi, "max_render_pixels": max_render_pixels, "max_pages": max_pages}

    def extract_one(row: dict) -> dict:
        document_started = time.perf_counter()
        slug, content_hash = identity(row)
        destination = output / "features" / slug / f"{content_hash[:12]}.json"
        provenance = {
            "schema_version": SCHEMA_VERSION,
            "parish_slug": slug,
            "content_hash": content_hash,
            "pdf_path": row["pdf_path"],
            "pdf_sha256": row["pdf_sha256"].lower(),
            "settings": settings,
        }
        try:
            data = Path(row["pdf_path"]).read_bytes()
            if hashlib.sha256(data).hexdigest() != provenance["pdf_sha256"]:
                raise ValueError(f"Frozen PDF SHA256 mismatch: {row['pdf_path']}")
            if destination.exists():
                try:
                    cached = read_json(destination)
                    if (
                        all(cached.get(key) == value for key, value in provenance.items())
                        and cached.get("status") == "ok"
                        and isinstance(cached.get("features"), dict)
                    ):
                        return {
                            **cached,
                            "scan_risk_routing": route_scan_risk(cached["features"]),
                            "resumed": True,
                            "walltime_seconds": time.perf_counter() - document_started,
                        }
                except (ValueError, KeyError, TypeError, AttributeError):
                    pass
            extraction_started = time.perf_counter()
            features = extract_pdf_features(data, **settings)
            result = {
                **provenance,
                "status": "ok",
                "features": features,
                "scan_risk_routing": route_scan_risk(features),
                "extraction_walltime_seconds": time.perf_counter() - extraction_started,
                "resumed": False,
            }
        except Exception as exc:
            result = {
                **provenance,
                "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
                "resumed": False,
            }
        result["walltime_seconds"] = time.perf_counter() - document_started
        write_json(destination, result)
        return result

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(extract_one, rows))
    aggregate = {
        "schema_version": SCHEMA_VERSION,
        "cohort_path": str(cohort),
        "settings": settings,
        "workers": workers,
        "walltime_seconds": time.perf_counter() - started,
        "counts": {
            "documents": len(results),
            "ok": sum(row["status"] == "ok" for row in results),
            "errors": sum(row["status"] == "error" for row in results),
            "resumed": sum(row["resumed"] for row in results),
        },
        "bulletins": results,
    }
    write_json(output / "features.json", aggregate)
    return aggregate


def vector(features: dict) -> dict[str, float]:
    pages = features.get("pages", [])
    count = max(1, len(pages))
    scans = [
        page
        for page in pages
        if page.get("text_chars") is not None
        and page["text_chars"] < 80
        and (page.get("image_coverage_fraction_estimate") or 0) >= 0.7
    ]
    return {
        "page_count": float(len(pages)),
        "scan_fraction": len(scans) / count,
        "early_scan_count": float(sum(page["page_number"] <= 3 for page in scans)),
        "mean_text_chars": sum(page.get("text_chars") or 0 for page in pages) / count,
        "mean_image_coverage": sum(
            page.get("image_coverage_fraction_estimate") or 0 for page in pages
        )
        / count,
        "mean_components": sum(page.get("text_like_component_count") or 0 for page in pages)
        / count,
        "min_line_pitch_low_px": min(
            (
                page["line_pitch_low_detail_px"]
                for page in pages
                if page.get("line_pitch_low_detail_px") is not None
            ),
            default=512,
        ),
        "min_native_height_low_px": min(
            (
                page["native_char_height_p10_low_detail_px"]
                for page in pages
                if page.get("native_char_height_p10_low_detail_px") is not None
            ),
            default=512,
        ),
        "feature_error_count": float(
            sum(bool(page.get("errors")) for page in pages)
            + bool(features.get("errors"))
            + bool(features.get("truncated"))
        ),
    }


def confusion(truth: list[bool], predictions: list[bool]) -> dict:
    if len(truth) != len(predictions):
        raise ValueError("Truth/prediction lengths differ")
    counts = {
        "tp": sum(actual and predicted for actual, predicted in zip(truth, predictions)),
        "fn": sum(actual and not predicted for actual, predicted in zip(truth, predictions)),
        "fp": sum(not actual and predicted for actual, predicted in zip(truth, predictions)),
        "tn": sum(not actual and not predicted for actual, predicted in zip(truth, predictions)),
    }
    return {
        **counts,
        "n": len(truth),
        "recall": counts["tp"] / sum(truth) if any(truth) else None,
        "precision": counts["tp"] / sum(predictions) if any(predictions) else None,
        "weighted_loss_fn5_fp1": 5 * counts["fn"] + counts["fp"],
        "weighted_loss_fn10_fp1": 10 * counts["fn"] + counts["fp"],
    }


def predict(rule: dict, values: dict) -> bool:
    if rule["feature"] == "constant":
        return rule["high"]
    value = values[rule["feature"]]
    return value <= rule["threshold"] if rule["operator"] == "<=" else value >= rule["threshold"]


def fit_threshold(vectors: list[dict], truth: list[bool], fn_weight: int = 5) -> dict:
    if not vectors or len(vectors) != len(truth):
        raise ValueError("Fitting requires nonempty, aligned training data")
    positives = sum(truth)
    negatives = len(truth) - positives

    def rank(rule: dict, false_negatives: int, false_positives: int) -> tuple:
        return (
            fn_weight * false_negatives + false_positives,
            false_negatives,
            false_positives,
            rule["feature"] != "constant",
            json.dumps(rule, sort_keys=True),
        )

    best_rule = {"feature": "constant", "high": False}
    best_rank = rank(best_rule, positives, 0)
    high_rule = {"feature": "constant", "high": True}
    high_rank = rank(high_rule, 0, negatives)
    if high_rank < best_rank:
        best_rule, best_rank = high_rule, high_rank
    for feature in sorted(vectors[0]):
        ordered = sorted((values[feature], actual) for values, actual in zip(vectors, truth))
        observed = [value for value, _ in ordered]
        if not all(math.isfinite(value) for value in observed):
            raise ValueError("Model features must be finite")
        prefix_positives = [0]
        for _, actual in ordered:
            prefix_positives.append(prefix_positives[-1] + actual)
        values = sorted(set(observed))
        thresholds = [
            *values,
            *[left + (right - left) / 2 for left, right in zip(values, values[1:])],
        ]
        for operator in ("<=", ">="):
            for threshold in thresholds:
                rule = {"feature": feature, "operator": operator, "threshold": threshold}
                if operator == "<=":
                    boundary = bisect_right(observed, threshold)
                    false_negatives = positives - prefix_positives[boundary]
                    false_positives = boundary - prefix_positives[boundary]
                else:
                    boundary = bisect_left(observed, threshold)
                    false_negatives = prefix_positives[boundary]
                    false_positives = negatives - (boundary - prefix_positives[boundary])
                candidate_rank = rank(rule, false_negatives, false_positives)
                if candidate_rank < best_rank:
                    best_rule, best_rank = rule, candidate_rank
    return best_rule


def reviewed_truth(review: dict | None, target: str) -> bool | None:
    if review is None or type(review.get(target)) is not bool:
        return None
    review_status = str(review.get("review_status", "")).strip().lower()
    if review_status in UNKNOWN_VERDICTS:
        return None
    if review_status == "no_relative_change":
        return False if review[target] is False else None
    verdict = review.get("verdict")
    if not isinstance(verdict, str) or not verdict.strip():
        return None
    if verdict.strip().lower() in UNKNOWN_VERDICTS:
        return None
    return review[target]


def analyze(
    cohort: Path,
    features_path: Path,
    review_path: Path,
    output: Path,
    *,
    train_parishes: list[str] | None = None,
) -> dict:
    manifest = indexed(read_json(cohort)["bulletins"])
    feature_rows = indexed(read_json(features_path)["bulletins"])
    reviews = indexed(read_json(review_path)["bulletins"])
    if set(feature_rows) != set(manifest) or not set(reviews) <= set(manifest):
        raise ValueError("Feature/review identities must match the frozen cohort")
    protected = {
        key[0]
        for key, row in manifest.items()
        if str(row.get("split", "")).lower() in {"eval", "evaluation", "test"}
        or str(reviews.get(key, {}).get("split", "")).lower() in {"eval", "evaluation", "test"}
    }
    all_parishes = {key[0] for key in manifest}
    training_pool = set(train_parishes) if train_parishes is not None else all_parishes - protected
    if not training_pool <= all_parishes or training_pool & protected:
        raise ValueError("Training parishes must exist and cannot include eval/test parishes")
    for key, row in feature_rows.items():
        frozen = manifest[key]
        if (
            row.get("pdf_sha256", "").lower() != frozen["pdf_sha256"].lower()
            or row.get("pdf_path") != frozen["pdf_path"]
        ):
            raise ValueError(f"Feature provenance differs from frozen cohort: {key}")
    result = {
        "schema_version": SCHEMA_VERSION,
        "validation": "held_out_parishes"
        if train_parishes is not None
        else "grouped_leave_one_parish_out",
        "false_negative_weights": [5, 10],
        "false_positive_weight": 1,
        "protected_parishes": sorted(protected),
        "training_pool": sorted(training_pool),
        "counts": {"documents": len(manifest), "parishes": len(all_parishes)},
        "targets": {},
    }
    for target in TARGETS:
        labels = {key: reviewed_truth(reviews.get(key), target) for key in manifest}
        usable = {
            key: row
            for key, row in feature_rows.items()
            if labels[key] is not None and row.get("status") == "ok"
        }
        vectors = {key: vector(row["features"]) for key, row in usable.items()}
        evaluation_parishes = (
            all_parishes - training_pool if train_parishes is not None else all_parishes
        )
        folds, predictions = [], []
        for parish in sorted(evaluation_parishes):
            testing = sorted(key for key in usable if key[0] == parish)
            training = sorted(key for key in usable if key[0] != parish and key[0] in training_pool)
            if not testing:
                continue
            rules = (
                {
                    str(weight): fit_threshold(
                        [vectors[key] for key in training],
                        [labels[key] for key in training],
                        weight,
                    )
                    for weight in (5, 10)
                }
                if training
                else {}
            )
            folds.append(
                {
                    "held_out_parish": parish,
                    "training_parishes": sorted({key[0] for key in training}),
                    "training_documents": len(training),
                    "test_documents": len(testing),
                    "rules": rules,
                    "status": "ok" if training else "no_training_data",
                }
            )
            for key in testing:
                predictions.append(
                    {
                        "parish_slug": key[0],
                        "content_hash": key[1],
                        "truth": labels[key],
                        "scan_risk": route_scan_risk(usable[key]["features"])["detail"] == "high",
                        "threshold_fn5": predict(rules["5"], vectors[key]) if rules else None,
                        "threshold_fn10": predict(rules["10"], vectors[key]) if rules else None,
                    }
                )
        comparisons = [row for row in predictions if row["threshold_fn5"] is not None]
        result["targets"][target] = {
            "counts": {
                "reviewed_positive": sum(value is True for value in labels.values()),
                "reviewed_negative": sum(value is False for value in labels.values()),
                "unknown": sum(value is None for value in labels.values()),
                "usable_reviewed": len(usable),
                "reviewed_feature_errors": sum(value is not None for value in labels.values())
                - len(usable),
                "evaluated": len(predictions),
                "model_evaluated": len(comparisons),
            },
            "scan_risk_all_reviewed_held_out": confusion(
                [row["truth"] for row in predictions],
                [row["scan_risk"] for row in predictions],
            ),
            "matched_comparison": {
                name: confusion(
                    [row["truth"] for row in comparisons], [row[name] for row in comparisons]
                )
                for name in ("scan_risk", "threshold_fn5", "threshold_fn10")
            },
            "folds": folds,
            "predictions": predictions,
        }
    write_json(output, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("features", "analysis", "model"))
    parser.add_argument("--cohort", type=Path, default=DEFAULT_COHORT)
    parser.add_argument("--output", type=Path, help="Output directory (default: cohort parent)")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--dpi", type=float, default=100)
    parser.add_argument("--max-render-pixels", type=int, default=2_000_000)
    parser.add_argument("--max-pages", type=int)
    parser.add_argument("--features", type=Path)
    parser.add_argument("--manual-review", type=Path)
    parser.add_argument(
        "--train-parish", action="append", help="Fixed training pool; all others held out"
    )
    args = parser.parse_args(argv)
    output = args.output or args.cohort.parent
    if args.action == "features":
        result = extract_features(
            args.cohort,
            output,
            workers=args.workers,
            dpi=args.dpi,
            max_render_pixels=args.max_render_pixels,
            max_pages=args.max_pages,
        )
        print(json.dumps(result["counts"]))
        return 1 if result["counts"]["errors"] else 0
    result = analyze(
        args.cohort,
        args.features or output / "features.json",
        args.manual_review or output / "manual_review.json",
        output / "feature_analysis.json",
        train_parishes=args.train_parish,
    )
    print(json.dumps({target: value["counts"] for target, value in result["targets"].items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
