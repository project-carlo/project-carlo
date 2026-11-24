"""The seed file: one parish's drafted schedule, committed as `data/seeds/<parish>.json`.

A seed file holds every slot an agent drafted for a parish, what each source
said about it, what it decided and why, and the questions it left for a
person (.claude/skills/draft-parish-seed/file-format.md). This module reads, writes and
checks the file's shape; `checks` checks it against the database, and
`loader` turns an approved one into a `seed` revision.

Entries are in the labels' event shape without `page_number`, `origin` and
`optional` (`model.ENTRY_KEYS`), with 24-hour `HH:MM` times, so they are what
`pnpm schedule seed` reads and can be scored against the labels as they are.

A file's `kind` is `bulletin` (the default, so files written before kinds existed
are bulletin seeds) or `source`: a parish with no bulletin, drafted from pages
of its own website or Facebook page that `seed capture` stored
(docs/source-schedules-plan.md). A source seed lists no bulletins and no calls.
Its `captures` are the pages read, each slot cites them, and it says why the
schedule looks current (`current_because`) and when to read it again
(`recheck_after`). Each capture's text is committed beside the seeds, in
`captures/<parish>/<content hash>.txt`, so its quotes can be checked anywhere, and
so is each screenshot a quote was read from (`<screenshot hash>.webp`), so a
reviewer anywhere can see it.
"""

from __future__ import annotations

import calendar
import json
import os
import re
import threading
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.model import (
    SOURCE_PLATFORMS,
    WEBSITE,
    canonical_json,
    is_iso_date,
    is_valid_hash,
    is_valid_slug,
    normalize_as_of,
    sha256_text,
    source_platform,
    validate_entry,
)
from pdf_extract.paths import DATA_DIR
from pdf_extract.storage import utc_now_iso

SCHEMA_VERSION = 1
SEEDS_DIR = DATA_DIR / "seeds"
# Where `seed pdf` and `seed pages` put the files they make (gitignored).
WORK_DIR = DATA_DIR / "seed-work"

DRAFTED_BY = "claude-code/draft-parish-seed"

DRAFTING = "drafting"
NEEDS_REVIEW = "needs_review"
READY = "ready"
APPROVED = "approved"
BLOCKED = "blocked"
STATUSES = (DRAFTING, NEEDS_REVIEW, READY, APPROVED, BLOCKED)

INCLUDE = "include"
EXCLUDE = "exclude"
DECISIONS = (INCLUDE, EXCLUDE)

SETTLED = "settled"
NEEDS_HUMAN = "needs_human"
SLOT_STATUSES = (SETTLED, NEEDS_HUMAN)

# A slot's `sources[].source`: the agent's own reading, extract mode's stored
# events, a page of the parish's website (with its `url`), or the id of one of
# the file's `calls`. A source seed's sources are its captures instead: `website`
# or `facebook`, each naming the capture it quotes.
AGENT = "agent"
HISTORY = "history"
SOURCE_KINDS = (AGENT, HISTORY, WEBSITE)
CAPTURE_SOURCES = SOURCE_PLATFORMS  # website, facebook

# A file's `kind` (module docstring).
BULLETIN_SEED = "bulletin"
SOURCE_SEED = "source"
SEED_KINDS = (BULLETIN_SEED, SOURCE_SEED)
# Where each capture's text is kept, under the seeds folder (committed).
CAPTURES_DIRNAME = "captures"
# A source seed is read again this many months after its `as_of`, by default.
RECHECK_MONTHS = 3

EXTRACT = "extract"
ASK = "ask"
CALL_KINDS = (EXTRACT, ASK)

# An answered question's `answer.choice`: an option's index, or what the
# reviewer did instead of picking one.
EDITED = "edited"
DROPPED = "dropped"

SEED_KEYS = (
    "schema_version", "parish_slug", "status", "as_of", "drafted_by", "drafted_at",
    "reviewer", "approved_at", "summary", "blocked_reason", "bulletins", "calls", "slots",
)
BULLETIN_KEYS = ("content_hash", "fetched_at", "published_date", "read")
SLOT_KEYS = (
    "id", "decision", "status", "entry", "page", "sources", "rationale", "question",
    "options", "answer",
)
# Keys a file may leave out (files written before they existed have none).
# `church_list_issues`: churches or chapels the bulletins name that the church
# list lacks or can't place, for whoever maintains data/churches.csv. A slot's
# `group`: open questions that share one are one question, answered together.
# A source seed's own keys, which a bulletin seed never has.
SOURCE_SEED_KEYS = ("kind", "captures", "current_because", "recheck_after")
OPTIONAL_SEED_KEYS = ("church_list_issues", *SOURCE_SEED_KEYS)
OPTIONAL_SLOT_KEYS = ("group", "weekly_omission")
# A capture: one page as `seed capture` stored it. `content_hash` is the SHA-256 of
# its committed text (`capture_document`: the page's address, and the Facebook pages it
# links, then its text), so two pages with the same text are two captures.
# `screenshot_hash` is the screenshot's (a WebP; null when none was taken), and
# `primary` marks the one page the website links as the times' source. A source that
# quotes the screenshot names it in `from_image`, so a new screenshot of the page
# can't silently stand behind an old quote.
CAPTURE_KEYS = (
    "content_hash", "url", "final_url", "platform", "captured_at", "screenshot_hash", "primary",
)
CHURCH_ISSUE_KEYS = ("church", "said", "bulletin", "page")
# Shortest prefix of a content hash that may name a bulletin inside a file.
MIN_HASH_PREFIX = 8

_write_lock = threading.Lock()


