"""Content storage for bulletin PDFs, extraction results and published data.

Everything the pipeline keeps as a file lives under a key such as
`bulletins/<parish>/<sha256>.pdf`. Locally a key is simply a path under
`data/`, so a checkout that has never been configured for R2 keeps working on
its own files exactly as before. When R2 credentials are present, the local
directory becomes a read-through cache in front of the bucket: a miss is
downloaded once and kept.

Writes to the bucket are opt-in (`CARLO_REMOTE_WRITE=1`). The weekly job sets
it; laptops and agent sessions normally hold read-only credentials and never
write shared state by accident, even when they run `fetch` or `process`
against their own copy of the data.

Environment:

- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`: enable R2.
- `R2_BUCKET`: bucket name (default `project-carlo-data`).
- `R2_ENDPOINT_URL`: override the endpoint (tests, or another S3 store).
- `CARLO_REMOTE_WRITE`: `1` to write through to the bucket.
"""

from __future__ import annotations

import logging
import os
import threading
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from pdf_extract.paths import DATA_DIR

LOGGER = logging.getLogger(__name__)

DEFAULT_BUCKET = "project-carlo-data"


class BlobStoreError(RuntimeError):
    """A remote store failed for a reason other than the key being absent."""


class BlobStore(Protocol):
    def get(self, key: str) -> bytes | None: ...

    def put(self, key: str, data: bytes, *, content_type: str | None = None) -> None: ...

    def exists(self, key: str) -> bool: ...

    def list(self, prefix: str) -> Iterator[str]: ...


# ── Keys ────────────────────────────────────────────────────────────────────
def bulletin_pdf_key(parish_slug: str, content_hash: str) -> str:
    """Where a fetched bulletin lives. Content-addressed, so never overwritten."""
    return f"bulletins/{parish_slug}/{content_hash}.pdf"


def _check_key(key: str) -> str:
    if not key or key.startswith("/") or "\\" in key or ".." in key.split("/"):
        raise ValueError(f"Invalid blob key: {key!r}")
    return key


# ── Local filesystem ────────────────────────────────────────────────────────
@dataclass
class LocalBlobStore:
    root: Path

    def path(self, key: str) -> Path:
        return self.root / _check_key(key)

    def get(self, key: str) -> bytes | None:
        path = self.path(key)
        try:
            return path.read_bytes()
        except FileNotFoundError:
            return None

    def put(self, key: str, data: bytes, *, content_type: str | None = None) -> None:
        path = self.path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Write-then-rename so a crash never leaves a truncated blob behind a
        # key that readers treat as complete.
        tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}-{threading.get_ident()}")
        tmp.write_bytes(data)
        tmp.replace(path)

    def exists(self, key: str) -> bool:
        return self.path(key).is_file()

    def list(self, prefix: str) -> Iterator[str]:
        base = self.root
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.name.startswith("."):
                continue
            key = path.relative_to(base).as_posix()
            if key.startswith(prefix):
                yield key


# ── S3-compatible (Cloudflare R2) ───────────────────────────────────────────
class S3BlobStore:
    def __init__(self, *, bucket: str, client: Any) -> None:
        self.bucket = bucket
        self.client = client

    def _is_missing(self, exc: Exception) -> bool:
        response = getattr(exc, "response", None) or {}
        code = str(response.get("Error", {}).get("Code", ""))
        return code in {"NoSuchKey", "404", "NotFound"}

    def get(self, key: str) -> bytes | None:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=_check_key(key))
        except Exception as exc:
            if self._is_missing(exc):
                return None
            raise BlobStoreError(f"Reading {key} from bucket {self.bucket} failed: {exc}") from exc
        return response["Body"].read()

    def put(self, key: str, data: bytes, *, content_type: str | None = None) -> None:
        extra = {"ContentType": content_type} if content_type else {}
        try:
            self.client.put_object(Bucket=self.bucket, Key=_check_key(key), Body=data, **extra)
        except Exception as exc:
            raise BlobStoreError(f"Writing {key} to bucket {self.bucket} failed: {exc}") from exc

    def exists(self, key: str) -> bool:
        try:
            self.client.head_object(Bucket=self.bucket, Key=_check_key(key))
        except Exception as exc:
            if self._is_missing(exc):
                return False
            raise BlobStoreError(f"Checking {key} in bucket {self.bucket} failed: {exc}") from exc
        return True

    def list(self, prefix: str) -> Iterator[str]:
        paginator = self.client.get_paginator("list_objects_v2")
        try:
            for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                for item in page.get("Contents", []):
                    yield item["Key"]
        except Exception as exc:
            raise BlobStoreError(f"Listing {prefix} in bucket {self.bucket} failed: {exc}") from exc


