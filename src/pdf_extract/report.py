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
from pathlib import Path
from typing import Any

from pdf_extract.bulletin_week import (
    STALE_BULLETIN_AGE_DAYS,
    bulletin_reference_date,
    stale_parishes,
)
from pdf_extract.parish_sites.resolve import OLD_PICK_MARK
from pdf_extract.runs import (
    FAILED_STATUSES,
    FETCH_NEW,
    PROCESS_OLD_ISSUE,
    PROCESS_REPEATED_WEEK,
    consecutive_failures,
    parish_results,
)
from pdf_extract.schedule.report import render_update_mode, update_mode_report
from pdf_extract.schedule.store import update_mode_slugs
from pdf_extract.storage import (
    fetch_only_slugs,
    latest_bulletin_ids,
    load_bulletins,
    load_events,
)
from pdf_extract.timeparse import time_to_minutes

# A parish that showed at least this many events and now shows none holds the
# run for review: far more often a wrong PDF or a failed extraction than a
# parish that really stopped listing anything.
PARISH_DROP_TO_ZERO_MIN_EVENTS = 3

# A parish losing more than this share of its events is called out as a
# warning, without holding the run.
PARISH_DROP_WARN_FRACTION = 0.5
PARISH_DROP_WARN_MIN_EVENTS = 6

# More than this share of attempted parishes failing to fetch holds the run:
# the checks below compare against unchanged data and would otherwise pass a
# week in which almost nothing was refreshed.
FETCH_FAILURE_HOLD_FRACTION = 0.5

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


def _current_state(
    conn: sqlite3.Connection, excluding: set[str] = frozenset(),
) -> dict[str, tuple[int, set[EventKey], int]]:
    """Parish slug -> (current bulletin id, its event keys, its event count).

    Parishes in `excluding` (the update-mode ones) are left out.
    """
    latest = {
        slug: bulletin_id for slug, bulletin_id in latest_bulletin_ids(conn).items()
        if slug not in excluding
    }
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
    """What changed for each extract-mode parish.

    A parish in update mode in either database is left out: its changes are
    reported from its calls' proposals (`schedule.report`). So is a parish
    that is fetch-only in a database, as the website leaves it out.
    """
    before_conn, after_conn = _open_ro(before), _open_ro(after)
    try:
        update_mode = update_mode_slugs(before_conn) | update_mode_slugs(after_conn)
        before_state = _current_state(before_conn, update_mode | fetch_only_slugs(before_conn))
        after_state = _current_state(after_conn, update_mode | fetch_only_slugs(after_conn))
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


def _stale_parishes(
    conn: sqlite3.Connection, attempted: set[str],
) -> dict[str, dict[str, str | None] | None]:
    """Parishes whose newest bulletin is two weeks old, with when it was last served.

    A site still serving that bulletin is alive but not updated; one that
    stopped answering was last seen when it was fetched.
    """
    stale = stale_parishes(load_bulletins(conn), sorted(attempted))
    out: dict[str, dict[str, str | None] | None] = {}
    for slug, newest in stale.items():
        if newest is None:
            out[slug] = None
            continue
        reference = bulletin_reference_date(newest)
        out[slug] = {
            "bulletin_date": reference.isoformat() if reference else None,
            "fetched_at": newest.get("fetched_at"),
            "last_seen_at": newest.get("last_seen_at"),
            "source_url": newest.get("source_url"),
        }
    return out


def _fetch_only_report(
    conn: sqlite3.Connection, fetch_only: set[str], results: list[dict[str, Any]],
) -> dict[str, Any]:
    """How the fetch-only parishes' bulletins came in this run.

    These parishes are fetched but not processed, so this is the place to see
    whether a new diocese's bulletins are being found before switching it on.
    """
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {
        "parishes": len(fetch_only),
        "attempted": len({r["parish_slug"] for r in results}),
        "fetch": dict(sorted(counts.items())),
        "failures": [
            {
                **r,
                "consecutive_failures": consecutive_failures(conn, r["parish_slug"], r["stage"]),
            }
            for r in results if r["status"] in FAILED_STATUSES
        ],
        "old_picks": [
            r for r in results
            if r["status"] == FETCH_NEW and OLD_PICK_MARK in (r.get("detail") or "")
        ],
        "stale_parishes": _stale_parishes(conn, {r["parish_slug"] for r in results}),
    }


