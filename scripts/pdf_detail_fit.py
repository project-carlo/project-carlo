"""Compare scan-risk heuristics and cost-weighted decision stumps on reviewed PDFs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pdf_detail_study import DEFAULT_OUTPUT, write_json

from pdf_extract.evals.report import load_scored_bulletins, match_events, score_records
from pdf_extract.pdf_detail import route_scan_risk


def vector(features: dict) -> dict[str, float]:
    pages = features["pages"]
    scans = [
        page
        for page in pages
        if page.get("text_chars", 0) < 80
        and (page.get("image_coverage_fraction_estimate") or 0) >= 0.7
    ]
    pitches = [
        page["line_pitch_low_detail_px"]
        for page in pages
        if page.get("line_pitch_low_detail_px") is not None
    ]
    heights = [
        page["native_char_height_p10_low_detail_px"]
        for page in pages
        if page.get("native_char_height_p10_low_detail_px") is not None
    ]
    return {
        "page_count": float(len(pages)),
        "mean_text_chars": sum(page.get("text_chars", 0) for page in pages) / len(pages),
        "scan_fraction": len(scans) / len(pages),
        "early_scan_count": float(sum(page["page_number"] <= 3 for page in scans)),
        "mean_image_coverage": sum(
            page.get("image_coverage_fraction_estimate") or 0 for page in pages
        )
        / len(pages),
        "mean_image_count": sum(page.get("image_count") or 0 for page in pages) / len(pages),
        "min_line_pitch_low_px": min(pitches, default=512),
        "min_native_height_low_px": min(heights, default=512),
        "mean_components": sum(page["text_like_component_count"] for page in pages) / len(pages),
    }


def confusion(truth: list[bool], predictions: list[bool]) -> dict:
    counts = {
        "tp": sum(actual and predicted for actual, predicted in zip(truth, predictions)),
        "fn": sum(actual and not predicted for actual, predicted in zip(truth, predictions)),
        "fp": sum(not actual and predicted for actual, predicted in zip(truth, predictions)),
        "tn": sum(not actual and not predicted for actual, predicted in zip(truth, predictions)),
    }
    return {
        **counts,
        "recall": counts["tp"] / sum(truth) if any(truth) else None,
        "precision": counts["tp"] / sum(predictions) if any(predictions) else None,
        "high_detail_count": sum(predictions),
        "weighted_loss_fn5_fp1": 5 * counts["fn"] + counts["fp"],
    }


def predict(rule: dict, values: dict) -> bool:
    if rule["feature"] == "constant":
        return rule["high"]
    value = values[rule["feature"]]
    return value <= rule["threshold"] if rule["operator"] == "<=" else value >= rule["threshold"]


def fit_stump(vectors: list[dict], truth: list[bool]) -> dict:
    candidates = [{"feature": "constant", "high": False}, {"feature": "constant", "high": True}]
    for feature in vectors[0]:
        values = sorted({values[feature] for values in vectors})
        thresholds = [
            values[0] - 1,
            *[(left + right) / 2 for left, right in zip(values, values[1:])],
            values[-1] + 1,
        ]
        candidates.extend(
            {"feature": feature, "operator": operator, "threshold": threshold}
            for operator in ("<=", ">=")
            for threshold in thresholds
        )

    def rank(rule: dict) -> tuple:
        metrics = confusion(truth, [predict(rule, values) for values in vectors])
        return (
            metrics["weighted_loss_fn5_fp1"],
            metrics["fn"],
            metrics["high_detail_count"],
            rule["feature"] != "constant",
            json.dumps(rule, sort_keys=True),
        )

    return min(candidates, key=rank)


def hybrid_score(output: Path, selection: dict[str, bool], repeat: bool = False) -> dict:
    root = output / "repeat" if repeat else output
    records = []
    for detail in ("low", "high"):
        bulletins, missing = load_scored_bulletins(root / detail, output / "labels")
        if missing:
            raise ValueError(f"Incomplete predictions in {root / detail}")
        for bulletin in bulletins:
            if selection[bulletin["parish_slug"]] == (detail == "high"):
                records.extend(
                    match_events(bulletin["label"]["events"], bulletin["pred"]["events"])
                )
    return score_records(records)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    feature_data = json.loads((args.output / "features.json").read_text(encoding="utf-8"))
    reviews = json.loads((args.output / "manual_review.json").read_text(encoding="utf-8"))
    rows = sorted(feature_data["bulletins"], key=lambda row: row["parish_slug"])
    reviewed = {row["parish_slug"]: row for row in reviews["bulletins"]}
    cohort = json.loads((args.output / "cohort.json").read_text(encoding="utf-8"))
    expected = {(row["parish_slug"], row["content_hash"]) for row in cohort["bulletins"]}
    if {(row["parish_slug"], row["content_hash"]) for row in rows} != expected:
        raise ValueError("Feature identities do not match the frozen cohort")
    vectors = [vector(row["features"]) for row in rows]
    scan_predictions = [route_scan_risk(row["features"])["detail"] == "high" for row in rows]
    result = {
        "false_negative_weight": 5,
        "false_positive_weight": 1,
        "targets": {},
        "vectors": [
            {"parish_slug": row["parish_slug"], **values} for row, values in zip(rows, vectors)
        ],
    }
    result["feature_resolution_experiments"] = {}
    for name, experiment in feature_data.get("experiments", {}).items():
        decisions = {
            identity.split(":", 1)[0]: route_scan_risk(row["features"])
            for identity, row in experiment["bulletins"].items()
        }
        result["feature_resolution_experiments"][name] = {
            "settings": experiment["settings"],
            "current_rule_selected": sorted(
                slug for slug, decision in decisions.items() if decision["detail"] == "high"
            ),
            "current_rule_decisions": decisions,
            "previous_rule_selected": sorted(
                identity.split(":", 1)[0]
                for identity, decision in experiment["scan_risk_api_results"][
                    "routing_by_bulletin"
                ].items()
                if decision["detail"] == "high"
            ),
        }
    for target in ("observed_supported_advantage", "observed_raster_advantage"):
        truth = [reviewed[row["parish_slug"]][target] for row in rows]
        rule = fit_stump(vectors, truth)
        fitted = [predict(rule, values) for values in vectors]
        loo = []
        for held_out, values in enumerate(vectors):
            training = [index for index in range(len(rows)) if index != held_out]
            trained = fit_stump(
                [vectors[index] for index in training], [truth[index] for index in training]
            )
            loo.append(predict(trained, values))
        predictions = {
            "all_low": [False] * len(rows),
            "all_high": [True] * len(rows),
            "scan_risk": scan_predictions,
            "exploratory_native_and_raster": [
                row["default_routing"]["detail"] == "high" for row in rows
            ],
            "fitted_stump_in_sample": fitted,
            "fitted_stump_leave_one_out": loo,
        }
        result["targets"][target] = {
            "positives": [row["parish_slug"] for row, actual in zip(rows, truth) if actual],
            "fitted_stump": rule,
            "experiments": {
                name: {
                    **confusion(truth, chosen),
                    "selected": [row["parish_slug"] for row, high in zip(rows, chosen) if high],
                    "initial_hybrid": hybrid_score(
                        args.output, {row["parish_slug"]: high for row, high in zip(rows, chosen)}
                    ),
                    "repeat_hybrid": hybrid_score(
                        args.output,
                        {row["parish_slug"]: high for row, high in zip(rows, chosen)},
                        repeat=True,
                    ),
                }
                for name, chosen in predictions.items()
            },
        }
    write_json(args.output / "classification_experiments.json", result)
    print(
        json.dumps(
            {
                key: {
                    "positives": value["positives"],
                    "rule": value["fitted_stump"],
                    "metrics": {
                        name: {
                            metric: experiment[metric]
                            for metric in ("tp", "fn", "fp", "tn", "recall", "precision")
                        }
                        for name, experiment in value["experiments"].items()
                    },
                }
                for key, value in result["targets"].items()
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
