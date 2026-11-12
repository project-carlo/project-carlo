import hashlib
import http.client
import logging
import sqlite3
import threading
import time
from collections import Counter
from contextlib import contextmanager
from datetime import date
from pathlib import Path

import pytest

from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.db import create_db
from pdf_extract.duplicates import Validators
from pdf_extract.fetch import (
    BulletinLink,
    Download,
    DownloadTooLarge,
    FetchSource,
    _Response,
    _site_for_source,
    _site_for_url,
    fetch_bulletins,
)
from pdf_extract.runs import consecutive_failures, parish_results, start_run
from pdf_extract.storage import connect_db, load_bulletins
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


def _bulletins(db: Path) -> list[dict]:
    conn = connect_db(db)
    try:
        return load_bulletins(conn)
    finally:
        conn.close()


def _fake_browser(monkeypatch) -> None:
    @contextmanager
    def fake_launch_stealth_browser():
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", fake_launch_stealth_browser)


def _link_to(monkeypatch, *urls: str) -> list[str]:
    """Resolve each parish to the next of `urls` (the last one repeating); returns the calls."""
    calls: list[str] = []

    def build_link(
        bulletin_provider, fetch_provider_id, *, page=None, recipe="", reference_date=None,
    ):
        url = urls[min(len(calls), len(urls) - 1)]
        calls.append(url)
        return BulletinLink(source_url=url, fetch_url=url)

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    return calls


def _serve(monkeypatch, *pdfs: bytes, etag: str | None = None) -> list[dict]:
    """Download each of `pdfs` in turn (the last one repeating); returns the calls."""
    calls: list[dict] = []

    def download(**kwargs):
        pdf = pdfs[min(len(calls), len(pdfs) - 1)]
        calls.append(kwargs)
        return Download(pdf=pdf, etag=etag)

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    return calls


def _results(db: Path, run_id: str) -> dict[str, dict]:
    conn = connect_db(db)
    try:
        return {r["parish_slug"]: r for r in parish_results(conn, run_id)}
    finally:
        conn.close()


def _start_run(db: Path, run_id: str) -> None:
    conn = connect_db(db)
    try:
        start_run(conn, run_id, git_sha=None, trigger="test")
    finally:
        conn.close()


