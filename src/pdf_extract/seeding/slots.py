"""`seed slot ...`, `seed summary`, `seed church-issue`, `seed block`: a draft's slots by command.

A drafter writes a slot's substance (its entry, sources, decision, rationale and
question) with short commands instead of editing the JSON, and `finalize` still
does the bookkeeping. Each command reads the file, applies the change, checks
the slots it touched with the file's own validation (`files.slot_problems`,
`files.group_problems`, `checks.entry_problem`), and writes it only if they pass.
The entry and source specs are in `USAGE` (`pnpm seed slot --help`).

An approved file is the reviewer's, and nothing here writes it. A slot a reviewer
answered keeps its decision: only sources may be added to it. A slot citing a
paid call keeps that evidence.
"""

from __future__ import annotations

import argparse
import copy
import re
import shlex
from dataclasses import dataclass, field
from typing import Any

from pdf_extract.labeling.labels import DAYS, WEEKS_OF_MONTH
from pdf_extract.schedule.entries import Entry, parse_entry
from pdf_extract.schedule.store import normalize_as_of
from pdf_extract.seeding.checks import entry_problem
from pdf_extract.seeding.files import (
    AGENT,
    APPROVED,
    BLOCKED,
    DRAFTING,
    EXCLUDE,
    HISTORY,
    INCLUDE,
    MIN_HASH_PREFIX,
    NEEDS_HUMAN,
    RULE_ID,
    SETTLED,
    WEBSITE,
    church_issue_problems,
    group_problems,
    resolve_hash,
    slot_problems,
)
from pdf_extract.seeding.finalize import fill_slot, next_slot_id
from pdf_extract.seeding.queries import SeedError
from pdf_extract.timeparse import time_to_minutes

USAGE = """\
Write a draft's slots without editing its JSON. Each command checks the slots it
touched (shape, churches, groups, duplicates) and writes the file only if they
pass. `finalize` still does the bookkeeping. Approved files, reviewers' answers
and paid calls' evidence are never changed.

ENTRY: words in any order
  type       mass | confession | adoration
  when       Sat | Mon-Fri | Tue,Thu | daily; or a date 2026-10-12 (a dated entry)
  time       16:00 | 15:00-15:45 | 08:00,10:30 | 4pm (24-hour HH:MM, or say am/pm)
  @church    a church slug, or a unique part of one of the parish's (required
             when the parish has several; an excluded entry may name another)
  weeks      first | 2nd,4th | last; except=last for the weeks it skips
  season     season=9-5 | season=9/15-5/31 | season=sep-may
  cancelled  the dated entry is called off
  note=...   last: the rest of the spec is the note
  Several days or times make one slot each (in `ask`, one grouped slot each).
  `edit --entry` changes only what it names (`17:00`, `note=` clears the note,
  `weeks=` the weeks). An option entry `+ ...` is the first option's entry (in
  `edit`, the slot's) with those changes: `+ except=first`, `+ weeks=`.

SOURCE: "HEAD: what it said, in its words"
  latest p2: ...             the newest listed bulletin, page 2
  9f2c41d0,1ab3e7c2 p2: ...  several bulletins: one source each
  web https://...: ...       a page `seed site` printed (never in a test run)
  history [9f2c41d0]: ...    only what history can't say itself
  c1 p3: ...                 a paid call
  A slot's --page defaults to its source's page on the newest bulletin, and a
  source on the newest bulletin without a page takes the slot's.

OPTION: --option "LABEL" ["ENTRY"], repeated; `*` before one label marks the
  leaning, and an option without an entry leaves the slot out.

Examples (P is the parish):
  slot include P "mass Sat 16:00 note=Vigil" --src "latest p2: Sat 4:00 PM Vigil" \\
      --src "1ab3e7c2,77d0be19 p2: Sat 4 PM" --why "R1: in the schedule box of all three"
  slot include P "mass Mon-Fri 08:00 @st-marys" --src "latest p2: Mon-Fri 8 AM" --why "R1: ..."
  slot include P "mass 2026-10-12 08:00 cancelled note=Columbus Day" \\
      --src "latest p3: No 8 AM Mass on Monday, October 12" --why "R1, R16: ..."
  slot exclude P "mass Mon-Thu 12:15 @destiny-chapel" --src "latest p2: ..." --why "R23: ..."
  slot exclude P - --src "latest p3: Confession by appointment" --why "R26: no time"
  slot ask P "Add a first-Friday 9:45 AM Holy Hour?" \\
      --option "*First Fridays 9:45 AM" "adoration Fri 09:45 first" --option "Leave out" \\
      --src "latest p2: First Friday Holy Hour 9:45 AM" --why "R32: no place given. ..."
  slot edit P s4 --entry "17:00 note=" --src "1ab3e7c2 p2: Sun 5 PM"
  slot edit P s9 --include      (settle a question by its leaning option)
  slot batch P plan.txt         (the lines above without `slot` and P; `-`: stdin)
"""

ENTRY_HELP = (
    "an entry is `TYPE DAYS|DATES TIMES [@church] [first|2nd,4th|except=last] "
    "[season=9-5] [cancelled] [note=rest of text]`, e.g. `mass Sat 16:00 note=Vigil`"
)
SOURCE_HELP = (
    "a source is `HEAD: what it said`, the head `latest p2`, `9f2c41d0,1ab3e7c2 p3`, "
    "`web https://…`, `history [bulletin]` or a call id (`c1 p2`)"
)

_TYPES = {"mass": "mass", "masses": "mass", "confession": "confession",
          "confessions": "confession", "adoration": "adoration"}
