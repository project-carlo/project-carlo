"""Seeding believed schedules (docs/seeding-plan.md): seed files, the agent's tools,
the labeler's review and loading approved seeds."""

from __future__ import annotations

import copy
import http.client
import io
import json
import threading
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.__main__ import main
from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, bulletin_pdf_key, set_store
from pdf_extract.classifiers.seed_ask import GEMINI_MODEL, OPENAI_MODEL, SeedAsker
from pdf_extract.db import create_db, ensure_db
from pdf_extract.labeling.demo import build_demo, make_pdf
from pdf_extract.labeling.server import LabelerApp, make_server
from pdf_extract.report import render_seeds
from pdf_extract.schedule.store import (
    live_entries,
    parish_churches,
    rebuild_current_schedule,
    update_mode_parishes,
)
from pdf_extract.seeding import calls as seed_calls
from pdf_extract.seeding import cli as seed_cli
from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.coverage import diff, event_said, matches, missing_warning
from pdf_extract.seeding.files import (
    APPROVED,
    NEEDS_REVIEW,
    READY,
    SeedFileError,
    included_slots,
    read_seed,
    seed_digest,
    seed_path,
    validate_seed,
    write_seed_file,
)
from pdf_extract.seeding.finalize import finalize_seed
from pdf_extract.seeding.loader import is_loaded, load_approved_seeds
from pdf_extract.seeding.queries import (
    SeedContext,
    SeedError,
    brief,
    export_pdf,
    find_churches,
    grep_bulletins,
    history,
    list_bulletins,
    page_texts,
    parish_bulletins,
    recent_history,
    render_pages,
    resolve_bulletin,
    stored_pdfs,
)
from pdf_extract.seeding.review import (
    SeedReviewError,
    approve_seed,
    save_reviewed_seed,
    seed_detail,
    seed_queue,
)
from pdf_extract.seeding.slots import Draft
from pdf_extract.storage import connect_db

PARISH = "holy-family-demo"
HF = "holy-family-demo-rochester"
SJ = "st-joseph-demo-penfield"


@pytest.fixture
def demo(tmp_path: Path) -> dict[str, Path]:
    paths = build_demo(tmp_path / "demo")
    set_store(CachedBlobStore(LocalBlobStore(paths["root"])))
    return paths


@pytest.fixture
def conn(demo: dict[str, Path]):
    c = connect_db(demo["db_path"])
    yield c
    c.close()


@pytest.fixture
def seed(demo: dict[str, Path]) -> dict[str, Any]:
    loaded = read_seed(PARISH, demo["seeds_dir"])
    assert loaded is not None
    return loaded


def _slot(seed: dict[str, Any], slot_id: str) -> dict[str, Any]:
    return next(s for s in seed["slots"] if s["id"] == slot_id)


def _settle_all(seed: dict[str, Any], reviewer: str = "Reviewer") -> dict[str, Any]:
    """Answer every open question with the option the agent leaned to."""
    seed = copy.deepcopy(seed)
    for slot in seed["slots"]:
        if slot["status"] != "needs_human":
            continue
        index = next(i for i, o in enumerate(slot["options"]) if o.get("leaning"))
        option = slot["options"][index]
        slot.update(status="settled", decision="include" if option["entry"] else "exclude",
                    entry=option["entry"] or slot["entry"],
                    answer={"choice": index, "by": reviewer, "at": "2026-10-10T12:00:00Z"})
    seed["status"] = READY
    return seed


def _approved(seed: dict[str, Any]) -> dict[str, Any]:
    seed = _settle_all(seed)
    seed.update(status=APPROVED, reviewer="Reviewer", approved_at="2026-10-10T12:05:00Z")
    return seed


# ── The file ────────────────────────────────────────────────────────────────
def test_the_demo_draft_is_a_valid_seed(conn, seed):
    assert validate_seed(seed, parish_slug=PARISH) == []
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    assert seed["status"] == NEEDS_REVIEW
    assert len(included_slots(seed)) == 14


@pytest.mark.parametrize("change, message", [
    (lambda s: s.pop("summary"), "missing summary"),
    (lambda s: s.update(status="done"), "status must be one of"),
    (lambda s: _slot(s, "s16").update(options=None), "at least two options"),
    (lambda s: _slot(s, "s16")["options"][1].update(leaning=True), "exactly one option"),
    (lambda s: _slot(s, "s16").update(question=""), "question is required"),
    (lambda s: _slot(s, "s1").update(rationale=" "), "rationale is required"),
    (lambda s: _slot(s, "s1").update(sources=[]), "at least one source"),
    (lambda s: _slot(s, "s1")["sources"][0].update(bulletin="deadbeef"),
     "must name one of the file's bulletins"),
    (lambda s: _slot(s, "s1")["sources"][0].update(source="c9"), "agent, history, website or a call"),
    (lambda s: _slot(s, "s1")["entry"].update(start_time="4:00 PM"), "HH:MM"),
    (lambda s: _slot(s, "s1")["entry"].pop("note"), "missing note"),
    (lambda s: _slot(s, "s1").update(decision=None), "include or exclude for a settled"),
    (lambda s: _slot(s, "s1").update(entry=None), "required for an included slot"),
    (lambda s: _slot(s, "s2").update(id="s1"), "used twice"),
    (lambda s: s.update(status=READY), "questions are still open"),
    (lambda s: s.update(status=APPROVED), "questions are still open"),
    (lambda s: s.update(status="blocked"), "blocked_reason"),
    (lambda s: s.update(as_of=None), "as_of is required"),
    (lambda s: s.update(summary=" "), "summary is required"),
    (lambda s: _slot(s, "s1")["sources"].append({"source": "website", "said": "Sat 4 PM"}),
     "url is required for a website source"),
    (lambda s: _slot(s, "s1")["sources"][0].update(url="https://example.org"),
     "url is only for a website source"),
])
def test_validate_seed_rejects_malformed_files(seed, change, message):
    change(seed)
    errors = validate_seed(seed, parish_slug=PARISH)
    assert any(message in e for e in errors), errors


def test_a_website_source_cites_the_page_read(seed):
    _slot(seed, "s1")["sources"].append(
        {"source": "website", "url": "https://example.org/mass-times", "said": "Sat 4 PM"})
    assert validate_seed(seed, parish_slug=PARISH) == []


def test_a_slot_left_out_needs_no_entry(conn, seed):
    # A chapel open only by arrangement has no time to record, only the call.
    _slot(seed, "s1").update(decision="exclude", entry=None)
    assert validate_seed(seed, parish_slug=PARISH) == []
    assert check_seed(conn, seed, parish_slug=PARISH) == []


def test_a_ready_file_must_have_no_open_question_and_an_approval_needs_a_reviewer(seed):
    ready = _settle_all(seed)
    assert validate_seed(ready) == []
    ready["status"] = NEEDS_REVIEW
    assert any("no question is open" in e for e in validate_seed(ready))
    ready.update(status=APPROVED)
    assert any("reviewer" in e for e in validate_seed(ready))


def test_seed_path_refuses_unsafe_slugs(tmp_path: Path):
    with pytest.raises(SeedFileError):
        seed_path("../escape", tmp_path)
    with pytest.raises(SeedFileError):
        seed_path("Bad Slug", tmp_path)
    assert seed_path("st-mary", tmp_path) == (tmp_path / "st-mary.json").resolve()


def test_digest_covers_entries_pages_and_as_of_only(seed):
    digest = seed_digest(seed)
    edited = copy.deepcopy(seed)
    _slot(edited, "s1")["rationale"] = "Reworded."
    edited["summary"] = "Reworded too."
    assert seed_digest(edited) == digest
    _slot(edited, "s1")["page"] = 3
    assert seed_digest(edited) != digest
    moved = copy.deepcopy(seed)
    moved["as_of"] = "2026-09-25T22:00:00Z"
    assert seed_digest(moved) != digest


# ── Finalizing a draft ──────────────────────────────────────────────────────
_ENTRY_DEFAULTED = ("event_kind", "day_of_week", "date", "end_time", "cancelled",
                    "weeks_of_month", "season", "note")


def _bare(entry: dict[str, Any] | None) -> dict[str, Any] | None:
    """`entry` as an agent may write it: only the keys that say something."""
    if entry is None:
        return None
    return {k: v for k, v in entry.items()
            if k not in _ENTRY_DEFAULTED or v not in (None, False, [], "weekly")}


def test_finalize_does_the_bookkeeping_of_a_bare_draft(conn, seed):
    bare = copy.deepcopy(seed)
    bare.update(status="drafting", as_of=None)
    for b in bare["bulletins"]:
        b["read"] = False
    for slot in bare["slots"]:
        for key in ("page", "question", "options", "answer"):
            if slot[key] is None:
                del slot[key]
        slot["entry"] = _bare(slot["entry"])
        if slot["entry"] is None:
            del slot["entry"]
        for option in slot.get("options") or []:
            option["entry"] = _bare(option["entry"])
            if not option.get("leaning"):
                option.pop("leaning", None)
        if slot.get("entry") and slot["entry"].get("event_kind") == "specific_date":
            slot["entry"]["event_kind"] = "dated"
    del bare["slots"][0]["id"], bare["slots"][0]["status"]
    finalized = finalize_seed(bare, [HF, SJ])
    assert finalized == seed
    assert check_seed(conn, finalized, parish_slug=PARISH) == []


def test_finalize_names_the_one_church_and_settles_status(seed):
    seed["slots"] = [s for s in seed["slots"] if s["status"] != "needs_human"]
    seed["slots"][0]["entry"].pop("church_slug")
    finalized = finalize_seed(seed, [HF])
    assert finalized["slots"][0]["entry"]["church_slug"] == HF
    assert finalized["status"] == READY
    assert finalize_seed({**seed, "status": "blocked"}, [HF])["status"] == "blocked"
    approved = {**seed, "status": APPROVED, "as_of": None}
    assert finalize_seed(approved, [HF]) == approved
    misshapen = {"s1": seed["slots"][0]}
    assert finalize_seed({**seed, "slots": misshapen}, [HF])["slots"] == misshapen


def test_finalize_splits_a_source_citing_several_bulletins(conn, seed):
    new, old = (b["content_hash"] for b in seed["bulletins"])
    s1 = _slot(seed, "s1")
    expected = copy.deepcopy(s1["sources"][:2])
    for source in expected:
        source["said"] = "Saturday Vigil: 4:00 PM"
    s1["sources"][:2] = [{"source": "agent", "bulletins": [new[:8], old[:10]], "page": 2,
                          "said": "Saturday Vigil: 4:00 PM"}]
    assert any("drafting shorthand" in e for e in validate_seed(seed, parish_slug=PARISH))
    for b in seed["bulletins"]:
        b["read"] = False
    finalized = finalize_seed(seed, [HF, SJ])
    sources = _slot(finalized, "s1")["sources"]
    assert [s["bulletin"] for s in sources[:2]] == [new[:8], old[:10]]
    assert [{**s, "bulletin": None} for s in sources[:2]] == [
        {**s, "bulletin": None} for s in expected]
    assert all(b["read"] for b in finalized["bulletins"])
    assert check_seed(conn, finalized, parish_slug=PARISH) == []


def _without_history(seed: dict[str, Any]) -> dict[str, Any]:
    seed = copy.deepcopy(seed)
    for slot in seed["slots"]:
        slot["sources"] = [s for s in slot["sources"] if s["source"] != "history"]
    return seed


def test_finalize_attaches_the_history_that_matches_each_slot_once(conn, seed):
    new, old = (b["content_hash"] for b in seed["bulletins"])
    past = recent_history(conn, PARISH)
    assert [b["content_hash"] for b in past] == [new, old]
    bare = _without_history(seed)
    bare["slots"][15]["sources"].append(seed["slots"][15]["sources"][2])  # the drafter's own
    finalized = finalize_seed(bare, [HF, SJ], past)

    def cited(slot_id: str) -> list[tuple[str, str]]:
        return [(s["bulletin"][:8], s["said"]) for s in _slot(finalized, slot_id)["sources"]
                if s["source"] == "history"]

    assert cited("s1") == [(new[:8], f"weekly mass Saturday 16:00 {HF}"),
                           (old[:8], f"weekly mass Saturday 16:00 {HF}")]
    assert cited("s9") == [(new[:8], f"specific_date mass 2026-10-02 19:00 {SJ}  "
                                     "“Feast of the Guardian Angels”")]
    # s16's option is a weekly Monday Mass; the drafter already cited the older bulletin.
    assert cited("s16") == [(old[:8], "no weekday Masses stored"),
                            (new[:8], f"weekly mass Monday 08:00 {HF}")]
    assert cited("s11") == []  # a Saturday 9:00 AM "Mass" history never had
    assert finalize_seed(finalized, [HF, SJ], past) == finalized
    assert check_seed(conn, finalized, parish_slug=PARISH) == []


_SUNDAY = {"church_slug": HF, "event_type": "mass", "event_kind": "weekly",
           "day_of_week": "Sunday", "date": None, "start_time": "09:00"}
_DATED = {**_SUNDAY, "event_kind": "specific_date", "day_of_week": None, "date": "2026-10-04"}


@pytest.mark.parametrize("entry, event, matched", [
    (_SUNDAY, _SUNDAY, True),
    ({**_SUNDAY, "church_slug": None}, _SUNDAY, True),  # a draft not finalized yet
    ({**_SUNDAY, "weeks_of_month": ["first"], "end_time": "10:00"}, _SUNDAY, True),
    ({**_SUNDAY, "church_slug": SJ}, _SUNDAY, False),
    ({**_SUNDAY, "event_type": "confession"}, _SUNDAY, False),
    ({**_SUNDAY, "start_time": "09:30"}, _SUNDAY, False),
    ({**_SUNDAY, "day_of_week": "Saturday"}, _SUNDAY, False),
    (_DATED, _SUNDAY, False),
    (_DATED, _DATED, True),
    ({**_DATED, "date": "2026-10-11"}, _DATED, False),
    (_SUNDAY, _DATED, True),  # October 4, 2026 is a Sunday: the weekly slot that week
    (_SUNDAY, {**_DATED, "cancelled": True}, False),  # calling it off is news
    ({**_DATED, "cancelled": True}, {**_DATED, "cancelled": True}, True),
])
def test_history_matches_a_slot_by_type_day_or_date_time_and_church(entry, event, matched):
    assert matches(entry, event) is matched


def test_an_event_says_its_weeks_and_whether_they_are_skipped():
    assert event_said({**_SUNDAY, "weeks_of_month": ["first", "third"]}).endswith("weeks first/third")
    assert event_said(
        {**_SUNDAY, "weeks_of_month": ["last"], "exclude_weeks": True},
    ).endswith("weeks except last")


def _history_of(*events: dict[str, Any], short: str = "aaaaaaaaaaaa") -> dict[str, Any]:
    return {"short": short, "content_hash": short + "0" * 52, "wrong_bulletin": False,
            "events": [{"end_time": None, "cancelled": False, "page_number": 2, "note": None,
                        **ev} for ev in events]}