class SeedFileError(ValueError):
    """A seed file, slug or path that must not be read or written."""


# ── Paths ───────────────────────────────────────────────────────────────────
def seed_path(parish_slug: str, seeds_dir: Path = SEEDS_DIR) -> Path:
    """Where a parish's seed file lives; raises SeedFileError for anything unsafe."""
    if not is_valid_slug(parish_slug):
        raise SeedFileError(f"Invalid parish slug: {parish_slug!r}")
    root = seeds_dir.resolve()
    path = (root / f"{parish_slug}.json").resolve()
    if not path.is_relative_to(root):
        raise SeedFileError(f"Seed path escapes {seeds_dir}: {path}")
    return path


def capture_text_path(parish_slug: str, content_hash: str, seeds_dir: Path = SEEDS_DIR) -> Path:
    """Where a capture's text is committed; raises SeedFileError for anything unsafe."""
    if not is_valid_slug(parish_slug) or not is_valid_hash(content_hash):
        raise SeedFileError(f"Invalid capture: {parish_slug!r} {content_hash!r}")
    return seeds_dir / CAPTURES_DIRNAME / parish_slug / f"{content_hash}.txt"


def read_capture_text(
    parish_slug: str, content_hash: str, seeds_dir: Path = SEEDS_DIR,
) -> str | None:
    try:
        return capture_text_path(parish_slug, content_hash, seeds_dir).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None


def screenshot_path(parish_slug: str, screenshot_hash: str, seeds_dir: Path = SEEDS_DIR) -> Path:
    """Where a screenshot a quote was read from is committed (`seed finalize` puts it there)."""
    if not is_valid_slug(parish_slug) or not is_valid_hash(screenshot_hash):
        raise SeedFileError(f"Invalid screenshot: {parish_slug!r} {screenshot_hash!r}")
    return seeds_dir / CAPTURES_DIRNAME / parish_slug / f"{screenshot_hash}.webp"


# A capture's committed text opens with what it is of, hashed with the page's text:
# the address asked for, where it ended when that differs, and the Facebook pages it
# links (what makes a Facebook page the parish's own). A blank line ends it.
CAPTURED_FROM = "Captured from "
ENDED_AT = "Ended at "
LINKS_FACEBOOK = "Links to Facebook page "


def capture_document(url: str, final_url: str | None, facebook_pages: list[str], text: str,
                     ) -> str:
    """A capture's committed text: its header, a blank line, the page's text."""
    lines = [CAPTURED_FROM + url]
    if final_url:
        lines.append(ENDED_AT + final_url)
    lines += [LINKS_FACEBOOK + page for page in facebook_pages]
    return "\n".join(lines) + "\n\n" + text.rstrip("\n") + "\n"


def parse_capture_document(document: str) -> tuple[dict[str, Any], str] | None:
    """A capture's header (`url`, `final_url`, `facebook_pages`) and the page's text, or
    None when it doesn't open with a header."""
    head, sep, body = document.partition("\n\n")
    lines = head.split("\n")
    if not sep or not lines[0].startswith(CAPTURED_FROM):
        return None
    header: dict[str, Any] = {"url": lines[0].removeprefix(CAPTURED_FROM), "final_url": None,
                              "facebook_pages": []}
    for line in lines[1:]:
        if line.startswith(ENDED_AT) and header["final_url"] is None:
            header["final_url"] = line.removeprefix(ENDED_AT)
        elif line.startswith(LINKS_FACEBOOK):
            header["facebook_pages"].append(line.removeprefix(LINKS_FACEBOOK))
        else:
            return None
    return header, body


def seed_slugs(seeds_dir: Path = SEEDS_DIR) -> list[str]:
    """The parish slugs that have a seed file, sorted."""
    if not seeds_dir.is_dir():
        return []
    return sorted(p.stem for p in seeds_dir.glob("*.json") if is_valid_slug(p.stem))


def read_seed(parish_slug: str, seeds_dir: Path = SEEDS_DIR) -> dict[str, Any] | None:
    path = seed_path(parish_slug, seeds_dir)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except ValueError as exc:
        raise SeedFileError(f"{path} is not JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SeedFileError(f"{path} must hold a JSON object")
    return data


def write_seed_file(seed: dict[str, Any], seeds_dir: Path = SEEDS_DIR) -> Path:
    """Write a seed file as it is (callers validate first). Returns its path."""
    path = seed_path(seed["parish_slug"], seeds_dir)
    data = json.dumps(seed, indent=2, ensure_ascii=False) + "\n"
    with _write_lock:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}-{threading.get_ident()}")
        tmp.write_text(data, encoding="utf-8")
        tmp.replace(path)
    return path


def new_seed(parish_slug: str, bulletins: list[dict[str, Any]]) -> dict[str, Any]:
    """An empty draft listing the parish's bulletins, none of them read yet."""
    return {
        "schema_version": SCHEMA_VERSION,
        "parish_slug": parish_slug,
        "status": DRAFTING,
        "as_of": None,
        "drafted_by": DRAFTED_BY,
        "drafted_at": utc_now_iso(),
        "reviewer": None,
        "approved_at": None,
        "summary": "",
        "blocked_reason": None,
        "bulletins": [
            {
                "content_hash": b["content_hash"],
                "fetched_at": b["fetched_at"],
                "published_date": b.get("published_date"),
                "read": False,
            }
            for b in bulletins
        ],
        "calls": [],
        "slots": [],
    }


def new_source_seed(parish_slug: str) -> dict[str, Any]:
    """An empty source draft: no bulletins, no captures yet."""
    return {
        **new_seed(parish_slug, []),
        "kind": SOURCE_SEED,
        "captures": [],
        "current_because": None,
        "recheck_after": None,
    }


