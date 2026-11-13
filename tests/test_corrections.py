"""Corrections: reviewed hand edits committed as files (schedule/corrections.py)."""

from __future__ import annotations

import csv
import json
import sqlite3
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.db import create_db, ensure_db
from pdf_extract.report import render_corrections
from pdf_extract.runs import start_run
from pdf_extract.schedule.corrections import (
    CHANGED_SINCE,
    CORRECTIONS_DIR,
    INVALID_FILE,
    NOT_IN_SCHEDULE,
    UNKNOWN_BULLETIN,
    correction_files,
    load_corrections,
    read_correction,
    schedule_as_of,
)
from pdf_extract.schedule.edits import edit_entry
from pdf_extract.schedule.entries import parse_entry
from pdf_extract.schedule.policy import DUPLICATE, MASS_DELETE, REJECTED
from pdf_extract.schedule.store import live_entries, parish_churches, write_seed
from pdf_extract.schedule.update import process_update_mode
from pdf_extract.storage import (
    CHURCHES_CSV_PATH,
    PARISHES_CSV_PATH,
    connect_db,
    insert_bulletin,
)
from tests.conftest import CHURCH_FIELDS, PARISH_FIELDS, ROOT, write_csv
from tests.test_schedule_state import FakeUpdater, _reply

PARISH = {"slug": "test-parish", "name": "Test Parish", "website": "https://example.org"}
CHURCH = {
    "parish_id": "test-parish", "slug": "test-church", "name": "Test Church",
    "line1": "1 Main St", "city": "Rochester", "state": "NY", "postal_code": "14620",
}
SUN_9 = {
    "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
    "day_of_week": "Sunday", "start_time": "9:00 AM",
}
SUN_11 = {**SUN_9, "start_time": "11:00 AM"}
SAT_5 = {**SUN_9, "day_of_week": "Saturday", "start_time": "5:00 PM"}
TODAY = date(2026, 11, 9)
HASH = "ab" * 32


@pytest.fixture
def conn(pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch):
    write_csv(PARISHES_CSV_PATH, PARISH_FIELDS, [PARISH])
    write_csv(CHURCHES_CSV_PATH, CHURCH_FIELDS, [CHURCH])
    create_db()
    monkeypatch.setattr(
        "pdf_extract.schedule.update.read_bulletin_pdf", lambda slug, content_hash: b"%PDF",
    )
    c = connect_db()
    yield c
    c.close()


def _pid(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT id FROM parish WHERE slug = 'test-parish'").fetchone()[0]


def _seed(conn: sqlite3.Connection, entries: list[dict]) -> None:
    churches = parish_churches(conn, _pid(conn))
    with conn:
        write_seed(conn, _pid(conn), [parse_entry(e, churches) for e in entries],
                   as_of="2026-10-01T00:00:00Z", actor="test")


def _times(conn: sqlite3.Connection) -> list[tuple[str, int]]:
    return sorted((e.day_of_week, e.start_time) for e in live_entries(conn, _pid(conn)).values())


def _revisions(conn: sqlite3.Connection) -> list[tuple]:
    return [tuple(r) for r in conn.execute(
        "SELECT revision, source_kind, actor FROM schedule_revision ORDER BY revision",
    ).fetchall()]


def _write(name: str, operations: list[dict[str, Any]], *, as_of: str, **fields: Any) -> Path:
    path = CORRECTIONS_DIR / "test-parish" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"parish": "test-parish", "actor": "luke", "note": "checked the bulletin",
            "as_of": as_of, "operations": operations, **fields}
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_a_correction_file_loads_once_as_one_human_revision(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SUN_11])
    as_of = schedule_as_of(conn, _pid(conn))
    path = _write("2026-11-09-fix-masses.json", [
        {"op": "modify", "before": SUN_9, "after": {**SUN_9, "note": "Latin"}},
        {"op": "delete", "before": SUN_11},
        {"op": "add", "after": SAT_5},
    ], as_of=as_of)

    result = load_corrections(conn, today=TODAY)

    assert result["skipped"] == []
    [loaded] = result["loaded"]
    assert (loaded["file"], loaded["revision"], loaded["changes"]) == (
        "test-parish/2026-11-09-fix-masses.json", 2, 3)
    assert _revisions(conn) == [(1, "seed", "test"), (2, "human", "luke")]
    assert _times(conn) == [("Saturday", 1020), ("Sunday", 540)]
    ops = [r[0] for r in conn.execute(
        "SELECT op FROM schedule_change WHERE revision = 2 ORDER BY id").fetchall()]
    assert ops == ["modify", "delete", "add"]

    # Loading it again, or after its note is reworded, makes no second revision.
    assert load_corrections(conn, today=TODAY) == {"loaded": [], "skipped": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    path.write_text(json.dumps({**data, "note": "reworded"}), encoding="utf-8")
    assert load_corrections(conn, today=TODAY) == {"loaded": [], "skipped": []}
    assert ensure_db()["corrections"] == {"loaded": [], "skipped": []}
    assert len(_revisions(conn)) == 2


def test_a_stale_correction_is_skipped_and_reported(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SUN_11])
    as_of = schedule_as_of(conn, _pid(conn))
    # The schedule moved on: the 11:00 Mass now has a note, so `before` no longer matches.
    sun11 = next(i for i, e in live_entries(conn, _pid(conn)).items() if e.start_time == 660)
    edit_entry(conn, _pid(conn), "modify", target_entry_id=sun11,
               entry={**SUN_11, "note": "Choir"}, actor="model", today=TODAY)
    _write("2026-11-09-drop-eleven.json", [
        {"op": "add", "after": SAT_5},
        {"op": "delete", "before": SUN_11},
    ], as_of=as_of)

    result = load_corrections(conn, today=TODAY)

    assert result["loaded"] == []
    [skipped] = result["skipped"]
    assert skipped["file"] == "test-parish/2026-11-09-drop-eleven.json"
    assert skipped["reason"].startswith(f"{NOT_IN_SCHEDULE}: operation 2")
    # All or nothing: the add before it was not applied either.
    assert _times(conn) == [("Sunday", 540), ("Sunday", 660)]
    assert len(_revisions(conn)) == 2
    # It is reported again until the file is fixed or removed.
    assert len(load_corrections(conn, today=TODAY)["skipped"]) == 1

    lines = render_corrections(result)
    assert lines[1] == "### Corrections"
    assert "skipped: not_in_schedule" in lines[3]


