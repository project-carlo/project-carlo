"""Extract the frontend snapshot from parish_events.db.

The snapshot is every church and event the website shows, with columns
stripped down to what the web app reads. It is gzipped JSON, written to
apps/web/public/frontend.json.gz for Vite to serve as an opaque static asset;
the app (apps/web/src/lib/snapshot.ts) decodes it into memory.

Format (version 1). Each table is stored column by column, as parallel arrays:

    {
      "version": 1,
      "churches": {"id": [...], "parish_id": [...], "slug": [...], ...},
      "events": {"id": {"deltas": [...]}, "church_id": [...], ...}
    }

A column is one of:

    [v0, v1, ...]                              the values themselves
    {"values": [...], "codes": [i0, i1, ...]}  an index into `values` per row
                                               (null for null), for repeated strings
    {"deltas": [d0, d1, ...]}                  each value minus the one before it
                                               (the first minus 0), for event ids

`churches` has CHURCH_COLUMNS, ordered by name then id; `events` has
EVENT_COLUMNS, ordered by id. `church_id` is the church's id, `cancelled` a
boolean, times are minutes after midnight, and `date` is an ISO date.

Bump SNAPSHOT_VERSION (and the app's) on any change the app would misread.
"""

from __future__ import annotations

import gzip
import json
import logging
import sqlite3
import zlib
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from pdf_extract.storage import (
    DEFAULT_DB_PATH,
    configure_sqlite_connection,
    latest_bulletin_order,
)

LOGGER = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DB = DEFAULT_DB_PATH
SNAPSHOT_NAME = "frontend.json.gz"
DEST_SNAPSHOT = ROOT / "apps" / "web" / "public" / SNAPSHOT_NAME
SNAPSHOT_VERSION = 1

# The columns the SELECTs below produce, in order.
CHURCH_COLUMNS = (
    "id", "parish_id", "slug", "name", "address_line1", "address_line2", "city", "state",
    "postal_code", "latitude", "longitude", "homepage_url", "bulletin_url",
)
EVENT_COLUMNS = (
    "id", "church_id", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "page_number", "note",
)
# Strings that repeat across rows: a table of distinct values plus small
# integers is smaller and faster for the browser to parse than the strings.
_CODED_COLUMNS = {
    "churches": {"city", "state"},
    "events": {"event_type", "event_kind", "day_of_week", "date", "note"},
}
# Event ids mostly go up by one, so their differences compress far better.
_DELTA_COLUMNS = {"churches": set(), "events": {"id"}}


class SnapshotFormatError(ValueError):
    """The bytes are not a snapshot in the format this code writes."""


def _encode_column(table: str, name: str, values: list[Any]) -> Any:
    if name in _CODED_COLUMNS[table]:
        distinct: dict[Any, int] = {}
        codes = [None if v is None else distinct.setdefault(v, len(distinct)) for v in values]
        return {"values": list(distinct), "codes": codes}
    if name in _DELTA_COLUMNS[table]:
        previous = 0
        deltas = []
        for value in values:
            deltas.append(value - previous)
            previous = value
        return {"deltas": deltas}
    return values


def _decode_column(column: Any) -> list[Any]:
    if isinstance(column, list):
        return column
    if "codes" in column:
        values = column["values"]
        return [None if code is None else values[code] for code in column["codes"]]
    total = 0
    decoded = []
    for delta in column["deltas"]:
        total += delta
        decoded.append(total)
    return decoded


def _encode_table(table: str, columns: Sequence[str], rows: list[tuple]) -> dict[str, Any]:
    return {
        name: _encode_column(table, name, [row[i] for row in rows])
        for i, name in enumerate(columns)
    }


