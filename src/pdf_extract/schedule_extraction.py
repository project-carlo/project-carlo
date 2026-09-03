"""Extract structured schedule data from bulletin PDFs using Gemini."""

import json
import logging
import random
import re
import threading
import time
from datetime import date
from typing import Any, Literal

from google import genai
from google.genai import errors, types
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from pdf_extract.schedule_pattern import (
    NO_SEASON,
    Season,
    normalize_season,
    normalize_weeks_of_month,
)

LOGGER = logging.getLogger(__name__)

# Bump whenever the extraction schema or prompt changes in a way that would make
# a stored result wrong or incomplete. Classifiers fold it into their `version`,
# which keys the on-disk result cache, so an old bulletin re-processed after a
# change is re-extracted instead of served from a cache that predates it.
# 2: weeks_of_month and the season months on weekly slots.
# 3: season boundaries to the day.
SCHEMA_VERSION = 3

_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_MAX_API_ATTEMPTS = 8
_BASE_BACKOFF_SECONDS = 2.0
_MAX_BACKOFF_SECONDS = 30.0

# Shared backoff gate: when any thread hits a transient Gemini error, no thread
# starts a new request until the backoff window has expired. This stops fresh
# requests from outcompeting the backed-off one for quota.
_pause_lock = threading.Lock()
_pause_until = 0.0  # time.monotonic() deadline


def _wait_for_gate() -> None:
    """Block until any active global backoff window has expired."""
    while True:
        with _pause_lock:
            remaining = _pause_until - time.monotonic()
        if remaining <= 0:
            return
        time.sleep(remaining)


def _extend_gate(delay: float) -> None:
    """Hold all new Gemini requests for at least `delay` seconds from now."""
    global _pause_until
    deadline = time.monotonic() + delay
    with _pause_lock:
        _pause_until = max(_pause_until, deadline)

# ── LLM extraction schema ──────────────────────────────────────────────────


