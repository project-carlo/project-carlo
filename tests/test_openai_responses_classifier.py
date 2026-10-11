"""OpenAI Responses classifier: request layout, schema, and result normalisation."""

from __future__ import annotations

import base64
import json
from datetime import date
from types import SimpleNamespace
from typing import Any

import pytest

from pdf_extract.classifiers import ClassifierOptionError, get_classifier
from pdf_extract.classifiers.openai_responses import (
    RESPONSE_SCHEMA,
    OpenAIResponsesClassifier,
    render_pages,
)
from pdf_extract.classifiers.qualified_schedule import (
    CONTEXT_TEMPLATE,
    SCHEMA_FINGERPRINT,
    QualifiedSchedulePayload,
    fingerprint,
    flatten_events,
)
from pdf_extract.classifiers.schedule_policy import POLICY

CHURCHES = [{"slug": "st-mary", "name": "St. Mary", "address": "123 Main"}]
TODAY = date(2026, 9, 18)


class _FakeResponses:
    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> SimpleNamespace:
        self.calls.append(kwargs)
        return SimpleNamespace(
            id="resp_1",
            status="completed",
            incomplete_details=None,
            output_text=self.output_text,
            usage=SimpleNamespace(
                input_tokens=3000,
                input_tokens_details=SimpleNamespace(cached_tokens=1200, cache_write_tokens=0),
                output_tokens=900,
                output_tokens_details=SimpleNamespace(reasoning_tokens=600),
            ),
        )


def _classifier(output: dict[str, Any] | str, **kwargs: Any):
    classifier = OpenAIResponsesClassifier(model="gpt-6-luna", **kwargs)
    fake = _FakeResponses(output if isinstance(output, str) else json.dumps(output))
    classifier._client = SimpleNamespace(responses=fake)
    return classifier, fake


def _payload(**weekly_mass: Any) -> dict[str, Any]:
    slot = {
        "church_slug": "st-mary", "day_of_week": "Friday", "start_time": "7:00 PM",
        "end_time": None, "weeks_of_month": [], "season": None, "page_number": 2, "note": None,
    } | weekly_mass
    empty = {"masses": [], "confessions": [], "adorations": []}
    return {
        "weekly_schedule": empty | {"masses": [slot]},
        "single_events": empty,
        "cancellations": empty,
        "church_list_needs_review": False,
        "published_date": "2026-09-20",
        "wrong_bulletin": False,
    }


def test_static_prompt_comes_before_the_bulletin_and_is_the_cache_breakpoint():
    pdf = b"%PDF-1.4 hello"
    classifier, fake = _classifier(_payload())
    classifier.extract(pdf, churches=CHURCHES, today=TODAY)

    request = fake.calls[0]
    developer, user = request["input"]
    assert developer["role"] == "developer"
    assert developer["content"] == [{
        "type": "input_text",
        "text": POLICY,
        "prompt_cache_breakpoint": {"mode": "explicit"},
    }]
    assert request["prompt_cache_options"] == {"mode": "explicit"}

    context, file_part = user["content"]
    assert context["type"] == "input_text"
    assert "st-mary" in context["text"] and "2026-09-18 (Friday)" in context["text"]
    assert file_part["type"] == "input_file"
    assert file_part["detail"] == "low"
    assert file_part["file_data"] == (
        "data:application/pdf;base64," + base64.b64encode(pdf).decode("ascii")
    )
    # Nothing per-bulletin may sit in the cached prefix.
    assert "st-mary" not in POLICY and "{" not in POLICY


def test_request_settings_and_strict_toggle():
    classifier, fake = _classifier(_payload())
    classifier.extract(b"%PDF", churches=CHURCHES, today=TODAY)
    request = fake.calls[0]
    assert request["model"] == "gpt-6-luna"
    assert request["reasoning"] == {"effort": "medium"}
    assert request["text"]["format"]["type"] == "json_schema"
    assert request["text"]["format"]["strict"] is True

    nonstrict, fake = _classifier(_payload(), strict=False)
    nonstrict.extract(b"%PDF", churches=CHURCHES, today=TODAY)
    assert fake.calls[0]["text"]["format"]["strict"] is False
    assert fake.calls[0]["text"]["format"]["schema"] == request["text"]["format"]["schema"]
    assert nonstrict.version != classifier.version


