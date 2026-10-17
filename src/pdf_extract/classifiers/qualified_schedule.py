"""What a classifier is asked for when it is scored against the ground-truth labels.

The production extraction schema (`schedule_extraction.SchedulePayload`) plus the
two recurrence qualifiers the labels record on weekly slots: which weeks of the
month a slot falls on (`weeks_of_month`) and which part of the year it runs
(`season`). The qualifier field descriptions follow PR 22's extraction schema.

The prompt is in two parts so the part that never changes comes first: the
shared policy (`schedule_policy.POLICY`) is identical for every bulletin and
every provider, and can be served from a prompt cache, while `CONTEXT_TEMPLATE`
(the parish's churches and today's date) and then the PDF follow it.

`flatten_events` turns a payload into the pipeline's flat event dicts, with the
qualifiers in the flat form PR 22 uses (`weeks_of_month`, `season_start_month`,
...) plus `exclude_weeks`; `labeling.bulletins.gemini_rows` reads that form into
label rows.
"""

from __future__ import annotations

import json
from hashlib import sha256
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from pdf_extract.classifiers.schedule_policy import POLICY
from pdf_extract.labeling.labels import DAYS_IN_MONTH, WEEKS_OF_MONTH, canonical_weeks
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
            "devotions; `[\"first\", \"third\"]` for 1st and 3rd Saturdays. The "
            "weeks the slot happens on, unless `exclude_weeks`: 'every Saturday except "
            "the first' is `[\"second\", \"third\", \"fourth\", \"fifth\"]`. Leave "
            "empty when the slot happens every week."
        ),
    )
    exclude_weeks: bool = Field(
        default=False,
        description=(
            "True when `weeks_of_month` lists the weeks the slot skips, for an "
            "exclusion of the last week, which the remaining weeks can't say: 'every "
            "Sunday except the last' is `[\"last\"]` with this true. False otherwise."
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
            "location nuance, `Benediction`, etc.). Do not restate what "
            "`weeks_of_month` or `season` already say, and do not describe an "
            "exclusion: say it with `weeks_of_month` and `exclude_weeks`."
        ),
    )


class DateSlot(BaseModel):
    """One calendar-dated time slot at a church (Mass, Confession, or Adoration)."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(description=_SLUG_DESC)
    date: str = Field(
        description=(
            "Specific calendar date formatted as `YYYY-MM-DD`. The bulletin must print "
            "it, or tie a weekday to one clear day (\"this Saturday\"); never project "
            "a date from a weekly slot or a weeks-of-the-month pattern."
        ),
    )
    start_time: str = Field(description=_TIME_DESC)
    end_time: str | None = Field(default=None, description=_END_TIME_DESC)
    page_number: int | None = Field(default=None, description=_PAGE_DESC)
    note: str | None = Field(
        default=None,
        description=(
            "Short phrase only when there is genuinely special context (language, "
            "season, location nuance, `Benediction`, etc.)."
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
# The static policy (`schedule_policy.POLICY`) comes first; this per-bulletin
# section follows it, then the PDF.
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
    POLICY,
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


def _week_fields(item: dict[str, Any]) -> dict[str, Any]:
    """A weekly slot's `weeks_of_month` and `exclude_weeks`, in their canonical form."""
    weeks, exclude = canonical_weeks(
        _weeks(item.get("weeks_of_month")), item.get("exclude_weeks") is True,
    )
    return {"weeks_of_month": weeks, "exclude_weeks": exclude}


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
                    **(
                        _week_fields(item) if weekly
                        else {"weeks_of_month": [], "exclude_weeks": False}
                    ),
                    **_season_fields(item.get("season") if weekly else None),
                })

    return {
        "events": events,
        "church_list_needs_review": bool(raw.get("church_list_needs_review", False)),
        "published_date": _normalize_published_date(raw.get("published_date")),
        "wrong_bulletin": bool(raw.get("wrong_bulletin", False)),
    }
