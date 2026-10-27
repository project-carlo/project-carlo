"""The pipeline database: migrations and reference-data seeding.

`data/parish_events.db` is the source of truth for everything the pipeline
observes (bulletins, events, recurrence history, run records). It is not
rebuilt: it is pulled from the published copy (`pnpm data:pull`), changed in
place by pipeline commands, and published back by the weekly job.

Two tables are the exception. `parish` and `church` are curated by hand in
`data/parishes.csv` and `data/churches.csv`, reviewed in pull requests, and
seeded into the database (matched by slug) before every pipeline command, so
an edited CSV takes effect on the next command.
"""

from __future__ import annotations

import csv
import logging
import runpy
import sqlite3
from pathlib import Path
from typing import Any

from pdf_extract.schedule.store import DELETE, REFERENCE, Change, append_revision
from pdf_extract.seeding.files import SEEDS_DIR
from pdf_extract.seeding.loader import load_approved_seeds
from pdf_extract.storage import (
    CHURCHES_CSV_PATH,
    DEFAULT_DB_PATH,
    MIGRATIONS_DIR,
    PARISHES_CSV_PATH,
    connect_db,
    delete_db,
    utc_now_iso,
)

LOGGER = logging.getLogger(__name__)


class DatabaseMissingError(FileNotFoundError):
    pass


# ── Migrations ──────────────────────────────────────────────────────────────
def _migration_files(migrations_dir: Path = MIGRATIONS_DIR) -> list[tuple[int, Path]]:
    files: list[tuple[int, Path]] = []
    for path in sorted(p for p in migrations_dir.iterdir() if p.suffix in (".sql", ".py")):
        prefix = path.name.split("_", 1)[0]
        if not prefix.isdigit():
            raise ValueError(f"Migration file name must start with a number: {path.name}")
        files.append((int(prefix), path))
    numbers = [n for n, _ in files]
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"Migrations must be numbered 1..N without gaps, found {numbers}")
    return files


def schema_version(conn: sqlite3.Connection) -> int:
    return int(conn.execute("PRAGMA user_version").fetchone()[0])


def migrate(conn: sqlite3.Connection, migrations_dir: Path = MIGRATIONS_DIR) -> int:
    """Apply migrations newer than the database's user_version. Returns how many ran.

    Each migration runs in its own transaction together with the version bump,
    so a failure leaves the database at the previous version. Foreign keys are
    off while migrations run, so a migration can rebuild a table the way SQLite
    requires (create, copy, drop, rename) without the drop cascading; they are
    checked before each migration commits.
    """
    current = schema_version(conn)
    files = _migration_files(migrations_dir)
    if current > len(files):
        raise RuntimeError(
            f"Database is at schema version {current} but this checkout only knows "
            f"{len(files)} migrations; pull the latest code."
        )
    applied = 0
    foreign_keys = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    # The pragma is a no-op inside a transaction, so it is set around them.
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        for number, path in files:
            if number <= current:
                continue
            LOGGER.info("Applying migration %s", path.name)
            # executescript would commit on its own; wrap it so the version bump
            # is part of the same transaction as the migration's statements.
            try:
                if path.suffix == ".sql":
                    conn.executescript("BEGIN;\n" + path.read_text(encoding="utf-8"))
                else:
                    conn.execute("BEGIN")
                    runpy.run_path(str(path))["migrate"](conn)
                conn.execute(f"PRAGMA user_version = {number}")
                violations = conn.execute("PRAGMA foreign_key_check").fetchall()
                if violations:
                    raise RuntimeError(
                        f"Migration {path.name} leaves {len(violations)} foreign key "
                        f"violations, e.g. {tuple(violations[0])}"
                    )
            except BaseException:
                if conn.in_transaction:
                    conn.rollback()
                raise
            conn.commit()
            applied += 1
    finally:
        conn.execute(f"PRAGMA foreign_keys = {'ON' if foreign_keys else 'OFF'}")
    return applied


