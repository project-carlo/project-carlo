"""Load approved seed files into the database as `seed` revisions.

The published database is only written by the pipeline, so seeds reach it the
way `parishes.csv` does: pipeline commands load the approved files in
`data/seeds/` after re-seeding parishes and churches from the CSVs
(docs/seeding-plan.md, "Loading seeds").

- Each file is loaded once per digest of its included entries, pages and
  `as_of` (`files.seed_digest`), which the revision's note carries.
- A file the parish already has a seed for is loaded again only when its
  `as_of` is later than the latest seed's, so re-loading it can't undo what
  update mode has applied since.
- A file that fails its checks is skipped and reported; the rest load.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Any

from pdf_extract.schedule.entries import parse_entry
from pdf_extract.schedule.store import (
    normalize_as_of,
    parish_churches,
    update_mode_parishes,
    write_seed,
)
from pdf_extract.seeding.checks import check_seed
from pdf_extract.seeding.files import (
    APPROVED,
    SEEDS_DIR,
    SeedFileError,
    included_slots,
    newest_read_bulletin,
    read_seed,
    revision_note,
    seed_slugs,
)

LOGGER = logging.getLogger(__name__)


def is_loaded(conn: sqlite3.Connection, parish_id: int, seed: dict[str, Any]) -> bool:
    """Whether a seed revision of the parish was made from exactly this file's content."""
    return conn.execute(
        """SELECT 1 FROM schedule_revision
           WHERE parish_id = ? AND source_kind = 'seed' AND note = ? LIMIT 1""",
        (parish_id, revision_note(seed)),
    ).fetchone() is not None


def _bulletin_id(conn: sqlite3.Connection, parish_id: int, content_hash: str) -> int | None:
    row = conn.execute(
        """SELECT id FROM bulletin WHERE parish_id = ? AND content_hash = ?
           ORDER BY fetched_at DESC, id DESC LIMIT 1""",
        (parish_id, content_hash),
    ).fetchone()
    return None if row is None else int(row[0])


def load_seed(
    conn: sqlite3.Connection, seed: dict[str, Any], parish_id: int, *, run_id: str | None = None,
) -> dict[str, Any]:
    """Write an approved, checked seed as a seed revision. Returns what was loaded.

    Sightings are written for the newest bulletin read, at each included slot's
    page; a slot with no page isn't printed there and gets none.
    """
    churches = parish_churches(conn, parish_id)
    slots = included_slots(seed)
    entries = [parse_entry(slot["entry"], churches) for slot in slots]
    newest = newest_read_bulletin(seed)
    bulletin_id = None if newest is None else _bulletin_id(conn, parish_id, newest["content_hash"])
    sightings = [] if bulletin_id is None else [
        (bulletin_id, entry, slot["page"])
        for slot, entry in zip(slots, entries) if slot["page"] is not None
    ]
    with conn:
        revision = write_seed(
            conn, parish_id, entries,
            as_of=seed["as_of"], actor=seed["reviewer"], note=revision_note(seed),
            run_id=run_id, sightings=sightings,
        )
    return {
        "parish": seed["parish_slug"],
        "revision": revision,
        "entries": len(entries),
        "sightings": len(sightings),
        "as_of": normalize_as_of(seed["as_of"]),
        "reviewer": seed["reviewer"],
    }


def load_approved_seeds(
    conn: sqlite3.Connection, seeds_dir: Path = SEEDS_DIR, *, run_id: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Load every approved seed file not loaded yet. Returns what loaded and what was skipped."""
    loaded: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    latest_seeds: dict[int, str] | None = None
    for slug in seed_slugs(seeds_dir):
        try:
            seed = read_seed(slug, seeds_dir)
        except SeedFileError as exc:
            skipped.append({"parish": slug, "reason": str(exc)})
            continue
        if not isinstance(seed, dict) or seed.get("status") != APPROVED:
            continue
        problems = check_seed(conn, seed, parish_slug=slug, check_bulletins=False)
        if problems:
            skipped.append({"parish": slug, "reason": "; ".join(problems[:3])})
            continue
        parish_id = int(conn.execute(
            "SELECT id FROM parish WHERE slug = ?", (slug,),
        ).fetchone()[0])
        if is_loaded(conn, parish_id, seed):
            continue
        if latest_seeds is None:
            latest_seeds = update_mode_parishes(conn)
        latest = latest_seeds.get(parish_id)
        if latest is not None and normalize_as_of(seed["as_of"]) <= latest:
            skipped.append({
                "parish": slug,
                "reason": f"changed, but its as_of ({seed['as_of']}) is not later than the "
                f"parish's latest seed ({latest}): re-loading it would undo what update mode "
                "has applied since",
            })
            continue
        try:
            result = load_seed(conn, seed, parish_id, run_id=run_id)
        except ValueError as exc:
            skipped.append({"parish": slug, "reason": str(exc)})
            continue
        latest_seeds[parish_id] = result["as_of"]
        LOGGER.info("Loaded seed for %s as revision %s", slug, result["revision"])
        loaded.append(result)
    for item in skipped:
        LOGGER.warning("Seed file for %s not loaded: %s", item["parish"], item["reason"])
    return {"loaded": loaded, "skipped": skipped}