def test_policy_changes_invalidate_the_qualified_cache_fingerprint():
    schema = json.dumps(QualifiedSchedulePayload.model_json_schema(), sort_keys=True)
    assert SCHEMA_FINGERPRINT == fingerprint(POLICY, CONTEXT_TEMPLATE, schema)
    assert fingerprint(POLICY + "\nChanged policy", CONTEXT_TEMPLATE, schema) != SCHEMA_FINGERPRINT
    classifier = OpenAIResponsesClassifier(model="gpt-6-luna")
    assert classifier.version.endswith(f"+prompt-{SCHEMA_FINGERPRINT}")


def test_schema_is_strict_compatible_and_carries_the_qualifiers():
    text = json.dumps(RESPONSE_SCHEMA)
    assert '"default"' not in text

    def objects(node: Any):
        if isinstance(node, dict):
            if node.get("type") == "object":
                yield node
            for value in node.values():
                yield from objects(value)
        elif isinstance(node, list):
            for value in node:
                yield from objects(value)

    for obj in objects(RESPONSE_SCHEMA):
        assert obj["additionalProperties"] is False
        assert set(obj["required"]) == set(obj["properties"])

    weekly = RESPONSE_SCHEMA["$defs"]["WeeklySlot"]["properties"]
    assert weekly["weeks_of_month"]["items"]["enum"] == [
        "first", "second", "third", "fourth", "fifth", "last",
    ]
    assert "season" in weekly
    assert "weeks_of_month" not in RESPONSE_SCHEMA["$defs"]["DateSlot"]["properties"]


def test_qualifiers_are_flattened_like_pr_22():
    classifier, _ = _classifier(_payload(
        weeks_of_month=["third", "first"],
        season={"start_month": "October", "start_day": None, "end_month": "June", "end_day": 15},
    ))
    result = classifier.extract(b"%PDF", churches=CHURCHES, today=TODAY)

    [event] = result["events"]
    assert event["type"] == "mass" and event["kind"] == "weekly"
    assert event["weeks_of_month"] == ["first", "third"]
    assert (event["season_start_month"], event["season_start_day"]) == (10, None)
    assert (event["season_end_month"], event["season_end_day"]) == (6, 15)
    assert result["published_date"] == "2026-09-20"
    assert result["usage"] == {
        "input_tokens": 3000, "cached_tokens": 1200, "cache_write_tokens": 0,
        "output_tokens": 900, "reasoning_tokens": 600,
    }
    assert result["response_id"] == "resp_1"


def test_excluded_weeks_are_flattened_in_their_canonical_form():
    [event] = flatten_events(_payload(weeks_of_month=["last"], exclude_weeks=True))["events"]
    assert (event["weeks_of_month"], event["exclude_weeks"]) == (["last"], True)
    [event] = flatten_events(_payload(weeks_of_month=["first"], exclude_weeks=True))["events"]
    assert (event["weeks_of_month"], event["exclude_weeks"]) == (
        ["second", "third", "fourth", "fifth"], False)
    [event] = flatten_events(_payload())["events"]
    assert event["exclude_weeks"] is False


def test_lenient_reading_drops_impossible_qualifiers():
    raw = _payload(
        weeks_of_month=["first", "1st", "last"],
        season={"start_month": "February", "start_day": 30, "end_month": "nope"},
    )
    [event] = flatten_events(raw)["events"]
    assert event["weeks_of_month"] == ["first", "last"]
    assert event["season_start_month"] is None and event["season_end_month"] is None

    raw = _payload(season={"start_month": "February", "start_day": 30, "end_month": "March"})
    [event] = flatten_events(raw)["events"]
    assert (event["season_start_month"], event["season_start_day"]) == (2, None)


def test_unparseable_reply_is_an_empty_result():
    classifier, _ = _classifier("not json")
    result = classifier.extract(b"%PDF", churches=CHURCHES, today=TODAY)
    assert result["events"] == [] and result["wrong_bulletin"] is False


