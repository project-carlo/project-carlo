"""List-price cost of a call's recorded token usage."""

from __future__ import annotations

import pytest

from pdf_extract.evals.pricing import call_cost, model_of, thinking_unrecorded


def test_model_of_takes_the_version_before_its_options():
    assert model_of("gpt-6-luna+strict+reasoning-medium+detail-low") == "gpt-6-luna"
    assert model_of("gemini-3-flash-preview+prompt-abc") == "gemini-3-flash-preview"
    assert model_of("gpt-5.4-mini") == "gpt-5.4-mini"
    assert model_of(None) is None


def test_openai_cache_reads_and_writes_come_out_of_input():
    usage = {
        "input_tokens": 100_000, "cached_tokens": 20_000, "cache_write_tokens": 10_000,
        "output_tokens": 10_000, "reasoning_tokens": 6_000,
    }
    # 70k × 0.10 + 20k × 0.01 + 10k × 0.125 + 10k × 0.50 (reasoning is in output).
    assert call_cost("gpt-6-luna", usage) == pytest.approx(0.007 + 0.0002 + 0.00125 + 0.005)


def test_openai_long_context_bills_the_whole_request_at_the_higher_rate():
    usage = {"input_tokens": 300_000, "output_tokens": 10_000}
    assert call_cost("gpt-6-luna", usage) == pytest.approx(0.3 * 0.20 + 0.01 * 0.75)


def test_gemini_thinking_is_billed_as_output():
    usage = {
        "prompt_tokens": 100_000, "cached_tokens": 40_000,
        "output_tokens": 10_000, "thinking_tokens": 30_000,
    }
    # 60k × 0.50 + 40k × 0.05 + 40k × 3.00.
    assert call_cost("gemini-3-flash-preview", usage) == pytest.approx(0.03 + 0.002 + 0.12)
    assert not thinking_unrecorded("gemini-3-flash-preview", usage)
    assert thinking_unrecorded("gemini-3-flash-preview", {"prompt_tokens": 1})
    assert not thinking_unrecorded("gpt-6-luna", {"input_tokens": 1})


def test_a_model_without_a_price_is_not_priced():
    assert call_cost("gpt-6.1-sol", {"input_tokens": 1_000}) is None
    assert call_cost(None, {"input_tokens": 1_000}) is None
