"""Disjoint variants of a weekly slot survive checks, writes, updates and replay."""

from __future__ import annotations

import json
from datetime import date

import pytest

from pdf_extract.db import _migration_files, create_db, migrate
from pdf_extract.schedule.edits import EditError, edit_entry
from pdf_extract.schedule.entries import parse_entry
from pdf_extract.schedule.policy import (
    APPLIED,
    DUPLICATE,
    REJECTED,
    UNKNOWN_ITEM,
    Proposal,
    decide,
)
from pdf_extract.schedule.store import (
    ADD,
    HUMAN,
    Change,
    append_revision,
    intern_entry,
    live_entries,
    load_entries,
    rebuild_current_schedule,
    render_view,
    write_seed,
)
from pdf_extract.storage import MIGRATIONS_DIR, connect_db

BASE = {
    "church_slug": "test-church", "event_type": "adoration", "event_kind": "weekly",
    "day_of_week": "Friday", "start_time": "11:30 AM",
}
FIRST = {**BASE, "weeks_of_month": ["first"], "end_time": "4:00 PM"}
REMAINING = {
    **BASE, "weeks_of_month": ["second", "third", "fourth", "fifth"], "end_time": "1:00 PM",
}
CHURCHES = {"test-church": 1}


def season(start, end):
    return dict(zip(("start_month", "start_day", "end_month", "end_day"), (*start, *end)))


@pytest.fixture
def conn(pipeline_dir):
    create_db()
    c = connect_db()
    yield c
    c.close()


def seed(conn, *entries):
    with conn:
        write_seed(conn, 1, [parse_entry(e, CHURCHES) for e in entries], as_of="2026-10-01")


@pytest.mark.parametrize("left,right,overlap", [
    (FIRST, REMAINING, False),
    (BASE, FIRST, True),
    (FIRST, {**FIRST, "end_time": "5:00 PM", "note": "Chapel"}, True),
    (FIRST, {**BASE, "weeks_of_month": ["first", "third"]}, True),
    ({**BASE, "weeks_of_month": ["last"]}, {**BASE, "weeks_of_month": ["fourth"]}, True),
    ({**BASE, "weeks_of_month": ["last"]}, {**BASE, "weeks_of_month": ["fifth"]}, True),
    ({**BASE, "weeks_of_month": ["last"], "exclude_weeks": True},
     {**BASE, "weeks_of_month": ["last"]}, False),
    ({**BASE, "weeks_of_month": ["last"], "exclude_weeks": True},
     {**BASE, "weeks_of_month": ["fourth"]}, True),
    ({**BASE, "weeks_of_month": ["last"], "exclude_weeks": True},
     {**BASE, "weeks_of_month": ["fifth"]}, False),
    ({**BASE, "season": season((10, None), (5, None))},
     {**BASE, "season": season((6, None), (9, None))}, False),
    ({**BASE, "season": season((10, 1), (5, 31))},
     {**BASE, "season": season((5, 31), (9, 30))}, True),
    ({**BASE, "season": season((10, 1), (5, 31))},
     {**BASE, "season": season((6, 1), (9, 30))}, False),
    ({**FIRST, "season": season((1, 1), (1, 7))},
     {**FIRST, "season": season((1, 8), (1, 31))}, False),
    ({**BASE, "weeks_of_month": ["fifth"]},
     {**BASE, "season": season((2, 29), (2, 29))}, True),
    ({**BASE, "weeks_of_month": ["fifth"]},
     {**BASE, "season": season((2, 28), (2, 28))}, False),
    ({**BASE, "weeks_of_month": ["last"], "exclude_weeks": True},
     {**BASE, "season": season((2, 22), (2, 22))}, True),  # leap February only
    (FIRST, {**FIRST, "day_of_week": "Saturday"}, False),
    (FIRST, {**FIRST, "start_time": "11:31 AM"}, False),
    (FIRST, {**FIRST, "event_type": "mass"}, False),
])
def test_recurrence_conflicts_are_occurrence_overlap(left, right, overlap):
    a, b = (parse_entry(e, CHURCHES) for e in (left, right))
    assert a.conflicts_with(b) is overlap
    assert b.conflicts_with(a) is overlap


