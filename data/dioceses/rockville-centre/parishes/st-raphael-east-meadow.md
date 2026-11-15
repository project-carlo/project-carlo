---
name: St. Raphael
website: https://www.straphaelparish.org/about-us/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.straphaelparish.org/about-us/bulletin']
group: ''
evidence:
- url: https://www.canva.com/design/DAHZ4RIcMMM/V8Pa0kP8A2xbKI5FS4wS5A/view
  seen: 2026-11-13
  note: 'Where the 8 November 2026 bulletin link redirects (visit.py; page title ''St. Raphael - 11/8/26'',
    12 pages, read as screenshots). Page 1: ''NOVEMBER 8, 2026 + THIRTY-SECOND SUNDAY IN ORDINARY TIME
    ... The Parish of St. Raphael, EAST MEADOW, NEW YORK''. Page 2: ''The Parish of St. Raphael, 600 Newbridge
    Road, East Meadow, NY 11554''; Pastor Father Leo Song; Associate Pastor Father Stan Choragwicki.'
- url: https://www.straphaelparish.org/about-us/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url answers 403): 361-november-8-2026/file, 360-november-1-2026/file,
    359-october-25-2026/file, newest first; each /file redirects to a Canva view link.'
- url: https://www.straphaelparish.org/
  seen: 2026-11-13
  note: 'Home page (visit.py): Weekend Mass Saturday 5:00 pm; Sunday 8:00 am, 10:00 am, 12:00 pm & 5:00
    pm; first Sunday 2 pm Mass for people and families with special needs; Weekday Mass Monday-Friday
    7:30 am & 9:00 am, Saturday 9:00 am. ''Site by Solutio''.'
bulletin_status: unsupported-format
fetch_gap:
  kind: canva-design-viewer
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list whose /file links redirect to a Canva design viewer (canva.com/design/<id>/<key>/view),
    not a PDF; probe get answers 403 on /file. fetch:check on 2026-11-13: ''No PDF links found on bulletin
    post page: .../361-november-8-2026/file''. The pages can only be read as screenshots.'
  url: https://www.straphaelparish.org/about-us/bulletin/361-november-8-2026/file
---

## Publisher

The Parish of St. Raphael, 600 Newbridge Road, East Meadow publishes its own weekly bulletin, designed in Canva and posted as a Canva view link. The 8 November 2026 issue (the list's `361-november-8-2026/file`, which redirects to `https://www.canva.com/design/DAHZ4RIcMMM/V8Pa0kP8A2xbKI5FS4wS5A/view`, 12 pages, read 2026-11-13 as screenshots) has the cover "NOVEMBER 8, 2026 ... The Parish of St. Raphael, EAST MEADOW, NEW YORK" and on page 2 "The Parish of St. Raphael, 600 Newbridge Road, East Meadow, NY 11554", with Father Leo Song, Pastor. Pages 1-3 of the issue were read; the Mass schedule was not found there. The parish home page (read 2026-11-13) gives Saturday 5:00 pm; Sunday 8:00 am, 10:00 am, 12:00 pm and 5:00 pm, with a 2 pm Mass for people with special needs on the first Sunday; Monday-Friday 7:30 am and 9:00 am; Saturday 9:00 am. That matches the drvc.org Mass-times page.

## Worship sites

One: the church at 600 Newbridge Road (`st-raphael-east-meadow-church`). The home page's schedule names no other building. The diocesan locator (directory:63), GCatholic (16835) and the Mass-times page list only this church.

## Website and bulletin provider

straphaelparish.org is a Solutio (Joomla) site (`probe url` answers 403; `visit.py` reads it). `/about-us/bulletin` lists issues newest first as `/about-us/bulletin/<n>-<date>/file`, but each one redirects to a Canva design viewer rather than a PDF, so no collector can read it: the row is `unsupported` with `fetch_gap` `canva-design-viewer`. `fetch:check` (2026-11-13) failed: "No PDF links found on bulletin post page". No printer's listing applies, since the parish designs the bulletin in Canva itself.

## Not yet confirmed

The Mass schedule was taken from the home page, not the bulletin (pages 4-12 of the Canva issue were not read). When a collector reads Canva view links, set the provider, run `fetch:check` and clear `fetch_gap`.
