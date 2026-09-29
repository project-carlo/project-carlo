"""List prices for the models the classifiers call, and the cost of one call.

Every classifier reports token usage in the same normalised shape (see
`schedule_extraction._token_usage` and `classifiers.openai_gpt`):

    prompt_tokens         all input tokens, cached ones included
    cached_prompt_tokens  the part of prompt_tokens served from the provider's cache
    output_tokens         visible output tokens
    thinking_tokens       reasoning/thinking tokens (billed as output)

Prices are USD per million tokens at the standard (non-batch) paid tier.
Update them here when a provider changes its price list.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelPrice:
    input: float
    cached_input: float
    output: float


MODEL_PRICES: dict[str, ModelPrice] = {
    # https://ai.google.dev/gemini-api/docs/pricing (text/image/video input).
    "gemini-3-flash-preview": ModelPrice(input=0.50, cached_input=0.05, output=3.00),
    # https://developers.openai.com/api/docs/models/gpt-6-luna
    "gpt-6-luna": ModelPrice(input=0.10, cached_input=0.01, output=0.50),
}

USAGE_KEYS = ("prompt_tokens", "cached_prompt_tokens", "output_tokens", "thinking_tokens")


def price_for(model: str | None) -> ModelPrice | None:
    return MODEL_PRICES.get(model) if model else None


def usage_cost(usage: dict[str, Any], price: ModelPrice) -> float:
    """USD cost of one call's normalised usage."""
    prompt = int(usage.get("prompt_tokens") or 0)
    cached = min(int(usage.get("cached_prompt_tokens") or 0), prompt)
    output = int(usage.get("output_tokens") or 0) + int(usage.get("thinking_tokens") or 0)
    return (
        (prompt - cached) * price.input + cached * price.cached_input + output * price.output
    ) / 1_000_000


def summarize_usage(
    usages: list[dict[str, Any] | None], price: ModelPrice | None,
) -> dict[str, Any]:
    """Token totals and cost over a set of results' usage (None: result had none).

    `results_missing_thinking_tokens` counts results recorded before thinking
    tokens were: their cost leaves thinking out, so a total that includes one
    is a lower bound.
    """
    totals = dict.fromkeys(USAGE_KEYS, 0)
    with_usage = 0
    legacy = 0
    cost = 0.0
    for usage in usages:
        if not usage:
            continue
        with_usage += 1
        if "thinking_tokens" not in usage:
            legacy += 1
        for key in USAGE_KEYS:
            totals[key] += int(usage.get(key) or 0)
        if price is not None:
            cost += usage_cost(usage, price)
    return {
        "results": len(usages),
        "results_with_usage": with_usage,
        "results_missing_thinking_tokens": legacy,
        **totals,
        "cost_usd": round(cost, 6) if price is not None else None,
    }
