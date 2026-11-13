---
name: St. Hedwig
website: https://sthedwig.church/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://sthedwig.church/bulletin/
publication: ['url:https://sthedwig.church/bulletin/#st-hedwig']
group: ''
evidence:
- url: https://sthedwig.church/wp-content/uploads/2026/11/StHed_Nov8_26.pdf
  seen: 2026-11-13
  quote: 'Website: sthedwig.church'
  note: Issue for November 08, 2026 (7 pages, Microsoft Print To PDF). Masthead names St. Hedwig's Church,
    One Depan Avenue, Floral Park alone; MASS SCHEDULE daily 7:00 AM (English), 8:00 AM (Polish); Saturday
    5:00 PM; Sunday 7:00 AM, 8:00 AM (Polish), 9:30 AM, 11:00 AM (Polish), 6:30 PM; Administrator Rev.
    Dr. Marcin Nabożny, Parochial Vicar Rev. Dr. Jerzy Breś (fr.jerzy@stladislaus.church).
- url: https://sthedwig.church/bulletin/
  seen: 2026-11-13
  note: WordPress bulletin page (read with parish-site-access visit.py) links issues from August 2026
    to November 8, 2026 (StHed_Nov8_26.pdf), the newest.
- url: https://www.sthedwigfloralpark.org/bulletin?year=2026
  seen: 2026-11-13
  note: The old site (the locator's and Mass-times page's link) lists issues only up to September 13,
    2026 (bulletin/files/346), which itself names the new site sthedwig.church.
bulletin_status: available
publication_reviews:
- parish: st-ladislaus-hempstead
  decision: separate
  evidence:
  - url: https://sthedwig.church/wp-content/uploads/2026/11/StHed_Nov8_26.pdf
    seen: 2026-11-13
    note: The November 08, 2026 masthead names St. Hedwig's Church, One Depan Avenue, Floral Park alone,
      with its own Mass schedule and contact@sthedwig.church.
  - url: https://stladislaus.church/wp-content/uploads/2026/11/St.-Ladislaus-November-15-2026.pdf
    seen: 2026-11-13
    note: The November 15, 2026 masthead names St. Ladislaus Church, 18 Richardson Place, Hempstead alone,
      with its own Mass schedule; the same administrator and vicar.
---

## Publisher

St. Hedwig, Floral Park (a Polish parish) publishes its own weekly bulletin. The newest issue on 2026-11-13, `https://sthedwig.church/wp-content/uploads/2026/11/StHed_Nov8_26.pdf` (7 pages), has the masthead "St. Hedwig's Church, One Depan Avenue, Floral Park, NY 11001, Website: sthedwig.church", "THIRTY-SECOND SUNDAY IN ORDINARY TIME, NOVEMBER 08, 2026", and a MASS SCHEDULE: daily 7:00 AM (English) and 8:00 AM (Polish); Saturday evening 5:00 PM; Sunday 7:00 AM, 8:00 AM (Polish), 9:30 AM, 11:00 AM (Polish), 6:30 PM. Staff: "ADMINISTRATOR Rev. Dr. Marcin Nabożny", "PARIOCHAL VICAR Rev. Dr. Jerzy Breś ... fr.jerzy@stladislaus.church".

St. Hedwig and St. Ladislaus, Hempstead share an administrator and a parochial vicar, but each publishes its own bulletin: the St. Ladislaus issue of November 15, 2026 has its own masthead (18 Richardson Place, Hempstead) and its own Mass schedule. So they are separate rows (see publication_reviews).

## Worship sites

One: the church at 1 Depan Avenue (`st-hedwig-floral-park-church`). The bulletin's schedule names no other place. The diocesan locator (directory:44), GCatholic (16844) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

The parish moved to a new WordPress site, sthedwig.church, named in the bulletin's masthead. Its `/bulletin/` page links issues as `wp-content/uploads/<yyyy>/<mm>/<name>.pdf` with irregular names (StH_Sep13.pdf, StHedwig_Sep20.pdf, StHed_Oct1126.pdf, StHed_Nov8_26.pdf), not in date order (a February issue sits among September ones). The old site sthedwigfloralpark.org (the locator's and Mass-times page's link) is still up but its bulletin list stops at September 13, 2026. visit.py read the new page despite a 403 status on first load; `probe get` downloads its PDFs.

`fetch:check` (2026-11-13) with page-pdfs on `/bulletin/` picked `StHed_Nov8_26.pdf`, the November 8, 2026 issue, the newest posted.

## Not yet confirmed

Nothing open.
