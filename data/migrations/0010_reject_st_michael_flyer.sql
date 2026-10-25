-- The October 25 run processed this donuts / bottle-drive flyer before the
-- undated-empty-PDF guard shipped in #154. A rerun finds the real October 11
-- bulletin unchanged, so it never revisits the flyer's stored valid verdict.
-- Its fetch date then outranks the real bulletin's issue date on the site.
--
-- Repair only the reviewed PDF, matched by parish and content rather than
-- database-specific ids. Keep its record and extraction history, and leave
-- any later issue or corrected extraction alone. Deploy snapshot builds apply
-- migrations too, so merging restores the schedule without another model call.
UPDATE bulletin
SET wrong_bulletin = 1
WHERE parish_id = (
    SELECT id FROM parish WHERE slug = 'st-michael-st-peter-our-lady-of-hope-syracuse'
)
  AND content_hash = '1afe3ca1dc887823f9030e44ae3f824ccc5516a4aa3ec500759b2635e5a1a59b'
  AND published_date IS NULL
  AND processed_at IS NOT NULL
  AND COALESCE(wrong_bulletin, 0) = 0
  AND NOT EXISTS (SELECT 1 FROM event WHERE bulletin_id = bulletin.id);