# ── Reference data from CSV ─────────────────────────────────────────────────
def _validate_csv_headers(
    fieldnames: list[str] | None, required: set[str], filename: str,
) -> None:
    """Raise ValueError if required CSV columns are missing."""
    if fieldnames is None:
        raise ValueError(f"{filename}: CSV file is empty or has no header row")
    missing = required - set(fieldnames)
    if missing:
        raise ValueError(f"{filename}: missing required columns: {sorted(missing)}")


def _csv_bool(value: str | None) -> int:
    """Map a CSV boolean (true/false/empty) to an integer (1/0/0)."""
    return 1 if (value or "").strip().lower() == "true" else 0


def _csv_float(value: str | None) -> float | None:
    """Parse a CSV float value, returning None for empty/missing."""
    raw = (value or "").strip()
    if not raw:
        return None
    return float(raw)


def _read_csv(path: Path, required: set[str]) -> list[dict[str, str]]:
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _validate_csv_headers(reader.fieldnames, required, path.name)
        return list(reader)


def seed_reference_data(
    conn: sqlite3.Connection,
    *,
    parishes_csv: Path = PARISHES_CSV_PATH,
    churches_csv: Path = CHURCHES_CSV_PATH,
) -> dict[str, int]:
    """Make the parish and church tables match the CSVs, matching rows by slug.

    Rows are updated in place so their ids, and everything that references
    them, survive. A parish or church removed from its CSV is deleted along
    with its bulletins and events; the previous published database still holds
    them if that was a mistake.

    A church is different once it has believed-schedule entries, since its
    parish's change log points at them and is never rewritten
    (docs/schedule-state-plan.md, "Churches leaving the CSV"). When such a
    church leaves the CSV or names another parish, its live entries are
    deleted from its old parish's schedule by a `reference` revision; one that
    leaves is retired (`retired_at`) rather than deleted, and comes back with
    its id if it returns to the CSV.
    """
    stats = {
        "parishes_upserted": 0,
        "parishes_deleted": 0,
        "churches_upserted": 0,
        "churches_deleted": 0,
        "churches_retired": 0,
        "churches_skipped": 0,
        "schedule_entries_removed": 0,
    }
    now = utc_now_iso()

    # A missing CSV must not read as "every parish was removed": that would
    # delete the whole database's bulletins and events by cascade.
    for path in (parishes_csv, churches_csv):
        if not path.exists():
            raise FileNotFoundError(
                f"{path} not found; run commands from the repository root"
            )
    parish_rows = _read_csv(parishes_csv, {"slug", "name", "website"})
    church_rows = _read_csv(
        churches_csv,
        {"parish_id", "slug", "name", "line1", "city", "state", "postal_code"},
    )

    with conn:
        parish_slugs = set()
        for row in parish_rows:
            slug = row["slug"].strip()
            parish_slugs.add(slug)
            conn.execute(
                """INSERT INTO parish(
                       slug, name, homepage_url, bulletin_provider, provider_id, fetch_only,
                       created_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(slug) DO UPDATE SET
                       name = excluded.name,
                       homepage_url = excluded.homepage_url,
                       bulletin_provider = excluded.bulletin_provider,
                       provider_id = excluded.provider_id,
                       fetch_only = excluded.fetch_only""",
                (
                    slug,
                    row["name"],
                    row["website"],
                    (row.get("bulletin_provider") or "").strip() or None,
                    (row.get("provider_id") or "").strip() or None,
                    _csv_bool(row.get("fetch_only")),
                    now,
                ),
            )
            stats["parishes_upserted"] += 1

        # Before the churches, so a removed parish's churches are skipped as
        # orphans rather than upserted and then deleted by the cascade.
        for parish in conn.execute("SELECT id, slug FROM parish").fetchall():
            if parish["slug"] not in parish_slugs:
                LOGGER.warning("Parish %s is no longer in parishes.csv; deleting", parish["slug"])
                stats["churches_retired"] += keep_churches_other_parishes_reference(
                    conn, parish["id"], now,
                )
                conn.execute("DELETE FROM parish WHERE id = ?", (parish["id"],))
                stats["parishes_deleted"] += 1

        existing = {
            r["slug"]: r for r in conn.execute(
                "SELECT id, slug, parish_id, retired_at FROM church"
            ).fetchall()
        }
        church_slugs = set()
        for row in church_rows:
            parish = conn.execute(
                "SELECT id FROM parish WHERE slug = ?", (row["parish_id"],)
            ).fetchone()
            if parish is None:
                LOGGER.warning(
                    "churches.csv: church %s names unknown parish %s; skipping",
                    row["slug"], row["parish_id"],
                )
                stats["churches_skipped"] += 1
                continue
            church_slugs.add(row["slug"])
            old = existing.get(row["slug"])
            if old is not None and old["parish_id"] != parish["id"]:
                stats["schedule_entries_removed"] += remove_church_entries(
                    conn, old["id"], old["parish_id"], reason="moved to another parish",
                )
            conn.execute(
                """INSERT INTO church(
                       parish_id, slug, name, address_line1, address_line2, city, state,
                       postal_code, name_verified, address_verified, latitude, longitude,
                       created_at
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(slug) DO UPDATE SET
                       parish_id = excluded.parish_id,
                       name = excluded.name,
                       address_line1 = excluded.address_line1,
                       address_line2 = excluded.address_line2,
                       city = excluded.city,
                       state = excluded.state,
                       postal_code = excluded.postal_code,
                       name_verified = excluded.name_verified,
                       address_verified = excluded.address_verified,
                       latitude = excluded.latitude,
                       longitude = excluded.longitude,
                       retired_at = NULL""",
                (
                    parish["id"],
                    row["slug"],
                    row["name"],
                    row.get("line1") or None,
                    row.get("line2") or None,
                    row.get("city") or None,
                    row.get("state") or None,
                    row.get("postal_code") or None,
                    _csv_bool(row.get("name_verified")),
                    _csv_bool(row.get("address_verified")),
                    _csv_float(row.get("latitude")),
                    _csv_float(row.get("longitude")),
                    now,
                ),
            )
            stats["churches_upserted"] += 1

        for church in conn.execute(
            "SELECT id, slug, parish_id, retired_at FROM church"
        ).fetchall():
            if church["slug"] in church_slugs:
                continue
            stats["schedule_entries_removed"] += remove_church_entries(
                conn, church["id"], church["parish_id"], reason="left churches.csv",
            )
            has_entries = conn.execute(
                "SELECT 1 FROM schedule_entry WHERE church_id = ? LIMIT 1", (church["id"],)
            ).fetchone()
            if has_entries is None:
                LOGGER.warning("Church %s is no longer in churches.csv; deleting", church["slug"])
                conn.execute("DELETE FROM church WHERE id = ?", (church["id"],))
                stats["churches_deleted"] += 1
            elif church["retired_at"] is None:
                LOGGER.warning(
                    "Church %s is no longer in churches.csv; retiring it (its schedule "
                    "entries stay in the log)", church["slug"],
                )
                conn.execute(
                    "UPDATE church SET retired_at = ? WHERE id = ?", (now, church["id"]),
                )
                stats["churches_retired"] += 1

    return stats


