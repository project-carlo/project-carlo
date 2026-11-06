---
name: Church of the Korean Martyrs, Saddle Brook
website: https://www.rcckm.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.rcckm.org/
  seen: 2026-11-03
  quote: Unfortunately, this site is temporarily unavailable.
  note: probe get on https://www.rcckm.org/, http://www.rcckm.org and https://rcckm.org/ returned the
    same 316-byte 'Temporarily Unavailable' page; visit.py rendered it with verdict NO-PARISH-WORDS.
- url: http://web.archive.org/web/20260713060348/https://www.rcckm.org/
  seen: 2026-11-03
  quote: VIGIL MASS - SATURDAY 5:00 PM (KOREAN)
  note: 'The Wayback copy of 13 July 2026 (title ''성 백삼위 한인천주교회 RCCKM'') has a 주보 (bulletin) menu with
    one page per year, 2019 to 2026 (2026: /2026-----), and gives the Mass times and the address 585 Saddle
    River Road, Saddle Brook, NJ 07663.'
- url: https://parishesonline.com/organization/church-of-the-korean-martyrs-07663
  seen: 2026-11-03
  note: 'probe po: org ''Church of the Korean Martyrs'', 585 Saddle River Rd, Saddle Brook, NJ 07663,
    website rcckm.org, lpi 0018000000QxAC4AAN, with no publications (''this organization does not publish
    a bulletin here now'').'
revisit: Open https://www.rcckm.org/ (probe get, then visit.py). If it loads, read its 2026 주보 (bulletin)
  page (/2026-----), find where the weekly PDF is hosted, set the provider and run fetch:check. If it
  still answers 'Temporarily Unavailable', read the Wayback copy of /2026----- for the file host.
revisit_after: 2026-11-17
research:
- method: probe get and visit.py on the parish site
  url: https://www.rcckm.org/
  checked: '2026-11-03'
  outcome: access-blocked
  next_action: Reload the site and read its 2026 주보 page for the weekly bulletin's file host
  retry_when: rcckm.org stops answering 'Temporarily Unavailable'
  revisit_after: 2026-11-17
- method: probe po on the ParishesOnline org
  url: https://parishesonline.com/organization/church-of-the-korean-martyrs-07663
  checked: '2026-11-03'
  outcome: not-found
  next_action: Recheck the org only if the parish site links ParishesOnline
  retry_when: The parish site or a bulletin names a ParishesOnline listing
- method: probe get on the Wayback copy of the 2026 bulletin page
  url: https://web.archive.org/web/20260516042728/https://www.rcckm.org/2026-----
  checked: '2026-11-03'
  outcome: access-blocked
  next_action: Fetch the 16 May 2026 snapshot of /2026----- and read where its bulletin links point
  retry_when: web.archive.org stops answering HTTP 429 (it answered 429 on four tries over about three
    minutes)
bulletin_status: access-blocked
---

## Publisher

The parish publishes a weekly bulletin (주보) on its own site, but I could not read it. On 3 November 2026 https://www.rcckm.org/ answered only "Unfortunately, this site is temporarily unavailable." (probe get on three URL forms, and visit.py). The Wayback copy of 13 July 2026 shows the site, titled "성 백삼위 한인천주교회 RCCKM", with a 주보 menu holding one page per year, 2019 to 2026. The 2026 page's snapshot (16 May 2026) answered HTTP 429 on every try, so I don't know where its files are hosted or what format they are in. The ParishesOnline org church-of-the-korean-martyrs-07663 exists but has no issues. Expect the bulletin to be in Korean.

## Worship sites

There is one church, `korean-martyrs-saddle-brook`. The 13 July 2026 homepage snapshot lists Masses only there: Saturday vigil 5:00 PM (Korean), Sunday 8:00 AM and 10:00 AM (Korean) and 12:00 PM (English), and daily Masses in Korean. The archdiocese directory (184) and GCatholic (18552, language Korean) each list only this church. It is a separate parish from St. Philip the Apostle, 410 m down Saddle River Road; St. Philip's 1 November 2026 bulletin doesn't mention it.

## Website and bulletin provider

The website is the parish's own https://www.rcckm.org/ (the directory's and GCatholic's URL), which is down for now. The provider is `no_bulletin` until the bulletin can be read: no recipe can collect it while the site is down, so the row stays off the site (Settled policy 4). `bulletin_status` is `access-blocked`. No fetch check was run, because there is no bulletin source to check.

## Not yet confirmed

- Where the 2026 bulletins are hosted and whether fetch can read them. Next step: see `revisit` and `research` (retry from 2026-11-17, or as soon as rcckm.org or web.archive.org answers).
- Current Mass times. The ones above come from the July 2026 snapshot, not a current source.
