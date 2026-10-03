import shutil
import sqlite3
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import runs
from pdf_extract.db import create_db
from pdf_extract.report import (
    build_report,
    describe_event,
    diff_databases,
    render_markdown,
)
from pdf_extract.runs import record_parish_result, start_run
from pdf_extract.storage import connect_db, insert_bulletin, save_processed_bulletin, utc_now_iso

MASS_9 = {
    "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
    "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM", "end_time": None,
    "cancelled": False,
}
MASS_11 = {**MASS_9, "start_time": "11:00 AM"}
CONFESSION = {
    **MASS_9, "event_type": "confession", "day_of_week": "Saturday",
    "start_time": "3:00 PM", "end_time": "4:00 PM",
}


def _masses(count: int) -> list[dict[str, Any]]:
    return [{**MASS_9, "start_time": f"{hour}:00 AM"} for hour in range(1, count + 1)]


def _add_bulletin(
    db_path: Path,
    rows: list[dict[str, Any]],
    *,
    published_date: str,
    fetched_at: str | None = None,
    processed: bool = True,
) -> int:
    conn = connect_db(db_path)
    try:
        parish_id = conn.execute(
            "SELECT id FROM parish WHERE slug = 'test-parish'"
        ).fetchone()["id"]
        bulletin_id = insert_bulletin(
            conn, parish_id=parish_id,
            source_url=f"https://example.org/{published_date}.pdf",
            content_hash=published_date, fetched_at=fetched_at or utc_now_iso(),
        )
        if processed:
            save_processed_bulletin(
                conn, bulletin_id, rows,
                processed_at=utc_now_iso(), published_date=published_date,
            )
        return bulletin_id
    finally:
        conn.close()


def _before_and_after(
    pipeline_dir: Path, before_rows: list[dict[str, Any]],
) -> tuple[Path, Path]:
    """A database with one processed bulletin, and a copy of it to change."""
    before = pipeline_dir / "before.db"
    after = pipeline_dir / "after.db"
    create_db(before)
    if before_rows is not None:
        _add_bulletin(before, before_rows, published_date="2026-09-13")
    shutil.copyfile(before, after)
    return before, after


def _passing_verification() -> dict[str, Any]:
    return {
        "passed": True,
        "thresholds": {"event_delta_max_pct": 10.0, "weekly_match_min_pct": 90.0},
        "churches": {"current": 1, "previous": 1, "passed": True},
        "events": {"current": 3, "previous": 3, "delta_pct": 0.0, "passed": True},
        "weekly_events": {"match_pct": 100.0, "passed": True},
        "errors": [],
    }


