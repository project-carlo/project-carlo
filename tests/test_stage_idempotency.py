import hashlib
import logging
import threading
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import pytest

from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.db import create_db
from pdf_extract.fetch import BulletinLink, fetch_bulletins
from pdf_extract.process import process_bulletins
from pdf_extract.recurrence import load_history_from_db, save_history_to_db
from pdf_extract.runs import parish_results, start_run
from pdf_extract.storage import (
    connect_db,
    latest_bulletin_ids,
    load_bulletins,
    load_events,
    replace_bulletin_events,
)
from tests.conftest import CHURCH_FIELDS, PARISH_FIELDS, write_csv


@pytest.fixture
def db(tmp_path: Path, monkeypatch) -> Path:
    """An empty pipeline DB with one parish (test-parish) and church (st-mary-anytown)."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    parishes = [{
        "slug": "test-parish", "name": "Test Parish", "website": "https://test.org",
        "bulletin_provider": "ecatholic",
    }]
    churches = [{
        "parish_id": "test-parish", "slug": "st-mary-anytown", "name": "St. Mary",
        "line1": "123 Main St", "city": "Anytown", "state": "NY", "postal_code": "14000",
    }]
    for idx in range(1, 3):
        parishes.append({
            "slug": f"test-parish-{idx}", "name": f"Test Parish {idx}",
            "website": f"https://test-{idx}.org", "bulletin_provider": "ecatholic",
        })
        churches.append({
            "parish_id": f"test-parish-{idx}", "slug": f"st-mary-anytown-{idx}",
            "name": "St. Mary", "line1": "123 Main St", "city": "Anytown", "state": "NY",
            "postal_code": "14000",
        })
    write_csv(work / "data" / "parishes.csv", PARISH_FIELDS, parishes)
    write_csv(work / "data" / "churches.csv", CHURCH_FIELDS, churches)
    create_db()
    # These tests stub PDFs with non-PDF bytes; skip the pypdf-based truncation helper.
    monkeypatch.setattr("pdf_extract.storage.ensure_truncated_pdf", lambda path, **kwargs: path)
    return work / "data" / "parish_events.db"


def _add_bulletin(
    db: Path,
    *,
    parish_slug: str = "test-parish",
    source_url: str,
    content_hash: str,
    pdf_bytes: bytes = b"fake",
    fetched_at: str,
    processed_at: str | None = None,
    published_date: str | None = None,
) -> int:
    get_store().put(bulletin_pdf_key(parish_slug, content_hash), pdf_bytes)
    conn = connect_db(db)
    try:
        with conn:
            cursor = conn.execute(
                """INSERT INTO bulletin(
                       parish_id, source_url, content_hash, fetched_at, processed_at,
                       published_date
                   ) SELECT id, ?, ?, ?, ?, ? FROM parish WHERE slug = ?""",
                (source_url, content_hash, fetched_at, processed_at, published_date, parish_slug),
            )
        return int(cursor.lastrowid)
    finally:
        conn.close()


def _event(**overrides):
    event = {
        "church_slug": "st-mary-anytown",
        "type": "mass",
        "kind": "weekly",
        "day_of_week": "Sunday",
        "date": None,
        "start_time": "9:00 AM",
        "end_time": None,
        "cancelled": False,
        "page_number": 1,
        "note": None,
    }
    event.update(overrides)
    return event


def _extraction(*events, published_date=None, wrong_bulletin=False):
    return {
        "events": list(events),
        "church_list_needs_review": False,
        "published_date": published_date,
        "wrong_bulletin": wrong_bulletin,
    }


def _stub_extractor(monkeypatch, result) -> None:
    monkeypatch.setattr(
        "pdf_extract.classifiers.gemini.extract_events",
        lambda pdf_bytes, *, churches, model="gemini-3-flash-preview", today=None: result,
    )


def _current_events(db: Path) -> list[dict]:
    conn = connect_db(db)
    try:
        return load_events(conn, list(latest_bulletin_ids(conn).values()))
    finally:
        conn.close()


def _bulletins(db: Path) -> list[dict]:
    conn = connect_db(db)
    try:
        return load_bulletins(conn)
    finally:
        conn.close()


def test_fetch_stage_is_idempotent(monkeypatch, db: Path) -> None:
    monkeypatch.setattr(
        "pdf_extract.fetch._build_bulletin_link",
        lambda bulletin_provider, fetch_provider_id, *, page=None: BulletinLink(
            source_url="https://example.org/bulletin.pdf",
            fetch_url="https://example.org/bulletin.pdf",
        ),
    )
    monkeypatch.setattr("pdf_extract.fetch._download_pdf", lambda **kwargs: b"%PDF-1.4 fake")

    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)

    first = fetch_bulletins(parish_name="Test Parish")
    second = fetch_bulletins(parish_name="Test Parish")

    assert first["fetched_bulletins"] == 1
    assert second["fetched_bulletins"] == 0
    assert second["skipped_existing_urls"] == 1

    [bulletin] = _bulletins(db)
    assert bulletin["processed_at"] is None
    assert get_store().get(
        bulletin_pdf_key("test-parish", bulletin["content_hash"])
    ) == b"%PDF-1.4 fake"


def test_fetch_stores_a_compacted_copy_under_the_downloaded_hash(monkeypatch, db: Path) -> None:
    monkeypatch.setattr(
        "pdf_extract.fetch._build_bulletin_link",
        lambda bulletin_provider, fetch_provider_id, *, page=None: BulletinLink(
            source_url="https://example.org/bulletin.pdf",
            fetch_url="https://example.org/bulletin.pdf",
        ),
    )
    monkeypatch.setattr("pdf_extract.fetch._download_pdf", lambda **kwargs: b"%PDF-1.4 big")
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data: b"%PDF small")

    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)

    fetch_bulletins(parish_name="Test Parish")

    [bulletin] = _bulletins(db)
    assert bulletin["content_hash"] == hashlib.sha256(b"%PDF-1.4 big").hexdigest()
    assert get_store().get(
        bulletin_pdf_key("test-parish", bulletin["content_hash"])
    ) == b"%PDF small"


def test_fetch_keeps_an_already_stored_bulletin(monkeypatch, db: Path) -> None:
    # The same PDF re-posted at a new URL: the stored copy is not rewritten.
    urls = iter(["https://example.org/a.pdf", "https://example.org/b.pdf"])

    def build_link(bulletin_provider, fetch_provider_id, *, page=None):
        url = next(urls)
        return BulletinLink(source_url=url, fetch_url=url)

    compactions = []

    def compact(data: bytes) -> bytes:
        compactions.append(data)
        return b"%PDF compacted " + str(len(compactions)).encode()

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch._download_pdf", lambda **kwargs: b"%PDF-1.4 same")
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", compact)

    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)

    fetch_bulletins(parish_name="Test Parish")
    fetch_bulletins(parish_name="Test Parish")

    assert len(compactions) == 1
    content_hash = hashlib.sha256(b"%PDF-1.4 same").hexdigest()
    assert get_store().get(bulletin_pdf_key("test-parish", content_hash)) == b"%PDF compacted 1"


@pytest.mark.parametrize(
    ("provider", "url", "stored"),
    [
        # A parish that overwrites one file every week: each new issue is kept.
        ("other", "https://test.org/files/bulletin.pdf", 2),
        # A dated address names one issue, and a publisher's address is never reused.
        ("other", "https://test.org/files/bulletin-2026-09-27.pdf", 1),
        ("ecatholic", "https://files.ecatholic.com/1/bulletins/bulletin.pdf", 1),
    ],
)
def test_fetch_reads_an_undated_bulletin_address_again_for_a_new_issue(
    monkeypatch, db: Path, provider: str, url: str, stored: int,
) -> None:
    issues = iter([b"%PDF-1.4 week 1", b"%PDF-1.4 week 1", b"%PDF-1.4 week 2"])
    monkeypatch.setattr(
        "pdf_extract.fetch._build_bulletin_link",
        lambda bulletin_provider, fetch_provider_id, *, page=None: BulletinLink(
            source_url=url, fetch_url=url,
        ),
    )
    monkeypatch.setattr("pdf_extract.fetch._download_pdf", lambda **kwargs: next(issues))
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source", lambda parish: (provider, "https://test.org"),
    )

    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)

    results = [fetch_bulletins(parish_name="Test Parish") for _ in range(3)]

    assert [r["fetched_bulletins"] for r in results] == [1, 0, stored - 1]
    bulletins = _bulletins(db)
    assert len(bulletins) == stored
    if stored == 2:
        week_2 = hashlib.sha256(b"%PDF-1.4 week 2").hexdigest()
        assert {b["source_url"] for b in bulletins} == {url, f"{url}#{week_2[:12]}"}


def test_fetch_records_each_parish_outcome_for_the_run(monkeypatch, db: Path) -> None:
    def build_link(bulletin_provider, fetch_provider_id, *, page=None):
        return BulletinLink(
            source_url="https://example.org/bulletin.pdf",
            fetch_url="https://example.org/bulletin.pdf",
        )

    def download(*, fetch_url, source_url):
        if download.calls:
            raise OSError("connection reset")
        download.calls += 1
        return b"%PDF-1.4 fake"

    download.calls = 0

    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch._download_pdf", download)
    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source",
        lambda parish: ("ecatholic", parish["slug"]),
    )

    conn = connect_db(db)
    start_run(conn, "run-1", git_sha=None, trigger="test")
    conn.close()

    result = fetch_bulletins(run_id="run-1")
    assert result["fetched_bulletins"] == 1
    assert result["failed_parishes"] == 2

    conn = connect_db(db)
    try:
        statuses = {r["parish_slug"]: r["status"] for r in parish_results(conn, "run-1")}
    finally:
        conn.close()
    assert statuses == {
        "test-parish": "new",
        "test-parish-1": "download_failed",
        "test-parish-2": "download_failed",
    }


def test_fetch_limits_to_the_given_slugs(monkeypatch, db: Path) -> None:
    monkeypatch.setattr(
        "pdf_extract.fetch._build_bulletin_link",
        lambda bulletin_provider, fetch_provider_id, *, page=None: BulletinLink(
            source_url=f"https://example.org/{fetch_provider_id}.pdf",
            fetch_url=f"https://example.org/{fetch_provider_id}.pdf",
        ),
    )
    monkeypatch.setattr("pdf_extract.fetch._download_pdf", lambda **kwargs: b"%PDF-1.4 fake")

    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)

    result = fetch_bulletins(slugs=["test-parish-1"])

    assert result["fetched_bulletins"] == 1
    assert [bulletin["parish_slug"] for bulletin in _bulletins(db)] == ["test-parish-1"]
    with pytest.raises(ValueError, match="no-such-parish"):
        fetch_bulletins(slugs=["no-such-parish"])


def test_process_limits_to_the_given_slugs(monkeypatch, db: Path) -> None:
    for slug in ("test-parish", "test-parish-1"):
        _add_bulletin(
            db, parish_slug=slug, source_url=f"https://example.org/{slug}.pdf",
            content_hash=slug, fetched_at="2026-01-01T00:00:00Z",
        )
    _stub_extractor(monkeypatch, _extraction(_event()))

    result = process_bulletins(slugs=["test-parish"])

    assert result["processed_bulletins"] == 1
    processed = {bulletin["parish_slug"] for bulletin in _bulletins(db) if bulletin["processed_at"]}
    assert processed == {"test-parish"}
    with pytest.raises(ValueError, match="no-such-parish"):
        process_bulletins(slugs=["no-such-parish"])


def test_process_stage_is_idempotent(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/parsed.pdf", content_hash="def",
        fetched_at="2026-01-01T00:00:00Z", published_date="2026-02-22",
    )
    _stub_extractor(monkeypatch, _extraction(_event()))

    first = process_bulletins(parish_name="Test Parish")
    second = process_bulletins(parish_name="Test Parish")

    assert first["processed_bulletins"] == 1
    assert first["inserted_events"] == 1
    assert second["processed_bulletins"] == 0
    assert second["inserted_events"] == 0


def test_process_only_latest_fetched_unprocessed_per_parish(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/older.pdf", content_hash="older",
        pdf_bytes=b"older", fetched_at="2026-01-01T00:00:00Z", published_date="2026-03-01",
    )
    _add_bulletin(
        db, source_url="https://example.org/latest.pdf", content_hash="latest",
        pdf_bytes=b"latest", fetched_at="2026-02-01T00:00:00Z", published_date="2026-01-01",
    )

    processed: list[bytes] = []

    def _extract_events(pdf_bytes, *, churches, model="gemini-3-flash-preview", today=None):
        processed.append(pdf_bytes)
        return _extraction(_event())

    monkeypatch.setattr("pdf_extract.classifiers.gemini.extract_events", _extract_events)

    result = process_bulletins(parish_name="Test Parish")

    assert result["processed_bulletins"] == 1
    assert result["inserted_events"] == 1
    assert processed == [b"latest"]


def test_process_skips_older_when_latest_already_processed(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/older.pdf", content_hash="older",
        fetched_at="2026-01-01T00:00:00Z",
    )
    _add_bulletin(
        db, source_url="https://example.org/latest.pdf", content_hash="latest",
        fetched_at="2026-02-01T00:00:00Z", processed_at="2026-02-02T00:00:00Z",
    )
    _stub_extractor(monkeypatch, _extraction(_event()))

    result = process_bulletins(parish_name="Test Parish")

    assert result["processed_bulletins"] == 0
    assert result["inserted_events"] == 0


def test_process_bounds_prepared_pdfs_to_concurrency(monkeypatch, db: Path) -> None:
    for idx, parish_slug in enumerate(["test-parish", "test-parish-1", "test-parish-2"]):
        _add_bulletin(
            db, parish_slug=parish_slug, source_url=f"https://example.org/bulletin-{idx}.pdf",
            content_hash=f"hash-{idx}", pdf_bytes=f"pdf-{idx}".encode(),
            fetched_at=f"2026-01-0{idx + 1}T00:00:00Z",
        )

    started = threading.Event()
    extract_calls = 0
    prepare_calls = 0

    original_prepare = __import__(
        "pdf_extract.runner", fromlist=["load_bulletin_work_item"],
    ).load_bulletin_work_item

    def _load_bulletin_work_item(entry, conn):
        nonlocal prepare_calls
        prepare_calls += 1
        if prepare_calls == 2:
            assert started.wait(timeout=1), "second PDF prepared before extraction started"
        return original_prepare(entry, conn)

    def _extract_events(pdf_bytes, *, churches, model="gemini-3-flash-preview", today=None):
        nonlocal extract_calls
        extract_calls += 1
        started.set()
        return _extraction()

    monkeypatch.setattr("pdf_extract.runner.load_bulletin_work_item", _load_bulletin_work_item)
    monkeypatch.setattr("pdf_extract.classifiers.gemini.extract_events", _extract_events)

    result = process_bulletins(concurrency=1)

    assert result["processed_bulletins"] == 3
    assert result["inserted_events"] == 0
    assert extract_calls == 3


def test_process_skips_events_when_wrong_bulletin_flag_is_set(
    monkeypatch, db: Path, caplog,
) -> None:
    _add_bulletin(
        db, source_url="https://example.org/wrong.pdf", content_hash="abc",
        fetched_at="2026-01-01T00:00:00Z",
    )
    _stub_extractor(
        monkeypatch, _extraction(_event(), published_date="2025-01-15", wrong_bulletin=True),
    )

    caplog.set_level(logging.WARNING, logger="pdf_extract.process")
    result = process_bulletins(parish_name="Test Parish")

    assert result["processed_bulletins"] == 1
    assert result["inserted_events"] == 0
    assert any("flagged as wrong PDF" in rec.message for rec in caplog.records)

    [bulletin] = _bulletins(db)
    assert bulletin["processed_at"] is not None
    assert bulletin["published_date"] == "2025-01-15"
    assert _current_events(db) == []


def test_process_stores_published_date_and_note(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/good.pdf", content_hash="xyz",
        fetched_at="2026-04-15T00:00:00Z",
    )
    _stub_extractor(
        monkeypatch,
        _extraction(
            _event(start_time="11:00 AM", page_number=2, note="Spanish"),
            published_date="2026-04-12",
        ),
    )

    result = process_bulletins(parish_name="Test Parish")

    assert result["processed_bulletins"] == 1
    assert result["inserted_events"] == 1
    assert _bulletins(db)[0]["published_date"] == "2026-04-12"

    [event] = _current_events(db)
    assert event["note"] == "Spanish"
    assert event["start_time"] == "11:00 AM"
    assert event["page_number"] == 2


def test_process_counts_events_for_unknown_churches_as_skipped(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/good.pdf", content_hash="xyz",
        fetched_at="2026-04-15T00:00:00Z",
    )
    _stub_extractor(
        monkeypatch, _extraction(_event(), _event(church_slug="not-a-known-church")),
    )

    result = process_bulletins(parish_name="Test Parish")

    assert result["inserted_events"] == 1
    assert result["skipped_events"] == 1


def test_superseded_bulletins_keep_their_events_but_are_not_current(
    monkeypatch, db: Path,
) -> None:
    older = _add_bulletin(
        db, source_url="https://example.org/older.pdf", content_hash="older",
        fetched_at="2026-01-01T00:00:00Z", processed_at="2026-01-02T00:00:00Z",
        published_date="2026-01-01",
    )
    conn = connect_db(db)
    replace_bulletin_events(conn, older, [{
        "church_slug": "st-mary-anytown", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Saturday", "start_time": "4:00 PM",
    }])
    conn.close()
    _add_bulletin(
        db, source_url="https://example.org/latest.pdf", content_hash="latest",
        fetched_at="2026-02-01T00:00:00Z",
    )
    _stub_extractor(monkeypatch, _extraction(_event(), published_date="2026-02-01"))

    result = process_bulletins(parish_name="Test Parish")
    assert result["processed_bulletins"] == 1

    current = _current_events(db)
    assert [e["bulletin_source_url"] for e in current] == ["https://example.org/latest.pdf"]
    assert current[0]["day_of_week"] == "Sunday"

    conn = connect_db(db)
    try:
        assert len(load_events(conn)) == 2, "the older bulletin's rows are kept"
    finally:
        conn.close()


def test_current_bulletin_prefers_published_latest_over_fetched_latest(
    monkeypatch, db: Path,
) -> None:
    """A re-served old issue (fetched later, published earlier) must not displace
    the events of the most recently *published* bulletin."""
    current = _add_bulletin(
        db, source_url="https://example.org/current.pdf", content_hash="current",
        fetched_at="2026-05-23T00:00:00Z", processed_at="2026-05-23T01:00:00Z",
        published_date="2026-05-24",
    )
    conn = connect_db(db)
    replace_bulletin_events(conn, current, [{
        "church_slug": "st-mary-anytown", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "start_time": "9:00 AM",
    }])
    conn.close()
    # Fetched later, but the parish site re-served a year-old issue.
    _add_bulletin(
        db, source_url="https://example.org/stale.pdf", content_hash="stale",
        fetched_at="2026-06-07T00:00:00Z",
    )
    _stub_extractor(
        monkeypatch,
        _extraction(_event(day_of_week="Saturday", start_time="4:00 PM"),
                    published_date="2025-06-08"),
    )

    result = process_bulletins(parish_name="Test Parish")
    assert result["processed_bulletins"] == 1

    events = _current_events(db)
    assert [e["bulletin_source_url"] for e in events] == ["https://example.org/current.pdf"]
    assert events[0]["day_of_week"] == "Sunday"


def test_unprocessed_bulletin_does_not_blank_the_parish(db: Path) -> None:
    """A newer bulletin that failed extraction must not become the current one."""
    current = _add_bulletin(
        db, source_url="https://example.org/current.pdf", content_hash="current",
        fetched_at="2026-05-23T00:00:00Z", processed_at="2026-05-23T01:00:00Z",
    )
    _add_bulletin(
        db, source_url="https://example.org/failed.pdf", content_hash="failed",
        fetched_at="2026-06-07T00:00:00Z",
    )
    conn = connect_db(db)
    try:
        assert latest_bulletin_ids(conn) == {"test-parish": current}
    finally:
        conn.close()


def test_process_serves_cached_extraction_without_api_call(monkeypatch, db: Path) -> None:
    """A re-run after processed_at is reset reuses the result cache."""
    _add_bulletin(
        db, source_url="https://example.org/parsed.pdf", content_hash="def",
        fetched_at="2026-01-01T00:00:00Z",
    )

    extract_calls = 0

    def _extract_events(pdf_bytes, *, churches, model="gemini-3-flash-preview", today=None):
        nonlocal extract_calls
        extract_calls += 1
        return {**_extraction(_event()), "usage": {"prompt_tokens": 100, "output_tokens": 20}}

    monkeypatch.setattr("pdf_extract.classifiers.gemini.extract_events", _extract_events)

    first = process_bulletins(parish_name="Test Parish")
    assert first["processed_bulletins"] == 1
    assert first["cache_hits"] == 0
    assert (first["prompt_tokens"], first["output_tokens"]) == (100, 20)
    assert extract_calls == 1

    conn = connect_db(db)
    with conn:
        conn.execute("UPDATE bulletin SET processed_at = NULL")
    conn.close()

    second = process_bulletins(parish_name="Test Parish")
    assert second["processed_bulletins"] == 1
    assert second["inserted_events"] == 1
    assert second["cache_hits"] == 1
    assert extract_calls == 1, "cache hit must not call the classifier again"
    assert (second["prompt_tokens"], second["output_tokens"]) == (0, 0)
    assert len(_current_events(db)) == 1, "reprocessing replaces, not duplicates"


def test_process_records_failures_and_leaves_the_bulletin_pending(
    monkeypatch, db: Path,
) -> None:
    _add_bulletin(
        db, source_url="https://example.org/parsed.pdf", content_hash="def",
        fetched_at="2026-01-01T00:00:00Z",
    )

    def _extract_events(pdf_bytes, *, churches, model="gemini-3-flash-preview", today=None):
        raise RuntimeError("quota exhausted")

    monkeypatch.setattr("pdf_extract.classifiers.gemini.extract_events", _extract_events)
    conn = connect_db(db)
    start_run(conn, "run-1", git_sha=None, trigger="test")
    conn.close()

    result = process_bulletins(run_id="run-1")

    assert result["failed_bulletins"] == 1
    assert _bulletins(db)[0]["processed_at"] is None
    conn = connect_db(db)
    try:
        [row] = parish_results(conn, "run-1")
    finally:
        conn.close()
    assert row["status"] == "failed"
    assert "quota exhausted" in row["detail"]


def test_process_promotes_a_dated_event_that_recurred_the_past_two_weeks(
    monkeypatch, db: Path,
) -> None:
    _add_bulletin(
        db, source_url="https://example.org/parsed.pdf", content_hash="recurring",
        fetched_at="2026-08-19T00:00:00Z", published_date="2026-08-19",
    )
    # The same 7:00 PM Wednesday Adoration was printed in the two prior bulletins.
    conn = connect_db(db)
    save_history_to_db(conn, {
        ("st-mary-anytown", "adoration", 1140): {
            date(2026, 8, 5),
            date(2026, 8, 12),
        },
    })
    conn.close()

    _stub_extractor(
        monkeypatch,
        _extraction(
            _event(type="adoration", kind="specific_date", day_of_week=None,
                   date="2026-08-19", start_time="7:00 PM", page_number=2),
            published_date="2026-08-19",
        ),
    )

    result = process_bulletins(parish_name="Test Parish")

    assert result["weekly_promotions"] == 1
    [event] = _current_events(db)
    assert event["event_kind"] == "weekly"
    assert event["day_of_week"] == "Wednesday"
    assert event["date"] is None

    # The raw dated sighting is still recorded, so next week's bulletin can
    # keep the chain going even though the stored row no longer holds a date.
    conn = connect_db(db)
    try:
        history = load_history_from_db(conn)
    finally:
        conn.close()
    assert sorted(d.isoformat() for d in history[("st-mary-anytown", "adoration", 1140)]) == [
        "2026-08-05", "2026-08-12", "2026-08-19",
    ]