def keep_churches_other_parishes_reference(
    conn: sqlite3.Connection, parish_id: int, now: str,
) -> int:
    """Before a parish is deleted, move out the churches another parish's log still names.

    A church that moved to this parish keeps its entries in its old parish's
    log, proposals and sightings, which are never rewritten. Deleting this
    parish would delete the church and its entries by cascade, under those
    rows. Such a church is instead moved back to (the lowest-id) parish that
    references it and retired there; it comes back if churches.csv lists it
    again. Returns how many churches were kept.
    """
    rows = conn.execute(
        """SELECT c.id AS church_id, MIN(ref.parish_id) AS parish_id
           FROM church c
           JOIN schedule_entry e ON e.church_id = c.id
           JOIN (
               SELECT parish_id, before_entry_id AS entry_id FROM schedule_change
               UNION ALL SELECT parish_id, after_entry_id FROM schedule_change
               UNION ALL SELECT l.parish_id, p.entry_id FROM proposed_change p
                   JOIN llm_call l ON l.id = p.llm_call_id
               UNION ALL SELECT b.parish_id, s.entry_id FROM entry_sighting s
                   JOIN bulletin b ON b.id = s.bulletin_id
           ) ref ON ref.entry_id = e.id
           WHERE c.parish_id = ? AND ref.parish_id != ?
           GROUP BY c.id""",
        (parish_id, parish_id),
    ).fetchall()
    for row in rows:
        LOGGER.warning(
            "Church %s is still named by parish %s's schedule log; moving it there, retired",
            row["church_id"], row["parish_id"],
        )
        conn.execute(
            "UPDATE church SET parish_id = ?, retired_at = COALESCE(retired_at, ?) WHERE id = ?",
            (row["parish_id"], now, row["church_id"]),
        )
    return len(rows)


