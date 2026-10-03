import sqlite3
from pathlib import Path

import pytest

from pdf_extract.db import (
    DatabaseMissingError,
    _migration_files,
    create_db,
    ensure_db,
    migrate,
    schema_version,
    seed_reference_data,
)
from pdf_extract.storage import (
    CHURCHES_CSV_PATH,
    DEFAULT_DB_PATH,
    MIGRATIONS_DIR,
    PARISHES_CSV_PATH,
    connect_db,
    insert_bulletin,
    save_processed_bulletin,
)
from tests.conftest import CHURCH_FIELDS, PARISH_FIELDS, write_csv

OBSERVED_TABLES = ("bulletin", "event", "event_occurrence", "pipeline_run", "run_parish_result")

TEST_PARISH = {"slug": "test-parish", "name": "Test Parish", "website": "https://example.org"}
OTHER_PARISH = {"slug": "other-parish", "name": "Other Parish", "website": "https://other.org"}
TEST_CHURCH = {
    "parish_id": "test-parish", "slug": "test-church", "name": "Test Church",
    "line1": "1 Main St", "city": "Rochester", "state": "NY", "postal_code": "14620",
}
SECOND_CHURCH = {**TEST_CHURCH, "slug": "second-church", "name": "Second Church"}
OTHER_CHURCH = {**TEST_CHURCH, "parish_id": "other-parish", "slug": "other-church",
                "name": "Other Church"}

EVENT_ROW = {
    "event_type": "mass", "event_kind": "weekly", "day_of_week": "Sunday", "date": None,
    "start_time": "9:00 AM", "end_time": None, "cancelled": False,
}


def _count_migrations() -> int:
    return len(list(MIGRATIONS_DIR.glob("*.sql")))


def _count(conn: sqlite3.Connection, table: str) -> int:
    return conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0]


def _write_reference(parishes: list[dict[str, str]], churches: list[dict[str, str]]) -> None:
    write_csv(PARISHES_CSV_PATH, PARISH_FIELDS, parishes)
    write_csv(CHURCHES_CSV_PATH, CHURCH_FIELDS, churches)


def _add_processed_bulletin(
    conn: sqlite3.Connection, parish_slug: str, church_slugs: list[str],
) -> int:
    parish_id = conn.execute(
        "SELECT id FROM parish WHERE slug = ?", (parish_slug,)
    ).fetchone()["id"]
    bulletin_id = insert_bulletin(
        conn, parish_id=parish_id, source_url=f"https://example.org/{parish_slug}.pdf",
        content_hash="h", fetched_at="2026-09-20T00:00:00Z",
    )
    save_processed_bulletin(
        conn, bulletin_id, [{**EVENT_ROW, "church_slug": slug} for slug in church_slugs],
        processed_at="2026-09-20T00:00:00Z", published_date="2026-09-20",
    )
    return bulletin_id


# ── Migrations ──────────────────────────────────────────────────────────────
def test_migrate_empty_db_sets_user_version_and_is_idempotent(tmp_path: Path) -> None:
    conn = connect_db(tmp_path / "x.db")
    try:
        assert schema_version(conn) == 0
        assert migrate(conn) == _count_migrations()
        assert schema_version(conn) == _count_migrations()
        assert migrate(conn) == 0
        assert schema_version(conn) == _count_migrations()
    finally:
        conn.close()


def test_migrate_refuses_database_newer_than_checkout(tmp_path: Path) -> None:
    conn = connect_db(tmp_path / "x.db")
    try:
        conn.execute(f"PRAGMA user_version = {_count_migrations() + 1}")
        with pytest.raises(RuntimeError, match="pull the latest code"):
            migrate(conn)
    finally:
        conn.close()


def test_migrate_applies_only_pending_migrations(tmp_path: Path) -> None:
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "0001_a.sql").write_text("CREATE TABLE a(x);", encoding="utf-8")
    conn = connect_db(tmp_path / "x.db")
    try:
        assert migrate(conn, migrations) == 1
        (migrations / "0002_b.sql").write_text("CREATE TABLE b(x);", encoding="utf-8")
        assert migrate(conn, migrations) == 1
        assert schema_version(conn) == 2
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
        assert {"a", "b"} <= tables
    finally:
        conn.close()


