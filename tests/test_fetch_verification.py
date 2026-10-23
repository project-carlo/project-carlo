"""Offline evidence checks using real, small PDFs and recorded-page resolvers."""

from contextlib import nullcontext
from datetime import date
from io import BytesIO
from urllib.error import URLError

import pytest
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from pdf_extract import fetch, fetch_check
from pdf_extract.fetch_check import PageSnapshot, SnapshotPage, _check_one, check_fetch

TODAY = date(2026, 10, 21)
HOME = "https://example.org"
FIXED = f"{HOME}/current.pdf"
IDENTITY = "Saint Joseph Parish, Renovo"


def _pdf(*lines: str) -> bytes:
    """A real text PDF, exercising the same parser as downloaded documents."""
    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    font = DictionaryObject({
        NameObject("/Type"): NameObject("/Font"),
        NameObject("/Subtype"): NameObject("/Type1"),
        NameObject("/BaseFont"): NameObject("/Helvetica"),
    })
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)}),
    })
    content = DecodedStreamObject()
    commands = ["BT /F1 12 Tf 30 760 Td 16 TL"]
    for line in lines:
        literal = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        commands.append(f"({literal}) Tj T*")
    commands.append("ET")
    content.set_data("\n".join(commands).encode("ascii"))
    page[NameObject("/Contents")] = writer._add_object(content)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def _check(monkeypatch, pdf: bytes, *, url: str = FIXED, fetch_url: str | None = None, **kwargs):
    monkeypatch.setattr(
        fetch_check, "_resolve", lambda *a, **k: fetch.BulletinLink(url, fetch_url or url),
    )
    monkeypatch.setattr(fetch, "_download_pdf", lambda **k: pdf)
    return _check_one(
        "renovo", fetch.FetchSource("other", HOME), SnapshotPage([]),
        reference_date=TODAY, download=kwargs.pop("download", True), **kwargs,
    )


def test_successful_stale_renovo_issue_keeps_legacy_ok(monkeypatch):
    row = _check(
        monkeypatch, _pdf(IDENTITY, "October 4, 2026"), expected_identity=IDENTITY,
        expected_issue_date=date(2026, 10, 18),
    )
    assert row["status"] == "ok"
    verification = row["verification"]
    assert verification["transport"]["status"] == "ok"
    assert verification["document_type"]["status"] == "pdf"
    assert verification["publication_identity"]["status"] == "matched"
    assert verification["issue_date"]["date"] == "2026-10-04"
    assert verification["issue_date"]["expected_status"] == "mismatch"
    assert verification["freshness"] == {
        "status": "stale", "max_issue_age_days": 14, "age_days": 17, "date_status": "observed",
    }
    assert verification["overall"] == "failed"


def test_wrong_publication_does_not_pass_from_successful_pdf(monkeypatch):
    row = _check(
        monkeypatch, _pdf("Saint Anne Parish, Johnstown", "October 18, 2026"),
        expected_identity=IDENTITY,
    )
    assert row["status"] == "ok"
    verification = row["verification"]
    assert verification["publication_identity"]["status"] == "not_matched"
    assert verification["freshness"]["status"] == "fresh"
    assert verification["overall"] == "failed"


def test_fixed_url_with_no_issue_date_stays_unknown_despite_expected_date(monkeypatch):
    row = _check(
        monkeypatch, _pdf(IDENTITY, "Parish bulletin", "Dinner October 18, 2026 at 6 pm"),
        expected_identity=IDENTITY, expected_issue_date=date(2026, 10, 18),
    )
    verification = row["verification"]
    assert "url_date" not in row
    assert verification["issue_date"]["status"] == "unknown"
    assert verification["issue_date"]["expected_status"] == "unknown"
    assert verification["freshness"]["status"] == "unknown"
    assert verification["overall"] == "unverified"


def test_document_identity_is_never_inferred_without_expectation(monkeypatch):
    verification = _check(monkeypatch, _pdf(IDENTITY, "October 18, 2026"))["verification"]
    assert verification["publication_identity"]["status"] == "unverified"
    assert verification["overall"] == "unverified"


def test_current_document_matching_explicit_expectations_is_verified(monkeypatch):
    verification = _check(
        monkeypatch, _pdf(IDENTITY.upper(), "Bulletin date: October 18, 2026"),
        expected_identity="Saint Joseph Parish Renovo", expected_issue_date=date(2026, 10, 18),
    )["verification"]
    assert verification["overall"] == "verified"
    assert verification["issue_date"]["expected_status"] == "matched"


@pytest.mark.parametrize("printed", ["18 Oct. 2025", "Oct. 18, 2025", "10/18/25"])
def test_explicit_old_year_cannot_become_current_during_verification(monkeypatch, printed):
    verification = _check(
        monkeypatch, _pdf(IDENTITY, printed), expected_identity=IDENTITY,
        expected_issue_date=date(2026, 10, 18),
    )["verification"]
    assert verification["issue_date"]["date"] == "2025-10-18"
    assert verification["issue_date"]["expected_status"] == "mismatch"
    assert verification["freshness"]["status"] == "stale"
    assert verification["overall"] == "failed"


