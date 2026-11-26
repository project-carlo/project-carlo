"""The schedule's vocabulary, shared by every part of the pipeline.

An event is a Mass, Confession or Adoration, weekly or on one date. A weekly
event can be limited to some weeks of the month (`weeks_of_month`, the same
tokens and ranges `schedule_pattern` uses) and to a season. `weeks_of_month`
lists the weeks an event happens on, or, with `exclude_weeks` true, the weeks
it doesn't: "every Sunday except the last" is `["last"]` excluded, which no
list of the weeks that remain can say.

One more kind is Adoration only: a `continuous` entry is a standing chapel open
every day around the clock. It has no day, date or times; `access` says how a
visitor gets in (`ACCESS_KINDS`), and `open_from`/`open_until` the hours it is
unlocked when a door code is needed at the others. The site words these itself,
so nothing a person types is shown for them but a short `note`.

A schedule entry is one event written down this way (`ENTRY_KEYS`,
`validate_entry`). A seed (`pdf_extract.seeding`) holds entries in this shape,
and a label event (`pdf_extract.labeling.labels`) is an entry plus the keys
that describe one reading of one bulletin.

This module sits at the bottom of the package: it imports nothing from
`pdf_extract` but `timeparse`, so the schedule, the seeds, the labeler and the
evals can all import it without importing each other.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, date, datetime, time
from hashlib import sha256
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

from pdf_extract.timeparse import normalize_event_date, time_to_minutes

EVENT_TYPES = ("mass", "confession", "adoration")
EVENT_TYPE_LABELS = {"mass": "Mass", "confession": "Confession", "adoration": "Adoration"}
EVENT_KINDS = ("weekly", "specific_date")
# A standing chapel open around the clock, every day (docs/believed-schedules.md,
# "Chapels open 24 hours"). Adoration only, at most one per church. Kept out of
# EVENT_KINDS, which are the kinds with a day or a date and a start time.
CONTINUOUS = "continuous"
ENTRY_KINDS = (*EVENT_KINDS, CONTINUOUS)
# How a visitor gets into a continuous chapel: the bulletin says nothing; a code
# is needed outside its unlocked hours (`open_from`-`open_until`, when given); a
# code is needed at every hour; or only by arrangement with the parish.
ACCESS_KINDS = ("not_stated", "code_after_hours", "code", "arrangement")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
WEEKS_OF_MONTH = ("first", "second", "third", "fourth", "fifth", "last")
# The ordinals a month can have of a weekday; "last" is the fourth or the fifth.
ORDINAL_WEEKS = WEEKS_OF_MONTH[:5]

# A parish with no bulletin whose schedule comes from its own website or Facebook
# page instead: a source seed (docs/source-schedules-plan.md). `fetch` and `process`
# skip it; the seed is only replaced by a later approved one.
WEBSITE_SCHEDULE = "website_schedule"
# Where a source schedule is read: the parish's website, or its Facebook page.
WEBSITE = "website"
FACEBOOK = "facebook"
SOURCE_PLATFORMS = (WEBSITE, FACEBOOK)

# February has 29: a season boundary recurs every year, leap years included.
DAYS_IN_MONTH = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
SEASON_KEYS = ("start_month", "start_day", "end_month", "end_day")

ENTRY_KEYS = (
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "weeks_of_month", "exclude_weeks", "season", "note",
    "access", "open_from", "open_until",
)
# Keys an entry written before they existed may lack; a missing one reads as
# false (`exclude_weeks`) or null (the continuous chapel's access fields).
ENTRY_KEYS_ADDED_LATER = ("exclude_weeks", "access", "open_from", "open_until")
CONTINUOUS_KEYS = ("access", "open_from", "open_until")

# An event as the extraction compares it: church slug, event type, event kind,
# day of week, date, start time, end time, cancelled.
EventKey = tuple[str, str, str, str | None, str | None, str, str | None, bool]

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ── Weeks of the month ──────────────────────────────────────────────────────
def canonical_weeks(weeks: Any, exclude: Any) -> tuple[list[str], bool]:
    """The one way to write a weeks-of-the-month selection, in the labels' order.

    An exclusion that leaves out no "last" is the list of the weeks that
    remain ("every week except the first" is second to fifth). One that leaves
    out "last" stays an exclusion, without "fifth" (a fifth weekday is always
    the last). Excluding nothing is every week, and a selection that leaves no
    week (`weeks_never_happen`) is kept as given. Unknown tokens are dropped.
    """
    listed = set(weeks) if isinstance(weeks, list) else set()
    ordered = [w for w in WEEKS_OF_MONTH if w in listed]
    if exclude is not True or not ordered:
        return ordered, False
    if weeks_never_happen(ordered, True):
        return ordered, True
    if "last" not in listed:
        return [w for w in ORDINAL_WEEKS if w not in listed], False
    return [w for w in ordered if w != "fifth"], True


def weeks_never_happen(weeks: Any, exclude: Any) -> bool:
    """Whether a selection leaves no week at all: every ordinal, or the first four and the last, excluded."""
    listed = set(weeks) if isinstance(weeks, list) else set()
    return exclude is True and set(ORDINAL_WEEKS[:4]) <= listed and bool({"fifth", "last"} & listed)


# ── Identifiers ─────────────────────────────────────────────────────────────
def is_valid_slug(value: Any) -> bool:
    return isinstance(value, str) and len(value) <= 120 and bool(_SLUG_RE.match(value))


def is_valid_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_HASH_RE.match(value))


# ── Validation ──────────────────────────────────────────────────────────────
def is_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or not _DATE_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def check_keys(
    obj: dict[str, Any], expected: tuple[str, ...], where: str, *, may_lack: tuple[str, ...] = (),
) -> list[str]:
    """The keys `obj` is missing or has beyond `expected`, as error messages."""
    errors = []
    missing = [k for k in expected if k not in obj and k not in may_lack]
    extra = sorted(k for k in obj if k not in expected)
    if missing:
        errors.append(f"{where}: missing {', '.join(missing)}")
    if extra:
        errors.append(f"{where}: unknown {', '.join(extra)}")
    return errors


def _validate_season(season: Any, where: str) -> list[str]:
    if season is None:
        return []
    if not isinstance(season, dict):
        return [f"{where}.season must be null or an object"]
    errors = check_keys(season, SEASON_KEYS, f"{where}.season")
    if errors:
        return errors
    for edge in ("start", "end"):
        month = season[f"{edge}_month"]
        day = season[f"{edge}_day"]
        if not is_int(month) or not 1 <= month <= 12:
            errors.append(f"{where}.season.{edge}_month must be 1-12")
            continue
        if day is not None and (not is_int(day) or not 1 <= day <= DAYS_IN_MONTH[month - 1]):
            errors.append(f"{where}.season.{edge}_day must be null or a day of month {month}")
    return errors


def entry_value_errors(entry: dict[str, Any], where: str) -> list[str]:
    """Every reason the values of `entry`, whose keys are already checked, are not an entry's."""
    errors = []
    if not is_valid_slug(entry["church_slug"]):
        errors.append(f"{where}.church_slug must be a church slug")
    if entry["event_type"] not in EVENT_TYPES:
        errors.append(f"{where}.event_type must be one of {', '.join(EVENT_TYPES)}")
    kind = entry["event_kind"]
    if kind == CONTINUOUS:
        return errors + _continuous_errors(entry, where)
    if kind not in EVENT_KINDS:
        errors.append(f"{where}.event_kind must be one of {', '.join(ENTRY_KINDS)}")
    elif kind == "weekly":
        if entry["day_of_week"] not in DAYS:
            errors.append(f"{where}.day_of_week must be a weekday name for a weekly event")
        if entry["date"] is not None:
            errors.append(f"{where}.date must be null for a weekly event")
    else:
        if entry["day_of_week"] is not None:
            errors.append(f"{where}.day_of_week must be null for a dated event")
        if not is_iso_date(entry["date"]):
            errors.append(f"{where}.date must be YYYY-MM-DD for a dated event")

    if not isinstance(entry["start_time"], str) or not _TIME_RE.match(entry["start_time"]):
        errors.append(f"{where}.start_time must be HH:MM (24-hour)")
    end = entry["end_time"]
    if end is not None and (not isinstance(end, str) or not _TIME_RE.match(end)):
        errors.append(f"{where}.end_time must be null or HH:MM (24-hour)")
    if not isinstance(entry["cancelled"], bool):
        errors.append(f"{where}.cancelled must be true or false")

    weeks = entry["weeks_of_month"]
    if not isinstance(weeks, list) or any(w not in WEEKS_OF_MONTH for w in weeks):
        errors.append(f"{where}.weeks_of_month must be a list of {', '.join(WEEKS_OF_MONTH)}")
    elif len(set(weeks)) != len(weeks):
        errors.append(f"{where}.weeks_of_month has duplicates")
    elif weeks and kind == "specific_date":
        errors.append(f"{where}.weeks_of_month applies to weekly events only")
    exclude = entry.get("exclude_weeks", False)
    if not isinstance(exclude, bool):
        errors.append(f"{where}.exclude_weeks must be true or false")
    elif exclude and not weeks:
        errors.append(f"{where}.exclude_weeks needs the weeks it leaves out in weeks_of_month")
    elif exclude and weeks_never_happen(weeks, exclude):
        errors.append(f"{where}.exclude_weeks leaves out every week")
    errors.extend(_validate_season(entry["season"], where))
    if entry["season"] is not None and kind == "specific_date":
        errors.append(f"{where}.season applies to weekly events only")
    for key in CONTINUOUS_KEYS:
        if entry.get(key) is not None:
            errors.append(f"{where}.{key} is for a continuous chapel only")

    errors.extend(_note_errors(entry["note"], where))
    return errors


