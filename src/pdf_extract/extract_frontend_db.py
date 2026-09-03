"""Extract a minimal SQLite database snapshot for the frontend from parish_events.db.

Only the church and event tables are copied, with columns stripped down to what
the web app actually needs. The SQLite output is gzip-compressed and written to
apps/web/public/frontend.snapshot so Vite can serve it as an opaque static asset.
"""

from __future__ import annotations

import gzip
import logging
import sqlite3
import tempfile
from pathlib import Path

from pdf_extract.storage import configure_sqlite_connection

LOGGER = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DB = ROOT / "data" / "parish_events.db"
DEST_DB = ROOT / "apps" / "web" / "public" / "frontend.snapshot"
FRONTEND_SCHEMA_PATH = ROOT / "data" / "frontend_schema.sql"

# Columns of the frontend_schema.sql tables, in the order the SELECTs below
# produce them. Named rather than positional so a column added to the schema
# fails loudly here instead of silently shifting every value one place over.
_CHURCH_COLUMNS = (
    "id, parish_id, slug, name, address_line1, address_line2, city, state,"
    " postal_code, latitude, longitude, homepage_url, bulletin_url"
)
_EVENT_COLUMNS = (
    "id, church_id, event_type, event_kind, day_of_week, date, start_time,"
    " end_time, cancelled, page_number, note"
)


def _latest_bulletin_order(alias: str = "") -> str:
    """ORDER BY that puts a parish's current bulletin first.

    Most recently published, then most recently fetched, then most recently
    processed, with the highest id as a deterministic tie-break. Both queries
    below rank by it — church.bulletin_url has to name the same bulletin the
    copied events came from — and process.py mirrors it in Python as
    `_frontend_bulletin_rank` to decide what events.json may compact away.
    """
    col = f"{alias}." if alias else ""
    return (
        f"COALESCE({col}published_date, '') DESC,"
        f" COALESCE({col}fetched_at, '') DESC,"
        f" COALESCE({col}processed_at, '') DESC,"
        f" {col}id DESC"
    )


def _insert_all(
    conn: sqlite3.Connection, table: str, columns: str, rows: list[tuple]
) -> None:
    placeholders = ", ".join("?" * (columns.count(",") + 1))
    conn.executemany(f"INSERT INTO {table}({columns}) VALUES ({placeholders})", rows)


def extract(source: Path = SOURCE_DB, dest: Path = DEST_DB) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source database not found: {source}")

    dest.parent.mkdir(parents=True, exist_ok=True)
    previous_dest = dest.with_name(f"{dest.name}.previous")
    if dest.exists():
        previous_dest.unlink(missing_ok=True)
        dest.replace(previous_dest)
    legacy_dest = dest.with_suffix(".db")
    legacy_dest.unlink(missing_ok=True)

    temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    temp_path = Path(temp_file.name)
    temp_file.close()

    src = sqlite3.connect(source)
    configure_sqlite_connection(src)
    dst = sqlite3.connect(temp_path)
    dst.execute("PRAGMA journal_mode=DELETE")
    dst.execute("PRAGMA foreign_keys = ON")
    try:
        dst.executescript(FRONTEND_SCHEMA_PATH.read_text(encoding="utf-8"))

        churches = src.execute(
            f"""
            SELECT c.id, c.parish_id, c.slug, c.name, c.address_line1, c.address_line2,
                   c.city, c.state, c.postal_code, c.latitude, c.longitude,
                   p.homepage_url,
                   (SELECT b.source_url FROM bulletin b
                    WHERE b.parish_id = c.parish_id AND b.source_url IS NOT NULL
                    ORDER BY {_latest_bulletin_order("b")}
                    LIMIT 1)
            FROM church c
            LEFT JOIN parish p ON c.parish_id = p.id
            """
        ).fetchall()
        _insert_all(dst, "church", _CHURCH_COLUMNS, churches)

        events = src.execute(
            f"""
            SELECT e.id, e.church_id, e.event_type, e.event_kind,
                   e.day_of_week, e.date, e.start_time, e.end_time, e.cancelled,
                   e.page_number, e.note
            FROM event e
            INNER JOIN bulletin b ON e.bulletin_id = b.id
            INNER JOIN (
                SELECT parish_id, id,
                       ROW_NUMBER() OVER (
                           PARTITION BY parish_id
                           ORDER BY {_latest_bulletin_order()}
                       ) AS rn
                FROM bulletin
            ) latest ON b.parish_id = latest.parish_id AND b.id = latest.id AND latest.rn = 1
            """
        ).fetchall()
        _insert_all(dst, "event", _EVENT_COLUMNS, events)

        dst.commit()
        dst.execute("VACUUM")

        church_count = dst.execute("SELECT count(*) FROM church").fetchone()[0]
        event_count = dst.execute("SELECT count(*) FROM event").fetchone()[0]
    finally:
        src.close()
        dst.close()

    raw_size_kb = temp_path.stat().st_size / 1024
    with temp_path.open("rb") as raw, dest.open("wb") as out:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=out, compresslevel=9, mtime=0
        ) as compressed:
            compressed.write(raw.read())
    temp_path.unlink(missing_ok=True)

    compressed_size_kb = dest.stat().st_size / 1024
    LOGGER.info(
        "frontend.snapshot: %d churches, %d events, %.1f KB compressed from %.1f KB",
        church_count,
        event_count,
        compressed_size_kb,
        raw_size_kb,
    )


if __name__ == "__main__":
    extract()
