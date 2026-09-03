"""Turns classifier runs into the decisions a human actually has to make.

The unit of review is one bulletin. Every event any classifier proposed for it
becomes a *candidate*; candidates every run agreed on are pre-accepted, and the
rest are grouped so that a disagreement costs one keystroke rather than several:

- **agreed** — proposed by every run that saw the bulletin. Almost always right,
  so these default to accepted and stay collapsed.
- **conflicts** — disputed candidates that sit within one logical field of each
  other (see `labelapp.events`). These are the same slot read two ways, so they
  are shown as one card: pick the right variant, or reject the lot.
- **singletons** — disputed candidates nothing else came near. One run saw an
  event the others missed: keep it or drop it.

Nothing here decides whether a candidate is *correct* — that is the human's job.
It only decides what gets put in front of them, and in what order.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any

from pdf_extract.compare import EventKey, event_key
from pdf_extract.timeparse import time_to_minutes

from labelapp import events as ev
from labelapp.corpus import Bulletin, Run


@dataclass
class Candidate:
    """One distinct event key proposed by at least one classifier."""

    key_id: str
    event: dict[str, Any]
    #: run names that proposed this exact event, in the caller's run order
    sources: list[str]
    #: True when every run that saw this bulletin proposed it
    unanimous: bool
    #: 1-indexed PDF page, by majority vote across the runs that reported one
    page_number: int | None = None
    #: per-run commentary, shown but never part of identity
    notes: list[dict[str, str]] = field(default_factory=list)
    #: agreed candidates a variant away, shown as read-only context on a singleton
    context: list["Candidate"] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "key_id": self.key_id,
            "event": self.event,
            "sources": self.sources,
            "unanimous": self.unanimous,
            "page_number": self.page_number,
            "notes": self.notes,
            "context": [
                {"summary": ev.describe_event(row.event), "key_id": row.key_id}
                for row in self.context
            ],
            "summary": ev.describe_event(self.event),
            "when": ev.describe_when(self.event),
        }


@dataclass
class Conflict:
    """Disputed candidates that are variants of one another."""

    conflict_id: str
    #: logical field names the variants disagree on
    fields: list[str]
    variants: list[Candidate]
    #: unanimous candidates sitting one field away, shown as read-only context
    context: list[Candidate] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "conflict_id": self.conflict_id,
            "fields": self.fields,
            "field_labels": [ev.FIELD_LABELS.get(name, name) for name in self.fields],
            "variants": [candidate.to_json() for candidate in self.variants],
            "context": [candidate.to_json() for candidate in self.context],
        }


def _majority_page(pages: list[int]) -> int | None:
    if not pages:
        return None
    counts = Counter(pages)
    best = max(counts.values())
    # Ties go to the earliest page: scrolling back is cheaper than hunting forward.
    return min(page for page, count in counts.items() if count == best)


def build_candidates(
    bulletin_url: str,
    runs: dict[str, Run],
    run_order: list[str],
) -> tuple[list[Candidate], list[str]]:
    """Collect every event proposed for one bulletin.

    Returns the candidates and the names of the runs that actually saw this
    bulletin — agreement is measured against those, not against every run the
    caller asked for, so a run that has not reached this bulletin yet neither
    counts as agreeing nor as dissenting.
    """
    covering = [name for name in run_order if bulletin_url in runs[name].covered]

    grouped: dict[EventKey, dict[str, Any]] = {}
    for name in covering:
        for row in runs[name].events_by_bulletin.get(bulletin_url, []):
            key = event_key(row)
            entry = grouped.setdefault(
                key, {"event": ev.normalize_event(row), "sources": [], "pages": [], "notes": []}
            )
            if name not in entry["sources"]:
                entry["sources"].append(name)
            page = row.get("page_number")
            if isinstance(page, int):
                entry["pages"].append(page)
            note = row.get("note")
            if isinstance(note, str) and note.strip():
                entry["notes"].append({"run": name, "note": note.strip()})

    candidates = [
        Candidate(
            key_id=ev.key_id(key),
            event=entry["event"],
            sources=entry["sources"],
            unanimous=bool(covering) and len(entry["sources"]) == len(covering),
            page_number=_majority_page(entry["pages"]),
            notes=entry["notes"],
        )
        for key, entry in grouped.items()
    ]
    candidates.sort(key=_candidate_sort_key)
    return candidates, covering


def _candidate_sort_key(candidate: Candidate) -> tuple[Any, ...]:
    """Read order: by church, then type, then when, then time."""
    event = candidate.event
    return (
        event["church_slug"],
        event["event_type"],
        event["event_kind"],
        event["day_of_week"] or "",
        event["date"] or "",
        _time_sort_key(event["start_time"]),
        event["start_time"],
    )


def _time_sort_key(value: str) -> int:
    """Minutes past midnight for `h:MM AM`, or a large sentinel if unparseable.

    Only used for ordering cards, so an unreadable time sorts last rather than
    raising — the human still sees it, just at the end of its group.
    """
    minutes = time_to_minutes(value)
    return minutes if minutes is not None else 10_000


def _variant_of(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Whether two events are competing readings of the same schedule slot.

    They must differ in exactly one logical field, and — when that field is
    `when` — describe the same day. A weekly Sunday slot and a Mass dated to a
    Sunday are one slot filed two ways, which is the extractor's most common
    mistake. A weekly Tuesday slot and a weekly Thursday one are two Masses, and
    asking a human to choose between them is a question with no right answer.
    """
    differing = ev.differing_fields(a, b)
    if len(differing) != 1:
        return False
    if differing[0] != ev.FIELD_WHEN:
        return True

    kinds = {a["event_kind"], b["event_kind"]}
    if kinds != {"weekly", "specific_date"}:
        return False
    weekly, dated = (a, b) if a["event_kind"] == "weekly" else (b, a)
    return ev.weekday_of(dated["date"]) == weekly["day_of_week"]


