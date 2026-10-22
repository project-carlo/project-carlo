"""The believed-schedule tables: entries, revisions, the change log and its fold.

The change log (`schedule_change`, grouped into `schedule_revision`s) is the
source of truth. `current_schedule` is the log replayed in order: a revision is
appended and then folded in (`append_revision`), nothing else writes it, and
`rebuild_current_schedule` replays the log from scratch to check or restore it.

None of these functions commits: callers group them into one transaction.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from hashlib import sha256
from typing import Any

from pdf_extract.labeling.labels import DAYS
from pdf_extract.schedule.entries import ENTRY_COLUMNS, Entry, entry_from_row
from pdf_extract.storage import utc_now_iso

SEED = "seed"
LLM = "llm"
HUMAN = "human"
REFERENCE = "reference"

ADD = "add"
MODIFY = "modify"
DELETE = "delete"


def sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    """Sorted keys, no whitespace: the same value always hashes the same."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


# ── Entries ─────────────────────────────────────────────────────────────────
def intern_entry(conn: sqlite3.Connection, entry: Entry) -> int:
    """The id of the `schedule_entry` holding exactly this content, adding it if new."""
    entry_hash = entry.hash
    row = conn.execute("SELECT id FROM schedule_entry WHERE hash = ?", (entry_hash,)).fetchone()
    if row is not None:
        return int(row[0])
    values = [getattr(entry, name) for name in ENTRY_COLUMNS]
    cursor = conn.execute(
        f"""INSERT INTO schedule_entry (hash, identity_key, {", ".join(ENTRY_COLUMNS)})
            VALUES (?, ?, {", ".join("?" * len(ENTRY_COLUMNS))})""",
        (entry_hash, entry.identity_key, *values),
    )
    return int(cursor.lastrowid)


def load_entries(conn: sqlite3.Connection, entry_ids: Iterable[int]) -> dict[int, Entry]:
    ids = sorted(set(entry_ids))
    out: dict[int, Entry] = {}
    for start in range(0, len(ids), 500):
        chunk = ids[start:start + 500]
        rows = conn.execute(
            f"SELECT id, {', '.join(ENTRY_COLUMNS)} FROM schedule_entry"
            f" WHERE id IN ({', '.join('?' * len(chunk))})",
            chunk,
        ).fetchall()
        out.update({row["id"]: entry_from_row(row) for row in rows})
    return out


# ── Parishes and churches ───────────────────────────────────────────────────
def update_mode_parishes(conn: sqlite3.Connection) -> dict[int, str]:
    """Parish id -> its latest seed's `as_of`, for every parish in update mode.

    A parish is in update mode exactly when it has a seed revision.
    """
    rows = conn.execute(
        """SELECT parish_id, as_of FROM schedule_revision r
           WHERE source_kind = 'seed' AND revision = (
               SELECT MAX(revision) FROM schedule_revision
               WHERE parish_id = r.parish_id AND source_kind = 'seed'
           )"""
    ).fetchall()
    return {row["parish_id"]: row["as_of"] for row in rows}


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,),
    ).fetchone() is not None


def update_mode_slugs(conn: sqlite3.Connection) -> set[str]:
    """Slugs of the parishes in update mode (none in a database before migration 4)."""
    if not table_exists(conn, "schedule_revision"):
        return set()
    rows = conn.execute(
        """SELECT DISTINCT p.slug FROM schedule_revision r JOIN parish p ON p.id = r.parish_id
           WHERE r.source_kind = 'seed'"""
    ).fetchall()
    return {row[0] for row in rows}


def is_update_mode(conn: sqlite3.Connection, parish_id: int) -> bool:
    return conn.execute(
        "SELECT 1 FROM schedule_revision WHERE parish_id = ? AND source_kind = 'seed' LIMIT 1",
        (parish_id,),
    ).fetchone() is not None


def parish_churches(conn: sqlite3.Connection, parish_id: int) -> dict[str, int]:
    """Slug -> id of the parish's churches a proposal may name: retired ones left out."""
    rows = conn.execute(
        "SELECT id, slug FROM church WHERE parish_id = ? AND retired_at IS NULL",
        (parish_id,),
    ).fetchall()
    return {row["slug"]: row["id"] for row in rows}


