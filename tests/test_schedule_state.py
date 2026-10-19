"""Believed schedules updated by proposed changes (docs/schedule-state-plan.md)."""

from __future__ import annotations

import json
import sqlite3
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
import pytest
from openai import APITimeoutError, InternalServerError, RateLimitError

from pdf_extract import process
from pdf_extract.blobstore import get_store
from pdf_extract.classifiers.schedule_update import (
    LENIENT,
    OK,
    PARSE_FAILED,
    POLICY,
    STRICT_SCHEMA,
    OpenAIScheduleUpdater,
    RawReply,
    parse_response,
)
from pdf_extract.db import create_db, ensure_db, migrate
from pdf_extract.extract_frontend_db import extract, read_snapshot
from pdf_extract.labeling.bulletins import load_gemini_source
from pdf_extract.report import build_report, diff_databases, render_markdown
from pdf_extract.runs import parish_results, start_run
from pdf_extract.schedule.edits import EditError, apply_proposals, edit_entry
from pdf_extract.schedule.entries import (
    ENTRY_COLUMNS,
    INVALID_ENTRY,
    UNKNOWN_CHURCH,
    EntryError,
    parse_entry,
)
from pdf_extract.schedule.history import call_week, parish_history
from pdf_extract.schedule.policy import (
    APPLIED,
    AUTO,
    DUPLICATE,
    INVALID_MODIFY,
    MASS_DELETE,
    NO_CHANGE,
    PAST_DATE,
    REJECTED,
    STALE_BULLETIN,
    UNKNOWN_ITEM,
    WRONG_BULLETIN,
    Proposal,
    decide,
    whole_call_reason,
)
from pdf_extract.schedule.qualifiers import (
    QualifierError,
    columns_to_season,
    describe_schedule_pattern,
    mask_excludes_weeks,
    mask_to_weeks,
    season_to_columns,
    weeks_to_mask,
)
from pdf_extract.schedule.report import describe_entry
from pdf_extract.schedule.store import (
    current_revision,
    intern_entry,
    live_entries,
    load_entries,
    parish_churches,
    rebuild_current_schedule,
    render_view,
    update_mode_parishes,
    write_seed,
)
from pdf_extract.schedule.update import (
    MAX_FAILED_CALLS,
    call_record_key,
    process_update_mode,
    request_key,
)
from pdf_extract.seeding.files import revision_note
from pdf_extract.storage import (
    CHURCHES_CSV_PATH,
    DEFAULT_DB_PATH,
    PARISHES_CSV_PATH,
    connect_db,
    insert_bulletin,
    save_processed_bulletin,
)
from tests.conftest import CHURCH_FIELDS, PARISH_FIELDS, write_csv

PARISH = {"slug": "test-parish", "name": "Test Parish", "website": "https://example.org"}
OTHER_PARISH = {"slug": "other-parish", "name": "Other Parish", "website": "https://o.org"}
CHURCH = {
    "parish_id": "test-parish", "slug": "test-church", "name": "Test Church",
    "line1": "1 Main St", "city": "Rochester", "state": "NY", "postal_code": "14620",
}
SECOND = {**CHURCH, "slug": "second-church", "name": "Second Church"}
OTHER = {**CHURCH, "parish_id": "other-parish", "slug": "other-church", "name": "Other"}

SUN_9 = {
    "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
    "day_of_week": "Sunday", "start_time": "9:00 AM",
}
SUN_11 = {**SUN_9, "start_time": "11:00 AM"}
SAT_5 = {**SUN_9, "day_of_week": "Saturday", "start_time": "5:00 PM"}
CONFESSION = {
    **SUN_9, "event_type": "confession", "day_of_week": "Saturday", "start_time": "3:00 PM",
    "end_time": "3:45 PM", "weeks_of_month": ["first"],
}
SEED_AS_OF = "2026-10-01T00:00:00Z"


def _write_reference(parishes: list[dict], churches: list[dict]) -> None:
    write_csv(PARISHES_CSV_PATH, PARISH_FIELDS, parishes)
    write_csv(CHURCHES_CSV_PATH, CHURCH_FIELDS, churches)


@pytest.fixture
def conn(pipeline_dir: Path, monkeypatch: pytest.MonkeyPatch):
    _write_reference([PARISH, OTHER_PARISH], [CHURCH, SECOND, OTHER])
    create_db()
    monkeypatch.setattr(
        "pdf_extract.schedule.update.read_bulletin_pdf", lambda slug, content_hash: b"%PDF",
    )
    c = connect_db()
    yield c
    c.close()


def _parish_id(conn: sqlite3.Connection, slug: str = "test-parish") -> int:
    return conn.execute("SELECT id FROM parish WHERE slug = ?", (slug,)).fetchone()[0]


def _churches(conn: sqlite3.Connection, slug: str = "test-parish") -> dict[str, int]:
    return parish_churches(conn, _parish_id(conn, slug))


def _seed(
    conn: sqlite3.Connection, entries: list[dict], *, as_of: str = SEED_AS_OF,
    slug: str = "test-parish",
) -> int:
    churches = _churches(conn, slug)
    with conn:
        return write_seed(
            conn, _parish_id(conn, slug), [parse_entry(e, churches) for e in entries],
            as_of=as_of, actor="test",
        )


def _ids(conn: sqlite3.Connection, slug: str = "test-parish") -> dict[str, int]:
    """Live entry ids by "<day> <start>" (weekly) or "<date> <start>" (dated)."""
    out = {}
    for entry_id, entry in live_entries(conn, _parish_id(conn, slug)).items():
        anchor = entry.day_of_week or entry.date
        out[f"{entry.event_type} {anchor} {entry.start_time}"] = entry_id
    return out


def _bulletin(
    conn: sqlite3.Connection, name: str, fetched_at: str, *, slug: str = "test-parish",
    published_date: str | None = None, processed: bool = False,
) -> int:
    bulletin_id = insert_bulletin(
        conn, parish_id=_parish_id(conn, slug), source_url=f"https://example.org/{name}.pdf",
        content_hash=name, fetched_at=fetched_at,
    )
    if processed:
        save_processed_bulletin(
            conn, bulletin_id, [], processed_at=fetched_at, published_date=published_date,
        )
    return bulletin_id


class FakeUpdater(OpenAIScheduleUpdater):
    """Answers each call with the next reply; records the contexts it was given."""

    def __init__(self, *replies: Any) -> None:
        super().__init__(model="fake-model")
        self.replies = list(replies)
        self.contexts: list[str] = []

    def call(self, pdf_bytes: bytes, context: str) -> RawReply:
        self.contexts.append(context)
        reply = self.replies.pop(0)
        if callable(reply):
            reply = reply(context)
        if isinstance(reply, BaseException):
            raise reply
        text = reply if isinstance(reply, str) else json.dumps(reply)
        return RawReply(
            text=text, served_model="fake-model-001",
            usage={"prompt_tokens": 100, "cached_tokens": 10, "output_tokens": 20},
            latency_ms=5, service_tier="flex",
        )


def _reply(**fields: Any) -> dict[str, Any]:
    return {
        "published_date": None, "wrong_bulletin": False, "church_list_needs_review": False,
        "seen": [], "changes": [], **fields,
    }


def _run(conn: sqlite3.Connection, updater: FakeUpdater, run_id: str | None = None) -> dict:
    return process_update_mode(conn, run_id=run_id, updater=updater, concurrency=2)


def _proposals(conn: sqlite3.Connection) -> list[tuple]:
    return [
        tuple(r) for r in conn.execute(
            "SELECT llm_call_id, seq, op, decision, reason FROM proposed_change ORDER BY id"
        ).fetchall()
    ]


