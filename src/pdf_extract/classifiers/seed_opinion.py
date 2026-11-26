"""The `seed_opinion` task: a parish's schedule read blind from its recent bulletins.

A second reader for a seed (docs/seed-second-opinion-plan.md). gpt-6-luna is
given the newest few bulletins of one parish at once (B1 newest) and answers
with the schedule they establish together, as a seed would hold it on the
newest bulletin's date: weekly slots, plus dated entries and cancellations from
that date on. It is shown no history, website or seed, so its reading is
independent of the drafter's.

The request is the extraction policy (`schedule_policy.POLICY`) and the
seed-specific `TASK`, both static and sent as one developer message marked as
an explicit prompt-cache breakpoint, then the parish's churches, the date and
each PDF after its label. It runs as update mode does
(`schedule_update.OpenAIScheduleUpdater`: flex first, the standard tier when
flex has no room, strict decoding), with reasoning high and PDFs at low detail.

Each slot carries `evidence`: the bulletins that print it, the page and the
words there, so a drafter can check it against the PDF in seconds.
`opinion_entries` turns a reply into seed-shaped entries, each with its
evidence.
"""

from __future__ import annotations

import json
from datetime import date
from typing import Any

from openai.lib._pydantic import to_strict_json_schema
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from pdf_extract.classifiers.openai_responses import _b64, _without_defaults
from pdf_extract.classifiers.qualified_schedule import (
    Season,
    WeekOfMonth,
    fingerprint,
    flatten_events,
)
from pdf_extract.classifiers.schedule_policy import POLICY
from pdf_extract.classifiers.schedule_update import OpenAIScheduleUpdater, RawReply
from pdf_extract.model import gemini_rows
from pdf_extract.schedule_extraction import _normalize_published_date

OPINION_MODEL = "gpt-6-luna"

