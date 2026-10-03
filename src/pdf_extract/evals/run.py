"""Run a classifier over the labeled bulletins: `python -m pdf_extract eval run`.

The bulletins are the ones in data/labels/ (by default those marked done), and
each is classified as of the day it was fetched, so a bulletin labeled months
ago is not judged stale by the date in the prompt. Results go through the
shared result cache (see runner.py), keyed by classifier version, PDF and
church list: re-running the same version costs nothing, and a prompt, schema
or model change is a new version that gets fresh calls.

Output, under `data/runs/<classifier>/eval/<version>/`:

- `predictions/<parish_slug>/<content_hash[:12]>.json`: the classifier's output
  for one bulletin, with its events in the label's row shape (`event_type`,
  `event_kind`, 24-hour `HH:MM` times, `weeks_of_month`, `season`), so it lines
  up with `data/labels/<parish_slug>/<content_hash>.json` key for key. The file
  holds the full `content_hash`; its name is cut short, like `<version>`, to
  keep the path inside Windows' 260-character limit, as these are committed.
- `run.json`: what was run, cache hits, errors, token usage and timings.

Nothing here reads or writes the event table or `bulletin.processed_at`.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
import time
from collections.abc import Iterable
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Any

from pdf_extract.classifiers import Classifier, get_classifier
from pdf_extract.labeling.bulletins import find_bulletin, gemini_rows
from pdf_extract.labeling.labels import LABELS_DIR, is_valid_hash, is_valid_slug
from pdf_extract.runner import (
    ExtractFn,
    iter_extraction_outcomes,
    load_cached_result,
    run_dir,
    store_cached_result,
)
from pdf_extract.storage import DEFAULT_DB_PATH, churches_for_parish, connect_db, utc_now_iso

LOGGER = logging.getLogger(__name__)

DEFAULT_STATUSES = ("done",)


# Characters of the content hash a prediction file is named by.
PREDICTION_HASH_CHARS = 12
# Longest readable part of a version directory's name (a digest follows it).
_VERSION_DIR_CHARS = 56
# The prompt fingerprint the classifiers end their versions with; the digest covers it.
_PROMPT_PART = re.compile(r"\+prompt-[0-9A-Za-z]+")


def version_dir_name(classifier_name: str, version: str) -> str:
    """A short directory name for one classifier version.

    The model is dropped when the classifier is named after it (the directory
    above already says it) and so is the prompt fingerprint; the digest of the
    whole version keeps every version apart. `gpt-6-luna+strict+reasoning-medium+
    detail-low+prompt-ebbd...` becomes `strict_reasoning-medium_detail-low-<digest>`.
    """
    model, sep, rest = version.partition("+")
    readable = rest if sep and classifier_name.startswith(model) else version
    readable = _PROMPT_PART.sub("", readable)
    readable = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in readable)
    readable = readable.strip("_.-")[:_VERSION_DIR_CHARS] or "default"
    return f"{readable}-{sha256(version.encode('utf-8')).hexdigest()[:12]}"


def eval_dir(classifier: Classifier) -> Path:
    """Where one classifier version's evaluation output lives."""
    return run_dir(classifier.name) / "eval" / version_dir_name(classifier.name, classifier.version)


def prediction_path(out_dir: Path, parish_slug: str, content_hash: str) -> Path:
    return out_dir / "predictions" / parish_slug / f"{content_hash[:PREDICTION_HASH_CHARS]}.json"


# ── Selecting the labeled bulletins ─────────────────────────────────────────
def labeled_bulletins(
    labels_dir: Path = LABELS_DIR,
    *,
    statuses: Iterable[str] = DEFAULT_STATUSES,
    parish_slug: str | None = None,
) -> list[dict[str, Any]]:
    """Every label with one of `statuses`, as bulletin entries, in a stable order."""
    wanted = set(statuses)
    out: list[dict[str, Any]] = []
    for path in sorted(labels_dir.glob("*/*.json")):
        slug, content_hash = path.parent.name, path.stem
        if not (is_valid_slug(slug) and is_valid_hash(content_hash)):
            continue
        if parish_slug is not None and slug != parish_slug:
            continue
        try:
            label = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            LOGGER.warning("Skipping unreadable label %s", path)
            continue
        if not isinstance(label, dict) or label.get("status") not in wanted:
            continue
        out.append({
            "parish_slug": slug,
            "content_hash": content_hash,
            "source_url": label.get("source_url"),
            "label_status": label["status"],
        })
    return out


def _reference_date(entry: dict[str, Any]) -> date:
    """The day the bulletin was fetched: "today" as production would have seen it."""
    fetched_at = entry.get("fetched_at")
    if isinstance(fetched_at, str):
        try:
            return date.fromisoformat(fetched_at[:10])
        except ValueError:
            pass
    LOGGER.warning("No fetch date for %s; using today", entry.get("source_url"))
    return date.today()


def _attach_bulletin(conn: sqlite3.Connection, entry: dict[str, Any]) -> bool:
    """Fill in the bulletin's fetch date (and source URL) from the database."""
    row = find_bulletin(conn, entry["parish_slug"], entry["content_hash"])
    if row is None:
        return False
    entry["fetched_at"] = row["fetched_at"]
    entry["source_url"] = entry.get("source_url") or row["source_url"]
    return True


def _timed(extract: ExtractFn) -> ExtractFn:
    """`extract`, with the call's wall time recorded on the result."""
    def call(*args: Any, **kwargs: Any) -> dict[str, Any]:
        started = time.monotonic()
        result = extract(*args, **kwargs)
        return {**result, "seconds": round(time.monotonic() - started, 3)}
    return call


