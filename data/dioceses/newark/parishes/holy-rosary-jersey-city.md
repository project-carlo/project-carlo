---
name: Holy Rosary, Jersey City
website: https://www.holyrosarychurch.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/619
publication: ['url:https://www.church-bulletin.org/holy-rosary-church-jersey-city-nj-07302']
group: Planning Area F
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-rosary-church-jersey-city-nj-07302/2026-11-01.pdf
  seen: 2026-11-03
  quote: Celebrating 141 Years as the First Italian Parish in the State of New Jersey
  note: '1 November 2026 John Patrick issue, page 1 masthead: ''Holy Rosary Church'', ''Rev. Rafal Smola,
    Pastor'', ''344 Sixth Street Jersey City, New Jersey 07302'', Website www.HolyRosaryChurch.com. Mass
    Schedule: Monday-Friday 8:30 am; Saturday 5:00 pm (Vigil); Sunday 9:00 am (Italian/English), 11:30
    am (English). Page 3 lists weekday Masses as ''Mass (Chapel)''.'
- url: https://www.church-bulletin.org/bulletin/holy-rosary-church-jersey-city-nj-07302/2026-11-01.pdf
  seen: 2026-11-03
  quote: Holy Rosary Church 619 Page 1
  note: Page 2 header gives the John Patrick account 619.
- url: https://church-bulletin.org/619
  seen: 2026-11-03
  quote: Latest Edition November 1, 2026 Bulletin
  note: Redirects to www.church-bulletin.org/holy-rosary-church-jersey-city-nj-07302, 'Holy Rosary Church,
    Jersey City, NJ 07302', 344 6th Street; weekly archive back through 2026.
- url: https://www.holyrosarychurch.com/
  seen: 2026-11-03
  note: 'probe url: HTTP 403. visit.py (browser) loads an eCatholic site (ecatholic:36975), title ''Holy
    Rosary Church - Jersey City, NJ'', ''344 Sixth St., Jersey City''; its bulletin link is https://www.jppc.net/onlinebulletins/619template.pdf
    (John Patrick account 619).'
bulletin_status: available
---

## Publisher

Holy Rosary, Jersey City (the first Italian national parish in New Jersey) publishes a weekly bulletin printed by John Patrick Publishing, account 619. I read the 1 November 2026 issue (church-bulletin.org/bulletin/holy-rosary-church-jersey-city-nj-07302/2026-11-01.pdf): the page 1 masthead names 'Holy Rosary Church', 344 Sixth Street, with Rev. Rafal Smola as pastor, and one Mass schedule for this church alone. Page 2's header reads 'Holy Rosary Church 619 Page 1'.

St. Anthony of Padua stands next door (330 Sixth Street, `st-anthony-of-padua-jersey-city`), and an earlier batch asked whether the two share a bulletin. They don't: St. Anthony's 1 November 2026 LPi issue (container 04/1040) names Very Rev. Canon Joseph Urban as pastor and has no mention of 'Rosary' (probe pdf grep, 0 hits), while Holy Rosary's issue names a different pastor and only its own Masses.

## Worship sites

- Holy Rosary, 344 Sixth Street (`holy-rosary-jersey-city`): Monday-Friday 8:30 am; Saturday 5:00 pm vigil; Sunday 9:00 am Italian/English and 11:30 am English. Weekday Masses are in the parish chapel, which the parish site places 'in between the church and parish office, below the parish office building', on the same property, so it is not a separate church row.

The directory (93) and GCatholic (18438) list only this church.

## Website and bulletin provider

https://www.holyrosarychurch.com/ is an eCatholic site (ecatholic:36975) that answers `probe url` with 403 and loads in the browser (visit.py, 2026-11-03). Its bulletin link is jppc.net/onlinebulletins/619template.pdf, so the eCatholic id is only the website and is left out of `publication`. The survey listed holyrosarychurch.com among lost domains; it is live. The provider is `other`, read with `page-pdfs https://church-bulletin.org/619`, the dated listing, per the playbook.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/619: current` and picked church-bulletin.org/bulletin/holy-rosary-church-jersey-city-nj-07302/2026-11-01.pdf, the 1 November 2026 issue read above; freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing open.
