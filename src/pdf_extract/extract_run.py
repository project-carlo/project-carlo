"""Experimental classifier runner: runs a registered classifier against the
fetched bulletin corpus and writes its outputs to data/runs/<classifier>/.

Independent of the production process.py bookkeeping:
- does not consult or update `bulletin.processed_at`
- does not write events to the database
- does not touch the SQLite parish_events.db beyond reads

It shares the on-disk result cache with the production path (see runner.py):
each classifier output is keyed by (classifier name + version, bulletin
content_hash). A cache hit means zero classifier calls on re-run.
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import bulletin_pdf_key
from pdf_extract.classifiers import Classifier, get_classifier
from pdf_extract.paths import DATA_DIR
from pdf_extract.runner import (
    flatten_extracted_events,
    iter_extraction_outcomes,
    latest_per_parish,
    load_cached_result,
    run_dir,
    store_cached_result,
)
from pdf_extract.storage import (
    churches_for_parish,
    connect_db,
    get_parish_by_name,
    load_bulletins,
    save_json_list,
    utc_now_iso,
)

LOGGER = logging.getLogger(__name__)


# ── On-disk layout ──────────────────────────────────────────────────────────
def events_path(classifier_name: str) -> Path:
    return run_dir(classifier_name) / "events.json"


def bulletins_path(classifier_name: str) -> Path:
    return run_dir(classifier_name) / "bulletins.json"


def run_summary_path(classifier_name: str) -> Path:
    return run_dir(classifier_name) / "run.json"


# ── Main entry point ────────────────────────────────────────────────────────
def run(
    *,
    classifier_name: str | None = None,
    classifier: Classifier | None = None,
    parish_name: str | None = None,
    concurrency: int = 5,
    source_urls: set[str] | None = None,
    bulletins: set[tuple[str, str]] | None = None,
    cache_only: bool = False,
    today_for: Callable[[dict[str, Any]], date | None] | None = None,
    undated_fallback: bool = False,
) -> dict[str, Any]:
    """Run a classifier over the fetched bulletin corpus.

    Re-uses cached classifier outputs keyed by (classifier+version, content_hash).
    Always rebuilds the run's events.json from the cache so it stays in sync.

    Pass a registered `classifier_name`, or a configured `classifier` instance.
    `source_urls` limits the run to those bulletins. `bulletins` instead picks
    exactly these (parish slug, content hash) PDFs, latest or not (the labeled
    bulletins of a ground-truth benchmark); `cache_only` serves cached
    results and skips the rest instead of calling the classifier (the benchmark
    reads the Gemini baseline this way, from what the weekly job already paid for).

    `today_for` gives each bulletin the date the classifier is told is today
    (None: the real date), and results made that way are cached under it. With
    `undated_fallback`, a bulletin with no result for its date is served one
    extracted on the day it ran, if there is one (the weekly job's Gemini
    results, extracted the week each bulletin was fetched). The manifest
    records the date each served result was extracted as of, when set.
    """
    if classifier is None:
        if classifier_name is None:
            raise ValueError("Pass classifier_name or classifier")
        classifier = get_classifier(classifier_name)
    LOGGER.info(
        "Starting extract run (classifier=%s version=%s parish=%s concurrency=%s)",
        classifier.name,
        classifier.version,
        parish_name or "*all*",
        concurrency,
    )

    started = time.monotonic()
    cache_hits = 0
    cache_misses = 0
    skipped = 0
    errors: list[dict[str, str]] = []
    cached_results: dict[str, dict[str, Any]] = {}  # source_url -> classifier output
    fresh_urls: set[str] = set()  # results paid for in this run
    served_as_of: dict[str, date | None] = {}  # source_url -> the "today" it was extracted as of

    conn = connect_db()
    try:
        if bulletins is None:
            candidates = latest_per_parish(load_bulletins(conn))
        else:
            candidates = _pick_bulletins(load_bulletins(conn), bulletins)
        if parish_name:
            parish_row = get_parish_by_name(conn, parish_name)
            if not parish_row:
                LOGGER.warning("Parish not found: %s", parish_name)
                return _summary(classifier)
            target_slug = parish_row["slug"]
            candidates = [m for m in candidates if m["parish_slug"] == target_slug]
        if source_urls is not None:
            candidates = [m for m in candidates if m["source_url"] in source_urls]

        # Pass 1: serve everything we already have cached, build the work list.
        pending: list[dict[str, Any]] = []
        for entry in candidates:
            content_hash = entry.get("content_hash")
            if not isinstance(content_hash, str) or not content_hash:
                LOGGER.warning(
                    "Skipping bulletin without content_hash: %s",
                    entry.get("source_url"),
                )
                skipped += 1
                continue
            churches = churches_for_parish(conn, entry["parish_slug"])
            today = today_for(entry) if today_for else None
            cached = load_cached_result(
                classifier.name, classifier.version, content_hash, churches, today,
            )
            if cached is None and today is not None and undated_fallback:
                cached = load_cached_result(
                    classifier.name, classifier.version, content_hash, churches,
                )
                today = None
            served_as_of[entry["source_url"]] = today
            if cached is not None:
                cached_results[entry["source_url"]] = cached
                cache_hits += 1
            elif cache_only:
                skipped += 1
            else:
                pending.append(entry)

        # Pass 2: run the classifier on cache misses, with bounded concurrency.
        for outcome in iter_extraction_outcomes(
            pending, conn, classifier.extract, concurrency=concurrency, today_for=today_for,
        ):
            if outcome.skipped:
                skipped += 1
                continue
            if outcome.extracted is None:
                errors.append(
                    {
                        "source_url": str(outcome.entry.get("source_url")),
                        "error": repr(outcome.error),
                    }
                )
                continue
            store_cached_result(
                classifier.name,
                classifier.version,
                outcome.entry["content_hash"],
                churches_for_parish(conn, outcome.entry["parish_slug"]),
                outcome.extracted,
                today_for(outcome.entry) if today_for else None,
            )
            served_as_of[outcome.entry["source_url"]] = (
                today_for(outcome.entry) if today_for else None
            )
            cached_results[outcome.entry["source_url"]] = outcome.extracted
            fresh_urls.add(outcome.entry["source_url"])
            cache_misses += 1
    finally:
        conn.close()

    # Rebuild events.json from the (now-current) cache for every served bulletin.
    events: list[dict[str, Any]] = []
    served_bulletins: list[dict[str, Any]] = []
    for entry in candidates:
        result = cached_results.get(entry["source_url"])
        if result is None:
            continue
        rows = flatten_extracted_events(entry, result)
        events.extend(rows)
        row = {
            "bulletin_source_url": entry["source_url"],
            "pdf_path": (
                DATA_DIR / bulletin_pdf_key(entry["parish_slug"], entry["content_hash"])
            ).as_posix(),
            "parish_slug": entry.get("parish_slug")
            if isinstance(entry.get("parish_slug"), str)
            else None,
            "published_date": (
                entry.get("published_date")
                if isinstance(entry.get("published_date"), str)
                else None
            ),
            "content_hash": entry["content_hash"],
            "event_count": len(rows),
            "wrong_bulletin": bool(result.get("wrong_bulletin")),
            "published_date_extracted": result.get("published_date"),
            "cache_hit": entry["source_url"] not in fresh_urls,
            "usage": result.get("usage") or {},
            "timing": result.get("timing") or {},
            "text_chars": result.get("text_chars"),
        }
        if today_for:
            as_of = served_as_of.get(entry["source_url"])
            row["extracted_as_of"] = as_of.isoformat() if as_of else None
        served_bulletins.append(row)

    save_json_list(events_path(classifier.name), events)
    save_json_list(bulletins_path(classifier.name), served_bulletins)

    summary = _summary(
        classifier,
        bulletins_total=len(candidates),
        bulletins_served=len(cached_results),
        cache_hits=cache_hits,
        cache_misses=cache_misses,
        skipped=skipped,
        errors=errors,
        events_written=len(events),
        usage_total=_sum_usage(served_bulletins),
        wall_seconds=round(time.monotonic() - started, 3),
    )

    summary_path = run_summary_path(classifier.name)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    LOGGER.info("Extract run finished: %s", summary)
    return summary


def _pick_bulletins(
    rows: list[dict[str, Any]], wanted: set[tuple[str, str]],
) -> list[dict[str, Any]]:
    """One bulletin row per wanted (parish slug, content hash): the latest fetched.

    A PDF fetched under two URLs is one bulletin; its latest row stands for it.
    """
    picked: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (row.get("parish_slug"), row.get("content_hash"))
        if key not in wanted:
            continue
        current = picked.get(key)
        if current is None or str(row.get("fetched_at") or "") >= str(current.get("fetched_at") or ""):
            picked[key] = row
    return list(picked.values())


def _summary(classifier: Classifier, **counters: Any) -> dict[str, Any]:
    """A run summary: every field at its zero value, overridden by `counters`.

    The early return for an unknown parish and the end of a real run both build
    their summary here, so the two cannot come to disagree about the keys.
    """
    return {
        "classifier": classifier.name,
        "classifier_version": classifier.version,
        "ran_at": utc_now_iso(),
        "bulletins_total": 0,
        "bulletins_served": 0,
        "cache_hits": 0,
        "cache_misses": 0,
        "skipped": 0,
        "errors": [],
        "events_written": 0,
        "usage_total": {},
        "wall_seconds": 0.0,
    } | counters


def _sum_usage(bulletins: list[dict[str, Any]]) -> dict[str, int]:
    """Token counts summed over every served bulletin, cached or not.

    Cached results carry the usage of the call that produced them, so this is
    what the run would cost from scratch, comparable across classifiers.
    """
    totals: dict[str, int] = {}
    for row in bulletins:
        for key, value in (row.get("usage") or {}).items():
            if isinstance(value, int):
                totals[key] = totals.get(key, 0) + value
    return totals