@pytest.fixture
def ticking_clock(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Distinct, increasing pipeline_run.started_at values for consecutive runs."""
    counter = iter(range(10_000))
    monkeypatch.setattr(
        runs, "utc_now_iso", lambda: f"2026-09-{1 + next(counter):02d}T00:00:00Z",
    )
    yield


# ── describe_event ──────────────────────────────────────────────────────────
def test_describe_weekly_event() -> None:
    key = ("c", "mass", "weekly", "Sunday", None, "9:00 AM", None, False)
    assert describe_event(key) == "Mass · Sun 9:00 AM"


def test_describe_dated_event_with_end_time() -> None:
    key = ("c", "confession", "specific_date", None, "2026-10-04", "3:00 PM", "4:00 PM", False)
    assert describe_event(key) == "Confession · 2026-10-04 3:00 PM–4:00 PM"


def test_describe_cancelled_event() -> None:
    key = ("c", "adoration", "specific_date", None, "2026-10-04", "9:00 AM", None, True)
    assert describe_event(key) == "Adoration · 2026-10-04 9:00 AM (cancelled)"


def test_describe_event_with_unknown_type_and_missing_fields() -> None:
    assert describe_event(("c", "vespers", "weekly", "Funday", None, "5:00 PM", None, False)) == (
        "vespers · Funday 5:00 PM"
    )
    assert describe_event(("c", "", "weekly", None, None, "5:00 PM", None, False)) == (
        "Event · ? 5:00 PM"
    )
    assert describe_event(("c", "mass", "specific_date", None, None, "5:00 PM", None, False)) == (
        "Mass · ? 5:00 PM"
    )


# ── diff_databases ──────────────────────────────────────────────────────────
def test_diff_reports_added_and_removed_events(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, CONFESSION])
    _add_bulletin(after, [MASS_9, MASS_11], published_date="2026-09-20")

    [change] = diff_databases(before, after)

    assert change.parish_slug == "test-parish"
    assert change.bulletin_changed
    assert (change.before_count, change.after_count) == (2, 2)
    assert change.added == [
        ("test-church", "mass", "weekly", "Sunday", None, "11:00 AM", None, False),
    ]
    assert change.removed == [
        ("test-church", "confession", "weekly", "Saturday", None, "3:00 PM", "4:00 PM", False),
    ]


def test_diff_of_unchanged_database(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])

    [change] = diff_databases(before, after)

    assert not change.bulletin_changed
    assert change.added == change.removed == []
    assert (change.before_count, change.after_count) == (1, 1)


def test_diff_new_bulletin_with_same_events_is_not_a_schedule_change(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, MASS_11])
    _add_bulletin(after, [MASS_11, MASS_9], published_date="2026-09-20")

    [change] = diff_databases(before, after)

    assert change.bulletin_changed
    assert change.added == change.removed == []


def test_diff_ignores_unprocessed_and_older_bulletins(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    _add_bulletin(after, [], published_date="2026-09-20", processed=False)
    _add_bulletin(after, [MASS_11], published_date="2026-09-06")

    [change] = diff_databases(before, after)

    assert not change.bulletin_changed
    assert change.added == change.removed == []


def test_diff_parish_with_first_bulletin(pipeline_dir: Path) -> None:
    before = pipeline_dir / "before.db"
    create_db(before)
    after = pipeline_dir / "after.db"
    shutil.copyfile(before, after)
    _add_bulletin(after, [MASS_9], published_date="2026-09-20")

    [change] = diff_databases(before, after)

    assert change.bulletin_changed
    assert (change.before_count, change.after_count) == (0, 1)
    assert len(change.added) == 1


# ── build_report ────────────────────────────────────────────────────────────
def test_report_holds_when_parish_drops_to_zero(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, MASS_11, CONFESSION])
    _add_bulletin(after, [], published_date="2026-09-20")

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["status"] == "held"
    assert report["attention"]["dropped_to_zero"] == ["test-parish"]
    assert report["gates"][0] == {
        "name": "No parish dropped to zero events", "passed": False, "detail": "test-parish",
    }
    assert all(gate["passed"] for gate in report["gates"][1:])
    assert report["totals"]["events_before"] == 3
    assert report["totals"]["events_after"] == 0
    assert report["totals"]["events_removed"] == 3
    assert report["totals"]["parishes_showing_events"] == 0


def test_report_passes_small_parish_dropping_to_zero(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, MASS_11])
    _add_bulletin(after, [], published_date="2026-09-20")

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["status"] == "passed"
    assert report["attention"]["dropped_to_zero"] == []


def test_report_passes_and_summarises_changes(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, CONFESSION, MASS_11])
    _add_bulletin(
        after, [MASS_9, MASS_11, {**CONFESSION, "start_time": "2:00 PM"}],
        published_date="2026-09-20",
    )

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={"fetch": {"new": 1}},
        snapshot_verification=_passing_verification(),
    )

    assert report["status"] == "passed"
    assert all(gate["passed"] for gate in report["gates"])
    assert [g["name"] for g in report["gates"]] == [
        "Church count unchanged",
        "Total events within ±10.0%",
        "Weekly schedule at least 90.0% unchanged",
        "No parish dropped to zero events",
        "No parish or church removed from the CSVs",
        "At most 50% of parishes failed to fetch",
    ]
    assert report["gates"][0]["detail"] == "1 → 1"
    assert report["totals"] == {
        "parishes_showing_events": 1,
        "events_before": 3,
        "events_after": 3,
        "events_added": 1,
        "events_removed": 1,
        "parishes_changed": 1,
        "parishes_with_new_bulletin": 1,
    }
    [change] = report["changes"]
    assert [e["summary"] for e in change["added"]] == ["Confession · Sat 2:00 PM–4:00 PM"]
    assert [e["summary"] for e in change["removed"]] == ["Confession · Sat 3:00 PM–4:00 PM"]
    assert change["added"][0]["church_slug"] == "test-church"


def test_report_unchanged_parishes_are_not_listed_as_changes(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["changes"] == []
    assert report["totals"]["parishes_changed"] == 0


@pytest.mark.parametrize("failing", ["churches", "events", "weekly_events"])
def test_report_holds_when_snapshot_verification_fails(pipeline_dir: Path, failing: str) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    verification = _passing_verification()
    verification[failing]["passed"] = False

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={},
        snapshot_verification=verification,
    )

    assert report["status"] == "held"
    assert [g["passed"] for g in report["gates"]].count(False) == 1


def test_report_holds_on_snapshot_verification_errors(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={},
        snapshot_verification={"passed": False, "errors": ["Snapshot not found: x"]},
    )

    assert report["status"] == "held"
    assert {"name": "Snapshot verification", "passed": False,
            "detail": "Snapshot not found: x"} in report["gates"]


def test_report_warns_about_big_drops_without_holding(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, _masses(6))
    _add_bulletin(after, _masses(2), published_date="2026-09-20")

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["status"] == "passed"
    assert report["attention"]["big_drops"] == ["test-parish"]


def test_report_lists_failures_with_consecutive_failure_streak(
    pipeline_dir: Path, ticking_clock: None,
) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    conn = connect_db(after)
    try:
        for run_id, fetch_status in (
            ("run-1", "download_failed"),
            ("run-2", "new"),
            ("run-3", "resolve_failed"),
            ("run-4", "download_failed"),
        ):
            start_run(conn, run_id, git_sha=None, trigger=None)
            record_parish_result(
                conn, run_id, "test-parish", "fetch", fetch_status, detail="HTTP 503",
            )
        record_parish_result(conn, "run-4", "test-parish", "process", "skipped")
        record_parish_result(
            conn, "run-4", "other-parish", "process", "wrong_bulletin",
            source_url="https://example.org/wrong.pdf",
        )
    finally:
        conn.close()

    report = build_report(
        run_id="run-4", before_db=before, after_db=after, stages={},
        snapshot_verification=None,
    )

    failures = {(f["parish_slug"], f["stage"]): f for f in report["attention"]["failures"]}
    assert set(failures) == {("test-parish", "fetch"), ("test-parish", "process")}
    assert failures[("test-parish", "fetch")]["consecutive_failures"] == 2
    assert failures[("test-parish", "fetch")]["status"] == "download_failed"
    assert failures[("test-parish", "fetch")]["detail"] == "HTTP 503"
    assert failures[("test-parish", "process")]["consecutive_failures"] == 1
    assert [r["parish_slug"] for r in report["attention"]["wrong_bulletins"]] == [
        "other-parish",
    ]
    # The only attempted parish failed to fetch: more than half, so the run is held.
    assert report["status"] == "held"
    [fetch_gate] = [g for g in report["gates"] if "failed to fetch" in g["name"]]
    assert fetch_gate == {
        "name": "At most 50% of parishes failed to fetch", "passed": False, "detail": "1 of 1",
    }


def test_report_passes_when_a_minority_of_parishes_fail_to_fetch(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    conn = connect_db(after)
    try:
        start_run(conn, "r", git_sha=None, trigger=None)
        record_parish_result(conn, "r", "test-parish", "fetch", "download_failed")
        for slug in ("a", "b"):
            record_parish_result(conn, "r", slug, "fetch", "unchanged")
    finally:
        conn.close()

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["status"] == "passed"
    assert len(report["attention"]["failures"]) == 1


def test_report_holds_when_the_csvs_removed_a_church(pipeline_dir: Path) -> None:
    """Seeding deletes before the run's "before" copy, so only `seeded` can show it."""
    before, after = _before_and_after(pipeline_dir, [MASS_9])

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={},
        snapshot_verification=None,
        seeded={"parishes_deleted": 0, "churches_deleted": 1},
    )

    assert report["status"] == "held"
    [gate] = [g for g in report["gates"] if "removed from the CSVs" in g["name"]]
    assert gate["passed"] is False
    assert gate["detail"] == "0 parishes, 1 churches deleted with their bulletins and events"