def test_failed_migration_leaves_previous_version(tmp_path: Path) -> None:
    migrations = tmp_path / "migrations"
    migrations.mkdir()
    (migrations / "0001_a.sql").write_text("CREATE TABLE a(x);", encoding="utf-8")
    (migrations / "0002_b.sql").write_text(
        "CREATE TABLE b(x);\nTHIS IS NOT SQL;", encoding="utf-8",
    )
    db_path = tmp_path / "x.db"
    conn = connect_db(db_path)
    try:
        with pytest.raises(sqlite3.OperationalError):
            migrate(conn, migrations)
    finally:
        conn.close()

    conn = connect_db(db_path)
    try:
        assert schema_version(conn) == 1
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
        assert "a" in tables
        assert "b" not in tables
    finally:
        conn.close()


def test_migration_files_are_numbered_in_order(tmp_path: Path) -> None:
    (tmp_path / "0002_second.sql").write_text("", encoding="utf-8")
    (tmp_path / "0001_first.sql").write_text("", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("", encoding="utf-8")

    assert _migration_files(tmp_path) == [
        (1, tmp_path / "0001_first.sql"),
        (2, tmp_path / "0002_second.sql"),
    ]


def test_migration_files_reject_gaps(tmp_path: Path) -> None:
    (tmp_path / "0001_first.sql").write_text("", encoding="utf-8")
    (tmp_path / "0003_third.sql").write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="without gaps"):
        _migration_files(tmp_path)


def test_migration_files_reject_unnumbered_names(tmp_path: Path) -> None:
    (tmp_path / "initial.sql").write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="must start with a number"):
        _migration_files(tmp_path)


def test_repository_migrations_are_valid() -> None:
    files = _migration_files()
    assert [n for n, _ in files] == list(range(1, _count_migrations() + 1))


# ── Creating and opening ────────────────────────────────────────────────────
def test_create_db_has_reference_data_and_empty_observed_tables(pipeline_dir: Path) -> None:
    result = create_db()

    assert result["db_path"] == str(DEFAULT_DB_PATH)
    assert result["migrations_applied"] == _count_migrations()
    assert result["parishes_upserted"] == 1
    assert result["churches_upserted"] == 1
    conn = connect_db()
    try:
        assert schema_version(conn) == _count_migrations()
        assert _count(conn, "parish") == 1
        assert _count(conn, "church") == 1
        for table in OBSERVED_TABLES:
            assert _count(conn, table) == 0, table
    finally:
        conn.close()


def test_create_db_replaces_existing_database(pipeline_dir: Path) -> None:
    create_db()
    conn = connect_db()
    try:
        _add_processed_bulletin(conn, "test-parish", ["test-church"])
    finally:
        conn.close()

    create_db()

    conn = connect_db()
    try:
        assert _count(conn, "bulletin") == 0
        assert _count(conn, "event") == 0
    finally:
        conn.close()


def test_ensure_db_raises_when_database_is_missing(pipeline_dir: Path) -> None:
    with pytest.raises(DatabaseMissingError, match="data:pull"):
        ensure_db()
    assert not DEFAULT_DB_PATH.exists()


def test_ensure_db_reseeds_existing_database(pipeline_dir: Path) -> None:
    create_db()
    _write_reference([TEST_PARISH], [TEST_CHURCH, SECOND_CHURCH])

    result = ensure_db()

    assert result["migrations_applied"] == 0
    assert result["churches_upserted"] == 2


