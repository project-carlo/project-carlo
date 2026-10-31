"""Fetch-only parishes: fetched every week, but not processed or shown on the site."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

import pytest

from pdf_extract.apply import apply_detect_results
from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.db import create_db, ensure_db
from pdf_extract.extract_frontend_db import extract, read_snapshot
from pdf_extract.process import process_bulletins
from pdf_extract.report import build_report, render_markdown
from pdf_extract.runs import record_parish_result, start_run
from pdf_extract.storage import (
    DEFAULT_DB_PATH,
    connect_db,
    fetch_only_slugs,
    insert_bulletin,
    load_bulletins,
    save_processed_bulletin,
    utc_now_iso,
)
from tests.conftest import CHURCH_FIELDS, PARISH_FIELDS, write_csv

FIELDS = [*PARISH_FIELDS, "fetch_only"]


def _write_parishes(work: Path, *, held: bool = True) -> None:
    write_csv(work / "data" / "parishes.csv", FIELDS, [
        {"slug": "live-parish", "name": "Live Parish", "website": "https://live.org"},
        {"slug": "new-parish", "name": "New Parish", "website": "https://new.org",
         "fetch_only": "true" if held else ""},
    ])


@pytest.fixture
def work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A database with a live parish and a fetch-only one, one church each."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    _write_parishes(work)
    write_csv(work / "data" / "churches.csv", CHURCH_FIELDS, [
        {"parish_id": slug, "slug": f"{slug}-church", "name": "St. Mary", "line1": "1 Main St",
         "city": "Town", "state": "NY", "postal_code": "14000"}
        for slug in ("live-parish", "new-parish")
    ])
    create_db()
    monkeypatch.setattr("pdf_extract.storage.ensure_truncated_pdf", lambda path, **kwargs: path)
    return work


def _add_bulletin(slug: str, *, events: list[dict] | None = None) -> int:
    """A fetched bulletin for `slug`; processed with `events` when they are given."""
    get_store().put(bulletin_pdf_key(slug, slug), b"fake")
    conn = connect_db()
    try:
        parish_id = conn.execute("SELECT id FROM parish WHERE slug = ?", (slug,)).fetchone()[0]
        bulletin_id = insert_bulletin(
            conn, parish_id=parish_id, source_url=f"https://example.org/{slug}.pdf",
            content_hash=slug, fetched_at=utc_now_iso(),
        )
        if events is not None:
            save_processed_bulletin(
                conn, bulletin_id, events, processed_at=utc_now_iso(),
                published_date="2026-10-11",
            )
        return bulletin_id
    finally:
        conn.close()


def _mass(church_slug: str) -> dict:
    return {
        "church_slug": church_slug, "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM", "end_time": None,
        "cancelled": False,
    }


def _processed() -> set[str]:
    conn = connect_db()
    try:
        return {b["parish_slug"] for b in load_bulletins(conn) if b["processed_at"]}
    finally:
        conn.close()


@pytest.fixture
def extractor(monkeypatch: pytest.MonkeyPatch) -> list[bytes]:
    """Stand in for Gemini; returns the PDFs it was called with."""
    calls: list[bytes] = []

    def extract_events(pdf_bytes, *, churches, model=None, today=None):
        calls.append(pdf_bytes)
        event = {
            "church_slug": churches[0]["slug"], "type": "mass", "kind": "weekly",
            "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM", "end_time": None,
            "cancelled": False, "page_number": 1, "note": None,
        }
        return {"events": [event], "church_list_needs_review": False,
                "published_date": None, "wrong_bulletin": False}

    monkeypatch.setattr("pdf_extract.classifiers.gemini.extract_events", extract_events)
    return calls


@pytest.fixture
def update_scopes(monkeypatch: pytest.MonkeyPatch) -> list:
    """Record the parishes the update-mode stage is asked to process."""
    scopes: list = []

    def process_update_mode(conn, *, slugs=None, **kwargs):
        scopes.append(None if slugs is None else sorted(slugs))
        return {}

    monkeypatch.setattr("pdf_extract.process.process_update_mode", process_update_mode)
    return scopes


# ── Seeding ─────────────────────────────────────────────────────────────────
def test_the_flag_is_seeded_from_parishes_csv(work: Path) -> None:
    conn = connect_db()
    try:
        assert fetch_only_slugs(conn) == {"new-parish"}
    finally:
        conn.close()

    _write_parishes(work, held=False)
    ensure_db(load_seeds=False)
    conn = connect_db()
    try:
        assert fetch_only_slugs(conn) == set()
    finally:
        conn.close()


def test_a_csv_without_the_column_has_no_fetch_only_parishes(work: Path) -> None:
    write_csv(work / "data" / "parishes.csv", PARISH_FIELDS, [
        {"slug": "live-parish", "name": "Live Parish", "website": "https://live.org"},
        {"slug": "new-parish", "name": "New Parish", "website": "https://new.org"},
    ])
    ensure_db(load_seeds=False)
    conn = connect_db()
    try:
        assert fetch_only_slugs(conn) == set()
    finally:
        conn.close()


# ── Process ─────────────────────────────────────────────────────────────────
def test_process_makes_no_model_call_for_a_fetch_only_parish(
    work: Path, extractor: list[bytes], update_scopes: list,
) -> None:
    _add_bulletin("live-parish")
    _add_bulletin("new-parish")

    result = process_bulletins()

    assert len(extractor) == 1
    assert _processed() == {"live-parish"}
    assert result["fetch_only_parishes"] == 1
    assert update_scopes == [["live-parish"]]


def test_process_leaves_a_named_fetch_only_parish_alone(
    work: Path, extractor: list[bytes], update_scopes: list,
) -> None:
    _add_bulletin("new-parish")

    assert process_bulletins(parish_name="New Parish")["processed_bulletins"] == 0
    assert process_bulletins(slugs=["new-parish"])["processed_bulletins"] == 0
    assert extractor == []
    assert update_scopes == [[], []]


def test_process_can_include_fetch_only_parishes(
    work: Path, extractor: list[bytes], update_scopes: list,
) -> None:
    _add_bulletin("new-parish")

    result = process_bulletins(parish_name="New Parish", include_fetch_only=True)

    assert result["processed_bulletins"] == 1
    assert result["fetch_only_parishes"] == 0
    assert update_scopes == [["new-parish"]]


def test_clearing_the_flag_processes_the_latest_bulletin(
    work: Path, extractor: list[bytes], update_scopes: list,
) -> None:
    _add_bulletin("new-parish")
    process_bulletins()
    assert _processed() == set()

    _write_parishes(work, held=False)
    ensure_db(load_seeds=False)
    result = process_bulletins()

    assert result["processed_bulletins"] == 1
    assert _processed() == {"new-parish"}
    assert update_scopes[-1] is None


# ── Snapshot ────────────────────────────────────────────────────────────────
def test_the_snapshot_leaves_out_fetch_only_churches_and_events(
    work: Path, tmp_path: Path,
) -> None:
    _add_bulletin("live-parish", events=[_mass("live-parish-church")])
    _add_bulletin("new-parish", events=[_mass("new-parish-church")])
    dest = tmp_path / "frontend.json.gz"

    result = extract(DEFAULT_DB_PATH, dest)

    tables = read_snapshot(dest.read_bytes())
    assert [c["slug"] for c in tables["churches"]] == ["live-parish-church"]
    assert {e["church_id"] for e in tables["events"]} == {tables["churches"][0]["id"]}
    assert (result["churches"], result["events"]) == (1, 1)


# ── Report ──────────────────────────────────────────────────────────────────
def test_the_report_keeps_fetch_only_results_apart(work: Path) -> None:
    before = work / "before.db"
    shutil.copyfile(DEFAULT_DB_PATH, before)
    conn = connect_db()
    try:
        start_run(conn, "r", git_sha=None, trigger=None)
        record_parish_result(conn, "r", "live-parish", "fetch", "unchanged")
        record_parish_result(conn, "r", "new-parish", "fetch", "resolve_failed",
                             detail="no bulletin link")
    finally:
        conn.close()

    report = build_report(
        run_id="r", before_db=before, after_db=DEFAULT_DB_PATH, stages={},
        snapshot_verification=None,
    )

    assert report["status"] == "passed"
    assert report["attention"]["failures"] == []
    [fetch_gate] = [g for g in report["gates"] if "failed to fetch" in g["name"]]
    assert fetch_gate["detail"] == "0 of 1"
    section = report["fetch_only"]
    assert (section["parishes"], section["attempted"]) == (1, 1)
    assert section["fetch"] == {"resolve_failed": 1}
    assert [f["parish_slug"] for f in section["failures"]] == ["new-parish"]
    assert list(section["stale_parishes"]) == ["new-parish"]
    markdown = render_markdown(report)
    assert "### Fetch-only parishes" in markdown
    assert "**new-parish** fetch resolve_failed: no bulletin link" in markdown


def test_the_fetch_only_notes_are_capped() -> None:
    from pdf_extract.report import _render_fetch_only

    section = {
        "parishes": 5, "attempted": 5, "fetch": {"resolve_failed": 5},
        "failures": [
            {"parish_slug": f"p{i}", "stage": "fetch", "status": "resolve_failed",
             "consecutive_failures": 1}
            for i in range(5)
        ],
    }
    lines = _render_fetch_only(section, max_notes=2)
    assert [line for line in lines if line.startswith("- ")] == [
        "- **p0** fetch resolve_failed", "- **p1** fetch resolve_failed",
        "- … and 3 more (all in report.json)",
    ]


def test_the_report_has_no_fetch_only_section_without_such_parishes(work: Path) -> None:
    _write_parishes(work, held=False)
    ensure_db(load_seeds=False)
    before = work / "before.db"
    shutil.copyfile(DEFAULT_DB_PATH, before)

    report = build_report(
        run_id="r", before_db=before, after_db=DEFAULT_DB_PATH, stages={},
        snapshot_verification=None,
    )

    assert report["fetch_only"]["parishes"] == 0
    assert "Fetch-only" not in render_markdown(report)


# ── CSV writers ─────────────────────────────────────────────────────────────
def test_applying_detect_results_keeps_the_column(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    parishes = tmp_path / "parishes.csv"
    write_csv(parishes, FIELDS, [
        {"slug": "a", "name": "A", "website": "https://a.org", "fetch_only": "true"},
        {"slug": "b", "name": "B", "website": "https://b.org"},
    ])
    detect = tmp_path / "detect_results.json"
    detect.write_text(json.dumps({"b": {"bulletin_provider": "ecatholic"}}), encoding="utf-8")
    monkeypatch.setattr("pdf_extract.apply.PARISHES_CSV_PATH", parishes)
    monkeypatch.setattr("pdf_extract.apply.DETECT_RESULTS_PATH", detect)

    apply_detect_results()

    with open(parishes, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [(r["slug"], r["bulletin_provider"], r["fetch_only"]) for r in rows] == [
        ("a", "", "true"), ("b", "ecatholic", ""),
    ]