def test_report_flags_stale_parishes_that_were_attempted(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, None)
    _add_bulletin(
        after, [MASS_9], published_date="2026-01-04", fetched_at="2026-01-05T00:00:00Z",
    )
    conn = connect_db(after)
    try:
        start_run(conn, "r", git_sha=None, trigger=None)
        record_parish_result(conn, "r", "test-parish", "fetch", "unchanged")
        record_parish_result(conn, "r", "never-fetched", "fetch", "resolve_failed")
    finally:
        conn.close()

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["attention"]["stale_parishes"] == {
        "never-fetched": None,
        "test-parish": {
            "bulletin_date": "2026-01-04",
            "fetched_at": "2026-01-05T00:00:00Z",
            "last_seen_at": "2026-01-05T00:00:00Z",
            "source_url": "https://example.org/2026-01-04.pdf",
        },
    }
    markdown = render_markdown(report)
    assert "**never-fetched** has no bulletin from the last 14 days (never fetched)" in markdown
    assert (
        "**test-parish** has no bulletin from the last 14 days "
        "(newest is for 2026-01-04, fetched 2026-01-05)"
    ) in markdown


def test_report_calls_a_parish_whose_site_serves_an_old_issue_stale(pipeline_dir: Path) -> None:
    # Fetched this week, but the bulletin is for a week long gone: a site
    # that is alive but no longer updated.
    before, after = _before_and_after(pipeline_dir, None)
    _add_bulletin(after, [MASS_9], published_date="2026-01-04")
    conn = connect_db(after)
    try:
        start_run(conn, "r", git_sha=None, trigger=None)
        record_parish_result(conn, "r", "test-parish", "fetch", "unchanged")
    finally:
        conn.close()

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert report["attention"]["stale_parishes"]["test-parish"]["bulletin_date"] == "2026-01-04"