TASK = """\
# Your task here: one schedule from several bulletins

Above is the policy for reading one bulletin. Here you are given several recent bulletins of one parish, labelled B1, B2, ... with B1 the newest. Read every one in full with the policy, then answer with the single schedule they establish together, as it stands on today's date (given below: the day B1 was fetched).

## Weekly or dated, across bulletins

- **Weekly slots** are the parish's regular schedule as of B1. The same church, service, weekday and time printed in two or more of these bulletins, covering different weeks and not marked special or one-off, is weekly: the policy's rule 4 of "Weekly or dated" applies across bulletins, not only inside one.
- **Check the weeks in between.** Rule 4 needs the slot in each week the bulletins show, not in two of them. Before you record a slot as weekly because it appears in some issues, look at every week the bulletins cover that lists that weekday's services (a calendar, the Mass intentions, a weekly schedule). If the weeks that have it alternate with weeks whose listing for that weekday lacks it (there, absent, there, absent), it is not weekly: record only its printed dates on or after today as dated entries. Only weeks a bulletin shows count: a week that no bulletin covers is not a week without the slot. One shown week without it, between weeks that have it, is an omission, not alternation: the slot stays weekly. Dates printed two or more weeks apart ("Tuesdays, October 13 & 27"), "every other week", and a table that rotates a service among churches by date are never weekly.
- A weekly slot that the older bulletins establish and B1 simply omits, with no cancellation or change of that service, is still weekly.
- A weeks-of-the-month slot ("First Friday Adoration") that B1 cannot show, because B1's week holds no such day, is still weekly when an older bulletin prints it.
- When the bulletins disagree on a regular time, follow the newest that prints it, unless the difference is clearly a one-date exception: then the standing slot stays, and the exception is a dated entry or a cancellation.
- A change announced for a later date ("From November 1, the Friday Mass moves to Tuesday"): keep the current schedule and leave the future one out.
- **Seasons and patterns the fields can't hold.** Set `season` only when the bulletin prints both a start and an end month ("October through June", "September to May"). A period bounded by a holiday or a weekend ("Memorial Day to Columbus Day", "through Labor Day"), or given by only one end ("from October", "through mid-January"), is not a season, and "first full weekend of the month" is not `first`: record the printed dates on or after today as dated entries, and otherwise leave the slot out. Never widen a season to the months you happen to see.
- **Dated entries and cancellations**: only those on or after today's date, from any bulletin, unless a newer bulletin contradicts them. Leave out every date before today.
- Leave out the events of a bulletin you mark `wrong_bulletin`.

## Read every page, not only the schedule box

- Masses, Confessions, Adoration and Holy Hours are often printed only outside the schedule box: in calendars, event lists, sidebars, flyers, notice boxes, the pastor's column and announcements, including ones headed by something else (a meeting, a speaker, a devotion night, a fundraiser). Words inside pictures and graphics count as printed. Go through every page of every bulletin and gather every such service with a time before deciding how to record each one. A service named inside a larger programme ("6:15 Confession, 6:30 Rosary, 7 Mass") is a service in its own right.
- Look in particular for dated services and cancellations on or after today (holy days, All Souls, Thanksgiving, a parish feast, a visiting bishop, a Mass cancelled or moved), and record each. A feast or occasion listed at a regular slot's church and time (All Saints at the usual Sunday Masses) is that weekly slot, not a dated entry; only a time outside the weekly schedule is dated.
- A day heading above several church lines ("Tuesday, Wednesday & First Friday" over "8:00 am at St. Peter's" and "9:30 am at St. John's") applies to every line under it.

## Exceptions printed with a slot

- Read each regular slot together with its qualifiers and with the dated listings for that weekday. A clause in the same sentence or notice ("except", "other than", "not on", "on days other than First Fridays") limits the slot: set `weeks_of_month` (and `exclude_weeks`) to match, and quote the clause in the evidence.
- An exception limits a slot only when it is about that slot: it names its time, or its church and service. A notice about a separately named service ("First Saturday Masses are discontinued", "no First Saturday Mass") leaves the regular slots of that day as they are. Before you limit a weekly slot to some weeks of the month, look for a week the bulletins show that the limit would leave out: if that week's dated listing still prints the slot, do not limit it.
- When the schedule prints a different time or church for one day of a range ("Monday through Friday 8:30 AM at St. Joseph's ... Wednesday 8:30 AM at St. Peter's"), that day follows the exception, not the range.
- When a monthly service is printed for a weekday ("Last Sunday of the Month: 10 a.m. bilingual") and that week's dated listings show only it, the regular slots of that weekday skip that week.
- A regular slot taken from a reused template (an intentions list) gives way to that week's dated listing for the same day: if the calendar says a Communion Service, no Mass, or another church at that time, follow it.
- A notice that cancels a time on some days ("NO 8:30 AM MASS Monday-Wednesday") shows that the time is regular on those days.
- When the bulletin says a day's only Mass, or only Masses, are X ("the only Mass for our parishes is at Resurrection at 8:30"), record a cancellation on that date for each of your weekly Masses on that weekday that X does not include.

## Times

- "N minutes before Mass", "1/2 hour before weekday Masses", "an hour before the Mass": one entry for each of those Masses, starting N minutes before it and ending when it starts. A start you work out this way always has that end.
- A clock time printed in the bulletin and followed by a Mass, with no end or duration of its own ("Adoration 10:00 am followed by 11:00 am Mass"), has no `end_time`. This is only for a following Mass: a period followed by another service at a stated time ("followed by Evening Prayer at 6:00 PM", "Benediction at 5:45") ends at that time.
- Benediction closes an Adoration period. When the bulletin gives the period's start (a clock time, or "following the noon Mass") and a Benediction time, record one Adoration from that start to the Benediction time. Use a Benediction time as the start only when Benediction is the whole service.
- A period that runs past midnight ("Wednesday 9 am through Thursday 10 pm", "First Friday 7 am until First Saturday 9 am") is one entry per day: the first ends at 11:59 PM, the next starts at 12:00 AM. Adoration "24 hours", "24/7" or "perpetual", with no hours given, is 12:00 AM to 11:59 PM on each day it covers.
- When another passage, in any of the bulletins, gives the same slot's end time or duration ("Confession from 5:30 to 6 PM" in the pastor's column, against "Penance Tuesday 5:30 pm" in the box), use it and cite both.
- Take a start and its end from the same line and the same church's block; never join times from neighbouring blocks.
- Hours listed for volunteers ("Adorers needed", "hours which need to be filled", "open hours", "partner required", "substitutes needed") are not Adoration times: never record them. Take Adoration times from the schedule of exposition.
- If a printed time is cut off or garbled ("3:00 pm - 3:4pm"), do not complete it: leave that end null, or leave out an entry whose start is unreadable.

## Before you answer

- Compare every dated entry with your weekly slots. If a weekly slot has the same church, type, weekday and start and falls on that date, delete the dated entry, whatever the occasion.
- Check that every Mass, Confession and Adoration time in each schedule box, and every regular time the dated listings of two or more weeks print, is in your answer, unless a rule here leaves it out.
- For every weekly slot, check once more that it is not missing from alternate weeks the bulletins show, unless it is named by its week of the month.
- A `note` never holds a time, a day or an exception: express those with entries and fields.

For every slot, give `evidence`: one item for each bulletin that prints it, with `bulletin` (`B1`, `B2`...), the PDF `page` (counted from 1 within that bulletin's own PDF; pages move between issues) and `quote`, the bulletin's own words there, exactly as printed, misprints included. Keep it short, but quote the whole clause with any qualifier or exception. A slot kept from an older bulletin cites that bulletin. In `bulletins`, give each bulletin's issue date as `published_date` and set `wrong_bulletin` as the policy says.
"""