def test_identity_canonicalizes_exclusions_and_keeps_dated_overrides_separate():
    remaining = parse_entry(REMAINING, CHURCHES)
    excluded = parse_entry({**BASE, "weeks_of_month": ["first"], "exclude_weeks": True},
                           CHURCHES)
    assert remaining.identity_key == excluded.identity_key
    assert parse_entry(FIRST, CHURCHES).identity_key != remaining.identity_key
    dated = {**BASE, "event_kind": "specific_date", "day_of_week": None, "date": "2026-10-02"}
    a = parse_entry(dated, CHURCHES)
    b = parse_entry({**dated, "cancelled": True}, CHURCHES)
    assert a.identity_key == a.slot_key == b.identity_key
    assert a.conflicts_with(b)
    assert not a.conflicts_with(parse_entry(FIRST, CHURCHES))


def test_reviewed_st_luke_intervals_are_disjoint_without_changing_the_seed():
    path = MIGRATIONS_DIR.parent / "seeds" / "st-luke-schenectady.json"
    slots = {s["id"]: s for s in json.loads(path.read_text())["slots"]}
    churches = {"st-luke-schenectady": 1}
    remaining, first = (parse_entry(slots[s]["entry"], churches) for s in ("s9", "s11"))
    assert slots["s11"]["answer"]["choice"] == 0
    assert (remaining.start_time, remaining.end_time, first.start_time, first.end_time) == (
        690, 780, 690, 960,
    )
    assert not remaining.conflicts_with(first)


def test_disjoint_entries_survive_storage_views_reseeding_and_replay(conn):
    seed(conn, FIRST, REMAINING)
    before = live_entries(conn, 1)
    assert len(before) == 2
    assert load_entries(conn, before) == before
    text, _ = render_view(conn, 1, date(2026, 10, 2))
    entries = json.loads(text)["churches"][0]["entries"]
    assert {(e["end_time"], tuple(e["weeks_of_month"])) for e in entries} == {
        ("4:00 PM", ("first",)), ("1:00 PM", ("second", "third", "fourth", "fifth")),
    }
    seed(conn, REMAINING, FIRST)
    assert live_entries(conn, 1) == before
    seed(conn, REMAINING, {**FIRST, "end_time": "5:00 PM", "note": "Benediction"})
    assert [r[0] for r in conn.execute("SELECT op FROM schedule_change WHERE revision=3")] == [
        "modify",
    ]
    assert rebuild_current_schedule(conn)["differing_rows"] == 0
    rows = conn.execute("SELECT e.identity_key, s.identity_key FROM current_schedule s "
                        "JOIN schedule_entry e ON e.id=s.entry_id").fetchall()
    assert len({r[0] for r in rows}) == 2
    assert all(r[0] == r[1] for r in rows)


def test_reseeding_qualifiers_remains_a_modify_when_the_pair_is_unambiguous(conn):
    seed(conn, FIRST, REMAINING)
    remaining_id = next(i for i, e in live_entries(conn, 1).items() if e.weeks_of_month != 1)
    seed(conn, REMAINING, {**FIRST, "season": season((10, None), (5, None))})
    changes = conn.execute("SELECT op, before_entry_id FROM schedule_change WHERE revision=2")
    assert [(r[0], r[1] != remaining_id) for r in changes] == [("modify", True)]
    assert remaining_id in live_entries(conn, 1)
    seed(conn, REMAINING, {**FIRST, "weeks_of_month": ["first"],
                           "season": season((11, 1), (4, 30))})
    assert [r[0] for r in conn.execute("SELECT op FROM schedule_change WHERE revision=3")] == [
        "modify",
    ]
    assert rebuild_current_schedule(conn)["differing_rows"] == 0


def test_reseeding_splits_and_merges_removes_old_patterns_before_adding_new_ones(conn):
    seed(conn, BASE)
    seed(conn, FIRST, REMAINING)
    assert [r[0] for r in conn.execute("SELECT op FROM schedule_change WHERE revision=2")] == [
        "delete", "add", "add",
    ]
    seed(conn, BASE)
    assert [r[0] for r in conn.execute("SELECT op FROM schedule_change WHERE revision=3")] == [
        "delete", "delete", "add",
    ]
    assert rebuild_current_schedule(conn)["differing_rows"] == 0


