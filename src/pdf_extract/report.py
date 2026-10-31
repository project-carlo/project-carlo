"""The weekly change report: what a run changed, in terms a person can check.

Compares the frontend snapshot of the database before a run with the one
after it, read on the same date (`schedule_diff`, gated by
`verify_frontend_snapshot`), so extract- and update-mode parishes get the same
checks: which Masses, Confessions and Adorations changed, appeared or
disappeared at which church, and which upcoming dates a visitor would lose.
The databases add what a snapshot doesn't carry: parish slugs and modes,
which parishes have a new bulletin, each parish's fetch/process outcome for
the run, and the update-mode calls and proposals behind a change.

Rendered as Markdown for the GitHub job summary and issues, and as JSON for
anything that wants to read it programmatically.
"""

from __future__ import annotations

import sqlite3
import tempfile
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.bulletin_week import (
    STALE_BULLETIN_AGE_DAYS,
    bulletin_reference_date,
    stale_parishes,
)
from pdf_extract.extract_frontend_db import extract as extract_snapshot
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
from pdf_extract.schedule.store import table_exists, update_mode_slugs
from pdf_extract.schedule_diff import parish_changed
from pdf_extract.storage import (
    fetch_only_slugs,
    latest_bulletin_ids,
    load_bulletins,
)
from pdf_extract.verify_frontend_snapshot import verify_frontend_snapshot

# More than this share of attempted parishes failing to fetch holds the run:
# the checks below compare against unchanged data and would otherwise pass a
# week in which almost nothing was refreshed.
FETCH_FAILURE_HOLD_FRACTION = 0.5

_TYPE_LABELS = {"mass": "Mass", "confession": "Confession", "adoration": "Adoration"}
_DAY_ABBREV = {
    "monday": "Mon", "tuesday": "Tue", "wednesday": "Wed", "thursday": "Thu",
    "friday": "Fri", "saturday": "Sat", "sunday": "Sun",
}
EXTRACT, UPDATE, SEEDED, NEW = "extract", "update", "extract→update", "new"

EventKey = tuple[str, str, str, str | None, str | None, str, str | None, bool]


