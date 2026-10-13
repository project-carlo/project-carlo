"""The `schedule_update` task: the model reads a bulletin against the believed schedule.

Unlike the extraction classifiers, the model is shown the parish's believed
schedule (the view, `schedule.store.render_view`) and answers with the changes
it thinks the bulletin calls for, plus the entries it saw unchanged. See
docs/schedule-state-plan.md, "The model's input and output".

The calls run on gpt-6-luna through the OpenAI Responses API, set up as the
eval module's `gpt-6-luna` classifier is (`classifiers/openai_responses.py`):
the static policy (`POLICY`, which carries every rule of the eval policy,
`schedule_policy.POLICY`, worded for changes) as a developer message marked as
an explicit prompt-cache breakpoint, then the per-bulletin context
(`CONTEXT_TEMPLATE`: the church list, today's date, the view) and the PDF, with
the response schema enforced by strict decoding. Reasoning effort is high and
the PDF is read at low detail.

Calls ask for the flex service tier, billed at half the standard rate in
exchange for slower replies and, at times, no capacity: a 429, a 5xx, a
timeout, or a response that was accepted and then ends `failed` with a
`server_error`. Once the client's (fewer) flex retries are spent, such a call
is asked again at the standard tier, so a busy week costs more but no parish
is held back. An account out of quota is not retried that way: the standard
tier would refuse it too. The tier changes neither the request nor the reply,
so it is left out of `params` (and so of `version` and the request key,
keeping stored replies reusable); the tier that served each call is recorded
with it and prices it.

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

from openai import APIConnectionError, InternalServerError, OpenAI, RateLimitError
from openai.lib._pydantic import to_strict_json_schema
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from pdf_extract.classifiers.base import ClassifierOptionError
from pdf_extract.classifiers.openai_responses import (
    PDF_DETAILS,
    REASONING_EFFORTS,
    REQUEST_TIMEOUT_SECONDS,
    ImageDetail,
    ReasoningEffort,
    _b64,
    _usage,
    _without_defaults,
)
from pdf_extract.schedule_extraction import _normalize_published_date

LOGGER = logging.getLogger(__name__)

TASK = "schedule_update"

# ── Prompt ──────────────────────────────────────────────────────────────────
POLICY = """\
# Role

You keep a Catholic parish's Mass, Confession, and Adoration schedule up to date. You are given the schedule we currently believe (the "believed schedule", after these instructions) and the parish's latest bulletin (the attached PDF). Read the bulletin and answer with the changes it calls for. The schedule feeds a public Mass-times website, so a wrong time is worse than a missing one, and a change you are not sure of is worse than no change.

# What counts

- Only Mass, Confession (Reconciliation, Penance), and Adoration (Exposition, Holy Hour) events. Ignore every other kind of event or activity in the bulletin.
- Benediction implies Adoration: record Benediction as an Adoration entry with the note `Benediction`. "Adoration and Benediction" or "Holy Hour with Benediction" is one Adoration entry with that note, not two entries.
- A Communion Service (a Liturgy of the Word with Communion, led by a deacon or lay minister) is not a Mass: never record one as a Mass. When the bulletin says a Communion Service replaces a Mass on a date, that Mass is cancelled on that date.
- Leave out a Mass that is closed to the public: a private Mass, or one the bulletin limits to a group (a school Mass for students only, a Mass for residents only, a Mass by invitation).
- Leave out anything without a definite start time, such as "Confession by appointment" or "call the office".

# Churches and chapels

- Attach every entry to one of the churches in the known-churches list (given after these instructions) using its exact `slug`.
- Only record events held at one of those churches. Leave out an event held anywhere else, such as another parish, a retreat house, a cemetery, a hospital, or a school or hall at another address.
- An event in a chapel or room of a listed church itself ("in the chapel", "Blessed Sacrament Chapel", "in the church hall") belongs to that church; say where in a short `note`.
- A parish adoration chapel belongs to the church it is at. When it is at the same location as a listed church (inside it, attached to it, or on the same grounds), record its times at that church and name the chapel in a short `note`. Leave it out when it is somewhere else you would need to drive to, or when it is unclear where it is.
- An event at a separate chapel at another address (a convent, school, hospital, nursing home or mission chapel), or one whose location is unclear, is left out unless the known-churches list includes that chapel or its address. If you leave out such a chapel that clearly has its own Mass, Confession or Adoration times, or a listed church's name or address is obviously wrong, set `church_list_needs_review` to true.

# Entries: weekly or dated

Each entry is one weekly slot or one dated occurrence at one church:

