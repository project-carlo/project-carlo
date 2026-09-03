"""events.json to frontend snapshot, with the recurrence qualifiers intact.

The snapshot is written with a positional `INSERT INTO event VALUES (...)`, so a
column added to one schema and not the other, or added in a different order,
silently shifts every value in the row. This walks the whole path a qualifier
takes to the browser and checks it arrives on the right slot.
"""

from __future__ import annotations

import gzip
import json
import sqlite3
from pathlib import Path

import pytest

from pdf_extract import db as db_module
from pdf_extract import storage
from pdf_extract.db import create_db
from pdf_extract.extract_frontend_db import extract

BULLETIN_URL = "https://example.test/bulletin.pdf"

EVENTS = [
    {
        "church_slug": "holy-trinity", "bulletin_source_url": BULLETIN_URL,
        "event_type": "mass", "event_kind": "weekly", "day_of_week": "Sunday",
        "date": None, "start_time": "9:00 AM", "cancelled": False,
    },
    {
        "church_slug": "holy-trinity", "bulletin_source_url": BULLETIN_URL,
        "event_type": "confession", "event_kind": "weekly",
        "day_of_week": "Tuesday", "date": None, "start_time": "4:30 PM",
        "cancelled": False, "season_start_month": 10, "season_end_month": 6,
        "season_note": "October through June",
    },
    {
        "church_slug": "holy-trinity", "bulletin_source_url": BULLETIN_URL,
        "event_type": "mass", "event_kind": "weekly", "day_of_week": "Thursday",
        "date": None, "start_time": "8:30 AM", "cancelled": False,
        "season_start_month": 6, "season_start_day": 4,
        "season_end_month": 9, "season_end_day": 10,
        "season_note": "June 4 - September 10",
    },
    {
        "church_slug": "holy-trinity", "bulletin_source_url": BULLETIN_URL,
        "event_type": "adoration", "event_kind": "weekly",
        "day_of_week": "Friday", "date": None, "start_time": "7:00 PM",
        "cancelled": False, "weeks_of_month": ["first"],
        "note": "ends with Benediction",
    },
    {
        "church_slug": "holy-trinity", "bulletin_source_url": BULLETIN_URL,
        "event_type": "mass", "event_kind": "specific_date", "day_of_week": None,
        "date": "2026-09-04", "start_time": "8:00 AM", "cancelled": False,
        # A dated occurrence cannot recur, so a qualifier on one is meaningless.
        "weeks_of_month": ["first"], "season_start_month": 10,
        "season_end_month": 6, "season_note": "October through June",
    },
]


@pytest.fixture
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A minimal one-parish corpus in place of the repository's data/ files."""
    (tmp_path / "parishes.csv").write_text(
        "slug,name,website,bulletin_provider,provider_id\n"
        "webster,Webster Parish,https://example.test,ecatholic,\n",
        encoding="utf-8",
    )
    (tmp_path / "churches.csv").write_text(
        "parish_id,slug,name,line1,line2,city,state,postal_code,"
        "name_verified,address_verified,latitude,longitude\n"
        "webster,holy-trinity,Holy Trinity Church,1460 Ridge Road,,Webster,NY,"
        "14580,,,43.2145951,-77.4162619\n",
        encoding="utf-8",
    )
    (tmp_path / "metadata.json").write_text(json.dumps([{
        "parish_slug": "webster",
        "source_url": BULLETIN_URL,
        "pdf_path": "bulletin.pdf",
        "content_hash": "abc",
        "fetched_at": "2026-08-30T00:00:00Z",
        "processed_at": "2026-08-30T01:00:00Z",
        "published_date": "2026-08-30",
    }]), encoding="utf-8")
    (tmp_path / "events.json").write_text(json.dumps(EVENTS), encoding="utf-8")

    monkeypatch.setattr(storage, "PARISHES_CSV_PATH", tmp_path / "parishes.csv")
    monkeypatch.setattr(db_module, "CHURCHES_CSV_PATH", tmp_path / "churches.csv")
    monkeypatch.setattr(db_module, "BULLETINS_METADATA_PATH", tmp_path / "metadata.json")
    monkeypatch.setattr(db_module, "EVENTS_PATH", tmp_path / "events.json")
    return tmp_path


def _snapshot_events(data_dir: Path) -> dict[str, sqlite3.Row]:
    """Build the DB and the frontend snapshot, keyed by weekday or date."""
    source = data_dir / "parish_events.db"
    create_db(source)
    dest = data_dir / "frontend.snapshot"
    extract(source=source, dest=dest)

    unpacked = data_dir / "frontend.db"
    unpacked.write_bytes(gzip.decompress(dest.read_bytes()))
    conn = sqlite3.connect(unpacked)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("SELECT * FROM event").fetchall()
    finally:
        conn.close()
    return {str(row["day_of_week"] or row["date"]): row for row in rows}


def test_qualifiers_reach_the_snapshot(data_dir: Path) -> None:
    rows = _snapshot_events(data_dir)
    assert set(rows) == {"Sunday", "Tuesday", "Thursday", "Friday", "2026-09-04"}

    plain = rows["Sunday"]
    assert plain["weeks_of_month"] is None
    assert plain["season_start_month"] is None
    assert plain["season_end_month"] is None
    assert plain["season_note"] is None

    seasonal = rows["Tuesday"]
    assert seasonal["event_type"] == "confession"
    assert seasonal["start_time"] == 16 * 60 + 30
    assert seasonal["weeks_of_month"] is None
    assert seasonal["season_start_month"] == 10
    assert seasonal["season_end_month"] == 6
    # No day either side; the bulletin ranged whole months and is quoted so.
    assert seasonal["season_start_day"] is None
    assert seasonal["season_end_day"] is None
    assert seasonal["season_note"] == "October through June"

    dated_season = rows["Thursday"]
    assert dated_season["season_start_month"] == 6
    assert dated_season["season_start_day"] == 4
    assert dated_season["season_end_month"] == 9
    assert dated_season["season_end_day"] == 10
    assert dated_season["season_note"] == "June 4 - September 10"

    monthly = rows["Friday"]
    assert monthly["weeks_of_month"] == "first"
    assert monthly["season_start_month"] is None
    # Nothing to caption: "First Friday of the month" derives from the column.
    assert monthly["season_note"] is None
    assert monthly["note"] == "ends with Benediction"


def test_dated_events_are_never_qualified(data_dir: Path) -> None:
    dated = _snapshot_events(data_dir)["2026-09-04"]
    assert dated["event_kind"] == "specific_date"
    assert dated["weeks_of_month"] is None
    assert dated["season_start_month"] is None
    assert dated["season_end_month"] is None
    assert dated["season_note"] is None
