"""Apply the reviewed October 25 corrections to the recorded source state only.

Each parish's corrections are one human revision; the run's calls and decisions
stay as they were. See data/update-evals/2026-10-25/verification.md. A
correction names the run, the bulletin's content and the entries' content
(0012_oct25_review.json), never database ids. It is skipped when a change after
the call touched one of its slots, when the schedule no longer holds what it
replaces, or when a replacement would overlap an entry that stays.

Self-contained: entries are given, hashed and keyed as `schedule_entry` stood at
version 12, without the application's code, so later changes can't alter it.
"""

import json
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path

# schedule_entry's content columns at version 12, in hash order.
COLUMNS = (
    "church_id", "event_type", "event_kind", "day_of_week", "date", "start_time", "end_time",
    "cancelled", "weeks_of_month", "season_start_month", "season_start_day",
    "season_end_month", "season_end_day", "note", "valid_from", "valid_until",
)
EARLIEST, LATEST = "0001-01-01", "9999-12-31"


def _hash(e):
    # Entries without date bounds hash without those two columns.
    bounded = e["valid_from"] is not None or e["valid_until"] is not None
    content = [e[c] for c in COLUMNS if bounded or c not in ("valid_from", "valid_until")]
    return sha256(json.dumps(content).encode("utf-8")).hexdigest()


def _slot(e):
    anchor = e["day_of_week"] if e["event_kind"] == "weekly" else e["date"]
    return f"{e['church_id']}|{e['event_type']}|{e['event_kind']}|{anchor}|{e['start_time']}"


def _identity(e):
    if e["event_kind"] != "weekly":
        return _slot(e)
    qualifiers = ("weeks_of_month", "season_start_month", "season_start_day",
                  "season_end_month", "season_end_day")
    key = _slot(e) + "|" + "|".join(str(e[q] or 0) for q in qualifiers)
    if e["valid_from"] is not None or e["valid_until"] is not None:
        key += f"|{e['valid_from'] or ''}|{e['valid_until'] or ''}"
    return key


def _may_overlap(a, b):
    """Whether two entries may claim one occurrence. Disjoint weeks or seasons count as
    overlapping, which only ever skips a correction."""
    if _slot(a) != _slot(b):
        return False
    if a["event_kind"] != "weekly":
        return True
    return max(a["valid_from"] or EARLIEST, b["valid_from"] or EARLIEST) <= min(
        a["valid_until"] or LATEST, b["valid_until"] or LATEST,
    )


def _intern(conn, e):
    entry_hash = _hash(e)
    row = conn.execute("SELECT id FROM schedule_entry WHERE hash = ?", (entry_hash,)).fetchone()
    if row is not None:
        return row[0]
    return conn.execute(
        f"""INSERT INTO schedule_entry (hash, identity_key, {", ".join(COLUMNS)})
            VALUES (?, ?, {", ".join("?" * len(COLUMNS))})""",
        (entry_hash, _identity(e), *(e[c] for c in COLUMNS)),
    ).lastrowid


def _entries(conn, sql, params):
    rows = conn.execute(
        sql.format(columns=", ".join(f"e.{c}" for c in COLUMNS)), params,
    ).fetchall()
    return {row[0]: dict(zip(COLUMNS, row[1:], strict=True)) for row in rows}


def _correct(conn, run_id, case):
    call = conn.execute(
        """SELECT call.id, call.parish_id, call.bulletin_id, call.published_date,
                  call.call_date, COALESCE(rev.revision, call.base_revision)
           FROM llm_call call JOIN parish p ON p.id = call.parish_id
           JOIN bulletin b ON b.id = call.bulletin_id
           LEFT JOIN schedule_revision rev ON rev.llm_call_id = call.id
           WHERE p.slug = ? AND call.run_id = ? AND b.content_hash = ?
             AND call.status IN ('ok', 'lenient')""",
        (case["parish"], run_id, case["content_hash"]),
    ).fetchone()
    if call is None:
        return
    _, parish_id, bulletin_id, published_date, call_date, source_revision = call
    churches = dict(conn.execute(
        "SELECT slug, id FROM church WHERE parish_id = ? AND retired_at IS NULL", (parish_id,),
    ).fetchall())
    live = _entries(
        conn, """SELECT e.id, {columns} FROM current_schedule s
                 JOIN schedule_entry e ON e.id = s.entry_id WHERE s.parish_id = ?""",
        (parish_id,),
    )
    touched = {_slot(e) for e in _entries(
        conn, """SELECT e.id, {columns} FROM schedule_change sc JOIN schedule_entry e
                 ON e.id IN (sc.before_entry_id, sc.after_entry_id)
                 WHERE sc.parish_id = ? AND sc.revision > ?""",
        (parish_id, source_revision),
    ).values()}
    changes = []
    sightings = []
    for repair in case["repairs"]:
        raw = repair["before"] + repair["after"]
        if any(e["church_slug"] not in churches for e in raw):
            continue
        before, after = (
            [{**e, "church_id": churches[e["church_slug"]]} for e in entries]
            for entries in (repair["before"], repair["after"])
        )
        if any(_slot(e) in touched for e in before + after):
            continue
        targets = [next((i for i, e in live.items() if all(e[c] == old[c] for c in COLUMNS)),
                        None) for old in before]
        if None in targets:
            continue
        remaining = [e for i, e in live.items() if i not in targets]
        if any(_may_overlap(new, old) for new in after for old in remaining):
            continue
        for target in targets:
            changes.append(("delete", target, None))
            del live[target]
        for entry in after:
            entry_id = _intern(conn, entry)
            changes.append(("add", None, entry_id))
            live[entry_id] = entry
            # Only the replacement actually printed in the source earns a sighting.
            if not entry["valid_from"] or entry["valid_from"] <= (published_date or call_date):
                sightings.append((bulletin_id, entry_id, repair["page"]))
    if not changes:
        return
    revision = conn.execute(
        "SELECT MAX(revision) + 1 FROM schedule_revision WHERE parish_id = ?", (parish_id,),
    ).fetchone()[0]
    conn.execute(
        """INSERT INTO schedule_revision (parish_id, revision, source_kind, actor, note, created_at)
           VALUES (?, ?, 'human', 'weekly-run-review', ?, ?)""",
        (parish_id, revision, f"October 25 source review ({run_id}); see verification.md",
         datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")),
    )
    for op, before_id, after_id in changes:
        conn.execute(
            """INSERT INTO schedule_change (parish_id, revision, op, before_entry_id, after_entry_id)
               VALUES (?, ?, ?, ?, ?)""",
            (parish_id, revision, op, before_id, after_id),
        )
        if before_id is not None:
            conn.execute(
                "DELETE FROM current_schedule WHERE parish_id = ? AND entry_id = ?",
                (parish_id, before_id),
            )
        if after_id is not None:
            conn.execute(
                """INSERT INTO current_schedule (parish_id, entry_id, identity_key, since_revision)
                   SELECT ?, id, identity_key, ? FROM schedule_entry WHERE id = ?""",
                (parish_id, revision, after_id),
            )
    conn.executemany(
        "INSERT OR IGNORE INTO entry_sighting (bulletin_id, entry_id, page_number) "
        "VALUES (?, ?, ?)", sightings,
    )


def migrate(conn):
    spec = json.loads(Path(__file__).with_suffix(".json").read_text(encoding="utf-8"))
    for case in spec["parishes"]:
        _correct(conn, spec["run_id"], case)
