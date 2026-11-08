"""`replay-gates`: today's snapshot gates over archived runs, from local databases."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import __main__ as cli
from pdf_extract.db import create_db
from pdf_extract.replay_gates import render, replay, run_date
from pdf_extract.storage import connect_db, insert_bulletin, save_processed_bulletin, utc_now_iso

MASS = {
    "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
    "day_of_week": "Sunday", "start_time": "9:00 AM", "cancelled": False,
}
MASSES = [{**MASS, "start_time": f"{hour}:00 AM"} for hour in (7, 8, 9)]
RUNS = ["20260914T060000Z-a", "20260921T060000Z-b", "20260928T060000Z-c"]


def _database(path: Path, events: list[dict[str, Any]], week: str) -> Path:
    create_db(path)
    conn = connect_db(path)
    try:
        parish_id = conn.execute("SELECT id FROM parish WHERE slug = 'test-parish'").fetchone()[0]
        bulletin_id = insert_bulletin(
            conn, parish_id=parish_id, source_url=f"https://example.org/{week}.pdf",
            content_hash=week, fetched_at=utc_now_iso(),
        )
        save_processed_bulletin(
            conn, bulletin_id, events, processed_at=utc_now_iso(), published_date=week,
        )
    finally:
        conn.close()
    return path


@pytest.fixture
def archive(pipeline_dir: Path) -> dict[str, tuple[dict[str, Any], Path]]:
    """Three archived runs: unchanged, then the parish's events gone."""
    store = pipeline_dir / "archive"
    store.mkdir()
    return {
        RUNS[0]: ({"status": "passed"}, _database(store / "a.db", MASSES, "2026-09-13")),
        RUNS[1]: ({"status": "passed"}, _database(store / "b.db", MASSES, "2026-09-20")),
        RUNS[2]: ({"status": "passed"}, _database(store / "c.db", [], "2026-09-27")),
    }


def _fetch(archive: dict[str, tuple[dict[str, Any], Path]]):
    def fetch(run_id: str, directory: Path) -> tuple[dict[str, Any], Path]:
        manifest, source = archive[run_id]
        copy = directory / f"{run_id}.db"
        shutil.copyfile(source, copy)
        return manifest, copy
    return fetch


def test_replay_reports_each_pair_against_its_recorded_status(
    archive: dict[str, tuple[dict[str, Any], Path]],
) -> None:
    result = replay(RUNS, fetch=_fetch(archive))

    first, second = result["pairs"]
    assert (first["before_run"], first["after_run"], first["as_of"]) == (
        RUNS[0], RUNS[1], "2026-09-21",
    )
    assert (first["recorded_status"], first["replayed_status"]) == ("passed", "passed")
    assert first["failed_gates"] == []
    assert first["weekly_match_pct"] == 100.0
    assert (second["recorded_status"], second["replayed_status"]) == ("passed", "held")
    assert second["dropped_to_zero"] == ["test-parish"]
    assert "No parish dropped to zero events" in {g["name"] for g in second["failed_gates"]}
    assert {loss["level"] for loss in second["local_losses"]} == {"parish", "church"}
    assert (result["would_hold"], result["recorded_held"]) == (1, 0)

    text = render(result)
    assert f"{RUNS[1]} → {RUNS[2]} as of 2026-09-28: recorded passed, replayed held  (differs)" \
        in text
    assert "  ✗ No parish dropped to zero events: test-parish" in text
    assert text.endswith("1 of 2 pairs would hold; 0 were recorded held.")


def test_replay_needs_two_runs() -> None:
    with pytest.raises(ValueError, match="at least two runs"):
        replay(RUNS[:1], fetch=lambda run_id, directory: ({}, directory))


def test_a_run_date_comes_from_its_id_or_its_manifest() -> None:
    assert run_date("20261025T061502Z-123", {}) == date(2026, 10, 25)
    assert run_date("local-x", {"created_at": "2026-10-26T01:00:00Z"}) == date(2026, 10, 26)
    with pytest.raises(ValueError, match="Can't tell when run local-x happened"):
        run_date("local-x", {})


def test_cli_replays_the_named_runs(
    archive: dict[str, tuple[dict[str, Any], Path]], monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "replay", lambda run_ids: replay(run_ids, fetch=_fetch(archive)))

    assert cli.main(["replay-gates", "--run", RUNS[0], "--run", RUNS[1]]) == 0

    assert "recorded passed, replayed passed" in capsys.readouterr().out


def test_cli_verifies_snapshots_as_of_the_date_given(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[date | None] = []

    def fake_verify(*, as_of: date | None) -> dict[str, Any]:
        calls.append(as_of)
        return {"passed": False, "comparison": {"parishes": []}}

    monkeypatch.setattr(cli, "_load_dotenv", lambda: None)
    monkeypatch.setattr(cli, "verify_frontend_snapshot", fake_verify)

    assert cli.main(["verify-frontend-snapshot", "--as-of", "2026-10-25"]) == 1
    assert cli.main(["verify-frontend-snapshot"]) == 1

    assert calls == [date(2026, 10, 25), None]
