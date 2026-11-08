-- Once its daily download cap is hit, Discover Mass answers download.php with
-- HTTP 200 and a 134-byte HTML page ("Maximum number of files downloaded
-- today. Please contact Discover Mass for support."). Until the fetch stage
-- refused bodies that are not PDFs, it stored that page as a bulletin: 66
-- fetch-only parishes on the October 25 run, 13:16-13:25Z. Every run since
-- matched the page by its hash and reported those parishes "unchanged".
--
-- The rows are not bulletins, so they are deleted rather than flagged
-- `wrong_bulletin` (a real PDF the extractor took for another parish's). A
-- flagged row would still answer duplicate and ETag lookups, and stay the
-- parish's newest bulletin when it is the only one, as each of these is.
-- Without them the parishes have no recent bulletin, so the next run fetches
-- them again and the report lists them as stale until it succeeds. Run
-- results keep their record of what happened: they name the hash, not the row.
--
-- Matched by content rather than database ids. Foreign keys are off while
-- migrations run, so a delete would not cascade: a row anything refers to (an
-- extraction, events, sightings) is flagged instead, keeping that history.
-- None did when this was written.
UPDATE bulletin
SET wrong_bulletin = 1
WHERE content_hash = 'df175220b1d967b5204b2dea47961626b06f0e346a6a4e54094544af84ae0117'
  AND (
      EXISTS (SELECT 1 FROM event WHERE bulletin_id = bulletin.id)
      OR EXISTS (SELECT 1 FROM llm_call WHERE bulletin_id = bulletin.id)
      OR EXISTS (SELECT 1 FROM entry_sighting WHERE bulletin_id = bulletin.id)
  );

DELETE FROM bulletin
WHERE content_hash = 'df175220b1d967b5204b2dea47961626b06f0e346a6a4e54094544af84ae0117'
  AND NOT EXISTS (SELECT 1 FROM event WHERE bulletin_id = bulletin.id)
  AND NOT EXISTS (SELECT 1 FROM llm_call WHERE bulletin_id = bulletin.id)
  AND NOT EXISTS (SELECT 1 FROM entry_sighting WHERE bulletin_id = bulletin.id);
