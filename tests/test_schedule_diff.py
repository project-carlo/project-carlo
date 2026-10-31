"""The snapshot comparison (`schedule_diff`) and the gates built on it."""

from __future__ import annotations

import gzip
import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.extract_frontend_db import EVENT_COLUMNS, encode_snapshot, read_snapshot
from pdf_extract.schedule_diff import ComparisonError, canonicalize, compare
from pdf_extract.verify_frontend_snapshot import (
    GATE_POLICY_VERSION,
    check_snapshots,
    seed_is_current,
    verify_frontend_snapshot,
)

# A Monday. The window runs to Sunday 2026-12-13: six of every weekday.
AS_OF = date(2026, 11, 2)
FRIDAYS = ["2026-11-06", "2026-11-13", "2026-11-20", "2026-11-27", "2026-12-04", "2026-12-11"]

CHURCHES = [
    {"id": 1, "parish_id": 10, "slug": "a", "bulletin_url": "https://a/b.pdf",
     "bulletin_week": "2026-11-01"},
    {"id": 2, "parish_id": 20, "slug": "b", "bulletin_url": "https://b/b.pdf",
     "bulletin_week": "2026-11-01"},
]


def _event(id: int, church_id: int = 1, **fields: Any) -> dict[str, Any]:
    row: dict[str, Any] = {column: None for column in EVENT_COLUMNS}
    row.update({
        "id": id, "church_id": church_id, "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "start_time": 540, "cancelled": False,
        "weeks_of_month": [], "exclude_weeks": False,
    })
    row.update(fields)
    return row


def _dated(id: int, day: str, church_id: int = 1, **fields: Any) -> dict[str, Any]:
    return _event(id, church_id, event_kind="specific_date", day_of_week=None, date=day,
                  **fields)


def _cancel(id: int, day: str, cancels: int, church_id: int = 1, **fields: Any) -> dict:
    return _dated(id, day, church_id, cancelled=True, cancels_event_id=cancels, **fields)


def _adoration(id: int, church_id: int = 1, **fields: Any) -> dict[str, Any]:
    return _event(id, church_id, **{
        "event_type": "adoration", "day_of_week": "Friday", "start_time": 1140,
        "end_time": 1200, **fields,
    })


def _tables(events: list[dict[str, Any]], churches: list[dict] = CHURCHES) -> dict:
    return {"churches": [dict(c) for c in churches], "events": events}


def _parish(result: dict[str, Any], parish_id: int) -> dict[str, Any]:
    [parish] = [p for p in result["parishes"] if p["parish_id"] == parish_id]
    return parish


def _gate(result: dict[str, Any], prefix: str) -> dict[str, Any]:
    [gate] = [g for g in result["gates"] if g["name"].startswith(prefix)]
    return gate


def _unchanged(result: dict[str, Any]) -> bool:
    return all(
        not (p["recurring"] or p["dated"] or p["cancellations"])
        and not p["availability"]["lost"] and not p["availability"]["gained"]
        for p in result["parishes"]
    )


# ── The issue's reproductions ───────────────────────────────────────────────
def test_every_friday_to_first_friday_is_a_change_that_loses_dates() -> None:
    before = _tables([_adoration(1)])
    after = _tables([_adoration(1, weeks_of_month=["first"])])

    result = compare(before, after, AS_OF)

    assert result["recurring"] == {
        "before": 1, "after": 1, "matched": 0, "removed": 1, "added": 1,
    }
    [change] = _parish(result, 10)["recurring"]
    assert change["change"] == "modified"
    assert change["summary"] == (
        "Adoration · Fri 7:00 PM–8:00 PM, every Friday → First Friday of the month; "
        "4 of 6 dates in the window removed"
    )
    assert change["before"]["window_dates"] == 6
    assert change["after"]["window_dates"] == 2
    [group] = _parish(result, 10)["availability"]["groups"]
    assert group["lost_dates"] == [f"{day} 7:00 PM" for day in FRIDAYS if day[-2:] > "07"]

    gates = check_snapshots(after, before, AS_OF)
    assert not gates["passed"]
    assert gates["weekly_events"]["match_pct"] == 0.0
    assert not _gate(gates, "Weekly schedule")["passed"]
    assert not _gate(gates, "No severe local loss")["passed"]


