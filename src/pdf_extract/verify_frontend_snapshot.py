"""Verify that frontend snapshots stay similar enough between updates.

The gates compare the two snapshots read on one date (`schedule_diff`), for
every parish whatever its mode:

- the church count is unchanged, and the raw event count within ±10%;
- at least 90% of last time's recurring slots are still there, compared by
  their full meaning (times, weeks of the month, season, valid dates), with
  additions not making up for removals;
- no parish that showed at least 3 events shows none;
- no parish, and no church's Masses, Confessions or Adorations, lost at
  least 3 of its dates in the coming weeks and more than half of them.

A parish seeded this run is checked like any other, except that its local
losses don't hold the run when the seed is at least as recent as its current
bulletin's week: those are a reviewed schedule replacing an extracted one.

Bump GATE_POLICY_VERSION when a gate or threshold changes, so reports from
different policies aren't read as comparable.
"""

from __future__ import annotations

import logging
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.bulletin_week import nearest_sunday, parse_iso_date
from pdf_extract.extract_frontend_db import DEST_SNAPSHOT, SnapshotFormatError, read_snapshot
from pdf_extract.schedule_diff import WINDOW_DAYS, ComparisonError, compare, current_rows

LOGGER = logging.getLogger(__name__)

CURRENT_SNAPSHOT_PATH = DEST_SNAPSHOT
PREVIOUS_SNAPSHOT_PATH = DEST_SNAPSHOT.with_name(f"{DEST_SNAPSHOT.name}.previous")

# 1: weekday and start time only, extract-mode parish checks in the report.
# 2: full recurring meaning, both modes, local availability holds.
GATE_POLICY_VERSION = 2

EVENT_DELTA_THRESHOLD_PCT = 10.0
WEEKLY_MATCH_THRESHOLD_PCT = 90.0

# A parish that showed at least this many events and now shows none holds the
# run: far more often a wrong PDF or a failed extraction than a parish that
# really stopped listing anything.
PARISH_DROP_TO_ZERO_MIN_EVENTS = 3

# A parish losing more than this share of its events is called out as a
# warning, without holding the run.
PARISH_DROP_WARN_FRACTION = 0.5
PARISH_DROP_WARN_MIN_EVENTS = 6

# A parish, or one church's services of one type, that loses at least this
# many dates in the window, and more than this share of them, holds the run.
LOCAL_LOSS_MIN_DATES = 3
LOCAL_LOSS_MAX_FRACTION = 0.5
# The levels whose severe losses hold the run; a level left out is reported only.
LOCAL_LOSS_HOLD_LEVELS = ("parish", "church")

Tables = dict[str, list[dict[str, Any]]]


def _load(path: Path) -> Tables:
    if not path.exists():
        raise FileNotFoundError(f"Snapshot not found: {path}")
    try:
        return read_snapshot(path.read_bytes())
    except SnapshotFormatError as exc:
        raise SnapshotFormatError(f"{path}: {exc}") from exc


def _gate(
    name: str, passed: bool, detail: str, *, threshold: Any = None,
    numerator: float | None = None, denominator: float | None = None,
    affected: list[Any] | None = None,
) -> dict[str, Any]:
    return {
        "name": name, "passed": passed, "detail": detail, "threshold": threshold,
        "numerator": numerator, "denominator": denominator, "affected": affected or [],
    }


def seed_is_current(seed_as_of: str | None, bulletin_week: str | None) -> bool:
    """Whether a seed is at least as recent as the parish's current bulletin's week.

    Weeks are compared as `bulletin_week` names them (the nearest Sunday), so a
    seed drafted from this week's bulletin counts as current.
    """
    seeded = parse_iso_date((seed_as_of or "")[:10])
    week = parse_iso_date(bulletin_week)
    if seeded is None:
        return False
    return week is None or nearest_sunday(seeded) >= week


