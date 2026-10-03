-- What the fetch stage needs to tell a bulletin it already has from a new one
-- without trusting the address (see pdf_extract.duplicates):
--
--   etag, last_modified  the validators the server sent with the PDF, for a
--                        conditional GET of the same address next time
--   text_fingerprint     a hash of the PDF's words, for a server that rebuilds
--                        the file (new bytes, same bulletin) on each request
--   last_seen_at         when the site last served this bulletin, so a parish
--                        whose site is alive but unchanged can be told from
--                        one that stopped answering
--   wrong_bulletin       the extractor said the PDF is not this parish's
--                        current bulletin, so its date is not to be trusted
--
-- The byte hash is `content_hash`, already there.

ALTER TABLE bulletin ADD COLUMN etag TEXT;
ALTER TABLE bulletin ADD COLUMN last_modified TEXT;
ALTER TABLE bulletin ADD COLUMN text_fingerprint TEXT;
ALTER TABLE bulletin ADD COLUMN last_seen_at TEXT;
ALTER TABLE bulletin ADD COLUMN wrong_bulletin INTEGER NOT NULL DEFAULT 0
    CHECK (wrong_bulletin IN (0, 1));

UPDATE bulletin SET last_seen_at = fetched_at;

-- Runs so far recorded the extractor's verdict only in their results.
UPDATE bulletin SET wrong_bulletin = 1
WHERE EXISTS (
    SELECT 1 FROM run_parish_result r JOIN parish p ON p.slug = r.parish_slug
    WHERE r.stage = 'process' AND r.status = 'wrong_bulletin'
      AND p.id = bulletin.parish_id AND r.content_hash = bulletin.content_hash
);
