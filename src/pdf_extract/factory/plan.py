"""Which job a Run needs next. The stage order is here, in code.

Map Run:  survey, survey-review, map × each batch (integrate whenever *New lessons*
          passes the threshold, and once more after the last batch if any wait),
          reconcile, promote, pr.
Seed Run: seed × each parish, a batch at a time, then seed-review of the parishes drafted
          since the last one: after the first batch, once they hold
          seed_review_questions open questions, after a redraft, and after the last
          batch; then pr.
Follow-up Runs (parked parishes answered after the PR opened) start with their jobs
queued, then go map → promote → pr, or seed → seed-review → pr.

A queued job (a send-back, a parked parish answered) always comes first.
"""

from __future__ import annotations

import json
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pdf_extract.dioceses.records import (
    CHURCH,
    EXCLUDED,
    NO_BULLETIN_PROVIDERS,
    OFF_SITE_PROVIDERS,
    OPEN,
    UNSUPPORTED,
    parse_file,
)
from pdf_extract.factory import git, playbook
from pdf_extract.factory.handoff import APPROVE
from pdf_extract.factory.ledger import DONE, MAP, Ledger
from pdf_extract.seeding import files

OTHER_BATCH = "(no batch)"


@dataclass
class Next:
    stage: str
    inputs: dict[str, Any]


def diocese_dir(worktree: Path, diocese: str) -> Path:
    return worktree / "data" / "dioceses" / diocese


def ordered_batches(worktree: Path, diocese: str) -> list[dict[str, Any]]:
    """The survey's batches, `first_batch` first, then in file order."""
    path = diocese_dir(worktree, diocese) / "batches.json"
    if not path.exists():
        return []
    plan = json.loads(path.read_text(encoding="utf-8"))
    batches = list(plan.get("batches") or [])
    first = plan.get("first_batch")
    batches.sort(key=lambda b: b.get("id") != first)
    return batches


def roster_entry(worktree: Path, diocese: str, ref: str) -> dict[str, Any]:
    name, _, entry_id = ref.partition(":")
    path = diocese_dir(worktree, diocese) / "rosters" / f"{name}.json"
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))["entries"]
    except (OSError, ValueError, KeyError):
        return {}
    return next((e for e in entries if str(e.get("id")) == entry_id), {})


def describe_entry(worktree: Path, diocese: str, ref: str) -> str:
    e = roster_entry(worktree, diocese, ref)
    where = ", ".join(str(e[k]) for k in ("city", "state") if e.get(k))
    return f"{ref} {e.get('name', '?')}" + (f" ({where})" if where else "")


def parish_records(worktree: Path, diocese: str) -> dict[str, dict[str, Any]]:
    out = {}
    for path in sorted((diocese_dir(worktree, diocese) / "parishes").glob("*.md")):
        front, _ = parse_file(path)
        out[path.stem] = front
    return out


def _with_source(worktree: Path, diocese: str) -> dict[str, dict[str, Any]]:
    return {slug: r for slug, r in parish_records(worktree, diocese).items()
            if r.get("bulletin_provider")
            and r.get("bulletin_provider") not in NO_BULLETIN_PROVIDERS}


def seedable_parishes(worktree: Path, diocese: str) -> list[str]:
    """Parishes the map Run promoted with a bulletin source; excluded and open ones never,
    nor one whose bulletin `fetch` can't collect yet (`unsupported`, or a `fetch_gap`): it
    has no bulletins to seed from until its collector lands, its provider is set and the
    gap is cleared. A `website_schedule` parish has no bulletin to wait for: its source
    seed is drafted outside seed Runs (docs/source-schedules-plan.md)."""
    return [slug for slug, r in _with_source(worktree, diocese).items()
            if not r.get("fetch_gap") and r.get("bulletin_provider") not in OFF_SITE_PROVIDERS]


def fetch_gap_parishes(worktree: Path, diocese: str) -> list[str]:
    """Parishes with a bulletin that wait on a collector (`unsupported` or `fetch_gap`)."""
    return [slug for slug, r in _with_source(worktree, diocese).items()
            if r.get("fetch_gap") or r.get("bulletin_provider") == UNSUPPORTED]


