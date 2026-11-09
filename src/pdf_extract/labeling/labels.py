"""Ground-truth label files: one JSON file per bulletin, committed to git.

A label records what a person read off one bulletin PDF: every Mass,
Confession and Adoration it lists, each a schedule entry (`pdf_extract.model`,
which holds the vocabulary) plus the page it was read on and where it came
from, so ground truth can be scored against any classifier later.

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
import threading
from pathlib import Path
from typing import Any

from pdf_extract.model import (
    ENTRY_KEYS_ADDED_LATER,
    check_keys,
    entry_value_errors,
    is_int,
    is_iso_date,
    is_valid_hash,
    is_valid_slug,
)
from pdf_extract.paths import DATA_DIR
from pdf_extract.storage import utc_now_iso

SCHEMA_VERSION = 1
LABELS_DIR = DATA_DIR / "labels"

STATUSES = ("in_progress", "done", "skipped")
FLAGS = ("wrong_bulletin", "unreadable", "no_schedule", "church_missing", "conflicting_info")
ORIGINS = ("human", "gemini", "gemini-edited")
OPTIONAL_PREFERENCES = ("include", "exclude")

LABEL_KEYS = (
    "schema_version", "parish_slug", "content_hash", "source_url", "status", "flags",
    "published_date", "note", "labeler", "seconds_spent", "updated_at", "events",
)
EVENT_KEYS = (
    "church_slug", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "weeks_of_month", "exclude_weeks", "season", "page_number",
    "note", "origin", "optional",
)
# Keys a label written before they existed may lack; a missing one reads as
# null (`exclude_weeks`: false).
EVENT_KEYS_ADDED_LATER = (*ENTRY_KEYS_ADDED_LATER, "optional")

_write_lock = threading.Lock()


class LabelError(ValueError):
    """A label, slug or hash that must not be written."""


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
def _validate_event(event: Any, where: str) -> list[str]:
    if not isinstance(event, dict):
        return [f"{where} must be an object"]
    errors = check_keys(event, EVENT_KEYS, where, may_lack=EVENT_KEYS_ADDED_LATER)
    if errors:
        return errors
    errors = entry_value_errors(event, where)
    page = event["page_number"]
    if page is not None and (not is_int(page) or page < 1):
        errors.append(f"{where}.page_number must be null or a positive integer")
    if event["origin"] not in ORIGINS:
        errors.append(f"{where}.origin must be one of {', '.join(ORIGINS)}")
    if event.get("optional") not in (None, *OPTIONAL_PREFERENCES):
        errors.append(f"{where}.optional must be null, {' or '.join(OPTIONAL_PREFERENCES)}")
    return errors


def validate_label(label: Any) -> list[str]:
    """Every reason `label` is not a valid schema-version-1 label (empty when valid)."""
    if not isinstance(label, dict):
        return ["label must be a JSON object"]
    errors = check_keys(label, LABEL_KEYS, "label")
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
        errors.extend(check_keys(flags, FLAGS, "flags"))
        errors.extend(
            f"flags.{k} must be true or false"
            for k in FLAGS if k in flags and not isinstance(flags[k], bool)
        )

    if label["published_date"] is not None and not is_iso_date(label["published_date"]):
        errors.append("published_date must be null or YYYY-MM-DD")
    for key in ("note", "labeler", "updated_at"):
        if not isinstance(label[key], str):
            errors.append(f"{key} must be a string")
    if not is_int(label["seconds_spent"]) or label["seconds_spent"] < 0:
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