class WeeklySlot(BaseModel):
    """One recurring weekly time slot at a church (Mass, Confession, or Adoration)."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(min_length=1, description="Must exactly match a `slug` from the provided known-churches list.")
    day_of_week: str = Field(min_length=1, description="Full English weekday name, e.g. `Monday`.")
    start_time: str = Field(min_length=1, description="Formatted as `h:MM AM` or `h:MM PM`.")
    end_time: str | None = Field(default=None, description="For Mass, leave null. For Confession and Adoration, include when available.")
    weeks_of_month: list[str] = Field(
        default_factory=list,
        description=(
            "Only for a slot that falls on particular weeks of the month rather than every week, "
            "e.g. `[\"first\"]` for First Friday devotions or `[\"first\", \"third\"]` for "
            "1st and 3rd Saturdays. Allowed values: `first`, `second`, `third`, `fourth`, `fifth`, "
            "`last`. Leave empty for a slot that happens every week."
        ),
    )
    season_start_month: str | None = Field(
        default=None,
        description=(
            "First month of the year the slot runs, e.g. `October` for "
            "'Confessions Tuesdays, October through June'. Full English month name. "
            "Leave null for a slot that runs all year round."
        ),
    )
    season_start_day: int | None = Field(
        default=None,
        description=(
            "Day of `season_start_month` the slot starts on, e.g. `4` for 'June 4 "
            "through September 10'. Only when the bulletin gives a date; leave null "
            "when it names the month alone."
        ),
    )
    season_end_month: str | None = Field(
        default=None,
        description=(
            "Last month of the year the slot runs, e.g. `June`. Set it together with "
            "`season_start_month`; leave both null for a slot that runs all year round."
        ),
    )
    season_end_day: int | None = Field(
        default=None,
        description=(
            "Day of `season_end_month` the slot runs through, e.g. `10`. Only when the "
            "bulletin gives a date; leave null when it names the month alone."
        ),
    )
    page_number: int | None = Field(default=None, description="1-indexed PDF page where this entry was found.")
    note: str | None = Field(default=None, description="Short phrase only when there is genuinely special context (language, location nuance, benediction, etc.). Do not restate what `weeks_of_month` or the season fields already say.")


class DateSlot(BaseModel):
    """One calendar-dated time slot at a church (Mass, Confession, or Adoration)."""

    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(min_length=1, description="Must exactly match a `slug` from the provided known-churches list.")
    date: str = Field(min_length=1, description="Specific calendar date formatted as `YYYY-MM-DD`.")
    start_time: str = Field(min_length=1, description="Formatted as `h:MM AM` or `h:MM PM`.")
    end_time: str | None = Field(default=None, description="For Mass, leave null. For Confession and Adoration, include when available.")
    page_number: int | None = Field(default=None, description="1-indexed PDF page where this entry was found.")
    note: str | None = Field(default=None, description="Short phrase only when there is genuinely special context (language, season, location nuance, benediction, etc.).")


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


class SchedulePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weekly_schedule: WeeklySchedule = Field(
        default_factory=WeeklySchedule,
        description="Recurring weekly Mass, Confession, and Adoration entries.",
    )
    single_events: SingleEvents = Field(
        default_factory=SingleEvents,
        description=(
            "One-off or extra dates. Do not include an entry that duplicates an existing `weekly_schedule` slot."
        ),
    )
    cancellations: Cancellations = Field(
        default_factory=Cancellations,
        description=(
            "Include cancelled events here."
        ),
    )
    church_list_needs_review: bool = Field(
        default=False,
        description=(
            "True only if (a) the bulletin clearly shows a church in the parish that has events but is not in the provided list, "
            "or (b) a provided church name/address is obviously wrong."
        ),
    )
    published_date: str | None = Field(
        default=None,
        description=(
            "The bulletin's issue date as `YYYY-MM-DD`."
        ),
    )
    wrong_bulletin: bool = Field(
        default=False,
        description=(
            "True only if this is clearly not the correct bulletin (not a bulletin at all, not the correct parish, from a different year, etc.)"
        ),
    )


def _valid_str(s: Any) -> bool:
    return isinstance(s, str) and bool(s.strip())


def _collect_events(
    section: dict[str, Any],
    *,
    kind: Literal["weekly", "specific_date"],
    cancelled: bool,
) -> list[dict[str, Any]]:
    """Collect flat events from a section (weekly_schedule, single_events, or cancellations)."""
    if not isinstance(section, dict):
        return []
    events: list[dict[str, Any]] = []
    for event_type, key in [("mass", "masses"), ("confession", "confessions"), ("adoration", "adorations")]:
        for item in section.get(key) or []:
            if not isinstance(item, dict):
                continue
            church_slug = item.get("church_slug")
            start_time = item.get("start_time")
            if kind == "weekly":
                day_of_week = item.get("day_of_week")
                date_val = None
                if not _valid_str(church_slug) or not _valid_str(start_time) or not _valid_str(day_of_week):
                    continue
                pattern = _pattern_fields(
                    item.get("weeks_of_month"),
                    normalize_season(
                        item.get("season_start_month"),
                        item.get("season_start_day"),
                        item.get("season_end_month"),
                        item.get("season_end_day"),
                    ),
                )
            else:
                day_of_week = None
                date_val = item.get("date")
                if not _valid_str(church_slug) or not _valid_str(start_time) or not _valid_str(date_val):
                    continue
                pattern = _pattern_fields(None, NO_SEASON)
            end_time = item.get("end_time") if isinstance(item.get("end_time"), str) else None
            page_number = item.get("page_number") if isinstance(item.get("page_number"), int) else None
            note_raw = item.get("note")
            note = note_raw.strip() if isinstance(note_raw, str) and note_raw.strip() else None
            events.append({
                "church_slug": church_slug,
                "type": event_type,
                "kind": kind,
                "day_of_week": day_of_week,
                "date": date_val,
                "start_time": start_time,
                "end_time": end_time,
                "cancelled": cancelled,
                "page_number": page_number,
                "note": note,
                **pattern,
            })
    return events


_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _normalize_published_date(raw: Any) -> str | None:
    """Accept a YYYY-MM-DD string from the LLM, or None."""
    if not isinstance(raw, str):
        return None
    value = raw.strip()
    if not value:
        return None
    if not _ISO_DATE_RE.match(value):
        return None
    return value


def _note_value(note: str | None) -> str | None:
    if note is None:
        return None
    stripped = note.strip()
    return stripped or None


def _pattern_fields(weeks_of_month: Any, season: Season) -> dict[str, Any]:
    """Canonicalise a weekly slot's recurrence qualifiers for the flat event dict.

    Normalising here rather than at the database boundary means events.json —
    and the on-disk extraction cache behind it — holds one settled form of these
    fields, so the recurrence detector and the DB loader do not each have to
    re-interpret whatever wording the model chose.
    """
    return {
        "weeks_of_month": normalize_weeks_of_month(weeks_of_month),
        "season_start_month": season.start_month,
        "season_start_day": season.start_day,
        "season_end_month": season.end_month,
        "season_end_day": season.end_day,
    }


def _weekly_slot_to_event(
    slot: WeeklySlot,
    *,
    event_type: Literal["mass", "confession", "adoration"],
    cancelled: bool,
) -> dict[str, Any]:
    return {
        "church_slug": slot.church_slug,
        "type": event_type,
        "kind": "weekly",
        "day_of_week": slot.day_of_week,
        "date": None,
        "start_time": slot.start_time,
        "end_time": slot.end_time,
        "cancelled": cancelled,
        "page_number": slot.page_number,
        "note": _note_value(slot.note),
        **_pattern_fields(
            slot.weeks_of_month,
            normalize_season(
                slot.season_start_month,
                slot.season_start_day,
                slot.season_end_month,
                slot.season_end_day,
            ),
        ),
    }


def _date_slot_to_event(
    slot: DateSlot,
    *,
    event_type: Literal["mass", "confession", "adoration"],
    cancelled: bool,
) -> dict[str, Any]:
    return {
        "church_slug": slot.church_slug,
        "type": event_type,
        "kind": "specific_date",
        "day_of_week": None,
        "date": slot.date,
        "start_time": slot.start_time,
        "end_time": slot.end_time,
        "cancelled": cancelled,
        "page_number": slot.page_number,
        "note": _note_value(slot.note),
        **_pattern_fields(None, NO_SEASON),
    }


def _events_from_payload(payload: SchedulePayload) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for event_type, slots in [
        ("mass", payload.weekly_schedule.masses),
        ("confession", payload.weekly_schedule.confessions),
        ("adoration", payload.weekly_schedule.adorations),
    ]:
        for slot in slots:
            events.append(_weekly_slot_to_event(slot, event_type=event_type, cancelled=False))
    for event_type, slots in [
        ("mass", payload.single_events.masses),
        ("confession", payload.single_events.confessions),
        ("adoration", payload.single_events.adorations),
    ]:
        for slot in slots:
            events.append(_date_slot_to_event(slot, event_type=event_type, cancelled=False))
    for event_type, slots in [
        ("mass", payload.cancellations.masses),
        ("confession", payload.cancellations.confessions),
        ("adoration", payload.cancellations.adorations),
    ]:
        for slot in slots:
            events.append(_date_slot_to_event(slot, event_type=event_type, cancelled=True))
    return events


def _reconstruct_events_from_dict(raw: dict[str, Any]) -> dict[str, Any]:
    ws = raw.get("weekly_schedule") or {}
    se = raw.get("single_events") or {}
    can = raw.get("cancellations") or {}

    events: list[dict[str, Any]] = []
    events.extend(_collect_events(ws, kind="weekly", cancelled=False))
    events.extend(_collect_events(se, kind="specific_date", cancelled=False))
    events.extend(_collect_events(can, kind="specific_date", cancelled=True))

    return {
        "events": events,
        "church_list_needs_review": bool(raw.get("church_list_needs_review", False)),
        "published_date": _normalize_published_date(raw.get("published_date")),
        "wrong_bulletin": bool(raw.get("wrong_bulletin", False)),
    }


def reconstruct_events(raw: SchedulePayload | dict[str, Any]) -> dict[str, Any]:
    """Convert structured schema to flat events format.

    Returns:
        Dict with "events" (list of flat event dicts), "church_list_needs_review" (bool),
        "published_date" (str | None, YYYY-MM-DD), and "wrong_bulletin" (bool).
    """
    if isinstance(raw, SchedulePayload):
        return {
            "events": _events_from_payload(raw),
            "church_list_needs_review": raw.church_list_needs_review,
            "published_date": _normalize_published_date(raw.published_date),
            "wrong_bulletin": raw.wrong_bulletin,
        }
    return _reconstruct_events_from_dict(raw)


def _parse_llm_json(content: str, *, context: str) -> dict[str, Any]:
    """Parse a Gemini JSON string, warning (not raising) on bad output.

    Gemini is configured with response_mime_type=application/json and a JSON schema,
    so malformed output or non-dict top-level values indicate an LLM-side problem.
    We coalesce to {} so downstream normalisation treats it as an empty result,
    but log enough detail to distinguish this from a genuinely empty bulletin.
    """
    snippet = content[:200].replace("\n", " ")
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        LOGGER.warning(
            "%s: failed to parse Gemini JSON (len=%d, err=%s): %r",
            context, len(content), exc, snippet,
        )
        return {}
    if not isinstance(data, dict):
        LOGGER.warning(
            "%s: Gemini JSON top-level is %s, expected object (len=%d): %r",
            context, type(data).__name__, len(content), snippet,
        )
        return {}
    return data


def _is_retryable_api_error(exc: Exception) -> bool:
    """Return true when the Gemini API error is likely transient."""
    return isinstance(exc, errors.APIError) and exc.code in _RETRYABLE_STATUS_CODES


def _generate_content_with_backoff(
    client: genai.Client,
    *,
    model: str,
    contents: list[str | types.Part],
    config: types.GenerateContentConfig,
):
    """Call Gemini generate_content with exponential backoff for transient API failures.

    Backoff windows are shared process-wide via the gate above: while any thread
    is backing off, no thread starts a new request.
    """
    for attempt in range(1, _MAX_API_ATTEMPTS + 1):
        _wait_for_gate()
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
        except Exception as exc:
            is_last_attempt = attempt == _MAX_API_ATTEMPTS
            if not _is_retryable_api_error(exc) or is_last_attempt:
                raise

            backoff = min(_MAX_BACKOFF_SECONDS, _BASE_BACKOFF_SECONDS * (2 ** (attempt - 1)))
            delay = backoff + random.uniform(0, 0.25 * backoff)
            LOGGER.warning(
                "Gemini request failed with status %s on attempt %s/%s; retrying in %.1fs",
                getattr(exc, "code", "unknown"),
                attempt,
                _MAX_API_ATTEMPTS,
                delay,
            )
            _extend_gate(delay)


# ── Verification models ──────────────────────────────────────────────────────


class Address(BaseModel):
    model_config = ConfigDict(extra="forbid")

    line1: str | None = None
    line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None


class ChurchVerification(BaseModel):
    model_config = ConfigDict(extra="forbid")

    church_slug: str = Field(min_length=1)
    name_status: Literal["verified", "incorrect", "unverifiable"]
    address_status: Literal["verified", "incorrect", "unverifiable"]
    corrected_name: str | None = None
    corrected_address: Address | None = None
    slug_needs_review: bool = False


class NewChurch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    slug: str | None = None
    address: Address | None = None


class VerificationPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    existing_churches: list[ChurchVerification]
    new_churches: list[NewChurch]


# ── Event extraction ─────────────────────────────────────────────────────────


EVENTS_SYSTEM_PROMPT = """\
# Role

