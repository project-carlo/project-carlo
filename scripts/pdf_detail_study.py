"""Reproduce a matched PDF-detail experiment without changing historical evals."""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import time
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from pdf_extract.__main__ import _load_dotenv
from pdf_extract.evals.report import CORE_FIELDS, build_report, render_markdown
from pdf_extract.evals.run import run

DEFAULT_COHORT = Path(
    "data/runs/gemini-3-flash-preview-qualified/eval/prompt-0c3297072125-0ada6e8be280"
)
DEFAULT_OUTPUT = Path("data/runs/pdf-detail-study/eval/2026-10-09")


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def prepare(cohort: Path, output: Path, parishes: list[str] | None = None) -> Path:
    labels = output / "labels"
    entries = []
    for prediction_path in sorted((cohort / "predictions").glob("*/*.json")):
        prediction = json.loads(prediction_path.read_text(encoding="utf-8"))
        slug, content_hash = prediction["parish_slug"], prediction["content_hash"]
        if parishes and slug not in parishes:
            continue
        source = Path("data/labels") / slug / f"{content_hash}.json"
        target = labels / slug / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        entries.append(
            {
                "parish_slug": slug,
                "content_hash": content_hash,
                "published_date": prediction.get("published_date"),
                "reference_date": prediction.get("today"),
                "source_url": prediction.get("source_url"),
            }
        )
    if not entries:
        raise ValueError(f"No predictions in {cohort}")
    write_json(output / "cohort.json", {"source_eval": str(cohort), "bulletins": entries})
    return labels


def event_key(event: dict) -> str:
    fields = (*CORE_FIELDS, "end_time", "weeks_of_month", "season")
    return json.dumps({key: event.get(key) for key in fields}, sort_keys=True)


def analyze(output: Path) -> None:
    reports = {
        detail: build_report(output / detail, output / "labels") for detail in ("low", "high")
    }
    indexed = {
        detail: {entry["parish_slug"]: entry for entry in report["bulletins"]}
        for detail, report in reports.items()
    }
    if set(indexed["low"]) != set(indexed["high"]):
        raise ValueError("Low/high predictions do not cover the same bulletin cohort")
    rows = []
    for slug in sorted(indexed["low"]):
        low = indexed["low"][slug]
        if low["content_hash"] != indexed["high"][slug]["content_hash"]:
            raise ValueError(f"Low/high PDF hashes differ for {slug}")
        predictions = {}
        for detail in ("low", "high"):
            path = output / detail / "predictions" / slug / f"{low['content_hash'][:12]}.json"
            predictions[detail] = json.loads(path.read_text(encoding="utf-8"))
        counters = {
            detail: Counter(event_key(event) for event in pred["events"])
            for detail, pred in predictions.items()
        }
        changes = {
            detail: [json.loads(key) for key in (counters[detail] - counters[other]).elements()]
            for detail, other in (("low", "high"), ("high", "low"))
        }
        rows.append(
            {
                "parish_slug": slug,
                "content_hash": low["content_hash"],
                "schedule_different": counters["low"] != counters["high"],
                "raw_events_different": predictions["low"]["events"]
                != predictions["high"]["events"],
                "low_only": changes["low"],
                "high_only": changes["high"],
                "scores": {
                    detail: {
                        key: indexed[detail][slug][key]
                        for key in ("levels", "outcomes", "spurious", "optional")
                    }
                    for detail in ("low", "high")
                },
            }
        )
    write_json(output / "comparison.json", rows)
    for row in rows:
        if row["schedule_different"]:
            print(
                row["parish_slug"],
                "low/high strict F1",
                *(
                    round(row["scores"][detail]["levels"]["strict"]["f1"], 4)
                    for detail in ("low", "high")
                ),
            )
            print("LOW ONLY", json.dumps(row["low_only"]))
            print("HIGH ONLY", json.dumps(row["high_only"]))