# ── Local cache in front of an optional remote ──────────────────────────────
class CachedBlobStore:
    """Local directory first, then the remote; writes go local and, if enabled, remote.

    Blobs are immutable once written (keys are content hashes or run ids), so
    a local hit never needs revalidating against the remote.
    """

    def __init__(
        self,
        local: LocalBlobStore,
        remote: BlobStore | None = None,
        *,
        remote_write: bool = False,
    ) -> None:
        self.local = local
        self.remote = remote
        self.remote_write = remote_write and remote is not None

    @property
    def is_remote(self) -> bool:
        return self.remote is not None

    def get(self, key: str) -> bytes | None:
        data = self.local.get(key)
        if data is not None or self.remote is None:
            return data
        data = self.remote.get(key)
        if data is not None:
            self.local.put(key, data)
        return data

    def local_path(self, key: str) -> Path | None:
        """A local file holding `key`, downloading it first if needed."""
        if self.get(key) is None:
            return None
        return self.local.path(key)

    def put(self, key: str, data: bytes, *, content_type: str | None = None) -> None:
        self.local.put(key, data)
        if self.remote_write:
            assert self.remote is not None
            self.remote.put(key, data, content_type=content_type)

    def put_remote(self, key: str, data: bytes, *, content_type: str | None = None) -> None:
        """Write to the remote only, failing loudly when it is not writable.

        For publishing, where silently landing only on local disk would look
        like success while nobody else could see the result.
        """
        if not self.remote_write:
            raise BlobStoreError(
                "Remote writes are disabled: set R2 credentials and CARLO_REMOTE_WRITE=1"
            )
        assert self.remote is not None
        self.remote.put(key, data, content_type=content_type)

    def get_remote(self, key: str) -> bytes | None:
        """Read from the remote, bypassing the local cache (for mutable pointers)."""
        if self.remote is None:
            raise BlobStoreError("No remote configured: set the R2_* environment variables")
        return self.remote.get(key)

    def exists(self, key: str) -> bool:
        if self.local.exists(key):
            return True
        return self.remote.exists(key) if self.remote is not None else False

    def list(self, prefix: str) -> Iterator[str]:
        if self.remote is not None:
            return self.remote.list(prefix)
        return self.local.list(prefix)


# ── Configuration ───────────────────────────────────────────────────────────
def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def remote_from_env(env: dict[str, str] | None = None) -> S3BlobStore | None:
    env = dict(os.environ) if env is None else env
    account = env.get("R2_ACCOUNT_ID", "").strip()
    access_key = env.get("R2_ACCESS_KEY_ID", "").strip()
    secret_key = env.get("R2_SECRET_ACCESS_KEY", "").strip()
    endpoint = env.get("R2_ENDPOINT_URL", "").strip()
    if not (access_key and secret_key and (account or endpoint)):
        return None

    import boto3
    from botocore.config import Config

    client = boto3.client(
        "s3",
        endpoint_url=endpoint or f"https://{account}.r2.cloudflarestorage.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=Config(retries={"max_attempts": 5, "mode": "standard"}),
    )
    bucket = env.get("R2_BUCKET", "").strip() or DEFAULT_BUCKET
    return S3BlobStore(bucket=bucket, client=client)


_store: CachedBlobStore | None = None
_store_lock = threading.Lock()


def get_store() -> CachedBlobStore:
    """The process-wide store, built from the environment on first use."""
    global _store
    with _store_lock:
        if _store is None:
            remote = remote_from_env()
            _store = CachedBlobStore(
                LocalBlobStore(DATA_DIR),
                remote,
                remote_write=_truthy(os.environ.get("CARLO_REMOTE_WRITE")),
            )
            LOGGER.debug(
                "Blob store: local=%s remote=%s remote_write=%s",
                DATA_DIR,
                getattr(remote, "bucket", None),
                _store.remote_write,
            )
        return _store


def set_store(store: CachedBlobStore | None) -> None:
    """Replace the process-wide store (tests; None rebuilds from the environment)."""
    global _store
    with _store_lock:
        _store = store
