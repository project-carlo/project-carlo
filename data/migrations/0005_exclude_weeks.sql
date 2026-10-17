-- A weekly slot can skip weeks of the month as well as keep them: "every
-- Sunday except the last" can't be written as the weeks that remain, since
-- the last Sunday is the fourth in some months and the fifth in others.
-- `schedule_entry.weeks_of_month` gains bit 6: set, the listed weeks are the
-- ones the slot skips (`schedule.qualifiers.weeks_to_mask`). Existing values
-- keep their meaning and their hashes.
--
-- SQLite can't change a CHECK in place, so the table is rebuilt (foreign keys
-- are off while migrations run; the rows keep their ids).

CREATE TABLE schedule_entry_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,        -- sha256 of every column below
    identity_key TEXT NOT NULL,       -- what makes two entries the same slot (below)
    -- Cascades only when the church's whole parish is removed: a church on its
    -- own is retired instead (church.retired_at).
    church_id INTEGER NOT NULL REFERENCES church(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL CHECK (event_type IN ('mass', 'confession', 'adoration')),
    event_kind TEXT NOT NULL CHECK (event_kind IN ('weekly', 'specific_date')),
    day_of_week TEXT CHECK (day_of_week IN
        ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    date TEXT,                        -- ISO date, specific_date only
    start_time INTEGER NOT NULL CHECK (start_time BETWEEN 0 AND 1439),
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
    CHECK ((event_kind = 'weekly' AND day_of_week IS NOT NULL AND date IS NULL)
        OR (event_kind = 'specific_date' AND date IS NOT NULL AND day_of_week IS NULL)),
    CHECK (event_kind = 'weekly' OR (weeks_of_month = 0 AND season_start_month IS NULL)),
    CHECK (event_kind = 'specific_date' OR cancelled = 0),
    CHECK ((season_start_month IS NULL) = (season_end_month IS NULL)),
    CHECK (season_start_day IS NULL OR season_start_month IS NOT NULL),
    CHECK (season_end_day IS NULL OR season_end_month IS NOT NULL)
);

INSERT INTO schedule_entry_new SELECT * FROM schedule_entry;
DROP TABLE schedule_entry;
ALTER TABLE schedule_entry_new RENAME TO schedule_entry;
