"""Migration 13 removes the Discover Mass cap page stored as 66 parishes' bulletin."""

import shutil
from datetime import date

import pytest

from pdf_extract.bulletin_week import stale_parishes
from pdf_extract.db import _migration_files, migrate
from pdf_extract.storage import MIGRATIONS_DIR, connect_db, insert_bulletin, load_bulletins

CAP_HASH = "df175220b1d967b5204b2dea47961626b06f0e346a6a4e54094544af84ae0117"
PARISHES = ("only-the-page", "had-a-real-one", "page-with-events")


@pytest.fixture
def before_cleanup(tmp_path):
    previous = tmp_path / "migrations"
    previous.mkdir()
    # Every file of the earlier migrations, with 12's JSON beside its script.
    for path in MIGRATIONS_DIR.glob("[0-9]*_*"):
        if int(path.name.split("_", 1)[0]) < 13:
            shutil.copy(path, previous / path.name)
    conn = connect_db(tmp_path / "parish.db")
    migrate(conn, previous)
    with conn:
        for slug in PARISHES:
            conn.execute(
                "INSERT INTO parish(slug, name, homepage_url) VALUES (?, ?, ?)",
                (slug, slug, f"https://{slug}.org"),
            )
        conn.execute("INSERT INTO church(parish_id, slug, name) VALUES (3, 'church', 'Church')")
    yield conn
    conn.close()


def add_bulletin(conn, parish_id, content_hash, *, fetched_at="2026-10-25T13:16:38Z"):
    return insert_bulletin(
        conn, parish_id=parish_id, content_hash=content_hash, fetched_at=fetched_at,
        source_url=f"https://bulletins.discovermass.com/download.php?bulletin={content_hash}",
    )


def test_the_cap_page_stops_being_any_parishs_bulletin(before_cleanup):
    conn = before_cleanup
    add_bulletin(conn, 1, CAP_HASH)
    real = add_bulletin(conn, 2, "real", fetched_at="2026-10-18T13:00:00Z")
    add_bulletin(conn, 2, CAP_HASH)
    kept = add_bulletin(conn, 3, CAP_HASH)
    with conn:
        conn.execute(
            "INSERT INTO event(church_id, bulletin_id, event_type, event_kind, day_of_week,"
            " start_time) VALUES (1, ?, 'mass', 'weekly', 'Sunday', 540)",
            (kept,),
        )
    # Fresh by its fetch date, so the parish is not fetched again in earnest.
    fresh = stale_parishes(load_bulletins(conn), PARISHES, today=date(2026, 11, 1))
    assert "only-the-page" not in fresh

    assert migrate(conn) == len(_migration_files()) - 12

    rows = {b["id"]: b for b in load_bulletins(conn)}
    assert rows.keys() == {real, kept}
    # A row something refers to is flagged rather than left dangling.
    assert rows[kept]["wrong_bulletin"] == 1
    assert rows[real]["wrong_bulletin"] == 0
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    stale = stale_parishes(rows.values(), PARISHES, today=date(2026, 11, 8))
    assert stale["only-the-page"] is None
    assert stale["page-with-events"] is None
    assert stale["had-a-real-one"]["id"] == real
    assert migrate(conn) == 0