# ── Seeding reference data ──────────────────────────────────────────────────
def test_seed_updates_rows_in_place_keeping_ids(pipeline_dir: Path) -> None:
    create_db()
    conn = connect_db()
    try:
        parish_id = conn.execute("SELECT id FROM parish").fetchone()["id"]
        church_id = conn.execute("SELECT id FROM church").fetchone()["id"]
        bulletin_id = _add_processed_bulletin(conn, "test-parish", ["test-church"])

        _write_reference(
            [{**TEST_PARISH, "name": "Renamed Parish", "bulletin_provider": "ecatholic"}],
            [{**TEST_CHURCH, "name": "Renamed Church", "latitude": "43.1",
              "longitude": "-77.6", "name_verified": "true"}],
        )
        stats = seed_reference_data(conn)

        assert stats["parishes_upserted"] == 1
        assert stats["churches_upserted"] == 1
        assert stats["parishes_deleted"] == stats["churches_deleted"] == 0
        parish = conn.execute("SELECT * FROM parish").fetchone()
        church = conn.execute("SELECT * FROM church").fetchone()
        assert (parish["id"], parish["name"], parish["bulletin_provider"]) == (
            parish_id, "Renamed Parish", "ecatholic",
        )
        assert (church["id"], church["name"]) == (church_id, "Renamed Church")
        assert (church["latitude"], church["longitude"]) == (43.1, -77.6)
        assert (church["name_verified"], church["address_verified"]) == (1, 0)
        # Observed data referencing the rows survives the update.
        assert _count(conn, "event") == 1
        assert conn.execute("SELECT parish_id FROM bulletin WHERE id = ?",
                            (bulletin_id,)).fetchone()[0] == parish_id
    finally:
        conn.close()


def test_seed_deletes_removed_church_with_its_events(pipeline_dir: Path) -> None:
    _write_reference([TEST_PARISH], [TEST_CHURCH, SECOND_CHURCH])
    create_db()
    conn = connect_db()
    try:
        _add_processed_bulletin(conn, "test-parish", ["test-church", "second-church"])
        assert _count(conn, "event") == 2

        _write_reference([TEST_PARISH], [TEST_CHURCH])
        stats = seed_reference_data(conn)

        assert stats["churches_deleted"] == 1
        assert [r["slug"] for r in conn.execute("SELECT slug FROM church")] == ["test-church"]
        remaining = conn.execute(
            "SELECT c.slug FROM event e JOIN church c ON c.id = e.church_id"
        ).fetchall()
        assert [r["slug"] for r in remaining] == ["test-church"]
        assert _count(conn, "bulletin") == 1
    finally:
        conn.close()


def test_seed_deletes_removed_parish_with_its_bulletins(pipeline_dir: Path) -> None:
    _write_reference([TEST_PARISH, OTHER_PARISH], [TEST_CHURCH, OTHER_CHURCH])
    create_db()
    conn = connect_db()
    try:
        _add_processed_bulletin(conn, "test-parish", ["test-church"])
        _add_processed_bulletin(conn, "other-parish", ["other-church"])

        _write_reference([TEST_PARISH], [TEST_CHURCH])
        stats = seed_reference_data(conn)

        assert stats["parishes_deleted"] == 1
        # other-church goes with its parish by cascade, before the church pass.
        assert stats["churches_deleted"] == 0
        assert [r["slug"] for r in conn.execute("SELECT slug FROM parish")] == ["test-parish"]
        assert [r["slug"] for r in conn.execute("SELECT slug FROM church")] == ["test-church"]
        bulletins = conn.execute(
            "SELECT p.slug FROM bulletin b JOIN parish p ON p.id = b.parish_id"
        ).fetchall()
        assert [r["slug"] for r in bulletins] == ["test-parish"]
        assert _count(conn, "event") == 1
    finally:
        conn.close()


def test_seed_skips_church_naming_unknown_parish(pipeline_dir: Path) -> None:
    _write_reference(
        [TEST_PARISH],
        [TEST_CHURCH, {**TEST_CHURCH, "parish_id": "no-such-parish", "slug": "orphan"}],
    )

    stats = create_db()

    assert stats["churches_upserted"] == 1
    assert stats["churches_skipped"] == 1
    conn = connect_db()
    try:
        assert [r["slug"] for r in conn.execute("SELECT slug FROM church")] == ["test-church"]
    finally:
        conn.close()


