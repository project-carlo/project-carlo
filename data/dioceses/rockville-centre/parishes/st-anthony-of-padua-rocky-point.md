---
name: St. Anthony of Padua
website: https://www.stanthonyrp.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stanthonyrp.org/news/bulletin#st-anthony-of-padua']
group: ''
evidence:
- url: https://www.stanthonyrp.org/news/bulletin/309-november-15-2026/file
  seen: 2026-11-13
  quote: '614 Rte 25A, Rocky Point: 631-744-2609'
  note: '15 November 2026 issue (16 pages, Creator Canva, downloaded in Chrome). Page 3 masthead: ''St.
    Anthony of Padua Church, "Beautiful" Rocky Point''; Pastor Rev. Collins Adutwum. Mass schedule: Saturday
    Evening 5PM; Sunday 8AM, 10AM, 12 Noon; Weekday Masses 8AM Monday through Saturday. Back page: ''#267
    FOR ADVERTISING: THE CHURCH BULLETIN INC. 200 DALE ST. W.BABYLON''.'
- url: https://www.stanthonyrp.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url of www.starockypoint.com gets 403 and redirects
    here): newest first, 309-november-15-2026, 308-november-8-2026 ...'
research:
- method: pdftotext of the 15 November 2026 issue for a printer mark (4lpi.com, LPi footer, John Patrick);
    visit.py of the site for an embedded publisher
  url: https://www.stanthonyrp.org/news/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (as provider other, unpinned) found the 15 November
    post and failed: ''No PDF links found on bulletin post page: .../309-november-15-2026/file'' (the
    /file link is the PDF, which Chrome downloads with tools/browser_get.py). Printed by The Church Bulletin
    Inc. (job #267), which posts no listing.'
  url: https://www.stanthonyrp.org/news/bulletin/309-november-15-2026/file
---

## Publisher

St. Anthony of Padua, 614 Route 25A, Rocky Point publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#267 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 15 November 2026 issue (`https://www.stanthonyrp.org/news/bulletin/309-november-15-2026/file`, downloaded in Chrome 2026-11-13; 16 pages, Creator Canva, text layer readable) has its masthead on page 3: "St. Anthony of Padua Church, “Beautiful” Rocky Point", Pastor Rev. Collins Adutwum, "614 Rte 25A, Rocky Point: 631-744-2609". No other parish is named in the masthead; `group` is empty.

## Worship sites

One: the Mass schedule on page 3 ("Saturday Evening: 5PM / Sunday: 8AM, 10AM, 12 Noon / Weekday Masses: 8AM Monday through Saturday") names no second place, so all Masses are at the church (`st-anthony-of-padua-rocky-point-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church.

## Website and bulletin provider

The diocese lists www.starockypoint.com, which redirects to www.stanthonyrp.org (`probe url` gets 403; `visit.py` reads it). It is a Solutio (Joomla) site listing issues newest first at /news/bulletin as one post per Sunday whose `/file` link is the PDF. `fetch:check` (2026-11-13, as provider `other`) found the 15 November post and failed: "No PDF links found on bulletin post page". The printer posts no listing and the issue carries no LPi or John Patrick mark, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` links.
