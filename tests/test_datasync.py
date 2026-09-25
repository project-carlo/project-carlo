import gzip
import hashlib
import json
import sqlite3
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import boto3
import pytest
from moto import mock_aws

from pdf_extract import __main__ as cli
from pdf_extract import datasync
from pdf_extract.blobstore import (
    BlobStoreError,
    CachedBlobStore,
    LocalBlobStore,
    S3BlobStore,
    bulletin_pdf_key,
    set_store,
)
from pdf_extract.datasync import (
    LATEST_KEY,
    import_legacy,
    promote,
    pull,
    push_candidate,
    run_key,
    run_out_dir,
    status,
    upload_bulletins,
)
from pdf_extract.db import create_db
from pdf_extract.storage import DEFAULT_DB_PATH

BUCKET = "carlo-test"
SNAPSHOT_BYTES = gzip.compress(b"snapshot", mtime=0)


@pytest.fixture
def s3_client() -> Iterator[Any]:
    with mock_aws():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket=BUCKET)
        yield client


@pytest.fixture
def remote_store(tmp_path: Path, s3_client: Any) -> CachedBlobStore:
    store = CachedBlobStore(
        LocalBlobStore(tmp_path / "cache"),
        S3BlobStore(bucket=BUCKET, client=s3_client),
        remote_write=True,
    )
    set_store(store)
    return store


def _bucket_keys(client: Any) -> list[str]:
    return sorted(o["Key"] for o in client.list_objects_v2(Bucket=BUCKET).get("Contents", []))


def _prepare_run(
    run_id: str, *, run_status: str = "passed", snapshot: bytes = SNAPSHOT_BYTES,
) -> Path:
    """A database plus the files `weekly` leaves in data/out/<run_id>/."""
    if not DEFAULT_DB_PATH.exists():
        create_db()
    out = run_out_dir(run_id)
    out.mkdir(parents=True, exist_ok=True)
    (out / "frontend.snapshot").write_bytes(snapshot)
    (out / "report.json").write_text(json.dumps({"status": run_status}), encoding="utf-8")
    (out / "report.md").write_text(f"# {run_id}\n", encoding="utf-8")
    return out


def _parish_rows(db_path: Path) -> list[tuple]:
    conn = sqlite3.connect(db_path)
    try:
        return conn.execute("SELECT id, slug, name, homepage_url FROM parish ORDER BY id").fetchall()
    finally:
        conn.close()


# ── Keys ────────────────────────────────────────────────────────────────────
def test_run_key_format() -> None:
    assert run_key("2026-09-25", "manifest.json") == "pipeline/runs/2026-09-25/manifest.json"


@pytest.mark.parametrize("run_id", ["a/b", "", ".hidden", ".."])
def test_run_key_rejects_bad_run_ids(run_id: str) -> None:
    with pytest.raises(ValueError, match="Invalid run id"):
        run_key(run_id, "manifest.json")


# ── Push, promote, pull ─────────────────────────────────────────────────────
def test_push_uploads_run_without_publishing(
    pipeline_dir: Path, remote_store: CachedBlobStore, s3_client: Any,
) -> None:
    _prepare_run("run-1", run_status="held")

    manifest = push_candidate("run-1", git_sha="abc123")

    assert _bucket_keys(s3_client) == sorted(
        run_key("run-1", name)
        for name in (
            "manifest.json", "parish_events.db.gz", "frontend.snapshot",
            "report.md", "report.json",
        )
    )
    assert manifest["status"] == "held"
    assert manifest["git_sha"] == "abc123"
    assert manifest["report_md_key"] == run_key("run-1", "report.md")
    assert manifest["report_json_key"] == run_key("run-1", "report.json")
    assert manifest["snapshot_sha256"] == hashlib.sha256(SNAPSHOT_BYTES).hexdigest()
    stored = json.loads(
        s3_client.get_object(Bucket=BUCKET, Key=run_key("run-1", "manifest.json"))["Body"].read()
    )
    assert stored == manifest
    assert remote_store.get_remote(LATEST_KEY) is None
    # Published objects go to the bucket only, not into the local cache.
    assert not remote_store.local.exists(run_key("run-1", "manifest.json"))


