"""The weekly pipeline run: fetch, process, snapshot, check, report.

One command so a run has one identity. Every stage records its per-parish
outcome under the run id, and the run ends with a report comparing the
database before and after:

    data/out/<run_id>/before.db           the database as the run found it
    data/out/<run_id>/frontend.snapshot   the snapshot the run would publish
    data/out/<run_id>/report.md|json      what changed, and the publishing checks

Nothing is published here. The run's status says whether it may be:
`passed` (publish automatically), `held` (a check failed; a person decides),
or `failed` (a stage crashed).
"""

from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path
from typing import Any

from pdf_extract.datasync import compact_copy, run_out_dir
from pdf_extract.db import ensure_db
from pdf_extract.extract_frontend_db import extract as extract_snapshot
from pdf_extract.fetch import fetch_bulletins
from pdf_extract.process import process_bulletins
from pdf_extract.report import build_report, render_markdown
from pdf_extract.runs import finish_run, start_run
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db
from pdf_extract.verify_frontend_snapshot import verify_frontend_snapshot

LOGGER = logging.getLogger(__name__)


def run_weekly(
    *,
    run_id: str,
    model: str = DEFAULT_GEMINI_MODEL,
    concurrency: int = 5,
    git_sha: str | None = None,
    trigger: str | None = None,
) -> dict[str, Any]:
    # The stages always work on the default database, so the run does too.
    db_path = DEFAULT_DB_PATH
    out = run_out_dir(run_id)
    out.mkdir(parents=True, exist_ok=True)

    ensure_db(db_path)
    before_db = out / "before.db"
    compact_copy(db_path, before_db)

    conn = connect_db(db_path)
    try:
        start_run(conn, run_id, git_sha=git_sha, trigger=trigger)
    finally:
        conn.close()

    stages: dict[str, Any] = {}
    status = "failed"
    report: dict[str, Any] | None = None
    try:
        stages["fetch"] = fetch_bulletins(run_id=run_id)
        stages["process"] = process_bulletins(
            model=model, concurrency=concurrency, run_id=run_id,
        )

        snapshot = out / "frontend.snapshot"
        stages["snapshot"] = extract_snapshot(db_path, snapshot, keep_previous=False)
        with tempfile.TemporaryDirectory() as tmp:
            before_snapshot = Path(tmp) / "before.snapshot"
            extract_snapshot(before_db, before_snapshot, keep_previous=False)
            verification = verify_frontend_snapshot(current=snapshot, previous=before_snapshot)

        report = build_report(
            run_id=run_id,
            before_db=before_db,
            after_db=db_path,
            stages=stages,
            snapshot_verification=verification,
        )
        status = report["status"]
    finally:
        conn = connect_db(db_path)
        try:
            finish_run(conn, run_id, status=status, summary=stages)
        finally:
            conn.close()
        if report is None:
            report = _failed_report(run_id, stages)
        report["status"] = status
        (out / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
        )
        (out / "report.md").write_text(render_markdown(report), encoding="utf-8")

    LOGGER.info("Weekly run %s finished: %s", run_id, status)
    return {
        "run_id": run_id,
        "status": status,
        "report": str(out / "report.md"),
        "stages": stages,
        "totals": report["totals"],
    }


def _failed_report(run_id: str, stages: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "status": "failed",
        "gates": [{"name": "Pipeline completed", "passed": False, "detail": "a stage crashed"}],
        "stages": stages,
        "totals": {
            "parishes_showing_events": 0,
            "events_before": 0,
            "events_after": 0,
            "events_added": 0,
            "events_removed": 0,
            "parishes_changed": 0,
            "parishes_with_new_bulletin": 0,
        },
        "attention": {
            "failures": [],
            "wrong_bulletins": [],
            "stale_parishes": {},
            "dropped_to_zero": [],
            "big_drops": [],
        },
        "changes": [],
    }
