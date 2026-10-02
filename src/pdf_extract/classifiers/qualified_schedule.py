"""What a classifier is asked for when it is scored against the ground-truth labels.

The production extraction schema (`schedule_extraction.SchedulePayload`) plus the
two recurrence qualifiers the labels record on weekly slots: which weeks of the
month a slot falls on (`weeks_of_month`) and which part of the year it runs
(`season`). The qualifier field descriptions follow PR 22's extraction schema.

The prompt starts from the production Gemini prompt, with the labeling rules
added (weekly vs dated, chapels, Communion Services, times relative to a Mass),
and is split in two so the part that never changes comes first: `INSTRUCTIONS` is identical for every bulletin and can be
served from a provider's prompt cache, while `CONTEXT_TEMPLATE` (the parish's
churches and today's date) and then the PDF follow it.

`flatten_events` turns a payload into the pipeline's flat event dicts, with the
qualifiers in the flat form PR 22 uses (`weeks_of_month`, `season_start_month`,
...); `labeling.bulletins.gemini_rows` reads that form into label rows.
"""

from __future__ import annotations

import json
from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from pdf_extract.labeling.labels import DAYS_IN_MONTH, WEEKS_OF_MONTH
from pdf_extract.schedule_extraction import _normalize_published_date, _valid_str

MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)

