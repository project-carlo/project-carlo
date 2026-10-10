"""The `schedule_update` task: the model reads a bulletin against the believed schedule.

Unlike the extraction classifiers, the model is shown the parish's believed
schedule (the view, `schedule.store.render_view`) and answers with the changes
it thinks the bulletin calls for, plus the entries it saw unchanged. See
docs/schedule-state-plan.md, "The model's input and output".

The request is the static policy (`POLICY`), then the per-bulletin context
(`CONTEXT_TEMPLATE`: the church list, today's date, the view), then the PDF, so
every request starts with the same text and can be served from the provider's
prompt cache.

Every call is stored (`llm_call`) with the hashes of the policy, the response
schema and the context template, its parameters, and `version`, a digest of all
of them with the provider and model. `parse_response` reads a reply strictly,
or leniently when it fails validation, into the shape the policy decides.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from datetime import date
from hashlib import sha256
from typing import Any, Literal

from google import genai
from google.genai import types
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from pdf_extract.schedule_extraction import (
    DEFAULT_GEMINI_MODEL,
    _generate_content_with_backoff,
    _normalize_published_date,
    _token_usage,
    gemini_client,
)

LOGGER = logging.getLogger(__name__)

TASK = "schedule_update"

# ── Prompt ──────────────────────────────────────────────────────────────────
POLICY = """\
# Role

You keep a Catholic parish's Mass, Confession and Adoration schedule up to date. You are given the schedule we currently believe (the "believed schedule", after these instructions) and the parish's latest bulletin (the attached PDF). Read the bulletin and answer with the changes it calls for. The schedule feeds a public Mass-times website, so a wrong time is worse than a missing one, and a change you are not sure of is worse than no change.

# What counts

- Only Mass, Confession (Reconciliation, Penance), and Adoration (Exposition, Holy Hour) events. Ignore every other kind of event or activity.
- Benediction implies Adoration: "Adoration and Benediction" or "Holy Hour with Benediction" is one Adoration entry with the note `Benediction`.
- A Communion Service (a Liturgy of the Word with Communion) is not a Mass. When the bulletin says one replaces a Mass on a date, that Mass is cancelled on that date.
- Leave out a Mass closed to the public (private, school-only, residents-only, by invitation), and anything without a definite start time ("by appointment").
- Only events at one of the known churches (given after these instructions), named by their exact `slug`. An event in a chapel or room of a listed church belongs to that church; say where in a short `note`. Leave out events anywhere else. If the bulletin clearly shows a church or chapel of this parish with its own schedule that is not in the list, or a listed church's name or address is obviously wrong, set `church_list_needs_review` to true.

# Entries

Each entry is one weekly slot or one dated occurrence at one church:

