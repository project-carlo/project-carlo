"""Extract the frontend snapshot from parish_events.db.

The snapshot is every church and event the website shows, with columns
stripped down to what the web app reads. It is gzipped JSON, written to
apps/web/public/frontend.json.gz for Vite to serve as an opaque static asset;
the app (packages/core/src/snapshot.ts) decodes it into memory.

Format (version 3). Each table is stored column by column, as parallel arrays:

    {
      "version": 3,
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
or null when the bulletin has no date at all. A `website_schedule` parish has
no bulletin (docs/source-schedules-plan.md): its churches' `schedule_source`
(`website` or `facebook`), `source_url` and `checked_on` (the ISO date of its
latest seed's `as_of` in the parishes' Eastern time zone) say where its times
were read and when, and it has no `bulletin_url` or `bulletin_week`, whatever
it once published; the three are null for every other church, which the app
reads as a bulletin's times.
`schedule_source` and `checked_on` are coded. Churches retired from
churches.csv are left out, and so are the churches of parishes without an
approved seed: their bulletins are fetched, but they aren't on the site yet.

A parish's events are its believed schedule (`current_schedule`,
docs/schedule-state-plan.md), each entry's id negated (ids from before update
mode were the old `event` table's), and its `page_number` the entry's sighting
in the parish's current bulletin (null when that bulletin doesn't print it).

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

Version 4 adds chapels open 24 hours (`continuous` rows, docs/believed-schedules.md,
"Chapels open 24 hours"): Adoration rows with no day, date, start or end time, and
`access` (`not_stated`, `code_after_hours`, `code` or `arrangement`) with the
unlocked hours `open_from`/`open_until` (minutes after midnight, or null), all three
null on every other row. A version 3 reader would take such a row's null
`start_time` for a time, so it must refuse version 4. Churches gain `kind`
(`church`, or `adoration_chapel` for a parish's Adoration chapel at its own
address); `read_snapshot` takes an older snapshot's churches as `church` there.
Notes holding what looks like a phone number, email address or door code
(`model.private_detail`) are left out of every row.

Bump SNAPSHOT_VERSION (and the app's) on any change the app would misread.
Version 3 adds inclusive absolute valid_from/valid_until dates for weekly
entries. They do not repeat annually. Older web readers must refuse version 3
rather than advertise expired times; the new reader also accepts version 2.
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
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from pdf_extract.bulletin_week import parse_iso_date, week_order_sql
from pdf_extract.model import DAYS, WEBSITE_SCHEDULE, private_detail
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
SNAPSHOT_VERSION = 4
# Versions `read_snapshot` reads. The app accepts 2 to 4.
READABLE_VERSIONS = (1, 2, 3, 4)

# The columns the SELECTs below produce, in order.
CHURCH_COLUMNS = (
    "id", "parish_id", "slug", "name", "address_line1", "address_line2", "city", "state",
    "postal_code", "latitude", "longitude", "homepage_url", "bulletin_url", "bulletin_week",
    "schedule_source", "source_url", "checked_on", "kind",
)
EVENT_COLUMNS = (
    "id", "church_id", "event_type", "event_kind", "day_of_week", "date", "start_time",
    "end_time", "cancelled", "page_number", "note",
    "weeks_of_month", "season_start_month", "season_start_day", "season_end_month",
    "season_end_day", "cancels_event_id", "exclude_weeks",
    "valid_from", "valid_until", "access", "open_from", "open_until",
)
# The columns version 2 added. A version 1 snapshot's rows read as every
# week ([]), no season and no cancellation (None) in them.
_V2_DEFAULTS = frozenset({
    "weeks_of_month", "season_start_month", "season_start_day", "season_end_month",
    "season_end_day", "cancels_event_id",
})
# Columns added since version 1 shipped. A snapshot written before one was
# added lacks it; readers take it as all nulls.
ADDED_COLUMNS = {
    "churches": {"bulletin_week", "schedule_source", "source_url", "checked_on", "kind"},
    "events": {"exclude_weeks", "valid_from", "valid_until", "access", "open_from",
               "open_until"},
}
# Strings that repeat across rows: a table of distinct values plus small
# integers is smaller and faster for the browser to parse than the strings.
_CODED_COLUMNS = {
    "churches": {"city", "state", "bulletin_week", "schedule_source", "checked_on", "kind"},
    "events": {"event_type", "event_kind", "day_of_week", "date", "note", "access"},
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
            ["church"] * rows
            if table == "churches" and name == "kind" and name not in stored
            else [None] * rows
            if name not in stored and name in ADDED_COLUMNS[table]
            else [[] if name == "weeks_of_month" else None for _ in range(rows)]
            if version == 1 and table == "events" and name in _V2_DEFAULTS
            else _decode_column(stored[name])
            for name in names
        ]
        tables[table] = [dict(zip(names, row, strict=True)) for row in zip(*columns, strict=True)]
    return tables


# Each parish's latest seed revision, when it was loaded from a source seed. A later
# bulletin seed (the parish found a bulletin) hides it, as does a provider that isn't
# `website_schedule` (the joins in `extract` and `_SOURCED_PARISHES`).
_LATEST_SOURCE_SEED = """
    SELECT * FROM (
        SELECT parish_id, schedule_source, schedule_source_url, as_of,
               ROW_NUMBER() OVER (PARTITION BY parish_id ORDER BY revision DESC) AS rn
        FROM schedule_revision WHERE source_kind = 'seed'
    ) WHERE schedule_source IS NOT NULL