def test_fetch_stage_is_idempotent(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 fake")
    _fake_browser(monkeypatch)

    first = fetch_bulletins(parish_name="Test Parish")
    second = fetch_bulletins(parish_name="Test Parish")

    assert first["fetched_bulletins"] == 1
    assert second["fetched_bulletins"] == 0
    assert second["unchanged_bulletins"] == 1

    [bulletin] = _bulletins(db)
    assert bulletin["processed_at"] is None
    assert get_store().get(
        bulletin_pdf_key("test-parish", bulletin["content_hash"])
    ) == b"%PDF-1.4 fake"


def test_fetch_takes_a_new_issue_at_an_address_it_already_has(monkeypatch, db: Path) -> None:
    # stpaulsnorwich.com overwrites /bulletin.pdf each week.
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 week 1", b"%PDF-1.4 week 1", b"%PDF-1.4 week 2")
    _fake_browser(monkeypatch)

    results = [fetch_bulletins(parish_name="Test Parish") for _ in range(3)]

    assert [r["fetched_bulletins"] for r in results] == [1, 0, 1]
    assert [b["content_hash"] for b in _bulletins(db)] == [
        hashlib.sha256(b"%PDF-1.4 week 1").hexdigest(),
        hashlib.sha256(b"%PDF-1.4 week 2").hexdigest(),
    ]


def test_fetch_compares_a_dated_address_by_content(monkeypatch, db: Path) -> None:
    # The date in an address is a hint, not proof the bulletin is unchanged.
    _link_to(monkeypatch, "https://example.org/bulletins/20260927.pdf")
    downloads = _serve(monkeypatch, b"%PDF-1.4 first", b"%PDF-1.4 reissued")
    _fake_browser(monkeypatch)

    fetch_bulletins(parish_name="Test Parish")
    second = fetch_bulletins(parish_name="Test Parish")

    assert len(downloads) == 2
    assert second["fetched_bulletins"] == 1


def test_fetch_records_a_bulletin_served_at_a_new_address_as_seen_again(
    monkeypatch, db: Path,
) -> None:
    # Discover Mass hands out a new download.php?bulletin= token on every
    # request for the same PDF.
    _link_to(
        monkeypatch,
        "https://bulletins.discovermass.com/download.php?bulletin=first-token",
        "https://bulletins.discovermass.com/download.php?bulletin=second-token",
    )
    _serve(monkeypatch, b"%PDF-1.4 same")
    _fake_browser(monkeypatch)
    _start_run(db, "run-2")

    fetch_bulletins(parish_name="Test Parish")
    [first] = _bulletins(db)
    second = fetch_bulletins(parish_name="Test Parish", run_id="run-2")

    [bulletin] = _bulletins(db)
    assert second["unchanged_bulletins"] == 1
    assert bulletin["source_url"].endswith("first-token")
    assert bulletin["last_seen_at"] >= first["last_seen_at"]
    result = _results(db, "run-2")["test-parish"]
    assert result["status"] == "unchanged"
    assert result["detail"] == f"same bulletin as #{bulletin['id']} (byte hash)"


def test_fetch_asks_whether_the_copy_it_has_is_current(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    calls: list[dict] = []

    def download(**kwargs):
        calls.append(kwargs)
        if kwargs.get("validators"):
            return Download(pdf=None)
        return Download(pdf=b"%PDF-1.4 fake", etag='"v1"', last_modified="Sat, 26 Sep 2026")

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    _fake_browser(monkeypatch)

    fetch_bulletins(parish_name="Test Parish")
    second = fetch_bulletins(parish_name="Test Parish")

    assert calls[0]["validators"] is None
    assert calls[1]["validators"] == Validators('"v1"', "Sat, 26 Sep 2026")
    assert second["unchanged_bulletins"] == 1
    [bulletin] = _bulletins(db)
    assert bulletin["etag"] == '"v1"'


def test_fetch_skips_a_parish_that_has_this_weekends_bulletin(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/current.pdf", content_hash="current",
        fetched_at="2026-10-03T09:00:00Z", processed_at="2026-10-03T10:00:00Z",
        published_date="2026-10-04",
    )
    resolved = _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 fake")
    _fake_browser(monkeypatch)
    _start_run(db, "run-1")

    # A run lands anywhere from the Saturday before to the Monday after.
    for today in (date(2026, 10, 3), date(2026, 10, 5)):
        result = fetch_bulletins(parish_name="Test Parish", run_id="run-1", today=today)
        assert result["already_current"] == 1

    assert resolved == []
    assert _results(db, "run-1")["test-parish"]["status"] == "current"
    assert result["stale_parishes"] == 0

    fetch_bulletins(parish_name="Test Parish", today=date(2026, 10, 10))
    assert len(resolved) == 1, "next weekend is fetched"


@pytest.mark.parametrize(
    ("fetched_at", "published_date", "processed_at", "wrong_bulletin"),
    [
        pytest.param("2026-10-03T09:00:00Z", None, None, False, id="no AI date"),
        pytest.param(
            "2026-10-03T09:00:00Z", "2026-10-04", "2026-10-03T10:00:00Z", True,
            id="wrong bulletin",
        ),
        pytest.param(
            # Fetched long before the date the extractor read: a misreading.
            "2026-09-13T09:00:00Z", "2026-10-04", "2026-09-13T10:00:00Z", False,
            id="implausible date",
        ),
    ],
)
def test_fetch_does_not_trust_a_doubtful_date_to_skip(
    monkeypatch, db: Path, fetched_at, published_date, processed_at, wrong_bulletin,
) -> None:
    bulletin_id = _add_bulletin(
        db, source_url="https://example.org/doubtful.pdf", content_hash="doubtful",
        fetched_at=fetched_at, processed_at=processed_at, published_date=published_date,
    )
    if wrong_bulletin:
        conn = connect_db(db)
        with conn:
            conn.execute("UPDATE bulletin SET wrong_bulletin = 1 WHERE id = ?", (bulletin_id,))
        conn.close()
    resolved = _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 fake")
    _fake_browser(monkeypatch)

    result = fetch_bulletins(parish_name="Test Parish", today=date(2026, 10, 4))

    assert result["already_current"] == 0
    assert len(resolved) == 1


def test_fetch_does_not_count_a_failed_recheck_as_a_failure(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/bulletin.pdf", content_hash="had",
        fetched_at="2026-09-26T09:00:00Z",
    )
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")

    def download(**kwargs):
        raise OSError("connection reset")

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    _fake_browser(monkeypatch)
    _start_run(db, "run-1")

    # The bulletin is this week's, but undated, so it is checked again.
    result = fetch_bulletins(parish_name="Test Parish", run_id="run-1", today=date(2026, 9, 26))

    assert result["failed_parishes"] == 0
    assert result["recheck_failed"] == 1
    assert _results(db, "run-1")["test-parish"]["status"] == "recheck_failed"


def test_fetch_counts_a_failed_download_as_a_failure_when_the_address_had_an_older_week(
    monkeypatch, db: Path,
) -> None:
    # A site that overwrites one address each week: what we have from it is
    # last week's, so failing to download it now misses this week's.
    _add_bulletin(
        db, source_url="https://example.org/bulletin.pdf", content_hash="had",
        fetched_at="2026-09-26T09:00:00Z", published_date="2026-09-27",
        processed_at="2026-09-26T10:00:00Z",
    )
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")

    def download(**kwargs):
        raise OSError("connection reset")

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    _fake_browser(monkeypatch)
    _start_run(db, "run-1")

    result = fetch_bulletins(parish_name="Test Parish", run_id="run-1", today=date(2026, 10, 3))

    assert result["failed_parishes"] == 1
    assert result["recheck_failed"] == 0
    assert _results(db, "run-1")["test-parish"]["status"] == "download_failed"


def test_fetch_resolves_the_bulletin_for_the_run_date(monkeypatch, db: Path) -> None:
    seen: list[date | None] = []

    def build_link(bulletin_provider, fetch_provider_id, *, page=None, recipe="", reference_date=None):
        seen.append(reference_date)
        raise ValueError("stop here")

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    _fake_browser(monkeypatch)

    fetch_bulletins(parish_name="Test Parish", today=date(2026, 9, 27))

    assert seen == [date(2026, 9, 27)]


def test_fetch_stores_a_compacted_copy_under_the_downloaded_hash(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 big")
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: b"%PDF small")
    _fake_browser(monkeypatch)

    fetch_bulletins(parish_name="Test Parish")

    [bulletin] = _bulletins(db)
    assert bulletin["content_hash"] == hashlib.sha256(b"%PDF-1.4 big").hexdigest()
    assert get_store().get(
        bulletin_pdf_key("test-parish", bulletin["content_hash"])
    ) == b"%PDF small"


def test_fetch_stores_nothing_over_the_size_limit(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 big")
    monkeypatch.setattr("pdf_extract.fetch.MAX_STORED_BULLETIN_BYTES", 8)
    monkeypatch.setattr(
        "pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: b"%PDF still too big",
    )
    _fake_browser(monkeypatch)
    puts = []
    monkeypatch.setattr(get_store(), "put", lambda key, *_a, **_k: puts.append(key))
    _start_run(db, "run-1")

    result = fetch_bulletins(parish_name="Test Parish", run_id="run-1")

    assert puts == []
    assert _bulletins(db) == []
    assert result["failed_parishes"] == 1
    outcome = _results(db, "run-1")["test-parish"]
    assert outcome["status"] == "too_large"
    assert "not stored" in outcome["detail"]


def test_fetch_stores_a_bulletin_exactly_at_the_size_limit(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _serve(monkeypatch, b"%PDF-1.4 big")
    monkeypatch.setattr("pdf_extract.fetch.MAX_STORED_BULLETIN_BYTES", 10)
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: b"%PDF small")
    _fake_browser(monkeypatch)

    fetch_bulletins(parish_name="Test Parish")

    assert len(_bulletins(db)) == 1


def test_fetch_reports_a_download_over_the_limit_as_too_large(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")

    def download(**_):
        raise DownloadTooLarge("Over 1000 MB: https://example.org/bulletin.pdf")

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    _fake_browser(monkeypatch)
    _start_run(db, "run-1")

    result = fetch_bulletins(parish_name="Test Parish", run_id="run-1")

    assert result["failed_parishes"] == 1
    assert _bulletins(db) == []
    assert _results(db, "run-1")["test-parish"]["status"] == "too_large"


DISCOVER_MASS_CAP_PAGE = (
    b"Maximum number of files downloaded today. Please contact "
    b"<a href='https://discovermass.com/contact-us/'>Discover Mass</a> for support."
)


def test_fetch_fails_a_parish_served_a_page_instead_of_its_bulletin(monkeypatch, db: Path) -> None:
    # The 2026-10-25 run stored Discover Mass's cap page as the bulletin, and
    # every run after matched it by hash and called the parish unchanged.
    download = "https://bulletins.discovermass.com/download.php?bulletin=abc%3D"
    cap_hash = hashlib.sha256(DISCOVER_MASS_CAP_PAGE).hexdigest()
    _add_bulletin(
        db, source_url=download, content_hash=cap_hash, pdf_bytes=DISCOVER_MASS_CAP_PAGE,
        fetched_at="2026-10-25T13:16:38Z",
    )
    _link_to(monkeypatch, download)
    monkeypatch.setattr(
        "pdf_extract.fetch._http_get", lambda url, **_: _Response(DISCOVER_MASS_CAP_PAGE),
    )
    _fake_browser(monkeypatch)

    for run_id in ("run-1", "run-2"):
        _start_run(db, run_id)
        result = fetch_bulletins(parish_name="Test Parish", run_id=run_id)
        assert result["failed_parishes"] == 1
        assert result["unchanged_bulletins"] == 0

    outcome = _results(db, "run-2")["test-parish"]
    assert outcome["status"] == "download_failed"
    assert "Maximum number of files downloaded today" in outcome["detail"]
    assert "<a " not in outcome["detail"]
    assert outcome["source_url"] == download
    assert [b["content_hash"] for b in _bulletins(db)] == [cap_hash]
    conn = connect_db(db)
    try:
        assert consecutive_failures(conn, "test-parish", "fetch") == 2
    finally:
        conn.close()


def test_fetch_does_not_count_an_oversized_recheck_as_a_failure(monkeypatch, db: Path) -> None:
    _add_bulletin(
        db, source_url="https://example.org/bulletin.pdf", content_hash="had",
        fetched_at="2026-09-26T09:00:00Z",
    )
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")

    def download(**_):
        raise DownloadTooLarge("Over 1000 MB: https://example.org/bulletin.pdf")

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    _fake_browser(monkeypatch)
    _start_run(db, "run-1")

    result = fetch_bulletins(parish_name="Test Parish", run_id="run-1", today=date(2026, 9, 26))

    assert result["failed_parishes"] == 0
    assert _results(db, "run-1")["test-parish"]["status"] == "recheck_failed"


def test_fetch_keeps_an_already_stored_bulletin(monkeypatch, db: Path) -> None:
    # A PDF stored by a run whose database was not published: the stored copy
    # is not rewritten.
    content_hash = hashlib.sha256(b"%PDF-1.4 same").hexdigest()
    get_store().put(bulletin_pdf_key("test-parish", content_hash), b"%PDF compacted before")
    _link_to(monkeypatch, "https://example.org/a.pdf")
    _serve(monkeypatch, b"%PDF-1.4 same")
    compactions = []
    monkeypatch.setattr(
        "pdf_extract.fetch.compact_bulletin_pdf",
        lambda data, **_: compactions.append(data) or data,
    )
    _fake_browser(monkeypatch)

    fetch_bulletins(parish_name="Test Parish")

    assert compactions == []
    assert [b["content_hash"] for b in _bulletins(db)] == [content_hash]
    assert get_store().get(
        bulletin_pdf_key("test-parish", content_hash)
    ) == b"%PDF compacted before"


def test_fetch_records_each_parish_outcome_for_the_run(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")

    def download(**kwargs):
        if download.calls:
            raise OSError("connection reset")
        download.calls += 1
        return Download(pdf=b"%PDF-1.4 fake")

    download.calls = 0

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    _fake_browser(monkeypatch)
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source",
        lambda parish: FetchSource("ecatholic", parish["slug"]),
    )
    _start_run(db, "run-1")

    result = fetch_bulletins(run_id="run-1")
    assert result["fetched_bulletins"] == 1
    assert result["failed_parishes"] == 2

    statuses = {slug: r["status"] for slug, r in _results(db, "run-1").items()}
    assert statuses == {
        "test-parish": "new",
        "test-parish-1": "download_failed",
        "test-parish-2": "download_failed",
    }


def test_fetch_limits_to_the_given_slugs(monkeypatch, db: Path) -> None:
    monkeypatch.setattr(
        "pdf_extract.fetch._build_bulletin_link",
        lambda bulletin_provider, fetch_provider_id, **_: BulletinLink(
            source_url=f"https://example.org/{fetch_provider_id}.pdf",
            fetch_url=f"https://example.org/{fetch_provider_id}.pdf",
        ),
    )
    _serve(monkeypatch, b"%PDF-1.4 fake")
    _fake_browser(monkeypatch)

    result = fetch_bulletins(slugs=["test-parish-1"])

    assert result["fetched_bulletins"] == 1
    assert [bulletin["parish_slug"] for bulletin in _bulletins(db)] == ["test-parish-1"]
    with pytest.raises(ValueError, match="no-such-parish"):
        fetch_bulletins(slugs=["no-such-parish"])


def test_fetch_never_has_two_requests_in_flight_to_one_site(monkeypatch, db: Path) -> None:
    sources = {
        "test-parish": FetchSource("parishes_online", "first"),
        "test-parish-1": FetchSource("parishes_online", "second"),
        "test-parish-2": FetchSource("other", "https://www.parish-two.org"),
    }
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source", lambda parish: sources[parish["slug"]],
    )
    _fake_browser(monkeypatch)
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: data)

    lock = threading.Lock()
    in_flight: Counter[str] = Counter()
    most: Counter[str] = Counter()

    @contextmanager
    def request(site: str):
        with lock:
            in_flight[site] += 1
            most[site] = max(most[site], in_flight[site])
            most["*"] = max(most["*"], in_flight.total())
        try:
            time.sleep(0.2)
            yield
        finally:
            with lock:
                in_flight[site] -= 1

    def build_link(bulletin_provider, fetch_provider_id, **_):
        if bulletin_provider == "parishes_online":
            with request("parishesonline"):
                url = f"https://container.parishesonline.com/{fetch_provider_id}.pdf"
        else:
            with request("parish-two"):
                url = "https://files.parish-two.org/bulletin.pdf"
        return BulletinLink(source_url=url, fetch_url=url)

    def download(*, fetch_url, source_url, validators=None):
        site = "parishesonline" if "parishesonline" in fetch_url else "parish-two"
        with request(site):
            return Download(pdf=f"%PDF {fetch_url}".encode())

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)

    result = fetch_bulletins()

    assert result["fetched_bulletins"] == 3
    assert most["parishesonline"] == 1
    assert most["parish-two"] == 1
    assert most["*"] == 2, "the two sites were fetched at the same time"


def test_fetch_fails_when_a_worker_crashes(monkeypatch, db: Path) -> None:
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")
    _fake_browser(monkeypatch)

    def download(**kwargs):
        raise RuntimeError("unexpected")

    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)

    with pytest.raises(RuntimeError, match="unexpected"):
        fetch_bulletins()


