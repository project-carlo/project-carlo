"""The labeler's Seeds mode: the queue of seed files, one file for review, and saving it.

A reviewer settles the open questions, may edit, drop or reopen any slot, and
approves the parish. The server keeps what the agent wrote about the parish
(its bulletins, calls, summary and `as_of`) as the file has it, and takes the
slots, the status and the reviewer from the request. An approved file must
pass `seed check`, and its `approved_at` is stamped here.
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
    NEEDS_REVIEW,
    READY,
    SEEDS_DIR,
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


def _save(
    conn: sqlite3.Connection, parish_slug: str, body: Any, seeds_dir: Path,
) -> dict[str, Any]:
    current = read_seed(parish_slug, seeds_dir)
    if current is None:
        raise SeedReviewError("No seed file for this parish")
    if current.get("status") == DRAFTING:
        raise SeedReviewError("A subagent is still drafting this parish; review it when it is done")
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


