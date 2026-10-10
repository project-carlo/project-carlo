"""The weekly report's section for update-mode parishes.

Built from the run's calls and their `proposed_change` rows, per parish:
the applied changes (a modify as before -> after), flags that block nothing,
and the rejections. See docs/schedule-state-plan.md, "The report".
"""

from __future__ import annotations

import sqlite3
from collections import Counter
from typing import Any

from pdf_extract.schedule.entries import Entry
from pdf_extract.schedule.history import SUCCEEDED, CallPlace, parish_history
from pdf_extract.schedule.policy import APPLIED, MASS_DELETE, REJECTED, STALE_BULLETIN
from pdf_extract.schedule.qualifiers import describe_schedule_pattern, mask_to_weeks
from pdf_extract.schedule.store import church_slugs, live_entries, load_entries, table_exists
from pdf_extract.timeparse import minutes_to_time

# A parish whose schedule changed in each of this many calls in a row is flagged.
CHANGED_IN_A_ROW = 3
# A live weekly entry none of the parish's last this-many bulletins printed is flagged.
UNSEEN_BULLETINS = 4

def describe_entry(entry: Entry) -> str:
    """`report.describe_event` with the weeks of the month, season and note an entry carries."""
    from pdf_extract.report import describe_event  # report imports this module

    text = describe_event((
        "", entry.event_type, entry.event_kind, entry.day_of_week, entry.date,
        minutes_to_time(entry.start_time), minutes_to_time(entry.end_time),
        bool(entry.cancelled),
    ))
    pattern = describe_schedule_pattern(
        mask_to_weeks(entry.weeks_of_month), entry.season(), entry.day_of_week,
    )
    qualifiers = [part for part in (pattern, entry.note) if part]
    return text + (f" ({'; '.join(qualifiers)})" if qualifiers else "")


def _unseen_weekly(
    conn: sqlite3.Connection, parish_id: int, places: list[CallPlace],
) -> list[int]:
    """Live weekly entries none of the last UNSEEN_BULLETINS bulletins since they went live printed."""
    counted = {p.llm_call_id: p for p in places if not p.wrong_bulletin and not p.stale}
    calls = conn.execute(
        """SELECT id, bulletin_id, base_revision FROM llm_call
           WHERE parish_id = ? ORDER BY id""",
        (parish_id,),
    ).fetchall()
    calls = [c for c in calls if c["id"] in counted]
    since = dict(conn.execute(
        "SELECT entry_id, since_revision FROM current_schedule WHERE parish_id = ?",
        (parish_id,),
    ).fetchall())
    out = []
    for entry_id, entry in live_entries(conn, parish_id).items():
        if not entry.weekly:
            continue
        shown = [c for c in calls if c["base_revision"] >= since[entry_id]]
        if len(shown) < UNSEEN_BULLETINS:
            continue
        last = [c["bulletin_id"] for c in shown[-UNSEEN_BULLETINS:]]
        printed = conn.execute(
            f"""SELECT 1 FROM entry_sighting WHERE entry_id = ?
                AND bulletin_id IN ({", ".join("?" * len(last))}) LIMIT 1""",
            (entry_id, *last),
        ).fetchone()
        if printed is None:
            out.append(entry_id)
    return sorted(out)


