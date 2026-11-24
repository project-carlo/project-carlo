"""A seed against a blind second reading of its bulletins (`classifiers.seed_opinion`).

Both sides are reduced to what an entry means: church, type, weekly day or
date, start time, end time (not for Mass), cancelled, and for a weekly entry
the month-days its weeks of the month and season allow
(`qualifiers.recurrence_mask`), so "every Sunday except the last" and "first to
fourth Sunday" compare equal while "every Friday" and "first Friday" don't.
"24 hours" compares equal however it is written: a start at 12:00 AM with an
end of 12:00 AM, 11:59 PM or none is all day. So does a period past midnight:
"Friday 8:00 PM-6:00 AM" (an end at or before its start) is compared as its two
days' parts, Friday 8:00-11:59 PM and Saturday 12:00-6:00 AM, so it matches the
same period written as two entries. Notes are not compared.

Each of the opinion's entries is matched against the seed's:

- an included slot with the same meaning: agreement;
- a question's leaning option: agreement; another option: `question`;
- an excluded slot: `excluded` (the drafter left it out on purpose).

What is left on either side is then dropped when it changes nothing a visitor
would see:

- a dated entry that an included weekly slot (on either side) already covers:
  the same church, type, weekday and start, on a date the slot's weeks and
  season include (POLICY: never duplicate a weekly slot as a dated entry);
- a cancellation that cancels nothing on either side: no included weekly slot
  at that church, type, weekday and time, and no dated entry on that date.

The rest is paired on the same church, type and day (or date): first the same
start time (an end time, weeks or season differ), then the nearest start
within `PAIR_WINDOW` minutes, or any start when the day has exactly one of
each: `differs`, naming the fields. An opinion entry still unpaired that has
the start of an excluded slot on its day is `excluded` (its weeks, season or
end differ); otherwise it is `missing`. An included slot still unpaired is
`extra`. Dated entries before the seed's date are out of scope and dropped.

Some differences are `resolved` at once, because the opinion could not see
what settled them: a settled exclusion that cites R22-R26 (`policy-exclusion`),
an included slot the parish website settled (a `website` source and R6 (or C9) cited,
or no bulletin source among the opinion's bulletins: `website`), and one
resting only on bulletins the opinion wasn't given (`unseen-bulletins`).
Differences that are the same but for the weekday ("Mon-Fri 8:00 vs 8:30") are
grouped into one item.
"""

from __future__ import annotations

import difflib
import re
from collections import defaultdict
from datetime import date, timedelta
from typing import Any

from pdf_extract.schedule.qualifiers import (
    QualifierError,
    recurrence_includes_date,
    recurrence_mask,
    season_to_columns,
    weeks_to_mask,
)
from pdf_extract.seeding.files import AGENT, EXCLUDE, HISTORY, INCLUDE, SETTLED, WEBSITE
from pdf_extract.timeparse import time_to_minutes

AGREE = "agree"
MISSING = "missing"
EXTRA = "extra"
DIFFERS = "differs"
EXCLUDED = "excluded"
QUESTION = "question"
KINDS = (MISSING, EXTRA, DIFFERS, EXCLUDED, QUESTION)

# Why a difference needs no answer from the drafter.
POLICY_EXCLUSION = "policy-exclusion"
WEBSITE_BACKED = "website"
UNSEEN_BULLETINS = "unseen-bulletins"
RESOLVED_REASONS = (POLICY_EXCLUSION, WEBSITE_BACKED, UNSEEN_BULLETINS)

# Why a leftover entry is not a difference at all.
COVERED_BY_WEEKLY = "covered-by-weekly"
CANCELS_NOTHING = "cancels-nothing"

# A settled exclusion resting on these rules is a policy call the opinion can't see
# (another parish's church, an unlisted chapel, a devotion, no time...).
POLICY_EXCLUSION_RULES = ("R22", "R23", "R24", "R25", "R26")
# R6, or C9, the candidate rule it was promoted from.
_R6 = re.compile(r"\b(?:R6|C9)\b")

