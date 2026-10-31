"""The labeler's Seeds mode: the queue of seed files, one file for review, and saving it.

A reviewer settles the open questions, may edit, drop or reopen any slot, and
approves the parish. The server keeps what the agent wrote about the parish
(its bulletins, calls, summary and `as_of`) as the file has it, and takes the
slots, the status and the reviewer from the request. An approved file must
pass `seed check`, and its `approved_at` is stamped here.

An agent reviewer (the factory's `seed-review`) answers and approves through
`approve_seed` (`pnpm seed approve`) instead, with the same slot changes and the
same save. Its `by` and `reviewer` start with `agent:`.
"""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Any

from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.files import (
    APPROVED,
    BLOCKED,
    DRAFTING,
    DROPPED,
    EDITED,
    EXCLUDE,
    INCLUDE,
    NEEDS_HUMAN,
    NEEDS_REVIEW,
    READY,
    SEEDS_DIR,
    SETTLED,
    SeedFileError,
    SeedSummary,
    read_seed,
    seed_slugs,
    validate_seed,
    write_seed_file,
)
from pdf_extract.seeding.loader import is_loaded
from pdf_extract.storage import church_list_for_prompt, utc_now_iso

QUEUE_ORDER = (NEEDS_REVIEW, READY, DRAFTING, BLOCKED, APPROVED)
REVIEW_STATUSES = (NEEDS_REVIEW, READY, APPROVED, BLOCKED)
# What a review may change; everything else stays as the agent wrote it.
REVIEWED_KEYS = ("slots", "status", "reviewer", "blocked_reason")
# How an agent reviewer's `by` and `reviewer` start (`agent:seed-review@<commit>`).
AGENT_PREFIX = "agent:"


_save_lock = threading.Lock()


class SeedReviewError(ValueError):
    """A review that can't be saved: the message says why."""


def _parish(conn: sqlite3.Connection, slug: str) -> sqlite3.Row | None:
    return conn.execute("SELECT id, slug, name FROM parish WHERE slug = ?", (slug,)).fetchone()


def seed_queue(conn: sqlite3.Connection, seeds_dir: Path = SEEDS_DIR) -> list[dict[str, Any]]:
    """Every seed file, open questions first, with whether the database has loaded it."""
    rows = []
    for slug in seed_slugs(seeds_dir):
        parish = _parish(conn, slug)
        try:
            seed = read_seed(slug, seeds_dir)
            summary = SeedSummary.of(slug, seed)
        except SeedFileError as exc:
            seed, summary = None, SeedSummary.of(slug, None, problem=str(exc))
        rows.append({
            **summary.__dict__,
            "parish_name": parish["name"] if parish else slug,
            "loaded": bool(parish and seed and is_loaded(conn, parish["id"], seed)),
        })
    order = {status: i for i, status in enumerate(QUEUE_ORDER)}
    rows.sort(key=lambda r: (order.get(r["status"], len(order)), -r["open_questions"],
                             r["parish_name"].lower()))
    return rows


def seed_detail(
    conn: sqlite3.Connection, parish_slug: str, seeds_dir: Path = SEEDS_DIR,
) -> dict[str, Any] | None:
    """One seed file with what the review page shows beside it, or None if there is none."""
    seed = read_seed(parish_slug, seeds_dir)
    if seed is None:
        return None
    parish = _parish(conn, parish_slug)
    known: set[str] = set()
    if parish is not None:
        known = {
            r[0] for r in conn.execute(
                "SELECT content_hash FROM bulletin WHERE parish_id = ?", (parish["id"],),
            ).fetchall()
        }
    shape = validate_seed(seed, parish_slug=parish_slug)
    problems = shape or check_seed(conn, seed, parish_slug=parish_slug)
    return {
        # A file the page can't show (a key missing, a list that isn't one) comes
        # back as its problems only, to be fixed in the file.
        "seed": None if shape else seed,
        "parish": {"slug": parish_slug, "name": parish["name"] if parish else parish_slug},
        "churches": church_list_for_prompt(conn, parish["id"]) if parish else [],
        "bulletins_in_db": sorted(known),
        "problems": [p for p in problems if not p.startswith("status is still drafting")],
        "loaded": bool(parish and is_loaded(conn, parish["id"], seed)),
    }


def save_reviewed_seed(
    conn: sqlite3.Connection, parish_slug: str, body: Any, seeds_dir: Path = SEEDS_DIR,
) -> dict[str, Any]:
    """Validate and save a review of a seed file. Returns the saved file's detail.

    Saves are one at a time, so two in flight can't interleave their read and write.
    """
    with _save_lock:
        return _save(conn, parish_slug, body, seeds_dir)


