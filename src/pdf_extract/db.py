"""Create and populate the database from schema.sql and data files."""

from __future__ import annotations

import csv
import logging
from pathlib import Path

from pdf_extract.schedule_pattern import (
    NO_SEASON,
    normalize_season,
    normalize_weeks_of_month,
    weeks_of_month_to_text,
)
from pdf_extract.storage import (
    BULLETINS_METADATA_PATH,
    CHURCHES_CSV_PATH,
    DEFAULT_DB_PATH,
    EVENTS_PATH,
    PARISHES_CSV_PATH,
    SCHEMA_PATH,
    connect_db,
    delete_db,
    load_json_list,
    utc_now_iso,
)
from pdf_extract.timeparse import normalize_event_date, time_to_minutes

LOGGER = logging.getLogger(__name__)


def _validate_csv_headers(
    fieldnames: list[str] | None, required: set[str], filename: str,
) -> None:
    """Raise ValueError if required CSV columns are missing."""
    if fieldnames is None:
        raise ValueError(f"{filename}: CSV file is empty or has no header row")
    missing = required - set(fieldnames)
    if missing:
        raise ValueError(f"{filename}: missing required columns: {sorted(missing)}")


def create_db(db_path: Path = DEFAULT_DB_PATH) -> dict[str, int]:
    """Drop and recreate the database from schema + data files.

    Each load step is idempotent and skipped if its source file is missing.
    """
    LOGGER.info("Creating database at %s", db_path)
    delete_db(db_path)
    conn = connect_db(db_path)
    try:
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        LOGGER.info("Schema created")

        stats: dict[str, int] = {}

        # Load order follows the foreign keys: parishes, then the bulletins and
        # churches that reference them, then the events that reference both.
        stats["parishes"] = _load_parishes(conn)
        stats["bulletins"] = _load_bulletins(conn)
        stats["churches"] = _load_churches(conn)
        stats["events"] = _load_events(conn)

        conn.commit()
        LOGGER.info("Database created: %s", stats)
        return stats
    finally:
        conn.close()


