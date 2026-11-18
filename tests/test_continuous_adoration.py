"""Chapels open 24 hours: one `continuous` entry per church (issue #111)."""

from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path

import pytest

from pdf_extract.classifiers.qualified_schedule import QualifiedSchedulePayload, flatten_events
from pdf_extract.db import church_kind
from pdf_extract.extract_frontend_db import extract, read_snapshot
from pdf_extract.model import gemini_rows, private_detail, validate_entry
from pdf_extract.schedule.entries import EntryError, parse_entry
from pdf_extract.schedule.policy import DUPLICATE, Schedule, check_proposal
from pdf_extract.schedule.report import describe_entry
from pdf_extract.schedule.store import live_entries, render_view
from pdf_extract.schedule_diff import compare
from pdf_extract.seeding.slots import build_entries, format_entry, parse_entry_spec
from pdf_extract.storage import DEFAULT_DB_PATH
from tests.test_schedule_state import (
    FakeUpdater,
    _bulletin,
    _parish_id,
    _reply,
    _run,
    _seed,
)
from tests.test_schedule_state import conn as schedule_conn  # noqa: F401

CHURCHES = {"test-church": 1}
CHAPEL = {
    "church_slug": "test-church", "event_type": "adoration", "event_kind": "continuous",
    "access": "code_after_hours", "open_from": "6:00 AM", "open_until": "9:00 PM",
    "note": "Adoration Chapel",
}
SUN_9 = {
    "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
    "day_of_week": "Sunday", "start_time": "9:00 AM",
}


@pytest.fixture
def conn(request):
    return request.getfixturevalue("schedule_conn")


# ── The entry ───────────────────────────────────────────────────────────────
def test_a_chapel_is_one_entry_with_no_day_or_times() -> None:
    entry = parse_entry(CHAPEL, CHURCHES)

    assert (entry.event_kind, entry.day_of_week, entry.date) == ("continuous", None, None)
    assert (entry.start_time, entry.end_time) == (None, None)
    assert (entry.access, entry.open_from, entry.open_until) == ("code_after_hours", 360, 1260)
    assert entry.identity_key == "1|adoration|continuous"
    assert entry.labels_form("test-church") == {
        "church_slug": "test-church", "event_type": "adoration", "event_kind": "continuous",
        "start_time": None, "end_time": None, "note": "Adoration Chapel",
        "access": "code_after_hours", "open_from": "6:00 AM", "open_until": "9:00 PM",
    }
    assert parse_entry(entry.labels_form("test-church"), CHURCHES) == entry
    assert describe_entry(entry) == (
        "Adoration · every day, 24 hours (code_after_hours, unlocked 6:00 AM–9:00 PM; "
        "Adoration Chapel)"
    )


def test_a_weekly_entry_keeps_its_hash() -> None:
    # Entries written before chapels existed hash without the access columns.
    weekly = parse_entry(SUN_9, CHURCHES)
    assert weekly.access is None
    assert weekly.hash == parse_entry({**SUN_9, "access": None}, CHURCHES).hash


@pytest.mark.parametrize("change,message", [
    ({"event_type": "mass"}, "Adoration only"),
    ({"start_time": "9:00 AM"}, "no start_time"),
    ({"day_of_week": "Friday"}, "no day_of_week"),
    ({"access": None}, "access must be one of"),
    ({"access": "code"}, "unlocked hours of a code_after_hours chapel"),
    ({"open_until": None}, "both open_from and open_until"),
    ({"open_until": "6:00 AM"}, "must differ"),
    ({"note": "Call 315-555-1212 for the code"}, "phone number"),
])
def test_a_chapel_entry_is_checked(change: dict, message: str) -> None:
    with pytest.raises(EntryError, match=message):
        parse_entry({**CHAPEL, **change}, CHURCHES)


def test_a_timed_entry_has_no_access() -> None:
    with pytest.raises(EntryError, match="continuous chapel only"):
        parse_entry({**SUN_9, "access": "code"}, CHURCHES)


def test_two_chapels_at_one_church_conflict_unless_their_dates_part() -> None:
    open_now = parse_entry(CHAPEL, CHURCHES)
    other = parse_entry({**CHAPEL, "access": "arrangement", "open_from": None,
                         "open_until": None}, CHURCHES)
    closed = parse_entry({**CHAPEL, "valid_until": "2026-11-30"}, CHURCHES)
    reopened = parse_entry({**CHAPEL, "valid_from": "2027-01-04"}, CHURCHES)

    assert open_now.conflicts_with(other)
    assert not closed.conflicts_with(reopened)
    assert closed.conflicts_with(open_now)
    assert closed.expired_before(date(2026, 12, 1))


