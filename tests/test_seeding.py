"""Seeding believed schedules (docs/seeding-plan.md): seed files, the agent's tools,
the labeler's review, loading approved seeds, and scoring test runs."""

from __future__ import annotations

import copy
import http.client
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
from pdf_extract.labeling.labels import write_label
from pdf_extract.labeling.server import LabelerApp, make_server
from pdf_extract.report import render_seeds
from pdf_extract.schedule.store import live_entries, update_mode_parishes
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
    pick,
    recent_history,
    render_pages,
    resolve_bulletin,
    start_eval_run,
    stored_pdfs,
)
from pdf_extract.seeding.review import (
    SeedReviewError,
    save_reviewed_seed,
    seed_detail,
    seed_queue,
)
from pdf_extract.seeding.score import score_parish, score_run
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
def test_bulletins_newest_first_and_hidden_after_a_cutoff(conn):
    bulletins = parish_bulletins(conn, PARISH)
    assert [b["published_date"] for b in bulletins] == ["2026-09-27", "2026-09-20"]
    hidden = parish_bulletins(conn, PARISH, cutoff="2026-09-19T00:00:00Z")
    assert [b["published_date"] for b in hidden] == ["2026-09-20"]
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
    with pytest.raises(SeedError, match="cutoff"):
        resolve_bulletin(conn, PARISH, newest["content_hash"][:10],
                         cutoff="2026-09-19T00:00:00Z")
    with pytest.raises(SeedError, match="Parish not found"):
        resolve_bulletin(conn, "no-such-parish", "latest")


def test_history_is_extract_modes_events_per_bulletin(conn):
    result = history(conn, PARISH)
    assert [b["published_date"] for b in result["bulletins"]] == ["2026-09-27", "2026-09-20"]
    vigil = result["bulletins"][1]["events"]
    assert {"church_slug": HF, "event_type": "mass", "day_of_week": "Saturday",
            "start_time": "16:00"}.items() <= next(
        e for e in vigil if e["day_of_week"] == "Saturday" and e["event_type"] == "mass").items()
    assert history(conn, PARISH, cutoff="2026-09-19T00:00:00Z")["bulletins"][0][
        "published_date"] == "2026-09-20"


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


def test_pick_leaves_out_drafted_parishes_and_takes_one_church_first(conn, demo):
    picked = pick(conn, seeds_dir=demo["seeds_dir"], limit=0)
    slugs = [p["parish"] for p in picked["parishes"]]
    assert PARISH not in slugs  # it has a seed file
    assert set(slugs) == {"st-anne-demo", "our-lady-demo"}
    assert all(p["churches"] == 1 for p in picked["parishes"])


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


# ── Loading ─────────────────────────────────────────────────────────────────
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


# ── Test runs ───────────────────────────────────────────────────────────────
def test_a_test_run_hides_newer_bulletins_and_scores_the_drafts(conn, demo, seed, tmp_path):
    newest = parish_bulletins(conn, PARISH)[0]
    labels_dir = tmp_path / "labels"
    events = []
    for slot in included_slots(_settle_all(seed)):
        events.append({**slot["entry"], "page_number": 2, "origin": "human", "optional": None})
    events[0] = {**events[0], "start_time": "17:00"}  # the label says 5 PM for the vigil
    write_label({
        "schema_version": 1, "parish_slug": PARISH, "content_hash": newest["content_hash"],
        "source_url": "", "status": "done",
        "flags": {f: False for f in ("wrong_bulletin", "unreadable", "no_schedule",
                                     "church_missing", "conflicting_info")},
        "published_date": "2026-09-27", "note": "", "labeler": "t", "seconds_spent": 1,
        "updated_at": "", "events": events,
    }, parish_slug=PARISH, content_hash=newest["content_hash"], source_url="",
        labels_dir=labels_dir)
    evals_dir = tmp_path / "seed-evals"
    started = start_eval_run(conn, "try-1", labels_dir=labels_dir, evals_dir=evals_dir)
    assert [p["parish"] for p in started["parishes"]] == [PARISH]
    ctx = SeedContext.for_run("try-1", evals_dir=evals_dir)
    assert ctx.cutoff(PARISH) == newest["fetched_at"]
    with pytest.raises(SeedError, match="not in test run"):
        ctx.cutoff("st-anne-demo")
    write_seed_file(seed, ctx.seeds_dir)
    assert check_seed(conn, seed, parish_slug=PARISH, cutoff=ctx.cutoff(PARISH)) == []

    report = score_run("try-1", labels_dir=labels_dir, ctx=ctx)
    parish = report["parishes"][PARISH]
    assert parish["settled_included"] == 14
    assert parish["settled"]["strict"]["found"] == 13  # the vigil is at the wrong time
    assert parish["open_questions"] == 2
    assert all(x["matched_label"] for x in parish["leaning"])
    assert (evals_dir / "try-1" / "report.md").read_text().startswith("# Seeding test run")


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


def test_init_prints_where_the_draft_starts(demo_cli, capsys):
    assert main(["seed", "init", "st-anne-demo"]) == 0
    out = capsys.readouterr().out
    assert "a draft listing 1 bulletins" in out
    assert "https://example.org/st-anne" in out
    assert "st-anne-demo-fairport                    St. Anne Church, 9 Church St, Fairport" in out
    assert "newest PDF: data/seed-work/st-anne-demo/" in out
    assert main(["seed", "init", "st-anne-demo"]) == 1
    assert "seed brief st-anne-demo" in capsys.readouterr().err


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