def check_snapshots(
    current: Tables,
    previous: Tables,
    as_of: date,
    *,
    parish_slugs: dict[int, str] | None = None,
    seeded_this_run: dict[int, str] | None = None,
    window_days: int = WINDOW_DAYS,
) -> dict[str, Any]:
    """Every snapshot gate for two decoded snapshots, read on `as_of`.

    `parish_slugs` names parishes in the details (parish id otherwise).
    `seeded_this_run` is parish id -> its seed's as_of, for parishes that
    switched to update mode in this run.
    """
    slugs = parish_slugs or {}
    seeded = seeded_this_run or {}

    def name(parish_id: int | None) -> str:
        return slugs.get(parish_id) or f"parish #{parish_id}"

    errors: list[str] = []
    gates: list[dict[str, Any]] = []

    church_now, church_was = len(current["churches"]), len(previous["churches"])
    slugs_now = {str(c["slug"]) for c in current["churches"]}
    slugs_was = {str(c["slug"]) for c in previous["churches"]}
    gates.append(_gate(
        "Church count unchanged", church_now == church_was, f"{church_was} → {church_now}",
        threshold="equal", numerator=church_now, denominator=church_was,
        affected=[{"church_slug": s, "change": "removed"} for s in sorted(slugs_was - slugs_now)]
        + [{"church_slug": s, "change": "added"} for s in sorted(slugs_now - slugs_was)],
    ))

    # Raw rows, duplicates and all, but only those still to come on as_of: a
    # snapshot saved yesterday still has yesterday's dated rows.
    events_now = len(current_rows(current, as_of))
    events_was = len(current_rows(previous, as_of))
    if events_was > 0:
        delta_pct = abs(events_now - events_was) / events_was * 100.0
    else:
        delta_pct = 0.0 if events_now == 0 else 100.0
    gates.append(_gate(
        f"Total events within ±{EVENT_DELTA_THRESHOLD_PCT}%",
        delta_pct <= EVENT_DELTA_THRESHOLD_PCT,
        f"{events_was} → {events_now} ({round(delta_pct, 2)}%)",
        threshold=EVENT_DELTA_THRESHOLD_PCT, numerator=abs(events_now - events_was),
        denominator=events_was,
    ))

    try:
        comparison = compare(previous, current, as_of, window_days)
    except ComparisonError as exc:
        errors.append(f"Snapshot comparison failed: {exc}")
        comparison = None

    result: dict[str, Any] = {
        "as_of": as_of.isoformat(),
        "gate_policy_version": GATE_POLICY_VERSION,
        "thresholds": {
            "church_count_must_match_exactly": True,
            "event_delta_max_pct": EVENT_DELTA_THRESHOLD_PCT,
            "weekly_match_min_pct": WEEKLY_MATCH_THRESHOLD_PCT,
            "parish_drop_to_zero_min_events": PARISH_DROP_TO_ZERO_MIN_EVENTS,
            "local_loss_min_dates": LOCAL_LOSS_MIN_DATES,
            "local_loss_max_fraction": LOCAL_LOSS_MAX_FRACTION,
            "local_loss_hold_levels": list(LOCAL_LOSS_HOLD_LEVELS),
            "window_days": window_days,
        },
        "churches": {
            "current": church_now, "previous": church_was, "passed": church_now == church_was,
        },
        "events": {
            "current": events_now, "previous": events_was,
            "delta_pct": round(delta_pct, 2), "passed": delta_pct <= EVENT_DELTA_THRESHOLD_PCT,
        },
    }
    if comparison is None:
        result.update({
            "weekly_events": {"passed": False, "measured": False},
            "comparison": None, "dropped_to_zero": [], "big_drops": [],
            "local_losses": [], "onboarding": [],
        })
    else:
        result.update(_comparison_gates(comparison, gates, name, seeded))
    gates.extend(
        _gate("Snapshot verification", False, error) for error in errors
    )
    result["gates"] = gates
    result["errors"] = errors
    result["passed"] = all(g["passed"] for g in gates)
    LOGGER.info(
        "frontend snapshot verification as of %s: passed=%s | events delta=%.2f%% | "
        "weekly match=%s%%",
        as_of, result["passed"], delta_pct, result["weekly_events"].get("match_pct"),
    )
    return result