def test_seed_and_revision_writers_reject_overlapping_patterns_atomically(conn):
    seed(conn, FIRST)
    before = live_entries(conn, 1)
    with pytest.raises(ValueError, match="same slot"):
        seed(conn, FIRST, BASE)
    with pytest.raises(ValueError, match="already has an entry"):
        with conn:
            entry_id = intern_entry(conn, parse_entry(BASE, CHURCHES))
            append_revision(conn, 1, source_kind=HUMAN,
                            changes=[Change(ADD, after_entry_id=entry_id)])
    assert live_entries(conn, 1) == before
    assert conn.execute("SELECT MAX(revision) FROM schedule_revision").fetchone()[0] == 1


def test_proposals_check_disjoint_and_overlapping_entries_added_in_the_same_call():
    decisions = decide([
        Proposal(1, "add", {}, entry=FIRST),
        Proposal(2, "add", {}, entry=REMAINING),
        Proposal(3, "add", {}, entry=BASE),
    ], live={}, churches=CHURCHES, today=date(2026, 10, 1), whole_call=None)
    assert [d.decision for d in decisions] == [APPLIED, APPLIED, REJECTED]
    assert decisions[2].reason == DUPLICATE


def test_qualifier_modifies_exclude_the_target_but_check_siblings_and_prior_modifies(conn):
    seed(conn, FIRST, REMAINING)
    ids = {e.weeks_of_month: i for i, e in live_entries(conn, 1).items()}
    first_id, remaining_id = ids[1], ids[30]
    expanded = {**FIRST, "weeks_of_month": ["first", "second"]}
    narrowed = {**REMAINING, "weeks_of_month": ["third", "fourth", "fifth"]}
    decisions = decide([
        Proposal(1, "modify", {}, first_id, expanded),
        Proposal(2, "modify", {}, remaining_id, narrowed),
        Proposal(3, "modify", {}, first_id, expanded),
        Proposal(4, "add", {}, entry=REMAINING),
    ], live=live_entries(conn, 1), churches=CHURCHES, today=date(2026, 10, 1), whole_call=None)
    # The first expansion waits for the narrowing it overlaps and is applied after it, so
    # the repeated expansion finds its target already changed.
    assert [d.decision for d in decisions] == [APPLIED, APPLIED, REJECTED, REJECTED]
    assert [d.order for d in decisions[:2]] == [1, 0]
    assert (decisions[2].reason, decisions[3].reason) == (UNKNOWN_ITEM, DUPLICATE)
    with pytest.raises(EditError, match="duplicate"):
        edit_entry(conn, 1, "modify", target_entry_id=first_id, entry=expanded, actor="test")
    edit_entry(conn, 1, "modify", target_entry_id=remaining_id, entry=narrowed, actor="test")
    edit_entry(conn, 1, "modify", target_entry_id=first_id, entry=expanded, actor="test")
    assert {e.weeks_of_month for e in live_entries(conn, 1).values()} == {3, 28}
    assert rebuild_current_schedule(conn)["differing_rows"] == 0


