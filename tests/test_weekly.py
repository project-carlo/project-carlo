import gzip
import json
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import __main__ as cli
from pdf_extract import weekly
from pdf_extract.datasync import run_out_dir
from pdf_extract.db import DatabaseMissingError, create_db
from pdf_extract.runs import record_parish_result
from pdf_extract.storage import (
    DEFAULT_DB_PATH,
    connect_db,
    insert_bulletin,
    save_processed_bulletin,
    utc_now_iso,
)
from pdf_extract.weekly import run_weekly

EVENTS = [
    {
        "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": start, "end_time": None,
        "cancelled": False,
    }
    for start in ("8:00 AM", "10:00 AM", "12:00 PM")
]
NEW_URL = "https://example.org/2026-09-20.pdf"


def _parish_id(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT id FROM parish WHERE slug = 'test-parish'").fetchone()["id"]


@pytest.fixture
def published_db(pipeline_dir: Path) -> Path:
    """The database as last week's run left it: one processed bulletin with EVENTS."""
    create_db()
    conn = connect_db()
    try:
        bulletin_id = insert_bulletin(
            conn, parish_id=_parish_id(conn), source_url="https://example.org/2026-09-13.pdf",
            content_hash="old", fetched_at=utc_now_iso(),
        )
        save_processed_bulletin(
            conn, bulletin_id, EVENTS, processed_at=utc_now_iso(), published_date="2026-09-13",
        )
    finally:
        conn.close()
    return DEFAULT_DB_PATH


def _install_stages(
    monkeypatch: pytest.MonkeyPatch, events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Fake fetch/process: a new bulletin for test-parish, extracted to `events`."""
    calls: list[dict[str, Any]] = []

    def fake_fetch(**kwargs: Any) -> dict[str, Any]:
        calls.append({"stage": "fetch", **kwargs})
        conn = connect_db()
        try:
            insert_bulletin(
                conn, parish_id=_parish_id(conn), source_url=NEW_URL, content_hash="new",
                fetched_at=utc_now_iso(),
            )
            record_parish_result(
                conn, kwargs["run_id"], "test-parish", "fetch", "new",
                source_url=NEW_URL, content_hash="new",
            )
        finally:
            conn.close()
        return {"new": 1, "unchanged": 0}

    def fake_process(**kwargs: Any) -> dict[str, Any]:
        calls.append({"stage": "process", **kwargs})
        conn = connect_db()
        try:
            bulletin_id = conn.execute(
                "SELECT id FROM bulletin WHERE source_url = ?", (NEW_URL,)
            ).fetchone()["id"]
            stored, _ = save_processed_bulletin(
                conn, bulletin_id, events, processed_at=utc_now_iso(),
                published_date="2026-09-20",
            )
            record_parish_result(
                conn, kwargs["run_id"], "test-parish", "process", "extracted",
                event_count=stored,
            )
        finally:
            conn.close()
        return {"extracted": 1, "events": len(events)}

    monkeypatch.setattr(weekly, "fetch_bulletins", fake_fetch)
    monkeypatch.setattr(weekly, "process_bulletins", fake_process)
    return calls


def _pipeline_run(run_id: str) -> dict[str, Any]:
    conn = connect_db()
    try:
        return dict(conn.execute("SELECT * FROM pipeline_run WHERE id = ?", (run_id,)).fetchone())
    finally:
        conn.close()


def _snapshot_event_count(path: Path) -> int:
    db = path.with_name("unzipped.db")
    db.write_bytes(gzip.decompress(path.read_bytes()))
    conn = sqlite3.connect(db)
    try:
        return conn.execute("SELECT count(*) FROM event").fetchone()[0]
    finally:
        conn.close()


# ── run_weekly ──────────────────────────────────────────────────────────────
def test_weekly_run_passes_and_writes_outputs(
    published_db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_stages(monkeypatch, EVENTS)

    result = run_weekly(run_id="run-1", model="m", concurrency=2, git_sha="abc", trigger="cron")

    out = run_out_dir("run-1")
    assert result["status"] == "passed"
    assert result["run_id"] == "run-1"
    assert result["report"] == str(out / "report.md")
    assert result["stages"]["fetch"] == {"new": 1, "unchanged": 0}
    assert result["stages"]["process"] == {"extracted": 1, "events": 3}
    assert result["stages"]["snapshot"]["events"] == 3
    assert result["totals"]["parishes_with_new_bulletin"] == 1
    assert calls == [
        {"stage": "fetch", "run_id": "run-1"},
        {"stage": "process", "model": "m", "concurrency": 2, "run_id": "run-1"},
    ]

    for name in ("report.md", "report.json", "frontend.snapshot", "before.db"):
        assert (out / name).is_file(), name
    report = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert all(gate["passed"] for gate in report["gates"])
    assert "`run-1`: passed" in (out / "report.md").read_text(encoding="utf-8")
    assert _snapshot_event_count(out / "frontend.snapshot") == 3

    # before.db is the database as the run found it: no new bulletin, no run row.
    before = sqlite3.connect(out / "before.db")
    try:
        assert before.execute("SELECT count(*) FROM bulletin").fetchone()[0] == 1
        assert before.execute("SELECT count(*) FROM pipeline_run").fetchone()[0] == 0
    finally:
        before.close()

    row = _pipeline_run("run-1")
    assert row["status"] == "passed"
    assert row["finished_at"] is not None
    assert (row["git_sha"], row["trigger"]) == ("abc", "cron")
    assert json.loads(row["summary_json"])["fetch"] == {"new": 1, "unchanged": 0}


def test_weekly_run_is_held_when_parish_loses_its_events(
    published_db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_stages(monkeypatch, [])

    result = run_weekly(run_id="run-1")

    assert result["status"] == "held"
    report = json.loads((run_out_dir("run-1") / "report.json").read_text(encoding="utf-8"))
    assert report["status"] == "held"
    assert report["attention"]["dropped_to_zero"] == ["test-parish"]
    failed_gates = {g["name"] for g in report["gates"] if not g["passed"]}
    assert "No parish dropped to zero events" in failed_gates
    assert "Total events within ±10.0%" in failed_gates
    assert "held" in (run_out_dir("run-1") / "report.md").read_text(encoding="utf-8")
    assert _pipeline_run("run-1")["status"] == "held"


def test_weekly_run_is_held_when_weekly_schedule_changes(
    published_db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    changed = [*EVENTS[:2], {**EVENTS[2], "start_time": "5:00 PM"}]
    _install_stages(monkeypatch, changed)

    result = run_weekly(run_id="run-1")

    assert result["status"] == "held"
    report = json.loads((run_out_dir("run-1") / "report.json").read_text(encoding="utf-8"))
    assert [g["name"] for g in report["gates"] if not g["passed"]] == [
        "Weekly schedule at least 90.0% unchanged",
    ]
    assert report["totals"]["events_added"] == report["totals"]["events_removed"] == 1


@pytest.mark.parametrize("failing_stage", ["fetch_bulletins", "process_bulletins"])
def test_weekly_run_failure_is_recorded_and_reraised(
    published_db: Path, monkeypatch: pytest.MonkeyPatch, failing_stage: str,
) -> None:
    _install_stages(monkeypatch, EVENTS)

    def boom(**kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("stage crashed")

    monkeypatch.setattr(weekly, failing_stage, boom)

    with pytest.raises(RuntimeError, match="stage crashed"):
        run_weekly(run_id="run-1")

    out = run_out_dir("run-1")
    report = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert report["gates"] == [
        {"name": "Pipeline completed", "passed": False, "detail": "a stage crashed"},
    ]
    assert "`run-1`: failed" in (out / "report.md").read_text(encoding="utf-8")
    assert (out / "before.db").is_file()
    assert not (out / "frontend.snapshot").exists()
    row = _pipeline_run("run-1")
    assert row["status"] == "failed"
    assert row["finished_at"] is not None
    summary = json.loads(row["summary_json"])
    assert ("fetch" in summary) == (failing_stage == "process_bulletins")


def test_weekly_run_requires_existing_database(
    pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_stages(monkeypatch, EVENTS)

    with pytest.raises(DatabaseMissingError):
        run_weekly(run_id="run-1")

    assert calls == []
    assert not DEFAULT_DB_PATH.exists()


# ── CLI exit codes ──────────────────────────────────────────────────────────
@pytest.mark.parametrize(
    ("status", "exit_code"),
    [("passed", 0), ("held", 10), ("failed", 1), (None, 1)],
)
def test_cli_weekly_exit_code_follows_status(
    pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch, status: str | None, exit_code: int,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_run_weekly(**kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        return {"status": status}

    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "run_weekly", fake_run_weekly)

    assert cli.main(["weekly", "--run-id", "x"]) == exit_code
    assert calls[0]["run_id"] == "x"


def test_cli_weekly_exit_code_when_run_raises(
    pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run_weekly(**kwargs: Any) -> dict[str, Any]:
        raise RuntimeError("boom")

    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "run_weekly", fake_run_weekly)

    assert cli.main(["weekly", "--run-id", "x"]) == 1


def test_cli_weekly_defaults_run_id_and_passes_options(
    pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_run_weekly(**kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        return {"status": "passed"}

    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "run_weekly", fake_run_weekly)

    assert cli.main([
        "weekly", "--concurrency", "3", "--git-sha", "abc", "--trigger", "schedule",
    ]) == 0

    [kwargs] = calls
    assert kwargs["run_id"].startswith("local-")
    assert ":" not in kwargs["run_id"]
    assert (kwargs["concurrency"], kwargs["git_sha"], kwargs["trigger"]) == (
        3, "abc", "schedule",
    )