def _continuous_errors(entry: dict[str, Any], where: str) -> list[str]:
    """Why a `continuous` entry, its type and church already checked, is not one."""
    errors = []
    if entry["event_type"] != "adoration":
        errors.append(f"{where}: a continuous entry is Adoration only")
    for key in ("day_of_week", "date", "start_time", "end_time", "season"):
        if entry.get(key) is not None:
            errors.append(f"{where}.{key} must be null for a continuous entry")
    if entry.get("cancelled") is not False:
        errors.append(f"{where}.cancelled must be false for a continuous entry")
    if entry.get("weeks_of_month") != [] or entry.get("exclude_weeks", False) is not False:
        errors.append(f"{where}: a continuous entry has no weeks of the month")
    errors.extend(continuous_access_errors(
        entry.get("access"), entry.get("open_from"), entry.get("open_until"), where,
    ))
    errors.extend(_note_errors(entry["note"], where))
    return errors


def continuous_access_errors(
    access: Any, open_from: Any, open_until: Any, where: str,
) -> list[str]:
    """Why a continuous chapel's access fields (times as HH:MM) don't fit together."""
    if access not in ACCESS_KINDS:
        return [f"{where}.access must be one of {', '.join(ACCESS_KINDS)}"]
    errors = []
    for key, value in (("open_from", open_from), ("open_until", open_until)):
        if value is not None and (not isinstance(value, str) or not _TIME_RE.match(value)):
            errors.append(f"{where}.{key} must be null or HH:MM (24-hour)")
    if (open_from is None) != (open_until is None):
        errors.append(f"{where}: give both open_from and open_until, or neither")
    elif open_from is not None and access != "code_after_hours":
        errors.append(f"{where}: open_from and open_until are the unlocked hours of a "
                      "code_after_hours chapel")
    elif open_from is not None and open_from == open_until:
        errors.append(f"{where}: open_from and open_until must differ")
    return errors


