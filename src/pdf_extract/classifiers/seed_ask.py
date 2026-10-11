"""One question about one bulletin, for the seeding agent's second opinions (`seed ask`).

The request is the extraction policy (`schedule_policy.POLICY`, sent first and
unchanged, so it is served from the prompt cache as the classifiers' is), then
the parish's churches, the date and the question, then the PDF. The answer is
`answer`, the `page` it is on, and the words read there (`quote`), so the agent
can check it against the bulletin itself.

`version` names the model, the prompt and the schema, and keys the cache as a
classifier's version does (docs/seeding-plan.md, "Tools").
"""

from __future__ import annotations

import base64
import json
from datetime import date
from typing import Any

from google.genai import types
from openai import OpenAI
from openai.lib._pydantic import to_strict_json_schema
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from pdf_extract.classifiers.base import ClassifierOptionError
from pdf_extract.classifiers.openai_responses import (
    REQUEST_TIMEOUT_SECONDS,
    _usage,
    _without_defaults,
)
from pdf_extract.classifiers.qualified_schedule import fingerprint
from pdf_extract.classifiers.schedule_policy import POLICY
from pdf_extract.schedule_extraction import gemini_client, request_schedule

OPENAI_MODEL = "gpt-6.1-sol"
GEMINI_MODEL = "gemini-3-flash-preview"
MODELS = (OPENAI_MODEL, GEMINI_MODEL)

QUESTION_TEMPLATE = """\
# Known churches for this parish

```json
{churches_json}
```

# Today's date

{today_iso} ({today_day_of_week})

# Your task here

Do not extract the schedule. Answer only the question below about the attached
bulletin, reading it with the policy above. Give the page the answer is printed
on (pages counted from 1 in the PDF as attached, null when the bulletin does
not say) and quote the bulletin's own words there, exactly as printed. When the
bulletin does not answer the question, say so in `answer` and leave `quote`
empty.

# Question

{question}
"""


class AskAnswer(BaseModel):
    model_config = ConfigDict(extra="ignore")

    answer: str = Field(description="The answer, in a sentence or two.")
    page: int | None = Field(description="The PDF page the answer is printed on, or null.")
    quote: str = Field(description="The bulletin's words on that page, exactly as printed.")


RESPONSE_SCHEMA = _without_defaults(to_strict_json_schema(AskAnswer))
PROMPT_FINGERPRINT = fingerprint(
    POLICY, QUESTION_TEMPLATE, json.dumps(AskAnswer.model_json_schema(), sort_keys=True),
)


def render_question(
    churches: list[dict[str, Any]], today: date, question: str,
) -> str:
    return QUESTION_TEMPLATE.format(
        churches_json=json.dumps(churches, ensure_ascii=False),
        today_iso=today.isoformat(),
        today_day_of_week=today.strftime("%A"),
        question=question.strip(),
    )


def _answer(payload: AskAnswer | dict[str, Any]) -> dict[str, Any]:
    data = payload.model_dump() if isinstance(payload, AskAnswer) else payload
    page = data.get("page")
    return {
        "answer": data.get("answer") if isinstance(data.get("answer"), str) else "",
        "page": page if isinstance(page, int) and not isinstance(page, bool) else None,
        "quote": data.get("quote") if isinstance(data.get("quote"), str) else "",
    }


class SeedAsker:
    """Asks `model` one question about one bulletin."""

    name = "seed-ask"

    def __init__(self, model: str) -> None:
        if model not in MODELS:
            raise ClassifierOptionError(f"seed ask takes {' or '.join(MODELS)}, not {model!r}")
        self.model = model
        self.version = f"{model}+prompt-{PROMPT_FINGERPRINT}"
        self._client: Any = None

    def ask(
        self, pdf_bytes: bytes, *, churches: list[dict[str, Any]], today: date, question: str,
    ) -> dict[str, Any]:
        """{"answer", "page", "quote", "usage"} for one question."""
        text = render_question(churches, today, question)
        if self.model == GEMINI_MODEL:
            return self._ask_gemini(pdf_bytes, text)
        return self._ask_openai(pdf_bytes, text)

    def _ask_openai(self, pdf_bytes: bytes, text: str) -> dict[str, Any]:
        if self._client is None:
            self._client = OpenAI(max_retries=5, timeout=REQUEST_TIMEOUT_SECONDS)
        response = self._client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "developer",
                    "content": [{
                        "type": "input_text", "text": POLICY,
                        "prompt_cache_breakpoint": {"mode": "explicit"},
                    }],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": text},
                        {
                            "type": "input_file",
                            "filename": "bulletin.pdf",
                            "file_data": "data:application/pdf;base64,"
                            + base64.b64encode(pdf_bytes).decode("ascii"),
                            # A question is about small print: read it closely.
                            "detail": "high",
                        },
                    ],
                },
            ],
            reasoning={"effort": "medium"},
            text={"format": {
                "type": "json_schema", "name": "seed_answer", "schema": RESPONSE_SCHEMA,
                "strict": True,
            }},
            prompt_cache_options={"mode": "explicit"},
            store=False,
        )
        try:
            payload: AskAnswer | dict[str, Any] = AskAnswer.model_validate_json(
                response.output_text or "",
            )
        except ValidationError:
            try:
                loaded = json.loads(response.output_text or "")
            except json.JSONDecodeError:
                loaded = {}
            payload = loaded if isinstance(loaded, dict) else {}
        return {**_answer(payload), "usage": _usage(response)}

    def _ask_gemini(self, pdf_bytes: bytes, text: str) -> dict[str, Any]:
        if self._client is None:
            self._client = gemini_client()
        payload, usage = request_schedule(
            [POLICY, text, types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")],
            payload_model=AskAnswer,
            model=self.model,
            context=self.name,
            client=self._client,
        )
        return {**_answer(payload), "usage": usage}
