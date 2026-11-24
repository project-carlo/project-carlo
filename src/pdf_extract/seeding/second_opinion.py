"""The second opinion in a seed file: a blind reading of the bulletins, compared with the slots.

docs/seed-second-opinion-plan.md has the design. The dispatcher asks gpt-6-luna
(`classifiers.seed_opinion`) to read a parish's newest bulletins on its own
(`pick_bulletins`, `run_opinion`). Once the drafter's gates pass, it writes the
reading into the file as `second_opinion` (`reveal`) and compares it with the
slots (`seeding.opinion.compare`). Each difference must then be resolved:

- **changed**: the drafter changed the seed and the difference is gone;
- **asked**: a `needs_human` question has the opinion's reading as an option;
- **kept**: `seed opinion keep` records a bulletin page and a rule that support the
  slot as it is;
- **answered**: a reviewer answered the slot's question;
- **auto**: the opinion couldn't see what settled it (`opinion.RESOLVED_REASONS`:
  the website, a settled R22-R26 exclusion, bulletins it wasn't given).

The comparison runs again on every check (`refresh`), so a difference a later edit
creates needs resolving too, and one the seed no longer has is resolved by the
change. A difference keeps its id (and a kept one stays kept) while its kind, the
opinion's entries, the slots and what they hold stay the same. Matching slots get a source naming the
opinion's call ("gpt-6-luna read the same: B1 p2 ..."), so a reviewer sees which
slots two model families agree on.

The opinion's entries are the dispatcher's: `seed check` fails when they no longer
hash to `entries_sha256`, or to the hash the dispatcher kept (`OPINION_SHA_ENV`).
"""

from __future__ import annotations

import copy
import os
from collections.abc import Callable
from datetime import date
from hashlib import sha256
from typing import Any, Protocol

from pdf_extract.classifiers import pricing
from pdf_extract.classifiers.seed_opinion import (
    bulletin_reads,
    label,
    opinion_entries,
    parse_reply,
    render_context,
)
from pdf_extract.model import ENTRY_KEYS, canonical_json, normalize_as_of, sha256_text
from pdf_extract.seeding import opinion as compare_mod
from pdf_extract.seeding.files import (
    ANSWERED,
    APPROVED,
    ASKED,
    AUTO,
    CHANGED,
    INCLUDE,
    KEPT,
    NEEDS_HUMAN,
    OPINION,
    RULE_ID,
    SETTLED,
    next_call_id,
    resolve_hash,
)
from pdf_extract.storage import utc_now_iso

SECTION = "second_opinion"
MIN_BULLETINS = 2
MAX_BULLETINS = 4
# Set by the dispatcher for its gates: `parish=sha256 ...`, the hash of the opinion's
# entries it revealed to each parish.
OPINION_SHA_ENV = "CARLO_SEED_OPINION_SHA256"


class OpinionError(ValueError):
    """A reply that can't be revealed, or a resolution that can't be recorded."""


# ── The bulletins and the call ──────────────────────────────────────────────
def pick_bulletins(
    bulletins: list[dict[str, Any]], stored: Callable[[str], bool], *,
    most: int = MAX_BULLETINS, as_of: str | None = None,
) -> list[dict[str, Any]]:
    """The newest `most` bulletins with a stored PDF, one per issue week, newest first.

    Only those fetched at or before `as_of` (the drafter's newest read) count. An issue
    week is the published date, or for an undated issue its content hash, so repeat
    fetches of one issue count once.
    """
    limit = normalize_as_of(as_of) if as_of else None
    out: list[dict[str, Any]] = []
    weeks: set[str] = set()
    for b in sorted(bulletins, key=lambda b: normalize_as_of(b["fetched_at"]), reverse=True):
        if limit is not None and normalize_as_of(b["fetched_at"]) > limit:
            continue
        week = b.get("published_date") or b["content_hash"]
        if week in weeks or not stored(b["content_hash"]):
            continue
        weeks.add(week)
        out.append({k: b.get(k) for k in ("content_hash", "fetched_at", "published_date")})
        if len(out) == most:
            break
    return out


