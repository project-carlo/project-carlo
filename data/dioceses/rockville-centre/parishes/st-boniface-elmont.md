---
name: St. Boniface
website: https://www.saintbonifaceelmont.com/news-events/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.saintbonifaceelmont.com/news-events/bulletin#st-boniface']
group: ''
evidence:
- url: https://www.saintbonifaceelmont.com/news-events/bulletin/331-november-8-2026/file
  seen: 2026-11-13
  quote: The Parish of St. Boniface
  note: 'Issue for November 8, 2026 (12 pages, made in Canva). Cover: The Parish of St. Boniface Roman
    Catholic Church, 631 Elmont Road, Elmont; Rev. Joseph Baidoo, Pastor; MASS TIMES Monday-Friday 7:00,
    8:30 am; Saturday 8:30 am, 5:00 pm (Vigil); Sunday 7:00 am, 9:00 am, 11:00 & 1:00 pm; Spanish Saturday
    8:00 pm (U.C), Sunday 1:00 pm (L.C); Haitian Sunday 10:00 am (L.C). Downloaded through Chrome (tools/browser_get.py).'
- url: https://www.saintbonifaceelmont.com/news-events/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin page, read with parish-site-access visit.py (probe url answers 403):
    issues newest first as /news-events/bulletin/<n>-<date>/file, the newest 331-november-8-2026.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../331-november-8-2026/file" (the /file link is the PDF, which
    Chrome downloads with tools/browser_get.py). The issue is made in Canva; no printer listing.'
  url: https://www.saintbonifaceelmont.com/news-events/bulletin/331-november-8-2026/file
---

## Publisher

St. Boniface, Elmont publishes its own weekly bulletin, made in Canva (PDF Creator "Canva"); no printer's name or listing appears. The newest issue on 2026-11-13, `https://www.saintbonifaceelmont.com/news-events/bulletin/331-november-8-2026/file` (12 pages), has the cover "The Parish of St. Boniface Roman Catholic Church, 631 Elmont Road, Elmont, NY 11003, November 8, 2026", "Rev. Joseph Baidoo, Pastor", and MASS TIMES: Monday-Friday 7:00 and 8:30 am; Saturday 8:30 am and 5:00 pm (Vigil); Sunday 7:00 am, 9:00 am, 11:00 and 1:00 pm; Spanish Saturday 8:00 pm (U.C) and Sunday 1:00 pm (L.C); Haitian Sunday 10:00 am (L.C).

## Worship sites

One: the church at 631 Elmont Road (`st-boniface-elmont-church`). "U.C" and "L.C" are its upper and lower churches, one building. The diocesan locator (directory:35), GCatholic (16840) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

saintbonifaceelmont.com is a Solutio (Joomla) site, the locator's and Mass-times page's link. `probe url` answers 403; visit.py reads it. Its bulletin page lists issues newest first as `/news-events/bulletin/<n>-<date>/file`; Chrome downloads them (tools/browser_get.py).

`fetch:check` (2026-11-13) found the 8 November post but failed: "No PDF links found on bulletin post page", because the `/file` link is itself the PDF. The issue is made in Canva and no printer listing is linked, so under the diocese's rule for Solutio sites the row is `unsupported` with fetch_gap `joomla-file-endpoint`.

## Not yet confirmed

Nothing open.
