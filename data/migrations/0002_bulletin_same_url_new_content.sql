-- A parish can publish every week's bulletin at the same address
-- ("/bulletin.pdf", overwritten each week). Key a bulletin by its content as
-- well as its address, so a new issue there is a new row, not a duplicate.
--
-- SQLite cannot drop a UNIQUE constraint in place, so the table is rebuilt.
-- `migrate` runs migrations with foreign keys off, so dropping the old table
-- does not cascade into `event`, and checks them before committing.

CREATE TABLE bulletin_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    source_url TEXT NOT NULL,
    content_hash TEXT,
    published_date TEXT,
    fetched_at TEXT,
    processed_at TEXT,
    UNIQUE(parish_id, source_url, content_hash)
);

INSERT INTO bulletin_new (id, parish_id, source_url, content_hash, published_date, fetched_at, processed_at)
SELECT id, parish_id, source_url, content_hash, published_date, fetched_at, processed_at FROM bulletin;

DROP TABLE bulletin;
ALTER TABLE bulletin_new RENAME TO bulletin;

CREATE INDEX idx_bulletin_parish_processed ON bulletin(parish_id, processed_at);