def today_of(bulletins: list[dict[str, Any]]) -> date:
    """The newest bulletin's fetch date: "today" as the pipeline saw it."""
    return date.fromisoformat(str(bulletins[0]["fetched_at"])[:10])


def request_key(version: str, parish: str, bulletins: list[dict[str, Any]],
                churches: list[dict[str, Any]], today: date) -> str:
    """What a reply is stored under: the caller's version (model, prompt, settings), the
    bulletins, the churches and today. The same request is never paid for twice."""
    asked = canonical_json({
        "version": version, "parish": parish,
        "bulletins": [b["content_hash"] for b in bulletins],
        "churches": sorted(churches, key=lambda c: str(c.get("slug"))),
        "today": today.isoformat(),
    })
    return sha256(asked.encode("utf-8")).hexdigest()[:32]


class Caller(Protocol):
    model: str

    @property
    def version(self) -> str: ...

    def opinion(self, pdfs: list[bytes], context: str) -> Any: ...


class ReplyStore(Protocol):
    """Where replies are kept by request key (the dispatcher's ledger)."""

    def get(self, key: str) -> dict[str, Any] | None: ...

    def put(self, key: str, record: dict[str, Any]) -> None: ...


def run_opinion(
    caller: Caller, parish: str, bulletins: list[dict[str, Any]],
    churches: list[dict[str, Any]], store: ReplyStore, *,
    read_pdf: Callable[[str, str], bytes],
) -> dict[str, Any]:
    """The opinion on one parish's bulletins (newest first): the stored reply under its
    request key if there is one, else one call, whose raw reply is stored before it is
    returned. The record has `cached` set to whether it was stored already. `read_pdf`
    is `queries.bulletin_pdf`, or a test's."""
    if len(bulletins) < MIN_BULLETINS:
        raise OpinionError(f"{len(bulletins)} bulletin(s) with a stored PDF; an opinion "
                           f"reads {MIN_BULLETINS} or more")
    today = today_of(bulletins)
    key = request_key(caller.version, parish, bulletins, churches, today)
    record = store.get(key)
    if record is not None:
        return {**record, "cached": True}
    pdfs = [read_pdf(parish, b["content_hash"]) for b in bulletins]
    reply = caller.opinion(pdfs, render_context(churches, today, bulletins))
    cost = pricing.call_cost(caller.model, reply.usage, service_tier=reply.service_tier)
    record = {
        "request_key": key, "parish": parish, "model": caller.model,
        "version": caller.version, "today": today.isoformat(),
        "bulletins": [{k: b.get(k) for k in ("content_hash", "fetched_at", "published_date")}
                      for b in bulletins],
        "churches": churches, "text": reply.text, "usage": reply.usage,
        "service_tier": reply.service_tier, "served_model": reply.served_model,
        "latency_ms": reply.latency_ms,
        "cost_usd": None if cost is None else round(cost, 6), "asked_at": utc_now_iso(),
    }
    store.put(key, record)
    return {**record, "cached": False}


# ── Revealing it ────────────────────────────────────────────────────────────
def section(seed: dict[str, Any]) -> dict[str, Any] | None:
    found = seed.get(SECTION)
    return found if isinstance(found, dict) else None


def entries_sha(entries: Any) -> str:
    return sha256_text(canonical_json(entries))


def _evidence(items: Any) -> list[dict[str, Any]]:
    out = []
    for e in items if isinstance(items, list) else []:
        if not isinstance(e, dict):
            continue
        page = e.get("page")
        out.append({"bulletin": str(e.get("bulletin") or ""),
                    "page": page if isinstance(page, int) and not isinstance(page, bool)
                    and page >= 1 else None,
                    "quote": str(e.get("quote") or "")})
    return out


def _source_prefix(sec: dict[str, Any]) -> str:
    return f"{sec.get('model')} read the same"