def _on_main(repo: Path, ref: str, diocese: str,
             read: Callable[[Path, str], list[str]]) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        folder = diocese_dir(Path(tmp), diocese) / "parishes"
        folder.mkdir(parents=True)
        for name, text in git.read_folder(
                repo, ref, f"data/dioceses/{diocese}/parishes").items():
            if name.endswith(".md"):
                (folder / name).write_text(text, encoding="utf-8")
        return read(Path(tmp), diocese)


def seedable_on_main(repo: Path, ref: str, diocese: str) -> list[str]:
    """`seedable_parishes` as main (`ref`) has them, since a merged Run's worktree is gone."""
    return _on_main(repo, ref, diocese, seedable_parishes)


def fetch_gaps_on_main(repo: Path, ref: str, diocese: str) -> list[str]:
    """`fetch_gap_parishes` as main (`ref`) has them."""
    return _on_main(repo, ref, diocese, fetch_gap_parishes)


def parish_roster_refs(worktree: Path, diocese: str) -> tuple[dict[str, set[str]],
                                                               dict[str, set[str]]]:
    """Each parish's roster refs: its churches' (and any on the parish record itself),
    then, apart, those of the excluded and open records that name it as their `parish`."""
    own: dict[str, set[str]] = {}
    for slug, r in parish_records(worktree, diocese).items():
        own.setdefault(slug, set()).update(r.get("roster") or [])
    linked: dict[str, set[str]] = {}
    for kind, into in ((CHURCH, own), (EXCLUDED, linked), (OPEN, linked)):
        for path in sorted((diocese_dir(worktree, diocese) / kind.dir).glob("*.md")):
            front, _ = parse_file(path)
            if front.get("parish"):
                into.setdefault(front["parish"], set()).update(front.get("roster") or [])
    return own, linked


def seed_batches(worktree: Path, diocese: str, parishes: list[str]) -> list[tuple[str, list[str]]]:
    """The map Run's batches as parish slugs, keeping only `parishes`; the rest last.

    A parish goes to the first batch holding one of its churches' roster refs. One whose
    churches are in no batch falls back to the refs of its excluded and open records."""
    own, linked = parish_roster_refs(worktree, diocese)
    batches = [(b["id"], set(b.get("entries") or [])) for b in ordered_batches(worktree, diocese)]
    wanted = list(parishes)
    where: dict[str, str] = {}
    for refs in (own, linked):
        for batch_id, entries in batches:
            for p in wanted:
                if p not in where and entries & refs.get(p, set()):
                    where[p] = batch_id
    out = [(batch_id, slugs) for batch_id, _ in batches
           if (slugs := [p for p in wanted if where.get(p) == batch_id])]
    rest = [p for p in wanted if p not in where]
    if rest:
        out.append((OTHER_BATCH, rest))
    return out


def _done(ledger: Ledger, run_id: str, stage: str) -> list[Any]:
    return [j for j in ledger.jobs(run_id, stage) if j["status"] == DONE]


def _handoff(job: Any) -> dict[str, Any]:
    return json.loads(job["handoff"] or "{}")


def read_seed(worktree: Path, parish: str) -> dict[str, Any] | None:
    """The parish's seed file in the worktree; None when it is missing or unreadable."""
    try:
        return files.read_seed(parish, worktree / "data" / "seeds")
    except files.SeedFileError:
        return None


def seed_status(worktree: Path, parish: str) -> str | None:
    seed = read_seed(worktree, parish)
    return seed.get("status") if seed else None


def open_questions(worktree: Path, parish: str) -> int:
    """The questions a reviewer answers in the parish's seed, as `pnpm seed status` counts."""
    seed = read_seed(worktree, parish)
    return files.question_count(seed) if seed else 0


def chunk_label(batches: list[str]) -> str:
    """A seed-review's batches in a few words: `b3`, or `b3 +2 more`."""
    return batches[0] + (f" +{len(batches) - 1} more" if len(batches) > 1 else "")


def next_job(ledger: Ledger, run: Any, *, lessons_before_integrate: int,
             seed_review_questions: int) -> Next | None:
    """The Run's next job, or None when it has nothing left (its PR is open)."""
    if run["kind"] == MAP:
        return _next_map(ledger, run, lessons_before_integrate)
    return _next_seed(ledger, run, seed_review_questions)


