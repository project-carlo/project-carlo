"""Rewrite bulletin PDFs that were stored before compaction existed.

`fetch` hashes the download and stores a compacted copy under that hash
(`bulletins/<parish>/<sha256>.pdf`). Labels, bulletin rows and classifier
caches all use the hash, never a hash of the stored bytes, so replacing the
object in place keeps them valid. Fetch itself will not do it: an existing
key is left alone.

The cutoff is the commit that turned compaction on (`fda42b0`, 2026-09-25
20:59:33 UTC). Objects last written earlier are the pre-compaction set.
Later fetches already ran `compact_bulletin_pdf`; running it again would
recompress JPEGs. Pass `--cutoff` if a fetch without Ghostscript stored a
full-size PDF after that.

The default is a dry run. `--apply` needs the write token and
`CARLO_REMOTE_WRITE=1`. It saves each original under the backup directory,
overwrites the same key, reads the object back, and puts the original back
if the read does not match. It also replaces this machine's local cache file
so the cache does not keep serving the old bytes.
"""

from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from pdf_extract.blobstore import BlobStoreError, CachedBlobStore, bulletin_pdf_key
from pdf_extract.labeling.labels import LABELS_DIR, is_valid_hash, is_valid_slug, read_label
from pdf_extract.paths import DATA_DIR
from pdf_extract.pdf_compact import compact_bulletin_pdf
from pdf_extract.pdf_truncate import MAX_BULLETIN_PAGES

LOGGER = logging.getLogger(__name__)

# fetch started storing compacted bytes in fda42b0, committed at this time.
COMPACTION_CUTOFF = datetime(2026, 9, 25, 20, 59, 33, tzinfo=UTC)
BACKUP_DIR = DATA_DIR / "bulletin-precompact"
BULLETINS_PREFIX = "bulletins/"


@dataclass
class _Plan:
    key: str
    parish_slug: str
    content_hash: str
    last_modified: str
    size: int
    action: str
    reason: str
    original_pages: int | None = None
    compacted_pages: int | None = None
    compacted_size: int | None = None
    has_label: bool = False
    label_max_page: int | None = None
    original: bytes | None = None
    compacted: bytes | None = None

    def public(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "parish_slug": self.parish_slug,
            "content_hash": self.content_hash,
            "last_modified": self.last_modified,
            "size": self.size,
            "action": self.action,
            "reason": self.reason,
            "original_pages": self.original_pages,
            "compacted_pages": self.compacted_pages,
            "compacted_size": self.compacted_size,
            "has_label": self.has_label,
            "label_max_page": self.label_max_page,
        }


def parse_cutoff(value: str) -> datetime:
    """An ISO-8601 timestamp, interpreted as UTC when it carries no offset."""
    text = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def parse_bulletin_pdf_key(key: str) -> tuple[str, str] | None:
    """`(parish_slug, content_hash)` for a stored bulletin, else None."""
    parts = key.split("/")
    if len(parts) != 3 or parts[0] != "bulletins" or not parts[2].endswith(".pdf"):
        return None
    slug, content_hash = parts[1], parts[2][:-4]
    if not (is_valid_slug(slug) and is_valid_hash(content_hash)):
        return None
    return slug, content_hash


def _page_count(data: bytes) -> int:
    return len(PdfReader(BytesIO(data)).pages)


def _label_pages(label: dict[str, Any]) -> list[int]:
    events = label.get("events")
    if not isinstance(events, list):
        raise ValueError("label events is not a list")
    pages: list[int] = []
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("label event is not an object")
        page = event.get("page_number")
        if page is None:
            continue
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError(f"label page_number is invalid: {page!r}")
        pages.append(page)
    return pages


def _plan_bytes(
    data: bytes,
    *,
    key: str,
    parish_slug: str,
    content_hash: str,
    last_modified: str,
    labels_dir: Path,
) -> _Plan:
    """What to do with one stored PDF. `replace` only when the result is safe to store."""
    base = _Plan(
        key=key, parish_slug=parish_slug, content_hash=content_hash,
        last_modified=last_modified, size=len(data), action="keep", reason="",
        original=data,
    )
    try:
        label = read_label(parish_slug, content_hash, labels_dir)
    except (OSError, ValueError) as exc:
        base.action = "skip"
        base.reason = f"label file cannot be read: {exc}"
        return base
    if label is not None:
        base.has_label = True
        try:
            pages = _label_pages(label)
        except ValueError as exc:
            base.action = "skip"
            base.reason = str(exc)
            return base
        base.label_max_page = max(pages) if pages else None

    try:
        original_pages = _page_count(data)
    except Exception:
        LOGGER.warning("Leaving unreadable PDF in place: %s", key, exc_info=True)
        base.action = "keep"
        base.reason = "stored PDF does not open"
        return base
    base.original_pages = original_pages

    compacted = compact_bulletin_pdf(data)
    expected = min(original_pages, MAX_BULLETIN_PAGES)
    if compacted is data or len(compacted) >= len(data):
        base.compacted_pages = original_pages
        base.compacted_size = len(data)
        base.action = "keep"
        base.reason = "compaction would not shrink the file"
        return base
    try:
        compacted_pages = _page_count(compacted)
    except Exception:
        LOGGER.warning("Discarding unreadable compacted PDF: %s", key, exc_info=True)
        base.action = "skip"
        base.reason = "compacted PDF does not open"
        return base
    base.compacted = compacted
    base.compacted_pages = compacted_pages
    base.compacted_size = len(compacted)
    if compacted_pages != expected:
        base.action = "skip"
        base.reason = f"compacted PDF has {compacted_pages} pages, expected {expected}"
        base.compacted = None
        return base
    if base.label_max_page is not None and base.label_max_page > compacted_pages:
        base.action = "skip"
        base.reason = (
            f"label cites page {base.label_max_page}, compacted PDF has {compacted_pages}"
        )
        base.compacted = None
        return base
    base.action = "replace"
    base.reason = f"{len(data)} bytes -> {len(compacted)} bytes, {compacted_pages} pages"
    return base