# ── Migration ───────────────────────────────────────────────────────────────
def test_migration_adds_the_schedule_tables(conn: sqlite3.Connection) -> None:
    tables = {
        r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    assert {
        "prompt_blob", "schedule_view", "llm_call", "schedule_entry", "schedule_revision",
        "proposed_change", "schedule_change", "current_schedule", "entry_sighting",
    } <= tables
    columns = {r[1] for r in conn.execute("PRAGMA table_info(church)")}
    assert "retired_at" in columns


# ── Qualifiers and entries ──────────────────────────────────────────────────
def test_qualifiers_are_described_as_the_web_app_describes_them() -> None:
    # The display table of PR 22's PRD, which apps/web/src/lib/schedulePattern.ts follows.
    def season(start_month, start_day, end_month, end_day):
        return columns_to_season(start_month, start_day, end_month, end_day)

    assert describe_schedule_pattern([], None, "Friday") is None
    assert describe_schedule_pattern(["first"], None, "Friday") == "First Friday of the month"
    assert describe_schedule_pattern(["fourth", "second"], None, "saturday") == (
        "Second and fourth Saturdays of the month")
    assert describe_schedule_pattern([], season(10, None, 6, None), "Tuesday") == (
        "October through June")
    assert describe_schedule_pattern([], season(6, 4, 9, 10), "Thursday") == (
        "June 4 through September 10")
    assert describe_schedule_pattern(["first"], season(10, None, 6, None), "Friday") == (
        "First Friday of the month, October through June")
    assert describe_schedule_pattern(["last"], None, "sunday", True) == (
        "Every Sunday except the last")
    assert describe_schedule_pattern(["first", "last"], None, None, True) == (
        "Every week except the first and last")


def test_weeks_and_seasons_convert_both_ways() -> None:
    assert weeks_to_mask(["first", "third"]) == 0b101
    assert weeks_to_mask([]) == 0
    assert mask_to_weeks(0b100001) == ["first", "last"]
    assert season_to_columns({"start_month": "October", "start_day": None,
                              "end_month": 6, "end_day": 15}) == (10, None, 6, 15)
    assert columns_to_season(10, None, 6, 15) == {
        "start_month": 10, "start_day": None, "end_month": 6, "end_day": 15,
    }
    assert columns_to_season(None, None, None, None) is None
    with pytest.raises(QualifierError):
        weeks_to_mask(["first", "first"])


def test_excluded_weeks_are_stored_in_their_canonical_form() -> None:
    # Every week except the last: the listed week plus the exclusion bit.
    assert weeks_to_mask(["last"], True) == 0b1100000
    assert (mask_to_weeks(0b1100000), mask_excludes_weeks(0b1100000)) == (["last"], True)
    assert not mask_excludes_weeks(0b100001)
    # An exclusion the remaining weeks can say is stored as them.
    assert weeks_to_mask(["second"], True) == weeks_to_mask(["first", "third", "fourth", "fifth"])
    # A fifth week is always the last, so excluding both is excluding the last.
    assert weeks_to_mask(["fifth", "last"], True) == weeks_to_mask(["last"], True)
    # Excluding nothing is every week.
    assert weeks_to_mask([], True) == 0
    for never in (["first", "second", "third", "fourth", "fifth"],
                  ["first", "second", "third", "fourth", "last"]):
        with pytest.raises(QualifierError):
            weeks_to_mask(never, True)
    with pytest.raises(QualifierError):
        weeks_to_mask(["last"], "yes")


def test_an_excluded_week_round_trips_through_the_database(conn: sqlite3.Connection) -> None:
    churches = _churches(conn)
    except_last = parse_entry({**SUN_9, "weeks_of_month": ["last"], "exclude_weeks": True},
                              churches)
    assert except_last.identity_key == parse_entry(SUN_9, churches).identity_key
    with conn:
        entry_id = intern_entry(conn, except_last)
    stored = load_entries(conn, [entry_id])[entry_id]
    assert stored == except_last
    form = stored.labels_form("test-church")
    assert (form["weeks_of_month"], form["exclude_weeks"]) == (["last"], True)
    assert describe_entry(stored).endswith("(Every Sunday except the last)")
    # The same slot written as the weeks it keeps when it can be.
    except_first = parse_entry({**SUN_9, "weeks_of_month": ["first"], "exclude_weeks": True},
                               churches)
    assert except_first.labels_form("")["weeks_of_month"] == [
        "second", "third", "fourth", "fifth"]
    assert except_first.labels_form("")["exclude_weeks"] is False


def test_the_database_refuses_an_exclusion_of_no_weeks(conn: sqlite3.Connection) -> None:
    entry = parse_entry(SUN_9, _churches(conn))
    with pytest.raises(sqlite3.IntegrityError), conn:
        conn.execute(
            f"INSERT INTO schedule_entry (hash, identity_key, {', '.join(ENTRY_COLUMNS)}) "
            f"VALUES (?, ?, {', '.join('?' * len(ENTRY_COLUMNS))})",
            ("x", entry.identity_key,
             *(64 if name == "weeks_of_month" else getattr(entry, name)
               for name in ENTRY_COLUMNS)),
        )
    with pytest.raises(QualifierError):
        season_to_columns({"start_month": 2, "start_day": 30, "end_month": 3, "end_day": None})


def test_an_entry_is_read_and_its_identity_leaves_out_end_time_weeks_and_note(
    conn: sqlite3.Connection,
) -> None:
    churches = _churches(conn)
    entry = parse_entry(CONFESSION, churches)
    assert (entry.start_time, entry.end_time, entry.weeks_of_month) == (900, 945, 1)
    changed = parse_entry({**CONFESSION, "end_time": "4:00 PM", "weeks_of_month": [],
                           "note": "chapel"}, churches)
    assert changed.identity_key == entry.identity_key
    assert changed.hash != entry.hash
    moved = parse_entry({**CONFESSION, "start_time": "3:30 PM"}, churches)
    assert moved.identity_key != entry.identity_key


@pytest.mark.parametrize(
    ("change", "reason"),
    [
        ({"church_slug": "other-church"}, UNKNOWN_CHURCH),
        ({"date": "2026-10-10"}, INVALID_ENTRY),
        ({"start_time": "soon"}, INVALID_ENTRY),
        ({"event_type": "rosary"}, INVALID_ENTRY),
        ({"cancelled": True}, INVALID_ENTRY),
        ({"season": {"start_month": 4, "start_day": 31, "end_month": 5, "end_day": None}},
         INVALID_ENTRY),
        ({"event_kind": "specific_date", "date": "2026-10-10", "weeks_of_month": ["first"]},
         INVALID_ENTRY),
        ({"event_kind": "specific_date", "date": "2026-10-10", "weeks_of_month": ["last"],
          "exclude_weeks": True}, INVALID_ENTRY),
        ({"weeks_of_month": ["first", "second", "third", "fourth", "last"],
          "exclude_weeks": True}, INVALID_ENTRY),
        ({"weeks_of_month": ["last"], "exclude_weeks": "true"}, INVALID_ENTRY),
        ({"colour": "green"}, INVALID_ENTRY),
    ],
)
def test_entry_checks(conn: sqlite3.Connection, change: dict, reason: str) -> None:
    with pytest.raises(EntryError) as exc:
        parse_entry({**SUN_9, **change}, _churches(conn))
    assert exc.value.reason == reason


def test_a_dated_entry_may_repeat_its_own_weekday(conn: sqlite3.Connection) -> None:
    dated = {**SUN_9, "event_kind": "specific_date", "date": "2026-10-11"}
    assert parse_entry(dated, _churches(conn)).day_of_week is None
    with pytest.raises(EntryError):
        parse_entry({**dated, "day_of_week": "Monday"}, _churches(conn))


# ── Seeds, the log and the view ─────────────────────────────────────────────
def test_a_seed_switches_the_parish_to_update_mode(conn: sqlite3.Connection) -> None:
    assert update_mode_parishes(conn) == {}
    revision = _seed(conn, [SUN_9, SAT_5])
    assert revision == 1
    assert update_mode_parishes(conn) == {_parish_id(conn): SEED_AS_OF}
    assert sorted(_ids(conn)) == ["mass Saturday 1020", "mass Sunday 540"]


def test_a_later_seed_is_adds_modifies_and_deletes(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SAT_5])
    old = _ids(conn)
    _seed(conn, [{**SUN_9, "note": "Latin"}, SUN_11], as_of="2026-10-05T00:00:00Z")
    ops = sorted(r[0] for r in conn.execute(
        "SELECT op FROM schedule_change WHERE revision = 2"
    ).fetchall())
    assert ops == ["add", "delete", "modify"]
    new = _ids(conn)
    assert new["mass Sunday 540"] != old["mass Sunday 540"]
    assert "mass Saturday 1020" not in new
    assert update_mode_parishes(conn) == {_parish_id(conn): "2026-10-05T00:00:00Z"}


def test_rebuild_from_the_log_gives_the_same_table(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SAT_5])
    _seed(conn, [SUN_11, SAT_5])
    before = set(conn.execute("SELECT * FROM current_schedule").fetchall())
    with conn:
        result = rebuild_current_schedule(conn)
    assert result == {"parishes": 1, "differing_rows": 0}
    assert set(conn.execute("SELECT * FROM current_schedule").fetchall()) == before


