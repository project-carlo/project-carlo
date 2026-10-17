"""Moving the pipeline database between this checkout and the published copy.

Published data lives in the blob store (R2) under `pipeline/`:

    pipeline/runs/<run_id>/manifest.json         what the run produced (+ hashes)
    pipeline/runs/<run_id>/parish_events.db.gz   the full database after the run
    pipeline/runs/<run_id>/frontend.json.gz      what the website serves (runs
                                                 before it: frontend.snapshot,
                                                 an older format)
    pipeline/runs/<run_id>/report.md|report.json the run's change report
    pipeline/runs/<run_id>/published.json        present once the run has been published
    pipeline/latest.json                         pointer to the published run

A run's objects are written once and never changed. Publishing is moving the
`latest.json` pointer, so rolling back is pointing it at an earlier run.
Only the weekly job has credentials to write; everyone else pulls.

Each run holds a full copy of a database that grows every week, so old runs
are pruned (`prune`): recent weeks and one run a month stay available to roll
back to.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import logging
import re
import sqlite3
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import BlobStoreError, CachedBlobStore, get_store
from pdf_extract.extract_frontend_db import (
    DEST_SNAPSHOT,
    SNAPSHOT_NAME,
    SnapshotFormatError,
    extract,
    read_snapshot,
)
from pdf_extract.paths import DATA_DIR
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db, utc_now_iso

LOGGER = logging.getLogger(__name__)

PIPELINE_PREFIX = "pipeline"
LATEST_KEY = f"{PIPELINE_PREFIX}/latest.json"
SNAPSHOT_PATH = DEST_SNAPSHOT
OUT_DIR = DATA_DIR / "out"
PUBLIC_SNAPSHOT_URL = f"https://projectcarlo.com/{SNAPSHOT_NAME}"


def run_key(run_id: str, name: str) -> str:
    if not run_id or "/" in run_id or run_id.startswith("."):
        raise ValueError(f"Invalid run id: {run_id!r}")
    return f"{PIPELINE_PREFIX}/runs/{run_id}/{name}"


def run_out_dir(run_id: str) -> Path:
    return OUT_DIR / run_id


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(store: CachedBlobStore, key: str) -> dict[str, Any] | None:
    data = store.get_remote(key)
    return None if data is None else json.loads(data.decode("utf-8"))


def _put_json(store: CachedBlobStore, key: str, payload: dict[str, Any]) -> None:
    body = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    store.put_remote(key, body, content_type="application/json")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def compact_copy(source: Path, dest: Path) -> None:
    """Copy a live (WAL-mode) database into one self-contained file."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.unlink(missing_ok=True)
    conn = sqlite3.connect(source)
    try:
        conn.execute("VACUUM INTO ?", (str(dest),))
    finally:
        conn.close()


def _install_db(data: bytes, db_path: Path) -> None:
    """Replace the local database, keeping the one it replaces as .bak."""
    if db_path.exists():
        if Path(f"{db_path}-wal").exists():
            # Fold the write-ahead log into the file first, so the backup holds
            # every committed transaction.
            conn = sqlite3.connect(db_path)
            try:
                conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            finally:
                conn.close()
        db_path.replace(db_path.with_name(db_path.name + ".bak"))
    for suffix in ("-wal", "-shm"):
        Path(f"{db_path}{suffix}").unlink(missing_ok=True)
    _atomic_write(db_path, data)


