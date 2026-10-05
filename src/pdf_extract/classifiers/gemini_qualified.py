"""Gemini classifier over the qualified schedule schema, for scoring against the labels.

The production Gemini extraction (`schedule_extraction.extract_events`: the same
client, timeout, shared backoff gate, JSON-schema response and lenient fallback)
with its prompt and schema swapped for the ones the OpenAI eval classifier uses:
the shared `schedule_policy.POLICY` and `qualified_schedule.QualifiedSchedulePayload`.

The request's contents are the policy, then the per-bulletin context (known
churches, today's date), then the PDF, so every request starts with the same
text and Gemini's implicit prompt cache can serve it.
"""

from __future__ import annotations

import logging
import re
from datetime import date
from typing import Any

from google.genai import types
from pydantic import ValidationError

from pdf_extract.classifiers.base import ClassifierOptionError
from pdf_extract.classifiers.qualified_schedule import (
    SCHEMA_FINGERPRINT,
    QualifiedSchedulePayload,
    flatten_events,
    render_context,
)
from pdf_extract.classifiers.schedule_policy import POLICY
from pdf_extract.schedule_extraction import (
    DEFAULT_GEMINI_MODEL,
    _gemini_client,
    _generate_content_with_backoff,
    _parse_llm_json,
    _token_usage,
)

LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "gemini-flash-qualified"
RESPONSE_SCHEMA = QualifiedSchedulePayload.model_json_schema()

# What a Gemini model id may look like here: it names a directory under data/runs/.
_MODEL_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


class GeminiQualifiedClassifier:
    name: str
    version: str

    def __init__(self, *, model: str = DEFAULT_GEMINI_MODEL, name: str | None = None) -> None:
        self._model = model
        self.name = name or DEFAULT_NAME
        # Keys the result cache, so it names everything that changes the output.
        self.version = f"{model}+prompt-{SCHEMA_FINGERPRINT}"

    def contents(
        self, pdf_bytes: bytes, *, churches: list[dict[str, Any]], today: date,
    ) -> list[str | types.Part]:
        """The request contents for one bulletin: policy, context, PDF."""
        return [
            POLICY,
            render_context(churches, today.isoformat(), today.strftime("%A")),
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        ]

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        churches: list[dict[str, Any]],
        today: date,
    ) -> dict[str, Any]:
        if not pdf_bytes:
            return flatten_events({})

        response = _generate_content_with_backoff(
            _gemini_client(),
            model=self._model,
            contents=self.contents(pdf_bytes, churches=churches, today=today),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=RESPONSE_SCHEMA,
            ),
        )
        content = response.text or "{}"
        try:
            payload: QualifiedSchedulePayload | dict[str, Any] = (
                QualifiedSchedulePayload.model_validate_json(content)
            )
        except ValidationError as exc:
            LOGGER.warning(
                "%s output failed validation (%s); reading it leniently", self._model, exc,
            )
            payload = _parse_llm_json(content, context=self.name)
        result = flatten_events(payload)
        result["usage"] = _token_usage(response)
        return result


def gemini_qualified_classifier(*, model: str | None = None) -> GeminiQualifiedClassifier:
    """The registry entry's classifier, on `model` in place of the production one when given.

    Another model is named `<model>-qualified`, so its results are cached and
    written under its own `data/runs/<model>-qualified/`.
    """
    if model is None:
        return GeminiQualifiedClassifier()
    if not _MODEL_NAME.fullmatch(model):
        raise ClassifierOptionError(f"{model!r} is not a Gemini model name")
    return GeminiQualifiedClassifier(model=model, name=f"{model}-qualified")