def test_fetch_stops_the_workers_when_recording_fails(monkeypatch, db: Path) -> None:
    _fake_browser(monkeypatch)
    downloads: list[str] = []

    def build_link(bulletin_provider, fetch_provider_id, **_):
        # The parishes share a site, so they are resolved one after another.
        time.sleep(0.2)
        url = f"https://example.org/{fetch_provider_id}.pdf"
        return BulletinLink(source_url=url, fetch_url=url)

    def download(*, fetch_url, source_url, validators=None):
        downloads.append(fetch_url)
        return Download(pdf=f"%PDF {fetch_url}".encode())

    def record(*args, **kwargs):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    monkeypatch.setattr("pdf_extract.fetch.record_parish_result", record)

    with pytest.raises(sqlite3.OperationalError):
        fetch_bulletins()
    assert len(downloads) < 3, "no parish is started after the failure"


@pytest.mark.parametrize(
    ("url", "site"),
    [
        ("https://parishesonline.com/organization/x", "parishes_online"),
        ("https://container.parishesonline.com/bulletins/06/0144/x.pdf", "parishes_online"),
        ("https://files.ecatholic.com/20434/bulletins/x.pdf", "ecatholic"),
        ("https://bulletins.discovermass.com/download.php?bulletin=1", "discover_mass"),
        ("https://parishes.rcda.org/holycross/bulletin.php", "rcda.org"),
        ("https://www.rcda.org/parishes/x/bulletins", "rcda.org"),
        ("https://www.stpeterparish.us/bulletins", "stpeterparish.us"),
        ("netcatholic.org", "netcatholic.org"),
        ("stmary.org/bulletins//2026", "stmary.org"),
        ("https://www.stmary.org.au/bulletins", "stmary.org.au"),
        ("https://parish.example.co.uk/x.pdf", "example.co.uk"),
        ("http://10.0.0.5/bulletin.pdf", "10.0.0.5"),
    ],
)
def test_fetch_groups_requests_by_site(url: str, site: str) -> None:
    assert _site_for_url(url) == site


