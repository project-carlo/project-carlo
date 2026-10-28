---
name: St. Joseph
website: https://www.stjosephmiddletown.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-joseph-parish-middletown-de-19709
publication: ['url:https://www.church-bulletin.org/saint-joseph-parish-middletown-de-19709']
group: Iron Hill Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-joseph-parish-middletown-de-19709/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Page 1 of the 25 October 2026 issue (12 pages, scanned images with no text layer, so read as
    a rendered image): masthead ''ST. JOSEPH PARISH / PARROQUIA SAN JOSE'' over photos of Saint Francis
    Xavier, Saint Joseph Church and Saint Rose of Lima Church; ''OUR CHURCHES & SACRAMENT SCHEDULE'':
    St. Joseph Church, 371 East Main Street, Middletown: Saturday Vigil 5:00 PM, Sunday 8:30AM, 10:30AM,
    1:00 PM (Espanol), weekdays Monday to Friday 8:30 AM; ''St. Rose of Lima Mission: 301 Lock St, Chesapeake
    City, MD ... Sunday Masses: 9:00 AM''; ''St. Francis Xavier Shrine: 1704 Bohemia Church Road, Warwick,
    MD ... The Church is currently closed for repairs.'' One bulletin for all three places.'
- url: https://jppc.net/onlinebulletins/319template.pdf
  seen: 2026-10-27
  note: curl -L redirects to https://www.church-bulletin.org/saint-joseph-parish-middletown-de-19709 ('Saint
    Joseph Parish Bulletin', 'Latest Edition October 25, 2026', 319 East Main Street), a John Patrick
    Publishing listing of dated PDFs, newest first (2026-10-25, 10-18, 10-11, 10-04 ...). The parish's
    own site links this template as its bulletin.
- url: https://www.stjosephmiddletown.com/news-events/bulletin
  seen: 2026-10-27
  quote: OCTOBER 18, 2026
  note: Read in the browser (curl and probe url get HTTP 403). The parish site's own Bulletin page, a
    page of its own uploaded files (file URLs like /news-events/bulletin/563-october-18-2026/file), is
    a week behind the John Patrick listing (newest 18 October).
promoted: 2026-10-27
---

## Publisher

St. Joseph, Middletown publishes one weekly bulletin, printed by John Patrick Publishing (no. 319). The 25 October 2026 cover is headed 'ST. JOSEPH PARISH / PARROQUIA SAN JOSE', shows the three churches and lists their Mass times under 'OUR CHURCHES & SACRAMENT SCHEDULE' (quoted in the evidence). It is scanned images (all 12 pages: `probe pdf` finds no text on the 25 October, 18 October or 20 September issues), so the pipeline will have to read it as an image. The directory, GCatholic and the summer guide all say St. Rose of Lima is a mission of this parish; the bulletin confirms it by listing it as 'St. Rose of Lima Mission'.

## Worship sites

- St. Joseph Church, 371 East Main Street, Middletown (the Sunday 1:00 PM Mass is in Spanish).
- St. Rose of Lima, 301 Lock Street, Chesapeake City, MD: Sunday 9:00 AM.
- St. Francis Xavier Shrine (Old Bohemia), 1704 Bohemia Church Road, Warwick, MD: named on the cover, but 'currently closed for repairs'. The Dialog (2 September 2026) says it reopens to the public on 6 December 2026 after more than two years of renovation, then has Mass monthly on the first Sunday at 2 p.m., April to December. It has no church row yet; see `open/st-francis-xavier-shrine-warwick.md`.
- Ruled out: St. Joseph's original church at 15 W Cochran St., Middletown, sold in November 2006 and now a Protestant church (`excluded/st-joseph-former-church-middletown.md`).

The parish office phone (302-378-5800) and the website are the same for all three entries in the diocese's directory.

## Website and bulletin provider

`other`, pinned to the church-bulletin.org listing as for St. Margaret of Scotland and St. Hedwig. The parish site (stjosephmiddletown.com, a Solutio site) answers HTTP 403 to curl and `probe url` and loads only in the browser; its own bulletin page lags the listing by a week, so the listing is the pick. The directory's own 'website' for the Middletown entry is a catholicmasses.org listing, which isn't used.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-joseph-middletown` (2026-10-27): picked church-bulletin.org 2026-10-25.pdf (8.9 MB); transport ok, document type PDF, freshness fresh. The tool leaves identity 'unverified'; the masthead read above settles it. The pinned recipe is already in `provider_id`, so no new recipe is recorded.

## Not yet confirmed

The Mass times on the cover are read from an image, not a text layer. The Spanish Mass is Sunday 1:00 PM on the cover and the website, and the directory agrees.
