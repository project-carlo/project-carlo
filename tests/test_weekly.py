import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import __main__ as cli
from pdf_extract import weekly
from pdf_extract.datasync import run_out_dir
from pdf_extract.db import DatabaseMissingError, create_db
from pdf_extract.dioceses.records import DioceseError
from pdf_extract.extract_frontend_db import read_snapshot
from pdf_extract.runs import record_parish_result
from pdf_extract.seeding.files import write_seed_file
from pdf_extract.storage import (
    DEFAULT_DB_PATH,
    connect_db,
    insert_bulletin,
    save_processed_bulletin,
    utc_now_iso,
)
from pdf_extract.weekly import RunScopeError, resolve_run_scope, run_weekly

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
    return len(read_snapshot(path.read_bytes())["events"])


# ── run_weekly ──────────────────────────────────────────────────────────────
def test_weekly_run_loads_approved_seeds_after_its_before_copy(
    published_db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_stages(monkeypatch, EVENTS)
    seed = {
        "schema_version": 1, "parish_slug": "test-parish", "status": "approved",
        "as_of": "2026-09-14T00:00:00Z", "drafted_by": "test", "drafted_at": None,
        "reviewer": "R", "approved_at": "2026-09-15T00:00:00Z", "summary": "",
        "blocked_reason": None, "calls": [],
        "bulletins": [{"content_hash": "a" * 64, "fetched_at": "2026-09-14T00:00:00Z",
                       "published_date": None, "read": True}],
        "slots": [{
            "id": "s1", "decision": "include", "status": "settled", "page": 1,
            "entry": {**EVENTS[0], "start_time": "08:00", "weeks_of_month": [],
                      "season": None, "note": None},
            "sources": [{"source": "agent", "said": "Sunday 8 AM"}], "rationale": "Printed.",
            "question": None, "options": None, "answer": None,
        }],
    }
    write_seed_file(seed, Path("data") / "seeds")

    result = run_weekly(run_id="run-seeds", model="m")

    assert [s["parish"] for s in result["seeds"]["loaded"]] == ["test-parish"]
    assert "test-parish** seeded" in (run_out_dir("run-seeds") / "report.md").read_text()
    before = sqlite3.connect(run_out_dir("run-seeds") / "before.db")
    try:
        assert before.execute("SELECT count(*) FROM schedule_revision").fetchone()[0] == 0
    finally:
        before.close()
    conn = connect_db()
    try:
        row = conn.execute("SELECT run_id, actor FROM schedule_revision").fetchone()
        assert (row["run_id"], row["actor"]) == ("run-seeds", "R")
    finally:
        conn.close()


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
        {"stage": "fetch", "run_id": "run-1", "slugs": None},
        {"stage": "process", "model": "m", "concurrency": 2, "run_id": "run-1", "slugs": None},
    ]
    assert result["scope"] is None

    for name in ("report.md", "report.json", "frontend.json.gz", "before.db"):
        assert (out / name).is_file(), name
    report = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert report["status"] == "passed"
    assert all(gate["passed"] for gate in report["gates"])
    assert "`run-1`: passed" in (out / "report.md").read_text(encoding="utf-8")
    assert _snapshot_event_count(out / "frontend.json.gz") == 3

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
    assert not (out / "frontend.json.gz").exists()
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
    assert kwargs["parishes"] is None and kwargs["dioceses"] is None


def test_cli_weekly_forwards_parish_and_diocese_limits(
    pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, Any]] = []

    def fake_run_weekly(**kwargs: Any) -> dict[str, Any]:
        calls.append(kwargs)
        return {"status": "passed"}

    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "run_weekly", fake_run_weekly)

    assert cli.main([
        "weekly", "--parish", "one, two", "--parish", "three", "--diocese", "buffalo",
    ]) == 0

    [kwargs] = calls
    assert kwargs["parishes"] == ["one, two", "three"]
    assert kwargs["dioceses"] == ["buffalo"]


def test_cli_weekly_prints_a_scope_error_without_a_traceback(
    published_db: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)

    assert cli.main(["weekly", "--parish", "no-such-parish"]) == 1

    captured = capsys.readouterr()
    assert "Parish not found: no-such-parish" in captured.err
    assert "Traceback" not in captured.err
    conn = connect_db()
    try:
        assert conn.execute("SELECT count(*) FROM pipeline_run").fetchone()[0] == 0
    finally:
        conn.close()
    assert not Path("data/out").exists()