def _drop_agreements(seed: dict[str, Any], sec: dict[str, Any]) -> None:
    """Take off the sources an earlier refresh added for the opinion's agreements."""
    prefix = _source_prefix(sec)
    for slot in seed.get("slots") or []:
        if isinstance(slot, dict) and isinstance(slot.get("sources"), list):
            slot["sources"] = [s for s in slot["sources"] if not (
                isinstance(s, dict) and s.get("source") == sec.get("call")
                and str(s.get("said") or "").startswith(prefix))]


def reveal(seed: dict[str, Any], record: dict[str, Any], *, at: str | None = None,
           ) -> dict[str, Any]:
    """The seed with `record` (`run_opinion`'s) written in as its second opinion, compared.

    A second opinion already in the file is replaced; its call stays in `calls`.
    """
    payload, _ = parse_reply(str(record.get("text") or ""))
    if payload is None:
        raise OpinionError("the reply is not JSON")
    seed = copy.deepcopy(seed)
    at = at or utc_now_iso()
    found = opinion_entries(payload)
    slugs = [str(c.get("slug")) for c in record.get("churches") or [] if isinstance(c, dict)]
    compare_mod.fix_church_slugs(found, slugs)
    entries = [{"id": f"o{i}", "entry": {k: e.get(k) for k in ENTRY_KEYS},
                "evidence": _evidence(e.get("evidence")),
                "problems": [str(p) for p in e.get("problems") or []]}
               for i, e in enumerate(found, start=1)]
    bulletins = [{"label": label(i), "content_hash": b["content_hash"],
                  "fetched_at": b.get("fetched_at"), "published_date": b.get("published_date")}
                 for i, b in enumerate(record["bulletins"])]
    old = section(seed)
    if old is not None:
        _drop_agreements(seed, old)
    calls = seed.setdefault("calls", [])
    call_id = next_call_id(seed)
    listed = next((b["content_hash"] for b in bulletins if resolve_hash(seed, b["content_hash"])),
                  bulletins[0]["content_hash"])
    calls.append({"id": call_id, "kind": OPINION, "model": record["model"],
                  "classifier_version": record["version"], "bulletin": listed,
                  "bulletins": [b["content_hash"] for b in bulletins],
                  "cached": bool(record.get("cached")), "cost_usd": record.get("cost_usd"),
                  "at": at})
    seed[SECTION] = {
        "model": record["model"], "version": record["version"], "call": call_id,
        "request_key": record["request_key"], "today": record["today"], "revealed_at": at,
        "bulletins": bulletins, "cost_usd": record.get("cost_usd"),
        "reads": bulletin_reads(payload),
        "church_list_needs_review": payload.get("church_list_needs_review") is True,
        "entries": entries, "entries_sha256": entries_sha(entries), "differences": [],
    }
    return refresh(seed)


# ── Comparing it, every time ────────────────────────────────────────────────
def compare(seed: dict[str, Any]) -> dict[str, Any] | None:
    """`opinion.compare` of the file's slots and its second opinion, or None without one."""
    sec = section(seed)
    if sec is None:
        return None
    entries = [{**e["entry"], "_id": e["id"], "evidence": e.get("evidence") or []}
               for e in sec.get("entries") or []
               if isinstance(e, dict) and isinstance(e.get("entry"), dict)]
    seen = [b["content_hash"] for b in sec.get("bulletins") or [] if isinstance(b, dict)]
    return compare_mod.compare(seed, entries, str(sec.get("today")), seen_bulletins=seen)


def _unique(values: list[Any]) -> list[Any]:
    return list(dict.fromkeys(v for v in values if v))


