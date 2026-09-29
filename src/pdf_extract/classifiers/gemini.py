"""Gemini classifier: thin adapter over schedule_extraction.extract_events."""

from __future__ import annotations

import json
from datetime import date
from hashlib import sha256
from typing import Any

from pdf_extract.schedule_extraction import (
    DEFAULT_GEMINI_MODEL,
    EVENTS_SYSTEM_PROMPT,
    SchedulePayload,
    extract_events,
)

# Cached results are keyed by classifier version, so the version has to change
# whenever the output could: the model, the prompt, or the response schema.
# Every classifier sent this prompt and schema builds its version from this.
PROMPT_FINGERPRINT = sha256(
    (
        EVENTS_SYSTEM_PROMPT
        + json.dumps(SchedulePayload.model_json_schema(), sort_keys=True)
    ).encode("utf-8")
).hexdigest()[:12]


class GeminiClassifier:
    name: str
    version: str
    _model: str

    def __init__(self, *, model: str = DEFAULT_GEMINI_MODEL, name: str | None = None) -> None:
        self._model = model
        self.name = name or "gemini-flash"
        self.version = f"{model}+prompt-{PROMPT_FINGERPRINT}"

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        churches: list[dict[str, Any]],
        today: date,
    ) -> dict[str, Any]:
        return extract_events(
            pdf_bytes,
            churches=churches,
            model=self._model,
            today=today,
        )