def test_fetch_counts_a_hosted_providers_parish_sites_as_the_provider() -> None:
    assert _site_for_source(FetchSource("ecatholic", "https://netcatholic.org")) == "ecatholic"
    assert _site_for_source(FetchSource("parishes_online", "all-saints")) == "parishes_online"
    assert _site_for_source(
        FetchSource("other", "https://www.stpeterparish.us", "")
    ) == "stpeterparish.us"


def test_fetch_waits_to_download_from_a_site_another_worker_holds(
    monkeypatch, db: Path,
) -> None:
    # An "other" parish keeps its bulletin on ParishesOnline, which another
    # worker is fetching a parish from.
    sources = {
        "test-parish": FetchSource("other", "https://www.parish-one.org"),
        "test-parish-1": FetchSource("parishes_online", "second"),
    }
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source", lambda parish: sources.get(parish["slug"]),
    )
    _fake_browser(monkeypatch)
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: data)

    lock = threading.Lock()
    in_flight: Counter[str] = Counter()
    most: Counter[str] = Counter()

    @contextmanager
    def request(site: str):
        with lock:
            in_flight[site] += 1
            most[site] = max(most[site], in_flight[site])
        try:
            time.sleep(0.2)
            yield
        finally:
            with lock:
                in_flight[site] -= 1

    def build_link(bulletin_provider, fetch_provider_id, **_):
        site = "parishesonline" if bulletin_provider == "parishes_online" else "parish-one"
        with request(site):
            url = f"https://container.parishesonline.com/{fetch_provider_id}.pdf"
        return BulletinLink(source_url=url, fetch_url=url)

    def download(*, fetch_url, source_url, validators=None):
        with request("parishesonline"):
            return Download(pdf=f"%PDF {fetch_url}".encode())

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)

    assert fetch_bulletins()["fetched_bulletins"] == 2
    assert most["parishesonline"] == 1