_DAY_ALIASES = {
    **{d.lower(): d for d in DAYS}, **{d[:3].lower(): d for d in DAYS},
    "tues": "Tuesday", "weds": "Wednesday", "thur": "Thursday", "thurs": "Thursday",
}
_ORDINALS = {
    **{w: w for w in WEEKS_OF_MONTH},
    "1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth", "5th": "fifth",
    "1": "first", "2": "second", "3": "third", "4": "fourth", "5": "fifth",
}
_MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_HHMM = re.compile(r"^\d{2}:\d{2}$")
_NOTE = re.compile(r"(?:^|\s)note=")
_PAGE = re.compile(r"^p(\d+|-)$")


# ── Entry specs ─────────────────────────────────────────────────────────────
@dataclass
class EntrySpec:
    """A parsed entry spec: the fields it sets, and the days/dates and times it lists."""

    text: str
    fields: dict[str, Any] = field(default_factory=dict)
    church: str | None = None
    whens: list[tuple[str, str]] | None = None  # ("weekly", day) or ("dated", date)
    times: list[tuple[str, str | None]] | None = None
    patch: bool = False


def _bad(text: str, why: str) -> SeedError:
    return SeedError(f"entry {text!r}: {why}; {ENTRY_HELP}")


def _clock(raw: str, text: str) -> str:
    """`16:00`, `4pm`, `4:30 pm`, `noon` as `HH:MM`; `4:00` is refused as ambiguous."""
    if _HHMM.match(raw):
        minutes = time_to_minutes(raw)
    elif re.search(r"[ap]\.?m\.?$|^noon$|^midnight$", raw, re.I):
        minutes = time_to_minutes(re.sub(r"(?<=\d)(?=[ap])", " ", raw, flags=re.I))
    else:
        raise _bad(text, f"time {raw!r} must be 24-hour HH:MM (16:00, 08:00) or say am/pm")
    if minutes is None:
        raise _bad(text, f"{raw!r} is not a time")
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _times(token: str, text: str) -> list[tuple[str, str | None]]:
    out = []
    for item in token.split(","):
        start, _, end = item.partition("-")
        out.append((_clock(start, text), _clock(end, text) if end else None))
    return out


def _days(token: str, text: str) -> list[str] | None:
    """The weekdays `Sat`, `Mon-Fri`, `Tue,Thu`, `daily` name, or None if it names none."""
    if token.lower() in ("daily", "everyday"):
        return list(DAYS)
    days: list[str] = []
    for item in token.split(","):
        first, sep, last = item.partition("-")
        a, b = _DAY_ALIASES.get(first.lower()), _DAY_ALIASES.get(last.lower())
        if a is None or (sep and b is None):
            return None
        if not sep:
            days.append(a)
            continue
        i, j = DAYS.index(a), DAYS.index(b)
        if j < i:
            raise _bad(text, f"day range {item!r} runs backwards")
        days.extend(DAYS[i:j + 1])
    return list(dict.fromkeys(days))


def _weeks(value: str, text: str) -> list[str]:
    weeks = []
    for item in re.split(r"[,/]", value):
        if not item:
            continue
        week = _ORDINALS.get(item.lower())
        if week is None:
            raise _bad(text, f"{item!r} is not a week of the month "
                       "(first..fifth, 1st..5th, last)")
        weeks.append(week)
    return list(dict.fromkeys(weeks))


def _month_day(part: str, text: str) -> tuple[int, int | None]:
    m = re.match(r"^([a-z]+|\d{1,2})(?:/(\d{1,2}))?$", part.lower())
    if not m:
        raise _bad(text, f"season edge {part!r} is a month (9, sep) or month/day (9/15)")
    month = int(m[1]) if m[1].isdigit() else next(
        (i + 1 for i, name in enumerate(_MONTHS) if m[1].startswith(name)), 0)
    if not 1 <= month <= 12:
        raise _bad(text, f"{m[1]!r} is not a month")
    return month, int(m[2]) if m[2] else None


def _season(value: str, text: str) -> dict[str, Any] | None:
    if not value:
        return None
    parts = value.split("-")
    if len(parts) != 2:
        raise _bad(text, "a season is `season=START-END`, both ends given (R15)")
    (sm, sd), (em, ed) = (_month_day(p, text) for p in parts)
    return {"start_month": sm, "start_day": sd, "end_month": em, "end_day": ed}


def parse_entry_spec(text: str) -> EntrySpec:
    """Parse an entry spec (module docstring). A spec starting with `+` is a change."""
    raw = text.strip()
    spec = EntrySpec(text=text)
    if raw.startswith("+"):
        spec.patch = True
        raw = raw[1:]
    note = _NOTE.search(raw)
    if note:
        spec.fields["note"] = raw[note.end():].strip() or None
        raw = raw[:note.start()]
    for token in raw.split():
        low = token.lower()
        key, eq, value = token.partition("=")
        if low in _TYPES:
            spec.fields["event_type"] = _TYPES[low]
        elif token.startswith("@"):
            spec.church = token[1:]
        elif low in ("cancelled", "canceled"):
            spec.fields["cancelled"] = True
        elif low in ("cancelled=no", "canceled=no", "not-cancelled"):
            spec.fields["cancelled"] = False
        elif eq and key.lower() == "weeks":
            spec.fields.update(weeks_of_month=_weeks(value, text), exclude_weeks=False)
        elif eq and key.lower() == "except":
            weeks = _weeks(value, text)
            if not weeks:
                raise _bad(text, "except= names the weeks it skips")
            spec.fields.update(weeks_of_month=weeks, exclude_weeks=True)
        elif eq and key.lower() == "season":
            spec.fields["season"] = _season(value, text)
        elif eq:
            raise _bad(text, f"unknown field {key!r}")
        elif all(_DATE.match(d) for d in token.split(",")):
            spec.whens = (spec.whens or []) + [("dated", d) for d in token.split(",")]
        elif (days := _days(token, text)) is not None:
            spec.whens = (spec.whens or []) + [("weekly", d) for d in days]
        elif all(w.lower() in _ORDINALS and not w.isdigit() for w in re.split(r"[,/]", token)):
            spec.fields.update(weeks_of_month=_weeks(token, text), exclude_weeks=False)
        elif re.search(r"\d|noon|midnight", low):
            spec.times = (spec.times or []) + _times(token, text)
        else:
            raise _bad(text, f"don't know {token!r}")
    return spec