CONTEXT_TEMPLATE = """\
# Known churches for this parish

```json
{churches_json}
```

# Today's date

{today_iso} ({today_day_of_week})

# The bulletins

{bulletin_list}

Each PDF follows its label below.
"""

_TIME_DESC = "Formatted as `h:MM AM` or `h:MM PM`."
_END_TIME_DESC = "For Mass, leave null. For Confession and Adoration, include when available."
_SLUG_DESC = "Must exactly match a `slug` from the provided known-churches list."
_NOTE_DESC = (
    "Short phrase only when there is genuinely special context (language, location "
    "nuance, `Benediction`, etc.). Do not restate what `weeks_of_month` or `season` "
    "already say."
)


class Evidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bulletin: str = Field(description="The bulletin's label: `B1`, `B2`...")
    page: int = Field(description="1-indexed page of that bulletin's PDF.")
    quote: str = Field(description="The bulletin's words there, exactly as printed.")


class WeeklyOpinion(BaseModel):
    """One recurring weekly slot at a church."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(description=_SLUG_DESC)
    day_of_week: str = Field(description="Full English weekday name, e.g. `Monday`.")
    start_time: str = Field(description=_TIME_DESC)
    end_time: str | None = Field(default=None, description=_END_TIME_DESC)
    weeks_of_month: list[WeekOfMonth] = Field(
        default_factory=list,
        description=(
            "Which occurrences of `day_of_week` in the month the slot falls on; `last` is "
            "not `fourth`. 'Every Saturday except the first' is `[\"second\", \"third\", "
            "\"fourth\", \"fifth\"]`. Empty when it happens every week."
        ),
    )
    exclude_weeks: bool = Field(
        default=False,
        description=(
            "True only when `weeks_of_month` lists the weeks the slot skips, for an "
            "exclusion of the last week: 'every Sunday except the last' is `[\"last\"]` "
            "with this true."
        ),
    )
    season: Season | None = Field(
        default=None,
        description="The part of the year the slot runs, when limited; null for all year.",
    )
    note: str | None = Field(default=None, description=_NOTE_DESC)
    evidence: list[Evidence]


class DatedOpinion(BaseModel):
    """One dated occurrence (or cancellation) at a church."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(description=_SLUG_DESC)
    date: str = Field(description="`YYYY-MM-DD`, on or after today's date.")
    start_time: str = Field(description=_TIME_DESC)
    end_time: str | None = Field(default=None, description=_END_TIME_DESC)
    note: str | None = Field(default=None, description=_NOTE_DESC)
    evidence: list[Evidence]


class WeeklyOpinions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    masses: list[WeeklyOpinion] = Field(default_factory=list)
    confessions: list[WeeklyOpinion] = Field(default_factory=list)
    adorations: list[WeeklyOpinion] = Field(default_factory=list)


class DatedOpinions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    masses: list[DatedOpinion] = Field(default_factory=list)
    confessions: list[DatedOpinion] = Field(default_factory=list)
    adorations: list[DatedOpinion] = Field(default_factory=list)


