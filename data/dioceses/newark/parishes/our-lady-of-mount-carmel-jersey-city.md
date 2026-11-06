---
name: Our Lady of Mount Carmel, Jersey City
website: https://olmcjc.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6051O
publication: ['url:https://www.church-bulletin.org/our-lady-of-mount-carmel-jersey-city-nj-07306-o']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-jersey-city-nj-07306-o/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 6 pages, image only (read with render.py). Page 1 masthead: ''Our Lady
    of Mount Carmel'', ''November 1st, 2026'', ''Roman Catholic Church | EST 1905, 99 Broadway, Jersey
    City, NJ 07306 | 201-435-7080'', ''WWW.OLMCJC.COM''; Mass Schedule: Saturday Vigil 5 PM (English),
    Sunday 9:00 AM (English), 11:15 AM (Español); daily 8:30 AM (English), Tuesdays and Thursdays 6:30
    PM (Español). Rev. Pedro Repollet, Pastor. Page 6 footer: ''6051 Our Lady of Mt. Carmel & St. Ann,
    Jersey City, NJ (B) … John Patrick Publishing Co.'''
- url: https://church-bulletin.org/6051O
  seen: 2026-11-03
  note: John Patrick listing 'Our Lady of Mount Carmel Bulletin' (canonical slug our-lady-of-mount-carmel-jersey-city-nj-07306-o),
    dated issues through 2026-11-01. The bare id church-bulletin.org/6051 opens an 'Our Lady of Mount
    Carmel' page with no issues; 6051A is St. Ann's separate bulletin.
- url: https://olmcjc.com/
  seen: 2026-11-03
  quote: Current Bulletin &#038; Archive
  note: Homepage menu links https://church-bulletin.org/?id=6051O; probe get, no mention of St. Ann.
bulletin_status: available
publication_reviews:
- parish: st-ann-jersey-city
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-jersey-city-nj-07306-o/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Our Lady of Mount Carmel alone (99 Broadway), with its own
      Mass schedule; listing 6051O.
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-mount-carmel-jersey-city-nj-07306-a/2026-11-01.pdf
    seen: 2026-11-03
    note: The 1 November 2026 masthead names Saint Ann's Polish R. C. Church alone (291 St. Paul's Ave),
      with its own Mass schedule; listing 6051A.
---

## Publisher

Our Lady of Mount Carmel, Jersey City publishes a weekly bulletin printed by John Patrick Publishing, under account 6051, listing `6051O`. I read the 1 November 2026 issue (6 pages, image only, rendered with render.py). The page 1 masthead says 'Our Lady of Mount Carmel … Roman Catholic Church | EST 1905, 99 Broadway, Jersey City, NJ 07306', with one Mass schedule and Rev. Pedro Repollet as pastor. The page 6 footer says '6051 Our Lady of Mt. Carmel & St. Ann, Jersey City, NJ (B)'.

The footer names both parishes because Fr. Repollet has also administered St. Ann (Polish) since November 2025, and John Patrick prints both bulletins under one account. They are still two bulletins. Listing 6051A (from 30 November 2025) carries St. Ann's own issue, 'Saint Ann's Polish R. C. Church, 291 St. Paul's Ave', with its own Mass schedule (`st-ann-jersey-city`). The OLMC issue's pages 2 to 5 (intentions, parish news, flyers) do not mention St. Ann. So these are separate rows, recorded in `publication_reviews`.

## Worship sites

- Our Lady of Mount Carmel, 99 Broadway (`our-lady-of-mount-carmel-jersey-city`): Saturday 5:00 PM; Sunday 9:00 AM, 11:15 AM (Spanish); weekdays 8:30 AM, and Tuesday and Thursday 6:30 PM (Spanish). These are the page 1 and page 2 schedules.

A page 3 notice says that from 10 May 2026, because of repairs to the church building, 'all Masses will be held in the Parish Hall'. The hall is the parish's own and at the same address, so this stays one church row at 99 Broadway. The directory (90) and GCatholic (18441) list only this church.

## Website and bulletin provider

https://olmcjc.com/ is the parish site. Its 'Current Bulletin & Archive' menu item links church-bulletin.org/?id=6051O. GCatholic gives the old domain www.olmcjc.org, which `publisher_fingerprint.sh` could not fetch; the masthead says WWW.OLMCJC.COM. The provider is `other`, read with `page-pdfs https://church-bulletin.org/6051O`. That pins the dated listing and not `?id=` (see the playbook). The bare `church-bulletin.org/6051` shows an empty page, and `6051A` is St. Ann's, so the `O` suffix matters.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/6051O: current` and picked church-bulletin.org/bulletin/our-lady-of-mount-carmel-jersey-city-nj-07306-o/2026-11-01.pdf, the 1 November 2026 issue read above (date from the file name); freshness fresh (2 days). Publication identity `unverified` only because the issue is image only and no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

How long the church repairs (Masses in the parish hall) will last. The bulletin gives no end date, and the row does not depend on it.
