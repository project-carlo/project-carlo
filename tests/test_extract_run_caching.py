"""Caching behavior of the experimental classifier runner."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import extract_run, runner
from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.classifiers import REGISTRY
from pdf_extract.db import create_db
from pdf_extract.storage import churches_for_parish, connect_db, load_bulletins


class _CountingClassifier:
    """Records every call so the test can assert cache hits skip the real call."""

    name = "counting"
    version = "v1"

    def __init__(self, payload: dict[str, Any]) -> None:
        self._payload = payload
        self.call_count = 0

    def extract(self, pdf_bytes, *, churches, today: date):
        self.call_count += 1
        return self._payload


def _payload_one_event() -> dict[str, Any]:
    return {
        "events": [
            {
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
        ],
        "church_list_needs_review": False,
        "published_date": None,
        "wrong_bulletin": False,
    }


def _churches() -> list[dict[str, Any]]:
    conn = connect_db()
    try:
        return churches_for_parish(conn, "test-parish")
    finally:
        conn.close()


@pytest.fixture
def seeded_run(pipeline_dir: Path, monkeypatch):
    """One unprocessed bulletin for test-parish and a counting classifier."""
    create_db()
    get_store().put(bulletin_pdf_key("test-parish", "hash-abc"), b"fake")
    conn = connect_db()
    with conn:
        conn.execute(
            """INSERT INTO bulletin(parish_id, source_url, content_hash, fetched_at)
               SELECT id, 'https://example.org/parsed.pdf', 'hash-abc',
                      '2026-01-01T00:00:00Z'
               FROM parish WHERE slug = 'test-parish'"""
        )
    conn.close()

    # Skip the pypdf truncation helper for these stub PDFs.
    monkeypatch.setattr("pdf_extract.storage.ensure_truncated_pdf", lambda path, **kwargs: path)
    classifier = _CountingClassifier(_payload_one_event())
    monkeypatch.setitem(REGISTRY, classifier.name, lambda: classifier)
    return pipeline_dir, classifier


def test_first_run_calls_classifier_and_writes_outputs(seeded_run):
    tmp_path, classifier = seeded_run

    summary = extract_run.run(classifier_name="counting", concurrency=1)

    assert classifier.call_count == 1
    assert summary["cache_hits"] == 0
    assert summary["cache_misses"] == 1
    assert summary["events_written"] == 1

    cached = json.loads(get_store().get(runner.cache_key("counting", "v1", "hash-abc", _churches())))
    assert cached["events"][0]["church_slug"] == "st-mary-anytown"

    bulletins_file = extract_run.bulletins_path("counting")
    bulletins = json.loads(bulletins_file.read_text(encoding="utf-8"))
    assert bulletins == [
        {
            "bulletin_source_url": "https://example.org/parsed.pdf",
            "pdf_path": "data/bulletins/test-parish/hash-abc.pdf",
            "parish_slug": "test-parish",
            "published_date": None,
            "content_hash": "hash-abc",
            "event_count": 1,
            "wrong_bulletin": False,
            "published_date_extracted": None,
            "cache_hit": False,
            "usage": {},
            "timing": {},
            "text_chars": None,
        }
    ]

    events_file = tmp_path / "data" / "runs" / "counting" / "events.json"
    events = json.loads(events_file.read_text(encoding="utf-8"))
    assert events[0]["bulletin_source_url"] == "https://example.org/parsed.pdf"
    assert events[0]["event_type"] == "mass"


def test_second_run_serves_from_cache_without_calling_classifier(seeded_run):
    _, classifier = seeded_run

    extract_run.run(classifier_name="counting", concurrency=1)
    assert classifier.call_count == 1

    summary = extract_run.run(classifier_name="counting", concurrency=1)
    assert classifier.call_count == 1, "cache hit should skip classifier"
    assert summary["cache_hits"] == 1
    assert summary["cache_misses"] == 0
    assert summary["events_written"] == 1


def test_cache_miss_after_classifier_version_changes(seeded_run):
    _, classifier = seeded_run

    extract_run.run(classifier_name="counting", concurrency=1)
    assert classifier.call_count == 1

    classifier.version = "v2"
    summary = extract_run.run(classifier_name="counting", concurrency=1)

    assert classifier.call_count == 2
    assert summary["cache_hits"] == 0
    assert summary["cache_misses"] == 1
    assert get_store().exists(runner.cache_key("counting", "v2", "hash-abc", _churches()))


def test_run_does_not_touch_processed_at(seeded_run):
    extract_run.run(classifier_name="counting", concurrency=1)

    conn = connect_db()
    try:
        bulletins = load_bulletins(conn)
    finally:
        conn.close()
    assert bulletins[0]["processed_at"] is None, (
        "experimental runs must not mark bulletins as processed for the prod path"
    )


def test_unknown_classifier_raises(seeded_run):
    with pytest.raises(KeyError):
        extract_run.run(classifier_name="nope")


def test_a_failed_cache_write_does_not_fail_the_run(seeded_run, monkeypatch):
    """The cache is an optimisation: losing a write must not lose the extraction."""
    def failing_put(*args, **kwargs):
        raise RuntimeError("R2 unavailable")

    monkeypatch.setattr(get_store(), "put", failing_put)

    summary = extract_run.run(classifier_name="counting", concurrency=1)

    assert summary["events_written"] == 1
    assert summary["errors"] == []


def test_cache_miss_after_the_church_list_changes(seeded_run):
    """Results name church slugs from the prompt's list, so a new list re-extracts."""
    tmp_path, classifier = seeded_run
    extract_run.run(classifier_name="counting", concurrency=1)

    churches_csv = tmp_path / "data" / "churches.csv"
    churches_csv.write_text(
        churches_csv.read_text(encoding="utf-8").replace("Test Church", "Renamed Church"),
        encoding="utf-8",
    )
    create_db()  # re-seed from the edited CSV
    get_store().put(bulletin_pdf_key("test-parish", "hash-abc"), b"fake")
    conn = connect_db()
    with conn:
        conn.execute(
            """INSERT INTO bulletin(parish_id, source_url, content_hash, fetched_at)
               SELECT id, 'https://example.org/parsed.pdf', 'hash-abc', '2026-01-01T00:00:00Z'
               FROM parish WHERE slug = 'test-parish'"""
        )
    conn.close()

    summary = extract_run.run(classifier_name="counting", concurrency=1)

    assert classifier.call_count == 2
    assert summary["cache_hits"] == 0
