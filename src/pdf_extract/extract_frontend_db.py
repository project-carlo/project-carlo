"""Extract the frontend snapshot from parish_events.db.

The snapshot is every church and event the website shows, with columns
stripped down to what the web app reads. It is gzipped JSON, written to
apps/web/public/frontend.json.gz for Vite to serve as an opaque static asset;
the app (apps/web/src/lib/snapshot.ts) decodes it into memory.

Format (version 2). Each table is stored column by column, as parallel arrays:

    {
      "version": 2,
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
boolean, times are minutes after midnight, and `date` is an ISO date. A
church's `bulletin_url` and `bulletin_week` describe its parish's current
bulletin, the one its events come from: `bulletin_week` is the ISO date of
the Sunday of the week that bulletin is for (`bulletin_week.bulletin_week`),
or null when the bulletin has no date at all. Churches retired from
churches.csv are left out, and so are the churches (and events) of fetch-only
parishes, which are fetched but not yet processed.

Each parish's events come from its own mode (docs/schedule-state-plan.md):

- extract mode: the `event` rows of its current bulletin, every week, no season;
- update mode: its believed schedule (`current_schedule`), each entry's id
  negated so it can't collide with an event id, and its `page_number` the
  entry's sighting in the parish's current bulletin (null when that bulletin
  doesn't print it).

Version 2 added, after `note`: `weeks_of_month` (a list of "first" ...
"last"; [] for every week), the season as four integer columns (months 1-12,
days null or a day of the month; all null for all year), and
`cancels_event_id`: a cancelled dated row names the weekly row (same church,
event type and start time, on the date's weekday) whose occurrence it cancels.
The weekly row's weeks of the month, exclusions and season must include the date.
A cancellation that matches no weekly row is left out, and so is every dated
row before the build date. `read_snapshot` still reads version 1, as every
week, no season and no cancellations, so a run can be checked against a
version 1 snapshot.

`exclude_weeks` was added to version 2 later, last: true when the row's
`weeks_of_month` are the weeks it skips ("every Sunday except the last" is
`["last"]` excluded). A snapshot written before it reads as null there, which
the app takes as false.

Bump SNAPSHOT_VERSION (and the app's) on any change the app would misread.
A new column needs no bump when its absence reads as null: list it in
ADDED_COLUMNS, and the app and `read_snapshot` take a snapshot written before
it (an older published run, or the live site's while a deploy is pending)
as having nulls there, rather than refuse it.
"""

from __future__ import annotations

import gzip
import json
import logging
import sqlite3
import zlib
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import Any

from pdf_extract.bulletin_week import parse_iso_date, week_order_sql
from pdf_extract.labeling.labels import DAYS
from pdf_extract.schedule.qualifiers import (
    mask_excludes_weeks,
    mask_to_weeks,
    recurrence_includes_date,
    weeks_to_mask,
)
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
SNAPSHOT_VERSION = 2
# Versions `read_snapshot` reads. The app reads only SNAPSHOT_VERSION.
READABLE_VERSIONS = (1, 2)

