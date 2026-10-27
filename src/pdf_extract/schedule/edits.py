"""Hand edits: `human` revisions, for acting on what the policy rejected or the report flagged.

- `apply_proposals` applies a call's rejected proposals, all of them or chosen
  `seq`s. Each is checked against the current schedule with the per-proposal
  rules (the whole-call rules are what the person is overriding), in `seq` order
  with the policy's wait for later removals (`check_in_order`); any that fail
  are reported and skipped. The log rows carry the `proposed_change_id` they
  apply; the proposals' own decisions stay as the policy made them.
- `edit_entry` adds, modifies or deletes one entry directly, with the same checks.

`actor` is the person and `note` says why. Each call is one transaction.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Collection
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from pdf_extract.classifiers.schedule_update import _without_nulls
from pdf_extract.schedule.policy import APPLIED, Schedule, check_in_order, check_proposal
from pdf_extract.schedule.store import (
    ADD,
    DELETE,
    HUMAN,
    MODIFY,
    Change,
    append_revision,
    intern_entry,
    is_update_mode,
    live_entries,
    parish_churches,
    retire_ended,
)


class EditError(ValueError):
    """An edit that can't be made."""


@dataclass
class EditResult:
    parish_id: int
    revision: int | None = None
    applied: list[int] = field(default_factory=list)
    """The seqs applied (for `apply_proposals`)."""
    skipped: list[tuple[int, str, str | None]] = field(default_factory=list)
    """(seq, reason, detail) of the proposals that failed the checks or were applied already."""


def _require_update_mode(conn: sqlite3.Connection, parish_id: int) -> None:
    """Hand edits are for believed schedules: an extract-mode parish has none to edit."""
    if not is_update_mode(conn, parish_id):
        raise EditError(
            "the parish is in extract mode (it has no seed revision); seed it first"
        )


def apply_proposals(
    conn: sqlite3.Connection,
    llm_call_id: int,
    seqs: Collection[int] | None = None,
    *,
    actor: str,
    note: str | None = None,
    today: date | None = None,
) -> EditResult:
    """Apply a call's rejected proposals (all, or the chosen `seqs`) as one human revision."""
    call = conn.execute(
        "SELECT parish_id FROM llm_call WHERE id = ?", (llm_call_id,),
    ).fetchone()
    if call is None:
        raise EditError(f"no call {llm_call_id}")
    rows = conn.execute(
        "SELECT * FROM proposed_change WHERE llm_call_id = ? ORDER BY seq", (llm_call_id,),
    ).fetchall()
    if seqs is not None:
        unknown = sorted(set(seqs) - {r["seq"] for r in rows})
        if unknown:
            raise EditError(f"call {llm_call_id} has no proposal {', '.join(map(str, unknown))}")
        rows = [r for r in rows if r["seq"] in set(seqs)]

    _require_update_mode(conn, call["parish_id"])
    result = EditResult(parish_id=call["parish_id"])
    today = today or date.today()
    with conn:
        live = live_entries(conn, call["parish_id"])
        retired = retire_ended(live, today)
        schedule = Schedule(ids=live)
        churches = parish_churches(conn, call["parish_id"])
        for row in rows:
            if row["decision"] == APPLIED:
                result.skipped.append((row["seq"], "already_applied", None))
        pending = [row for row in rows if row["decision"] != APPLIED]
        outcomes = check_in_order(
            [
                (row["op"], row["target_entry_id"],
                 _without_nulls(json.loads(row["raw_json"]).get("entry")))
                for row in pending
            ],
            schedule=schedule, churches=churches, today=today,
        )
        applied: list[tuple[int, Change]] = []
        for row, outcome in zip(pending, outcomes, strict=True):
            if outcome.reason is not None:
                result.skipped.append((row["seq"], outcome.reason, outcome.detail))
                continue
            applied.append((outcome.order, Change(
                row["op"],
                before_entry_id=row["target_entry_id"],
                after_entry_id=intern_entry(conn, outcome.entry) if outcome.entry else None,
                proposed_change_id=row["id"],
            )))
            result.applied.append(row["seq"])
        result.skipped.sort(key=lambda item: item[0])
        # Logged in the order applied: a deferred add or modify after the removals it waited for.
        changes = [change for _, change in sorted(applied, key=lambda item: item[0])]
        if changes:
            result.revision = append_revision(
                conn, call["parish_id"], source_kind=HUMAN, changes=retired + changes, actor=actor,
                note=note or f"applied proposals of call {llm_call_id}",
            )
    return result


def edit_entry(
    conn: sqlite3.Connection,
    parish_id: int,
    op: str,
    *,
    target_entry_id: int | None = None,
    entry: dict[str, Any] | None = None,
    actor: str,
    note: str | None = None,
    today: date | None = None,
) -> EditResult:
    """Add, modify or delete one entry of the parish's schedule as a human revision.

    Raises EditError when the edit fails the per-proposal checks.
    """
    if op not in (ADD, MODIFY, DELETE):
        raise EditError(f"unknown op {op!r}")
    if (op == ADD) != (target_entry_id is None):
        raise EditError("add takes no entry id; modify and delete need one")
    if (op == DELETE) != (entry is None):
        raise EditError("add and modify need the new entry; delete takes none")
    _require_update_mode(conn, parish_id)
    result = EditResult(parish_id=parish_id)
    today = today or date.today()
    with conn:
        live = live_entries(conn, parish_id)
        retired = retire_ended(live, today)
        parsed, reason, detail = check_proposal(
            op, target_entry_id, entry, schedule=Schedule(ids=live),
            churches=parish_churches(conn, parish_id), today=today,
        )
        if reason is not None:
            raise EditError(f"{reason}: {detail}")
        result.revision = append_revision(
            conn, parish_id, source_kind=HUMAN,
            changes=[*retired, Change(
                op, before_entry_id=target_entry_id,
                after_entry_id=intern_entry(conn, parsed) if parsed else None,
            )],
            actor=actor, note=note,
        )
    return result
