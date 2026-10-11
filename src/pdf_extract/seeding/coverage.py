"""A seed file's slots against extract mode's history: which history event is which slot.

One matching rule serves `seed finalize`, which attaches a slot's history
sources, and `seed diff`, which lists what the two disagree on. A history event
matches an entry (a slot's or an option's) when its type and start time are the
entry's, its church is the entry's (when the entry names one), and:

- a weekly event: the entry is weekly, on the same day;
- a dated event: the entry is dated the same day, or is weekly on that weekday
  and the event is not a cancellation (the policy never repeats a weekly slot as
  a dated one, but a cancellation of it is news).

For `seed diff` alone, a cancellation is also accounted for by a weekly slot
left out on that weekday and time: the Mass it calls off isn't in the seed.

`weeks_of_month`, `season` and end times are not compared: they are what a
drafter reads the bulletin for, and history's are often missing.

History bulletins are `queries.recent_history`'s: extract mode's events per
bulletin, newest first. A bulletin it flagged as wrong is left out here.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from pdf_extract.labeling.labels import DAYS
from pdf_extract.schedule.store import normalize_as_of
from pdf_extract.seeding.files import (
    EXCLUDE,
    HISTORY,
    included_slots,
    newest_read_bulletin,
    resolve_hash,
)


# ── Saying what an event is ─────────────────────────────────────────────────
def event_parts(ev: dict[str, Any]) -> dict[str, str]:
    """An event's fields as `seed history` prints them, and as a history source says them."""
    end = f"–{ev['end_time']}" if ev.get("end_time") else ""
    extra = []
    if ev.get("weeks_of_month"):
        excluded = "except " if ev.get("exclude_weeks") else ""
        extra.append(f"weeks {excluded}" + "/".join(ev["weeks_of_month"]))
    if ev.get("season"):
        s = ev["season"]
        extra.append(f"season {s['start_month']}/{s.get('start_day') or ''}–"
                     f"{s['end_month']}/{s.get('end_day') or ''}")
    if ev.get("cancelled"):
        extra.append("CANCELLED")
    if ev.get("note"):
        extra.append(f"“{ev['note']}”")
    return {
        "kind": ev.get("event_kind") or "?",
        "type": ev.get("event_type") or "?",
        "when": ev.get("day_of_week") or ev.get("date") or "?",
        "time": (ev.get("start_time") or "?") + end,
        "church": ev.get("church_slug") or "?",
        "extra": "; ".join(extra),
    }


def event_said(ev: dict[str, Any]) -> str:
    """One line for an event: `weekly mass Saturday 16:00 st-marys-oswego`."""
    p = event_parts(ev)
    said = f"{p['kind']} {p['type']} {p['when']} {p['time']} {p['church']}"
    return f"{said}  {p['extra']}" if p["extra"] else said


# ── Matching ────────────────────────────────────────────────────────────────
def _weekday(iso: Any) -> str | None:
    try:
        return DAYS[date.fromisoformat(iso).weekday()]
    except (TypeError, ValueError):
        return None


def matches(entry: Any, event: dict[str, Any]) -> bool:
    """Whether history's `event` is the slot `entry` describes (see the module's docstring)."""
    if not isinstance(entry, dict):
        return False
    if entry.get("event_type") != event.get("event_type"):
        return False
    if not event.get("start_time") or entry.get("start_time") != event["start_time"]:
        return False
    church = entry.get("church_slug")
    if church and event.get("church_slug") and church != event["church_slug"]:
        return False
    if event.get("event_kind") == "weekly":
        return not entry.get("date") and entry.get("day_of_week") == event.get("day_of_week")
    if entry.get("date"):
        return entry["date"] == event.get("date")
    return not event.get("cancelled") and entry.get("day_of_week") == _weekday(event.get("date"))


def slot_entries(slot: dict[str, Any]) -> list[dict[str, Any]]:
    """A slot's entry and its options' entries: every reading of it the file proposes."""
    entries = [slot.get("entry")]
    options = slot.get("options")
    for option in options if isinstance(options, list) else []:
        if isinstance(option, dict):
            entries.append(option.get("entry"))
    return [e for e in entries if isinstance(e, dict)]