- `event_kind` `weekly`: a recurring weekly time, with `day_of_week` (full English weekday name). `weeks_of_month` lists the weeks of the month it happens on when it is not every week (`["first"]` for First Friday, `["first", "third"]` for 1st and 3rd Saturdays; "last" is not "fourth"; an exclusion is written as the weeks that remain), else `[]`. `season` gives the months (and days, only when the bulletin dates the boundary) of the part of the year it runs, when the bulletin limits it, else null.
- `event_kind` `specific_date`: one date, `date` as `YYYY-MM-DD`, with `cancelled` true when it is a cancellation. Holy days, holidays, Christmas, Holy Week and other special services at times outside the weekly schedule are dated. A special occasion at a regular weekly Mass is not an entry of its own.
- Times are `h:MM AM` or `h:MM PM`; "noon" is `12:00 PM`. For Mass leave `end_time` null; for Confession and Adoration give it when the bulletin gives one or a duration. A clock time in the bulletin always wins; only when an event is timed relative to a Mass with no clock time, work it out: "after" a weekend Mass is 1 hour after it starts, "after" a weekday Mass 30 minutes after, "N minutes before Mass" ends when the Mass starts.
- Every `date` must be a day the bulletin pins down (a printed date, or "this Saturday" counted from the bulletin's own date). Never project dates from a weekly slot or a weeks-of-the-month pattern.
- Only add a `note` for genuinely special context: language, place within the church, `Benediction`, a relative timing you converted, the occasion of a dated special service. Don't write "Vigil Mass", and don't repeat what `weeks_of_month` or `season` say.

# Changes

Answer with the changes the bulletin calls for, each with the bulletin page it is printed on and a one-sentence `rationale` quoting or citing the bulletin:

- `add`: a new entry, given whole in `entry`.
- `modify`: an existing entry changed, with its `entry_id` and the whole new entry in `entry` (not just the fields that changed).
- `delete`: an existing entry removed, with its `entry_id`.

Rules:

- **Silence is not a change.** An entry the bulletin doesn't mention stays. Propose a delete only when the bulletin says the entry is discontinued, or prints what is clearly the full schedule for that church and event type without it.
- **Weekly changes wait until they are in effect.** Propose a change to a weekly entry only when it is already in effect in the bulletin's week. An announced future change ("from November 1 the vigil moves to 5 PM") waits for a bulletin from a week where it is in effect.
- **Dated entries don't wait.** Propose dated entries (holy days, Christmas, Holy Week, one-off events) and cancellations for any date from today on. Never propose a dated entry before today.
- **Cancelling a weekly slot** on one date is an `add` of a dated entry with `cancelled: true` for the same church, event type and start time on that date. Cancelling a dated entry is a `modify` of it with `cancelled: true`. A moved event is a cancellation of the original date and time plus a dated entry at the new one.
- **Seasons.** Put a `season` on both sets of entries only when the bulletin gives both schedules with their date ranges ("Summer, June-August: ...; September-May: ..."). Otherwise replace the weekly entries outright, and replace them back when the regular schedule returns.
- **Modify, not delete + add,** for a change to an existing entry (time, end time, weeks, season, note). Delete + add only when one entry is replaced by a different one. A modify never changes an entry's church, event type or kind.
- Never add an entry for a slot the believed schedule already has (same church, event type, weekday or date, and start time): modify that entry instead.
- Refer to existing entries only by the `id`s in the believed schedule. Each entry may be changed at most once.

# Seen

List in `seen` every entry from the believed schedule that the bulletin prints and you don't change, with the page it is printed on (null if you can't tell). An entry you change carries its page on the change instead. Be thorough: an entry missing from `seen` week after week is taken as possibly gone.

# Bulletin

- Report the bulletin's own issue date as `published_date` (`YYYY-MM-DD`).
- Set `wrong_bulletin` to true only if the PDF is clearly not a current bulletin for this parish (wrong parish, wrong year, not a bulletin at all). Then propose no changes. When the printed issue date is clearly from the wrong year relative to today's date, set it even if the schedule could still be read.

Read the whole bulletin, including calendars, sidebars and the back page.
"""

CONTEXT_TEMPLATE = """\
# Known churches for this parish

```json
{churches_json}
```

# Today's date

{today_iso} ({today_day_of_week})

# Believed schedule

The schedule we currently believe, by church. Dated entries before today are left out. Refer to entries by `id`.