def test_an_end_time_change_is_a_change_that_loses_no_date() -> None:
    before = _tables([_adoration(1)])
    after = _tables([_adoration(1, end_time=1185)])

    result = compare(before, after, AS_OF)

    [change] = _parish(result, 10)["recurring"]
    assert change["summary"] == "Adoration · Fri 7:00 PM–8:00 PM, every Friday → 7:00 PM–7:45 PM"
    assert result["availability"]["lost"] == 0

    gates = check_snapshots(after, before, AS_OF)
    assert not gates["passed"]
    weekly = _gate(gates, "Weekly schedule")
    assert (weekly["passed"], weekly["numerator"], weekly["denominator"]) == (False, 0, 1)
    assert weekly["affected"] == [{
        "parish_id": 10, "parish_slug": "parish #10", "recurring_before": 1,
        "recurring_removed": 1,
    }]
    assert _gate(gates, "No severe local loss")["passed"]


# ── What isn't a change ─────────────────────────────────────────────────────
@pytest.mark.parametrize(("before_fields", "after_fields"), [
    ({"weeks_of_month": []},
     {"weeks_of_month": ["first", "second", "third", "fourth", "fifth"]}),
    ({"weeks_of_month": ["fifth"], "exclude_weeks": True},
     {"weeks_of_month": ["first", "second", "third", "fourth"]}),
    ({"season_start_month": 10, "season_end_month": 6},
     {"season_start_month": 10, "season_start_day": 1, "season_end_month": 6,
      "season_end_day": 30}),
    ({"season_start_month": 11, "season_end_month": 2},
     {"season_start_month": 11, "season_start_day": 1, "season_end_month": 2,
      "season_end_day": 29}),
    ({"valid_from": "2026-10-01"}, {"valid_from": None}),
    ({"valid_from": "2026-11-02"}, {}),
], ids=["every-week", "exclusion", "season-days", "season-new-year", "started", "starts-today"])
def test_equivalent_encodings_are_not_changes(
    before_fields: dict[str, Any], after_fields: dict[str, Any],
) -> None:
    result = compare(_tables([_adoration(1, **before_fields)]),
                     _tables([_adoration(1, **after_fields)]), AS_OF)

    assert result["recurring"]["matched"] == 1
    assert _unchanged(result)


@pytest.mark.parametrize(("before_fields", "after_fields"), [
    ({"weeks_of_month": ["last"]}, {"weeks_of_month": ["fifth"]}),
    ({"weeks_of_month": ["last"], "exclude_weeks": True},
     {"weeks_of_month": ["first", "second", "third", "fourth"]}),
    ({}, {"season_start_month": 11, "season_end_month": 2}),
    ({}, {"valid_from": "2026-12-01"}),
    ({}, {"valid_until": "2027-06-30"}),
    ({}, {"cancelled": True}),
    ({}, {"end_time": None}),
], ids=["last-vs-fifth", "except-last-vs-four", "season", "starts-later", "ends", "cancelled",
        "no-end"])
def test_qualifier_changes_are_changes(
    before_fields: dict[str, Any], after_fields: dict[str, Any],
) -> None:
    result = compare(_tables([_adoration(1, **before_fields)]),
                     _tables([_adoration(1, **after_fields)]), AS_OF)

    assert result["recurring"]["matched"] == 0
    assert result["recurring"]["removed"] == result["recurring"]["added"] == 1


def test_ids_order_pages_and_bulletin_links_are_not_changes() -> None:
    before = _tables([
        _event(1, page_number=1), _adoration(2, page_number=2),
        _dated(3, "2026-12-08", start_time=720), _cancel(4, "2026-11-08", 1),
    ])
    churches = [{**c, "bulletin_url": c["bulletin_url"] + "?v=2", "bulletin_week": "2026-11-08"}
                for c in CHURCHES]
    # Update mode negates and regenerates ids; the cancellation follows its row.
    after = _tables([
        _cancel(-9, "2026-11-08", -7), _dated(-8, "2026-12-08", start_time=720),
        _event(-7, page_number=4), _adoration(-6),
    ], churches)

    result = compare(before, after, AS_OF)

    assert result["recurring"] == {
        "before": 2, "after": 2, "matched": 2, "removed": 0, "added": 0,
    }
    assert _unchanged(result)
    assert not check_snapshots(after, before, AS_OF)["errors"]
    assert check_snapshots(after, before, AS_OF)["passed"]


