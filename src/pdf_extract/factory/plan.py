"""Which job a Run needs next. The stage order is here, in code (§3).

Map Run:  survey, survey-review, map × each batch (integrate whenever *New lessons*
          passes the threshold), reconcile, promote, pr.
Seed Run: for each batch, seed × each parish, then seed-review; then pr.
Follow-up Runs (parked parishes answered after the PR opened) start with their jobs
queued, then go map → promote → pr, or seed → seed-review → pr.

A queued job (a send-back, a parked parish answered) always comes first.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pdf_extract.dioceses.records import NO_BULLETIN, parse_file
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


def seedable_parishes(worktree: Path, diocese: str) -> list[str]:
    """Parishes the map Run promoted with a bulletin source; excluded and open ones never."""
    return [slug for slug, r in parish_records(worktree, diocese).items()
            if r.get("bulletin_provider") and r.get("bulletin_provider") != NO_BULLETIN]


def seedable_on_main(repo: Path, ref: str, diocese: str) -> list[str]:
    """`seedable_parishes` as main (`ref`) has them, since a merged Run's worktree is gone."""
    with tempfile.TemporaryDirectory() as tmp:
        folder = diocese_dir(Path(tmp), diocese) / "parishes"
        folder.mkdir(parents=True)
        for name, text in git.read_folder(
                repo, ref, f"data/dioceses/{diocese}/parishes").items():
            if name.endswith(".md"):
                (folder / name).write_text(text, encoding="utf-8")
        return seedable_parishes(Path(tmp), diocese)


def seed_batches(worktree: Path, diocese: str, parishes: list[str]) -> list[tuple[str, list[str]]]:
    """The map Run's batches as parish slugs, keeping only `parishes`; the rest last."""
    records = parish_records(worktree, diocese)
    wanted = [p for p in parishes]
    placed: set[str] = set()
    out = []
    for batch in ordered_batches(worktree, diocese):
        entries = set(batch.get("entries") or [])
        slugs = [p for p in wanted if p not in placed
                 and entries & set(records.get(p, {}).get("roster") or [])]
        placed.update(slugs)
        if slugs:
            out.append((batch["id"], slugs))
    rest = [p for p in wanted if p not in placed]
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


def next_job(ledger: Ledger, run: Any, *, lessons_before_integrate: int) -> Next | None:
    """The Run's next job, or None when it has nothing left (its PR is open)."""
    if run["kind"] == MAP:
        return _next_map(ledger, run, lessons_before_integrate)
    return _next_seed(ledger, run)


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
        meta = diocese_dir(worktree, diocese) / "diocese.md"
        if (meta.exists() and len(playbook.bullets(meta, playbook.NEW_LESSONS)) > threshold
                and (last is None or last["stage"] != "integrate")):
            return Next("integrate", {})
        mapped = {json.loads(j["input"]).get("batch") for j in _done(ledger, run_id, "map")}
        for batch in ordered_batches(worktree, diocese):
            if batch["id"] not in mapped:
                return Next("map", {"batch": batch["id"]})
        if not _done(ledger, run_id, "reconcile"):
            return Next("reconcile", {})
    if not _done(ledger, run_id, "promote"):
        return Next("promote", {})
    if not _done(ledger, run_id, "pr"):
        return Next("pr", {})
    return None


def _next_seed(ledger: Ledger, run: Any) -> Next | None:
    worktree, run_id = Path(run["worktree"]), run["id"]
    parishes = json.loads(run["parishes"] or "[]")
    parked = _parked_subjects(ledger, run_id)
    seeds = ledger.jobs(run_id, "seed")
    verdicts = {}
    for row in ledger.all("SELECT v.* FROM verdict v JOIN job j ON j.id = v.job_id "
                          "WHERE j.run_id = ? ORDER BY v.id", run_id):
        verdicts[row["subject"]] = row
    for batch, slugs in seed_batches(worktree, run["diocese"], parishes):
        pending_review = []
        redrafted = []
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
                if seen is not None:
                    redrafted.append(parish)
        if pending_review:
            return Next("seed-review", {"batch": batch, "parishes": pending_review,
                                        "redrafted": redrafted})
    if not _done(ledger, run_id, "pr"):
        return Next("pr", {})
    return None