- `event_kind` `weekly`: a recurring weekly time, with `day_of_week` (full English weekday name) and the qualifiers below.
- `event_kind` `specific_date`: one date, `date` as `YYYY-MM-DD`, with `cancelled` true when the bulletin says the event is cancelled, moved, or will not take place on that date. A moved event is a cancellation of the original date and time plus a dated entry at the new one.

To decide between weekly and dated:

1. Times presented as the parish's regular schedule ("Weekend Masses", "Daily Mass", "Mass Schedule", "Confessions: Saturdays 3:00-3:45 PM") are weekly. A range of days ("Monday-Friday 8:00 AM") is one weekly entry per day.
2. Slots tied to certain weeks of the month ("First Friday Adoration", "1st and 3rd Tuesdays", "last Sunday of the month") are always weekly, with `weeks_of_month` set, never dated. This holds even when the bulletin also gives this month's date for it ("First Friday, October 2"), unless it says the event is a one-time occurrence.
3. Times given only with a date, or with a date and its weekday ("Tuesday, October 6, 7:00 PM Adoration"), are dated, including the dated times in a weekly calendar or a list of Mass intentions. So are one-off times given with a weekday that means one particular day ("this Saturday at 9:00 AM"; see Dates).
4. Exception: if the bulletin shows dated times for two or more weeks and the same slot (church, type, weekday and time) appears in each of those weeks, it is weekly, unless the bulletin marks it as special or one-off.
5. When it is unclear, prefer dated (rule 2 still wins for weeks-of-the-month slots). A dated time that matches a weekly entry of the believed schedule is that entry printed again: list it in `seen`.
6. Never duplicate a weekly slot as a dated entry just because the bulletin also lists it on a date in a specific week.
7. A special occasion celebrated at a regular weekly Mass (a First Communion, an anniversary, a feast or a named Mass at the usual Sunday 10:00 AM Mass) is not an entry of its own: it is the weekly slot. Holy days, holidays, Christmas, Holy Week, feast-day Masses and other special services at times outside the weekly schedule are dated.

# Dates

Every `date` must be a day the bulletin pins down. A printed date (next to the event, or as the heading of the calendar day it is listed under) pins it down. So does a weekday the bulletin ties to one particular day, such as "this Saturday" or "next Friday": count it from the bulletin's own issue date or the week it covers, and use that date. Only do this when it is clear which day is meant; if the bulletin's date or week is unclear, or the weekday could be more than one day, do not guess.

Never project dates in any other way: do not work a date out from a weeks-of-the-month pattern or from a weekly slot, and do not turn a weekly slot into dated entries for the coming weeks. An event whose day the bulletin does not pin down is weekly if it is part of the regular schedule, and is left out otherwise.

# Weekly qualifiers

- `weeks_of_month`: for slots that only happen on some occurrences of the weekday in a month, such as `["first"]` for "First Friday Adoration" or `["first", "third"]` for "1st and 3rd Saturdays"; "last" is not "fourth". Leave it empty (`[]`) for every week.
- `exclude_weeks`: false, except for an exclusion the remaining weeks can't say. Write an exclusion as the weeks that remain: "every Saturday except the first" is `["second", "third", "fourth", "fifth"]`. An exclusion of the last week can't be written that way, since the last is the fourth in some months and the fifth in others: list the weeks the slot skips in `weeks_of_month` and set `exclude_weeks` to true, so "every Sunday except the last" is `["last"]` and "every Sunday except the first and last" is `["first", "last"]`. Do not describe the exclusion in the `note`.
- `season`: for slots the bulletin limits to part of the year ("October through June", "summer schedule"), with the months it gives; null for a slot that runs all year. Give a day only where the bulletin dates the boundary ("June 4 through September 10"); never invent the 1st or the 30th. A half-stated season ("runs from October", no end) is no season. A start later in the year than the end wraps the new year.

# Times

- `start_time` and `end_time` are formatted as `h:MM AM` or `h:MM PM`; "noon" is `12:00 PM`.
- For Mass, leave `end_time` null. For Confession and Adoration, give `end_time` when the bulletin gives one or a duration ("one hour"); leave it null for "until all are heard" or no end.
- A clock time stated in the bulletin always wins. When the bulletin gives one, use it, even if it also places the event relative to a Mass: "Confession after the 8:00 AM Mass, 8:40-9:15 AM" starts at 8:40 AM.
- Only when the bulletin times an event relative to a Mass and gives no clock time for it, work it out from that Mass's start time:
  - "After" or "following" a weekend Mass (Saturday evening vigil or Sunday): 1 hour after the Mass starts.
  - "After" or "following" a weekday Mass: 30 minutes after the Mass starts.
  - "N minutes before Mass": N minutes before it, ending when the Mass starts. "Before every Mass" is one entry for each Mass it refers to.

