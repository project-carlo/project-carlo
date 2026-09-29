"""List-price cost of classifier calls, and the usage Gemini replies are read into."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from pdf_extract.pricing import MODEL_PRICES, ModelPrice, summarize_usage, usage_cost
from pdf_extract.schedule_extraction import _token_usage

PRICE = ModelPrice(input=1.0, cached_input=0.1, output=10.0)


def test_cost_bills_cached_input_at_its_rate_and_thinking_as_output():
    usage = {
        "prompt_tokens": 1_000_000,
        "cached_prompt_tokens": 400_000,
        "output_tokens": 50_000,
        "thinking_tokens": 50_000,
    }
    # 600k fresh input at $1 + 400k cached at $0.10 + 100k output at $10.
    assert usage_cost(usage, PRICE) == pytest.approx(0.6 + 0.04 + 1.0)


def test_summary_totals_and_flags_results_without_thinking_counts():
    new = {"prompt_tokens": 1_000_000, "cached_prompt_tokens": 0, "output_tokens": 0,
           "thinking_tokens": 100_000}
    legacy = {"prompt_tokens": 1_000_000, "output_tokens": 0}

    summary = summarize_usage([new, legacy, None], PRICE)

    assert summary["results"] == 3
    assert summary["results_with_usage"] == 2
    assert summary["results_missing_thinking_tokens"] == 1
    assert summary["prompt_tokens"] == 2_000_000
    assert summary["thinking_tokens"] == 100_000
    assert summary["cost_usd"] == pytest.approx(3.0)


def test_summary_without_a_price_has_no_cost():
    assert summarize_usage([{"prompt_tokens": 5}], None)["cost_usd"] is None


def test_the_benchmarked_models_are_priced():
    assert {"gemini-3-flash-preview", "gpt-6-luna"} <= set(MODEL_PRICES)


def test_gemini_usage_records_thinking_and_cached_tokens():
    response = SimpleNamespace(usage_metadata=SimpleNamespace(
        prompt_token_count=1200,
        candidates_token_count=300,
        cached_content_token_count=None,
        thoughts_token_count=900,
    ))

    assert _token_usage(response) == {
        "prompt_tokens": 1200,
        "output_tokens": 300,
        "cached_prompt_tokens": 0,
        "thinking_tokens": 900,
    }


def test_gemini_usage_is_empty_without_metadata():
    assert _token_usage(SimpleNamespace()) == {}