def _comparison_gates(
    comparison: dict[str, Any], gates: list[dict[str, Any]], name, seeded: dict[int, str],
) -> dict[str, Any]:
    recurring = comparison["recurring"]
    before, matched = recurring["before"], recurring["matched"]
    if before:
        match_pct = matched / before * 100.0
        weekly_passed = match_pct >= WEEKLY_MATCH_THRESHOLD_PCT
        detail = (
            f"{matched} of {before} recurring slots unchanged ({round(match_pct, 2)}%); "
            f"{recurring['removed']} removed or changed, {recurring['added']} added"
        )
    else:
        match_pct, weekly_passed = None, True
        detail = f"not measured: no recurring slots last time ({recurring['after']} now)"
    parishes = comparison["parishes"]
    gates.append(_gate(
        f"Weekly schedule at least {WEEKLY_MATCH_THRESHOLD_PCT}% unchanged", weekly_passed,
        detail, threshold=WEEKLY_MATCH_THRESHOLD_PCT, numerator=matched, denominator=before,
        affected=[
            {"parish_id": p["parish_id"], "parish_slug": name(p["parish_id"]),
             "recurring_before": p["recurring_before"],
             "recurring_removed": p["recurring_removed"]}
            for p in sorted(parishes, key=lambda p: -p["recurring_removed"])
            if p["recurring_removed"]
        ],
    ))

    dropped = [
        p for p in parishes
        if p["events_before"] >= PARISH_DROP_TO_ZERO_MIN_EVENTS and p["events_after"] == 0
    ]
    gates.append(_gate(
        "No parish dropped to zero events", not dropped,
        ", ".join(name(p["parish_id"]) for p in dropped) or "none",
        threshold=PARISH_DROP_TO_ZERO_MIN_EVENTS, numerator=len(dropped),
        denominator=sum(
            1 for p in parishes if p["events_before"] >= PARISH_DROP_TO_ZERO_MIN_EVENTS
        ),
        affected=[{"parish_id": p["parish_id"], "parish_slug": name(p["parish_id"]),
                   "events_before": p["events_before"]} for p in dropped],
    ))
    big_drops = [
        name(p["parish_id"]) for p in parishes
        if p["events_before"] >= PARISH_DROP_WARN_MIN_EVENTS
        and 0 < p["events_after"] < p["events_before"] * (1 - PARISH_DROP_WARN_FRACTION)
    ]

    losses: list[dict[str, Any]] = []
    onboarding: list[dict[str, Any]] = []
    for p in parishes:
        parish_id = p["parish_id"]
        seed_as_of = seeded.get(parish_id)
        exempt = seed_as_of is not None and seed_is_current(seed_as_of, p["bulletin_week"])
        availability = p["availability"]
        levels = [("parish", None, None, availability)] + [
            ("church", g["church_slug"], g["event_type"], g) for g in availability["groups"]
        ]
        for level, church, event_type, counts in levels:
            if counts["before"] == 0:
                if counts["after"] and level == "parish":
                    onboarding.append({
                        "parish_id": parish_id, "parish_slug": name(parish_id),
                        "dates": counts["after"],
                    })
                continue
            if not counts["lost"]:
                continue
            fraction = counts["lost"] / counts["before"]
            severe = counts["lost"] >= LOCAL_LOSS_MIN_DATES and fraction > LOCAL_LOSS_MAX_FRACTION
            losses.append({
                "level": level,
                "parish_id": parish_id,
                "parish_slug": name(parish_id),
                "church_slug": church,
                "event_type": event_type,
                "before": counts["before"],
                "lost": counts["lost"],
                "fraction": round(fraction, 3),
                "lost_dates": counts.get("lost_dates", []),
                "severe": severe,
                "seeded_this_run": seed_as_of is not None,
                "holds": severe and not exempt and level in LOCAL_LOSS_HOLD_LEVELS,
            })
    holding = [loss for loss in losses if loss["holds"]]
    gates.append(_gate(
        "No severe local loss of upcoming services", not holding,
        "; ".join(_describe_loss(loss) for loss in holding) or "none",
        threshold={"min_dates": LOCAL_LOSS_MIN_DATES, "max_fraction": LOCAL_LOSS_MAX_FRACTION},
        numerator=len(holding),
        denominator=len([p for p in parishes if p["availability"]["before"]]),
        affected=holding,
    ))
    return {
        "weekly_events": {
            "current_count": recurring["after"],
            "previous_count": before,
            "matching_count": matched,
            "match_pct": None if match_pct is None else round(match_pct, 2),
            "measured": match_pct is not None,
            "passed": weekly_passed,
        },
        "comparison": comparison,
        "dropped_to_zero": [name(p["parish_id"]) for p in dropped],
        "big_drops": big_drops,
        "local_losses": losses,
        "onboarding": onboarding,
    }


def _describe_loss(loss: dict[str, Any]) -> str:
    where = loss["parish_slug"]
    if loss["level"] == "church":
        where += f" `{loss['church_slug']}` {loss['event_type']}"
    return f"{where}: {loss['lost']} of {loss['before']} dates"


def verify_frontend_snapshot(
    current: Path = CURRENT_SNAPSHOT_PATH,
    previous: Path = PREVIOUS_SNAPSHOT_PATH,
    as_of: date | None = None,
    *,
    parish_slugs: dict[int, str] | None = None,
    seeded_this_run: dict[int, str] | None = None,
) -> dict[str, Any]:
    """`check_snapshots` on two snapshot files, read on `as_of` (default today)."""
    as_of = as_of or date.today()
    paths = {"current_snapshot_path": str(current), "previous_snapshot_path": str(previous)}
    try:
        current_tables = _load(current)
        previous_tables = _load(previous)
    except (FileNotFoundError, SnapshotFormatError) as exc:
        return {
            "passed": False, "as_of": as_of.isoformat(),
            "gate_policy_version": GATE_POLICY_VERSION,
            "gates": [_gate("Snapshot verification", False, str(exc))],
            "errors": [str(exc)], **paths,
        }
    result = check_snapshots(
        current_tables, previous_tables, as_of,
        parish_slugs=parish_slugs, seeded_this_run=seeded_this_run,
    )
    return {**result, **paths}