def describe_group(entries: list[dict[str, Any] | None]) -> str:
    """Several readings of one difference, their weekdays joined: `mass Mon,Tue 08:00 @x`."""
    entries = [(e.get("overnight_of") or e) for e in entries if isinstance(e, dict)]
    if not entries:
        return "-"
    lines = _unique([compare_mod.describe(e) for e in entries])
    days = _unique([(e.get("day_of_week") or "")[:3] for e in entries
                    if compare_mod.weekly(e)])
    if len(lines) > 1 and len(days) == len(lines) and all(compare_mod.weekly(e) for e in entries):
        parts = lines[0].split(" ")
        parts[1] = ",".join(days)
        return " ".join(parts)
    return "; ".join(lines)


def _item(group: list[dict[str, Any]]) -> dict[str, Any]:
    first = group[0]
    return {
        "kind": first["kind"], "fields": list(first.get("fields") or []),
        "opinion": _unique([(d.get("opinion") or {}).get("_id") for d in group]),
        "slots": _unique([d.get("slot") for d in group]),
        "opinion_said": describe_group([d.get("opinion") for d in group]),
        "seed_said": describe_group([d.get("seed") for d in group]),
        "auto": first.get("resolved"),
    }


def _signature(item: dict[str, Any]) -> tuple:
    """What makes a difference the same one: a change to either reading is a new one."""
    return (item["kind"], tuple(item["opinion"]), tuple(item["slots"]), tuple(item["fields"]),
            item["seed_said"])


def _next_id(items: list[dict[str, Any]]) -> Callable[[], str]:
    taken = [int(i["id"][1:]) for i in items if isinstance(i.get("id"), str)
             and i["id"][1:].isdigit()]
    counter = iter(range(max(taken, default=0) + 1, 1_000_000))
    return lambda: f"d{next(counter)}"


def refresh(seed: dict[str, Any]) -> dict[str, Any]:
    """The seed with its second opinion compared again (module docstring): differences
    resolved by what changed, kept ones kept while they stand, new ones open, and the
    opinion's call a source on each slot it agrees with. A seed without one is returned
    as it is."""
    sec = section(seed)
    if sec is None:
        return seed
    seed = copy.deepcopy(seed)
    sec = seed[SECTION]
    result = compare(seed)
    assert result is not None
    slots = {s.get("id"): s for s in seed.get("slots") or [] if isinstance(s, dict)}
    recorded = [d for d in sec.get("differences") or [] if isinstance(d, dict)]
    by_signature = {_signature(d): d for d in recorded if all(
        isinstance(d.get(k), list) for k in ("opinion", "slots", "fields"))}
    new_id = _next_id(recorded)
    out: list[dict[str, Any]] = []
    seen: set[tuple] = set()
    for group in result["groups"]:
        item = _item(group)
        signature = _signature(item)
        seen.add(signature)
        old = by_signature.get(signature)
        auto = item.pop("auto")
        if auto:
            resolution: dict[str, Any] | None = {"how": AUTO, "reason": auto}
        elif item["kind"] == compare_mod.QUESTION:
            resolution = {"how": ASKED}
        elif any(isinstance(slots.get(s, {}).get("answer"), dict) for s in item["slots"]):
            resolution = {"how": ANSWERED}
        elif old is not None and isinstance(old.get("resolution"), dict) \
                and old["resolution"].get("how") == KEPT:
            resolution = old["resolution"]
        else:
            resolution = None
        out.append({"id": old["id"] if old else new_id(), **item, "resolution": resolution})
    for old in recorded:
        try:
            if _signature(old) in seen:
                continue
        except (KeyError, TypeError):
            continue
        how = (old.get("resolution") or {}).get("how")
        if how == AUTO:
            continue  # nothing was decided: it simply no longer applies
        if how not in (CHANGED, ASKED, ANSWERED):
            asked = any(slots.get(s, {}).get("status") == NEEDS_HUMAN for s in old.get("slots") or [])
            old = {**old, "resolution": {"how": ASKED if asked else CHANGED}}
        out.append(old)
    out.sort(key=lambda d: int(str(d["id"])[1:]) if str(d["id"])[1:].isdigit() else 0)
    sec["differences"] = out
    _add_agreements(seed, sec, result["agree"])
    return seed


