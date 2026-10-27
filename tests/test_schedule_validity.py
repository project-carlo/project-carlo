"""Announced transitions and reviewed repairs survive through storage and export."""

import json
import runpy
import sqlite3
from dataclasses import astuple
from datetime import date
from hashlib import sha256
from pathlib import Path

import pytest

from pdf_extract.db import migrate
from pdf_extract.extract_frontend_db import extract, read_snapshot
from pdf_extract.runs import start_run
from pdf_extract.schedule.edits import edit_entry
from pdf_extract.schedule.entries import ENTRY_COLUMNS, Entry, EntryError, parse_entry
from pdf_extract.schedule.policy import PAST_DATE
from pdf_extract.schedule.store import live_entries, rebuild_current_schedule, render_view
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db
from tests.test_schedule_state import (
    SAT_5,
    SUN_9,
    FakeUpdater,
    _bulletin,
    _ids,
    _reply,
    _run,
    _seed,
)
from tests.test_schedule_state import conn as schedule_conn  # noqa: F401

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / 'data/migrations/0012_oct25_review.py'
FROZEN = json.loads(MIGRATION.with_suffix('.json').read_text())
CHURCHES = {'test-church': 1}


def _labels(columns: dict) -> dict:
    """A frozen 0012 entry as a hand edit gives one."""
    values = {c: columns[c] for c in ENTRY_COLUMNS if c != 'church_id'}
    return Entry(church_id=0, **values).labels_form(columns['church_slug'])


# The reviewed October 25 corrections, in the form the schedule tools take.
SPEC = {'run_id': FROZEN['run_id'], 'parishes': [
    {**case, 'repairs': [
        {**repair, **{side: [_labels(e) for e in repair[side]] for side in ('before', 'after')}}
        for repair in case['repairs']
    ]} for case in FROZEN['parishes']
]}


@pytest.fixture
def conn(request):
    return request.getfixturevalue('schedule_conn')


@pytest.mark.parametrize('replacement', [
    {**SAT_5, 'start_time': '4:00 PM'},
    {**SAT_5, 'note': 'Main church'},
    {**SAT_5, 'day_of_week': 'Monday'},
])
def test_future_transition_needs_no_later_bulletin(conn, tmp_path, replacement):
    _seed(conn, [SAT_5])
    original = _ids(conn)['mass Saturday 1020']
    _bulletin(conn, 'transition', '2026-10-25T10:00:00Z')
    result = _run(conn, FakeUpdater(_reply(published_date='2026-10-25', changes=[
        {'op': 'add', 'entry': {**replacement, 'valid_from': '2026-10-31'}},
        {'op': 'modify', 'entry_id': original,
         'entry': {**SAT_5, 'valid_until': '2026-10-30'}},
    ])))
    assert result['update_changes_applied'] == 2
    before = live_entries(conn, 1)
    assert len(before) == 2
    assert _run(conn, FakeUpdater())['update_calls'] == 0
    assert live_entries(conn, 1) == before
    assert rebuild_current_schedule(conn)['differing_rows'] == 0
    view, _ = render_view(conn, 1, date(2026, 11, 7))
    assert len(json.loads(view)['churches'][1]['entries']) == 1
    dest = tmp_path / 'snapshot.gz'
    extract(DEFAULT_DB_PATH, dest, build_date=date(2026, 10, 25))
    assert len(read_snapshot(dest.read_bytes())['events']) == 2
    extract(DEFAULT_DB_PATH, dest, build_date=date(2026, 11, 7))
    [row] = read_snapshot(dest.read_bytes())['events']
    assert row['valid_from'] == '2026-10-31'
    assert row['valid_until'] is None


@pytest.mark.parametrize('bad', [
    {'valid_from': '2026-02-30'}, {'valid_until': 'tomorrow'},
    {'valid_from': '2026-11-01', 'valid_until': '2026-10-31'},
    {'valid_from': True},
    {'event_kind': 'specific_date', 'day_of_week': None,
     'date': '2026-11-01', 'valid_from': '2026-11-01'},
])
def test_absolute_bounds_are_validated(bad):
    with pytest.raises(EntryError):
        parse_entry({**SUN_9, **bad}, CHURCHES)


def test_bounded_variants_conflict_only_when_dates_overlap():
    old = parse_entry({**SUN_9, 'valid_until': '2026-10-31'}, CHURCHES)
    new = parse_entry({**SUN_9, 'valid_from': '2026-11-01'}, CHURCHES)
    assert not old.conflicts_with(new)
    assert old.conflicts_with(parse_entry({**SUN_9, 'valid_from': '2026-10-31'}, CHURCHES))
    legacy = parse_entry(SUN_9, CHURCHES)
    assert legacy.hash == sha256(json.dumps(astuple(legacy)[:-2]).encode()).hexdigest()


