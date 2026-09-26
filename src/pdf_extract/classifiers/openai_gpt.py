"""OpenAI gpt-5.4-mini classifier.

Uses the Responses API with a base64 PDF input_file and a Pydantic-typed
structured output (text_format=SchedulePayload). Reuses the prompt and the
flat-event normalizer from schedule_extraction so output shape matches the
Gemini classifier exactly.

Module is named openai_gpt.py (not openai.py) to avoid shadowing the upstream
`openai` package.
"""

from __future__ import annotations

import base64
import json
import logging
import time
from datetime import date
from typing import Any

from openai import OpenAI

from pdf_extract.schedule_extraction import (
    EVENTS_SYSTEM_PROMPT,
    SchedulePayload,
    reconstruct_events,
)

LOGGER = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-5.4-mini"


def openai_usage(response: Any) -> dict[str, int]:
    """Token counts of a Responses API call, in the keys run reports sum."""
    usage = getattr(response, "usage", None)
    input_details = getattr(usage, "input_tokens_details", None)
    output_details = getattr(usage, "output_tokens_details", None)
    counts = {
        "prompt_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "cached_tokens": getattr(input_details, "cached_tokens", None),
        "reasoning_tokens": getattr(output_details, "reasoning_tokens", None),
    }
    return {k: v for k, v in counts.items() if isinstance(v, int)}


class OpenAIClassifier:
    name: str
    version: str
    _model: str

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        name: str | None = None,
        max_retries: int = 5,
        reasoning_effort: str | None = None,
    ) -> None:
        self._model = model
        self._max_retries = max_retries
        self._reasoning_effort = reasoning_effort
        self.name = name or model
        self.version = f"{model}+effort-{reasoning_effort}" if reasoning_effort else model

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        churches: list[dict[str, Any]],
        today: date,
    ) -> dict[str, Any]:
        if not pdf_bytes:
            return reconstruct_events({})

        prompt = EVENTS_SYSTEM_PROMPT.format(
            churches_json=json.dumps(churches, ensure_ascii=False),
            today_iso=today.isoformat(),
            today_day_of_week=today.strftime("%A"),
        )
        encoded = base64.b64encode(pdf_bytes).decode("ascii")

        extra: dict[str, Any] = {}
        if self._reasoning_effort:
            extra["reasoning"] = {"effort": self._reasoning_effort}

        started = time.monotonic()
        # The SDK retries 429 / 5xx responses internally; bump the budget.
        client = OpenAI(max_retries=self._max_retries, timeout=600)
        response = client.responses.parse(
            model=self._model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "filename": "bulletin.pdf",
                            "file_data": f"data:application/pdf;base64,{encoded}",
                        },
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                    ],
                }
            ],
            text_format=SchedulePayload,
            **extra,
        )
        llm_seconds = time.monotonic() - started

        parsed = response.output_parsed
        if parsed is None:
            # Refusal or schema mismatch — log and degrade to empty result so the
            # bulletin shows up in the run as zero-events rather than crashing.
            LOGGER.warning(
                "OpenAI %s returned no parsed output; treating as empty bulletin",
                self._model,
            )
            result = reconstruct_events({})
        else:
            result = reconstruct_events(parsed)
        result["usage"] = openai_usage(response)
        result["timing"] = {"llm_seconds": round(llm_seconds, 3)}
        return result
