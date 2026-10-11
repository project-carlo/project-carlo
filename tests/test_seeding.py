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
from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, set_store
from pdf_extract.classifiers.seed_ask import GEMINI_MODEL, OPENAI_MODEL, SeedAsker
from pdf_extract.db import create_db, ensure_db
from pdf_extract.labeling.demo import build_demo
from pdf_extract.labeling.labels import write_label
from pdf_extract.labeling.server import LabelerApp, make_server
from pdf_extract.report import render_seeds
from pdf_extract.schedule.store import live_entries, update_mode_parishes
from pdf_extract.seeding import calls as seed_calls
from pdf_extract.seeding.checks import check_seed
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
from pdf_extract.seeding.loader import is_loaded, load_approved_seeds
from pdf_extract.seeding.queries import (
    SeedContext,
    SeedError,
    export_pdf,
    history,
    list_bulletins,
    parish_bulletins,
    pick,
    render_pages,
    resolve_bulletin,
    start_eval_run,
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
    (lambda s: _slot(s, "s1")["sources"][0].update(source="c9"), "agent, history or a call"),
    (lambda s: _slot(s, "s1")["entry"].update(start_time="4:00 PM"), "HH:MM"),
    (lambda s: _slot(s, "s1")["entry"].pop("note"), "missing note"),
    (lambda s: _slot(s, "s1").update(decision=None), "include or exclude for a settled"),
    (lambda s: _slot(s, "s2").update(id="s1"), "used twice"),
    (lambda s: s.update(status=READY), "questions are still open"),
    (lambda s: s.update(status=APPROVED), "questions are still open"),
    (lambda s: s.update(status="blocked"), "blocked_reason"),
    (lambda s: s.update(as_of=None), "as_of is required"),
])
def test_validate_seed_rejects_malformed_files(seed, change, message):
    change(seed)
    errors = validate_seed(seed, parish_slug=PARISH)
    assert any(message in e for e in errors), errors


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
    assert listed["not_shown"] == 0


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

