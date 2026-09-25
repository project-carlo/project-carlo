"""Moving the pipeline database between this checkout and the published copy.

Published data lives in the blob store (R2) under `pipeline/`:

    pipeline/runs/<run_id>/manifest.json         what the run produced (+ hashes)
    pipeline/runs/<run_id>/parish_events.db.gz   the full database after the run
    pipeline/runs/<run_id>/frontend.snapshot     what the website serves
    pipeline/runs/<run_id>/report.md|report.json the run's change report
    pipeline/latest.json                         pointer to the published run

A run's objects are written once and never changed. Publishing is moving the
`latest.json` pointer, so rolling back is pointing it at an earlier run.
Only the weekly job has credentials to write; everyone else pulls.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import logging
import sqlite3
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from pdf_extract.blobstore import (
    BlobStoreError,
    CachedBlobStore,
    bulletin_pdf_key,
    get_store,
)
from pdf_extract.db import import_legacy_json
from pdf_extract.paths import DATA_DIR, ROOT
from pdf_extract.recurrence import history_from_records
from pdf_extract.storage import DEFAULT_DB_PATH, utc_now_iso

LOGGER = logging.getLogger(__name__)

PIPELINE_PREFIX = "pipeline"
LATEST_KEY = f"{PIPELINE_PREFIX}/latest.json"
SNAPSHOT_PATH = ROOT / "apps" / "web" / "public" / "frontend.snapshot"
OUT_DIR = DATA_DIR / "out"
PUBLIC_SNAPSHOT_URL = "https://projectcarlo.com/frontend.snapshot"

LEGACY_FILES = ("data/metadata.json", "data/events.json", "data/event_history.json")


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

    With `public_fallback`, a snapshot-only pull that has no credentials, or
    finds nothing published yet, takes the snapshot the live site is serving,
    so a deploy keeps showing the current data rather than failing.
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
            if snapshot_only and public_fallback:
                LOGGER.warning("Nothing published to R2 yet; using the live site's snapshot")
                return _pull_public_snapshot(snapshot_path)
            raise BlobStoreError(
                f"Nothing published yet ({LATEST_KEY} not found). Publish a run with the "
                "Publish Data Run workflow, or run Weekly Data Refresh with bootstrap."
            )
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
    if data[:2] != b"\x1f\x8b":
        raise BlobStoreError(f"{PUBLIC_SNAPSHOT_URL} did not return a gzip snapshot")
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
    snapshot_path = snapshot_path or out / "frontend.snapshot"

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
        "snapshot_key": run_key(run_id, "frontend.snapshot"),
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


def build_deploy_snapshot(
    *,
    snapshot_path: Path = SNAPSHOT_PATH,
    db_path: Path = DEFAULT_DB_PATH,
    public_fallback: bool = False,
) -> dict[str, Any]:
    """The snapshot to deploy, built from the published database by *this* code.

    Building here rather than reusing the published run's snapshot keeps the
    snapshot's format in step with the web code being deployed, and lets
    parishes.csv/churches.csv edits (seeded by `ensure_db`) show up in a
    preview and on merge without waiting for the next weekly run.
    """
    # Imported here: db and extract_frontend_db import this module's neighbours.
    from pdf_extract.db import ensure_db
    from pdf_extract.extract_frontend_db import extract

    store = get_store()
    if not store.is_remote or store.get_remote(LATEST_KEY) is None:
        if not public_fallback:
            raise BlobStoreError("Nothing published to build a snapshot from")
        LOGGER.warning("No published database; using the live site's snapshot")
        return _pull_public_snapshot(snapshot_path)

    pulled = pull(db=True, snapshot=False, db_path=db_path)
    seeded = ensure_db(db_path)
    built = extract(db_path, snapshot_path, keep_previous=False)
    return {"run_id": pulled["run_id"], "seeded": seeded, "snapshot": built}


# ── One-time migration helpers ──────────────────────────────────────────────
def import_legacy(
    *, git_ref: str | None = None, source_dir: Path | None = None,
    db_path: Path = DEFAULT_DB_PATH, force: bool = False,
) -> dict[str, Any]:
    """Build the database from the JSON files the repository used to commit.

    Reads them from a git revision (`git_ref`) or a directory holding
    metadata.json, events.json and event_history.json.

    Refuses when R2 already has a published run (unless `force`): the legacy
    files are frozen, so importing them again would roll back every bulletin,
    event and run record added since.
    """
    if (git_ref is None) == (source_dir is None):
        raise ValueError("Pass exactly one of git_ref or source_dir")
    store = get_store()
    if not force and store.is_remote and store.get_remote(LATEST_KEY) is not None:
        raise BlobStoreError(
            "A run is already published; importing the legacy JSON would replace it with "
            "older data. Pull the published database instead (or pass --force)."
        )

    def load(name: str) -> list[Any]:
        if source_dir is not None:
            path = source_dir / Path(name).name
            return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        completed = subprocess.run(
            ["git", "show", f"{git_ref}:{name}"],
            capture_output=True, text=True, check=False, cwd=ROOT,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"git show {git_ref}:{name} failed: {completed.stderr.strip()}")
        return json.loads(completed.stdout)

    metadata, events, history = (load(name) for name in LEGACY_FILES)
    stats = import_legacy_json(
        db_path, metadata=metadata, events=events, history=history_from_records(history),
    )
    return {"source": git_ref or str(source_dir), **stats}


def upload_bulletins(bulletins_dir: Path = DATA_DIR / "bulletins") -> dict[str, int]:
    """Upload local bulletin PDFs the bucket does not have yet.

    For moving PDFs that were only ever fetched on one machine into shared
    storage. Needs write credentials and CARLO_REMOTE_WRITE=1.
    """
    store = get_store()
    if not store.remote_write:
        raise BlobStoreError("Uploading needs R2 write credentials and CARLO_REMOTE_WRITE=1")
    assert store.remote is not None
    uploaded = present = skipped = 0
    for path in sorted(bulletins_dir.glob("*/*.pdf")):
        content_hash = path.stem
        if len(content_hash) != 64 or not all(c in "0123456789abcdef" for c in content_hash):
            skipped += 1  # truncated copies and anything not named by its hash
            continue
        key = bulletin_pdf_key(path.parent.name, content_hash)
        if store.remote.exists(key):
            present += 1
            continue
        data = path.read_bytes()
        if _sha256(data) != content_hash:
            LOGGER.warning("Skipping %s: contents do not match its name", path)
            skipped += 1
            continue
        store.remote.put(key, data, content_type="application/pdf")
        uploaded += 1
    return {"uploaded": uploaded, "already_present": present, "skipped": skipped}