def test_diff_lists_what_history_and_the_seed_disagree_on(seed):
    _slot(seed, "s3")["entry"]["start_time"] = "11:00"
    seed["slots"] = [s for s in seed["slots"] if s["id"] != "s4"]
    past = [
        _history_of({**_SUNDAY, "start_time": "10:30"},  # s3 says 11:00 now
                    {**_SUNDAY, "church_slug": SJ},  # s4 is gone
                    {**_SUNDAY, "event_type": "confession"},  # never in the seed
                    {**_DATED, "date": "2026-09-20"},  # before as_of: outside a seed
                    {**_DATED, "date": "2026-10-05", "start_time": "08:00", "cancelled": True}),
        _history_of({**_SUNDAY, "church_slug": SJ}, short="bbbbbbbbbbbb"),
        {**_history_of({**_SUNDAY, "start_time": "07:00"}, short="cccccccccccc"),
         "wrong_bulletin": True},
    ]
    found = diff(seed, past)
    assert found["bulletins"] == ["aaaaaaaaaaaa", "bbbbbbbbbbbb"]
    assert found["scope_date"] == "2026-09-25"
    assert {row["said"]: row["bulletins"] for row in found["missing"]} == {
        f"weekly mass Sunday 10:30 {HF}": ["aaaaaaaaaaaa"],
        f"weekly mass Sunday 09:00 {SJ}": ["aaaaaaaaaaaa", "bbbbbbbbbbbb"],
        f"weekly confession Sunday 09:00 {HF}": ["aaaaaaaaaaaa"],
    }
    # History here has only s10, the dated cancellation, of the seed's included slots.
    assert {u["slot"] for u in found["unseen"]} == {
        s["id"] for s in included_slots(seed)} - {"s10"}
    assert missing_warning(found["missing"][1], 2) == (
        f"history has weekly mass Sunday 09:00 {SJ} (2 of 2 bulletins, p2) and no slot or "
        "option covers it")


def test_diff_leaves_out_a_cancellation_of_a_weekly_slot_left_out(seed):
    # s11, a Saturday 9:00 AM "Mass", is left out; October 3 is a Saturday.
    cancelled = {**_DATED, "date": "2026-10-03", "cancelled": True}
    assert diff(seed, [_history_of(cancelled)])["missing"] == []
    _slot(seed, "s11")["decision"] = "include"
    assert len(diff(seed, [_history_of(cancelled)])["missing"]) == 1


def test_diff_with_the_demo_history(conn, seed):
    found = diff(seed, recent_history(conn, PARISH))
    assert found["missing"] == [] and found["unseen"] == []
    seed["slots"] = [s for s in seed["slots"] if s["id"] != "s5"]
    found = diff(seed, recent_history(conn, PARISH, bulletins=1))
    assert found["missing"] == []  # only the older bulletin has the Wednesday Spanish Mass
    found = diff(seed, recent_history(conn, PARISH))
    assert [row["said"] for row in found["missing"]] == [
        f"weekly mass Wednesday 19:00 {SJ}  “Spanish”"]


# ── Checks against the database ─────────────────────────────────────────────
def test_check_finds_what_needs_the_database(conn, seed):
    bad = copy.deepcopy(seed)
    _slot(bad, "s2")["entry"]["start_time"] = "16:00"
    _slot(bad, "s2")["entry"]["day_of_week"] = "Saturday"  # s1's slot
    _slot(bad, "s3")["entry"]["church_slug"] = "st-anne-demo-fairport"
    _slot(bad, "s9")["entry"]["date"] = "2026-09-20"
    problems = check_seed(conn, bad, parish_slug=PARISH)
    assert any("same slot as s1" in p for p in problems)
    assert any("unknown_church" in p for p in problems)
    assert any("before as_of" in p for p in problems)


def _disjoint_friday_slots(seed):
    first = _slot(seed, "s1")
    first["entry"].update(event_type="adoration", day_of_week="Friday", start_time="11:30",
                          end_time="16:00", weeks_of_month=["first"], note="Benediction")
    remaining = copy.deepcopy(first)
    remaining["id"] = "s18"
    remaining["entry"].update(end_time="13:00",
                              weeks_of_month=["second", "third", "fourth", "fifth"])
    seed["slots"].append(remaining)
    return first, remaining


@pytest.mark.parametrize("overlap", [False, True])
def test_seed_and_draft_checks_allow_only_disjoint_recurrence_variants(conn, seed, overlap):
    seed = _settle_all(seed)
    _, remaining = _disjoint_friday_slots(seed)
    if overlap:
        remaining["entry"]["weeks_of_month"].append("first")
    problems = check_seed(conn, seed, parish_slug=PARISH, check_evidence=False)
    assert bool(problems) is overlap
    parish_id = conn.execute("SELECT id FROM parish WHERE slug=?", (PARISH,)).fetchone()[0]
    draft = Draft(seed, parish_churches(conn, parish_id), touched=["s18"])
    if overlap:
        assert any("same slot as s1" in p for p in problems)
        with pytest.raises(SeedError, match="s1 and s18 are the same slot"):
            draft.check()
    else:
        draft.check()


def test_check_requires_as_of_to_be_the_newest_bulletin_read(conn, seed):
    seed["as_of"] = seed["bulletins"][1]["fetched_at"]
    problems = check_seed(conn, seed, parish_slug=PARISH)
    assert any("newest bulletin read" in p for p in problems)


def test_check_reports_bulletins_the_database_lacks_and_drafts(conn, seed):
    older = seed["bulletins"][1]["content_hash"]
    seed = json.loads(json.dumps(seed).replace(older, "e" * 64))
    seed["status"] = "drafting"
    problems = check_seed(conn, seed, parish_slug=PARISH)
    assert any("not one of the parish's" in p for p in problems)
    assert any("still drafting" in p for p in problems)


# ── The agent's queries ─────────────────────────────────────────────────────
def test_bulletins_newest_first(conn):
    bulletins = parish_bulletins(conn, PARISH)
    assert [b["published_date"] for b in bulletins] == ["2026-09-27", "2026-09-20"]
    listed = list_bulletins(conn, PARISH)
    assert listed["bulletins"][0]["pages"] == 3
    assert listed["bulletins"][0]["stored"] is True
    assert listed["not_shown"] == 0


def test_a_bulletin_whose_pdf_is_gone_is_listed_but_not_read(conn, demo):
    older = parish_bulletins(conn, PARISH)[1]
    LocalBlobStore(demo["root"]).delete([bulletin_pdf_key(PARISH, older["content_hash"])])
    listed = list_bulletins(conn, PARISH)["bulletins"]
    assert listed[1]["stored"] is False and listed[1]["pages"] is None
    with pytest.raises(SeedError, match="no longer stored"):
        export_pdf(conn, PARISH, older["content_hash"][:8])


def test_stored_pdfs_lists_the_remote_and_the_local_cache_once(conn, demo, tmp_path):
    newest, older = parish_bulletins(conn, PARISH)
    local = LocalBlobStore(demo["root"])
    remote = LocalBlobStore(tmp_path / "remote")
    remote.put(bulletin_pdf_key(PARISH, newest["content_hash"]), b"%PDF")
    remote.put(bulletin_pdf_key("another-parish", "f" * 64), b"%PDF")
    local.delete([bulletin_pdf_key(PARISH, newest["content_hash"])])

    class NoLookups(CachedBlobStore):
        def exists(self, key: str) -> bool:
            raise AssertionError(f"looked up {key}")

    set_store(NoLookups(local, remote))
    # The newest is only in R2, the older only in the local cache (pruned from R2).
    assert stored_pdfs(PARISH) == {newest["content_hash"], older["content_hash"]}
    assert all(b["stored"] for b in list_bulletins(conn, PARISH)["bulletins"])


def test_resolve_bulletin_by_latest_or_prefix(conn):
    newest, older = parish_bulletins(conn, PARISH)
    assert resolve_bulletin(conn, PARISH, "latest")["content_hash"] == newest["content_hash"]
    assert resolve_bulletin(conn, PARISH, older["content_hash"][:8])["id"] == older["id"]
    with pytest.raises(SeedError, match="at least 6"):
        resolve_bulletin(conn, PARISH, "abc")
    with pytest.raises(SeedError, match="has no bulletin"):
        resolve_bulletin(conn, PARISH, "f" * 10)
    with pytest.raises(SeedError, match="Parish not found"):
        resolve_bulletin(conn, "no-such-parish", "latest")


def test_history_is_extract_modes_events_per_bulletin(conn):
    result = history(conn, PARISH)
    assert [b["published_date"] for b in result["bulletins"]] == ["2026-09-27", "2026-09-20"]
    vigil = result["bulletins"][1]["events"]
    assert {"church_slug": HF, "event_type": "mass", "day_of_week": "Saturday",
            "start_time": "16:00"}.items() <= next(
        e for e in vigil if e["day_of_week"] == "Saturday" and e["event_type"] == "mass").items()


def test_pdf_and_pages_are_written_for_the_agent(conn, tmp_path: Path):
    pdf = export_pdf(conn, PARISH, "latest", work_dir=tmp_path)
    assert Path(pdf["path"]).read_bytes().startswith(b"%PDF")
    assert pdf["pages"] == 3
    pages = render_pages(conn, PARISH, "latest", page=2, dpi=50, work_dir=tmp_path)
    assert len(pages["paths"]) == 1 and Path(pages["paths"][0]).read_bytes()[:4] == b"\x89PNG"
    with pytest.raises(SeedError, match="pages 1 to 3"):
        render_pages(conn, PARISH, "latest", page=9, work_dir=tmp_path)


def test_text_reads_each_page_and_marks_the_ones_that_are_only_images(conn):
    texts = page_texts(conn, PARISH, "latest")
    assert texts["pages"] == 3 and [p["page"] for p in texts["texts"]] == [1, 2, 3]
    assert any("Mass" in p["text"] and not p["image_only"] for p in texts["texts"])
    assert [p["page"] for p in page_texts(conn, PARISH, "latest", page=2)["texts"]] == [2]
    with pytest.raises(SeedError, match="pages 1 to 3"):
        page_texts(conn, PARISH, "latest", page=9)


def _grep_lines(result: dict[str, Any]) -> dict[str, list[str]]:
    """Each bulletin's matching lines, by its date, `>` marking a match."""
    return {
        b["published_date"]: [f"p{p['page']} {'>' if line['match'] else ' '} {line['text']}"
                              for p in b["pages"] for hunk in p["hunks"] for line in hunk]
        for b in result["bulletins"]
    }


def test_grep_finds_schedule_words_with_a_line_of_context(conn):
    found = grep_bulletins(conn, PARISH)
    assert [b["published_date"] for b in found["bulletins"]] == ["2026-09-27", "2026-09-20"]
    assert _grep_lines(found)["2026-09-20"] == [
        "p2 > MASS SCHEDULE",
        "p2   Holy Family: Saturday 4:00 PM; Sunday 8:00 AM, 10:30 AM; weekdays 8:00 AM",
        "p2   St. Joseph: Sunday 9:00 AM; Wednesday 7:00 PM (Spanish)",
        "p2 > CONFESSIONS",
        "p2   Holy Family: Saturday 3:00 - 3:45 PM",
    ]
    newest = _grep_lines(found)["2026-09-27"]
    assert newest[-5:] == [
        "p3   THIS WEEK AT THE PARISH",
        "p3 > Please note: the 8:00 AM Mass at Holy Family on Monday, October 5 is cancelled.",
        "p3 > Feast of the Guardian Angels: Mass at St. Joseph on Friday, October 2 at 7:00 PM.",
        "p3 > Parish picnic: Sunday, October 4 after the 10:30 AM Mass on the lawn.",
        "p3   Food pantry volunteers needed Saturdays from 9:00 to 11:00 AM.",
    ]
    for word in ("CONFESSION", "First Friday", "ADORATION", "Holy Hour", "Vigil"):
        assert any(word in line for line in newest if " > " in line), word


def test_grep_takes_a_pattern_and_flags_pages_that_are_only_images(conn, demo):
    found = grep_bulletins(conn, PARISH, "PICNIC|bible study")
    assert _grep_lines(found)["2026-09-27"] == [
        "p3   Feast of the Guardian Angels: Mass at St. Joseph on Friday, October 2 at 7:00 PM.",
        "p3 > Parish picnic: Sunday, October 4 after the 10:30 AM Mass on the lawn.",
        "p3   Food pantry volunteers needed Saturdays from 9:00 to 11:00 AM.",
        "p3 > Bible study meets Tuesdays at 10:00 AM in the parish hall.",
    ]
    assert _grep_lines(found)["2026-09-20"] == []
    assert len(grep_bulletins(conn, PARISH, "picnic", bulletins=1)["bulletins"]) == 1
    with pytest.raises(SeedError, match="regular expression"):
        grep_bulletins(conn, PARISH, "(unclosed")
    image = make_pdf([[(11, "")], [(11, "Masses: Saturday 4:00 PM and Sunday 8:00 AM, 10:30 AM")]])
    newest = parish_bulletins(conn, PARISH)[0]
    LocalBlobStore(demo["root"]).put(bulletin_pdf_key(PARISH, newest["content_hash"]), image)
    pages = grep_bulletins(conn, PARISH, bulletins=1)["bulletins"][0]["pages"]
    assert [(p["page"], p["image_only"], len(p["hunks"])) for p in pages] == [
        (1, True, 0), (2, False, 1)]


def test_church_looks_up_by_slug_name_town_or_address(conn):
    def found(query: str) -> list[str]:
        return [c["church"] for c in find_churches(conn, query)["churches"]]

    assert found("PENFIELD") == [SJ]
    assert found("st. joseph") == [SJ]
    assert found("9 church st") == ["st-anne-demo-fairport"]
    assert found("holy-family-demo") == [HF, SJ]  # the parish's slug
    assert found("nowhere") == []
    assert find_churches(conn, "oak ave")["churches"] == [{
        "church": SJ, "parish": PARISH, "name": "St. Joseph Church",
        "address": "45 Oak Ave, Penfield, NY 14526"}]
    with pytest.raises(SeedError, match="Name something"):
        find_churches(conn, " ")


def test_brief_is_where_a_draft_starts(conn, tmp_path):
    result = brief(conn, PARISH, work_dir=tmp_path)
    assert result["website"] == "https://example.org/holy-family"
    assert [c["church"] for c in result["churches"]] == [HF, SJ]
    assert result["churches"][0]["address"] == "123 Main St, Rochester, NY 14620"
    assert [b["published_date"] for b in result["bulletins"]["bulletins"]] == [
        "2026-09-27", "2026-09-20"]
    assert Path(result["pdf"]["path"]).read_bytes().startswith(b"%PDF")
    seen = {(h["event"]["day_of_week"] or h["event"]["date"], h["event"]["start_time"],
             h["event"]["church_slug"]): h["bulletins"] for h in result["history"]}
    assert seen[("Saturday", "16:00", HF)] == 2 and seen[("Monday", "08:00", HF)] == 1
    assert ("2026-10-05", "08:00", HF) in seen  # dated after the newest bulletin's fetch
    our_lady = brief(conn, "our-lady-demo", work_dir=tmp_path)
    assert our_lady["history"] == [] and "path" in our_lady["pdf"]


