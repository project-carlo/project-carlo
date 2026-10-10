"""`seed extract` and `seed ask`: an external model's second opinion, recorded in the seed file.

Both go through a cache, so asking twice costs one call: `extract` the result
cache the classifiers share (`runner.cache_key`), `ask` its own under
`runs/seed-ask/cache/`. Every call, served from the cache or not, is appended to
the seed file's `calls`, which a slot's sources can then name.

Once a parish has made `CARLO_SEED_CALL_LIMIT` (default 4) calls that were not
served from a cache, both refuse, so a confused subagent can't run up the bill.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from datetime import date
from hashlib import sha256
from typing import Any

from pdf_extract.blobstore import get_store
from pdf_extract.classifiers import get_classifier
from pdf_extract.classifiers.seed_ask import GEMINI_MODEL, MODELS, OPENAI_MODEL, SeedAsker
from pdf_extract.evals import pricing
from pdf_extract.labeling.bulletins import gemini_rows
from pdf_extract.runner import (
    _cache_version_component,
    load_cached_result,
    store_cached_result,
)
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.seeding.files import (
    ASK,
    EXTRACT,
    new_seed,
    next_call_id,
    paid_calls,
    read_seed,
    write_seed_file,
)
from pdf_extract.seeding.queries import (
    SeedContext,
    SeedError,
    bulletin_pdf,
    parish_bulletins,
    resolve_bulletin,
)
from pdf_extract.storage import churches_for_parish, utc_now_iso

LOGGER = logging.getLogger(__name__)

DEFAULT_CALL_LIMIT = 4
CALL_LIMIT_ENV = "CARLO_SEED_CALL_LIMIT"
MAX_QUESTION_CHARS = 1000


def call_limit() -> int:
    raw = os.environ.get(CALL_LIMIT_ENV, "").strip()
    if not raw:
        return DEFAULT_CALL_LIMIT
    try:
        return max(0, int(raw))
    except ValueError as exc:
        raise SeedError(f"{CALL_LIMIT_ENV} must be a whole number, not {raw!r}") from exc


def extraction_classifier(model: str):
    """The classifier `seed extract --model` runs: the eval classifiers, so their cache is shared."""
    if model == OPENAI_MODEL:
        return get_classifier("gpt-6-luna", model=model)
    if model == GEMINI_MODEL:
        if model == DEFAULT_GEMINI_MODEL:
            return get_classifier("gemini-flash-qualified")
        return get_classifier("gemini-flash-qualified", model=model)
    raise SeedError(f"--model must be one of {', '.join(MODELS)}, not {model!r}")


def load_or_start(
    conn: sqlite3.Connection, ctx: SeedContext, parish_slug: str,
) -> dict[str, Any]:
    """The parish's seed file, or a new draft listing its bulletins (not yet written)."""
    seed = read_seed(parish_slug, ctx.seeds_dir)
    if seed is not None:
        return seed
    bulletins = [
        b for b in parish_bulletins(conn, parish_slug, cutoff=ctx.cutoff(parish_slug))
        if b["duplicate_of"] is None
    ]
    return new_seed(parish_slug, bulletins)


def _list_bulletin(seed: dict[str, Any], bulletin: dict[str, Any]) -> None:
    """Make sure the file lists a bulletin a call was made on."""
    if any(b.get("content_hash") == bulletin["content_hash"] for b in seed["bulletins"]):
        return
    seed["bulletins"].append({
        "content_hash": bulletin["content_hash"],
        "fetched_at": bulletin["fetched_at"],
        "published_date": bulletin["published_date"],
        "read": False,
    })
    seed["bulletins"].sort(key=lambda b: b["fetched_at"], reverse=True)


def _check_limit(seed: dict[str, Any], parish_slug: str) -> None:
    limit = call_limit()
    used = paid_calls(seed)
    if used >= limit:
        raise SeedError(
            f"{parish_slug} has used its {limit} external calls ({CALL_LIMIT_ENV}). Decide from "
            "the bulletins and history, or leave the slot as a question for the reviewer."
        )


def _today(bulletin: dict[str, Any]) -> date:
    """The bulletin's fetch date: "today" as the pipeline saw it, so a replay hits the cache."""
    return date.fromisoformat(bulletin["fetched_at"][:10])


def _cost(model: str | None, usage: dict[str, Any]) -> float | None:
    cost = pricing.call_cost(model, usage or {})
    return None if cost is None else round(cost, 6)


