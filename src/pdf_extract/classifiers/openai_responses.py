"""OpenAI Responses API classifier over the qualified schedule schema.

One request per bulletin, laid out so the shared part is a cacheable prefix:

1. a developer message holding the static `INSTRUCTIONS`, marked as an explicit
   prompt-cache breakpoint (the response schema in `text.format` is part of
   that prefix too);
2. a user message with the per-bulletin context (known churches, today's date)
   and then the PDF.

Caching runs in explicit mode so the only cache write is that shared prefix.
In the default implicit mode OpenAI puts a breakpoint at the end of the last
user message, which would write every unique PDF to the cache at 1.25x the
input rate for no later hit.

`strict` toggles constrained decoding (`json_schema` with `strict: true`). The
same schema is sent either way, and the reply goes through the same lenient
parse, so the two modes differ only in whether the API enforces the schema.

`pdf_as_images` sends each page rendered to a JPEG (`input_image`, each after a
"Page N of M" line so page numbers stay right) in place of the PDF. Images take
the `original` detail level as well as `low` and `high`; a PDF takes only the
latter two.
"""

from __future__ import annotations

import base64
import io
import json
import logging
import re
import threading
from datetime import date
from typing import Any, Literal

import pypdfium2 as pdfium
from openai import OpenAI
from openai.lib._pydantic import to_strict_json_schema
from pydantic import ValidationError

from pdf_extract.classifiers.base import ClassifierOptionError
from pdf_extract.classifiers.qualified_schedule import (
    INSTRUCTIONS,
    SCHEMA_FINGERPRINT,
    QualifiedSchedulePayload,
    flatten_events,
    render_context,
)

LOGGER = logging.getLogger(__name__)

ReasoningEffort = Literal["none", "minimal", "low", "medium", "high", "xhigh", "max"]
ImageDetail = Literal["auto", "low", "high", "original"]
REASONING_EFFORTS: tuple[str, ...] = ReasoningEffort.__args__
IMAGE_DETAILS: tuple[str, ...] = ImageDetail.__args__
# `input_file` takes no `original`: that level exists only for images.
PDF_DETAILS = ("auto", "low", "high")

# Resolution pages are rendered at when sent as images (US Letter: 1700x2200).
PAGE_DPI = 200
PAGE_JPEG_QUALITY = 90

# What an OpenAI model id may look like here: it names a directory under data/runs/.
_MODEL_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")

# PDFium is not thread-safe, and the runner calls `extract` from a thread pool.
_PDFIUM_LOCK = threading.Lock()

# Seconds one request may take before the SDK gives up (and retries).
REQUEST_TIMEOUT_SECONDS = 600.0


def _without_defaults(schema: Any) -> Any:
    """The schema with `default` keys dropped: every field is required in strict mode."""
    if isinstance(schema, dict):
        return {k: _without_defaults(v) for k, v in schema.items() if k != "default"}
    if isinstance(schema, list):
        return [_without_defaults(v) for v in schema]
    return schema


RESPONSE_SCHEMA = _without_defaults(to_strict_json_schema(QualifiedSchedulePayload))


def render_pages(pdf_bytes: bytes, *, dpi: int = PAGE_DPI) -> list[bytes]:
    """Every page of the PDF as a JPEG, in page order."""
    pages: list[bytes] = []
    with _PDFIUM_LOCK:
        pdf = pdfium.PdfDocument(pdf_bytes)
        try:
            for page in pdf:
                try:
                    image = page.render(scale=dpi / 72).to_pil().convert("RGB")
                finally:
                    page.close()
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=PAGE_JPEG_QUALITY)
                pages.append(buffer.getvalue())
        finally:
            pdf.close()
    return pages