def church_slugs(conn: sqlite3.Connection, church_ids: Iterable[int]) -> dict[int, str]:
    ids = sorted(set(church_ids))
    if not ids:
        return {}
    rows = conn.execute(
        f"SELECT id, slug FROM church WHERE id IN ({', '.join('?' * len(ids))})", ids,
    ).fetchall()
    return {row["id"]: row["slug"] for row in rows}


# ── The current schedule ────────────────────────────────────────────────────
def live_entries(conn: sqlite3.Connection, parish_id: int) -> dict[int, Entry]:
    """Entry id -> content of every entry the parish's current schedule holds.

    Dated entries in the past are still live: they expire from the view and the
    snapshot, never from the schedule.
    """
    rows = conn.execute(
        f"""SELECT e.id, {", ".join(f"e.{c}" for c in ENTRY_COLUMNS)}
            FROM current_schedule s JOIN schedule_entry e ON e.id = s.entry_id
            WHERE s.parish_id = ?""",
        (parish_id,),
    ).fetchall()
    return {row["id"]: entry_from_row(row) for row in rows}


def current_revision(conn: sqlite3.Connection, parish_id: int) -> int:
    """The parish's latest revision number, 0 when it has none."""
    row = conn.execute(
        "SELECT MAX(revision) FROM schedule_revision WHERE parish_id = ?", (parish_id,),
    ).fetchone()
    return int(row[0] or 0)


def _view_order(entry: Entry, slug: str) -> tuple:
    anchor = (
        (DAYS.index(entry.day_of_week), "") if entry.weekly
        else (len(DAYS), entry.date or "")
    )
    return (slug, 0 if entry.weekly else 1, anchor, entry.start_time, entry.event_type)


def render_view(
    conn: sqlite3.Connection, parish_id: int, call_date: date,
) -> tuple[str, str]:
    """The parish's believed schedule as the model is shown it: (canonical JSON, sha256).

    Dated entries before `call_date` are left out. Entries are grouped by
    church (every non-retired church is listed, even with no entries), then
    ordered weekly before dated, by weekday or date, then time.
    """
    # Imported here because seed-file helpers share this module's JSON/hash helpers.
    from pdf_extract.schedule.context import reviewed_seed_context

    live = live_entries(conn, parish_id)
    churches = parish_churches(conn, parish_id)
    slugs = church_slugs(conn, [e.church_id for e in live.values()])
    by_church: dict[str, list[tuple[tuple, dict[str, Any]]]] = {slug: [] for slug in churches}
    for entry_id, entry in live.items():
        if entry.dated_before(call_date):
            continue
        slug = slugs[entry.church_id]
        by_church.setdefault(slug, []).append((_view_order(entry, slug), entry.view(entry_id)))
    view = {
        "churches": [
            {"slug": slug, "entries": [item for _, item in sorted(items, key=lambda i: i[0])]}
            for slug, items in sorted(by_church.items())
        ]
    }
    context = reviewed_seed_context(conn, parish_id)
    if context is not None:
        view["reviewed_seed_context"] = context
    text = canonical_json(view)
    return text, sha256_text(text)


def store_view(conn: sqlite3.Connection, text: str) -> str:
    view_hash = sha256_text(text)
    conn.execute(
        "INSERT OR IGNORE INTO schedule_view (hash, json) VALUES (?, ?)", (view_hash, text),
    )
    return view_hash


def store_prompt_blob(conn: sqlite3.Connection, kind: str, text: str) -> str:
    blob_hash = sha256_text(text)
    conn.execute(
        "INSERT OR IGNORE INTO prompt_blob (hash, kind, text) VALUES (?, ?, ?)",
        (blob_hash, kind, text),
    )
    return blob_hash


# ── Revisions and the log ───────────────────────────────────────────────────
@dataclass(frozen=True)
class Change:
    """One `schedule_change` row to append."""

    op: str
    before_entry_id: int | None = None
    after_entry_id: int | None = None
    proposed_change_id: int | None = None


