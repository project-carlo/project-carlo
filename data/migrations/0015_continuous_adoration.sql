-- Chapels open 24 hours (issue #111; docs/believed-schedules.md, "Chapels open
-- 24 hours"). A standing Adoration chapel, open every day around the clock, is
-- one `continuous` entry with no day, date or times. `access` says how a
-- visitor gets in, and `open_from`/`open_until` (minutes after midnight) the
-- hours it is unlocked when a door code is needed at the others. The site words
-- these itself, so no contact or code is ever stored for them.
--
-- A continuous entry may have valid_from/valid_until, as a weekly one may: a
-- closure ends one entry and a reopening starts another.
--
-- SQLite can't change a CHECK in place, so the table is rebuilt (foreign keys
-- are off while migrations run; the rows keep their ids and hashes).

CREATE TABLE schedule_entry_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,        -- sha256 of every column below
    identity_key TEXT NOT NULL,       -- what makes two entries the same slot (below)
    -- Cascades only when the church's whole parish is removed: a church on its
    -- own is retired instead (church.retired_at).
    church_id INTEGER NOT NULL REFERENCES church(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL CHECK (event_type IN ('mass', 'confession', 'adoration')),
    event_kind TEXT NOT NULL CHECK (event_kind IN ('weekly', 'specific_date', 'continuous')),
    day_of_week TEXT CHECK (day_of_week IN
        ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    date TEXT,                        -- ISO date, specific_date only
    -- null for a continuous entry only
    start_time INTEGER CHECK (start_time BETWEEN 0 AND 1439),
    end_time INTEGER CHECK (end_time IS NULL OR end_time BETWEEN 0 AND 1439),
    cancelled INTEGER NOT NULL DEFAULT 0 CHECK (cancelled IN (0, 1)),
    -- weeks of the month, as the labels' list: bit 0 first, 1 second, 2 third,
    -- 3 fourth, 4 fifth, 5 last. 0 = every week. Bit 6 (the labels'
    -- `exclude_weeks`): the listed weeks are the ones skipped, so it needs
    -- at least one of them.
    weeks_of_month INTEGER NOT NULL DEFAULT 0 CHECK (
        weeks_of_month BETWEEN 0 AND 127 AND weeks_of_month <> 64
    ),
    -- season, as the labels' object: months 1-12, days null or a day of that month
    season_start_month INTEGER CHECK (season_start_month BETWEEN 1 AND 12),
    season_start_day INTEGER CHECK (season_start_day BETWEEN 1 AND 31),
    season_end_month INTEGER CHECK (season_end_month BETWEEN 1 AND 12),
    season_end_day INTEGER CHECK (season_end_day BETWEEN 1 AND 31),
    note TEXT,
    -- Inclusive absolute dates for announced changes, weekly or continuous.
    valid_from TEXT CHECK (valid_from IS NULL
        OR (event_kind IN ('weekly', 'continuous') AND date(valid_from) = valid_from)),
    valid_until TEXT CHECK (valid_until IS NULL
        OR (event_kind IN ('weekly', 'continuous') AND date(valid_until) = valid_until)),
    -- continuous only: how a visitor gets in, and the unlocked hours of a
    -- chapel that needs a code at the others.
    access TEXT CHECK (access IN ('not_stated', 'code_after_hours', 'code', 'arrangement')),
    open_from INTEGER CHECK (open_from BETWEEN 0 AND 1439),
    open_until INTEGER CHECK (open_until BETWEEN 0 AND 1439),
    CHECK ((event_kind = 'weekly' AND day_of_week IS NOT NULL AND date IS NULL)
        OR (event_kind = 'specific_date' AND date IS NOT NULL AND day_of_week IS NULL)
        OR (event_kind = 'continuous' AND date IS NULL AND day_of_week IS NULL)),
    CHECK (event_kind = 'weekly' OR (weeks_of_month = 0 AND season_start_month IS NULL)),
    CHECK (event_kind = 'specific_date' OR cancelled = 0),
    CHECK ((season_start_month IS NULL) = (season_end_month IS NULL)),
    CHECK (season_start_day IS NULL OR season_start_month IS NOT NULL),
    CHECK (season_end_day IS NULL OR season_end_month IS NOT NULL),
    CHECK ((event_kind = 'continuous') = (start_time IS NULL)),
    CHECK ((event_kind = 'continuous') = (access IS NOT NULL)),
    CHECK (event_kind <> 'continuous' OR (event_type = 'adoration' AND end_time IS NULL)),
    CHECK ((open_from IS NULL) = (open_until IS NULL)),
    CHECK (open_from IS NULL OR (access = 'code_after_hours' AND open_from <> open_until))
);

INSERT INTO schedule_entry_new (
    id, hash, identity_key, church_id, event_type, event_kind, day_of_week, date,
    start_time, end_time, cancelled, weeks_of_month, season_start_month, season_start_day,
    season_end_month, season_end_day, note, valid_from, valid_until
)
SELECT id, hash, identity_key, church_id, event_type, event_kind, day_of_week, date,
       start_time, end_time, cancelled, weeks_of_month, season_start_month, season_start_day,
       season_end_month, season_end_day, note, valid_from, valid_until
FROM schedule_entry;
DROP TABLE schedule_entry;
ALTER TABLE schedule_entry_new RENAME TO schedule_entry;

-- The extraction's events (the labeler's demo database writes them) gain the
-- same columns, so an extracted chapel is stored as one row too.
CREATE TABLE event_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    church_id INTEGER NOT NULL REFERENCES church(id) ON DELETE CASCADE,
    bulletin_id INTEGER NOT NULL REFERENCES bulletin(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_kind TEXT NOT NULL,
    day_of_week TEXT,
    date TEXT,
    start_time INTEGER CHECK (start_time BETWEEN 0 AND 1439),  -- null when continuous
    end_time INTEGER CHECK (end_time IS NULL OR end_time BETWEEN 0 AND 1439),
    cancelled INTEGER NOT NULL DEFAULT 0 CHECK (cancelled IN (0, 1)),
    page_number INTEGER,              -- 1-indexed page of source PDF
    note TEXT,                        -- optional special context (e.g. language, seasonal)
    access TEXT CHECK (access IN ('not_stated', 'code_after_hours', 'code', 'arrangement')),
    open_from INTEGER CHECK (open_from BETWEEN 0 AND 1439),
    open_until INTEGER CHECK (open_until BETWEEN 0 AND 1439),
    CHECK ((event_kind = 'continuous') = (start_time IS NULL))
);
INSERT INTO event_new (
    id, church_id, bulletin_id, event_type, event_kind, day_of_week, date, start_time,
    end_time, cancelled, page_number, note
)
SELECT id, church_id, bulletin_id, event_type, event_kind, day_of_week, date, start_time,
       end_time, cancelled, page_number, note
FROM event;
DROP TABLE event;
ALTER TABLE event_new RENAME TO event;
CREATE INDEX idx_event_bulletin ON event(bulletin_id);
CREATE INDEX idx_event_church ON event(church_id);

-- A church row is a place of public Mass, or a parish's Adoration chapel at an
-- address of its own (`adoration_chapel`), from churches.csv's `kind`.
ALTER TABLE church ADD COLUMN kind TEXT NOT NULL DEFAULT 'church'
    CHECK (kind IN ('church', 'adoration_chapel'));