def test_the_view_is_canonical_and_leaves_out_past_dated_entries(
    conn: sqlite3.Connection,
) -> None:
    past = {**SUN_9, "event_kind": "specific_date", "date": "2026-10-04"}
    future = {**SUN_9, "event_kind": "specific_date", "date": "2026-10-18",
              "start_time": "7:00 AM", "cancelled": True}
    _seed(conn, [SUN_11, SUN_9, CONFESSION, past, future])
    text, view_hash = render_view(conn, _parish_id(conn), date(2026, 10, 10))
    view = json.loads(text)
    assert [c["slug"] for c in view["churches"]] == ["second-church", "test-church"]
    entries = view["churches"][1]["entries"]
    assert [(e["event_type"], e.get("day_of_week") or e.get("date"), e["start_time"])
            for e in entries] == [
        ("confession", "Saturday", "3:00 PM"),
        ("mass", "Sunday", "9:00 AM"),
        ("mass", "Sunday", "11:00 AM"),
        ("mass", "2026-10-18", "7:00 AM"),
    ]
    assert entries[0]["weeks_of_month"] == ["first"]
    assert entries[3]["cancelled"] is True
    assert text == json.dumps(view, sort_keys=True, separators=(",", ":"))
    assert render_view(conn, _parish_id(conn), date(2026, 10, 10)) == (text, view_hash)


def _reviewed_seed(conn, *, status="approved"):
    seed = {
        "parish_slug": "test-parish", "status": status, "reviewer": "Reviewer",
        "as_of": SEED_AS_OF, "summary": "Stale draft summary: Friday is an open question.",
        "slots": [
            {"id": "s1", "status": "settled", "decision": "include", "entry": SUN_9},
            {"id": "s2", "status": "settled", "decision": "include",
             "entry": CONFESSION, "rationale": "Monthly service omitted by the routine panel."},
            {"id": "s3", "status": "settled", "decision": "exclude",
             "entry": {**SUN_9, "day_of_week": "Friday"},
             "rationale": "Relocated to another church until January.",
             "answer": {"choice": 1, "by": "Reviewer", "at": SEED_AS_OF}},
        ],
    }
    Path("data/seeds").mkdir(parents=True)
    Path("data/seeds/test-parish.json").write_text(json.dumps(seed))
    with conn:
        write_seed(conn, _parish_id(conn),
                   [parse_entry(e, _churches(conn)) for e in (SUN_9, CONFESSION)],
                   as_of=SEED_AS_OF, actor="Reviewer", note=revision_note(seed))
    return seed


def test_view_carries_resolved_exclusions_and_monthly_evidence_but_not_draft_summary(conn):
    _reviewed_seed(conn)
    text, _ = render_view(conn, _parish_id(conn), date(2026, 10, 18))
    context = json.loads(text)["reviewed_seed_context"]
    assert [d["id"] for d in context["decisions"]] == ["s2", "s3"]
    assert context["decisions"][1]["decision"] == "exclude"
    assert context["decisions"][1]["answer"]["choice"] == 1
    assert "Stale draft summary" not in text
    assert len(json.loads(text)["churches"][1]["entries"]) == 2


def test_review_context_changes_invalidate_cached_questions_without_reseeding(conn):
    seed = _reviewed_seed(conn)
    today = date(2026, 10, 18)
    entries = live_entries(conn, _parish_id(conn))
    _, before = render_view(conn, _parish_id(conn), today)
    seed["slots"][2]["rationale"] = "Now relocated until February."
    Path("data/seeds/test-parish.json").write_text(json.dumps(seed))
    _, after = render_view(conn, _parish_id(conn), today)
    assert before != after
    assert request_key("version", "pdf", before, today, "churches") != request_key(
        "version", "pdf", after, today, "churches",
    )
    assert live_entries(conn, _parish_id(conn)) == entries


@pytest.mark.parametrize("case", ["draft", "unimported", "newer_manual_seed"])
def test_view_does_not_use_context_from_an_unapproved_or_superseded_seed(conn, case):
    seed = _reviewed_seed(conn)
    if case == "draft":
        seed["status"] = "ready"
    elif case == "unimported":
        seed["slots"][0]["entry"] = SUN_11
    else:
        _seed(conn, [SUN_11], as_of="2026-10-17T00:00:00Z")
    Path("data/seeds/test-parish.json").write_text(json.dumps(seed))
    text, _ = render_view(conn, _parish_id(conn), date(2026, 10, 18))
    assert "reviewed_seed_context" not in json.loads(text)


@pytest.mark.parametrize("slug,church,event_type,day,time,weeks,op", [
    ("all-saints-corning", "st-marys-corning", "mass", "Saturday", "4:00 PM", [], "add"),
    ("st-edward-the-confessor-clifton-park", "st-edward-the-confessor-clifton-park",
     "mass", "Friday", "9:00 AM", [], "add"),
    ("holy-trinity-webster", "holy-trinity", "mass", "Saturday", "6:30 PM", ["first"], "delete"),
    ("mary-mother-of-our-savior-utica", "our-lady-of-lourdes-utica", "mass", "Saturday",
     "8:15 AM", ["first"], "delete"),
    ("mary-mother-of-our-savior-utica", "our-lady-of-lourdes-utica", "confession", "Saturday",
     "8:45 AM", ["first"], "delete"),
])
@pytest.mark.parametrize("later_review", [False, True])
def test_weekly_repair_appends_inverse_changes_but_preserves_later_reviews(
    conn, slug, church, event_type, day, time, weeks, op, later_review,
):
    parish_id = _parish_id(conn)
    conn.execute("UPDATE parish SET slug=? WHERE id=?", (slug, parish_id))
    conn.execute("UPDATE church SET slug=? WHERE slug='test-church'", (church,))
    baseline = {**SUN_9, "church_slug": church}
    target = {**baseline, "event_type": event_type, "day_of_week": day,
              "start_time": time, "weeks_of_month": weeks}
    _seed(conn, [baseline] + ([target] if op == "delete" else []), slug=slug)
    target_id = next(iter(live_entries(conn, parish_id))) if op == "add" else next(
        i for i, e in live_entries(conn, parish_id).items() if e.day_of_week == day
    )
    _bulletin(conn, "new", "2026-10-18T10:00:00Z", slug=slug)
    run_id = "20261018T123547Z-gh39127931592"
    start_run(conn, run_id, git_sha="test", trigger="test")
    changes = [{"op": op, "entry": target} if op == "add" else
               {"op": "delete", "entry_id": target_id}]
    updater = FakeUpdater(_reply(published_date="2026-10-18", changes=changes))
    result = process_update_mode(conn, slugs=[slug], updater=updater, run_id=run_id)
    assert result["update_changes_applied"] == 1
    target_id = intern_entry(conn, parse_entry(target, _churches(conn, slug)))
    if later_review:
        # Reaffirm the same final state as the bad proposal with new human edits.
        # Content equality alone must not let the migration undo that later decision.
        if op == "add":
            edit_entry(conn, parish_id, "delete", target_entry_id=target_id, actor="Reviewer")
            edit_entry(conn, parish_id, "add", entry=target, actor="Reviewer")
        else:
            edit_entry(conn, parish_id, "add", entry=target, actor="Reviewer")
            edit_entry(conn, parish_id, "delete", target_entry_id=target_id, actor="Reviewer")
    # An unrelated change after the faulty call must survive the repair too.
    edit_entry(conn, parish_id, "add", entry={**baseline, "start_time": "11:00 AM"},
               actor="Reviewer")
    old_state = set(live_entries(conn, parish_id))
    old_proposals = _proposals(conn)
    conn.execute("PRAGMA user_version = 7")
    conn.commit()
    assert migrate(conn) == 1
    state = set(live_entries(conn, parish_id))
    if later_review:
        assert state == old_state
    else:
        assert state == (old_state - {target_id} if op == "add" else old_state | {target_id})
        revision = conn.execute(
            "SELECT * FROM schedule_revision WHERE actor='weekly-run-review'",
        ).fetchone()
        assert revision["source_kind"] == "human"
    assert _proposals(conn) == old_proposals
    assert rebuild_current_schedule(conn)["differing_rows"] == 0
    assert migrate(conn) == 0