def test_push_without_report_files(
    pipeline_dir: Path, remote_store: CachedBlobStore, s3_client: Any,
) -> None:
    out = _prepare_run("run-1")
    (out / "report.json").unlink()
    (out / "report.md").unlink()

    manifest = push_candidate("run-1")

    assert "status" not in manifest
    assert "report_md_key" not in manifest
    assert run_key("run-1", "report.md") not in _bucket_keys(s3_client)


def test_push_promote_pull_round_trip(
    pipeline_dir: Path, remote_store: CachedBlobStore, tmp_path: Path,
) -> None:
    _prepare_run("run-1")
    push_candidate("run-1")
    pointer = promote("run-1")
    assert pointer["run_id"] == "run-1"
    assert pointer["previous_run_id"] is None

    pulled_db = tmp_path / "pulled" / "parish_events.db"
    pulled_snapshot = tmp_path / "pulled" / "frontend.snapshot"
    result = pull(db_path=pulled_db, snapshot_path=pulled_snapshot)

    assert result == {
        "run_id": "run-1", "db_path": str(pulled_db), "snapshot_path": str(pulled_snapshot),
    }
    assert _parish_rows(pulled_db) == _parish_rows(DEFAULT_DB_PATH)
    conn = sqlite3.connect(pulled_db)
    try:
        assert conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    finally:
        conn.close()
    assert pulled_snapshot.read_bytes() == SNAPSHOT_BYTES


def test_pull_keeps_replaced_database_as_backup(
    pipeline_dir: Path, remote_store: CachedBlobStore, tmp_path: Path,
) -> None:
    _prepare_run("run-1")
    push_candidate("run-1")
    promote("run-1")
    pulled_db = tmp_path / "local.db"
    pulled_db.write_bytes(b"old database")

    pull(db_path=pulled_db, snapshot=False)

    assert (tmp_path / "local.db.bak").read_bytes() == b"old database"
    assert _parish_rows(pulled_db) == _parish_rows(DEFAULT_DB_PATH)


def test_pull_specific_run(
    pipeline_dir: Path, remote_store: CachedBlobStore, tmp_path: Path,
) -> None:
    _prepare_run("run-1", snapshot=gzip.compress(b"one"))
    push_candidate("run-1")
    _prepare_run("run-2", snapshot=gzip.compress(b"two"))
    push_candidate("run-2")
    promote("run-2")
    snapshot_path = tmp_path / "s.snapshot"

    result = pull(run_id="run-1", db=False, snapshot_path=snapshot_path)

    assert result["run_id"] == "run-1"
    assert gzip.decompress(snapshot_path.read_bytes()) == b"one"
    with pytest.raises(BlobStoreError, match="No run run-9"):
        pull(run_id="run-9", db=False, snapshot_path=snapshot_path)


def test_promote_records_previous_run(
    pipeline_dir: Path, remote_store: CachedBlobStore,
) -> None:
    for run_id in ("run-1", "run-2"):
        _prepare_run(run_id)
        push_candidate(run_id)

    promote("run-1")
    pointer = promote("run-2")

    assert pointer["run_id"] == "run-2"
    assert pointer["previous_run_id"] == "run-1"
    latest = json.loads(remote_store.get_remote(LATEST_KEY))
    assert latest["run_id"] == "run-2"
    assert latest["previous_run_id"] == "run-1"
    assert "published_at" in latest


def test_promote_unknown_run_raises(pipeline_dir: Path, remote_store: CachedBlobStore) -> None:
    with pytest.raises(BlobStoreError, match="upload it first"):
        promote("never-uploaded")
    assert remote_store.get_remote(LATEST_KEY) is None


def test_promote_refuses_incomplete_run(
    pipeline_dir: Path, remote_store: CachedBlobStore, s3_client: Any,
) -> None:
    _prepare_run("run-1")
    push_candidate("run-1")
    s3_client.delete_object(Bucket=BUCKET, Key=run_key("run-1", "frontend.snapshot"))

    with pytest.raises(BlobStoreError, match="incomplete"):
        promote("run-1")
    assert remote_store.get_remote(LATEST_KEY) is None