def _open_ro(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


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


def _parish_ids(conn: sqlite3.Connection) -> dict[int, str]:
    return {row[0]: row[1] for row in conn.execute("SELECT id, slug FROM parish")}


def _seeds(conn: sqlite3.Connection) -> dict[int, str]:
    """Parish id -> its latest seed's as_of, for every update-mode parish."""
    if not table_exists(conn, "schedule_revision"):
        return {}
    rows = conn.execute(
        """SELECT parish_id, MAX(as_of) FROM schedule_revision
           WHERE source_kind = 'seed' GROUP BY parish_id"""
    ).fetchall()
    return {row[0]: row[1] for row in rows}


def snapshot_context(before_db: Path, after_db: Path) -> dict[str, Any]:
    """What the snapshot gates need from the databases, as `verify_frontend_snapshot` takes it.

    `parish_slugs` names each parish (from the after database, else the
    before one); `seeded_this_run` is parish id -> seed as_of for the parishes
    that switched to update mode between the two.
    """
    before_conn, after_conn = _open_ro(before_db), _open_ro(after_db)
    try:
        slugs = {**_parish_ids(before_conn), **_parish_ids(after_conn)}
        seeds_before, seeds_after = _seeds(before_conn), _seeds(after_conn)
    finally:
        before_conn.close()
        after_conn.close()
    return {
        "parish_slugs": slugs,
        "seeded_this_run": {
            parish_id: as_of for parish_id, as_of in seeds_after.items()
            if parish_id not in seeds_before
        },
    }


def verify_databases(before_db: Path, after_db: Path, as_of: date) -> dict[str, Any]:
    """Build both databases' snapshots as of `as_of` and run the snapshot gates on them."""
    with tempfile.TemporaryDirectory() as tmp:
        current, previous = Path(tmp) / "after.json.gz", Path(tmp) / "before.json.gz"
        extract_snapshot(after_db, current, keep_previous=False, build_date=as_of)
        extract_snapshot(before_db, previous, keep_previous=False, build_date=as_of)
        result = verify_frontend_snapshot(
            current, previous, as_of, **snapshot_context(before_db, after_db),
        )
    result.pop("current_snapshot_path", None)
    result.pop("previous_snapshot_path", None)
    return result


def _modes(
    before_db: Path, after_db: Path,
) -> tuple[dict[int, str], dict[str, str], dict[str, bool]]:
    """Parish id -> slug, slug -> its mode this run, and slug -> whether its bulletin changed."""
    before_conn, after_conn = _open_ro(before_db), _open_ro(after_db)
    try:
        ids = {**_parish_ids(before_conn), **_parish_ids(after_conn)}
        known_before = set(_parish_ids(before_conn).values())
        update_before, update_after = update_mode_slugs(before_conn), update_mode_slugs(after_conn)
        bulletins_before = latest_bulletin_ids(before_conn)
        bulletins_after = latest_bulletin_ids(after_conn)
        hidden = fetch_only_slugs(after_conn)
        slugs = known_before | set(_parish_ids(after_conn).values())
    finally:
        before_conn.close()
        after_conn.close()
    modes = {}
    for slug in slugs:
        if slug not in known_before:
            modes[slug] = NEW
        elif slug in update_after:
            modes[slug] = UPDATE if slug in update_before else SEEDED
        else:
            modes[slug] = EXTRACT
    changed = {
        slug: bulletins_before.get(slug) != bulletins_after.get(slug)
        for slug in slugs if slug not in hidden
    }
    return ids, modes, changed


def _parish_report(
    section: dict[str, Any], slug: str, mode: str, bulletin_changed: bool,
    losses: list[dict[str, Any]],
) -> dict[str, Any]:
    availability = section["availability"]
    return {
        "parish_slug": slug,
        "parish_id": section["parish_id"],
        "mode": mode,
        "bulletin_changed": bulletin_changed,
        "bulletin_url": section["bulletin_url"],
        "bulletin_week": section["bulletin_week"],
        "before_count": section["events_before"],
        "after_count": section["events_after"],
        "onboarding": section["events_before"] == 0 and section["events_after"] > 0,
        "recurring": section["recurring"],
        "dated": section["dated"],
        "cancellations": section["cancellations"],
        "availability": {
            "before": availability["before"],
            "after": availability["after"],
            "lost": availability["lost"],
            "gained": availability["gained"],
            "moved": availability["moved"],
            "groups": [g for g in availability["groups"] if g["lost"] or g["gained"]],
        },
        "local_losses": [loss for loss in losses if loss["parish_id"] == section["parish_id"]],
        "notes": section["notes"],
        "diagnostics": section["diagnostics"],
    }


def _blank_totals() -> dict[str, int]:
    return {
        "parishes": 0, "parishes_showing_events": 0, "events_before": 0, "events_after": 0,
        "events_added": 0, "events_removed": 0, "parishes_changed": 0,
    }


def _totals(parishes: list[tuple[dict[str, Any], str]]) -> dict[str, Any]:
    """Site-wide totals from the comparison, then the same per mode, then onboarding."""
    totals = {**_blank_totals(), "cancellations_added": 0, "cancellations_removed": 0}
    by_mode: dict[str, dict[str, int]] = {}
    onboarding = {"parishes": 0, "events": 0}
    for p, mode in parishes:
        added = p["recurring_added"] + p["dated_added"]
        removed = p["recurring_removed"] + p["dated_removed"]
        for bucket in (totals, by_mode.setdefault(mode, _blank_totals())):
            bucket["parishes"] += 1
            bucket["parishes_showing_events"] += bool(p["events_after"])
            bucket["events_before"] += p["events_before"]
            bucket["events_after"] += p["events_after"]
            bucket["events_added"] += added
            bucket["events_removed"] += removed
            bucket["parishes_changed"] += parish_changed(p)
        totals["cancellations_added"] += p["cancellations_added"]
        totals["cancellations_removed"] += p["cancellations_removed"]
        if p["events_before"] == 0 and p["events_after"]:
            onboarding["parishes"] += 1
            onboarding["events"] += p["events_after"]
    del totals["parishes"]
    return {**totals, "by_mode": dict(sorted(by_mode.items())), "onboarding": onboarding}


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

    The schedule changes and their gates come from `snapshot_verification`
    (`verify_frontend_snapshot`, as the weekly run passes it); None builds it
    from the two databases as of today (`verify_databases`).

    `seeded` is what re-seeding from the CSVs did at the start of the run.
    Its deletions happen before `before_db` is taken, so the before/after
    comparison cannot see them; they are reported and gated here instead.
    `seeds` is what loading the approved seed files did (`seeding.loader`),
    after `before_db` was taken, so their schedules are in the comparison.
    """
    if snapshot_verification is None:
        snapshot_verification = verify_databases(before_db, after_db, date.today())
    verification = snapshot_verification
    comparison = verification.get("comparison")
    slugs, modes, bulletin_changed = _modes(before_db, after_db)

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

    gates: list[dict[str, Any]] = list(verification.get("gates") or [])
    if not verification.get("passed", False) and all(g["passed"] for g in gates):
        # A verification that failed without saying which gate: hold anyway.
        gates.extend(
            {"name": "Snapshot verification", "passed": False, "detail": error}
            for error in verification.get("errors") or ["verification failed"]
        )
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
        "threshold": FETCH_FAILURE_HOLD_FRACTION,
        "numerator": fetch_failed,
        "denominator": len(attempted),
    })

    losses = verification.get("local_losses") or []
    sections = [
        (p, slugs.get(p["parish_id"]) or f"parish #{p['parish_id']}")
        for p in (comparison or {}).get("parishes", [])
    ]
    changes = [
        _parish_report(
            p, slug, modes.get(slug, EXTRACT), bulletin_changed.get(slug, False), losses,
        )
        for p, slug in sorted(sections, key=lambda item: item[1])
        if parish_changed(p) or p["notes"] or p["diagnostics"] or p["availability"]["lost"]
        or any(loss["parish_id"] == p["parish_id"] for loss in losses)
    ]
    passed = all(g["passed"] for g in gates)
    totals = _totals([(p, modes.get(slug, EXTRACT)) for p, slug in sections])
    return {
        "run_id": run_id,
        "status": "passed" if passed else "held",
        "as_of": verification.get("as_of"),
        "gates": gates,
        "stages": stages,
        "comparison": None if comparison is None else {
            "as_of": comparison["as_of"],
            "window": comparison["window"],
            "gate_policy_version": verification.get("gate_policy_version"),
            "thresholds": verification.get("thresholds"),
            "recurring": comparison["recurring"],
            "availability": comparison["availability"],
            "weekly_events": verification.get("weekly_events"),
        },
        "totals": {
            **totals,
            "parishes_with_new_bulletin": sum(bulletin_changed.values()),
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
            "dropped_to_zero": verification.get("dropped_to_zero") or [],
            "big_drops": verification.get("big_drops") or [],
            "local_losses": [loss for loss in losses if loss["severe"]],
            "onboarding": verification.get("onboarding") or [],
        },
        "changes": changes,
    }


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


def _comparison_lines(report: dict[str, Any]) -> list[str]:
    """When and how the schedules were compared, and the totals per mode."""
    comparison = report.get("comparison")
    totals = report["totals"]
    lines: list[str] = []
    if comparison:
        window = comparison["window"]
        last = date.fromisoformat(window["end"]).toordinal() - 1
        lines.append(
            f"Compared as of {comparison['as_of']}; upcoming dates "
            f"{window['start']} to {date.fromordinal(last).isoformat()} ({window['days']} days); "
            f"gate policy v{comparison.get('gate_policy_version')}."
        )
    modes = totals.get("by_mode") or {}
    if len(modes) > 1 or set(modes) - {EXTRACT}:
        lines.append("By mode: " + "; ".join(
            f"{mode} {m['parishes']} parishes, {m['events_before']} → {m['events_after']} "
            f"events (+{m['events_added']} / −{m['events_removed']})"
            for mode, m in modes.items()
        ) + ".")
    onboarding = totals.get("onboarding") or {}
    if onboarding.get("parishes"):
        lines.append(
            f"Onboarding: {onboarding['parishes']} parishes showing events for the first time "
            f"({onboarding['events']} events), not counted as retained or lost."
        )
    return lines + [""] if lines else []


def _describe_loss(loss: dict[str, Any]) -> str:
    where = f"**{loss['parish_slug']}**"
    if loss["level"] == "church":
        label = _TYPE_LABELS.get(loss["event_type"], loss["event_type"])
        where += f" `{loss['church_slug']}` {label}"
    text = f"{where} loses {loss['missing']} of its {loss['before']} upcoming dates"
    if loss["moved"]:
        text += f" ({loss['moved']} more moved to another time)"
    if loss["holds"]:
        return text + " (holds the run)"
    if loss["seeded_this_run"] and loss["severe"]:
        return text + " (seeded this run from a current seed; does not hold)"
    return text + " (reported only)" if loss["severe"] else text


def _by_church(changes: list[dict[str, Any]], *, signs: bool = True) -> list[str]:
    marks = {"added": "+ ", "removed": "− ", "modified": "changed: "}
    by_church: dict[str, list[str]] = {}
    for change in changes:
        mark = marks.get(change.get("change"), "") if signs else ""
        by_church.setdefault(change["church_slug"], []).append(f"{mark}{change['summary']}")
    lines = []
    for church, texts in sorted(by_church.items()):
        lines.append(f"- `{church}`")
        lines += [f"  - {text}" for text in texts]
    return lines


def _render_parish(change: dict[str, Any]) -> list[str]:
    counts = [
        f"{n} {label}" for n, label in (
            (len(change["recurring"]), "recurring"),
            (len(change["dated"]), "dated"),
            (len(change["cancellations"]), "cancellations"),
        ) if n
    ]
    bits = [change["mode"]] + (["new bulletin"] if change["bulletin_changed"] else [])
    lines = [
        f"<details><summary><b>{change['parish_slug']}</b> ({', '.join(bits)}): "
        f"{', '.join(counts) or 'no schedule change'} "
        f"({change['before_count']} → {change['after_count']} events)</summary>",
        "",
    ]
    if change.get("bulletin_url"):
        week = f" for the week of {change['bulletin_week']}" if change.get("bulletin_week") else ""
        lines += [f"[Current bulletin]({change['bulletin_url']}){week}.", ""]
    for key, title in (
        ("recurring", "Recurring schedule"), ("dated", "Dated events"),
        ("cancellations", "Cancellations"),
    ):
        if change[key]:
            lines += [f"**{title}**", ""] + _by_church(change[key]) + [""]
    availability = change["availability"]
    if availability["lost"] or availability["gained"]:
        lines.append(
            f"**Upcoming dates**: {availability['before']} → {availability['after']} "
            f"(−{availability['lost']} / +{availability['gained']})"
        )
        lines.append("")
        for group in availability["groups"]:
            label = _TYPE_LABELS.get(group["event_type"], group["event_type"])
            text = (
                f"- `{group['church_slug']}` {label}: lost {group['lost']} of {group['before']}"
                f", gained {group['gained']}"
                + (f" ({group['moved']} of them a time that moved)" if group["moved"] else "")
            )
            if group["lost_dates"]:
                shown = ", ".join(group["lost_dates"][:6])
                more = len(group["lost_dates"]) - 6
                text += f" (lost {shown}{f', and {more} more' if more > 0 else ''})"
            lines.append(text)
        lines.append("")
    if change["notes"]:
        lines += ["**Notes** (not counted as schedule changes)", ""]
        for note in change["notes"]:
            before = "; ".join(note["before"]) or "no note"
            after = "; ".join(note["after"]) or "no note"
            lines.append(f"- `{note['church_slug']}` {note['summary']}: “{before}” → “{after}”")
        lines.append("")
    if change["diagnostics"]:
        lines += ["**Data quality**", ""] + [f"- {d}" for d in change["diagnostics"]] + [""]
    return lines + ["</details>"]


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
        f"(+{totals['events_added']} / −{totals['events_removed']} events"
        + (
            f", +{totals['cancellations_added']} / −{totals['cancellations_removed']} "
            "cancellations" if totals.get("cancellations_added")
            or totals.get("cancellations_removed") else ""
        ) + ").",
        "",
    ]
    lines += _comparison_lines(report)
    lines += [
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
    for loss in attention.get("local_losses", []):
        notes.append(f"- {_describe_loss(loss)}")
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
        lines += _render_parish(change)
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