def test_fetch_hands_a_parish_tried_again_to_another_worker(monkeypatch, db: Path) -> None:
    # Two workers. One finishes its parish while the other's browser breaks,
    # and the broken one's relaunch fails: the first worker must still be
    # there to try the parish again.
    sources = {
        "test-parish": FetchSource("other", "https://www.parish-one.org"),
        "test-parish-1": FetchSource("other", "https://www.parish-two.org"),
    }
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source", lambda parish: sources.get(parish["slug"]),
    )

    class Page:
        crashed = False

        def goto(self, url, **_) -> None:
            if self.crashed:
                raise RuntimeError("Target page, context or browser has been closed")

    lock = threading.Lock()
    launches = 0

    @contextmanager
    def launch():
        nonlocal launches
        with lock:
            launches += 1
            if launches > 2:
                raise RuntimeError("Chrome would not start")
        yield Page()

    attempts: Counter[str] = Counter()

    def build_link(bulletin_provider, fetch_provider_id, *, page, **_):
        attempts[fetch_provider_id] += 1
        if "parish-one" in fetch_provider_id and attempts[fetch_provider_id] == 1:
            time.sleep(0.3)
            page.crashed = True
            raise RuntimeError("Target page, context or browser has been closed")
        url = f"{fetch_provider_id}/bulletin.pdf"
        return BulletinLink(source_url=url, fetch_url=url)

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", launch)
    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: data)
    _serve(monkeypatch, b"%PDF one", b"%PDF two")

    assert fetch_bulletins(workers=2)["fetched_bulletins"] == 2
    assert attempts["https://www.parish-one.org"] == 2