def add_months(day: date, months: int) -> date:
    """`day` that many months later, on the month's last day when it has fewer days."""
    month = day.month - 1 + months
    year, month = day.year + month // 12, month % 12 + 1
    return day.replace(year=year, month=month,
                       day=min(day.day, calendar.monthrange(year, month)[1]))


def default_recheck_after(as_of: str) -> str:
    """When a source seed is read again by default: RECHECK_MONTHS after its `as_of`."""
    return add_months(date.fromisoformat(normalize_as_of(as_of)[:10]), RECHECK_MONTHS).isoformat()


# ── Reading a file ──────────────────────────────────────────────────────────
def seed_kind(seed: dict[str, Any]) -> str:
    """`bulletin` or `source` (anything else is reported by `validate_seed`)."""
    kind = seed.get("kind", BULLETIN_SEED)
    return kind if isinstance(kind, str) else str(kind)


def is_source_seed(seed: dict[str, Any]) -> bool:
    return seed_kind(seed) == SOURCE_SEED


def captures(seed: dict[str, Any]) -> list[dict[str, Any]]:
    return [c for c in _list(seed.get("captures")) if isinstance(c, dict)
            and isinstance(c.get("content_hash"), str)]


def resolve_capture(seed: dict[str, Any], ref: Any) -> dict[str, Any] | None:
    """The file's capture `ref` names (its content hash or a unique prefix)."""
    if not isinstance(ref, str) or len(ref) < MIN_HASH_PREFIX:
        return None
    ref = ref.removesuffix("…").lower()
    found = [c for c in captures(seed) if c["content_hash"].startswith(ref)]
    return found[0] if len(found) == 1 else None


def newest_capture(seed: dict[str, Any]) -> dict[str, Any] | None:
    """The newest capture: the one a source seed's `as_of` names."""
    timed = [c for c in captures(seed) if _is_time(c.get("captured_at"))]
    return max(timed, key=lambda c: normalize_as_of(c["captured_at"]), default=None)


def primary_capture(seed: dict[str, Any]) -> dict[str, Any] | None:
    """The page the website links as the times' source."""
    return next((c for c in captures(seed) if c.get("primary") is True), None)


def short_capture(seed: dict[str, Any], full: str) -> str:
    """The shortest prefix (8 characters or more) naming capture `full` in the file."""
    for n in range(MIN_HASH_PREFIX, len(full)):
        found = resolve_capture(seed, full[:n])
        if found is not None and found["content_hash"] == full:
            return full[:n]
    return full


def normalize_quote(text: str) -> str:
    """Text as a quote is matched against a capture: case and whitespace folded, and
    typographic quotes, dashes and dots made plain."""
    text = text.translate({0x2018: "'", 0x2019: "'", 0x201C: '"', 0x201D: '"',
                           0x2013: "-", 0x2014: "-", 0x2026: "...", 0xA0: " "})
    return " ".join(text.lower().split())
def _list(value: Any) -> list[Any]:
    """A list field of a file that may be malformed: anything but a list reads as empty."""
    return value if isinstance(value, list) else []


def open_questions(seed: dict[str, Any]) -> list[dict[str, Any]]:
    """The open slots: one per slot, so a group's slots are each listed."""
    return [s for s in _list(seed.get("slots")) if isinstance(s, dict)
            and s.get("status") == NEEDS_HUMAN]


def question_count(seed: dict[str, Any]) -> int:
    """How many questions a reviewer answers: an open group counts once."""
    groups = set()
    count = 0
    for slot in open_questions(seed):
        group = slot.get("group")
        if isinstance(group, str) and group:
            if group in groups:
                continue
            groups.add(group)
        count += 1
    return count


# Rule and candidate IDs of the seeding rules (.claude/skills/draft-parish-seed/rules.md).
RULE_ID = re.compile(r"\b[RC]\d+\b")


def asked_questions(seed: dict[str, Any]) -> list[dict[str, Any]]:
    """Every question the file asked, open or answered: a group's once, by its first slot.

    `match` says how the answer relates to the leaning: `leaning`, `other` (another
    option), `dropped` or `edited`, or None while open. `matched` is true when the
    outcome is the leaning's, including a drop when the leaning was to leave it out.
    """
    found: dict[str, dict[str, Any]] = {}
    for slot in _list(seed.get("slots")):
        if not isinstance(slot, dict) or not _nonempty(slot.get("question")):
            continue
        group = slot.get("group") if _nonempty(slot.get("group")) else None
        key = f"group:{group}" if group else f"slot:{slot.get('id')}"
        if key in found:
            found[key]["slots"].append(slot.get("id"))
            continue
        options = [o for o in _list(slot.get("options")) if isinstance(o, dict)]
        leaning = next((i for i, o in enumerate(options) if o.get("leaning") is True), None)
        answer = slot.get("answer") if isinstance(slot.get("answer"), dict) else None
        choice = answer.get("choice") if answer else None
        if answer is None:
            match = None
        elif choice in (EDITED, DROPPED):
            match = choice
        else:
            match = "leaning" if choice == leaning else "other"
        leaned_out = leaning is not None and options[leaning].get("entry") is None
        rationale = slot.get("rationale") if isinstance(slot.get("rationale"), str) else ""
        found[key] = {
            "group": group, "slots": [slot.get("id")], "status": slot.get("status"),
            "question": slot["question"], "rationale": rationale,
            "options": [{"label": o.get("label"), "leaning": o.get("leaning") is True,
                         "entry": o.get("entry")} for o in options],
            "answer": answer, "match": match,
            "matched": None if answer is None else (
                match == "leaning" or (match == DROPPED and leaned_out)),
            "cites": sorted(set(RULE_ID.findall(rationale)), key=lambda c: (c[0], int(c[1:]))),
        }
    return list(found.values())


