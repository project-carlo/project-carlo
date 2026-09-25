"""Verify that frontend snapshots stay similar enough between updates."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from pdf_extract.extract_frontend_db import DEST_SNAPSHOT, SnapshotFormatError, read_snapshot

LOGGER = logging.getLogger(__name__)

CURRENT_SNAPSHOT_PATH = DEST_SNAPSHOT
PREVIOUS_SNAPSHOT_PATH = DEST_SNAPSHOT.with_name(f"{DEST_SNAPSHOT.name}.previous")

EVENT_DELTA_THRESHOLD_PCT = 10.0
WEEKLY_MATCH_THRESHOLD_PCT = 90.0

WeeklyKey = tuple[int, str, str, int]
Tables = dict[str, list[dict[str, Any]]]


def _load(path: Path) -> Tables:
    if not path.exists():
        raise FileNotFoundError(f"Snapshot not found: {path}")
    try:
        return read_snapshot(path.read_bytes())
    except SnapshotFormatError as exc:
        raise SnapshotFormatError(f"{path}: {exc}") from exc


def _weekly_keys(tables: Tables) -> set[WeeklyKey]:
    return {
        (int(e["church_id"]), str(e["event_type"]), e["day_of_week"] or "", int(e["start_time"]))
        for e in tables["events"]
        if str(e["event_kind"]).lower() == "weekly"
    }


def verify_frontend_snapshot(
    current: Path = CURRENT_SNAPSHOT_PATH,
    previous: Path = PREVIOUS_SNAPSHOT_PATH,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        current_tables = _load(current)
        previous_tables = _load(previous)
    except FileNotFoundError as exc:
        errors.append(str(exc))
        return {
            "passed": False,
            "errors": errors,
            "current_snapshot_path": str(current),
            "previous_snapshot_path": str(previous),
        }

    current_church_count = len(current_tables["churches"])
    previous_church_count = len(previous_tables["churches"])
    churches_equal = current_church_count == previous_church_count

    current_event_count = len(current_tables["events"])
    previous_event_count = len(previous_tables["events"])
    if previous_event_count > 0:
        event_delta_pct = abs(current_event_count - previous_event_count) / previous_event_count * 100.0
    else:
        event_delta_pct = 0.0 if current_event_count == 0 else 100.0
    events_within_threshold = event_delta_pct <= EVENT_DELTA_THRESHOLD_PCT

    current_weekly_keys = _weekly_keys(current_tables)
    previous_weekly_keys = _weekly_keys(previous_tables)
    weekly_matches = len(current_weekly_keys & previous_weekly_keys)
    if previous_weekly_keys:
        weekly_match_pct = weekly_matches / len(previous_weekly_keys) * 100.0
    else:
        weekly_match_pct = 100.0 if not current_weekly_keys else 0.0
    weekly_match_pass = weekly_match_pct >= WEEKLY_MATCH_THRESHOLD_PCT

    passed = churches_equal and events_within_threshold and weekly_match_pass
    result = {
        "passed": passed,
        "thresholds": {
            "church_count_must_match_exactly": True,
            "event_delta_max_pct": EVENT_DELTA_THRESHOLD_PCT,
            "weekly_match_min_pct": WEEKLY_MATCH_THRESHOLD_PCT,
        },
        "current_snapshot_path": str(current),
        "previous_snapshot_path": str(previous),
        "churches": {
            "current": current_church_count,
            "previous": previous_church_count,
            "passed": churches_equal,
        },
        "events": {
            "current": current_event_count,
            "previous": previous_event_count,
            "delta_pct": round(event_delta_pct, 2),
            "passed": events_within_threshold,
        },
        "weekly_events": {
            "current_count": len(current_weekly_keys),
            "previous_count": len(previous_weekly_keys),
            "matching_count": weekly_matches,
            "match_pct": round(weekly_match_pct, 2),
            "passed": weekly_match_pass,
        },
        "errors": errors,
    }

    LOGGER.info(
        "frontend snapshot verification: passed=%s | events delta=%.2f%% | weekly match=%.2f%%",
        passed,
        event_delta_pct,
        weekly_match_pct,
    )
    return result