# ── Policy ──────────────────────────────────────────────────────────────────
def _decide(conn: sqlite3.Connection, proposals: list[Proposal], whole: str | None = None):
    return [
        (d.proposal.seq, d.decision, d.reason)
        for d in decide(
            proposals, live=live_entries(conn, _parish_id(conn)), churches=_churches(conn),
            today=date(2026, 10, 10), whole_call=whole,
        )
    ]


def test_each_proposal_is_checked_against_the_schedule_the_earlier_ones_left(
    conn: sqlite3.Connection,
) -> None:
    _seed(conn, [SUN_9, SAT_5, CONFESSION])
    ids = _ids(conn)
    sun9, sat5, conf = ids["mass Sunday 540"], ids["mass Saturday 1020"], ids[
        "confession Saturday 900"]
    proposals = [
        Proposal(1, "modify", {}, sun9, {**SUN_9, "start_time": "9:30 AM"}),
        Proposal(2, "delete", {}, sun9),  # already changed by seq 1
        Proposal(3, "add", {}, None, SAT_5),  # the slot is taken
        Proposal(4, "modify", {}, sat5, {**SAT_5, "event_type": "confession"}),
        Proposal(5, "add", {}, None, {**SUN_9, "event_kind": "specific_date",
                                       "day_of_week": None, "date": "2026-10-01"}),
        Proposal(6, "modify", {}, conf, CONFESSION),
        Proposal(7, "add", {}, None, {**SUN_9, "church_slug": "other-church"}),
        Proposal(8, "add", {}, None, {**SUN_9, "start_time": "9:30 AM"}),  # seq 1 took it
        Proposal(9, "delete", {}, 999_999),
        Proposal(10, "add", {}, None, {**SUN_9, "event_kind": "specific_date",
                                        "date": "2026-10-11", "cancelled": True}),
    ]
    assert _decide(conn, proposals) == [
        (1, APPLIED, AUTO),
        (2, REJECTED, UNKNOWN_ITEM),
        (3, REJECTED, DUPLICATE),
        (4, REJECTED, INVALID_MODIFY),
        (5, REJECTED, PAST_DATE),
        (6, REJECTED, NO_CHANGE),
        (7, REJECTED, UNKNOWN_CHURCH),
        (8, REJECTED, DUPLICATE),
        (9, REJECTED, UNKNOWN_ITEM),
        (10, APPLIED, AUTO),
    ]


def test_whole_call_reasons(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SUN_11, SAT_5, CONFESSION])
    live = live_entries(conn, _parish_id(conn))
    ids = list(_ids(conn).values())
    deletes = [Proposal(i, "delete", {}, entry_id) for i, entry_id in enumerate(ids[:3], 1)]
    assert whole_call_reason(wrong_bulletin=False, stale=False, proposals=deletes,
                             live=live) == MASS_DELETE
    assert whole_call_reason(wrong_bulletin=False, stale=False, proposals=deletes[:2],
                             live=live) is None
    assert whole_call_reason(wrong_bulletin=True, stale=True, proposals=[],
                             live=live) == WRONG_BULLETIN
    assert whole_call_reason(wrong_bulletin=False, stale=True, proposals=[],
                             live=live) == STALE_BULLETIN
    assert _decide(conn, deletes, MASS_DELETE) == [
        (1, REJECTED, MASS_DELETE), (2, REJECTED, MASS_DELETE), (3, REJECTED, MASS_DELETE),
    ]


# ── Weeks and the high-water mark ───────────────────────────────────────────
def test_call_weeks() -> None:
    assert call_week("2026-10-11", "2026-10-10T12:00:00Z") == date(2026, 10, 11)
    assert call_week("2026-10-10", "2026-10-10T12:00:00Z") == date(2026, 10, 11)
    assert call_week(None, "2026-10-10T12:00:00Z") is None
    # Implausibly far past the fetch: undated, not a guess from the fetch date.
    assert call_week("2026-12-25", "2026-10-10T12:00:00Z") is None


def test_the_mark_starts_at_the_newest_dated_bulletin_in_the_seed(
    conn: sqlite3.Connection,
) -> None:
    _bulletin(conn, "seeded", "2026-09-26T12:00:00Z", published_date="2026-09-27",
              processed=True)
    _bulletin(conn, "later", "2026-10-03T12:00:00Z", published_date="2026-10-04",
              processed=True)
    _seed(conn, [SUN_9], as_of="2026-09-30T00:00:00Z")
    history = parish_history(conn, _parish_id(conn))
    assert (history.places, history.mark) == ([], date(2026, 9, 27))
    assert history.counted_weeks == [date(2026, 9, 27)]


# ── The update stage ────────────────────────────────────────────────────────
def test_a_bulletin_is_read_against_the_believed_schedule(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SAT_5, CONFESSION])
    ids = _ids(conn)
    bulletin_id = _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    with conn:
        start_run(conn, "run-1", git_sha=None, trigger="test")
    updater = FakeUpdater(_reply(
        published_date="2026-10-11",
        seen=[{"entry_id": ids["mass Sunday 540"], "page_number": 2},
              {"entry_id": 424242, "page_number": 9}],
        changes=[
            {"op": "modify", "entry_id": ids["confession Saturday 900"],
             "entry": {**CONFESSION, "end_time": "4:00 PM", "date": None, "cancelled": False,
                       "season": None, "note": None},
             "page_number": 3, "rationale": "Now until 4."},
            {"op": "add", "entry": {**SUN_9, "event_kind": "specific_date",
                                    "date": "2026-10-18", "cancelled": True},
             "page_number": 1, "rationale": "No 9 AM Mass on the 18th."},
            {"op": "delete", "entry_id": ids["mass Saturday 1020"], "page_number": 1,
             "rationale": "Vigil discontinued."},
        ],
    ))

    stats = _run(conn, updater, "run-1")

    assert stats["update_calls"] == 1
    assert stats["update_changes_applied"] == 3
    # The model was shown the church list, the fetch date and the view.
    [context] = updater.contexts
    assert "2026-10-10 (Saturday)" in context
    assert f'"id":{ids["mass Sunday 540"]}' in context
    call = conn.execute("SELECT * FROM llm_call").fetchone()
    assert (call["status"], call["base_revision"], call["call_date"]) == (OK, 1, "2026-10-10")
    assert (call["served_model"], call["input_tokens"], call["output_tokens"]) == (
        "fake-model-001", 100, 20)
    assert call["service_tier"] == "flex"
    assert call["response_key"] == call_record_key(call["request_key"])
    assert get_store().get(call["response_key"]) is not None
    assert {r[0] for r in conn.execute("SELECT kind FROM prompt_blob")} == {
        "policy", "schema", "context_template"}
    assert [p[2:] for p in _proposals(conn)] == [
        ("modify", APPLIED, AUTO), ("add", APPLIED, AUTO), ("delete", APPLIED, AUTO),
    ]
    revision = conn.execute("SELECT * FROM schedule_revision WHERE revision = 2").fetchone()
    assert (revision["source_kind"], revision["llm_call_id"], revision["run_id"]) == (
        "llm", call["id"], "run-1")
    assert current_revision(conn, _parish_id(conn)) == 2
    assert "mass Saturday 1020" not in _ids(conn)
    # Sightings: the seen entry that is in the view, and the applied new entries.
    sightings = conn.execute(
        "SELECT entry_id, page_number FROM entry_sighting WHERE bulletin_id = ?",
        (bulletin_id,),
    ).fetchall()
    assert len(sightings) == 3
    assert (ids["mass Sunday 540"], 2) in [tuple(s) for s in sightings]
    bulletin = conn.execute("SELECT * FROM bulletin WHERE id = ?", (bulletin_id,)).fetchone()
    assert bulletin["published_date"] == "2026-10-11"
    assert bulletin["processed_at"] is not None
    [result] = parish_results(conn, "run-1")
    assert result["status"] == "updated"
    with conn:
        assert rebuild_current_schedule(conn)["differing_rows"] == 0

    # Nothing is pending any more.
    assert _run(conn, FakeUpdater())["update_calls"] == 0