Extract Mass, Confession, and Adoration schedule information from the attached Catholic parish bulletin PDF.

# Known churches for this parish

```json
{churches_json}
```

# Today's date

{today_iso} ({today_day_of_week})

# Instructions

- Only extract Mass, Confession, and Adoration events. Ignore every other kind of event or activity in the bulletin.
- Attach every event to one of the churches in the known-churches list using its exact `slug`.
- Sort each event into exactly one bucket:
  - `weekly_schedule` for recurring weekly times.
  - `single_events` for one-off or extra occurrences on a specific date that are not already covered by a weekly entry.
  - `cancellations` for events that the bulletin explicitly says are cancelled, moved, or will not take place on a specific date.
- Never duplicate a weekly slot as a single event just because the bulletin also mentions it in a specific week.
- A weekly entry that only falls on certain weeks of the month ("First Friday devotions", "1st and 3rd Saturdays", "Healing Mass on the first Monday") still belongs in `weekly_schedule`: give it that weekday and list those weeks in `weeks_of_month`. Leave `weeks_of_month` empty for a slot that happens every week.
- A weekly entry that only runs for part of the year ("Confessions Tuesdays, October through June", "summer Mass schedule", "resumes after Labor Day") also belongs in `weekly_schedule`: fill in `season_start_month` and `season_end_month`. Set both or neither. Use the months the bulletin states; when it names a season instead, use the months that season covers for this parish (summer as June through August, a school-year schedule as September through June). Read an exclusion the same way — a slot that does not run in July or August is a September-through-June slot.
- When the bulletin dates the range precisely ("June 4 through September 10", "Masses resume Sept. 8"), also fill in `season_start_day` and `season_end_day`. Leave a day null when the bulletin names only the month; do not invent the 1st or the 30th, since a range stated in whole months is read back to the reader in whole months.
- Only add a `note` when there is genuinely special context worth surfacing (language, alternate location, benediction, etc.). No need to specify 'Vigil Mass', and do not restate in `note` what `weeks_of_month` or the season fields already carry — a slot on certain weeks of the month needs no note at all unless the bulletin says something further about it.
- Identify the bulletin's own issue date and report it as `published_date`.
- Set `wrong_bulletin` to true only if the attached PDF is clearly not a current bulletin for this parish (wrong parish, wrong year, not a bulletin at all, etc.). In that case you may return empty event lists.

