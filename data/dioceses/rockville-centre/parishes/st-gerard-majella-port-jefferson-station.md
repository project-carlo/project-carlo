---
name: St. Gerard Majella
website: https://www.stgmajella.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stgmajella.org/news/bulletin#st-gerard-majella']
group: ''
evidence:
- url: https://www.stgmajella.org/news/bulletin/586-november-8-2026/file
  seen: 2026-11-13
  quote: 300 Terryville Road
  note: '8 November 2026 issue (16 pages, Creator Canva, downloaded in Chrome). Page 1 masthead: ''St.
    Gerard Majella Roman Catholic Church, 300 Terryville Road, Port Jefferson Station, NY 11776, www.stgmajella.org'';
    Pastor Rev. Gregory Rannazzisi. Mass & Devotions: Saturday 5:00pm; Sunday 8:00am, 10:00am, 12:00pm;
    Weekdays 9:00am; First Saturday 11:00am Mass with the Anointing of the Sick. Back page: ''#195 FOR
    ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON''.'
- url: https://www.stgmajella.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''pdf November 8,
    2026'' -> /news/bulletin/586-november-8-2026/file, then November 1, October 25 ...'
research:
- method: pdftotext of the 8 November 2026 issue for a printer mark; visit.py of the site for an LPi,
    ParishesOnline or John Patrick listing
  url: https://www.stgmajella.org/news/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post and failed: "No PDF
    links found on bulletin post page: .../586-november-8-2026/file" (the /file link is the PDF, which Chrome
    downloads with tools/browser_get.py). Printed by The Church Bulletin Inc. (job #195), which posts
    no listing.'
  url: https://www.stgmajella.org/news/bulletin/586-november-8-2026/file
publication_reviews:
- parish: infant-jesus-port-jefferson
  decision: separate
  evidence:
  - url: https://www.stgmajella.org/news/bulletin/586-november-8-2026/file
    seen: 2026-11-13
    note: 'The 8 November 2026 masthead names St. Gerard Majella Roman Catholic Church, 300 Terryville
      Road alone, with its own Mass times; Church Bulletin Inc. job #195.'
  - url: https://www.infantjesus.org/bulletin/236-11-08-2026-bulletin/file
    seen: 2026-11-13
    note: 'The 8 November 2026 masthead names Infant Jesus Roman Catholic Church, 110 Myrtle Avenue alone,
      with its own Mass times (Church and Chapel); Church Bulletin Inc. job #264. Same pastor (Rev. Gregory
      Rannazzisi).'
---

## Publisher

St. Gerard Majella, 300 Terryville Road, Port Jefferson Station publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#195 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 8 November 2026 issue (`https://www.stgmajella.org/news/bulletin/586-november-8-2026/file`, downloaded in Chrome 2026-11-13; 16 pages, Creator Canva, text layer readable) has the masthead "St. Gerard Majella Roman Catholic Church, 300 Terryville Road, Port Jefferson Station, NY 11776" and names Rev. Gregory Rannazzisi, Pastor.

Rev. Rannazzisi is also pastor of Infant Jesus, Port Jefferson, and the two share parochial vicars and deacons, but each prints its own bulletin (Infant Jesus's is Church Bulletin Inc. job #264, with its own masthead and Mass times): two rows, with a `separate` review. No source names them a pastorate or cluster, so `group` is empty.

## Worship sites

One row: the church at 300 Terryville Road (`st-gerard-majella-port-jefferson-station-church`). The masthead's "Mass & Devotions" lists Saturday 5:00pm; Sunday 8:00am, 10:00am, 12:00pm; Weekdays 9:00am, with no other place named. The diocesan locator (directory:91), GCatholic (16901) and the Mass-times page list the same one church.

## Website and bulletin provider

www.stgmajella.org is a Solutio (Joomla) site: `probe url` gets 403, `visit.py` reads it. Issues are listed newest first at /news/bulletin as one `/file` link per Sunday. `fetch:check` (2026-11-13) found the 8 November post and failed: "No PDF links found on bulletin post page". The printer, The Church Bulletin Inc., West Babylon (job #195), posts no copies online and the site embeds no other publisher, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

The 8 November issue was the newest posted on 2026-11-13; the 15 November issue was not yet up.
