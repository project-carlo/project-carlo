import gzip
import json
from datetime import date
from pathlib import Path

import pytest

from pdf_extract.db import create_db
from pdf_extract.extract_frontend_db import (
    SNAPSHOT_VERSION,
    SnapshotFormatError,
    encode_snapshot,
    extract,
    read_snapshot,
)
from pdf_extract.storage import (
    DEFAULT_DB_PATH,
    connect_db,
    insert_bulletin,
    save_processed_bulletin,
    utc_now_iso,
)
from pdf_extract.verify_frontend_snapshot import verify_frontend_snapshot

BUILD_DATE = date(2026, 10, 1)
EVENTS = [
    {
        "church_slug": "test-church", "event_type": "mass", "event_kind": "weekly",
        "day_of_week": "Sunday", "date": None, "start_time": "10:00 AM", "end_time": None,
        "cancelled": False,
    },
    {
        "church_slug": "test-church", "event_type": "confession", "event_kind": "weekly",
        "day_of_week": "Thursday", "date": None, "start_time": "3:00 PM", "end_time": "4:00 PM",
        "cancelled": False,
    },
    {
        "church_slug": "test-church", "event_type": "confession", "event_kind": "specific_date",
        "day_of_week": None, "date": "2026-12-24", "start_time": "3:00 PM",
        "end_time": "4:00 PM", "cancelled": True, "note": "Christmas Eve",
    },
]


WEB_FIXTURE = Path(__file__).resolve().parents[1] / "apps/web/src/lib/snapshot.fixture.json"
# Nulls, strings that repeat, and a gap in the event ids.
CHURCH_ROWS = [
    (7, 1, "b", "B", None, None, "Rochester", "NY", None, 43.1, -77.6, None, None, "2026-09-20"),
    (3, 1, "a", "A", "1 Main St", None, None, "NY", "14620", None, None, "https://a", None, None),
]
# A negative id (an update-mode entry), weeks of the month, weeks excluded, a
# season that wraps the new year, and a cancellation naming a weekly row.
EVENT_ROWS = [
    (-118, 3, "mass", "weekly", "Friday", None, 0, None, 0, None, None, ["fourth", "last"],
     10, None, 6, 15, None, False),
    (10, 7, "mass", "weekly", "Sunday", None, 600, None, 0, 2, None, ["last"], None, None, None,
     None, None, True),
    (11, 3, "mass", "specific_date", None, "2026-12-25", 0, 60, 1, None, "Midnight", [], None,
     None, None, None, -118, False),
    (15, 7, "adoration", "weekly", "Friday", None, 1140, 1200, 0, 3, "Midnight", [], None, None,
     None, None, None, False),
]


def _add_bulletin(url: str, published_date: str, events: list[dict]) -> None:
    conn = connect_db()
    try:
        parish_id = conn.execute("SELECT id FROM parish WHERE slug = 'test-parish'").fetchone()[0]
        bulletin_id = insert_bulletin(
            conn, parish_id=parish_id, source_url=url, content_hash=url, fetched_at=utc_now_iso(),
        )
        save_processed_bulletin(
            conn, bulletin_id, events, processed_at=utc_now_iso(), published_date=published_date,
        )
    finally:
        conn.close()


@pytest.fixture
def db(pipeline_dir: Path) -> Path:
    create_db()
    _add_bulletin("https://example.org/old.pdf", "2026-09-13", EVENTS[:1])
    _add_bulletin("https://example.org/new.pdf", "2026-09-20", EVENTS)
    return DEFAULT_DB_PATH