def _load_parishes(conn) -> int:
    if not PARISHES_CSV_PATH.exists():
        LOGGER.info("No parishes.csv found, skipping parish load")
        return 0
    count = 0
    now = utc_now_iso()
    with open(PARISHES_CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _validate_csv_headers(reader.fieldnames, {"slug", "name", "website"}, "parishes.csv")
        for row in reader:
            bp = (row.get("bulletin_provider") or "").strip() or None
            pid = (row.get("provider_id") or "").strip() or None
            conn.execute(
                """INSERT OR IGNORE INTO parish(
                    slug, name, homepage_url, bulletin_provider, provider_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)""",
                (row["slug"], row["name"], row["website"], bp, pid, now),
            )
            count += 1
    LOGGER.info("Loaded %d parishes from parishes.csv", count)
    return count


def _load_bulletins(conn) -> int:
    entries = load_json_list(BULLETINS_METADATA_PATH)
    if not entries:
        LOGGER.info("No bulletins/metadata.json found, skipping")
        return 0

    count = 0
    for entry in entries:
        parish_row = conn.execute("SELECT id FROM parish WHERE slug = ?", (entry["parish_slug"],)).fetchone()
        if not parish_row:
            continue
        cursor = conn.execute(
            """INSERT OR IGNORE INTO bulletin(parish_id, source_url, pdf_path, published_date, fetched_at, processed_at, content_hash)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                parish_row["id"],
                entry["source_url"],
                entry.get("pdf_path"),
                entry.get("published_date"),
                entry.get("fetched_at"),
                entry.get("processed_at"),
                entry.get("content_hash"),
            ),
        )
        if cursor.rowcount > 0:
            count += 1

    LOGGER.info("Loaded %d bulletins from metadata.json", count)
    return count


def _csv_bool(value: str | None) -> int:
    """Map a CSV boolean (true/false/empty) to an integer (1/0/0)."""
    return 1 if (value or "").strip().lower() == "true" else 0


def _csv_float(value: str | None) -> float | None:
    """Parse a CSV float value, returning None for empty/missing."""
    raw = (value or "").strip()
    if not raw:
        return None
    return float(raw)


def _load_churches(conn) -> int:
    """Insert churches from churches.csv into the database."""
    if not CHURCHES_CSV_PATH.exists():
        LOGGER.info("No churches.csv found, skipping")
        return 0

    now = utc_now_iso()
    count = 0
    with open(CHURCHES_CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _validate_csv_headers(
            reader.fieldnames,
            {"parish_id", "slug", "name", "line1", "city", "state", "postal_code"},
            "churches.csv",
        )
        for row in reader:
            parish_row = conn.execute(
                "SELECT id FROM parish WHERE slug = ?", (row["parish_id"],)
            ).fetchone()
            if not parish_row:
                continue
            lat = _csv_float(row.get("latitude"))
            lng = _csv_float(row.get("longitude"))
            cursor = conn.execute(
                """INSERT OR IGNORE INTO church(
                    parish_id, slug, name, address_line1, address_line2, city, state, postal_code,
                    name_verified, address_verified, latitude, longitude, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    parish_row["id"],
                    row["slug"],
                    row["name"],
                    row.get("line1") or None,
                    row.get("line2") or None,
                    row.get("city") or None,
                    row.get("state") or None,
                    row.get("postal_code") or None,
                    _csv_bool(row.get("name_verified")),
                    _csv_bool(row.get("address_verified")),
                    lat,
                    lng,
                    now,
                ),
            )
            if cursor.rowcount > 0:
                count += 1
    LOGGER.info("Loaded %d churches from churches.csv", count)
    return count


def _load_events(conn) -> int:
    entries = load_json_list(EVENTS_PATH)
    if not entries:
        LOGGER.info("No events.json found, skipping")
        return 0

    count = 0
    for entry in entries:
        church_slug = entry.get("church_slug")
        if not church_slug:
            continue
        church_row = conn.execute(
            "SELECT id, parish_id FROM church WHERE slug = ?", (church_slug,)
        ).fetchone()
        if not church_row:
            continue

        # Resolve bulletin_id if we can find it
        bulletin_id = None
        bulletin_row = conn.execute(
            "SELECT id FROM bulletin WHERE parish_id = ? AND source_url = ?",
            (church_row["parish_id"], entry.get("bulletin_source_url")),
        ).fetchone()
        if bulletin_row:
            bulletin_id = bulletin_row["id"]

        start_minutes = time_to_minutes(entry.get("start_time"))
        if start_minutes is None:
            LOGGER.warning(
                "Skipping event: unparseable start_time %r (church=%s)",
                entry.get("start_time"), church_slug,
            )
            continue

        end_minutes = time_to_minutes(entry.get("end_time"))

        page_number = entry.get("page_number")
        if not isinstance(page_number, int):
            page_number = None

        note_raw = entry.get("note")
        note = note_raw.strip() if isinstance(note_raw, str) and note_raw.strip() else None

        # Only a weekly slot recurs, so only a weekly slot can be qualified by
        # which weeks of the month it falls on or which part of the year it runs.
        event_kind = entry.get("event_kind", "")
        if event_kind == "weekly":
            weeks_of_month = weeks_of_month_to_text(
                normalize_weeks_of_month(entry.get("weeks_of_month"))
            )
            season = normalize_season(
                entry.get("season_start_month"),
                entry.get("season_start_day"),
                entry.get("season_end_month"),
                entry.get("season_end_day"),
            )
        else:
            weeks_of_month, season = None, NO_SEASON

        event_date = None
        if event_kind == "specific_date":
            event_date = normalize_event_date(entry.get("date"))
            if event_date is None:
                LOGGER.warning(
                    "Skipping event: unparseable specific_date %r (church=%s)",
                    entry.get("date"), church_slug,
                )
                continue

        conn.execute(
            """INSERT INTO event(church_id, bulletin_id, event_type, event_kind, day_of_week, date, start_time, end_time, cancelled, page_number, note, weeks_of_month, season_start_month, season_start_day, season_end_month, season_end_day)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                church_row["id"],
                bulletin_id,
                entry.get("event_type", ""),
                event_kind,
                entry.get("day_of_week"),
                event_date,
                start_minutes,
                end_minutes,
                int(entry.get("cancelled", False)),
                page_number,
                note,
                weeks_of_month,
                season.start_month,
                season.start_day,
                season.end_month,
                season.end_day,
            ),
        )

        count += 1

    LOGGER.info("Loaded %d events from events.json", count)
    return count
