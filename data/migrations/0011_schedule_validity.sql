-- Inclusive absolute dates for announced changes. These are not annual seasons.
ALTER TABLE schedule_entry ADD COLUMN valid_from TEXT
    CHECK (valid_from IS NULL OR (event_kind = 'weekly' AND date(valid_from) = valid_from));
ALTER TABLE schedule_entry ADD COLUMN valid_until TEXT
    CHECK (valid_until IS NULL OR (event_kind = 'weekly' AND date(valid_until) = valid_until));