def encode_snapshot(churches: list[tuple], events: list[tuple]) -> bytes:
    """Gzipped snapshot of rows in CHURCH_COLUMNS / EVENT_COLUMNS order.

    The same rows always give the same bytes (no gzip timestamp), so an
    unchanged snapshot hashes the same from one run to the next.
    """
    cancelled = EVENT_COLUMNS.index("cancelled")
    events = [(*row[:cancelled], bool(row[cancelled]), *row[cancelled + 1:]) for row in events]
    document = {
        "version": SNAPSHOT_VERSION,
        "churches": _encode_table("churches", CHURCH_COLUMNS, churches),
        "events": _encode_table("events", EVENT_COLUMNS, events),
    }
    text = json.dumps(document, ensure_ascii=False, separators=(",", ":"))
    return gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0)


def read_snapshot(data: bytes) -> dict[str, list[dict[str, Any]]]:
    """Decode snapshot bytes into {"churches": [row, ...], "events": [row, ...]}.

    Raises SnapshotFormatError for anything but this format version, such as
    the gzipped SQLite snapshots that runs published before it.
    """
    try:
        document = json.loads(gzip.decompress(data))
    except (OSError, EOFError, zlib.error, ValueError) as exc:
        raise SnapshotFormatError(f"not a gzipped JSON snapshot ({exc})") from exc
    version = document.get("version") if isinstance(document, dict) else None
    if version != SNAPSHOT_VERSION:
        raise SnapshotFormatError(
            f"snapshot format version {version!r}; this code reads version {SNAPSHOT_VERSION}"
        )
    tables: dict[str, list[dict[str, Any]]] = {}
    for table, names in (("churches", CHURCH_COLUMNS), ("events", EVENT_COLUMNS)):
        columns = [_decode_column(document[table][name]) for name in names]
        tables[table] = [dict(zip(names, row, strict=True)) for row in zip(*columns, strict=True)]
    return tables


def extract(
    source: Path = SOURCE_DB, dest: Path = DEST_SNAPSHOT, *, keep_previous: bool = True,
) -> dict[str, object]:
    """Write the frontend snapshot of `source` to `dest`.

    With `keep_previous`, an existing snapshot at `dest` is first moved to
    `<dest>.previous` for `verify-frontend-snapshot` to compare against.
    """
    if not source.exists():
        raise FileNotFoundError(f"Source database not found: {source}")

    src = sqlite3.connect(source)
    configure_sqlite_connection(src)
    try:
        churches = src.execute(
            f"""
            SELECT c.id, c.parish_id, c.slug, c.name, c.address_line1, c.address_line2,
                   c.city, c.state, c.postal_code, c.latitude, c.longitude,
                   p.homepage_url,
                   (SELECT b.source_url FROM bulletin b
                    WHERE b.parish_id = c.parish_id AND b.processed_at IS NOT NULL
                    ORDER BY {latest_bulletin_order("b")}
                    LIMIT 1)
            FROM church c
            LEFT JOIN parish p ON c.parish_id = p.id
            ORDER BY c.name, c.id
            """
        ).fetchall()

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
                           ORDER BY {latest_bulletin_order()}
                       ) AS rn
                FROM bulletin
                WHERE processed_at IS NOT NULL
            ) latest ON b.parish_id = latest.parish_id AND b.id = latest.id AND latest.rn = 1
            ORDER BY e.id
            """
        ).fetchall()
    finally:
        src.close()

    data = encode_snapshot(churches, events)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if keep_previous and dest.exists():
        dest.replace(dest.with_name(f"{dest.name}.previous"))
    dest.write_bytes(data)

    raw_size_kb = len(gzip.decompress(data)) / 1024
    compressed_size_kb = len(data) / 1024
    LOGGER.info(
        "%s: %d churches, %d events, %.1f KB compressed from %.1f KB",
        dest.name,
        len(churches),
        len(events),
        compressed_size_kb,
        raw_size_kb,
    )
    return {
        "churches": len(churches),
        "events": len(events),
        "raw_kb": round(raw_size_kb, 1),
        "compressed_kb": round(compressed_size_kb, 1),
        "snapshot_path": str(dest),
    }