"""
# The parishes shown with a source: their churches have no current bulletin.
_SOURCED_PARISHES = f"""
    SELECT sourced.parish_id FROM ({_LATEST_SOURCE_SEED}) sourced
    JOIN parish p ON p.id = sourced.parish_id
    WHERE sourced.rn = 1 AND p.bulletin_provider = '{WEBSITE_SCHEDULE}'
"""

# The parishes on the site are all in the Eastern time zone (Delaware to New York), so
# a source's `checked_on` is the date there, not UTC's: a page captured on an evening
# was checked that day.
SITE_TIMEZONE = ZoneInfo("America/New_York")


def checked_on(as_of: str | None) -> str | None:
    """The ISO date a source seed's `as_of` (an ISO time) falls on in SITE_TIMEZONE."""
    if not as_of:
        return None
    moment = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment.astimezone(SITE_TIMEZONE).date().isoformat()


_LATEST_BULLETIN = f"""
    SELECT parish_id, id, source_url, NULLIF({week_order_sql()}, '') AS week,
           ROW_NUMBER() OVER (PARTITION BY parish_id ORDER BY {latest_bulletin_order()}) AS rn
    FROM bulletin
    WHERE processed_at IS NOT NULL
"""


def _schedule_events(conn: sqlite3.Connection) -> list[tuple]:
    """Each seeded parish's believed schedule, entry ids negated.

    The page is the entry's sighting in its parish's current bulletin, the one
    the church's `bulletin_url` opens. A parish shown with a source has none, so
    an entry its old bulletin printed has no page.
    """
    columns = {row[1] for row in conn.execute('PRAGMA table_info(schedule_entry)')}
    bounds = ', '.join(f'e.{name}' if name in columns else 'NULL'
                       for name in ('valid_from', 'valid_until', 'access', 'open_from',
                                    'open_until'))
    rows = conn.execute(
        f"""
        SELECT e.id, e.church_id, e.event_type, e.event_kind, e.day_of_week, e.date,
               e.start_time, e.end_time, e.cancelled, sighting.page_number, e.note,
               e.weeks_of_month, e.season_start_month, e.season_start_day,
               e.season_end_month, e.season_end_day, {bounds}
        FROM current_schedule s
        JOIN schedule_entry e ON e.id = s.entry_id
        LEFT JOIN ({_LATEST_BULLETIN}) latest ON latest.parish_id = s.parish_id AND latest.rn = 1
            AND s.parish_id NOT IN ({_SOURCED_PARISHES})
        LEFT JOIN entry_sighting sighting
            ON sighting.bulletin_id = latest.id AND sighting.entry_id = e.id
        WHERE s.parish_id IN (
            SELECT parish_id FROM schedule_revision WHERE source_kind = 'seed'
        )
        """
    ).fetchall()
    return [
        (
            -row[0], *row[1:10], public_note(row[10], -row[0]), mask_to_weeks(row[11]),
            *row[12:16], None, mask_excludes_weeks(row[11]),
            *row[16:21],
        )
        for row in rows
    ]


