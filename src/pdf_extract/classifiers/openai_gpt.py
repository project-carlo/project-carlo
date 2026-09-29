"""OpenAI classifiers that read the bulletin PDF themselves (gpt-5.4-mini, luna-pdf).

Sends a request built like the Gemini one, so the two compare on equal terms:
the same events prompt, then the bulletin PDF (as a base64 input_file), with
the same `SchedulePayload` JSON schema Gemini is given. The reply is parsed
and normalised by the same code as Gemini's reply.

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
import time
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


def openai_usage(response: Any) -> dict[str, int]:
    """Token counts of a Responses API call, in the keys run reports sum.

    OpenAI counts `reasoning_tokens` inside `output_tokens`, and `cached_tokens`
    inside `prompt_tokens`.
    """
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
        file_detail: FileDetail | None = None,
    ) -> None:
        """`file_detail` sets the PDF input's `detail`; None leaves OpenAI's default."""
        self._model = model
        self._max_retries = max_retries
        self._reasoning_effort = reasoning_effort
        self._file_detail = file_detail
        self.name = name or model
        self.version = (
            model
            + (f"+effort-{reasoning_effort}" if reasoning_effort else "")
            + (f"+detail-{file_detail}" if file_detail else "")
            + f"+prompt-{PROMPT_FINGERPRINT}"
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

        extra: dict[str, Any] = {}
        if self._reasoning_effort:
            extra["reasoning"] = {"effort": self._reasoning_effort}

        started = time.monotonic()
        # The SDK retries 429 / 5xx responses internally; bump the budget.
        client = OpenAI(max_retries=self._max_retries, timeout=600)
        response = client.responses.create(
            model=self._model,
            # Prompt, then PDF: the order Gemini gets them in.
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
            **extra,
        )
        llm_seconds = time.monotonic() - started

        content = response.output_text
        if not content:
            # Refusal or an empty reply: degrade to an empty result so the
            # bulletin shows up in the run as zero-events rather than crashing.
            LOGGER.warning(
                "OpenAI %s returned no output (status=%s); treating as empty bulletin",
                self._model,
                getattr(response, "status", None),
            )
        result = events_from_json(content or "{}", context=f"openai {self._model}")
        result["usage"] = openai_usage(response)
        result["timing"] = {"llm_seconds": round(llm_seconds, 3)}
        return result
