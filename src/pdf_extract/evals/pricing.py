"""API list prices, for putting a dollar figure on an eval run's token usage.

Prices are USD per million tokens at the standard tier (and, where a model's
`flex` is set, the flex tier), as published on the date in PRICES_AS_OF; update
both together. A model missing from PRICES, or a flex call on a model with no
flex price, is reported unpriced rather than guessed at.

The usage keys are the ones the classifiers record:

- OpenAI Responses (`openai_responses._usage`): `input_tokens` includes
  `cached_tokens` and `cache_write_tokens`; `output_tokens` includes
  `reasoning_tokens`.
- Gemini (`schedule_extraction._token_usage`): `prompt_tokens` includes
  `cached_tokens`; `output_tokens` leaves out `thinking_tokens`, which are
  billed as output.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PRICES_AS_OF = "2026-10-12"


@dataclass(frozen=True)
class ModelPrice:
    input: float
    cached_input: float
    output: float
    cache_write: float | None = None
    """None: cache writes cost the same as input."""
    long_context_over: int | None = None
    """Input tokens above which the whole request is billed at `long_context`."""
    long_context: ModelPrice | None = None
    flex: ModelPrice | None = None
    """The flex service tier's prices, None when unknown."""
    source: str = ""


PRICES: dict[str, ModelPrice] = {
    "gpt-6-luna": ModelPrice(
        input=0.10, cached_input=0.01, cache_write=0.125, output=0.50,
        long_context_over=272_000,
        long_context=ModelPrice(input=0.20, cached_input=0.02, cache_write=0.25, output=0.75),
        flex=ModelPrice(
            input=0.05, cached_input=0.005, cache_write=0.0625, output=0.25,
            long_context_over=272_000,
            long_context=ModelPrice(
                input=0.10, cached_input=0.01, cache_write=0.125, output=0.375,
            ),
        ),
        source="https://developers.openai.com/api/docs/pricing",
    ),
    "gemini-3-flash-preview": ModelPrice(
        input=0.50, cached_input=0.05, output=3.00,
        source="https://ai.google.dev/gemini-api/docs/pricing",
    ),
}

# A Gemini usage record made before thinking tokens were recorded leaves out
# billed output, so a cost from it is too low.
THINKING_KEY = "thinking_tokens"
_REPORTS_THINKING = frozenset({"gemini-3-flash-preview"})


def model_of(classifier_version: str | None) -> str | None:
    """The model a classifier version ran on: the part before its first `+`."""
    if not classifier_version:
        return None
    return classifier_version.partition("+")[0] or None


def price_for(model: str | None) -> ModelPrice | None:
    return PRICES.get(model) if model else None


def _count(usage: dict[str, Any], key: str) -> int:
    value = usage.get(key)
    return value if isinstance(value, int) else 0


def call_cost(
    model: str | None, usage: dict[str, Any], *, service_tier: str | None = None,
) -> float | None:
    """The USD cost of one call's `usage` on `model`, or None when it has no price.

    `service_tier` is the tier the response says served the call; any tier but
    flex is priced at the standard rate.
    """
    price = price_for(model)
    if price is not None and service_tier == "flex":
        price = price.flex
    if price is None:
        return None
    total_input = _count(usage, "input_tokens") or _count(usage, "prompt_tokens")
    if price.long_context_over is not None and total_input > price.long_context_over:
        price = price.long_context or price
    cached = _count(usage, "cached_tokens")
    written = _count(usage, "cache_write_tokens")
    uncached = max(total_input - cached - written, 0)
    output = _count(usage, "output_tokens") + _count(usage, THINKING_KEY)
    cache_write = price.input if price.cache_write is None else price.cache_write
    dollars = (
        uncached * price.input + cached * price.cached_input
        + written * cache_write + output * price.output
    )
    return dollars / 1_000_000


def thinking_unrecorded(model: str | None, usage: dict[str, Any]) -> bool:
    """Whether `usage` comes from a model that bills thinking separately but lacks it."""
    return model in _REPORTS_THINKING and THINKING_KEY not in usage
