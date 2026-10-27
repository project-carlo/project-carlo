"""Guarded, source-specific human repairs without rewriting model history.

A repair names the original run, bulletin content and expected entry content,
never installation-specific ids. Later decisions touching the affected slots
win, including a reviewer removing and then restoring identical content.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from pdf_extract.schedule.entries import parse_entry
from pdf_extract.schedule.store import (
    HUMAN,
    Change,
    append_revision,
    intern_entry,
    live_entries,
    load_entries,
    parish_churches,
)


def apply_review(conn: sqlite3.Connection, spec: dict[str, Any]) -> int:
    """Append at most one human revision per parish. Caller owns the transaction."""
    applied = 0
    for case in spec["parishes"]:
        call = conn.execute(
            """SELECT call.*, COALESCE(rev.revision, call.base_revision) AS source_revision
               FROM llm_call call JOIN parish p ON p.id = call.parish_id
               JOIN bulletin b ON b.id = call.bulletin_id
               LEFT JOIN schedule_revision rev ON rev.llm_call_id = call.id
               WHERE p.slug = ? AND call.run_id = ? AND b.content_hash = ?
                 AND call.status IN ('ok', 'lenient')""",
            (case["parish"], spec["run_id"], case["content_hash"]),
        ).fetchone()
        if call is None:
            continue
        pid = call["parish_id"]
        churches = parish_churches(conn, pid)
        live = live_entries(conn, pid)
        changes = []
        sightings = []
        for repair in case["repairs"]:
            raw_before = repair.get("before", [])
            raw_after = repair.get("after", [])
            if any(e["church_slug"] not in churches for e in raw_before + raw_after):
                continue
            before = [parse_entry(e, churches) for e in raw_before]
            after = [parse_entry(e, churches) for e in raw_after]
            affected = before + after
            slots = {e.slot_key for e in affected}
            touched = conn.execute(
                """SELECT sc.before_entry_id, sc.after_entry_id FROM schedule_change sc
                   WHERE sc.parish_id = ? AND sc.revision > ?""",
                (pid, call["source_revision"]),
            ).fetchall()
            entries = load_entries(conn, [i for row in touched for i in row if i is not None])
            if any(e.slot_key in slots for e in entries.values()):
                continue
            targets = [next((i for i, e in live.items() if e == old), None) for old in before]
            if None in targets:
                continue
            remaining = {i: e for i, e in live.items() if i not in targets}
            if any(e.conflicts_with(other) for e in after for other in remaining.values()):
                continue
            if any(a.conflicts_with(b) for n, a in enumerate(after) for b in after[n + 1:]):
                raise ValueError("review contains overlapping replacement entries")
            for target in targets:
                changes.append(Change("delete", before_entry_id=target))
                live.pop(target)
            for entry in after:
                entry_id = intern_entry(conn, entry)
                changes.append(Change("add", after_entry_id=entry_id))
                live[entry_id] = entry
                # Only the replacement actually printed in the source earns a sighting.
                if not entry.valid_from or entry.valid_from <= (call["published_date"] or call["call_date"]):
                    sightings.append((call["bulletin_id"], entry_id, repair["page"]))
        if changes:
            append_revision(
                conn, pid, source_kind=HUMAN, actor="weekly-run-review",
                note=f"October 25 source review ({spec['run_id']}); see verification.md",
                changes=changes,
            )
            conn.executemany(
                "INSERT OR IGNORE INTO entry_sighting (bulletin_id, entry_id, page_number) "
                "VALUES (?, ?, ?)", sightings,
            )
            applied += len(changes)
    return applied
