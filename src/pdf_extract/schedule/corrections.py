"""Corrections: reviewed hand edits to believed schedules, committed as files.

A person's correction to a live schedule is a file in `data/corrections/`,
reviewed in a pull request, that pipeline commands load the way they load
approved seeds (`seeding.loader`). Migrations stay schema only.

    data/corrections/<parish-slug>/<YYYY-MM-DD>-<short-name>.json

    {
      "parish": "st-mary-albany",
      "actor": "luke",
      "note": "Page 2 still lists the 11:00 Mass; the October 25 run removed it.",
      "as_of": "2026-10-25T13:20:11Z",
      "operations": [
        {"op": "add", "after": {...}},
        {"op": "modify", "before": {...}, "after": {...}},
        {"op": "delete", "before": {...}},
        {"op": "apply", "run_id": "...", "content_hash": "...", "seq": [1, 3]},
        {"op": "wrong_bulletin", "content_hash": "..."}
      ]
    }

Everything is addressed by content, never by database ids: entries in the
labels' form (as `pnpm schedule add --entry` takes them), a call by its run and
its bulletin's content hash, a bulletin by its content hash. `as_of` is the
schedule the correction was made against: the time of the parish's newest
model (`llm`) revision then, or its seed's `as_of` if that is later (an ISO
time, or a date for the end of that day).

Only model revisions count as changes since `as_of`. They are written once, by
the weekly run, and a pulled database carries their times. Seeds, corrections
and the CSVs' `reference` revisions come from committed files and are written
again, with a new time, into every database that loads them (the author's, each
deploy's, the published one), so their times say nothing about what the author
saw. A conflict with one of those shows as a `before` no longer in the schedule,
or a failed check.

- **Once per digest.** A file is loaded as one `human` revision whose note
  carries the digest of its parish, `as_of` and operations (`correction_digest`),
  so loading it again does nothing and editing its note does not load it again.
  A file of only `wrong_bulletin` marks still writes one (empty) revision, so
  every loaded file is recorded the same way.
- **All or nothing.** The schedule operations are checked in order, with the
  hand edits' per-proposal checks (`policy.check_in_order`). The file is skipped
  and reported, not forced, when any operation fails: a `before` the schedule
  no longer holds, a slot a model revision after `as_of` touched (for `apply`,
  one after the call other than the call's own), a call, proposal or bulletin
  the database doesn't have, or a bulletin not processed yet. A skipped file is
  tried again by every command until it loads or is removed.

`write_correction` writes a file from what `pnpm schedule ... --write-correction`
was given; `load_corrections` loads every file not loaded yet.
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.classifiers.schedule_update import _without_nulls
from pdf_extract.labeling.labels import is_valid_hash, is_valid_slug
from pdf_extract.paths import DATA_DIR
from pdf_extract.schedule.entries import Entry, EntryError, parse_entry
from pdf_extract.schedule.history import SUCCEEDED
from pdf_extract.schedule.policy import APPLIED, Schedule, check_in_order
from pdf_extract.schedule.store import (
    ADD,
    DELETE,
    HUMAN,
    LLM,
    MODIFY,
    Change,
    append_revision,
    canonical_json,
    church_slugs,
    intern_entry,
    is_update_mode,
    live_entries,
    load_entries,
    normalize_as_of,
    parish_churches,
    retire_ended,
    sha256_text,
)

LOGGER = logging.getLogger(__name__)

CORRECTIONS_DIR = DATA_DIR / "corrections"

APPLY = "apply"
WRONG_BULLETIN = "wrong_bulletin"
OPS = (ADD, MODIFY, DELETE, APPLY, WRONG_BULLETIN)

# Why a file is skipped, besides the policy's per-proposal reasons.
INVALID_FILE = "invalid_file"
NOT_SEEDED = "not_seeded"
NOT_IN_SCHEDULE = "not_in_schedule"
CHANGED_SINCE = "changed_since"
UNKNOWN_CALL = "unknown_call"
UNKNOWN_PROPOSAL = "unknown_proposal"
UNKNOWN_BULLETIN = "unknown_bulletin"
NOT_PROCESSED = "not_processed"

FILE_KEYS = ("parish", "actor", "note", "as_of", "operations")
OP_KEYS = {
    ADD: ({"after"}, set()),
    MODIFY: ({"before", "after"}, set()),
    DELETE: ({"before"}, set()),
    APPLY: ({"run_id", "content_hash"}, {"seq"}),
    WRONG_BULLETIN: ({"content_hash"}, set()),
}
_NAME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.json$")
_MARKER_RE = re.compile(r"\[correction ([0-9a-f]{64})\]")


class CorrectionFileError(ValueError):
    """A correction file that can't be read, or is not in the expected shape."""


