"""Gemini classifier over the qualified schema: request, schema, and result normalisation."""

from __future__ import annotations

import json
from datetime import date
from types import SimpleNamespace
from typing import Any

import pytest

from pdf_extract import schedule_extraction
from pdf_extract.classifiers import ClassifierOptionError, gemini_qualified, get_classifier
from pdf_extract.classifiers.openai_responses import OpenAIResponsesClassifier
from pdf_extract.classifiers.schedule_policy import POLICY
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL

CHURCHES = [{"slug": "st-mary", "name": "St. Mary", "address": "123 Main"}]
TODAY = date(2026, 9, 18)


def _payload(**weekly_mass: Any) -> dict[str, Any]:
    slot = {
        "church_slug": "st-mary", "day_of_week": "Saturday", "start_time": "4:00 PM",
        "weeks_of_month": ["second", "third", "fourth", "fifth"], "page_number": 2,
    } | weekly_mass
    return {
        "weekly_schedule": {"masses": [slot]},
        "single_events": {},
        "published_date": "2026-09-20",
    }


@pytest.fixture
def fake_gemini(monkeypatch):
    calls: list[dict[str, Any]] = []
    reply = {"text": json.dumps(_payload())}

    def generate(client, *, model, contents, config):
        calls.append({"client": client, "model": model, "contents": contents, "config": config})
        return SimpleNamespace(
            text=reply["text"],
            usage_metadata=SimpleNamespace(prompt_token_count=2500, candidates_token_count=400),
        )

    clients = iter(range(100))
    monkeypatch.setattr(gemini_qualified, "gemini_client", lambda: f"client-{next(clients)}")
    monkeypatch.setattr(schedule_extraction, "_generate_content_with_backoff", generate)
    return calls, reply


def test_request_sends_the_shared_policy_then_context_then_pdf(fake_gemini):
    calls, _ = fake_gemini
    classifier = get_classifier("gemini-flash-qualified")
    classifier.extract(b"%PDF-1.4 hello", churches=CHURCHES, today=TODAY)

    [call] = calls
    assert call["model"] == DEFAULT_GEMINI_MODEL
    policy, context, pdf = call["contents"]
    assert policy is POLICY
    assert "st-mary" in context and "2026-09-18 (Friday)" in context
    assert pdf.inline_data.mime_type == "application/pdf"
    assert pdf.inline_data.data == b"%PDF-1.4 hello"
    assert call["config"].response_mime_type == "application/json"
    schema = call["config"].response_json_schema
    assert "weeks_of_month" in schema["$defs"]["WeeklySlot"]["properties"]
    assert "season" in schema["$defs"]["WeeklySlot"]["properties"]


def test_result_is_flattened_with_qualifiers_and_usage(fake_gemini):
    result = get_classifier("gemini-flash-qualified").extract(
        b"%PDF", churches=CHURCHES, today=TODAY,
    )
    [event] = result["events"]
    assert event["type"] == "mass" and event["kind"] == "weekly"
    assert event["weeks_of_month"] == ["second", "third", "fourth", "fifth"]
    assert event["season_start_month"] is None
    assert result["published_date"] == "2026-09-20"
    assert result["usage"] == {"prompt_tokens": 2500, "output_tokens": 400}


def test_invalid_reply_is_read_leniently(fake_gemini):
    _, reply = fake_gemini
    reply["text"] = json.dumps(_payload(weeks_of_month=["first", "1st"], extra="x"))
    [event] = get_classifier("gemini-flash-qualified").extract(
        b"%PDF", churches=CHURCHES, today=TODAY,
    )["events"]
    assert event["weeks_of_month"] == ["first"]

    reply["text"] = "not json"
    result = get_classifier("gemini-flash-qualified").extract(
        b"%PDF", churches=CHURCHES, today=TODAY,
    )
    assert result["events"] == [] and result["wrong_bulletin"] is False


def test_one_client_serves_every_bulletin(fake_gemini):
    calls, _ = fake_gemini
    classifier = get_classifier("gemini-flash-qualified")
    for _ in range(3):
        classifier.extract(b"%PDF", churches=CHURCHES, today=TODAY)
    assert [call["client"] for call in calls] == ["client-0"] * 3


def test_empty_pdf_makes_no_call(fake_gemini):
    calls, _ = fake_gemini
    result = get_classifier("gemini-flash-qualified").extract(b"", churches=CHURCHES, today=TODAY)
    assert result["events"] == [] and calls == []


def test_version_and_model_option():
    default = get_classifier("gemini-flash-qualified")
    luna = OpenAIResponsesClassifier(model="gpt-6-luna")
    assert default.name == "gemini-flash-qualified"
    assert default.version.startswith(f"{DEFAULT_GEMINI_MODEL}+prompt-")
    # The same policy and schema fingerprint as the OpenAI eval classifier.
    assert default.version.split("+prompt-")[1] == luna.version.split("+prompt-")[1]

    pro = get_classifier("gemini-flash-qualified", model="gemini-3-pro-preview")
    assert pro.name == "gemini-3-pro-preview-qualified"
    assert pro.version.startswith("gemini-3-pro-preview+prompt-")
    assert get_classifier("gemini-flash-qualified", model=None).name == "gemini-flash-qualified"

    with pytest.raises(ClassifierOptionError, match="not a valid Gemini model name"):
        get_classifier("gemini-flash-qualified", model="../gemini")
    with pytest.raises(ClassifierOptionError, match="does not take reasoning_effort"):
        get_classifier("gemini-flash-qualified", reasoning_effort="high")