def test_snapshot_has_the_latest_bulletins_churches_and_events(db: Path, tmp_path: Path) -> None:
    dest = tmp_path / "frontend.json.gz"

    result = extract(db, dest, build_date=BUILD_DATE)

    assert result["churches"] == 1
    assert result["events"] == 3
    tables = read_snapshot(dest.read_bytes())
    [church] = tables["churches"]
    assert church["slug"] == "test-church"
    assert church["city"] == "Rochester"
    assert church["address_line2"] is None
    assert church["bulletin_url"] == "https://example.org/new.pdf"
    assert church["bulletin_week"] == "2026-09-20"
    assert church["homepage_url"] == "https://example.org"
    mass, weekly_confession, confession = tables["events"]
    assert mass["id"] < confession["id"]
    assert mass["church_id"] == church["id"]
    assert (mass["event_kind"], mass["day_of_week"], mass["start_time"]) == ("weekly", "Sunday", 600)
    assert mass["end_time"] is None
    assert mass["cancelled"] is False
    assert (mass["weeks_of_month"], mass["season_start_month"]) == ([], None)
    assert (confession["date"], confession["end_time"]) == ("2026-12-24", 960)
    assert confession["cancelled"] is True
    assert confession["note"] == "Christmas Eve"
    assert confession["cancels_event_id"] == weekly_confession["id"]


def test_past_dated_rows_and_unmatched_cancellations_are_left_out(
    db: Path, tmp_path: Path,
) -> None:
    dest = tmp_path / "frontend.json.gz"

    extract(db, dest, build_date=date(2026, 12, 25))
    kinds = [e["event_kind"] for e in read_snapshot(dest.read_bytes())["events"]]

    assert kinds == ["weekly", "weekly"]


def test_a_cancellation_matching_no_weekly_row_is_left_out(
    pipeline_dir: Path, tmp_path: Path,
) -> None:
    create_db()
    _add_bulletin("https://example.org/new.pdf", "2026-09-20", [EVENTS[0], EVENTS[2]])
    dest = tmp_path / "frontend.json.gz"

    extract(DEFAULT_DB_PATH, dest, build_date=BUILD_DATE)

    assert [e["event_kind"] for e in read_snapshot(dest.read_bytes())["events"]] == ["weekly"]


def test_a_version_1_snapshot_reads_as_every_week_with_no_cancellations() -> None:
    document = json.loads(gzip.decompress(encode_snapshot(CHURCH_ROWS, EVENT_ROWS)))
    document["version"] = 1
    for name in (
        "weeks_of_month", "season_start_month", "season_start_day", "season_end_month",
        "season_end_day", "cancels_event_id",
    ):
        del document["events"][name]
    data = gzip.compress(json.dumps(document).encode())

    events = read_snapshot(data)["events"]

    assert [e["weeks_of_month"] for e in events] == [[], [], [], []]
    assert {e["season_start_month"] for e in events} == {None}
    assert {e["cancels_event_id"] for e in events} == {None}


def test_a_parish_with_no_processed_bulletin_has_no_bulletin(
    pipeline_dir: Path, tmp_path: Path,
) -> None:
    create_db()
    dest = tmp_path / "frontend.json.gz"

    extract(DEFAULT_DB_PATH, dest)

    [church] = read_snapshot(dest.read_bytes())["churches"]
    assert (church["bulletin_url"], church["bulletin_week"]) == (None, None)


def test_a_snapshot_written_before_an_added_column_reads_it_as_null() -> None:
    document = json.loads(gzip.decompress(encode_snapshot(CHURCH_ROWS, EVENT_ROWS)))
    del document["churches"]["bulletin_week"]
    del document["events"]["exclude_weeks"]
    data = gzip.compress(json.dumps(document).encode())

    tables = read_snapshot(data)
    churches = tables["churches"]

    assert [church["bulletin_week"] for church in churches] == [None, None]
    assert [church["slug"] for church in churches] == ["b", "a"]
    assert [event["exclude_weeks"] for event in tables["events"]] == [None] * 4


def test_snapshot_bytes_are_deterministic(db: Path, tmp_path: Path) -> None:
    first = tmp_path / "a.json.gz"
    second = tmp_path / "b.json.gz"
    extract(db, first)
    extract(db, second)
    assert first.read_bytes() == second.read_bytes()