def test_fetch_records_a_cut_off_download_as_failed(monkeypatch, db: Path) -> None:
    _fake_browser(monkeypatch)
    _link_to(monkeypatch, "https://example.org/bulletin.pdf")

    def http_get(url, **_):
        raise http.client.IncompleteRead(b"%PDF", 1000)

    monkeypatch.setattr("pdf_extract.fetch._http_get", http_get)

    assert fetch_bulletins(parish_name="Test Parish")["failed_parishes"] == 1


def test_fetch_carries_on_when_a_workers_browser_will_not_launch(monkeypatch, db: Path) -> None:
    sources = {
        slug: FetchSource("other", f"https://www.{slug}.org")
        for slug in ("test-parish", "test-parish-1", "test-parish-2")
    }
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source", lambda parish: sources.get(parish["slug"]),
    )
    lock = threading.Lock()
    launches = 0

    @contextmanager
    def launch():
        nonlocal launches
        with lock:
            launches += 1
            if launches == 1:
                raise RuntimeError("Chrome would not start")
        yield None

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", launch)
    _link_to(monkeypatch, "https://example.org/a.pdf")
    _serve(monkeypatch, b"%PDF a", b"%PDF b", b"%PDF c")

    assert fetch_bulletins(workers=3)["fetched_bulletins"] == 3