Carefully find the events listed in the bulletin.
"""


def extract_events(
    pdf_bytes: bytes,
    *,
    churches: list[dict],
    model: str = "gemini-3-flash-preview",
    today: date | None = None,
) -> dict[str, Any]:
    """Use Gemini to extract Mass, Confession, and Adoration schedule from a PDF.

    Args:
        pdf_bytes: Raw PDF bytes to analyze.
        churches: List of known churches [{name, address}, ...].
        model: Gemini model to use.
        today: Reference date used to help the LLM judge whether the bulletin is
            stale/misrouted. Defaults to today's local date.

    Returns:
        Dict with:
        - "events": list of event dicts (each with church_slug, type, kind, etc., including note)
        - "church_list_needs_review": bool
        - "published_date": str | None (YYYY-MM-DD)
        - "wrong_bulletin": bool

    """
    if not pdf_bytes:
        return reconstruct_events({})

    if today is None:
        today = date.today()

    churches_json = json.dumps(churches, ensure_ascii=False)
    prompt = EVENTS_SYSTEM_PROMPT.format(
        churches_json=churches_json,
        today_iso=today.isoformat(),
        today_day_of_week=today.strftime("%A"),
    )

    client = genai.Client()
    response = _generate_content_with_backoff(
        client,
        model=model,
        contents=[
            prompt,
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=SchedulePayload.model_json_schema(),
        ),
    )
    content = response.text or "{}"
    try:
        payload = SchedulePayload.model_validate_json(content)
    except ValidationError as exc:
        LOGGER.warning(
            "extract_events: Pydantic validation failed (%s); using lenient fallback",
            exc,
        )
        return reconstruct_events(_parse_llm_json(content, context="extract_events"))
    return reconstruct_events(payload)


# ── Verification extraction ──────────────────────────────────────────────────


VERIFY_SYSTEM_PROMPT = """\
You are a precise assistant that verifies church information against a Catholic parish bulletin PDF.

