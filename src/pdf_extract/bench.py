"""Benchmark a challenger classifier against the baseline's cached results.

Only the challenger is paid for:

1. The baseline (the production Gemini classifier by default) runs cache-only,
   serving the results the weekly job already paid for. Bulletins it has no
   cached result for are left out rather than extracted.
2. The challenger runs on exactly those bulletins (its own cache still applies,
   so a re-run costs nothing).
3. The two runs are compared: agreement, cache hit rates, and cost.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pdf_extract.compare import compare
from pdf_extract.extract_run import bulletins_path
from pdf_extract.extract_run import run as run_extract

LOGGER = logging.getLogger(__name__)

DEFAULT_BASELINE = "gemini-flash"
DEFAULT_CHALLENGER = "gpt-6-luna"


def bench(
    *,
    challenger: str = DEFAULT_CHALLENGER,
    baseline: str = DEFAULT_BASELINE,
    parish_name: str | None = None,
    limit: int | None = None,
    concurrency: int = 5,
    out_path: Path | None = None,
) -> dict[str, Any]:
    if challenger == baseline:
        raise ValueError("Challenger and baseline must be different classifiers")

    base = run_extract(
        classifier_name=baseline, parish_name=parish_name, cache_only=True, limit=limit,
    )
    served = [
        row["bulletin_source_url"]
        for row in json.loads(bulletins_path(baseline).read_text(encoding="utf-8"))
    ]
    print(
        f"{baseline}: {base['cache_hits']} cached results served, "
        f"{base['not_cached']} bulletins without one left out (not extracted)"
    )
    if not served:
        raise RuntimeError(
            f"No cached {baseline} results to benchmark against. "
            "Pull the shared data (`pnpm data:pull`) or check the church lists match."
        )

    chal = run_extract(
        classifier_name=challenger, source_urls=served, concurrency=concurrency,
    )
    print(
        f"{challenger}: {chal['cache_hits']} served from cache, "
        f"{chal['cache_misses']} extracted now, {len(chal['errors'])} errors"
    )
    print()
    report = compare([baseline, challenger], out_path=out_path)
    # The full report is on disk; keep what the CLI echoes short enough that
    # the tables compare printed stay on screen.
    return {
        "markdown_report_path": report["markdown_report_path"],
        "per_classifier": [
            {k: c.get(k) for k in ("classifier", "model", "cache_hit_rate", "usage")}
            for c in report["per_classifier"]
        ],
        "cost": report["pairwise"][0]["cost"],
    }