# ── Pull ────────────────────────────────────────────────────────────────────
def pull(
    *,
    run_id: str | None = None,
    db: bool = True,
    snapshot: bool = True,
    db_path: Path = DEFAULT_DB_PATH,
    snapshot_path: Path = SNAPSHOT_PATH,
    public_fallback: bool = False,
) -> dict[str, Any]:
    """Download the published (or a given run's) database and snapshot.

    Bulletin PDFs are not downloaded up front; commands fetch the ones they
    need on first use.

    With `public_fallback`, a snapshot-only pull that has no credentials takes
    the snapshot the live site is serving, which is all the web app needs.

    A run published before the current snapshot format has a snapshot this
    code can't read; with the database pulled too, the snapshot is rebuilt
    from it (the same data), and a snapshot-only pull of such a run fails.
    """
    store = get_store()
    snapshot_only = snapshot and not db
    if not store.is_remote:
        if snapshot_only and public_fallback:
            return _pull_public_snapshot(snapshot_path)
        raise BlobStoreError(
            "No R2 credentials: set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID and "
            "R2_SECRET_ACCESS_KEY (read-only keys are enough to pull)."
        )

    if run_id is None:
        manifest = _read_json(store, LATEST_KEY)
        if manifest is None:
            raise BlobStoreError(f"Nothing published ({LATEST_KEY} not found)")
    else:
        manifest = _read_json(store, run_key(run_id, "manifest.json"))
        if manifest is None:
            raise BlobStoreError(f"No run {run_id} in the bucket")

    result: dict[str, Any] = {"run_id": manifest["run_id"]}
    if db:
        compressed = _fetch_verified(store, manifest["db_key"], manifest["db_sha256"])
        _install_db(gzip.decompress(compressed), db_path)
        result["db_path"] = str(db_path)
    if snapshot:
        data = _fetch_verified(store, manifest["snapshot_key"], manifest["snapshot_sha256"])
        try:
            read_snapshot(data)
        except SnapshotFormatError as exc:
            if not db:
                raise BlobStoreError(
                    f"Run {manifest['run_id']}'s snapshot is in a format this code can't "
                    f"read ({exc}). Pull without --snapshot-only to rebuild it from the "
                    "run's database."
                ) from exc
            LOGGER.info("Run %s's snapshot predates this format; rebuilding it", manifest["run_id"])
            extract(db_path, snapshot_path, keep_previous=False)
        else:
            _atomic_write(snapshot_path, data)
        result["snapshot_path"] = str(snapshot_path)
    LOGGER.info("Pulled run %s", manifest["run_id"])
    return result


def _fetch_verified(store: CachedBlobStore, key: str, sha256: str) -> bytes:
    data = store.get_remote(key)
    if data is None:
        raise BlobStoreError(f"{key} is missing from the bucket")
    if _sha256(data) != sha256:
        raise BlobStoreError(f"{key} does not match the hash in its manifest")
    return data