You are given:
1) A parish bulletin PDF
2) A list of known churches for this parish: {churches_json}

Each church in the list has a "slug" (stable URL identifier), "name", and "address".

For each church in the provided list:
- Echo back the church_slug exactly as provided (this is the only church identifier needed).
- Check if the church name can be verified from the bulletin. Report name_status as:
  - "verified" if the name matches what's in the bulletin
  - "incorrect" if the bulletin shows a different name — provide corrected_name
  - "unverifiable" if the bulletin doesn't mention this church
- Check if the church address can be verified from the bulletin. Report address_status as:
  - "verified" if the address matches what's in the bulletin
  - "incorrect" if the bulletin shows a different address — provide corrected_address as a structured object with fields: line1, line2 (or null), city, state, postal_code
  - "unverifiable" if the bulletin doesn't show an address for this church
- Set slug_needs_review to true ONLY if the slug is clearly a poor match for this church (e.g. slug says one city but the church is obviously in a different city, or slug refers to a completely different saint). Otherwise false.

For any churches that are clearly part of this parish (not guest/visiting churches) and are NOT in the provided list, add them to new_churches with name, slug (a short URL-friendly identifier based on the church name and city, like "st-marys-corning"), and address (as a structured object with line1, line2, city, state, postal_code).

Return output that matches the provided JSON schema exactly."""


def extract_verification(
    pdf_bytes: bytes,
    *,
    churches: list[dict],
    model: str = "gemini-3-flash-preview",
) -> dict[str, Any]:
    """Use Gemini to verify church data against a bulletin PDF.

    Args:
        pdf_bytes: Raw PDF bytes to analyze.
        churches: List of known churches [{name, address}, ...].
        model: Gemini model to use.

    Returns:
        Dict with existing_churches and new_churches.
    """
    if not pdf_bytes:
        return {"existing_churches": [], "new_churches": []}

    churches_json = json.dumps(churches, ensure_ascii=False)
    prompt = VERIFY_SYSTEM_PROMPT.format(churches_json=churches_json)

    client = genai.Client()
    response = _generate_content_with_backoff(
        client,
        model=model,
        contents=[
            prompt,
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=VerificationPayload.model_json_schema(),
        ),
    )
    content = response.text or "{}"
    try:
        payload = VerificationPayload.model_validate_json(content)
    except ValidationError as exc:
        LOGGER.warning(
            "extract_verification: Pydantic validation failed (%s); using lenient fallback",
            exc,
        )
        return _normalize_verification_lenient(
            _parse_llm_json(content, context="extract_verification")
        )
    return payload.model_dump(mode="json")


def _normalize_verification_lenient(data: dict[str, Any]) -> dict[str, Any]:
    """Lenient fallback when VerificationPayload.model_validate_json fails."""
    existing: list[dict[str, Any]] = []
    new_churches: list[dict[str, Any]] = []

    for c in data.get("existing_churches", []):
        if not isinstance(c, dict):
            continue
        church_slug = c.get("church_slug")
        if not isinstance(church_slug, str) or not church_slug.strip():
            continue
        name_status = c.get("name_status")
        if name_status not in {"verified", "incorrect", "unverifiable"}:
            name_status = "unverifiable"
        address_status = c.get("address_status")
        if address_status not in {"verified", "incorrect", "unverifiable"}:
            address_status = "unverifiable"
        entry: dict[str, Any] = {
            "church_slug": church_slug,
            "name_status": name_status,
            "address_status": address_status,
            "slug_needs_review": bool(c.get("slug_needs_review", False)),
        }
        if name_status == "incorrect":
            corrected = c.get("corrected_name")
            entry["corrected_name"] = corrected if isinstance(corrected, str) else None
        else:
            entry["corrected_name"] = None
        if address_status == "incorrect":
            corrected = c.get("corrected_address")
            entry["corrected_address"] = corrected if isinstance(corrected, dict) else None
        else:
            entry["corrected_address"] = None
        existing.append(entry)

    for c in data.get("new_churches", []):
        if not isinstance(c, dict):
            continue
        name = c.get("name")
        if not isinstance(name, str) or not name.strip():
            continue
        slug = c.get("slug")
        new_churches.append({
            "name": name,
            "slug": slug if isinstance(slug, str) else None,
            "address": c.get("address") if isinstance(c.get("address"), dict) else None,
        })

    # Round-trip through the model so this path returns the exact same shape
    # as the strict model_validate_json path.
    payload = VerificationPayload.model_validate(
        {"existing_churches": existing, "new_churches": new_churches}
    )
    return payload.model_dump(mode="json")