Month = Literal[
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
WeekOfMonth = Literal["first", "second", "third", "fourth", "fifth", "last"]

_TIME_DESC = "Formatted as `h:MM AM` or `h:MM PM`."
_END_TIME_DESC = "For Mass, leave null. For Confession and Adoration, include when available."
_PAGE_DESC = "1-indexed PDF page where this entry was found."
_SLUG_DESC = "Must exactly match a `slug` from the provided known-churches list."


# ── Schema ──────────────────────────────────────────────────────────────────
class Season(BaseModel):
    """The part of the year a weekly slot runs; months and days are inclusive."""

    model_config = ConfigDict(extra="forbid")

    start_month: Month = Field(
        description=(
            "First month of the year the slot runs, e.g. `October` for 'Confessions "
            "Tuesdays, October through June'."
        ),
    )
    start_day: int | None = Field(
        default=None,
        description=(
            "Day of `start_month` the slot starts on, e.g. `4` for 'June 4 through "
            "September 10'. Fill only when the bulletin dated the boundary; leave null "
            "when it names the month alone. Do not invent the 1st."
        ),
    )
    end_month: Month = Field(
        description=(
            "Last month of the year the slot runs, e.g. `June`. A start later in the "
            "calendar than the end wraps the new year."
        ),
    )
    end_day: int | None = Field(
        default=None,
        description=(
            "Day of `end_month` the slot runs through, e.g. `10`. Fill only when the "
            "bulletin dated the boundary; leave null when it names the month alone. "
            "Do not invent the 30th."
        ),
    )


class WeeklySlot(BaseModel):
    """One recurring weekly time slot at a church (Mass, Confession, or Adoration)."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(description=_SLUG_DESC)
    day_of_week: str = Field(description="Full English weekday name, e.g. `Monday`.")
    start_time: str = Field(description=_TIME_DESC)
    end_time: str | None = Field(default=None, description=_END_TIME_DESC)
    weeks_of_month: list[WeekOfMonth] = Field(
        default_factory=list,
        description=(
            "Which occurrences of `day_of_week` within the month this slot falls on. "
            "`last` is not `fourth`. Examples: `[\"first\"]` for First Friday "
            "devotions; `[\"first\", \"third\"]` for 1st and 3rd Saturdays. Leave "
            "empty when the slot happens every week."
        ),
    )
    season: Season | None = Field(
        default=None,
        description=(
            "The part of the year the slot runs, when the bulletin limits it (e.g. "
            "'October through June', 'summer schedule'). Leave null for a slot that "
            "runs all year. A half-stated season ('runs from October', no end) is no "
            "season: leave it null rather than inventing an end month."
        ),
    )
    page_number: int | None = Field(default=None, description=_PAGE_DESC)
    note: str | None = Field(
        default=None,
        description=(
            "Short phrase only when there is genuinely special context (language, "
            "location nuance, benediction, etc.). Do not restate what "
            "`weeks_of_month` or `season` already say. Exclusions the fields cannot "
            "express ('every Saturday except the first') stay here."
        ),
    )


class DateSlot(BaseModel):
    """One calendar-dated time slot at a church (Mass, Confession, or Adoration)."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(description=_SLUG_DESC)
    date: str = Field(description="Specific calendar date formatted as `YYYY-MM-DD`.")
    start_time: str = Field(description=_TIME_DESC)
    end_time: str | None = Field(default=None, description=_END_TIME_DESC)
    page_number: int | None = Field(default=None, description=_PAGE_DESC)
    note: str | None = Field(
        default=None,
        description=(
            "Short phrase only when there is genuinely special context (language, "
            "season, location nuance, benediction, etc.)."
        ),
    )


class WeeklySchedule(BaseModel):
    """Recurring weekly lines grouped by Mass, Confession, and Adoration."""

    model_config = ConfigDict(extra="forbid")

    masses: list[WeeklySlot] = Field(default_factory=list)
    confessions: list[WeeklySlot] = Field(default_factory=list)
    adorations: list[WeeklySlot] = Field(default_factory=list)


class SingleEvents(BaseModel):
    """One-off or extra dated occurrences not already covered by `WeeklySchedule`."""

    model_config = ConfigDict(extra="forbid")

    masses: list[DateSlot] = Field(default_factory=list)
    confessions: list[DateSlot] = Field(default_factory=list)
    adorations: list[DateSlot] = Field(default_factory=list)


class Cancellations(BaseModel):
    """Dated occurrences the bulletin marks as cancelled."""

    model_config = ConfigDict(extra="forbid")

    masses: list[DateSlot] = Field(default_factory=list)
    confessions: list[DateSlot] = Field(default_factory=list)
    adorations: list[DateSlot] = Field(default_factory=list)


class QualifiedSchedulePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weekly_schedule: WeeklySchedule = Field(
        default_factory=WeeklySchedule,
        description="Recurring weekly Mass, Confession, and Adoration entries.",
    )
    single_events: SingleEvents = Field(
        default_factory=SingleEvents,
        description=(
            "One-off or extra dates. Do not include an entry that duplicates an "
            "existing `weekly_schedule` slot."
        ),
    )
    cancellations: Cancellations = Field(
        default_factory=Cancellations,
        description="Include cancelled events here.",
    )
    church_list_needs_review: bool = Field(
        default=False,
        description=(
            "True only if (a) the bulletin clearly shows a church in the parish that "
            "has events but is not in the provided list, or (b) a provided church "
            "name/address is obviously wrong."
        ),
    )
    published_date: str | None = Field(
        default=None,
        description="The bulletin's issue date as `YYYY-MM-DD`.",
    )
    wrong_bulletin: bool = Field(
        default=False,
        description=(
            "True only if this is clearly not the correct bulletin (not a bulletin at "
            "all, not the correct parish, from a different year, etc.)"
        ),
    )


# ── Prompt ──────────────────────────────────────────────────────────────────
# Started from the production Gemini prompt (schedule_extraction.EVENTS_SYSTEM_PROMPT)
# and extended with the labeling rules. Its two per-bulletin sections come after
# these instructions, so everything up to them is the same for every request.
INSTRUCTIONS = """\
# Role

Extract Mass, Confession, and Adoration schedule information from the attached Catholic parish bulletin PDF. The output feeds a public Mass-times website, so a wrong time is worse than a missing one.

# What to extract

- Only extract Mass, Confession (Reconciliation, Penance), and Adoration (Exposition, Holy Hour) events. Ignore every other kind of event or activity in the bulletin.
- A Communion Service (a Liturgy of the Word with Communion, led by a deacon or lay minister) is not a Mass: never record one as a Mass. When the bulletin says a Communion Service replaces a Mass on a date, record that Mass under `cancellations` for that date.
- Skip anything without a definite start time, such as "Confession by appointment" or "call the office".

# Churches and chapels

- Attach every event to one of the churches in the known-churches list (given after these instructions) using its exact `slug`.
- An event in a chapel or room of a listed church itself ("in the chapel", "Blessed Sacrament Chapel", "in the church hall") belongs to that church; say where in a short `note`.
- An event at a separate chapel (a convent, school, hospital, nursing home or mission chapel with its own building), or one whose location is unclear, is left out unless the known-churches list includes that chapel or its address. If you leave out such a chapel that clearly has its own Mass, Confession or Adoration times, set `church_list_needs_review` to true.

# Weekly or dated

Sort each event into exactly one bucket:

- `weekly_schedule` for recurring weekly times.
- `single_events` for occurrences on a specific date that are not already covered by a weekly entry.
- `cancellations` for events that the bulletin says are cancelled, moved, or will not take place on a specific date. A moved event is a cancellation of the original date and time plus a single event at the new one.

To decide between weekly and dated:

1. Times presented as the parish's regular schedule ("Weekend Masses", "Daily Mass", "Mass Schedule", "Confessions: Saturdays 3:00-3:45 PM") are weekly. A range of days ("Monday-Friday 8:00 AM") is one weekly entry per day.
2. Times given only with a date, or with a date and its weekday ("Tuesday, October 6, 7:00 PM Adoration"), are dated, including the dated times in a weekly calendar or a list of Mass intentions.
3. Exception: if the bulletin shows dated times for two or more weeks and the same slot (church, type, weekday and time) appears in each of those weeks, record it as weekly, unless the bulletin marks it as special or one-off.
4. When it is unclear, prefer dated. A slot recorded as dated that turns up again in later bulletins is promoted to weekly automatically; a slot wrongly recorded as weekly stays wrong.
5. Never duplicate a weekly slot as a single event just because the bulletin also lists it on a date in a specific week. Holy days, holidays, feast-day Masses and other special services are dated.

# Weekly qualifiers

- `weeks_of_month`: for slots that only happen on some occurrences of the weekday in a month, such as "First Friday Adoration" or "1st and 3rd Saturdays". Leave it empty for every week.
- `season`: for slots the bulletin limits to part of the year ("October through June", "summer schedule"), with the months it gives.

# Times

- `start_time` and `end_time` are formatted as `h:MM AM` or `h:MM PM`; "noon" is `12:00 PM`.
- For Mass, leave `end_time` null. For Confession and Adoration, give `end_time` when the bulletin gives one or a duration ("one hour"); leave it null for "until all are heard" or no end.
- When the bulletin times an event relative to a Mass rather than giving a clock time, work it out from that Mass's start time:
  - "After" or "following" a weekend Mass (Saturday evening vigil or Sunday): 1 hour after the Mass starts.
  - "After" or "following" a weekday Mass: 30 minutes after the Mass starts.
  - "N minutes before Mass": N minutes before it, ending when the Mass starts. "Before every Mass" is one entry for each Mass it refers to.

# Notes

Only add a `note` when there is genuinely special context worth surfacing: language, location within the church, benediction, a relative timing you converted ("after the 4:00 PM Mass"), a special occasion. Do not write 'Vigil Mass', and do not repeat what `weeks_of_month` or `season` already say.

# Bulletin

- Identify the bulletin's own issue date and report it as `published_date`.
- Set `wrong_bulletin` to true only if the attached PDF is clearly not a current bulletin for this parish (wrong parish, wrong year, not a bulletin at all, etc.). In that case you may return empty event lists.

Read the whole bulletin, including calendars, sidebars and the back page, and carefully find every event it lists.
"""

CONTEXT_TEMPLATE = """\
# Known churches for this parish

```json
{churches_json}
```

# Today's date

{today_iso} ({today_day_of_week})
"""


def render_context(churches: list[dict[str, Any]], today_iso: str, today_day: str) -> str:
    return CONTEXT_TEMPLATE.format(
        churches_json=json.dumps(churches, ensure_ascii=False),
        today_iso=today_iso,
        today_day_of_week=today_day,
    )


def fingerprint(*parts: str) -> str:
    """A short digest of everything that shapes the output, for cache versions."""
    return sha256("\x00".join(parts).encode("utf-8")).hexdigest()[:12]


SCHEMA_FINGERPRINT = fingerprint(
    INSTRUCTIONS,
    CONTEXT_TEMPLATE,
    json.dumps(QualifiedSchedulePayload.model_json_schema(), sort_keys=True),
)


# ── Flattening ──────────────────────────────────────────────────────────────
_MONTH_NUMBER = {name: i for i, name in enumerate(MONTHS, start=1)}
_SECTIONS = (
    ("weekly_schedule", "weekly", False),
    ("single_events", "specific_date", False),
    ("cancellations", "specific_date", True),
)
_TYPES = (("mass", "masses"), ("confession", "confessions"), ("adoration", "adorations"))


def _month(value: Any) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool):
        return value if 1 <= value <= 12 else None
    return _MONTH_NUMBER.get(value.strip().capitalize()) if isinstance(value, str) else None