def church_list_issues(seed: dict[str, Any]) -> list[dict[str, Any]]:
    return [i for i in _list(seed.get("church_list_issues")) if isinstance(i, dict)]


def included_slots(seed: dict[str, Any]) -> list[dict[str, Any]]:
    """The settled slots the seed would load."""
    return [
        s for s in _list(seed.get("slots"))
        if isinstance(s, dict) and s.get("status") == SETTLED and s.get("decision") == INCLUDE
    ]


def paid_calls(seed: dict[str, Any]) -> int:
    """External model calls that were not served from a cache."""
    return sum(1 for c in _list(seed.get("calls")) if isinstance(c, dict) and not c.get("cached"))


def calls_cost(seed: dict[str, Any]) -> float:
    return sum(
        c["cost_usd"] for c in _list(seed.get("calls"))
        if isinstance(c, dict) and isinstance(c.get("cost_usd"), (int, float))
    )


def next_call_id(seed: dict[str, Any]) -> str:
    taken = {c.get("id") for c in _list(seed.get("calls"))
             if isinstance(c, dict) and isinstance(c.get("id"), str)}
    n = len(taken) + 1
    while f"c{n}" in taken:
        n += 1
    return f"c{n}"


def resolve_hash(seed: dict[str, Any], ref: Any) -> str | None:
    """The full content hash of the file's bulletin `ref` names (a hash or a unique prefix)."""
    if not isinstance(ref, str) or len(ref) < MIN_HASH_PREFIX:
        return None
    ref = ref.removesuffix("…").lower()
    hashes = [
        b["content_hash"] for b in _list(seed.get("bulletins"))
        if isinstance(b, dict) and isinstance(b.get("content_hash"), str)
        and b["content_hash"].startswith(ref)
    ]
    return hashes[0] if len(hashes) == 1 else None


def newest_read_bulletin(seed: dict[str, Any]) -> dict[str, Any] | None:
    """The newest bulletin the agent read: the one `as_of` names and `page` refers to."""
    read = [
        b for b in _list(seed.get("bulletins"))
        if isinstance(b, dict) and b.get("read") and isinstance(b.get("fetched_at"), str)
    ]
    return max(read, key=lambda b: normalize_as_of(b["fetched_at"]), default=None)


def seed_digest(seed: dict[str, Any]) -> str:
    """A digest of what loading the file writes: its included entries, pages and `as_of`.

    The loader records it in the seed revision's note, so an unchanged file is
    loaded once, and editing a rationale or a question does not load it again.
    A source seed's digest also covers its primary page, which the revision
    records; a bulletin seed's is what it always was.
    """
    entries = sorted(
        canonical_json({"entry": s["entry"], "page": s.get("page")}) for s in included_slots(seed)
    )
    as_of = seed.get("as_of")
    content: dict[str, Any] = {
        "as_of": normalize_as_of(as_of) if isinstance(as_of, str) else None,
        "entries": entries,
    }
    if is_source_seed(seed):
        primary = primary_capture(seed)
        content["source"] = primary.get("url") if primary else None
    return sha256_text(canonical_json(content))


def revision_note(seed: dict[str, Any]) -> str:
    """The note the loader writes on the seed revision it makes from this file."""
    return f"seed file {seed.get('parish_slug')} {seed_digest(seed)}"


# ── Validation ──────────────────────────────────────────────────────────────
def _keys(
    obj: dict[str, Any], expected: tuple[str, ...], where: str, optional: tuple[str, ...] = (),
) -> list[str]:
    errors = []
    missing = [k for k in expected if k not in obj]
    extra = sorted(k for k in obj if k not in expected and k not in optional)
    if missing:
        errors.append(f"{where}: missing {', '.join(missing)}")
    if extra:
        errors.append(f"{where}: unknown {', '.join(extra)}")
    return errors