def _parked_subjects(ledger: Ledger, run_id: str) -> set[str]:
    return {f["subject"] for f in ledger.parked(run_id)}


def _next_map(ledger: Ledger, run: Any, threshold: int) -> Next | None:
    worktree, diocese, run_id = Path(run["worktree"]), run["diocese"], run["id"]
    jobs = ledger.jobs(run_id)
    last = next((j for j in reversed(jobs) if j["status"] == DONE), None)
    if run["follow_up_of"] is None:
        surveys = _done(ledger, run_id, "survey")
        if not surveys:
            return Next("survey", {})
        approved = [j for j in _done(ledger, run_id, "survey-review")
                    if _handoff(j).get("verdict") == APPROVE]
        if not approved or approved[-1]["finished_at"] < surveys[-1]["finished_at"]:
            return Next("survey-review", {"survey_job": surveys[-1]["id"]})
        mapped = {json.loads(j["input"]).get("batch") for j in _done(ledger, run_id, "map")}
        unmapped = [b["id"] for b in ordered_batches(worktree, diocese) if b["id"] not in mapped]
        reconciled = bool(_done(ledger, run_id, "reconcile"))
        meta = diocese_dir(worktree, diocese) / "diocese.md"
        lessons = len(playbook.bullets(meta, playbook.NEW_LESSONS)) if meta.exists() else 0
        # Past the threshold, and once more before reconcile, so the playbook the PR
        # carries has every lesson folded in. Never twice in a row, so lessons an
        # integrate left can't loop it.
        due = lessons > threshold or (lessons > 0 and not unmapped and not reconciled)
        if due and (last is None or last["stage"] != "integrate"):
            return Next("integrate", {})
        if unmapped:
            return Next("map", {"batch": unmapped[0]})
        if not reconciled:
            return Next("reconcile", {})
    if not _done(ledger, run_id, "promote"):
        return Next("promote", {})
    if not _done(ledger, run_id, "pr"):
        return Next("pr", {})
    return None


def _next_seed(ledger: Ledger, run: Any, review_questions: int) -> Next | None:
    """Seeds a batch at a time, in plan order. The parishes drafted and not reviewed since
    go to seed-review together at the end of a batch: the first batch on its own, so the
    diocese has precedents early; then once they hold `review_questions` open questions;
    at once when one is a redraft; and whatever is left once nothing is left to draft.
    Everything is read again each time, so a restarted dispatcher decides the same."""
    worktree, run_id = Path(run["worktree"]), run["id"]
    parishes = json.loads(run["parishes"] or "[]")
    parked = _parked_subjects(ledger, run_id)
    seeds = ledger.jobs(run_id, "seed")
    verdicts = {}
    for row in ledger.all("SELECT v.* FROM verdict v JOIN job j ON j.id = v.job_id "
                          "WHERE j.run_id = ? ORDER BY v.id", run_id):
        verdicts[row["subject"]] = row
    chunk: list[str] = []
    pending_review: list[str] = []
    redrafted: list[str] = []
    questions = 0
    for n, (batch, slugs) in enumerate(seed_batches(worktree, run["diocese"], parishes)):
        waiting = len(pending_review)
        for parish in slugs:
            if parish in parked or seed_status(worktree, parish) == "approved":
                continue
            mine = [j for j in seeds if json.loads(j["input"]).get("parish") == parish]
            if not mine:
                return Next("seed", {"parish": parish, "batch": batch})
            job = mine[-1]
            if job["status"] != DONE:
                continue
            seen = verdicts.get(parish)
            if seen is None or seen["at"] <= job["finished_at"]:
                pending_review.append(parish)
                questions += open_questions(worktree, parish)
                if seen is not None:
                    redrafted.append(parish)
        if len(pending_review) > waiting:
            chunk.append(batch)
        if pending_review and (n == 0 or redrafted or questions >= review_questions):
            break
    if pending_review:
        return Next("seed-review", {"batch": chunk_label(chunk), "batches": chunk,
                                    "parishes": pending_review, "redrafted": redrafted})
    if not _done(ledger, run_id, "pr"):
        return Next("pr", {})
    return None
