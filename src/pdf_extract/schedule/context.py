"""Short reviewed decisions from the approved seed that initialized this schedule.

Keep exclusions and unusual included slots visible to the updater without
turning an old draft summary into instructions or replacing the live schedule.
The caller includes this in the stored, hashed schedule view.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from pdf_extract.seeding.files import APPROVED, SETTLED, read_seed, revision_note


def reviewed_seed_context(conn: sqlite3.Connection, parish_id: int) -> dict[str, Any] | None:
    row = conn.execute("SELECT slug FROM parish WHERE id = ?", (parish_id,)).fetchone()
    seed = read_seed(row["slug"]) if row is not None else None
    if seed is None or seed.get("status") != APPROVED:
        return None
    latest = conn.execute(
        """SELECT note FROM schedule_revision WHERE parish_id = ? AND source_kind = 'seed'
           ORDER BY revision DESC LIMIT 1""", (parish_id,),
    ).fetchone()
    if latest is None or latest["note"] != revision_note(seed):
        # An unimported edit or a newer manual seed must not supply older decisions.
        return None
    decisions = []
    for slot in seed.get("slots", []):
        if slot.get("status") != SETTLED:
            continue
        entry = slot.get("entry") or {}
        if not (slot.get("answer") or slot.get("decision") == "exclude"
                or entry.get("weeks_of_month") or entry.get("season")):
            continue
        decisions.append({
            key: slot.get(key) for key in
            ("id", "decision", "entry", "rationale", "sources", "question", "answer")
        })
    if not decisions:
        return None
    return {"as_of": seed["as_of"], "reviewer": seed["reviewer"], "decisions": decisions}