def test_a_correction_is_skipped_when_a_later_revision_touched_its_slot(
    conn: sqlite3.Connection,
) -> None:
    _seed(conn, [SUN_9, SUN_11])
    as_of = schedule_as_of(conn, _pid(conn))
    pid = _pid(conn)
    sun11 = next(i for i, e in live_entries(conn, pid).items() if e.start_time == 660)
    # Deleted and put back: the content is the same, but someone looked at the slot since.
    edit_entry(conn, pid, "delete", target_entry_id=sun11, actor="model", today=TODAY)
    edit_entry(conn, pid, "add", entry=SUN_11, actor="model", today=TODAY)
    with conn:
        conn.execute("UPDATE schedule_revision SET created_at = '2099-01-01T00:00:00Z' "
                     "WHERE revision > 1")
    _write("2026-11-09-drop-eleven.json", [{"op": "delete", "before": SUN_11}], as_of=as_of)

    [skipped] = load_corrections(conn, today=TODAY)["skipped"]

    assert skipped["reason"].startswith(CHANGED_SINCE)
    # A slot no later revision touched still loads.
    _write("2026-11-09-drop-nine.json", [{"op": "delete", "before": SUN_9}], as_of=as_of)
    assert [r["file"] for r in load_corrections(conn, today=TODAY)["loaded"]] == [
        "test-parish/2026-11-09-drop-nine.json"]


def test_a_bulletin_can_be_marked_wrong_by_a_file(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    bulletin = insert_bulletin(conn, parish_id=_pid(conn), source_url="https://example.org/f.pdf",
                               content_hash=HASH, fetched_at="2026-11-01T12:00:00Z")
    as_of = schedule_as_of(conn, _pid(conn))
    _write("2026-11-09-flyer.json", [{"op": "wrong_bulletin", "content_hash": HASH}],
           as_of=as_of)
    _write("2026-11-09-missing.json", [{"op": "wrong_bulletin", "content_hash": "cd" * 32}],
           as_of=as_of)

    result = load_corrections(conn, today=TODAY)

    assert [(r["file"], r["changes"], r["wrong_bulletins"]) for r in result["loaded"]] == [
        ("test-parish/2026-11-09-flyer.json", 0, 1)]
    assert [r["reason"].split(":")[0] for r in result["skipped"]] == [UNKNOWN_BULLETIN]
    flag = conn.execute("SELECT wrong_bulletin FROM bulletin WHERE id = ?", (bulletin,))
    assert flag.fetchone()[0] == 1
    # Recorded as a revision with no changes, so it loads once.
    assert _revisions(conn)[-1] == (2, "human", "luke")
    assert load_corrections(conn, today=TODAY)["loaded"] == []


def test_a_rejected_call_is_applied_by_run_and_bulletin(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SUN_11, SAT_5])
    ids = list(live_entries(conn, _pid(conn)))
    insert_bulletin(conn, parish_id=_pid(conn), source_url="https://example.org/b.pdf",
                    content_hash=HASH, fetched_at="2026-11-01T12:00:00Z")
    with conn:
        start_run(conn, "run-1", git_sha=None, trigger="test")
    process_update_mode(conn, run_id="run-1", concurrency=1, updater=FakeUpdater(_reply(
        changes=[{"op": "delete", "entry_id": i, "page_number": 1, "rationale": "gone"}
                 for i in ids]
        + [{"op": "add", "entry": {**SUN_9, "start_time": "10:00 AM"}, "page_number": 1,
            "rationale": "new"}],
    )))
    assert {r[0] for r in conn.execute("SELECT reason FROM proposed_change")} == {MASS_DELETE}
    as_of = schedule_as_of(conn, _pid(conn))
    _write("2026-11-09-apply-run-1.json", [
        {"op": "apply", "run_id": "run-1", "content_hash": HASH, "seq": [1, 4]},
    ], as_of=as_of)

    [loaded] = load_corrections(conn, today=TODAY)["loaded"]

    assert loaded["changes"] == 2
    rows = conn.execute("SELECT op, proposed_change_id FROM schedule_change "
                        "WHERE revision = ? ORDER BY id", (loaded["revision"],)).fetchall()
    assert [r[0] for r in rows] == ["delete", "add"] and all(r[1] for r in rows)
    assert {r[0] for r in conn.execute("SELECT decision FROM proposed_change")} == {REJECTED}

    # Applying the add again would duplicate it: skipped.
    _write("2026-11-09-apply-again.json", [
        {"op": "apply", "run_id": "run-1", "content_hash": HASH, "seq": [4]},
    ], as_of=as_of)
    [skipped] = load_corrections(conn, today=TODAY)["skipped"]
    assert skipped["reason"].startswith(DUPLICATE)