def test_report_lists_repeated_weeks_and_old_issues(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    conn = connect_db(after)
    try:
        start_run(conn, "r", git_sha=None, trigger=None)
        record_parish_result(
            conn, "r", "test-parish", "process", "repeated_week",
            detail="bulletin 3 for 2026-09-13 (after #1, #2)", source_url="https://x/3.pdf",
        )
        record_parish_result(
            conn, "r", "other-parish", "process", "old_issue",
            detail="for 2026-08-30, older than #4 for 2026-09-13", source_url="https://x/o.pdf",
        )
    finally:
        conn.close()

    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert [r["parish_slug"] for r in report["attention"]["repeated_weeks"]] == ["test-parish"]
    assert [r["parish_slug"] for r in report["attention"]["old_issues"]] == ["other-parish"]
    assert report["attention"]["failures"] == []
    markdown = render_markdown(report)
    assert "**test-parish**: another bulletin for a week we already had two of" in markdown
    assert "**other-parish**: the site served an older issue than the one shown" in markdown


def test_report_opens_databases_read_only(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    before_bytes = before.read_bytes()

    build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    assert before.read_bytes() == before_bytes
    with pytest.raises(sqlite3.OperationalError):
        diff_databases(pipeline_dir / "missing.db", after)


# ── render_markdown ─────────────────────────────────────────────────────────
def test_render_markdown_includes_status_gates_and_changes(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, CONFESSION])
    _add_bulletin(after, [MASS_11, CONFESSION], published_date="2026-09-20")
    report = build_report(
        run_id="run-7", before_db=before, after_db=after,
        stages={"fetch": {"new": 1, "parishes": ["x"]}},
        snapshot_verification=_passing_verification(),
    )

    markdown = render_markdown(report)

    assert "## ✅ Weekly data run `run-7`: passed" in markdown
    assert "| Church count unchanged | ✅ | 1 → 1 |" in markdown
    assert "| No parish dropped to zero events | ✅ | none |" in markdown
    assert "| fetch | new 1 |" in markdown
    assert "<b>test-parish</b>: +1 / −1 (2 → 2 events)" in markdown
    # Entries sort by their text (so "11:00" before "9:00"), not by sign.
    # In clock order, not text order ("11:00" sorts before "9:00" as text).
    assert "- `test-church`\n  - − Mass · Sun 9:00 AM\n  - + Mass · Sun 11:00 AM\n" in markdown
    assert markdown.endswith("\n")


def test_render_markdown_held_report_with_attention_notes(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9, MASS_11, CONFESSION])
    _add_bulletin(after, [], published_date="2026-09-20")
    conn = connect_db(after)
    try:
        start_run(conn, "r", git_sha=None, trigger=None)
        record_parish_result(conn, "r", "test-parish", "process", "failed", detail="boom")
    finally:
        conn.close()
    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    markdown = render_markdown(report)

    assert "## ⏸️ Weekly data run `r`: held" in markdown
    assert "| No parish dropped to zero events | ❌ | test-parish |" in markdown
    assert "- **test-parish** process failed: boom" in markdown
    assert "- **test-parish** now shows no events (holds the run)" in markdown


