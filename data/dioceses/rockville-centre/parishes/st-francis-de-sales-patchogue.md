---
name: St. Francis de Sales
website: https://www.stfrancispatchogue.com/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stfrancispatchogue.com/news/bulletin']
group: ''
evidence:
- url: https://www.stfrancispatchogue.com/news/bulletin/367-bulletin-11-08-2026/file
  seen: 2026-11-13
  note: 'Page 1 of the 8 November 2026 issue, read as an image (12 pages; PDF Creator Canva, Producer
    Acrobat Distiller; downloaded through Chrome with tools/browser_get.py; the text layer overprints
    itself, so page 1 was rendered). Masthead: ''The Roman Catholic Church of St. Francis de Sales, 7
    Amily [sic] Street, Patchogue, New York 11772''; Rev. Dave Atanasio, Pastor. Schedule of Masses: Saturday
    5:30 pm; Sunday 7:00am, 9:15am (Spanish), 11:00am, 5:30pm; Weekdays 9:15am Monday-Friday, 7:00pm Wednesday
    (Spanish). Back page: ''# 268 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON''.'
- url: https://www.stfrancispatchogue.com/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py (probe url: certificate hostname mismatch on
    the bare domain): newest first, ''Bulletin 11-08-2026 New'' (367-bulletin-11-08-2026/file), ''Bulletin
    11/1/2026'' (366-...), ''Bulletin 10/25/2026'' (365-...).'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: ''No PDF
    links found on bulletin page: .../367-bulletin-11-08-2026/file'' (the post is the PDF, which answers
    403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://www.stfrancispatchogue.com/news/bulletin/367-bulletin-11-08-2026/file
---

## Publisher

St. Francis de Sales, 7 Amity Street, Patchogue publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "# 268 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no listing online. The 8 November 2026 issue (`https://www.stfrancispatchogue.com/news/bulletin/367-bulletin-11-08-2026/file`, 12 pages, read 2026-11-13 as an image of page 1, because the text layer overprints itself) has the masthead "The Roman Catholic Church of St. Francis de Sales, 7 Amily Street, Patchogue, New York 11772" and names Rev. Dave Atanasio, Pastor. Schedule of Masses: Saturday 5:30 pm; Sunday 7:00am, 9:15am (Spanish), 11:00am, 5:30pm; weekdays 9:15am Monday-Friday and 7:00pm Wednesday (Spanish).

The same pastor leads Our Lady of Mount Carmel, Patchogue, but that parish has its own masthead, schedule and site (`our-lady-of-mount-carmel-patchogue`; see `publication_reviews`). The drvc.org Mass-times page gives an older schedule (Saturday 5:00 PM; Sunday 7:30, 9:00 Spanish, 10:30, 12:30 Spanish); the bulletin is followed.

## Worship sites

One: the church at 7 Amity Street (`st-francis-de-sales-patchogue-church`). The schedule names no other building. The diocesan locator (directory:93), GCatholic (16897) and the Mass-times page list only this church.

## Website and bulletin provider

The locator links stfrancispatchogue.com and GCatholic stfrancispatch.info; the masthead's e-mail and the Mass-times page use stfrancispatchogue.com, whose www. host is a Solutio (Joomla) site (the bare domain fails certificate verification for `probe url`). `/news/bulletin` lists the issues newest first, each a `/news/bulletin/<n>-<date>/file` PDF that Chrome downloads with tools/browser_get.py. The printer posts nothing online, so following the diocese's rule for Solutio sites the row is `unsupported` with `fetch_gap` `joomla-file-endpoint` (see the gap note for the fetch:check result).

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