class OpenAIResponsesClassifier:
    name: str
    version: str

    def __init__(
        self,
        *,
        model: str,
        name: str | None = None,
        reasoning_effort: ReasoningEffort = "medium",
        file_detail: ImageDetail = "low",
        pdf_as_images: bool = False,
        strict: bool = True,
        max_retries: int = 5,
    ) -> None:
        if reasoning_effort not in REASONING_EFFORTS:
            raise ClassifierOptionError(f"Unknown reasoning effort {reasoning_effort!r}")
        if file_detail not in (IMAGE_DETAILS if pdf_as_images else PDF_DETAILS):
            raise ClassifierOptionError(
                f"Detail {file_detail!r} is not available for a PDF; "
                "send the pages as images to use it",
            )
        self._model = model
        self._reasoning_effort = reasoning_effort
        self._file_detail = file_detail
        self._pdf_as_images = pdf_as_images
        self._strict = strict
        self._max_retries = max_retries
        self._client: OpenAI | None = None
        self.name = name or model
        # Keys the result cache, so it names everything that changes the output.
        self.version = (
            f"{model}+{'strict' if strict else 'nonstrict'}+reasoning-{reasoning_effort}"
            f"+detail-{file_detail}{f'+pages-{PAGE_DPI}dpi' if pdf_as_images else ''}"
            f"+prompt-{SCHEMA_FINGERPRINT}"
        )

    def _openai(self) -> OpenAI:
        # Built on first use, so listing the registry needs no API key. The
        # client is thread-safe; the SDK retries 429 / 5xx and timeouts itself.
        if self._client is None:
            self._client = OpenAI(max_retries=self._max_retries, timeout=REQUEST_TIMEOUT_SECONDS)
        return self._client

    def request(
        self, pdf_bytes: bytes, *, churches: list[dict[str, Any]], today: date,
    ) -> dict[str, Any]:
        """The keyword arguments for `responses.create`, for one bulletin."""
        return {
            "model": self._model,
            "input": [
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "input_text",
                            "text": INSTRUCTIONS,
                            "prompt_cache_breakpoint": {"mode": "explicit"},
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": render_context(
                                churches, today.isoformat(), today.strftime("%A"),
                            ),
                        },
                        *self._bulletin_parts(pdf_bytes),
                    ],
                },
            ],
            "reasoning": {"effort": self._reasoning_effort},
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "schedule_payload",
                    "schema": RESPONSE_SCHEMA,
                    "strict": self._strict,
                },
            },
            "prompt_cache_options": {"mode": "explicit"},
            "store": False,
        }

    def _bulletin_parts(self, pdf_bytes: bytes) -> list[dict[str, Any]]:
        """The bulletin as content parts: the PDF, or one image per page."""
        if not self._pdf_as_images:
            return [{
                "type": "input_file",
                "filename": "bulletin.pdf",
                "file_data": f"data:application/pdf;base64,{_b64(pdf_bytes)}",
                "detail": self._file_detail,
            }]
        pages = render_pages(pdf_bytes)
        parts: list[dict[str, Any]] = []
        for number, jpeg in enumerate(pages, start=1):
            parts.append({"type": "input_text", "text": f"Page {number} of {len(pages)}"})
            parts.append({
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{_b64(jpeg)}",
                "detail": self._file_detail,
            })
        return parts

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        churches: list[dict[str, Any]],
        today: date,
    ) -> dict[str, Any]:
        if not pdf_bytes:
            return flatten_events({})

        response = self._openai().responses.create(
            **self.request(pdf_bytes, churches=churches, today=today),
        )
        if response.status != "completed":
            LOGGER.warning(
                "%s response %s is %s (%s)",
                self._model, response.id, response.status, response.incomplete_details,
            )
        result = flatten_events(_parse(response.output_text or "", model=self._model))
        result["usage"] = _usage(response)
        result["response_id"] = response.id
        return result


def responses_classifier(
    default_model: str, *, model: str | None = None, strict: bool = True, **options: Any,
) -> OpenAIResponsesClassifier:
    """A registry entry's classifier, on `model` in place of its default when given.

    The classifier is named after the model it runs (`-nonstrict` appended when
    `strict` is off), so another model's results are cached and written under
    its own `data/runs/<model>/`.
    """
    model = model or default_model
    if not _MODEL_NAME.fullmatch(model):
        raise ClassifierOptionError(f"{model!r} is not an OpenAI model name")
    return OpenAIResponsesClassifier(
        model=model, name=model if strict else f"{model}-nonstrict", strict=strict, **options,
    )


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _parse(text: str, *, model: str) -> QualifiedSchedulePayload | dict[str, Any]:
    """The validated payload, or the raw JSON object when it does not validate.

    Strict mode should always validate; a refusal or a truncated reply comes back
    as an empty result so the bulletin scores as zero events rather than crashing.
    """
    try:
        return QualifiedSchedulePayload.model_validate_json(text)
    except ValidationError as exc:
        LOGGER.warning("%s output failed validation (%s); reading it leniently", model, exc)
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        LOGGER.warning("%s returned no JSON object: %r", model, text[:200])
        return {}
    return data if isinstance(data, dict) else {}


def _usage(response: Any) -> dict[str, int]:
    """Token counts for run cost reporting, including the prompt-cache split."""
    usage = getattr(response, "usage", None)
    if usage is None:
        return {}
    input_details = getattr(usage, "input_tokens_details", None)
    output_details = getattr(usage, "output_tokens_details", None)
    counts = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "cached_tokens": getattr(input_details, "cached_tokens", None),
        "cache_write_tokens": getattr(input_details, "cache_write_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "reasoning_tokens": getattr(output_details, "reasoning_tokens", None),
    }
    return {k: v for k, v in counts.items() if isinstance(v, int)}
