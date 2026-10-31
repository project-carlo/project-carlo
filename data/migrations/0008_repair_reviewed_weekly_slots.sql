-- Correct five proposals from the October 18 run without rewriting its calls,
-- decisions or seed files. Append human revisions, then fold only those changes.
--
-- The monthly services were removed solely because routine panels omitted them.
-- The two added Masses reversed reviewed exclusions (unresolved public venue at
-- All Saints; relocation to St. Mary's at St. Edward's). See the replay report in
-- data/update-evals/2026-10-18/. The other changes from the run are preserved.
--
-- Match the run and slot rather than database-specific ids. Only reverse a
-- proposal when no later change touched that identity, and the current schedule
-- still reflects it. An already corrected or subsequently reviewed slot stays put.
CREATE TEMP TABLE weekly_slot_repairs AS
WITH targets(parish_slug, church_slug, event_type, weekday, start_time, weeks, original_op) AS (
    VALUES
        ('all-saints-corning', 'st-marys-corning', 'mass', 'Saturday', 960, 0, 'add'),
        ('st-edward-the-confessor-clifton-park', 'st-edward-the-confessor-clifton-park',
         'mass', 'Friday', 540, 0, 'add'),
        ('holy-trinity-webster', 'holy-trinity', 'mass', 'Saturday', 1110, 1, 'delete'),
        ('mary-mother-of-our-savior-utica', 'our-lady-of-lourdes-utica',
         'mass', 'Saturday', 495, 1, 'delete'),
        ('mary-mother-of-our-savior-utica', 'our-lady-of-lourdes-utica',
         'confession', 'Saturday', 525, 1, 'delete')
)
SELECT p.id AS parish_id, e.id AS entry_id, e.identity_key,
       CASE pc.op WHEN 'add' THEN 'delete' ELSE 'add' END AS repair_op
FROM targets t
JOIN parish p ON p.slug = t.parish_slug
JOIN church church ON church.parish_id = p.id AND church.slug = t.church_slug
JOIN llm_call call ON call.parish_id = p.id
    AND call.run_id = '20261018T123547Z-gh39127931592'
JOIN proposed_change pc ON pc.llm_call_id = call.id
    AND pc.op = t.original_op AND pc.decision = 'applied'
JOIN schedule_entry e ON e.id = COALESCE(pc.entry_id, pc.target_entry_id)
    AND e.church_id = church.id AND e.event_type = t.event_type
    AND e.event_kind = 'weekly' AND e.day_of_week = t.weekday
    AND e.start_time = t.start_time AND e.weeks_of_month = t.weeks
JOIN schedule_change change ON change.proposed_change_id = pc.id AND change.op = pc.op
WHERE church.retired_at IS NULL
  AND NOT EXISTS (
      SELECT 1 FROM schedule_change later
      LEFT JOIN schedule_entry before ON before.id = later.before_entry_id
      LEFT JOIN schedule_entry after ON after.id = later.after_entry_id
      WHERE later.parish_id = p.id AND later.id > change.id
        AND (before.identity_key = e.identity_key OR after.identity_key = e.identity_key)
  )
  AND (
      (pc.op = 'add' AND EXISTS (
          SELECT 1 FROM current_schedule current
          WHERE current.parish_id = p.id AND current.entry_id = e.id
            AND current.since_revision = change.revision
      ))
      OR (pc.op = 'delete' AND NOT EXISTS (
          SELECT 1 FROM current_schedule current
          WHERE current.parish_id = p.id AND current.identity_key = e.identity_key
      ))
  );

CREATE TEMP TABLE weekly_repair_revisions AS
SELECT repair.parish_id, MAX(revision.revision) + 1 AS revision
FROM (SELECT DISTINCT parish_id FROM weekly_slot_repairs) repair
JOIN schedule_revision revision ON revision.parish_id = repair.parish_id
GROUP BY repair.parish_id;

INSERT INTO schedule_revision (parish_id, revision, source_kind, actor, note, created_at)
SELECT parish_id, revision, 'human', 'weekly-run-review',
       'Repair unsupported monthly deletions and reversed reviewed exclusions from '
       || '20261018T123547Z-gh39127931592 (migration 0008)',
       strftime('%Y-%m-%dT%H:%M:%SZ', 'now')
FROM weekly_repair_revisions;

INSERT INTO schedule_change (parish_id, revision, op, before_entry_id, after_entry_id)
SELECT repair.parish_id, revision.revision, repair.repair_op,
       CASE repair.repair_op WHEN 'delete' THEN repair.entry_id END,
       CASE repair.repair_op WHEN 'add' THEN repair.entry_id END
FROM weekly_slot_repairs repair
JOIN weekly_repair_revisions revision ON revision.parish_id = repair.parish_id;

DELETE FROM current_schedule
WHERE (parish_id, entry_id) IN (
    SELECT parish_id, entry_id FROM weekly_slot_repairs WHERE repair_op = 'delete'
);
INSERT INTO current_schedule (parish_id, entry_id, identity_key, since_revision)
SELECT repair.parish_id, repair.entry_id, repair.identity_key, revision.revision
FROM weekly_slot_repairs repair
JOIN weekly_repair_revisions revision ON revision.parish_id = repair.parish_id
WHERE repair.repair_op = 'add';

DROP TABLE weekly_repair_revisions;
DROP TABLE weekly_slot_repairs;
