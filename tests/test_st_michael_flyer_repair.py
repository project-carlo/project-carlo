import shutil
from datetime import date

import pytest

from pdf_extract.db import _migration_files, migrate
from pdf_extract.extract_frontend_db import extract, read_snapshot
from pdf_extract.storage import connect_db, insert_bulletin, latest_bulletin_ids

PARISH = "st-michael-st-peter-our-lady-of-hope-syracuse"
FLYER_HASH = "1afe3ca1dc887823f9030e44ae3f824ccc5516a4aa3ec500759b2635e5a1a59b"


@pytest.fixture
def before_repair(tmp_path):
    previous = tmp_path / "migrations"
    previous.mkdir()
    for number, path in _migration_files():
        if number < 10:
            shutil.copy(path, previous / path.name)
    db = tmp_path / "parish.db"
    conn = connect_db(db)
    migrate(conn, previous)
    with conn:
        conn.execute(
            "INSERT INTO parish(slug, name, homepage_url) VALUES (?, ?, ?)",
            (PARISH, "St. Michael & St. Peter", "https://www.stmichael-stpeter.org"),
        )
        conn.execute("INSERT INTO church(parish_id, slug, name) VALUES (1, 'church', 'Church')")
    yield conn, db
    conn.close()


def add_bulletin(conn, content_hash, published=None, *, events=False, processed=True):
    bulletin_id = insert_bulletin(
        conn,
        parish_id=1,
        source_url=f"https://example.org/{content_hash}.pdf",
        content_hash=content_hash,
        fetched_at="2026-10-25T13:25:00Z",
    )
    with conn:
        conn.execute(
            "UPDATE bulletin SET published_date = ?, processed_at = ? WHERE id = ?",
            (published, "2026-10-25T13:49:49Z" if processed else None, bulletin_id),
        )
        if events:
            conn.execute(
                "INSERT INTO event(church_id, bulletin_id, event_type, event_kind, "
                "day_of_week, start_time) VALUES (1, ?, ?, ?, ?, ?)",
                (bulletin_id, "mass", "weekly", "Sunday", 540),
            )
    return bulletin_id


@pytest.mark.parametrize("newer_issue", [False, True])
def test_repair_restores_real_schedule_and_preserves_newer_issue(before_repair, newer_issue):
    conn, db = before_repair
    real = add_bulletin(conn, "real", "2026-10-11", events=True)
    flyer = add_bulletin(conn, FLYER_HASH)
    assert latest_bulletin_ids(conn)[PARISH] == flyer
    before = extract(db, db.with_suffix(".before.gz"), build_date=date(2026, 10, 25))
    assert before["events"] == 0
    if newer_issue:
        real = add_bulletin(conn, "newer", "2026-11-01", events=True)

    assert migrate(conn) == len(_migration_files()) - 9
    assert latest_bulletin_ids(conn)[PARISH] == real
    assert conn.execute("SELECT count(*) FROM bulletin").fetchone()[0] == 2 + newer_issue
    dest = db.with_suffix(".after.gz")
    assert extract(db, dest, build_date=date(2026, 10, 25))["events"] == 1
    [church] = read_snapshot(dest.read_bytes())["churches"]
    assert church["bulletin_url"].endswith("/newer.pdf" if newer_issue else "/real.pdf")
    assert migrate(conn) == 0


@pytest.mark.parametrize("variation", ["parish", "hash", "dated", "events", "unprocessed"])
def test_repair_leaves_other_records_alone(before_repair, variation):
    conn, _ = before_repair
    bulletin = add_bulletin(
        conn,
        "different" if variation == "hash" else FLYER_HASH,
        "2026-10-25" if variation == "dated" else None,
        events=variation == "events",
        processed=variation != "unprocessed",
    )
    if variation == "parish":
        with conn:
            conn.execute("UPDATE parish SET slug = 'other-parish'")
    migrate(conn)
    assert (
        conn.execute(
            "SELECT wrong_bulletin FROM bulletin WHERE id = ?",
            (bulletin,),
        ).fetchone()[0]
        == 0
    )