def _add_agreements(seed: dict[str, Any], sec: dict[str, Any],
                    agree: list[dict[str, Any]]) -> None:
    _drop_agreements(seed, sec)
    slots = {s.get("id"): s for s in seed.get("slots") or [] if isinstance(s, dict)}
    labels = {b.get("label"): b.get("content_hash") for b in sec.get("bulletins") or []
              if isinstance(b, dict)}
    done: set[str] = set()
    for a in agree:
        slot = slots.get(a.get("slot"))
        if slot is None or a["slot"] in done or not isinstance(slot.get("sources"), list):
            continue
        if slot.get("status") == SETTLED and slot.get("decision") != INCLUDE:
            continue
        done.add(a["slot"])
        evidence = next(iter((a.get("opinion") or {}).get("evidence") or []), None) or {}
        full = resolve_hash(seed, labels.get(evidence.get("bulletin")))
        where = " ".join(str(p) for p in (
            evidence.get("bulletin"), f"p{evidence['page']}" if evidence.get("page") else None)
            if p)
        quote = f" “{evidence['quote']}”" if evidence.get("quote") else ""
        source: dict[str, Any] = {"source": sec.get("call")}
        if full:
            source["bulletin"] = full
            source["page"] = evidence.get("page")
        said = _source_prefix(sec) + (" as the leaning option" if a.get("question") else "")
        source["said"] = f"{said}: {where}{quote}" if where or quote else said
        slot["sources"].append(source)


def _recorded(seed: dict[str, Any]) -> list[dict[str, Any]]:
    sec = section(seed) or {}
    return [d for d in sec.get("differences") or [] if isinstance(d, dict)]


def unresolved(seed: dict[str, Any]) -> list[dict[str, Any]]:
    """The differences that still need the drafter, after comparing again."""
    return [d for d in _recorded(refresh(seed)) if d.get("resolution") is None]


def stats(seed: dict[str, Any]) -> dict[str, Any] | None:
    """A second opinion's differences by how each was resolved, for the PR and foremen.

    `differences` counts those the drafter had to answer (not `auto`); a question the
    drafter asked counts once, however many readings of it there are.
    """
    sec = section(seed)
    if sec is None:
        return None
    items = _recorded(seed)
    asked_slots = {s for d in items if (d.get("resolution") or {}).get("how") == ASKED
                   and d.get("kind") != compare_mod.QUESTION for s in d.get("slots") or []}
    counted = [d for d in items if (d.get("resolution") or {}).get("how") != AUTO
               and not (d.get("kind") == compare_mod.QUESTION
                        and set(d.get("slots") or []) <= asked_slots)]
    hows = [(d.get("resolution") or {}).get("how") for d in counted]
    result = compare(seed)
    return {
        "differences": len(counted), "unresolved": hows.count(None),
        "changed": hows.count(CHANGED), "asked": hows.count(ASKED),
        "kept": hows.count(KEPT), "answered": hows.count(ANSWERED),
        "auto": sum(1 for d in items if (d.get("resolution") or {}).get("how") == AUTO),
        "agree": len(result["agree"]) if result else 0,
        "entries": len(sec.get("entries") or []), "cost_usd": sec.get("cost_usd"),
    }


