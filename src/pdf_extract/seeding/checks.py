"""`seed check`: a seed file against the database, as the loader and the labeler need it.

`files.validate_seed` checks the file's shape. This adds what needs the
database (docs/seeding-plan.md, "Tools"):

- every entry parses as `pnpm schedule seed` would (`schedule.entries.parse_entry`),
  with an included entry's church one of the parish's (one left out, or an
  option, may name a chapel elsewhere);
- no two included entries share a slot;
- the dated entries a seed holds are on or after its `as_of` date;
- the file's bulletins are the parish's, and `as_of` is the fetch time of the
  newest one the agent read (in a test run, of the labeled bulletin);
- the newest listed bulletin is marked read, and an agent's settled inclusions
  cite its own reading there at their page (reviewer answers may include older slots),
  except what the newest bulletin can't be expected to print (`older_evidence_ok`):
  a weeks-of-the-month slot none of whose weeks fall in the newest bulletin's
  week, or a dated entry from `as_of` on that an older bulletin announced;
- a historical eval contains no live website evidence.
"""

from __future__ import annotations

import calendar
import sqlite3
from datetime import date, timedelta
from typing import Any

from pdf_extract.bulletin_week import bulletin_week
from pdf_extract.labeling.labels import DAYS, WEEKS_OF_MONTH
from pdf_extract.schedule.entries import UNKNOWN_CHURCH, EntryError, parse_entry
from pdf_extract.schedule.store import normalize_as_of, parish_churches
from pdf_extract.seeding.files import (
    AGENT,
    BLOCKED,
    DRAFTING,
    INCLUDE,
    NEEDS_HUMAN,
    WEBSITE,
    newest_read_bulletin,
    resolve_hash,
    validate_seed,
)

# The days a bulletin's calendar is taken to cover: its week's Sunday through
# the next Sunday (an issue's calendar usually runs from its Sunday to the next).
COVERED_DAYS = 8