def _write_diocese(root: Path, slug: str, parishes: list[str]) -> None:
    folder = root / "data" / "dioceses" / slug
    (folder / "parishes").mkdir(parents=True)
    (folder / "diocese.md").write_text(f"---\nname: {slug}\n---\n", encoding="utf-8")
    for parish in parishes:
        (folder / "parishes" / f"{parish}.md").write_text("---\nname: x\n---\n", encoding="utf-8")


def test_resolve_run_scope_matches_slugs_names_and_dioceses(
    pipeline_dir: Path, caplog: pytest.LogCaptureFixture,
) -> None:
    from tests.conftest import PARISH_FIELDS, write_csv

    write_csv(
        pipeline_dir / "data" / "parishes.csv",
        PARISH_FIELDS,
        [
            {"slug": "test-parish", "name": "Test Parish", "website": "https://example.org"},
            {"slug": "mary", "name": "Mary, Mother of Mercy", "website": "https://mary.example"},
        ],
    )
    create_db()
    _write_diocese(pipeline_dir, "example", ["test-parish", "not-live"])
    _write_diocese(pipeline_dir, "empty", ["not-live"])

    conn = connect_db()
    try:
        assert resolve_run_scope(conn) is None
        assert resolve_run_scope(conn, parishes=["  "], dioceses=[","]) is None

        named = resolve_run_scope(conn, parishes=["Mary, Mother of Mercy"])
        assert named is not None
        assert named.parishes == ("mary",)
        assert named.selected == ("mary",)

        listed = resolve_run_scope(conn, parishes=["mary, test-parish", "Test Parish"])
        assert listed is not None
        assert listed.parishes == ("mary", "test-parish")
        assert listed.selected == ("test-parish", "mary")

        with caplog.at_level(logging.WARNING):
            diocese = resolve_run_scope(conn, dioceses=["example, example"])
        assert diocese is not None
        assert diocese.dioceses == ("example",)
        assert diocese.selected == ("test-parish",)
        assert "not-live" in caplog.text

        both = resolve_run_scope(conn, parishes=["mary"], dioceses=["example"])
        assert both is not None
        assert both.selected == ("test-parish", "mary")
        assert both.summary() == "Refreshed 2 parishes: diocese `example`; `mary`."

        with pytest.raises(RunScopeError, match="no-such-parish"):
            resolve_run_scope(conn, parishes=["no-such-parish, mary"])
        with pytest.raises(RunScopeError, match="no parishes"):
            resolve_run_scope(conn, dioceses=["empty"])
        with pytest.raises(DioceseError, match="no diocese"):
            resolve_run_scope(conn, dioceses=["missing"])
    finally:
        conn.close()


def test_weekly_run_refreshes_only_the_named_parishes(
    published_db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_stages(monkeypatch, EVENTS)

    result = run_weekly(run_id="run-1", parishes=["Test Parish"], dioceses=None)

    assert result["status"] == "passed"
    assert result["scope"]["selected"] == ["test-parish"]
    assert result["scope"]["summary"] == "Refreshed 1 parish: `test-parish`."
    assert calls == [
        {"stage": "fetch", "run_id": "run-1", "slugs": ["test-parish"]},
        {
            "stage": "process", "model": "gemini-3-flash-preview", "concurrency": 5,
            "run_id": "run-1", "slugs": ["test-parish"],
        },
    ]
    report_path = run_out_dir("run-1")
    report = json.loads((report_path / "report.json").read_text(encoding="utf-8"))
    assert report["scope"]["parishes"] == ["test-parish"]
    assert report["scope"]["summary"] in (report_path / "report.md").read_text(encoding="utf-8")


def test_weekly_run_refreshes_the_live_parishes_of_a_diocese(
    published_db: Path, pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_stages(monkeypatch, EVENTS)
    _write_diocese(pipeline_dir, "example", ["test-parish", "not-live"])

    result = run_weekly(run_id="run-1", dioceses=["example"])

    assert result["scope"]["dioceses"] == ["example"]
    assert result["scope"]["selected"] == ["test-parish"]
    assert calls[0]["slugs"] == ["test-parish"]
    assert calls[1]["slugs"] == ["test-parish"]


def test_weekly_run_rejects_an_unknown_parish_before_starting(
    published_db: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = _install_stages(monkeypatch, EVENTS)

    with pytest.raises(RunScopeError, match="no-such-parish"):
        run_weekly(run_id="run-1", parishes=["no-such-parish"])

    assert calls == []
    assert not Path("data/out").exists()