# Notes

Only add a `note` when there is genuinely special context worth surfacing: language, location within the church or the adoration chapel's name, `Benediction`, a relative timing you converted ("after the 4:00 PM Mass"), the occasion of a dated special service. Do not write 'Vigil Mass', and do not repeat what `weeks_of_month`, `exclude_weeks` or `season` already say.

# Changes

Answer with the changes the bulletin calls for, each with the bulletin page it is printed on and a one-sentence `rationale` quoting or citing the bulletin:

- `add`: a new entry, given whole in `entry`.
- `modify`: an existing entry changed, with its `entry_id` and the whole new entry in `entry` (not just the fields that changed).
- `delete`: an existing entry removed, with its `entry_id`.

Rules:

- **Silence is not a change.** An entry the bulletin doesn't mention stays. Propose a delete only when the bulletin says the entry is discontinued, or prints what is clearly the full schedule for that church and event type without it.
- **Weekly changes wait until they are in effect.** Propose a change to a weekly entry only when it is already in effect in the bulletin's week. An announced future change ("from November 1 the vigil moves to 5 PM") waits for a bulletin from a week where it is in effect.
- **Dated entries don't wait.** Propose dated entries (holy days, Christmas, Holy Week, one-off events) and cancellations for any date from today on. Never propose a dated entry before today.
- **Cancelling a weekly slot** on one date is an `add` of a dated entry with `cancelled: true` for the same church, event type and start time on that date. Cancelling a dated entry is a `modify` of it with `cancelled: true`.
- **Seasons.** Put a `season` on both sets of entries only when the bulletin gives both schedules with their date ranges ("Summer, June-August: ...; September-May: ..."). Otherwise replace the weekly entries outright, and replace them back when the regular schedule returns.
- **Modify, not delete + add,** for a change to an existing entry (time, end time, weeks, season, note). Delete + add only when one entry is replaced by a different one. A modify never changes an entry's church, event type or kind.
- Never add an entry for a slot the believed schedule already has (same church, event type, weekday or date, and start time): modify that entry instead.
- Refer to existing entries only by the `id`s in the believed schedule. Each entry may be changed at most once.

# Seen

List in `seen` every entry from the believed schedule that the bulletin prints and you don't change, with the page it is printed on (null if you can't tell). An entry you change carries its page on the change instead. Be thorough: an entry missing from `seen` week after week is taken as possibly gone.

# Bulletin

- Identify the bulletin's own issue date and report it as `published_date` (`YYYY-MM-DD`).
- Set `wrong_bulletin` to true only if the attached PDF is clearly not a current bulletin for this parish (wrong parish, wrong year, not a bulletin at all, etc.). Then propose no changes.

Read the whole bulletin, including calendars, sidebars and the back page, and carefully find every event it lists.

# Final source checks

