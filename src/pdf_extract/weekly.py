"""The weekly pipeline run: fetch, process, snapshot, check, report.

One command so a run has one identity. Every stage records its per-parish
outcome under the run id, and the run ends with a report comparing the
database before and after:

    data/out/<run_id>/before.db           the database as the run found it
    data/out/<run_id>/frontend.json.gz    the snapshot the run would publish
    data/out/<run_id>/report.md|json      what changed, and the publishing checks

Nothing is published here. The run's status says whether it may be:
`passed` (publish automatically), `held` (a check failed; a person decides),
or `failed` (a stage crashed).

`parishes` and `dioceses` limit a manual run. Omit both to refresh every
parish. A diocese contributes the parish files under
`data/dioceses/<diocese>/parishes/` that are already in the live parish table.
Parishes outside the limit keep the bulletins they already had.
"""

from __future__ import annotations

import json
import logging
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pdf_extract.datasync import compact_copy, run_out_dir
from pdf_extract.db import ensure_db
from pdf_extract.dioceses.records import PARISH, diocese_dir
from pdf_extract.extract_frontend_db import SNAPSHOT_NAME
from pdf_extract.extract_frontend_db import extract as extract_snapshot
from pdf_extract.fetch import fetch_bulletins
from pdf_extract.process import process_bulletins
from pdf_extract.report import build_report, render_markdown
from pdf_extract.runs import finish_run, start_run
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db, list_parishes
from pdf_extract.verify_frontend_snapshot import verify_frontend_snapshot

LOGGER = logging.getLogger(__name__)


class RunScopeError(ValueError):
    """The weekly run was asked for parishes or dioceses it cannot refresh."""


@dataclass(frozen=True)
class RunScope:
    """Who a manual run refreshes.

    `parishes` are the ones named directly, `dioceses` the ones named directly,
    and `selected` the union, in parish-table order.
    """

    parishes: tuple[str, ...]
    dioceses: tuple[str, ...]
    selected: tuple[str, ...]

    def summary(self) -> str:
        bits: list[str] = []
        if self.dioceses:
            label = "diocese" if len(self.dioceses) == 1 else "dioceses"
            bits.append(f"{label} " + ", ".join(f"`{slug}`" for slug in self.dioceses))
        if self.parishes:
            bits.append(", ".join(f"`{slug}`" for slug in self.parishes))
        count = len(self.selected)
        noun = "parish" if count == 1 else "parishes"
        return f"Refreshed {count} {noun}: {'; '.join(bits)}."

    def as_dict(self) -> dict[str, Any]:
        return {
            "parishes": list(self.parishes),
            "dioceses": list(self.dioceses),
            "selected": list(self.selected),
            "summary": self.summary(),
        }


def _tokens(values: list[str] | None, *, known: set[str] | None = None) -> list[str]:
    """Flatten repeated CLI values into the tokens to look up.

    A value that is itself a known parish (its slug or its name) stays whole,
    so a name containing a comma is one parish. Anything else splits on commas,
    which is how a workflow input passes several slugs in one string.
    """
    out: list[str] = []
    for value in values or []:
        text = value.strip()
        if not text:
            continue
        if known is not None and text in known:
            out.append(text)
            continue
        out.extend(part.strip() for part in text.split(",") if part.strip())
    return out


def resolve_run_scope(
    conn,
    *,
    parishes: list[str] | None = None,
    dioceses: list[str] | None = None,
) -> RunScope | None:
    """The parishes a run should refresh, or None to refresh every parish.

    Raises `RunScopeError` for a parish or diocese that cannot be refreshed,
    and `DioceseError` for a diocese slug that does not exist.
    """
    rows = list(list_parishes(conn))
    by_slug = {row["slug"]: row["slug"] for row in rows}
    by_name: dict[str, str] = {}
    for row in rows:
        by_name.setdefault(row["name"], row["slug"])
    known = set(by_slug) | set(by_name)

    parish_tokens = _tokens(parishes, known=known)
    diocese_tokens = _tokens(dioceses)
    if not parish_tokens and not diocese_tokens:
        return None

    requested: list[str] = []
    missing: list[str] = []
    for token in parish_tokens:
        slug = by_slug.get(token) or by_name.get(token)
        if slug is None:
            missing.append(token)
        elif slug not in requested:
            requested.append(slug)
    if missing:
        raise RunScopeError(
            "Parish not found: " + ", ".join(missing)
            + ". Use a slug or name from data/parishes.csv."
        )

    selected = list(requested)
    seen = set(selected)
    resolved_dioceses: list[str] = []
    for diocese in diocese_tokens:
        if diocese in resolved_dioceses:
            continue
        folder = diocese_dir(diocese) / PARISH.dir
        files = sorted(path.stem for path in folder.glob("*.md")) if folder.is_dir() else []
        live = [slug for slug in files if slug in by_slug]
        absent = [slug for slug in files if slug not in by_slug]
        if not live:
            extra = (
                f" ({len(absent)} recorded but not in data/parishes.csv)" if absent else ""
            )
            raise RunScopeError(
                f"Diocese {diocese!r} has no parishes in data/parishes.csv{extra}."
            )
        if absent:
            LOGGER.warning(
                "Diocese %s: skipping %d parish records not in data/parishes.csv: %s",
                diocese, len(absent), ", ".join(absent),
            )
        resolved_dioceses.append(diocese)
        for slug in live:
            if slug not in seen:
                seen.add(slug)
                selected.append(slug)

    order = {row["slug"]: index for index, row in enumerate(rows)}
    selected.sort(key=lambda slug: order[slug])
    return RunScope(
        parishes=tuple(requested),
        dioceses=tuple(resolved_dioceses),
        selected=tuple(selected),
    )


def run_weekly(
    *,
    run_id: str,
    model: str = DEFAULT_GEMINI_MODEL,
    concurrency: int = 5,
    git_sha: str | None = None,
    trigger: str | None = None,
    parishes: list[str] | None = None,
    dioceses: list[str] | None = None,
) -> dict[str, Any]:
    # The stages always work on the default database, so the run does too.
    db_path = DEFAULT_DB_PATH
    seeded = ensure_db(db_path)
    conn = connect_db(db_path)
    try:
        scope = resolve_run_scope(conn, parishes=parishes, dioceses=dioceses)
    finally:
        conn.close()
    slugs = None if scope is None else list(scope.selected)
    if scope is not None:
        LOGGER.info("Weekly run %s: %s", run_id, scope.summary())

    out = run_out_dir(run_id)
    out.mkdir(parents=True, exist_ok=True)

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
        stages["fetch"] = fetch_bulletins(run_id=run_id, slugs=slugs)
        stages["process"] = process_bulletins(
            model=model, concurrency=concurrency, run_id=run_id, slugs=slugs,
        )

        snapshot = out / SNAPSHOT_NAME
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
            seeded=seeded,
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
        if scope is not None:
            report["scope"] = scope.as_dict()
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
        "scope": None if scope is None else scope.as_dict(),
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