```json
{view_json}
```
"""


def render_context(churches: list[dict[str, Any]], today: date, view_json: str) -> str:
    return CONTEXT_TEMPLATE.format(
        churches_json=json.dumps(churches, ensure_ascii=False),
        today_iso=today.isoformat(),
        today_day_of_week=today.strftime("%A"),
        view_json=view_json,
    )


# ── Response schema ─────────────────────────────────────────────────────────
WeekOfMonth = Literal["first", "second", "third", "fourth", "fifth", "last"]


class Season(BaseModel):
    """The part of the year a weekly entry runs; months and days are inclusive."""

    model_config = ConfigDict(extra="forbid")

    start_month: int = Field(ge=1, le=12, description="First month the entry runs, 1-12.")
    start_day: int | None = Field(
        default=None, description="Day of `start_month` it starts, only when the bulletin dates it.",
    )
    end_month: int = Field(
        ge=1, le=12,
        description="Last month the entry runs, 1-12. Earlier than the start wraps the new year.",
    )
    end_day: int | None = Field(
        default=None, description="Day of `end_month` it runs through, only when the bulletin dates it.",
    )


class ScheduleEntry(BaseModel):
    """One weekly slot or dated occurrence at one church."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(description="Exactly a `slug` from the known-churches list.")
    event_type: Literal["mass", "confession", "adoration"]
    event_kind: Literal["weekly", "specific_date"]
    day_of_week: str | None = Field(
        default=None, description="weekly only: full English weekday name, e.g. `Sunday`.",
    )
    date: str | None = Field(default=None, description="specific_date only: `YYYY-MM-DD`.")
    start_time: str = Field(description="`h:MM AM` or `h:MM PM`.")
    end_time: str | None = Field(
        default=None, description="Null for Mass; for Confession and Adoration when given.",
    )
    cancelled: bool = Field(default=False, description="specific_date only: a cancellation.")
    weeks_of_month: list[WeekOfMonth] = Field(
        default_factory=list, description="weekly only: the weeks it happens on; [] = every week.",
    )
    season: Season | None = Field(default=None, description="weekly only: part of the year.")
    note: str | None = None


class Sighting(BaseModel):
    """An entry of the believed schedule that the bulletin prints and the call doesn't change."""

    model_config = ConfigDict(extra="forbid")

    entry_id: int = Field(description="An `id` from the believed schedule.")
    page_number: int | None = Field(default=None, description="1-indexed PDF page.")


class Change(BaseModel):
    model_config = ConfigDict(extra="forbid")

    op: Literal["add", "modify", "delete"]
    entry_id: int | None = Field(
        default=None, description="modify, delete: an `id` from the believed schedule.",
    )
    entry: ScheduleEntry | None = Field(
        default=None, description="add, modify: the whole new entry.",
    )
    page_number: int | None = Field(default=None, description="1-indexed PDF page.")
    rationale: str | None = Field(default=None, description="One sentence citing the bulletin.")


class ScheduleUpdatePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    published_date: str | None = Field(
        default=None, description="The bulletin's issue date as `YYYY-MM-DD`.",
    )
    wrong_bulletin: bool = Field(
        default=False, description="True only if this is clearly not this parish's current bulletin.",
    )
    church_list_needs_review: bool = Field(
        default=False,
        description=(
            "True only if the bulletin clearly shows a church of the parish with its own "
            "schedule that is not in the list, or a listed church's name or address is wrong."
        ),
    )
    seen: list[Sighting] = Field(default_factory=list)
    changes: list[Change] = Field(default_factory=list)


SCHEMA_TEXT = json.dumps(ScheduleUpdatePayload.model_json_schema(), sort_keys=True)


# ── Reading a reply ─────────────────────────────────────────────────────────
OK = "ok"
LENIENT = "lenient"
PARSE_FAILED = "parse_failed"
API_ERROR = "api_error"


@dataclass
class ParsedChange:
    seq: int
    op: str
    raw: dict[str, Any]
    entry_id: int | None
    entry: Any
    page_number: int | None
    rationale: str | None


@dataclass
class ParsedReply:
    status: str
    published_date: str | None = None
    wrong_bulletin: bool = False
    church_list_needs_review: bool = False
    seen: list[tuple[int, int | None]] = field(default_factory=list)
    changes: list[ParsedChange] = field(default_factory=list)
    error: str | None = None


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _text(value: Any) -> str | None:
    return value.strip() or None if isinstance(value, str) else None