def test_total_precision_leaves_out_slots_matching_only_optional_rows():
    sunday = {"church_slug": HF, "event_type": "mass", "event_kind": "weekly",
              "day_of_week": "Sunday", "date": None, "start_time": "09:00", "end_time": None,
              "cancelled": False, "weeks_of_month": [], "season": None, "note": None}
    monday = {**sunday, "day_of_week": "Monday", "start_time": "08:00"}
    slots = [{"id": f"s{i}", "status": "settled", "decision": "include", "entry": e}
             for i, e in enumerate((sunday, monday))]
    label = {"events": [{**sunday, "optional": None}, {**monday, "optional": "include"}]}
    parish = score_parish({"slots": slots, "calls": []}, label, "2026-10-01")
    assert parish["settled_scored"] == 1
    assert parish["settled"]["strict"] == {"precision": 1.0, "recall": 1.0, "found": 1,
                                           "covered": 1}


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


def test_cli_starts_an_eval_and_routes_all_parish_commands(routed_cli, seed, capsys):
    newest = seed["bulletins"][0]
    labels = Path("data/labels") / PARISH
    labels.mkdir(parents=True)
    (labels / f"{newest['content_hash']}.json").write_text('{"status": "done"}')
    production = {**seed, "summary": "Production must remain unchanged."}
    write_seed_file(production)

    assert main(["seed", "pick", "--labeled", "--eval", "new-run"]) == 0
    manifest = Path("data/seed-evals/new-run/run.json")
    original_manifest = manifest.read_bytes()
    ctx = SeedContext.for_run("new-run")
    assert ctx.cutoff(PARISH) == newest["fetched_at"]
    assert main(["seed", "init", PARISH, "--eval", "new-run"]) == 0
    assert read_seed(PARISH, ctx.seeds_dir)["status"] == "drafting"
    assert main(["seed", "mark-read", PARISH, "latest", "--eval", "new-run"]) == 0
    assert read_seed(PARISH, ctx.seeds_dir)["bulletins"][0]["read"]
    assert main(["seed", "church", "rochester", "--eval", "new-run"]) == 0

    # Picking again keeps cutoffs; --resume offers an interrupted eval draft.
    capsys.readouterr()
    assert main(["seed", "pick", "--labeled", "--eval", "new-run", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["parishes"] == []
    assert main(["seed", "pick", "--labeled", "--eval", "new-run", "--resume",
                 "--json"]) == 0
    picked = json.loads(capsys.readouterr().out)
    assert [p["parish"] for p in picked["parishes"]] == [PARISH]
    assert manifest.read_bytes() == original_manifest

    write_seed_file(seed, ctx.seeds_dir)
    assert main(["seed", "finalize", PARISH, "--eval", "new-run"]) == 0
    assert main(["seed", "check", "--all", "--eval", "new-run"]) == 0
    capsys.readouterr()
    assert main(["seed", "status", "--eval", "new-run", "--json"]) == 0
    status = json.loads(capsys.readouterr().out)
    assert status["eval_run"] == "new-run"
    assert status["seeds"][0]["loaded"] is None
    assert read_seed(PARISH) == production


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


def test_pick_resume_offers_only_unfinished_existing_drafts(conn, demo, seed):
    seed["status"] = "drafting"
    write_seed_file(seed, demo["seeds_dir"])
    assert PARISH not in {p["parish"] for p in pick(conn, seeds_dir=demo["seeds_dir"])["parishes"]}
    assert PARISH in {p["parish"] for p in pick(
        conn, seeds_dir=demo["seeds_dir"], resume=True)["parishes"]}
    for status in (READY, APPROVED, "blocked"):
        write_seed_file({**seed, "status": status}, demo["seeds_dir"])
        assert PARISH not in {p["parish"] for p in pick(
            conn, seeds_dir=demo["seeds_dir"], resume=True)["parishes"]}


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


def test_historical_evals_reject_live_website_evidence(conn, seed):
    _slot(seed, "s1")["sources"].append(
        {"source": "website", "url": "https://example.org/times", "said": "Saturday 4 PM"})
    assert check_seed(conn, seed, parish_slug=PARISH) == []
    assert any("website sources are not allowed" in p for p in check_seed(
        conn, seed, parish_slug=PARISH, cutoff=seed["as_of"]))


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


def test_mark_read_obeys_the_eval_cutoff_and_preserves_the_file(routed_cli, seed, capsys):
    old = seed["bulletins"][1]
    folder = Path("data/seed-evals/old-run")
    folder.mkdir(parents=True)
    (folder / "run.json").write_text(json.dumps({"parishes": {
        PARISH: {"fetched_at": old["fetched_at"], "label_hash": old["content_hash"]}}}))
    assert main(["seed", "init", PARISH, "--eval", "old-run"]) == 0
    path = seed_path(PARISH, folder / "seeds")
    before = path.read_bytes()
    assert main(["seed", "mark-read", PARISH, seed["bulletins"][0]["content_hash"],
                 "--eval", "old-run"]) == 1
    assert "cutoff" in capsys.readouterr().err
    assert path.read_bytes() == before
    assert main(["seed", "mark-read", PARISH, "latest", "--eval", "old-run"]) == 0
    marked = read_seed(PARISH, folder / "seeds")
    assert [(b["content_hash"], b["read"]) for b in marked["bulletins"]] == [
        (old["content_hash"], True)]


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
    assert main(["seed", "init", PARISH, "--resume"]) == 1
    assert main(["seed", "mark-read", PARISH, "latest"]) == 1
    assert "belongs to its reviewer" in capsys.readouterr().err
    assert path.read_bytes() == before