def test_render_markdown_without_changes(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    report = build_report(
        run_id="r", before_db=before, after_db=after, stages={}, snapshot_verification=None,
    )

    markdown = render_markdown(report)

    assert "No parish's schedule changed." in markdown
    assert "Nothing." in markdown
    assert "### Stages" not in markdown


def test_render_markdown_truncates_long_change_lists() -> None:
    change = {
        "parish_slug": "p", "before_count": 0, "after_count": 0,
        "added": [], "removed": [],
    }
    report = {
        "run_id": "r", "status": "passed", "gates": [], "stages": {},
        "totals": {
            "parishes_showing_events": 0, "events_before": 0, "events_after": 0,
            "events_added": 0, "events_removed": 0, "parishes_changed": 3,
            "parishes_with_new_bulletin": 0,
        },
        "attention": {
            "failures": [], "wrong_bulletins": [], "stale_parishes": {},
            "dropped_to_zero": [], "big_drops": [],
        },
        "changes": [change, change, change],
    }

    markdown = render_markdown(report, max_changed_parishes=2)

    assert markdown.count("<details>") == 2
    assert "…and 1 more parishes; see report.json." in markdown


def test_report_points_out_a_new_bulletin_not_dated_this_week(pipeline_dir: Path) -> None:
    before, after = _before_and_after(pipeline_dir, [MASS_9])
    conn = connect_db(after)
    try:
        start_run(conn, "run-1", git_sha=None, trigger=None)
        record_parish_result(
            conn, "run-1", "test-parish", "fetch", "new",
            detail="page-pdfs on https://p.org/bulletins: first-listed, dated 2026-09-06",
            source_url="https://p.org/2026-09-06.pdf",
        )
        record_parish_result(
            conn, "run-1", "other-parish", "fetch", "new",
            detail="page-pdfs on https://o.org/bulletins: current",
        )
    finally:
        conn.close()

    report = build_report(
        run_id="run-1", before_db=before, after_db=after, stages={},
        snapshot_verification=None,
    )

    assert [r["parish_slug"] for r in report["attention"]["old_picks"]] == ["test-parish"]
    assert "**test-parish**: took a bulletin not dated this week" in render_markdown(report)
