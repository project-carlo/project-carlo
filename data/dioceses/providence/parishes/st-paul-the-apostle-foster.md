---
name: St. Paul the Apostle
website: https://stpaulsfoster.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://stpaulsfoster.org/
  seen: 2026-11-14
  quote: Sunday Mass at 8:00 AM and 10:00 AM
  note: 'GoDaddy-builder site, read with probe url, probe get and visit.py --text (home, /resources, /services,
    /family, /faith): Mass times (Saturday 5:00 PM vigil, Sunday 8:00 and 10:00 AM, Monday, Wednesday,
    Friday 9:00 AM) but no bulletin link, PDF or publisher; the only PDF is ''Prayer for Peace.pdf'' on
    /resources.'
- url: https://www.facebook.com/foster.catholic/
  seen: 2026-11-14
  note: 'Parish Facebook page ''Saint Paul the Apostle Catholic Church'' (309 followers), logged-out view:
    newest visible post 12 June 2026 (a bake sale); no bulletin posted.'
revisit: Look again for a bulletin on stpaulsfoster.org and its Facebook page, or ask the office (401-647-3664)
  whether one is published.
revisit_after: 2027-05-01
research:
- method: probe url, probe get and visit.py --bulletin/--text of stpaulsfoster.org and its subpages
  url: https://stpaulsfoster.org/
  checked: '2026-11-14'
  outcome: not-found
  next_action: Recheck the site and Facebook page for a bulletin link, or ask the parish office whether
    a bulletin is published
  retry_when: The site adds a bulletin page or a publisher link, or by the revisit date
- method: visit.py --text of the parish Facebook page (logged out)
  url: https://www.facebook.com/foster.catholic/
  checked: '2026-11-14'
  outcome: not-found
  next_action: Check the page's posts for bulletin images or PDFs with a logged-in view
  retry_when: A logged-in browser session becomes available
bulletin_status: not-found
---

## Publisher

No bulletin found. St. Paul the Apostle, Foster's site (https://stpaulsfoster.org/, read 2026-11-14: home, /resources, /services, /family, /faith) gives Mass times but links no bulletin, PDF issue or publisher, and the finder homepage survey found no publisher there either. Its Facebook page (https://www.facebook.com/foster.catholic/, logged-out view) shows posts but no bulletin; the newest visible was 12 June 2026. Absence only: no source says the parish publishes nothing.

## Worship sites

One church, St. Paul the Apostle, 116A Danielson Pike. The finder (12151) and GCatholic (22366) list only this church.

## Website and bulletin provider

`no_bulletin`, with the parish's own site as website, so the row and its church stay in the records but off the site (Settled policy 4). No fetch:check: there is nothing to fetch.

## Not yet confirmed

Whether the parish publishes a bulletin anywhere (an emailed or paper-only one, or images on Facebook visible only when logged in). See research and revisit.