def test_identity_does_not_match_inside_a_different_word(monkeypatch):
    verification = _check(
        monkeypatch, _pdf("Saint Josephine Parish", "October 18, 2026"),
        expected_identity="Saint Joseph",
    )["verification"]
    assert verification["publication_identity"]["status"] == "not_matched"


@pytest.mark.parametrize("download", [False, True])
def test_filename_date_is_inferred_and_never_document_verified(monkeypatch, download):
    row = _check(
        monkeypatch, _pdf(IDENTITY), url=f"{HOME}/bulletin-20261004.pdf",
        expected_identity=IDENTITY, download=download,
    )
    verification = row["verification"]
    assert row["status"] == "ok"
    assert row["url_date"] == "2026-10-04"
    assert verification["issue_date"]["status"] == "inferred"
    assert verification["freshness"]["status"] == "stale"
    assert verification["transport"]["status"] == ("ok" if download else "not_checked")
    assert verification["document_type"]["status"] == ("pdf" if download else "not_checked")
    assert verification["overall"] == "failed"


def test_no_download_leaves_transport_and_identity_unchecked(monkeypatch):
    def unexpected_download(**kwargs):
        pytest.fail("no-download must not download")

    _check(monkeypatch, b"")
    monkeypatch.setattr(fetch, "_download_pdf", unexpected_download)
    row = _check_one(
        "renovo", fetch.FetchSource("other", HOME), SnapshotPage([]),
        reference_date=TODAY, download=False, expected_identity=IDENTITY,
    )
    assert row["status"] == "ok"
    verification = row["verification"]
    assert verification["transport"]["status"] == "not_checked"
    assert verification["publication_identity"]["status"] == "unknown"
    assert verification["overall"] == "unverified"


def test_upload_folder_and_query_are_not_issue_dates(monkeypatch):
    row = _check(
        monkeypatch, _pdf(IDENTITY),
        url=f"{HOME}/uploads/2026/10/current.pdf?uploaded=20261018",
    )
    assert row["verification"]["issue_date"]["status"] == "unknown"


@pytest.mark.parametrize("content,document_type,legacy", [
    (b"<html>Not a bulletin</html>", "not_pdf", "not_pdf"),
    (b"%PDF-1.7 truncated", "invalid_pdf", "ok"),
])
def test_transport_success_is_separate_from_pdf_validity(
    monkeypatch, content, document_type, legacy,
):
    row = _check(monkeypatch, content)
    assert row["status"] == legacy
    assert row["verification"]["transport"]["status"] == "ok"
    assert row["verification"]["document_type"]["status"] == document_type
    assert row["verification"]["overall"] == "failed"


def test_download_failure_keeps_independent_url_evidence(monkeypatch):
    _check(monkeypatch, b"", url=f"{HOME}/20261018.pdf")

    def unavailable(**kwargs):
        raise URLError("offline fixture")

    monkeypatch.setattr(fetch, "_download_pdf", unavailable)
    row = _check_one(
        "renovo", fetch.FetchSource("other", HOME), SnapshotPage([]),
        reference_date=TODAY, download=True,
    )
    assert row["status"] == "download_failed"
    assert row["verification"]["transport"]["status"] == "failed"
    assert row["verification"]["issue_date"]["status"] == "inferred"
    assert row["verification"]["overall"] == "failed"


def test_resolution_failure_still_has_verification_dimensions():
    row = _check_one(
        "renovo", fetch.FetchSource("other", HOME), SnapshotPage([]),
        reference_date=TODAY, download=True,
    )
    assert row["status"] == "resolve_failed"
    assert row["verification"]["transport"]["status"] == "not_checked"
    assert row["verification"]["overall"] == "failed"


@pytest.mark.parametrize("lines,url", [
    ((IDENTITY, "October 4, 2026"), f"{HOME}/20261018.pdf"),
    ((IDENTITY, "October 4, 2026", "October 18, 2026"), FIXED),
])
def test_conflicting_dates_stay_unknown(monkeypatch, lines, url):
    verification = _check(monkeypatch, _pdf(*lines), url=url)["verification"]
    assert verification["issue_date"]["status"] == "conflict"
    assert verification["freshness"]["status"] == "unknown"
    assert verification["overall"] == "unverified"


def test_fetch_url_date_is_evidence_from_the_selected_download(monkeypatch):
    row = _check(monkeypatch, _pdf(), fetch_url=f"{HOME}/20261004.pdf")
    assert row["verification"]["freshness"]["status"] == "stale"
    assert row["verification"]["issue_date"]["evidence"] == [{
        "date": "2026-10-04", "source": "fetch_url", "url": f"{HOME}/20261004.pdf",
    }]


