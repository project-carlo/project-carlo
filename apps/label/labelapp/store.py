"""Persistence for human labels.

Ground truth is the one artifact here that cannot be regenerated, so it is kept
as a single human-readable JSON file, `data/labels.json`, committed alongside
the other pipeline data. Each entry is keyed by bulletin source URL and records
both what the labeler accepted and what they rejected: the rejections are as
valuable as the acceptances, since a confirmed-wrong candidate is a scored false
positive for whichever run proposed it.

Everything arriving from the browser is re-normalized and re-keyed here rather
than trusted, so a stale or hand-edited payload cannot write an event whose
stored `key_id` disagrees with its own fields.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from pdf_extract.storage import DATA_DIR, utc_now_iso

from labelapp import events as ev

#: Resolved on every call rather than bound as a default argument, so tests
#: and callers can point the app at a different file.
LABELS_PATH = DATA_DIR / "labels.json"

STATUS_IN_PROGRESS = "in_progress"
STATUS_COMPLETE = "complete"
STATUS_SKIPPED = "skipped"
VALID_STATUSES = (STATUS_IN_PROGRESS, STATUS_COMPLETE, STATUS_SKIPPED)

ORIGIN_MODEL = "model"
ORIGIN_HUMAN = "human"


def load_labels(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """All labels, keyed by bulletin source URL. Missing file means none yet."""
    path = path or LABELS_PATH
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError(f"{path} must contain a JSON object keyed by bulletin URL")
    return {key: value for key, value in raw.items() if isinstance(value, dict)}


def save_labels(labels: dict[str, dict[str, Any]], path: Path | None = None) -> None:
    """Write all labels atomically.

    Ground truth is expensive to reproduce, so the file is never truncated in
    place: a crash mid-write would otherwise cost every label collected so far.
    """
    path = path or LABELS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = {key: labels[key] for key in sorted(labels)}
    payload = json.dumps(ordered, indent=2, ensure_ascii=False) + "\n"

    handle = tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=path.name, suffix=".tmp", delete=False,
    )
    try:
        with handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(handle.name, path)
    except BaseException:
        Path(handle.name).unlink(missing_ok=True)
        raise


def _clean_event(raw: Any, *, default_origin: str) -> dict[str, Any] | None:
    """Normalize one labeled event, or None if it lacks the fields to be one."""
    if not isinstance(raw, dict):
        return None
    event = ev.normalize_event(raw)
    if not event["church_slug"] or not event["event_type"] or not event["start_time"]:
        return None
    if event["event_kind"] not in ("weekly", "specific_date"):
        return None

    origin = raw.get("origin")
    sources = [name for name in raw.get("sources") or [] if isinstance(name, str)]
    note = raw.get("note")

    event["key_id"] = ev.event_id(event)
    event["origin"] = origin if origin in (ORIGIN_MODEL, ORIGIN_HUMAN) else default_origin
    event["sources"] = sources
    event["note"] = note.strip() if isinstance(note, str) and note.strip() else None
    page_number = raw.get("page_number")
    event["page_number"] = page_number if isinstance(page_number, int) else None
    return event


def _clean_events(raw: Any) -> list[dict[str, Any]]:
    """Normalize a list of submitted events, dropping any that are unusable."""
    if not isinstance(raw, list):
        return []
    cleaned: list[dict[str, Any]] = []
    for row in raw:
        event = _clean_event(row, default_origin=ORIGIN_MODEL)
        if event is not None:
            cleaned.append(event)
    return cleaned


def _dedupe(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep the first row per key_id; a set has no room for the same event twice."""
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for row in rows:
        if row["key_id"] in seen:
            continue
        seen.add(row["key_id"])
        unique.append(row)
    return unique


def normalize_label(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and canonicalize a label submitted by the app.

    Raises ValueError when the payload could not identify a bulletin.
    """
    source_url = payload.get("bulletin_source_url")
    if not isinstance(source_url, str) or not source_url:
        raise ValueError("bulletin_source_url is required")

    status = payload.get("status")
    if status not in VALID_STATUSES:
        status = STATUS_IN_PROGRESS

    accepted = _dedupe(_clean_events(payload.get("events")))
    accepted_ids = {row["key_id"] for row in accepted}
    # An event cannot be both ground truth and a confirmed miss; acceptance wins.
    rejected = [
        row
        for row in _dedupe(_clean_events(payload.get("rejected")))
        if row["key_id"] not in accepted_ids
    ]

    notes = payload.get("notes")
    skip_reason = payload.get("skip_reason")
    seconds_spent = payload.get("seconds_spent")

    return {
        "bulletin_source_url": source_url,
        "parish_slug": str(payload.get("parish_slug") or ""),
        "content_hash": (
            payload["content_hash"] if isinstance(payload.get("content_hash"), str) else None
        ),
        "status": status,
        "wrong_bulletin": bool(payload.get("wrong_bulletin", False)),
        "published_date": (
            payload["published_date"] if isinstance(payload.get("published_date"), str) else None
        ),
        "events": accepted,
        "rejected": rejected,
        "notes": notes.strip() if isinstance(notes, str) and notes.strip() else None,
        "skip_reason": (
            skip_reason.strip()
            if isinstance(skip_reason, str) and skip_reason.strip()
            else None
        ),
        "labeler": str(payload.get("labeler") or "").strip() or None,
        "labeled_at": utc_now_iso(),
        "seconds_spent": (
            int(seconds_spent) if isinstance(seconds_spent, (int, float)) and seconds_spent >= 0
            else None
        ),
    }


def put_label(payload: dict[str, Any], path: Path | None = None) -> dict[str, Any]:
    """Normalize and persist one label. Returns the stored document."""
    label = normalize_label(payload)
    labels = load_labels(path)
    labels[label["bulletin_source_url"]] = label
    save_labels(labels, path)
    return label


def delete_label(source_url: str, path: Path | None = None) -> bool:
    """Drop a label. Returns False when there was nothing to drop."""
    labels = load_labels(path)
    if source_url not in labels:
        return False
    del labels[source_url]
    save_labels(labels, path)
    return True


def decided_ids(label: dict[str, Any] | None) -> set[str]:
    """key_ids the labeler has ruled on, either way."""
    if not label:
        return set()
    return {row["key_id"] for row in label.get("events") or []} | {
        row["key_id"] for row in label.get("rejected") or []
    }


def accepted_keys(label: dict[str, Any]) -> set[tuple[Any, ...]]:
    """Ground-truth event keys for one bulletin, for scoring."""
    from pdf_extract.compare import event_key

    return {event_key(row) for row in label.get("events") or []}