# ── External calls ──────────────────────────────────────────────────────────
class _FakeClassifier:
    name = "fake-extract"
    version = "fake-model+prompt-0"
    calls = 0

    def extract(self, pdf_bytes, *, churches, today):
        type(self).calls += 1
        return {"events": [{"church_slug": HF, "type": "mass", "kind": "weekly",
                            "day_of_week": "Sunday", "start_time": "8:00 AM"}],
                "published_date": "2026-09-27", "wrong_bulletin": False,
                "usage": {"input_tokens": 1000, "output_tokens": 100}}


def test_extract_is_cached_recorded_and_limited(conn, demo, monkeypatch):
    _FakeClassifier.calls = 0
    monkeypatch.setattr(seed_calls, "extraction_classifier", lambda model: _FakeClassifier())
    monkeypatch.setenv("CARLO_SEED_CALL_LIMIT", "1")
    ctx = SeedContext(seeds_dir=demo["seeds_dir"])
    first = seed_calls.run_extract(conn, ctx, PARISH, "latest", OPENAI_MODEL)
    again = seed_calls.run_extract(conn, ctx, PARISH, "latest", OPENAI_MODEL)
    assert _FakeClassifier.calls == 1
    assert (first["cached"], again["cached"]) == (False, True)
    assert first["events"][0]["start_time"] == "08:00"
    assert [c["id"] for c in read_seed(PARISH, demo["seeds_dir"])["calls"]] == ["c1", "c2"]
    older = parish_bulletins(conn, PARISH)[1]["content_hash"][:8]
    with pytest.raises(SeedError, match="used its 1 external calls"):
        seed_calls.run_extract(conn, ctx, PARISH, older, OPENAI_MODEL)
    assert validate_seed(read_seed(PARISH, demo["seeds_dir"])) == []


def test_ask_answers_with_a_page_and_quote_and_starts_a_file(conn, demo, monkeypatch):
    asked = []

    def fake_ask(self, pdf, *, churches, today, question):
        asked.append((self.model, today.isoformat(), question))
        return {"answer": "3:00-3:45 PM", "page": 2, "quote": "Saturday 3:00 - 3:45 PM",
                "usage": {"prompt_tokens": 2000, "output_tokens": 50}}

    monkeypatch.setattr(SeedAsker, "ask", fake_ask)
    ctx = SeedContext(seeds_dir=demo["root"] / "fresh-seeds")
    call = seed_calls.run_ask(conn, ctx, "st-anne-demo", "latest", GEMINI_MODEL,
                              "When are Saturday confessions?")
    assert call["answer"] == "3:00-3:45 PM" and call["page"] == 2 and not call["cached"]
    assert call["cost_usd"] is not None
    again = seed_calls.run_ask(conn, ctx, "st-anne-demo", "latest", GEMINI_MODEL,
                               "When are Saturday confessions?")
    assert again["cached"] and len(asked) == 1
    assert asked[0] == (GEMINI_MODEL, "2026-09-25", "When are Saturday confessions?")
    started = read_seed("st-anne-demo", ctx.seeds_dir)
    assert started["status"] == "drafting" and len(started["calls"]) == 2
    with pytest.raises(SeedError, match="must be one of"):
        seed_calls.run_ask(conn, ctx, "st-anne-demo", "latest", "gpt-4", "Q?")


# ── Review ──────────────────────────────────────────────────────────────────
def test_review_answers_then_approves(conn, demo, seed):
    with pytest.raises(SeedReviewError, match="questions are still open"):
        save_reviewed_seed(conn, PARISH, {**seed, "status": APPROVED, "reviewer": "R"},
                           demo["seeds_dir"])
    settled = _settle_all(seed)
    settled["calls"] = [{"id": "c1", "forged": True}]  # not the reviewer's to change
    detail = save_reviewed_seed(conn, PARISH, settled, demo["seeds_dir"])
    assert detail["seed"]["status"] == READY and detail["seed"]["calls"] == []
    with pytest.raises(SeedReviewError, match="reviewer"):
        save_reviewed_seed(conn, PARISH, {**settled, "status": APPROVED, "reviewer": " "},
                           demo["seeds_dir"])
    approved = save_reviewed_seed(conn, PARISH, {**settled, "status": APPROVED,
                                                 "reviewer": "Reviewer"}, demo["seeds_dir"])
    assert approved["seed"]["approved_at"] and approved["problems"] == []
    queue = seed_queue(conn, demo["seeds_dir"])
    assert queue[0]["status"] == APPROVED and queue[0]["open_questions"] == 0


def test_review_refuses_a_draft_still_being_written(conn, demo, seed):
    seed["status"] = "drafting"
    write_seed_file(seed, demo["seeds_dir"])
    with pytest.raises(SeedReviewError, match="still drafting"):
        save_reviewed_seed(conn, PARISH, {**seed, "status": NEEDS_REVIEW}, demo["seeds_dir"])


AGENT = "agent:seed-review@abc1234"


def _weekday_group(seed: dict[str, Any]) -> list[str]:
    """Make the Monday to Friday 8:00 AM Masses one grouped question, each its own day."""
    s16 = _slot(seed, "s16")
    ids = ["s12", "s13", "s14", "s15", "s16"]
    for slot_id in ids:
        slot = _slot(seed, slot_id)
        entry = slot["entry"] or s16["options"][0]["entry"]
        slot.update(status="needs_human", decision=None, entry=None, group="weekday",
                    question="Are the weekday 8:00 AM Masses weekly?", options=[
                        {"label": "Weekly, 8:00 AM", "entry": entry, "leaning": True},
                        {"label": "Leave out", "entry": None}])
    return ids


def test_agent_approval_answers_as_seeds_mode_does_and_changes_nothing_else(conn, demo, seed):
    before = copy.deepcopy(seed)
    result = approve_seed(conn, PARISH, AGENT, [
        {"slot": "s16", "choice": 0, "question": "…", "basis": "rule", "why": "R35"},
        {"slot": "s17", "choice": "dropped"},
    ], demo["seeds_dir"])
    assert result["status"] == APPROVED and result["reviewer"] == AGENT
    assert result["answered"] == [{"slots": ["s16"], "choice": 0, "decision": "include"},
                                  {"slots": ["s17"], "choice": "dropped", "decision": "exclude"}]
    saved = read_seed(PARISH, demo["seeds_dir"])
    assert saved["approved_at"] == result["approved_at"] and saved["reviewer"] == AGENT
    s16, s17 = _slot(saved, "s16"), _slot(saved, "s17")
    assert (s16["status"], s16["decision"]) == ("settled", "include")
    assert s16["entry"] == _slot(before, "s16")["options"][0]["entry"]
    # Dropped keeps the leaning option's entry for review, as the labeler does.
    assert (s17["status"], s17["decision"]) == ("settled", "exclude")
    assert s17["entry"] == _slot(before, "s17")["options"][0]["entry"]
    for slot in (s16, s17):
        assert slot["answer"]["by"] == AGENT and slot["answer"]["at"].endswith("Z")
        assert slot["question"] and slot["options"]  # kept, as in the labeler
    unchanged = {"status", "reviewer", "approved_at", "slots"}
    assert {k: v for k, v in saved.items() if k not in unchanged} == \
        {k: v for k, v in before.items() if k not in unchanged}
    assert [s for s in saved["slots"] if s["id"] not in ("s16", "s17")] == \
        [s for s in before["slots"] if s["id"] not in ("s16", "s17")]
    assert check_seed(conn, saved, parish_slug=PARISH) == []


def test_agent_approval_settles_an_edited_slot_with_its_entry_and_page(conn, demo, seed):
    entry = {**_slot(seed, "s17")["options"][1]["entry"], "start_time": "18:30"}
    approve_seed(conn, PARISH, AGENT, [
        {"slot": "s16", "choice": 1},
        {"slot": "s17", "choice": "edited", "entry": entry, "page": 2},
    ], demo["seeds_dir"])
    saved = read_seed(PARISH, demo["seeds_dir"])
    s16, s17 = _slot(saved, "s16"), _slot(saved, "s17")
    assert (s16["decision"], s16["answer"]["choice"]) == ("exclude", 1)
    assert s16["entry"] == _slot(seed, "s16")["options"][0]["entry"]
    assert (s17["status"], s17["decision"], s17["entry"], s17["page"]) == (
        "settled", "include", entry, 2)
    assert s17["answer"]["choice"] == "edited"


def test_agent_approval_answers_a_whole_group_with_one_answer(conn, demo, seed):
    ids = _weekday_group(seed)
    write_seed_file(seed, demo["seeds_dir"])
    with pytest.raises(SeedReviewError, match="option 2 can't settle s12, s13, s14, s15, s16"):
        approve_seed(conn, PARISH, AGENT, [{"slot": "s16", "choice": 2}], demo["seeds_dir"])
    with pytest.raises(SeedReviewError, match="s12 is already answered"):
        approve_seed(conn, PARISH, AGENT, [{"slot": "s16", "choice": 0},
                                           {"slot": "s12", "choice": 1}], demo["seeds_dir"])
    # Listing each slot of the group with the group's answer is the same as listing one.
    result = approve_seed(conn, PARISH, AGENT, [
        {"slot": "s14", "choice": 0}, {"slot": "s16", "choice": 0},
        {"slot": "s17", "choice": 0},
    ], demo["seeds_dir"])
    assert result["answered"][0] == {"slots": ids, "choice": 0, "decision": "include"}
    saved = read_seed(PARISH, demo["seeds_dir"])
    assert all(_slot(saved, i)["decision"] == "include" and _slot(saved, i)["answer"]["by"]
               == AGENT for i in ids)
    assert [_slot(saved, i)["entry"]["day_of_week"] for i in ids] == [
        "Tuesday", "Wednesday", "Thursday", "Friday", "Monday"]


@pytest.mark.parametrize("answers, message", [
    ([{"slot": "s16", "choice": 0}], "1 slots are still open: s17"),
    ([], "2 slots are still open: s16, s17"),
    ([{"slot": "s99", "choice": 0}], "no slot s99"),
    ([{"slot": "s1", "choice": 0}], "s1 is not an open question"),
    ([{"slot": "s16", "choice": "maybe"}], "choice must be an option's index"),
    ([{"slot": "s16", "choice": True}], "choice must be an option's index"),
    ([{"slot": "s16", "choice": "edited"}], "an edited answer gives its entry"),
    ([{"slot": "s16", "choice": 0, "page": 2}], "only an edited answer"),
    ([{"choice": 0}], "Answer 1 must be an object with a slot and a choice"),
    ({"slot": "s16", "choice": 0}, "a list of"),
])
def test_agent_approval_refuses_answers_that_leave_it_unsettled(conn, demo, seed, answers,
                                                                 message):
    before = seed_path(PARISH, demo["seeds_dir"]).read_bytes()
    with pytest.raises(SeedReviewError, match=message):
        approve_seed(conn, PARISH, AGENT, answers, demo["seeds_dir"])
    assert seed_path(PARISH, demo["seeds_dir"]).read_bytes() == before


@pytest.mark.parametrize("reviewer", ["Reviewer", "agent:", "agent:  ", " agent:x", "", None])
def test_agent_approval_needs_an_agent_reviewer(conn, demo, seed, reviewer):
    with pytest.raises(SeedReviewError, match="people approve in the labeler"):
        approve_seed(conn, PARISH, reviewer, [], demo["seeds_dir"])


@pytest.mark.parametrize("status, message", [
    ("drafting", "still drafting"), ("approved", "Already approved by Reviewer"),
    ("blocked", "a person decides on a blocked parish"), (None, "No seed file"),
])
def test_agent_approval_refuses_drafts_approved_blocked_and_missing_files(
    conn, demo, seed, status, message,
):
    if status is None:
        seed_path(PARISH, demo["seeds_dir"]).unlink()
    else:
        changed = _approved(seed) if status == APPROVED else {**seed, "status": status}
        if status == "blocked":
            changed["blocked_reason"] = "no bulletin since June"
        write_seed_file(changed, demo["seeds_dir"])
    with pytest.raises(SeedReviewError, match=message):
        approve_seed(conn, PARISH, AGENT, [], demo["seeds_dir"])


def test_agent_approval_of_a_ready_file_needs_no_answers(conn, demo, seed):
    write_seed_file(_settle_all(seed), demo["seeds_dir"])
    result = approve_seed(conn, PARISH, AGENT, [], demo["seeds_dir"])
    assert result["answered"] == [] and result["status"] == APPROVED
    # The person's earlier answers stay theirs.
    assert _slot(read_seed(PARISH, demo["seeds_dir"]), "s16")["answer"]["by"] == "Reviewer"


# ── Loading ─────────────────────────────────────────────────────────────────
def test_approved_disjoint_patterns_load_without_changing_reviewer_decisions(conn, demo, seed):
    approved = _approved(seed)
    first, _ = _disjoint_friday_slots(approved)
    first["options"] = [
        {"label": "First Fridays", "entry": copy.deepcopy(first["entry"]), "leaning": True},
        {"label": "Leave out", "entry": None},
    ]
    first["answer"] = {"choice": 0, "by": "Reviewer", "at": "2026-10-10T12:00:00Z"}
    path = write_seed_file(approved, demo["seeds_dir"])
    before = path.read_bytes()
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert result["skipped"] == []
    assert result["loaded"][0]["entries"] == len(included_slots(approved))
    parish_id = conn.execute("SELECT id FROM parish WHERE slug=?", (PARISH,)).fetchone()[0]
    friday = [e for e in live_entries(conn, parish_id).values()
              if e.event_type == "adoration" and e.start_time == 690]
    assert {(e.weeks_of_month, e.end_time) for e in friday} == {(1, 960), (30, 780)}
    assert path.read_bytes() == before
    assert rebuild_current_schedule(conn)["differing_rows"] == 0
    assert load_approved_seeds(conn, demo["seeds_dir"]) == {"loaded": [], "skipped": []}


def test_an_approved_seed_loads_once_and_switches_the_parish(conn, demo, seed):
    assert load_approved_seeds(conn, demo["seeds_dir"]) == {"loaded": [], "skipped": []}
    approved = _approved(seed)
    write_seed_file(approved, demo["seeds_dir"])
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert [r["parish"] for r in result["loaded"]] == [PARISH]
    parish_id = conn.execute("SELECT id FROM parish WHERE slug = ?", (PARISH,)).fetchone()[0]
    assert update_mode_parishes(conn)[parish_id] == "2026-09-25T21:00:00Z"
    assert len(live_entries(conn, parish_id)) == len(included_slots(approved)) == 16
    newest = parish_bulletins(conn, PARISH)[0]
    sightings = conn.execute(
        "SELECT COUNT(*) FROM entry_sighting WHERE bulletin_id = ?", (newest["id"],),
    ).fetchone()[0]
    assert sightings == 16
    assert is_loaded(conn, parish_id, approved)
    assert load_approved_seeds(conn, demo["seeds_dir"]) == {"loaded": [], "skipped": []}

    # A change with the same as_of would undo update mode's changes: skipped.
    changed = copy.deepcopy(approved)
    _slot(changed, "s1")["entry"]["note"] = None
    write_seed_file(changed, demo["seeds_dir"])
    skipped = load_approved_seeds(conn, demo["seeds_dir"])
    assert skipped["loaded"] == [] and "not later" in skipped["skipped"][0]["reason"]

    # A later as_of is a new seed revision.
    changed["bulletins"][0]["fetched_at"] = changed["as_of"] = "2026-10-02T21:00:00Z"
    write_seed_file(changed, demo["seeds_dir"])
    again = load_approved_seeds(conn, demo["seeds_dir"])
    assert again["loaded"][0]["revision"] == 2


