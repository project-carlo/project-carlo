"""In-place compaction of bulletin PDFs stored before compaction existed."""

from __future__ import annotations

import json
import os
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfWriter

from pdf_extract.blobstore import (
    BlobStoreError,
    CachedBlobStore,
    LocalBlobStore,
    bulletin_pdf_key,
)
from pdf_extract.bulletin_compact import (
    COMPACTION_CUTOFF,
    compact_bulletins,
    parse_bulletin_pdf_key,
)
from pdf_extract.labeling.labels import empty_label, write_label
from pdf_extract.pdf_compact import compact_bulletin_pdf

HASH = "ab" * 32
OTHER = "cd" * 32


def _pdf(pages: int, pad: int = 0) -> bytes:
    writer = PdfWriter()
    for _ in range(pages):
        writer.add_blank_page(width=612, height=792)
    out = BytesIO()
    writer.write(out)
    data = out.getvalue()
    if pad:
        data += b"\n%" + (b"x" * pad)
    return data


def _age(path: Path, when) -> None:
    stamp = when.timestamp()
    os.utime(path, (stamp, stamp))


def _store(tmp_path: Path, *, remote_write: bool = False) -> CachedBlobStore:
    return CachedBlobStore(
        LocalBlobStore(tmp_path / "local"),
        LocalBlobStore(tmp_path / "remote"),
        remote_write=remote_write,
    )


def _put_old(store: CachedBlobStore, key: str, data: bytes, *, when=None) -> None:
    assert store.remote is not None
    store.remote.put(key, data)
    _age(store.remote.path(key), when or (COMPACTION_CUTOFF - timedelta(seconds=1)))


def test_parse_bulletin_pdf_key_accepts_only_stored_bulletins() -> None:
    assert parse_bulletin_pdf_key(bulletin_pdf_key("st-mary", HASH)) == ("st-mary", HASH)
    assert parse_bulletin_pdf_key(f"bulletins/st-mary/{HASH}-truncated.pdf") is None
    assert parse_bulletin_pdf_key("bulletins/St-Mary/" + HASH + ".pdf") is None
    assert parse_bulletin_pdf_key("pipeline/latest.json") is None


def test_dry_run_selects_only_pre_cutoff_bulletin_pdfs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda data: data,
    )
    store = _store(tmp_path)
    old = bulletin_pdf_key("test-parish", HASH)
    newer = bulletin_pdf_key("test-parish", OTHER)
    _put_old(store, old, _pdf(1))
    _put_old(store, newer, _pdf(1), when=COMPACTION_CUTOFF)
    assert store.remote is not None
    store.remote.put("bulletins/notes.txt", b"nope")
    _age(store.remote.path("bulletins/notes.txt"), COMPACTION_CUTOFF - timedelta(days=1))

    result = compact_bulletins(store, labels_dir=tmp_path / "labels", require_ghostscript=False)

    assert result["mode"] == "dry-run"
    assert result["listed"] == 3
    assert result["ignored"] == 1
    assert result["candidates"] == 1
    assert result["keep"] == 1
    assert result["items"][0]["key"] == old
    assert result["items"][0]["reason"] == "compaction would not shrink the file"


