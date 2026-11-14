---
name: St. Gertrude Roman Catholic Church
website: https://stgerts.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stgerts.org/news/bulletin']
group: ''
evidence:
- url: https://stgerts.org/news/bulletin/69-november-8-2026/file
  seen: 2026-11-13
  note: 'Page 1 of the 8 November 2026 issue (24 pages; PDF Creator Canva, the parish''s own layout; downloaded
    through Chrome with tools/browser_get.py). Masthead: ''ST. GERTRUDE ROMAN CATHOLIC CHURCH ... NOVEMBER
    8, 2026 | 32ND SUNDAY IN ORDINARY TIME'', ''28 School Street Bayville, NY 11709''. Mass Schedule:
    Saturday 8:30 am, 5:00 pm Vigil; Sunday 7:30 am, 9:30 am, 11:30 am; Weekdays 8:30 am. ''©LPi'' marks
    only a licensed Scripture reflection; no printer listing or advertising pages.'
- url: https://stgerts.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py (probe url answers 403; stgerts.com redirects
    here): newest first, 69-november-8-2026, 68-november-1-2026.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: ''No PDF
    links found on bulletin post page: https://stgerts.org/news/bulletin/69-november-8-2026/file'' (the
    post is the PDF, which answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://stgerts.org/news/bulletin/69-november-8-2026/file
---

## Publisher

St. Gertrude, 28 School Street, Bayville publishes its own weekly bulletin, laid out by the parish in Canva (PDF Creator "Canva"; no printer's id or advertising pages; the "©LPi" line marks only a licensed Scripture reflection). The 8 November 2026 issue (`https://stgerts.org/news/bulletin/69-november-8-2026/file`, 24 pages, downloaded through Chrome and read 2026-11-13) has the page-1 masthead "ST. GERTRUDE ROMAN CATHOLIC CHURCH / NOVEMBER 8, 2026 | 32ND SUNDAY IN ORDINARY TIME" with "28 School Street Bayville, NY 11709". Its Mass Schedule: Saturday 8:30 am and 5:00 pm Vigil; Sunday 7:30 am, 9:30 am, 11:30 am; Weekdays 8:30 am. The Mass-times page (roster entry read 2026-11-12) gives the same weekend Masses.

## Worship sites

One: the church at 28 School Street (`st-gertrude-bayville-church`). The bulletin's schedule names no other building; its "lower church" is the outreach pantry in the same building. The diocesan locator (directory:43), GCatholic (16810) and the Mass-times page list only this church.

## Website and bulletin provider

stgerts.com (the locator's and GCatholic's link) redirects to stgerts.org, a Solutio (Joomla) site that answers 403 to `probe url`; `visit.py` reads it. Its bulletin list (`/news/bulletin`) links one item per Sunday, newest first, at `/news/bulletin/<n>-<date>/file`. No printer listing exists to collect from instead (the issue is the parish's own Canva layout).

`fetch:check` (2026-11-13) failed: "No PDF links found on bulletin post page: https://stgerts.org/news/bulletin/69-november-8-2026/file". With no printer listing, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, as the diocese's rule for Solutio sites says; it goes live when a collector reads Solutio `/file` links.

## Not yet confirmed

Nothing open.