def test_bulletins_are_called_in_fetch_order_and_older_ones_are_stale(
    conn: sqlite3.Connection,
) -> None:
    _bulletin(conn, "seeded", "2026-09-26T12:00:00Z", published_date="2026-09-27",
              processed=True)
    _seed(conn, [SUN_9], as_of="2026-09-30T00:00:00Z")
    sun9 = _ids(conn)["mass Sunday 540"]
    _bulletin(conn, "new", "2026-10-03T12:00:00Z")
    _bulletin(conn, "fallback", "2026-10-04T12:00:00Z")
    _bulletin(conn, "correction", "2026-10-05T12:00:00Z")
    updater = FakeUpdater(
        _reply(published_date="2026-10-04", changes=[
            {"op": "add", "entry": SUN_11, "page_number": 1, "rationale": "new"}]),
        _reply(published_date="2026-09-20", changes=[
            {"op": "delete", "entry_id": sun9, "page_number": 1, "rationale": "old"}]),
        _reply(published_date="2026-10-04", seen=[{"entry_id": sun9, "page_number": 1}]),
    )

    _run(conn, updater, None)

    assert [p[2:] for p in _proposals(conn)] == [
        ("add", APPLIED, AUTO), ("delete", REJECTED, STALE_BULLETIN),
    ]
    history = parish_history(conn, _parish_id(conn))
    places = history.places
    assert [p.stale for p in places] == [False, True, False]
    assert places[2].same_week_before == 1  # a correction
    assert history.mark == date(2026, 10, 4)
    # The stale call wrote no sightings.
    stale_bulletin = places[1].bulletin_id
    assert conn.execute(
        "SELECT COUNT(*) FROM entry_sighting WHERE bulletin_id = ?", (stale_bulletin,),
    ).fetchone()[0] == 0


def test_a_bulletin_before_the_seed_is_never_called(conn: sqlite3.Connection) -> None:
    _bulletin(conn, "old", "2026-09-26T12:00:00Z")
    _seed(conn, [SUN_9])
    assert _run(conn, FakeUpdater())["update_calls"] == 0


def test_a_wrong_bulletin_is_rejected_whole(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    bulletin_id = _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(wrong_bulletin=True, changes=[
        {"op": "add", "entry": SUN_11, "page_number": 1, "rationale": "x"}])))
    assert [p[3:] for p in _proposals(conn)] == [(REJECTED, WRONG_BULLETIN)]
    assert conn.execute(
        "SELECT wrong_bulletin FROM bulletin WHERE id = ?", (bulletin_id,),
    ).fetchone()[0] == 1
    assert current_revision(conn, _parish_id(conn)) == 1


def test_a_failed_call_is_retried_until_it_is_given_up(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    for attempt in range(MAX_FAILED_CALLS):
        stats = _run(conn, FakeUpdater(RuntimeError("boom") if attempt else "not json"))
        assert stats["update_failed_calls"] == 1
    statuses = [r[0] for r in conn.execute("SELECT status FROM llm_call ORDER BY id")]
    assert statuses == [PARSE_FAILED, "api_error", "api_error"]
    stats = _run(conn, FakeUpdater())
    assert (stats["update_calls"], stats["update_gave_up"]) == (0, 1)


def test_a_failed_call_keeps_what_was_tried_before_it(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    error = RuntimeError("standard tier down")
    error.add_note("asked at the standard tier after flex failed: flex full")
    _run(conn, FakeUpdater(error))
    [stored] = [r[0] for r in conn.execute("SELECT error FROM llm_call")]
    assert stored == (
        "RuntimeError: standard tier down; "
        "asked at the standard tier after flex failed: flex full"
    )


def test_a_stored_reply_is_decided_without_calling_again(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    reply = _reply(changes=[{"op": "add", "entry": SUN_11, "page_number": 1,
                             "rationale": "x"}])
    # A crash after the reply was stored and before the decision committed.
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(
            "pdf_extract.schedule.update.decide_and_apply",
            lambda *a, **k: (_ for _ in ()).throw(KeyboardInterrupt()),
        )
        with pytest.raises(KeyboardInterrupt):
            _run(conn, FakeUpdater(reply))
    assert conn.execute("SELECT COUNT(*) FROM llm_call").fetchone()[0] == 0

    stats = _run(conn, FakeUpdater())  # no replies: a call would fail

    assert (stats["update_calls"], stats["update_reused_replies"]) == (0, 1)
    assert "mass Sunday 660" in _ids(conn)


def test_a_view_that_no_longer_matches_fails_the_parish(
    conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")

    real_render = __import__("pdf_extract.schedule.update", fromlist=["render_view"]).render_view
    calls = {"n": 0}

    def render(*args, **kwargs):
        calls["n"] += 1
        text, view_hash = real_render(*args, **kwargs)
        return (text, view_hash if calls["n"] == 1 else "something-else")

    monkeypatch.setattr("pdf_extract.schedule.update.render_view", render)
    with conn:
        start_run(conn, "run-1", git_sha=None, trigger="test")
    stats = _run(conn, FakeUpdater(_reply()), "run-1")

    assert stats["update_failed_calls"] == 1
    assert conn.execute("SELECT COUNT(*) FROM proposed_change").fetchone()[0] == 0
    [result] = parish_results(conn, "run-1")
    assert result["status"] == "failed"
    assert "no longer renders" in result["detail"]


def test_the_process_stage_splits_parishes_by_mode(
    conn: sqlite3.Connection, monkeypatch: pytest.MonkeyPatch,
) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "update-1", "2026-10-10T12:00:00Z")
    _bulletin(conn, "extract-1", "2026-10-10T12:00:00Z", slug="other-parish")
    extracted: list[str] = []

    def fake_extract(self, pdf_bytes, *, churches, today):
        extracted.append(churches[0]["slug"])
        return {"events": [], "published_date": None, "wrong_bulletin": False}

    monkeypatch.setattr(process.GeminiClassifier, "extract", fake_extract)
    monkeypatch.setattr("pdf_extract.storage.read_bulletin_pdf", lambda *a: b"%PDF")
    updater = FakeUpdater(_reply())
    monkeypatch.setattr(process, "OpenAIScheduleUpdater", lambda: updater)

    result = process.process_bulletins(concurrency=1)

    assert extracted == ["other-church"]
    assert result["processed_bulletins"] == 1
    assert result["update_calls"] == 1


# ── Snapshot ────────────────────────────────────────────────────────────────
def test_an_update_mode_parish_is_snapshotted_from_its_believed_schedule(
    conn: sqlite3.Connection, tmp_path: Path,
) -> None:
    _seed(conn, [
        SUN_9, CONFESSION, {**SUN_11, "weeks_of_month": ["last"], "exclude_weeks": True},
    ])
    ids = _ids(conn)
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(
        published_date="2026-10-11",
        seen=[{"entry_id": ids["mass Sunday 540"], "page_number": 2}],
        changes=[{"op": "add", "entry": {**SUN_9, "event_kind": "specific_date",
                                         "date": "2026-10-18", "cancelled": True},
                  "page_number": 1, "rationale": "x"}],
    )))
    dest = tmp_path / "frontend.json.gz"

    extract(DEFAULT_DB_PATH, dest, build_date=date(2026, 10, 10))

    tables = read_snapshot(dest.read_bytes())
    church = next(c for c in tables["churches"] if c["slug"] == "test-church")
    assert church["bulletin_url"] == "https://example.org/b1.pdf"
    assert church["bulletin_week"] == "2026-10-11"
    events = {e["id"]: e for e in tables["events"]}
    sun9 = events[-ids["mass Sunday 540"]]
    assert sun9["page_number"] == 2
    confession = events[-ids["confession Saturday 900"]]
    assert (confession["weeks_of_month"], confession["page_number"]) == (["first"], None)
    assert confession["exclude_weeks"] is False
    sun11 = events[-ids["mass Sunday 660"]]
    assert (sun11["weeks_of_month"], sun11["exclude_weeks"]) == (["last"], True)
    [cancellation] = [e for e in events.values() if e["cancelled"]]
    assert cancellation["id"] < 0
    assert cancellation["cancels_event_id"] == sun9["id"]


# ── Churches leaving the CSV ────────────────────────────────────────────────
def test_a_church_with_entries_that_leaves_the_csv_is_retired(
    conn: sqlite3.Connection, tmp_path: Path,
) -> None:
    _seed(conn, [SUN_9, {**SUN_9, "church_slug": "second-church"}])
    second_id = _churches(conn)["second-church"]
    _write_reference([PARISH, OTHER_PARISH], [CHURCH, OTHER])

    stats = ensure_db()

    assert (stats["churches_retired"], stats["schedule_entries_removed"]) == (1, 1)
    row = conn.execute("SELECT retired_at FROM church WHERE id = ?", (second_id,)).fetchone()
    assert row["retired_at"] is not None
    revision = conn.execute(
        "SELECT source_kind, actor FROM schedule_revision WHERE revision = 2"
    ).fetchone()
    assert tuple(revision) == ("reference", "churches.csv")
    assert list(_ids(conn)) == ["mass Sunday 540"]
    assert "second-church" not in _churches(conn)
    text, _ = render_view(conn, _parish_id(conn), date(2026, 10, 10))
    assert "second-church" not in text
    extract(DEFAULT_DB_PATH, tmp_path / "s.json.gz")
    slugs = {c["slug"] for c in read_snapshot((tmp_path / "s.json.gz").read_bytes())["churches"]}
    assert "second-church" not in slugs

    # It comes back with its id and an empty schedule.
    _write_reference([PARISH, OTHER_PARISH], [CHURCH, SECOND, OTHER])
    ensure_db()
    row = conn.execute("SELECT id, retired_at FROM church WHERE slug = 'second-church'").fetchone()
    assert (row["id"], row["retired_at"]) == (second_id, None)


def test_a_church_without_entries_is_still_deleted(conn: sqlite3.Connection) -> None:
    _write_reference([PARISH, OTHER_PARISH], [CHURCH, OTHER])
    stats = ensure_db()
    assert (stats["churches_deleted"], stats["churches_retired"]) == (1, 0)


def test_a_church_moving_parish_leaves_its_entries_behind(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, {**SUN_9, "church_slug": "second-church"}])
    _write_reference([PARISH, OTHER_PARISH],
                     [CHURCH, {**SECOND, "parish_id": "other-parish"}, OTHER])
    stats = ensure_db()
    assert stats["schedule_entries_removed"] == 1
    assert list(_ids(conn)) == ["mass Sunday 540"]