def _pairable(a: Candidate, b: Candidate) -> bool:
    """Whether two disputed candidates belong on one decision card.

    Beyond being variants of each other, no classifier may have proposed both:
    a run that listed two slots separately plainly considers them two events, so
    they are not two readings of one.
    """
    if set(a.sources) & set(b.sources):
        return False
    return _variant_of(a.event, b.event)


def _similarity(a: Candidate, b: Candidate) -> int:
    """How many raw identity columns two candidates share.

    Used to pick the best partner when a candidate could pair with several: the
    reading that agrees on more columns is the one describing the same slot.
    """
    return sum(1 for name in ev.EVENT_FIELDS if a.event[name] == b.event[name])


def _pair_candidates(disputed: list[Candidate]) -> list[list[Candidate]]:
    """Group disputed candidates into mutually-compatible readings of one slot.

    Groups are cliques rather than connected components — every member must be
    pairable with every other — so a chain of loosely related events cannot
    merge into one oversized decision. Strongest pairing wins first.
    """
    edges = [
        (-_similarity(a, b), index_a, index_b)
        for index_a, a in enumerate(disputed)
        for index_b, b in enumerate(disputed)
        if index_a < index_b and _pairable(a, b)
    ]
    edges.sort()

    group_of: dict[int, int] = {}
    groups: list[list[int]] = []
    for _, index_a, index_b in edges:
        home_a = group_of.get(index_a)
        home_b = group_of.get(index_b)
        if home_a is not None and home_b is not None:
            continue  # both already placed; merging groups risks a chain
        if home_a is None and home_b is None:
            group_of[index_a] = group_of[index_b] = len(groups)
            groups.append([index_a, index_b])
            continue
        home, newcomer = (home_a, index_b) if home_a is not None else (home_b, index_a)
        members = groups[home]
        if all(_pairable(disputed[newcomer], disputed[member]) for member in members):
            members.append(newcomer)
            group_of[newcomer] = home

    grouped = [[disputed[index] for index in sorted(members)] for members in groups]
    loners = [
        [candidate]
        for index, candidate in enumerate(disputed)
        if index not in group_of
    ]
    return grouped + loners


def group_candidates(candidates: list[Candidate]) -> dict[str, Any]:
    """Split candidates into agreed / conflicts / singletons."""
    agreed = [candidate for candidate in candidates if candidate.unanimous]
    disputed = [candidate for candidate in candidates if not candidate.unanimous]

    conflicts: list[Conflict] = []
    singletons: list[Candidate] = []

    for members in _pair_candidates(disputed):
        if len(members) == 1:
            # A lone candidate still gets its neighbours: an event only one model
            # found is very often a duplicate of one they all agreed on.
            loner = members[0]
            loner.context = _context_for([loner], agreed, list(ev.FIELD_LABELS))
            singletons.append(loner)
            continue
        fields: set[str] = set()
        for position, first in enumerate(members):
            for second in members[position + 1 :]:
                fields.update(ev.differing_fields(first.event, second.event))
        ordered_fields = [name for name in ev.FIELD_LABELS if name in fields]
        conflicts.append(
            Conflict(
                conflict_id=members[0].key_id,
                fields=ordered_fields,
                variants=members,
                context=_context_for(members, agreed, ordered_fields),
            )
        )

    return {"agreed": agreed, "conflicts": conflicts, "singletons": singletons}


def _context_for(
    variants: list[Candidate],
    agreed: list[Candidate],
    fields: list[str],
) -> list[Candidate]:
    """Agreed candidates that differ from a variant along the conflict's own axis.

    A dated slot that duplicates a weekly one every model already agreed on is
    almost always the extractor double-filing it, and seeing that neighbour turns
    the decision into a glance. Neighbours that differ on some *other* field are
    unrelated events that happen to sit nearby, so they are left out.
    """
    allowed = set(fields)
    return [
        candidate
        for candidate in agreed
        if any(
            _variant_of(candidate.event, variant.event)
            and ev.differing_fields(candidate.event, variant.event)[0] in allowed
            for variant in variants
        )
    ]


def build_review(
    bulletin: Bulletin,
    runs: dict[str, Run],
    run_order: list[str],
) -> dict[str, Any]:
    """Everything the UI needs to review one bulletin, minus any saved label."""
    candidates, covering = build_candidates(bulletin.source_url, runs, run_order)
    groups = group_candidates(candidates)
    disputed_count = len(candidates) - len(groups["agreed"])

    return {
        "bulletin_source_url": bulletin.source_url,
        "parish_slug": bulletin.parish_slug,
        "content_hash": bulletin.content_hash,
        "published_date": bulletin.published_date,
        "fetched_at": bulletin.fetched_at,
        "has_pdf": bool(bulletin.pdf_path and bulletin.pdf_path.exists()),
        "runs": covering,
        "run_event_counts": {
            name: len(runs[name].events_by_bulletin.get(bulletin.source_url, []))
            for name in covering
        },
        "wrong_bulletin_runs": [
            name for name in covering if bulletin.source_url in runs[name].wrong_bulletin
        ],
        "candidate_count": len(candidates),
        "agreed_count": len(groups["agreed"]),
        "disputed_count": disputed_count,
        "conflict_count": len(groups["conflicts"]),
        "agreed": [candidate.to_json() for candidate in groups["agreed"]],
        "conflicts": [conflict.to_json() for conflict in groups["conflicts"]],
        "singletons": [candidate.to_json() for candidate in groups["singletons"]],
    }
