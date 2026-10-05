"""Gemini classifier over the qualified schedule schema, for scoring against the labels.

The production Gemini call (`schedule_extraction.request_schedule`, which
`extract_events` also makes: the same client, timeout, shared backoff gate,
JSON-schema response and lenient fallback) with its prompt and schema swapped
for the ones the OpenAI eval classifier uses: the shared `schedule_policy.POLICY`
and `qualified_schedule.QualifiedSchedulePayload`.

The request's contents are the policy, then the per-bulletin context (known
churches, today's date), then the PDF, so every request starts with the same
text and Gemini's implicit prompt cache can serve it.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from google import genai
from google.genai import types

from pdf_extract.classifiers.base import validate_model_name
from pdf_extract.classifiers.qualified_schedule import (
    SCHEMA_FINGERPRINT,
    QualifiedSchedulePayload,
    flatten_events,
    render_context,
)
from pdf_extract.classifiers.schedule_policy import POLICY
from pdf_extract.schedule_extraction import DEFAULT_GEMINI_MODEL, gemini_client, request_schedule

DEFAULT_NAME = "gemini-flash-qualified"


class GeminiQualifiedClassifier:
    name: str
    version: str

    def __init__(self, *, model: str = DEFAULT_GEMINI_MODEL, name: str | None = None) -> None:
        self._model = model
        self.name = name or DEFAULT_NAME
        # Keys the result cache, so it names everything that changes the output.
        self.version = f"{model}+prompt-{SCHEMA_FINGERPRINT}"
        self._client: genai.Client | None = None

    def _gemini(self) -> genai.Client:
        """One client for every bulletin, built on first use (building a classifier
        for its name and version needs no API key)."""
        if self._client is None:
            self._client = gemini_client()
        return self._client

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
        payload, usage = request_schedule(
            self.contents(pdf_bytes, churches=churches, today=today),
            payload_model=QualifiedSchedulePayload,
            model=self._model,
            context=self.name,
            client=self._gemini(),
        )
        result = flatten_events(payload)
        result["usage"] = usage
        return result


def gemini_qualified_classifier(*, model: str | None = None) -> GeminiQualifiedClassifier:
    """The registry entry's classifier, on `model` in place of the production one when given.

    Another model is named `<model>-qualified`, so its results are cached and
    written under its own `data/runs/<model>-qualified/`.
    """
    if model is None:
        return GeminiQualifiedClassifier()
    validate_model_name(model, "Gemini")
    return GeminiQualifiedClassifier(model=model, name=f"{model}-qualified")
