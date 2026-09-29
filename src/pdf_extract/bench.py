"""Benchmark text-extraction stacks against the production Gemini extractions.

One command (`pnpm bench`) runs the whole comparison:

1. Brings the local database up (pulling the published one from R2 if there
   is none) so the corpus is each parish's current bulletin.
2. Serves the Gemini baseline from the extraction cache the weekly job already
   paid for (no Gemini key needed); only bulletins with a cached baseline are
   benchmarked, unless `--fill-baseline` is given with a GEMINI_API_KEY.
3. Runs each stack on those bulletins, for each OpenAI model under test: a
   text extractor (PyMuPDF with an OCR fallback, Docling, or full-page OCR)
   followed by the model reading the text, plus the model reading the PDF
   itself as a control, once per PDF `detail` and schema mode under test.
4. Scores every stack against the baseline (`compare --baseline`) and writes
   the report under data/runs/bench/.

With `--labels` the hand-made labels in data/labels/ are the truth instead:
the corpus is every bulletin labeled `done` (latest or not), Gemini is scored
beside the stacks rather than against them, and the report comes from
`labeling.score` (data/runs/labels/). Every classifier is told today is the
Sunday the bulletin is dated to (see `bulletin_sunday`), not the day it runs.

`--models` takes any OpenAI model id, and any Gemini model id (`gemini-*`),
which reads the PDF the way production does: once, whatever the stacks.

Every stage caches: extracted text per extractor version, and model results
per classifier version, so a re-run only pays for what changed.
"""

from __future__ import annotations

import logging
import os
import random
from collections.abc import Callable
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import get_store
from pdf_extract.classifiers import STACKS, Classifier, stack_classifier, stack_name
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.classifiers.openai_gpt import FileDetail
from pdf_extract.classifiers.text_llm import DEFAULT_REASONING_EFFORT, DEFAULT_TEXT_MODEL
from pdf_extract.compare import compare, load_manifest
from pdf_extract.datasync import pull
from pdf_extract.db import ensure_db
from pdf_extract.extract_run import run as run_extract
from pdf_extract.labeling.labels import LABELS_DIR
from pdf_extract.labeling.score import load_truth, score_against_labels
from pdf_extract.runner import RUNS_DIR
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db, get_parish_by_name

LOGGER = logging.getLogger(__name__)

BENCH_DIR = RUNS_DIR / "bench"
BASELINE = "gemini-flash"

DEFAULT_STACKS = ("pymupdf", "docling", "ocr", "pdf")
DEFAULT_MODELS = (DEFAULT_TEXT_MODEL,)
# The `pdf` stack sends the bulletin at low detail, with Gemini's exact
# schema, unless asked for more.
DEFAULT_DETAILS: tuple[FileDetail, ...] = ("low",)
DEFAULT_SCHEMAS = ("exact",)


class BenchError(RuntimeError):
    """The benchmark cannot run as configured (missing key, data or baseline)."""


def is_gemini(model: str) -> bool:
    return model.startswith("gemini-")


def _configurations(
    stacks: list[str],
    models: list[str],
    details: list[FileDetail],
    schemas: list[str] | None = None,
) -> list[tuple[str, str, FileDetail, str]]:
    """(stack, model, detail, schema) for every run: each model × stack, and the
    `pdf` stack once per detail and schema mode (the text stacks send no PDF and
    always ask for strict output, so both are moot for them).
    A Gemini model runs once, on the PDF, as production does."""
    schemas = list(schemas or DEFAULT_SCHEMAS)
    return [
        (stack, model, detail, schema)
        for model in models
        for stack in (["pdf"] if is_gemini(model) else stacks)
        for detail in (details if STACKS[stack] is None and not is_gemini(model) else details[:1])
        for schema in (schemas if STACKS[stack] is None and not is_gemini(model) else ["exact"])
    ]


def _classifier(
    stack: str, model: str, detail: FileDetail, effort: str | None,
    schema: str = "exact",
) -> Classifier:
    if is_gemini(model):
        # The production model keeps the production name, so it shares its cache.
        return GeminiClassifier(model=model, name=None if model == DEFAULT_GEMINI_MODEL else model)
    return stack_classifier(stack, model=model, detail=detail, schema=schema, effort=effort)


def _labeled_sample(
    labels_dir: Path, limit: int | None, seed: int, parish_name: str | None,
) -> set[tuple[str, str]]:
    """The labeled bulletins (parish slug, content hash) to benchmark."""
    keys = set(load_truth(labels_dir))
    if parish_name:
        conn = connect_db()
        try:
            parish = get_parish_by_name(conn, parish_name)
        finally:
            conn.close()
        keys = {key for key in keys if parish and key[0] == parish["slug"]}
    if not keys:
        raise BenchError(
            f"No labels marked done in {labels_dir}"
            + (f" for parish {parish_name!r}" if parish_name else "")
            + ": label some with `pnpm label` first."
        )
    ordered = sorted(keys)
    by_id = {"/".join(key): key for key in ordered}
    return {by_id[k] for k in _sample(list(by_id), limit, seed)}


