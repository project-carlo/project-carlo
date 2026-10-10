"""The seed file: one parish's drafted schedule, committed as `data/seeds/<parish>.json`.

A seed file holds every slot an agent drafted for a parish, what each source
said about it, what it decided and why, and the questions it left for a
person (docs/seeding-plan.md, "The seed file"). This module reads, writes and
checks the file's shape; `checks` checks it against the database, and
`loader` turns an approved one into a `seed` revision.

Entries are in the labels' event shape without `page_number`, `origin` and
`optional` (`labels.ENTRY_KEYS`), with 24-hour `HH:MM` times, so they are what
`pnpm schedule seed` reads and can be scored against the labels as they are.
"""

from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pdf_extract.labeling.labels import is_valid_hash, is_valid_slug, validate_entry
from pdf_extract.paths import DATA_DIR
from pdf_extract.schedule.store import canonical_json, normalize_as_of, sha256_text
from pdf_extract.storage import utc_now_iso

SCHEMA_VERSION = 1
SEEDS_DIR = DATA_DIR / "seeds"
# Test runs on the labeled parishes (`seed pick --labeled --eval RUN`): drafts
# under `<run>/seeds/`, never loaded, and the run's manifest and score beside them.
SEED_EVALS_DIR = DATA_DIR / "seed-evals"
# Where `seed pdf` and `seed pages` put the files they make (gitignored).
WORK_DIR = DATA_DIR / "seed-work"

DRAFTED_BY = "claude-code/seed-parishes"

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
# events, or the id of one of the file's `calls`.
AGENT = "agent"
HISTORY = "history"

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


# ── Reading a file ──────────────────────────────────────────────────────────
def open_questions(seed: dict[str, Any]) -> list[dict[str, Any]]:
    return [s for s in seed.get("slots") or [] if isinstance(s, dict)
            and s.get("status") == NEEDS_HUMAN]


def included_slots(seed: dict[str, Any]) -> list[dict[str, Any]]:
    """The settled slots the seed would load."""
    return [
        s for s in seed.get("slots") or []
        if isinstance(s, dict) and s.get("status") == SETTLED and s.get("decision") == INCLUDE
    ]


def paid_calls(seed: dict[str, Any]) -> int:
    """External model calls that were not served from a cache."""
    return sum(1 for c in seed.get("calls") or [] if isinstance(c, dict) and not c.get("cached"))


def calls_cost(seed: dict[str, Any]) -> float:
    return sum(
        c["cost_usd"] for c in seed.get("calls") or []
        if isinstance(c, dict) and isinstance(c.get("cost_usd"), (int, float))
    )


def next_call_id(seed: dict[str, Any]) -> str:
    taken = {c.get("id") for c in seed.get("calls") or [] if isinstance(c, dict)}
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
        b["content_hash"] for b in seed.get("bulletins") or []
        if isinstance(b, dict) and isinstance(b.get("content_hash"), str)
        and b["content_hash"].startswith(ref)
    ]
    return hashes[0] if len(hashes) == 1 else None


def newest_read_bulletin(seed: dict[str, Any]) -> dict[str, Any] | None:
    """The newest bulletin the agent read: the one `as_of` names and `page` refers to."""
    read = [
        b for b in seed.get("bulletins") or []
        if isinstance(b, dict) and b.get("read") and isinstance(b.get("fetched_at"), str)
    ]
    return max(read, key=lambda b: normalize_as_of(b["fetched_at"]), default=None)


def seed_digest(seed: dict[str, Any]) -> str:
    """A digest of what loading the file writes: its included entries, pages and `as_of`.

    The loader records it in the seed revision's note, so an unchanged file is
    loaded once, and editing a rationale or a question does not load it again.
    """
    entries = sorted(
        canonical_json({"entry": s["entry"], "page": s.get("page")}) for s in included_slots(seed)
    )
    as_of = seed.get("as_of")
    return sha256_text(canonical_json({
        "as_of": normalize_as_of(as_of) if isinstance(as_of, str) else None,
        "entries": entries,
    }))


def revision_note(seed: dict[str, Any]) -> str:
    """The note the loader writes on the seed revision it makes from this file."""
    return f"seed file {seed.get('parish_slug')} {seed_digest(seed)}"