def update_mode_report(conn: sqlite3.Connection, run_id: str) -> dict[str, Any]:
    """The update-mode section of the run's report."""
    empty: dict[str, Any] = {
        "parishes": [], "rejections_by_reason": {}, "rejected_calls": [], "gave_up": [],
        "applied": 0, "rejected": 0,
    }
    if not table_exists(conn, "llm_call"):
        return empty
    parish_rows = conn.execute(
        """SELECT DISTINCT p.id, p.slug FROM llm_call c JOIN parish p ON p.id = c.parish_id
           WHERE c.run_id = ? ORDER BY p.slug""",
        (run_id,),
    ).fetchall()
    by_reason: Counter[str] = Counter()
    rejected_calls: list[dict[str, Any]] = []
    parishes: list[dict[str, Any]] = []
    total_applied = total_rejected = 0

    for parish in parish_rows:
        places = parish_history(conn, parish["id"]).places
        place_by_call = {p.llm_call_id: p for p in places}
        calls = conn.execute(
            """SELECT c.id, c.bulletin_id, c.status, c.error, c.published_date,
                      c.wrong_bulletin, c.church_list_needs_review, b.source_url
               FROM llm_call c JOIN bulletin b ON b.id = c.bulletin_id
               WHERE c.run_id = ? AND c.parish_id = ? ORDER BY c.id""",
            (run_id, parish["id"]),
        ).fetchall()
        proposals = conn.execute(
            f"""SELECT pc.* FROM proposed_change pc
                WHERE pc.llm_call_id IN ({", ".join("?" * len(calls))})
                ORDER BY pc.llm_call_id, pc.seq""",
            [c["id"] for c in calls],
        ).fetchall()
        entries = load_entries(conn, [
            i for p in proposals for i in (p["entry_id"], p["target_entry_id"]) if i is not None
        ])
        slugs = church_slugs(conn, [e.church_id for e in entries.values()])

        def describe(entry_id: int | None) -> str | None:
            entry = entries.get(entry_id) if entry_id is not None else None
            return None if entry is None else describe_entry(entry)

        def church(p: sqlite3.Row) -> str | None:
            entry = entries.get(p["entry_id"]) or entries.get(p["target_entry_id"])
            return None if entry is None else slugs.get(entry.church_id)

        applied = [
            {
                "llm_call_id": p["llm_call_id"],
                "op": p["op"],
                "church_slug": church(p),
                "before": describe(p["target_entry_id"]),
                "after": describe(p["entry_id"]),
                "slot": _slot(entries.get(p["entry_id"]) or entries.get(p["target_entry_id"])),
                "page_number": p["page_number"],
                "rationale": p["rationale"],
            }
            for p in proposals if p["decision"] == APPLIED
        ]
        rejected = [p for p in proposals if p["decision"] == REJECTED]
        reasons = Counter(p["reason"] for p in rejected)
        by_reason.update(reasons)
        total_applied += len(applied)
        total_rejected += len(rejected)

        flags: list[str] = []
        call_summaries = []
        for call in calls:
            place = place_by_call.get(call["id"])
            summary = {
                "llm_call_id": call["id"],
                "bulletin_id": call["bulletin_id"],
                "source_url": call["source_url"],
                "status": call["status"],
                "error": call["error"],
                "published_date": call["published_date"],
                "week": place.week.isoformat() if place and place.week else None,
                "stale": bool(place and place.stale),
                "wrong_bulletin": bool(call["wrong_bulletin"]),
            }
            call_summaries.append(summary)
            if place is None:
                continue
            if place.week is None and not place.wrong_bulletin:
                flags.append(f"bulletin #{call['bulletin_id']} is undated")
            elif place.same_week_before == 1:
                flags.append(
                    f"bulletin #{call['bulletin_id']} is a correction: the 2nd for "
                    f"{place.week.isoformat()}"
                )
            elif place.same_week_before >= 2:
                flags.append(
                    f"bulletin #{call['bulletin_id']} is number {place.same_week_before + 1} "
                    f"for {place.week.isoformat()}; check it"
                )
            if call["church_list_needs_review"]:
                flags.append("the church list may need review")
            call_rejections = [p for p in rejected if p["llm_call_id"] == call["id"]]
            whole = {p["reason"] for p in call_rejections} & {MASS_DELETE, STALE_BULLETIN}
            if whole:
                rejected_calls.append({
                    "parish_slug": parish["slug"],
                    "llm_call_id": call["id"],
                    "source_url": call["source_url"],
                    "reason": whole.pop(),
                    "proposals": [
                        {
                            "seq": p["seq"],
                            "op": p["op"],
                            "before": describe(p["target_entry_id"]),
                            "after": describe(p["entry_id"]),
                            "page_number": p["page_number"],
                            "rationale": p["rationale"],
                        }
                        for p in call_rejections
                    ],
                })

        if _changed_in_a_row(conn, parish["id"]):
            flags.append(f"the schedule changed in each of its last {CHANGED_IN_A_ROW} calls")
        unseen = _unseen_weekly(conn, parish["id"], places)
        if unseen:
            unseen_entries = load_entries(conn, unseen)
            unseen_slugs = church_slugs(conn, [e.church_id for e in unseen_entries.values()])
            for entry_id in unseen:
                entry = unseen_entries[entry_id]
                flags.append(
                    f"`{unseen_slugs.get(entry.church_id)}` {describe_entry(entry)} is still "
                    f"believed, but none of the last {UNSEEN_BULLETINS} bulletins printed it"
                )

        parishes.append({
            "parish_slug": parish["slug"],
            "calls": call_summaries,
            "applied": applied,
            "rejections": dict(sorted(reasons.items())),
            "flags": flags,
        })

    gave_up = conn.execute(
        """SELECT parish_slug, detail, source_url FROM run_parish_result
           WHERE run_id = ? AND stage = 'process' AND detail LIKE '%no longer retried%'
           ORDER BY parish_slug""",
        (run_id,),
    ).fetchall()
    return {
        "parishes": parishes,
        "applied": total_applied,
        "rejected": total_rejected,
        "rejections_by_reason": dict(sorted(by_reason.items())),
        "rejected_calls": rejected_calls,
        "gave_up": [dict(r) for r in gave_up],
    }