ALL_DAY_END = 23 * 60 + 59
# Two readings of one day's slot whose starts are this far apart or less are paired.
PAIR_WINDOW = 120


def _minutes(value: Any) -> int | None:
    return time_to_minutes(value) if isinstance(value, str) else None


def _mask(entry: dict[str, Any]) -> int | None:
    try:
        weeks = weeks_to_mask(entry.get("weeks_of_month") or [], entry.get("exclude_weeks") is True)
        return recurrence_mask(weeks, *season_to_columns(entry.get("season")))
    except QualifierError:
        return None


def weekly(entry: dict[str, Any]) -> bool:
    return entry.get("event_kind") == "weekly" or (
        entry.get("event_kind") is None and not entry.get("date")
    )


def _date(entry: dict[str, Any]) -> date | None:
    try:
        return date.fromisoformat(str(entry.get("date")))
    except ValueError:
        return None


def _weekday(entry: dict[str, Any]) -> str:
    """The entry's weekday, for a dated entry the weekday of its date."""
    if weekly(entry):
        return (entry.get("day_of_week") or "").lower()
    day = _date(entry)
    return day.strftime("%A").lower() if day else ""


def _times(entry: dict[str, Any]) -> tuple[int | None, int | None]:
    """Start and end in minutes; no end for Mass, and 24 hours written one way."""
    start = _minutes(entry.get("start_time"))
    if entry.get("event_type") == "mass":
        return start, None
    end = _minutes(entry.get("end_time"))
    if start == 0 and end in (0, None, ALL_DAY_END):
        end = ALL_DAY_END
    elif end == 0 and start is not None:
        end = ALL_DAY_END  # "11:00 PM-12:00 AM" ends at midnight, not the next day
    return start, end


WEEKDAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


def overnight_parts(entry: dict[str, Any]) -> list[dict[str, Any]]:
    """A period ending at or before its start (past midnight) as its two days' parts.

    The second part keeps the first's weeks of the month and season, as both
    readers write "First Friday 8 PM to Saturday 6 AM". Anything else is itself.
    """
    start, end = _times(entry)
    if entry.get("event_type") == "mass" or start in (None, 0) or end is None or end > start:
        return [entry]
    first = {**entry, "end_time": "23:59", "overnight_of": entry}
    second = {**entry, "start_time": "00:00", "overnight_of": entry}
    if weekly(entry):
        day = (entry.get("day_of_week") or "").lower()
        if day not in WEEKDAYS:
            return [entry]
        second["day_of_week"] = WEEKDAYS[(WEEKDAYS.index(day) + 1) % 7].capitalize()
    else:
        day = _date(entry)
        if day is None:
            return [entry]
        second["date"] = (day + timedelta(days=1)).isoformat()
    return [first, second]


def loose_key(entry: dict[str, Any]) -> tuple:
    """Church, type and day (or date): what two readings of one slot share."""
    anchor = (entry.get("day_of_week") or "").lower() if weekly(entry) else entry.get("date")
    return (
        "weekly" if weekly(entry) else "dated", entry.get("church_slug"),
        entry.get("event_type"), anchor, bool(entry.get("cancelled")),
    )


def _parts(entry: dict[str, Any]) -> dict[str, Any]:
    start, end = _times(entry)
    return {
        "start": start,
        "end": end,
        "recurrence": _mask(entry) if weekly(entry) else None,
    }


def key(entry: dict[str, Any]) -> tuple:
    parts = _parts(entry)
    return (*loose_key(entry), parts["start"], parts["end"], parts["recurrence"])


def _differing(a: dict[str, Any], b: dict[str, Any]) -> list[str]:
    pa, pb = _parts(a), _parts(b)
    names = {"start": "start time", "end": "end time", "recurrence": "weeks/season"}
    return [names[k] for k in pa if pa[k] != pb[k]]


def _leaning(slot: dict[str, Any]) -> int | None:
    for i, option in enumerate(slot.get("options") or []):
        if isinstance(option, dict) and option.get("leaning"):
            return i
    return None


def _policy_exclusion(slot: dict[str, Any]) -> bool:
    rationale = str(slot.get("rationale") or "")
    return any(rule in rationale for rule in POLICY_EXCLUSION_RULES)


