"""SQLite storage helpers and shared data paths."""

from __future__ import annotations

import json
import logging
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pdf_extract.address import format_address
from pdf_extract.blobstore import bulletin_pdf_key, get_store
from pdf_extract.paths import DATA_DIR, ROOT
from pdf_extract.pdf_truncate import ensure_truncated_pdf
from pdf_extract.timeparse import minutes_to_time, normalize_event_date, time_to_minutes

LOGGER = logging.getLogger(__name__)

# ── Data paths ──────────────────────────────────────────────────────────────
DEFAULT_DB_PATH = DATA_DIR / "parish_events.db"
MIGRATIONS_DIR = ROOT / "data" / "migrations"
PARISHES_CSV_PATH = DATA_DIR / "parishes.csv"
CHURCHES_CSV_PATH = DATA_DIR / "churches.csv"
DETECT_RESULTS_PATH = DATA_DIR / "detect_results.json"
VERIFY_RESULTS_PATH = DATA_DIR / "verify_results.json"
GEOCODE_RESULTS_PATH = DATA_DIR / "geocode_results.json"
# Dioceses still being explored; see pdf_extract.dioceses.
DIOCESES_DIR = DATA_DIR / "dioceses"

# Wait on SQLITE_BUSY before failing (multiple processes / concurrent sessions).
SQLITE_BUSY_TIMEOUT_MS = 10_000


# ── Connection helpers ──────────────────────────────────────────────────────
def configure_sqlite_connection(conn: sqlite3.Connection) -> None:
    """Shared PRAGMAs for pipeline DB access: WAL concurrency, lock backoff, FK checks."""
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute(f"PRAGMA busy_timeout={SQLITE_BUSY_TIMEOUT_MS}")