def test_promote_without_remote_write_raises(
    pipeline_dir: Path, remote_store: CachedBlobStore,
) -> None:
    _prepare_run("run-1")
    push_candidate("run-1")
    remote_store.remote_write = False

    with pytest.raises(BlobStoreError, match="Remote writes are disabled"):
        promote("run-1")


def test_pull_detects_tampered_object(
    pipeline_dir: Path, remote_store: CachedBlobStore, s3_client: Any, tmp_path: Path,
) -> None:
    _prepare_run("run-1")
    push_candidate("run-1")
    promote("run-1")
    s3_client.put_object(
        Bucket=BUCKET, Key=run_key("run-1", "parish_events.db.gz"),
        Body=gzip.compress(b"not the database"),
    )
    pulled_db = tmp_path / "pulled.db"

    with pytest.raises(BlobStoreError, match="hash"):
        pull(db_path=pulled_db, snapshot_path=tmp_path / "s.snapshot")
    assert not pulled_db.exists()


def test_pull_detects_missing_object(
    pipeline_dir: Path, remote_store: CachedBlobStore, s3_client: Any, tmp_path: Path,
) -> None:
    _prepare_run("run-1")
    push_candidate("run-1")
    promote("run-1")
    s3_client.delete_object(Bucket=BUCKET, Key=run_key("run-1", "frontend.snapshot"))

    with pytest.raises(BlobStoreError, match="missing"):
        pull(db=False, snapshot_path=tmp_path / "s.snapshot")


def test_pull_with_nothing_published_raises(
    pipeline_dir: Path, remote_store: CachedBlobStore, tmp_path: Path,
) -> None:
    with pytest.raises(BlobStoreError, match="Nothing published"):
        pull(db_path=tmp_path / "x.db", snapshot_path=tmp_path / "s.snapshot")


def test_status_lists_published_and_recent_runs(
    pipeline_dir: Path, remote_store: CachedBlobStore,
) -> None:
    for run_id in ("2026-09-01", "2026-09-08", "2026-09-15"):
        _prepare_run(run_id)
        push_candidate(run_id)
    promote("2026-09-08")

    result = status(limit=2)

    assert result["published"]["run_id"] == "2026-09-08"
    assert result["recent_runs"] == ["2026-09-15", "2026-09-08"]


def test_status_with_empty_bucket(remote_store: CachedBlobStore) -> None:
    assert status() == {"published": None, "recent_runs": []}


# ── Public snapshot fallback ────────────────────────────────────────────────
class _FakeResponse:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *exc: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


