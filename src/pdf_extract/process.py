"""Bulletin process pipeline: extract schedules from PDFs with Gemini AI.

Runs the production Gemini classifier over each parish's latest fetched
bulletin. `bulletin.processed_at` is the gate that keeps a bulletin from being
re-extracted; the shared result cache in the blob store (keyed by classifier
version + bulletin content hash) is a second layer that lets a re-run skip the
API call.

Each bulletin's events are stored against that bulletin; superseded
bulletins keep theirs, and the frontend reads only each parish's latest (see
`storage.latest_bulletin_order`). Every occurrence is also recorded in the
`event_occurrence` table before weekly promotion can rewrite it; that history
is what lets `pdf_extract.recurrence` recognise a "one-off" the bulletins have
in fact been printing every week.
"""

from __future__ import annotations

import logging
from typing import Any

from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.recurrence import (
    History,
    bulletin_reference_date,
    load_history_from_db,
    promote_recurring_events,
    prune_history,
    record_observations,
    save_history_to_db,
)
from pdf_extract.runner import (
    flatten_extracted_events,
    iter_extraction_outcomes,
    latest_per_parish,
    load_cached_result,
    store_cached_result,
)
from pdf_extract.runs import (
    PROCESS_CACHED,
    PROCESS_EXTRACTED,
    PROCESS_FAILED,
    PROCESS_SKIPPED,
    PROCESS_WRONG_BULLETIN,
    record_parish_result,
)
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.storage import (
    churches_for_parish,
    connect_db,
    get_parish_by_name,
    load_bulletins,
    save_processed_bulletin,
    utc_now_iso,
)

LOGGER = logging.getLogger(__name__)


def _prepare_rows(
    entry: dict[str, Any],
    extracted: dict[str, Any],
    history: History,
) -> tuple[list[dict[str, Any]], int]:
    """Turn one extracted result into the rows to store for its bulletin.

    Occurrences are recorded in `history` (in place) before promotion, so the
    raw sighting survives even when the row itself is rewritten as weekly.

    Returns the rows and the number promoted to weekly.
    """
    parish_slug = entry["parish_slug"]
    if extracted.get("wrong_bulletin"):
        LOGGER.warning(
            "Bulletin flagged as wrong PDF for parish %s (source=%s); skipping events",
            parish_slug, entry.get("source_url"),
        )
    published_date = extracted.get("published_date")
    if isinstance(published_date, str) and published_date.strip():
        entry["published_date"] = published_date

    rows = flatten_extracted_events(entry, extracted)
    # Recorded before promotion: a promoted row loses its date, and the raw
    # sighting is what keeps next week's chain going.
    record_observations(history, rows, bulletin_date=bulletin_reference_date(entry))
    rows, promoted = promote_recurring_events(rows, history)

    if extracted.get("church_list_needs_review"):
        LOGGER.warning(
            "Church list may need review for parish %s — run 'pnpm verify --parish \"%s\"'",
            parish_slug, parish_slug,
        )
    return rows, promoted


