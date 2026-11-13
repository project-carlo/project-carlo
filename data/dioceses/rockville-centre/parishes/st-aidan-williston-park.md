---
name: St. Aidan
website: https://staidanparish.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://staidanparish.org/bulletins/
publication: ['url:https://staidanparish.org/bulletins/#st-aidan']
group: ''
evidence:
- url: https://staidanparish.org/wp-content/uploads/2026/11/NOVEMBER-08-BULLETIN.pdf
  seen: 2026-11-13
  quote: ST. AIDAN CATHOLIC CHURCH & SCHOOL
  note: Issue for November 8, 2026 (28 pages, Microsoft Word). Masthead names St. Aidan, 505 Willis Ave.,
    Williston Park alone; its Mass intentions list daily 6:30 AM, 9:00 AM, 5:30 PM; Saturday 9:00 AM,
    5:00 PM, 7:30 PM; Sunday 7:30, 9:00, 10:30 AM, 12:00 PM, 5:00 PM; Pastor Father Michael Bissex.
- url: https://staidanparish.org/bulletins/
  seen: 2026-11-13
  note: WordPress bulletin page (read with parish-site-access visit.py; probe url could not connect) lists
    issues newest first, NOVEMBER-08-BULLETIN.pdf first, back to August 2026.
bulletin_status: available
---

## Publisher

St. Aidan, Williston Park publishes its own weekly bulletin, made in Microsoft Word and posted on its WordPress site. The newest issue on 2026-11-13, `https://staidanparish.org/wp-content/uploads/2026/11/NOVEMBER-08-BULLETIN.pdf` (28 pages), opens "ST. AIDAN CATHOLIC CHURCH & SCHOOL, WILLISTON PARK, NEW YORK", "serving the communities of Williston Park, East Williston, Albertson, Mineola, Roslyn Heights, and Searingtown", gives the address 505 Willis Ave., Williston Park NY 11596, and names "Pastor Father Michael Bissex". Its Mass intentions for November 9-15 list weekday Masses at 6:30 AM, 9:00 AM and 5:30 PM; Saturday 9:00 AM, 5:00 PM and 7:30 PM; Sunday 7:30 AM, 9:00 AM, 10:30 AM, 12:00 PM and 5:00 PM.

## Worship sites

One: the church at 505 Willis Avenue (`st-aidan-williston-park-church`). The bulletin's schedule names no other place (the convent and school are mentioned only as meeting places). The diocesan locator (directory:29), GCatholic (16935) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

The site `staidanparish.org` (the locator's and GCatholic's link) did not answer `probe url` (egress proxy EOF) but loads in a browser; its `/bulletins/` page lists issues as `wp-content/uploads/<yyyy>/<mm>/<MONTH>-<DD>-BULLETIN.pdf`, newest first (one stray name, `Aidan10-11R.pdf`, for October 11). `probe pdf` was disconnected too, so the issue was downloaded with the run's `browser_get.py`.

`fetch:check` (2026-11-13) with `page-pdfs https://staidanparish.org/bulletins/` picked `NOVEMBER-08-BULLETIN.pdf` (url_date 2026-11-08), the newest issue posted.

## Not yet confirmed

Nothing open.