def test_fetch_fails_when_no_browser_will_launch(monkeypatch, db: Path) -> None:
    @contextmanager
    def launch():
        raise RuntimeError("Chrome would not start")
        yield

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", launch)
    _link_to(monkeypatch, "https://example.org/a.pdf")

    with pytest.raises(RuntimeError, match="No browser could be launched") as raised:
        fetch_bulletins()
    assert "Chrome would not start" in str(raised.value.__cause__)


def test_fetch_relaunches_a_broken_browser_and_tries_its_parish_again(
    monkeypatch, db: Path,
) -> None:
    class Page:
        crashed = False

        def goto(self, url, **_) -> None:
            if self.crashed:
                raise RuntimeError("Target page, context or browser has been closed")

    pages: list[Page] = []

    @contextmanager
    def launch():
        pages.append(Page())
        yield pages[-1]

    def build_link(bulletin_provider, fetch_provider_id, *, page, **_):
        if len(pages) == 1:
            page.crashed = True
            raise RuntimeError("Target page, context or browser has been closed")
        return BulletinLink(source_url="https://example.org/a.pdf", fetch_url="https://example.org/a.pdf")

    monkeypatch.setattr("pdf_extract.fetch.launch_stealth_browser", launch)
    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    _serve(monkeypatch, b"%PDF a")

    assert fetch_bulletins(parish_name="Test Parish")["fetched_bulletins"] == 1
    assert len(pages) == 2


def test_fetch_logs_a_workers_error_when_recording_fails(monkeypatch, db: Path, caplog) -> None:
    sources = {
        "test-parish": FetchSource("other", "https://www.parish-one.org"),
        "test-parish-1": FetchSource("other", "https://www.parish-two.org"),
    }
    monkeypatch.setattr(
        "pdf_extract.fetch._resolve_fetch_source", lambda parish: sources.get(parish["slug"]),
    )
    _fake_browser(monkeypatch)

    def build_link(bulletin_provider, fetch_provider_id, **_):
        url = f"{fetch_provider_id}/bulletin.pdf"
        return BulletinLink(source_url=url, fetch_url=url)

    def download(*, fetch_url, source_url, validators=None):
        if "parish-two" in fetch_url:
            time.sleep(0.3)
            raise RuntimeError("worker broke")
        return Download(pdf=b"%PDF one")

    def record(*args, **kwargs):
        raise sqlite3.OperationalError("database is locked")

    monkeypatch.setattr("pdf_extract.fetch._build_bulletin_link", build_link)
    monkeypatch.setattr("pdf_extract.fetch._download_bulletin", download)
    monkeypatch.setattr("pdf_extract.fetch.compact_bulletin_pdf", lambda data, **_: data)
    monkeypatch.setattr("pdf_extract.fetch.record_parish_result", record)

    with caplog.at_level(logging.ERROR), pytest.raises(sqlite3.OperationalError):
        fetch_bulletins()
    assert "worker broke" in caplog.text
