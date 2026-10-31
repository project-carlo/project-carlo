"""Replay the snapshot gates over archived runs, to see which would have held.

Each archived run keeps the database it ended with
(`pipeline/runs/<run_id>/parish_events.db.gz`). For each pair of consecutive
runs given, this rebuilds both snapshots with this code, reads them on the
later run's date, runs today's gates and prints which fire next to the status
the later run recorded. The earlier run's database stands in for the later
run's `before.db`: the same thing when the earlier run was published, an
approximation when it was held.

Read-only: it needs R2 read credentials, and writes only to a temporary
directory, where each downloaded database is migrated to this checkout's
schema before its snapshot is built.
"""

from __future__ import annotations

import gzip
import logging
import re
import tempfile
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import BlobStoreError, get_store
from pdf_extract.datasync import PIPELINE_PREFIX, _fetch_verified, _read_json, run_key
from pdf_extract.db import migrate
from pdf_extract.report import verify_databases
from pdf_extract.storage import connect_db

LOGGER = logging.getLogger(__name__)

_RUN_DATE = re.compile(r"^(\d{4})(\d{2})(\d{2})T")

# Run id -> (manifest, path of its database), so tests can supply local databases.
Fetch = Callable[[str, Path], tuple[dict[str, Any], Path]]


def run_date(run_id: str, manifest: dict[str, Any]) -> date:
    """The day a run happened: its id's UTC timestamp, else its manifest's created_at."""
    match = _RUN_DATE.match(run_id)
    if match:
        return date(*(int(part) for part in match.groups()))
    created = str(manifest.get("created_at") or "")[:10]
    try:
        return date.fromisoformat(created)
    except ValueError as exc:
        raise ValueError(f"Can't tell when run {run_id} happened") from exc


def archived_run_ids(last: int) -> list[str]:
    """The `last` most recent archived runs that still have a manifest, oldest first."""
    store = get_store()
    if store.remote is None:
        raise BlobStoreError(
            "No R2 credentials: set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY"
        )
    run_ids = sorted({
        key.split("/")[2] for key in store.remote.list(f"{PIPELINE_PREFIX}/runs/")
        if key.endswith("/manifest.json")
    })
    return run_ids[-last:]


def fetch_run(run_id: str, directory: Path) -> tuple[dict[str, Any], Path]:
    """Download a run's manifest and database into `directory`."""
    store = get_store()
    manifest = _read_json(store, run_key(run_id, "manifest.json"))
    if manifest is None:
        raise BlobStoreError(f"No run {run_id} in the bucket")
    data = _fetch_verified(store, manifest["db_key"], manifest["db_sha256"])
    path = directory / f"{run_id}.db"
    path.write_bytes(gzip.decompress(data))
    return manifest, path


def _upgrade(path: Path) -> Path:
    """Bring a downloaded copy to this checkout's schema, as `before.db` would be.

    Migrations only: the reference data stays as the run had it.
    """
    conn = connect_db(path)
    try:
        migrate(conn)
    finally:
        conn.close()
    return path


def replay(run_ids: list[str], *, fetch: Fetch = fetch_run) -> dict[str, Any]:
    """The gates for each consecutive pair of `run_ids` (oldest first)."""
    if len(run_ids) < 2:
        raise ValueError("Replaying needs at least two runs")
    pairs: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as tmp:
        _, previous_db = fetch(run_ids[0], Path(tmp))
        _upgrade(previous_db)
        for earlier, later in zip(run_ids, run_ids[1:]):
            manifest, db = fetch(later, Path(tmp))
            _upgrade(db)
            as_of = run_date(later, manifest)
            LOGGER.info("Replaying %s -> %s as of %s", earlier, later, as_of)
            result = verify_databases(previous_db, db, as_of)
            failed = [g for g in result["gates"] if not g["passed"]]
            pairs.append({
                "before_run": earlier,
                "after_run": later,
                "as_of": as_of.isoformat(),
                "recorded_status": manifest.get("status"),
                "replayed_status": "passed" if result["passed"] else "held",
                "failed_gates": [{"name": g["name"], "detail": g["detail"]} for g in failed],
                "gates": {g["name"]: g["passed"] for g in result["gates"]},
                "weekly_match_pct": (result.get("weekly_events") or {}).get("match_pct"),
                "local_losses": [
                    {key: loss[key] for key in (
                        "parish_slug", "level", "church_slug", "event_type", "before", "lost",
                        "moved", "missing", "holds", "seeded_this_run",
                    )}
                    for loss in result.get("local_losses") or [] if loss["severe"]
                ],
                "dropped_to_zero": result.get("dropped_to_zero") or [],
            })
            previous_db.unlink(missing_ok=True)
            previous_db = db
    return {
        "runs": run_ids,
        "pairs": pairs,
        "would_hold": sum(1 for p in pairs if p["replayed_status"] == "held"),
        "recorded_held": sum(1 for p in pairs if p["recorded_status"] == "held"),
    }


def render(result: dict[str, Any]) -> str:
    """One line per pair: the recorded status, the replayed one, and the gates that fired."""
    lines = []
    for pair in result["pairs"]:
        mark = "" if pair["recorded_status"] == pair["replayed_status"] else "  (differs)"
        lines.append(
            f"{pair['before_run']} → {pair['after_run']} as of {pair['as_of']}: "
            f"recorded {pair['recorded_status']}, replayed {pair['replayed_status']}{mark}"
        )
        for gate in pair["failed_gates"]:
            lines.append(f"  ✗ {gate['name']}: {gate['detail']}")
    lines.append(
        f"{result['would_hold']} of {len(result['pairs'])} pairs would hold; "
        f"{result['recorded_held']} were recorded held."
    )
    return "\n".join(lines)
