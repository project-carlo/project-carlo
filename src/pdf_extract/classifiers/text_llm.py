"""Text → LLM classifiers: a non-LLM PDF-to-text step, then a small OpenAI model.

The production classifier hands the PDF to Gemini, which reads the pages
itself. These classifiers split that in two so each half can be swapped and
measured: a text extractor (see `pdf_extract.text_extractors`) turns the
bulletin into plain text, and an OpenAI model reads only that text and fills
the same `SchedulePayload` schema, so the output compares one-to-one with the
Gemini baseline.

Extracted text is cached on local disk under data/runs/text/<extractor>/,
keyed by extractor version and a hash of the PDF bytes, so re-running with a
different model or prompt does not pay for a slow extraction again. The files
are also there to read when a stack misses an event: most misses are visible
in the text.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Any

from openai import OpenAI

from pdf_extract.classifiers.openai_gpt import openai_usage
from pdf_extract.paths import DATA_DIR
from pdf_extract.schedule_extraction import (
    EVENTS_SYSTEM_PROMPT,
    SchedulePayload,
    reconstruct_events,
)
from pdf_extract.text_extractors import TextExtractor, get_text_extractor, page_header

LOGGER = logging.getLogger(__name__)

DEFAULT_TEXT_MODEL = "gpt-6-luna"
DEFAULT_REASONING_EFFORT = "medium"

TEXT_CACHE_DIR = DATA_DIR / "runs" / "text"

_PDF_INTRO = "from the attached Catholic parish bulletin PDF."
if _PDF_INTRO not in EVENTS_SYSTEM_PROMPT:
    raise RuntimeError("EVENTS_SYSTEM_PROMPT was reworded; update TEXT_EVENTS_PROMPT to match")

# The production prompt, reworded for a text input: same instructions and
# schema, so differences in results come from the input, not the prompt.
TEXT_EVENTS_PROMPT = EVENTS_SYSTEM_PROMPT.replace(
    _PDF_INTRO,
    "from a Catholic parish bulletin. The bulletin was converted from PDF to text by an "
    "automated tool; it is given below, after the instructions.",
).replace("the attached PDF", "the bulletin") + f"""
# About the bulletin text

- Each page starts with a line like `{page_header(1)}`. Use that number as `page_number`.
- The conversion may have lost or reordered some of the page layout: columns can be
  interleaved, table cells split across lines, and text inside images may be missing or
  contain OCR errors. Bracketed position hints such as `[x 0-33% y 10-40%]`, where present,
  give where a block sits on the page (x from the left edge, y from the top); use them to
  work out which heading, day or church a time belongs to.
- Do not invent events that are not supported by the text.
"""

_PROMPT_FINGERPRINT = sha256(
    (TEXT_EVENTS_PROMPT + json.dumps(SchedulePayload.model_json_schema(), sort_keys=True))
    .encode("utf-8")
).hexdigest()[:12]


def _text_cache_path(extractor: TextExtractor, pdf_bytes: bytes) -> Path:
    digest = sha256(pdf_bytes).hexdigest()
    version = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in extractor.version)
    return TEXT_CACHE_DIR / extractor.name / version / f"{digest}.txt"


def extract_text_cached(extractor: TextExtractor, pdf_bytes: bytes) -> tuple[str, float]:
    """The extractor's text for a PDF, from the local cache when possible.

    Returns (text, seconds the extraction took). On a cache hit the seconds
    are the ones recorded when the text was first extracted: they describe
    the stack, and reports compare them across runs.
    """
    path = _text_cache_path(extractor, pdf_bytes)
    timing_path = path.with_suffix(".json")
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        pass
    else:
        try:
            seconds = float(json.loads(timing_path.read_text(encoding="utf-8"))["seconds"])
        except (OSError, ValueError, KeyError, TypeError):
            seconds = 0.0
        return text, seconds

    started = time.monotonic()
    text = extractor.extract_text(pdf_bytes)
    elapsed = time.monotonic() - started
    path.parent.mkdir(parents=True, exist_ok=True)
    timing_path.write_text(json.dumps({"seconds": round(elapsed, 3)}) + "\n", encoding="utf-8")
    # Write-then-rename, so a concurrent reader never sees half a file.
    tmp = path.with_name(f".{path.name}.tmp-{threading.get_ident()}")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)
    return text, elapsed


class TextLLMClassifier:
    """Extract text with a registered text extractor, then classify it with OpenAI."""

    name: str
    version: str

    def __init__(
        self,
        *,
        extractor: str,
        name: str,
        model: str = DEFAULT_TEXT_MODEL,
        reasoning_effort: str | None = DEFAULT_REASONING_EFFORT,
        max_retries: int = 5,
    ) -> None:
        self._extractor_name = extractor
        self._extractor: TextExtractor | None = None
        self._model = model
        self._reasoning_effort = reasoning_effort
        self._max_retries = max_retries
        self.name = name
        # The extractor's version is only known once it is loaded; loading it
        # here keeps `version` honest for the result cache.
        extractor_version = self._get_extractor().version
        self.version = (
            f"{model}+effort-{reasoning_effort or 'default'}"
            f"+{extractor}-{extractor_version}+prompt-{_PROMPT_FINGERPRINT}"
        )

    def _get_extractor(self) -> TextExtractor:
        if self._extractor is None:
            self._extractor = get_text_extractor(self._extractor_name)
        return self._extractor

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        churches: list[dict[str, Any]],
        today: date,
    ) -> dict[str, Any]:
        if not pdf_bytes:
            return reconstruct_events({})

        text, text_seconds = extract_text_cached(self._get_extractor(), pdf_bytes)

        prompt = TEXT_EVENTS_PROMPT.format(
            churches_json=json.dumps(churches, ensure_ascii=False),
            today_iso=today.isoformat(),
            today_day_of_week=today.strftime("%A"),
        )
        request: dict[str, Any] = {
            "model": self._model,
            "input": [
                {"role": "developer", "content": prompt},
                {"role": "user", "content": f"# Bulletin text\n\n{text}"},
            ],
            "text_format": SchedulePayload,
        }
        if self._reasoning_effort:
            request["reasoning"] = {"effort": self._reasoning_effort}

        started = time.monotonic()
        # The SDK retries 429 / 5xx responses internally; bump the budget.
        client = OpenAI(max_retries=self._max_retries, timeout=600)
        response = client.responses.parse(**request)
        llm_seconds = time.monotonic() - started

        parsed = response.output_parsed
        if parsed is None:
            LOGGER.warning(
                "%s returned no parsed output; treating as empty bulletin", self._model,
            )
            result = reconstruct_events({})
        else:
            result = reconstruct_events(parsed)
        result["usage"] = openai_usage(response)
        result["timing"] = {
            "text_seconds": round(text_seconds, 3),
            "llm_seconds": round(llm_seconds, 3),
        }
        result["text_chars"] = len(text)
        return result