def _note_errors(note: Any, where: str) -> list[str]:
    if note is None:
        return []
    if not isinstance(note, str):
        return [f"{where}.note must be null or a string"]
    private = private_detail(note)
    return [f"{where}.note {private}"] if private else []


# ── Keeping people's details out of notes ───────────────────────────────────
# A note is shown on the site as written, so it never holds a phone number, an
# email address or a door code (docs/believed-schedules.md, "Notes"). Names
# can't be told apart from a chapel's or a saint's: seed review is their check.
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]\d{4}(?!\d)")
# "code 4321", "code: 12#", "PIN is 0420", "combination 1-2-3", "4321#": three
# digits or more after the word, or digits ending in # or *. "code needed, 2
# doors" and "Room #205" name none.
_CODE_RE = re.compile(
    r"\b(?:code|pin|combination|keypad|passcode)\b\W{0,3}(?:\w+\W{1,3}){0,2}?"
    r"(?:\d(?:[\s-]?\d){2,}|\d+\s?[#*])"
    r"|\b\d{3,}#",
    re.IGNORECASE,
)


# Clock times and round-the-clock hours, taken out before looking for a code:
# "code needed 9 PM-6 AM" and "access code required, 24/7" name none.
_CLOCK_RE = re.compile(
    r"\b\d{1,2}(?::\d{2})?\s{0,3}(?:a\.?\s?m\b\.?|p\.?\s?m\b\.?|noon|midnight)"
    r"|\b\d{1,2}:\d{2}\b"
    r"|\b24\s?(?:/\s?7|-?\s?(?:hours?|hrs?)\b)",
    re.IGNORECASE,
)