def resolve_church(ref: str, churches: list[str], text: str = "") -> str:
    """A church slug from `@ref`: the slug itself, or a unique part of one of the parish's."""
    if ref in churches:
        return ref
    found = [c for c in churches if c.startswith(ref)] or [c for c in churches if ref in c]
    if len(found) == 1:
        return found[0]
    if len(found) > 1:
        raise _bad(text, f"@{ref} could be {', '.join(found)}")
    if re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", ref):
        return ref  # a church elsewhere: an excluded entry or an option may name one
    raise _bad(text, f"@{ref} is not a church slug")


def build_entries(
    spec: EntrySpec, churches: list[str], base: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """The entries a spec makes: one per day or date and time, on top of `base` if given."""
    start = copy.deepcopy(base) if base else {}
    if spec.church is not None:
        start["church_slug"] = resolve_church(spec.church, churches, spec.text)
    start.update(copy.deepcopy(spec.fields))
    if base is None:
        if "event_type" not in start:
            raise _bad(spec.text, "name its type: mass, confession or adoration")
        if not spec.whens:
            raise _bad(spec.text, "name its day (Sat, Mon-Fri) or date (2026-10-12)")
        if not spec.times:
            raise _bad(spec.text, "give its time (16:00 or 15:00-15:45)")
        if "church_slug" not in start:
            if len(churches) != 1:
                raise _bad(spec.text, "the parish has several churches: name it with @, one "
                           f"of {', '.join(churches) or '(none)'}")
            start["church_slug"] = churches[0]
    whens: list[tuple[str, str] | None] = list(spec.whens or [None])
    times: list[tuple[str, str | None] | None] = list(spec.times or [None])
    entries = []
    for when in whens:
        for time in times:
            entry = copy.deepcopy(start)
            if when is not None and when[0] == "weekly":
                entry.update(event_kind="weekly", day_of_week=when[1], date=None)
            elif when is not None:
                entry.update(event_kind="specific_date", date=when[1], day_of_week=None,
                             weeks_of_month=[], exclude_weeks=False, season=None)
            if time is not None:
                entry.update(start_time=time[0], end_time=time[1])
            entries.append(entry)
    return entries


def format_entry(entry: Any) -> str:
    """An entry as the spec that writes it: `mass Sat 16:00 @st-marys-oswego note=Vigil`."""
    if not isinstance(entry, dict):
        return "(no entry)"
    parts = [str(entry.get("event_type") or "?"),
             entry.get("date") or str(entry.get("day_of_week") or "?")[:3],
             str(entry.get("start_time") or "?")
             + (f"-{entry['end_time']}" if entry.get("end_time") else "")]
    if entry.get("church_slug"):
        parts.append(f"@{entry['church_slug']}")
    if entry.get("weeks_of_month"):
        parts.append(("except=" if entry.get("exclude_weeks") else "")
                     + ",".join(entry["weeks_of_month"]))
    season = entry.get("season")
    if isinstance(season, dict):
        def edge(m: Any, d: Any) -> str:
            return f"{m}/{d}" if d else str(m)
        parts.append(f"season={edge(season.get('start_month'), season.get('start_day'))}-"
                     f"{edge(season.get('end_month'), season.get('end_day'))}")
    if entry.get("cancelled"):
        parts.append("cancelled")
    if entry.get("note"):
        parts.append(f"note={entry['note']}")
    return " ".join(parts)


# ── Source specs ────────────────────────────────────────────────────────────
def _bulletins(seed: dict[str, Any]) -> list[dict[str, Any]]:
    listed = seed.get("bulletins")
    return [b for b in listed if isinstance(b, dict) and isinstance(b.get("content_hash"), str)
            and isinstance(b.get("fetched_at"), str)] if isinstance(listed, list) else []


def newest_listed(seed: dict[str, Any]) -> str | None:
    """The newest bulletin the file lists: the one a draft reads first and `page` refers to."""
    bulletins = _bulletins(seed)
    newest = max(bulletins, key=lambda b: normalize_as_of(b["fetched_at"]), default=None)
    return newest["content_hash"] if newest else None


def short_hash(seed: dict[str, Any], full: str) -> str:
    """The shortest prefix (8 characters or more) naming `full` among the file's bulletins."""
    for n in range(MIN_HASH_PREFIX, len(full)):
        if resolve_hash(seed, full[:n]) == full:
            return full[:n]
    return full


def _bulletin_ref(seed: dict[str, Any], ref: str, text: str) -> str:
    full = newest_listed(seed) if ref.lower() == "latest" else resolve_hash(seed, ref)
    if full is None:
        listed = ", ".join(b["content_hash"][:8] for b in _bulletins(seed)) or "none"
        raise SeedError(f"source {text!r}: {ref!r} names none of the file's bulletins "
                        f"(latest, or 8+ characters of one of {listed}); {SOURCE_HELP}")
    return full


def parse_source(seed: dict[str, Any], text: str, *, head_optional: bool = False,
                 ) -> list[dict[str, Any]]:
    """The sources a source spec makes: one per bulletin it names (module docstring)."""
    head, sep, said = text.partition(": ")
    if not sep:
        if not head_optional:
            raise SeedError(f"source {text!r}: no `: ` after its head; {SOURCE_HELP}")
        head, said = "", text
    said = said.strip()
    if not said:
        raise SeedError(f"source {text!r}: say what it said after `: `")
    tokens = head.split()
    calls = {c.get("id"): c for c in seed.get("calls") or [] if isinstance(c, dict)}
    kind: str = AGENT
    page: int | None = None
    refs: list[str] = []
    if tokens and tokens[0].lower() in ("web", "website"):
        if len(tokens) != 2 or not tokens[1].startswith(("https://", "http://")):
            raise SeedError(f"source {text!r}: a website source is `web URL: said`")
        return [{"source": WEBSITE, "url": tokens[1], "said": said}]
    if tokens and tokens[0].lower() in (HISTORY, AGENT) or tokens and tokens[0] in calls:
        kind = tokens[0] if tokens[0] in calls else tokens[0].lower()
        tokens = tokens[1:]
    for token in tokens:
        m = _PAGE.match(token.lower())
        if m:
            page = None if m[1] == "-" else int(m[1])
            if page == 0:
                raise SeedError(f"source {text!r}: pages count from 1")
        else:
            refs += [_bulletin_ref(seed, r, text) for r in token.split(",") if r]
    if kind in calls and not refs and resolve_hash(seed, calls[kind].get("bulletin")):
        refs = [resolve_hash(seed, calls[kind]["bulletin"])]
    if kind == AGENT and not refs and not head_optional:
        raise SeedError(f"source {text!r}: name the bulletin it was read in; {SOURCE_HELP}")
    out = []
    for full in dict.fromkeys(refs) or [None]:
        source: dict[str, Any] = {"source": kind}
        if full is not None:
            source["bulletin"] = short_hash(seed, full)
        if page is not None or kind == AGENT:
            source["page"] = page
        source["said"] = said
        out.append(source)
    return out


def format_source(source: Any) -> str:
    """A source as the spec that writes it."""
    if not isinstance(source, dict):
        return repr(source)
    kind = source.get("source")
    if kind == WEBSITE:
        head = f"web {source.get('url')}"
    else:
        bulletin = source.get("bulletin")
        head = " ".join(str(p) for p in (
            None if kind == AGENT else kind,
            bulletin[:MIN_HASH_PREFIX] if isinstance(bulletin, str) else None,
            f"p{source['page']}" if source.get("page") else None) if p)
    return f"{head}: {source.get('said')}"


# ── A draft being written ───────────────────────────────────────────────────
@dataclass
class Draft:
    """A seed file in memory while commands change it: what they touched, and warnings."""

    seed: dict[str, Any]
    church_ids: dict[str, int]  # the parish's churches, slug -> id
    eval_run: str | None = None
    touched: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.seed.get("status") == APPROVED:
            raise SeedError("An approved seed belongs to its reviewer; it cannot be changed")
        for key in ("slots", "bulletins", "calls"):
            if not isinstance(self.seed.get(key), list):
                raise SeedError(f"the file's {key} is not a list: fix it by hand first")

    @property
    def churches(self) -> list[str]:
        return sorted(self.church_ids)

    @property
    def slots(self) -> list[dict[str, Any]]:
        return self.seed["slots"]

    def slot(self, slot_id: str) -> dict[str, Any]:
        found = next((s for s in self.slots if isinstance(s, dict) and s.get("id") == slot_id),
                     None)
        if found is None:
            ids = [s.get("id") for s in self.slots if isinstance(s, dict)]
            raise SeedError(f"no slot {slot_id} (the file has {', '.join(map(str, ids))})"
                            if ids else f"no slot {slot_id}: the file has no slots yet")
        return found

    def touch(self, slot_id: str) -> None:
        if slot_id not in self.touched:
            self.touched.append(slot_id)

    def sources(self, specs: list[str] | None) -> list[dict[str, Any]]:
        out = [s for spec in specs or [] for s in parse_source(self.seed, spec)]
        if self.eval_run is not None and any(s["source"] == WEBSITE for s in out):
            raise SeedError("website sources are not allowed in a historical test run (R5)")
        return out

    def new_slot(self, slot: dict[str, Any]) -> str:
        taken = {s["id"] for s in self.slots if isinstance(s, dict)
                 and isinstance(s.get("id"), str)}
        slot = {"id": next_slot_id(taken), **slot}
        self.slots.append(self.fill(slot))
        self.touch(slot["id"])
        return slot["id"]

    def fill(self, slot: dict[str, Any]) -> dict[str, Any]:
        """The slot with `finalize`'s defaults, as the file stores it."""
        return fill_slot(slot, self.churches[0] if len(self.churches) == 1 else None, set())

    def check(self) -> None:
        """Raise with every problem in the slots touched; warn of what `finalize` will."""
        problems: list[str] = []
        live = [s for s in self.slots if isinstance(s, dict)]
        churches = self.church_ids
        included: list[tuple[str, Entry]] = []
        for slot in live:
            if slot.get("status") == SETTLED and slot.get("decision") == INCLUDE \
                    and isinstance(slot.get("entry"), dict) \
                    and not entry_problem(slot["entry"], churches, ""):
                entry = parse_entry(slot["entry"], churches)
                slot_id = str(slot.get("id"))
                for other_id, other in included:
                    if {slot_id, other_id} & set(self.touched) and entry.conflicts_with(other):
                        problems.append(f"{other_id} and {slot_id} are the same slot: "
                                        "their recurrence patterns overlap; one of them must go")
                included.append((slot_id, entry))
        groups = set()
        for slot in live:
            if slot.get("id") not in self.touched:
                continue
            where = str(slot["id"])
            found = slot_problems(self.seed, slot, where)
            if not found:
                is_in = slot["status"] == SETTLED and slot["decision"] == INCLUDE
                if slot["entry"] is not None:
                    found += [p for p in [entry_problem(
                        slot["entry"], churches, f"{where}.entry", outside_ok=not is_in)] if p]
                for j, option in enumerate(slot["options"] or []):
                    if option.get("entry") is not None:
                        found += [p for p in [entry_problem(
                            option["entry"], churches, f"{where}.options[{j}].entry",
                            outside_ok=True)] if p]
                rationale = slot["rationale"]
                if slot["status"] == SETTLED and not (
                        RULE_ID.match(rationale.strip()) or "POLICY" in rationale):
                    self.warnings.append(f"{where}: a settled slot's rationale starts with the "
                                         "rule it rests on (R1: …) or names the POLICY section")
            problems += found
            if slot.get("group"):
                groups.add(slot["group"])
        problems += group_problems(self.slots, groups)
        if problems:
            raise SeedError("nothing written:\n  " + "\n  ".join(problems))


# ── Commands ────────────────────────────────────────────────────────────────
UNSET = object()


def _page(value: str) -> int | None:
    if value.lower() in ("-", "none", "null"):
        return None
    if not value.isdigit() or int(value) < 1:
        raise argparse.ArgumentTypeError(f"a page is a number from 1, or - for none: {value!r}")
    return int(value)


def _anchor(draft: Draft, page: Any, sources: list[dict[str, Any]]) -> int | None:
    """The slot's `page`: as given, else where an agent source reads the newest bulletin.
    An agent source on the newest bulletin without a page takes the slot's."""
    newest = newest_listed(draft.seed)

    def on_newest(s: dict[str, Any]) -> bool:
        return s["source"] == AGENT and resolve_hash(draft.seed, s.get("bulletin")) == newest

    if page is UNSET:
        page = next((s["page"] for s in sources if on_newest(s) and s.get("page")), None)
    for s in sources:
        if on_newest(s) and s.get("page") is None and page is not None:
            s["page"] = page
    return page


def _options(
    draft: Draft, raw: list[list[str]] | None, bases: list[dict[str, Any] | None],
) -> list[list[dict[str, Any]]]:
    """Each slot's options from `--option LABEL [ENTRY]` (a `*` before the label marks the
    leaning). `bases[k]` is slot k's entry, which `+` entries change; without one, a `+`
    entry changes the first option's."""
    if not raw:
        raise SeedError("a question needs its options: --option '*Label' 'ENTRY' and "
                        "--option 'Leave out' (no entry), a * marking the leaning")
    parsed = []
    for item in raw:
        if len(item) > 2:
            raise SeedError(f"--option takes a label and an entry, not {len(item)} values: "
                            f"{item!r} (quote each)")
        label = item[0]
        leaning = label.startswith("*")
        parsed.append((label.removeprefix("*").strip(), leaning,
                       parse_entry_spec(item[1]) if len(item) == 2 else None))
    n = len(bases)
    first = next((spec for _, _, spec in parsed if spec and not spec.patch), None)
    if first is not None and all(b is None for b in bases):
        made = build_entries(first, draft.churches)
        if n == 1 and len(made) > 1:
            raise SeedError(f"option entry {first.text!r} makes {len(made)} entries: ask "
                            "about several days with `slot ask` (one slot each), or name one")
        bases = made if len(made) == n else bases
    per_slot: list[list[dict[str, Any]]] = [[] for _ in range(n)]
    for label, leaning, spec in parsed:
        if spec is None:
            entries: list[dict[str, Any] | None] = [None] * n
        elif spec.patch:
            if any(b is None for b in bases):
                raise SeedError(f"option {label!r}: a `+` entry changes the slot's entry or "
                                "the first option's, and there is none")
            entries = []
            for b in bases:
                made = build_entries(spec, draft.churches, b)
                if len(made) != 1:
                    raise SeedError(f"option {label!r}: a `+` entry changes one entry, and "
                                    f"{spec.text!r} makes {len(made)}")
                entries.append(made[0])
        else:
            made = build_entries(spec, draft.churches)
            if len(made) == 1 and n > 1 and spec is not first:
                raise SeedError(f"option {label!r} makes one entry for {n} slots: start it "
                                "with + to change each slot's own")
            if len(made) not in (1, n):
                raise SeedError(f"option {label!r} makes {len(made)} entries for {n} slots")
            entries = made if len(made) == n else made * n
        for k in range(n):
            option: dict[str, Any] = {"label": label, "entry": entries[k]}
            if leaning:
                option["leaning"] = True
            per_slot[k].append(option)
    return per_slot


def add_settled(draft: Draft, args: argparse.Namespace, decision: str) -> list[str]:
    """`slot include` / `slot exclude`: one settled slot per day/date and time."""
    if args.entry in (None, "-", "none"):
        if decision == INCLUDE:
            raise SeedError(f"an included slot needs its entry: {ENTRY_HELP}")
        entries: list[dict[str, Any] | None] = [None]  # R26: nothing to record
    else:
        entries = list(build_entries(parse_entry_spec(args.entry), draft.churches))
    sources = draft.sources(args.src)
    page = _anchor(draft, args.page, sources)
    return [draft.new_slot({
        "decision": decision, "status": SETTLED, "entry": entry, "page": page,
        "sources": copy.deepcopy(sources), "rationale": args.why or "",
    }) for entry in entries]


def add_question(draft: Draft, args: argparse.Namespace) -> list[str]:
    """`slot ask`: an open question; an option with several days asks one slot per day,
    grouped so one answer settles them."""
    question = args.question
    if not question and args.group:
        lead = next((s for s in draft.slots if isinstance(s, dict)
                     and s.get("group") == args.group), None)
        question = lead.get("question") if lead else None
    if not question:
        raise SeedError("say the question: `slot ask PARISH \"Add a first-Friday Holy Hour?\" "
                        "--option ...`")
    probe = next((parse_entry_spec(o[1]) for o in args.option or []
                  if len(o) == 2 and not o[1].lstrip().startswith("+")), None)
    n = len(build_entries(probe, draft.churches)) if probe else 1
    options = _options(draft, args.option, [None] * n)
    sources = draft.sources(args.src)
    page = _anchor(draft, args.page, sources)
    group = args.group if args.group not in (None, "-") else None
    ids = []
    for k in range(n):
        slot: dict[str, Any] = {
            "decision": None, "status": NEEDS_HUMAN, "entry": None, "page": page,
            "sources": copy.deepcopy(sources), "rationale": args.why or "",
            "question": question, "options": options[k],
        }
        if group:
            slot["group"] = group
        ids.append(draft.new_slot(slot))
        if n > 1 and not group:
            group = ids[0]
            draft.slot(ids[0])["group"] = group
    return ids


def _cites_call(draft: Draft, slot: dict[str, Any]) -> bool:
    calls = {c.get("id") for c in draft.seed["calls"] if isinstance(c, dict)}
    return any(isinstance(s, dict) and s.get("source") in calls for s in slot.get("sources") or [])


_ANSWERED_ONLY = ("src",)


def edit_slots(draft: Draft, args: argparse.Namespace) -> list[str]:
    """`slot edit`: change the named slots' fields, keeping their ids."""
    changes = {k for k in ("entry", "no_entry", "include", "exclude", "ask", "option",
                           "src", "drop_src", "why", "group")
               if getattr(args, k, None) not in (None, False, [])}
    if args.page is not UNSET:
        changes.add("page")
    if not changes:
        raise SeedError("say what to change: --entry, --include/--exclude/--ask, --option, "
                        "--page, --src, --drop-src, --why or --group")
    if sum(1 for k in ("include", "exclude", "ask") if k in changes) > 1:
        raise SeedError("--include, --exclude and --ask each set the decision: give one")
    for slot_id in args.ids:
        slot = draft.slot(slot_id)
        if isinstance(slot.get("answer"), dict) and changes - set(_ANSWERED_ONLY):
            raise SeedError(f"{slot_id} was answered by {slot['answer'].get('by')}: its "
                            "decision is the reviewer's; only --src may add evidence")
        _edit(draft, slot, args, changes)
        draft.touch(slot_id)
    return list(args.ids)


def _edit(draft: Draft, slot: dict[str, Any], args: argparse.Namespace, changes: set[str]) -> None:
    sid = slot["id"]
    base = slot.get("entry") if isinstance(slot.get("entry"), dict) else next(
        (o["entry"] for o in slot.get("options") or []
         if isinstance(o, dict) and isinstance(o.get("entry"), dict)), None)
    entry = slot.get("entry")
    if "entry" in changes:
        spec = parse_entry_spec(args.entry)
        made = build_entries(spec, draft.churches, entry if isinstance(entry, dict) else None)
        if len(made) != 1:
            raise SeedError(f"{sid}: entry {args.entry!r} makes {len(made)} entries; a slot "
                            "has one (add the others with `slot include`)")
        entry = made[0]
    if "no_entry" in changes:
        entry = None
    if "option" in changes:
        slot["options"] = _options(draft, args.option, [
            entry if isinstance(entry, dict) else base])[0]
    if "include" in changes or "exclude" in changes:
        decision = INCLUDE if "include" in changes else EXCLUDE
        if entry is None and "no_entry" not in changes:
            options = [o for o in slot.get("options") or [] if isinstance(o, dict)]
            lean = next((o for o in options if o.get("leaning") is True), None)
            pick = lean.get("entry") if lean else None
            entry = pick if pick is not None or decision == INCLUDE else base
        slot.update(decision=decision, status=SETTLED, question=None, options=None)
        slot.pop("group", None)
    if "ask" in changes:
        slot.update(status=NEEDS_HUMAN, decision=None, question=args.ask)
        entry = None
        if not slot.get("options"):
            raise SeedError(f"{sid}: a question needs its options (--option)")
    slot["entry"] = entry
    if "page" in changes:
        slot["page"] = args.page
    if "drop_src" in changes:
        sources = slot.get("sources") or []
        for n in sorted(set(args.drop_src), reverse=True):
            if not 1 <= n <= len(sources):
                raise SeedError(f"{sid} has no source {n} (it has {len(sources)}; "
                                "`slot show` numbers them)")
            if _cites_call(draft, {"sources": [sources[n - 1]]}):
                raise SeedError(f"{sid}: source {n} is a paid call's evidence and stays")
            del sources[n - 1]
    if "src" in changes:
        slot["sources"] = (slot.get("sources") or []) + draft.sources(args.src)
    if "why" in changes:
        slot["rationale"] = args.why
    if "group" in changes:
        if args.group == "-":
            slot.pop("group", None)
        else:
            slot["group"] = args.group
    slot.update(draft.fill(slot))


def remove_slots(draft: Draft, args: argparse.Namespace) -> list[str]:
    """`slot rm`: remove slots the drafter added; never a reviewer's answer or a call's
    evidence."""
    for slot_id in args.ids:
        slot = draft.slot(slot_id)
        if isinstance(slot.get("answer"), dict):
            raise SeedError(f"{slot_id} was answered by {slot['answer'].get('by')}; it stays")
        if _cites_call(draft, slot):
            raise SeedError(f"{slot_id} cites a paid call, whose evidence stays: change it "
                            "with `slot edit` (to --exclude, say) instead")
    draft.seed["slots"] = [s for s in draft.slots
                           if not (isinstance(s, dict) and s.get("id") in args.ids)]
    draft.removed += [i for i in args.ids if i not in draft.removed]
    draft.touched = [i for i in draft.touched if i not in args.ids]
    return []


def set_summary(draft: Draft, args: argparse.Namespace) -> list[str]:
    if not args.text.strip():
        raise SeedError("a summary is two or three sentences a reviewer reads first")
    draft.seed["summary"] = args.text.strip()
    return []


def set_church_issue(draft: Draft, args: argparse.Namespace) -> list[str]:
    """`church-issue`: list a church or chapel the church list lacks, once (R23)."""
    issues = [i for i in draft.seed.get("church_list_issues") or []
              if not (isinstance(i, dict) and i.get("church") == args.church)]
    if not args.rm:
        if not args.said:
            raise SeedError("say what the bulletin holds there: `church-issue PARISH CHURCH "
                            "'9f2c41d0 p2: Mon-Thu 12:15 Mass'`")
        sources = parse_source(draft.seed, args.said, head_optional=True)
        if len(sources) != 1 or sources[0]["source"] != AGENT:
            raise SeedError("a church issue names at most one bulletin and its page")
        issue = {"church": args.church, "said": sources[0]["said"]}
        for key in ("bulletin", "page"):
            if sources[0].get(key) is not None:
                issue[key] = sources[0][key]
        issues.append(issue)
    draft.seed["church_list_issues"] = issues
    problems = church_issue_problems(draft.seed)
    if problems:
        raise SeedError("nothing written: " + "; ".join(problems))
    return []


def set_blocked(draft: Draft, args: argparse.Namespace) -> list[str]:
    """`block`: R34. `--clear` goes back to drafting."""
    if args.clear:
        draft.seed.update(status=DRAFTING, blocked_reason=None)
    elif not args.reason:
        raise SeedError("say why it is blocked, or pass --clear")
    else:
        draft.seed.update(status=BLOCKED, blocked_reason=args.reason)
    return []


# ── Arguments, shared by the commands and `slot batch` ──────────────────────
def _source_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--src", action="append", metavar="'HEAD: SAID'",
                   help="A source, repeatable: `latest p2: Sat 4 PM`, `9f2c41d0,1ab3e7c2 p2: …`, "
                        "`web URL: …`, `history: …`, `c1 p2: …`")