def _pull_public_snapshot(snapshot_path: Path) -> dict[str, Any]:
    """Without credentials, the snapshot can still come from the live site."""
    LOGGER.info("No R2 credentials; downloading the snapshot from %s", PUBLIC_SNAPSHOT_URL)
    request = urllib.request.Request(
        PUBLIC_SNAPSHOT_URL, headers={"User-Agent": "project-carlo-data-pull"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    try:
        read_snapshot(data)
    except SnapshotFormatError as exc:
        # The live site serves the format of the code it was deployed from.
        raise BlobStoreError(
            f"{PUBLIC_SNAPSHOT_URL} did not return a snapshot this code can read ({exc}). "
            "If the live site runs code older than this format, pull with R2 credentials "
            "instead, or build one from a local database with `pnpm extract:web`."
        ) from exc
    _atomic_write(snapshot_path, data)
    return {"run_id": None, "snapshot_path": str(snapshot_path), "source": PUBLIC_SNAPSHOT_URL}


# ── Publish ─────────────────────────────────────────────────────────────────
def push_candidate(
    run_id: str,
    *,
    db_path: Path = DEFAULT_DB_PATH,
    snapshot_path: Path | None = None,
    git_sha: str | None = None,
) -> dict[str, Any]:
    """Upload a run's database, snapshot and report. Does not publish them.

    The files come from `data/out/<run_id>/`, where `weekly` leaves them.
    """
    store = get_store()
    if store.get_remote(run_key(run_id, "manifest.json")) is not None:
        raise BlobStoreError(
            f"Run {run_id} is already uploaded; runs are written once. Use a new run id."
        )
    out = run_out_dir(run_id)
    snapshot_path = snapshot_path or out / SNAPSHOT_NAME

    with tempfile.TemporaryDirectory() as tmp:
        compact = Path(tmp) / "parish_events.db"
        compact_copy(db_path, compact)
        db_gz = gzip.compress(compact.read_bytes(), compresslevel=9, mtime=0)
    snapshot = snapshot_path.read_bytes()

    manifest: dict[str, Any] = {
        "run_id": run_id,
        "created_at": utc_now_iso(),
        "git_sha": git_sha,
        "db_key": run_key(run_id, "parish_events.db.gz"),
        "db_sha256": _sha256(db_gz),
        "snapshot_key": run_key(run_id, SNAPSHOT_NAME),
        "snapshot_sha256": _sha256(snapshot),
    }
    store.put_remote(manifest["db_key"], db_gz, content_type="application/gzip")
    store.put_remote(manifest["snapshot_key"], snapshot, content_type="application/octet-stream")
    for name, content_type in (
        ("report.md", "text/markdown; charset=utf-8"),
        ("report.json", "application/json"),
    ):
        path = out / name
        if path.exists():
            key = run_key(run_id, name)
            store.put_remote(key, path.read_bytes(), content_type=content_type)
            manifest[f"{name.replace('.', '_')}_key"] = key
    report = out / "report.json"
    if report.exists():
        manifest["status"] = json.loads(report.read_text(encoding="utf-8")).get("status")
    _put_json(store, run_key(run_id, "manifest.json"), manifest)
    LOGGER.info("Uploaded run %s (not yet published)", run_id)
    return manifest


def promote(run_id: str, *, rollback: bool = False) -> dict[str, Any]:
    """Publish a run: point `latest.json` at it.

    Refuses a run older than the one published unless `rollback`: every run
    starts from the published database, so publishing an older one silently
    drops everything the newer one added (a held run approved a week late,
    say, after the next week's run already passed).
    """
    store = get_store()
    manifest = _read_json(store, run_key(run_id, "manifest.json"))
    if manifest is None:
        raise BlobStoreError(f"No run {run_id} in the bucket; upload it first")
    if manifest.get("status") == "failed":
        raise BlobStoreError(f"Run {run_id} failed partway; it cannot be published")
    for key in (manifest["db_key"], manifest["snapshot_key"]):
        if store.remote is None or not store.remote.exists(key):
            raise BlobStoreError(f"Run {run_id} is incomplete: {key} is missing")

    current = _read_json(store, LATEST_KEY)
    if (
        current is not None
        and not rollback
        and str(manifest.get("created_at", "")) < str(current.get("created_at", ""))
    ):
        raise BlobStoreError(
            f"Run {run_id} is older than the published run {current['run_id']}; publishing "
            "it would drop newer data. Pass --rollback if that is what you want."
        )
    published_marker = run_key(run_id, "published.json")
    if store.get_remote(published_marker) is None:
        # Marks the run as one a person or the checks let go live, so pruning
        # keeps it as a rollback point even if its status was "held".
        _put_json(store, published_marker, {"run_id": run_id, "published_at": utc_now_iso()})
    pointer = dict(manifest)
    pointer["published_at"] = utc_now_iso()
    pointer["previous_run_id"] = current["run_id"] if current else None
    _put_json(store, LATEST_KEY, pointer)
    LOGGER.info("Published run %s (previously %s)", run_id, pointer["previous_run_id"])
    return pointer


def status(limit: int = 10) -> dict[str, Any]:
    """The published run and the most recent uploaded runs, with their status."""
    store = get_store()
    latest = _read_json(store, LATEST_KEY)
    assert store.remote is not None
    run_ids = sorted(
        {key.split("/")[2] for key in store.remote.list(f"{PIPELINE_PREFIX}/runs/")},
        reverse=True,
    )
    recent = []
    for run_id in run_ids[:limit]:
        manifest = _read_json(store, run_key(run_id, "manifest.json")) or {}
        recent.append({
            "run_id": run_id,
            "status": manifest.get("status"),
            "created_at": manifest.get("created_at"),
            "git_sha": manifest.get("git_sha"),
            "published": bool(latest and latest.get("run_id") == run_id),
        })
    return {"published": latest, "recent_runs": recent}


# ── Prune ───────────────────────────────────────────────────────────────────
DEFAULT_KEEP_RECENT = 8
DEFAULT_KEEP_MONTHLY = 12
# The weekly workflow's run ids: `date -u +%Y%m%dT%H%M%SZ` then a suffix.
_TIMESTAMPED_RUN_ID = re.compile(r"^\d{8}T\d{6}Z")


def prune(
    *,
    keep_recent: int = DEFAULT_KEEP_RECENT,
    keep_monthly: int = DEFAULT_KEEP_MONTHLY,
    apply: bool = False,
) -> dict[str, Any]:
    """Delete old runs from `pipeline/runs/`, keeping the ones worth rolling back to.

    Kept: the published run and every run after it (candidates and held runs
    still waiting on a person), the `keep_recent` most recent runs, and for
    each of the `keep_monthly` most recent months, that month's last run that
    passed its checks or was published. Runs whose id is not the workflow's
    `<UTC timestamp>-...` form are never touched, since their order is
    unknown. Without `apply`, only reports what it would delete.
    """
    if keep_recent < 1 or keep_monthly < 0:
        raise ValueError("keep_recent must be at least 1 and keep_monthly at least 0")
    store = get_store()
    latest = _read_json(store, LATEST_KEY)
    if latest is None:
        raise BlobStoreError("No run is published; nothing to prune against")
    published = str(latest["run_id"])
    if not _TIMESTAMPED_RUN_ID.match(published):
        raise BlobStoreError(
            f"The published run id {published!r} does not start with a UTC timestamp, "
            "so which runs are older is unknown; not pruning"
        )

    assert store.remote is not None
    keys_by_run: dict[str, list[str]] = {}
    for key in store.remote.list(f"{PIPELINE_PREFIX}/runs/"):
        keys_by_run.setdefault(key.split("/")[2], []).append(key)
    if published not in keys_by_run:
        raise BlobStoreError(f"The published run {published} is missing from the bucket")
    ignored = sorted(run_id for run_id in keys_by_run if not _TIMESTAMPED_RUN_ID.match(run_id))
    # Fixed-width UTC timestamps, so sorting the ids sorts the runs by time.
    run_ids = sorted(run_id for run_id in keys_by_run if _TIMESTAMPED_RUN_ID.match(run_id))

    keep = {run_id for run_id in run_ids if run_id >= published}
    keep.update(run_ids[-keep_recent:])
    last_of_month: dict[str, str] = {}
    for run_id in run_ids:
        keys = keys_by_run[run_id]
        if run_key(run_id, "manifest.json") not in keys:
            continue  # an upload that never finished: nothing to roll back to
        manifest = _read_json(store, run_key(run_id, "manifest.json")) or {}
        went_live = run_key(run_id, "published.json") in keys
        if manifest.get("status") != "passed" and not went_live:
            continue  # held or failed: never approved, so not a rollback point
        last_of_month[f"{run_id[:4]}-{run_id[4:6]}"] = run_id
    for month in sorted(last_of_month)[-keep_monthly:] if keep_monthly else []:
        keep.add(last_of_month[month])

    deleted = [run_id for run_id in run_ids if run_id not in keep]
    if apply:
        for run_id in deleted:
            keys = keys_by_run[run_id]
            manifest_key = run_key(run_id, "manifest.json")
            # The manifest goes first, so a run whose deletion stops halfway no
            # longer looks complete and is swept up by the next prune.
            if manifest_key in keys:
                store.delete_remote([manifest_key])
            store.delete_remote([key for key in keys if key != manifest_key])
            LOGGER.info("Deleted run %s (%d objects)", run_id, len(keys))
    else:
        for run_id in deleted:
            LOGGER.info("Would delete run %s", run_id)
    if ignored:
        LOGGER.warning("Left alone runs without a timestamped id: %s", ", ".join(ignored))
    return {
        "published": published,
        "applied": apply,
        "kept": sorted(keep),
        "deleted": deleted,
        "ignored": ignored,
    }


def build_deploy_snapshot(
    *,
    snapshot_path: Path = SNAPSHOT_PATH,
    db_path: Path = DEFAULT_DB_PATH,
) -> dict[str, Any]:
    """The snapshot to deploy, built from the published database by *this* code.

    Building here rather than reusing the published run's snapshot keeps the
    snapshot's format in step with the web code being deployed, and lets
    parishes.csv/churches.csv edits (seeded by `ensure_db`) show up in a
    preview and on merge without waiting for the next weekly run.
    """
    # Imported here: db imports this module's neighbours.
    from pdf_extract.db import ensure_db, migrate

    pulled = pull(db=True, snapshot=False, db_path=db_path)
    conn = connect_db(db_path)
    try:
        migrations = migrate(conn)
    finally:
        conn.close()
    # The published run's data as it stands, before the CSVs are applied.
    published = extract(db_path, snapshot_path, keep_previous=False)
    # Seed files wait for the weekly run, whose checks compare a newly seeded
    # parish with its last extracted schedule; a deploy would skip them.
    seeded = {**ensure_db(db_path, load_seeds=False), "migrations_applied": migrations}
    removed_churches = seeded["churches_deleted"] + seeded.get("churches_retired", 0)
    if seeded["parishes_deleted"] or removed_churches:
        # Removing a parish or church deletes its events (or, for a church
        # retired from a believed schedule, its entries). That goes live only
        # through a weekly run a person has reviewed (the run is held for it),
        # never as a side effect of a deploy: keep the published data.
        LOGGER.warning(
            "The CSVs remove %d parishes and %d churches; deploying the published "
            "data unchanged until a reviewed weekly run publishes the removal",
            seeded["parishes_deleted"], removed_churches,
        )
        return {
            "run_id": pulled["run_id"],
            "seeded": seeded,
            "snapshot": {
                **published,
                "source": "published database (CSV removals await a reviewed weekly run)",
            },
        }
    built = extract(db_path, snapshot_path, keep_previous=False)
    return {"run_id": pulled["run_id"], "seeded": seeded, "snapshot": built}