@pytest.mark.parametrize("note,private", [
    ("Adoration Chapel", False),
    ("closed during Mass", False),
    ("access code needed 9:00 PM-6:00 AM", False),
    ("code needed after 9 pm", False),
    ("door code 4321", True),
    ("Code: 12#", True),
    ("call (315) 555-1212", True),
    ("email office@example.org", True),
])
def test_notes_never_hold_contacts_or_codes(note: str, private: bool) -> None:
    assert (private_detail(note) is not None) == private


def test_every_reviewed_note_passes_the_privacy_check() -> None:
    seeds = Path(__file__).resolve().parents[1] / "data" / "seeds"
    for path in seeds.glob("*.json"):
        seed = json.loads(path.read_text(encoding="utf-8"))
        for slot in seed.get("slots") or []:
            entry = slot.get("entry") if slot.get("decision") == "include" else None
            note = entry.get("note") if isinstance(entry, dict) else None
            assert not (note and private_detail(note)), f"{path.name} {slot['id']}: {note!r}"


# ── Seeds ───────────────────────────────────────────────────────────────────
def test_the_seed_cli_writes_a_chapel_as_24h() -> None:
    [entry] = build_entries(
        parse_entry_spec("adoration 24h open=06:00-21:00 note=Adoration Chapel"), ["st-x"],
    )

    assert entry["event_kind"] == "continuous"
    assert (entry["access"], entry["open_from"], entry["open_until"]) == (
        "code_after_hours", "06:00", "21:00",
    )
    assert validate_entry(entry, "entry") == []
    assert format_entry(entry) == (
        "adoration 24h @st-x access=code-after-hours open=06:00-21:00 note=Adoration Chapel"
    )
    [arranged] = build_entries(parse_entry_spec("adoration 24h access=arrangement"), ["st-x"])
    assert (arranged["access"], arranged["open_from"]) == ("arrangement", None)


def test_the_seed_cli_refuses_a_chapel_with_a_time() -> None:
    from pdf_extract.seeding.queries import SeedError
    with pytest.raises(SeedError, match="no day or time"):
        build_entries(parse_entry_spec("adoration 24h 09:00"), ["st-x"])


def test_a_seed_entry_for_a_chapel_validates_like_one() -> None:
    entry = {
        "church_slug": "st-x", "event_type": "adoration", "event_kind": "continuous",
        "day_of_week": None, "date": None, "start_time": None, "end_time": None,
        "cancelled": False, "weeks_of_month": [], "exclude_weeks": False, "season": None,
        "note": None, "access": "not_stated", "open_from": None, "open_until": None,
    }
    assert validate_entry(entry, "e") == []
    assert validate_entry({**entry, "start_time": "00:00"}, "e") == [
        "e.start_time must be null for a continuous entry",
    ]
    weekly = {**entry, "event_kind": "weekly", "event_type": "mass", "day_of_week": "Sunday",
              "start_time": "09:00"}
    assert validate_entry(weekly, "e") == ["e.access is for a continuous chapel only"]


# ── Extraction ──────────────────────────────────────────────────────────────
def test_the_extraction_schema_returns_a_chapel_as_one_event() -> None:
    payload = QualifiedSchedulePayload.model_validate({"continuous_adoration": [{
        "church_slug": "test-church", "access": "code", "note": "Adoration Chapel",
        "page_number": 2,
    }]})
    [event] = flatten_events(payload)["events"]

    assert event["kind"] == "continuous" and event["type"] == "adoration"
    assert (event["start_time"], event["access"], event["page_number"]) == (None, "code", 2)
    [row] = gemini_rows([event])
    assert row["event_kind"] == "continuous" and row["problems"] == []


# ── The believed schedule, the view and the snapshot ────────────────────────
def test_a_chapel_is_shown_to_the_model_first_and_published_apart(
    conn: sqlite3.Connection, tmp_path: Path,
) -> None:
    _seed(conn, [SUN_9, {**SUN_9, "event_type": "adoration", "day_of_week": "Friday",
                         "start_time": "7:00 PM", "end_time": "8:00 PM"}, CHAPEL])
    parish_id = _parish_id(conn)

    view, _ = render_view(conn, parish_id, date(2026, 11, 17))
    [church] = [c for c in json.loads(view)["churches"] if c["slug"] == "test-church"]
    assert [e["event_kind"] for e in church["entries"]] == ["continuous", "weekly", "weekly"]

    dest = tmp_path / "frontend.json.gz"
    extract(DEFAULT_DB_PATH, dest, build_date=date(2026, 11, 17))
    events = read_snapshot(dest.read_bytes())["events"]
    [chapel] = [e for e in events if e["event_kind"] == "continuous"]
    assert chapel["start_time"] is None and chapel["day_of_week"] is None
    assert (chapel["access"], chapel["open_from"], chapel["open_until"]) == (
        "code_after_hours", 360, 1260,
    )
    # The scheduled Holy Hour keeps its own weekly row beside the chapel.
    assert any(e["event_type"] == "adoration" and e["event_kind"] == "weekly" for e in events)


