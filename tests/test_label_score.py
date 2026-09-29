"""Scoring classifiers against the hand-made labels, and `bench --labels`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import bench
from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.db import create_db
from pdf_extract.labeling.labels import FLAGS, SCHEMA_VERSION
from pdf_extract.labeling.score import align, score_against_labels, tier_key
from pdf_extract.runner import store_cached_result
from pdf_extract.storage import churches_for_parish, connect_db
from tests.test_bench import fake_extractor, fake_openai  # noqa: F401  (fixtures)

HASH_OLD = "a" * 64
HASH_NEW = "b" * 64
OLD_URL = "https://example.org/old.pdf"


def _truth(**overrides: Any) -> dict[str, Any]:
    """A label row: a weekly Sunday 9 AM Mass at test-church, page 1, no note."""
    return {
        "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "09:00", "end_time": None,
        "cancelled": False, "weeks_of_month": [], "season": None, "page_number": 1,
        "note": None, "origin": "human",
    } | overrides


def _predicted(**overrides: Any) -> dict[str, Any]:
    """The same Mass as a classifier writes it (flattened run row)."""
    return {
        "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM", "end_time": None,
        "cancelled": False, "page_number": 1, "note": None,
    } | overrides


def _normalized(**overrides: Any) -> dict[str, Any]:
    from pdf_extract.labeling.bulletins import gemini_rows

    return gemini_rows([_predicted(**overrides)])[0]


def test_a_dated_event_matches_its_weekday_at_the_slot_tier_only():
    truth = _truth()
    dated = _normalized(event_kind="specific_date", day_of_week=None, date="2026-09-27")
    assert tier_key(dated, "slot") == tier_key(truth, "slot")
    assert tier_key(dated, "kind") != tier_key(truth, "kind")
    other_church = _normalized(church_slug="other-church")
    assert tier_key(other_church, "kind") == tier_key(truth, "kind")
    assert tier_key(other_church, "church") != tier_key(truth, "church")


def test_align_pairs_each_church_with_its_own_event():
    truths = [_truth(church_slug="a-church"), _truth(church_slug="b-church")]
    predicted = [_normalized(church_slug="b-church"), _normalized(church_slug="a-church")]
    pairs = align(predicted, truths)
    assert sorted((p["church_slug"], t["church_slug"]) for p, t in pairs) == [
        ("a-church", "a-church"), ("b-church", "b-church"),
    ]


def _write_label(slug: str, content_hash: str, url: str, events: list[dict[str, Any]], **kw) -> None:
    label = {
        "schema_version": SCHEMA_VERSION, "parish_slug": slug, "content_hash": content_hash,
        "source_url": url, "status": "done", "flags": dict.fromkeys(FLAGS, False),
        "published_date": "2026-09-20", "note": "", "labeler": "test", "seconds_spent": 1,
        "updated_at": "2026-09-28T00:00:00Z", "events": events,
    } | kw
    path = Path("data/labels") / slug / f"{content_hash}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(label), encoding="utf-8")


def _write_run(name: str, rows: list[dict[str, Any]], *, published: str = "2026-09-20") -> None:
    run = Path("data/runs") / name
    run.mkdir(parents=True, exist_ok=True)
    (run / "events.json").write_text(
        json.dumps([{**r, "bulletin_source_url": OLD_URL} for r in rows]), encoding="utf-8",
    )
    (run / "bulletins.json").write_text(json.dumps([{
        "bulletin_source_url": OLD_URL, "parish_slug": "test-parish", "content_hash": HASH_OLD,
        "published_date_extracted": published, "usage": {},
    }]), encoding="utf-8")
    (run / "run.json").write_text(json.dumps({"classifier_version": "v1"}), encoding="utf-8")


def test_scores_every_tier_and_field(pipeline_dir):
    _write_label("test-parish", HASH_OLD, OLD_URL, [
        _truth(),
        _truth(event_type="confession", day_of_week="Saturday", start_time="15:00",
               end_time="15:45", page_number=2, note="In the chapel"),
        _truth(event_kind="specific_date", day_of_week=None, date="2026-09-23",
               start_time="12:00", cancelled=True),
    ])
    # The Sunday Mass exactly; the Confession on the wrong page, without the
    # note, with no end time; the cancellation filed as weekly; one extra Mass.
    _write_run("model", [
        _predicted(),
        _predicted(type="confession", event_type="confession", day_of_week="Saturday",
                   start_time="3:00 PM", page_number=3),
        _predicted(day_of_week="Wednesday", start_time="12:00 PM", cancelled=True),
        _predicted(start_time="11:00 AM"),
    ], published="2026-09-19")

    report = score_against_labels(["model"])
    r = report["results"][0]
    assert r["bulletins_scored"] == 1
    tiers = {tier: (v["tp"], v["predicted"], v["expected"]) for tier, v in r["tiers"].items()}
    assert tiers == {
        "slot": (3, 4, 3), "kind": (2, 4, 3), "church": (2, 4, 3), "exact": (1, 4, 3),
    }
    assert r["tiers"]["slot"]["recall"] == 1.0
    assert r["tiers"]["slot"]["precision"] == 0.75
    assert r["by_event_type"]["confession"]["slot"]["recall"] == 1.0
    assert r["by_event_type"]["mass"]["kind"]["recall"] == 0.5

    attrs = {field: (v["correct"], v["total"]) for field, v in r["attributes"].items()}
    assert attrs == {
        "weekly_vs_dated": (2, 3), "church": (3, 3), "end_time": (2, 3),
        "page_number": (2, 3), "note_presence": (2, 3),
    }
    assert (r["notes_missed"], r["notes_extra"]) == (1, 0)
    assert r["published_date"] == {"correct": 0, "total": 1, "rate": 0.0}
    assert r["bulletins_exact"]["slot"] == 0

    bulletin = r["per_bulletin"][0]
    assert bulletin["missed"] == []
    assert [e["start_time"] for e in bulletin["extra"]] == ["11:00"]
    markdown = Path(report["report_markdown"]).read_text(encoding="utf-8")
    assert "Against ground truth: 1 labeled bulletins, 3 events" in markdown
    assert "Wrong fields" in markdown


def test_only_done_labels_count(pipeline_dir):
    _write_label("test-parish", HASH_OLD, OLD_URL, [_truth()], status="in_progress")
    _write_run("model", [_predicted()])
    with pytest.raises(ValueError, match="No labels marked done"):
        score_against_labels(["model"])


def test_bench_against_labels_runs_the_labeled_bulletin_even_when_not_latest(
    pipeline_dir, fake_openai, fake_extractor, monkeypatch,  # noqa: F811
):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr("pdf_extract.storage.ensure_truncated_pdf", lambda path, **kw: path)
    create_db()
    conn = connect_db()
    with conn:
        # The labeled bulletin is older than the parish's current one.
        for url, content_hash, fetched in (
            (OLD_URL, HASH_OLD, "2026-09-20T00:00:00Z"),
            ("https://example.org/new.pdf", HASH_NEW, "2026-09-27T00:00:00Z"),
        ):
            conn.execute(
                """INSERT INTO bulletin(parish_id, source_url, content_hash, fetched_at)
                   SELECT id, ?, ?, ? FROM parish WHERE slug = 'test-parish'""",
                (url, content_hash, fetched),
            )
            get_store().put(bulletin_pdf_key("test-parish", content_hash), b"%PDF test")
    churches = churches_for_parish(conn, "test-parish")
    conn.close()
    _write_label("test-parish", HASH_OLD, OLD_URL, [
        _truth(),
        _truth(event_type="confession", day_of_week="Saturday", start_time="15:00"),
    ])
    gemini = GeminiClassifier()
    store_cached_result(gemini.name, gemini.version, HASH_OLD, churches, {
        "events": [
            {"church_slug": "test-church", "type": "mass", "kind": "weekly",
             "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM", "end_time": None,
             "cancelled": False, "page_number": 1, "note": None},
            {"church_slug": "test-church", "type": "confession", "kind": "weekly",
             "day_of_week": "Saturday", "date": None, "start_time": "3:00 PM",
             "end_time": None, "cancelled": False, "page_number": 1, "note": None},
        ],
        "published_date": "2026-09-20", "wrong_bulletin": False,
        "church_list_needs_review": False, "usage": {"prompt_tokens": 10, "output_tokens": 5},
    })

    # A luna result extracted on the day it ran is not one extracted as of the
    # bulletin's Sunday, so it must not be served.
    luna = bench._classifier("pdf", "gpt-6-luna", "low", bench.DEFAULT_REASONING_EFFORT)
    store_cached_result(luna.name, luna.version, HASH_OLD, churches, {"events": []})

    result = bench.run_bench(stacks=["pdf"], labels=True, concurrency=1)

    assert result["bulletins"] == 1
    assert set(result["stacks"]) == {"gemini-flash", "luna-pdf-low"}
    assert result["stacks"]["gemini-flash"]["api_calls"] == 0
    assert len(fake_openai.requests) == 1
    # Told today is the Sunday the label dates the bulletin to, not the real date.
    prompt = fake_openai.requests[0]["input"][0]["content"][0]["text"]
    assert "2026-09-20" in prompt and "Sunday" in prompt
    report = json.loads(Path(result["report_json"]).read_text(encoding="utf-8"))
    rows = {r["classifier"]: r for r in report["results"]}
    assert rows["luna-pdf-low"]["bulletins_as_of_sunday"] == 1
    # Gemini is served the weekly job's result, extracted the week it was fetched.
    assert rows["gemini-flash"]["bulletins_as_of_sunday"] == 0
    assert rows["gemini-flash"]["tiers"]["exact"]["f1"] == 1.0
    # The fake model finds the Sunday Mass only.
    assert rows["luna-pdf-low"]["tiers"]["slot"]["recall"] == 0.5
    assert rows["luna-pdf-low"]["tiers"]["slot"]["precision"] == 1.0


def test_the_date_sent_is_the_nearest_sunday():
    from datetime import date

    assert bench.nearest_sunday(date(2026, 9, 27)) == date(2026, 9, 27)
    assert bench.nearest_sunday(date(2026, 10, 3)) == date(2026, 10, 4)  # Saturday
    assert bench.nearest_sunday(date(2026, 9, 29)) == date(2026, 9, 27)  # Tuesday
    # No published date on the label or bulletin: the week it was fetched.
    entry = {"published_date": None, "fetched_at": "2026-09-23T10:00:00Z"}
    assert bench.bulletin_sunday({"published_date": None}, entry) == date(2026, 9, 20)
    assert bench.bulletin_sunday({"published_date": "2026-10-04"}, entry) == date(2026, 10, 4)


def test_gemini_models_run_once_on_the_pdf():
    configurations = bench._configurations(
        ["pymupdf", "pdf"], ["gemini-3-pro-preview", "gpt-6-luna"], ["low", "high"],
    )
    assert configurations == [
        ("pdf", "gemini-3-pro-preview", "low"),
        ("pymupdf", "gpt-6-luna", "low"),
        ("pdf", "gpt-6-luna", "low"),
        ("pdf", "gpt-6-luna", "high"),
    ]


def test_other_gemini_models_need_a_key(pipeline_dir, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(bench.BenchError, match="GEMINI_API_KEY"):
        bench.run_bench(models=["gemini-3-pro-preview"], labels=True)