def test_a_seed_that_fails_its_checks_is_skipped(conn, demo, seed):
    bad = _approved(seed)
    _slot(bad, "s1")["entry"]["church_slug"] = "st-anne-demo-fairport"
    write_seed_file(bad, demo["seeds_dir"])
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert result["loaded"] == [] and "unknown_church" in result["skipped"][0]["reason"]
    assert render_seeds(result)[-1].startswith(f"- **{PARISH}** seed file not loaded")


def test_ensure_db_loads_approved_seeds_unless_told_not_to(pipeline_dir: Path):
    create_db()
    seed = {
        "schema_version": 1, "parish_slug": "test-parish", "status": APPROVED,
        "as_of": "2026-10-01T00:00:00Z", "drafted_by": "test", "drafted_at": None,
        "reviewer": "R", "approved_at": "2026-10-02T00:00:00Z", "summary": "",
        "blocked_reason": None, "calls": [],
        "bulletins": [{"content_hash": "f" * 64, "fetched_at": "2026-10-01T00:00:00Z",
                       "published_date": None, "read": True}],
        "slots": [{
            "id": "s1", "decision": "include", "status": "settled", "page": None,
            "entry": {"church_slug": "test-church", "event_type": "mass",
                      "event_kind": "weekly", "day_of_week": "Sunday", "date": None,
                      "start_time": "09:00", "end_time": None, "cancelled": False,
                      "weeks_of_month": [], "season": None, "note": None},
            "sources": [{"source": "agent", "said": "Sunday 9 AM"}], "rationale": "Printed.",
            "question": None, "options": None, "answer": None,
        }],
    }
    write_seed_file(seed, pipeline_dir / "data" / "seeds")
    held = ensure_db(load_seeds=False)
    assert "seeds" not in held
    result = ensure_db()
    # The bulletin isn't in this database: the seed loads without a sighting.
    assert [(r["parish"], r["entries"], r["sightings"]) for r in result["seeds"]["loaded"]] == [
        ("test-parish", 1, 0)]
    assert ensure_db()["seeds"] == {"loaded": [], "skipped": []}