def _read(store: CachedBlobStore, key: str) -> bytes | None:
    """The remote object when R2 is configured, so a stale local cache is not compacted."""
    if store.remote is not None:
        return store.remote.get(key)
    return store.local.get(key)


def _write_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _drop_local_sidecar(store: CachedBlobStore, key: str) -> None:
    """Remove a read-time truncation leftover so it cannot outlive the rewritten PDF."""
    path = store.local.path(key)
    sidecar = path.with_name(f"{path.stem}-truncated{path.suffix}")
    sidecar.unlink(missing_ok=True)


def _replace_one(store: CachedBlobStore, plan: _Plan, backup_dir: Path) -> _Plan:
    assert plan.original is not None and plan.compacted is not None
    backup = backup_dir / plan.parish_slug / f"{plan.content_hash}.pdf"
    _write_file(backup, plan.original)
    try:
        store.put_remote(plan.key, plan.compacted, content_type="application/pdf")
        stored = store.get_remote(plan.key)
    except BlobStoreError as exc:
        plan.action = "failed"
        plan.reason = f"upload failed after backup {backup}: {exc}"
        return plan
    if stored != plan.compacted:
        restored = _restore_remote(store, plan.key, plan.original)
        plan.action = "failed"
        plan.reason = (
            "uploaded bytes did not match; original restored"
            if restored
            else f"uploaded bytes did not match; restore failed, backup is {backup}"
        )
        return plan
    store.local.put(plan.key, plan.compacted)
    _drop_local_sidecar(store, plan.key)
    plan.action = "replaced"
    plan.original = None
    plan.compacted = None
    return plan


def _restore_remote(store: CachedBlobStore, key: str, data: bytes) -> bool:
    try:
        store.put_remote(key, data, content_type="application/pdf")
        return store.get_remote(key) == data
    except BlobStoreError:
        LOGGER.warning("Failed to restore %s", key, exc_info=True)
        return False


def _summarize(
    *,
    mode: str,
    cutoff: datetime | None,
    backup_dir: Path,
    listed: int,
    ignored: int,
    plans: list[_Plan],
) -> dict[str, Any]:
    counts = {"replace": 0, "replaced": 0, "restored": 0, "keep": 0, "skip": 0, "failed": 0}
    bytes_before = 0
    bytes_after = 0
    labeled: list[dict[str, Any]] = []
    for plan in plans:
        counts[plan.action] = counts.get(plan.action, 0) + 1
        if plan.action in {"replace", "replaced"}:
            bytes_before += plan.size
            bytes_after += plan.compacted_size or 0
        if plan.has_label:
            labeled.append({
                "parish_slug": plan.parish_slug,
                "content_hash": plan.content_hash,
                "action": plan.action,
                "label_max_page": plan.label_max_page,
                "reason": plan.reason,
            })
    return {
        "mode": mode,
        "cutoff": None if cutoff is None else cutoff.isoformat(),
        "backup_dir": str(backup_dir),
        "listed": listed,
        "ignored": ignored,
        "candidates": len(plans),
        "replace": counts["replace"],
        "replaced": counts["replaced"],
        "restored": counts["restored"],
        "keep": counts["keep"],
        "skip": counts["skip"],
        "failed": counts["failed"],
        "bytes_before": bytes_before,
        "bytes_after": bytes_after,
        "bytes_saved": bytes_before - bytes_after,
        "labeled": labeled,
        "items": [plan.public() for plan in plans],
    }


def _require_ghostscript() -> None:
    if shutil.which("gs") is None:
        raise RuntimeError(
            "Ghostscript (gs) is not installed. Without it, compaction only truncates "
            "past page 10 and leaves images at full size."
        )


