"""The decision policy (v1): apply or reject each change a call proposes.

Every proposal is decided when its call is processed; nothing waits for a
later bulletin or a person. The whole call is rejected, every proposal with the
same reason, when the bulletin is the wrong one, older than the parish's
high-water mark, or deletes most of the parish's weekly schedule. Otherwise
each proposal is decided in `seq` order against the schedule as the proposals
before it left it. See docs/schedule-state-plan.md, "Decision policy (v1)".

The per-proposal checks (`check_proposal`) are also what a hand edit must pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from pdf_extract.schedule.entries import (
    INVALID_ENTRY,
    UNKNOWN_CHURCH,
    Entry,
    EntryError,
    parse_entry,
)
from pdf_extract.schedule.store import ADD, DELETE, MODIFY

POLICY_VERSION = "1"
DECIDED_BY = f"policy@{POLICY_VERSION}"

APPLIED = "applied"
REJECTED = "rejected"

AUTO = "auto"
# Whole-call reasons.
WRONG_BULLETIN = "wrong_bulletin"
STALE_BULLETIN = "stale_bulletin"
MASS_DELETE = "mass_delete"
# Per-proposal reasons, in the order they are checked.
INVALID_MODIFY = "invalid_modify"
PAST_DATE = "past_date"
UNKNOWN_ITEM = "unknown_item"
DUPLICATE = "duplicate"
# A modify whose new entry is exactly its target: there is nothing to change.
NO_CHANGE = "no_change"

WHOLE_CALL_REASONS = (WRONG_BULLETIN, STALE_BULLETIN, MASS_DELETE)
PROPOSAL_REASONS = (
    UNKNOWN_CHURCH, INVALID_ENTRY, INVALID_MODIFY, PAST_DATE, UNKNOWN_ITEM, DUPLICATE, NO_CHANGE,
)

# A call deleting at least this many weekly entries, and more than half of the
# parish's live weekly entries, is rejected whole.
MASS_DELETE_MIN_ENTRIES = 3
MASS_DELETE_FRACTION = 0.5


@dataclass
class Proposal:
    """One change as the model proposed it."""

    seq: int
    op: str
    raw: dict[str, Any]
    target_entry_id: int | None = None
    entry: Any = None
    """add, modify: the new entry in the labels' form, as written."""
    page_number: int | None = None
    rationale: str | None = None


@dataclass
class Decision:
    proposal: Proposal
    decision: str
    reason: str
    entry: Entry | None = None
    """add, modify: the new entry, when it could be read (stored even if rejected)."""
    detail: str | None = field(default=None, compare=False)


def whole_call_reason(
    *, wrong_bulletin: bool, stale: bool, proposals: list[Proposal], live: dict[int, Entry],
) -> str | None:
    """Why the whole call is rejected, or None when its proposals are decided one by one."""
    if wrong_bulletin:
        return WRONG_BULLETIN
    if stale:
        return STALE_BULLETIN
    live_weekly = {entry_id for entry_id, entry in live.items() if entry.weekly}
    deleted = {
        p.target_entry_id for p in proposals
        if p.op == DELETE and p.target_entry_id in live_weekly
    }
    if (
        len(deleted) >= MASS_DELETE_MIN_ENTRIES
        and len(deleted) > len(live_weekly) * MASS_DELETE_FRACTION
    ):
        return MASS_DELETE
    return None


@dataclass
class Schedule:
    """A parish's schedule while a call's proposals are decided against it.

    `ids` are the live entries that still stand; `added` are entries an
    earlier proposal in the call brought in (they have no id the model could
    name yet).
    """

    ids: dict[int, Entry]
    added: list[Entry] = field(default_factory=list)

    def identities(self, *, excluding: int | None = None) -> set[str]:
        keys = {e.identity_key for i, e in self.ids.items() if i != excluding}
        return keys | {e.identity_key for e in self.added}

    def apply(self, op: str, target: int | None, entry: Entry | None) -> None:
        if target is not None:
            del self.ids[target]
        if entry is not None:
            self.added.append(entry)


def check_proposal(
    op: str,
    target_entry_id: int | None,
    raw_entry: Any,
    *,
    schedule: Schedule,
    churches: dict[str, int],
    today: date,
) -> tuple[Entry | None, str | None, str | None]:
    """Check one proposal against the schedule: (new entry, rejection reason, detail).

    The reason is None when the proposal may be applied. The new entry is
    returned whenever it could be read, so a rejected one is still stored.
    """
    entry: Entry | None = None
    if op in (ADD, MODIFY):
        try:
            entry = parse_entry(raw_entry, churches)
        except EntryError as exc:
            return None, exc.reason, str(exc)
    target = schedule.ids.get(target_entry_id) if target_entry_id is not None else None
    if op == MODIFY and target is not None and entry is not None and (
        (entry.church_id, entry.event_type, entry.event_kind)
        != (target.church_id, target.event_type, target.event_kind)
    ):
        return entry, INVALID_MODIFY, "a modify can't change the church, event type or kind"
    if entry is not None and entry.dated_before(today):
        return entry, PAST_DATE, f"{entry.date} is before {today.isoformat()}"
    if op in (MODIFY, DELETE) and target is None:
        return entry, UNKNOWN_ITEM, f"entry {target_entry_id} is not in the current schedule"
    if entry is not None and entry.identity_key in schedule.identities(excluding=target_entry_id):
        return entry, DUPLICATE, "the schedule already has an entry for that slot"
    if op == MODIFY and entry == target:
        return entry, NO_CHANGE, "the new entry is the same as the old one"
    return entry, None, None


def decide(
    proposals: list[Proposal],
    *,
    live: dict[int, Entry],
    churches: dict[str, int],
    today: date,
    whole_call: str | None,
) -> list[Decision]:
    """Decide every proposal of one call, in `seq` order."""
    schedule = Schedule(ids=dict(live))
    decisions: list[Decision] = []
    for proposal in sorted(proposals, key=lambda p: p.seq):
        entry, reason, detail = check_proposal(
            proposal.op, proposal.target_entry_id, proposal.entry,
            schedule=schedule, churches=churches, today=today,
        )
        if whole_call is not None:
            reason, detail = whole_call, None
        if reason is None:
            schedule.apply(proposal.op, proposal.target_entry_id, entry)
            decisions.append(Decision(proposal, APPLIED, AUTO, entry))
        else:
            decisions.append(Decision(proposal, REJECTED, reason, entry, detail))
    return decisions