def _slot(entry: Entry | None) -> tuple | None:
    """Church, type and weekday (or date): a delete and an add of the same one pair up."""
    if entry is None:
        return None
    return (entry.church_id, entry.event_type, entry.day_of_week or entry.date)


def _changed_in_a_row(conn: sqlite3.Connection, parish_id: int) -> bool:
    calls = conn.execute(
        f"""SELECT c.id,
                   EXISTS (SELECT 1 FROM proposed_change p
                           WHERE p.llm_call_id = c.id AND p.decision = 'applied') AS changed
            FROM llm_call c
            WHERE c.parish_id = ? AND c.status IN ({", ".join("?" * len(SUCCEEDED))})
            ORDER BY c.id DESC LIMIT ?""",
        (parish_id, *SUCCEEDED, CHANGED_IN_A_ROW),
    ).fetchall()
    return len(calls) == CHANGED_IN_A_ROW and all(c["changed"] for c in calls)


def render_update_mode(section: dict[str, Any]) -> list[str]:
    """Markdown lines for the update-mode section (none when no update-mode parish ran)."""
    if not section["parishes"] and not section["gave_up"]:
        return []
    lines = [
        "", "### Update-mode parishes", "",
        f"{len(section['parishes'])} parishes read against their believed schedule: "
        f"{section['applied']} changes applied, {section['rejected']} rejected"
        + (
            " (" + ", ".join(f"{reason} {n}" for reason, n in
                             section["rejections_by_reason"].items()) + ")"
            if section["rejections_by_reason"] else ""
        ) + ".",
    ]
    for item in section["gave_up"]:
        lines.append(f"- **{item['parish_slug']}**: {item['detail']}")
    for parish in section["parishes"]:
        changed = bool(parish["applied"])
        if not (changed or parish["flags"] or parish["rejections"]):
            continue
        lines += ["", f"<details><summary><b>{parish['parish_slug']}</b>: "
                  f"{len(parish['applied'])} applied"
                  + (f", {sum(parish['rejections'].values())} rejected"
                     if parish["rejections"] else "")
                  + "</summary>", ""]
        for flag in parish["flags"]:
            lines.append(f"- ⚠️ {flag}")
        lines += _render_applied(parish["applied"])
        if parish["rejections"]:
            lines.append(
                "- Rejected: " + ", ".join(f"{r} {n}" for r, n in parish["rejections"].items())
            )
        lines += ["", "</details>"]
    for call in section["rejected_calls"]:
        lines += [
            "",
            f"**{call['parish_slug']}** call #{call['llm_call_id']} rejected whole as "
            f"`{call['reason']}` ({call['source_url']}):",
        ]
        for p in call["proposals"]:
            lines.append(
                f"- {p['op']}: {_change_text(p['before'], p['after'])}"
                + _source(p["page_number"], p["rationale"])
            )
    return lines


def _change_text(before: str | None, after: str | None) -> str:
    if before and after:
        return f"{before} → {after}"
    if after:
        return f"+ {after}"
    return f"− {before}"


def _source(page: int | None, rationale: str | None) -> str:
    bits = [f"p. {page}" if page else None, rationale]
    text = "; ".join(b for b in bits if b)
    return f" ({text})" if text else ""


def _render_applied(applied: list[dict[str, Any]]) -> list[str]:
    """Applied changes by church; a delete and an add of one slot side by side."""
    lines: list[str] = []
    by_church: dict[str, list[dict[str, Any]]] = {}
    for change in applied:
        by_church.setdefault(change["church_slug"] or "?", []).append(change)
    for church, changes in sorted(by_church.items()):
        lines.append(f"- `{church}`")
        used: set[int] = set()
        for i, change in enumerate(changes):
            if i in used:
                continue
            partner = None
            if change["op"] in ("add", "delete"):
                other_op = "add" if change["op"] == "delete" else "delete"
                partner = next(
                    (j for j, c in enumerate(changes)
                     if j not in used and j != i and c["op"] == other_op
                     and c["slot"] == change["slot"] and c["llm_call_id"] == change["llm_call_id"]),
                    None,
                )
            if partner is not None:
                used.add(partner)
                deleted, added = (
                    (change, changes[partner]) if change["op"] == "delete"
                    else (changes[partner], change)
                )
                lines.append(
                    f"  - replaced: {deleted['before']} → {added['after']}"
                    + _source(added["page_number"], added["rationale"])
                )
            else:
                lines.append(
                    f"  - {_change_text(change['before'], change['after'])}"
                    + _source(change["page_number"], change["rationale"])
                )
    return lines