# The columns the SELECTs below produce, in order.
CHURCH_COLUMNS = (
    "id", "parish_id", "slug", "name", "address_line1", "address_line2", "city", "state",
    "postal_code", "latitude", "longitude", "homepage_url", "bulletin_url", "bulletin_week",
)
EVENT_COLUMNS = (
    "id", "church_id", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "page_number", "note",
    "weeks_of_month", "season_start_month", "season_start_day", "season_end_month",
    "season_end_day", "cancels_event_id", "exclude_weeks",
)
# The columns version 2 added. A version 1 snapshot's rows read as every
# week ([]), no season and no cancellation (None) in them.
_V2_DEFAULTS = frozenset({
    "weeks_of_month", "season_start_month", "season_start_day", "season_end_month",
    "season_end_day", "cancels_event_id",
})
# Columns added since version 1 shipped. A snapshot written before one was
# added lacks it; readers take it as all nulls.
ADDED_COLUMNS = {"churches": {"bulletin_week"}, "events": {"exclude_weeks"}}
# Strings that repeat across rows: a table of distinct values plus small
# integers is smaller and faster for the browser to parse than the strings.
_CODED_COLUMNS = {
    "churches": {"city", "state", "bulletin_week"},
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

    Raises SnapshotFormatError for a format version it doesn't read, such as
    the gzipped SQLite snapshots that runs published before version 1. A
    version 1 snapshot's events read as every week, no season and no
    cancellations.
    """
    try:
        document = json.loads(gzip.decompress(data))
    except (OSError, EOFError, zlib.error, ValueError) as exc:
        raise SnapshotFormatError(f"not a gzipped JSON snapshot ({exc})") from exc
    version = document.get("version") if isinstance(document, dict) else None
    if version not in READABLE_VERSIONS:
        raise SnapshotFormatError(
            f"snapshot format version {version!r}; this code reads versions "
            f"{', '.join(map(str, READABLE_VERSIONS))}"
        )
    tables: dict[str, list[dict[str, Any]]] = {}
    for table, names in (("churches", CHURCH_COLUMNS), ("events", EVENT_COLUMNS)):
        stored = document[table]
        rows = len(_decode_column(stored["id"]))
        columns = [
            [None] * rows
            if name not in stored and name in ADDED_COLUMNS[table]
            else [[] if name == "weeks_of_month" else None for _ in range(rows)]
            if version == 1 and table == "events" and name in _V2_DEFAULTS
            else _decode_column(stored[name])
            for name in names
        ]
        tables[table] = [dict(zip(names, row, strict=True)) for row in zip(*columns, strict=True)]
    return tables


_LATEST_BULLETIN = f"""
    SELECT parish_id, id, source_url, NULLIF({week_order_sql()}, '') AS week,
           ROW_NUMBER() OVER (PARTITION BY parish_id ORDER BY {latest_bulletin_order()}) AS rn
    FROM bulletin
    WHERE processed_at IS NOT NULL
"""


def _extract_mode_events(conn: sqlite3.Connection, update_mode: set[int]) -> list[tuple]:
    """Each extract-mode parish's current bulletin's events, as every week, no season."""
    rows = conn.execute(
        f"""
        SELECT e.id, e.church_id, e.event_type, e.event_kind,
               e.day_of_week, e.date, e.start_time, e.end_time, e.cancelled,
               e.page_number, e.note, b.parish_id
        FROM event e
        INNER JOIN bulletin b ON e.bulletin_id = b.id
        INNER JOIN ({_LATEST_BULLETIN}) latest
            ON b.parish_id = latest.parish_id AND b.id = latest.id AND latest.rn = 1
        ORDER BY e.id
        """
    ).fetchall()
    return [
        (*row[:11], [], None, None, None, None, None, False)
        for row in rows if row[11] not in update_mode
    ]


def _update_mode_events(conn: sqlite3.Connection) -> list[tuple]:
    """Each update-mode parish's believed schedule, entry ids negated.

    The page is the entry's sighting in its parish's current bulletin, the one
    the church's `bulletin_url` opens.
    """
    rows = conn.execute(
        f"""
        SELECT e.id, e.church_id, e.event_type, e.event_kind, e.day_of_week, e.date,
               e.start_time, e.end_time, e.cancelled, sighting.page_number, e.note,
               e.weeks_of_month, e.season_start_month, e.season_start_day,
               e.season_end_month, e.season_end_day
        FROM current_schedule s
        JOIN schedule_entry e ON e.id = s.entry_id
        LEFT JOIN ({_LATEST_BULLETIN}) latest ON latest.parish_id = s.parish_id AND latest.rn = 1
        LEFT JOIN entry_sighting sighting
            ON sighting.bulletin_id = latest.id AND sighting.entry_id = e.id
        WHERE s.parish_id IN (
            SELECT parish_id FROM schedule_revision WHERE source_kind = 'seed'
        )
        """
    ).fetchall()
    return [
        (
            -row[0], *row[1:11], mask_to_weeks(row[11]), *row[12:16], None,
            mask_excludes_weeks(row[11]),
        )
        for row in rows
    ]


def _fetch_only_parish_ids(conn: sqlite3.Connection) -> set[int]:
    """Parishes the site leaves out until their bulletins are processed (none before migration 7)."""
    columns = {row[1] for row in conn.execute("PRAGMA table_info(parish)").fetchall()}
    if "fetch_only" not in columns:
        return set()
    return {row[0] for row in conn.execute("SELECT id FROM parish WHERE fetch_only = 1")}


_ID, _CHURCH, _TYPE, _KIND, _DAY, _DATE, _START = range(7)
_CANCELLED = EVENT_COLUMNS.index("cancelled")
_CANCELS = EVENT_COLUMNS.index("cancels_event_id")
_WEEKS = EVENT_COLUMNS.index("weeks_of_month")
_EXCLUDE_WEEKS = EVENT_COLUMNS.index("exclude_weeks")
_SEASON = slice(EVENT_COLUMNS.index("season_start_month"), EVENT_COLUMNS.index("season_end_day") + 1)


def finish_events(rows: list[tuple], build_date: date) -> list[tuple]:
    """Drop past dated rows, match each cancellation to the weekly row it cancels, sort by id.

    A cancelled dated row cancels the weekly row with the same church, event
    type and start time on its date's weekday, whose weeks of the month and
    season include that date. One that matches nothing is left out (cancelled
    rows are hidden anyway). In update mode the identity rules allow at most
    one matching recurrence; an extract-mode bulletin can repeat a slot, and
    then the lowest id is named.
    """
    today = build_date.isoformat()
    rows = [r for r in rows if r[_KIND] != "specific_date" or (r[_DATE] or "") >= today]
    weekly: dict[tuple, list[tuple]] = {}
    for row in sorted(rows, key=lambda r: r[_ID]):
        if row[_KIND] == "weekly":
            weekly.setdefault((row[_CHURCH], row[_TYPE], row[_DAY], row[_START]), []).append(row)
    out = []
    for row in rows:
        if row[_CANCELLED] and row[_KIND] == "specific_date":
            day = parse_iso_date(row[_DATE])
            if day is None:
                continue
            candidates = weekly.get(
                (row[_CHURCH], row[_TYPE], DAYS[day.weekday()], row[_START]), [],
            )
            match = next((
                candidate[_ID] for candidate in candidates
                if recurrence_includes_date(
                    day, weeks_to_mask(candidate[_WEEKS], candidate[_EXCLUDE_WEEKS]),
                    *candidate[_SEASON],
                )
            ), None)
            if match is None:
                continue
            row = (*row[:_CANCELS], match, *row[_CANCELS + 1:])
        out.append(row)
    return sorted(out, key=lambda r: r[_ID])


def extract(
    source: Path = SOURCE_DB,
    dest: Path = DEST_SNAPSHOT,
    *,
    keep_previous: bool = True,
    build_date: date | None = None,
) -> dict[str, object]:
    """Write the frontend snapshot of `source` to `dest`.

    With `keep_previous`, an existing snapshot at `dest` is first moved to
    `<dest>.previous` for `verify-frontend-snapshot` to compare against.
    `build_date` (default today) is the day before which dated rows are left out.
    """
    if not source.exists():
        raise FileNotFoundError(f"Source database not found: {source}")

    src = sqlite3.connect(source)
    configure_sqlite_connection(src)
    try:
        churches = src.execute(
            f"""
            WITH latest AS ({_LATEST_BULLETIN})
            SELECT c.id, c.parish_id, c.slug, c.name, c.address_line1, c.address_line2,
                   c.city, c.state, c.postal_code, c.latitude, c.longitude,
                   p.homepage_url, latest.source_url, latest.week
            FROM church c
            LEFT JOIN parish p ON c.parish_id = p.id
            LEFT JOIN latest ON latest.parish_id = c.parish_id AND latest.rn = 1
            WHERE c.retired_at IS NULL
            ORDER BY c.name, c.id
            """
        ).fetchall()
        update_mode = {
            row[0] for row in src.execute(
                "SELECT DISTINCT parish_id FROM schedule_revision WHERE source_kind = 'seed'"
            ).fetchall()
        }
        events = finish_events(
            _extract_mode_events(src, update_mode) + _update_mode_events(src),
            build_date or date.today(),
        )
        hidden = _fetch_only_parish_ids(src)
        if hidden:
            churches = [row for row in churches if row[1] not in hidden]
            shown = {row[0] for row in churches}
            events = [row for row in events if row[_CHURCH] in shown]
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