def test_extract_keeps_the_previous_snapshot(db: Path, tmp_path: Path) -> None:
    dest = tmp_path / "frontend.json.gz"
    dest.write_bytes(b"previous")

    extract(db, dest, build_date=BUILD_DATE)

    assert (tmp_path / "frontend.json.gz.previous").read_bytes() == b"previous"
    assert len(read_snapshot(dest.read_bytes())["events"]) == 3


def test_encoded_columns_round_trip() -> None:
    tables = read_snapshot(encode_snapshot(CHURCH_ROWS, EVENT_ROWS))

    assert [tuple(row.values()) for row in tables["churches"]] == CHURCH_ROWS
    assert [tuple(row.values()) for row in tables["events"]] == [
        (*row[:8], bool(row[8]), *row[9:]) for row in EVENT_ROWS
    ]


def test_encoded_format_matches_the_web_apps_fixture() -> None:
    # apps/web/src/lib/snapshot.test.ts decodes the same file, so the writer and
    # the app's reader can't drift apart unnoticed.
    written = json.loads(gzip.decompress(encode_snapshot(CHURCH_ROWS, EVENT_ROWS)))
    assert written == json.loads(WEB_FIXTURE.read_text(encoding="utf-8")), (
        f"The snapshot format changed: update {WEB_FIXTURE} and snapshot.test.ts to match"
    )


@pytest.mark.parametrize(
    "data",
    [
        gzip.compress(b"SQLite format 3\x00" + bytes(84)),
        b"not gzip",
        gzip.compress(json.dumps({"version": SNAPSHOT_VERSION + 1}).encode()),
        gzip.compress(b"[]"),
    ],
    ids=["sqlite", "not-gzip", "newer-version", "not-an-object"],
)
def test_read_snapshot_rejects_other_formats(data: bytes) -> None:
    with pytest.raises(SnapshotFormatError):
        read_snapshot(data)


def test_verify_passes_for_the_same_data(db: Path, tmp_path: Path) -> None:
    extract(db, tmp_path / "previous.json.gz")
    extract(db, tmp_path / "current.json.gz")

    result = verify_frontend_snapshot(
        current=tmp_path / "current.json.gz", previous=tmp_path / "previous.json.gz",
    )

    assert result["passed"]
    assert result["churches"] == {"current": 1, "previous": 1, "passed": True}
    assert result["events"]["delta_pct"] == 0.0
    assert result["weekly_events"]["match_pct"] == 100.0


def test_verify_fails_when_weekly_events_and_churches_change(tmp_path: Path) -> None:
    church = (1, 1, "a", "A", None, None, None, None, None, None, None, None, None, None)
    other = (2, 1, "b", "B", None, None, None, None, None, None, None, None, None, None)
    weekly = [
        (i, 1, "mass", "weekly", "Sunday", None, 480 + 60 * i, None, 0, None, None,
         [], None, None, None, None, None, False)
        for i in range(1, 11)
    ]
    moved = [(*row[:6], row[6] + 15, *row[7:]) for row in weekly]
    (tmp_path / "previous.json.gz").write_bytes(encode_snapshot([church], weekly))
    (tmp_path / "current.json.gz").write_bytes(encode_snapshot([church, other], moved))

    result = verify_frontend_snapshot(
        current=tmp_path / "current.json.gz", previous=tmp_path / "previous.json.gz",
    )

    assert not result["passed"]
    assert not result["churches"]["passed"]
    assert result["events"]["passed"]
    assert result["weekly_events"]["match_pct"] == 0.0
    assert not result["weekly_events"]["passed"]


def test_verify_reports_a_missing_snapshot(tmp_path: Path) -> None:
    result = verify_frontend_snapshot(
        current=tmp_path / "current.json.gz", previous=tmp_path / "previous.json.gz",
    )
    assert not result["passed"]
    assert result["errors"] == [f"Snapshot not found: {tmp_path / 'current.json.gz'}"]