def approve_ready_seeds(
    conn: sqlite3.Connection, reviewer: Any, seeds_dir: Path = SEEDS_DIR,
) -> dict[str, Any]:
    """Approve every currently ready file, reporting failures without stopping the batch.

    Use the same validation and timestamps as a parish's Approve button. Hold
    the review lock so other review saves cannot change the files mid-batch.
    """
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise SeedReviewError("Say who you are (the reviewer) before approving")
    approved: list[str] = []
    failed: list[dict[str, str]] = []
    with _save_lock:
        for row in seed_queue(conn, seeds_dir):
            if row["status"] != READY:
                continue
            slug = row["parish_slug"]
            try:
                current = read_seed(slug, seeds_dir)
                if current is None or current.get("status") != READY:
                    raise SeedReviewError("This seed is no longer ready to approve")
                _save(conn, slug, {**current, "status": APPROVED,
                                  "reviewer": reviewer.strip()}, seeds_dir)
            except (SeedFileError, SeedReviewError, OSError) as exc:
                failed.append({"parish_slug": slug, "error": str(exc)})
            else:
                approved.append(slug)
        return {"approved": approved, "failed": failed, "seeds": seed_queue(conn, seeds_dir)}


def is_agent(by: Any) -> bool:
    """Whether an answer's `by` (or a file's `reviewer`) is an agent reviewer's."""
    return isinstance(by, str) and by.startswith(AGENT_PREFIX)


def approve_seed(
    conn: sqlite3.Connection, parish_slug: str, reviewer: str, answers: Any,
    seeds_dir: Path = SEEDS_DIR,
) -> dict[str, Any]:
    """Answer a seed's open questions for an agent reviewer, then approve it.

    `answers` is a list of `{"slot", "choice", "entry", "page"}` (other keys are
    ignored). Each changes its slot as Seeds mode does for a person (`lib/seeds.ts`):
    an option's index or `dropped` answers the slot's whole group, `edited` the slot
    alone. The approval is the Approve button's save, so nothing else changes.
    """
    if not is_agent(reviewer) or not reviewer[len(AGENT_PREFIX):].strip():
        raise SeedReviewError(f"An agent reviewer is {AGENT_PREFIX}<name>@<commit>; "
                              "people approve in the labeler")
    reviewer = reviewer.strip()
    with _save_lock:
        current = read_seed(parish_slug, seeds_dir)
        if current is None:
            raise SeedReviewError("No seed file for this parish")
        status = current.get("status")
        if status == DRAFTING:
            raise SeedReviewError("A drafter is still drafting this parish; review it when "
                                  "it is done")
        if status == APPROVED:
            raise SeedReviewError(f"Already approved by {current.get('reviewer')}")
        if status == BLOCKED:
            raise SeedReviewError(f"Blocked ({current.get('blocked_reason')}): a person "
                                  "decides on a blocked parish")
        slots, answered = _answer_slots(current, answers, reviewer)
        still = [s.get("id") for s in slots
                 if isinstance(s, dict) and s.get("status") == NEEDS_HUMAN]
        if still:
            raise SeedReviewError(f"{len(still)} slots are still open: "
                                  f"{', '.join(map(str, still))}")
        detail = _save(conn, parish_slug, {**current, "slots": slots, "status": APPROVED,
                                           "reviewer": reviewer}, seeds_dir)
    seed = detail["seed"]
    return {"parish": parish_slug, "status": seed["status"], "reviewer": seed["reviewer"],
            "approved_at": seed["approved_at"], "answered": answered}


def _kept_entry(slot: dict[str, Any]) -> Any:
    """The entry an excluded slot keeps for review (`keptEntry`): its own, or an option's."""
    if slot.get("entry"):
        return slot["entry"]
    options = [o for o in slot.get("options") or [] if isinstance(o, dict) and o.get("entry")]
    leaning = next((o for o in options if o.get("leaning") is True), None)
    return (leaning or options[0])["entry"] if options else None


def _chosen(slot: dict[str, Any], index: int, answer: dict[str, Any]) -> dict[str, Any] | None:
    """`chooseOption`: the slot settled with one of its options, or None if it has no such."""
    options = slot.get("options") if isinstance(slot.get("options"), list) else []
    option = options[index] if 0 <= index < len(options) else None
    if not isinstance(option, dict):
        return None
    if option.get("entry"):
        return {**slot, "status": SETTLED, "decision": INCLUDE, "entry": option["entry"],
                "answer": answer}
    return {**slot, "status": SETTLED, "decision": EXCLUDE, "entry": _kept_entry(slot),
            "answer": answer}