def test_a_waiting_proposal_needs_every_overlap_removed_and_its_removal_targetable(conn):
    seed(conn, FIRST, REMAINING)
    ids = {e.weeks_of_month: i for i, e in live_entries(conn, 1).items()}
    first_id, remaining_id = ids[1], ids[30]
    live = live_entries(conn, 1)
    kwargs = {"churches": CHURCHES, "today": date(2026, 10, 1), "whole_call": None}

    def outcome(decisions):
        return [(d.decision, d.reason, d.order) for d in decisions]

    # An add duplicating two entries waits until both are deleted.
    assert outcome(decide([
        Proposal(1, "add", {}, entry=BASE),
        Proposal(2, "delete", {}, first_id),
        Proposal(3, "delete", {}, remaining_id),
    ], live=live, **kwargs)) == [
        (APPLIED, "auto", 2), (APPLIED, "auto", 0), (APPLIED, "auto", 1)]
    # Only one of them deleted: the add is still a duplicate.
    assert outcome(decide([
        Proposal(1, "add", {}, entry=BASE),
        Proposal(2, "delete", {}, first_id),
    ], live=live, **kwargs)) == [(REJECTED, DUPLICATE, None), (APPLIED, "auto", 0)]
    # A delete the call may not name removes nothing.
    assert outcome(decide([
        Proposal(1, "modify", {}, first_id, BASE),
        Proposal(2, "delete", {}, remaining_id),
    ], live=live, targetable={first_id}, **kwargs)) == [
        (REJECTED, DUPLICATE, None), (REJECTED, UNKNOWN_ITEM, None)]
    # A whole-call rejection overrides any wait.
    assert outcome(decide([
        Proposal(1, "modify", {}, first_id, BASE),
        Proposal(2, "delete", {}, remaining_id),
    ], live=live, **{**kwargs, "whole_call": "mass_delete"})) == [
        (REJECTED, "mass_delete", None), (REJECTED, "mass_delete", None)]
    # An earlier waiting proposal keeps the slot over a later one, and a swap of
    # overlapping modifies (each waiting on the other) is rejected.
    assert outcome(decide([
        Proposal(1, "add", {}, entry={**BASE, "note": "first"}),
        Proposal(2, "delete", {}, first_id),
        Proposal(3, "add", {}, entry={**BASE, "note": "second"}),
        Proposal(4, "delete", {}, remaining_id),
    ], live=live, **kwargs)) == [
        (APPLIED, "auto", 2), (APPLIED, "auto", 0), (REJECTED, DUPLICATE, None),
        (APPLIED, "auto", 1)]
    expanded = {**FIRST, "weeks_of_month": ["first", "second"]}
    assert outcome(decide([
        Proposal(1, "modify", {}, first_id, expanded),
        Proposal(2, "modify", {}, remaining_id, {**REMAINING, "weeks_of_month": ["first"]}),
    ], live=live, **kwargs)) == [(REJECTED, DUPLICATE, None), (REJECTED, DUPLICATE, None)]


def test_migration_rekeys_history_and_current_without_changing_content_or_references(tmp_path):
    previous = tmp_path / "migrations"
    previous.mkdir()
    for number, path in _migration_files():
        if number < 9:
            (previous / path.name).write_text(path.read_text())
    conn = connect_db(tmp_path / "old.db")
    try:
        migrate(conn, previous)
        with conn:
            conn.execute("INSERT INTO parish(slug,name,homepage_url) VALUES ('p','P','https://p')")
            conn.execute("INSERT INTO church(parish_id,slug,name) VALUES (1,'test-church','C')")
        dated = {**BASE, "event_kind": "specific_date", "day_of_week": None,
                 "date": "2026-10-02"}
        seed(conn, FIRST, dated)
        seed(conn, {**FIRST, "season": season((10, None), (5, 31))}, dated)
        with conn:
            # Recreate the derived keys written by the old application.
            for row in conn.execute("SELECT id FROM schedule_entry").fetchall():
                entry = load_entries(conn, [row[0]])[row[0]]
                conn.execute("UPDATE schedule_entry SET identity_key=? WHERE id=?",
                             (entry.slot_key, row[0]))
            conn.execute("UPDATE current_schedule SET identity_key=(SELECT identity_key "
                         "FROM schedule_entry WHERE id=entry_id)")
        before = load_entries(conn, [r[0] for r in conn.execute("SELECT id FROM schedule_entry")])
        hashes = list(map(tuple, conn.execute("SELECT id,hash FROM schedule_entry")))
        changes = list(map(tuple, conn.execute("SELECT * FROM schedule_change")))
        assert migrate(conn) == len(_migration_files()) - 8
        assert load_entries(conn, before) == before
        assert list(map(tuple, conn.execute("SELECT id,hash FROM schedule_entry"))) == hashes
        assert list(map(tuple, conn.execute("SELECT * FROM schedule_change"))) == changes
        for row in conn.execute("SELECT id,identity_key FROM schedule_entry"):
            assert row[1] == before[row[0]].identity_key
        for row in conn.execute("SELECT entry_id,identity_key FROM current_schedule"):
            assert row[1] == before[row[0]].identity_key
        seed(conn, {**FIRST, "season": season((10, None), (5, 31))}, REMAINING, dated)
        assert len(live_entries(conn, 1)) == 3
        assert rebuild_current_schedule(conn)["differing_rows"] == 0
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
        assert migrate(conn) == 0
    finally:
        conn.close()