def extract_features(output: Path, dpi: float, max_render_pixels: int) -> None:
    from pdf_extract.pdf_detail import extract_pdf_features, route_pdf_detail, route_scan_risk

    cohort = json.loads((output / "cohort.json").read_text(encoding="utf-8"))
    started = time.monotonic()
    rows = []
    for bulletin in cohort["bulletins"]:
        slug, content_hash = bulletin["parish_slug"], bulletin["content_hash"]
        source = Path("data/bulletins") / slug / f"{content_hash}.pdf"
        measured = time.monotonic()
        features = extract_pdf_features(source, dpi=dpi, max_render_pixels=max_render_pixels)
        rows.append(
            {
                "parish_slug": slug,
                "content_hash": content_hash,
                "features": features,
                "default_routing": route_pdf_detail(features),
                "scan_routing": route_scan_risk(features),
                "elapsed_seconds": time.monotonic() - measured,
            }
        )
        logging.info("Measured %s in %.2fs", slug, rows[-1]["elapsed_seconds"])
    write_json(
        output / "features.json",
        {
            "settings": {"dpi": dpi, "max_render_pixels": max_render_pixels},
            "elapsed_seconds": time.monotonic() - started,
            "bulletins": rows,
        },
    )


def set_aside(output: Path) -> None:
    cohort = json.loads((output / "cohort.json").read_text(encoding="utf-8"))
    reviews = json.loads((output / "manual_review.json").read_text(encoding="utf-8"))
    identities = {row["parish_slug"]: row for row in cohort["bulletins"]}
    destination = Path("data/out/pdf-detail-study") / output.name
    manifest = []
    for review in reviews["bulletins"]:
        if not review["observed_supported_advantage"]:
            continue
        bulletin = identities[review["parish_slug"]]
        source = (
            Path("data/bulletins") / bulletin["parish_slug"] / (bulletin["content_hash"] + ".pdf")
        )
        category = (
            "raster-observed-gain"
            if review["observed_raster_advantage"]
            else ("native-semantic-observed-gain")
        )
        target = (
            destination
            / category
            / (bulletin["parish_slug"] + "-" + bulletin["content_hash"][:12] + ".pdf")
        )
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        manifest.append(
            {
                **bulletin,
                "category": category,
                "pdf_copy": target.as_posix(),
                "review": review["verdict"],
            }
        )
    write_json(
        output / "benefit_manifest.json",
        {
            "qualification": "Observed source-supported gains, not guaranteed repeatable benefits",
            "bulletins": manifest,
        },
    )
    print(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "run", "analyze", "features", "set-aside"])
    parser.add_argument("--detail", choices=["low", "high"], default="low")
    parser.add_argument("--cohort", type=Path, default=DEFAULT_COHORT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--parish", action="append", help="Prepare only these cohort parishes")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--dpi", type=float, default=100)
    parser.add_argument("--max-render-pixels", type=int, default=2000000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    _load_dotenv()
    if args.action == "features":
        extract_features(args.output, args.dpi, args.max_render_pixels)
        return
    if args.action == "set-aside":
        set_aside(args.output)
        return
    if args.action == "analyze":
        analyze(args.output)
        return
    if args.action == "prepare":
        print(prepare(args.cohort, args.output, args.parish))
        return
    labels = args.output / "labels"
    if not (args.output / "cohort.json").exists():
        raise ValueError("Run prepare first to freeze the matched labels")
    destination = args.output / args.detail
    with patch("pdf_extract.evals.run.eval_dir", return_value=destination):
        summary = run(
            classifier_name="gpt-6-luna",
            classifier_options={"reasoning_effort": "high", "file_detail": args.detail},
            concurrency=args.concurrency,
            refresh=args.refresh,
            labels_dir=labels,
        )
    report = build_report(destination, labels)
    write_json(destination / "report.json", report)
    (destination / "report.md").write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    if summary.get("errors") or summary.get("skipped"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