def _holds_email(text: str) -> bool:
    """Whether `text` holds `name@domain.tld`.

    Read from each "@", without a regular expression: a search for the whole
    address would try every character as the start of its name.
    """
    at = text.find("@")
    while at != -1:
        named = at > 0 and (text[at - 1].isalnum() or text[at - 1] in "_.+-")
        end = at + 1
        while end < len(text) and (text[end].isalnum() or text[end] in "_.-"):
            end += 1
        # The domain: a label, a dot and another label ("example.org").
        label, dot, rest = text[at + 1:end].partition(".")
        if named and label and dot and rest[:1] not in ("", "."):
            return True
        at = text.find("@", at + 1)
    return False


def private_detail(text: str) -> str | None:
    """What in `text` looks like a person's contact or a door code, as an error's tail."""
    if _holds_email(text):
        return "holds an email address; notes never carry contact details"
    if _PHONE_RE.search(text):
        return "holds a phone number; notes never carry contact details"
    if _CODE_RE.search(_CLOCK_RE.sub(" ", text)):
        return "holds what looks like a door code; notes never carry one"
    return None


def validate_entry(entry: Any, where: str) -> list[str]:
    """Every reason `entry` is not a schedule entry (empty when it is one)."""
    if not isinstance(entry, dict):
        return [f"{where} must be an object"]
    errors = check_keys(entry, ENTRY_KEYS, where, may_lack=ENTRY_KEYS_ADDED_LATER)
    if errors:
        return errors
    return entry_value_errors(entry, where)