# ── Validation ──────────────────────────────────────────────────────────────
def _keys(obj: dict[str, Any], expected: tuple[str, ...], where: str) -> list[str]:
    errors = []
    missing = [k for k in expected if k not in obj]
    extra = sorted(k for k in obj if k not in expected)
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
        if not _nonempty(call.get("id")) or call["id"] in ids or call["id"] in (AGENT, HISTORY):
            errors.append(f"{where}.id must be a unique id other than agent and history")
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
    errors = _keys(slot, SLOT_KEYS, where)
    if errors:
        return errors
    if not _nonempty(slot["id"]):
        errors.append(f"{where}.id is required")
    status = slot["status"]
    if status not in SLOT_STATUSES:
        errors.append(f"{where}.status must be one of {', '.join(SLOT_STATUSES)}")
    if slot["entry"] is not None:
        errors.extend(validate_entry(slot["entry"], f"{where}.entry"))
    if slot["page"] is not None and not _is_page(slot["page"]):
        errors.append(f"{where}.page must be null or a page number")
    if not _nonempty(slot["rationale"]):
        errors.append(f"{where}.rationale is required")

    sources = slot["sources"]
    if not isinstance(sources, list) or not sources:
        errors.append(f"{where}.sources must list at least one source")
    else:
        for j, source in enumerate(sources):
            at = f"{where}.sources[{j}]"
            if not isinstance(source, dict):
                errors.append(f"{at} must be an object")
                continue
            extra = sorted(set(source) - {"source", "bulletin", "page", "said"})
            if extra:
                errors.append(f"{at}: unknown {', '.join(extra)}")
            name = source.get("source")
            if name not in (AGENT, HISTORY) and name not in call_ids:
                errors.append(f"{at}.source must be agent, history or a call's id")
            if source.get("bulletin") is not None and resolve_hash(seed, source["bulletin"]) is None:
                errors.append(f"{at}.bulletin must name one of the file's bulletins")
            if source.get("page") is not None and not _is_page(source["page"]):
                errors.append(f"{at}.page must be null or a page number")
            if not _nonempty(source.get("said")):
                errors.append(f"{at}.said is required: what the source says")

    if status == SETTLED:
        if slot["decision"] not in DECISIONS:
            errors.append(f"{where}.decision must be include or exclude for a settled slot")
        if slot["entry"] is None:
            errors.append(f"{where}.entry is required for a settled slot")
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


def validate_seed(seed: Any, *, parish_slug: str | None = None) -> list[str]:
    """Every reason `seed` is not a well-formed seed file (empty when it is).

    This is the file's shape only; `checks.check_seed` adds what needs the
    database (churches, bulletins, slots).
    """
    if not isinstance(seed, dict):
        return ["seed must be a JSON object"]
    errors = _keys(seed, SEED_KEYS, "seed")
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
    return status_errors(seed)


def status_errors(seed: dict[str, Any]) -> list[str]:
    """What the parish's status says that the rest of the file contradicts."""
    status = seed["status"]
    n_open = len(open_questions(seed))
    errors = []
    if status in (NEEDS_REVIEW, READY, APPROVED) and seed["as_of"] is None:
        errors.append(f"as_of is required once the draft is {status}")
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
    problem: str | None = None

    @classmethod
    def of(cls, slug: str, seed: dict[str, Any] | None, problem: str | None = None):
        seed = seed or {}
        slots = [s for s in seed.get("slots") or [] if isinstance(s, dict)]
        return cls(
            parish_slug=slug,
            status=seed.get("status") if seed.get("status") in STATUSES else "invalid",
            open_questions=len(open_questions(seed)),
            slots=len(slots),
            included=len(included_slots(seed)),
            calls=len(seed.get("calls") or []),
            cost_usd=round(calls_cost(seed), 4),
            as_of=seed.get("as_of") if isinstance(seed.get("as_of"), str) else None,
            reviewer=seed.get("reviewer") if isinstance(seed.get("reviewer"), str) else None,
            summary=seed.get("summary") if isinstance(seed.get("summary"), str) else "",
            blocked_reason=seed.get("blocked_reason")
            if isinstance(seed.get("blocked_reason"), str) else None,
            problem=problem,
        )