def _day(value: Any, month: int) -> int | None:
    if not isinstance(value, int) or isinstance(value, bool):
        return None
    return value if 1 <= value <= DAYS_IN_MONTH[month - 1] else None


def _weeks(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    wanted = {w.strip().lower() for w in value if isinstance(w, str)}
    return [w for w in WEEKS_OF_MONTH if w in wanted]


def _season_fields(value: Any) -> dict[str, int | None]:
    """PR 22's flat season fields; all null unless both months are readable."""
    fields: dict[str, int | None] = dict.fromkeys(
        ("season_start_month", "season_start_day", "season_end_month", "season_end_day")
    )
    if not isinstance(value, dict):
        return fields
    start, end = _month(value.get("start_month")), _month(value.get("end_month"))
    if start is None or end is None:
        return fields
    fields.update(
        season_start_month=start,
        season_start_day=_day(value.get("start_day"), start),
        season_end_month=end,
        season_end_day=_day(value.get("end_day"), end),
    )
    return fields


def flatten_events(raw: QualifiedSchedulePayload | dict[str, Any]) -> dict[str, Any]:
    """The classifier result shape (see classifiers.base) with qualifiers on each event.

    Takes a validated payload or, when validation failed, the raw parsed JSON;
    both go through the same lenient reading so they cannot differ in shape.
    """
    if isinstance(raw, QualifiedSchedulePayload):
        raw = raw.model_dump(mode="json")

    events: list[dict[str, Any]] = []
    for section_key, kind, cancelled in _SECTIONS:
        section = raw.get(section_key)
        if not isinstance(section, dict):
            continue
        for event_type, key in _TYPES:
            for item in section.get(key) or []:
                if not isinstance(item, dict):
                    continue
                weekly = kind == "weekly"
                anchor = item.get("day_of_week") if weekly else item.get("date")
                church_slug, start_time = item.get("church_slug"), item.get("start_time")
                if not (_valid_str(church_slug) and _valid_str(start_time) and _valid_str(anchor)):
                    continue
                end_time = item.get("end_time")
                page = item.get("page_number")
                note = item.get("note")
                events.append({
                    "church_slug": church_slug,
                    "type": event_type,
                    "kind": kind,
                    "day_of_week": anchor if weekly else None,
                    "date": None if weekly else anchor,
                    "start_time": start_time,
                    "end_time": end_time if isinstance(end_time, str) else None,
                    "cancelled": cancelled,
                    "page_number": page if isinstance(page, int) else None,
                    "note": note.strip() if isinstance(note, str) and note.strip() else None,
                    "weeks_of_month": _weeks(item.get("weeks_of_month")) if weekly else [],
                    **_season_fields(item.get("season") if weekly else None),
                })

    return {
        "events": events,
        "church_list_needs_review": bool(raw.get("church_list_needs_review", False)),
        "published_date": _normalize_published_date(raw.get("published_date")),
        "wrong_bulletin": bool(raw.get("wrong_bulletin", False)),
    }