def _why_arg(p: argparse.ArgumentParser, required: bool = True) -> None:
    p.add_argument("--why", required=required, metavar="RATIONALE",
                   help="The rationale, starting with the rule it rests on (R1: …)")


def _page_arg(p: argparse.ArgumentParser, default: Any) -> None:
    p.add_argument("--page", type=_page, default=default,
                   help="Where the newest bulletin prints it, - for none (default: the page "
                        "of a source on the newest bulletin)")


def _option_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--option", action="append", nargs="+", metavar="LABEL [ENTRY]",
                   help="An option, repeatable: a label (`*` before it marks the leaning) "
                        "and its entry; no entry leaves the slot out. A `+` entry changes "
                        "the first option's (or the slot's)")


def add_write_args(name: str, p: argparse.ArgumentParser) -> None:
    """The arguments of write command `name` after the parish, for the CLI and `slot batch`."""
    if name in ("include", "exclude"):
        p.add_argument("entry", nargs=None if name == "include" else "?",
                       help="The entry (" + ENTRY_HELP + ")"
                       + ("; - or none for nothing to record (R26)" if name == "exclude" else ""))
        _source_arg(p)
        _page_arg(p, UNSET)
        _why_arg(p)
    elif name == "ask":
        p.add_argument("question", nargs="?",
                       help="The question (with --group of an existing group: its question)")
        _option_arg(p)
        _source_arg(p)
        _page_arg(p, UNSET)
        _why_arg(p)
        p.add_argument("--group", help="Ask it with this group's other slots (R27)")
    elif name == "edit":
        p.add_argument("ids", nargs="+", metavar="ID", help="Slot ids (s3 s4)")
        p.add_argument("--entry", metavar="ENTRY",
                       help="Change the entry: only what it names (`17:00`, `note=`, `weeks=`)")
        p.add_argument("--no-entry", action="store_true", help="Nothing to record (R26)")
        how = p.add_mutually_exclusive_group()
        how.add_argument("--include", action="store_true", help="Settle it as included")
        how.add_argument("--exclude", action="store_true", help="Settle it as left out")
        how.add_argument("--ask", metavar="QUESTION", help="Make it, or change, a question")
        _option_arg(p)
        _page_arg(p, UNSET)
        _source_arg(p)
        p.add_argument("--drop-src", action="append", type=int, metavar="N",
                       help="Remove the drafter's source N (`slot show` numbers them)")
        _why_arg(p, required=False)
        p.add_argument("--group", help="Put it in this group (- for none)")
    elif name == "rm":
        p.add_argument("ids", nargs="+", metavar="ID", help="Slot ids")
    elif name == "summary":
        p.add_argument("text", help="Two or three sentences a reviewer reads first")
    elif name == "church-issue":
        p.add_argument("church", help="The church or chapel as the bulletin names it")
        p.add_argument("said", nargs="?", help="`9f2c41d0 p2: what it holds there`")
        p.add_argument("--rm", action="store_true", help="Take it off the list")
    elif name == "block":
        p.add_argument("reason", nargs="?", help="Why it can't be seeded now (R34)")
        p.add_argument("--clear", action="store_true", help="Unblock: back to drafting")


