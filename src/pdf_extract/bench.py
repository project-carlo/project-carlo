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

Every stage caches: extracted text per extractor version, and model results
per classifier version, so a re-run only pays for what changed.
"""

from __future__ import annotations

import logging
import os
import random
from datetime import datetime
from typing import Any

from pdf_extract.blobstore import get_store
from pdf_extract.classifiers import STACKS, Classifier, stack_classifier, stack_name
from pdf_extract.classifiers.openai_gpt import FileDetail
from pdf_extract.classifiers.text_llm import DEFAULT_REASONING_EFFORT, DEFAULT_TEXT_MODEL
from pdf_extract.compare import compare, load_manifest
from pdf_extract.datasync import pull
from pdf_extract.db import ensure_db
from pdf_extract.extract_run import run as run_extract
from pdf_extract.runner import RUNS_DIR
from pdf_extract.storage import DEFAULT_DB_PATH

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


def _configurations(
    stacks: list[str], models: list[str], details: list[FileDetail], schemas: list[str],
) -> list[tuple[str, str, FileDetail, str]]:
    """(stack, model, detail, schema) for every run: each model × stack, and the
    `pdf` stack once per detail and schema mode (the text stacks send no PDF and
    always ask for strict output, so both are moot for them)."""
    return [
        (stack, model, detail, schema)
        for model in models
        for stack in stacks
        for detail in (details if STACKS[stack] is None else details[:1])
        for schema in (schemas if STACKS[stack] is None else ["exact"])
    ]


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
) -> dict[str, Any]:
    stacks = list(stacks or DEFAULT_STACKS)
    models = list(dict.fromkeys(models or DEFAULT_MODELS))
    details = list(dict.fromkeys(details or DEFAULT_DETAILS))
    schemas = list(dict.fromkeys(schemas or DEFAULT_SCHEMAS))
    for stack in stacks:
        if stack not in STACKS:
            raise BenchError(f"Unknown stack {stack!r}. Available: {', '.join(STACKS)}")
    if not os.environ.get("OPENAI_API_KEY"):
        raise BenchError("OPENAI_API_KEY is not set (put it in .env or the environment).")
    if fill_baseline and not os.environ.get("GEMINI_API_KEY"):
        raise BenchError("--fill-baseline calls Gemini: set GEMINI_API_KEY.")

    if refresh_data or not DEFAULT_DB_PATH.exists():
        if not get_store().is_remote:
            raise BenchError(
                f"No database at {DEFAULT_DB_PATH} and no R2 credentials to pull one: set "
                "R2_ACCOUNT_ID, R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY (read-only is enough)."
            )
        LOGGER.info("Pulling the published database")
        pull(snapshot=False)
    ensure_db(DEFAULT_DB_PATH)

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

    names: list[str] = []
    runs: dict[str, Any] = {}
    skipped: dict[str, str] = {}
    for stack, model, detail, schema in _configurations(stacks, models, details, schemas):
        label = stack_name(stack, model=model, detail=detail, schema=schema, effort=effort)
        try:
            classifier: Classifier = stack_classifier(
                stack, model=model, detail=detail, schema=schema, effort=effort,
            )
        except ImportError as exc:
            LOGGER.error("Skipping stack %s: %s", label, exc)
            skipped[label] = str(exc)
            continue
        LOGGER.info("Running stack %s (%s)", classifier.name, classifier.version)
        summary = run_extract(classifier=classifier, source_urls=sample, concurrency=concurrency)
        runs[classifier.name] = summary
        if summary["bulletins_served"]:
            names.append(classifier.name)
        else:
            skipped[label] = f"no bulletins extracted ({len(summary['errors'])} errors)"

    if not names:
        raise BenchError(f"No stack produced results: {skipped}")

    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    report = compare(
        [BASELINE, *names], baseline=BASELINE, out_path=BENCH_DIR / f"bench_{ts}.json",
    )
    return {
        "bulletins": len(sample),
        "baseline": BASELINE,
        "stacks": {
            name: {
                "version": summary["classifier_version"],
                "served": summary["bulletins_served"],
                "api_calls": summary["cache_misses"],
                "errors": len(summary["errors"]),
            }
            for name, summary in runs.items()
        },
        "skipped_stacks": skipped,
        "report_json": str(BENCH_DIR / f"bench_{ts}.json"),
        "report_markdown": report["markdown_report_path"],
    }
