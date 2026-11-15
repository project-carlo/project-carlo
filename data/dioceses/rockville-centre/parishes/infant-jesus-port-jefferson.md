---
name: Infant Jesus
website: https://www.infantjesus.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.infantjesus.org/bulletin#infant-jesus']
group: ''
evidence:
- url: https://www.infantjesus.org/bulletin/236-11-08-2026-bulletin/file
  seen: 2026-11-13
  quote: 110 Myrtle Avenue
  note: '8 November 2026 issue (20 pages, Creator Canva, downloaded in Chrome). Page 1 masthead: ''Infant
    Jesus Roman Catholic Church, 110 Myrtle Avenue, Port Jefferson, NY 11777, www.infantjesus.org''; Pastor
    Rev. Gregory Rannazzisi. Mass: weekdays Church 7:30 AM, Chapel 12:00 Noon, Wednesdays 6:00 PM (Spanish);
    Saturday 9:00 AM Church; Saturday Vigil Chapel 4:30 PM; Sunday Church 7:30 AM, 8:45 AM (Spanish),
    10:30 AM, 5:00 PM; Chapel 9:00 AM, 12:00 Noon. Back page: ''#264 FOR ADVERTISING: THE CHURCH BULLETIN
    INC., 200 DALE ST., W. BABYLON''.'
- url: https://www.infantjesus.org/bulletin/236-11-08-2026-bulletin/file
  seen: 2026-11-13
  quote: Church on Main Street, or for the Chapel at St. Charles
  note: 'Page 2: weekly memorials ''are available for either the Church on Main Street, or for the Chapel
    at St. Charles Hospital''; page 8: a First Communion families Mass ''12pm on November 15th in the
    Chapel at St. Charles Hospital''.'
- url: https://www.infantjesus.org/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''pdf 11-08-2026
    Bulletin'' -> /bulletin/236-11-08-2026-bulletin/file, then 11-01-2026, 10-25-2026 ...'
research:
- method: pdftotext of the 8 November 2026 issue for a printer mark; visit.py of the site for an LPi,
    ParishesOnline or John Patrick listing
  url: https://www.infantjesus.org/bulletin
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
    links found on bulletin page: .../236-11-08-2026-bulletin/file" (the /file link is the PDF, which
    Chrome downloads with tools/browser_get.py). Printed by The Church Bulletin Inc. (job #264), which
    posts no listing.'
  url: https://www.infantjesus.org/bulletin/236-11-08-2026-bulletin/file
publication_reviews:
- parish: st-gerard-majella-port-jefferson-station
  decision: separate
  evidence:
  - url: https://www.infantjesus.org/bulletin/236-11-08-2026-bulletin/file
    seen: 2026-11-13
    note: 'The 8 November 2026 masthead names Infant Jesus Roman Catholic Church, 110 Myrtle Avenue alone,
      with its own Mass times (Church and Chapel); Church Bulletin Inc. job #264.'
  - url: https://www.stgmajella.org/news/bulletin/586-november-8-2026/file
    seen: 2026-11-13
    note: 'The 8 November 2026 masthead names St. Gerard Majella Roman Catholic Church, 300 Terryville
      Road alone, with its own Mass times; Church Bulletin Inc. job #195. Same pastor (Rev. Gregory Rannazzisi)
      and clergy as Infant Jesus.'
---

## Publisher

Infant Jesus, 110 Myrtle Avenue, Port Jefferson publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#264 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 8 November 2026 issue (`https://www.infantjesus.org/bulletin/236-11-08-2026-bulletin/file`, downloaded in Chrome 2026-11-13; 20 pages, Creator Canva, text layer readable) has the masthead "Infant Jesus Roman Catholic Church, 110 Myrtle Avenue, Port Jefferson, NY 11777" and names Rev. Gregory Rannazzisi, Pastor.

Rev. Rannazzisi is also pastor of St. Gerard Majella, Port Jefferson Station, and the two share parochial vicars and deacons, but each prints its own bulletin (St. Gerard's is Church Bulletin Inc. job #195, with its own masthead and Mass times): two rows, with a `separate` review. No source names them a pastorate or cluster, so `group` is empty.

## Worship sites

Two places, from the masthead's Mass schedule: "Church" (weekdays 7:30 AM; Saturday 9:00 AM; Sunday 7:30, 8:45 (Spanish), 10:30 AM and 5:00 PM) is the church at 110 Myrtle Avenue (`infant-jesus-port-jefferson-church`); "Chapel" (weekdays 12:00 Noon, Saturday Vigil 4:30 PM, Sunday 9:00 AM and 12:00 Noon) is the chapel at St. Charles Hospital, which the bulletin names ("the Church on Main Street, or for the Chapel at St. Charles Hospital"; "Bread and Wine at Infant Jesus Chapel"), recorded as `infant-jesus-chapel-st-charles-hospital-port-jefferson`. The diocese's Mass-times page also lists the parish's Chapel Masses (4:30 PM Saturday, 9:00 AM and Noon Sunday). The diocesan locator and GCatholic list only the church.

## Website and bulletin provider

www.infantjesus.org is a Solutio (Joomla) site: `probe url` gets 403, `visit.py` reads it. Issues are listed newest first at /bulletin as one `/file` link per Sunday. `fetch:check` (2026-11-13) found the 8 November post and failed: "No PDF links found on bulletin page". The printer, The Church Bulletin Inc., West Babylon (job #264), posts no copies online and the site embeds no other publisher, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

The 8 November issue was the newest posted on 2026-11-13; the 15 November issue was not yet up.
