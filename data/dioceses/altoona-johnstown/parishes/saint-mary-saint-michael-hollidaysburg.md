---
name: St. Mary and St. Michael Parishes, Hollidaysburg
website: https://stmichael-hldg-pa.org/
bulletin_provider: other
provider_id: page-pdfs https://stmichael-hldg-pa.org/bulletins
publication: ['url:https://stmichael-hldg-pa.org/bulletins']
group: ''
evidence:
- url: 'https://img1.wsimg.com/blobby/go/04d20257-8d78-4404-bc76-b4eabd903c10/downloads/ea4c8410-f270-4f9a-9f00-e862cc738ee7/Oct%2018%202026.pdf?ver=1792175665993'
  seen: 2026-10-21
  quote: 'Joint Parish website:   www.stmichael-hldg-pa.org (Bulletins are available on the website)'
  note: 'Page 1 of the 18 October 2026 issue (4 pages, text layer readable). Masthead "St. Mary & St. Michael Parishes, One Body in Christ", pastor Very Reverend Alan E. Thomas, VG; St. Mary Parish, 312 Clark Street, and St. Michael the Archangel Parish, 301 Spruce Street, side by side; one Mass schedule (Saturday vigil 4:00 PM St. Mary; Sunday 7:30 AM and 10:00 AM St. Mary, 10:00 AM and 11:30 AM St. Michael) and a joint Mass-intentions table "MASS INTENTIONS FOR ST. MARY AND ST. MICHAEL PARISHES".'
- url: https://www.webparish.com/aj/saintmarys/
  seen: 2026-10-21
  quote: St. Mary church has joined their website with St. Michael church also in Hollidaysburg.
  note: 'St. Mary''s own old site (the homepage GCatholic lists for it, webparish.com/aj/saintmarys) now only says this and points to the St. Michael site. It carries no bulletin.'
- url: https://stmichael-hldg-pa.org/bulletins
  seen: 2026-10-21
  note: 'The joint site (GoDaddy-hosted, PDFs on img1.wsimg.com) lists one PDF per Sunday: Sept 6, 13, 20, 27, Oct 4, 11 and 18 2026. Found with visit.py --bulletin from the home page; fetched once through the home-page link, but a direct browser load of /bulletins, and often of the home page, answers ERR_CONNECTION_RESET from this sandbox (intermittent).'
---

## Publisher

St. Mary and St. Michael, Hollidaysburg, share one pastor (Very Rev. Alan E. Thomas, VG), one
website (stmichael-hldg-pa.org) and **one bulletin**. The 18 October 2026 issue, read on
2026-10-21, is headed "St. Mary & St. Michael Parishes, One Body in Christ", prints one Mass
schedule for both churches and one Mass-intentions table for "ST. MARY AND ST. MICHAEL PARISHES".
Its footer says "Joint Parish website: www.stmichael-hldg-pa.org (Bulletins are available on the
website)". The directory gives both parishes that same homepage.

One row, not two: the only former separate channel I found was St. Mary's own webparish.com site,
which says "St. Mary church has joined their website with St. Michael church also in
Hollidaysburg." and carries no bulletin. I found no live bulletin of its own for either church
(searched: both directory homepages, GCatholic's homepages, the bulletins page; not checked:
ParishesOnline, Discover Mass and other aggregators by name).

## Worship sites

Two churches: St. Mary (312 Clark Street) and St. Michael the Archangel (301 Spruce Street). Both
are in the Mass-intentions table of the 18 October issue. Nothing else is named.

## Website and bulletin provider

The directory homepage `https://stmichael-hldg-pa.org/` is the site; its "Bulletins" page (the
`/bulletins` path) lists the weekly PDFs, hosted on GoDaddy's `img1.wsimg.com` blobs with a
`?ver=` query. `provider: other`, `publication: url:https://stmichael-hldg-pa.org/bulletins`.
The site resets connections from this sandbox intermittently (see the evidence note): on 2026-10-21
`pnpm fetch:check --diocese altoona-johnstown --parish saint-mary-saint-michael-hollidaysburg`
failed with `resolve_failed` (ERR_CONNECTION_RESET) five times and then succeeded twice in a row,
picking the `Oct 18 2026.pdf` blob above (status ok) with recipe
`page-pdfs https://stmichael-hldg-pa.org/bulletins`, which is the `provider_id`. The PDFs
themselves download fine with curl. A production fetch may see the same flakiness.

## Not yet confirmed

- Whether the weekly fetch is reliable given the connection resets; rerun `fetch:check` a few times.
- Whether either church has any other live bulletin channel (not searched by name).
