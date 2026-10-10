"""`seed check`: a seed file against the database, as the loader and the labeler need it.

`files.validate_seed` checks the file's shape. This adds what needs the
database (docs/seeding-plan.md, "Tools"):

- every entry parses as `pnpm schedule seed` would (`schedule.entries.parse_entry`),
  with its church one of the parish's;
- no two included entries share a slot;
- the dated entries a seed holds are on or after its `as_of` date;
- the file's bulletins are the parish's, and `as_of` is the fetch time of the
  newest one the agent read (in a test run, of the labeled bulletin).
"""

from __future__ import annotations

import sqlite3
from typing import Any

from pdf_extract.schedule.entries import EntryError, parse_entry
from pdf_extract.schedule.store import normalize_as_of, parish_churches
from pdf_extract.seeding.files import (
    BLOCKED,
    DRAFTING,
    INCLUDE,
    NEEDS_HUMAN,
    newest_read_bulletin,
    validate_seed,
)


def _parish_id(conn: sqlite3.Connection, parish_slug: str) -> int | None:
    row = conn.execute("SELECT id FROM parish WHERE slug = ?", (parish_slug,)).fetchone()
    return None if row is None else int(row[0])


def _entry_problem(raw: dict[str, Any], churches: dict[str, int], where: str) -> str | None:
    try:
        parse_entry(raw, churches)
    except EntryError as exc:
        return f"{where}: {exc.reason}: {exc}"
    return None


def check_seed(
    conn: sqlite3.Connection,
    seed: Any,
    *,
    parish_slug: str,
    cutoff: str | None = None,
    check_bulletins: bool = True,
) -> list[str]:
    """Every problem with a seed file (empty when it can be reviewed and loaded).

    A file still `drafting` is reported as such, since `seed check` is the
    last step of a draft. `check_bulletins` off skips comparing the file's
    bulletins with the database's, for a database that may not hold them all
    (the loader resolves what it can and needs only the entries).
    """
    problems = validate_seed(seed, parish_slug=parish_slug)
    if problems:
        return problems
    parish_id = _parish_id(conn, parish_slug)
    if parish_id is None:
        return [f"parish {parish_slug} is not in data/parishes.csv"]
    if seed["status"] == DRAFTING:
        problems.append(
            "status is still drafting: set needs_review (open questions) or ready, or blocked"
        )
    if seed["status"] == BLOCKED:
        return problems

    churches = parish_churches(conn, parish_id)
    as_of_date = normalize_as_of(seed["as_of"])[:10] if seed["as_of"] else None
    slots_by_identity: dict[str, str] = {}
    for i, slot in enumerate(seed["slots"]):
        where = f"slots[{i}] ({slot['id']})"
        if slot["entry"] is not None:
            problem = _entry_problem(slot["entry"], churches, f"{where}.entry")
            if problem:
                problems.append(problem)
            elif slot["decision"] == INCLUDE and slot["status"] != NEEDS_HUMAN:
                identity = parse_entry(slot["entry"], churches).identity_key
                if identity in slots_by_identity:
                    problems.append(
                        f"{where} is the same slot as {slots_by_identity[identity]}: "
                        "one of them must go"
                    )
                slots_by_identity.setdefault(identity, slot["id"])
                date = slot["entry"].get("date")
                if as_of_date and slot["entry"]["event_kind"] != "weekly" and date < as_of_date:
                    problems.append(
                        f"{where} is dated {date}, before as_of ({as_of_date}): a seed holds "
                        "only dated entries from as_of on"
                    )
        for j, option in enumerate(slot["options"] or []):
            if option.get("entry") is not None:
                problem = _entry_problem(option["entry"], churches, f"{where}.options[{j}].entry")
                if problem:
                    problems.append(problem)

    newest = newest_read_bulletin(seed)
    if seed["as_of"] is not None:
        as_of = normalize_as_of(seed["as_of"])
        if newest is None:
            problems.append("as_of names a bulletin, but no bulletin is marked read")
        elif normalize_as_of(newest["fetched_at"]) != as_of:
            problems.append(
                f"as_of must be the fetch time of the newest bulletin read "
                f"({newest['fetched_at']}, {newest['content_hash'][:12]}), not {seed['as_of']}"
            )
        if cutoff is not None and as_of != normalize_as_of(cutoff):
            problems.append(f"in a test run as_of is the labeled bulletin's fetch time, {cutoff}")
        for b in seed["bulletins"]:
            if normalize_as_of(b["fetched_at"]) > as_of and b["read"]:
                problems.append(f"bulletin {b['content_hash'][:12]} is read but newer than as_of")
    if check_bulletins:
        problems.extend(_bulletin_problems(conn, seed, parish_id, cutoff))
    return problems


def _bulletin_problems(
    conn: sqlite3.Connection, seed: dict[str, Any], parish_id: int, cutoff: str | None,
) -> list[str]:
    problems = []
    for b in seed["bulletins"]:
        rows = conn.execute(
            "SELECT fetched_at FROM bulletin WHERE parish_id = ? AND content_hash = ?",
            (parish_id, b["content_hash"]),
        ).fetchall()
        short = b["content_hash"][:12]
        if not rows:
            problems.append(f"bulletin {short} is not one of the parish's in the database")
            continue
        fetched = {normalize_as_of(r["fetched_at"]) for r in rows if r["fetched_at"]}
        if normalize_as_of(b["fetched_at"]) not in fetched:
            problems.append(
                f"bulletin {short} was fetched at {', '.join(sorted(fetched))}, "
                f"not {b['fetched_at']}"
            )
        if cutoff is not None and normalize_as_of(b["fetched_at"]) > normalize_as_of(cutoff):
            problems.append(f"bulletin {short} was fetched after the test run's cutoff")
    return problems
