"""The nightly ledger backup: SQLite's online backup, uploaded to R2.

Losing the ledger loses only history, costs and transcripts; the work is in git.
Uploading needs R2 keys that can write (the ones `pnpm data:push` uses).
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from pdf_extract.blobstore import remote_from_env
from pdf_extract.factory.config import DATA


def copy_database(source: Path, dest: Path) -> None:
    """SQLite's online backup, not a file copy: a database in WAL mode keeps recent
    commits in its -wal file, and a copy can catch a write halfway."""
    for stale in (dest, dest.with_name(dest.name + "-wal"), dest.with_name(dest.name + "-shm")):
        stale.unlink(missing_ok=True)
    src, out = sqlite3.connect(source), sqlite3.connect(dest)
    try:
        src.backup(out)
    finally:
        out.close()
        src.close()


def backup_ledger(ledger_path: Path, prefix: str, out_dir: Path = DATA / "backups") -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    dest = out_dir / f"factory-{stamp}.db"
    copy_database(ledger_path, dest)
    remote = remote_from_env()
    if remote is None:
        return f"{dest} (no R2 keys: not uploaded)"
    key = f"{prefix.rstrip('/')}/factory-{stamp}.db"
    remote.put(key, dest.read_bytes(), content_type="application/vnd.sqlite3")
    return f"r2:{key}"
