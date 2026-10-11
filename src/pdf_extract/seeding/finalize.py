"""`seed finalize`: the bookkeeping that finishes a draft, so the agent writes only its calls.

An agent drafting a parish writes the substance of each slot (its entry, sources,
decision, rationale and question) and leaves the rest to this:

- every key an entry, option entry or slot may leave out is filled with its default
  (`weeks_of_month` [], `season`, `end_time`, `note` and the like null, `cancelled`
  false), `event_kind` from whether the entry has a `date`, and `church_slug` when
  the parish has one church;
- `"dated"` is read as `specific_date`, the name the files use;
- a slot without an `id` gets the next free `sN`;
- a source citing several bulletins (`"bulletins": [...]` for `bulletin`, the same
  `said` in each) becomes one source per bulletin, as the files store them;
- a slot gets a `history` source for each event of extract mode's recent history
  that matches its entry or an option's (`coverage.attach_history`), for each
  bulletin it has none for yet;
- every bulletin a slot's `agent` source cites is marked read (none is unmarked);
- `as_of` is the fetch time of the newest bulletin read;
- `status` is `needs_review` while a question is open, else `ready` (a blocked file
  keeps its status).

An approved file is the reviewer's and is left as it is.

It changes nothing it can't fill in for certain: a wrong value is left for
`seed check` to report.
"""

from __future__ import annotations

from typing import Any

from pdf_extract.labeling.labels import ENTRY_KEYS
from pdf_extract.seeding.coverage import attach_history
from pdf_extract.seeding.files import (
    AGENT,
    APPROVED,
    BLOCKED,
    NEEDS_HUMAN,
    SLOT_KEYS,
    newest_read_bulletin,
    resolve_hash,
    status_after_review,
)

SPECIFIC_DATE = "specific_date"
# What agents call a dated entry; the files say `specific_date`.
DATED_ALIASES = ("dated", "date", "single", "single_event")

_ENTRY_DEFAULTS: dict[str, Any] = {
    "day_of_week": None, "date": None, "end_time": None, "cancelled": False,
    "weeks_of_month": [], "season": None, "note": None,
}
_SLOT_DEFAULTS: dict[str, Any] = {
    "decision": None, "entry": None, "page": None, "question": None, "options": None,
    "answer": None,
}


def _fill_entry(entry: Any, church: str | None) -> Any:
    """`entry` with its defaulted keys filled in, in the files' key order."""
    if not isinstance(entry, dict):
        return entry
    filled = dict(entry)
    for key, default in _ENTRY_DEFAULTS.items():
        filled.setdefault(key, list(default) if isinstance(default, list) else default)
    if church is not None:
        filled.setdefault("church_slug", church)
    kind = filled.get("event_kind")
    if kind in DATED_ALIASES:
        filled["event_kind"] = SPECIFIC_DATE
    elif kind is None:
        filled["event_kind"] = SPECIFIC_DATE if filled.get("date") else "weekly"
    known = [k for k in ENTRY_KEYS if k in filled]
    return {**{k: filled[k] for k in known}, **{k: v for k, v in filled.items() if k not in known}}


def _next_id(taken: set[str]) -> str:
    n = 1
    while f"s{n}" in taken:
        n += 1
    taken.add(f"s{n}")
    return f"s{n}"


def _expand_sources(sources: Any) -> Any:
    """`sources` with each one citing `bulletins` split into one source per bulletin."""
    if not isinstance(sources, list):
        return sources
    out = []
    for source in sources:
        refs = source.get("bulletins") if isinstance(source, dict) else None
        if not (isinstance(refs, list) and refs and all(isinstance(r, str) for r in refs)):
            out.append(source)  # nothing to expand, or something `seed check` reports
            continue
        if isinstance(source.get("bulletin"), str):
            refs = [source["bulletin"], *refs]
        for ref in dict.fromkeys(refs):
            one: dict[str, Any] = {}
            for key, value in source.items():
                if key == "bulletins":
                    one["bulletin"] = ref
                elif key != "bulletin":
                    one[key] = value
            out.append(one)
    return out


def _fill_slot(slot: dict[str, Any], church: str | None, taken: set[str]) -> dict[str, Any]:
    filled = dict(slot)
    if "sources" in filled:
        filled["sources"] = _expand_sources(filled["sources"])
    if not isinstance(filled.get("id"), str) or not filled["id"].strip():
        filled["id"] = _next_id(taken)
    for key, default in _SLOT_DEFAULTS.items():
        filled.setdefault(key, default)
    if "status" not in filled:
        filled["status"] = NEEDS_HUMAN if filled.get("question") else "settled"
    filled["entry"] = _fill_entry(filled["entry"], church)
    if isinstance(filled["options"], list):
        filled["options"] = [
            {**o, "entry": _fill_entry(o.get("entry"), church)} if isinstance(o, dict) else o
            for o in filled["options"]
        ]
    known = [k for k in SLOT_KEYS if k in filled]
    return {**{k: filled[k] for k in known}, **{k: v for k, v in filled.items() if k not in known}}


def finalize_seed(
    seed: dict[str, Any], churches: list[str], history: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """`seed` with its bookkeeping done. `churches` are the parish's church slugs, and
    `history` extract mode's recent bulletins (`queries.recent_history`) to cite."""
    if seed.get("status") == APPROVED:
        return seed
    seed = dict(seed)
    church = churches[0] if len(churches) == 1 else None
    slots = seed.get("slots")
    if isinstance(slots, list):  # anything else is left for `seed check` to report
        taken = {s["id"] for s in slots if isinstance(s, dict) and isinstance(s.get("id"), str)}
        slots = seed["slots"] = [
            attach_history(seed, _fill_slot(s, church, taken), history or [])
            if isinstance(s, dict) else s
            for s in slots
        ]
    else:
        slots = []

    cited = set()
    for slot in slots:
        sources = slot.get("sources") if isinstance(slot, dict) else None
        for source in sources if isinstance(sources, list) else []:
            if isinstance(source, dict) and source.get("source") == AGENT:
                full = resolve_hash(seed, source.get("bulletin"))
                if full:
                    cited.add(full)
    if isinstance(seed.get("bulletins"), list):
        seed["bulletins"] = [
            {**b, "read": True} if isinstance(b, dict) and b.get("content_hash") in cited else b
            for b in seed["bulletins"]
        ]

    newest = newest_read_bulletin(seed)
    if newest is not None:
        seed["as_of"] = newest["fetched_at"]
    if seed.get("status") != BLOCKED:
        seed["status"] = status_after_review(seed)
    return seed
