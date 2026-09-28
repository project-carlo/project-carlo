from collections.abc import Iterator
from pathlib import Path
from typing import Any

import boto3
import pytest
from moto import mock_aws

from pdf_extract.blobstore import (
    DEFAULT_BUCKET,
    BlobStoreError,
    CachedBlobStore,
    LocalBlobStore,
    S3BlobStore,
    bulletin_pdf_key,
    remote_from_env,
)

BUCKET = "test-bucket"


@pytest.fixture
def s3_client() -> Iterator[Any]:
    with mock_aws():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket=BUCKET)
        yield client


class _SmallPages:
    """Client wrapper whose list_objects_v2 paginator returns two keys per page."""

    def __init__(self, client: Any) -> None:
        self._client = client
        self.pages = 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self._client, name)

    def get_paginator(self, name: str) -> Any:
        paginator = self._client.get_paginator(name)
        outer = self

        class _Paginator:
            def paginate(self, **kwargs: Any) -> Iterator[dict[str, Any]]:
                for page in paginator.paginate(PaginationConfig={"PageSize": 2}, **kwargs):
                    outer.pages += 1
                    yield page

        return _Paginator()


# ── Keys ────────────────────────────────────────────────────────────────────
def test_bulletin_pdf_key_format() -> None:
    assert bulletin_pdf_key("st-monica", "abc123") == "bulletins/st-monica/abc123.pdf"


# ── LocalBlobStore ──────────────────────────────────────────────────────────
def test_local_store_put_get_exists(tmp_path: Path) -> None:
    store = LocalBlobStore(tmp_path)

    assert store.get("a/b.txt") is None
    assert not store.exists("a/b.txt")

    store.put("a/b.txt", b"hello")

    assert store.get("a/b.txt") == b"hello"
    assert store.exists("a/b.txt")
    assert (tmp_path / "a" / "b.txt").read_bytes() == b"hello"


def test_local_store_put_overwrites_and_leaves_no_temp_files(tmp_path: Path) -> None:
    store = LocalBlobStore(tmp_path)
    store.put("k.bin", b"one")
    store.put("k.bin", b"two")

    assert store.get("k.bin") == b"two"
    assert [p.name for p in tmp_path.iterdir()] == ["k.bin"]


def test_local_store_list_stats_reports_size_and_utc_mtime(tmp_path: Path) -> None:
    store = LocalBlobStore(tmp_path)
    store.put("bulletins/p/a.pdf", b"abc")
    (tmp_path / "bulletins" / "p" / ".hidden").write_bytes(b"nope")

    [info] = list(store.list_stats("bulletins/"))

    assert info.key == "bulletins/p/a.pdf"
    assert info.size == 3
    assert info.last_modified.tzinfo is not None


