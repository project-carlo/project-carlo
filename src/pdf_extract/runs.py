"""Pipeline run records: what each run did, parish by parish.

A run is one pass of the weekly pipeline. It gets a `pipeline_run` row, and
each stage writes a `run_parish_result` row per parish it touched, so "which
parishes failed to fetch this week" or "how long has this parish been stuck"
is a query rather than a trawl through CI logs. The records are published
inside the database along with the data they describe.
"""

from __future__ import annotations

import json
import sqlite3
from typing import Any

from pdf_extract.storage import utc_now_iso

# Fetch outcomes.
FETCH_NEW = "new"
# The site served a bulletin the parish already has.
FETCH_UNCHANGED = "unchanged"
# Not fetched: the parish already has this weekend's bulletin.
FETCH_CURRENT = "current"
FETCH_RESOLVE_FAILED = "resolve_failed"
FETCH_DOWNLOAD_FAILED = "download_failed"
# The address of a bulletin we already have did not answer. Not a failure:
# the parish still has that bulletin.
FETCH_RECHECK_FAILED = "recheck_failed"
FETCH_SAVE_FAILED = "save_failed"

# Process outcomes.
PROCESS_EXTRACTED = "extracted"
PROCESS_CACHED = "cached"
PROCESS_WRONG_BULLETIN = "wrong_bulletin"
# A second bulletin for a week we had: it replaces the first.
PROCESS_CORRECTION = "correction"
# A third or later bulletin for one week: flagged for a person to look at.
PROCESS_REPEATED_WEEK = "repeated_week"
# Dated before the parish's newest bulletin: stored, but not shown.
PROCESS_OLD_ISSUE = "old_issue"
PROCESS_FAILED = "failed"
PROCESS_SKIPPED = "skipped"

FAILED_STATUSES = frozenset({
    FETCH_RESOLVE_FAILED,
    FETCH_DOWNLOAD_FAILED,
    FETCH_SAVE_FAILED,
    PROCESS_FAILED,
    PROCESS_SKIPPED,
})

_DETAIL_MAX_CHARS = 500


def join_details(*parts: str | None) -> str | None:
    """The non-empty parts of a result's detail, joined; None if there are none."""
    return "; ".join(part for part in parts if part) or None


def start_run(
    conn: sqlite3.Connection, run_id: str, *, git_sha: str | None, trigger: str | None,
) -> None:
    with conn:
        conn.execute(
            """INSERT INTO pipeline_run(id, started_at, status, git_sha, trigger)
               VALUES (?, ?, 'running', ?, ?)""",
            (run_id, utc_now_iso(), git_sha, trigger),
        )


def finish_run(
    conn: sqlite3.Connection, run_id: str, *, status: str, summary: dict[str, Any],
) -> None:
    with conn:
        conn.execute(
            """UPDATE pipeline_run SET finished_at = ?, status = ?, summary_json = ?
               WHERE id = ?""",
            (utc_now_iso(), status, json.dumps(summary, sort_keys=True), run_id),
        )


def record_parish_result(
    conn: sqlite3.Connection,
    run_id: str | None,
    parish_slug: str,
    stage: str,
    status: str,
    *,
    detail: str | None = None,
    source_url: str | None = None,
    content_hash: str | None = None,
    event_count: int | None = None,
) -> None:
    """Record one stage's outcome for one parish. A no-op outside a run."""
    if run_id is None:
        return
    if detail is not None and len(detail) > _DETAIL_MAX_CHARS:
        detail = detail[: _DETAIL_MAX_CHARS - 1] + "…"
    with conn:
        conn.execute(
            """INSERT OR REPLACE INTO run_parish_result(
                   run_id, parish_slug, stage, status, detail, source_url,
                   content_hash, event_count
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (run_id, parish_slug, stage, status, detail, source_url, content_hash, event_count),
        )


def parish_results(conn: sqlite3.Connection, run_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """SELECT parish_slug, stage, status, detail, source_url, content_hash, event_count
           FROM run_parish_result WHERE run_id = ? ORDER BY parish_slug, stage""",
        (run_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def consecutive_failures(conn: sqlite3.Connection, parish_slug: str, stage: str) -> int:
    """How many of the most recent runs in a row this parish failed `stage`.

    Counts the runs this database knows about. Held and failed runs are not
    published, so the next run (which starts from the published database)
    does not see their records: a parish failing through several unpublished
    runs is undercounted.
    """
    rows = conn.execute(
        """SELECT r.status FROM run_parish_result r
           JOIN pipeline_run p ON p.id = r.run_id
           WHERE r.parish_slug = ? AND r.stage = ?
           ORDER BY p.started_at DESC, p.id DESC""",
        (parish_slug, stage),
    ).fetchall()
    streak = 0
    for row in rows:
        if row["status"] not in FAILED_STATUSES:
            break
        streak += 1
    return streak
