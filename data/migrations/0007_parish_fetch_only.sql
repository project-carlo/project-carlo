-- A fetch-only parish has its bulletins fetched and stored every week, but
-- the process stage makes no model call for it and the website snapshot
-- leaves its churches out. New dioceses start this way (`pnpm diocese
-- promote` marks the rows it adds), so their bulletins can be checked before
-- paying for extraction. Set from the `fetch_only` column of parishes.csv.

ALTER TABLE parish ADD COLUMN fetch_only INTEGER NOT NULL DEFAULT 0 CHECK (fetch_only IN (0, 1));