def _answer_slots(
    seed: dict[str, Any], answers: Any, by: str,
) -> tuple[list[Any], list[dict[str, Any]]]:
    """The file's slots with `answers` applied, and what each answer settled."""
    if not isinstance(answers, list):
        raise SeedReviewError('The answers are a list of {"slot", "choice"} objects')
    slots = list(seed.get("slots")) if isinstance(seed.get("slots"), list) else []
    index = {s.get("id"): i for i, s in enumerate(slots) if isinstance(s, dict)}
    at = utc_now_iso()
    given: dict[str, tuple[Any, ...]] = {}  # slot id: the answer that settled it here
    answered: list[dict[str, Any]] = []
    for n, a in enumerate(answers, 1):
        if not isinstance(a, dict) or not isinstance(a.get("slot"), str) or "choice" not in a:
            raise SeedReviewError(f"Answer {n} must be an object with a slot and a choice")
        slot_id, choice = a["slot"], a["choice"]
        key = (choice, a.get("entry"), a.get("page"))
        if slot_id in given:
            # A group's slots may each be listed with the group's one answer.
            if choice != EDITED and given[slot_id] == key:
                continue
            raise SeedReviewError(f"Answer {n}: {slot_id} is already answered by an earlier "
                                  "answer (of its group, or its own)")
        if slot_id not in index:
            raise SeedReviewError(f"Answer {n}: no slot {slot_id} in this seed")
        slot = slots[index[slot_id]]
        if slot.get("status") != NEEDS_HUMAN:
            raise SeedReviewError(f"Answer {n}: {slot_id} is not an open question")
        is_index = isinstance(choice, int) and not isinstance(choice, bool)
        if not is_index and choice not in (EDITED, DROPPED):
            raise SeedReviewError(f"Answer {n}: choice must be an option's index, {EDITED} "
                                  f"or {DROPPED}, not {choice!r}")
        if choice != EDITED and (a.get("entry") is not None or a.get("page") is not None):
            raise SeedReviewError(f"Answer {n}: only an {EDITED} answer gives an entry or page")
        answer = {"choice": choice, "by": by, "at": at}
        if choice == EDITED:
            if not isinstance(a.get("entry"), dict):
                raise SeedReviewError(f"Answer {n}: an {EDITED} answer gives its entry")
            changed = [{**slot, "status": SETTLED, "decision": INCLUDE, "entry": a["entry"],
                        "page": a.get("page", slot.get("page")), "answer": answer}]
        else:
            # `groupOf`: the slot, and the other open slots of its group.
            group = slot.get("group")
            mates = [s for s in slots if s is slot or group and isinstance(s, dict)
                     and s.get("group") == group and s.get("status") == NEEDS_HUMAN]
            if choice == DROPPED:
                changed = [{**s, "status": SETTLED, "decision": EXCLUDE,
                            "entry": _kept_entry(s), "answer": dict(answer)} for s in mates]
            else:
                chosen = [_chosen(s, choice, dict(answer)) for s in mates]
                if any(c is None for c in chosen):
                    raise SeedReviewError(
                        f"Answer {n}: option {choice} can't settle "
                        f"{', '.join(s['id'] for s, c in zip(mates, chosen) if c is None)}")
                changed = [c for c in chosen if c is not None]
        for s in changed:
            slots[index[s["id"]]] = s
            given[s["id"]] = key
        answered.append({"slots": [s["id"] for s in changed], "choice": choice,
                         "decision": changed[0]["decision"]})
    return slots, answered


def _save(
    conn: sqlite3.Connection, parish_slug: str, body: Any, seeds_dir: Path,
) -> dict[str, Any]:
    current = read_seed(parish_slug, seeds_dir)
    if current is None:
        raise SeedReviewError("No seed file for this parish")
    if current.get("status") == DRAFTING:
        raise SeedReviewError("A drafter is still drafting this parish; review it when it is done")
    if not isinstance(body, dict) or body.get("parish_slug") != parish_slug:
        raise SeedReviewError("The seed's parish_slug does not match the parish")
    if body.get("status") not in REVIEW_STATUSES:
        raise SeedReviewError(f"A review sets status to one of {', '.join(REVIEW_STATUSES)}")
    seed = {**current, **{k: body.get(k) for k in REVIEWED_KEYS}}
    if seed["status"] == APPROVED:
        if not isinstance(seed["reviewer"], str) or not seed["reviewer"].strip():
            raise SeedReviewError("Say who you are (the reviewer) before approving")
        if current.get("status") != APPROVED or not current.get("approved_at"):
            seed["approved_at"] = utc_now_iso()
    else:
        seed["approved_at"] = None
    if seed["status"] != BLOCKED:
        seed["blocked_reason"] = None
    errors = validate_seed(seed, parish_slug=parish_slug)
    if not errors and seed["status"] == APPROVED:
        errors = check_seed(conn, seed, parish_slug=parish_slug)
    if errors:
        raise SeedReviewError("; ".join(errors[:5]) + (" …" if len(errors) > 5 else ""))
    write_seed_file(seed, seeds_dir)
    detail = seed_detail(conn, parish_slug, seeds_dir)
    assert detail is not None
    return detail