def test_removing_a_parish_removes_its_schedule(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(changes=[
        {"op": "add", "entry": SUN_11, "page_number": 1, "rationale": "x"}])))
    _write_reference([OTHER_PARISH], [OTHER])
    ensure_db()
    for table in ("llm_call", "proposed_change", "schedule_revision", "schedule_change",
                  "current_schedule", "entry_sighting", "schedule_entry"):
        assert conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0, table


# ── Hand edits ──────────────────────────────────────────────────────────────
def test_a_rejected_call_can_be_applied_by_hand(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SUN_11, SAT_5])
    ids = _ids(conn)
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(changes=[
        {"op": "delete", "entry_id": entry_id, "page_number": 1, "rationale": "gone"}
        for entry_id in ids.values()
    ] + [{"op": "add", "entry": {**SUN_9, "start_time": "10:00 AM"}, "page_number": 1,
          "rationale": "new"}])))
    call_id = conn.execute("SELECT id FROM llm_call").fetchone()[0]
    assert {p[4] for p in _proposals(conn)} == {MASS_DELETE}

    result = apply_proposals(conn, call_id, [1, 4, 4], actor="luke", note="checked",
                             today=date(2026, 10, 10))

    assert result.applied == [1, 4]
    assert result.revision == 2
    rows = conn.execute(
        "SELECT op, proposed_change_id FROM schedule_change WHERE revision = 2 ORDER BY id"
    ).fetchall()
    assert [r["op"] for r in rows] == ["delete", "add"]
    assert all(r["proposed_change_id"] for r in rows)
    revision = conn.execute("SELECT * FROM schedule_revision WHERE revision = 2").fetchone()
    assert (revision["source_kind"], revision["actor"], revision["note"]) == (
        "human", "luke", "checked")
    # The proposals' own decisions stay as the policy made them.
    assert {p[3] for p in _proposals(conn)} == {REJECTED}
    # Applying it again: the deleted entry is gone, the added slot is taken.
    again = apply_proposals(conn, call_id, [1, 4], actor="luke", today=date(2026, 10, 10))
    assert [s[1] for s in again.skipped] == [UNKNOWN_ITEM, DUPLICATE]
    assert again.revision is None


def test_entries_can_be_edited_directly(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9])
    parish_id = _parish_id(conn)
    sun9 = _ids(conn)["mass Sunday 540"]
    edit_entry(conn, parish_id, "modify", target_entry_id=sun9,
               entry={**SUN_9, "note": "Latin"}, actor="luke", today=date(2026, 10, 10))
    edit_entry(conn, parish_id, "add", entry=SUN_11, actor="luke", today=date(2026, 10, 10))
    with pytest.raises(EditError, match="duplicate"):
        edit_entry(conn, parish_id, "add", entry=SUN_11, actor="luke")
    with pytest.raises(EditError, match="unknown_item"):
        edit_entry(conn, parish_id, "delete", target_entry_id=sun9, actor="luke")
    assert current_revision(conn, parish_id) == 3
    assert sorted(_ids(conn)) == ["mass Sunday 540", "mass Sunday 660"]


# ── The model's reply ───────────────────────────────────────────────────────
def test_replies_are_read_strictly_then_leniently() -> None:
    strict = parse_response(json.dumps(_reply(
        published_date="2026-10-11",
        seen=[{"entry_id": 3, "page_number": None}],
        changes=[{"op": "add", "entry": {**SUN_9, "event_kind": "weekly"}, "entry_id": None,
                  "page_number": 2, "rationale": " Because. "}],
    )))
    assert strict.status == OK
    assert strict.seen == [(3, None)]
    [change] = strict.changes
    assert (change.seq, change.op, change.page_number, change.rationale) == (
        1, "add", 2, "Because.")
    # Empty lists and nulls the schema fills in are dropped from the entry.
    assert "date" not in change.entry and "weeks_of_month" not in change.entry

    lenient = parse_response(json.dumps({"changes": [
        {"op": "rename"}, {"op": "delete", "entry_id": 5, "extra": 1},
    ], "published_date": "soon"}))
    assert lenient.status == LENIENT
    assert [(c.seq, c.op, c.entry_id) for c in lenient.changes] == [(2, "delete", 5)]
    assert lenient.published_date is None

    assert parse_response("nope").status == PARSE_FAILED
    assert parse_response("[]").status == PARSE_FAILED


def _fake_clients(create: Any) -> dict[str, Any]:
    client = SimpleNamespace(responses=SimpleNamespace(create=create))
    return {"flex": client, "default": client}


def _api_request() -> httpx.Request:
    return httpx.Request("POST", "https://api.openai.com/v1/responses")


def _completed(tier: str | None) -> SimpleNamespace:
    return SimpleNamespace(
        id="resp_2", status="completed", incomplete_details=None,
        model="gpt-6-luna-2026-09-01", output_text=json.dumps(_reply()),
        service_tier=tier, usage=None,
    )


def test_update_calls_run_on_gpt_6_luna_like_the_eval_classifier() -> None:
    updater = OpenAIScheduleUpdater()
    calls: list[dict[str, Any]] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        calls.append(kwargs)
        return SimpleNamespace(
            id="resp_1", status="completed", incomplete_details=None,
            model="gpt-6-luna-2026-09-01", output_text=json.dumps(_reply()),
            service_tier="flex",
            usage=SimpleNamespace(
                input_tokens=3000,
                input_tokens_details=SimpleNamespace(cached_tokens=1200, cache_write_tokens=0),
                output_tokens=900,
                output_tokens_details=SimpleNamespace(reasoning_tokens=600),
            ),
        )

    updater._clients = _fake_clients(create)
    reply = updater.call(b"%PDF-1.4", "the context")

    assert (updater.provider, updater.model) == ("openai", "gpt-6-luna")
    assert updater.params_json == '{"file_detail":"low","reasoning_effort":"high","strict":true}'
    [request] = calls
    assert request["reasoning"] == {"effort": "high"}
    assert request["text"]["format"]["strict"] is True
    assert request["store"] is False
    assert request["service_tier"] == "flex"
    developer, user = request["input"]
    assert developer["role"] == "developer"
    assert developer["content"] == [{
        "type": "input_text", "text": POLICY, "prompt_cache_breakpoint": {"mode": "explicit"},
    }]
    assert user["content"][0] == {"type": "input_text", "text": "the context"}
    assert user["content"][1]["type"] == "input_file"
    assert user["content"][1]["detail"] == "low"
    assert reply.served_model == "gpt-6-luna-2026-09-01"
    assert reply.usage["reasoning_tokens"] == 600
    assert reply.service_tier == "flex"
    assert parse_response(reply.text).status == OK

    # Strict decoding needs every field required and no defaults.
    assert '"default"' not in json.dumps(STRICT_SCHEMA)

    def objects(node: Any):
        if isinstance(node, dict):
            if node.get("type") == "object":
                yield node
            for value in node.values():
                yield from objects(value)
        elif isinstance(node, list):
            for value in node:
                yield from objects(value)

    for obj in objects(STRICT_SCHEMA):
        assert obj["additionalProperties"] is False
        assert set(obj["required"]) == set(obj["properties"])