def public_note(note: str | None, event_id: int) -> str | None:
    """A note as the site may show it: none at all when it looks like it holds a person's
    contact or a door code (`model.private_detail`), which no check let through on purpose."""
    if note is None:
        return None
    private = private_detail(note)
    if private:
        LOGGER.warning("event %d: note %s; leaving it out of the snapshot", event_id, private)
        return None
    return note


_ID, _CHURCH, _TYPE, _KIND, _DAY, _DATE, _START = range(7)
_CANCELLED = EVENT_COLUMNS.index("cancelled")
_CANCELS = EVENT_COLUMNS.index("cancels_event_id")
_WEEKS = EVENT_COLUMNS.index("weeks_of_month")
_EXCLUDE_WEEKS = EVENT_COLUMNS.index("exclude_weeks")
_VALID_FROM = EVENT_COLUMNS.index("valid_from")
_VALID_UNTIL = EVENT_COLUMNS.index("valid_until")
_SEASON = slice(EVENT_COLUMNS.index("season_start_month"), EVENT_COLUMNS.index("season_end_day") + 1)


def finish_events(rows: list[tuple], build_date: date) -> list[tuple]:
    """Drop past dated rows, match each cancellation to the weekly row it cancels, sort by id.

    A cancelled dated row cancels the weekly row with the same church, event
    type and start time on its date's weekday, whose weeks of the month and
    season include that date. One that matches nothing is left out (cancelled
    rows are hidden anyway). The identity rules allow at most one matching
    recurrence; should two match, the lowest id is named.
    """
    today = build_date.isoformat()
    rows = [r for r in rows if (
        (r[_KIND] != "specific_date" or (r[_DATE] or "") >= today)
        and (r[_VALID_UNTIL] is None or r[_VALID_UNTIL] >= today)
    )]
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
                and (candidate[_VALID_FROM] is None or candidate[_VALID_FROM] <= row[_DATE])
                and (candidate[_VALID_UNTIL] is None or candidate[_VALID_UNTIL] >= row[_DATE])
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
            WITH latest AS ({_LATEST_BULLETIN}), sourced AS ({_LATEST_SOURCE_SEED})
            SELECT c.id, c.parish_id, c.slug, c.name, c.address_line1, c.address_line2,
                   c.city, c.state, c.postal_code, c.latitude, c.longitude,
                   p.homepage_url,
                   -- A parish shown with a source has no current bulletin, whatever it
                   -- once published.
                   CASE WHEN sourced.parish_id IS NULL THEN latest.source_url END,
                   CASE WHEN sourced.parish_id IS NULL THEN latest.week END,
                   sourced.schedule_source, sourced.schedule_source_url, c.kind, sourced.as_of
            FROM church c
            LEFT JOIN parish p ON c.parish_id = p.id
            LEFT JOIN latest ON latest.parish_id = c.parish_id AND latest.rn = 1
            LEFT JOIN sourced ON sourced.parish_id = c.parish_id AND sourced.rn = 1
                AND p.bulletin_provider = '{WEBSITE_SCHEDULE}'
            WHERE c.retired_at IS NULL
            ORDER BY c.name, c.id
            """
        ).fetchall()
        seeded = {
            row[0] for row in src.execute(
                "SELECT DISTINCT parish_id FROM schedule_revision WHERE source_kind = 'seed'"
            ).fetchall()
        }
        # Only parishes with an approved seed are on the site.
        churches = [(*row[:-2], checked_on(row[-1]), row[-2] or "church")
                    for row in churches if row[1] in seeded]
        shown = {row[0] for row in churches}
        events = [
            row for row in finish_events(_schedule_events(src), build_date or date.today())
            if row[_CHURCH] in shown
        ]
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