def process_bulletins(
    *,
    parish_name: str | None = None,
    model: str = DEFAULT_GEMINI_MODEL,
    concurrency: int = 5,
    run_id: str | None = None,
) -> dict[str, int]:
    LOGGER.info(
        "Starting process stage (parish_name=%s, model=%s, concurrency=%s)",
        parish_name or "*all*", model, concurrency,
    )
    classifier = GeminiClassifier(model=model)

    processed_count = 0
    inserted_events = 0
    skipped_events = 0
    cache_hits = 0
    promoted_events = 0
    failed = 0
    # Tokens spent on this run's API calls (cache hits cost nothing).
    tokens = {"prompt_tokens": 0, "output_tokens": 0}

    conn = connect_db()
    try:
        # Keep only the latest fetched bulletin per parish, then process those still pending.
        latest = latest_per_parish(load_bulletins(conn))
        pending = [m for m in latest if m.get("processed_at") is None]

        if parish_name:
            parish_row = get_parish_by_name(conn, parish_name)
            if not parish_row:
                LOGGER.warning("Parish not found: %s", parish_name)
                return {
                    "processed_bulletins": 0,
                    "inserted_events": 0,
                    "skipped_events": 0,
                    "cache_hits": 0,
                    "weekly_promotions": 0,
                    "failed_bulletins": 0,
                }
            target_slug = parish_row["slug"]
            pending = [m for m in pending if m["parish_slug"] == target_slug]

        history = load_history_from_db(conn)
        pruned = prune_history(history)
        if pruned:
            LOGGER.info("Pruned %d expired occurrences from event history", pruned)
            save_history_to_db(conn, history)

        def commit(entry: dict[str, Any], extracted: dict[str, Any], status: str) -> None:
            """Store one result: history first, then the bulletin's events.

            In that order a crash in between leaves the bulletin unprocessed,
            so it is simply re-run (from the cache) and its sightings, already
            on file, are not double-counted.
            """
            nonlocal inserted_events, skipped_events, processed_count, promoted_events
            rows, promoted = _prepare_rows(entry, extracted, history)
            save_history_to_db(conn, history)
            stored, skipped = save_processed_bulletin(
                conn,
                entry["id"],
                rows,
                processed_at=utc_now_iso(),
                published_date=entry.get("published_date"),
            )
            inserted_events += stored
            skipped_events += skipped
            promoted_events += promoted
            processed_count += 1
            record_parish_result(
                conn, run_id, entry["parish_slug"], "process",
                PROCESS_WRONG_BULLETIN if extracted.get("wrong_bulletin") else status,
                source_url=entry.get("source_url"),
                content_hash=entry.get("content_hash"),
                event_count=stored,
                detail=f"{skipped} events could not be stored" if skipped else None,
            )

        # Serve bulletins whose extraction is already cached without an API call.
        uncached: list[dict[str, Any]] = []
        for entry in pending:
            content_hash = entry.get("content_hash")
            cached = (
                load_cached_result(
                    classifier.name, classifier.version, content_hash,
                    churches_for_parish(conn, entry["parish_slug"]),
                )
                if isinstance(content_hash, str) and content_hash
                else None
            )
            if cached is None:
                uncached.append(entry)
                continue
            cache_hits += 1
            commit(entry, cached, PROCESS_CACHED)

        for outcome in iter_extraction_outcomes(
            uncached, conn, classifier.extract, concurrency=concurrency,
        ):
            entry = outcome.entry
            if outcome.skipped or outcome.extracted is None:
                failed += 1
                record_parish_result(
                    conn, run_id, entry["parish_slug"], "process",
                    PROCESS_SKIPPED if outcome.skipped else PROCESS_FAILED,
                    source_url=entry.get("source_url"),
                    content_hash=entry.get("content_hash"),
                    detail=(
                        "PDF could not be loaded"
                        if outcome.skipped
                        else f"{type(outcome.error).__name__}: {outcome.error}"
                    ),
                )
                continue
            usage = outcome.extracted.get("usage")
            if isinstance(usage, dict):
                for key in tokens:
                    tokens[key] += int(usage.get(key) or 0)
            content_hash = entry.get("content_hash")
            if isinstance(content_hash, str) and content_hash:
                store_cached_result(
                    classifier.name, classifier.version, content_hash,
                    churches_for_parish(conn, entry["parish_slug"]), outcome.extracted,
                )
            commit(entry, outcome.extracted, PROCESS_EXTRACTED)
    finally:
        conn.close()

    result = {
        "processed_bulletins": processed_count,
        "inserted_events": inserted_events,
        "skipped_events": skipped_events,
        "cache_hits": cache_hits,
        "weekly_promotions": promoted_events,
        "failed_bulletins": failed,
        **tokens,
    }
    LOGGER.info("Process stage finished: %s", result)
    return result