# ── The drafter's answer: keeping a slot ────────────────────────────────────
def keep(seed: dict[str, Any], diff_id: str, sources: list[dict[str, Any]], why: str,
         *, at: str | None = None) -> dict[str, Any]:
    """The seed with difference `diff_id` resolved as kept, on `sources` (a bulletin page
    each) and `why` (the rule)."""
    if seed.get("status") == APPROVED:
        raise OpinionError("An approved seed belongs to its reviewer; it cannot be changed")
    if section(seed) is None:
        raise OpinionError(f"{seed.get('parish_slug')} has no second opinion yet: the dispatcher "
                        "writes it once your gates pass")
    seed = refresh(seed)
    items = {d.get("id"): d for d in _recorded(seed)}
    item = items.get(diff_id)
    if item is None:
        raise OpinionError(f"no difference {diff_id} (the file has "
                        f"{', '.join(map(str, items)) or 'none'})")
    how = (item.get("resolution") or {}).get("how")
    if how not in (None, KEPT):
        raise OpinionError(f"{diff_id} is already resolved ({how}): nothing to keep")
    if not sources or not all(s.get("bulletin") and s.get("page") for s in sources):
        raise OpinionError("--src must cite a bulletin page: `HASH pN: what it says` "
                        "(or `latest pN: ...`)")
    if not why.strip() or not (RULE_ID.search(why) or "POLICY" in why):
        raise OpinionError("--why gives the reason, citing its rule: \"R17: ...\"")
    item["resolution"] = {"how": KEPT, "src": sources, "why": why.strip(),
                          "at": at or utc_now_iso()}
    return seed


# ── Checks ──────────────────────────────────────────────────────────────────
def expected_shas(environ: dict[str, str] | None = None) -> dict[str, str]:
    """The hashes the dispatcher kept, from `OPINION_SHA_ENV` (`parish=sha ...`)."""
    raw = (os.environ if environ is None else environ).get(OPINION_SHA_ENV, "")
    return dict(p.split("=", 1) for p in raw.split() if "=" in p)


def evidence_text(sec: dict[str, Any], entry: dict[str, Any]) -> list[str]:
    """Where the opinion read an entry: `B1 1ab3e7c2 (issue 2026-11-15) p2: “...”`."""
    hashes = {b.get("label"): b for b in sec.get("bulletins") or [] if isinstance(b, dict)}
    lines = []
    for e in entry.get("evidence") or []:
        b = hashes.get(e.get("bulletin")) or {}
        head = " ".join(str(p) for p in (
            e.get("bulletin"), str(b.get("content_hash") or "")[:8] or None,
            f"(issue {b['published_date']})" if b.get("published_date") else None,
            f"p{e['page']}" if e.get("page") else None) if p)
        lines.append(f"{head}: “{e.get('quote')}”")
    return lines


def explain(sec: dict[str, Any], item: dict[str, Any]) -> list[str]:
    """A difference as the drafter reads it: what each side has, and the opinion's quotes."""
    entries = {e.get("id"): e for e in sec.get("entries") or [] if isinstance(e, dict)}
    fields = f": {', '.join(item.get('fields') or [])}" if item.get("fields") else ""
    lines = [f"{item.get('id')} {item.get('kind')}{fields}",
             f"  {sec.get('model')}: {item.get('opinion_said')}"]
    quotes = [q for oid in item.get("opinion") or []
              for q in evidence_text(sec, entries.get(oid) or {})]
    lines += [f"    {line}" for line in _unique(quotes)]
    slots = ", ".join(item.get("slots") or []) or "no slot"
    lines.append(f"  seed ({slots}): {item.get('seed_said')}")
    return lines


def opinion_problems(seed: dict[str, Any], *, expected_sha: str | None = None) -> list[str]:
    """What `seed check` reports about a draft's second opinion: entries changed since the
    dispatcher wrote them, else every difference not yet resolved."""
    sec = section(seed)
    if sec is None:
        return []
    sha = entries_sha(sec.get("entries"))
    if sha != sec.get("entries_sha256") or expected_sha is not None and sha != expected_sha:
        return [f"{SECTION}.entries were changed after the dispatcher wrote them: put them "
                "back as they were (`git diff` shows the change) and record your decisions as "
                "resolutions instead"]
    parish = seed.get("parish_slug")
    problems = []
    for item in unresolved(seed):
        lines = explain(sec, item)
        problems.append(
            f"{SECTION} difference {item['id']} unresolved: " + "; ".join(
                line.strip() for line in lines[1:])
            + f". Re-read the page, then change the slot, ask, or `pnpm seed opinion keep "
              f"{parish} {item['id']} --src \"HASH pN: ...\" --why \"R...\"`")
    return problems
