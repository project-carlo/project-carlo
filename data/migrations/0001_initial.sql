-- Project Carlo database schema, version 1.
--
-- Migrations in this directory are applied in filename order by
-- `pdf_extract.db.migrate`, which records progress in PRAGMA user_version.
-- Never edit a migration that has shipped: add the next numbered file instead.

PRAGMA foreign_keys = ON;

-- Curated reference data: seeded from data/parishes.csv and data/churches.csv
-- (the source of truth for these two tables) on every pipeline command.
CREATE TABLE parish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    homepage_url TEXT NOT NULL,
    bulletin_provider TEXT,
    provider_id TEXT,
    created_at TEXT
);

CREATE TABLE church (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    address_line1 TEXT,
    address_line2 TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    latitude REAL,
    longitude REAL,
    name_verified INTEGER NOT NULL DEFAULT 0,
    address_verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT
);

CREATE INDEX idx_church_parish_name ON church(parish_id, name);
CREATE INDEX idx_church_lat_lng ON church(latitude, longitude);

-- Observed data: written by the pipeline, published as a versioned database.

-- One row per bulletin PDF ever fetched. The PDF itself lives in the blob
-- store at bulletins/<parish slug>/<content_hash>.pdf.
CREATE TABLE bulletin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    source_url TEXT NOT NULL,
    content_hash TEXT,
    published_date TEXT,
    fetched_at TEXT,
    processed_at TEXT,
    UNIQUE(parish_id, source_url)
);

CREATE INDEX idx_bulletin_parish_processed ON bulletin(parish_id, processed_at);

-- Events extracted from each bulletin. Rows of superseded bulletins are kept:
-- the frontend snapshot reads only each parish's latest bulletin, and the
-- older rows are what week-over-week change reports compare against.
CREATE TABLE event (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    church_id INTEGER NOT NULL REFERENCES church(id) ON DELETE CASCADE,
    bulletin_id INTEGER NOT NULL REFERENCES bulletin(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_kind TEXT NOT NULL,
    day_of_week TEXT,
    date TEXT,
    start_time INTEGER NOT NULL CHECK (start_time BETWEEN 0 AND 1439),
    end_time INTEGER CHECK (end_time IS NULL OR end_time BETWEEN 0 AND 1439),
    cancelled INTEGER NOT NULL DEFAULT 0 CHECK (cancelled IN (0, 1)),
    page_number INTEGER,              -- 1-indexed page of source PDF
    note TEXT                         -- optional special context (e.g. language, seasonal)
);

CREATE INDEX idx_event_bulletin ON event(bulletin_id);
CREATE INDEX idx_event_church ON event(church_id);

-- Every (slot, date) the weekly-recurrence detector has seen. Keyed by church
-- slug rather than id so it survives a church being re-seeded.
CREATE TABLE event_occurrence (
    church_slug TEXT NOT NULL,
    event_type TEXT NOT NULL,
    start_time INTEGER NOT NULL,
    date TEXT NOT NULL,
    PRIMARY KEY (church_slug, event_type, start_time, date)
) WITHOUT ROWID;

-- One row per pipeline run, and what each run did for each parish.
CREATE TABLE pipeline_run (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,             -- running | passed | held | failed
    git_sha TEXT,
    trigger TEXT,
    summary_json TEXT
);

CREATE TABLE run_parish_result (
    run_id TEXT NOT NULL REFERENCES pipeline_run(id) ON DELETE CASCADE,
    parish_slug TEXT NOT NULL,
    stage TEXT NOT NULL,              -- fetch | process
    status TEXT NOT NULL,
    detail TEXT,
    source_url TEXT,
    content_hash TEXT,
    event_count INTEGER,
    PRIMARY KEY (run_id, parish_slug, stage)
);