def test_an_update_call_falls_back_to_the_standard_tier_when_flex_is_full() -> None:
    updater = OpenAIScheduleUpdater()
    tiers: list[str] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        tiers.append(kwargs["service_tier"])
        if kwargs["service_tier"] == "flex":
            request = httpx.Request("POST", "https://api.openai.com/v1/responses")
            raise RateLimitError(
                "Resource Unavailable", response=httpx.Response(429, request=request), body=None,
            )
        return SimpleNamespace(
            id="resp_1", status="completed", incomplete_details=None,
            model="gpt-6-luna-2026-09-01", output_text=json.dumps(_reply()),
            service_tier="default", usage=None,
        )

    updater._clients = _fake_clients(create)
    reply = updater.call(b"%PDF-1.4", "the context")

    assert tiers == ["flex", "default"]
    assert reply.service_tier == "default"
    assert parse_response(reply.text).status == OK


def test_an_update_call_falls_back_when_flex_capacity_is_lost_after_acceptance() -> None:
    updater = OpenAIScheduleUpdater()
    tiers: list[str] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        tiers.append(kwargs["service_tier"])
        if kwargs["service_tier"] == "flex":
            return SimpleNamespace(
                id="resp_1", status="failed", incomplete_details=None,
                error=SimpleNamespace(
                    code="server_error",
                    message="Flex processing is temporarily unavailable. Please try again later.",
                ),
                model="gpt-6-luna-2026-09-01", output_text="", service_tier="flex", usage=None,
            )
        return SimpleNamespace(
            id="resp_2", status="completed", incomplete_details=None,
            model="gpt-6-luna-2026-09-01", output_text=json.dumps(_reply()),
            service_tier="default", usage=None,
        )

    updater._clients = _fake_clients(create)
    reply = updater.call(b"%PDF-1.4", "the context")

    assert tiers == ["flex", "default"]
    assert reply.service_tier == "default"
    assert parse_response(reply.text).status == OK


def test_an_update_call_falls_back_when_flex_keeps_failing_with_a_server_error() -> None:
    updater = OpenAIScheduleUpdater()
    tiers: list[str] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        tiers.append(kwargs["service_tier"])
        if kwargs["service_tier"] == "flex":
            request = httpx.Request("POST", "https://api.openai.com/v1/responses")
            raise InternalServerError(
                "server error", response=httpx.Response(500, request=request), body=None,
            )
        return SimpleNamespace(
            id="resp_1", status="completed", incomplete_details=None,
            model="gpt-6-luna-2026-09-01", output_text=json.dumps(_reply()),
            service_tier="default", usage=None,
        )

    updater._clients = _fake_clients(create)
    reply = updater.call(b"%PDF-1.4", "the context")

    assert tiers == ["flex", "default"]
    assert reply.service_tier == "default"


def test_a_standard_tier_call_that_fails_is_not_asked_again() -> None:
    updater = OpenAIScheduleUpdater(service_tier="default")
    tiers: list[str] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        tiers.append(kwargs["service_tier"])
        return SimpleNamespace(
            id="resp_1", status="failed", incomplete_details=None,
            error=SimpleNamespace(code="server_error", message="boom"),
            model="gpt-6-luna-2026-09-01", output_text="", service_tier="default", usage=None,
        )

    updater._clients = _fake_clients(create)
    reply = updater.call(b"%PDF-1.4", "the context")

    assert tiers == ["default"]
    assert reply.text == ""


def test_an_update_call_falls_back_when_flex_times_out() -> None:
    updater = OpenAIScheduleUpdater()
    tiers: list[str] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        tiers.append(kwargs["service_tier"])
        if kwargs["service_tier"] == "flex":
            raise APITimeoutError(request=_api_request())
        return _completed("default")

    updater._clients = _fake_clients(create)
    reply = updater.call(b"%PDF-1.4", "the context")

    assert tiers == ["flex", "default"]
    assert reply.service_tier == "default"


def test_an_update_call_out_of_quota_is_not_asked_at_the_standard_tier() -> None:
    updater = OpenAIScheduleUpdater()
    tiers: list[str] = []

    def create(**kwargs: Any) -> SimpleNamespace:
        tiers.append(kwargs["service_tier"])
        raise RateLimitError(
            "You exceeded your current quota",
            response=httpx.Response(429, request=_api_request()),
            body={"code": "insufficient_quota", "message": "You exceeded your current quota"},
        )

    updater._clients = _fake_clients(create)
    with pytest.raises(RateLimitError):
        updater.call(b"%PDF-1.4", "the context")
    assert tiers == ["flex"]


def test_an_update_call_failing_at_both_tiers_says_flex_failed_first() -> None:
    updater = OpenAIScheduleUpdater()

    def create(**kwargs: Any) -> SimpleNamespace:
        raise InternalServerError(
            f"{kwargs['service_tier']} down",
            response=httpx.Response(500, request=_api_request()), body=None,
        )

    updater._clients = _fake_clients(create)
    with pytest.raises(InternalServerError, match="default down") as raised:
        updater.call(b"%PDF-1.4", "the context")
    [note] = raised.value.__notes__
    assert "flex failed: InternalServerError: flex down" in note


def test_an_update_call_takes_the_tier_asked_when_the_response_has_none() -> None:
    updater = OpenAIScheduleUpdater()
    updater._clients = _fake_clients(lambda **kwargs: _completed(None))
    assert updater.call(b"%PDF-1.4", "the context").service_tier == "flex"


def test_flex_calls_retry_less_and_wait_longer_than_standard_ones(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    updater = OpenAIScheduleUpdater()
    flex, default = updater._openai("flex"), updater._openai("default")
    assert (flex.max_retries, flex.timeout) == (2, 900.0)
    assert (default.max_retries, default.timeout) == (5, 600.0)
    assert updater._openai("flex") is flex


def test_update_policy_carries_the_eval_policy_rules() -> None:
    for rule in (
        "A parish adoration chapel belongs to the church it is at.",
        "Write an exclusion as the weeks that remain",
        "A clock time stated in the bulletin always wins.",
        "Keep church-specific schedule headings separate",
        "Apply the off-site rules to Mass-intentions entries too",
    ):
        assert rule in POLICY


# ── Report and labeler ──────────────────────────────────────────────────────
def test_the_report_has_a_section_for_update_mode_parishes(
    conn: sqlite3.Connection, tmp_path: Path,
) -> None:
    _seed(conn, [SUN_9, SAT_5])
    ids = _ids(conn)
    before = tmp_path / "before.db"
    conn.execute(f"VACUUM INTO '{before}'")
    with conn:
        start_run(conn, "run-1", git_sha=None, trigger="test")
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(
        changes=[
            {"op": "delete", "entry_id": ids["mass Saturday 1020"], "page_number": 1,
             "rationale": "Vigil moved."},
            {"op": "add", "entry": {**SAT_5, "start_time": "4:30 PM"}, "page_number": 1,
             "rationale": "Vigil now 4:30."},
            {"op": "add", "entry": {**SUN_9, "church_slug": "nowhere"}, "page_number": 1,
             "rationale": "?"},
        ],
    )), "run-1")

    report = build_report(
        run_id="run-1", before_db=before, after_db=DEFAULT_DB_PATH, stages={},
        snapshot_verification=None,
    )

    assert diff_databases(before, DEFAULT_DB_PATH) == []
    section = report["update_mode"]
    [parish] = section["parishes"]
    assert parish["parish_slug"] == "test-parish"
    assert [c["op"] for c in parish["applied"]] == ["delete", "add"]
    assert parish["rejections"] == {UNKNOWN_CHURCH: 1}
    assert any("is undated" in flag for flag in parish["flags"])
    assert report["totals"]["update_changes_applied"] == 2
    markdown = render_markdown(report)
    assert "### Update-mode parishes" in markdown
    assert "replaced: Mass · Sat 5:00 PM → Mass · Sat 4:30 PM" in markdown


