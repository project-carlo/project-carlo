-- Weekly entries at one weekday/start may have disjoint recurrence patterns.
-- Include weeks and season in their identity, leaving dated identities alone.
-- The unique key on current_schedule continues to guard identical patterns;
-- schedule writers also check for overlap between different patterns.
-- Only derived keys change: entry content, hashes, ids, log and decisions stay.
UPDATE schedule_entry
SET identity_key = church_id || '|' || event_type || '|' || event_kind || '|'
    || day_of_week || '|' || start_time || '|' || weeks_of_month || '|'
    || COALESCE(season_start_month, 0) || '|' || COALESCE(season_start_day, 0) || '|'
    || COALESCE(season_end_month, 0) || '|' || COALESCE(season_end_day, 0)
WHERE event_kind = 'weekly';

UPDATE current_schedule
SET identity_key = (SELECT identity_key FROM schedule_entry WHERE id = entry_id);
