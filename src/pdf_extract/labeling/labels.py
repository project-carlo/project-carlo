"""Ground-truth label files: one JSON file per bulletin, committed to git.

A label records what a person read off one bulletin PDF: every Mass,
Confession and Adoration it lists, in the shape of the pipeline's event rows
plus the recurrence qualifiers `weeks_of_month` and `season` (the same tokens
and ranges `schedule_pattern` uses), so ground truth can be scored against any
classifier later.

An event can be marked optional when it is a judgment call whether it belongs
in the schedule at all: `optional` is null for a required event, or the
preferred answer, `include` or `exclude`. Scoring leaves optional events out of the
headline numbers and reports how often a classifier made the preferred choice.

Files live at `data/labels/<parish_slug>/<content_hash>.json`. The slug and
hash come from HTTP requests, so both are checked against strict patterns and
the resolved path must stay inside the labels directory.
"""

from __future__ import annotations

import json
import os
import re
import threading
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.paths import DATA_DIR
from pdf_extract.storage import utc_now_iso

SCHEMA_VERSION = 1
LABELS_DIR = DATA_DIR / "labels"

STATUSES = ("in_progress", "done", "skipped")
FLAGS = ("wrong_bulletin", "unreadable", "no_schedule", "church_missing", "conflicting_info")
EVENT_TYPES = ("mass", "confession", "adoration")
EVENT_KINDS = ("weekly", "specific_date")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
WEEKS_OF_MONTH = ("first", "second", "third", "fourth", "fifth", "last")
ORIGINS = ("human", "gemini", "gemini-edited")
OPTIONAL_PREFERENCES = ("include", "exclude")

# February has 29: a season boundary recurs every year, leap years included.
DAYS_IN_MONTH = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

LABEL_KEYS = (
    "schema_version", "parish_slug", "content_hash", "source_url", "status", "flags",
    "published_date", "note", "labeler", "seconds_spent", "updated_at", "events",
)
EVENT_KEYS = (
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "weeks_of_month", "season", "page_number", "note", "origin",
    "optional",
)
# Keys a label written before they existed may lack; a missing one reads as null.
EVENT_KEYS_ADDED_LATER = ("optional",)
SEASON_KEYS = ("start_month", "start_day", "end_month", "end_day")

_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_write_lock = threading.Lock()


class LabelError(ValueError):
    """A label, slug or hash that must not be written."""


def is_valid_slug(value: Any) -> bool:
    return isinstance(value, str) and len(value) <= 120 and bool(_SLUG_RE.match(value))


def is_valid_hash(value: Any) -> bool:
    return isinstance(value, str) and bool(_HASH_RE.match(value))


def label_path(parish_slug: str, content_hash: str, labels_dir: Path = LABELS_DIR) -> Path:
    """Where a bulletin's label lives; raises LabelError for anything unsafe."""
    if not is_valid_slug(parish_slug):
        raise LabelError(f"Invalid parish slug: {parish_slug!r}")
    if not is_valid_hash(content_hash):
        raise LabelError(f"Invalid content hash: {content_hash!r}")
    root = labels_dir.resolve()
    path = (root / parish_slug / f"{content_hash}.json").resolve()
    if not path.is_relative_to(root):
        raise LabelError(f"Label path escapes {labels_dir}: {path}")
    return path


# ── Validation ──────────────────────────────────────────────────────────────
def _is_iso_date(value: Any) -> bool:
    if not isinstance(value, str) or not _DATE_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _check_keys(
    obj: dict[str, Any], expected: tuple[str, ...], where: str, *, may_lack: tuple[str, ...] = (),
) -> list[str]:
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
    errors = _check_keys(season, SEASON_KEYS, f"{where}.season")
    if errors:
        return errors
    for edge in ("start", "end"):
        month = season[f"{edge}_month"]
        day = season[f"{edge}_day"]
        if not _is_int(month) or not 1 <= month <= 12:
            errors.append(f"{where}.season.{edge}_month must be 1-12")
            continue
        if day is not None and (not _is_int(day) or not 1 <= day <= DAYS_IN_MONTH[month - 1]):
            errors.append(f"{where}.season.{edge}_day must be null or a day of month {month}")
    return errors