def test_a_malformed_file_is_skipped(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _write("2026-11-09-bad.json", [{"op": "rename"}], as_of="2026-11-01")
    _write("not-dated.json", [{"op": "add", "after": SAT_5}], as_of="2026-11-01")
    reasons = [r["reason"] for r in load_corrections(conn, today=TODAY)["skipped"]]
    assert len(reasons) == 2 and all(r.startswith(INVALID_FILE) for r in reasons)


def test_the_schedule_command_writes_and_checks_a_correction(
    conn: sqlite3.Connection, capsys: pytest.CaptureFixture[str],
) -> None:
    from pdf_extract.__main__ import main

    _seed(conn, [SUN_9, SUN_11])
    sun11 = next(i for i, e in live_entries(conn, _pid(conn)).items() if e.start_time == 660)
    assert main(["schedule", "modify", "--parish", "test-parish", "--entry-id", str(sun11),
                 "--entry", json.dumps({**SUN_11, "start_time": "11:30 AM"}),
                 "--actor", "luke", "--write-correction", "late-mass"]) == 1
    assert "needs a --note" in capsys.readouterr().err

    assert main(["schedule", "modify", "--parish", "test-parish", "--entry-id", str(sun11),
                 "--entry", json.dumps({**SUN_11, "start_time": "11:30 AM"}),
                 "--actor", "luke", "--note", "p. 2", "--write-correction", "late-mass"]) == 0
    out = json.loads(capsys.readouterr().out)
    [path] = correction_files()
    assert out["path"] == str(path) and path.name.endswith("-late-mass.json")
    data = read_correction(path)
    assert data["operations"] == [{
        "op": "modify", "before": SUN_11, "after": {**SUN_11, "start_time": "11:30 AM"},
    }]
    # Loaded into the local database already, so nothing is left to load.
    assert _times(conn) == [("Sunday", 540), ("Sunday", 690)]
    assert main(["schedule", "corrections"]) == 0
    assert json.loads(capsys.readouterr().out) == {"loaded": [], "skipped": []}

    # An edit that doesn't apply locally leaves no file behind.
    assert main(["schedule", "add", "--parish", "test-parish", "--entry", json.dumps(SUN_9),
                 "--actor", "luke", "--note", "x", "--write-correction", "again"]) == 1
    assert "duplicate" in capsys.readouterr().err
    assert correction_files() == [path]


def test_committed_corrections_are_well_formed() -> None:
    """Every file in data/corrections/ reads and names a parish and its churches."""
    data_dir = ROOT / "data"
    with (data_dir / "parishes.csv").open(encoding="utf-8") as f:
        parishes = {row["slug"] for row in csv.DictReader(f)}
    with (data_dir / "churches.csv").open(encoding="utf-8") as f:
        churches: dict[str, set[str]] = {}
        for row in csv.DictReader(f):
            churches.setdefault(row["parish_id"], set()).add(row["slug"])
    for path in correction_files(data_dir / "corrections"):
        data = read_correction(path)
        assert data["parish"] in parishes, path
        own = {slug: i for i, slug in enumerate(sorted(churches.get(data["parish"], ())))}
        for op in data["operations"]:
            for key in ("before", "after"):
                if key in op:
                    parse_entry(op[key], own)  # raises for an unknown church or bad entry