class BulletinRead(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bulletin: str = Field(description="The bulletin's label: `B1`, `B2`...")
    published_date: str | None = Field(description="Its issue date as `YYYY-MM-DD`.")
    wrong_bulletin: bool = Field(
        description="True only if it is clearly not a current bulletin of this parish.",
    )


class SeedOpinionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bulletins: list[BulletinRead]
    weekly_schedule: WeeklyOpinions = Field(
        default_factory=WeeklyOpinions,
        description="The parish's regular weekly Mass, Confession and Adoration slots.",
    )
    single_events: DatedOpinions = Field(
        default_factory=DatedOpinions,
        description="Dated occurrences on or after today not covered by a weekly slot.",
    )
    cancellations: DatedOpinions = Field(
        default_factory=DatedOpinions,
        description="Dated cancellations on or after today.",
    )
    church_list_needs_review: bool = Field(
        default=False,
        description=(
            "True only if a bulletin clearly shows a church of the parish with its own "
            "schedule that is not in the list, or a listed church's name or address is wrong."
        ),
    )


STRICT_SCHEMA = _without_defaults(to_strict_json_schema(SeedOpinionPayload))
PROMPT_FINGERPRINT = fingerprint(
    POLICY, TASK, CONTEXT_TEMPLATE,
    json.dumps(SeedOpinionPayload.model_json_schema(), sort_keys=True),
)


def label(index: int) -> str:
    return f"B{index + 1}"


def render_context(
    churches: list[dict[str, Any]], today: date, bulletins: list[dict[str, Any]],
) -> str:
    """The per-parish text. `bulletins` are newest first, with `published_date`/`fetched_at`."""
    lines = []
    for i, b in enumerate(bulletins):
        issue = b.get("published_date") or "issue date unknown"
        lines.append(f"- {label(i)}: issue {issue}, fetched {str(b.get('fetched_at'))[:10]}")
    return CONTEXT_TEMPLATE.format(
        churches_json=json.dumps(churches, ensure_ascii=False),
        today_iso=today.isoformat(),
        today_day_of_week=today.strftime("%A"),
        bulletin_list="\n".join(lines),
    )


class SeedOpinionCaller(OpenAIScheduleUpdater):
    """gpt-6-luna on the Responses API, asked for `SeedOpinionPayload` over several PDFs."""

    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("model", OPINION_MODEL)
        super().__init__(**kwargs)

    @property
    def version(self) -> str:
        return f"{self.model}+seed-opinion-{PROMPT_FINGERPRINT}+{self.params_json}"

    def opinion_request(self, pdfs: list[bytes], context: str) -> dict[str, Any]:
        content: list[dict[str, Any]] = [{"type": "input_text", "text": context}]
        for i, pdf in enumerate(pdfs):
            content.append({"type": "input_text", "text": f"## {label(i)}"})
            content.append({
                "type": "input_file",
                "filename": f"{label(i)}.pdf",
                "file_data": f"data:application/pdf;base64,{_b64(pdf)}",
                "detail": self.params["file_detail"],
            })
        return {
            "model": self.model,
            "input": [
                {
                    "role": "developer",
                    "content": [{
                        "type": "input_text",
                        "text": POLICY + "\n\n" + TASK,
                        "prompt_cache_breakpoint": {"mode": "explicit"},
                    }],
                },
                {"role": "user", "content": content},
            ],
            "reasoning": {"effort": self.params["reasoning_effort"]},
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "seed_opinion",
                    "schema": STRICT_SCHEMA,
                    "strict": True,
                },
            },
            "prompt_cache_options": {"mode": "explicit"},
            "service_tier": self.service_tier,
            "store": False,
        }

    def opinion(self, pdfs: list[bytes], context: str) -> RawReply:
        return self.send(self.opinion_request(pdfs, context))


# ── Reading a reply ─────────────────────────────────────────────────────────
_SECTIONS = ("weekly_schedule", "single_events", "cancellations")
_TYPES = ("masses", "confessions", "adorations")
_ENTRY_KEYS = (
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "weeks_of_month", "exclude_weeks", "season", "note",
)


def parse_reply(text: str) -> tuple[dict[str, Any] | None, str]:
    """The reply as a dict and `ok`, `lenient` (failed validation) or `parse_failed`."""
    try:
        return SeedOpinionPayload.model_validate_json(text).model_dump(mode="json"), "ok"
    except ValidationError:
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return None, "parse_failed"
        return (data, "lenient") if isinstance(data, dict) else (None, "parse_failed")


def opinion_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Each slot of a reply as a seed entry (`HH:MM` times), with `evidence` and `problems`."""
    out = []
    for section in _SECTIONS:
        block = payload.get(section)
        if not isinstance(block, dict):
            continue
        for key in _TYPES:
            for item in block.get(key) or []:
                if not isinstance(item, dict):
                    continue
                one = {s: {} for s in _SECTIONS}
                one[section] = {key: [{k: v for k, v in item.items() if k != "evidence"}]}
                flat = flatten_events(one)["events"]
                if not flat:
                    continue
                row = gemini_rows(flat)[0]
                entry = {k: row.get(k) for k in _ENTRY_KEYS}
                entry["evidence"] = [e for e in item.get("evidence") or [] if isinstance(e, dict)]
                entry["problems"] = row.get("problems") or []
                out.append(entry)
    return out


def bulletin_reads(payload: dict[str, Any]) -> list[dict[str, Any]]:
    reads = []
    for b in payload.get("bulletins") or []:
        if isinstance(b, dict):
            reads.append({
                "bulletin": b.get("bulletin"),
                "published_date": _normalize_published_date(b.get("published_date")),
                "wrong_bulletin": b.get("wrong_bulletin") is True,
            })
    return reads