def nearest_sunday(day: date) -> date:
    """The Sunday closest to `day` (itself, if it is one)."""
    ahead = (6 - day.weekday()) % 7
    return day + timedelta(days=ahead if ahead <= 3 else ahead - 7)


def bulletin_sunday(label: dict[str, Any] | None, entry: dict[str, Any]) -> date | None:
    """The Sunday a bulletin is dated to: from its label's published date, else
    the one the database has, else the day it was fetched (bulletins are
    fetched the week they come out)."""
    for raw in (
        (label or {}).get("published_date"),
        entry.get("published_date"),
        str(entry.get("fetched_at") or "")[:10],
    ):
        try:
            return nearest_sunday(date.fromisoformat(raw))
        except (TypeError, ValueError):
            continue
    return None


def _sample(urls: list[str], limit: int | None, seed: int) -> set[str]:
    """A deterministic sample of `limit` bulletins (all of them without a limit)."""
    ordered = sorted(urls)
    if limit is None or limit >= len(ordered):
        return set(ordered)
    return set(random.Random(seed).sample(ordered, limit))


def run_bench(
    *,
    stacks: list[str] | None = None,
    models: list[str] | None = None,
    details: list[FileDetail] | None = None,
    schemas: list[str] | None = None,
    effort: str | None = DEFAULT_REASONING_EFFORT,
    limit: int | None = None,
    seed: int = 0,
    parish_name: str | None = None,
    concurrency: int = 8,
    fill_baseline: bool = False,
    refresh_data: bool = False,
    labels: bool = False,
    labels_dir: Path = LABELS_DIR,
) -> dict[str, Any]:
    stacks = list(stacks or DEFAULT_STACKS)
    models = list(dict.fromkeys(models or DEFAULT_MODELS))
    details = list(dict.fromkeys(details or DEFAULT_DETAILS))
    schemas = list(dict.fromkeys(schemas or DEFAULT_SCHEMAS))
    for stack in stacks:
        if stack not in STACKS:
            raise BenchError(f"Unknown stack {stack!r}. Available: {', '.join(STACKS)}")
    if any(not is_gemini(m) for m in models) and not os.environ.get("OPENAI_API_KEY"):
        raise BenchError("OPENAI_API_KEY is not set (put it in .env or the environment).")
    if fill_baseline and not os.environ.get("GEMINI_API_KEY"):
        raise BenchError("--fill-baseline calls Gemini: set GEMINI_API_KEY.")
    other_gemini = [m for m in models if is_gemini(m) and m != DEFAULT_GEMINI_MODEL]
    if other_gemini and not os.environ.get("GEMINI_API_KEY"):
        raise BenchError(f"{', '.join(other_gemini)} runs on Gemini: set GEMINI_API_KEY.")

    if refresh_data or not DEFAULT_DB_PATH.exists():
        if not get_store().is_remote:
            raise BenchError(
                f"No database at {DEFAULT_DB_PATH} and no R2 credentials to pull one: set "
                "R2_ACCOUNT_ID, R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY (read-only is enough)."
            )
        LOGGER.info("Pulling the published database")
        pull(snapshot=False)
    ensure_db(DEFAULT_DB_PATH)

    if labels:
        return _run_against_labels(
            stacks=stacks, models=models, details=details, schemas=schemas, effort=effort,
            limit=limit, seed=seed, parish_name=parish_name, concurrency=concurrency,
            fill_baseline=fill_baseline, labels_dir=labels_dir,
        )

    # The baseline decides the corpus: every bulletin it has a result for.
    LOGGER.info("Loading the %s baseline%s", BASELINE, "" if fill_baseline else " from cache")
    baseline_all = run_extract(
        classifier_name=BASELINE,
        parish_name=parish_name,
        concurrency=concurrency,
        cache_only=not fill_baseline,
    )
    served_urls = set(load_manifest(BASELINE))
    if not served_urls:
        raise BenchError(
            f"No cached {BASELINE} results for the current bulletins "
            f"({baseline_all['bulletins_total']} bulletins, none cached). Pull a published run "
            "with `--refresh-data`, or pass --fill-baseline with a GEMINI_API_KEY."
        )
    sample = _sample(sorted(served_urls), limit, seed)
    LOGGER.info(
        "Benchmarking %d of %d bulletins with a baseline", len(sample), len(served_urls),
    )
    # Rewrite the baseline run to exactly the sample, so the report's totals match.
    run_extract(classifier_name=BASELINE, source_urls=sample, cache_only=True)

    # The baseline is the truth here, not one of the runs under test.
    configurations = [
        c for c in _configurations(stacks, models, details, schemas)
        if c[1] != DEFAULT_GEMINI_MODEL
    ]
    runs, skipped = _run_stacks(
        configurations, effort=effort, concurrency=concurrency, source_urls=sample,
    )
    names = [name for name, summary in runs.items() if summary["bulletins_served"]]
    if not names:
        raise BenchError(f"No stack produced results: {skipped}")

    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    report = compare(
        [BASELINE, *names], baseline=BASELINE, out_path=BENCH_DIR / f"bench_{ts}.json",
    )
    return {
        "bulletins": len(sample),
        "baseline": BASELINE,
        "stacks": _stack_summaries(runs),
        "skipped_stacks": skipped,
        "report_json": str(BENCH_DIR / f"bench_{ts}.json"),
        "report_markdown": report["markdown_report_path"],
    }


