"""The weekly change report: what a run changed, in terms a person can check.

Compares the database before a run with the database after it, the way the
website would see them (each parish's latest processed bulletin), and says
which Masses, Confessions and Adorations appeared or disappeared at which
church. It also collects each parish's fetch/process outcome for the run and
applies the per-parish publishing gate.

Rendered as Markdown for the GitHub job summary and issues, and as JSON for
anything that wants to read it programmatically.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from pdf_extract.runs import FAILED_STATUSES, consecutive_failures, parish_results
from pdf_extract.storage import latest_bulletin_ids, load_bulletins, load_events

# A parish that showed at least this many events and now shows none holds the
# run for review: far more often a wrong PDF or a failed extraction than a
# parish that really stopped listing anything.
PARISH_DROP_TO_ZERO_MIN_EVENTS = 3

# A parish losing more than this share of its events is called out as a
# warning, without holding the run.
PARISH_DROP_WARN_FRACTION = 0.5
PARISH_DROP_WARN_MIN_EVENTS = 6

STALE_BULLETIN_AGE_DAYS = 14

_TYPE_LABELS = {"mass": "Mass", "confession": "Confession", "adoration": "Adoration"}
_DAY_ABBREV = {
    "monday": "Mon", "tuesday": "Tue", "wednesday": "Wed", "thursday": "Thu",
    "friday": "Fri", "saturday": "Sat", "sunday": "Sun",
}

EventKey = tuple[str, str, str, str | None, str | None, str, str | None, bool]


@dataclass
class ParishChange:
    parish_slug: str
    before_count: int
    after_count: int
    bulletin_changed: bool
    added: list[EventKey] = field(default_factory=list)
    removed: list[EventKey] = field(default_factory=list)


def _open_ro(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _event_key(row: dict[str, Any]) -> EventKey:
    return (
        row["church_slug"],
        row["event_type"],
        row["event_kind"],
        row.get("day_of_week"),
        row.get("date"),
        row["start_time"],
        row.get("end_time"),
        bool(row.get("cancelled")),
    )


def _current_state(conn: sqlite3.Connection) -> dict[str, tuple[int, set[EventKey], int]]:
    """Parish slug -> (current bulletin id, its event keys, its event count)."""
    latest = latest_bulletin_ids(conn)
    by_bulletin: dict[int, list[dict[str, Any]]] = {}
    for row in load_events(conn, list(latest.values())):
        by_bulletin.setdefault(row["bulletin_id"], []).append(row)
    state = {}
    for slug, bulletin_id in latest.items():
        rows = by_bulletin.get(bulletin_id, [])
        state[slug] = (bulletin_id, {_event_key(r) for r in rows}, len(rows))
    return state


def describe_event(key: EventKey) -> str:
    """"Confession · Sat 3:00 PM–4:00 PM" or "Mass · 2026-10-04 9:00 AM (cancelled)"."""
    _church, event_type, kind, day_of_week, date, start, end, cancelled = key
    label = _TYPE_LABELS.get(event_type, event_type or "Event")
    when = (
        _DAY_ABBREV.get((day_of_week or "").lower(), day_of_week or "?")
        if kind == "weekly"
        else (date or "?")
    )
    time = f"{start}–{end}" if end else start
    return f"{label} · {when} {time}" + (" (cancelled)" if cancelled else "")


def diff_databases(before: Path, after: Path) -> list[ParishChange]:
    before_conn, after_conn = _open_ro(before), _open_ro(after)
    try:
        before_state = _current_state(before_conn)
        after_state = _current_state(after_conn)
    finally:
        before_conn.close()
        after_conn.close()

    changes = []
    for slug in sorted(set(before_state) | set(after_state)):
        b_id, b_keys, b_count = before_state.get(slug, (None, set(), 0))
        a_id, a_keys, a_count = after_state.get(slug, (None, set(), 0))
        changes.append(
            ParishChange(
                parish_slug=slug,
                before_count=b_count,
                after_count=a_count,
                bulletin_changed=b_id != a_id,
                added=sorted(a_keys - b_keys, key=_sort_key),
                removed=sorted(b_keys - a_keys, key=_sort_key),
            )
        )
    return changes


def _sort_key(key: EventKey) -> tuple:
    return tuple("" if v is None else str(v) for v in key)


def _stale_parishes(conn: sqlite3.Connection, attempted: set[str]) -> dict[str, str | None]:
    latest_fetch: dict[str, str] = {}
    for entry in load_bulletins(conn):
        fetched = entry.get("fetched_at") or ""
        if fetched > latest_fetch.get(entry["parish_slug"], ""):
            latest_fetch[entry["parish_slug"]] = fetched
    cutoff = (datetime.now(UTC) - timedelta(days=STALE_BULLETIN_AGE_DAYS)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return {
        slug: latest_fetch.get(slug)
        for slug in sorted(attempted)
        if latest_fetch.get(slug, "") < cutoff
    }


def build_report(
    *,
    run_id: str,
    before_db: Path,
    after_db: Path,
    stages: dict[str, Any],
    snapshot_verification: dict[str, Any] | None,
) -> dict[str, Any]:
    """Everything the run changed and every reason to hold it, as one dict."""
    changes = diff_databases(before_db, after_db)

    conn = _open_ro(after_db)
    try:
        results = parish_results(conn, run_id)
        attempted = {r["parish_slug"] for r in results if r["stage"] == "fetch"}
        failures = [
            {
                **r,
                "consecutive_failures": consecutive_failures(conn, r["parish_slug"], r["stage"]),
            }
            for r in results
            if r["status"] in FAILED_STATUSES
        ]
        wrong_bulletins = [r for r in results if r["status"] == "wrong_bulletin"]
        stale = _stale_parishes(conn, attempted)
    finally:
        conn.close()

    dropped_to_zero = [
        c.parish_slug for c in changes
        if c.before_count >= PARISH_DROP_TO_ZERO_MIN_EVENTS and c.after_count == 0
    ]
    big_drops = [
        c.parish_slug for c in changes
        if c.before_count >= PARISH_DROP_WARN_MIN_EVENTS
        and 0 < c.after_count < c.before_count * (1 - PARISH_DROP_WARN_FRACTION)
    ]

    gates = []
    if snapshot_verification is not None:
        gates.extend([
            {
                "name": "Church count unchanged",
                "passed": snapshot_verification.get("churches", {}).get("passed", False),
                "detail": _fmt_before_after(snapshot_verification.get("churches", {})),
            },
            {
                "name": "Total events within "
                f"±{snapshot_verification.get('thresholds', {}).get('event_delta_max_pct')}%",
                "passed": snapshot_verification.get("events", {}).get("passed", False),
                "detail": _fmt_before_after(snapshot_verification.get("events", {}))
                + f" ({snapshot_verification.get('events', {}).get('delta_pct')}%)",
            },
            {
                "name": "Weekly schedule at least "
                f"{snapshot_verification.get('thresholds', {}).get('weekly_match_min_pct')}%"
                " unchanged",
                "passed": snapshot_verification.get("weekly_events", {}).get("passed", False),
                "detail": f"{snapshot_verification.get('weekly_events', {}).get('match_pct')}%"
                " of last week's weekly slots still present",
            },
        ])
        for error in snapshot_verification.get("errors", []):
            gates.append({"name": "Snapshot verification", "passed": False, "detail": error})
    gates.append({
        "name": "No parish dropped to zero events",
        "passed": not dropped_to_zero,
        "detail": ", ".join(dropped_to_zero) or "none",
    })

    passed = all(g["passed"] for g in gates)
    changed = [c for c in changes if c.added or c.removed]
    return {
        "run_id": run_id,
        "status": "passed" if passed else "held",
        "gates": gates,
        "stages": stages,
        "totals": {
            "parishes_showing_events": sum(1 for c in changes if c.after_count),
            "events_before": sum(c.before_count for c in changes),
            "events_after": sum(c.after_count for c in changes),
            "events_added": sum(len(c.added) for c in changes),
            "events_removed": sum(len(c.removed) for c in changes),
            "parishes_changed": len(changed),
            "parishes_with_new_bulletin": sum(1 for c in changes if c.bulletin_changed),
        },
        "attention": {
            "failures": failures,
            "wrong_bulletins": wrong_bulletins,
            "stale_parishes": stale,
            "dropped_to_zero": dropped_to_zero,
            "big_drops": big_drops,
        },
        "changes": [
            {
                "parish_slug": c.parish_slug,
                "before_count": c.before_count,
                "after_count": c.after_count,
                "bulletin_changed": c.bulletin_changed,
                "added": [_key_dict(k) for k in c.added],
                "removed": [_key_dict(k) for k in c.removed],
            }
            for c in changed
        ],
    }


def _key_dict(key: EventKey) -> dict[str, Any]:
    names = (
        "church_slug", "event_type", "event_kind", "day_of_week", "date",
        "start_time", "end_time", "cancelled",
    )
    return {**dict(zip(names, key)), "summary": describe_event(key)}


def _fmt_before_after(section: dict[str, Any]) -> str:
    return f"{section.get('previous', '?')} → {section.get('current', '?')}"


# ── Markdown ────────────────────────────────────────────────────────────────
def render_markdown(report: dict[str, Any], *, max_changed_parishes: int = 40) -> str:
    status = report["status"]
    icon = {"passed": "✅", "held": "⏸️", "failed": "❌"}.get(status, "")
    totals = report["totals"]
    lines = [
        f"## {icon} Weekly data run `{report['run_id']}`: {status}",
        "",
        f"**{totals['events_after']}** events across "
        f"**{totals['parishes_showing_events']}** parishes "
        f"(was {totals['events_before']}). "
        f"{totals['parishes_with_new_bulletin']} parishes have a new bulletin; "
        f"{totals['parishes_changed']} changed their schedule "
        f"(+{totals['events_added']} / −{totals['events_removed']} events).",
        "",
        "### Publishing checks",
        "",
        "| Check | Result | Detail |",
        "| :-- | :-: | :-- |",
    ]
    for gate in report["gates"]:
        lines.append(
            f"| {gate['name']} | {'✅' if gate['passed'] else '❌'} | {gate['detail']} |"
        )

    stages = report.get("stages", {})
    if stages:
        lines += ["", "### Stages", "", "| Stage | Result |", "| :-- | :-- |"]
        for name, result in stages.items():
            summary = ", ".join(f"{k} {v}" for k, v in (result or {}).items()
                                if not isinstance(v, (dict, list)))
            lines.append(f"| {name} | {summary} |")

    attention = report["attention"]
    notes: list[str] = []
    for failure in attention["failures"]:
        streak = failure["consecutive_failures"]
        streak_note = f" — {streak} runs in a row" if streak > 1 else ""
        detail = f": {failure['detail']}" if failure.get("detail") else ""
        notes.append(
            f"- **{failure['parish_slug']}** {failure['stage']} {failure['status']}"
            f"{streak_note}{detail}"
        )
    for result in attention["wrong_bulletins"]:
        notes.append(
            f"- **{result['parish_slug']}**: the extractor says the PDF is not this "
            f"parish's current bulletin ({result.get('source_url')})"
        )
    for slug in attention["dropped_to_zero"]:
        notes.append(f"- **{slug}** now shows no events (holds the run)")
    for slug in attention["big_drops"]:
        notes.append(f"- **{slug}** lost more than half of its events")
    for slug, fetched in attention["stale_parishes"].items():
        notes.append(
            f"- **{slug}** has no bulletin newer than {STALE_BULLETIN_AGE_DAYS} days "
            f"(latest fetched {fetched[:10] if fetched else 'never'})"
        )
    lines += ["", "### Needs attention", ""]
    lines += notes or ["Nothing."]

    changes = report["changes"]
    lines += ["", "### Schedule changes", ""]
    if not changes:
        lines.append("No parish's schedule changed.")
    for change in changes[:max_changed_parishes]:
        lines.append(
            f"<details><summary><b>{change['parish_slug']}</b>: "
            f"+{len(change['added'])} / −{len(change['removed'])} "
            f"({change['before_count']} → {change['after_count']} events)</summary>"
        )
        lines.append("")
        by_church: dict[str, list[str]] = {}
        for sign, events in (("+", change["added"]), ("−", change["removed"])):
            for event in events:
                by_church.setdefault(event["church_slug"], []).append(
                    f"{sign} {event['summary']}"
                )
        for church, entries in sorted(by_church.items()):
            lines.append(f"- `{church}`")
            lines += [f"  - {entry}" for entry in sorted(entries, key=lambda e: e[2:])]
        lines += ["", "</details>"]
    if len(changes) > max_changed_parishes:
        lines.append(
            f"\n…and {len(changes) - max_changed_parishes} more parishes; see report.json."
        )
    return "\n".join(lines) + "\n"