def remove_church_entries(
    conn: sqlite3.Connection, church_id: int, parish_id: int, *, reason: str,
) -> int:
    """Delete a church's live entries from its parish's schedule with one `reference` revision.

    Returns how many entries were removed (0, and no revision, when it had none).
    """
    rows = conn.execute(
        """SELECT s.entry_id FROM current_schedule s
           JOIN schedule_entry e ON e.id = s.entry_id
           WHERE s.parish_id = ? AND e.church_id = ? ORDER BY s.entry_id""",
        (parish_id, church_id),
    ).fetchall()
    if not rows:
        return 0
    append_revision(
        conn, parish_id, source_kind=REFERENCE,
        changes=[Change(DELETE, before_entry_id=row["entry_id"]) for row in rows],
        actor="churches.csv", note=f"church {church_id} {reason}",
    )
    return len(rows)


# ── Opening the database ────────────────────────────────────────────────────
def create_db(db_path: Path = DEFAULT_DB_PATH) -> dict[str, Any]:
    """Create an empty database: schema plus reference data, no observed data.

    For tests and starting from scratch. To work on real data, pull the
    published database instead (`pnpm data:pull`).
    """
    LOGGER.info("Creating empty database at %s", db_path)
    delete_db(db_path)
    conn = connect_db(db_path)
    try:
        migrations = migrate(conn)
        seeded = seed_reference_data(conn)
    finally:
        conn.close()
    return {"db_path": str(db_path), "migrations_applied": migrations, **seeded}


def ensure_db(
    db_path: Path = DEFAULT_DB_PATH,
    *,
    load_seeds: bool = True,
    seeds_dir: Path = SEEDS_DIR,
) -> dict[str, Any]:
    """Bring an existing database up to date before a pipeline command runs.

    Applies pending migrations, re-seeds the reference tables from the CSVs,
    and loads the approved seed files not loaded yet (`seeding.loader`; the
    result is under `seeds`). Refuses to invent a database: running the
    pipeline against an empty one would look like every parish had lost its
    schedule.

    `load_seeds` off leaves the seed files for later: the weekly run loads
    them after taking its before-copy, so its change checks see them.
    """
    if not db_path.exists():
        raise DatabaseMissingError(
            f"No database at {db_path}. Run `pnpm data:pull` to download the published "
            "data, or `pnpm db:create` to start from an empty database."
        )
    conn = connect_db(db_path)
    try:
        migrations = migrate(conn)
        seeded = seed_reference_data(conn)
        result: dict[str, Any] = {"migrations_applied": migrations, **seeded}
        if load_seeds:
            result["seeds"] = load_approved_seeds(conn, seeds_dir)
    finally:
        conn.close()
    return result


def load_seeds(
    db_path: Path = DEFAULT_DB_PATH, *, seeds_dir: Path = SEEDS_DIR, run_id: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Load the approved seed files into the database at `db_path` (see `ensure_db`)."""
    conn = connect_db(db_path)
    try:
        return load_approved_seeds(conn, seeds_dir, run_id=run_id)
    finally:
        conn.close()
