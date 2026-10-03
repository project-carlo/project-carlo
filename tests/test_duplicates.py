"""Tests for telling a downloaded bulletin we already have from a new one."""

from __future__ import annotations

import hashlib

from pdf_extract.duplicates import Validators, bulletin_hash, find_duplicate, validators_for


def _stored(id: int, pdf: bytes, *, week: str) -> dict:
    return {
        "id": id,
        "source_url": f"https://example.org/{id}.pdf",
        "content_hash": bulletin_hash(pdf),
        "published_date": week,
        "fetched_at": f"{week}T09:00:00Z",
    }


def test_bulletin_hash_is_the_sha256_of_the_download() -> None:
    assert bulletin_hash(b"%PDF-1.4") == hashlib.sha256(b"%PDF-1.4").hexdigest()


def test_find_duplicate_matches_the_same_bytes_from_any_address_or_week() -> None:
    stored = [_stored(1, b"%PDF week 36", week="2026-09-06")] + [
        _stored(i, b"%%PDF other %d" % i, week=f"2026-09-{i + 10}") for i in range(2, 8)
    ]
    duplicate = find_duplicate(bulletin_hash(b"%PDF week 36"), stored)
    assert duplicate is not None
    assert duplicate.describe() == "same bulletin as #1 (byte hash)"
    assert find_duplicate(bulletin_hash(b"%PDF new"), stored) is None


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