def _same_service(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Same church, type, weekday and start (b's date gives its weekday)."""
    return (
        a.get("church_slug") == b.get("church_slug")
        and a.get("event_type") == b.get("event_type")
        and _weekday(a) == _weekday(b) != ""
        and _times(a)[0] == _times(b)[0]
    )


def covers(weekly_entry: dict[str, Any], dated: dict[str, Any]) -> bool:
    """Whether an included weekly entry already shows a (not cancelled) dated entry."""
    day = _date(dated)
    if day is None or not _same_service(weekly_entry, dated):
        return False
    end = _times(dated)[1]
    if end is not None and end != _times(weekly_entry)[1]:
        return False
    try:
        weeks = weeks_to_mask(
            weekly_entry.get("weeks_of_month") or [], weekly_entry.get("exclude_weeks") is True)
        return recurrence_includes_date(day, weeks, *season_to_columns(weekly_entry.get("season")))
    except QualifierError:
        return False


def cancels_something(
    cancellation: dict[str, Any], weeklies: list[dict[str, Any]], dated: list[dict[str, Any]],
) -> bool:
    """Whether a cancellation removes an included weekly slot or a dated entry."""
    return any(_same_service(w, cancellation) for w in weeklies) or any(
        d.get("date") == cancellation.get("date") and _same_service(d, cancellation)
        for d in dated
    )


def _drop_reason(
    entry: dict[str, Any], weeklies: list[dict[str, Any]], dated: list[dict[str, Any]],
) -> str | None:
    if weekly(entry):
        return None
    if entry.get("cancelled"):
        return None if cancels_something(entry, weeklies, dated) else CANCELS_NOTHING
    return COVERED_BY_WEEKLY if any(covers(w, entry) for w in weeklies) else None


def _seen(ref: Any, seen_bulletins: list[str]) -> bool:
    ref = str(ref or "").lower()
    return bool(ref) and any(h.lower().startswith(ref) for h in seen_bulletins)


def rests_on_seen(slot: dict[str, Any], seen_bulletins: list[str]) -> bool:
    """Whether the slot's bulletin sources include one the opinion read.

    The drafter's own (`agent`) sources are what the slot rests on; history's
    readings count only for a slot with no agent source.
    """
    sources = [s for s in slot.get("sources") or [] if isinstance(s, dict) and s.get("bulletin")]
    agent = [s for s in sources if s.get("source") == AGENT]
    cited = agent or [s for s in sources if s.get("source") == HISTORY]
    return any(_seen(s.get("bulletin"), seen_bulletins) for s in cited)


def _resolved(
    kind: str, slot: dict[str, Any] | None, seen_bulletins: list[str] | None,
) -> str | None:
    if slot is None:
        return None
    if kind == EXCLUDED:
        return POLICY_EXCLUSION if _policy_exclusion(slot) else None
    if kind not in (EXTRA, DIFFERS):
        return None
    on_seen = seen_bulletins is None or rests_on_seen(slot, seen_bulletins)
    website = any(isinstance(s, dict) and s.get("source") == WEBSITE
                  for s in slot.get("sources") or [])
    if website and (_R6.search(str(slot.get("rationale") or "")) or not on_seen):
        return WEBSITE_BACKED
    return None if on_seen else UNSEEN_BULLETINS


def _pair(
    entries: list[dict[str, Any]], slots: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Readings of one day's slots paired: same start first, then the nearest."""
    only_one = len(entries) == 1 and len(slots) == 1
    candidates = []
    for i, e in enumerate(entries):
        for j, s in enumerate(slots):
            a, b = _times(e)[0], _times(s["entry"])[0]
            gap = abs(a - b) if a is not None and b is not None else 24 * 60
            if gap <= PAIR_WINDOW or only_one:
                candidates.append((gap, i, j))
    pairs, used_e, used_s = [], set(), set()
    for _, i, j in sorted(candidates):
        if i not in used_e and j not in used_s:
            used_e.add(i)
            used_s.add(j)
            pairs.append((entries[i], slots[j]))
    return pairs


def fix_church_slugs(entries: list[dict[str, Any]], slugs: list[str]) -> int:
    """Map an entry's unlisted church slug to the one listed slug it plainly means.

    "st-mary-honeoye" for the listed "st-marys-honeoye". The entry gets a
    problem naming the slug it had; one with no close listed slug is left alone
    (it can't match). Returns how many entries changed.
    """
    fixed = 0
    for entry in entries:
        slug = entry.get("church_slug")
        if not slugs or slug in slugs or not isinstance(slug, str):
            continue
        close = difflib.get_close_matches(slug, slugs, n=2, cutoff=0.85)
        if len(close) == 1:
            entry["church_slug"] = close[0]
            entry.setdefault("problems", []).append(f"unlisted church slug {slug!r}")
            fixed += 1
    return fixed


def compare(
    seed: dict[str, Any], opinion: list[dict[str, Any]], today: str,
    seen_bulletins: list[str] | None = None,
) -> dict[str, Any]:
    """The opinion's entries (`seed_opinion.opinion_entries`) against the seed's slots.

    `seen_bulletins` are the content hashes the opinion was given; a seed slot
    resting on none of them is resolved (`unseen-bulletins`). Without them, no
    slot is.
    """
    included: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    excluded: dict[tuple, dict[str, Any]] = {}
    options: dict[tuple, tuple[dict[str, Any], bool]] = {}
    for slot in seed.get("slots") or []:
        if not isinstance(slot, dict):
            continue
        entry = slot.get("entry")
        if slot.get("status") == SETTLED and isinstance(entry, dict):
            for part in overnight_parts(entry):
                if slot.get("decision") == INCLUDE:
                    included[key(part)].append(slot)
                elif slot.get("decision") == EXCLUDE:
                    excluded.setdefault(key(part), slot)
        elif slot.get("status") != SETTLED:
            leaning = _leaning(slot)
            for i, option in enumerate(slot.get("options") or []):
                if isinstance(option, dict) and isinstance(option.get("entry"), dict):
                    options.setdefault(key(option["entry"]), (slot, i == leaning))

    agree: list[dict[str, Any]] = []
    differences: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    in_scope: list[dict[str, Any]] = []
    out_of_scope = 0
    seen: set[tuple] = set()
    matched_parts: dict[int, set[tuple]] = defaultdict(set)
    parts = [part for entry in opinion for part in overnight_parts(entry)]
    for entry in parts:
        if not weekly(entry) and (entry.get("date") or "") < today:
            out_of_scope += 1
            continue
        k = key(entry)
        if k in seen:
            continue  # the same slot read twice
        seen.add(k)
        in_scope.append(entry)
        if k in included:
            for slot in included[k]:
                matched_parts[id(slot)].add(k)
            agree.append({"opinion": entry, "slot": included[k][0].get("id")})
        elif k in options:
            slot, leaning = options[k]
            if leaning:
                agree.append({"opinion": entry, "slot": slot.get("id"), "question": True})
            else:
                differences.append({"kind": QUESTION, "opinion": entry, "slot": slot.get("id"),
                                    "seed": None})
        elif k in excluded:
            slot = excluded[k]
            differences.append({
                "kind": EXCLUDED, "opinion": entry, "slot": slot.get("id"), "seed": slot["entry"],
                "policy_exclusion": _policy_exclusion(slot),
                "rationale": slot.get("rationale"), "_slot": slot,
            })
        else:
            unmatched.append(entry)

    # What both sides schedule, to judge leftover dated entries and cancellations against.
    seed_entries = list({id(s): s["entry"] for slots in included.values() for s in slots}.values())
    pool = [e for e in seed_entries + in_scope if not e.get("cancelled")]
    weeklies = [e for e in pool if weekly(e)]
    dated = [e for e in pool if not weekly(e)]
    dropped: list[dict[str, Any]] = []

    by_loose: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    for entry in unmatched:
        why = _drop_reason(entry, weeklies, dated)
        if why:
            dropped.append({"why": why, "opinion": entry, "slot": None})
        else:
            by_loose[loose_key(entry)].append(entry)
    left: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    unique = {id(s): s for slots in included.values() for s in slots}
    for slot in unique.values():
        if matched_parts[id(slot)] >= {key(p) for p in overnight_parts(slot["entry"])}:
            continue  # every part of it agreed
        why = _drop_reason(slot["entry"], weeklies, dated)
        if why:
            dropped.append({"why": why, "opinion": None, "slot": slot.get("id")})
        else:
            left[loose_key(slot["entry"])].append(slot)

    excluded_by_loose: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    for slot in {id(s): s for s in excluded.values()}.values():
        excluded_by_loose[loose_key(slot["entry"])].append(slot)

    for lk, entries in by_loose.items():
        slots = left.get(lk, [])
        paired_entries = set()
        for entry, slot in _pair(entries, slots):
            paired_entries.add(id(entry))
            slots.remove(slot)
            differences.append({
                "kind": DIFFERS, "opinion": entry, "slot": slot.get("id"),
                "seed": slot["entry"], "fields": _differing(entry, slot["entry"]), "_slot": slot,
            })
        for entry in entries:
            if id(entry) in paired_entries:
                continue
            start = _times(entry)[0]
            near = next((s for s in excluded_by_loose.get(lk, [])
                         if _times(s["entry"])[0] == start), None)
            if near is not None:
                differences.append({
                    "kind": EXCLUDED, "opinion": entry, "slot": near.get("id"),
                    "seed": near["entry"], "fields": _differing(entry, near["entry"]),
                    "policy_exclusion": _policy_exclusion(near),
                    "rationale": near.get("rationale"), "_slot": near,
                })
            else:
                differences.append({"kind": MISSING, "opinion": entry, "slot": None, "seed": None})
    for slots in left.values():
        for slot in slots:
            differences.append({"kind": EXTRA, "opinion": None, "slot": slot.get("id"),
                                "seed": slot["entry"], "_slot": slot})

    for diff in differences:
        diff["resolved"] = _resolved(diff["kind"], diff.pop("_slot", None), seen_bulletins)

    groups = group(differences)
    return {
        "agree": agree,
        "differences": differences,
        "groups": groups,
        "counted": [g for g in groups if not g[0]["resolved"]],
        "dropped": dropped,
        "out_of_scope": out_of_scope,
        "included": len(unique),
    }


def _group_key(diff: dict[str, Any]) -> tuple:
    """A difference without its weekday, so "Mon-Fri" differences group together."""
    def strip(entry: dict[str, Any] | None) -> tuple | None:
        if entry is None:
            return None
        entry = entry.get("overnight_of") or entry  # both parts of one reading group together
        k = key(entry)
        if not weekly(entry):
            return k
        return (k[0], k[1], k[2], None, *k[4:])
    return (diff["kind"], strip(diff.get("opinion")), strip(diff.get("seed")),
            tuple(diff.get("fields") or ()), diff.get("resolved"))


def group(differences: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    groups: dict[tuple, list[dict[str, Any]]] = {}
    for diff in differences:
        groups.setdefault(_group_key(diff), []).append(diff)
    return list(groups.values())


def describe(entry: dict[str, Any] | None) -> str:
    """A short human line for an entry: `mass Sat 16:00 @church first season=9-5`."""
    if entry is None:
        return "-"
    parts = [str(entry.get("event_type"))]
    parts.append((entry.get("day_of_week") or "")[:3] if weekly(entry) else str(entry.get("date")))
    time = str(entry.get("start_time"))
    if entry.get("end_time") and entry.get("event_type") != "mass":
        time += f"-{entry['end_time']}"
    parts.append(time)
    if entry.get("cancelled"):
        parts.append("cancelled")
    parts.append(f"@{entry.get('church_slug')}")
    if entry.get("weeks_of_month"):
        weeks = ",".join(entry["weeks_of_month"])
        parts.append(f"except={weeks}" if entry.get("exclude_weeks") else weeks)
    season = entry.get("season")
    if isinstance(season, dict):
        parts.append(f"season={season.get('start_month')}-{season.get('end_month')}")
    return " ".join(parts)
