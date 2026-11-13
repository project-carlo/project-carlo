"""`python -m pdf_extract schedule ...`: look at and hand-edit believed schedules.

    schedule show    --parish SLUG [--date YYYY-MM-DD]
    schedule apply   --call ID [--seq N ...] --actor NAME [--note TEXT] [--write-correction NAME]
    schedule add     --parish SLUG --entry JSON --actor NAME [--note TEXT] [--write-correction NAME]
    schedule modify  --parish SLUG --entry-id ID --entry JSON --actor NAME [--note TEXT]
                     [--write-correction NAME]
    schedule delete  --parish SLUG --entry-id ID --actor NAME [--note TEXT]
                     [--write-correction NAME]
    schedule wrong-bulletin --parish SLUG --content-hash HASH --actor NAME [--note TEXT]
                     [--write-correction NAME]
    schedule corrections
    schedule seed    --parish SLUG --file ENTRIES.json --actor NAME [--as-of TIME] [--note TEXT]
    schedule rebuild [--parish SLUG]

Every command runs against the local database (data/parish_events.db). Only
the weekly run and Publish Data Run publish a database, so an edit made here
never leaves the machine. To correct the published schedule, add
`--write-correction NAME`: the command writes the edit, addressed by content,
to `data/corrections/<parish>/<today>-<NAME>.json`, loads that file into the
local database to check it, and leaves the file to be committed and reviewed
(`schedule.corrections`, docs/believed-schedules.md). `corrections` loads any
correction files not loaded yet and says which were skipped and why.

An entry is given in the labels' form, e.g.
`{"church_slug": "st-mary-albany", "event_type": "mass", "event_kind": "weekly",
"day_of_week": "Sunday", "start_time": "9:00 AM"}`. `seed` writes a seed
revision from a JSON list of entries; populating seeds is otherwise out of
scope (docs/schedule-state-plan.md).
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.db import ensure_db
from pdf_extract.labeling.labels import is_valid_hash
from pdf_extract.schedule.corrections import (
    APPLY,
    WRONG_BULLETIN,
    CorrectionFileError,
    entry_content,
    load_correction,
    load_corrections,
    schedule_as_of,
    write_correction,
)
from pdf_extract.schedule.edits import EditError, apply_proposals, edit_entry
from pdf_extract.schedule.entries import EntryError, parse_entry
from pdf_extract.schedule.store import (
    ADD,
    DELETE,
    MODIFY,
    current_revision,
    parish_churches,
    rebuild_current_schedule,
    render_view,
    write_seed,
)
from pdf_extract.storage import DEFAULT_DB_PATH, connect_db

Result = dict[str, Any]


class ScheduleCommandError(ValueError):
    """Bad input to a schedule command: the message says what to fix."""


def _connect(*, load_corrections: bool = True):
    ensure_db(DEFAULT_DB_PATH, load_corrections=load_corrections)
    return connect_db(DEFAULT_DB_PATH)


def _parish_id(conn, slug: str) -> int:
    row = conn.execute("SELECT id FROM parish WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise ScheduleCommandError(f"Parish not found: {slug}")
    return int(row["id"])


def _entry(text: str) -> dict[str, Any]:
    try:
        entry = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ScheduleCommandError(f"--entry is not JSON: {exc}") from exc
    if not isinstance(entry, dict):
        raise ScheduleCommandError("--entry must be a JSON object")
    return entry


def _cmd_show(args: argparse.Namespace) -> Result:
    conn = _connect()
    try:
        parish_id = _parish_id(conn, args.parish)
        day = date.fromisoformat(args.date) if args.date else date.today()
        text, view_hash = render_view(conn, parish_id, day)
        return {
            "parish": args.parish,
            "revision": current_revision(conn, parish_id),
            "view_hash": view_hash,
            "view": json.loads(text),
        }
    finally:
        conn.close()


def _write_and_load(
    conn, args: argparse.Namespace, parish: str, operations: list[dict[str, Any]],
) -> Result:
    """Write the edit as a correction file and load it into the local database to check it.

    A file that doesn't load is removed again: it would be skipped on the
    published database too.
    """
    if not args.note or not args.note.strip():
        raise ScheduleCommandError("--write-correction needs a --note saying why")
    try:
        path = write_correction(
            parish, args.write_correction, actor=args.actor, note=args.note,
            as_of=schedule_as_of(conn, _parish_id(conn, parish)), operations=operations,
        )
    except CorrectionFileError as exc:
        raise ScheduleCommandError(str(exc)) from exc
    result = load_correction(conn, path)
    if result is None or "reason" in result:
        path.unlink()
        reason = "an identical correction is loaded already" if result is None \
            else result["reason"]
        raise ScheduleCommandError(f"correction not written: {reason}")
    return {**result, "path": str(path)}


def _cmd_apply(args: argparse.Namespace) -> Result:
    conn = _connect()
    if args.write_correction:
        try:
            call = conn.execute(
                """SELECT c.run_id, b.content_hash, p.slug FROM llm_call c
                   JOIN bulletin b ON b.id = c.bulletin_id JOIN parish p ON p.id = c.parish_id
                   WHERE c.id = ?""", (args.call,),
            ).fetchone()
            if call is None:
                raise ScheduleCommandError(f"no call {args.call}")
            if not call["run_id"]:
                raise ScheduleCommandError(
                    f"call {args.call} has no run id, so a correction can't name it"
                )
            op: dict[str, Any] = {
                "op": APPLY, "run_id": call["run_id"], "content_hash": call["content_hash"],
            }
            if args.seq:
                op["seq"] = sorted(set(args.seq))
            return _write_and_load(conn, args, call["slug"], [op])
        finally:
            conn.close()
    try:
        result = apply_proposals(
            conn, args.call, args.seq or None, actor=args.actor, note=args.note,
        )
    except EditError as exc:
        raise ScheduleCommandError(str(exc)) from exc
    finally:
        conn.close()
    return {
        "revision": result.revision,
        "applied": result.applied,
        "skipped": [
            {"seq": seq, "reason": reason, "detail": detail}
            for seq, reason, detail in result.skipped
        ],
    }


def _edit(op: str) -> Callable[[argparse.Namespace], Result]:
    def handler(args: argparse.Namespace) -> Result:
        conn = _connect()
        if args.write_correction:
            try:
                return _write_and_load(conn, args, args.parish, [_correction_op(conn, op, args)])
            finally:
                conn.close()
        try:
            result = edit_entry(
                conn, _parish_id(conn, args.parish), op,
                target_entry_id=getattr(args, "entry_id", None),
                entry=_entry(args.entry) if op != DELETE else None,
                actor=args.actor, note=args.note,
            )
        except EditError as exc:
            raise ScheduleCommandError(str(exc)) from exc
        finally:
            conn.close()
        return {"parish": args.parish, "revision": result.revision}
    return handler


def _correction_op(conn, op: str, args: argparse.Namespace) -> dict[str, Any]:
    """An add, modify or delete as a correction names it: by the entries' content."""
    out: dict[str, Any] = {"op": op}
    if op != ADD:
        try:
            out["before"] = entry_content(conn, args.entry_id)
        except CorrectionFileError as exc:
            raise ScheduleCommandError(str(exc)) from exc
    if op != DELETE:
        out["after"] = _entry(args.entry)
    return out