@pytest.mark.parametrize("issue,threshold,status", [
    ("October 7, 2026", 14, "fresh"),
    ("October 7, 2026", 13, "stale"),
    ("October 25, 2026", 14, "future"),
])
def test_freshness_threshold_is_inclusive_and_future_is_separate(
    monkeypatch, issue, threshold, status,
):
    verification = _check(
        monkeypatch, _pdf(IDENTITY, issue), expected_identity=IDENTITY,
        max_issue_age_days=threshold,
    )["verification"]
    assert verification["freshness"]["status"] == status
    if status == "future":
        assert verification["overall"] == "unverified"


def test_scanned_or_oversized_documents_do_not_verify_identity(monkeypatch):
    verification = _check(monkeypatch, _pdf(), expected_identity=IDENTITY)["verification"]
    assert verification["document_type"]["status"] == "pdf"
    assert verification["publication_identity"]["status"] == "unknown"
    assert verification["overall"] == "unverified"
    monkeypatch.setattr(fetch_check, "_VERIFY_MAX_BYTES", 1)
    verification = _check(
        monkeypatch, _pdf(IDENTITY, "October 18, 2026"), expected_identity=IDENTITY,
    )["verification"]
    assert verification["document_type"]["status"] == "pdf_signature"
    assert verification["publication_identity"]["status"] == "unknown"


def test_masthead_read_is_bounded(monkeypatch):
    monkeypatch.setattr(fetch_check, "_MASTHEAD_CHARS", 10)
    verification = _check(
        monkeypatch, _pdf("Unrelated heading", IDENTITY, "October 18, 2026"),
        expected_identity=IDENTITY,
    )["verification"]
    assert verification["publication_identity"]["status"] == "not_matched"
    assert verification["issue_date"]["status"] == "unknown"


def test_check_fetch_summaries_and_slug_expectations_preserve_legacy_counts(monkeypatch):
    monkeypatch.setattr(fetch_check, "launch_stealth_browser", lambda: nullcontext(SnapshotPage([])))
    monkeypatch.setattr(
        fetch_check, "_resolve",
        lambda source, **k: fetch.BulletinLink(source.provider_id, source.provider_id),
    )
    documents = {
        f"{HOME}/a.pdf": _pdf(IDENTITY, "October 18, 2026"),
        f"{HOME}/b.pdf": _pdf("Saint Anne Parish", "October 4, 2026"),
        f"{HOME}/c.pdf": _pdf("Some publication"),
    }
    monkeypatch.setattr(fetch, "_download_pdf", lambda fetch_url, **k: documents[fetch_url])
    rows = [
        {"slug": slug, "website": url, "bulletin_provider": "other", "provider_id": ""}
        for slug, url in zip("abc", documents, strict=True)
    ]
    result = check_fetch(
        parishes=rows, reference_date=TODAY,
        expected_identity={"a": IDENTITY, "b": "Saint Anne Parish"},
        expected_issue_date={"a": date(2026, 10, 18)},
    )
    assert result["counts"] == {"ok": 3}
    summary = result["verification_counts"]
    assert summary["overall"] == {"verified": 1, "failed": 1, "unverified": 1}
    assert summary["transport"] == {"ok": 3}
    assert summary["publication_identity"] == {"matched": 2, "unverified": 1}
    assert summary["freshness"] == {"fresh": 1, "stale": 1, "unknown": 1}


@pytest.mark.parametrize("kwargs", [
    {"max_issue_age_days": -1}, {"expected_identity": "  "}, {"expected_identity": {"a": "!"}},
])
def test_invalid_verification_configuration_fails_before_browser_launch(monkeypatch, kwargs):
    def unexpected_browser():
        pytest.fail("invalid configuration must fail before launching browser")

    monkeypatch.setattr(fetch_check, "launch_stealth_browser", unexpected_browser)
    with pytest.raises(ValueError):
        check_fetch(parishes=[], **kwargs)


@pytest.mark.parametrize("other_first", [False, True])
def test_shared_page_verifies_selected_own_issue_during_delayed_upload(monkeypatch, other_first):
    own = '<a href="/St-Annes-Bulletin-Oct-4-2026.pdf">October 4, 2026</a>'
    other = '<a href="/STTHERESESBULLETIN-Oct-18-2026.pdf">October 18, 2026</a>'
    links = other + own if other_first else own + other
    page = SnapshotPage([PageSnapshot(HOME, HOME, links)])
    requested = []

    def download(fetch_url, **kwargs):
        requested.append(fetch_url)
        return _pdf("Saint Anne Parish", "October 4, 2026")

    monkeypatch.setattr(fetch, "_download_pdf", download)
    row = _check_one(
        "anne", fetch.FetchSource("other", HOME, "page-pdfs filename=St-Annes-Bulletin*.pdf"),
        page, reference_date=TODAY, download=True, expected_identity="Saint Anne Parish",
    )
    assert requested == [f"{HOME}/St-Annes-Bulletin-Oct-4-2026.pdf"]
    assert row["status"] == "ok"
    assert row["verification"]["publication_identity"]["status"] == "matched"
    assert row["verification"]["freshness"]["status"] == "stale"
