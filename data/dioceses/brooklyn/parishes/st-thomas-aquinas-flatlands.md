---
name: St. Thomas Aquinas (Flatlands)
website: https://stthomasaquinasbrooklyn.com/important-information/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://stthomasaquinasbrooklyn.com/important-information/bulletin/ filename=*_202[6-9]_*.pdf
publication: []
group: Deanery B11 (Brooklyn East)
evidence:
- url: http://stthomasaquinasbrooklyn.com/wp-content/uploads/sites/16/2026/11/nov8_2026_stthomas_compressed.pdf
  seen: 2026-11-06
  quote: 1550 Hendrickson Street, Brooklyn, NY 11234
  note: Page 1 masthead of the 8 November 2026 issue (4 pages) names St. Thomas Aquinas Parish, Founded
    in 1885, Flatlands, Brooklyn, with Very Rev. Dwayne D. Davis, V.F., Pastor; Mass schedule Monday-Friday
    12 Noon, Saturday 8:30am and Vigil 5:30 pm, Sunday 8:00am, 11:30am and 5:30pm. No other church or
    chapel is named.
- url: http://stthomasaquinasbrooklyn.com/wp-content/uploads/sites/16/2026/11/nov8_2026_stthomas_compressed.pdf
  seen: 2026-11-06
  quote: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY 11704-1104
  note: 'Page 4 ad-page footer ''#243'': printed by The Church Bulletin Inc., which has no online container.'
- url: https://stthomasaquinasbrooklyn.com/important-information/bulletin/
  seen: 2026-11-06
  note: 'Diocesan WordPress multisite (sites/16) bulletin page, read with parish-site-access visit.py
    (probe url gets RemoteDisconnected): links nov8_2026_stthomas_compressed.pdf, nov1, oct25, oct18,
    oct11 and oct4 2026 issues.'
promoted: 2026-11-12
research:
- method: 'Reconcile: headed fetch:check of every Brooklyn row with recipe ''page-pdfs https://stthomasaquinasbrooklyn.com/important-information/bulletin/''
    picked nov16_2025_stthomas_compressed.pdf (''current''): the page links last year''s issue with the
    text ''November 16,'' (no year), which the resolver dates 16 November 2026. Pinned ''filename=*_202[6-9]_*.pdf'';
    the rerun picked nov8_2026_stthomas_compressed.pdf'
  url: http://stthomasaquinasbrooklyn.com/wp-content/uploads/sites/16/2026/11/nov8_2026_stthomas_compressed.pdf
  checked: '2026-11-12'
  outcome: found
  next_action: Widen the filename filter before the parish's first 2030 issue
  retry_when: December 2029
bulletin_status: available
publication_reviews:
- parish: our-lady-help-of-christians-midwood
  decision: separate
  evidence:
  - url: http://stthomasaquinasbrooklyn.com/wp-content/uploads/sites/16/2026/11/nov8_2026_stthomas_compressed.pdf
    seen: 2026-11-06
    note: 'The 8 November 2026 masthead names St. Thomas Aquinas Parish, 1550 Hendrickson Street alone,
      with its own Mass schedule (Sunday 8:00am, 11:30am, 5:30pm), its own intentions and The Church Bulletin
      Inc. footer #243.'
  - url: https://olhcbrooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMjgvN2NhMHFtY2JjMl9PTEhDX0J1bGxldGluX05vdmVtYmVyXzFfMjAyNi5wZGYiXV0/OLHC%20Bulletin%20November%201%2C2026.pdf
    seen: 2026-11-06
    note: The 1 November 2026 masthead names Our Lady Help of Christians, 1315 East 28th Street alone,
      with its own Mass schedule (Saturday Vigil 4:00 pm, Sunday 10:00 am) and intentions; a self-made
      Tilma PDF with no printer footer that does not mention St. Thomas.
---

## Publisher

St. Thomas Aquinas, Flatlands publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "#243") and posted as PDFs on the parish's page of the diocesan WordPress multisite. The 8 November 2026 issue (read 2026-11-06, 4 pages) has the masthead "St. Thomas Aquinas Parish, Founded in 1885, Flatlands, Brooklyn, 1550 Hendrickson Street, Brooklyn, NY 11234", with Very Rev. Dwayne D. Davis, V.F., Pastor.

Fr. Davis is also Administrator of Our Lady Help of Christians, Midwood (its 1 November 2026 bulletin, page 2), and the two share parochial vicars (Fr. Stanley Shinkut, Fr. Paul Zwolak) and staff; St. Thomas's bulletin advertises joint "St. Thomas Aquinas/Our Lady Help of Christians" religious-education programs. The bulletins are nonetheless separate: each masthead names its own parish, with its own Mass schedule and intentions, and they come from different printers (Church Bulletin Inc. #243 here; a self-made Tilma PDF for OLHC). See `publication_reviews`.

## Worship sites

One. The page 1 Mass schedule lists Monday-Friday 12 Noon, Saturday 8:30am Mass and Vigil Mass 5:30 pm, Sunday 8:00am, 11:30am & 5:30pm, with no other church or chapel. The directory, the deanery list, GCatholic 16787 and Mass finder 1168 all give the one church at 1550 Hendrickson Street.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stthomasaquinasbrooklyn.com/important-information/bulletin/`. The site is on the diocesan multisite, which drops `probe url` connections; `visit.py` and fetch read it. There is no publication id: The Church Bulletin Inc. has no online container.

Reconcile (2026-11-12): the bulletin page links about 200 issues back to 2025, and labels some last-year links without a year ("November 16," for nov16_2025_stthomas_compressed.pdf). The unpinned recipe picked that 2025 file as "current" on 12 November 2026. The recipe is now `page-pdfs https://stthomasaquinasbrooklyn.com/important-information/bulletin/ filename=*_202[6-9]_*.pdf` (the parish's names carry the year: `nov8_2026_stthomas_compressed.pdf`), and fetch:check then picked the 8 November 2026 issue. The filter needs widening before 2030.

## Not yet confirmed

Nothing outstanding.