def _validate_event(event: Any, where: str) -> list[str]:
    if not isinstance(event, dict):
        return [f"{where} must be an object"]
    errors = _check_keys(event, EVENT_KEYS, where, may_lack=EVENT_KEYS_ADDED_LATER)
    if errors:
        return errors

    if not is_valid_slug(event["church_slug"]):
        errors.append(f"{where}.church_slug must be a church slug")
    if event["event_type"] not in EVENT_TYPES:
        errors.append(f"{where}.event_type must be one of {', '.join(EVENT_TYPES)}")
    kind = event["event_kind"]
    if kind not in EVENT_KINDS:
        errors.append(f"{where}.event_kind must be one of {', '.join(EVENT_KINDS)}")
    elif kind == "weekly":
        if event["day_of_week"] not in DAYS:
            errors.append(f"{where}.day_of_week must be a weekday name for a weekly event")
        if event["date"] is not None:
            errors.append(f"{where}.date must be null for a weekly event")
    else:
        if event["day_of_week"] is not None:
            errors.append(f"{where}.day_of_week must be null for a dated event")
        if not _is_iso_date(event["date"]):
            errors.append(f"{where}.date must be YYYY-MM-DD for a dated event")

    if not isinstance(event["start_time"], str) or not _TIME_RE.match(event["start_time"]):
        errors.append(f"{where}.start_time must be HH:MM (24-hour)")
    end = event["end_time"]
    if end is not None and (not isinstance(end, str) or not _TIME_RE.match(end)):
        errors.append(f"{where}.end_time must be null or HH:MM (24-hour)")
    if not isinstance(event["cancelled"], bool):
        errors.append(f"{where}.cancelled must be true or false")

    weeks = event["weeks_of_month"]
    if not isinstance(weeks, list) or any(w not in WEEKS_OF_MONTH for w in weeks):
        errors.append(f"{where}.weeks_of_month must be a list of {', '.join(WEEKS_OF_MONTH)}")
    elif len(set(weeks)) != len(weeks):
        errors.append(f"{where}.weeks_of_month has duplicates")
    elif weeks and kind == "specific_date":
        errors.append(f"{where}.weeks_of_month applies to weekly events only")
    errors.extend(_validate_season(event["season"], where))
    if event["season"] is not None and kind == "specific_date":
        errors.append(f"{where}.season applies to weekly events only")

    page = event["page_number"]
    if page is not None and (not _is_int(page) or page < 1):
        errors.append(f"{where}.page_number must be null or a positive integer")
    if event["note"] is not None and not isinstance(event["note"], str):
        errors.append(f"{where}.note must be null or a string")
    if event["origin"] not in ORIGINS:
        errors.append(f"{where}.origin must be one of {', '.join(ORIGINS)}")
    if event.get("optional") not in (None, *OPTIONAL_PREFERENCES):
        errors.append(f"{where}.optional must be null, {' or '.join(OPTIONAL_PREFERENCES)}")
    return errors


# A schedule entry is a label event without the keys that describe one reading
# of one bulletin: a seed (`pdf_extract.seeding`) holds entries in this shape.
ENTRY_KEYS = tuple(k for k in EVENT_KEYS if k not in ("page_number", "origin", "optional"))


def validate_entry(entry: Any, where: str) -> list[str]:
    """Every reason `entry` is not a label event minus page, origin and optional."""
    if not isinstance(entry, dict):
        return [f"{where} must be an object"]
    errors = _check_keys(entry, ENTRY_KEYS, where)
    if errors:
        return errors
    return _validate_event({**entry, "page_number": None, "origin": "human"}, where)