- Keep church-specific schedule headings separate: an unlisted church's times must not be assigned to a similar-named listed church. A parish-wide heading, parish-office address, or photograph caption is not a different church-specific schedule heading.
- Preserve a dated Mass with an explicit known church and time even when another church has a usual weekly Mass at that time. Different churches are not duplicates; the dated venue overrides a conflicting standing schedule for that date.
- An event that includes Confession or Adoration does not establish those components' start/end times. Do not copy the larger event's full hours onto its components; record a component only with its own definite timing or a permitted relative-to-Mass anchor.
- Apply the off-site rules to Mass-intentions entries too, resolving venue abbreviations from the bulletin's own context.
- When the bulletin's printed issue date is clearly from the wrong year relative to today's date, set `wrong_bulletin` to true even if its schedule can still be read. Do not mistake dates of other events or historical references for the issue date.
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

    start_month: int = Field(
        ge=1, le=12,
        description=(
            "First month of the year the entry runs, 1-12, e.g. `10` for 'Confessions "
            "Tuesdays, October through June'."
        ),
    )
    start_day: int | None = Field(
        default=None,
        description=(
            "Day of `start_month` the entry starts on, e.g. `4` for 'June 4 through "
            "September 10'. Fill only when the bulletin dated the boundary; leave null "
            "when it names the month alone. Do not invent the 1st."
        ),
    )
    end_month: int = Field(
        ge=1, le=12,
        description=(
            "Last month of the year the entry runs, 1-12, e.g. `6`. A start later in the "
            "calendar than the end wraps the new year."
        ),
    )
    end_day: int | None = Field(
        default=None,
        description=(
            "Day of `end_month` the entry runs through, e.g. `10`. Fill only when the "
            "bulletin dated the boundary; leave null when it names the month alone. "
            "Do not invent the 30th."
        ),
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
        default_factory=list,
        description=(
            "weekly only: which occurrences of `day_of_week` within the month the entry "
            "falls on. `last` is not `fourth`. Examples: `[\"first\"]` for First Friday "
            "devotions; `[\"first\", \"third\"]` for 1st and 3rd Saturdays. The "
            "weeks it happens on, unless `exclude_weeks`: 'every Saturday except the "
            "first' is `[\"second\", \"third\", \"fourth\", \"fifth\"]`. Empty for "
            "every week."
        ),
    )
    exclude_weeks: bool = Field(
        default=False,
        description=(
            "weekly only: true when `weeks_of_month` lists the weeks the entry skips, "
            "for an exclusion of the last week, which the remaining weeks can't say: "
            "'every Sunday except the last' is `[\"last\"]` with this true. False "
            "otherwise."
        ),
    )
    season: Season | None = Field(
        default=None,
        description=(
            "weekly only: the part of the year the entry runs, when the bulletin limits "
            "it (e.g. 'October through June', 'summer schedule'). Null for all year. A "
            "half-stated season ('runs from October', no end) is no season: leave it "
            "null rather than inventing an end month."
        ),
    )
    note: str | None = Field(
        default=None,
        description=(
            "Short phrase only when there is genuinely special context (language, "
            "location nuance, `Benediction`, etc.). Do not restate what "
            "`weeks_of_month` or `season` already say, and do not describe an "
            "exclusion: say it with `weeks_of_month` and `exclude_weeks`."
        ),
    )


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
    for item in _list(data.get("seen")):
        if isinstance(item, dict) and _int(item.get("entry_id")) is not None:
            seen.append((item["entry_id"], _int(item.get("page_number"))))
    changes = []
    # `seq` is the change's position in the model's answer, counting any dropped.
    for seq, item in enumerate(_list(data.get("changes")), start=1):
        if not isinstance(item, dict) or item.get("op") not in ("add", "modify", "delete"):
            LOGGER.warning("schedule_update: dropping a change with no known op: %r", item)
            continue
        changes.append(ParsedChange(
            seq=seq,
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
        wrong_bulletin=_flag(data.get("wrong_bulletin")),
        church_list_needs_review=_flag(data.get("church_list_needs_review")),
        seen=seen,
        changes=changes,
    )


def _list(value: Any) -> list[Any]:
    """A list from a lenient reply; anything else reads as empty."""
    return value if isinstance(value, list) else []


def _flag(value: Any) -> bool:
    """A lenient reply's boolean: true, or the string "true"; anything else is false."""
    if isinstance(value, str):
        return value.strip().lower() == "true"
    return value is True


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
    service_tier: str | None = None
    """The tier that served the call, as the response reports it."""


# The model and settings every update call runs with.
UPDATE_MODEL = "gpt-6-luna"
UPDATE_REASONING_EFFORT: ReasoningEffort = "high"
UPDATE_FILE_DETAIL: ImageDetail = "low"
UPDATE_SERVICE_TIER = "flex"

# Flex replies are slower; OpenAI suggests raising the 10-minute default to 15.
FLEX_TIMEOUT_SECONDS = 900.0
# Fewer retries at flex than at the standard tier: a timed-out flex call costs
# 15 minutes a try, and once these are spent the call moves to the standard tier.
FLEX_MAX_RETRIES = 2

# What strict decoding is given: every field required, no defaults.
STRICT_SCHEMA = _without_defaults(to_strict_json_schema(ScheduleUpdatePayload))


class OpenAIScheduleUpdater:
    """An OpenAI model on the Responses API, asked for `ScheduleUpdatePayload` under strict decoding."""

    provider = "openai"

    def __init__(
        self,
        *,
        model: str = UPDATE_MODEL,
        reasoning_effort: ReasoningEffort = UPDATE_REASONING_EFFORT,
        file_detail: ImageDetail = UPDATE_FILE_DETAIL,
        service_tier: str = UPDATE_SERVICE_TIER,
        max_retries: int = 5,
    ) -> None:
        if reasoning_effort not in REASONING_EFFORTS:
            raise ClassifierOptionError(f"Unknown reasoning effort {reasoning_effort!r}")
        if file_detail not in PDF_DETAILS:
            raise ClassifierOptionError(f"Detail {file_detail!r} is not available for a PDF")
        self.model = model
        self.params: dict[str, Any] = {
            "file_detail": file_detail,
            "reasoning_effort": reasoning_effort,
            "strict": True,
        }
        self.service_tier = service_tier
        self._max_retries = max_retries
        self._clients: dict[str, OpenAI] = {}

    @property
    def params_json(self) -> str:
        return json.dumps(self.params, sort_keys=True, separators=(",", ":"))

    @property
    def version(self) -> str:
        """A digest of everything that shapes the output but the bulletin and its context."""
        return version_digest(self.provider, self.model, self.params_json)

    def _openai(self, tier: str) -> OpenAI:
        # Built on first use, so a run with no update-mode parish needs no API key.
        if tier not in self._clients:
            if tier == "flex":
                client = OpenAI(max_retries=FLEX_MAX_RETRIES, timeout=FLEX_TIMEOUT_SECONDS)
            else:
                client = OpenAI(max_retries=self._max_retries, timeout=REQUEST_TIMEOUT_SECONDS)
            self._clients[tier] = client
        return self._clients[tier]

    def request(self, pdf_bytes: bytes, context: str) -> dict[str, Any]:
        """The keyword arguments for `responses.create`, for one bulletin."""
        return {
            "model": self.model,
            "input": [
                {
                    "role": "developer",
                    "content": [
                        {
                            "type": "input_text",
                            "text": POLICY,
                            "prompt_cache_breakpoint": {"mode": "explicit"},
                        },
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": context},
                        {
                            "type": "input_file",
                            "filename": "bulletin.pdf",
                            "file_data": f"data:application/pdf;base64,{_b64(pdf_bytes)}",
                            "detail": self.params["file_detail"],
                        },
                    ],
                },
            ],
            "reasoning": {"effort": self.params["reasoning_effort"]},
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "schedule_update",
                    "schema": STRICT_SCHEMA,
                    "strict": True,
                },
            },
            "prompt_cache_options": {"mode": "explicit"},
            "service_tier": self.service_tier,
            "store": False,
        }

    def call(self, pdf_bytes: bytes, context: str) -> RawReply:
        request = self.request(pdf_bytes, context)
        tier = self.service_tier
        started = time.monotonic()
        if tier != "flex":
            response = self._openai(tier).responses.create(**request)
        else:
            try:
                response = self._openai(tier).responses.create(**request)
            except (RateLimitError, InternalServerError, APIConnectionError) as exc:
                # The client has already backed off and retried; flex is still full or slow.
                if getattr(exc, "code", None) == "insufficient_quota":
                    raise
                no_capacity: str | None = f"{type(exc).__name__}: {exc}"
            else:
                no_capacity = _flex_capacity_lost(response)
            if no_capacity is not None:
                LOGGER.warning(
                    "%s has no flex capacity after %.0fs (%s); asking at the standard tier",
                    self.model, time.monotonic() - started, no_capacity,
                )
                # The latency recorded is the call that answered, not the flex tries.
                tier = "default"
                started = time.monotonic()
                try:
                    response = self._openai(tier).responses.create(
                        **{**request, "service_tier": tier},
                    )
                except Exception as exc:
                    exc.add_note(f"asked at the standard tier after flex failed: {no_capacity}")
                    raise
        if response.status != "completed":
            LOGGER.warning(
                "%s response %s is %s (%s)",
                self.model, response.id, response.status, response.incomplete_details,
            )
        return RawReply(
            text=response.output_text or "",
            served_model=getattr(response, "model", None),
            usage=_usage(response),
            latency_ms=int((time.monotonic() - started) * 1000),
            # The tier asked for, when the response doesn't say.
            service_tier=getattr(response, "service_tier", None) or tier,
        )


def _flex_capacity_lost(response: Any) -> str | None:
    """Why a flex response that was accepted then lost its capacity failed, or None.

    Flex capacity can run out after a request is accepted. The reply is then no
    429 but a `failed` response with a `server_error` ("Flex processing is
    temporarily unavailable"), no output and no usage.
    """
    if response.status != "failed":
        return None
    error = getattr(response, "error", None)
    if getattr(error, "code", None) != "server_error":
        return None
    message = getattr(error, "message", None) or "server_error"
    usage = _usage(response)
    # Flex reports none on such a failure; should that change, the log shows it.
    billed = f", usage {usage}" if any(usage.values()) else ""
    return f"response {response.id}: {message}{billed}"


def _sha(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


POLICY_HASH = _sha(POLICY)
SCHEMA_HASH = _sha(SCHEMA_TEXT)
CONTEXT_TEMPLATE_HASH = _sha(CONTEXT_TEMPLATE)


def version_digest(provider: str, model: str, params_json: str) -> str:
    return _sha("\x00".join((
        provider, model, POLICY_HASH, SCHEMA_HASH, CONTEXT_TEMPLATE_HASH, params_json,
    )))