class Skip(Exception):  # noqa: N818 (a reason to skip, not an error)
    """A correction that can't be applied to this database: `reason` and `detail`."""

    def __init__(self, reason: str, detail: str) -> None:
        super().__init__(f"{reason}: {detail}")
        self.reason = reason
        self.detail = detail


# ── The file ────────────────────────────────────────────────────────────────
def check_shape(data: Any, *, parish_slug: str | None = None) -> list[str]:
    """What is wrong with a correction's shape (not its content), as messages."""
    if not isinstance(data, dict):
        return ["the file must hold a JSON object"]
    errors = []
    missing = [k for k in FILE_KEYS if k not in data]
    extra = sorted(set(data) - set(FILE_KEYS))
    if missing:
        errors.append(f"missing {', '.join(missing)}")
    if extra:
        errors.append(f"unknown keys {', '.join(extra)}")
    if not is_valid_slug(data.get("parish")):
        errors.append("parish must be a parish slug")
    elif parish_slug is not None and data["parish"] != parish_slug:
        errors.append(f"parish is {data['parish']!r} but the file is in {parish_slug}/")
    for key in ("actor", "note"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key} must be non-empty text")
    if not isinstance(data.get("as_of"), str):
        errors.append("as_of must be an ISO date or time")
    else:
        try:
            normalize_as_of(data["as_of"])
        except ValueError as exc:
            errors.append(str(exc))
    operations = data.get("operations")
    if not isinstance(operations, list) or not operations:
        errors.append("operations must be a non-empty list")
        return errors
    for i, op in enumerate(operations):
        where = f"operation {i + 1}"
        if not isinstance(op, dict) or op.get("op") not in OPS:
            errors.append(f"{where}: op must be one of {', '.join(OPS)}")
            continue
        required, optional = OP_KEYS[op["op"]]
        keys = set(op) - {"op"}
        if required - keys:
            errors.append(f"{where}: missing {', '.join(sorted(required - keys))}")
        if keys - required - optional:
            errors.append(f"{where}: unknown keys {', '.join(sorted(keys - required - optional))}")
        for key in ("before", "after"):
            if key in op and not isinstance(op[key], dict):
                errors.append(f"{where}: {key} must be an entry object")
        if "content_hash" in op and not is_valid_hash(op["content_hash"]):
            errors.append(f"{where}: content_hash must be a sha256 hex digest")
        if "run_id" in op and (not isinstance(op["run_id"], str) or not op["run_id"]):
            errors.append(f"{where}: run_id must be text")
        if "seq" in op and not (
            isinstance(op["seq"], list) and op["seq"]
            and all(isinstance(s, int) and not isinstance(s, bool) for s in op["seq"])
        ):
            errors.append(f"{where}: seq must be a non-empty list of numbers")
    return errors