def _cmd_wrong_bulletin(args: argparse.Namespace) -> Result:
    if not is_valid_hash(args.content_hash):
        raise ScheduleCommandError("--content-hash must be a bulletin's sha256 content hash")
    conn = _connect()
    try:
        parish_id = _parish_id(conn, args.parish)
        if args.write_correction:
            return _write_and_load(conn, args, args.parish, [
                {"op": WRONG_BULLETIN, "content_hash": args.content_hash},
            ])
        with conn:
            marked = conn.execute(
                """UPDATE bulletin SET wrong_bulletin = 1
                   WHERE parish_id = ? AND content_hash = ?""",
                (parish_id, args.content_hash),
            ).rowcount
        if not marked:
            raise ScheduleCommandError("the parish has no bulletin with that content hash")
        return {"parish": args.parish, "bulletins_marked": marked}
    finally:
        conn.close()


def _cmd_corrections(args: argparse.Namespace) -> Result:
    conn = _connect(load_corrections=False)
    try:
        return load_corrections(conn)
    finally:
        conn.close()


def _cmd_seed(args: argparse.Namespace) -> Result:
    raw = json.loads(Path(args.file).read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ScheduleCommandError(f"{args.file} must hold a JSON list of entries")
    conn = _connect()
    try:
        parish_id = _parish_id(conn, args.parish)
        churches = parish_churches(conn, parish_id)
        entries = []
        for i, item in enumerate(raw):
            try:
                entries.append(parse_entry(item, churches))
            except EntryError as exc:
                raise ScheduleCommandError(f"entry {i}: {exc.reason}: {exc}") from exc
        try:
            with conn:
                revision = write_seed(
                    conn, parish_id, entries, as_of=args.as_of, actor=args.actor,
                    note=args.note,
                )
        except ValueError as exc:  # two entries for one slot, or an unreadable --as-of
            raise ScheduleCommandError(str(exc)) from exc
        return {"parish": args.parish, "revision": revision, "entries": len(entries)}
    finally:
        conn.close()


def _cmd_rebuild(args: argparse.Namespace) -> Result:
    conn = _connect()
    try:
        ids = [_parish_id(conn, args.parish)] if args.parish else None
        with conn:
            return rebuild_current_schedule(conn, ids)
    finally:
        conn.close()


def add_schedule_parser(
    subparsers: argparse._SubParsersAction,
    add_common_args: Callable[[argparse.ArgumentParser], None],
) -> None:
    parser = subparsers.add_parser(
        "schedule", help="Show and hand-edit believed schedules (update-mode parishes)",
    )
    parser.set_defaults(help_parser=parser)
    sub = parser.add_subparsers(dest="schedule_command")

    def leaf(name: str, help_text: str, handler: Callable[[argparse.Namespace], Result]):
        p = sub.add_parser(name, help=help_text)
        p.set_defaults(handler=handler)
        add_common_args(p)
        return p

    def who(p: argparse.ArgumentParser) -> None:
        p.add_argument("--actor", required=True, help="Who is making the edit")
        p.add_argument("--note", help="Why")

    def correction(p: argparse.ArgumentParser) -> None:
        p.add_argument(
            "--write-correction", metavar="NAME",
            help="Also write the edit to data/corrections/<parish>/<today>-NAME.json, to "
            "commit, so it reaches the published database (needs --note)",
        )

    show = leaf("show", "Print a parish's believed schedule as the model sees it", _cmd_show)
    show.add_argument("--parish", required=True, help="Parish slug")
    show.add_argument("--date", help="Leave out dated entries before this day (default today)")

    apply = leaf("apply", "Apply a call's rejected proposals", _cmd_apply)
    apply.add_argument("--call", type=int, required=True, help="llm_call id")
    apply.add_argument("--seq", type=int, action="append", help="Only this proposal (repeatable)")
    who(apply)
    correction(apply)

    for op, help_text in (
        (ADD, "Add an entry"), (MODIFY, "Replace an entry"), (DELETE, "Delete an entry"),
    ):
        p = leaf(op, help_text, _edit(op))
        p.add_argument("--parish", required=True, help="Parish slug")
        if op != ADD:
            p.add_argument("--entry-id", type=int, required=True, help="The entry's id")
        if op != DELETE:
            p.add_argument("--entry", required=True, help="The new entry as JSON")
        who(p)
        correction(p)

    wrong = leaf(
        "wrong-bulletin", "Mark a stored bulletin as not the parish's current bulletin",
        _cmd_wrong_bulletin,
    )
    wrong.add_argument("--parish", required=True, help="Parish slug")
    wrong.add_argument("--content-hash", required=True, help="The bulletin's content hash")
    who(wrong)
    correction(wrong)

    leaf(
        "corrections", "Load the correction files not loaded yet; report the ones skipped",
        _cmd_corrections,
    )

    seed = leaf("seed", "Write a seed revision from a JSON list of entries", _cmd_seed)
    seed.add_argument("--parish", required=True, help="Parish slug")
    seed.add_argument("--file", required=True, help="JSON list of entries in the labels' form")
    seed.add_argument(
        "--as-of",
        help="The fetch time the schedule is current as of: an ISO time, or a date for "
        "the end of that day (default: now)",
    )
    who(seed)

    rebuild = leaf(
        "rebuild", "Replay the change log into current_schedule and report differences",
        _cmd_rebuild,
    )
    rebuild.add_argument("--parish", help="Parish slug (default: every parish)")
