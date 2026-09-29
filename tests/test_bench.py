"""The text-stack benchmark: text classifier requests, text cache, and the bench flow."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from pdf_extract import bench
from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.classifiers import openai_gpt, text_llm
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.classifiers.text_llm import TEXT_EVENTS_PROMPT, TextLLMClassifier
from pdf_extract.db import create_db
from pdf_extract.runner import store_cached_result
from pdf_extract.schedule_extraction import SchedulePayload
from pdf_extract.storage import churches_for_parish, connect_db
from pdf_extract.text_extractors import page_header


def _payload(start_time: str = "9:00 AM") -> SchedulePayload:
    return SchedulePayload.model_validate({
        "weekly_schedule": {
            "masses": [{
                "church_slug": "test-church", "day_of_week": "Sunday",
                "start_time": start_time, "page_number": 1,
            }],
        },
        "published_date": "2026-09-20",
    })


class _FakeExtractor:
    name = "fake-text"
    version = "v1"

    def __init__(self) -> None:
        self.calls = 0

    def extract_text(self, pdf_bytes: bytes) -> str:
        self.calls += 1
        return f"{page_header(1)}\nMASS SCHEDULE\nSunday 9:00 AM"


class _FakeUsage:
    input_tokens = 1000
    output_tokens = 200
    input_tokens_details = type("D", (), {"cached_tokens": 0})()
    output_tokens_details = type("D", (), {"reasoning_tokens": 50})()


class _FakeResponses:
    def __init__(self, parsed: SchedulePayload) -> None:
        self.parsed = parsed
        self.requests: list[dict[str, Any]] = []

    def parse(self, **kwargs: Any) -> Any:
        self.requests.append(kwargs)
        return type("R", (), {"output_parsed": self.parsed, "usage": _FakeUsage()})()

    def create(self, **kwargs: Any) -> Any:
        """The PDF classifier asks for JSON against Gemini's schema and parses it itself."""
        self.requests.append(kwargs)
        return type("R", (), {
            "output_text": self.parsed.model_dump_json(), "usage": _FakeUsage(),
        })()


@pytest.fixture
def fake_openai(monkeypatch) -> _FakeResponses:
    responses = _FakeResponses(_payload())
    client = type("C", (), {"responses": responses})()
    monkeypatch.setattr(text_llm, "OpenAI", lambda **kwargs: client)
    monkeypatch.setattr(openai_gpt, "OpenAI", lambda **kwargs: client)
    return responses


@pytest.fixture
def fake_extractor(monkeypatch) -> _FakeExtractor:
    extractor = _FakeExtractor()
    monkeypatch.setattr(text_llm, "get_text_extractor", lambda name: extractor)
    return extractor


def test_text_classifier_sends_text_not_pdf(pipeline_dir, fake_openai, fake_extractor):
    classifier = TextLLMClassifier(extractor="fake-text", name="t", reasoning_effort="low")
    result = classifier.extract(
        b"%PDF fake", churches=[{"slug": "test-church"}], today=date(2026, 9, 25),
    )

    request = fake_openai.requests[0]
    assert request["model"] == "gpt-6-luna"
    assert request["reasoning"] == {"effort": "low"}
    developer, user = request["input"]
    assert "test-church" in developer["content"] and "2026-09-25" in developer["content"]
    assert "attached" not in developer["content"]
    assert "Sunday 9:00 AM" in user["content"]
    assert result["events"][0]["start_time"] == "9:00 AM"
    assert result["usage"] == {
        "prompt_tokens": 1000, "output_tokens": 200, "cached_tokens": 0, "reasoning_tokens": 50,
    }
    assert result["text_chars"] > 0
    assert "fake-text" in classifier.version and "effort-low" in classifier.version


def test_extracted_text_is_cached_per_pdf(pipeline_dir, fake_openai, fake_extractor):
    classifier = TextLLMClassifier(extractor="fake-text", name="t")
    for _ in range(2):
        classifier.extract(b"%PDF same", churches=[], today=date(2026, 9, 25))
    classifier.extract(b"%PDF other", churches=[], today=date(2026, 9, 25))
    assert fake_extractor.calls == 2
    assert len(list(Path("data/runs/text/fake-text/v1").glob("*.txt"))) == 2


def test_text_prompt_keeps_the_production_instructions():
    assert "`weekly_schedule`" in TEXT_EVENTS_PROMPT
    assert page_header(1) in TEXT_EVENTS_PROMPT
    # Still a format template with exactly the production placeholders.
    TEXT_EVENTS_PROMPT.format(churches_json="[]", today_iso="x", today_day_of_week="y")


