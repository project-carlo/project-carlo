---
name: St. Christopher
website: https://stchrisbaldwin.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://stchrisbaldwin.org/bulletin/ filename=St.-Christopher-Bulletin*.pdf
publication: ['url:https://stchrisbaldwin.org/bulletin/#st-christopher']
group: ''
evidence:
- url: https://stchrisbaldwin.org/wp-content/uploads/2026/11/St.-Christopher-Bulletin-11-8-26.pdf
  seen: 2026-11-13
  quote: Rev. Johnny R. Mendonça—Pastor
  note: Issue for November 8th, 2026, 32nd Sunday in Ordinary Time (16 pages, made in Canva). Cover masthead
    'The Parish of St.Christopher, Baldwin, New York'; page 2 (an image, rendered) gives MASS TIMES Saturday
    5:00 PM; Sunday 7:30 AM, 9:30 AM, 11:30 AM, 5:00 PM, 7:00 PM (Spanish); Weekdays 7:00 AM & 9:00 AM
    (M-F), 9:00 AM (Saturdays); office 15 Pershing Blvd, Baldwin, NY 11510. Downloaded through Chrome
    (tools/browser_get.py); probe pdf could not connect.
- url: https://stchrisbaldwin.org/bulletin/
  seen: 2026-11-13
  note: 'The WordPress Bulletin page lists one PDF per Sunday, newest first: St.-Christopher-Bulletin-11-8-26.pdf,
    -11-1-26, -10-25-26 ... after a parish registration form (read with parish-site-access visit.py).'
bulletin_status: available
---

## Publisher

St. Christopher, Baldwin publishes its own weekly bulletin, made in Canva and posted on its WordPress site. The newest issue on 2026-11-13, `https://stchrisbaldwin.org/wp-content/uploads/2026/11/St.-Christopher-Bulletin-11-8-26.pdf` (16 pages), has the cover "The Parish of St.Christopher, Baldwin, New York, November 8th, 2026, 32nd Sunday in Ordinary Time" and names "Rev. Johnny R. Mendonça—Pastor" on page 1. Page 2 is an image (rendered to read it): "MASS TIMES Saturday: 5:00 PM Sunday: 7:30 AM, 9:30 AM, 11:30 AM, 5:00 PM, 7:00 PM (Spanish) Weekdays: 7:00 AM & 9:00 AM (M-F) 9:00 AM (Saturdays)", parish office at 15 Pershing Blvd, Baldwin. The drvc.org Mass-times page gives a slightly older schedule (Sunday 11:00 AM and 12:30 PM where the bulletin has 11:30 AM).

## Worship sites

One: the church at 11 Gale Avenue (`st-christopher-baldwin-church`). The schedule names no other place; the bulletin also mentions an Adoration Chapel (in the old school building, per the Mass-times page) for adoration, not Mass. The diocesan locator (directory:39), GCatholic (16808) and the Mass-times page list only this church.

## Website and bulletin provider

stchrisbaldwin.org is the locator's and Mass-times page's link (GCatholic gives stchris.com). `probe url` and `probe pdf` could not connect; the site loads in the browser, and fetch reads it. Its `/bulletin/` page lists issues newest first after a registration-form PDF. `fetch:check` (2026-11-13) with page-pdfs on `/bulletin/` picked the 8 November 2026 issue, the newest posted; the recipe adds `filename=St.-Christopher-Bulletin*.pdf` to keep the form out.

## Not yet confirmed

Nothing open.
