"""The second opinion in a seed file (docs/seed-second-opinion-plan.md, Phase 1): the call
and its stored reply, revealing it, the comparison on every check, resolving each
difference, and the `seed opinion` commands. Replies are recorded, never asked for."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from pdf_extract.__main__ import main
from pdf_extract.blobstore import CachedBlobStore, LocalBlobStore, set_store
from pdf_extract.classifiers.schedule_update import RawReply
from pdf_extract.labeling.demo import build_demo
from pdf_extract.seeding import cli as seed_cli
from pdf_extract.seeding import files
from pdf_extract.seeding import opinion as compare_mod
from pdf_extract.seeding import second_opinion as so
from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.files import read_seed, validate_seed, write_seed_file
from pdf_extract.seeding.queries import SeedContext
from pdf_extract.seeding.review import approve_seed
from pdf_extract.storage import connect_db

PARISH = "holy-family-demo"
HF = "holy-family-demo-rochester"
SJ = "st-joseph-demo-penfield"
NEW = "dbb914e75c4d781a45ae502ca56352ba0a32c58154f50cad03538dfe04c7594d"
OLD = "26da817ae4a7107cadd8cc68545ee92a7507efa628c0dffbeab01c1a92d607a6"
BULLETINS = [
    {"content_hash": NEW, "fetched_at": "2026-09-25T21:00:00Z", "published_date": "2026-09-27"},
    {"content_hash": OLD, "fetched_at": "2026-09-18T21:00:00Z", "published_date": "2026-09-20"},
]
CHURCHES = [{"slug": HF, "name": "Holy Family"}, {"slug": SJ, "name": "St. Joseph"}]


# ── A recorded reply ────────────────────────────────────────────────────────
def _clock(hhmm: str) -> str:
    h, m = map(int, hhmm.split(":"))
    return f"{(h - 1) % 12 + 1}:{m:02d} {'AM' if h < 12 else 'PM'}"


def weekly(church: str, day: str, start: str, end: str | None = None, *, weeks=(),
           season=None, quote: str = "", page: int = 2, bulletin: str = "B1") -> dict[str, Any]:
    return {"church_slug": church, "day_of_week": day, "start_time": _clock(start),
            "end_time": _clock(end) if end else None, "weeks_of_month": list(weeks),
            "exclude_weeks": False, "season": season, "note": None,
            "evidence": [{"bulletin": bulletin, "page": page,
                          "quote": quote or f"{day} {_clock(start)}"}]}


def dated(church: str, day: str, start: str, *, quote: str = "", page: int = 3) -> dict[str, Any]:
    return {"church_slug": church, "date": day, "start_time": _clock(start), "end_time": None,
            "note": None, "evidence": [{"bulletin": "B1", "page": page,
                                        "quote": quote or f"{day} {_clock(start)}"}]}


SEPT_MAY = {"start_month": "September", "start_day": None, "end_month": "May", "end_day": None}


def reply(*, weekday: str = "08:00", extra_masses=(), adorations=None) -> str:
    """luna's reading of the demo parish: all the demo seed's slots, the weekday Masses at
    `weekday`, and `extra_masses` besides."""
    masses = [
        weekly(HF, "Saturday", "16:00", quote="Sat 4:00 PM Vigil"),
        weekly(HF, "Sunday", "08:00"), weekly(HF, "Sunday", "10:30"),
        weekly(SJ, "Sunday", "09:00"), weekly(SJ, "Wednesday", "19:00"),
        weekly(HF, "Monday", "08:00"),
        *[weekly(HF, day, weekday, quote=f"Tue-Fri {_clock(weekday)}")
          for day in ("Tuesday", "Wednesday", "Thursday", "Friday")],
        *extra_masses,
    ]
    payload = {
        "bulletins": [{"bulletin": "B1", "published_date": "2026-09-27", "wrong_bulletin": False},
                      {"bulletin": "B2", "published_date": "2026-09-20", "wrong_bulletin": False}],
        "weekly_schedule": {
            "masses": masses,
            "confessions": [weekly(HF, "Saturday", "15:00", "15:45"),
                            weekly(SJ, "Friday", "18:00", "19:00", weeks=["first"])],
            "adorations": adorations if adorations is not None else [
                weekly(HF, "Thursday", "09:00", "19:00", season=SEPT_MAY),
                weekly(SJ, "Tuesday", "18:00", "19:00", weeks=["first", "third", "fourth",
                                                               "fifth"])],
        },
        "single_events": {"masses": [dated(SJ, "2026-10-02", "19:00")], "confessions": [],
                          "adorations": []},
        "cancellations": {"masses": [dated(HF, "2026-10-05", "08:00")], "confessions": [],
                          "adorations": []},
        "church_list_needs_review": False,
    }
    return json.dumps(payload)


def record(text: str, **extra: Any) -> dict[str, Any]:
    """What `run_opinion` stores, for a recorded reply."""
    return {"request_key": "k" * 32, "parish": PARISH, "model": "gpt-6-luna",
            "version": "gpt-6-luna+seed-opinion-test", "today": "2026-09-25",
            "bulletins": BULLETINS, "churches": CHURCHES, "text": text,
            "usage": {"input_tokens": 9000, "output_tokens": 4000}, "service_tier": "flex",
            "served_model": "gpt-6-luna", "latency_ms": 1, "cost_usd": 0.0031,
            "asked_at": "2026-09-25T22:00:00Z", "cached": False, **extra}


class FakeCaller:
    """`SeedOpinionCaller` with a recorded reply (or an error), counting its calls."""

    model = "gpt-6-luna"

    def __init__(self, text: str | None = None, error: Exception | None = None) -> None:
        self.text, self.error, self.calls = text or reply(), error, []

    @property
    def version(self) -> str:
        return "gpt-6-luna+seed-opinion-test"

    def opinion(self, pdfs: list[bytes], context: str) -> RawReply:
        self.calls.append((pdfs, context))
        if self.error is not None:
            raise self.error
        return RawReply(text=self.text, served_model=self.model,
                        usage={"input_tokens": 9000, "output_tokens": 4000}, latency_ms=5,
                        service_tier="flex")


@pytest.fixture
def demo(tmp_path: Path) -> dict[str, Path]:
    paths = build_demo(tmp_path / "demo")
    set_store(CachedBlobStore(LocalBlobStore(paths["root"])))
    return paths


@pytest.fixture
def conn(demo):
    c = connect_db(demo["db_path"])
    yield c
    c.close()


@pytest.fixture
def seed(demo) -> dict[str, Any]:
    loaded = read_seed(PARISH, demo["seeds_dir"])
    assert loaded is not None
    return loaded


def revealed(seed: dict[str, Any], text: str | None = None) -> dict[str, Any]:
    return so.reveal(seed, record(text or reply(weekday="08:30")), at="2026-09-26T10:00:00Z")


def items(seed: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {d["id"]: d for d in seed["second_opinion"]["differences"]}


def open_items(seed: dict[str, Any]) -> list[dict[str, Any]]:
    return so.unresolved(seed)


def slot(seed: dict[str, Any], sid: str) -> dict[str, Any]:
    return next(s for s in seed["slots"] if s["id"] == sid)


# ── The call ────────────────────────────────────────────────────────────────
def test_the_bulletins_are_the_newest_distinct_weeks_with_a_pdf_up_to_the_drafters_newest():
    listed = [
        {"content_hash": "a" * 64, "fetched_at": "2026-10-20T10:00:00Z", "published_date": "2026-10-25"},
        {"content_hash": "b" * 64, "fetched_at": "2026-10-13T10:00:00Z", "published_date": "2026-10-18"},
        {"content_hash": "c" * 64, "fetched_at": "2026-10-14T10:00:00Z", "published_date": "2026-10-18"},
        {"content_hash": "d" * 64, "fetched_at": "2026-10-06T10:00:00Z", "published_date": "2026-10-11"},
        {"content_hash": "e" * 64, "fetched_at": "2026-09-29T10:00:00Z", "published_date": None},
        {"content_hash": "f" * 64, "fetched_at": "2026-09-22T10:00:00Z", "published_date": "2026-09-27"},
        {"content_hash": "9" * 64, "fetched_at": "2026-09-15T10:00:00Z", "published_date": "2026-09-20"},
    ]
    gone = {"d" * 64}
    picked = so.pick_bulletins(listed, lambda h: h not in gone, as_of="2026-10-14T10:00:00Z")
    # The newer issue is past the drafter's newest; the 18th's two fetches count once (the
    # newest); the 11th's PDF is gone; an undated issue is its own week.
    assert [b["content_hash"][0] for b in picked] == ["c", "e", "f", "9"]
    assert len(so.pick_bulletins(listed, lambda h: True, most=2)) == 2


def test_a_reply_is_stored_under_its_request_key_and_never_paid_twice():
    stored: dict[str, dict[str, Any]] = {}

    class Store:
        def get(self, key):
            return stored.get(key)

        def put(self, key, value):
            stored[key] = value

    caller = FakeCaller()
    pdfs = {NEW: b"%PDF new", OLD: b"%PDF old"}
    first = so.run_opinion(caller, PARISH, BULLETINS, CHURCHES, Store(),
                           read_pdf=lambda p, h: pdfs[h])
    again = so.run_opinion(caller, PARISH, BULLETINS, CHURCHES, Store(),
                           read_pdf=lambda p, h: pdfs[h])
    assert len(caller.calls) == 1 and (first["cached"], again["cached"]) == (False, True)
    pdf_list, context = caller.calls[0]
    assert pdf_list == [b"%PDF new", b"%PDF old"]  # B1 newest
    assert "2026-09-25 (Friday)" in context and "B2: issue 2026-09-20" in context
    assert list(stored) == [first["request_key"]] and first["cost_usd"] > 0
    # Another bulletin set, other churches or another prompt version is another request.
    key = so.request_key(caller.version, PARISH, BULLETINS, CHURCHES, so.today_of(BULLETINS))
    assert key == first["request_key"]
    assert so.request_key("v2", PARISH, BULLETINS, CHURCHES, so.today_of(BULLETINS)) != key
    assert so.request_key(caller.version, PARISH, BULLETINS[:1] + BULLETINS, CHURCHES,
                          so.today_of(BULLETINS)) != key
    with pytest.raises(so.OpinionError, match="1 bulletin"):
        so.run_opinion(caller, PARISH, BULLETINS[:1], CHURCHES, Store(),
                       read_pdf=lambda p, h: pdfs[h])


# ── Revealing it ────────────────────────────────────────────────────────────
def test_reveal_writes_the_opinion_its_call_and_its_differences(conn, seed):
    out = revealed(seed)
    assert validate_seed(out, parish_slug=PARISH) == []
    sec = out["second_opinion"]
    assert sec["call"] == "c1" and out["calls"][-1]["kind"] == "opinion"
    assert out["calls"][-1]["bulletin"] == NEW and sec["cost_usd"] == 0.0031
    assert [b["label"] for b in sec["bulletins"]] == ["B1", "B2"]
    assert sec["entries_sha256"] == so.entries_sha(sec["entries"])
    found = items(out)
    # Tue-Fri at 8:30 against the seed's 8:00: one difference, grouped.
    differs = next(d for d in found.values() if d["kind"] == "differs")
    assert differs["slots"] == ["s12", "s13", "s14", "s15"]
    assert differs["fields"] == ["start time"] and differs["resolution"] is None
    assert differs["opinion_said"].startswith("mass Tue,Wed,Thu,Fri 08:30")
    assert [d["kind"] for d in found.values()] == ["differs"]  # it agrees with the rest
    # The slots luna agrees with cite its call.
    vigil = [s for s in slot(out, "s1")["sources"] if s["source"] == "c1"]
    assert vigil == [{"source": "c1", "bulletin": NEW, "page": 2,
                      "said": "gpt-6-luna read the same: B1 p2 “Sat 4:00 PM Vigil”"}]
    leaning = [s for s in slot(out, "s16")["sources"] if s["source"] == "c1"]
    assert leaning and "as the leaning option" in leaning[0]["said"]
    assert not [s for s in slot(out, "s12")["sources"] if s["source"] == "c1"]
    # The check now wants each open difference resolved.
    problems = check_seed(conn, out, parish_slug=PARISH)
    assert any("difference d" in p and "unresolved" in p and "Tue-Fri 8:30 AM" in p
               for p in problems)


def test_revealing_again_replaces_the_opinion_and_keeps_the_old_call(seed):
    first = revealed(seed)
    again = so.reveal(first, record(reply()), at="2026-09-27T10:00:00Z")
    assert [c["id"] for c in again["calls"]] == ["c1", "c2"]
    assert again["second_opinion"]["call"] == "c2"
    sources = [s["source"] for s in slot(again, "s1")["sources"]]
    assert "c2" in sources and "c1" not in sources
    assert validate_seed(again, parish_slug=PARISH) == []


def test_an_unreadable_reply_is_not_revealed(seed):
    with pytest.raises(so.OpinionError):
        so.reveal(seed, record("not json"))


def test_the_kinds_are_the_comparisons():
    assert files.DIFFERENCE_KINDS == compare_mod.KINDS
    assert files.AUTO_REASONS == compare_mod.RESOLVED_REASONS


@pytest.mark.parametrize("change, message", [
    (lambda s: s["second_opinion"].update(extra=1), "unknown extra"),
    (lambda s: s["second_opinion"].pop("entries_sha256"), "missing entries_sha256"),
    (lambda s: s["second_opinion"].update(call="c9"), "must name one of the file's calls"),
    (lambda s: s["second_opinion"]["bulletins"][0].update(label="X"), "label must be B1"),
    (lambda s: s["second_opinion"]["differences"][0].update(kind="odd"), "kind must be one of"),
    (lambda s: s["second_opinion"]["differences"][0].update(opinion=["o99"]),
     "must name the section's entries"),
    (lambda s: s["second_opinion"]["differences"][0].update(resolution={"how": "maybe"}),
     "how is one of"),
    (lambda s: s["second_opinion"]["differences"][0].update(resolution={
        "how": "kept", "src": [{"source": "agent", "bulletin": NEW, "page": None,
                                "said": "Tue 8 AM"}], "why": "R1: printed",
        "at": "2026-09-26T10:00:00Z"}), "must cite a bulletin page"),
    (lambda s: s["second_opinion"]["differences"][0].update(resolution={
        "how": "kept", "src": [{"source": "agent", "bulletin": NEW, "page": 2,
                                "said": "Tue 8 AM"}], "why": "it is right",
        "at": "2026-09-26T10:00:00Z"}), "citing its rule"),
    (lambda s: s["second_opinion"]["differences"][0].update(resolution={
        "how": "auto", "reason": "a hunch"}), "reason must be one of"),
])
def test_validation_rejects_a_malformed_second_opinion(seed, change, message):
    out = revealed(seed)
    change(out)
    problems = validate_seed(out, parish_slug=PARISH)
    assert any(message in p for p in problems), problems


def test_a_file_without_one_is_valid_as_before(seed):
    assert "second_opinion" not in seed and validate_seed(seed, parish_slug=PARISH) == []
    assert so.refresh(seed) is seed and so.stats(seed) is None and so.unresolved(seed) == []


# ── The opinion's entries are the dispatcher's ──────────────────────────────
def test_editing_the_opinions_entries_fails_the_check(conn, seed):
    out = revealed(seed)
    sha = out["second_opinion"]["entries_sha256"]
    edited = copy.deepcopy(out)
    edited["second_opinion"]["entries"][0]["entry"]["start_time"] = "17:00"
    problems = check_seed(conn, edited, parish_slug=PARISH)
    assert any("entries were changed" in p for p in problems)
    # Rehashed in the file too: the dispatcher's hash still tells.
    edited["second_opinion"]["entries_sha256"] = so.entries_sha(
        edited["second_opinion"]["entries"])
    assert not any("entries were changed" in p for p in check_seed(conn, edited,
                                                                   parish_slug=PARISH))
    assert any("entries were changed" in p
               for p in check_seed(conn, edited, parish_slug=PARISH, opinion_sha=sha))
    assert so.expected_shas({so.OPINION_SHA_ENV: f"{PARISH}={sha} other=abc"}) == {
        PARISH: sha, "other": "abc"}


# ── Resolving differences ───────────────────────────────────────────────────
def _resolve_all_but(seed: dict[str, Any], kind: str) -> dict[str, Any]:
    """Keep every open difference but those of `kind`, with a page and a rule."""
    for d in open_items(seed):
        if d["kind"] != kind:
            seed = so.keep(seed, d["id"], [{"source": "agent", "bulletin": NEW, "page": 3,
                                            "said": "the bulletin's words"}],
                           "R24: not a service POLICY counts.")
    return seed


def test_a_difference_the_seed_no_longer_has_is_resolved_by_the_change(seed):
    out = _resolve_all_but(revealed(seed), "differs")
    differs = next(d for d in items(out).values() if d["kind"] == "differs")
    assert [d["id"] for d in open_items(out)] == [differs["id"]]
    for sid in ("s12", "s13", "s14", "s15"):
        slot(out, sid)["entry"]["start_time"] = "08:30"
    out = so.refresh(out)
    assert items(out)[differs["id"]]["resolution"] == {"how": "changed"}
    assert open_items(out) == []
    assert so.stats(out)["changed"] == 1
    # The changed slots now agree, and cite the call.
    assert any(s["source"] == "c1" for s in slot(out, "s12")["sources"])


def test_a_question_with_the_opinions_reading_as_an_option_resolves_it(seed):
    out = _resolve_all_but(revealed(seed), "differs")
    differs = next(d for d in open_items(out))
    for sid in ("s12", "s13", "s14", "s15"):
        s = slot(out, sid)
        entry = s["entry"]
        s.update(status="needs_human", decision=None, entry=None, group="weekday",
                 question="Weekday Mass at 8:00 or 8:30?",
                 options=[{"label": "8:00", "leaning": True, "entry": entry},
                          {"label": "8:30", "leaning": False,
                           "entry": {**entry, "start_time": "08:30"}}])
    out = so.refresh(out)
    assert open_items(out) == []
    assert items(out)[differs["id"]]["resolution"] == {"how": "asked"}
    st = so.stats(out)
    assert st["asked"] >= 1 and st["unresolved"] == 0


def test_a_kept_difference_needs_a_page_and_a_rule_and_stays_kept(seed):
    out = revealed(seed)
    first = open_items(out)[0]["id"]
    page = [{"source": "agent", "bulletin": NEW, "page": 2, "said": "Tue-Fri 8:00 AM"}]
    with pytest.raises(so.OpinionError, match="bulletin page"):
        so.keep(out, first, [{"source": "agent", "bulletin": NEW, "page": None,
                              "said": "x"}], "R1: printed")
    with pytest.raises(so.OpinionError, match="citing its rule"):
        so.keep(out, first, page, "it's right")
    with pytest.raises(so.OpinionError, match="no difference d99"):
        so.keep(out, "d99", page, "R1: printed")
    out = so.keep(out, first, page, "R1: the schedule box of both bulletins prints 8:00.")
    assert validate_seed(out, parish_slug=PARISH) == []
    assert so.refresh(out) == out  # comparing again changes nothing
    assert items(out)[first]["resolution"]["how"] == "kept"
    assert so.stats(out)["kept"] == 1


def test_a_change_after_a_keep_drops_it_and_a_new_difference_needs_resolving(seed):
    out = _resolve_all_but(revealed(seed), "")
    assert open_items(out) == []
    differs = next(d for d in items(out).values() if d["kind"] == "differs")
    # A later edit (after a send-back, say) makes the weekday Masses 9:00: the kept
    # difference is gone, and a new one opens.
    for sid in ("s12", "s13", "s14", "s15"):
        slot(out, sid)["entry"]["start_time"] = "09:00"
    out = so.refresh(out)
    assert items(out)[differs["id"]]["resolution"] == {"how": "changed"}
    new = open_items(out)
    assert len(new) == 1 and new[0]["id"] not in items(revealed(seed))
    assert new[0]["seed_said"].startswith("mass Tue,Wed,Thu,Fri 09:00")


def test_a_reviewers_answer_resolves_the_differences_on_its_slots(conn, demo, seed):
    out = _resolve_all_but(revealed(seed, reply(weekday="08:00", adorations=[
        weekly(HF, "Thursday", "09:00", "19:00", season=SEPT_MAY),
        weekly(SJ, "Tuesday", "18:00", "19:00")])), "")
    out["status"] = "needs_review"
    question = next(d for d in items(out).values() if d["kind"] == "question")
    assert question["slots"] == ["s17"] and question["resolution"] == {"how": "asked"}
    write_seed_file(out, demo["seeds_dir"])
    # The reviewer leaves the Holy Hour out: its reading is now an exclusion's, answered.
    approved = approve_seed(conn, PARISH, "agent:seed-review@abc", [
        {"slot": "s16", "choice": 0}, {"slot": "s17", "choice": 2}], demo["seeds_dir"])
    assert approved["status"] == "approved"
    after = so.refresh(read_seed(PARISH, demo["seeds_dir"]))
    hows = {d["kind"]: d["resolution"]["how"] for d in items(after).values()
            if "s17" in d["slots"]}
    assert set(hows.values()) <= {"answered", "asked"}


def test_a_settled_exclusion_citing_r22_to_r26_needs_no_answer(seed):
    slot(seed, "s11")["rationale"] = "R24: a volunteer shift, not a Mass."
    out = revealed(seed, reply(extra_masses=[weekly(HF, "Saturday", "09:00")]))
    excluded = next(d for d in items(out).values() if d["kind"] == "excluded")
    assert excluded["resolution"] == {"how": "auto", "reason": "policy-exclusion"}
    assert excluded["id"] not in {d["id"] for d in open_items(out)}
    assert so.stats(out)["auto"] >= 1


# ── The commands ────────────────────────────────────────────────────────────
@pytest.fixture
def demo_cli(demo, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(seed_cli, "_connect", lambda: connect_db(demo["db_path"]))
    monkeypatch.setattr(seed_cli, "_ctx", lambda args: SeedContext(seeds_dir=demo["seeds_dir"]))
    monkeypatch.delenv(so.OPINION_SHA_ENV, raising=False)
    return demo


def test_opinion_show_refuses_before_the_reveal(demo_cli, capsys):
    assert main(["seed", "opinion", "show", PARISH]) == 1
    assert "no second opinion yet" in capsys.readouterr().err


def test_opinion_show_lists_each_difference_with_its_quotes(demo_cli, seed, capsys):
    write_seed_file(revealed(seed), demo_cli["seeds_dir"])
    assert main(["seed", "opinion", "show", PARISH]) == 0
    out = capsys.readouterr().out
    assert "second opinion by gpt-6-luna (c1)" in out and "B1 dbb914e7 (issue 2026-09-27)" in out
    assert "differs: start time" in out and "UNRESOLVED" in out
    assert "B1 dbb914e7 (issue 2026-09-27) p2: “Tue-Fri 8:30 AM”" in out
    assert "seed (s12, s13, s14, s15): mass Tue,Wed,Thu,Fri 08:00" in out
    assert main(["seed", "opinion", "show", PARISH, "--json"]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["stats"]["unresolved"] >= 1 and "seed" not in shown


def test_opinion_keep_records_the_page_and_the_rule_and_check_passes_once_all_are_resolved(
        demo_cli, seed, capsys, monkeypatch):
    out = revealed(seed)
    path = write_seed_file(out, demo_cli["seeds_dir"])
    assert main(["seed", "check", PARISH]) == 1
    assert "unresolved" in capsys.readouterr().out
    for d in open_items(out):
        assert main(["seed", "opinion", "keep", PARISH, d["id"], "--src",
                     "latest p2: Daily Mass Tue-Fri 8:00 AM",
                     "--why", "R1: the newest schedule box prints 8:00."]) == 0
        assert f"{d['id']} " in capsys.readouterr().out
    saved = json.loads(path.read_text())
    kept = [d for d in saved["second_opinion"]["differences"]
            if (d["resolution"] or {}).get("how") == "kept"]
    assert kept and kept[0]["resolution"]["src"] == [
        {"source": "agent", "bulletin": NEW[:8], "page": 2,
         "said": "Daily Mass Tue-Fri 8:00 AM"}]
    assert main(["seed", "check", PARISH]) == 0
    # A source with no page, or no rule, is refused and nothing is written.
    before = path.read_bytes()
    assert main(["seed", "opinion", "keep", PARISH, kept[0]["id"], "--src", "latest: x",
                 "--why", "R1: x"]) == 1
    assert "bulletin page" in capsys.readouterr().err and path.read_bytes() == before
    # The dispatcher's hash of the entries, for its gates.
    sha = saved["second_opinion"]["entries_sha256"]
    monkeypatch.setenv(so.OPINION_SHA_ENV, f"{PARISH}={sha}")
    assert main(["seed", "check", PARISH]) == 0
    monkeypatch.setenv(so.OPINION_SHA_ENV, f"{PARISH}={'0' * 64}")
    assert main(["seed", "check", PARISH]) == 1
    assert "entries were changed" in capsys.readouterr().out


def test_finalize_writes_the_comparison_as_the_draft_stands(demo_cli, seed, capsys):
    out = _resolve_all_but(revealed(seed), "differs")
    for sid in ("s12", "s13", "s14", "s15"):
        slot(out, sid)["entry"]["start_time"] = "08:30"
    path = write_seed_file(out, demo_cli["seeds_dir"])
    assert main(["seed", "finalize", PARISH]) == 0, capsys.readouterr().out
    saved = json.loads(path.read_text())
    hows = [(d["kind"], (d["resolution"] or {}).get("how"))
            for d in saved["second_opinion"]["differences"]]
    assert ("differs", "changed") in hows and all(h for _, h in hows)


def test_an_approved_seed_is_not_held_to_its_opinion(conn, seed):
    out = revealed(seed)
    out["second_opinion"]["entries"][0]["entry"]["start_time"] = "17:00"
    for s in out["slots"]:
        if s["status"] == "needs_human":
            option = next(o for o in s["options"] if o.get("leaning"))
            s.update(status="settled", decision="include", entry=option["entry"],
                     answer={"choice": 0, "by": "R", "at": "2026-10-10T12:00:00Z"})
    out.update(status="approved", reviewer="R", approved_at="2026-10-10T12:05:00Z")
    assert not [p for p in check_seed(conn, out, parish_slug=PARISH, check_evidence=False)
                if "second_opinion" in p]