def test_replace_when_the_compacted_pdf_keeps_labeled_pages(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    small = _pdf(2)
    monkeypatch.setattr("pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda _data: small)
    store = _store(tmp_path)
    key = bulletin_pdf_key("test-parish", HASH)
    _put_old(store, key, _pdf(2, pad=5000))
    labels = tmp_path / "labels"
    saved = empty_label("test-parish", HASH, "https://example.org/b.pdf")
    saved["events"] = [{
        "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "09:00", "end_time": None,
        "cancelled": False, "weeks_of_month": [], "season": None, "page_number": 2,
        "note": None, "origin": "human",
    }]
    write_label(
        saved, parish_slug="test-parish", content_hash=HASH,
        source_url="https://example.org/b.pdf", labels_dir=labels,
    )

    result = compact_bulletins(store, labels_dir=labels, require_ghostscript=False)

    assert result["replace"] == 1
    assert result["bytes_before"] == len(_pdf(2, pad=5000))
    assert result["bytes_after"] == len(small)
    assert result["bytes_saved"] == result["bytes_before"] - result["bytes_after"]
    assert result["labeled"] == [{
        "parish_slug": "test-parish",
        "content_hash": HASH,
        "action": "replace",
        "label_max_page": 2,
        "reason": result["items"][0]["reason"],
    }]
    assert result["bytes_before"] == len(_pdf(2, pad=5000))
    assert result["bytes_after"] == len(small)


def test_skips_a_pdf_whose_label_cites_a_dropped_page(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda _data: _pdf(10))
    store = _store(tmp_path)
    key = bulletin_pdf_key("test-parish", HASH)
    _put_old(store, key, _pdf(12, pad=8000))
    labels = tmp_path / "labels"
    (labels / "test-parish").mkdir(parents=True)
    (labels / "test-parish" / f"{HASH}.json").write_text(
        json.dumps({"events": [{"page_number": 11}]}), encoding="utf-8",
    )

    result = compact_bulletins(store, labels_dir=labels, require_ghostscript=False)

    assert result["skip"] == 1
    assert "page 11" in result["items"][0]["reason"]
    assert store.remote is not None
    assert store.remote.get(key) == _pdf(12, pad=8000)


def test_skips_an_unreadable_label_and_keeps_an_unreadable_pdf(tmp_path: Path) -> None:
    store = _store(tmp_path)
    labeled = bulletin_pdf_key("test-parish", HASH)
    broken = bulletin_pdf_key("test-parish", OTHER)
    _put_old(store, labeled, _pdf(1, pad=1000))
    _put_old(store, broken, b"not a pdf")
    labels = tmp_path / "labels"
    (labels / "test-parish").mkdir(parents=True)
    (labels / "test-parish" / f"{HASH}.json").write_text("{", encoding="utf-8")

    result = compact_bulletins(store, labels_dir=labels, require_ghostscript=False)

    by_hash = {item["content_hash"]: item for item in result["items"]}
    assert by_hash[HASH]["action"] == "skip"
    assert "label file" in by_hash[HASH]["reason"]
    assert by_hash[OTHER]["action"] == "keep"
    assert by_hash[OTHER]["reason"] == "stored PDF does not open"


def test_skips_when_compacted_page_count_is_wrong(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda _data: _pdf(1))
    store = _store(tmp_path)
    _put_old(store, bulletin_pdf_key("test-parish", HASH), _pdf(3, pad=5000))

    result = compact_bulletins(store, labels_dir=tmp_path / "labels", require_ghostscript=False)

    assert result["skip"] == 1
    assert "expected 3" in result["items"][0]["reason"]


def test_apply_rewrites_the_same_key_and_refreshes_the_local_cache(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    small = _pdf(2)
    original = _pdf(2, pad=5000)
    monkeypatch.setattr("pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda _data: small)
    store = _store(tmp_path, remote_write=True)
    key = bulletin_pdf_key("test-parish", HASH)
    _put_old(store, key, original)
    store.local.put(key, b"stale local copy")
    sidecar = store.local.path(key).with_name(f"{HASH}-truncated.pdf")
    sidecar.write_bytes(b"stale truncation")
    backup_dir = tmp_path / "backup"

    result = compact_bulletins(
        store, apply=True, backup_dir=backup_dir,
        labels_dir=tmp_path / "labels", require_ghostscript=False,
    )

    assert result["replaced"] == 1
    assert result["replace"] == 0
    assert store.remote is not None
    assert store.remote.get(key) == small
    assert store.local.get(key) == small
    assert not sidecar.exists()
    assert (backup_dir / "test-parish" / f"{HASH}.pdf").read_bytes() == original
    manifest = json.loads((backup_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest[0]["key"] == key
    assert manifest[0]["backup"] == f"test-parish/{HASH}.pdf"


def test_apply_restores_the_original_when_the_upload_does_not_read_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = _pdf(2, pad=5000)

    class _Tamper(LocalBlobStore):
        def __init__(self, root: Path) -> None:
            super().__init__(root)
            self.gets = 0

        def get(self, key: str) -> bytes | None:
            self.gets += 1
            data = super().get(key)
            if self.gets == 2 and data is not None:
                return b"tampered"
            return data

    remote = _Tamper(tmp_path / "remote")
    store = CachedBlobStore(
        LocalBlobStore(tmp_path / "local"), remote, remote_write=True,
    )
    monkeypatch.setattr("pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda _data: _pdf(2))
    key = bulletin_pdf_key("test-parish", HASH)
    remote.put(key, original)
    _age(remote.path(key), COMPACTION_CUTOFF - timedelta(seconds=1))

    result = compact_bulletins(
        store, apply=True, backup_dir=tmp_path / "backup",
        labels_dir=tmp_path / "labels", require_ghostscript=False,
    )

    assert result["failed"] == 1
    assert "original restored" in result["items"][0]["reason"]
    assert remote.path(key).read_bytes() == original


def test_restore_puts_backups_back_at_the_same_keys(tmp_path: Path) -> None:
    store = _store(tmp_path, remote_write=True)
    original = _pdf(4, pad=100)
    backup_dir = tmp_path / "backup"
    key = bulletin_pdf_key("test-parish", HASH)
    backup = backup_dir / "test-parish" / f"{HASH}.pdf"
    backup.parent.mkdir(parents=True)
    backup.write_bytes(original)
    assert store.remote is not None
    store.remote.put(key, b"compacted")
    store.local.put(key, b"compacted")

    result = compact_bulletins(store, restore=True, backup_dir=backup_dir)

    assert result["mode"] == "restore"
    assert result["restored"] == 1
    assert store.remote.get(key) == original
    assert store.local.get(key) == original


def test_apply_refuses_without_write_access_before_compacting(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = {"n": 0}

    def compact(data: bytes) -> bytes:
        calls["n"] += 1
        return data

    monkeypatch.setattr("pdf_extract.bulletin_compact.compact_bulletin_pdf", compact)
    store = _store(tmp_path, remote_write=False)
    _put_old(store, bulletin_pdf_key("test-parish", HASH), _pdf(1))

    with pytest.raises(BlobStoreError, match="CARLO_REMOTE_WRITE"):
        compact_bulletins(store, apply=True, require_ghostscript=False)
    assert calls["n"] == 0


def test_refuses_to_plan_without_ghostscript(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("pdf_extract.bulletin_compact.shutil.which", lambda _name: None)

    with pytest.raises(RuntimeError, match="Ghostscript"):
        compact_bulletins(_store(tmp_path), require_ghostscript=True)


def test_cli_dry_run_and_failure_exit_code(
    blob_store: CachedBlobStore, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    from pdf_extract.__main__ import main

    monkeypatch.setattr("pdf_extract.bulletin_compact.shutil.which", lambda _name: "/usr/bin/gs")
    monkeypatch.setattr(
        "pdf_extract.bulletin_compact.compact_bulletin_pdf", lambda data: data,
    )
    key = bulletin_pdf_key("test-parish", HASH)
    blob_store.put(key, _pdf(1))
    _age(blob_store.local.path(key), COMPACTION_CUTOFF - timedelta(days=1))

    assert main(["bulletins", "compact", "--log-level", "ERROR"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "dry-run"
    assert payload["keep"] == 1

    monkeypatch.setattr(
        "pdf_extract.__main__.compact_bulletins", lambda *args, **kwargs: {"failed": 2},
    )
    assert main(["bulletins", "compact", "--log-level", "ERROR"]) == 1


def test_real_compaction_marks_a_photo_pdf_for_replacement(tmp_path: Path) -> None:
    if os.environ.get("SKIP_GS"):
        pytest.skip("Ghostscript skipped")
    from pdf_extract import pdf_compact
    if pdf_compact.shutil.which("gs") is None:
        pytest.skip("Ghostscript not installed")

    store = _store(tmp_path)
    # A page with a large image, built the same way as the compact unit test.
    original = _photo_pdf()
    assert compact_bulletin_pdf(original) is not original
    _put_old(store, bulletin_pdf_key("test-parish", HASH), original)

    result = compact_bulletins(store, labels_dir=tmp_path / "labels", require_ghostscript=True)

    assert result["replace"] == 1
    assert result["bytes_saved"] > 0
    assert result["items"][0]["compacted_pages"] == 1


def _photo_pdf() -> bytes:
    """One letter page holding a photo-like image well over 150 dpi."""
    import random
    import zlib

    from pypdf.generic import (
        DecodedStreamObject,
        DictionaryObject,
        NameObject,
        NumberObject,
        StreamObject,
    )

    rng = random.Random(0)
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    px = 400
    rows = bytearray()
    for y in range(px):
        for x in range(px):
            rows += bytes(((x + y) % 256, (x * 3) % 256, rng.randrange(256)))
    image = StreamObject()
    image._data = zlib.compress(bytes(rows))
    image.update({
        NameObject("/Type"): NameObject("/XObject"),
        NameObject("/Subtype"): NameObject("/Image"),
        NameObject("/Width"): NumberObject(px),
        NameObject("/Height"): NumberObject(px),
        NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
        NameObject("/BitsPerComponent"): NumberObject(8),
        NameObject("/Filter"): NameObject("/FlateDecode"),
    })
    content = DecodedStreamObject()
    content.set_data(b"q 540 0 0 540 36 126 cm /Im0 Do Q")
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/XObject"): DictionaryObject({NameObject("/Im0"): writer._add_object(image)}),
    })
    page[NameObject("/Contents")] = writer._add_object(content)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()