@pytest.fixture
def public_site(monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    """Serve SNAPSHOT_BYTES from the live-site URL; returns the requests made."""
    requested: list[Any] = []

    def fake_urlopen(request: Any, timeout: float) -> _FakeResponse:
        requested.append(request)
        return _FakeResponse(SNAPSHOT_BYTES)

    monkeypatch.setattr(datasync.urllib.request, "urlopen", fake_urlopen)
    return requested


def _public_result(snapshot_path: Path) -> dict[str, Any]:
    return {
        "run_id": None, "snapshot_path": str(snapshot_path),
        "source": datasync.PUBLIC_SNAPSHOT_URL,
    }


def test_pull_without_remote_raises_without_public_fallback(
    tmp_path: Path, public_site: list[Any],
) -> None:
    snapshot_path = tmp_path / "s.snapshot"

    with pytest.raises(BlobStoreError, match="No R2 credentials"):
        pull(db_path=tmp_path / "x.db", snapshot_path=snapshot_path)
    with pytest.raises(BlobStoreError, match="No R2 credentials"):
        pull(db=False, snapshot_path=snapshot_path)
    with pytest.raises(BlobStoreError, match="No R2 credentials"):
        pull(db=False, snapshot=False)
    assert public_site == []
    assert not snapshot_path.exists()


def test_pull_without_remote_public_fallback_is_only_for_snapshot_only_pulls(
    tmp_path: Path, public_site: list[Any],
) -> None:
    with pytest.raises(BlobStoreError, match="No R2 credentials"):
        pull(db_path=tmp_path / "x.db", snapshot_path=tmp_path / "s", public_fallback=True)
    with pytest.raises(BlobStoreError, match="No R2 credentials"):
        pull(db_path=tmp_path / "x.db", snapshot=False, public_fallback=True)
    assert public_site == []


def test_pull_without_remote_uses_public_snapshot_with_fallback(
    tmp_path: Path, public_site: list[Any],
) -> None:
    snapshot_path = tmp_path / "public" / "frontend.snapshot"

    result = pull(db=False, snapshot_path=snapshot_path, public_fallback=True)

    assert [r.full_url for r in public_site] == [datasync.PUBLIC_SNAPSHOT_URL]
    assert result == _public_result(snapshot_path)
    assert snapshot_path.read_bytes() == SNAPSHOT_BYTES


def test_pull_with_nothing_published_uses_public_snapshot_with_fallback(
    remote_store: CachedBlobStore, tmp_path: Path, public_site: list[Any],
) -> None:
    snapshot_path = tmp_path / "frontend.snapshot"

    result = pull(db=False, snapshot_path=snapshot_path, public_fallback=True)

    assert result == _public_result(snapshot_path)
    assert snapshot_path.read_bytes() == SNAPSHOT_BYTES


def test_pull_with_nothing_published_raises_without_fallback_or_for_database(
    remote_store: CachedBlobStore, tmp_path: Path, public_site: list[Any],
) -> None:
    with pytest.raises(BlobStoreError, match="Nothing published"):
        pull(db=False, snapshot_path=tmp_path / "s.snapshot")
    with pytest.raises(BlobStoreError, match="Nothing published"):
        pull(db_path=tmp_path / "x.db", snapshot_path=tmp_path / "s", public_fallback=True)
    assert public_site == []


def test_pull_public_fallback_does_not_apply_to_unknown_run(
    remote_store: CachedBlobStore, tmp_path: Path, public_site: list[Any],
) -> None:
    with pytest.raises(BlobStoreError, match="No run run-9"):
        pull(run_id="run-9", db=False, snapshot_path=tmp_path / "s", public_fallback=True)
    assert public_site == []


def test_pull_public_fallback_prefers_published_run(
    pipeline_dir: Path, remote_store: CachedBlobStore, tmp_path: Path, public_site: list[Any],
) -> None:
    published = gzip.compress(b"published")
    _prepare_run("run-1", snapshot=published)
    push_candidate("run-1")
    promote("run-1")
    snapshot_path = tmp_path / "frontend.snapshot"

    result = pull(db=False, snapshot_path=snapshot_path, public_fallback=True)

    assert result == {"run_id": "run-1", "snapshot_path": str(snapshot_path)}
    assert snapshot_path.read_bytes() == published
    assert public_site == []


def test_pull_public_snapshot_rejects_non_gzip_body(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        datasync.urllib.request, "urlopen",
        lambda request, timeout: _FakeResponse(b"<html>not found</html>"),
    )
    snapshot_path = tmp_path / "frontend.snapshot"

    with pytest.raises(BlobStoreError, match="did not return a gzip snapshot"):
        pull(db=False, snapshot_path=snapshot_path, public_fallback=True)
    assert not snapshot_path.exists()


def test_cli_data_pull_passes_public_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []

    def fake_pull(**kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        return {"run_id": None}

    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "pull", fake_pull)

    assert cli.main(["data", "pull", "--snapshot-only", "--public-fallback"]) == 0
    assert cli.main(["data", "pull"]) == 0

    assert calls == [
        {"run_id": None, "db": False, "snapshot": True, "public_fallback": True},
        {"run_id": None, "db": True, "snapshot": True, "public_fallback": False},
    ]


# ── Uploading bulletins ─────────────────────────────────────────────────────
def test_upload_bulletins_uploads_only_verified_pdfs(
    tmp_path: Path, remote_store: CachedBlobStore, s3_client: Any,
) -> None:
    bulletins = tmp_path / "bulletins"
    parish = bulletins / "test-parish"
    parish.mkdir(parents=True)
    good = b"%PDF good"
    good_hash = hashlib.sha256(good).hexdigest()
    (parish / f"{good_hash}.pdf").write_bytes(good)
    (parish / f"{good_hash}-truncated.pdf").write_bytes(b"%PDF truncated")
    (parish / "bulletin.pdf").write_bytes(b"%PDF unnamed")
    wrong_hash = hashlib.sha256(b"something else").hexdigest()
    (parish / f"{wrong_hash}.pdf").write_bytes(b"%PDF mismatched")
    present = b"%PDF already there"
    present_hash = hashlib.sha256(present).hexdigest()
    (parish / f"{present_hash}.pdf").write_bytes(present)
    s3_client.put_object(
        Bucket=BUCKET, Key=bulletin_pdf_key("test-parish", present_hash), Body=present,
    )

    result = upload_bulletins(bulletins)

    assert result == {"uploaded": 1, "already_present": 1, "skipped": 3}
    assert _bucket_keys(s3_client) == sorted([
        bulletin_pdf_key("test-parish", good_hash),
        bulletin_pdf_key("test-parish", present_hash),
    ])
    body = s3_client.get_object(Bucket=BUCKET, Key=bulletin_pdf_key("test-parish", good_hash))
    assert body["Body"].read() == good
    assert body["ContentType"] == "application/pdf"


def test_upload_bulletins_refuses_without_remote_write(
    tmp_path: Path, remote_store: CachedBlobStore, s3_client: Any,
) -> None:
    remote_store.remote_write = False
    parish = tmp_path / "bulletins" / "test-parish"
    parish.mkdir(parents=True)
    data = b"%PDF"
    (parish / f"{hashlib.sha256(data).hexdigest()}.pdf").write_bytes(data)

    with pytest.raises(BlobStoreError, match="CARLO_REMOTE_WRITE"):
        upload_bulletins(tmp_path / "bulletins")
    assert _bucket_keys(s3_client) == []


def test_upload_bulletins_refuses_local_only_store(tmp_path: Path) -> None:
    with pytest.raises(BlobStoreError):
        upload_bulletins(tmp_path / "bulletins")


# ── Legacy import ───────────────────────────────────────────────────────────
def test_import_legacy_from_source_dir(pipeline_dir: Path, tmp_path: Path) -> None:
    source = tmp_path / "legacy"
    source.mkdir()
    url = "https://example.org/bulletin.pdf"
    (source / "metadata.json").write_text(json.dumps([
        {"parish_slug": "test-parish", "source_url": url, "content_hash": "abc",
         "processed_at": "2026-09-19T00:00:00Z"},
    ]), encoding="utf-8")
    (source / "events.json").write_text(json.dumps([
        {"church_slug": "test-church", "bulletin_source_url": url, "event_type": "mass",
         "event_kind": "weekly", "day_of_week": "Sunday", "date": None,
         "start_time": "9:00 AM", "end_time": None, "cancelled": False},
    ]), encoding="utf-8")
    (source / "event_history.json").write_text(json.dumps([
        {"church_slug": "test-church", "event_type": "mass", "start_time": 540,
         "dates": ["2026-09-13", "2026-09-20"]},
    ]), encoding="utf-8")

    result = import_legacy(source_dir=source)

    assert result == {
        "source": str(source), "bulletins": 1, "events": 1, "events_skipped": 0,
        "occurrences": 2,
    }
    assert DEFAULT_DB_PATH.exists()


def test_import_legacy_with_missing_files_builds_empty_database(
    pipeline_dir: Path, tmp_path: Path,
) -> None:
    db_path = tmp_path / "empty.db"

    result = import_legacy(source_dir=tmp_path / "nothing-here", db_path=db_path)

    assert result["bulletins"] == result["events"] == result["occurrences"] == 0
    assert _parish_rows(db_path)[0][1] == "test-parish"


def test_import_legacy_needs_exactly_one_source(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="exactly one"):
        import_legacy()
    with pytest.raises(ValueError, match="exactly one"):
        import_legacy(git_ref="HEAD", source_dir=tmp_path)
