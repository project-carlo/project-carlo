"""The decision policy: apply or reject each change a call proposes.

Every proposal is decided when its call is processed; nothing waits for a
later bulletin or a person. The whole call is rejected, every proposal with the
same reason, when the bulletin is the wrong one, older than the parish's
high-water mark, or deletes most of the parish's weekly schedule. Otherwise
each proposal is decided in `seq` order against the schedule as the proposals
before it left it, except that an add or modify which duplicates only entries
a later proposal of the call removes waits for those removals (`check_in_order`).
See docs/schedule-state-plan.md, "Decision policy (v1)".

The per-proposal checks (`check_proposal`) are also what a hand edit must pass.
"""

from __future__ import annotations

from collections.abc import Collection
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

POLICY_VERSION = "2"
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
UNUSUAL_TIME = "unusual_time_review"

WHOLE_CALL_REASONS = (WRONG_BULLETIN, STALE_BULLETIN, MASS_DELETE)
PROPOSAL_REASONS = (
    UNKNOWN_CHURCH, INVALID_ENTRY, INVALID_MODIFY, PAST_DATE, UNKNOWN_ITEM, DUPLICATE, NO_CHANGE,
    UNUSUAL_TIME,
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
    order: int | None = field(default=None, compare=False)
    """applied: its position among the call's applied proposals, the order its change is logged
    and folded in (a deferred add or modify comes after the removals it waited for)."""


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

    def conflicts(self, entry: Entry, *, excluding: int | None = None) -> bool:
        return any(entry.conflicts_with(e) for i, e in self.ids.items() if i != excluding) \
            or any(entry.conflicts_with(e) for e in self.added)

    def conflicting_ids(self, entry: Entry, *, excluding: int | None = None) -> set[int] | None:
        """The live ids `entry` conflicts with, or None when it conflicts with an added entry
        (which no later proposal can name, so nothing can remove it)."""
        if any(entry.conflicts_with(e) for e in self.added):
            return None
        return {i for i, e in self.ids.items() if i != excluding and entry.conflicts_with(e)}

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
    targetable: Collection[int] | None = None,
) -> tuple[Entry | None, str | None, str | None]:
    """Check one proposal against the schedule: (new entry, rejection reason, detail).

    The reason is None when the proposal may be applied. The new entry is
    returned whenever it could be read, so a rejected one is still stored.
    `targetable` limits the entries a modify or delete may name (a call may
    name only the entries in its view); None allows any live entry.
    """
    entry: Entry | None = None
    if op in (ADD, MODIFY):
        try:
            entry = parse_entry(raw_entry, churches)
        except EntryError as exc:
            return None, exc.reason, str(exc)
    target = (
        schedule.ids.get(target_entry_id)
        if target_entry_id is not None
        and (targetable is None or target_entry_id in targetable)
        else None
    )
    if op == MODIFY and target is not None and entry is not None and (
        (entry.church_id, entry.event_type, entry.event_kind)
        != (target.church_id, target.event_type, target.event_kind)
    ):
        return entry, INVALID_MODIFY, "a modify can't change the church, event type or kind"
    if entry is not None and entry.dated_before(today):
        return entry, PAST_DATE, f"{entry.date} is before {today.isoformat()}"
    if op in (MODIFY, DELETE) and target is None:
        return entry, UNKNOWN_ITEM, f"entry {target_entry_id} is not in the current schedule"
    if entry is not None and schedule.conflicts(entry, excluding=target_entry_id):
        return entry, DUPLICATE, "the schedule already has an entry for that slot"
    if op == MODIFY and entry == target:
        return entry, NO_CHANGE, "the new entry is the same as the old one"
    return entry, None, None


@dataclass
class Outcome:
    """How one proposal of `check_in_order` came out."""

    entry: Entry | None
    reason: str | None
    """None when applied."""
    detail: str | None = None
    order: int | None = None
    """applied: its position in the order the changes were applied."""