WRITES = {
    "include": lambda d, a: add_settled(d, a, INCLUDE),
    "exclude": lambda d, a: add_settled(d, a, EXCLUDE),
    "ask": add_question,
    "edit": edit_slots,
    "rm": remove_slots,
    "summary": set_summary,
    "church-issue": set_church_issue,
    "block": set_blocked,
}


class _LineParser(argparse.ArgumentParser):
    def error(self, message: str):  # type: ignore[override]
        raise SeedError(message)


def _batch_parser() -> argparse.ArgumentParser:
    parser = _LineParser(prog="line", add_help=False)
    sub = parser.add_subparsers(dest="verb", required=True, parser_class=_LineParser)
    for name in WRITES:
        add_write_args(name, sub.add_parser(name, prog=name, add_help=False))
    return parser


def batch_lines(text: str) -> list[tuple[int, list[str]]]:
    """A batch's commands: one per line, `\\` at a line's end continuing it, `#` comments."""
    out: list[tuple[int, list[str]]] = []
    pending, start = "", 0
    for n, line in enumerate(text.splitlines(), start=1):
        if not pending:
            start = n
        if line.rstrip().endswith("\\"):
            pending += line.rstrip()[:-1] + " "
            continue
        whole = pending + line
        pending = ""
        try:
            words = shlex.split(whole, comments=True)
        except ValueError as exc:
            raise SeedError(f"line {start}: {exc}") from exc
        if words:
            out.append((start, words))
    if pending.strip():
        raise SeedError(f"line {start}: the batch ends inside a continued line")
    return out