# ── Canonical forms ─────────────────────────────────────────────────────────
def sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    """Sorted keys, no whitespace: the same value always hashes the same."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def normalize_as_of(value: str) -> str:
    """A seed's `as_of` in the form `fetched_at` is stored in, so the two compare as text.

    Takes an ISO time (`Z` or an offset; none means UTC) or a date, which
    means the end of that day: everything fetched that day is in the seed.
    """
    text = value.strip()
    try:
        if len(text) == 10:
            moment = datetime.combine(date.fromisoformat(text), time(23, 59, 59), UTC)
        else:
            moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=UTC)
    except ValueError as exc:
        raise ValueError(f"as_of must be an ISO date or time, not {value!r}") from exc
    return moment.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ── A classifier's flat events ──────────────────────────────────────────────
def _hhmm(raw: Any) -> str | None:
    minutes = time_to_minutes(raw) if isinstance(raw, str) else None
    return None if minutes is None else f"{minutes // 60:02d}:{minutes % 60:02d}"


def _day(raw: Any) -> str | None:
    if not isinstance(raw, str) or len(raw.strip()) < 2:
        return None
    prefix = raw.strip().lower()[:3]
    return next((d for d in DAYS if d.lower().startswith(prefix)), None)


def _weeks(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    weeks = {str(w).strip().lower() for w in raw}
    return [w for w in WEEKS_OF_MONTH if w in weeks]


def _season(ev: dict[str, Any]) -> dict[str, int | None] | None:
    """A season from the flat `season_*` fields the pipeline adds in schema v2, if any."""
    start, end = ev.get("season_start_month"), ev.get("season_end_month")
    if not (isinstance(start, int) and isinstance(end, int)):
        return None
    if not (1 <= start <= 12 and 1 <= end <= 12):
        return None
    start_day, end_day = ev.get("season_start_day"), ev.get("season_end_day")
    return {
        "start_month": start,
        "start_day": start_day if isinstance(start_day, int) else None,
        "end_month": end,
        "end_day": end_day if isinstance(end_day, int) else None,
    }


def gemini_rows(events: list[Any]) -> list[dict[str, Any]]:
    """Gemini's flat events in the label's row shape, keeping the raw strings.

    `problems` lists what could not be read (an unparseable time, say), so the
    labeler sees it instead of the row silently vanishing.
    """
    out = []
    for i, ev in enumerate(events):
        if not isinstance(ev, dict):
            continue
        event_type = ev.get("type", ev.get("event_type"))
        kind = ev.get("kind", ev.get("event_kind"))
        if kind == CONTINUOUS:
            out.append(_continuous_row(i, ev, event_type))
            continue
        weekly = kind == "weekly"
        weeks, exclude_weeks = canonical_weeks(
            _weeks(ev.get("weeks_of_month")), ev.get("exclude_weeks") is True,
        ) if weekly else ([], False)
        row = {
            "id": f"g{i}",
            "church_slug": ev.get("church_slug") if isinstance(ev.get("church_slug"), str) else "",
            "event_type": event_type if event_type in EVENT_TYPES else None,
            "event_kind": kind if kind in EVENT_KINDS else None,
            "day_of_week": _day(ev.get("day_of_week")) if weekly else None,
            "date": None if weekly else normalize_event_date(ev.get("date")),
            "start_time": _hhmm(ev.get("start_time")),
            "end_time": _hhmm(ev.get("end_time")),
            "cancelled": bool(ev.get("cancelled", False)),
            "weeks_of_month": weeks,
            "exclude_weeks": exclude_weeks,
            "season": _season(ev) if weekly else None,
            "page_number": ev.get("page_number") if isinstance(ev.get("page_number"), int) else None,
            "note": ev.get("note") if isinstance(ev.get("note"), str) and ev["note"].strip() else None,
            "raw": {
                k: ev.get(k) for k in ("day_of_week", "date", "start_time", "end_time")
                if ev.get(k) is not None
            },
        }
        problems = []
        if row["event_type"] is None:
            problems.append(f"unknown type {event_type!r}")
        if row["event_kind"] is None:
            problems.append(f"unknown kind {kind!r}")
        elif weekly and row["day_of_week"] is None:
            problems.append(f"unreadable day {ev.get('day_of_week')!r}")
        elif not weekly and row["date"] is None:
            problems.append(f"unreadable date {ev.get('date')!r}")
        if row["start_time"] is None:
            problems.append(f"unreadable start time {ev.get('start_time')!r}")
        if ev.get("end_time") and row["end_time"] is None:
            problems.append(f"unreadable end time {ev.get('end_time')!r}")
        row["problems"] = problems
        out.append(row)
    return out


def _continuous_row(i: int, ev: dict[str, Any], event_type: Any) -> dict[str, Any]:
    """A continuous chapel from a classifier, in the label's row shape (see `gemini_rows`)."""
    access = ev.get("access")
    hours = {key: _hhmm(ev.get(key)) for key in ("open_from", "open_until")}
    problems = []
    if event_type != "adoration":
        problems.append(f"a continuous entry must be adoration, not {event_type!r}")
    if access not in ACCESS_KINDS:
        problems.append(f"unknown access {access!r}")
    for key, value in hours.items():
        if ev.get(key) and value is None:
            problems.append(f"unreadable {key} {ev.get(key)!r}")
    note = ev.get("note")
    return {
        "id": f"g{i}",
        "church_slug": ev.get("church_slug") if isinstance(ev.get("church_slug"), str) else "",
        "event_type": "adoration",
        "event_kind": CONTINUOUS,
        "day_of_week": None,
        "date": None,
        "start_time": None,
        "end_time": None,
        "cancelled": False,
        "weeks_of_month": [],
        "exclude_weeks": False,
        "season": None,
        "page_number": ev.get("page_number") if isinstance(ev.get("page_number"), int) else None,
        "note": note if isinstance(note, str) and note.strip() else None,
        "access": access if access in ACCESS_KINDS else None,
        **hours,
        "raw": {k: ev.get(k) for k in ("open_from", "open_until") if ev.get(k) is not None},
        "problems": problems,
    }


