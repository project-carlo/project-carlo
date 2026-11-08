"""Parishes without an approved seed: fetched every week, but not processed or shown."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.db import create_db
from pdf_extract.extract_frontend_db import extract, read_snapshot
from pdf_extract.process import process_bulletins
from pdf_extract.report import build_report, render_markdown
from pdf_extract.runs import record_parish_result, start_run
from pdf_extract.schedule.store import unseeded_slugs
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db, insert_bulletin, utc_now_iso
from tests.conftest import CHURCH_FIELDS, PARISH_FIELDS, seed_parish, write_csv


@pytest.fixture
def work(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A database with a seeded parish and one without a seed, one church each."""
    work = tmp_path / "work"
    work.mkdir()
    monkeypatch.chdir(work)
    write_csv(work / "data" / "parishes.csv", PARISH_FIELDS, [
        {"slug": "live-parish", "name": "Live Parish", "website": "https://live.org"},
        {"slug": "new-parish", "name": "New Parish", "website": "https://new.org"},
    ])
    write_csv(work / "data" / "churches.csv", CHURCH_FIELDS, [
        {"parish_id": slug, "slug": f"{slug}-church", "name": "St. Mary", "line1": "1 Main St",
         "city": "Town", "state": "NY", "postal_code": "14000"}
        for slug in ("live-parish", "new-parish")
    ])
    create_db()
    conn = connect_db()
    try:
        seed_parish(conn, "live-parish", [_mass("live-parish-church")])
    finally:
        conn.close()
    return work


def _add_bulletin(slug: str) -> int:
    get_store().put(bulletin_pdf_key(slug, slug), b"fake")
    conn = connect_db()
    try:
        parish_id = conn.execute("SELECT id FROM parish WHERE slug = ?", (slug,)).fetchone()[0]
        return insert_bulletin(
            conn, parish_id=parish_id, source_url=f"https://example.org/{slug}.pdf",
            content_hash=slug, fetched_at=utc_now_iso(),
        )
    finally:
        conn.close()


def _mass(church_slug: str) -> dict:
    return {
        "church_slug": church_slug, "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM", "end_time": None,
        "cancelled": False,
    }


@pytest.fixture
def update_scopes(monkeypatch: pytest.MonkeyPatch) -> list:
    """Record the parishes the update stage is asked to process."""
    scopes: list = []

    def process_update_mode(conn, *, slugs=None, **kwargs):
        scopes.append(None if slugs is None else sorted(slugs))
        return {}

    monkeypatch.setattr("pdf_extract.process.process_update_mode", process_update_mode)
    monkeypatch.setattr("pdf_extract.process.OpenAIScheduleUpdater", lambda: None)
    return scopes


def test_a_parish_is_unseeded_until_its_seed_is_written(work: Path) -> None:
    conn = connect_db()
    try:
        assert unseeded_slugs(conn) == {"new-parish"}
        seed_parish(conn, "new-parish", [_mass("new-parish-church")])
        assert unseeded_slugs(conn) == set()
    finally:
        conn.close()


# ── Process ─────────────────────────────────────────────────────────────────
def test_process_counts_the_unseeded_parishes_it_leaves_alone(
    work: Path, update_scopes: list,
) -> None:
    _add_bulletin("live-parish")
    _add_bulletin("new-parish")

    assert process_bulletins()["unseeded_parishes"] == 1
    assert process_bulletins(parish_name="New Parish")["unseeded_parishes"] == 1
    assert process_bulletins(slugs=["live-parish"])["unseeded_parishes"] == 0
    assert update_scopes == [None, ["new-parish"], ["live-parish"]]


def test_process_rejects_an_unknown_parish(work: Path, update_scopes: list) -> None:
    with pytest.raises(ValueError, match="Parish not found: nowhere"):
        process_bulletins(slugs=["nowhere"])
    assert update_scopes == []


# ── Snapshot ────────────────────────────────────────────────────────────────
def test_the_snapshot_leaves_out_unseeded_churches(work: Path, tmp_path: Path) -> None:
    dest = tmp_path / "frontend.json.gz"

    result = extract(DEFAULT_DB_PATH, dest)

    tables = read_snapshot(dest.read_bytes())
    assert [c["slug"] for c in tables["churches"]] == ["live-parish-church"]
    assert {e["church_id"] for e in tables["events"]} == {tables["churches"][0]["id"]}
    assert (result["churches"], result["events"]) == (1, 1)


# ── Report ──────────────────────────────────────────────────────────────────
def test_the_report_keeps_unseeded_results_apart(work: Path) -> None:
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
    section = report["unseeded"]
    assert (section["parishes"], section["attempted"]) == (1, 1)
    assert section["fetch"] == {"resolve_failed": 1}
    assert [f["parish_slug"] for f in section["failures"]] == ["new-parish"]
    assert list(section["stale_parishes"]) == ["new-parish"]
    markdown = render_markdown(report)
    assert "### Parishes without an approved seed" in markdown
    assert "**new-parish** fetch resolve_failed: no bulletin link" in markdown


def test_the_unseeded_notes_are_capped() -> None:
    from pdf_extract.report import _render_unseeded

    section = {
        "parishes": 5, "attempted": 5, "fetch": {"resolve_failed": 5},
        "failures": [
            {"parish_slug": f"p{i}", "stage": "fetch", "status": "resolve_failed",
             "consecutive_failures": 1}
            for i in range(5)
        ],
    }
    lines = _render_unseeded(section, max_notes=2)
    assert [line for line in lines if line.startswith("- ")] == [
        "- **p0** fetch resolve_failed", "- **p1** fetch resolve_failed",
        "- … and 3 more (all in report.json)",
    ]


def test_the_report_has_no_unseeded_section_when_every_parish_is_seeded(work: Path) -> None:
    conn = connect_db()
    try:
        seed_parish(conn, "new-parish", [_mass("new-parish-church")])
    finally:
        conn.close()
    before = work / "before.db"
    shutil.copyfile(DEFAULT_DB_PATH, before)

    report = build_report(
        run_id="r", before_db=before, after_db=DEFAULT_DB_PATH, stages={},
        snapshot_verification=None,
    )

    assert report["unseeded"]["parishes"] == 0
    assert "without an approved seed" not in render_markdown(report)