def test_the_snapshot_leaves_out_a_note_that_holds_a_code(
    conn: sqlite3.Connection, tmp_path: Path,
) -> None:
    _seed(conn, [SUN_9])
    # Written straight to the table, past every check that would refuse it.
    with conn:
        conn.execute("UPDATE schedule_entry SET note = 'door code 4321'")
    dest = tmp_path / "frontend.json.gz"
    extract(DEFAULT_DB_PATH, dest, build_date=date(2026, 11, 17))
    assert [e["note"] for e in read_snapshot(dest.read_bytes())["events"]] == [None]


def test_the_database_refuses_a_chapel_with_a_time(conn: sqlite3.Connection) -> None:
    _seed(conn, [CHAPEL])
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE schedule_entry SET start_time = 0")
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("UPDATE schedule_entry SET event_type = 'mass'")


def test_a_church_kind_is_a_church_unless_it_says_chapel() -> None:
    assert church_kind("") == "church"
    assert church_kind("adoration_chapel") == "adoration_chapel"
    with pytest.raises(ValueError):
        church_kind("shrine")


def test_seven_whole_day_rows_becoming_one_chapel_moves_no_availability() -> None:
    church = {"id": 1, "parish_id": 1, "slug": "c", "bulletin_url": None, "bulletin_week": None}
    blank = {"date": None, "end_time": 1439, "cancelled": False, "weeks_of_month": [],
             "exclude_weeks": False, "season_start_month": None, "season_start_day": None,
             "season_end_month": None, "season_end_day": None, "cancels_event_id": None,
             "valid_from": None, "valid_until": None, "note": None}
    days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    before = [{**blank, "id": -i, "church_id": 1, "event_type": "adoration",
               "event_kind": "weekly", "day_of_week": day, "start_time": 0}
              for i, day in enumerate(days, start=1)]
    after = [{**blank, "id": -8, "church_id": 1, "event_type": "adoration",
              "event_kind": "continuous", "day_of_week": None, "start_time": None,
              "end_time": None, "access": "not_stated", "open_from": None, "open_until": None}]

    result = compare({"churches": [church], "events": before},
                     {"churches": [church], "events": after}, date(2026, 11, 17))

    availability = result["availability"]
    assert availability["lost"] == availability["moved"] == availability["gained"] == 42
    [parish] = result["parishes"]
    assert parish["recurring_removed"] == 7 and parish["recurring_added"] == 1


# ── Update mode ─────────────────────────────────────────────────────────────
def test_the_model_can_add_a_chapel_but_not_a_second_one(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-11-15T00:00:00Z")
    add = {"op": "add", "entry": {**CHAPEL, "start_time": None}, "page_number": 1,
           "rationale": "Page 1: Adoration Chapel open 24/7."}
    _run(conn, FakeUpdater(_reply(changes=[add])))

    live = live_entries(conn, _parish_id(conn))
    [chapel] = [e for e in live.values() if e.continuous]
    assert chapel.access == "code_after_hours"

    entry, reason, _ = check_proposal(
        "add", None, {**CHAPEL, "access": "not_stated", "open_from": None, "open_until": None},
        schedule=Schedule(ids=dict(live)), churches={"test-church": chapel.church_id,
                                                     "second-church": 0},
        today=date(2026, 11, 17),
    )
    assert entry is not None and reason == DUPLICATE


def test_the_model_cannot_put_a_phone_number_in_a_note(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-11-15T00:00:00Z")
    add = {"op": "add", "entry": {**CHAPEL, "note": "Call Joe at 315-555-1212"},
           "page_number": 1, "rationale": "Page 1."}
    _run(conn, FakeUpdater(_reply(changes=[add])))

    reason = conn.execute("SELECT reason FROM proposed_change").fetchone()[0]
    assert reason == "invalid_entry"
    assert not any(e.continuous for e in live_entries(conn, _parish_id(conn)).values())


def test_a_24h_slot_covers_the_whole_days_history_read() -> None:
    from pdf_extract.seeding.coverage import matches
    slot = {"church_slug": "st-x", "event_type": "adoration", "event_kind": "continuous"}
    whole_day = {"church_slug": "st-x", "event_type": "adoration", "event_kind": "weekly",
                 "day_of_week": "Monday", "start_time": "00:00", "end_time": "23:59"}

    assert matches(slot, whole_day)
    assert not matches(slot, {**whole_day, "start_time": "19:00", "end_time": "20:00"})
    assert not matches(slot, {**whole_day, "church_slug": "st-y"})