def _is_time(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    try:
        normalize_as_of(value)
    except ValueError:
        return False
    return True


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_page(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _validate_bulletins(seed: dict[str, Any]) -> list[str]:
    bulletins = seed["bulletins"]
    if not isinstance(bulletins, list):
        return ["bulletins must be a list"]
    errors: list[str] = []
    seen: set[str] = set()
    for i, b in enumerate(bulletins):
        where = f"bulletins[{i}]"
        if not isinstance(b, dict):
            errors.append(f"{where} must be an object")
            continue
        key_errors = _keys(b, BULLETIN_KEYS, where)
        if key_errors:
            errors.extend(key_errors)
            continue
        if not is_valid_hash(b["content_hash"]):
            errors.append(f"{where}.content_hash must be a full SHA-256 hex digest")
        elif b["content_hash"] in seen:
            errors.append(f"{where}: bulletin {b['content_hash'][:12]} is listed twice")
        else:
            seen.add(b["content_hash"])
        if not _is_time(b["fetched_at"]):
            errors.append(f"{where}.fetched_at must be an ISO time")
        if b["published_date"] is not None and not isinstance(b["published_date"], str):
            errors.append(f"{where}.published_date must be null or YYYY-MM-DD")
        if not isinstance(b["read"], bool):
            errors.append(f"{where}.read must be true or false")
    return errors


def _validate_calls(seed: dict[str, Any]) -> list[str]:
    calls = seed["calls"]
    if not isinstance(calls, list):
        return ["calls must be a list"]
    errors: list[str] = []
    ids: set[str] = set()
    for i, call in enumerate(calls):
        where = f"calls[{i}]"
        if not isinstance(call, dict):
            errors.append(f"{where} must be an object")
            continue
        if not _nonempty(call.get("id")) or call["id"] in ids or call["id"] in SOURCE_KINDS:
            errors.append(f"{where}.id must be a unique id other than {', '.join(SOURCE_KINDS)}")
        else:
            ids.add(call["id"])
        if call.get("kind") not in CALL_KINDS:
            errors.append(f"{where}.kind must be one of {', '.join(CALL_KINDS)}")
        if not _nonempty(call.get("model")):
            errors.append(f"{where}.model is required")
        if resolve_hash(seed, call.get("bulletin")) is None:
            errors.append(f"{where}.bulletin must name one of the file's bulletins")
        if not isinstance(call.get("cached"), bool):
            errors.append(f"{where}.cached must be true or false")
        if call.get("kind") == ASK and not _nonempty(call.get("question")):
            errors.append(f"{where}.question is required for an ask")
    return errors


def _validate_answer(answer: Any, options: Any, where: str) -> list[str]:
    if not isinstance(answer, dict):
        return [f"{where} must be null or an object"]
    errors = _keys(answer, ("choice", "by", "at"), where)
    if errors:
        return errors
    choice = answer["choice"]
    n_options = len(options) if isinstance(options, list) else 0
    is_index = isinstance(choice, int) and not isinstance(choice, bool)
    if is_index and not 0 <= choice < n_options:
        errors.append(f"{where}.choice {choice} is not one of the options")
    elif not is_index and choice not in (EDITED, DROPPED):
        errors.append(f"{where}.choice must be an option's index, {EDITED} or {DROPPED}")
    if not _nonempty(answer["by"]):
        errors.append(f"{where}.by must name the reviewer")
    if not _is_time(answer["at"]):
        errors.append(f"{where}.at must be an ISO time")
    return errors


def _validate_options(options: Any, where: str) -> list[str]:
    if not isinstance(options, list) or len(options) < 2:
        return [f"{where} must be a list of at least two options"]
    errors: list[str] = []
    for j, option in enumerate(options):
        at = f"{where}[{j}]"
        if not isinstance(option, dict):
            errors.append(f"{at} must be an object")
            continue
        extra = sorted(set(option) - {"label", "entry", "leaning"})
        if extra:
            errors.append(f"{at}: unknown {', '.join(extra)}")
        if not _nonempty(option.get("label")):
            errors.append(f"{at}.label is required")
        if "entry" not in option:
            errors.append(f"{at}.entry is required (null for leaving the slot out)")
        elif option["entry"] is not None:
            errors.extend(validate_entry(option["entry"], f"{at}.entry"))
        if option.get("leaning", False) not in (True, False):
            errors.append(f"{at}.leaning must be true or false")
    if sum(1 for o in options if isinstance(o, dict) and o.get("leaning") is True) != 1:
        errors.append(f"{where}: exactly one option must be the one the agent leans to")
    return errors


def _validate_slot(seed: dict[str, Any], slot: Any, where: str, call_ids: set[str]) -> list[str]:
    if not isinstance(slot, dict):
        return [f"{where} must be an object"]
    errors = _keys(slot, SLOT_KEYS, where, OPTIONAL_SLOT_KEYS)
    if errors:
        return errors
    if not _nonempty(slot["id"]):
        errors.append(f"{where}.id is required")
    if slot.get("group") is not None and not _nonempty(slot["group"]):
        errors.append(f"{where}.group must be null or a name its question's other slots share")
    status = slot["status"]
    if status not in SLOT_STATUSES:
        errors.append(f"{where}.status must be one of {', '.join(SLOT_STATUSES)}")
    if slot["entry"] is not None:
        errors.extend(validate_entry(slot["entry"], f"{where}.entry"))
    if slot["page"] is not None and not _is_page(slot["page"]):
        errors.append(f"{where}.page must be null or a page number")
    if not _nonempty(slot["rationale"]):
        errors.append(f"{where}.rationale is required")
    if "weekly_omission" in slot:
        check = slot["weekly_omission"]
        at = f"{where}.weekly_omission"
        if not isinstance(check, dict):
            errors.append(f"{at} must be an object")
        else:
            errors.extend(_keys(check, ("bulletin", "reason"), at))
            if resolve_hash(seed, check.get("bulletin")) is None:
                errors.append(f"{at}.bulletin must name one of the file's bulletins")
            if not _nonempty(check.get("reason")):
                errors.append(f"{at}.reason must explain the agent's omission judgment")

    sources = slot["sources"]
    if is_source_seed(seed):
        errors.extend(_validate_source_slot(seed, slot, where))
    elif not isinstance(sources, list) or not sources:
        errors.append(f"{where}.sources must list at least one source")
    else:
        for j, source in enumerate(sources):
            at = f"{where}.sources[{j}]"
            if not isinstance(source, dict):
                errors.append(f"{at} must be an object")
                continue
            if "bulletins" in source:
                errors.append(f"{at}.bulletins is a drafting shorthand: `pnpm seed finalize` "
                              "splits it into one source per bulletin")
            extra = sorted(set(source) - {"source", "bulletin", "bulletins", "page", "said",
                                          "url", "schedule_check"})
            if extra:
                errors.append(f"{at}: unknown {', '.join(extra)}")
            name = source.get("source")
            if not isinstance(name, str) or (name not in SOURCE_KINDS and name not in call_ids):
                errors.append(f"{at}.source must be agent, history, website or a call's id")
            if name == WEBSITE:
                url = source.get("url")
                if not (isinstance(url, str) and url.startswith(("https://", "http://"))):
                    errors.append(f"{at}.url is required for a website source: the page read")
                if source.get("bulletin") is not None:
                    errors.append(f"{at}: a website source names no bulletin")
            elif source.get("url") is not None:
                errors.append(f"{at}.url is only for a website source")
            if "schedule_check" in source:
                check = source["schedule_check"]
                check_at = f"{at}.schedule_check"
                if name != WEBSITE:
                    errors.append(f"{check_at} is only for a website source")
                if not isinstance(check, dict):
                    errors.append(f"{check_at} must be an object")
                else:
                    errors.extend(_keys(check, (
                        "checked_at", "current_because", "bulletin", "fits_because",
                    ), check_at))
                    if not _is_time(check.get("checked_at")):
                        errors.append(f"{check_at}.checked_at must be an ISO time")
                    for key in ("current_because", "fits_because"):
                        if not _nonempty(check.get(key)):
                            errors.append(f"{check_at}.{key} must explain the agent's judgment")
                    if resolve_hash(seed, check.get("bulletin")) is None:
                        errors.append(f"{check_at}.bulletin must name one of the file's bulletins")
            if source.get("bulletin") is not None and resolve_hash(seed, source["bulletin"]) is None:
                errors.append(f"{at}.bulletin must name one of the file's bulletins")
            if source.get("page") is not None and not _is_page(source["page"]):
                errors.append(f"{at}.page must be null or a page number")
            if not _nonempty(source.get("said")):
                errors.append(f"{at}.said is required: what the source says")

    if status == SETTLED:
        if slot["decision"] not in DECISIONS:
            errors.append(f"{where}.decision must be include or exclude for a settled slot")
        if slot["entry"] is None and slot["decision"] != EXCLUDE:
            errors.append(f"{where}.entry is required for an included slot")
        if slot["answer"] is not None:
            errors.extend(_validate_answer(slot["answer"], slot["options"], f"{where}.answer"))
    elif status == NEEDS_HUMAN:
        if slot["decision"] is not None and slot["decision"] not in DECISIONS:
            errors.append(f"{where}.decision must be null, include or exclude")
        if not _nonempty(slot["question"]):
            errors.append(f"{where}.question is required for an open question")
        errors.extend(_validate_options(slot["options"], f"{where}.options"))
        if slot["answer"] is not None:
            errors.append(f"{where}.answer must be null while the question is open")
    if status == SETTLED and slot["options"] is not None and slot["answer"] is None:
        errors.extend(_validate_options(slot["options"], f"{where}.options"))
    return errors


def _validate_source_slot(seed: dict[str, Any], slot: dict[str, Any], where: str) -> list[str]:
    """A source seed's slot: no bulletin page, and every source quotes one of its captures."""
    errors: list[str] = []
    if slot["page"] is not None:
        errors.append(f"{where}.page must be null: a source seed has no bulletin")
    if "weekly_omission" in slot:
        errors.append(f"{where}.weekly_omission is for a bulletin seed")
    sources = slot["sources"]
    if not isinstance(sources, list) or not sources:
        return errors + [f"{where}.sources must list at least one capture it quotes"]
    for j, source in enumerate(sources):
        at = f"{where}.sources[{j}]"
        if not isinstance(source, dict):
            errors.append(f"{at} must be an object")
            continue
        extra = sorted(set(source) - {"source", "capture", "url", "said", "from_image"})
        if extra:
            errors.append(f"{at}: unknown {', '.join(extra)} (a source seed's source is a "
                          "capture: source, capture, url, said, from_image)")
        if source.get("source") not in CAPTURE_SOURCES:
            errors.append(f"{at}.source must be website or facebook: the capture's platform")
        capture = resolve_capture(seed, source.get("capture"))
        if capture is None:
            errors.append(f"{at}.capture must name one of the file's captures")
            continue
        if source.get("source") != capture.get("platform"):
            errors.append(f"{at}.source must be {capture.get('platform')}, its capture's platform")
        if source.get("url") != capture.get("url"):
            errors.append(f"{at}.url must be its capture's, {capture.get('url')}")
        if not _nonempty(source.get("said")):
            errors.append(f"{at}.said is required: what the page says, in its words")
        if "from_image" in source:
            if not capture.get("screenshot_hash"):
                errors.append(f"{at}.from_image needs a capture with a screenshot")
            elif not is_valid_hash(source["from_image"]):
                errors.append(f"{at}.from_image is the screenshot_hash of the screenshot it "
                              "was read from, or left out")
    return errors


def _validate_captures(seed: dict[str, Any]) -> list[str]:
    found = seed.get("captures")
    if not isinstance(found, list):
        return ["captures must be a list"]
    errors: list[str] = []
    seen: set[str] = set()
    for i, capture in enumerate(found):
        where = f"captures[{i}]"
        if not isinstance(capture, dict):
            errors.append(f"{where} must be an object")
            continue
        key_errors = _keys(capture, CAPTURE_KEYS, where)
        if key_errors:
            errors.extend(key_errors)
            continue
        if not is_valid_hash(capture["content_hash"]):
            errors.append(f"{where}.content_hash must be the SHA-256 of the capture's text")
        elif capture["content_hash"] in seen:
            errors.append(f"{where}: capture {capture['content_hash'][:12]} is listed twice")
        else:
            seen.add(capture["content_hash"])
        url = capture["url"]
        if not (isinstance(url, str) and url.startswith(("https://", "http://"))):
            errors.append(f"{where}.url must be the page's http(s) address")
        elif capture["platform"] != source_platform(url):
            errors.append(f"{where}.platform must be {source_platform(url)} for {url}")
        if capture["final_url"] is not None and not isinstance(capture["final_url"], str):
            errors.append(f"{where}.final_url must be null or the address the page ended at")
        if capture["platform"] not in SOURCE_PLATFORMS:
            errors.append(f"{where}.platform must be website or facebook")
        if not _is_time(capture["captured_at"]):
            errors.append(f"{where}.captured_at must be an ISO time")
        if capture["screenshot_hash"] is not None and not is_valid_hash(capture["screenshot_hash"]):
            errors.append(f"{where}.screenshot_hash must be null or a SHA-256 hex digest")
        if not isinstance(capture["primary"], bool):
            errors.append(f"{where}.primary must be true or false")
    if not errors and found and sum(1 for c in found if c["primary"]) != 1:
        errors.append("captures: exactly one must be primary, the page the site links")
    return errors


def _validate_kind(seed: dict[str, Any]) -> list[str]:
    """A source seed's own keys, or their absence from a bulletin seed."""
    kind = seed.get("kind", BULLETIN_SEED)
    if kind not in SEED_KINDS:
        return [f"kind must be one of {', '.join(SEED_KINDS)}"]
    if kind == BULLETIN_SEED:
        extra = [k for k in SOURCE_SEED_KEYS if k != "kind" and k in seed]
        return [f"{', '.join(extra)}: only a source seed has these"] if extra else []
    errors = _keys(seed, (*SEED_KEYS, *SOURCE_SEED_KEYS), "seed", OPTIONAL_SEED_KEYS)
    if errors:
        return errors
    if seed["bulletins"]:
        errors.append("bulletins must be empty: a source seed is drafted from captures")
    if seed["calls"]:
        errors.append("calls must be empty: a source seed makes no paid calls")
    if seed["current_because"] is not None and not isinstance(seed["current_because"], str):
        errors.append("current_because must be null or a string")
    if seed["recheck_after"] is not None and not is_iso_date(seed["recheck_after"]):
        errors.append("recheck_after must be null or YYYY-MM-DD")
    return errors + _validate_captures(seed)


def validate_seed(seed: Any, *, parish_slug: str | None = None) -> list[str]:
    """Every reason `seed` is not a well-formed seed file (empty when it is).

    This is the file's shape only; `checks.check_seed` adds what needs the
    database (churches, bulletins, slots).
    """
    if not isinstance(seed, dict):
        return ["seed must be a JSON object"]
    errors = _keys(seed, SEED_KEYS, "seed", OPTIONAL_SEED_KEYS)
    if errors:
        return errors
    if seed["schema_version"] != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not is_valid_slug(seed["parish_slug"]):
        errors.append("parish_slug is not a valid slug")
    elif parish_slug is not None and seed["parish_slug"] != parish_slug:
        errors.append(f"parish_slug must be {parish_slug}, the file's name")
    status = seed["status"]
    if status not in STATUSES:
        errors.append(f"status must be one of {', '.join(STATUSES)}")
    if seed["as_of"] is not None and not _is_time(seed["as_of"]):
        errors.append("as_of must be null or an ISO time")
    for key in ("drafted_by", "summary"):
        if not isinstance(seed[key], str):
            errors.append(f"{key} must be a string")
    for key in ("drafted_at", "approved_at"):
        if seed[key] is not None and not _is_time(seed[key]):
            errors.append(f"{key} must be null or an ISO time")
    for key in ("reviewer", "blocked_reason"):
        if seed[key] is not None and not isinstance(seed[key], str):
            errors.append(f"{key} must be null or a string")
    errors.extend(_validate_bulletins(seed))
    errors.extend(_validate_calls(seed))
    errors.extend(_validate_church_issues(seed))
    if not errors:
        errors.extend(_validate_kind(seed))
    if errors:
        return errors

    call_ids = {c["id"] for c in seed["calls"]}
    slots = seed["slots"]
    if not isinstance(slots, list):
        return errors + ["slots must be a list"]
    ids: set[str] = set()
    for i, slot in enumerate(slots):
        errors.extend(_validate_slot(seed, slot, f"slots[{i}]", call_ids))
        if isinstance(slot, dict) and _nonempty(slot.get("id")):
            if slot["id"] in ids:
                errors.append(f"slots[{i}].id {slot['id']} is used twice")
            ids.add(slot["id"])
    if errors:
        return errors
    errors = _group_errors(slots)
    if errors:
        return errors
    return status_errors(seed)


def _validate_church_issues(seed: dict[str, Any]) -> list[str]:
    issues = seed.get("church_list_issues")
    if issues is None:
        return []
    if not isinstance(issues, list):
        return ["church_list_issues must be a list"]
    errors: list[str] = []
    for i, issue in enumerate(issues):
        where = f"church_list_issues[{i}]"
        if not isinstance(issue, dict):
            errors.append(f"{where} must be an object")
            continue
        extra = sorted(set(issue) - set(CHURCH_ISSUE_KEYS))
        if extra:
            errors.append(f"{where}: unknown {', '.join(extra)}")
        if not _nonempty(issue.get("church")):
            errors.append(f"{where}.church is required: the church or chapel as the bulletin "
                          "names it")
        if not _nonempty(issue.get("said")):
            errors.append(f"{where}.said is required: what the bulletin holds there, in its "
                          "words")
        if issue.get("bulletin") is not None and resolve_hash(seed, issue["bulletin"]) is None:
            errors.append(f"{where}.bulletin must name one of the file's bulletins")
        if issue.get("page") is not None and not _is_page(issue["page"]):
            errors.append(f"{where}.page must be null or a page number")
    return errors


def slot_problems(seed: dict[str, Any], slot: Any, where: str) -> list[str]:
    """Every reason one slot is malformed, as `validate_seed` reports it (`seed slot`)."""
    call_ids = {c["id"] for c in _list(seed.get("calls"))
                if isinstance(c, dict) and isinstance(c.get("id"), str)}
    return _validate_slot(seed, slot, where, call_ids)


def church_issue_problems(seed: dict[str, Any]) -> list[str]:
    """`validate_seed`'s check of the file's `church_list_issues` (`seed church-issue`)."""
    return _validate_church_issues(seed)


def group_problems(slots: list[Any], groups: set[str]) -> list[str]:
    """`validate_seed`'s check that each of `groups` asks one question."""
    return _group_errors([s for s in slots if isinstance(s, dict)], groups)


def _group_errors(slots: list[dict[str, Any]], only: set[str] | None = None) -> list[str]:
    """A group's open slots are answered with one choice, so they ask the same question
    with the same option labels, in the same order, leaning the same way."""
    errors = []
    first: dict[str, dict[str, Any]] = {}
    for i, slot in enumerate(slots):
        group = slot.get("group")
        if not group or slot.get("status") != NEEDS_HUMAN or (only is not None
                                                              and group not in only):
            continue
        lead = first.setdefault(group, slot)
        if lead is slot:
            continue

        def shape(s: dict[str, Any]) -> list[tuple[Any, bool, bool]]:
            return [(o.get("label"), o.get("leaning") is True, o.get("entry") is None)
                    for o in s["options"]]

        if slot["question"] != lead["question"] or shape(slot) != shape(lead):
            errors.append(
                f"slots[{i}] ({slot['id']}) is in group {group!r} with {lead['id']} but asks a "
                "different question: a group shares its question, its option labels (in order, "
                "with the same leaning) and which options leave the slot out"
            )
    return errors


def status_errors(seed: dict[str, Any]) -> list[str]:
    """What the parish's status says that the rest of the file contradicts."""
    status = seed["status"]
    n_open = len(open_questions(seed))
    errors = []
    if status in (NEEDS_REVIEW, READY, APPROVED) and seed["as_of"] is None:
        errors.append(f"as_of is required once the draft is {status}")
    if status in (NEEDS_REVIEW, READY) and not _nonempty(seed["summary"]):
        errors.append("summary is required once the draft is done: what a reviewer reads first")
    if status == NEEDS_REVIEW and not n_open:
        errors.append("status is needs_review but no question is open: it is ready")
    if status in (READY, APPROVED) and n_open:
        errors.append(f"status is {status} but {n_open} questions are still open")
    if status == APPROVED and not (_nonempty(seed["reviewer"]) and seed["approved_at"]):
        errors.append("an approved seed names its reviewer and approved_at")
    if status != APPROVED and seed["approved_at"] is not None:
        errors.append("approved_at is only set on an approved seed")
    if status == BLOCKED and not _nonempty(seed["blocked_reason"]):
        errors.append("a blocked seed says why in blocked_reason")
    if is_source_seed(seed) and status in (NEEDS_REVIEW, READY, APPROVED):
        if not captures(seed):
            errors.append("a source seed lists the pages it read: `pnpm seed capture`")
        if not _nonempty(seed.get("current_because")):
            errors.append("current_because is required once the draft is done: why the "
                          "schedule looks current (`pnpm seed current`)")
        recheck = seed.get("recheck_after")
        if recheck is None:
            errors.append("recheck_after is required once the draft is done: when to read "
                          "the pages again")
        elif isinstance(seed["as_of"], str) and recheck <= normalize_as_of(seed["as_of"])[:10]:
            errors.append(f"recheck_after ({recheck}) must be after as_of")
    return errors


def status_after_review(seed: dict[str, Any]) -> str:
    """The status a reviewed draft has: needs_review while questions are open, else ready."""
    return NEEDS_REVIEW if open_questions(seed) else READY


@dataclass(frozen=True)
class SeedSummary:
    """One seed file at a glance, for `seed status` and the labeler's queue."""

    parish_slug: str
    status: str
    open_questions: int
    slots: int
    included: int
    calls: int
    cost_usd: float
    as_of: str | None
    reviewer: str | None
    summary: str
    blocked_reason: str | None
    church_list_issues: int = 0
    problem: str | None = None
    kind: str = BULLETIN_SEED

    @classmethod
    def of(cls, slug: str, seed: dict[str, Any] | None, problem: str | None = None):
        seed = seed if isinstance(seed, dict) else {}
        slots = [s for s in _list(seed.get("slots")) if isinstance(s, dict)]
        return cls(
            parish_slug=slug,
            status=seed.get("status") if seed.get("status") in STATUSES else "invalid",
            open_questions=question_count(seed),
            slots=len(slots),
            included=len(included_slots(seed)),
            calls=len(_list(seed.get("calls"))),
            cost_usd=round(calls_cost(seed), 4),
            as_of=seed.get("as_of") if isinstance(seed.get("as_of"), str) else None,
            reviewer=seed.get("reviewer") if isinstance(seed.get("reviewer"), str) else None,
            summary=seed.get("summary") if isinstance(seed.get("summary"), str) else "",
            blocked_reason=seed.get("blocked_reason")
            if isinstance(seed.get("blocked_reason"), str) else None,
            church_list_issues=len(church_list_issues(seed)),
            problem=problem,
            kind=seed_kind(seed) if seed_kind(seed) in SEED_KINDS else "invalid",
        )