def test_cached_store_list_stats_reads_the_remote_when_there_is_one(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    local.put("bulletins/p/local.pdf", b"local")
    remote.put("bulletins/p/remote.pdf", b"remote-bytes")
    store = CachedBlobStore(local, remote)

    [info] = list(store.list_stats("bulletins/"))

    assert info.key == "bulletins/p/remote.pdf"
    assert info.size == len(b"remote-bytes")


def test_local_store_list_filters_by_prefix_and_skips_hidden_files(tmp_path: Path) -> None:
    store = LocalBlobStore(tmp_path)
    store.put("bulletins/p1/a.pdf", b"a")
    store.put("bulletins/p2/b.pdf", b"b")
    store.put("pipeline/latest.json", b"{}")
    (tmp_path / "bulletins" / "p1" / ".partial.tmp").write_bytes(b"x")

    assert list(store.list("bulletins/")) == ["bulletins/p1/a.pdf", "bulletins/p2/b.pdf"]
    assert list(store.list("pipeline/")) == ["pipeline/latest.json"]
    assert list(store.list("nothing/")) == []


def test_local_store_exists_is_false_for_directories(tmp_path: Path) -> None:
    store = LocalBlobStore(tmp_path)
    store.put("dir/file", b"x")

    assert not store.exists("dir")


@pytest.mark.parametrize("key", ["../x", "a/../../x", "/abs", "a\\b", ""])
def test_local_store_rejects_bad_keys(tmp_path: Path, key: str) -> None:
    store = LocalBlobStore(tmp_path)

    with pytest.raises(ValueError, match="Invalid blob key"):
        store.get(key)
    with pytest.raises(ValueError, match="Invalid blob key"):
        store.put(key, b"x")
    with pytest.raises(ValueError, match="Invalid blob key"):
        store.exists(key)


# ── CachedBlobStore ─────────────────────────────────────────────────────────
def test_cached_store_reads_through_and_copies_remote_hit_locally(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    remote.put("bulletins/p/h.pdf", b"pdf")
    store = CachedBlobStore(local, remote)

    assert store.get("bulletins/p/h.pdf") == b"pdf"
    assert local.get("bulletins/p/h.pdf") == b"pdf"
    assert store.get("missing") is None
    assert not local.exists("missing")


def test_cached_store_prefers_local_copy(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    local.put("k", b"local")
    remote.put("k", b"remote")

    assert CachedBlobStore(local, remote).get("k") == b"local"


def test_cached_store_without_remote_is_local_only(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    store = CachedBlobStore(local, remote_write=True)

    store.put("k", b"v")

    assert not store.is_remote
    assert not store.remote_write
    assert store.get("k") == b"v"
    assert store.exists("k")
    assert list(store.list("")) == ["k"]
    with pytest.raises(BlobStoreError):
        store.get_remote("k")


def test_cached_store_put_writes_remote_only_when_enabled(tmp_path: Path) -> None:
    remote = LocalBlobStore(tmp_path / "remote")

    read_only = CachedBlobStore(LocalBlobStore(tmp_path / "ro"), remote)
    read_only.put("a", b"1")
    assert read_only.local.get("a") == b"1"
    assert remote.get("a") is None

    writable = CachedBlobStore(LocalBlobStore(tmp_path / "rw"), remote, remote_write=True)
    writable.put("b", b"2")
    assert writable.local.get("b") == b"2"
    assert remote.get("b") == b"2"


def test_cached_store_put_remote_requires_remote_write(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")

    with pytest.raises(BlobStoreError, match="Remote writes are disabled"):
        CachedBlobStore(local, remote).put_remote("k", b"v")
    assert remote.get("k") is None

    CachedBlobStore(local, remote, remote_write=True).put_remote("k", b"v")
    assert remote.get("k") == b"v"
    assert local.get("k") is None


def test_cached_store_get_remote_bypasses_local_cache(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    local.put("pointer", b"stale")
    remote.put("pointer", b"fresh")

    assert CachedBlobStore(local, remote).get_remote("pointer") == b"fresh"


def test_cached_store_exists_checks_local_then_remote(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    local.put("l", b"1")
    remote.put("r", b"2")
    store = CachedBlobStore(local, remote)

    assert store.exists("l")
    assert store.exists("r")
    assert not store.exists("neither")


def test_cached_store_lists_remote_when_configured(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    local.put("x/local-only", b"1")
    remote.put("x/remote-only", b"2")

    assert list(CachedBlobStore(local, remote).list("x/")) == ["x/remote-only"]


def test_cached_store_local_path_downloads(tmp_path: Path) -> None:
    local = LocalBlobStore(tmp_path / "local")
    remote = LocalBlobStore(tmp_path / "remote")
    remote.put("bulletins/p/h.pdf", b"pdf")
    store = CachedBlobStore(local, remote)

    path = store.local_path("bulletins/p/h.pdf")

    assert path == tmp_path / "local" / "bulletins" / "p" / "h.pdf"
    assert path.read_bytes() == b"pdf"
    assert store.local_path("bulletins/p/missing.pdf") is None


# ── S3BlobStore (moto) ──────────────────────────────────────────────────────
def test_s3_store_get_missing_returns_none(s3_client: Any) -> None:
    store = S3BlobStore(bucket=BUCKET, client=s3_client)

    assert store.get("nope") is None
    assert not store.exists("nope")


def test_s3_store_put_get_exists(s3_client: Any) -> None:
    store = S3BlobStore(bucket=BUCKET, client=s3_client)

    store.put("pipeline/latest.json", b"{}", content_type="application/json")

    assert store.get("pipeline/latest.json") == b"{}"
    assert store.exists("pipeline/latest.json")
    head = s3_client.head_object(Bucket=BUCKET, Key="pipeline/latest.json")
    assert head["ContentType"] == "application/json"


def test_s3_store_rejects_bad_keys_without_writing(s3_client: Any) -> None:
    store = S3BlobStore(bucket=BUCKET, client=s3_client)

    # The key check runs inside the client-call try block, so the ValueError
    # surfaces wrapped in a BlobStoreError.
    with pytest.raises(BlobStoreError, match="Invalid blob key"):
        store.put("../escape", b"x")
    with pytest.raises(BlobStoreError, match="Invalid blob key"):
        store.get("/abs")
    assert s3_client.list_objects_v2(Bucket=BUCKET).get("KeyCount") == 0


def test_s3_store_errors_other_than_missing_raise_blobstore_error(s3_client: Any) -> None:
    store = S3BlobStore(bucket="no-such-bucket", client=s3_client)

    with pytest.raises(BlobStoreError):
        store.put("k", b"v")
    with pytest.raises(BlobStoreError):
        store.get("k")
    with pytest.raises(BlobStoreError):
        list(store.list(""))


def test_s3_store_list_stats_includes_size_and_last_modified(s3_client: Any) -> None:
    store = S3BlobStore(bucket=BUCKET, client=s3_client)
    store.put("bulletins/p/a.pdf", b"hello")

    [info] = list(store.list_stats("bulletins/"))

    assert info.key == "bulletins/p/a.pdf"
    assert info.size == 5
    assert info.last_modified.tzinfo is not None


def test_s3_store_list_follows_pagination(s3_client: Any) -> None:
    client = _SmallPages(s3_client)
    store = S3BlobStore(bucket=BUCKET, client=client)
    keys = [f"runs/r{i}/file" for i in range(5)]
    for key in keys:
        store.put(key, b"x")
    store.put("other/file", b"x")

    assert sorted(store.list("runs/")) == keys
    assert client.pages >= 3


# ── Configuration ───────────────────────────────────────────────────────────
def test_remote_from_env_without_credentials_is_none() -> None:
    assert remote_from_env({}) is None
    assert remote_from_env({"R2_ACCESS_KEY_ID": "a", "R2_SECRET_ACCESS_KEY": "b"}) is None
    assert remote_from_env({"R2_ACCOUNT_ID": "acct", "R2_ACCESS_KEY_ID": "a"}) is None


def test_remote_from_env_reads_process_environment_when_no_env_given() -> None:
    # conftest removes every R2_* variable.
    assert remote_from_env() is None


def test_remote_from_env_with_endpoint_url() -> None:
    store = remote_from_env({
        "R2_ACCESS_KEY_ID": "a",
        "R2_SECRET_ACCESS_KEY": "b",
        "R2_ENDPOINT_URL": "http://localhost:9000",
    })

    assert isinstance(store, S3BlobStore)
    assert store.bucket == DEFAULT_BUCKET == "project-carlo-data"
    assert store.client.meta.endpoint_url == "http://localhost:9000"


def test_remote_from_env_with_account_id_and_bucket() -> None:
    store = remote_from_env({
        "R2_ACCOUNT_ID": "acct",
        "R2_ACCESS_KEY_ID": "a",
        "R2_SECRET_ACCESS_KEY": "b",
        "R2_BUCKET": "other-bucket",
    })

    assert isinstance(store, S3BlobStore)
    assert store.bucket == "other-bucket"
    assert store.client.meta.endpoint_url == "https://acct.r2.cloudflarestorage.com"