def test_notes_are_annotations_not_changes() -> None:
    before = _tables([_event(1, note="Choir")])
    after = _tables([_event(1, note="Choir.")])

    result = compare(before, after, AS_OF)

    parish = _parish(result, 10)
    assert parish["recurring"] == []
    assert parish["notes"] == [{
        "church_slug": "a", "summary": "Mass · Sun 9:00 AM, every Sunday",
        "before": ["Choir"], "after": ["Choir."],
    }]


def test_duplicates_compare_once_and_are_reported() -> None:
    before = _tables([_event(1)])
    after = _tables([_event(5), _event(6, page_number=3)])

    result = compare(before, after, AS_OF)

    assert result["recurring"]["matched"] == 1
    assert result["recurring"]["added"] == 0
    assert _parish(result, 10)["diagnostics"] == [
        "`a` Mass · Sun 9:00 AM, every Sunday appears 2 times",
    ]


def test_an_ambiguous_change_is_shown_as_removals_and_additions() -> None:
    before = _tables([_event(1, start_time=480), _event(2, start_time=600)])
    after = _tables([_event(1, start_time=450), _event(2, start_time=630)])

    [*changes] = _parish(compare(before, after, AS_OF), 10)["recurring"]

    assert [c["change"] for c in changes] == ["removed", "removed", "added", "added"]


# ── Same comparison date, same answer ───────────────────────────────────────
def test_a_snapshot_saved_yesterday_compares_as_of_today() -> None:
    # Yesterday's build still had yesterday's dated Mass and a slot ending
    # yesterday; read as of today, neither is there to lose.
    yesterday = "2026-11-01"
    before = _tables([
        _event(1), _dated(2, yesterday, start_time=720), _event(3, valid_until=yesterday),
        _event(4, day_of_week="Monday", valid_from="2026-11-02"),
    ])
    after = _tables([_event(1), _event(4, day_of_week="Monday")])

    result = compare(before, after, AS_OF)

    assert result["recurring"]["before"] == 2
    assert _unchanged(result)
    assert check_snapshots(after, before, AS_OF)["passed"]


def test_built_on_two_dates_the_snapshots_compare_equal(pipeline_dir: Path) -> None:
    from pdf_extract.db import create_db
    from pdf_extract.extract_frontend_db import extract
    from pdf_extract.storage import (
        DEFAULT_DB_PATH,
        connect_db,
        insert_bulletin,
        save_processed_bulletin,
        utc_now_iso,
    )

    create_db()
    conn = connect_db()
    try:
        parish_id = conn.execute("SELECT id FROM parish WHERE slug = 'test-parish'").fetchone()[0]
        bulletin_id = insert_bulletin(
            conn, parish_id=parish_id, source_url="https://x/1.pdf", content_hash="1",
            fetched_at=utc_now_iso(),
        )
        save_processed_bulletin(conn, bulletin_id, [
            {"church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
             "day_of_week": "Sunday", "start_time": "9:00 AM", "cancelled": False},
            {"church_slug": "test-church", "event_type": "mass", "event_kind": "specific_date",
             "date": "2026-11-01", "start_time": "7:00 PM", "cancelled": False},
        ], processed_at=utc_now_iso(), published_date="2026-11-01")
    finally:
        conn.close()
    # Built either side of midnight, read on the later date.
    extract(DEFAULT_DB_PATH, pipeline_dir / "before.json.gz", build_date=date(2026, 11, 1))
    extract(DEFAULT_DB_PATH, pipeline_dir / "after.json.gz", build_date=date(2026, 11, 2))

    result = verify_frontend_snapshot(
        pipeline_dir / "after.json.gz", pipeline_dir / "before.json.gz", AS_OF,
    )

    assert _gate(result, "Weekly schedule")["passed"]
    assert result["comparison"]["recurring"]["matched"] == 1
    assert _unchanged(result["comparison"])


