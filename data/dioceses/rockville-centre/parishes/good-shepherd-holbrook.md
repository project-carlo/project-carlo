---
name: Good Shepherd
website: https://goodshepherdrcchurch.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://goodshepherdrcchurch.org/bulletin']
group: ''
evidence:
- url: https://goodshepherdrcchurch.org/bulletin/112-november-8-2026/file
  seen: 2026-11-13
  note: 'November 8, 2026 issue, 16 pages, Creator QuarkXPress (downloaded with browser_get.py; probe
    url answers 403 on the site). Page 1: Rev. Gerald Cestare - Pastor; ''Weekend Masses Saturday Evening
    5:00 PM Sunday 8:00 AM, 10:00 AM, 12Noon & 5:00 PM''; ''Weekday Masses Monday - Friday 9:00 AM''.
    Mass intentions ''For the People of Good Shepherd''. Back pages: ''#233 FOR ADVERTISING: THE CHURCH
    BULLETIN INC., 200 DALE ST., W. BABYLON''. No other church named.'
- url: https://goodshepherdrcchurch.org/bulletin
  seen: 2026-11-13
  note: 'Solutio bulletin list (visit.py): ''November 8, 2026'' (/bulletin/112-november-8-2026/file),
    ''November 1, 2026'', ''October 25, 2026'' ... newest first.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  url: https://goodshepherdrcchurch.org/bulletin/112-november-8-2026/file
  note: 'Solutio (Joomla) site; the bulletin list links each issue as /bulletin/<n>-<date>/file. fetch:check
    on 2026-11-13 found the 8 November post but failed: ''No PDF links found on bulletin post page: .../112-november-8-2026/file''
    (the /file link is the PDF, which Chrome downloads with tools/browser_get.py). Printed by The Church
    Bulletin Inc., which posts no issues online.'
---

## Publisher

Good Shepherd parish, Holbrook publishes its own bulletin, printed by The Church Bulletin Inc., West Babylon (#233), which posts no issues online. The November 8, 2026 issue (`https://goodshepherdrcchurch.org/bulletin/112-november-8-2026/file`, 16 pages, read 2026-11-13) gives on page 1 Weekend Masses Saturday 5:00 PM and Sunday 8:00 AM, 10:00 AM, 12 Noon and 5:00 PM, and Weekday Masses Monday-Friday 9:00 AM; its Mass intentions are "For the People of Good Shepherd". The masthead name is in the cover image, not the text layer.

## Worship sites

One: the church at 1370 Grundy Avenue (`good-shepherd-holbrook-church`). The bulletin names no other worship site; the diocesan locator (73), GCatholic (16863) and the Mass-times page list only this church.

## Website and bulletin provider

goodshepherdrcchurch.org (the locator's address; GCatholic's goodshepherdonline.com was not used) is a Solutio (Joomla) site: `probe url` answered 403, `visit.py` reads it. Its `/bulletin` list links each issue as `/bulletin/<n>-<date>/file`, which downloads in Chrome. The printer, The Church Bulletin Inc., has no online listing (playbook), so there is no printer channel. fetch:check on 2026-11-13 failed ("No PDF links found on bulletin post page"), so, following the diocese's Solutio rule, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish or church. The row goes live when fetch can read Solutio `/file` links.
