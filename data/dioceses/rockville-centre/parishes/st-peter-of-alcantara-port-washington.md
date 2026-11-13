---
name: St. Peter of Alcantara
website: https://www.stpeterofalcantara.org/about-us/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stpeterofalcantara.org/about-us/bulletin#st-peter-of-alcantara']
group: ''
evidence:
- url: https://flipbook.so/flip/ztexS2pcMP1b5jODqlXk
  seen: 2026-11-13
  quote: NOVEMBER 8, 2026 ST PETER OF ALCANTARA
  note: 'flipbook.so viewer reached from the parish''s November 8, 2026 bulletin link (read with visit.py).
    Its text layer: ''Parish of St. Peter of Alcántara, 1327 Port Washington Blvd., Port Washington, NY
    11050'', Pastor Rev. Monsignor Robert J. Clerkin; MASS SCHEDULE Saturday 5:00 p.m. vigil, Sunday 7:30
    a.m., 9:30 a.m., 11:30 a.m., Spanish Mass 9:30 a.m. (Lower Church), Weekdays (Monday-Saturday) 8:30
    a.m.; back page ''#189 FOR ADVERTISING: THE CHURCH BULLETIN INC. 200 DALE ST., W. BABYLON, NY 11704''.'
- url: https://www.stpeterofalcantara.org/about-us/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (read with visit.py; probe url got 403) links issues newest first
    as /about-us/bulletin/<n>-<month>-<d>-<yyyy>/file: 493-november-8-2026, 492-november-1-2026, 491-october-25-2026
    ... The November 8 and October 18 links both open flipbook.so viewers.'
research:
- method: fetch:check on the Solutio bulletin list (provider other, unpinned)
  url: https://www.stpeterofalcantara.org/about-us/bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Re-run fetch:check once a collector reads flipbook.so page images, or if the parish posts
    PDFs again
  retry_when: A flipbook.so collector lands, or the bulletin list links PDFs again
bulletin_status: unsupported-format
fetch_gap:
  kind: flipbook-so-viewer
  seen: 2026-11-13
  note: The Solutio bulletin list's /file links redirect to flipbook.so viewers (e.g. 'NOVEMBER 8, 2026
    ST PETER OF ALCANTARA - Flipso'), which serve each page as a .webp image on storage.googleapis.com
    and no PDF; fetch:check answered resolve_failed. The printer, The Church Bulletin Inc., posts nothing
    online.
  url: https://www.stpeterofalcantara.org/about-us/bulletin/493-november-8-2026/file
publication_reviews:
- parish: our-lady-of-fatima-manorhaven
  decision: separate
  evidence:
  - url: https://flipbook.so/flip/ztexS2pcMP1b5jODqlXk
    seen: 2026-11-13
    note: The November 8, 2026 masthead names the Parish of St. Peter of Alcántara, 1327 Port Washington
      Blvd. alone, with its own Mass schedule; pastor Msgr. Robert J. Clerkin; printed by The Church Bulletin
      Inc.
  - url: https://olfpw.org/bulletin/580-november-15-2026-thirty-third-sunday-in-ordinary-time/file
    seen: 2026-11-13
    note: The November 15, 2026 masthead names Our Lady of Fatima Parish Community, Manorhaven alone ('Fatima
      Focus', Canva), with its own Mass schedule and the same pastor.
---

## Publisher

St. Peter of Alcantara, Port Washington publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon ("#189 FOR ADVERTISING: THE CHURCH BULLETIN INC. 200 DALE ST., W. BABYLON, NY 11704" on the back page), which posts no bulletins online. The parish posts each issue as a flipbook.so viewer. The November 8, 2026 issue (`https://flipbook.so/flip/ztexS2pcMP1b5jODqlXk`, title "NOVEMBER 8, 2026 ST PETER OF ALCANTARA", read 2026-11-13 with visit.py) names "Parish of St. Peter of Alcántara, 1327 Port Washington Blvd., Port Washington, NY 11050", Pastor Rev. Monsignor Robert J. Clerkin, and gives the MASS SCHEDULE: Saturday 5:00 p.m. vigil; Sunday 7:30 a.m., 9:30 a.m., 11:30 a.m.; Spanish Mass 9:30 a.m. (Lower Church); weekdays (Monday-Saturday) 8:30 a.m.

Msgr. Clerkin is also pastor of Our Lady of Fatima, Manorhaven, which publishes its own bulletin ("Fatima Focus"), so the two are separate rows (see publication_reviews).

## Worship sites

One: the church at 1327 Port Washington Blvd. (`st-peter-of-alcantara-port-washington-church`). The Spanish Mass is in the "Lower Church", which the bulletin gives no separate address for; it is taken as part of the same building. The drvc.org Mass-times page calls it "the School Church" (9:30 AM Spanish); if that turns out to be a separate building, it needs its own record. The diocesan locator (directory:61), GCatholic (16902) and the Mass-times page list only this church.

Our Lady of Fatima, Manorhaven, in the same town, publishes its own bulletin (its own row).

## Website and bulletin provider

The site stpeterofalcantara.org is Solutio (Joomla), 403 to `probe url` and fine in `visit.py`. Its bulletin list `/about-us/bulletin` links issues newest first as `/about-us/bulletin/<n>-<month>-<d>-<yyyy>/file`, but those links redirect to flipbook.so viewers (checked for November 8 and October 18, 2026), whose pages are `.webp` images on storage.googleapis.com with no PDF. `fetch:check` (2026-11-13, provider `other`, unpinned) answered `resolve_failed`. The row is `unsupported` with fetch_gap `flipbook-so-viewer` until a collector reads these viewers.

## Not yet confirmed

Whether the "Lower Church" and the Mass-times page's "School Church" are the same space as the main church building: a bulletin or site page describing the Spanish Mass location would settle it.
