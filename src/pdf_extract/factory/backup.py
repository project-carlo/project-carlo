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


def backup_ledger(ledger_path: Path, prefix: str, out_dir: Path = DATA / "backups") -> str:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    dest = out_dir / f"factory-{stamp}.db"
    source = sqlite3.connect(ledger_path)
    target = sqlite3.connect(dest)
    try:
        source.backup(target)
    finally:
        target.close()
        source.close()
    remote = remote_from_env()
    if remote is None:
        return f"{dest} (no R2 keys: not uploaded)"
    key = f"{prefix.rstrip('/')}/factory-{stamp}.db"
    remote.put(key, dest.read_bytes(), content_type="application/vnd.sqlite3")
    return f"r2:{key}"