def test_the_report_lists_a_stale_call_in_full_and_flags_unprinted_entries(
    conn: sqlite3.Connection, tmp_path: Path,
) -> None:
    _seed(conn, [SUN_9, SAT_5], as_of="2026-09-01T00:00:00Z")
    sat5 = _ids(conn)["mass Saturday 1020"]
    replies = [
        _reply(published_date=f"2026-09-{day:02d}",
               seen=[{"entry_id": _ids(conn)["mass Sunday 540"], "page_number": 1}])
        for day in (6, 13, 20, 27)
    ]
    for i, day in enumerate((5, 12, 19, 26)):
        _bulletin(conn, f"w{i}", f"2026-09-{day:02d}T12:00:00Z")
    _bulletin(conn, "old", "2026-09-27T12:00:00Z")
    replies.append(_reply(published_date="2026-08-30", changes=[
        {"op": "delete", "entry_id": sat5, "page_number": 1, "rationale": "old issue"}]))
    with conn:
        start_run(conn, "run-1", git_sha=None, trigger="test")
    _run(conn, FakeUpdater(*replies), "run-1")

    report = build_report(
        run_id="run-1", before_db=DEFAULT_DB_PATH, after_db=DEFAULT_DB_PATH, stages={},
        snapshot_verification=None,
    )

    [rejected] = report["update_mode"]["rejected_calls"]
    assert rejected["reason"] == STALE_BULLETIN
    assert rejected["proposals"][0]["before"] == "Mass · Sat 5:00 PM"
    [parish] = report["update_mode"]["parishes"]
    assert any("none of the last 4 bulletins printed it" in f for f in parish["flags"])
    assert not any("Sun 9:00 AM" in f for f in parish["flags"])


def test_the_labeler_shows_the_view_with_the_applied_changes(conn: sqlite3.Connection) -> None:
    _seed(conn, [SUN_9, SAT_5])
    ids = _ids(conn)
    bulletin_id = _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(
        published_date="2026-10-11",
        seen=[{"entry_id": ids["mass Sunday 540"], "page_number": 2}],
        changes=[{"op": "modify", "entry_id": ids["mass Saturday 1020"],
                  "entry": {**SAT_5, "start_time": "4:30 PM"}, "page_number": 1,
                  "rationale": "x"}],
    )))

    source = load_gemini_source(
        conn, bulletin_id=bulletin_id, content_hash="b1", churches=[],
        published_date=None, processed_at=None,
    )

    assert source["source"]["kind"] == "update"
    assert source["published_date"] == "2026-10-11"
    rows = sorted((r["day_of_week"], r["start_time"], r["page_number"]) for r in source["events"])
    assert rows == [("Saturday", "16:30", 1), ("Sunday", "09:00", 2)]
    assert all(not r["problems"] for r in source["events"])


def test_the_schedule_command_seeds_shows_and_edits(
    conn: sqlite3.Connection, capsys: pytest.CaptureFixture[str], tmp_path: Path,
) -> None:
    from pdf_extract.__main__ import main

    seed_file = tmp_path / "seed.json"
    seed_file.write_text(json.dumps([SUN_9, SAT_5]), encoding="utf-8")
    assert main(["schedule", "seed", "--parish", "test-parish", "--file", str(seed_file),
                 "--actor", "luke"]) == 0
    capsys.readouterr()
    assert main(["schedule", "show", "--parish", "test-parish", "--date", "2026-10-10"]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["revision"] == 1
    assert len(shown["view"]["churches"][1]["entries"]) == 2
    assert main(["schedule", "add", "--parish", "test-parish", "--entry", json.dumps(SUN_11),
                 "--actor", "luke", "--note", "printed on p. 2"]) == 0
    assert main(["schedule", "add", "--parish", "test-parish", "--entry", json.dumps(SUN_11),
                 "--actor", "luke"]) == 1
    assert "duplicate" in capsys.readouterr().err
    assert main(["schedule", "rebuild"]) == 0
    assert json.loads(capsys.readouterr().out)["differing_rows"] == 0


# ── Review findings ─────────────────────────────────────────────────────────
def test_a_parish_can_be_removed_after_a_church_moved_into_it(
    conn: sqlite3.Connection,
) -> None:
    _seed(conn, [SUN_9, {**SUN_9, "church_slug": "second-church"}])
    second_id = _churches(conn)["second-church"]
    _write_reference([PARISH, OTHER_PARISH],
                     [CHURCH, {**SECOND, "parish_id": "other-parish"}, OTHER])
    ensure_db()
    _write_reference([PARISH], [CHURCH])

    stats = ensure_db()

    assert stats["parishes_deleted"] == 1
    row = conn.execute(
        "SELECT parish_id, retired_at FROM church WHERE id = ?", (second_id,),
    ).fetchone()
    assert (row["parish_id"], row["retired_at"] is not None) == (_parish_id(conn), True)
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    with conn:
        assert rebuild_current_schedule(conn)["differing_rows"] == 0


def test_a_malformed_lenient_reply_reads_as_empty() -> None:
    reply = parse_response(json.dumps({
        "seen": 5, "changes": True, "wrong_bulletin": "false",
        "church_list_needs_review": "true",
    }))
    assert (reply.status, reply.seen, reply.changes) == (LENIENT, [], [])
    assert (reply.wrong_bulletin, reply.church_list_needs_review) == (False, True)
    # seq is the position in the answer, counting a change that was dropped.
    reply = parse_response(json.dumps({"changes": [
        {"op": "rename"}, {"op": "delete", "entry_id": 5},
    ]}))
    assert [c.seq for c in reply.changes] == [2]


def test_a_copy_of_a_pdf_is_not_called_again_in_the_same_run(
    conn: sqlite3.Connection,
) -> None:
    _seed(conn, [SUN_9])
    for name, fetched in (("a", "2026-10-05T12:00:00Z"), ("b", "2026-10-06T12:00:00Z")):
        insert_bulletin(
            conn, parish_id=_parish_id(conn), source_url=f"https://example.org/{name}.pdf",
            content_hash="same-pdf", fetched_at=fetched,
        )
    stats = _run(conn, FakeUpdater(_reply()))
    assert stats["update_calls"] == 1


def test_a_seed_as_of_a_date_covers_that_whole_day(conn: sqlite3.Connection) -> None:
    _bulletin(conn, "that-day", "2026-10-04T12:00:00Z", published_date="2026-10-04",
              processed=True)
    _seed(conn, [SUN_9], as_of="2026-10-04")
    assert update_mode_parishes(conn) == {_parish_id(conn): "2026-10-04T23:59:59Z"}
    assert parish_history(conn, _parish_id(conn)).mark == date(2026, 10, 4)
    assert _run(conn, FakeUpdater())["update_calls"] == 0
    _seed(conn, [SUN_9], as_of="2026-10-05T08:00:00-04:00")
    assert update_mode_parishes(conn) == {_parish_id(conn): "2026-10-05T12:00:00Z"}


def test_the_first_call_for_the_seeds_week_is_a_correction(conn: sqlite3.Connection) -> None:
    _bulletin(conn, "seeded", "2026-10-03T12:00:00Z", published_date="2026-10-04",
              processed=True)
    _seed(conn, [SUN_9], as_of="2026-10-03T13:00:00Z")
    with conn:
        start_run(conn, "run-1", git_sha=None, trigger="test")
    _bulletin(conn, "fixed", "2026-10-04T12:00:00Z")
    _run(conn, FakeUpdater(_reply(published_date="2026-10-04")), "run-1")
    [result] = parish_results(conn, "run-1")
    assert result["status"] == "correction"


def test_a_call_can_only_change_entries_it_was_shown(conn: sqlite3.Connection) -> None:
    past = {**SUN_9, "event_kind": "specific_date", "date": "2026-10-04"}
    _seed(conn, [SUN_9, past])
    past_id = _ids(conn)["mass 2026-10-04 540"]
    _bulletin(conn, "b1", "2026-10-10T12:00:00Z")
    _run(conn, FakeUpdater(_reply(changes=[
        {"op": "delete", "entry_id": past_id, "page_number": 1, "rationale": "over"}])))
    assert [p[3:] for p in _proposals(conn)] == [(REJECTED, UNKNOWN_ITEM)]
    assert past_id in _ids(conn).values()


def test_hand_edits_need_an_update_mode_parish(conn: sqlite3.Connection) -> None:
    with pytest.raises(EditError, match="extract mode"):
        edit_entry(conn, _parish_id(conn), "add", entry=SUN_9, actor="luke")