def _usable(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [b for b in history if not b.get("wrong_bulletin")]


# ── finalize: history sources ───────────────────────────────────────────────
def attach_history(
    seed: dict[str, Any], slot: dict[str, Any], history: list[dict[str, Any]],
) -> dict[str, Any]:
    """`slot` with a history source for each history event that matches one of its entries.

    Only bulletins the file lists are cited, and a bulletin the slot already has
    a history source for is left as the drafter wrote it, so running it twice
    adds nothing.
    """
    sources = slot.get("sources")
    if not isinstance(sources, list):
        return slot
    entries = slot_entries(slot)
    if not entries:
        return slot
    cited = {
        resolve_hash(seed, s.get("bulletin")) for s in sources
        if isinstance(s, dict) and s.get("source") == HISTORY
    }
    added = []
    for bulletin in _usable(history):
        full = resolve_hash(seed, bulletin["content_hash"])
        if full is None or full in cited:
            continue
        seen = set()
        for ev in bulletin["events"]:
            if not any(matches(e, ev) for e in entries):
                continue
            said = event_said(ev)
            if (said, ev.get("page_number")) in seen:
                continue
            seen.add((said, ev.get("page_number")))
            source = {"source": HISTORY, "bulletin": full[:12], "said": said}
            if ev.get("page_number"):
                source["page"] = ev["page_number"]
            added.append(source)
    return {**slot, "sources": sources + added} if added else slot


# ── seed diff ───────────────────────────────────────────────────────────────
def scope_date(seed: dict[str, Any]) -> str | None:
    """The first date a seed's dated entries may have: `as_of`'s, or the newest bulletin's."""
    as_of = seed.get("as_of")
    if not isinstance(as_of, str):
        newest = newest_read_bulletin(seed)
        if newest is None:
            fetched = [b.get("fetched_at") for b in seed.get("bulletins") or []
                       if isinstance(b, dict) and isinstance(b.get("fetched_at"), str)]
            as_of = max(fetched, key=normalize_as_of, default=None)
        else:
            as_of = newest["fetched_at"]
    try:
        return normalize_as_of(as_of)[:10] if as_of else None
    except ValueError:
        return None


def diff(seed: dict[str, Any], history: list[dict[str, Any]]) -> dict[str, Any]:
    """What history and the seed disagree on.

    `missing`: history events no slot or option entry matches, included or left
    out, one row per event with the bulletins it is in. A dated event before the
    seed's scope (`scope_date`) is left out: a seed doesn't hold it.
    `unseen`: included slots no history event matches.
    """
    slots = [s for s in seed.get("slots") or [] if isinstance(s, dict)]
    entries = [e for s in slots for e in slot_entries(s)]
    left_out = [s["entry"] for s in slots
                if s.get("decision") == EXCLUDE and isinstance(s.get("entry"), dict)]
    first = scope_date(seed)
    usable = _usable(history)
    missing: dict[str, dict[str, Any]] = {}
    for bulletin in usable:
        for ev in bulletin["events"]:
            if ev.get("event_kind") != "weekly" and first and (ev.get("date") or "") < first:
                continue
            if any(matches(e, ev) for e in entries):
                continue
            if ev.get("cancelled") and any(
                matches(e, {**ev, "cancelled": False}) for e in left_out
            ):
                continue
            said = event_said(ev)
            row = missing.setdefault(said, {"said": said, "event": ev, "bulletins": [],
                                            "pages": []})
            if bulletin["short"] not in row["bulletins"]:
                row["bulletins"].append(bulletin["short"])
            if ev.get("page_number") and ev["page_number"] not in row["pages"]:
                row["pages"].append(ev["page_number"])
    unseen = [
        {"slot": s.get("id"), "said": event_said(s["entry"]), "entry": s["entry"]}
        for s in included_slots(seed)
        if isinstance(s.get("entry"), dict)
        and not any(matches(s["entry"], ev) for b in usable for ev in b["events"])
    ]
    return {
        "bulletins": [b["short"] for b in usable],
        "scope_date": first,
        "missing": list(missing.values()),
        "unseen": unseen,
    }


def missing_warning(row: dict[str, Any], of: int) -> str:
    """A `missing` row as `seed finalize` warns of it."""
    pages = "/".join(f"p{p}" for p in row["pages"])
    return (f"history has {row['said']} ({len(row['bulletins'])} of {of} bulletins"
            + (f", {pages}" if pages else "") + ") and no slot or option covers it")
