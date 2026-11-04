---
name: Our Lady of Sorrows, Kearny
website: http://olskearny.org/
bulletin_provider: parishes_online
provider_id: our-lady-of-sorrows-church-07032
publication: ['po-org:our-lady-of-sorrows-church-07032', 'lpi:0018000000QxAA1AAN', 'po-container:03/4021']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/4021/20261101B.pdf
  seen: 2026-11-04
  quote: WELCOME TO OUR LADY OF SORROWS CHURCH!
  note: '1 November 2026 issue, 4 pages, text layer. Page 1: ''136 Davis Avenue Kearny, NJ 07032'', ''Website:
    www.olskearny.org'', ''November 01, 2026''; Weekday Masses Monday - Friday 7:00 AM; Saturday evening
    Mass 5:00 PM; Sunday Mass 9:00 AM; Holy Days 7:00 AM, 7:00 PM. Staff: ''Rev. Cesar J. Quiñones Pastor'',
    ''Rev. Richard J. Mroz In Residence at St. Cecilia''.'
- url: https://parishesonline.com/organization/our-lady-of-sorrows-church-07032
  seen: 2026-11-04
  note: 'probe po: ''Our Lady of Sorrows Church'', 136 Davis Ave, Kearny, New Jersey, 07032, website http://olskearny.org/,
    LPi 0018000000QxAA1AAN, container 03/4021; weekly issues 2026-09-27 to 2026-11-01.'
- url: http://olskearny.org/
  seen: 2026-11-04
  note: probe get and visit.py both answer '503 Service Temporarily Unavailable'; https://www. has a self-signed
    certificate. Kept as the website because the 1 November masthead and the ParishesOnline org both still
    give it.
research:
- method: probe get and visit.py on the parish website
  url: http://olskearny.org/
  checked: '2026-11-04'
  outcome: access-blocked
  next_action: Reload olskearny.org; if it stays down, set website to the ParishesOnline org page
  retry_when: Next audit of the diocese
  revisit_after: 2027-01-15
bulletin_status: available
publication_reviews:
- parish: st-cecilia-kearny
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/4021/20261101B.pdf
    seen: 2026-11-04
    note: The 1 November 2026 masthead names Our Lady of Sorrows alone, 136 Davis Avenue, with its own
      Mass schedule; LPi container 03/4021.
  - url: https://www.church-bulletin.org/bulletin/saint-cecilia-church-kearny-nj-07032/2026-11-01.pdf
    seen: 2026-11-04
    note: The 1 November 2026 masthead names St. Cecilia Church alone, 120 Kearny Ave., with its own Mass
      schedule; John Patrick id 630. Both name Rev. Cesar Quiñones as pastor.
---

## Publisher

Our Lady of Sorrows, Kearny, publishes a weekly LPi bulletin on ParishesOnline (org `our-lady-of-sorrows-church-07032`, container 03/4021). I read the 1 November 2026 issue: page 1 gives '136 Davis Avenue Kearny, NJ 07032', 'Website: www.olskearny.org' and one Mass schedule; page 2 opens 'WELCOME TO OUR LADY OF SORROWS CHURCH!'.

Its staff box lists 'Rev. Cesar J. Quiñones, Pastor' and 'Rev. Richard J. Mroz, In Residence at St. Cecilia': the shared pastor with St. Cecilia, Kearny. St. Cecilia's own John Patrick bulletin (id 630) has its own masthead and schedule, and neither carries the other's Masses, so these are two rows (see `publication_reviews`).

## Worship sites

- Our Lady of Sorrows Church, 136 Davis Avenue (`our-lady-of-sorrows-kearny`): Saturday 5:00 PM; Sunday 9:00 AM; Monday-Friday 7:00 AM (1 November 2026 bulletin, page 1).

The directory (95) and GCatholic (18458) list only this church.

## Website and bulletin provider

Provider `parishes_online`, `provider_id` the org slug. The parish website http://olskearny.org/ answered 503 to both probe get and the browser on 2026-11-04; it stays recorded because the masthead and the ParishesOnline org still name it, and `fetch` reads this row by org slug, not website.

Fetch check (2026-11-04, headed): transport ok, PDF; resolved the latest issue on the ParishesOnline org page and picked container.parishesonline.com/bulletins/03/4021/20261101B.pdf, the 1 November 2026 issue read above; freshness fresh (3 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it.

## Not yet confirmed

Whether olskearny.org is down for good (see `research`).
