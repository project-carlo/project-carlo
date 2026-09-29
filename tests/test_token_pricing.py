"""Token usage recorded from Gemini replies, and what compare charges for it."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from pdf_extract.compare import MODEL_PRICES, _lacks_thinking, model_price, usage_cost
from pdf_extract.schedule_extraction import _token_usage


def test_gemini_usage_records_thinking_and_cached_tokens():
    response = SimpleNamespace(usage_metadata=SimpleNamespace(
        prompt_token_count=1200,
        candidates_token_count=300,
        cached_content_token_count=None,
        thoughts_token_count=900,
    ))

    assert _token_usage(response) == {
        "prompt_tokens": 1200, "output_tokens": 300, "cached_tokens": 0, "thinking_tokens": 900,
    }


def test_gemini_usage_is_empty_without_metadata():
    assert _token_usage(SimpleNamespace()) == {}


def test_gemini_thinking_is_billed_as_output():
    price = model_price("gemini-3-flash-preview+prompt-abc")
    usage = {"prompt_tokens": 1_000_000, "cached_tokens": 200_000,
             "output_tokens": 100_000, "thinking_tokens": 100_000}
    # 800k fresh in at $0.50 + 200k cached at $0.05 + 200k out at $3.00.
    assert usage_cost(usage, price) == pytest.approx(0.4 + 0.01 + 0.6)


def test_openai_reasoning_is_not_billed_twice():
    price = MODEL_PRICES["gpt-6-luna"]
    usage = {"prompt_tokens": 1_000_000, "output_tokens": 1_000_000, "reasoning_tokens": 800_000}
    assert usage_cost(usage, price) == pytest.approx(0.1 + 0.5)


def test_results_without_thinking_counts_are_flagged():
    assert _lacks_thinking({"prompt_tokens": 1, "output_tokens": 1})
    assert not _lacks_thinking({"prompt_tokens": 1, "thinking_tokens": 0})
    assert not _lacks_thinking({"prompt_tokens": 1, "reasoning_tokens": 0})
    assert not _lacks_thinking({})
