"""Matched low/high PDF-detail calls on all available raw-Gemini-backed bulletins."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import logging
import re
import shutil
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

from pdf_detail_study import event_key, write_json

from pdf_extract.__main__ import _load_dotenv
from pdf_extract.blobstore import get_store
from pdf_extract.classifiers import get_classifier
from pdf_extract.evals.report import build_report, render_markdown
from pdf_extract.evals.run import prediction
from pdf_extract.labeling.bulletins import gemini_rows
from pdf_extract.runner import _churches_fingerprint
from pdf_extract.storage import churches_for_parish, connect_db, read_bulletin_pdf, utc_now_iso

DEFAULT_OUTPUT = Path("data/runs/pdf-detail-full/eval/2026-10-09")
WORK_ROOT = Path("data/out/pdf-detail-followup")
HASH = re.compile(r"^[0-9a-f]{64}$")


def ident(row: dict) -> tuple[str, str]:
    return row["parish_slug"], row["content_hash"]


def pred_path(root: Path, row: dict) -> Path:
    return root / "predictions" / row["parish_slug"] / f"{row['content_hash'][:12]}.json"


def prepare(output: Path, concurrency: int) -> None:
    if (output / "cohort.json").exists():
        raise FileExistsError("Cohort already frozen; use a new output directory")
    store = get_store()
    if not store.remote:
        raise ValueError("Remote credentials required to discover the latest published data")
    latest = json.loads(store.get_remote("pipeline/latest.json"))
    compressed = store.get_remote(latest["db_key"])
    if hashlib.sha256(compressed).hexdigest() != latest["db_sha256"]:
        raise ValueError("Published database checksum mismatch")
    workspace = WORK_ROOT / output.name
    workspace.mkdir(parents=True, exist_ok=True)
    database = workspace / "reference.db"
    database.write_bytes(gzip.decompress(compressed))
    write_json(output / "published_manifest.json", latest)
    remote_objects = []
    paginator = store.remote.client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=store.remote.bucket, Prefix="runs/gemini-flash/cache/"):
        for obj in page.get("Contents", []):
            remote_objects.append(
                {"key": obj["Key"], "modified_at": obj["LastModified"].isoformat()}
            )
    write_json(output / "remote_gemini_objects.json", remote_objects)
    candidates = {}
    for obj in remote_objects:
        content_hash = obj["key"].rsplit("/", 1)[-1][:64]
        if HASH.fullmatch(content_hash):
            old = candidates.get(content_hash)
            if old is None or obj["modified_at"] > old["modified_at"]:
                candidates[content_hash] = {**obj, "kind": "remote_raw_cache"}
    for path in sorted(Path("data/runs/gemini-flash/cache").rglob("*.json")):
        content_hash = path.name[:64]
        if not HASH.fullmatch(content_hash) or content_hash in candidates:
            continue
        candidates[content_hash] = {
            "key": path.relative_to("data").as_posix(),
            "kind": "local_legacy_raw_cache",
            "modified_at": None,
            "timestamp_caveat": "Local mtime is not an extraction timestamp; legacy fallback only",
        }
    qualified = {}
    for run_path in Path("data/runs/gemini-3-flash-preview-qualified/eval").glob("*/run.json"):
        run = json.loads(run_path.read_text(encoding="utf-8"))
        for path in (run_path.parent / "predictions").glob("*/*.json"):
            result = json.loads(path.read_text(encoding="utf-8"))
            key = ident(result)
            old = qualified.get(key)
            if old is None or run["ran_at"] > old["ran_at"]:
                qualified[key] = {
                    "path": path.as_posix(),
                    "ran_at": run["ran_at"],
                    "result": result,
                }
    conn = connect_db(database)
    try:
        observed = {}
        for row in conn.execute(
            "SELECT b.*,p.slug AS parish_slug FROM bulletin b JOIN parish p ON p.id=b.parish_id "
            "WHERE b.content_hash IS NOT NULL ORDER BY b.fetched_at DESC,b.id DESC"
        ):
            observed.setdefault((row["parish_slug"], row["content_hash"]), dict(row))
        for key, source in qualified.items():
            if key not in observed:
                result = source["result"]
                observed[key] = {
                    "parish_slug": key[0],
                    "content_hash": key[1],
                    "source_url": result.get("source_url"),
                    "fetched_at": result["today"] + "T00:00:00Z",
                    "reference_date_provenance": "Historical qualified prediction today",
                }
        entries = []
        excluded = []
        for key, row in sorted(observed.items()):
            candidate = candidates.get(row["content_hash"])
            if candidate is None and key in qualified:
                candidate = {
                    "kind": "qualified_eval",
                    "key": qualified[key]["path"],
                    "modified_at": qualified[key]["ran_at"],
                }
            if candidate is None:
                excluded.append(
                    {
                        "parish_slug": key[0],
                        "content_hash": key[1],
                        "reason": "No recoverable raw Gemini result",
                    }
                )
                continue
            churches = churches_for_parish(conn, row["parish_slug"])
            entries.append(
                {
                    "parish_slug": row["parish_slug"],
                    "content_hash": row["content_hash"],
                    "source_url": row["source_url"],
                    "fetched_at": row["fetched_at"],
                    "reference_date": row["fetched_at"][:10],
                    "churches": churches,
                    "gemini_source": candidate,
                    "gemini_church_context_matches": (
                        candidate["key"].rsplit("-", 1)[-1].removesuffix(".json")
                        == _churches_fingerprint(churches)
                    )
                    if "-" in candidate["key"].rsplit("/", 1)[-1]
                    else None,
                }
            )
    finally:
        conn.close()

    def freeze(entry: dict) -> dict:
        content_hash, slug = entry["content_hash"], entry["parish_slug"]
        source = entry["gemini_source"]
        if source["kind"] == "qualified_eval":
            raw = Path(source["key"]).read_bytes()
        else:
            raw = (
                store.get_remote(source["key"])
                if source["kind"] == "remote_raw_cache"
                else store.get(source["key"])
            )
        if raw is None:
            raise FileNotFoundError(source["key"])
        baseline = json.loads(raw)
        baseline_events = (
            baseline["events"]
            if source["kind"] == "qualified_eval"
            else gemini_rows(baseline.get("events") or [])
        )
        newer = qualified.get(ident(entry))
        stored_at = source.get("modified_at") or ""
        if newer and newer["ran_at"][:19] > stored_at[:19]:
            baseline = newer["result"]
            baseline_events = baseline["events"]
            source = {"kind": "qualified_eval", "path": newer["path"], "ran_at": newer["ran_at"]}
        pdf = read_bulletin_pdf(slug, content_hash)
        if pdf is None:
            raise FileNotFoundError(f"No readable PDF: {slug}/{content_hash}")
        pdf_path = workspace / "pdfs" / slug / f"{content_hash[:12]}.pdf"
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(pdf)
        label = Path("data/labels") / slug / f"{content_hash}.json"
        label_status = "unlabeled"
        if label.exists():
            label_status = json.loads(label.read_text(encoding="utf-8")).get("status", "unlabeled")
            target = output / "labels" / slug / label.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(label, target)
        complete = {
            **entry,
            "pdf_path": pdf_path.as_posix(),
            "pdf_sha256": hashlib.sha256(pdf).hexdigest(),
            "label_status": label_status,
            "gemini_source": source,
        }
        for event in baseline_events:
            event.pop("id", None)
        write_json(
            pred_path(output / "gemini", complete),
            {
                "classifier": "latest-recorded-gemini",
                **complete,
                "published_date": baseline.get("published_date"),
                "wrong_bulletin": bool(baseline.get("wrong_bulletin", False)),
                "events": baseline_events,
                "usage": baseline.get("usage") or {},
            },
        )
        return complete

    complete = []
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        pending = {pool.submit(freeze, entry): entry for entry in entries}
        for future in as_completed(pending):
            entry = pending[future]
            try:
                complete.append(future.result())
            except Exception as exc:
                excluded.append({**entry, "reason": f"Freeze failed: {type(exc).__name__}: {exc}"})
            if (len(complete) + len(excluded)) % 25 == 0:
                logging.info("Frozen %d/%d", len(complete), len(entries))
    complete.sort(key=ident)
    write_json(
        output / "cohort.json",
        {
            "created_at": utc_now_iso(),
            "published_run": latest["run_id"],
            "selection": "All distinct parish/PDF identities with a recoverable raw Gemini result and readable available PDF; no label-status or latest-per-parish filtering",
            "latest_caveat": "Caches lack execution timestamps. Remote LastModified selects most recently stored raw results; later timestamped qualified evals supersede them. Local legacy results are fallback only.",
            "bulletins": complete,
        },
    )
    write_json(output / "excluded.json", excluded)
    print(
        json.dumps(
            {
                "selected": len(complete),
                "parishes": len({r["parish_slug"] for r in complete}),
                "excluded": len(excluded),
            },
            indent=2,
        )
    )


def run_calls(output: Path, detail: str, trial: str, concurrency: int, limit: int | None) -> None:
    cohort = json.loads((output / "cohort.json").read_text(encoding="utf-8"))["bulletins"]
    if limit is not None:
        cohort = cohort[:limit]
    classifier = get_classifier("gpt-6-luna", reasoning_effort="high", file_detail=detail)
    destination = output / trial / detail
    classifier._openai()
    started = time.monotonic()
    resumed = 0
    pending = []
    errors = []
    for entry in cohort:
        path = pred_path(destination, entry)
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8"))
            if (
                ident(existing) != ident(entry)
                or existing["classifier_version"] != classifier.version
            ):
                raise ValueError(f"Existing prediction identity/settings mismatch: {path}")
            resumed += 1
        else:
            pending.append(entry)

    def extract(entry: dict) -> dict:
        pdf = Path(entry["pdf_path"]).read_bytes()
        if hashlib.sha256(pdf).hexdigest() != entry["pdf_sha256"]:
            raise ValueError("Frozen PDF checksum mismatch")
        call_started = time.monotonic()
        result = classifier.extract(
            pdf, churches=entry["churches"], today=date.fromisoformat(entry["reference_date"])
        )
        result["seconds"] = round(time.monotonic() - call_started, 3)
        pred = prediction(classifier, entry, result, from_cache=False)
        pred["pdf_sha256"] = entry["pdf_sha256"]
        write_json(pred_path(destination, entry), pred)
        return pred

    done = 0
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(extract, entry): entry for entry in pending}
        for future in as_completed(futures):
            entry = futures[future]
            try:
                pred = future.result()
                done += 1
                logging.info(
                    "%s %s %d/%d %s/%s: %d events %.1fs",
                    trial,
                    detail,
                    done,
                    len(pending),
                    entry["parish_slug"],
                    entry["content_hash"][:12],
                    len(pred["events"]),
                    pred["seconds"],
                )
            except Exception as exc:
                errors.append(
                    {
                        "parish_slug": entry["parish_slug"],
                        "content_hash": entry["content_hash"],
                        "error": str(exc),
                    }
                )
                logging.exception("Failed %s/%s", *ident(entry))
    usage = Counter()
    for entry in cohort:
        path = pred_path(destination, entry)
        if path.exists():
            pred = json.loads(path.read_text(encoding="utf-8"))
            usage.update(
                {key: value for key, value in pred["usage"].items() if isinstance(value, int)}
            )
    write_json(
        destination / "run.json",
        {
            "classifier": classifier.name,
            "classifier_version": classifier.version,
            "ran_at": utc_now_iso(),
            "selected": len(cohort),
            "new_calls": done,
            "resumed": resumed,
            "served": done + resumed,
            "errors": errors,
            "usage": dict(usage),
            "wall_seconds": time.monotonic() - started,
        },
    )
    if (output / "labels").exists():
        report = build_report(destination, output / "labels")
        write_json(destination / "labeled_subset_report.json", report)
        (destination / "labeled_subset_report.md").write_text(
            render_markdown(report), encoding="utf-8"
        )
    if errors:
        raise SystemExit(1)


def compare(output: Path, trial: str, allow_partial: bool = False) -> None:
    cohort = json.loads((output / "cohort.json").read_text(encoding="utf-8"))["bulletins"]
    rows = []
    for entry in cohort:
        paths = {detail: pred_path(output / trial / detail, entry) for detail in ("low", "high")}
        if allow_partial and not all(path.exists() for path in paths.values()):
            continue
        predictions = {
            detail: json.loads(
                pred_path(output / trial / detail, entry).read_text(encoding="utf-8")
            )
            for detail in ("low", "high")
        }
        counters = {
            detail: Counter(map(event_key, result["events"]))
            for detail, result in predictions.items()
        }
        different = counters["low"] != counters["high"]
        metadata = {
            key: {detail: predictions[detail].get(key) for detail in ("low", "high")}
            for key in ("wrong_bulletin", "published_date")
            if predictions["low"].get(key) != predictions["high"].get(key)
        }
        rows.append(
            {
                "parish_slug": entry["parish_slug"],
                "content_hash": entry["content_hash"],
                "schedule_different": different,
                "metadata_differences": metadata,
                "review_needed": different or bool(metadata),
                "low_only": [
                    json.loads(key) for key in (counters["low"] - counters["high"]).elements()
                ],
                "high_only": [
                    json.loads(key) for key in (counters["high"] - counters["low"]).elements()
                ],
            }
        )
    write_json(
        output / trial / ("partial_comparison.json" if allow_partial else "comparison.json"), rows
    )
    print(
        json.dumps(
            {
                "cohort": len(rows),
                "schedule_differences": sum(r["schedule_different"] for r in rows),
                "review_needed": sum(r["review_needed"] for r in rows),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "run", "compare"])
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--detail", choices=["low", "high"], default="low")
    parser.add_argument("--trial", default="initial")
    parser.add_argument("--concurrency", type=int, default=8)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    _load_dotenv()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if args.action == "prepare":
        prepare(args.output, args.concurrency)
    elif args.action == "run":
        run_calls(args.output, args.detail, args.trial, args.concurrency, args.limit)
    else:
        compare(args.output, args.trial, args.allow_partial)


if __name__ == "__main__":
    main()