def normalize_as_of(value: str) -> str:
    """A seed's `as_of` in the form `fetched_at` is stored in, so the two compare as text.

    Takes an ISO time (`Z` or an offset; none means UTC) or a date, which
    means the end of that day: everything fetched that day is in the seed.
    """
    text = value.strip()
    try:
        if len(text) == 10:
            moment = datetime.combine(date.fromisoformat(text), time(23, 59, 59), UTC)
        else:
            moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=UTC)
    except ValueError as exc:
        raise ValueError(f"as_of must be an ISO date or time, not {value!r}") from exc
    return moment.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def append_revision(
    conn: sqlite3.Connection,
    parish_id: int,
    *,
    source_kind: str,
    changes: list[Change],
    llm_call_id: int | None = None,
    run_id: str | None = None,
    actor: str | None = None,
    note: str | None = None,
    as_of: str | None = None,
) -> int:
    """Append a revision with its changes to the log and fold it in. Returns its number.

    A seed's `as_of` defaults to its creation time; other kinds have none.
    """
    revision = current_revision(conn, parish_id) + 1
    created_at = utc_now_iso()
    if source_kind == SEED:
        as_of = created_at if as_of is None else normalize_as_of(as_of)
    conn.execute(
        """INSERT INTO schedule_revision (
               parish_id, revision, source_kind, llm_call_id, run_id, actor, note, as_of,
               created_at
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (parish_id, revision, source_kind, llm_call_id, run_id, actor, note,
         as_of if source_kind == SEED else None, created_at),
    )
    conn.executemany(
        """INSERT INTO schedule_change (
               parish_id, revision, op, before_entry_id, after_entry_id, proposed_change_id
           ) VALUES (?, ?, ?, ?, ?, ?)""",
        [
            (parish_id, revision, c.op, c.before_entry_id, c.after_entry_id,
             c.proposed_change_id)
            for c in changes
        ],
    )
    fold_revision(conn, parish_id, revision)
    return revision


def _fold_change(
    conn: sqlite3.Connection, parish_id: int, revision: int, row: sqlite3.Row,
) -> None:
    if row["before_entry_id"] is not None:
        deleted = conn.execute(
            "DELETE FROM current_schedule WHERE parish_id = ? AND entry_id = ?",
            (parish_id, row["before_entry_id"]),
        ).rowcount
        if not deleted:
            raise ValueError(
                f"revision {revision} of parish {parish_id} changes entry "
                f"{row['before_entry_id']}, which is not in its current schedule"
            )
    if row["after_entry_id"] is not None:
        entry = load_entries(conn, [row["after_entry_id"]])[row["after_entry_id"]]
        if any(entry.conflicts_with(other) for other in live_entries(conn, parish_id).values()):
            raise ValueError(f"the schedule already has an entry for that slot: {entry.slot_key}")
        conn.execute(
            """INSERT INTO current_schedule (parish_id, entry_id, identity_key, since_revision)
               SELECT ?, id, identity_key, ? FROM schedule_entry WHERE id = ?""",
            (parish_id, revision, row["after_entry_id"]),
        )


def fold_revision(conn: sqlite3.Connection, parish_id: int, revision: int) -> None:
    """Fold one appended revision into `current_schedule`, in log order."""
    rows = conn.execute(
        """SELECT before_entry_id, after_entry_id FROM schedule_change
           WHERE parish_id = ? AND revision = ? ORDER BY id""",
        (parish_id, revision),
    ).fetchall()
    for row in rows:
        _fold_change(conn, parish_id, revision, row)


def rebuild_current_schedule(
    conn: sqlite3.Connection, parish_ids: Iterable[int] | None = None,
) -> dict[str, int]:
    """Replay the log from scratch into `current_schedule`.

    Returns how many parishes were rebuilt and how many current rows differed
    from the replay (0 when the table already matched the log).
    """
    if parish_ids is None:
        parish_ids = [
            row[0] for row in
            conn.execute("SELECT DISTINCT parish_id FROM schedule_revision").fetchall()
        ]
    differing = 0
    rebuilt = 0
    for parish_id in parish_ids:
        before = set(conn.execute(
            "SELECT entry_id, since_revision FROM current_schedule WHERE parish_id = ?",
            (parish_id,),
        ).fetchall())
        conn.execute("DELETE FROM current_schedule WHERE parish_id = ?", (parish_id,))
        for row in conn.execute(
            """SELECT revision, before_entry_id, after_entry_id FROM schedule_change
               WHERE parish_id = ? ORDER BY revision, id""",
            (parish_id,),
        ).fetchall():
            _fold_change(conn, parish_id, row["revision"], row)
        after = set(conn.execute(
            "SELECT entry_id, since_revision FROM current_schedule WHERE parish_id = ?",
            (parish_id,),
        ).fetchall())
        differing += len(set(map(tuple, before)) ^ set(map(tuple, after)))
        rebuilt += 1
    return {"parishes": rebuilt, "differing_rows": differing}


# ── Sightings ───────────────────────────────────────────────────────────────
def replace_sightings(
    conn: sqlite3.Connection,
    bulletin_id: int,
    sightings: Iterable[tuple[int, int | None]],
    *,
    llm_call_id: int | None,
) -> int:
    """Make (entry id, page) the bulletin's sightings, dropping any it had."""
    conn.execute("DELETE FROM entry_sighting WHERE bulletin_id = ?", (bulletin_id,))
    pages: dict[int, int | None] = {}
    for entry_id, page in sightings:
        if pages.get(entry_id) is None:
            pages[entry_id] = page
    conn.executemany(
        """INSERT INTO entry_sighting (bulletin_id, entry_id, page_number, llm_call_id)
           VALUES (?, ?, ?, ?)""",
        [(bulletin_id, entry_id, page, llm_call_id) for entry_id, page in pages.items()],
    )
    return len(pages)


# ── Seeds ───────────────────────────────────────────────────────────────────
def seed_changes(
    conn: sqlite3.Connection, live: dict[int, Entry], entries: list[Entry],
) -> list[Change]:
    """The adds, modifies and deletes that turn `live` into exactly `entries`.

    Match recurrence identities first. A single unmatched old/new pair at an
    unqualified slot is a qualifier modify. Ambiguous splits/merges use deletes
    and adds, with deletions first so no temporary overlap enters the fold.
    """
    by_identity: dict[str, Entry] = {}
    for entry in entries:
        if any(entry.conflicts_with(other) for other in by_identity.values()):
            raise ValueError(f"two seed entries are the same slot: {entry.slot_key}")
        by_identity[entry.identity_key] = entry
    live_by_identity = {entry.identity_key: entry_id for entry_id, entry in live.items()}
    matched = {identity: live_by_identity[identity]
               for identity in by_identity.keys() & live_by_identity.keys()}
    old_by_slot: dict[str, list[int]] = {}
    new_by_slot: dict[str, list[str]] = {}
    for entry_id, entry in live.items():
        if entry.identity_key not in matched:
            old_by_slot.setdefault(entry.slot_key, []).append(entry_id)
    for identity, entry in by_identity.items():
        if identity not in matched:
            new_by_slot.setdefault(entry.slot_key, []).append(identity)
    for slot, identities in new_by_slot.items():
        old_ids = old_by_slot.get(slot, [])
        if len(identities) == len(old_ids) == 1:
            matched[identities[0]] = old_ids[0]
    retained = set(matched.values())
    changes: list[Change] = []
    for entry_id in sorted(live):
        if entry_id not in retained:
            changes.append(Change(DELETE, before_entry_id=entry_id))
    for identity, entry in sorted(by_identity.items()):
        new_id = intern_entry(conn, entry)
        old_id = matched.get(identity)
        if old_id is None:
            changes.append(Change(ADD, after_entry_id=new_id))
        elif old_id != new_id:
            changes.append(Change(MODIFY, before_entry_id=old_id, after_entry_id=new_id))
    return changes


def write_seed(
    conn: sqlite3.Connection,
    parish_id: int,
    entries: list[Entry],
    *,
    as_of: str | None = None,
    actor: str | None = None,
    note: str | None = None,
    run_id: str | None = None,
    sightings: Iterable[tuple[int, Entry, int | None]] = (),
) -> int:
    """Write a seed revision making the parish's schedule exactly `entries`.

    The first seed switches the parish to update mode; a later one is a new
    seed revision of the adds, modifies and deletes against what is believed
    now, with its own `as_of`. `sightings` are (bulletin id, entry, page) for
    entries whose bulletin the seeding method knows. Returns the revision.
    Initial population itself is out of scope (docs/schedule-state-plan.md);
    this is what such a method calls.
    """
    changes = seed_changes(conn, live_entries(conn, parish_id), entries)
    revision = append_revision(
        conn, parish_id, source_kind=SEED, changes=changes, run_id=run_id, actor=actor,
        note=note, as_of=as_of,
    )
    conn.executemany(
        """INSERT OR REPLACE INTO entry_sighting (bulletin_id, entry_id, page_number, llm_call_id)
           VALUES (?, ?, ?, NULL)""",
        [(bulletin_id, intern_entry(conn, entry), page) for bulletin_id, entry, page in sightings],
    )
    return revision