# ── HTTP ────────────────────────────────────────────────────────────────────
@pytest.fixture
def server(demo, tmp_path: Path):
    static = tmp_path / "dist"
    static.mkdir()
    (static / "index.html").write_text("<!doctype html>")
    app = LabelerApp(db_path=demo["db_path"], labels_dir=demo["labels_dir"], static_dir=static,
                     mode="demo", seeds_dir=demo["seeds_dir"])
    srv = make_server(app, port=0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    srv.server_close()


def _request(srv, method: str, path: str, body=None):
    conn = http.client.HTTPConnection("127.0.0.1", srv.server_address[1], timeout=10)
    headers = {"Host": f"localhost:{srv.server_address[1]}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    conn.request(method, path, body=data, headers=headers)
    resp = conn.getresponse()
    payload = json.loads(resp.read())
    conn.close()
    return resp.status, payload


def test_http_seed_queue_detail_and_save(server, seed):
    status, queue = _request(server, "GET", "/api/seeds")
    assert status == 200 and queue["seeds"][0]["parish_slug"] == PARISH
    status, detail = _request(server, "GET", f"/api/seeds/{PARISH}")
    assert status == 200 and detail["seed"]["status"] == NEEDS_REVIEW
    assert {c["slug"] for c in detail["churches"]} == {HF, SJ}
    status, saved = _request(server, "PUT", f"/api/seeds/{PARISH}", _settle_all(seed))
    assert status == 200 and saved["seed"]["status"] == READY
    status, error = _request(server, "PUT", f"/api/seeds/{PARISH}", {**seed, "status": "x"})
    assert status == 400 and "status" in error["error"]
    assert _request(server, "GET", "/api/seeds/st-anne-demo")[0] == 404
    assert _request(server, "GET", "/api/seeds/Bad_Slug")[0] == 404


def test_http_bulk_approval_only_approves_ready_files_and_reports_failures(server, demo, seed):
    ready = _settle_all(seed)
    write_seed_file(ready, demo["seeds_dir"])
    # This shape-valid ready file fails the database checks before the valid one.
    failed = {**ready, "parish_slug": "a-failed-ready"}
    write_seed_file(failed, demo["seeds_dir"])
    untouched = []
    for status in ("needs_review", "drafting", "blocked", "approved"):
        other = copy.deepcopy(_approved(seed) if status == "approved" else seed)
        other.update(parish_slug=f"skip-{status.replace('_', '-')}", status=status)
        if status == "blocked":
            other["blocked_reason"] = "Needs more evidence"
        untouched.append(write_seed_file(other, demo["seeds_dir"]))
    unreadable = demo["seeds_dir"] / "unreadable.json"
    unreadable.write_text("{broken JSON")
    untouched.append(unreadable)
    before = {p: p.read_bytes() for p in untouched}
    failed_before = seed_path("a-failed-ready", demo["seeds_dir"]).read_bytes()

    status, result = _request(server, "POST", "/api/seeds/approve-ready",
                              {"reviewer": "  Bulk Reviewer  "})
    assert status == 200
    assert result["approved"] == [PARISH]
    assert len(result["failed"]) == 1
    assert result["failed"][0]["parish_slug"] == "a-failed-ready"
    assert "not in data/parishes.csv" in result["failed"][0]["error"]
    approved = read_seed(PARISH, demo["seeds_dir"])
    assert approved["status"] == APPROVED
    assert approved["reviewer"] == "Bulk Reviewer" and approved["approved_at"]
    assert approved == {**ready, "status": APPROVED, "reviewer": "Bulk Reviewer",
                        "approved_at": approved["approved_at"]}
    assert {p: p.read_bytes() for p in untouched} == before
    assert seed_path("a-failed-ready", demo["seeds_dir"]).read_bytes() == failed_before
    assert result["seeds"] == _request(server, "GET", "/api/seeds")[1]["seeds"]

    # A repeated click cannot reapprove the successes or change their timestamps.
    status, again = _request(server, "POST", "/api/seeds/approve-ready", {"reviewer": "R"})
    assert status == 200 and again["approved"] == []
    assert read_seed(PARISH, demo["seeds_dir"]) == approved


@pytest.mark.parametrize("body", [{}, {"reviewer": ""}, {"reviewer": " "},
                                  {"reviewer": 123}, {"reviewer": None}, []])
def test_http_bulk_approval_requires_a_reviewer(server, demo, seed, body):
    path = write_seed_file(_settle_all(seed), demo["seeds_dir"])
    before = path.read_bytes()
    status, result = _request(server, "POST", "/api/seeds/approve-ready", body)
    assert status == 400 and "reviewer" in result["error"]
    assert path.read_bytes() == before


@pytest.mark.parametrize("problem", ["open", "evidence", "church"])
def test_http_bulk_approval_runs_the_usual_approval_checks(server, demo, seed, problem):
    ready = _settle_all(seed)
    if problem == "open":
        ready = {**seed, "status": READY}
        message = "questions are still open"
    elif problem == "evidence":
        _slot(ready, "s1")["sources"][0]["source"] = "history"
        message = "needs an agent source"
    else:
        _slot(ready, "s1")["entry"]["church_slug"] = "unknown-church"
        message = "unknown-church"
    path = write_seed_file(ready, demo["seeds_dir"])
    before = path.read_bytes()
    status, result = _request(server, "POST", "/api/seeds/approve-ready", {"reviewer": "R"})
    assert status == 200 and result["approved"] == []
    assert result["failed"][0]["parish_slug"] == PARISH
    assert message in result["failed"][0]["error"]
    assert path.read_bytes() == before


def test_http_bulk_approval_with_no_ready_seeds_is_a_noop(server, demo):
    before = seed_path(PARISH, demo["seeds_dir"]).read_bytes()
    status, result = _request(server, "POST", "/api/seeds/approve-ready", {"reviewer": "R"})
    assert status == 200 and result["approved"] == [] and result["failed"] == []
    assert result["seeds"][0]["status"] == NEEDS_REVIEW
    assert seed_path(PARISH, demo["seeds_dir"]).read_bytes() == before


# ── The command ─────────────────────────────────────────────────────────────
def test_seed_command_prints_text_or_json(pipeline_dir: Path, capsys):
    create_db()
    assert main(["seed", "status"]) == 0
    assert capsys.readouterr().out.strip() == "No seed files."
    assert main(["seed", "status", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["seeds"] == []
    assert main(["seed", "check", "test-parish"]) == 1
    assert "no seed file" in capsys.readouterr().out
    assert main(["seed", "bulletins", "nope"]) == 1
    assert "Parish not found" in capsys.readouterr().err


@pytest.fixture
def demo_cli(demo, tmp_path, monkeypatch):
    """`main` on the demo dataset, its seed files in `demo["seeds_dir"]`."""
    monkeypatch.chdir(tmp_path)  # `seed pdf` writes under data/seed-work/
    monkeypatch.setattr(seed_cli, "_connect", lambda: connect_db(demo["db_path"]))
    monkeypatch.setattr(seed_cli, "_ctx", lambda args: SeedContext(seeds_dir=demo["seeds_dir"]))
    return demo


def test_start_prints_where_the_draft_starts_and_then_resumes_it(demo_cli, capsys):
    assert main(["seed", "start", "st-anne-demo"]) == 0
    out = capsys.readouterr().out
    assert "a new draft listing 1 bulletins" in out
    assert "https://example.org/st-anne" in out
    assert "st-anne-demo-fairport                    St. Anne Church, 9 Church St, Fairport" in out
    assert "newest PDF: data/seed-work/st-anne-demo/" in out
    assert "warning" not in out
    path = seed_path("st-anne-demo", demo_cli["seeds_dir"])
    before = path.read_bytes()
    assert main(["seed", "start", "st-anne-demo"]) == 0
    out = capsys.readouterr().out
    assert "resumed an existing draft (drafting, 0 slots, 0 calls)" in out
    assert "Read it before editing" in out and "newest PDF:" in out
    assert path.read_bytes() == before


def test_init_is_an_alias_of_start_that_ignores_resume(demo_cli, capsys):
    assert main(["seed", "init", "st-anne-demo"]) == 0
    assert "a new draft" in capsys.readouterr().out
    path = seed_path("st-anne-demo", demo_cli["seeds_dir"])
    before = path.read_bytes()
    for args in (["seed", "init", "st-anne-demo"], ["seed", "init", "st-anne-demo", "--resume"]):
        assert main(args) == 0
        assert "resumed an existing draft" in capsys.readouterr().out
    assert path.read_bytes() == before


def test_seed_help_lists_every_command_by_phase(capsys):
    with pytest.raises(SystemExit):
        main(["seed", "--help"])
    out = capsys.readouterr().out
    heads = [out.index(h) for h in ("\nBatch:", "\nDraft:", "\nRead:", "\nCompare:",
                                    "\nPaid calls:")]
    assert heads == sorted(heads)
    listed = {line.split()[0] for line in out.splitlines() if line.startswith("  ")}
    assert listed >= {"status", "check", "questions", "approve", "start", "brief",
                      "mark-read", "finalize", "bulletins", "pdf", "text", "pages", "grep",
                      "history", "diff", "church", "site", "ask", "extract"}
    assert "init" not in listed


def test_questions_lists_each_question_its_leaning_and_answer(demo_cli, seed, capsys):
    s16, s17 = _slot(seed, "s16"), _slot(seed, "s17")
    s16["rationale"] += " Leaning per C2; R12 does not settle it."
    s17.update(status="settled", decision="exclude", answer={
        "choice": 1, "by": "Reviewer", "at": "2026-10-10T12:00:00Z"})
    for slot_id in ("s15", "s14"):  # a group is one question
        _slot(seed, slot_id).update(copy.deepcopy({k: s16[k] for k in (
            "status", "decision", "question", "options", "answer", "rationale")}),
            group="weekday")
    s16["group"] = "weekday"
    write_seed_file(seed, demo_cli["seeds_dir"])

    assert main(["seed", "questions"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[-1] == "2 questions, 1 answered, 0 matched the leaning (* marks it)"
    assert f"{PARISH} weekday (s14, s15, s16): Holy Family: is the Monday 8:00 AM Mass " \
        "weekly?" in out
    assert "  *0 Every Monday, 8:00 AM" in out and "   1 Leave out" in out
    assert "  open  cites C2, R12" in out
    assert "  answer: 1, not the leaning; Reviewer 2026-10-10" in out

    assert main(["seed", "questions", "--open", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert [q["slots"] for q in result["questions"]] == [["s14", "s15", "s16"]]
    assert result["questions"][0]["cites"] == ["C2", "R12"]
    _slot(seed, "s17")["answer"]["choice"] = 0
    s16.update(status="settled", answer={"choice": "dropped", "by": "R", "at": "2026-10-11"})
    s16["options"][0]["leaning"], s16["options"][1]["leaning"] = False, True
    seed["slots"] = [s for s in seed["slots"] if s["id"] not in ("s14", "s15")]
    write_seed_file(seed, demo_cli["seeds_dir"])
    assert main(["seed", "questions", "--answered", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert [(q["match"], q["matched"]) for q in result["questions"]] == [
        ("dropped", True), ("leaning", True)]
    assert result["totals"] == {"questions": 2, "answered": 2, "matched_leaning": 2,
                                "answered_by_person": 2, "answered_by_agent": 0}
    assert {q["answered_by"] for q in result["questions"]} == {"person"}


def test_approve_command_reads_answers_and_prints_text_or_json(demo_cli, seed, capsys,
                                                               monkeypatch, tmp_path):
    answers = tmp_path / "answers.json"
    answers.write_text(json.dumps([{"slot": "s16", "choice": 0}]))
    assert main(["seed", "approve", PARISH, "--reviewer", "Reviewer",
                 "--answers", str(answers)]) == 1
    assert "can't approve holy-family-demo: An agent reviewer is agent:<name>@<commit>" \
        in capsys.readouterr().err
    assert main(["seed", "approve", PARISH, "--reviewer", AGENT,
                 "--answers", str(answers)]) == 1
    assert "1 slots are still open: s17" in capsys.readouterr().err
    answers.write_text("not json")
    assert main(["seed", "approve", PARISH, "--reviewer", AGENT,
                 "--answers", str(answers)]) == 1
    assert "are not JSON" in capsys.readouterr().err
    assert main(["seed", "approve", "st-anne-demo", "--reviewer", AGENT]) == 1
    assert "st-anne-demo has no seed file to approve" in capsys.readouterr().err

    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps([
        {"slot": "s16", "choice": 0}, {"slot": "s17", "choice": "dropped"}])))
    assert main(["seed", "approve", PARISH, "--reviewer", AGENT, "--answers", "-"]) == 0
    out = capsys.readouterr().out.splitlines()
    approved_at = read_seed(PARISH, demo_cli["seeds_dir"])["approved_at"]
    assert out[0] == f"{seed_path(PARISH, demo_cli['seeds_dir']).relative_to(Path.cwd())}: " \
        f"approved by {AGENT} at {approved_at[:16].replace('T', ' ')}"
    assert out[1:] == ["  s16: 0 (include)", "  s17: dropped (exclude)"]
    assert main(["seed", "approve", PARISH, "--reviewer", AGENT, "--json"]) == 1
    assert "Already approved by agent:seed-review@abc1234" in capsys.readouterr().err


def test_questions_keeps_agent_answers_apart_from_peoples(demo_cli, seed, capsys):
    _slot(seed, "s17").update(status="settled", decision="exclude", answer={
        "choice": 2, "by": "Reviewer", "at": "2026-10-10T12:00:00Z"})
    _slot(seed, "s16").update(status="settled", decision="include",
                              entry=_slot(seed, "s16")["options"][0]["entry"], answer={
                                  "choice": 0, "by": AGENT, "at": "2026-10-11T12:00:00Z"})
    seed["slots"].append({**copy.deepcopy(_slot(seed, "s17")), "id": "s18", "answer": None,
                          "status": "needs_human", "decision": None})
    write_seed_file(seed, demo_cli["seeds_dir"])

    assert main(["seed", "questions", "--answered", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert [(q["slots"], q["answered_by"]) for q in result["questions"]] == [
        (["s16"], "agent"), (["s17"], "person")]
    assert result["totals"] == {"questions": 2, "answered": 2, "matched_leaning": 1,
                                "answered_by_person": 1, "answered_by_agent": 1}

    assert main(["seed", "questions", "--answered"]) == 0
    out = capsys.readouterr().out.splitlines()
    heads = [line.split(":")[0] for line in out if line.startswith(PARISH)]
    assert heads == [f"{PARISH} s17", f"{PARISH} s16"]
    assert out.index("Answered by agents:") == out.index(
        next(line for line in out if line.startswith(f"{PARISH} s16"))) - 1
    assert f"  answer: 0, the leaning; {AGENT} 2026-10-11" in out
    assert out[-1] == "2 questions, 2 answered (1 by people, 1 by agents), " \
        "1 matched the leaning (* marks it)"

    for by, slots in (("agent", [["s16"]]), ("person", [["s17"]])):
        assert main(["seed", "questions", "--by", by, "--json"]) == 0
        assert [q["slots"] for q in json.loads(capsys.readouterr().out)["questions"]] == slots
    # Without --answered, the open question is listed with people's, before the agents'.
    assert main(["seed", "questions"]) == 0
    out = capsys.readouterr().out
    assert out.index(f"{PARISH} s18") < out.index("Answered by agents:")
    assert main(["seed", "questions", "--open", "--by", "agent"]) == 1
    assert "--by picks answered questions" in capsys.readouterr().err


def test_finalize_warns_of_history_no_slot_covers_and_still_passes(demo_cli, seed, capsys):
    seed["slots"] = [s for s in seed["slots"] if s["id"] != "s4"]
    write_seed_file(seed, demo_cli["seeds_dir"])
    assert main(["seed", "finalize", PARISH]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"{PARISH}: needs_review, 2 open questions  OK"
    assert out[1:] == [f"  ! history has weekly mass Sunday 09:00 {SJ} (2 of 2 bulletins, p2) "
                       "and no slot or option covers it"]
    assert main(["seed", "diff", PARISH]) == 0
    assert f"weekly mass Sunday 09:00 {SJ}  (2/2 bulletins, p2)" in capsys.readouterr().out


# ── Review findings ─────────────────────────────────────────────────────────
def test_a_slot_left_out_may_name_a_chapel_outside_the_parish(conn, seed):
    _slot(seed, "s11")["entry"]["church_slug"] = "st-ann-chapel-elsewhere"
    _slot(seed, "s16")["options"][1]["entry"] = {
        **_slot(seed, "s16")["options"][0]["entry"], "church_slug": "st-ann-chapel-elsewhere"}
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    _slot(seed, "s1")["entry"]["church_slug"] = "st-ann-chapel-elsewhere"
    assert any("unknown_church" in p for p in check_seed(conn, seed, parish_slug=PARISH))


def test_malformed_files_are_reported_not_crashed_on(conn, demo, seed):
    _slot(seed, "s1")["sources"][0]["source"] = ["agent"]
    seed["calls"] = "none"
    assert validate_seed(seed)
    write_seed_file({**seed, "status": APPROVED}, demo["seeds_dir"])
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert result["loaded"] == [] and result["skipped"][0]["parish"] == PARISH
    assert seed_queue(conn, demo["seeds_dir"])[0]["calls"] == 0
    detail = seed_detail(conn, PARISH, demo["seeds_dir"])
    assert detail["seed"] is None and detail["problems"]


def test_one_seed_file_that_raises_does_not_stop_the_others(conn, demo, seed, monkeypatch):
    write_seed_file(_approved(seed), demo["seeds_dir"])
    monkeypatch.setattr("pdf_extract.seeding.loader.load_seed",
                        lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert result["skipped"] == [{"parish": PARISH, "reason": "RuntimeError: boom"}]


def test_a_call_keeps_what_the_file_gained_while_it_ran(conn, demo, monkeypatch):
    ctx = SeedContext(seeds_dir=demo["seeds_dir"])
    extract = _FakeClassifier.extract

    def extract_while_the_agent_saves(self, pdf, *, churches, today):
        saved = read_seed(PARISH, demo["seeds_dir"])
        saved["summary"] = "Written while the call ran."
        write_seed_file(saved, demo["seeds_dir"])
        return extract(self, pdf, churches=churches, today=today)

    monkeypatch.setattr(_FakeClassifier, "extract", extract_while_the_agent_saves)
    monkeypatch.setattr(seed_calls, "extraction_classifier", lambda model: _FakeClassifier())
    seed_calls.run_extract(conn, ctx, PARISH, "latest", OPENAI_MODEL)
    saved = read_seed(PARISH, demo["seeds_dir"])
    assert saved["summary"] == "Written while the call ran." and len(saved["calls"]) == 1


@pytest.fixture
def routed_cli(demo, tmp_path, monkeypatch):
    """Keep the real CLI context routing, with an isolated database and data tree."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(seed_cli, "_connect", lambda: connect_db(demo["db_path"]))
    return demo


def test_resume_preserves_decisions_evidence_and_paid_call_limit(
    demo_cli, conn, seed, monkeypatch,
):
    seed["status"] = "drafting"
    seed["calls"] = [{"id": "c1", "kind": "ask", "model": GEMINI_MODEL,
                      "bulletin": seed["bulletins"][0]["content_hash"], "cached": False,
                      "question": "When?", "answer": "Saturday", "page": 2,
                      "quote": "Sat 4 PM", "cost_usd": 0.01}]
    path = write_seed_file(seed, demo_cli["seeds_dir"])
    before = path.read_bytes()
    assert main(["seed", "init", PARISH, "--resume"]) == 0
    assert path.read_bytes() == before
    monkeypatch.setenv("CARLO_SEED_CALL_LIMIT", "1")
    _FakeClassifier.calls = 0
    monkeypatch.setattr(seed_calls, "extraction_classifier", lambda model: _FakeClassifier())
    with pytest.raises(SeedError, match="used its 1 external calls"):
        seed_calls.run_extract(conn, SeedContext(seeds_dir=demo_cli["seeds_dir"]),
                               PARISH, "latest", OPENAI_MODEL)
    assert _FakeClassifier.calls == 0


def test_mark_read_preserves_a_consulted_bulletin_without_slot_citations(demo_cli, seed, capsys):
    old = seed["bulletins"][1]["content_hash"]
    seed["slots"] = [_slot(seed, "s1")]
    seed["slots"][0]["sources"] = [
        {"source": "agent", "bulletin": old, "page": 2, "said": "Saturday 4 PM"}]
    seed["status"] = "drafting"
    for b in seed["bulletins"]:
        b["read"] = False
    write_seed_file(seed, demo_cli["seeds_dir"])
    assert main(["seed", "mark-read", PARISH, "latest"]) == 0
    assert main(["seed", "finalize", PARISH]) == 1  # older-only settled inclusion
    assert "settled inclusion needs an agent source" in capsys.readouterr().out
    saved = read_seed(PARISH, demo_cli["seeds_dir"])
    assert saved["bulletins"][0]["read"]
    assert saved["as_of"] == seed["bulletins"][0]["fetched_at"]


@pytest.mark.parametrize("source", ["history", "website", "older_agent", "no_bulletin"])
def test_settled_inclusions_need_agent_evidence_on_the_anchor(conn, seed, source):
    slot = _slot(seed, "s1")
    old = seed["bulletins"][1]["content_hash"]
    if source == "website":
        slot["sources"] = [{"source": "website", "url": "https://example.org/times",
                            "said": "Saturday 4 PM"}]
    elif source == "no_bulletin":
        slot["sources"] = [{"source": "agent", "page": 2, "said": "Saturday 4 PM"}]
    else:
        slot["sources"] = [{"source": "agent" if source == "older_agent" else "history",
                            "bulletin": old, "page": 2, "said": "Saturday 4 PM"}]
    assert any("settled inclusion needs an agent source" in p
               for p in check_seed(conn, seed, parish_slug=PARISH))


def test_review_can_explicitly_include_an_older_bulletin_candidate(conn, demo, seed):
    slot = _slot(seed, "s1")
    old = seed["bulletins"][1]["content_hash"]
    candidate = copy.deepcopy(slot["entry"])
    slot.update(status="needs_human", decision=None, entry=None, page=None,
                question="Keep the older Saturday Mass?", options=[
                    {"label": "Keep", "entry": candidate, "leaning": True},
                    {"label": "Leave out", "entry": None}],
                sources=[{"source": "agent", "bulletin": old, "page": 2,
                          "said": "Saturday 4 PM"}])
    write_seed_file(seed, demo["seeds_dir"])
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    reviewed = _settle_all(seed)
    approved = save_reviewed_seed(conn, PARISH, {**reviewed, "status": APPROVED,
                                                "reviewer": "Reviewer"}, demo["seeds_dir"])
    assert approved["problems"] == []
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert result["loaded"][0]["entries"] == 16


def test_new_approvals_require_evidence_but_older_approved_seeds_keep_loading(conn, demo, seed):
    reviewed = _settle_all(seed)
    slot = _slot(reviewed, "s1")
    slot["sources"] = [{"source": "history", "bulletin": reviewed["bulletins"][1]["content_hash"],
                        "said": "Saturday 4 PM"}]
    slot["page"] = None
    write_seed_file(reviewed, demo["seeds_dir"])
    with pytest.raises(SeedReviewError, match="settled inclusion needs an agent source"):
        save_reviewed_seed(conn, PARISH, {**reviewed, "status": APPROVED, "reviewer": "R"},
                           demo["seeds_dir"])
    # A seed approved before these drafting checks still loads without changing its file.
    legacy = {**reviewed, "status": APPROVED, "reviewer": "R",
              "approved_at": "2026-10-10T12:05:00Z"}
    path = write_seed_file(legacy, demo["seeds_dir"])
    before = path.read_bytes()
    result = load_approved_seeds(conn, demo["seeds_dir"])
    assert result["skipped"] == [] and result["loaded"][0]["entries"] == 16
    assert path.read_bytes() == before


def test_check_requires_reading_the_newest_listed_bulletin(conn, seed):
    seed["bulletins"][0]["read"] = False
    seed["as_of"] = seed["bulletins"][1]["fetched_at"]
    assert any("newest listed bulletin" in p for p in check_seed(conn, seed, parish_slug=PARISH))


def _website_slot(seed):
    slot = _slot(seed, "s1")
    slot.update(page=None, sources=[{
        "source": "website", "url": "https://example.org/times",
        "said": "Fall schedule: Saturday Vigil Mass at 6:15 PM at Holy Family.",
        "schedule_check": {
            "checked_at": "2026-10-10T12:00:00Z",
            "current_because": "Parish schedule linked from its current home page; the fall "
                               "schedule matches this year's parish announcements.",
            "bulletin": seed["bulletins"][0]["content_hash"][:8],
            "fits_because": "The newest bulletin directs readers to the parish website for "
                            "the fall Vigil schedule; it gives no conflicting Vigil time.",
        },
    }])
    # A website-only time, with no agent source asserting that a bulletin prints it.
    slot["entry"]["start_time"] = "18:15"
    return slot


def test_assessed_website_schedule_can_be_settled_without_a_bulletin_time(conn, seed):
    slot = _website_slot(seed)
    assert slot["answer"] is None
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    finalized = finalize_seed(seed, [HF, SJ])
    assert _slot(finalized, "s1")["sources"] == slot["sources"]
    assert check_seed(conn, finalized, parish_slug=PARISH) == []


@pytest.mark.parametrize("change, message", [
    (lambda s: s.update(page=2), "settled inclusion needs"),
    (lambda s: s["sources"][0].pop("schedule_check"), "settled inclusion needs"),
    (lambda s: s["sources"][0]["schedule_check"].update(bulletin="f" * 64),
     "bulletin must name"),
    (lambda s: s["sources"][0]["schedule_check"].update(current_because="  "),
     "current_because must explain"),
    (lambda s: s["sources"][0]["schedule_check"].pop("fits_because"), "missing fits_because"),
    (lambda s: s["sources"][0]["schedule_check"].update(checked_at="yesterday"),
     "checked_at must be an ISO time"),
    (lambda s: s["sources"][0]["schedule_check"].update(fresh=True), "unknown fresh"),
    (lambda s: s["sources"][0].update(schedule_check=True), "must be an object"),
    (lambda s: s["sources"][0].update(said="  "), "said is required"),
    (lambda s: s["sources"][0].pop("url"), "url is required"),
    (lambda s: s["sources"][0].update(url="file:///tmp/times"), "url is required"),
    (lambda s: s["sources"][0].update(bulletin="f" * 64), "website source names no bulletin"),
    (lambda s: s["sources"][0].update(source="history"),
     "schedule_check is only for a website source"),
    (lambda s: s.update(website_ok=True), "unknown website_ok"),
])
def test_website_assessment_requires_quoted_evidence_and_explicit_shape(conn, seed, change, message):
    slot = _website_slot(seed)
    change(slot)
    assert any(message in p for p in check_seed(conn, seed, parish_slug=PARISH))


def test_website_assessment_must_fit_the_newest_read_bulletin(conn, seed):
    slot = _website_slot(seed)
    slot["sources"][0]["schedule_check"]["bulletin"] = seed["bulletins"][1]["content_hash"]
    assert validate_seed(seed) == []  # known, but no longer the anchor for this assessment
    assert _evidence_problems(conn, seed)
    slot["sources"][0]["schedule_check"]["bulletin"] = seed["bulletins"][0]["content_hash"]
    seed["bulletins"][0]["read"] = False
    seed["as_of"] = seed["bulletins"][1]["fetched_at"]
    assert any("newest listed bulletin" in p for p in check_seed(conn, seed, parish_slug=PARISH))


def test_finalize_does_not_invent_a_website_assessment(conn, seed):
    slot = _website_slot(seed)
    del slot["sources"][0]["schedule_check"]
    finalized = finalize_seed(seed, [HF, SJ])
    assert "schedule_check" not in _slot(finalized, "s1")["sources"][0]
    assert _evidence_problems(conn, finalized)


def test_website_backed_agent_inclusion_can_be_reviewed_and_loaded(conn, demo, seed):
    _website_slot(seed)
    write_seed_file(seed, demo["seeds_dir"])
    reviewed = _settle_all(seed)
    saved = save_reviewed_seed(conn, PARISH, {
        **reviewed, "status": APPROVED, "reviewer": "Reviewer",
    }, demo["seeds_dir"])
    assert saved["problems"] == []
    assert load_approved_seeds(conn, demo["seeds_dir"])["loaded"][0]["entries"] == 16
    slot = _slot(read_seed(PARISH, demo["seeds_dir"]), "s1")
    assert slot["page"] is None and slot["answer"] is None


def test_a_settled_inclusions_page_must_match_its_newest_agent_source(conn, seed):
    _slot(seed, "s1")["page"] = 3
    assert any("settled inclusion needs an agent source" in p
               for p in check_seed(conn, seed, parish_slug=PARISH))


def test_each_excluded_history_event_needs_a_structured_slot(seed):
    first = copy.deepcopy(_slot(seed, "s1"))
    second = copy.deepcopy(_slot(seed, "s2"))
    for slot in (first, second):
        slot.update(decision="exclude", rationale="Leave out both Masses from another parish.")
    past = [_history_of(first["entry"], second["entry"])]
    # Mentioning both in a rationale alone does not account for the second event.
    assert len(diff({**seed, "slots": [first]}, past)["missing"]) == 1
    assert diff({**seed, "slots": [first, second]}, past)["missing"] == []


@pytest.mark.parametrize("command", ["check", "finalize"])
def test_batch_validation_reports_broken_json_and_continues(demo_cli, capsys, command):
    path = seed_path("a-broken", demo_cli["seeds_dir"])
    path.write_text('{')
    args = ["seed", command, "--all"] if command == "check" else [
        "seed", command, "a-broken", PARISH]
    assert main(args) == 1
    out = capsys.readouterr().out
    assert "a-broken: invalid" in out and "is not JSON" in out
    assert f"{PARISH}: needs_review, 2 open questions  OK" in out
    assert path.read_text() == '{'


def test_agents_cannot_resume_or_mark_read_an_approved_file(demo_cli, seed, capsys):
    path = write_seed_file(_approved(seed), demo_cli["seeds_dir"])
    before = path.read_bytes()
    assert main(["seed", "start", PARISH]) == 1
    assert main(["seed", "init", PARISH, "--resume"]) == 1
    assert main(["seed", "mark-read", PARISH, "latest"]) == 1
    assert "belongs to its reviewer" in capsys.readouterr().err
    assert path.read_bytes() == before


# ── Fewer questions: rules a drafter can settle by ──────────────────────────
def test_weeks_of_the_month_a_day_and_a_bulletins_week_hold():
    from datetime import date

    from pdf_extract.seeding.checks import covered_weeks, weeks_of

    assert weeks_of(date(2026, 10, 2)) == {"first"}
    assert weeks_of(date(2026, 10, 30)) == {"fifth", "last"}
    assert weeks_of(date(2026, 9, 24)) == {"fourth", "last"}
    # Issue of Sunday, October 11: its week runs to Sunday the 18th.
    issue = {"published_date": "2026-10-11", "fetched_at": "2026-10-11T16:00:00Z"}
    assert covered_weeks(issue, "Friday") == {"third"}
    assert covered_weeks(issue, "Sunday") == {"second", "third"}
    assert covered_weeks({"published_date": None, "fetched_at": None}, "Friday") is None


def _older_slot(seed: dict[str, Any], entry: dict[str, Any], *, source: str = "agent"):
    """s8 rewritten as a settled inclusion only the older demo bulletin prints."""
    slot = _slot(seed, "s8")
    slot.update(entry={**slot["entry"], **entry}, page=None, sources=[
        {"source": source, "bulletin": seed["bulletins"][1]["content_hash"], "page": 2,
         "said": "Holy Hour"}])
    return slot


def _evidence_problems(conn, seed) -> list[str]:
    problems = check_seed(conn, seed, parish_slug=PARISH)
    assert all("settled inclusion needs" in p for p in problems), problems
    return problems


def test_a_weeks_of_the_month_slot_the_newest_week_cant_hold_may_cite_an_older_bulletin(
    conn, seed,
):
    # The newest demo issue covers Sunday Sep 27 to Sunday Oct 4: Thursday Oct 1 is a first.
    _older_slot(seed, {"weeks_of_month": ["third"]})
    assert _evidence_problems(conn, seed) == []
    # A fourth Thursday: the older issue's week holds one (Sep 24), and it is cited.
    _older_slot(seed, {"weeks_of_month": ["fourth"]})
    assert _evidence_problems(conn, seed) == []


@pytest.mark.parametrize("entry, source", [
    ({"weeks_of_month": ["first"]}, "agent"),  # Oct 1: the newest issue would print it
    ({"weeks_of_month": []}, "agent"),  # every week: the newest issue would print it
    ({"weeks_of_month": ["third"], "exclude_weeks": True}, "agent"),
    ({"weeks_of_month": ["third"]}, "history"),  # history alone is no reading
])
def test_older_evidence_is_not_enough_for_a_slot_the_newest_week_holds(conn, seed, entry, source):
    _older_slot(seed, entry, source=source)
    assert _evidence_problems(conn, seed)


def test_a_weeks_of_the_month_slot_must_cite_the_newest_bulletin_whose_week_holds_it(conn, seed):
    # A fourth Thursday: the older issue's week holds one (Sep 24), the newest's doesn't,
    # so citing the newest issue, newer though it is, is no reading of it.
    slot = _older_slot(seed, {"weeks_of_month": ["fourth"]})
    slot["sources"][0]["bulletin"] = seed["bulletins"][0]["content_hash"]
    assert _evidence_problems(conn, seed)


def test_a_dated_entry_an_older_bulletin_announced_may_be_settled(conn, seed):
    dated = {"event_kind": "specific_date", "day_of_week": None, "date": "2026-11-02",
             "season": None, "weeks_of_month": []}
    _older_slot(seed, dated)
    assert _evidence_problems(conn, seed) == []
    _slot(seed, "s8")["page"] = 2  # it isn't on the newest bulletin's page 2
    assert _evidence_problems(conn, seed)


def _weekly_omission_slot(seed):
    newest, previous = seed["bulletins"]
    oldest = {**previous, "content_hash": "c" * 64, "published_date": "2026-09-13",
              "fetched_at": "2026-09-12T12:00:00Z"}
    seed["bulletins"].append(oldest)
    slot = _slot(seed, "s1")
    slot.update(page=None, sources=[
        {"source": "agent", "bulletin": b["content_hash"][:8], "page": 2,
         "said": "Holy Family: Saturday Vigil Mass 4 PM"} for b in (previous, oldest)
    ], weekly_omission={
        "bulletin": newest["content_hash"][:8],
        "reason": "The same church, Mass, Saturday and 4 PM recur in both older issues. "
                  "The newest issue omits that service once; its announcements and "
                  "schedule give no cancellation or changed time.",
    })
    return slot


def _omission_problems(conn, seed, **kwargs):
    # The third synthetic issue exercises evidence without adding database fixtures.
    return check_seed(conn, seed, parish_slug=PARISH, check_bulletins=False, **kwargs)


def test_established_weekly_slot_can_survive_one_assessed_omission(conn, seed):
    slot = _weekly_omission_slot(seed)
    assert _omission_problems(conn, seed) == []
    finalized = finalize_seed(seed, [HF, SJ])
    assert _slot(finalized, "s1")["weekly_omission"] == slot["weekly_omission"]
    assert _slot(finalized, "s1")["page"] is None
    assert _omission_problems(conn, finalized) == []
    # Published Saturdays and Sundays identify the same issue week.
    seed["bulletins"][1]["published_date"] = "2026-09-19"
    assert _omission_problems(conn, seed) == []


@pytest.mark.parametrize("change", [
    lambda s, slot: slot.pop("weekly_omission"),
    lambda s, slot: slot["weekly_omission"].update(bulletin=s["bulletins"][1]["content_hash"]),
    lambda s, slot: slot.update(page=2),
    lambda s, slot: slot["sources"].pop(),
    lambda s, slot: slot["sources"][1].update(bulletin=slot["sources"][0]["bulletin"]),
    lambda s, slot: slot["sources"][0].update(source="history"),
    lambda s, slot: slot["sources"][1].update(source="history"),
    lambda s, slot: slot["sources"][0].update(page=None),
    lambda s, slot: slot["sources"][1].update(page=None),
    lambda s, slot: s["bulletins"][1].update(read=False),
    lambda s, slot: s["bulletins"][2].update(read=False),
    lambda s, slot: s["bulletins"][2].update(published_date="2026-09-20"),
    lambda s, slot: s["bulletins"][1].update(published_date="2026-09-13"),
    lambda s, slot: s["bulletins"][2].update(published_date="2026-09-27"),
    lambda s, slot: s["bulletins"][2].update(published_date="2026-11-01"),
    lambda s, slot: s["bulletins"][1].update(fetched_at=s["bulletins"][0]["fetched_at"]),
    lambda s, slot: slot["entry"].update(weeks_of_month=["last"], exclude_weeks=True),
])
def test_weekly_omission_requires_distinct_read_issue_weeks_and_recent_support(
    conn, seed, change,
):
    slot = _weekly_omission_slot(seed)
    change(seed, slot)
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, seed))


@pytest.mark.parametrize("index", [0, 1, 2])
@pytest.mark.parametrize("published", [None, "", "unknown", "2026-02-30"])
def test_weekly_omission_never_uses_fetch_dates_to_manufacture_issue_weeks(
    conn, seed, index, published,
):
    _weekly_omission_slot(seed)
    seed["bulletins"][index]["published_date"] = published
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, seed))


def test_weekly_omission_must_cite_the_immediately_preceding_read_issue(conn, seed):
    _weekly_omission_slot(seed)
    # Another PDF of last week's issue was read more recently than the cited one.
    previous = seed["bulletins"][1]
    seed["bulletins"].append({**previous, "content_hash": "d" * 64,
                              "fetched_at": "2026-09-24T12:00:00Z"})
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, seed))
    # Repeated fetches of identical content cannot create another listed issue.
    seed["bulletins"][-1]["content_hash"] = previous["content_hash"]
    assert any("listed twice" in p for p in _omission_problems(conn, seed))


def test_weekly_omission_cannot_evade_targeted_monthly_evidence(conn, seed):
    slot = _weekly_omission_slot(seed)
    slot["entry"].update(day_of_week="Thursday", weeks_of_month=["first"])
    # Newest covers Oct 1, so a missing first Thursday needs the targeted evidence.
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, seed))
    slot["entry"]["weeks_of_month"] = ["fourth"]
    assert _omission_problems(conn, seed) == []  # existing monthly exception
    # Sep 24 is the latest relevant occurrence; older repetitions can't replace it.
    slot["sources"].pop(0)
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, seed))
    # Third Thursday was Sep 17. Cite two other weeks (including the preceding
    # issue), but omit that relevant issue: the weekly fallback must not rescue it.
    extra = {**seed["bulletins"][2], "content_hash": "d" * 64,
             "published_date": "2026-09-06", "fetched_at": "2026-09-05T12:00:00Z"}
    seed["bulletins"].append(extra)
    slot["entry"]["weeks_of_month"] = ["third"]
    slot["sources"] = [
        {**slot["sources"][0], "bulletin": b["content_hash"][:8]}
        for b in (seed["bulletins"][1], extra)
    ]
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, seed))


@pytest.mark.parametrize("change, message", [
    (lambda slot: slot.update(weekly_omission=True), "must be an object"),
    (lambda slot: slot["weekly_omission"].pop("reason"), "missing reason"),
    (lambda slot: slot["weekly_omission"].update(reason=" "), "omission judgment"),
    (lambda slot: slot["weekly_omission"].update(bulletin="deadbeef"), "bulletin must name"),
    (lambda slot: slot["weekly_omission"].update(approved=True), "unknown approved"),
    (lambda slot: slot["sources"][0].update(said=" "), "said is required"),
])
def test_weekly_omission_keeps_assessment_and_quotes_auditable(conn, seed, change, message):
    change(_weekly_omission_slot(seed))
    assert any(message in p for p in _omission_problems(conn, seed))


def test_finalize_does_not_invent_a_weekly_omission_assessment(conn, seed):
    _weekly_omission_slot(seed).pop("weekly_omission")
    finalized = finalize_seed(seed, [HF, SJ])
    assert "weekly_omission" not in _slot(finalized, "s1")
    assert any("settled inclusion needs" in p for p in _omission_problems(conn, finalized))


def test_a_history_event_that_reads_a_slot_at_another_time_is_a_variant_not_missing(seed):
    past = [_history_of(
        {**_SUNDAY, "event_type": "adoration", "day_of_week": "Thursday", "start_time": "09:30"},
        {**_SUNDAY, "start_time": "09:30"},  # Sunday 8:00 or 10:30? Not for diff to guess
    )]
    found = diff(seed, past)
    assert [(d["slot"], d["said"]) for d in found["differs"]] == [
        ("s8", f"weekly adoration Thursday 09:30 {HF}")]
    assert [row["said"] for row in found["missing"]] == [f"weekly mass Sunday 09:30 {HF}"]

    finalized = finalize_seed(_without_history(seed), [HF, SJ], [
        {**past[0], "short": seed["bulletins"][0]["content_hash"][:12],
         "content_hash": seed["bulletins"][0]["content_hash"]}])
    history = [s for s in _slot(finalized, "s8")["sources"] if s["source"] == "history"]
    assert [s["said"] for s in history] == [
        f"weekly adoration Thursday 09:30 {HF}  (a different time)"]
    assert finalize_seed(finalized, [HF, SJ], past) == finalized


def test_a_variant_needs_its_bulletin_to_leave_the_slot_unmatched(seed):
    adoration = {**_SUNDAY, "event_type": "adoration", "day_of_week": "Thursday"}
    past = [_history_of({**adoration, "start_time": "09:00"}, {**adoration, "start_time": "19:00"})]
    found = diff(seed, past)
    assert found["differs"] == []
    assert [row["said"] for row in found["missing"]] == [f"weekly adoration Thursday 19:00 {HF}"]


def test_two_events_near_one_slot_are_two_services_not_variants(seed):
    adoration = {**_SUNDAY, "event_type": "adoration", "day_of_week": "Thursday"}
    past = [_history_of({**adoration, "start_time": "09:30"}, {**adoration, "start_time": "19:00"})]
    found = diff(seed, past)
    assert found["differs"] == []
    assert sorted(row["said"] for row in found["missing"]) == [
        f"weekly adoration Thursday 09:30 {HF}", f"weekly adoration Thursday 19:00 {HF}"]
    # One reading printed on two pages is still one variant.
    found = diff(seed, [_history_of({**adoration, "start_time": "09:30"},
                                    {**adoration, "start_time": "09:30", "page_number": 3})])
    assert [d["slot"] for d in found["differs"]] == ["s8"]


def _group(seed: dict[str, Any]) -> None:
    for slot_id in ("s16", "s17"):
        slot = _slot(seed, slot_id)
        slot["group"] = "weekday"
        slot["question"] = "Add the weekday Masses?"
        slot["options"] = [{"label": "Add", "leaning": True, "entry": {
            **_slot(seed, "s12")["entry"], "day_of_week": "Monday" if slot_id == "s16"
            else "Saturday"}}, {"label": "Leave out", "entry": None}]


def test_a_group_of_slots_is_one_question(conn, seed):
    from pdf_extract.seeding.files import question_count

    assert question_count(seed) == 2
    _group(seed)
    assert validate_seed(seed, parish_slug=PARISH) == []
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    assert question_count(seed) == 1
    _slot(seed, "s17")["options"][0]["label"] = "Add Saturday"
    assert any("in group 'weekday' with s16 but asks a different question" in p
               for p in validate_seed(seed, parish_slug=PARISH))


@pytest.mark.parametrize("break_it", [
    lambda seed: seed["slots"].append(None),
    lambda seed: _slot(seed, "s17").update(group=["weekday"]),
    lambda seed: _slot(seed, "s17").update(options="Add"),
])
def test_a_malformed_slot_in_a_group_is_an_error_not_a_crash(seed, break_it):
    _group(seed)
    break_it(seed)
    assert validate_seed(seed, parish_slug=PARISH)


def test_church_list_issues_are_listed_once_and_checked(conn, seed):
    seed["church_list_issues"] = [{"church": "The Franciscan Place, Destiny USA",
                                   "said": "Mon-Thu 12:15 Mass", "bulletin":
                                   seed["bulletins"][0]["content_hash"][:8], "page": 2}]
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    seed["church_list_issues"].append({"church": "", "said": "x", "bulletin": "deadbeef0",
                                       "where": "?"})
    problems = validate_seed(seed, parish_slug=PARISH)
    assert any("church_list_issues[1]: unknown where" in p for p in problems)
    assert any("church_list_issues[1].church is required" in p for p in problems)
    assert any("church_list_issues[1].bulletin must name" in p for p in problems)


def test_church_search_matches_every_word_in_any_order(conn):
    def found(query: str) -> list[str]:
        return [c["church"] for c in find_churches(conn, query)["churches"]]

    assert found("joseph penfield") == [SJ]
    assert found("Saint Joseph's, Penfield") == [SJ]
    assert found("penfield st joseph") == [SJ]
    assert found("joseph fairport") == []


def test_check_leaves_an_approved_file_to_its_reviewer(demo_cli, seed, capsys):
    legacy = _approved(seed)
    _slot(legacy, "s1").update(page=None, sources=[
        {"source": "history", "bulletin": legacy["bulletins"][1]["content_hash"],
         "said": "Saturday 4 PM"}])
    write_seed_file(legacy, demo_cli["seeds_dir"])
    assert main(["seed", "check", "--all"]) == 0
    assert f"{PARISH}: approved  OK" in capsys.readouterr().out


def test_site_reads_a_page_as_text_with_its_schedule_links(demo_cli, monkeypatch, capsys):
    from pdf_extract.dioceses.web import Response
    from pdf_extract.seeding import site

    page = ("<html><body><nav><a href='/mass-times'>Mass Times</a> <a href='/give'>Give</a>"
            "<a href='https://elsewhere.org/mass'>Diocese</a></nav>"
            + "<p>Saturday Vigil 4:00 PM</p>" * 40 + "</body></html>")
    calls: list[str] = []

    def fake_fetch(url: str) -> Response:
        calls.append(url)
        return Response(url, 200, url, "text/html", page.encode())

    monkeypatch.setattr(site, "fetch", fake_fetch)
    monkeypatch.setattr(site, "_browser_html", lambda url: pytest.fail("no browser needed"))
    assert main(["seed", "site", "st-anne-demo", "times"]) == 0
    out = capsys.readouterr().out
    assert out.splitlines()[0].startswith("https://example.org/st-anne/times  (http at ")
    assert "  https://example.org/mass-times  Mass Times" in out
    assert "elsewhere.org" not in out and "/give" not in out
    assert "Saturday Vigil 4:00 PM" in out
    assert main(["seed", "site", "st-anne-demo", "times"]) == 0  # read again: today's copy
    assert "(read earlier, http at" in capsys.readouterr().out
    assert calls == ["https://example.org/st-anne/times"]


def test_site_falls_back_to_the_browser_and_says_when_it_cant_read(tmp_path, monkeypatch):
    from pdf_extract.dioceses.web import Response
    from pdf_extract.seeding import site

    challenge = b"<html><title>Just a moment...</title>Enable JavaScript and cookies</html>"
    monkeypatch.setattr(site, "fetch", lambda url: Response(url, 403, url, "text/html",
                                                            challenge, error="HTTP 403"))
    rendered = "<p>Confession Saturday 3:00 PM</p>" * 30
    monkeypatch.setattr(site, "_browser_html", lambda url: (rendered, url))
    read = site.read_site("p", "https://example.org/", work_dir=tmp_path)
    assert read["via"] == "browser" and "Confession Saturday 3:00 PM" in read["text"]
    assert read["notes"] == ["plain request: HTTP 403"]

    def no_browser(url):
        raise RuntimeError("Missing X server or $DISPLAY")

    monkeypatch.setattr(site, "_browser_html", no_browser)
    with pytest.raises(SeedError, match="Could not read .*Missing X server"):
        site.read_site("p", "https://example.org/x", work_dir=tmp_path)


# ── Writing slots by command (`seed slot`, `summary`, `church-issue`, `block`) ──
ANNE = "st-anne-demo"
ANNE_BATCH = """\
# St. Anne, from the newest bulletin's page 2
include "mass Sat 17:00 note=Vigil" --src "latest p2: Saturday 5:00 PM" --why "R1: Masses box."
include "mass Sun 09:30,11:30" --src "latest p2: Sunday 9:30 AM and 11:30 AM" \\
    --why "R1: Masses box."
include "mass Tue,Thu 12:10" --src "latest: Tuesday and Thursday 12:10 PM" --page 2 \\
    --why "R1: Masses box."
include "confession Sat 3:30pm-4:30pm" --src "latest p2: Saturday 3:30 - 4:30 PM" \\
    --why "R1: Confessions box."
exclude - --src "latest p2: or by appointment" --why "R26: by appointment has no time."
include "mass 2026-10-13 12:10 cancelled note=Father on retreat" \\
    --src "latest p2: No Tuesday Mass on October 13 (Father on retreat)." \\
    --why "R1, R16: a dated cancellation after as_of."
ask "Add first-Friday Adoration, 9 AM to noon?" \\
    --option "*First Fridays 9 AM-noon" "adoration Fri 09:00-12:00 first" \\
    --option "Every Friday" "+ weeks=" --option "Leave out" \\
    --src "latest p2: First Friday of each month, 9:00 AM until noon" \\
    --why "Printed once; leaning to the weeks it names."
summary "One church; every slot is in the newest bulletin's boxes. Open: first-Friday Adoration."
church-issue "Fairport hospital chapel" "latest p2: Communion Wednesdays"
"""


def _start_anne(capsys) -> None:
    assert main(["seed", "start", ANNE]) == 0
    capsys.readouterr()


def test_slot_entry_specs_say_a_slot_in_a_few_words():
    from pdf_extract.seeding.slots import build_entries, format_entry, parse_entry_spec

    def one(text: str, churches=(SJ,)) -> dict[str, Any]:
        [entry] = build_entries(parse_entry_spec(text), list(churches))
        return entry

    assert one("mass Sat 4pm note=Vigil Mass, in Spanish") == {
        "church_slug": SJ, "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Saturday", "date": None, "start_time": "16:00", "end_time": None,
        "note": "Vigil Mass, in Spanish"}
    entry = one("adoration Thu 09:00-7pm season=sep-may")
    assert (entry["end_time"], entry["season"]) == ("19:00", {
        "start_month": 9, "start_day": None, "end_month": 5, "end_day": None})
    assert one("adoration Thu 09:00 season=9/15-5/31")["season"] == {
        "start_month": 9, "start_day": 15, "end_month": 5, "end_day": 31}
    assert one("confession Fri 18:00 1st,3rd")["weeks_of_month"] == ["first", "third"]
    skips = one("mass Sun 10:30 except=last")
    assert (skips["weeks_of_month"], skips["exclude_weeks"]) == (["last"], True)
    assert one("mass 2026-10-12 08:00 cancelled @holy-family", [HF, SJ])["church_slug"] == HF
    dated = one("mass 2026-10-12 noon cancelled", [HF])
    assert (dated["event_kind"], dated["date"], dated["day_of_week"], dated["start_time"],
            dated["cancelled"]) == ("specific_date", "2026-10-12", None, "12:00", True)
    many = build_entries(parse_entry_spec("mass Mon-Wed,Fri 07:00,08:00"), [SJ])
    assert [(e["day_of_week"][:3], e["start_time"]) for e in many] == [
        (d, t) for d in ("Mon", "Tue", "Wed", "Fri") for t in ("07:00", "08:00")]
    # `+` (and edit) change only what they name, on top of another entry.
    base = one("adoration Fri 09:45 first note=Holy Hour")
    [changed] = build_entries(parse_entry_spec("+ weeks= 10:00 note="), [SJ], base)
    assert changed == {**base, "weeks_of_month": [], "exclude_weeks": False,
                       "start_time": "10:00", "end_time": None, "note": None}
    assert format_entry(base) == f"adoration Fri 09:45 @{SJ} first note=Holy Hour"
    for text, message in [
        ("mass Sat 4:00", "must be 24-hour HH:MM"),
        ("Sat 16:00", "name its type"),
        ("mass 16:00", "name its day"),
        ("mass Sat", "give its time"),
        ("mass Sat 16:00 weeks=6th", "not a week of the month"),
        ("mass Sat 16:00 season=9", "both ends given"),
        ("mass Sat 16:00 sometimes", "don't know 'sometimes'"),
        ("mass Fri-Mon 16:00", "runs backwards"),
    ]:
        with pytest.raises(SeedError, match=message):
            build_entries(parse_entry_spec(text), [SJ])
    with pytest.raises(SeedError, match="several churches: name it with @"):
        build_entries(parse_entry_spec("mass Sat 16:00"), [HF, SJ])
    with pytest.raises(SeedError, match="could be"):
        build_entries(parse_entry_spec("mass Sat 16:00 @demo"), [HF, SJ])


def test_slot_batch_drafts_a_whole_parish_that_finalizes(demo_cli, capsys, tmp_path):
    _start_anne(capsys)
    plan = tmp_path / "plan.txt"
    plan.write_text(ANNE_BATCH)
    assert main(["seed", "slot", "batch", ANNE, str(plan)]) == 0
    out = capsys.readouterr().out
    assert f"{ANNE}: drafting, 9 slots, 1 open questions" in out
    assert "s1   include p2   mass Sat 17:00 @st-anne-demo-fairport note=Vigil  (1 src)" in out
    assert "church list: Fairport hospital chapel: Communion Wednesdays" in out
    saved = read_seed(ANNE, demo_cli["seeds_dir"])
    newest = saved["bulletins"][0]["content_hash"]
    by_id = {s["id"]: s for s in saved["slots"]}
    assert [by_id[i]["entry"]["day_of_week"] for i in ("s4", "s5")] == ["Tuesday", "Thursday"]
    # A source on the newest bulletin without a page takes the slot's --page.
    assert by_id["s4"]["sources"] == [{"source": "agent", "bulletin": newest[:8], "page": 2,
                                       "said": "Tuesday and Thursday 12:10 PM"}]
    assert by_id["s6"]["entry"]["start_time"] == "15:30"
    assert by_id["s7"]["entry"] is None and by_id["s7"]["decision"] == "exclude"
    ask = by_id["s9"]
    assert ask["status"] == "needs_human" and ask["page"] == 2
    assert [(o["label"], o.get("leaning", False), (o["entry"] or {}).get("weeks_of_month"))
            for o in ask["options"]] == [("First Fridays 9 AM-noon", True, ["first"]),
                                         ("Every Friday", False, []), ("Leave out", False, None)]
    assert saved["church_list_issues"] == [{"church": "Fairport hospital chapel",
                                            "said": "Communion Wednesdays",
                                            "bulletin": newest[:8], "page": 2}]
    assert main(["seed", "finalize", ANNE]) == 0
    assert capsys.readouterr().out.splitlines()[0] == f"{ANNE}: needs_review, 1 open questions  OK"

    assert main(["seed", "slot", "list", ANNE]) == 0
    listed = capsys.readouterr().out
    assert "s9   ask     p2   Add first-Friday Adoration, 9 AM to noon?" in listed
    assert "       * First Fridays 9 AM-noon = adoration Fri 09:00-12:00 " \
        "@st-anne-demo-fairport first" in listed
    assert main(["seed", "slot", "show", ANNE, "s8", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["slots"][0]["entry"]["cancelled"] is True


def test_cli_records_edits_displays_and_clears_weekly_omission(
    conn, demo_cli, seed, capsys, tmp_path,
):
    assessment = _weekly_omission_slot(seed)["weekly_omission"]
    seed["slots"] = [s for s in seed["slots"] if s["id"] != "s1"]
    write_seed_file(seed, demo_cli["seeds_dir"])
    previous, oldest = [b["content_hash"][:8] for b in seed["bulletins"][1:]]
    plan = tmp_path / "omission.txt"
    plan.write_text(
        f'include "mass Sat 16:00 @holy-family" --src "{previous},{oldest} p2: '
        'Holy Family: Saturday Vigil Mass 4 PM" --page - '
        f'--weekly-omission "{assessment["reason"]}" --why "R36: One omission."\n'
    )
    assert main(["seed", "slot", "batch", PARISH, str(plan)]) == 0
    saved = read_seed(PARISH, demo_cli["seeds_dir"])
    slot = next(s for s in saved["slots"] if "weekly_omission" in s)
    assert slot["weekly_omission"] == assessment
    assert slot["page"] is None and slot["answer"] is None
    assert _omission_problems(conn, saved) == []
    capsys.readouterr()
    assert main(["seed", "slot", "show", PARISH, slot["id"]]) == 0
    out = capsys.readouterr().out
    assert assessment["bulletin"] in out and assessment["reason"] in out

    assert main(["seed", "slot", "edit", PARISH, slot["id"], "--weekly-omission", "-"]) == 0
    assert "weekly_omission" not in _slot(read_seed(PARISH, demo_cli["seeds_dir"]), slot["id"])
    assert main(["seed", "slot", "edit", PARISH, slot["id"], "--page", "-",
                 "--weekly-omission", assessment["reason"]]) == 0
    assert _omission_problems(conn, read_seed(PARISH, demo_cli["seeds_dir"])) == []
    path = seed_path(PARISH, demo_cli["seeds_dir"])
    before = path.read_bytes()
    assert main(["seed", "slot", "edit", PARISH, slot["id"], "--weekly-omission", " "]) == 1
    assert "omission judgment" in capsys.readouterr().err
    assert path.read_bytes() == before


def test_cli_cannot_replace_a_reviewers_judgment_with_a_weekly_omission(
    demo_cli, seed, capsys,
):
    seed = _settle_all(seed)
    path = write_seed_file(seed, demo_cli["seeds_dir"])
    before = path.read_bytes()
    assert main(["seed", "slot", "edit", PARISH, "s16", "--weekly-omission",
                 "Only an omission."]) == 1
    assert "decision is the reviewer's" in capsys.readouterr().err
    assert path.read_bytes() == before


def test_cli_records_and_displays_website_schedule_assessments(demo_cli, capsys, tmp_path):
    _start_anne(capsys)
    plan = tmp_path / "website.txt"
    plan.write_text(
        'include "mass Sat 18:15" --src "web https://example.org/times: Saturday 6:15 PM" '
        '--website-current "The parish home page links this fall schedule." '
        '--website-context "The newest bulletin refers to the website for fall times." '
        '--why "Website schedule assessed in the newest bulletin context."\n'
        'summary "One church; the parish website supplies the fall Vigil schedule."\n'
    )
    assert main(["seed", "slot", "batch", ANNE, str(plan)]) == 0
    saved = read_seed(ANNE, demo_cli["seeds_dir"])
    slot = saved["slots"][0]
    assessment = slot["sources"][0]["schedule_check"]
    assert slot["page"] is None and slot["answer"] is None
    assert assessment["bulletin"] == saved["bulletins"][0]["content_hash"][:8]
    assert assessment["current_because"] == "The parish home page links this fall schedule."
    assert validate_seed(saved) == []
    assert main(["seed", "mark-read", ANNE, "latest"]) == 0
    assert main(["seed", "finalize", ANNE]) == 0
    assert read_seed(ANNE, demo_cli["seeds_dir"])["slots"][0]["sources"] == slot["sources"]
    capsys.readouterr()
    assert main(["seed", "slot", "show", ANNE, "s1"]) == 0
    out = capsys.readouterr().out
    assert assessment["checked_at"] in out
    assert assessment["current_because"] in out
    assert assessment["fits_because"] in out
    # Adding another assessment through edit uses the same validation and representation.
    assert main([
        "seed", "slot", "edit", ANNE, "s1", "--src",
        "web https://example.org/vigil: Fall Vigil Mass: Saturday 6:15 PM",
        "--website-current", "The current parish calendar links this schedule.",
        "--website-context", "The bulletin links that calendar for Vigil times.",
    ]) == 0
    assert len(read_seed(ANNE, demo_cli["seeds_dir"])["slots"][0]["sources"]) == 2
    assert main(["seed", "finalize", ANNE]) == 0


@pytest.mark.parametrize("flags, message", [
    (["--website-current", "Current home page."], "give both --website-current"),
    (["--website-context", "Fits the bulletin."], "give both --website-current"),
    (["--website-current", " ", "--website-context", "Fits."], "give both --website-current"),
    (["--website-current", "Current.", "--website-context", "Fits."],
     "website explanations need a web --src"),
])
def test_cli_rejects_incomplete_or_unquoted_website_assessments(demo_cli, capsys, flags, message):
    _start_anne(capsys)
    path = seed_path(ANNE, demo_cli["seeds_dir"])
    before = path.read_bytes()
    assert main(["seed", "slot", "include", ANNE, "mass Sat 18:15",
                 "--why", "Website schedule.", *flags]) == 1
    assert message in capsys.readouterr().err
    assert path.read_bytes() == before


def test_the_file_format_batch_example_writes_a_draft_that_finalizes(demo_cli, capsys):
    doc = (Path(__file__).resolve().parents[1] / ".claude/skills/draft-parish-seed/"
           "file-format.md").read_text(encoding="utf-8")
    example = doc.split("## Writing slots", 1)[1].split("```\n", 2)[1]
    for other in ("1ab3e7c2", "77d0be19", "5e60aa31"):  # older bulletins St. Anne lacks
        example = example.replace(other, "latest")
    _start_anne(capsys)
    Path("plan.txt").write_text(example)
    assert main(["seed", "slot", "batch", ANNE, "plan.txt"]) == 0
    capsys.readouterr()
    saved = read_seed(ANNE, demo_cli["seeds_dir"])
    assert len(saved["slots"]) == 14
    assert [s["entry"] for s in saved["slots"] if s["decision"] == "exclude"][-1] is None
    convent = [s for s in saved["slots"] if s.get("group") == "convent"]
    assert [s["options"][0]["entry"]["day_of_week"][:3] for s in convent] == [
        "Mon", "Tue", "Wed", "Thu", "Fri"]
    assert main(["seed", "finalize", ANNE]) == 0
    assert capsys.readouterr().out.splitlines()[0] == f"{ANNE}: needs_review, 2 open questions  OK"


def test_slot_writes_check_what_they_write_and_write_nothing_on_a_problem(demo_cli, seed, capsys):
    path = seed_path(PARISH, demo_cli["seeds_dir"])
    before = path.read_bytes()
    newest = seed["bulletins"][0]["content_hash"][:8]
    for args, message in [
        (["include", "mass Sat 16:00", "--src", "latest p2: Sat 4", "--why", "R1"],
         "several churches: name it with @"),
        (["include", "mass Sat 16:00 @holy-family", "--src", "latest p2: Sat 4", "--why", "R1"],
         "s1 and s18 are the same slot"),
        (["include", "mass Sat 18:00 @holy-family", "--src", "ffffffff p2: Sat", "--why", "R1"],
         "'ffffffff' names none of the file's bulletins"),
        (["include", "mass Sat 18:00 @holy-family", "--src", "Sat 6 PM", "--why", "R1"],
         "no `: ` after its head"),
        (["include", "mass Sat 18:00 @elsewhere-chapel", "--src", "latest p2: x", "--why", "R1"],
         "s18.entry: unknown_church"),
        (["ask", "Which?", "--option", "*A", "mass Sat 18:00 @holy-family", "--option", "*B",
          "--src", "latest p2: x", "--why", "?"], "exactly one option must be the one"),
        (["edit", "s99", "--why", "R1"], "no slot s99"),
        (["edit", "s1"], "say what to change"),
    ]:
        assert main(["seed", "slot", args[0], PARISH, *args[1:]]) == 1
        err = capsys.readouterr().err
        assert message in err, (args, err)
        assert path.read_bytes() == before
    with pytest.raises(SystemExit):
        main(["seed", "slot", "edit", PARISH, "s1", "--include", "--exclude"])
    assert "not allowed with argument" in capsys.readouterr().err
    # A slot left out may name a church elsewhere; a settled one without a rule warns.
    assert main(["seed", "slot", "exclude", PARISH, "mass Sat 18:00 @elsewhere-chapel",
                 "--src", f"{newest} p3: Mass at the chapel", "--why", "Elsewhere."]) == 0
    out = capsys.readouterr().out
    assert "s18  exclude p3   mass Sat 18:00 @elsewhere-chapel" in out
    assert "! s18: a settled slot's rationale starts with the rule it rests on" in out


def test_slot_edit_and_rm_change_what_they_name_and_keep_the_reviewers(demo_cli, seed, capsys):
    s17 = _slot(seed, "s17")
    s17.update(status="settled", decision="exclude", answer={
        "choice": 2, "by": "Reviewer", "at": "2026-10-10T12:00:00Z"})
    write_seed_file(seed, demo_cli["seeds_dir"])
    newest = seed["bulletins"][0]["content_hash"][:8]

    def run(*args: str) -> tuple[int, str]:
        code = main(["seed", "slot", *args])
        captured = capsys.readouterr()
        return code, captured.out + captured.err

    assert run("edit", PARISH, "s1", "--entry", "16:30 note=", "--src",
               f"{newest} p2: Sat 4:30")[0] == 0
    s1 = _slot(read_seed(PARISH, demo_cli["seeds_dir"]), "s1")
    assert (s1["entry"]["start_time"], s1["entry"]["note"], s1["entry"]["church_slug"]) == (
        "16:30", None, HF)
    assert len(s1["sources"]) == 3 and s1["rationale"] == _slot(seed, "s1")["rationale"]
    assert run("edit", PARISH, "s1", "--drop-src", "3")[0] == 0
    assert len(_slot(read_seed(PARISH, demo_cli["seeds_dir"]), "s1")["sources"]) == 2

    # A question settled by its leaning option, then asked again with a `+` option.
    assert run("edit", PARISH, "s16", "--include", "--why", "R1: weekly.")[0] == 0
    s16 = _slot(read_seed(PARISH, demo_cli["seeds_dir"]), "s16")
    assert (s16["status"], s16["decision"], s16["question"], s16["entry"]["day_of_week"]) == (
        "settled", "include", None, "Monday")
    assert run("edit", PARISH, "s16", "--ask", "Monday weekly?", "--option", "*Yes", "+",
               "--option", "Leave out")[0] == 0
    s16 = _slot(read_seed(PARISH, demo_cli["seeds_dir"]), "s16")
    assert (s16["status"], s16["entry"], s16["options"][0]["entry"]["day_of_week"]) == (
        "needs_human", None, "Monday")

    # The reviewer's answer stays: only evidence may be added to the slot.
    code, out = run("edit", PARISH, "s17", "--why", "R1")
    assert code == 1 and "answered by Reviewer" in out
    assert run("edit", PARISH, "s17", "--src", f"{newest} p2: Holy Hour")[0] == 0
    code, out = run("rm", PARISH, "s17")
    assert code == 1 and "it stays" in out
    assert run("rm", PARISH, "s11", "s12")[0] == 0
    ids = [s["id"] for s in read_seed(PARISH, demo_cli["seeds_dir"])["slots"]]
    assert "s11" not in ids and "s12" not in ids and "s13" in ids
    code, out = run("show", PARISH, "s17")
    assert f"[2] {newest} p2: Holy Hour" in out and "answered 2 by Reviewer" in out


def test_ask_about_several_days_asks_one_grouped_slot_each(demo_cli, seed, capsys):
    newest = seed["bulletins"][0]["content_hash"][:8]
    assert main(["seed", "slot", "ask", PARISH, "St. Joseph weekday Mass at 7 AM?",
                 "--option", "*Mon-Wed 7 AM", "mass Mon-Wed 07:00 @st-joseph",
                 "--option", "First weeks only", "+ first", "--option", "Leave out",
                 "--src", f"{newest} p2: Mon-Wed 7 AM", "--why", "Seen once."]) == 0
    capsys.readouterr()
    saved = read_seed(PARISH, demo_cli["seeds_dir"])
    asked = [s for s in saved["slots"] if s.get("group") == "s18"]
    assert [s["id"] for s in asked] == ["s18", "s19", "s20"]
    assert [s["options"][1]["entry"]["day_of_week"] for s in asked] == [
        "Monday", "Tuesday", "Wednesday"]
    assert all(s["options"][1]["entry"]["weeks_of_month"] == ["first"] for s in asked)
    assert validate_seed(saved, parish_slug=PARISH) == []
    # Another slot joins the group, taking its question.
    assert main(["seed", "slot", "ask", PARISH, "--group", "s18",
                 "--option", "*Mon-Wed 7 AM", "mass Thu 07:00 @st-joseph",
                 "--option", "First weeks only", "+ first", "--option", "Leave out",
                 "--src", f"{newest} p2: Thu 7 AM", "--why", "Seen once."]) == 0
    assert _slot(read_seed(PARISH, demo_cli["seeds_dir"]), "s21")["question"] == \
        "St. Joseph weekday Mass at 7 AM?"


def test_slot_batch_is_all_or_nothing_and_says_which_line(demo_cli, capsys):
    _start_anne(capsys)
    path = seed_path(ANNE, demo_cli["seeds_dir"])
    before = path.read_bytes()
    bad = 'include "mass Sat 17:00" --src "latest p2: Sat 5" --why "R1"\n# fine so far\n' \
          'include "mass Sun 9:30" --src "latest p2: Sun" --why "R1"\n'
    for text, message in [(bad, "line 3 (include): entry 'mass Sun 9:30': time '9:30'"),
                          ("frobnicate s1\n", "line 1: 'frobnicate' is not one of"),
                          ("rm\n", "line 1 (rm): the following arguments are required"),
                          ("", "the batch is empty")]:
        Path("plan.txt").write_text(text)
        assert main(["seed", "slot", "batch", ANNE, "plan.txt"]) == 1
        assert message in capsys.readouterr().err
        assert path.read_bytes() == before


def test_summary_church_issue_and_block_set_the_file(demo_cli, seed, capsys):
    newest = seed["bulletins"][0]["content_hash"][:8]
    assert main(["seed", "summary", PARISH, "Two churches, all clear."]) == 0
    assert main(["seed", "church-issue", PARISH, "Mall chapel", f"{newest} p2: Mon 12:15"]) == 0
    assert main(["seed", "church-issue", PARISH, "Mall chapel", "Mon 12:15 Mass"]) == 0
    assert main(["seed", "church-issue", PARISH, "Hospital", "p3: Sun 8 AM"]) == 0
    saved = read_seed(PARISH, demo_cli["seeds_dir"])
    assert saved["summary"] == "Two churches, all clear."
    assert saved["church_list_issues"] == [{"church": "Mall chapel", "said": "Mon 12:15 Mass"},
                                           {"church": "Hospital", "said": "Sun 8 AM", "page": 3}]
    assert main(["seed", "church-issue", PARISH, "Hospital", "--rm"]) == 0
    assert main(["seed", "block", PARISH, "No bulletin prints a schedule."]) == 0
    saved = read_seed(PARISH, demo_cli["seeds_dir"])
    assert len(saved["church_list_issues"]) == 1
    assert (saved["status"], saved["blocked_reason"]) == (
        "blocked", "No bulletin prints a schedule.")
    assert main(["seed", "block", PARISH, "--clear", "--json"]) == 0
    capsys.readouterr()
    assert read_seed(PARISH, demo_cli["seeds_dir"])["status"] == "drafting"


def test_slot_writes_refuse_an_approved_file(demo_cli, seed, capsys):
    path = write_seed_file(_approved(seed), demo_cli["seeds_dir"])
    before = path.read_bytes()
    for args in (["slot", "include", PARISH, "mass Sat 18:00 @holy-family", "--src",
                  "latest p2: x", "--why", "R1"], ["slot", "rm", PARISH, "s1"],
                 ["summary", PARISH, "x"], ["block", PARISH, "x"]):
        assert main(["seed", *args]) == 1
        assert "belongs to its reviewer" in capsys.readouterr().err
    assert path.read_bytes() == before
    assert main(["seed", "slot", "list", PARISH]) == 0  # reading is fine