# ── Output ──────────────────────────────────────────────────────────────────
def prediction(
    classifier: Classifier, entry: dict[str, Any], result: dict[str, Any], *, from_cache: bool,
) -> dict[str, Any]:
    """One bulletin's classifier output, with events in the label's row shape."""
    events = []
    for row in gemini_rows(result.get("events") or []):
        row.pop("id", None)
        events.append(row)
    return {
        "classifier": classifier.name,
        "classifier_version": classifier.version,
        "parish_slug": entry["parish_slug"],
        "content_hash": entry["content_hash"],
        "source_url": entry.get("source_url"),
        "label_status": entry.get("label_status"),
        "today": _reference_date(entry).isoformat(),
        "from_cache": from_cache,
        "published_date": result.get("published_date"),
        "wrong_bulletin": bool(result.get("wrong_bulletin", False)),
        "church_list_needs_review": bool(result.get("church_list_needs_review", False)),
        "usage": result.get("usage") or {},
        "seconds": result.get("seconds"),
        "response_id": result.get("response_id"),
        "events": events,
    }


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _sum_usage(results: Iterable[dict[str, Any]]) -> dict[str, int]:
    total: dict[str, int] = {}
    for result in results:
        for key, value in (result.get("usage") or {}).items():
            if isinstance(value, int):
                total[key] = total.get(key, 0) + value
    return total


# ── Main entry point ────────────────────────────────────────────────────────
def run(
    *,
    classifier_name: str,
    statuses: Iterable[str] = DEFAULT_STATUSES,
    parish_slug: str | None = None,
    limit: int | None = None,
    concurrency: int = 5,
    refresh: bool = False,
    classifier_options: dict[str, Any] | None = None,
    labels_dir: Path = LABELS_DIR,
    db_path: Path = DEFAULT_DB_PATH,
) -> dict[str, Any]:
    """Classify every selected labeled bulletin and write the predictions.

    `classifier_options` (reasoning effort, detail level, ...) are passed to the
    classifier's factory; they are part of its version, so each combination gets
    its own cache entries and output directory.
    """
    classifier = get_classifier(classifier_name, **(classifier_options or {}))
    statuses = tuple(statuses)
    entries = labeled_bulletins(labels_dir, statuses=statuses, parish_slug=parish_slug)
    if limit is not None:
        entries = entries[:limit]
    out_dir = eval_dir(classifier)
    LOGGER.info(
        "Eval run: classifier=%s version=%s bulletins=%d out=%s",
        classifier.name, classifier.version, len(entries), out_dir,
    )

    started = time.monotonic()
    served: dict[tuple[str, str], tuple[dict[str, Any], dict[str, Any], bool]] = {}
    fresh: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    errors: list[dict[str, str]] = []

    conn = connect_db(db_path)
    try:
        pending: list[dict[str, Any]] = []
        for entry in entries:
            if not _attach_bulletin(conn, entry):
                LOGGER.warning(
                    "Skipping %s/%s: no such bulletin in the database",
                    entry["parish_slug"], entry["content_hash"],
                )
                skipped.append({**_ident(entry), "reason": "bulletin not in database"})
                continue
            churches = churches_for_parish(conn, entry["parish_slug"])
            cached = None if refresh else load_cached_result(
                classifier.name, classifier.version, entry["content_hash"], churches,
            )
            if cached is not None:
                served[_key(entry)] = (entry, cached, True)
            else:
                pending.append(entry)

        for outcome in iter_extraction_outcomes(
            pending, conn, _timed(classifier.extract),
            concurrency=concurrency, today_for=_reference_date,
        ):
            entry = outcome.entry
            if outcome.skipped:
                skipped.append({**_ident(entry), "reason": "PDF or parish unavailable"})
            elif outcome.extracted is None:
                errors.append({**_ident(entry), "error": repr(outcome.error)})
            else:
                store_cached_result(
                    classifier.name, classifier.version, entry["content_hash"],
                    churches_for_parish(conn, entry["parish_slug"]), outcome.extracted,
                )
                served[_key(entry)] = (entry, outcome.extracted, False)
                fresh.append(outcome.extracted)
                LOGGER.info(
                    "Classified %s/%s: %d events in %.1fs",
                    entry["parish_slug"], entry["content_hash"][:12],
                    len(outcome.extracted.get("events") or []),
                    outcome.extracted.get("seconds") or 0,
                )
    finally:
        conn.close()

    events_written = 0
    for entry, result, from_cache in served.values():
        pred = prediction(classifier, entry, result, from_cache=from_cache)
        events_written += len(pred["events"])
        _write_json(
            prediction_path(out_dir, entry["parish_slug"], entry["content_hash"]),
            pred,
        )

    summary = {
        "classifier": classifier.name,
        "classifier_version": classifier.version,
        "ran_at": utc_now_iso(),
        "out_dir": out_dir.as_posix(),
        "label_statuses": list(statuses),
        "parish": parish_slug,
        "bulletins_selected": len(entries),
        "bulletins_served": len(served),
        "cache_hits": len(served) - len(fresh),
        "classifier_calls": len(fresh),
        "skipped": skipped,
        "errors": errors,
        "events_written": events_written,
        "usage_new_calls": _sum_usage(fresh),
        "usage_all_served": _sum_usage(result for _, result, _ in served.values()),
        "wall_seconds": round(time.monotonic() - started, 3),
    }
    _write_json(out_dir / "run.json", summary)
    LOGGER.info("Eval run finished: %s", summary)
    return summary


def _key(entry: dict[str, Any]) -> tuple[str, str]:
    return entry["parish_slug"], entry["content_hash"]


def _ident(entry: dict[str, Any]) -> dict[str, str]:
    return {"parish_slug": entry["parish_slug"], "content_hash": entry["content_hash"]}