def test_a_season_crossing_new_year_is_expanded_by_its_dates() -> None:
    # Fridays from November 15 through February 15, read on December 20.
    slot = _adoration(1, season_start_month=11, season_start_day=15, season_end_month=2,
                      season_end_day=15)
    as_of = date(2026, 12, 20)

    result = compare(_tables([slot]), _tables([slot]), as_of, window_days=70)

    assert _unchanged(result)
    # Dec 25 ... Feb 12: nine Fridays, none after February 15.
    assert result["availability"]["before"] == 8
    later = compare(_tables([slot]), _tables([slot]), date(2027, 2, 16))
    assert later["availability"]["before"] == 0
    assert later["recurring"]["matched"] == 1  # still a slot, just out of season


def test_last_week_follows_the_real_month_length_in_a_leap_year() -> None:
    last_tuesday = _event(1, day_of_week="Tuesday", weeks_of_month=["last"])
    as_of = date(2028, 2, 1)

    canonical = canonicalize(_tables([last_tuesday]), as_of)
    result = compare(_tables([last_tuesday]), _tables([last_tuesday]), as_of, window_days=60)

    assert canonical.items[0].weekday == 1
    assert _unchanged(result)
    # 2028-02-29 is a Tuesday, the last of the month; March's is the 28th.
    assert result["availability"]["before"] == 2
    lost = compare(
        _tables([last_tuesday]),
        _tables([_event(1, day_of_week="Tuesday", weeks_of_month=["fourth"])]),
        as_of, window_days=60,
    )
    [group] = _parish(lost, 10)["availability"]["groups"]
    assert group["lost_dates"] == ["2028-02-29 9:00 AM"]


# ── Cancellations ───────────────────────────────────────────────────────────
def test_one_holiday_cancellation_is_listed_with_the_slot_still_matched() -> None:
    thursday = _event(1, day_of_week="Thursday", start_time=480)
    others = _masses(20, church_id=2)
    before = _tables([thursday, *others])
    after = _tables([thursday, *others, _cancel(2, "2026-11-26", 1, start_time=480)])

    result = compare(before, after, AS_OF)

    parish = _parish(result, 10)
    assert result["recurring"]["matched"] == result["recurring"]["before"] == 21
    assert parish["recurring"] == []
    [cancellation] = parish["cancellations"]
    assert cancellation["change"] == "added"
    assert cancellation["summary"] == (
        "Mass · 2026-11-26 8:00 AM, cancels Mass · Thu 8:00 AM, every Thursday, cancelled"
    )
    assert parish["availability"]["lost"] == 1
    assert check_snapshots(after, before, AS_OF)["passed"]


def test_cancelling_most_upcoming_dates_trips_the_local_hold() -> None:
    before = _tables([_adoration(1), _event(2)])
    after = _tables([_adoration(1), _event(2)] + [
        _cancel(10 + i, day, 1, start_time=1140) for i, day in enumerate(FRIDAYS[:4])
    ])

    result = check_snapshots(after, before, AS_OF)

    assert _gate(result, "Weekly schedule")["passed"]
    gate = _gate(result, "No severe local loss")
    assert not gate["passed"]
    [loss] = gate["affected"]
    assert (loss["level"], loss["church_slug"], loss["event_type"]) == ("church", "a", "adoration")
    assert (loss["lost"], loss["before"]) == (4, 6)


def test_a_cancellation_naming_no_weekly_row_fails_closed() -> None:
    before = _tables([_event(1)])
    after = _tables([_event(1), _cancel(2, "2026-11-08", 99)])

    with pytest.raises(ComparisonError, match="names event 99, which is not a weekly row"):
        compare(before, after, AS_OF)
    result = check_snapshots(after, before, AS_OF)
    assert not result["passed"]
    assert result["errors"][0].startswith("Snapshot comparison failed: `a` cancellation 2")


def test_an_event_at_an_unknown_church_fails_closed() -> None:
    before = _tables([_event(1)])
    after = _tables([_event(1), _event(2, church_id=7)])

    result = check_snapshots(after, before, AS_OF)

    assert not result["passed"]
    assert "names church id 7, which is not in the snapshot's churches" in result["errors"][0]
    assert _gate(result, "Snapshot verification")["passed"] is False