def test_seed_removed_parish_takes_its_still_listed_church_with_it(pipeline_dir: Path) -> None:
    _write_reference([TEST_PARISH, OTHER_PARISH], [TEST_CHURCH, OTHER_CHURCH])
    create_db()
    conn = connect_db()
    try:
        _write_reference([TEST_PARISH], [TEST_CHURCH, OTHER_CHURCH])
        seed_reference_data(conn)

        assert [r["slug"] for r in conn.execute("SELECT slug FROM church")] == ["test-church"]
    finally:
        conn.close()


def test_seed_counts_church_of_removed_parish_as_skipped(pipeline_dir: Path) -> None:
    _write_reference([TEST_PARISH, OTHER_PARISH], [TEST_CHURCH, OTHER_CHURCH])
    create_db()
    conn = connect_db()
    try:
        _write_reference([TEST_PARISH], [TEST_CHURCH, OTHER_CHURCH])
        stats = seed_reference_data(conn)
    finally:
        conn.close()

    # The parish is deleted first (its church goes with it by cascade), so the
    # church still listed in churches.csv names an unknown parish and is skipped.
    assert stats["parishes_deleted"] == 1
    assert stats["churches_upserted"] == 1
    assert stats["churches_skipped"] == 1
    assert stats["churches_deleted"] == 0


def test_seed_rejects_csv_missing_required_columns(pipeline_dir: Path) -> None:
    write_csv(PARISHES_CSV_PATH, ["slug", "name"], [{"slug": "p", "name": "P"}])

    with pytest.raises(ValueError, match="missing required columns"):
        create_db()


def test_seed_refuses_to_run_without_the_csvs(pipeline_dir: Path) -> None:
    """A missing CSV must not read as "every parish was removed"."""
    create_db()
    PARISHES_CSV_PATH.unlink()
    conn = connect_db()
    try:
        with pytest.raises(FileNotFoundError, match="parishes.csv"):
            seed_reference_data(conn)
        assert _count(conn, "parish") == 1
    finally:
        conn.close()


def test_bulletin_rebuild_keeps_events_and_allows_a_reissued_address(tmp_path: Path) -> None:
    first_only = tmp_path / "migrations"
    first_only.mkdir()
    (first_only / "0001_initial.sql").write_text(
        (MIGRATIONS_DIR / "0001_initial.sql").read_text(encoding="utf-8"), encoding="utf-8",
    )
    conn = connect_db(tmp_path / "x.db")
    try:
        migrate(conn, first_only)
        with conn:
            conn.execute(
                "INSERT INTO parish(slug, name, homepage_url) VALUES ('p', 'P', 'https://p.org')"
            )
            conn.execute("INSERT INTO church(parish_id, slug, name) VALUES (1, 'c', 'C')")
            conn.execute(
                "INSERT INTO bulletin(parish_id, source_url, content_hash) "
                "VALUES (1, 'https://p.org/bulletin.pdf', 'h1')"
            )
            conn.execute(
                "INSERT INTO event(church_id, bulletin_id, event_type, event_kind, start_time) "
                "VALUES (1, 1, 'mass', 'weekly', 540)"
            )

        assert migrate(conn) == _count_migrations() - 1

        assert _count(conn, "event") == 1
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        insert_bulletin(
            conn, parish_id=1, source_url="https://p.org/bulletin.pdf",
            content_hash="h2", fetched_at="2026-10-04T00:00:00Z",
        )
        assert [r[0] for r in conn.execute("SELECT id FROM bulletin ORDER BY id")] == [1, 2]
        with pytest.raises(sqlite3.IntegrityError):
            insert_bulletin(
                conn, parish_id=1, source_url="https://p.org/bulletin.pdf",
                content_hash="h2", fetched_at="2026-10-04T00:00:00Z",
            )
    finally:
        conn.close()