def parse_response(text: str) -> ParsedReply:
    """Read a reply strictly, else leniently; `parse_failed` when it is no JSON object.

    Both paths go through the same lenient reading, so they can't differ in
    shape. A change without a known `op` can't be stored and is dropped with a
    warning (the raw reply keeps it).
    """
    status = OK
    try:
        data: Any = ScheduleUpdatePayload.model_validate_json(text).model_dump(mode="json")
    except ValidationError as exc:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return ParsedReply(status=PARSE_FAILED, error=f"not JSON: {text[:200]!r}")
        if not isinstance(data, dict):
            return ParsedReply(status=PARSE_FAILED, error=f"not a JSON object: {text[:200]!r}")
        LOGGER.warning("schedule_update reply failed validation (%s); reading it leniently", exc)
        status = LENIENT

    seen = []
    for item in data.get("seen") or []:
        if isinstance(item, dict) and _int(item.get("entry_id")) is not None:
            seen.append((item["entry_id"], _int(item.get("page_number"))))
    changes = []
    for item in data.get("changes") or []:
        if not isinstance(item, dict) or item.get("op") not in ("add", "modify", "delete"):
            LOGGER.warning("schedule_update: dropping a change with no known op: %r", item)
            continue
        changes.append(ParsedChange(
            seq=len(changes) + 1,
            op=item["op"],
            raw=item,
            entry_id=_int(item.get("entry_id")),
            entry=_without_nulls(item.get("entry")),
            page_number=_int(item.get("page_number")),
            rationale=_text(item.get("rationale")),
        ))
    return ParsedReply(
        status=status,
        published_date=_normalize_published_date(data.get("published_date")),
        wrong_bulletin=bool(data.get("wrong_bulletin", False)),
        church_list_needs_review=bool(data.get("church_list_needs_review", False)),
        seen=seen,
        changes=changes,
    )


def _without_nulls(entry: Any) -> Any:
    """An entry with the keys the schema fills in for every entry dropped when empty.

    Strict output carries every key (a weekly entry gets `date: null` and
    `cancelled: false`); `parse_entry` reads an absent key and a null one the
    same, so this only keeps a dated entry's `weeks_of_month: []` from reading
    as a qualifier.
    """
    if not isinstance(entry, dict):
        return entry
    return {k: v for k, v in entry.items() if v not in (None, [])}


# ── The call ────────────────────────────────────────────────────────────────
@dataclass
class RawReply:
    text: str
    served_model: str | None
    usage: dict[str, int]
    latency_ms: int


class GeminiScheduleUpdater:
    """Gemini, asked for `ScheduleUpdatePayload` as JSON."""

    provider = "gemini"

    def __init__(self, *, model: str = DEFAULT_GEMINI_MODEL) -> None:
        self.model = model
        self.params: dict[str, Any] = {}
        self._client: genai.Client | None = None

    @property
    def params_json(self) -> str:
        return json.dumps(self.params, sort_keys=True, separators=(",", ":"))

    @property
    def version(self) -> str:
        """A digest of everything that shapes the output but the bulletin and its context."""
        return version_digest(self.provider, self.model, self.params_json)

    def _gemini(self) -> genai.Client:
        if self._client is None:
            self._client = gemini_client()
        return self._client

    def contents(self, pdf_bytes: bytes, context: str) -> list[str | types.Part]:
        return [POLICY, context, types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")]

    def call(self, pdf_bytes: bytes, context: str) -> RawReply:
        started = time.monotonic()
        response = _generate_content_with_backoff(
            self._gemini(),
            model=self.model,
            contents=self.contents(pdf_bytes, context),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=ScheduleUpdatePayload.model_json_schema(),
            ),
        )
        return RawReply(
            text=response.text or "",
            served_model=getattr(response, "model_version", None),
            usage=_token_usage(response),
            latency_ms=int((time.monotonic() - started) * 1000),
        )


def _sha(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


POLICY_HASH = _sha(POLICY)
SCHEMA_HASH = _sha(SCHEMA_TEXT)
CONTEXT_TEMPLATE_HASH = _sha(CONTEXT_TEMPLATE)


def version_digest(provider: str, model: str, params_json: str) -> str:
    return _sha("\x00".join((
        provider, model, POLICY_HASH, SCHEMA_HASH, CONTEXT_TEMPLATE_HASH, params_json,
    )))