def connect_db(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    configure_sqlite_connection(conn)
    return conn


def delete_db(db_path: Path = DEFAULT_DB_PATH) -> bool:
    if not db_path.exists():
        return False
    db_path.unlink()
    return True


# ── Timestamp helper ────────────────────────────────────────────────────────
def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ── JSON file helpers ───────────────────────────────────────────────────────
def load_json_list(path: Path) -> list[Any]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_list(path: Path, data: list[Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_json_dict(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_dict(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ── DB read helpers (used by pipeline steps) ────────────────────────────────
def list_parishes(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id, slug, name, homepage_url, bulletin_provider, provider_id FROM parish ORDER BY id"
    ).fetchall()


def get_parish_by_name(conn: sqlite3.Connection, name: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id, slug, name, homepage_url, bulletin_provider, provider_id"
        " FROM parish WHERE name = ?",
        (name,),
    ).fetchone()


def list_churches(conn: sqlite3.Connection, parish_id: int) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id, parish_id, slug, name, address_line1, address_line2, city, state, postal_code"
        " FROM church WHERE parish_id = ? ORDER BY id",
        (parish_id,),
    ).fetchall()


# ── Bulletins ───────────────────────────────────────────────────────────────
def latest_bulletin_order(alias: str = "") -> str:
    """ORDER BY that puts a parish's current bulletin first.

    Most recently published, then most recently fetched, then most recently
    processed, with the highest id as a deterministic tie-break. The frontend
    snapshot, the change report and `recurrence apply` all rank by it, so they
    agree on which bulletin a parish is currently showing. Only processed
    bulletins take part: one that was fetched but never extracted has no
    events, and ranking it first would blank the parish.
    """
    col = f"{alias}." if alias else ""
    return (
        f"COALESCE({col}published_date, '') DESC,"
        f" COALESCE({col}fetched_at, '') DESC,"
        f" COALESCE({col}processed_at, '') DESC,"
        f" {col}id DESC"
    )


def latest_bulletin_ids(conn: sqlite3.Connection) -> dict[str, int]:
    """Parish slug -> id of the processed bulletin the frontend shows for it."""
    rows = conn.execute(
        f"""
        SELECT slug, id FROM (
            SELECT p.slug, b.id,
                   ROW_NUMBER() OVER (
                       PARTITION BY b.parish_id ORDER BY {latest_bulletin_order("b")}
                   ) AS rn
            FROM bulletin b JOIN parish p ON p.id = b.parish_id
            WHERE b.processed_at IS NOT NULL
        ) WHERE rn = 1
        """
    ).fetchall()
    return {r["slug"]: r["id"] for r in rows}


def load_bulletins(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Every bulletin as a dict, in insertion order (the recency tie-break)."""
    rows = conn.execute(
        """SELECT b.id, p.slug AS parish_slug, b.source_url, b.content_hash,
                  b.published_date, b.fetched_at, b.processed_at
           FROM bulletin b JOIN parish p ON p.id = b.parish_id
           ORDER BY b.id"""
    ).fetchall()
    return [dict(r) for r in rows]


def insert_bulletin(
    conn: sqlite3.Connection,
    *,
    parish_id: int,
    source_url: str,
    content_hash: str,
    fetched_at: str,
) -> int:
    with conn:
        cursor = conn.execute(
            """INSERT INTO bulletin(parish_id, source_url, content_hash, fetched_at)
               VALUES (?, ?, ?, ?)""",
            (parish_id, source_url, content_hash, fetched_at),
        )
    return int(cursor.lastrowid)


def event_row_values(conn: sqlite3.Connection, row: dict[str, Any]) -> tuple | None:
    """Column values for an event row, from its extracted (string) form.

    Returns (church_id, event_type, event_kind, day_of_week, date, start_time,
    end_time, cancelled, page_number, note), or None with a logged warning when
    the row cannot be stored: an unknown church, or a start time or date the
    parsers cannot read.
    """
    church_slug = row.get("church_slug")
    church = conn.execute(
        "SELECT id FROM church WHERE slug = ?", (church_slug,)
    ).fetchone() if isinstance(church_slug, str) and church_slug else None
    if church is None:
        LOGGER.warning("Skipping event: unknown church %r", church_slug)
        return None

    start_minutes = time_to_minutes(row.get("start_time"))
    if start_minutes is None:
        LOGGER.warning(
            "Skipping event: unparseable start_time %r (church=%s)",
            row.get("start_time"), church_slug,
        )
        return None

    event_kind = row.get("event_kind", "")
    event_date = None
    if event_kind == "specific_date":
        event_date = normalize_event_date(row.get("date"))
        if event_date is None:
            LOGGER.warning(
                "Skipping event: unparseable specific_date %r (church=%s)",
                row.get("date"), church_slug,
            )
            return None

    page_number = row.get("page_number")
    note_raw = row.get("note")
    return (
        church["id"],
        row.get("event_type", ""),
        event_kind,
        row.get("day_of_week"),
        event_date,
        start_minutes,
        time_to_minutes(row.get("end_time")),
        int(bool(row.get("cancelled", False))),
        page_number if isinstance(page_number, int) else None,
        note_raw.strip() if isinstance(note_raw, str) and note_raw.strip() else None,
    )


def _insert_events(
    conn: sqlite3.Connection, bulletin_id: int, rows: list[dict[str, Any]],
) -> tuple[int, int]:
    stored = skipped = 0
    conn.execute("DELETE FROM event WHERE bulletin_id = ?", (bulletin_id,))
    for row in rows:
        values = event_row_values(conn, row)
        if values is None:
            skipped += 1
            continue
        conn.execute(
            """INSERT INTO event(
                   bulletin_id, church_id, event_type, event_kind, day_of_week, date,
                   start_time, end_time, cancelled, page_number, note
               ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (bulletin_id, *values),
        )
        stored += 1
    return stored, skipped


def replace_bulletin_events(
    conn: sqlite3.Connection, bulletin_id: int, rows: list[dict[str, Any]],
) -> tuple[int, int]:
    """Replace a bulletin's events. Returns (events stored, events skipped as unstorable)."""
    with conn:
        return _insert_events(conn, bulletin_id, rows)


def save_processed_bulletin(
    conn: sqlite3.Connection,
    bulletin_id: int,
    rows: list[dict[str, Any]],
    *,
    processed_at: str,
    published_date: str | None,
) -> tuple[int, int]:
    """Replace a bulletin's events and mark it processed, in one transaction.

    Returns (events stored, events skipped as unstorable).
    """
    with conn:
        counts = _insert_events(conn, bulletin_id, rows)
        conn.execute(
            """UPDATE bulletin
               SET processed_at = ?, published_date = COALESCE(?, published_date)
               WHERE id = ?""",
            (processed_at, published_date, bulletin_id),
        )
    return counts


def load_events(
    conn: sqlite3.Connection, bulletin_ids: list[int] | None = None,
) -> list[dict[str, Any]]:
    """Events in the extracted-row shape the recurrence detector works on.

    Times come back as "h:MM AM" strings, the form the extractor produces, so
    rows read from the database and rows fresh from the classifier are
    interchangeable. `bulletin_id` is included so callers can write changes back.
    """
    sql = """SELECT e.id, e.bulletin_id, c.slug AS church_slug,
                    b.source_url AS bulletin_source_url,
                    e.event_type, e.event_kind, e.day_of_week, e.date,
                    e.start_time, e.end_time, e.cancelled, e.page_number, e.note
             FROM event e
             JOIN church c ON c.id = e.church_id
             JOIN bulletin b ON b.id = e.bulletin_id"""
    params: tuple = ()
    if bulletin_ids is not None:
        if not bulletin_ids:
            return []
        sql += f" WHERE e.bulletin_id IN ({', '.join('?' * len(bulletin_ids))})"
        params = tuple(bulletin_ids)
    sql += " ORDER BY e.id"
    out = []
    for r in conn.execute(sql, params).fetchall():
        row = dict(r)
        row["start_time"] = minutes_to_time(row["start_time"])
        row["end_time"] = minutes_to_time(row["end_time"])
        row["cancelled"] = bool(row["cancelled"])
        out.append(row)
    return out


# ── Bulletin PDF and church-list loading ────────────────────────────────────
def read_bulletin_pdf(parish_slug: str, content_hash: str) -> bytes | None:
    """Read a bulletin PDF, truncated to the pages a classifier looks at.

    The PDF comes from the blob store (downloaded into data/bulletins/ on first
    use when R2 is configured). Returns None (with a logged warning) when the
    bulletin should be skipped: the PDF is missing, truncation failed, or the
    read failed. Every caller that hands a bulletin to an LLM goes through
    here, so the skip policy is defined once.
    """
    key = bulletin_pdf_key(parish_slug, content_hash)
    try:
        pdf_path = get_store().local_path(key)
    except Exception:
        LOGGER.warning("Skipping: failed loading %s from the blob store", key, exc_info=True)
        return None
    if pdf_path is None:
        LOGGER.warning("Skipping: PDF missing at %s", key)
        return None

    try:
        read_path = ensure_truncated_pdf(pdf_path)
    except Exception:
        LOGGER.warning("Skipping: failed truncating PDF at %s", pdf_path, exc_info=True)
        return None

    try:
        return read_path.read_bytes()
    except OSError:
        LOGGER.warning("Skipping: failed reading PDF at %s", read_path, exc_info=True)
        return None


def church_list_for_prompt(
    conn: sqlite3.Connection, parish_id: int
) -> list[dict[str, Any]]:
    """A parish's known churches in the {slug, name, address} shape the prompts take."""
    return [
        {
            "slug": r["slug"],
            "name": r["name"],
            "address": format_address(
                r["address_line1"], r["address_line2"],
                r["city"], r["state"], r["postal_code"],
            ),
        }
        for r in list_churches(conn, parish_id)
    ]


@dataclass
class BulletinWorkItem:
    """A bulletin loaded from the blob store and ready to hand to a classifier."""

    entry: dict[str, Any]
    pdf_bytes: bytes
    church_list: list[dict[str, Any]]


def load_bulletin_work_item(
    entry: dict[str, Any], conn: sqlite3.Connection
) -> BulletinWorkItem | None:
    """Load PDF bytes and known-church list for a bulletin entry.

    Returns None (with a logged warning) if the bulletin should be skipped:
    no content hash, PDF unreadable (see `read_bulletin_pdf`), or parish not
    in DB.

    Runs on the caller's thread; the sqlite connection must stay single-threaded.
    """
    parish_slug = entry["parish_slug"]
    content_hash = entry.get("content_hash")
    if not isinstance(content_hash, str) or not content_hash:
        LOGGER.warning("Skipping: bulletin %s has no content hash", entry.get("source_url"))
        return None

    pdf_bytes = read_bulletin_pdf(parish_slug, content_hash)
    if pdf_bytes is None:
        return None

    parish_row = conn.execute(
        "SELECT id FROM parish WHERE slug = ?", (parish_slug,)
    ).fetchone()
    if not parish_row:
        LOGGER.warning("Skipping: parish %s not found in DB", parish_slug)
        return None

    return BulletinWorkItem(
        entry=entry,
        pdf_bytes=pdf_bytes,
        church_list=church_list_for_prompt(conn, parish_row["id"]),
    )