def _run_against_labels(
    *,
    stacks: list[str],
    models: list[str],
    details: list[FileDetail],
    schemas: list[str],
    effort: str | None,
    limit: int | None,
    seed: int,
    parish_name: str | None,
    concurrency: int,
    fill_baseline: bool,
    labels_dir: Path,
) -> dict[str, Any]:
    """Run every configuration on the labeled bulletins and score each against the labels.

    Production Gemini is always scored too, served from its cache (or called,
    with `fill_baseline`), so every report shows where the stacks stand
    against it. Asking for the production model in `models` does the same.
    """
    sample = _labeled_sample(labels_dir, limit, seed, parish_name)
    LOGGER.info("Benchmarking %d labeled bulletins against ground truth", len(sample))
    truth = load_truth(labels_dir)

    def today_for(entry: dict[str, Any]) -> date | None:
        return bulletin_sunday(truth.get((entry["parish_slug"], entry["content_hash"])), entry)

    configurations = [
        ("pdf", DEFAULT_GEMINI_MODEL, details[0], "exact"),
        *(
            c for c in _configurations(stacks, models, details, schemas)
            if c[1] != DEFAULT_GEMINI_MODEL
        ),
    ]
    runs, skipped = _run_stacks(
        configurations, effort=effort, concurrency=concurrency, bulletins=sample,
        cache_only={BASELINE: not fill_baseline}, today_for=today_for,
        # Production's results were extracted the week each bulletin was
        # fetched; they stand in for the Sunday-dated ones until filled.
        undated_fallback={BASELINE},
    )
    names = [name for name, summary in runs.items() if summary["bulletins_served"]]
    if not names:
        raise BenchError(f"No classifier produced results: {skipped}")

    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    report = score_against_labels(
        names, labels_dir=labels_dir, bulletins=sample,
        out_path=BENCH_DIR / f"labels_{ts}.json",
    )
    return {
        "bulletins": len(sample),
        "truth": str(labels_dir),
        "stacks": _stack_summaries(runs),
        "skipped_stacks": skipped,
        "report_json": report["report_json"],
        "report_markdown": report["report_markdown"],
    }


def _run_stacks(
    configurations: list[tuple[str, str, FileDetail, str]],
    *,
    effort: str | None,
    concurrency: int,
    source_urls: set[str] | None = None,
    bulletins: set[tuple[str, str]] | None = None,
    cache_only: dict[str, bool] | None = None,
    today_for: Callable[[dict[str, Any]], date | None] | None = None,
    undated_fallback: set[str] | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Run each configuration on the sample: (run summaries by name, skipped with why)."""
    runs: dict[str, Any] = {}
    skipped: dict[str, str] = {}
    for stack, model, detail, schema in configurations:
        label = (
            model if is_gemini(model)
            else stack_name(stack, model=model, detail=detail, schema=schema, effort=effort)
        )
        try:
            classifier = _classifier(stack, model, detail, effort, schema=schema)
        except ImportError as exc:
            LOGGER.error("Skipping stack %s: %s", label, exc)
            skipped[label] = str(exc)
            continue
        LOGGER.info("Running %s (%s)", classifier.name, classifier.version)
        summary = run_extract(
            classifier=classifier, source_urls=source_urls, bulletins=bulletins,
            concurrency=concurrency, cache_only=(cache_only or {}).get(classifier.name, False),
            today_for=today_for, undated_fallback=classifier.name in (undated_fallback or set()),
        )
        runs[classifier.name] = summary
        if not summary["bulletins_served"]:
            skipped[label] = f"no bulletins extracted ({len(summary['errors'])} errors)"
    return runs, skipped


def _stack_summaries(runs: dict[str, Any]) -> dict[str, Any]:
    return {
        name: {
            "version": summary["classifier_version"],
            "served": summary["bulletins_served"],
            "api_calls": summary["cache_misses"],
            "errors": len(summary["errors"]),
        }
        for name, summary in runs.items()
    }
