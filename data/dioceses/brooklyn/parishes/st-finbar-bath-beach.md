---
name: St. Finbar (Bath Beach)
website: https://stfinbarbrooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://stfinbarbrooklyn.org/bulletins
publication: []
group: Deanery B10 (Brooklyn West)
evidence:
- url: https://stfinbarbrooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMzEveHlxNm93cWEwX05vdmVtYmVyXzFfMjAyNi5wZGYiXV0/November%201%2C%202026.pdf
  seen: 2026-11-06
  note: 1 November 2026 issue, 8 pages; text layer in a shifted font, page 1 read by render. The masthead
    names ST. FINBAR R.C. CHURCH alone, 'The Mother Church of Bensonhurst & Bath Beach', 138 Bay 20th
    Street, Brooklyn, NY 11214; Rev. Pedro Angucho, Pastor; Rev. Norbert Nkwayaya-Katembo, Parochial Vicar;
    Mass schedule Saturday 6:00pm Bilingual, Sunday 10:00am Español and 12:00pm English, Monday-Saturday
    9:00am English, Tuesday and Thursday 7:00pm Español. No other church or chapel.
- url: https://stfinbarbrooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMzEveHlxNm93cWEwX05vdmVtYmVyXzFfMjAyNi5wZGYiXV0/November%201%2C%202026.pdf
  seen: 2026-11-06
  quote: THE CHURCH BULLETIN INC. 200 DALE ST. W. BABYLON NY 11704
  note: 'Page 8 ad-page footer ''# 117'': printed by The Church Bulletin Inc.; no online container.'
- url: https://stfinbarbrooklyn.org/mass-times
  seen: 2026-11-06
  quote: Tuesday, Thursday
  note: 'Parish Mass Times page: Saturday 6pm (Bilingual); Sunday 10am (Español), 12pm (English); Monday
    - Saturday 9am (English); Tuesday, Thursday 7pm (Español). Agrees with the bulletin masthead.'
- url: https://stfinbarbrooklyn.org/bulletins
  seen: 2026-11-06
  note: 'Tilma bulletins page, server-rendered, newest first: ''November 01, 2026 / Download Bulletin''
    (November 1, 2026.pdf, uploaded 2026-10-31), October 25, October 18, October 04, September 27 ...
    Files Aug-Oct were named ''561070  MM-DD-YYYY.pdf'', later ones by date or ''Finbar10-25.pdf''.'
revisit: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later (the newest posted
  on 2026-11-12 was older than 8 November).
revisit_after: 2026-11-17
promoted: 2026-11-12
research:
- method: 'Reconcile: headed fetch:check of every Brooklyn row picked the issue dated 2026-11-01; the
    bulletin page lists no newer issue than the one picked'
  url: https://stfinbarbrooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMzEveHlxNm93cWEwX05vdmVtYmVyXzFfMjAyNi5wZGYiXV0/November%201%2C%202026.pdf
  checked: '2026-11-12'
  outcome: not-found
  next_action: Rerun fetch:check and confirm it picks the 15 November 2026 issue or later
  retry_when: After the weekend of 14-15 November 2026
bulletin_status: available
publication_reviews:
- parish: st-frances-cabrini-dyker-heights
  decision: separate
  evidence:
  - url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTAvMzAvNWg3Zjk0bDl5NV9GckNhYkJrbHluMTFfMS5wZGYiXV0/FrCabBklyn11-1.pdf
    seen: 2026-11-06
    note: 'The 1 November 2026 masthead names Saint Frances Cabrini alone (1562 86th St.), with its own
      Mass times (Sat 4 p.m., Sun 9:30 a.m. and 12:30 p.m. Spanish, weekdays 9 a.m.), its own intentions
      and collections, printed by The Church Bulletin Inc. #167.'
- parish: shrine-of-st-bernadette-dyker-heights
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/4063/20261108B.pdf
    seen: 2026-11-06
    note: The 8 November 2026 masthead names The Shrine Church of Saint Bernadette alone (8201 13th Avenue),
      with its own Mass times (Sat 5:30 p.m., Sun 8:30 and 11 a.m., Mon-Sat 8 a.m.); LPi container 03/4063.
      Same pastor (Rev. Jeremy Canna), separate bulletins.
---

## Publisher

St. Finbar publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "# 117") and posted as PDFs on the parish's Tilma site. The 1 November 2026 issue (read 2026-11-06, 8 pages) has on page 1 the masthead "ST. FINBAR R.C. CHURCH, The Mother Church of Bensonhurst & Bath Beach, 138 Bay 20th Street - Brooklyn, NY 11214", with Rev. Pedro Angucho, Pastor. Its text layer is in a shifted font (greps for 'Finbar' or 'Mass' find nothing); page 1 was read from a render.

## Worship sites

One. The masthead's Mass schedule (Saturday 6:00pm bilingual; Sunday 10:00am Spanish, 12:00pm English; Monday-Saturday 9:00am; Tuesday and Thursday 7:00pm Spanish) names no other church or chapel, and the site's /mass-times page gives the same times. The directory (St. Finbar), the deanery list (St. Finbar Roman Catholic Church), GCatholic 16704 and Mass finder 1192 all give the one church at 138 Bay 20th Street.

**Not shared with St. Frances Cabrini.** Guardian Angel's bulletin names "St. Finbarr and St. Frances Cabrini" together among its deanery neighbours, but St. Finbar's bulletin names St. Finbar alone, under its own pastor (Rev. Pedro Angucho, while Cabrini's is Rev. Jeremy Canna), with printer number #117 (Cabrini's is #167) and its own Mass times. Reviews are in `publication_reviews`.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stfinbarbrooklyn.org/bulletins` (the Tilma bulletins page, newest first). No publication id: The Church Bulletin Inc. has no online container. Some summer and autumn 2026 files were named `561070  MM-DD-YYYY.pdf`; `church-bulletin.org/561070` does not redirect to a John Patrick slug page (checked 2026-11-06), so the number is not taken as a publication id. Probe po found no ParishesOnline org at `st-finbar-church-11214` or `st-finbar-roman-catholic-church-11214`.

## Not yet confirmed

The archive has gaps (no 11 October card, nor 16 or 23 August), so the parish sometimes skips posting an issue; a stale page should be read against this before treating it as a stop.
