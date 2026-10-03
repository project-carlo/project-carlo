"""Tests for telling a downloaded bulletin we already have from a new one."""

from __future__ import annotations

import hashlib

from pdf_extract.duplicates import (
    MIN_WORDS_PER_PAGE,
    Validators,
    identify,
    text_fingerprint,
    validators_for,
)


def _text_pdf(pages: list[str]) -> bytes:
    """A minimal PDF with each page's text in Helvetica, one line per 12 words."""
    objects: list[bytes] = []

    def add(body: bytes) -> int:
        objects.append(body)
        return len(objects)

    font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids = []
    pages_id = len(pages) * 2 + 2
    for text in pages:
        words = text.split()
        lines = [" ".join(words[i:i + 12]) for i in range(0, len(words), 12)]
        stream = b"BT /F1 9 Tf 11 TL 36 760 Td " + b" ".join(
            b"(" + line.encode("latin-1") + b") Tj T*" for line in lines
        ) + b" ET"
        content = add(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream))
        page_ids.append(add(
            b"<< /Type /Page /Parent %d 0 R /MediaBox [0 0 612 792] /Contents %d 0 R"
            b" /Resources << /Font << /F1 %d 0 R >> >> >>" % (pages_id, content, font)
        ))
    kids = b" ".join(b"%d 0 R" % i for i in page_ids)
    assert add(b"<< /Type /Pages /Kids [%s] /Count %d >>" % (kids, len(page_ids))) == pages_id
    catalog = add(b"<< /Type /Catalog /Pages %d 0 R >>" % pages_id)

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objects) + 1, catalog, xref,
    )
    return bytes(out)


def _typed_bulletin(week: str, *, pages: int = 4) -> list[str]:
    return [
        f"Bulletin for the week of {week} page {page} " + " ".join(
            f"word{i}" for i in range(MIN_WORDS_PER_PAGE + 20)
        )
        for page in range(pages)
    ]


def _stored(id: int, pdf: bytes, *, week: str, fingerprint: str | None = None) -> dict:
    return {
        "id": id,
        "source_url": f"https://example.org/{id}.pdf",
        "content_hash": hashlib.sha256(pdf).hexdigest(),
        "text_fingerprint": fingerprint if fingerprint is not None else text_fingerprint(pdf),
        "published_date": week,
        "fetched_at": f"{week}T09:00:00Z",
    }


def test_text_fingerprint_ignores_layout_but_not_words() -> None:
    pages = _typed_bulletin("2026-10-04")
    fingerprint = text_fingerprint(_text_pdf(pages))
    assert fingerprint is not None and fingerprint.startswith("4:")
    respaced = [page.replace(" ", "   ").upper() for page in pages]
    assert text_fingerprint(_text_pdf(respaced)) == fingerprint
    assert text_fingerprint(_text_pdf(_typed_bulletin("2026-10-11"))) != fingerprint


def test_text_fingerprint_needs_typed_pages() -> None:
    # A scan with a typed cover: too little text to tell one week from the next.
    thin = ["Saint Mary Parish " + " ".join(f"w{i}" for i in range(600))] + [""] * 7
    assert text_fingerprint(_text_pdf(thin)) is None
    assert text_fingerprint(_text_pdf(["a few words"])) is None
    assert text_fingerprint(b"not a pdf") is None


def test_identify_matches_the_same_bytes_from_any_address_or_week() -> None:
    pdf = _text_pdf(_typed_bulletin("2026-09-06"))
    stored = [_stored(1, pdf, week="2026-09-06")] + [
        _stored(i, b"%%PDF other %d" % i, week=f"2026-09-{i + 10}") for i in range(2, 8)
    ]
    identified = identify(pdf, stored)
    assert identified.duplicate is not None
    assert (identified.duplicate.bulletin["id"], identified.duplicate.how) == (1, "byte hash")


def test_identify_matches_a_rebuilt_file_by_its_text() -> None:
    pages = _typed_bulletin("2026-10-04")
    stored = [_stored(1, _text_pdf(pages), week="2026-10-04")]
    rebuilt = _text_pdf([page + " " for page in pages]) + b"% rebuilt\n"

    identified = identify(rebuilt, stored)

    assert identified.duplicate is not None
    assert identified.duplicate.describe() == "same bulletin as #1 (same text)"


def test_identify_compares_text_with_recent_bulletins_only() -> None:
    pages = _typed_bulletin("2026-08-02")
    stored = [_stored(1, _text_pdf(pages), week="2026-08-02")] + [
        _stored(i, b"%%PDF later %d" % i, week=f"2026-09-{i + 10:02d}", fingerprint="")
        for i in range(2, 7)
    ]
    rebuilt = _text_pdf([page + " " for page in pages]) + b"% rebuilt\n"
    assert identify(rebuilt, stored).duplicate is None


def test_identify_does_not_match_by_text_where_the_text_never_changes() -> None:
    # Two weeks of one parish that read word for word alike: its text says
    # nothing about which week a PDF is.
    pages = _typed_bulletin("every week")
    stored = [
        _stored(1, _text_pdf(pages) + b"% one\n", week="2026-09-27"),
        _stored(2, _text_pdf(pages) + b"% two\n", week="2026-10-04"),
    ]
    identified = identify(_text_pdf(pages) + b"% three\n", stored)
    assert identified.duplicate is None
    assert identified.text_fingerprint == stored[0]["text_fingerprint"]


def test_identify_reports_fingerprints_of_a_new_bulletin() -> None:
    pdf = _text_pdf(_typed_bulletin("2026-10-11"))
    last_week = _stored(1, _text_pdf(_typed_bulletin("2026-10-04")), week="2026-10-04")
    identified = identify(pdf, [last_week])
    assert identified.duplicate is None
    assert identified.content_hash == hashlib.sha256(pdf).hexdigest()
    assert identified.text_fingerprint == text_fingerprint(pdf)


def test_validators_for_takes_the_latest_copy_from_the_address() -> None:
    stored = [
        {"id": 1, "source_url": "https://x/b.pdf", "etag": '"a"', "fetched_at": "2026-09-26"},
        {"id": 2, "source_url": "https://x/b.pdf", "etag": '"b"', "fetched_at": "2026-10-03"},
        {"id": 3, "source_url": "https://x/c.pdf", "etag": '"c"', "fetched_at": "2026-10-04"},
        {"id": 4, "source_url": "https://x/b.pdf", "fetched_at": "2026-10-05"},
    ]
    known = validators_for("https://x/b.pdf", stored)
    assert known is not None and known.bulletin["id"] == 2
    assert validators_for("https://x/new.pdf", stored) is None


def test_validators_headers() -> None:
    assert Validators('"a"', "Sat, 03 Oct 2026").request_headers() == {
        "If-None-Match": '"a"', "If-Modified-Since": "Sat, 03 Oct 2026",
    }
    assert not Validators()