def check_in_order(
    proposals: list[tuple[str, int | None, Any]],
    *,
    schedule: Schedule,
    churches: dict[str, int],
    today: date,
    targetable: Collection[int] | None = None,
    review_unusual_times: bool = False,
) -> list[Outcome]:
    """Check and apply (op, target, raw entry) proposals in the order given; one outcome each.

    `review_unusual_times` holds new services before 5 AM for a human. A human
    edit or approval uses the same structural checks with this flag off.

    Each is checked against the schedule as the proposals before it left it, with
    one exception, so that a merge the model lists in either order is kept
    whole: an add or modify rejected only as a `duplicate` of live entries that later
    proposals in the list modify or delete waits. It is checked again after each
    later proposal is applied, applied as soon as it passes (after the removals it
    waited for, before the proposals that follow), and rejected with its last
    reason once none of what it duplicates can still be removed. Removals that are
    rejected (unknown, not targetable) remove nothing, so a waiting proposal that
    still duplicates is rejected as before. Waiting proposals are retried in list
    order, so an earlier waiting proposal gets the first retry for the same slot.
    Circular dependencies where no proposal can apply remain rejected.
    """
    outcomes: list[Outcome | None] = [None] * len(proposals)
    waiting: dict[int, Outcome] = {}
    applied = 0
    approved_night = [e for e in schedule.ids.values() if e.weekly and e.start_time < 5 * 60]

    def removable(position: int, index: int) -> set[int]:
        """Entries that proposals after `position`, or other waiting ones, may still remove."""
        return {
            target for j, (op, target, _) in enumerate(proposals)
            if target is not None and op in (MODIFY, DELETE) and j != index
            and (j > position or j in waiting)
        }

    def attempt(index: int, position: int) -> bool:
        """Check one proposal; apply it, reject it or leave it waiting. True when applied."""
        nonlocal applied
        op, target, raw = proposals[index]
        entry, reason, detail = check_proposal(
            op, target, raw, schedule=schedule, churches=churches, today=today,
            targetable=targetable,
        )
        target_entry = schedule.ids.get(target) if target is not None else None
        if reason is None and review_unusual_times and entry is not None and (
            not entry.cancelled and entry.start_time < 5 * 60
            and not (target_entry is not None and target_entry.start_time == entry.start_time)
            and not any(
                entry.slot_key == old.slot_key and entry.weeks_of_month == old.weeks_of_month
                and entry.season() == old.season() for old in approved_night
            )
        ):
            reason, detail = UNUSUAL_TIME, "new service before 5 AM needs human confirmation"
        if reason is None:
            schedule.apply(op, target, entry)
            waiting.pop(index, None)
            outcomes[index] = Outcome(entry, None, order=applied)
            applied += 1
            return True
        if reason == DUPLICATE and entry is not None:
            ids = schedule.conflicting_ids(entry, excluding=target)
            if ids and ids <= removable(position, index):
                waiting[index] = Outcome(entry, reason, detail)
                return False
        waiting.pop(index, None)
        outcomes[index] = Outcome(entry, reason, detail)
        return False

    for position in range(len(proposals)):
        changed = attempt(position, position)
        while changed:
            changed = False
            for index in sorted(waiting):
                if attempt(index, position):
                    changed = True
                    break
    for index, outcome in waiting.items():
        outcomes[index] = outcome
    return [outcome for outcome in outcomes if outcome is not None]


def decide(
    proposals: list[Proposal],
    *,
    live: dict[int, Entry],
    churches: dict[str, int],
    today: date,
    whole_call: str | None,
    targetable: Collection[int] | None = None,
) -> list[Decision]:
    """Decide every proposal of one call, in `seq` order (see `check_in_order`).

    `targetable`: the entry ids the call was shown. A target outside them
    (a dated entry already past, left out of the view) is `unknown_item`.
    Decisions are returned in `seq` order; an applied one's `order` is where its
    change goes in the revision.
    """
    ordered = sorted(proposals, key=lambda p: p.seq)
    if whole_call is not None:
        schedule = Schedule(ids=dict(live))
        return [
            Decision(
                p, REJECTED, whole_call,
                check_proposal(
                    p.op, p.target_entry_id, p.entry, schedule=schedule, churches=churches,
                    today=today, targetable=targetable,
                )[0],
            )
            for p in ordered
        ]
    outcomes = check_in_order(
        [(p.op, p.target_entry_id, p.entry) for p in ordered],
        schedule=Schedule(ids=dict(live)), churches=churches, today=today,
        targetable=targetable,
        review_unusual_times=True,
    )
    return [
        Decision(p, APPLIED, AUTO, o.entry, order=o.order) if o.reason is None
        else Decision(p, REJECTED, o.reason, o.entry, o.detail)
        for p, o in zip(ordered, outcomes, strict=True)
    ]