def test_registered_variants():
    strict = get_classifier("gpt-6-luna")
    nonstrict = get_classifier("gpt-6-luna-nonstrict")
    assert strict.name == "gpt-6-luna"
    assert strict.version.startswith("gpt-6-luna+strict+reasoning-medium+detail-low+prompt-")
    assert nonstrict.version.startswith("gpt-6-luna+nonstrict+")


def _two_page_pdf() -> bytes:
    import io

    from pypdf import PdfWriter

    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=396)
    buffer = io.BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def test_render_pages_gives_one_jpeg_per_page_at_200_dpi():
    import io

    from PIL import Image

    pages = render_pages(_two_page_pdf())
    assert len(pages) == 2
    sizes = [Image.open(io.BytesIO(page)).size for page in pages]
    assert [Image.open(io.BytesIO(page)).format for page in pages] == ["JPEG", "JPEG"]
    assert sizes == [(1700, 2200), (1700, 1100)]


def test_pdf_as_images_sends_numbered_page_images_in_place_of_the_pdf():
    classifier, fake = _classifier(_payload(), pdf_as_images=True, file_detail="original")
    classifier.extract(_two_page_pdf(), churches=CHURCHES, today=TODAY)

    _, user = fake.calls[0]["input"]
    context, *pages = user["content"]
    assert context["type"] == "input_text" and "st-mary" in context["text"]
    assert [part["type"] for part in pages] == [
        "input_text", "input_image", "input_text", "input_image",
    ]
    assert [pages[0]["text"], pages[2]["text"]] == ["Page 1 of 2", "Page 2 of 2"]
    for image in pages[1::2]:
        assert image["detail"] == "original"
        assert image["image_url"].startswith("data:image/jpeg;base64,")


def test_model_options_change_the_request_and_the_version():
    default = get_classifier("gpt-6-luna")
    classifier, fake = _classifier(_payload(), reasoning_effort="high", file_detail="high")
    classifier.extract(b"%PDF", churches=CHURCHES, today=TODAY)
    request = fake.calls[0]
    assert request["reasoning"] == {"effort": "high"}
    assert request["input"][1]["content"][1]["detail"] == "high"
    assert "+reasoning-high+detail-high+prompt-" in classifier.version

    images = get_classifier("gpt-6-luna", pdf_as_images=True)
    assert "+detail-low+pages-200dpi+prompt-" in images.version
    versions = {default.version, classifier.version, images.version}
    assert len(versions) == 3
    # None means "the classifier's default", which is what the CLI passes for unset flags.
    assert get_classifier("gpt-6-luna", reasoning_effort=None).version == default.version


def test_invalid_model_options_are_refused():
    with pytest.raises(ClassifierOptionError, match="not available for a PDF"):
        get_classifier("gpt-6-luna", file_detail="original")
    with pytest.raises(ClassifierOptionError, match="reasoning effort"):
        get_classifier("gpt-6-luna", reasoning_effort="extreme")
    with pytest.raises(ClassifierOptionError, match="does not take reasoning_effort"):
        get_classifier("gemini-flash", reasoning_effort="high")


def test_model_option_runs_another_openai_model_under_its_own_name():
    sol = get_classifier("gpt-6-luna", model="gpt-6.1-sol", reasoning_effort="high")
    assert sol.name == "gpt-6.1-sol"
    assert sol.version.startswith("gpt-6.1-sol+strict+reasoning-high+")
    assert get_classifier("gpt-6-luna-nonstrict", model="gpt-6.1-sol").name == (
        "gpt-6.1-sol-nonstrict"
    )
    # The registered default keeps its name, so existing cached runs still match.
    assert get_classifier("gpt-6-luna", model=None).name == "gpt-6-luna"

    sol._client = SimpleNamespace(responses=_FakeResponses(json.dumps(_payload())))
    sol.extract(b"%PDF", churches=CHURCHES, today=TODAY)
    assert sol._client.responses.calls[0]["model"] == "gpt-6.1-sol"

    with pytest.raises(ClassifierOptionError, match="not a valid OpenAI model name"):
        get_classifier("gpt-6-luna", model="../gpt")
    with pytest.raises(ClassifierOptionError, match="does not take model"):
        get_classifier("gemini-flash", model="gpt-6.1-sol")