def build_report(
    *,
    run_id: str,
    before_db: Path,
    after_db: Path,
    stages: dict[str, Any],
    snapshot_verification: dict[str, Any] | None,
    seeded: dict[str, Any] | None = None,
    seeds: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Everything the run changed and every reason to hold it, as one dict.

    `seeded` is what re-seeding from the CSVs did at the start of the run.
    Its deletions happen before `before_db` is taken, so the before/after
    comparison cannot see them; they are reported and gated here instead.
    `seeds` is what loading the approved seed files did (`seeding.loader`),
    after `before_db` was taken, so their schedules are in the comparison.
    """
    changes = diff_databases(before_db, after_db)

    conn = _open_ro(after_db)
    try:
        # Fetch-only parishes are reported on their own, below, and don't
        # count toward the checks: they aren't on the site yet.
        fetch_only = fetch_only_slugs(conn)
        all_results = parish_results(conn, run_id)
        results = [r for r in all_results if r["parish_slug"] not in fetch_only]
        fetch_only_results = [
            r for r in all_results if r["parish_slug"] in fetch_only and r["stage"] == "fetch"
        ]
        attempted = {r["parish_slug"] for r in results if r["stage"] == "fetch"}
        failures = [
            {
                **r,
                "consecutive_failures": consecutive_failures(conn, r["parish_slug"], r["stage"]),
            }
            for r in results
            if r["status"] in FAILED_STATUSES
        ]
        fetch_only_report = _fetch_only_report(conn, fetch_only, fetch_only_results)
        wrong_bulletins = [r for r in results if r["status"] == "wrong_bulletin"]
        # A third bulletin for one week: the site keeps changing it, or the
        # duplicate check is missing a server's rebuilds.
        repeated_weeks = [r for r in results if r["status"] == PROCESS_REPEATED_WEEK]
        # The site went back to an older issue than one we already had.
        old_issues = [r for r in results if r["status"] == PROCESS_OLD_ISSUE]
        # A new bulletin the site dated, but not this week: a parish running
        # behind, or the resolver reading an archive.
        old_picks = [
            r for r in results
            if r["stage"] == "fetch" and r["status"] == FETCH_NEW
            and OLD_PICK_MARK in (r.get("detail") or "")
        ]
        stale = _stale_parishes(conn, attempted)
        update_mode = update_mode_report(conn, run_id)
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
    seeded = seeded or {}
    removed_parishes = seeded.get("parishes_deleted", 0)
    removed_churches = seeded.get("churches_deleted", 0)
    retired_churches = seeded.get("churches_retired", 0)
    gates.append({
        "name": "No parish or church removed from the CSVs",
        "passed": not (removed_parishes or removed_churches or retired_churches),
        "detail": f"{removed_parishes} parishes, {removed_churches} churches deleted"
        " with their bulletins and events"
        + (f"; {retired_churches} churches retired with their schedule entries"
           if retired_churches else ""),
    })
    fetch_failed = sum(1 for f in failures if f["stage"] == "fetch")
    gates.append({
        "name": f"At most {int(FETCH_FAILURE_HOLD_FRACTION * 100)}% of parishes failed to fetch",
        "passed": not attempted or fetch_failed <= len(attempted) * FETCH_FAILURE_HOLD_FRACTION,
        "detail": f"{fetch_failed} of {len(attempted)}",
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
            "update_mode_parishes": len(update_mode["parishes"]),
            "update_changes_applied": update_mode["applied"],
            "update_proposals_rejected": update_mode["rejected"],
        },
        "update_mode": update_mode,
        "fetch_only": fetch_only_report,
        "seeds": {
            "loaded": (seeds or {}).get("loaded", []),
            "skipped": (seeds or {}).get("skipped", []),
        },
        "attention": {
            "failures": failures,
            "wrong_bulletins": wrong_bulletins,
            "repeated_weeks": repeated_weeks,
            "old_issues": old_issues,
            "old_picks": old_picks,
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


_WEEKDAY_ORDER = {
    day: index for index, day in enumerate(
        ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
    )
}


def _display_order(event: dict[str, Any]) -> tuple:
    """Type, then weekday or date, then clock time (not the time's text)."""
    day = event.get("day_of_week")
    when = (
        (0, _WEEKDAY_ORDER.get(day.lower(), 7), "")
        if isinstance(day, str) and event.get("event_kind") == "weekly"
        else (1, 0, event.get("date") or "")
    )
    return (event["event_type"], when, time_to_minutes(event["start_time"]) or 0)


# ── Markdown ────────────────────────────────────────────────────────────────
def _describe_newest(newest: dict[str, str | None] | None) -> str:
    if newest is None:
        return "never fetched"
    fetched = (newest.get("fetched_at") or "")[:10]
    seen = (newest.get("last_seen_at") or "")[:10]
    text = f"newest is for {newest.get('bulletin_date') or 'an unknown date'}"
    if fetched:
        text += f", fetched {fetched}"
    if seen and seen != fetched:
        text += f"; the site still served it {seen}"
    return text


def _render_fetch_only(section: dict[str, Any], *, max_notes: int = 60) -> list[str]:
    """The fetch-only parishes' fetch results, or nothing when there are none.

    The notes stop at `max_notes`: a newly promoted diocese can have dozens of
    parishes not found yet, and the report also goes into a GitHub issue.
    """
    if not section.get("parishes"):
        return []
    counts = ", ".join(f"{status} {n}" for status, n in section.get("fetch", {}).items())
    lines = [
        "", "### Fetch-only parishes", "",
        f"{section['parishes']} parishes are fetched but not processed or shown "
        f"(`fetch_only` in data/parishes.csv). This run fetched {section['attempted']}"
        + (f": {counts}." if counts else "."),
    ]
    notes: list[str] = []
    for failure in section.get("failures", []):
        streak = failure["consecutive_failures"]
        streak_note = f" — {streak} runs in a row" if streak > 1 else ""
        detail = f": {failure['detail']}" if failure.get("detail") else ""
        notes.append(
            f"- **{failure['parish_slug']}** {failure['stage']} {failure['status']}"
            f"{streak_note}{detail}"
        )
    for result in section.get("old_picks", []):
        notes.append(
            f"- **{result['parish_slug']}**: took a bulletin not dated this week "
            f"({result['detail']}; {result.get('source_url')})"
        )
    for slug, newest in section.get("stale_parishes", {}).items():
        notes.append(
            f"- **{slug}** has no bulletin from the last {STALE_BULLETIN_AGE_DAYS} days "
            f"({_describe_newest(newest)})"
        )
    if len(notes) > max_notes:
        hidden = len(notes) - max_notes
        notes = notes[:max_notes] + [f"- … and {hidden} more (all in report.json)"]
    if notes:
        lines += [""] + notes
    return lines


def render_markdown(report: dict[str, Any], *, max_changed_parishes: int = 40) -> str:
    status = report["status"]
    icon = {"passed": "✅", "held": "⏸️", "failed": "❌"}.get(status, "")
    totals = report["totals"]
    scope = report.get("scope") or {}
    lines = [
        f"## {icon} Weekly data run `{report['run_id']}`: {status}",
        "",
    ]
    if scope.get("summary"):
        lines += [scope["summary"], ""]
    lines += [
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
    for result in attention.get("repeated_weeks", []):
        notes.append(
            f"- **{result['parish_slug']}**: another bulletin for a week we already had "
            f"two of; check it ({result['detail']}; {result.get('source_url')})"
        )
    for result in attention.get("old_issues", []):
        notes.append(
            f"- **{result['parish_slug']}**: the site served an older issue than the one "
            f"shown ({result['detail']}; {result.get('source_url')})"
        )
    for result in attention.get("old_picks", []):
        notes.append(
            f"- **{result['parish_slug']}**: took a bulletin not dated this week "
            f"({result['detail']}; {result.get('source_url')})"
        )
    for slug in attention["dropped_to_zero"]:
        notes.append(f"- **{slug}** now shows no events (holds the run)")
    for slug in attention["big_drops"]:
        notes.append(f"- **{slug}** lost more than half of its events")
    for slug, newest in attention["stale_parishes"].items():
        notes.append(
            f"- **{slug}** has no bulletin from the last {STALE_BULLETIN_AGE_DAYS} days "
            f"({_describe_newest(newest)})"
        )
    lines += ["", "### Needs attention", ""]
    lines += notes or ["Nothing."]
    lines += _render_fetch_only(report.get("fetch_only") or {})

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
        by_church: dict[str, list[tuple[tuple, str]]] = {}
        for sign, events in (("+", change["added"]), ("−", change["removed"])):
            for event in events:
                by_church.setdefault(event["church_slug"], []).append(
                    (_display_order(event), f"{sign} {event['summary']}")
                )
        for church, entries in sorted(by_church.items()):
            lines.append(f"- `{church}`")
            lines += [f"  - {text}" for _, text in sorted(entries)]
        lines += ["", "</details>"]
    if len(changes) > max_changed_parishes:
        lines.append(
            f"\n…and {len(changes) - max_changed_parishes} more parishes; see report.json."
        )
    lines += render_seeds(report.get("seeds") or {})
    if report.get("update_mode"):
        lines += render_update_mode(report["update_mode"])
    return "\n".join(lines) + "\n"


def render_seeds(seeds: dict[str, Any]) -> list[str]:
    """The seed files this run loaded and the ones it skipped, if any."""
    loaded, skipped = seeds.get("loaded") or [], seeds.get("skipped") or []
    if not loaded and not skipped:
        return []
    lines = ["", "### Seeds", ""]
    for item in loaded:
        lines.append(
            f"- **{item['parish']}** seeded (revision {item['revision']}, "
            f"{item['entries']} entries, as of {item['as_of']}, approved by "
            f"{item.get('reviewer') or 'unknown'}): in update mode from now on"
        )
    for item in skipped:
        lines.append(f"- **{item['parish']}** seed file not loaded: {item['reason']}")
    return lines