def _seed_bulletins(monkeypatch) -> None:
    """Two current bulletins; only the first has a cached Gemini baseline."""
    # A second parish in the CSV: every command re-seeds parishes from it.
    with Path("data/parishes.csv").open("a", encoding="utf-8") as f:
        f.write("other-parish,Other Parish,https://example.com,,\n")
    create_db()
    conn = connect_db()
    with conn:
        for slug, url, content_hash in (
            ("test-parish", "https://example.org/a.pdf", "hash-a"),
            ("other-parish", "https://example.org/b.pdf", "hash-b"),
        ):
            conn.execute(
                """INSERT INTO bulletin(parish_id, source_url, content_hash, fetched_at)
                   SELECT id, ?, ?, '2026-09-20T00:00:00Z' FROM parish WHERE slug = ?""",
                (url, content_hash, slug),
            )
            get_store().put(bulletin_pdf_key(slug, content_hash), f"%PDF {slug}".encode())
    churches = churches_for_parish(conn, "test-parish")
    conn.close()

    baseline = GeminiClassifier()
    store_cached_result(
        baseline.name, baseline.version, "hash-a", churches,
        {
            "events": [
                {"church_slug": "test-church", "type": "mass", "kind": "weekly",
                 "day_of_week": "Sunday", "date": None, "start_time": "9:00 AM",
                 "end_time": None, "cancelled": False, "page_number": 1, "note": None},
                {"church_slug": "test-church", "type": "confession", "kind": "weekly",
                 "day_of_week": "Saturday", "date": None, "start_time": "3:00 PM",
                 "end_time": "3:45 PM", "cancelled": False, "page_number": 1, "note": None},
            ],
            "published_date": "2026-09-20",
            "wrong_bulletin": False,
            "church_list_needs_review": False,
            "usage": {"prompt_tokens": 2000, "output_tokens": 400},
        },
    )
    monkeypatch.setattr("pdf_extract.storage.ensure_truncated_pdf", lambda path, **kw: path)


def test_bench_scores_stacks_against_the_cached_baseline(
    pipeline_dir, fake_openai, fake_extractor, monkeypatch,
):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    _seed_bulletins(monkeypatch)

    result = bench.run_bench(stacks=["pymupdf", "pdf"], concurrency=2)

    # Only the bulletin with a baseline is benchmarked, and Gemini is never called.
    assert result["bulletins"] == 1
    assert set(result["stacks"]) == {"luna-pymupdf", "luna-pdf"}
    assert all(s["served"] == 1 for s in result["stacks"].values())
    assert len(fake_openai.requests) == 2

    report = json.loads(Path(result["report_json"]).read_text(encoding="utf-8"))
    assert report["baseline"] == "gemini-flash"
    rows = {row["classifier"]: row for row in report["vs_baseline"]}
    text_row = rows["luna-pymupdf"]
    # Found the Mass, missed the Confession.
    assert text_row["strict"] == {"precision": 1.0, "recall": 0.5, "f1": 0.6667}
    assert text_row["by_event_type"]["mass"]["recall"] == 1.0
    assert text_row["by_event_type"]["confession"]["recall"] == 0.0
    assert text_row["published_date_agreement"] == 1.0
    # 1000 in + 200 out at $0.10 / $0.50 per 1M tokens.
    assert text_row["cost_usd_per_bulletin"] == pytest.approx(0.0002)
    # The baseline's 2000 in + 400 out at $0.50 / $3.00; its result predates
    # thinking tokens being recorded, so that cost is a lower bound.
    assert text_row["baseline_cost_usd_per_bulletin"] == pytest.approx(0.0022)
    assert text_row["cost_vs_baseline"] == pytest.approx(0.0909, abs=1e-4)
    assert text_row["baseline_cost_missing_thinking"] == 1
    stats = {c["classifier"]: c for c in report["per_classifier"]}
    assert stats["gemini-flash"]["cache_hit_rate"] == 1.0
    assert stats["gemini-flash"]["cost_usd_this_run"] == 0
    assert stats["luna-pdf"]["cache_hit_rate"] == 0.0

    # The PDF stack sends prompt then PDF, at low detail, with Gemini's schema.
    pdf_request = next(r for r in fake_openai.requests if "text" in r)
    text_part, file_part = pdf_request["input"][0]["content"]
    assert text_part["type"] == "input_text"
    assert file_part["detail"] == "low"
    assert pdf_request["text"]["format"]["schema"] == SchedulePayload.model_json_schema()
    markdown = Path(result["report_markdown"]).read_text(encoding="utf-8")
    assert "Agreement with baseline `gemini-flash`" in markdown
    assert "≥$0.00220" in markdown

    # A second run is served entirely from the caches.
    bench.run_bench(stacks=["pymupdf"], concurrency=2)
    assert len(fake_openai.requests) == 2
    assert fake_extractor.calls == 1


def test_bench_without_a_cached_baseline_says_so(pipeline_dir, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    create_db()
    with pytest.raises(bench.BenchError, match="No cached gemini-flash results"):
        bench.run_bench(stacks=["pdf"])


def test_bench_requires_an_openai_key(pipeline_dir, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(bench.BenchError, match="OPENAI_API_KEY"):
        bench.run_bench(stacks=["pdf"])


def test_sample_is_deterministic():
    urls = [f"https://example.org/{i}.pdf" for i in range(20)]
    assert bench._sample(urls, 5, seed=0) == bench._sample(list(reversed(urls)), 5, seed=0)
    assert len(bench._sample(urls, 5, seed=0)) == 5
    assert bench._sample(urls, None, seed=0) == set(urls)
