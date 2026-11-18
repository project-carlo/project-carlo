---
name: St. Lawrence the Martyr
website: https://www.stlawrencesayville.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stlawrencesayville.org/news/bulletin']
group: ''
evidence:
- url: https://www.stlawrencesayville.org/news/bulletin/312-november-8-2026/file
  seen: 2026-11-13
  note: '8 November 2026 issue, 6 pages, Creator Canva (downloaded with browser_get.py; probe url answers
    403 on the site). Page 1: ''The Parish of St. Lawrence the Martyr'', Rev. Brian J. Ingram, Pastor,
    ''240 West Main Street, Sayville, New York 11782''. Page 2 ''Mass Schedule'' of intentions: Saturday
    9:00 and 5:00, Sunday 7:30, 9:00, 11:00, Monday-Friday 9:00. No printer footer, no other church named.'
- url: https://www.stlawrencesayville.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio bulletin list (visit.py): ''November 8, 2026'' (312-november-8-2026/file), ''November
    1, 2026'', ''October 25, 2026'' ... newest first.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  url: https://www.stlawrencesayville.org/news/bulletin/312-november-8-2026/file
  note: 'Solutio (Joomla) site; the bulletin list links each issue as /news/bulletin/<n>-<date>/file.
    fetch:check on 2026-11-13 found the 8 November post but failed: ''No PDF links found on bulletin post
    page: .../312-november-8-2026/file'' (the /file link is the PDF, which Chrome downloads with tools/browser_get.py).
    The issue is made in Canva; no printer listing.'
---

## Publisher

The Parish of St. Lawrence the Martyr, 240 West Main Street, Sayville makes its own bulletin in Canva. The 8 November 2026 issue (`https://www.stlawrencesayville.org/news/bulletin/312-november-8-2026/file`, 6 pages, read 2026-11-13) has the masthead "The Parish of St. Lawrence the Martyr" and the Mass intentions for one church: Saturday 9:00 and 5:00, Sunday 7:30, 9:00 and 11:00, weekdays 9:00.

## Worship sites

One: the church at 240 West Main Street (`st-lawrence-the-martyr-sayville-church`). The bulletin names no mission or chapel; the diocesan locator (119), GCatholic (16911) and the Mass-times page list only this church. The bulletin does not mention the Fire Island chapels.

## Website and bulletin provider

stlawrencesayville.org is a Solutio (Joomla) site (`probe url` answered 403; `visit.py` reads it). Its `/news/bulletin` list links each issue as `/news/bulletin/<n>-<date>/file`, which answers 403 to `probe get` but downloads in Chrome. The issue's Creator is Canva and it carries no printer's footer, so there is no ParishesOnline or John Patrick listing to use. fetch:check on 2026-11-13 failed ("No PDF links found on bulletin post page"), so, following the diocese's Solutio rule, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish or church. The row goes live when fetch can read Solutio `/file` links.
