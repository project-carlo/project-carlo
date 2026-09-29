"""OpenAI classifiers (gpt-5.4-mini, gpt-6-luna).

Sends a request built like the Gemini one, so the two can be compared on
equal terms: the same events prompt, then the bulletin PDF (as a base64
input_file), with the same `SchedulePayload` JSON schema Gemini is given. The
reply is parsed and normalised by the same code as Gemini's reply.

The schema goes over non-strict: OpenAI's strict mode only accepts schemas
rewritten to its subset (every property required, no defaults), which would
no longer be the schema Gemini sees.

Module is named openai_gpt.py (not openai.py) to avoid shadowing the upstream
`openai` package.
"""

from __future__ import annotations

import base64
import json
import logging
from datetime import date
from typing import Any, Literal

from openai import OpenAI

from pdf_extract.classifiers.gemini import PROMPT_FINGERPRINT
from pdf_extract.schedule_extraction import (
    EVENTS_SYSTEM_PROMPT,
    SchedulePayload,
    events_from_json,
    reconstruct_events,
)

LOGGER = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-5.4-mini"

FileDetail = Literal["low", "high"]


class OpenAIClassifier:
    name: str
    version: str
    model: str

    def __init__(
        self,
        *,
        model: str = DEFAULT_MODEL,
        name: str | None = None,
        file_detail: FileDetail | None = None,
        max_retries: int = 5,
    ) -> None:
        """`file_detail` sets the PDF input's `detail`; None leaves OpenAI's default."""
        self.model = model
        self._file_detail = file_detail
        self._max_retries = max_retries
        self.name = name or model
        self.version = f"{model}+prompt-{PROMPT_FINGERPRINT}" + (
            f"+detail-{file_detail}" if file_detail else ""
        )

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
        file_part: dict[str, Any] = {
            "type": "input_file",
            "filename": "bulletin.pdf",
            "file_data": f"data:application/pdf;base64,{encoded}",
        }
        if self._file_detail:
            file_part["detail"] = self._file_detail

        # The SDK retries 429 / 5xx responses internally; bump the budget.
        client = OpenAI(max_retries=self._max_retries)
        response = client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": prompt}, file_part],
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "SchedulePayload",
                    "schema": SchedulePayload.model_json_schema(),
                    "strict": False,
                }
            },
        )

        content = response.output_text
        if not content:
            # Refusal or an empty reply: degrade to an empty result so the
            # bulletin shows up in the run as zero-events rather than crashing.
            LOGGER.warning(
                "OpenAI %s returned no output (status=%s); treating as empty bulletin",
                self.model,
                getattr(response, "status", None),
            )
        result = events_from_json(content or "{}", context=f"openai {self.model}")
        result["usage"] = _token_usage(response)
        return result


def _token_usage(response: Any) -> dict[str, int]:
    """Token counts of a Responses API reply, in the keys of `pricing.USAGE_KEYS`.

    OpenAI counts reasoning tokens inside `output_tokens`; they are split out
    here so both providers' usage reads the same way.
    """
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    cached = getattr(getattr(usage, "input_tokens_details", None), "cached_tokens", None)
    reasoning = getattr(getattr(usage, "output_tokens_details", None), "reasoning_tokens", None)
    cached = cached if isinstance(cached, int) else 0
    reasoning = reasoning if isinstance(reasoning, int) else 0
    return {
        "prompt_tokens": int(usage.input_tokens),
        "cached_prompt_tokens": cached,
        "output_tokens": int(usage.output_tokens) - reasoning,
        "thinking_tokens": reasoning,
    }