def validate_label(label: Any) -> list[str]:
    """Every reason `label` is not a valid schema-version-1 label (empty when valid)."""
    if not isinstance(label, dict):
        return ["label must be a JSON object"]
    errors = _check_keys(label, LABEL_KEYS, "label")
    if errors:
        return errors
    if label["schema_version"] != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not is_valid_slug(label["parish_slug"]):
        errors.append("parish_slug is not a valid slug")
    if not is_valid_hash(label["content_hash"]):
        errors.append("content_hash is not a SHA-256 hex digest")
    if not isinstance(label["source_url"], str):
        errors.append("source_url must be a string")
    if label["status"] not in STATUSES:
        errors.append(f"status must be one of {', '.join(STATUSES)}")

    flags = label["flags"]
    if not isinstance(flags, dict):
        errors.append("flags must be an object")
    else:
        errors.extend(_check_keys(flags, FLAGS, "flags"))
        errors.extend(
            f"flags.{k} must be true or false"
            for k in FLAGS if k in flags and not isinstance(flags[k], bool)
        )

    if label["published_date"] is not None and not _is_iso_date(label["published_date"]):
        errors.append("published_date must be null or YYYY-MM-DD")
    for key in ("note", "labeler", "updated_at"):
        if not isinstance(label[key], str):
            errors.append(f"{key} must be a string")
    if not _is_int(label["seconds_spent"]) or label["seconds_spent"] < 0:
        errors.append("seconds_spent must be a non-negative integer")

    events = label["events"]
    if not isinstance(events, list):
        errors.append("events must be a list")
    else:
        for i, event in enumerate(events):
            errors.extend(_validate_event(event, f"events[{i}]"))
    return errors


# ── Reading and writing ─────────────────────────────────────────────────────
def empty_label(parish_slug: str, content_hash: str, source_url: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "parish_slug": parish_slug,
        "content_hash": content_hash,
        "source_url": source_url,
        "status": "in_progress",
        "flags": {flag: False for flag in FLAGS},
        "published_date": None,
        "note": "",
        "labeler": "",
        "seconds_spent": 0,
        "updated_at": "",
        "events": [],
    }


def read_label(
    parish_slug: str, content_hash: str, labels_dir: Path = LABELS_DIR,
) -> dict[str, Any] | None:
    path = label_path(parish_slug, content_hash, labels_dir)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None


def write_label(
    label: dict[str, Any],
    *,
    parish_slug: str,
    content_hash: str,
    source_url: str,
    labels_dir: Path = LABELS_DIR,
) -> dict[str, Any]:
    """Validate and save a label, stamping `updated_at`. Returns what was written.

    The slug, hash and source URL come from the bulletin being labelled, not
    from the request body, so a label can only ever describe that bulletin.
    """
    path = label_path(parish_slug, content_hash, labels_dir)
    if not isinstance(label, dict):
        raise LabelError("label must be a JSON object")
    if label.get("parish_slug") != parish_slug or label.get("content_hash") != content_hash:
        raise LabelError("label parish_slug/content_hash do not match the bulletin")
    saved = {key: label.get(key) for key in LABEL_KEYS}
    saved["source_url"] = source_url
    saved["updated_at"] = utc_now_iso()
    unknown = sorted(k for k in label if k not in LABEL_KEYS)
    errors = validate_label(saved) + ([f"label: unknown {', '.join(unknown)}"] if unknown else [])
    if errors:
        raise LabelError("; ".join(errors))

    data = json.dumps(saved, indent=2, ensure_ascii=False) + "\n"
    with _write_lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}-{threading.get_ident()}")
        tmp.write_text(data, encoding="utf-8")
        tmp.replace(path)
    return saved


def label_statuses(labels_dir: Path = LABELS_DIR) -> dict[tuple[str, str], str]:
    """(parish slug, content hash) -> status, for every readable label file."""
    out: dict[tuple[str, str], str] = {}
    if not labels_dir.is_dir():
        return out
    for path in labels_dir.glob("*/*.json"):
        parish_slug, content_hash = path.parent.name, path.stem
        if not (is_valid_slug(parish_slug) and is_valid_hash(content_hash)):
            continue
        try:
            status = json.loads(path.read_text(encoding="utf-8")).get("status")
        except (OSError, ValueError, AttributeError):
            continue
        if status in STATUSES:
            out[(parish_slug, content_hash)] = status
    return out
