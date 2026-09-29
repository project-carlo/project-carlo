"""OpenAI classifier: verify request shape and result normalization."""

from __future__ import annotations

import base64
import json
from datetime import date
from types import SimpleNamespace
from typing import Any

import pytest

from pdf_extract.classifiers import openai_gpt
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.classifiers.openai_gpt import OpenAIClassifier
from pdf_extract.schedule_extraction import SchedulePayload


def _usage(**overrides: int) -> SimpleNamespace:
    values = {"input": 1000, "cached": 0, "output": 300, "reasoning": 200} | overrides
    return SimpleNamespace(
        input_tokens=values["input"],
        input_tokens_details=SimpleNamespace(cached_tokens=values["cached"]),
        output_tokens=values["output"],
        output_tokens_details=SimpleNamespace(reasoning_tokens=values["reasoning"]),
    )


class _FakeResponses:
    def __init__(self, output_text: str) -> None:
        self._output_text = output_text
        self.last_kwargs: dict[str, Any] = {}
        self.call_count = 0

    def create(self, **kwargs: Any) -> SimpleNamespace:
        self.call_count += 1
        self.last_kwargs = kwargs
        return SimpleNamespace(output_text=self._output_text, usage=_usage(), status="completed")


def _install_fake(monkeypatch, payload: dict[str, Any] | str | None = None) -> _FakeResponses:
    text = payload if isinstance(payload, str) else json.dumps(payload or {})
    fake_responses = _FakeResponses(text)
    monkeypatch.setattr(
        openai_gpt, "OpenAI", lambda **kwargs: SimpleNamespace(responses=fake_responses)
    )
    return fake_responses


def _one_mass() -> dict[str, Any]:
    return {
        "weekly_schedule": {
            "masses": [{
                "church_slug": "st-mary", "day_of_week": "Sunday", "start_time": "9:00 AM",
                "end_time": None, "page_number": 1, "note": None,
            }],
        },
        "published_date": "2026-05-03",
    }


def test_request_sends_prompt_then_pdf_with_geminis_schema(monkeypatch):
    pdf_bytes = b"%PDF-1.4 hello"
    fake = _install_fake(monkeypatch, {})

    OpenAIClassifier(model="gpt-5.4-mini").extract(
        pdf_bytes,
        churches=[{"slug": "st-mary", "name": "St. Mary", "address": "123 Main"}],
        today=date(2026, 5, 4),
    )

    assert fake.call_count == 1
    kwargs = fake.last_kwargs
    assert kwargs["model"] == "gpt-5.4-mini"
    assert "reasoning" not in kwargs
    fmt = kwargs["text"]["format"]
    assert fmt["type"] == "json_schema"
    assert fmt["schema"] == SchedulePayload.model_json_schema(), "the schema Gemini is given"
    assert fmt["strict"] is False

    text_part, file_part = kwargs["input"][0]["content"]
    assert text_part["type"] == "input_text"
    assert "Mass, Confession" in text_part["text"]
    assert "st-mary" in text_part["text"]
    assert "2026-05-04" in text_part["text"]

    expected_b64 = base64.b64encode(pdf_bytes).decode("ascii")
    assert file_part["type"] == "input_file"
    assert file_part["file_data"] == f"data:application/pdf;base64,{expected_b64}"
    assert file_part["filename"].endswith(".pdf")
    assert "detail" not in file_part


def test_luna_pdf_sends_the_pdf_at_low_detail(monkeypatch):
    from pdf_extract.classifiers import get_classifier

    fake = _install_fake(monkeypatch, {})

    get_classifier("luna-pdf-low").extract(b"%PDF-1.4 x", churches=[], today=date(2026, 5, 4))

    assert fake.last_kwargs["model"] == "gpt-6-luna"
    assert fake.last_kwargs["reasoning"] == {"effort": "medium"}
    assert fake.last_kwargs["input"][0]["content"][1]["detail"] == "low"