def read_correction(path: Path) -> dict[str, Any]:
    """Read and shape-check one correction file. Raises CorrectionFileError."""
    if not _NAME_RE.match(path.name):
        raise CorrectionFileError(
            f"{path.name}: the name must be <YYYY-MM-DD>-<short-name>.json, in lowercase"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CorrectionFileError(f"{path.name}: {exc}") from exc
    errors = check_shape(data, parish_slug=path.parent.name)
    if errors:
        raise CorrectionFileError("; ".join(errors[:3]))
    return data


def correction_files(corrections_dir: Path = CORRECTIONS_DIR) -> list[Path]:
    """Every correction file, by parish and then by name (so by date)."""
    if not corrections_dir.is_dir():
        return []
    return sorted(corrections_dir.glob("*/*.json"))


def correction_digest(data: dict[str, Any]) -> str:
    """A digest of what loading the file does: its parish, `as_of` and operations."""
    return sha256_text(canonical_json({
        "parish": data["parish"],
        "as_of": normalize_as_of(data["as_of"]),
        "operations": data["operations"],
    }))


def _marker(digest: str) -> str:
    return f"[correction {digest}]"


def revision_note(data: dict[str, Any], path: Path) -> str:
    """The note on the revision a file makes: its own note, its file and its digest."""
    return f"{data['note'].strip()} ({path.parent.name}/{path.name}) {_marker(correction_digest(data))}"


def loaded_digests(conn: sqlite3.Connection) -> set[tuple[int, str]]:
    """(parish id, digest) of every correction the database has a revision for."""
    rows = conn.execute(
        """SELECT parish_id, note FROM schedule_revision
           WHERE source_kind = 'human' AND note LIKE '%[correction %'""",
    ).fetchall()
    return {(int(r[0]), d) for r in rows for d in _MARKER_RE.findall(r[1])}


def is_loaded(conn: sqlite3.Connection, parish_id: int, data: dict[str, Any]) -> bool:
    """Whether the parish has a revision made by a file with this content."""
    return (parish_id, correction_digest(data)) in loaded_digests(conn)


def check_bulletin(conn: sqlite3.Connection, parish_id: int, content_hash: str) -> None:
    """Raise Skip unless the parish has a processed bulletin with this hash to mark wrong.

    An unprocessed one is left alone: processing it would set the flag from the
    model's answer and undo the mark.
    """
    rows = conn.execute(
        "SELECT processed_at FROM bulletin WHERE parish_id = ? AND content_hash = ?",
        (parish_id, content_hash),
    ).fetchall()
    if not rows:
        raise Skip(UNKNOWN_BULLETIN, "the parish has no bulletin with that hash")
    if any(r[0] is None for r in rows):
        raise Skip(NOT_PROCESSED, "the bulletin isn't processed yet; it is marked once it is")


def mark_wrong_bulletin(conn: sqlite3.Connection, parish_id: int, content_hash: str) -> int:
    """Mark the parish's bulletin with this hash as not its own. Returns the rows marked."""
    return conn.execute(
        "UPDATE bulletin SET wrong_bulletin = 1 WHERE parish_id = ? AND content_hash = ?",
        (parish_id, content_hash),
    ).rowcount


# ── Loading ─────────────────────────────────────────────────────────────────
@dataclass
class _Op:
    """One schedule change to check: (op, target id, raw entry) for `check_in_order`."""

    index: int
    op: str
    target: int | None
    raw: Any
    since: int | None = None
    """The revision after which a touched slot makes it stale (None: after `as_of`)."""
    call_id: int | None = None
    """apply: the call, whose own revision doesn't count as a change since it."""
    proposed_change_id: int | None = None


def _entry(raw: Any, churches: dict[str, int], where: str) -> Entry:
    try:
        return parse_entry(raw, churches)
    except EntryError as exc:
        raise Skip(exc.reason, f"{where}: {exc}") from exc


def _find_live(live: dict[int, Entry], entry: Entry, where: str) -> int:
    for entry_id, other in live.items():
        if other == entry:
            return entry_id
    raise Skip(NOT_IN_SCHEDULE, f"{where}: the schedule no longer holds the entry it replaces")


def _call_ops(
    conn: sqlite3.Connection, parish_id: int, index: int, op: dict[str, Any],
) -> list[_Op]:
    where = f"operation {index + 1}"
    call = conn.execute(
        f"""SELECT c.id, c.base_revision FROM llm_call c JOIN bulletin b ON b.id = c.bulletin_id
            WHERE c.parish_id = ? AND c.run_id = ? AND b.content_hash = ?
              AND c.status IN ({", ".join("?" * len(SUCCEEDED))})
            ORDER BY c.id DESC LIMIT 1""",
        (parish_id, op["run_id"], op["content_hash"], *SUCCEEDED),
    ).fetchone()
    if call is None:
        raise Skip(UNKNOWN_CALL, f"{where}: no call of run {op['run_id']} for that bulletin")
    rows = conn.execute(
        "SELECT * FROM proposed_change WHERE llm_call_id = ? ORDER BY seq", (call["id"],),
    ).fetchall()
    if "seq" in op:
        wanted = set(op["seq"])
        unknown = sorted(wanted - {r["seq"] for r in rows})
        if unknown:
            raise Skip(UNKNOWN_PROPOSAL,
                       f"{where}: the call has no proposal {', '.join(map(str, unknown))}")
        rows = [r for r in rows if r["seq"] in wanted]
        done = [r["seq"] for r in rows if r["decision"] == APPLIED]
        if done:
            raise Skip(UNKNOWN_PROPOSAL,
                       f"{where}: proposal {', '.join(map(str, done))} was applied already")
    rows = [r for r in rows if r["decision"] != APPLIED]
    if not rows:
        raise Skip(UNKNOWN_PROPOSAL, f"{where}: the call has no rejected proposals to apply")
    return [
        _Op(index, r["op"], r["target_entry_id"],
            _without_nulls(json.loads(r["raw_json"]).get("entry")),
            since=call["base_revision"], call_id=call["id"], proposed_change_id=r["id"])
        for r in rows
    ]


def _touched_slots(
    conn: sqlite3.Connection, parish_id: int, *, after_revision: int | None = None,
    after_time: str | None = None, call_id: int | None = None,
) -> set[str]:
    """Slot keys of the entries the parish's model revisions after a revision or a time
    changed, leaving out `call_id`'s own (see the module docstring)."""
    if after_revision is not None:
        where, params = "r.revision > ?", [after_revision]
    else:
        where, params = "r.created_at > ?", [after_time]
    if call_id is not None:
        where += " AND COALESCE(r.llm_call_id, -1) != ?"
        params.append(call_id)
    rows = conn.execute(
        f"""SELECT c.before_entry_id, c.after_entry_id FROM schedule_change c
            JOIN schedule_revision r ON r.parish_id = c.parish_id AND r.revision = c.revision
            WHERE c.parish_id = ? AND r.source_kind = ? AND {where}""",
        (parish_id, LLM, *params),
    ).fetchall()
    ids = {i for row in rows for i in row if i is not None}
    return {entry.slot_key for entry in load_entries(conn, ids).values()}


def _apply(
    conn: sqlite3.Connection, data: dict[str, Any], path: Path, parish_id: int, *,
    run_id: str | None, today: date,
) -> dict[str, Any]:
    """Check and write one file inside the caller's transaction. Raises Skip."""
    if not is_update_mode(conn, parish_id):
        raise Skip(NOT_SEEDED, "the parish has no seed revision, so no schedule to correct")
    churches = parish_churches(conn, parish_id)
    live = live_entries(conn, parish_id)
    retired = retire_ended(live, today)

    ops: list[_Op] = []
    bulletins: list[tuple[int, str]] = []
    for index, op in enumerate(data["operations"]):
        where = f"operation {index + 1}"
        kind = op["op"]
        if kind == WRONG_BULLETIN:
            try:
                check_bulletin(conn, parish_id, op["content_hash"])
            except Skip as exc:
                raise Skip(exc.reason, f"{where}: {exc.detail}") from exc
            bulletins.append((index, op["content_hash"]))
        elif kind == APPLY:
            ops += _call_ops(conn, parish_id, index, op)
        else:
            target = None
            if kind != ADD:
                target = _find_live(live, _entry(op["before"], churches, where), where)
            ops.append(_Op(index, kind, target, op.get("after")))

    outcomes = check_in_order(
        [(o.op, o.target, o.raw) for o in ops],
        schedule=Schedule(ids=dict(live)), churches=churches, today=today,
    )
    for o, outcome in zip(ops, outcomes, strict=True):
        if outcome.reason is not None:
            raise Skip(outcome.reason, f"operation {o.index + 1}: {outcome.detail}")

    as_of = normalize_as_of(data["as_of"])
    touched: dict[tuple[int | None, int | None], set[str]] = {}
    for o, outcome in zip(ops, outcomes, strict=True):
        key = (o.since, o.call_id)
        if key not in touched:
            touched[key] = _touched_slots(
                conn, parish_id, after_revision=o.since, after_time=as_of, call_id=o.call_id,
            )
        slots = {e.slot_key for e in (live.get(o.target), outcome.entry) if e is not None}
        if slots & touched[key]:
            since = f"revision {o.since}" if o.since is not None else as_of
            raise Skip(CHANGED_SINCE,
                       f"operation {o.index + 1}: a model revision after {since} "
                       "changed its slot")

    changes = [
        Change(o.op, before_entry_id=o.target,
               after_entry_id=intern_entry(conn, outcome.entry) if outcome.entry else None,
               proposed_change_id=o.proposed_change_id)
        for o, outcome in sorted(zip(ops, outcomes, strict=True), key=lambda p: p[1].order)
    ]
    for _, content_hash in bulletins:
        mark_wrong_bulletin(conn, parish_id, content_hash)
    revision = append_revision(
        conn, parish_id, source_kind=HUMAN, changes=retired + changes, run_id=run_id,
        actor=data["actor"], note=revision_note(data, path),
    )
    return {
        "parish": data["parish"],
        "file": f"{path.parent.name}/{path.name}",
        "revision": revision,
        "actor": data["actor"],
        "note": data["note"],
        "changes": len(changes),
        "wrong_bulletins": len(bulletins),
    }


def load_correction(
    conn: sqlite3.Connection, path: Path, *, run_id: str | None = None,
    today: date | None = None, loaded: set[tuple[int, str]] | None = None,
) -> dict[str, Any] | None:
    """Load one file: what loaded, `{"parish", "file", "reason"}` when skipped, None when
    it was loaded before. `loaded` is `loaded_digests`, when the caller has read it."""
    name = f"{path.parent.name}/{path.name}"
    try:
        data = read_correction(path)
    except CorrectionFileError as exc:
        return {"parish": path.parent.name, "file": name, "reason": f"{INVALID_FILE}: {exc}"}
    row = conn.execute("SELECT id FROM parish WHERE slug = ?", (data["parish"],)).fetchone()
    if row is None:
        return {"parish": data["parish"], "file": name,
                "reason": f"{INVALID_FILE}: no parish {data['parish']}"}
    parish_id = int(row[0])
    digest = correction_digest(data)
    if (parish_id, digest) in (loaded_digests(conn) if loaded is None else loaded):
        return None
    try:
        with conn:
            result = _apply(conn, data, path, parish_id, run_id=run_id,
                            today=today or date.today())
    except Skip as exc:
        return {"parish": data["parish"], "file": name, "reason": str(exc)}
    if loaded is not None:
        loaded.add((parish_id, digest))
    return result


def load_corrections(
    conn: sqlite3.Connection, corrections_dir: Path = CORRECTIONS_DIR, *,
    run_id: str | None = None, today: date | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Load every correction file not loaded yet. Returns what loaded and what was skipped."""
    loaded: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    digests = loaded_digests(conn)
    for path in correction_files(corrections_dir):
        try:
            result = load_correction(conn, path, run_id=run_id, today=today, loaded=digests)
        except Exception as exc:  # one bad file must not stop every pipeline command
            LOGGER.exception("Loading the correction %s failed", path)
            result = {"parish": path.parent.name, "file": f"{path.parent.name}/{path.name}",
                      "reason": f"{type(exc).__name__}: {exc}"}
        if result is None:
            continue
        if "reason" in result:
            LOGGER.warning("Correction %s not loaded: %s", result["file"], result["reason"])
            skipped.append(result)
        else:
            LOGGER.info("Loaded correction %s as revision %s", result["file"], result["revision"])
            loaded.append(result)
    return {"loaded": loaded, "skipped": skipped}


# ── Writing ─────────────────────────────────────────────────────────────────
def entry_content(conn: sqlite3.Connection, entry_id: int) -> dict[str, Any]:
    """A stored entry in the labels' form, as a correction's `before` names it."""
    entries = load_entries(conn, [entry_id])
    if entry_id not in entries:
        raise CorrectionFileError(f"no entry {entry_id}")
    entry = entries[entry_id]
    slug = church_slugs(conn, [entry.church_id])[entry.church_id]
    form = entry.labels_form(slug)
    if not entry.weekly and not form.get("cancelled"):
        del form["cancelled"]
    if entry.weekly and not form.get("exclude_weeks"):
        del form["exclude_weeks"]
    return _without_nulls(form)


def schedule_as_of(conn: sqlite3.Connection, parish_id: int) -> str:
    """The schedule a correction is made against: when the parish's newest model revision
    was written, or its seed's `as_of` if that is later (see the module docstring)."""
    row = conn.execute(
        """SELECT MAX(CASE WHEN source_kind = 'seed' THEN as_of ELSE created_at END)
           FROM schedule_revision WHERE parish_id = ? AND source_kind IN ('seed', 'llm')""",
        (parish_id,),
    ).fetchone()
    if row[0] is None:
        raise CorrectionFileError("the parish has no schedule to correct")
    return row[0]


def write_correction(
    parish_slug: str, name: str, *, actor: str, note: str, as_of: str,
    operations: list[dict[str, Any]], corrections_dir: Path = CORRECTIONS_DIR,
    day: date | None = None,
) -> Path:
    """Write a new correction file. Raises CorrectionFileError for a bad one or a taken name."""
    path = corrections_dir / parish_slug / f"{(day or date.today()).isoformat()}-{name}.json"
    data = {"parish": parish_slug, "actor": actor, "note": note, "as_of": as_of,
            "operations": operations}
    if not _NAME_RE.match(path.name):
        raise CorrectionFileError(
            f"{name!r}: a correction's short name is lowercase words joined by hyphens"
        )
    errors = check_shape(data, parish_slug=parish_slug)
    if errors:
        raise CorrectionFileError("; ".join(errors))
    if path.exists():
        raise CorrectionFileError(f"{path} exists already")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