@pytest.mark.parametrize('day', ['2026-10-25', '2026-11-01'])
def test_cancellation_targets_the_version_effective_on_its_date(conn, tmp_path, day):
    _seed(conn, [
        {**SUN_9, 'valid_until': '2026-10-31', 'note': 'Chapel'},
        {**SUN_9, 'valid_from': '2026-11-01'},
        {**SUN_9, 'event_kind': 'specific_date', 'day_of_week': None,
         'date': day, 'cancelled': True},
    ])
    dest = tmp_path / 'snapshot.gz'
    extract(DEFAULT_DB_PATH, dest, build_date=date(2026, 10, 25))
    rows = read_snapshot(dest.read_bytes())['events']
    cancelled = next(e for e in rows if e['cancelled'])
    target = next(e for e in rows if e['id'] == cancelled['cancels_event_id'])
    assert target['note'] == ('Chapel' if day == '2026-10-25' else None)


def test_midnight_and_night_services_apply_without_review(conn):
    _seed(conn, [SUN_9])
    _bulletin(conn, 'christmas', '2026-12-13T10:00:00Z')
    midnight = {**SUN_9, 'event_kind': 'specific_date', 'day_of_week': None,
                'date': '2026-12-25', 'start_time': '12:00 AM'}
    result = _run(conn, FakeUpdater(_reply(published_date='2026-12-13', changes=[
        {'op': 'add', 'entry': midnight},
        {'op': 'add', 'entry': {**SAT_5, 'start_time': '3:00 AM', 'event_type': 'adoration'}},
    ])))
    assert result['update_changes_applied'] == 2
    assert {0, 180} <= {e.start_time for e in live_entries(conn, 1).values()}


def test_ended_entry_is_retired_and_does_not_block_its_slot(conn, tmp_path):
    _seed(conn, [SUN_9, {**SAT_5, 'valid_until': '2026-10-30'}])
    _bulletin(conn, 'spring', '2027-04-03T10:00:00Z')
    result = _run(conn, FakeUpdater(_reply(published_date='2027-04-03', changes=[
        {'op': 'add', 'entry': SAT_5},
    ])))
    assert result['update_changes_applied'] == 1
    assert sorted(e.valid_until or '' for e in live_entries(conn, 1).values()) == ['', '']
    assert rebuild_current_schedule(conn)['differing_rows'] == 0
    # A hand edit retires an ended entry the same way.
    _seed(conn, [SUN_9, {**SAT_5, 'valid_until': '2026-10-30'}])
    edit_entry(conn, 1, 'add', entry=SAT_5, actor='Reviewer', today=date(2027, 4, 3))
    assert all(e.valid_until is None for e in live_entries(conn, 1).values())


def test_add_that_already_ended_is_rejected_but_a_late_transition_applies(conn):
    _seed(conn, [SAT_5])
    original = _ids(conn)['mass Saturday 1020']
    _bulletin(conn, 'late', '2026-11-02T10:00:00Z')
    result = _run(conn, FakeUpdater(_reply(published_date='2026-11-02', changes=[
        {'op': 'add', 'entry': {**SUN_9, 'valid_until': '2026-10-20'}},
        {'op': 'modify', 'entry_id': original, 'entry': {**SAT_5, 'valid_until': '2026-10-31'}},
        {'op': 'add', 'entry': {**SAT_5, 'start_time': '4:00 PM', 'valid_from': '2026-11-01'}},
    ])))
    assert result['update_changes_applied'] == 2
    reasons = [r[0] for r in conn.execute('SELECT reason FROM proposed_change ORDER BY seq')]
    assert reasons == [PAST_DATE, 'auto', 'auto']
    view, _ = render_view(conn, 1, date(2026, 11, 2))
    [entry] = json.loads(view)['churches'][1]['entries']
    assert entry['start_time'] == '4:00 PM'


def test_approved_night_slot_can_transition_and_be_cancelled(conn):
    night = {**SAT_5, 'start_time': '3:00 AM', 'event_type': 'adoration'}
    _seed(conn, [night])
    original = next(iter(live_entries(conn, 1)))
    _bulletin(conn, 'night-change', '2026-10-25T10:00:00Z')
    result = _run(conn, FakeUpdater(_reply(published_date='2026-10-25', changes=[
        {'op': 'modify', 'entry_id': original,
         'entry': {**night, 'valid_until': '2026-10-30'}},
        {'op': 'add', 'entry': {**night, 'valid_from': '2026-10-31', 'note': 'Main church'}},
        {'op': 'add', 'entry': {**night, 'event_kind': 'specific_date', 'day_of_week': None,
                                'date': '2026-11-07', 'cancelled': True}},
    ])))
    assert result['update_changes_applied'] == 3
    assert result['update_changes_rejected'] == 0


