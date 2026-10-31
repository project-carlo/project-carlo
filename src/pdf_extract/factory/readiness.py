"""Which mapped parishes are ready to seed, and when a seed Run starts (§11).

A parish from a merged map Run is ready once the database has at least 2 of its
bulletins. Only parishes promoted with a bulletin source count, and not one waiting on a
collector (`fetch_gap`): it counts once the gap is cleared on main. The first seed Run
starts once 80% are ready; a follow-up seeds the rest once they are all ready. 6 weeks
after the map Run merged, whatever is ready is seeded (even short of 80%, for the first
Run), and each parish still not ready gets an issue.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path

from pdf_extract.factory.config import Config
from pdf_extract.factory.ledger import ACTIVE, BLOCKED, MAP, MERGED, PENDING, SEED, Ledger
from pdf_extract.factory.plan import fetch_gaps_on_main, seedable_on_main


def bulletin_counts(db_path: Path, parishes: list[str]) -> dict[str, int]:
    if not parishes or not db_path.exists():
        return {}
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        marks = ",".join("?" * len(parishes))
        rows = conn.execute(
            f"SELECT p.slug, COUNT(DISTINCT b.content_hash) FROM parish p "
            f"JOIN bulletin b ON b.parish_id = p.id WHERE p.slug IN ({marks}) GROUP BY p.slug",
            parishes).fetchall()
    finally:
        conn.close()
    return {slug: n for slug, n in rows}


@dataclass
class Readiness:
    diocese: str
    seedable: list[str]
    seeding: list[str]  # already in a seed Run
    ready: list[str]
    not_ready: list[str]
    start: list[str] = field(default_factory=list)  # parishes for a new seed Run
    overdue: list[str] = field(default_factory=list)  # still not ready after the wait
    fetch_gaps: list[str] = field(default_factory=list)  # waiting on a collector, not counted


def assess(ledger: Ledger, config: Config, diocese: str, db_path: Path,
           at: datetime | None = None, *, repo: Path) -> Readiness | None:
    """`repo` is the dispatcher's checkout: the mapped parishes are read from its main."""
    at = at or datetime.now(UTC)
    maps = [r for r in ledger.runs(MERGED) if r["diocese"] == diocese and r["kind"] == MAP]
    if not maps:
        return None
    seedable = sorted(seedable_on_main(repo, config.upstream, diocese))
    seed_runs = [r for r in ledger.runs() if r["diocese"] == diocese and r["kind"] == SEED]
    seeding = sorted({p for r in seed_runs for p in json.loads(r["parishes"] or "[]")})
    remaining = [p for p in seedable if p not in seeding]
    counts = bulletin_counts(db_path, remaining)
    ready = [p for p in remaining if counts.get(p, 0) >= config.seed_ready_bulletins]
    not_ready = [p for p in remaining if p not in ready]
    gaps = sorted(set(fetch_gaps_on_main(repo, config.upstream, diocese)) - set(seeding))
    result = Readiness(diocese, seedable, seeding, ready, not_ready, fetch_gaps=gaps)
    if not remaining or any(r["status"] in (ACTIVE, BLOCKED, PENDING) for r in seed_runs):
        return result
    merged = [datetime.fromisoformat(r["merged_at"]) for r in maps if r["merged_at"]]
    waited = bool(merged) and at >= min(merged) + timedelta(weeks=config.seed_follow_up_weeks)
    if not seed_runs and not waited:
        if seedable and len(ready) >= config.seed_first_run_share * len(seedable):
            result.start = ready
        return result
    if not not_ready or waited:
        result.start = ready
        result.overdue = not_ready if waited else []
    return result


def dioceses_to_check(ledger: Ledger) -> list[str]:
    return sorted({r["diocese"] for r in ledger.runs(MERGED) if r["kind"] == MAP})