# ── Gates ───────────────────────────────────────────────────────────────────
def _masses(count: int, church_id: int = 1, first_id: int = 100) -> list[dict[str, Any]]:
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    return [
        _event(first_id + i, church_id, day_of_week=days[i % 7], start_time=420 + 30 * (i // 7))
        for i in range(count)
    ]


def test_a_severe_local_loss_holds_while_the_site_barely_changes() -> None:
    # 30 slots, one of them changed (97% retained), two added elsewhere (+6.5%):
    # every site-wide gate passes, yet church b's Adoration lost most dates.
    before = _tables(_masses(30) + [_adoration(1, church_id=2)])
    after = _tables(_masses(30) + [
        _event(300, start_time=1260), _event(301, start_time=1290),
        _adoration(1, church_id=2, weeks_of_month=["first"]),
    ])

    result = check_snapshots(after, before, AS_OF, parish_slugs={10: "pa", 20: "pb"})

    assert _gate(result, "Total events")["passed"]
    assert _gate(result, "Weekly schedule")["passed"]
    assert result["weekly_events"]["match_pct"] == pytest.approx(96.77)
    gate = _gate(result, "No severe local loss")
    assert not gate["passed"]
    assert {(loss["level"], loss["parish_slug"]) for loss in gate["affected"]} == {
        ("parish", "pb"), ("church", "pb"),
    }
    assert gate["detail"] == "pb: 4 of 6 dates; pb `b` adoration: 4 of 6 dates"
    assert gate["threshold"] == {"min_dates": 3, "max_fraction": 0.5}


def test_a_level_left_out_of_the_hold_levels_is_reported_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from pdf_extract import verify_frontend_snapshot as gates

    monkeypatch.setattr(gates, "LOCAL_LOSS_HOLD_LEVELS", ("parish",))
    # Church a's Adoration loses most dates; the parish as a whole keeps most.
    before = _tables([_adoration(1), *_masses(10)])
    after = _tables([_adoration(1, weeks_of_month=["first"]), *_masses(10)])

    result = check_snapshots(after, before, AS_OF)

    assert _gate(result, "No severe local loss")["passed"]
    [loss] = [loss for loss in result["local_losses"] if loss["severe"]]
    assert (loss["level"], loss["holds"]) == ("church", False)


def test_a_small_or_partial_local_loss_is_reported_without_holding() -> None:
    before = _tables([_adoration(1), _event(2), _event(3, start_time=600)])
    # Two of six Fridays: under the minimum. Three of six Sundays at 9: half, not more.
    after = _tables([
        _adoration(1, weeks_of_month=["first"], exclude_weeks=True),
        _event(2, weeks_of_month=["first", "third", "fifth"]), _event(3, start_time=600),
    ])

    result = check_snapshots(after, before, AS_OF)

    assert _gate(result, "No severe local loss")["passed"]
    assert {(loss["event_type"], loss["severe"]) for loss in result["local_losses"]} >= {
        ("adoration", False), ("mass", False),
    }


def test_a_parish_dropping_to_zero_holds_and_a_small_one_does_not() -> None:
    before = _tables(_masses(3) + _masses(2, church_id=2, first_id=200))
    after = _tables([])

    result = check_snapshots(after, before, AS_OF, parish_slugs={10: "pa", 20: "pb"})

    gate = _gate(result, "No parish dropped to zero")
    assert (gate["passed"], gate["detail"]) == (False, "pa")
    assert result["dropped_to_zero"] == ["pa"]


def test_ordinary_expiry_is_not_a_drop_to_zero() -> None:
    before = _tables([_dated(i, f"2026-11-0{i}") for i in (1, 2, 3)] + [_dated(4, "2026-10-31")])
    after = _tables([_dated(2, "2026-11-02"), _dated(3, "2026-11-03")])

    # As of the 4th, nothing the earlier snapshot had is still to come.
    result = check_snapshots(after, before, date(2026, 11, 4))

    assert _gate(result, "No parish dropped to zero")["passed"]


def test_a_zero_baseline_is_not_measured_and_onboarding_is_reported() -> None:
    before = _tables([])
    after = _tables([_event(1), _event(2, church_id=2)])

    result = check_snapshots(after, before, AS_OF)

    weekly = _gate(result, "Weekly schedule")
    assert weekly["passed"]
    assert weekly["detail"] == "not measured: no recurring slots last time (2 now)"
    assert result["weekly_events"]["measured"] is False
    assert result["weekly_events"]["match_pct"] is None
    assert [o["parish_id"] for o in result["onboarding"]] == [10, 20]
    assert _gate(result, "No severe local loss")["passed"]


@pytest.mark.parametrize(("seed_as_of", "holds"), [
    ("2026-11-01T00:00:00Z", False),  # drafted from the current bulletin's week
    ("2026-10-02T00:00:00Z", True),  # older than the current bulletin
])
def test_a_parish_seeded_this_run_holds_only_on_an_out_of_date_seed(
    seed_as_of: str, holds: bool,
) -> None:
    before = _tables([_adoration(1), _event(2)])
    after = _tables([_adoration(1, weeks_of_month=["first"]), _event(2)])

    result = check_snapshots(after, before, AS_OF, seeded_this_run={10: seed_as_of})

    gate = _gate(result, "No severe local loss")
    assert gate["passed"] is not holds
    severe = [loss for loss in result["local_losses"] if loss["severe"]]
    assert severe and all(loss["seeded_this_run"] for loss in severe)
    assert all(loss["holds"] is holds for loss in severe)
    # Never exempt from the site-wide retention check.
    assert not _gate(result, "Weekly schedule")["passed"]


def test_a_parish_seeded_this_run_still_cannot_drop_to_zero() -> None:
    before = _tables(_masses(4))
    after = _tables([])

    result = check_snapshots(after, before, AS_OF,
                             seeded_this_run={10: "2026-11-01T00:00:00Z"})

    assert not _gate(result, "No parish dropped to zero")["passed"]


def test_seed_is_current_compares_bulletin_weeks() -> None:
    assert seed_is_current("2026-10-30T00:00:00Z", "2026-11-01")  # Friday rounds forward
    assert not seed_is_current("2026-10-28T00:00:00Z", "2026-11-01")
    assert seed_is_current("2026-10-28", None)
    assert not seed_is_current(None, "2026-11-01")


def test_gates_carry_their_numbers() -> None:
    before = _tables(_masses(10))
    after = _tables(_masses(10)[:9], CHURCHES[:1])

    result = check_snapshots(after, before, AS_OF)

    assert result["gate_policy_version"] == GATE_POLICY_VERSION
    assert result["as_of"] == "2026-11-02"
    for gate in result["gates"]:
        assert {"threshold", "numerator", "denominator", "affected"} <= set(gate)
    churches = _gate(result, "Church count")
    assert churches["affected"] == [{"church_slug": "b", "change": "removed"}]
    weekly = _gate(result, "Weekly schedule")
    assert (weekly["numerator"], weekly["denominator"], weekly["threshold"]) == (9, 10, 90.0)


def test_verify_reads_snapshot_files_on_the_date_given(tmp_path: Path) -> None:
    def columns(rows: list[dict[str, Any]], names: tuple[str, ...]) -> list[tuple]:
        return [tuple(row.get(name) for name in names) for row in rows]

    from pdf_extract.extract_frontend_db import CHURCH_COLUMNS

    churches = columns(CHURCHES, CHURCH_COLUMNS)
    previous = [_event(1), _dated(2, "2026-11-01", start_time=720)]
    (tmp_path / "previous.json.gz").write_bytes(
        encode_snapshot(churches, columns(previous, EVENT_COLUMNS)))
    (tmp_path / "current.json.gz").write_bytes(
        encode_snapshot(churches, columns(previous[:1], EVENT_COLUMNS)))
    assert len(read_snapshot((tmp_path / "previous.json.gz").read_bytes())["events"]) == 2

    on_the_day = verify_frontend_snapshot(
        tmp_path / "current.json.gz", tmp_path / "previous.json.gz", date(2026, 11, 1))
    after_it = verify_frontend_snapshot(
        tmp_path / "current.json.gz", tmp_path / "previous.json.gz", AS_OF)

    assert on_the_day["comparison"]["parishes"][0]["dated_removed"] == 1
    assert after_it["comparison"]["parishes"][0]["dated_removed"] == 0


def test_verify_fails_closed_on_a_malformed_snapshot(tmp_path: Path) -> None:
    (tmp_path / "previous.json.gz").write_bytes(gzip.compress(json.dumps([]).encode()))
    (tmp_path / "current.json.gz").write_bytes(gzip.compress(b"[]"))

    result = verify_frontend_snapshot(
        tmp_path / "current.json.gz", tmp_path / "previous.json.gz", AS_OF)

    assert not result["passed"]
    assert result["gates"][0]["name"] == "Snapshot verification"
    assert "current.json.gz" in result["errors"][0]
