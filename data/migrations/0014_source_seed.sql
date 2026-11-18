-- Where a source seed's schedule was read (docs/source-schedules-plan.md): a
-- seed revision loaded from a source seed file names the page the website
-- links as the times' source. Null for every other revision, including a seed
-- drafted from bulletins.
ALTER TABLE schedule_revision ADD COLUMN schedule_source TEXT
    CHECK (schedule_source IS NULL OR (source_kind = 'seed'
                                       AND schedule_source IN ('website', 'facebook')));
ALTER TABLE schedule_revision ADD COLUMN schedule_source_url TEXT
    CHECK ((schedule_source IS NULL) = (schedule_source_url IS NULL));
