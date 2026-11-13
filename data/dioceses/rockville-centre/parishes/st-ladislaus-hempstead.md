---
name: St. Ladislaus
website: https://stladislaus.church/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://stladislaus.church/bulletin/
publication: ['url:https://stladislaus.church/bulletin/#st-ladislaus']
group: ''
evidence:
- url: https://stladislaus.church/wp-content/uploads/2026/11/St.-Ladislaus-November-15-2026.pdf
  seen: 2026-11-13
  quote: 18 Richardson Place
  note: Issue for November 15, 2026 (7 pages, Microsoft Publisher). Masthead names St. Ladislaus Church,
    18 Richardson Place, Hempstead alone; MASS SCHEDULE daily 9:00 AM; Saturday 5:00 PM; Sunday 8:00 AM,
    9:30 AM (Polish), 4:00 PM (Spanish); Administrator Rev. Dr. Marcin Nabozny, Parochial Vicar Rev. Dr.
    Jerzy Breś.
- url: https://stladislaus.church/bulletin/
  seen: 2026-11-13
  note: WordPress bulletin page (read with parish-site-access visit.py) links issues from September 2026
    to St.-Ladislaus-November-15-2026.pdf, the newest.
bulletin_status: available
publication_reviews:
- parish: st-hedwig-floral-park
  decision: separate
  evidence:
  - url: https://stladislaus.church/wp-content/uploads/2026/11/St.-Ladislaus-November-15-2026.pdf
    seen: 2026-11-13
    note: The November 15, 2026 masthead names St. Ladislaus Church, 18 Richardson Place, Hempstead alone,
      with its own Mass schedule and contact@stladislaus.church.
  - url: https://sthedwig.church/wp-content/uploads/2026/11/StHed_Nov8_26.pdf
    seen: 2026-11-13
    note: The November 08, 2026 masthead names St. Hedwig's Church, One Depan Avenue, Floral Park alone,
      with its own Mass schedule; the same administrator and vicar.
---

## Publisher

St. Ladislaus, Hempstead (a Polish parish, with Spanish and English Masses) publishes its own weekly bulletin. The newest issue on 2026-11-13, `https://stladislaus.church/wp-content/uploads/2026/11/St.-Ladislaus-November-15-2026.pdf` (7 pages, Microsoft Publisher), has the masthead "St. Ladislaus Church, 18 Richardson Place, Hempstead, NY 11550, Website: stladislaus.church", "THIRTY-THIRD SUNDAY IN ORDINARY TIME, November 15, 2026", and a MASS SCHEDULE: daily 9:00 AM; Saturday evening 5:00 PM; Sunday 8:00 AM, 9:30 AM (Polish), 4:00 PM (Spanish). Staff: "ADMINISTRATOR Rev. Dr. Marcin Nabozny", "PAROCHIAL VICAR Rev. Dr. Jerzy Breś".

St. Ladislaus and St. Hedwig, Floral Park share that administrator and vicar (the June 2025 appointments put the vicar's residence at St. Ladislaus), but each publishes its own bulletin: St. Hedwig's issue of November 08, 2026 has its own masthead (One Depan Avenue, Floral Park) and Mass schedule. So they are separate rows (see publication_reviews).

## Worship sites

One: the church at 18 Richardson Place (`st-ladislaus-hempstead-church`). The bulletin's schedule names no other place. The diocesan locator (directory:53), GCatholic (16858) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

stladislaus.church (WordPress) is the locator's link. Its `/bulletin/` page, in tabs, links issues as `wp-content/uploads/<yyyy>/<mm>/<name>.pdf` with irregular names (StLadislausOctober2526.pdf, StLadislaus8Nov2026.pdf, St.-Ladislaus-November-15-2026.pdf). `probe url` reads the site; `probe get` downloads its PDFs.

`fetch:check` (2026-11-13) with page-pdfs on `/bulletin/` picked `St.-Ladislaus-November-15-2026.pdf`, the November 15, 2026 issue, the newest posted.

## Not yet confirmed

Nothing open.