def _require_write(store: CachedBlobStore) -> None:
    if not store.remote_write:
        raise BlobStoreError(
            "Remote writes are disabled. The dry run needs only read keys. "
            "To replace objects, set the write token and CARLO_REMOTE_WRITE=1."
        )


def compact_bulletins(
    store: CachedBlobStore,
    *,
    apply: bool = False,
    restore: bool = False,
    backup_dir: Path = BACKUP_DIR,
    labels_dir: Path = LABELS_DIR,
    cutoff: datetime = COMPACTION_CUTOFF,
    require_ghostscript: bool = True,
) -> dict[str, Any]:
    """Dry-run, apply, or restore pre-compaction bulletin PDFs."""
    if restore:
        _require_write(store)
        return _restore(store, backup_dir)
    if require_ghostscript:
        _require_ghostscript()
    if apply:
        _require_write(store)

    source = store.remote if store.remote is not None else store.local
    plans: list[_Plan] = []
    listed = 0
    ignored = 0
    for info in source.list_stats(BULLETINS_PREFIX):
        listed += 1
        parsed = parse_bulletin_pdf_key(info.key)
        modified = info.last_modified
        if modified.tzinfo is None:
            modified = modified.replace(tzinfo=UTC)
        if parsed is None:
            ignored += 1
            continue
        if modified.astimezone(UTC) >= cutoff:
            continue
        parish_slug, content_hash = parsed
        LOGGER.info("Reading %s (%d bytes, %s)", info.key, info.size, modified.isoformat())
        try:
            data = _read(store, info.key)
        except BlobStoreError as exc:
            plans.append(_Plan(
                key=info.key, parish_slug=parish_slug, content_hash=content_hash,
                last_modified=modified.isoformat(), size=info.size,
                action="failed", reason=f"download failed: {exc}",
            ))
            continue
        if data is None:
            plans.append(_Plan(
                key=info.key, parish_slug=parish_slug, content_hash=content_hash,
                last_modified=modified.isoformat(), size=info.size,
                action="failed", reason="object disappeared while reading",
            ))
            continue
        plan = _plan_bytes(
            data, key=info.key, parish_slug=parish_slug, content_hash=content_hash,
            last_modified=modified.isoformat(), labels_dir=labels_dir,
        )
        LOGGER.info("%s %s: %s", plan.action, plan.key, plan.reason)
        if apply and plan.action == "replace":
            plan = _replace_one(store, plan, backup_dir)
            if plan.action == "replaced":
                _record_manifest(backup_dir, plan)
            LOGGER.info("%s %s: %s", plan.action, plan.key, plan.reason)
        plan.original = None
        plan.compacted = None
        plans.append(plan)

    plans.sort(key=lambda plan: (plan.parish_slug, plan.content_hash))
    return _summarize(
        mode="apply" if apply else "dry-run",
        cutoff=cutoff,
        backup_dir=backup_dir,
        listed=listed,
        ignored=ignored,
        plans=plans,
    )


def _record_manifest(backup_dir: Path, plan: _Plan) -> None:
    path = backup_dir / "manifest.json"
    existing: list[dict[str, Any]] = []
    if path.is_file():
        existing = json.loads(path.read_text(encoding="utf-8"))
    existing.append({
        **plan.public(),
        "backup": f"{plan.parish_slug}/{plan.content_hash}.pdf",
    })
    _write_file(path, (json.dumps(existing, indent=2) + "\n").encode("utf-8"))


def _restore(store: CachedBlobStore, backup_dir: Path) -> dict[str, Any]:
    if not backup_dir.is_dir():
        raise FileNotFoundError(f"No backup directory: {backup_dir}")
    plans: list[_Plan] = []
    for path in sorted(backup_dir.glob("*/*.pdf")):
        parsed = parse_bulletin_pdf_key(bulletin_pdf_key(path.parent.name, path.stem))
        if parsed is None:
            LOGGER.warning("Skipping backup that is not a bulletin key: %s", path)
            continue
        parish_slug, content_hash = parsed
        key = bulletin_pdf_key(parish_slug, content_hash)
        data = path.read_bytes()
        plan = _Plan(
            key=key, parish_slug=parish_slug, content_hash=content_hash,
            last_modified="", size=len(data), action="restored", reason=f"restored from {path}",
        )
        try:
            store.put_remote(key, data, content_type="application/pdf")
            stored = store.get_remote(key)
        except BlobStoreError as exc:
            plan.action = "failed"
            plan.reason = f"restore failed: {exc}"
            plans.append(plan)
            continue
        if stored != data:
            plan.action = "failed"
            plan.reason = "restored bytes did not match the backup"
            plans.append(plan)
            continue
        store.local.put(key, data)
        _drop_local_sidecar(store, key)
        plans.append(plan)
        LOGGER.info("Restored %s (%d bytes)", key, len(data))
    return _summarize(
        mode="restore", cutoff=None, backup_dir=backup_dir,
        listed=len(plans), ignored=0, plans=plans,
    )