def _record(
    ctx: SeedContext, seed: dict[str, Any], bulletin: dict[str, Any], call: dict[str, Any],
) -> dict[str, Any]:
    _list_bulletin(seed, bulletin)
    call = {"id": next_call_id(seed), **call, "bulletin": bulletin["content_hash"],
            "at": utc_now_iso()}
    seed["calls"].append(call)
    write_seed_file(seed, ctx.seeds_dir)
    return call


def run_extract(
    conn: sqlite3.Connection, ctx: SeedContext, parish_slug: str, ref: str, model: str,
) -> dict[str, Any]:
    """A full extraction of one bulletin with the eval policy, appended to the seed file."""
    classifier = extraction_classifier(model)
    bulletin = resolve_bulletin(conn, parish_slug, ref, cutoff=ctx.cutoff(parish_slug))
    seed = load_or_start(conn, ctx, parish_slug)
    churches = churches_for_parish(conn, parish_slug)
    result = load_cached_result(
        classifier.name, classifier.version, bulletin["content_hash"], churches,
    )
    cached = result is not None
    if result is None:
        _check_limit(seed, parish_slug)
        pdf = bulletin_pdf(parish_slug, bulletin["content_hash"])
        result = classifier.extract(pdf, churches=churches, today=_today(bulletin))
        store_cached_result(
            classifier.name, classifier.version, bulletin["content_hash"], churches, result,
        )
    events = []
    for row in gemini_rows(result.get("events") or []):
        events.append({k: v for k, v in row.items() if k not in ("id", "raw")})
    usage = result.get("usage") or {}
    return _record(ctx, seed, bulletin, {
        "kind": EXTRACT,
        "model": model,
        "classifier_version": classifier.version,
        "cached": cached,
        "cost_usd": None if cached else _cost(pricing.model_of(classifier.version), usage),
        "published_date": result.get("published_date"),
        "wrong_bulletin": bool(result.get("wrong_bulletin", False)),
        "events": events,
    })


def ask_cache_key(
    asker: SeedAsker, content_hash: str, churches: list[dict[str, Any]], today: date,
    question: str,
) -> str:
    """Where an answer is cached: by model and prompt version, PDF, churches, date and question."""
    asked = json.dumps(
        {"churches": sorted(churches, key=lambda c: str(c.get("slug"))),
         "today": today.isoformat(), "question": question.strip()},
        sort_keys=True, ensure_ascii=False,
    )
    digest = sha256(asked.encode("utf-8")).hexdigest()[:16]
    return (
        f"runs/{asker.name}/cache/{_cache_version_component(asker.version)}/"
        f"{content_hash}-{digest}.json"
    )


def run_ask(
    conn: sqlite3.Connection, ctx: SeedContext, parish_slug: str, ref: str, model: str,
    question: str,
) -> dict[str, Any]:
    """One question about one bulletin, answered with a page and a quote, appended to the file."""
    if model not in MODELS:
        raise SeedError(f"--model must be one of {', '.join(MODELS)}, not {model!r}")
    question = question.strip()
    if not question:
        raise SeedError("Ask a question")
    if len(question) > MAX_QUESTION_CHARS:
        raise SeedError(f"Keep the question under {MAX_QUESTION_CHARS} characters")
    asker = SeedAsker(model)
    bulletin = resolve_bulletin(conn, parish_slug, ref, cutoff=ctx.cutoff(parish_slug))
    seed = load_or_start(conn, ctx, parish_slug)
    churches = churches_for_parish(conn, parish_slug)
    today = _today(bulletin)
    key = ask_cache_key(asker, bulletin["content_hash"], churches, today, question)
    store = get_store()
    cached_bytes = None
    try:
        cached_bytes = store.get(key)
    except Exception:
        LOGGER.warning("Cache lookup failed for %s; treating as a miss", key, exc_info=True)
    result = json.loads(cached_bytes.decode("utf-8")) if cached_bytes else None
    cached = result is not None
    if result is None:
        _check_limit(seed, parish_slug)
        pdf = bulletin_pdf(parish_slug, bulletin["content_hash"])
        result = asker.ask(pdf, churches=churches, today=today, question=question)
        try:
            store.put(key, (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode(),
                      content_type="application/json")
        except Exception:
            LOGGER.warning("Could not store cache entry %s", key, exc_info=True)
    return _record(ctx, seed, bulletin, {
        "kind": ASK,
        "model": model,
        "classifier_version": asker.version,
        "cached": cached,
        "cost_usd": None if cached else _cost(model, result.get("usage") or {}),
        "question": question,
        "answer": result.get("answer", ""),
        "page": result.get("page"),
        "quote": result.get("quote", ""),
    })