def _correct(conn, case) -> int:
    """Run migration 0012 for one parish; how many revisions it appended."""
    frozen = next(c for c in FROZEN['parishes'] if c['parish'] == case['parish'])
    before = conn.execute('SELECT COUNT(*) FROM schedule_revision').fetchone()[0]
    runpy.run_path(str(MIGRATION))['_correct'](conn, FROZEN['run_id'], frozen)
    return conn.execute('SELECT COUNT(*) FROM schedule_revision').fetchone()[0] - before


def test_frozen_oct25_repairs_are_valid_entries():
    for case in FROZEN['parishes']:
        for repair in case['repairs']:
            for columns in repair['before'] + repair['after']:
                entry = parse_entry(_labels(columns), {columns['church_slug']: 0})
                assert columns == {'church_slug': columns['church_slug'], **{
                    c: getattr(entry, c) for c in ENTRY_COLUMNS if c != 'church_id'}}


@pytest.mark.parametrize('case', SPEC['parishes'], ids=lambda case: case['parish'])
@pytest.mark.parametrize('later_review', [False, True])
def test_oct25_repairs_match_sources_preserve_later_reviews_and_replay(conn, case, later_review):
    slug = case['parish']
    conn.execute('UPDATE parish SET slug=? WHERE id=1', (slug,))
    raw = [e for repair in case['repairs'] for e in repair.get('before', [])]
    church = (raw or case['repairs'][0]['after'])[0]['church_slug']
    conn.execute("UPDATE church SET slug=? WHERE id=1", (church,))
    baseline = {**SUN_9, 'church_slug': church}
    _seed(conn, [baseline, *raw], slug=slug)
    _bulletin(conn, case['content_hash'], '2026-10-25T10:00:00Z', slug=slug)
    start_run(conn, SPEC['run_id'], git_sha='test', trigger='test')
    _run(conn, FakeUpdater(_reply(published_date='2026-10-25')), SPEC['run_id'])
    if later_review:
        # Reaffirm every old value, or explicitly reject each missing addition.
        for repair in case['repairs']:
            for e in repair.get('before', []) or repair['after']:
                parsed = parse_entry(e, {church: 1})
                target = next((i for i, value in live_entries(conn, 1).items() if value == parsed), None)
                if target is not None:
                    edit_entry(conn, 1, 'delete', target_entry_id=target, actor='Reviewer')
                    edit_entry(conn, 1, 'add', entry=e, actor='Reviewer', today=date(2026, 10, 25))
                else:
                    edit_entry(conn, 1, 'add', entry=e, actor='Reviewer', today=date(2026, 10, 25))
                    target = next(i for i, value in live_entries(conn, 1).items() if value == parsed)
                    edit_entry(conn, 1, 'delete', target_entry_id=target, actor='Reviewer')
    edit_entry(conn, 1, 'add', entry={**baseline, 'start_time': '11:00 AM'}, actor='Unrelated')
    before = live_entries(conn, 1)
    calls = list(map(tuple, conn.execute('SELECT * FROM llm_call')))
    with conn:
        count = _correct(conn, case)
    assert (count == 0) == later_review
    if later_review:
        assert live_entries(conn, 1) == before
    else:
        for repair in case['repairs']:
            for e in repair['after']:
                assert parse_entry(e, {church: 1}) in live_entries(conn, 1).values()
    assert _correct(conn, case) == 0
    assert list(map(tuple, conn.execute('SELECT * FROM llm_call'))) == calls
    assert rebuild_current_schedule(conn)['differing_rows'] == 0
    assert not list(conn.execute('PRAGMA foreign_key_check'))


def test_python_migration_rolls_back_data_and_version(tmp_path):
    migrations = tmp_path / 'migrations'
    migrations.mkdir()
    (migrations / '0001_first.py').write_text(
        "def migrate(conn):\n    conn.execute('CREATE TABLE t (id INTEGER)')\n"
        "    conn.execute('INSERT INTO t VALUES (1)')\n    raise ValueError('stop')\n"
    )
    with connect_db(tmp_path / 'db') as db:
        with pytest.raises(ValueError, match='stop'):
            migrate(db, migrations)
        assert db.execute('PRAGMA user_version').fetchone()[0] == 0
        assert db.execute("SELECT 1 FROM sqlite_master WHERE name='t'").fetchone() is None


def test_python_migration_commits_a_pending_write_first(tmp_path):
    migrations = tmp_path / 'migrations'
    migrations.mkdir()
    (migrations / '0001_first.py').write_text(
        "def migrate(conn):\n    conn.execute('CREATE TABLE t (id INTEGER)')\n"
    )
    with connect_db(tmp_path / 'db') as db:
        db.execute('CREATE TABLE pending (id INTEGER)')
        db.execute('INSERT INTO pending VALUES (1)')
        assert migrate(db, migrations) == 1
    with sqlite3.connect(tmp_path / 'db') as check:
        assert check.execute('SELECT id FROM pending').fetchall() == [(1,)]