def test_returns_normalized_event_shape_usage_and_timing(monkeypatch):
    _install_fake(monkeypatch, _one_mass())

    out = OpenAIClassifier().extract(
        b"%PDF-1.4 x", churches=[{"slug": "st-mary", "name": "x", "address": "x"}],
        today=date(2026, 5, 4),
    )
    assert out["published_date"] == "2026-05-03"
    assert out["wrong_bulletin"] is False
    ev = out["events"][0]
    assert (ev["church_slug"], ev["type"], ev["kind"]) == ("st-mary", "mass", "weekly")
    assert (ev["day_of_week"], ev["start_time"]) == ("Sunday", "9:00 AM")
    assert out["usage"] == {
        "prompt_tokens": 1000, "output_tokens": 300, "cached_tokens": 0, "reasoning_tokens": 200,
    }
    assert "llm_seconds" in out["timing"]


def test_invalid_slot_falls_back_to_lenient_parsing(monkeypatch):
    payload = _one_mass()
    payload["weekly_schedule"]["masses"].append(
        {"church_slug": "", "day_of_week": "Saturday", "start_time": "5:00 PM"}
    )
    _install_fake(monkeypatch, payload)

    out = OpenAIClassifier().extract(b"%PDF-1.4 x", churches=[], today=date(2026, 5, 4))

    assert [ev["start_time"] for ev in out["events"]] == ["9:00 AM"]


def test_empty_pdf_short_circuits_without_calling_api(monkeypatch):
    fake = _install_fake(monkeypatch)

    out = OpenAIClassifier().extract(b"", churches=[], today=date(2026, 5, 4))

    assert fake.call_count == 0
    assert out["events"] == []
    assert out["wrong_bulletin"] is False


def test_refusal_or_empty_output_returns_empty_result(monkeypatch):
    _install_fake(monkeypatch, "")

    out = OpenAIClassifier().extract(b"%PDF-1.4 x", churches=[], today=date(2026, 5, 4))

    assert out["events"] == []
    assert out["usage"]["prompt_tokens"] == 1000


def test_classifiers_are_registered():
    from pdf_extract.classifiers import REGISTRY, get_classifier

    assert get_classifier("gpt-5.4-mini").name == "gpt-5.4-mini"
    # Both Luna models, and the PDF control at both detail levels.
    for name, version in (
        ("luna-pdf-low", "gpt-6-luna+effort-medium+detail-low+"),
        ("luna-pdf-high", "gpt-6-luna+effort-medium+detail-high+"),
        ("luna5.6-pdf-low", "gpt-5.6-luna+effort-medium+detail-low+"),
        ("luna5.6-pdf-high", "gpt-5.6-luna+effort-medium+detail-high+"),
    ):
        assert name in REGISTRY
        classifier = get_classifier(name)
        assert classifier.name == name
        assert classifier.version.startswith(version)
    # Text stacks keep their names (and so their cached results) for gpt-6-luna.
    assert {"luna-pymupdf", "luna5.6-pymupdf"} <= set(REGISTRY)


def test_version_tracks_the_shared_prompt_and_settings():
    """Cached results are keyed by version: a prompt, schema or setting change must move it."""
    fingerprint = GeminiClassifier(model="m").version.removeprefix("m+")
    assert OpenAIClassifier(model="x").version == f"x+{fingerprint}"
    assert (
        OpenAIClassifier(model="x", reasoning_effort="low", file_detail="low").version
        == f"x+effort-low+detail-low+{fingerprint}"
    )


@pytest.mark.parametrize("custom_name", ["alt-name", None])
def test_name_defaults_to_model_id(custom_name):
    c = OpenAIClassifier(model="gpt-5.4-mini", name=custom_name)
    assert c.name == (custom_name or "gpt-5.4-mini")


def test_strict_mode_sends_the_sdks_strict_schema(monkeypatch):
    from openai.lib._pydantic import to_strict_json_schema

    from pdf_extract.classifiers import get_classifier

    fake = _install_fake(monkeypatch, _one_mass())

    classifier = get_classifier("luna-pdf-low-strict")
    out = classifier.extract(b"%PDF-1.4 x", churches=[], today=date(2026, 5, 4))

    fmt = fake.last_kwargs["text"]["format"]
    assert fmt["strict"] is True
    assert fmt["schema"] == to_strict_json_schema(SchedulePayload)
    # The strict rewrite requires every property, which Gemini's schema does not.
    assert set(fmt["schema"]["required"]) == set(SchedulePayload.model_fields)
    assert fake.last_kwargs["input"][0]["content"][1]["detail"] == "low"
    assert classifier.version.startswith("gpt-6-luna+effort-medium+detail-low+strict+")
    assert [ev["start_time"] for ev in out["events"]] == ["9:00 AM"]
