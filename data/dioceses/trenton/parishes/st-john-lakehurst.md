---
name: St. John's Catholic Church
website: https://www.stjohnlakehurst.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-john-s-catholic-church-lakehurst-nj-08733
publication: ['url:https://www.church-bulletin.org/saint-john-s-catholic-church-lakehurst-nj-08733', 'ecatholic:25374']
group: Cohort 23 (Jackson, Lakehurst, Whiting)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-john-s-catholic-church-lakehurst-nj-08733/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (All Saints Day), image-only (probe pdf: no extractable text),
    so pages 1-2 were read from renders. Page 1: ''St. John''s Catholic Church, 619 Chestnut Street, Lakehurst,
    New Jersey''. Page 2: ''Rev. James F. O''Neill, Pastor''; ''Our parish covers Lakehurst, a small part
    of Jackson, and the eastern half of Manchester''; Sunday Mass Saturday 4 PM and 6 PM, Sunday 9 AM
    and 11 AM; ''CHAPEL SCHEDULE: Daily Mass: Monday to Saturday 8 AM with Rosary at 7:35 AM''. It names
    this parish alone.'
- url: https://www.church-bulletin.org/saint-john-s-catholic-church-lakehurst-nj-08733
  seen: 2026-10-30
  note: John Patrick Publishing listing 6022 ('Saint John's Catholic Church, Lakehurst, NJ 08733'); latest
    edition 1 November 2026.
- url: https://www.stjohnlakehurst.com/bulletins
  seen: 2026-10-30
  quote: October 25, 2026
  note: The parish's own eCatholic site (ecatholic:25374). Its Bulletins page lists one PDF per Sunday
    (files.ecatholic.com/25374/bulletins/<yyyymmdd>.pdf), newest 25 October 2026, and its homepage 'Current
    Bulletin' link goes to jppc.net/onlinebulletins/6022template.pdf. The 25 October eCatholic PDF is
    byte-identical to the listing's 2026-10-25.pdf (md5 97fc0fef74b1ae40a862c7de4e0fe107, 7,221,323 bytes);
    the listing already has 1 November.
- url: https://www.stjohnlakehurst.com/mass-times
  seen: 2026-10-30
  quote: Saturday Vigil
  note: 'Mass Times page (plain fetch; the homepage shows the same): Saturday Vigil 4:00 PM and 6:00 PM,
    Sunday 9:00 AM and 11:00 AM, Monday to Saturday 8:00 AM; confessions in the chapel and in the church
    (homepage).'
- url: https://dioceseoftrenton.org/decisions
  seen: 2026-10-30
  quote: Collaborative Model for all four parishes in the Cohort
  note: 'Faith in Our Future decisions, Cohort 23 (St. Aloysius and St. Monica, Jackson; St. John, Lakehurst;
    St. Elizabeth Ann Seton, Whiting): the Collaborative Model for all four, so a cohort and not a linkage;
    item 2 ''Status of St. Monica to be reviewed periodically, beginning July 1, 2018''. Read in the browser
    with visit.py --text.'
research:
- method: pnpm fetch:check --diocese trenton --parish st-john-lakehurst (headed Chrome); page-pdfs on
    the John Patrick listing
  url: https://www.church-bulletin.org/saint-john-s-catholic-church-lakehurst-nj-08733
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
publication_reviews:
- parish: st-aloysius-jackson
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-aloysius-church-jackson-nj-08527/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Aloysius: page 1 masthead ''SAINT ALOYSIUS
      CHURCH'' names St. Aloysius alone (Pastor Very Rev. John P. Bambrick, Mass schedule 8:30am daily,
      Sat 5:00pm, Sun 7:00am, 8:30am and 10:30am). Different pastor, staff and Mass times from St. John''s,
      Lakehurst.'
- parish: st-monica-jackson
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/church-of-saint-monica-jackson-nj-08527/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Monica: page 1 masthead ''CHURCH OF SAINT
      MONICA'' names St. Monica alone (Pastor Rev. Alex Enriquez, Masses Mon-Thu 9 am, Sat 4 pm, Sun 9
      am and 11 am). Different pastor, staff and Mass times from St. John''s, Lakehurst.'
- parish: st-elizabeth-ann-seton-whiting
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2166/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Elizabeth Ann Seton: page 1 masthead names
      St. Elizabeth Ann Seton, 30 Schoolhouse Road, Whiting alone (Pastor Rev. Evarist Kabagambe, Sat
      4:00 pm, Sun 8:00, 10:00 am and 12:00 pm). Different pastor, staff and Mass times from St. John''s,
      Lakehurst.'
---

## Publisher

St. John's Catholic Church (Lakehurst) publishes one weekly bulletin through John Patrick Publishing (listing 6022 on church-bulletin.org) and posts the same PDF on its own eCatholic site (25374). The 1 November 2026 issue is image-only; its rendered page 1 is headed "St. John's Catholic Church, 619 Chestnut Street, Lakehurst" and page 2 names Rev. James F. O'Neill as pastor, with one Mass schedule for the church and its chapel. It names this parish alone. The other Cohort 23 parishes have their own bulletins (listings 640 and 649; Bon Venture 2166).

## Worship sites

One church, 619 Chestnut Street (see `st-john-lakehurst`). Page 2 of the bulletin has a "Chapel Schedule" (daily Mass Monday to Saturday 8 AM, Monday exposition, confessions): it is the chapel of the same campus, given no street of its own, so it is recorded as part of St. John's site and not a second church. A source giving the chapel a separate address would make it one.

## Website and bulletin provider

stjohnlakehurst.com (eCatholic 25374) refused `probe url` (403) but loaded in the browser. Its /bulletins page is current to 25 October and byte-identical to the listing's issue of the same date; the listing already has 1 November, so the row reads the listing and keeps `ecatholic:25374` in `publication`.

## Not yet confirmed

Nothing outstanding beyond the chapel's address.