_FACEBOOK_HOSTS = ("facebook.com", "fb.com", "fb.me")


def source_platform(url: str) -> str:
    """`facebook` for a Facebook address, else `website`."""
    host = (urlsplit(url).hostname or "").lower()
    return FACEBOOK if any(host == h or host.endswith(f".{h}") for h in _FACEBOOK_HOSTS) \
        else WEBSITE


# A Facebook address's first path segment when it names no page: sharing links, the
# page plugin (whose `href` names the page) and the like.
_FACEBOOK_NOT_PAGES = frozenset({
    "", "sharer", "sharer.php", "share", "share.php", "dialog", "plugins", "tr", "login",
    "login.php", "home.php", "watch", "events", "hashtag", "help", "policies", "privacy",
    "legal", "photo", "photo.php", "story.php", "permalink.php", "reel", "reels", "search",
    "l.php", "media", "stories", "notes", "photos", "videos",
})
# A page's id at the end of a path segment: `/p/St-Rita-Parish-100064512345678/`.
_FACEBOOK_TRAILING_ID = re.compile(r"-(\d+)$")


def facebook_page(url: str) -> str | None:
    """The Facebook page `url` is on, as a canonical address, or None when it names none.

    Every address on one page names it alike: `facebook.com/StRita`, `m.facebook.com/
    strita/posts/1` and `facebook.com/profile.php?id=1` with its `id`, as do `/p/St-Rita-1`,
    `/people/St-Rita/1` and `/pages/category/Church/St-Rita-1`. A page plugin's address
    names the page in its `href`. One under `/p/`, `/people/` or `/pages/` with no id
    names none that can be told apart from another's.
    """
    if source_platform(url) != FACEBOOK:
        return None
    parts = urlsplit(url)
    query = parse_qs(parts.query)
    segments = [unquote(s) for s in parts.path.split("/") if s]
    head = segments[0].lower() if segments else ""
    if head == "plugins" and query.get("href"):
        return facebook_page(query["href"][0])
    if head == "profile.php" and query.get("id"):
        return f"https://www.facebook.com/profile.php?id={query['id'][0]}"
    if head == "pg" and len(segments) >= 2:
        return f"https://www.facebook.com/{segments[1].lower()}"
    if head in ("pages", "people", "p"):
        # By the page's id: a segment of its own (/pages/Name/123, /people/Name/123), or
        # the end of its name (/p/Name-123, /pages/category/Kind/Name-123).
        rest = segments[1:4]
        page_id = next((s for s in rest if s.isdigit()), None) or next(
            (m.group(1) for s in rest if (m := _FACEBOOK_TRAILING_ID.search(s))), None)
        return None if page_id is None else f"https://www.facebook.com/profile.php?id={page_id}"
    if head == "groups" and len(segments) >= 2:
        return f"https://www.facebook.com/groups/{segments[1].lower()}"
    if head in _FACEBOOK_NOT_PAGES:
        return None
    return f"https://www.facebook.com/{head}"