def weeks_of(day: date) -> set[str]:
    """Which of `weeks_of_month`'s weeks `day` is in for its weekday: `first` to
    `fifth`, and `last` when it is that weekday's last in the month."""
    weeks = {WEEKS_OF_MONTH[(day.day - 1) // 7]}
    if day.day + 7 > calendar.monthrange(day.year, day.month)[1]:
        weeks.add("last")
    return weeks


def covered_weeks(bulletin: dict[str, Any], day_of_week: str) -> set[str] | None:
    """The weeks of the month `day_of_week` falls in during the days `bulletin` covers,
    or None when the bulletin has no date to tell."""
    start = bulletin_week(bulletin)
    if start is None or day_of_week not in DAYS:
        return None
    weeks: set[str] = set()
    for offset in range(COVERED_DAYS):
        day = start + timedelta(days=offset)
        if DAYS[day.weekday()] == day_of_week:
            weeks |= weeks_of(day)
    return weeks


def older_evidence_ok(
    seed: dict[str, Any], slot: dict[str, Any], newest: dict[str, Any], as_of_date: str | None,
) -> bool:
    """Whether a settled inclusion may rest on an older bulletin than the newest read.

    Two kinds of slot don't appear in every issue, so the newest one not printing
    them says nothing:

    - a weekly slot on some weeks of the month ("First Friday"), when none of its
      weeks falls in the newest bulletin's week. It must cite the newest bulletin
      read whose week does hold one of them, if any does: that one would print it.
    - a dated entry on or after `as_of` an older bulletin announced (a Mass on
      All Souls Day printed a month ahead).

    Either way the slot has no `page` (the newest bulletin doesn't print it) and
    an agent source on a read bulletin at a page.
    """
    entry = slot["entry"]
    if slot["page"] is not None or not isinstance(entry, dict):
        return False
    read = sorted(
        (b for b in seed["bulletins"] if b["read"]),
        key=lambda b: normalize_as_of(b["fetched_at"]), reverse=True,
    )
    cited = {
        resolve_hash(seed, s.get("bulletin")) for s in slot["sources"]
        if s.get("source") == AGENT and s.get("page") is not None
    }
    cited_read = [b for b in read if b["content_hash"] in cited]
    if not cited_read:
        return False
    if entry.get("event_kind") == "weekly":
        weeks = set(entry.get("weeks_of_month") or [])
        if not weeks or entry.get("exclude_weeks"):
            return False
        here = covered_weeks(newest, entry.get("day_of_week") or "")
        if here is None or here & weeks:
            return False
        covering = [b for b in read if (covered_weeks(b, entry["day_of_week"]) or set()) & weeks]
        if not covering:
            return True
        latest = normalize_as_of(covering[0]["fetched_at"])
        return any(normalize_as_of(b["fetched_at"]) >= latest for b in cited_read)
    return bool(as_of_date and entry.get("date") and entry["date"] >= as_of_date)


def _parish_id(conn: sqlite3.Connection, parish_slug: str) -> int | None:
    row = conn.execute("SELECT id FROM parish WHERE slug = ?", (parish_slug,)).fetchone()
    return None if row is None else int(row[0])


def _entry_problem(
    raw: dict[str, Any], churches: dict[str, int], where: str, *, outside_ok: bool = False,
) -> str | None:
    """Why the entry can't be stored, or None. With `outside_ok`, a church that isn't the
    parish's is fine: an entry left out on purpose may be a chapel elsewhere."""
    try:
        parse_entry(raw, churches)
    except EntryError as exc:
        if outside_ok and exc.reason == UNKNOWN_CHURCH:
            return None
        return f"{where}: {exc.reason}: {exc}"
    return None


def check_seed(
    conn: sqlite3.Connection,
    seed: Any,
    *,
    parish_slug: str,
    cutoff: str | None = None,
    check_bulletins: bool = True,
    check_evidence: bool = True,
) -> list[str]:
    """Every problem with a seed file (empty when it can be reviewed and loaded).

    A file still `drafting` is reported as such, since `seed check` is the
    last step of a draft. `check_bulletins` off skips comparing the file's
    bulletins with the database's, for a database that may not hold them all
    (the loader resolves what it can and needs only the entries).
    `check_evidence` off trusts a person's already-approved decisions: newer
    drafting evidence rules must not prevent previously approved seeds loading.
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
    newest = newest_read_bulletin(seed)
    latest = max(seed["bulletins"], key=lambda b: normalize_as_of(b["fetched_at"]), default=None)
    if check_evidence and latest is not None and not latest["read"]:
        problems.append(
            f"newest listed bulletin {latest['content_hash'][:12]} must be marked read: "
            "use `pnpm seed mark-read` after reading it, even when no slot cites it"
        )
    as_of_date = normalize_as_of(seed["as_of"])[:10] if seed["as_of"] else None
    slots_by_identity: dict[str, str] = {}
    for i, slot in enumerate(seed["slots"]):
        where = f"slots[{i}] ({slot['id']})"
        included = slot["decision"] == INCLUDE and slot["status"] != NEEDS_HUMAN
        if check_evidence and included and slot["answer"] is None:
            # A reviewer may explicitly include an older/website-backed option.
            # An agent's settled inclusion needs its own reading of the anchor PDF.
            anchored = newest is not None and slot["page"] is not None and any(
                source.get("source") == AGENT
                and resolve_hash(seed, source.get("bulletin")) == newest["content_hash"]
                and source.get("page") == slot["page"]
                for source in slot["sources"]
            )
            if not anchored and not (
                newest is not None and older_evidence_ok(seed, slot, newest, as_of_date)
            ):
                problems.append(
                    f"{where}: a settled inclusion needs an agent source on the newest "
                    "bulletin at its page; otherwise leave it needs_human with page null "
                    "(a weeks-of-the-month slot whose weeks the newest bulletin's week "
                    "doesn't hold, or a dated entry from as_of on, may instead cite an older "
                    "bulletin read, with page null)"
                )
        if cutoff is not None and any(s.get("source") == WEBSITE for s in slot["sources"]):
            problems.append(
                f"{where}: website sources are not allowed in a historical test run; "
                "use only bulletins and history within its cutoff"
            )
        if slot["entry"] is not None:
            problem = _entry_problem(
                slot["entry"], churches, f"{where}.entry", outside_ok=not included,
            )
            if problem:
                problems.append(problem)
            elif included:
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
                # An option is only a proposal: choosing one that names a church
                # outside the parish fails the included slot's check instead.
                problem = _entry_problem(
                    option["entry"], churches, f"{where}.options[{j}].entry", outside_ok=True,
                )
                if problem:
                    problems.append(problem)

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