def run_batch(draft: Draft, text: str) -> None:
    """Apply a batch's commands in order (`slot batch`); a bad line stops it, unwritten."""
    parser = _batch_parser()
    lines = batch_lines(text)
    if not lines:
        raise SeedError("the batch is empty")
    for n, words in lines:
        if words[0] not in WRITES:
            raise SeedError(f"line {n}: {words[0]!r} is not one of {', '.join(WRITES)} "
                            "(a batch line leaves out `pnpm seed slot` and the parish)")
        try:
            args = parser.parse_args(words)
            WRITES[args.verb](draft, args)
        except SeedError as exc:
            raise SeedError(f"line {n} ({words[0]}): {exc}") from exc


# ── Text ────────────────────────────────────────────────────────────────────
def _clip(text: str, n: int = 90) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= n else text[:n - 1] + "…"


def slot_lines(slot: Any, *, full: bool = False) -> list[str]:
    """A slot as `seed slot list` (or, with `full`, `seed slot show`) prints it."""
    if not isinstance(slot, dict):
        return [f"(not a slot: {_clip(repr(slot))})"]
    page = f"p{slot['page']}" if slot.get("page") else "p-"
    sources = slot.get("sources") if isinstance(slot.get("sources"), list) else []
    if slot.get("status") == NEEDS_HUMAN or slot.get("question") and full:
        what = "ask" if slot.get("status") == NEEDS_HUMAN else str(slot.get("decision"))
        head = f"{slot.get('id', '?'):4} {what:7} {page:4} {slot.get('question')}"
    else:
        head = f"{slot.get('id', '?'):4} {str(slot.get('decision')):7} {page:4} " \
            f"{format_entry(slot.get('entry'))}"
    if slot.get("group"):
        head += f"  [group {slot['group']}]"
    if not full:
        head += f"  ({len(sources)} src)"
    lines = [head]
    options = slot.get("options") if isinstance(slot.get("options"), list) else []
    if slot.get("status") == NEEDS_HUMAN or full:
        for o in options:
            if isinstance(o, dict):
                lines.append(f"       {'*' if o.get('leaning') else ' '} {o.get('label')}"
                             + (f" = {format_entry(o['entry'])}" if o.get("entry") else ""))
    answer = slot.get("answer")
    if isinstance(answer, dict):
        lines.append(f"       answered {answer.get('choice')} by {answer.get('by')} "
                     f"{str(answer.get('at') or '')[:10]}")
    if full:
        if slot.get("status") != NEEDS_HUMAN and slot.get("question"):
            lines.append(f"       entry {format_entry(slot.get('entry'))}")
        lines += [f"       [{i}] {format_source(s)}" for i, s in enumerate(sources, start=1)]
        lines.append(f"       why: {slot.get('rationale')}")
    else:
        lines.append(f"       {_clip(slot.get('rationale'))}")
    return lines
