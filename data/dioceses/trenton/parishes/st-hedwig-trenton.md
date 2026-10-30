---
name: St. Hedwig Parish
website: https://www.sainthedwigparish.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-hedwig-parish-trenton-nj-08638
publication: ['url:https://www.church-bulletin.org/saint-hedwig-parish-trenton-nj-08638']
group: Cohort 9
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
  seen: 2026-10-30
  quote: SAINT HEDWIG PARISH
  note: '1 November 2026 issue, 7 pages, text layer on 6 (page 1 is an image). Page 2 (bilingual English/Polish):
    ''SAINT HEDWIG PARISH / PARAFIA ŚW. JADWIGI'', ''872 Brunswick Ave., Trenton, N.J. 08638'', pastor
    Rev. Can. Dr. Jacek W. Labinski. MASS SCHEDULE: Saturday 5 P.M. (English); Sunday 8 A.M. (Polish),
    9:30 A.M. (English), 11 A.M. (Polish); Daily 8 A.M. (Monday and Friday) in Chapel (English); Wed.
    7 P.M. (Polish) in Chapel with Novena; Holy Days 8 A.M. (English-Chapel) and 7 P.M. (Polish-Church).
    Footer of the Mass intentions names Saint Hedwig Parish alone.'
- url: https://www.church-bulletin.org/saint-hedwig-parish-trenton-nj-08638
  seen: 2026-10-30
  quote: Latest Edition November 1, 2026
  note: John Patrick Publishing listing 592 (church-bulletin.org/?id=592).
- url: https://www.sainthedwigparish.com/ParishBulletin
  seen: 2026-10-30
  quote: https://www.jppc.net/onlinebulletins/592template.pdf
  note: 'The parish''s own Parish Bulletin page links the John Patrick bulletin 592 and also lists self-hosted
    /Bulletins/Bulletin-<date>.pdf files, the newest of which is Bulletin-2026-07-19.pdf (the 1 November
    file answers 404): that archive is stale (about 15 weeks), the listing is current.'
research:
- method: probe url on sainthedwigparish.com; probe pdf on the 1 November 2026 listing issue; compared
    the site's own /Bulletins archive
  url: https://www.sainthedwigparish.com/ParishBulletin
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese trenton --parish st-hedwig-trenton (headed Chrome)
  url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: It picked the 1 November 2026 issue (freshness 'future', pdf); identity 'unverified' by
    the tool, read by hand from the masthead.
bulletin_status: available
publication_reviews:
- parish: our-lady-of-good-counsel-west-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 2) names Saint Hedwig Parish alone (pastor Rev. Can. Dr.
      Jacek W. Labinski, 872 Brunswick Ave.), with its own Mass schedule. (John Patrick 592)
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Our Lady of Good Counsel alone (pastor
      Fr. Ariel Robles, 137 West Upper Ferry Road), with its own Mass schedule. (John Patrick 533)
- parish: incarnation-st-james-ewing
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 2) names Saint Hedwig Parish alone (pastor Rev. Can. Dr.
      Jacek W. Labinski, 872 Brunswick Ave.), with its own Mass schedule. (John Patrick 592)
  - url: https://container.parishesonline.com/bulletins/04/0399/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Incarnation-St. James Parish alone (pastor Fr. Stanley DeBoe,
      O.SS.T.), with its own Mass schedule for Incarnation and St. James churches. (ParishesOnline 04/0399)
- parish: sacred-heart-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 2) names Saint Hedwig Parish alone (pastor Rev. Can. Dr.
      Jacek W. Labinski, 872 Brunswick Ave.), with its own Mass schedule. (John Patrick 592)
  - url: http://www.trentonsacredheart.org/storage/November%201%202026.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Parish alone (pastor Rev. Msgr. Dennis A. Apoldite),
      with its own Mass schedule for Sacred Heart and Holy Cross churches.
---

## Publisher

St. Hedwig Parish, Trenton, Cohort 9 (July 2024 cohort list), a personal parish for Polish Catholics since January 2017 (the 2017 *Faith in Our Future* decisions, Cohort 7, item 2: "St. Hedwig designated as a personal parish for Polish Catholics, effective immediately", https://dioceseoftrenton.org/decisions, read 2026-10-30). The decisions list it in Cohort 7 (the 2017 numbering); the 2024 list moved it to Cohort 9. It publishes its own bilingual bulletin through John Patrick Publishing (listing 592): the 1 November 2026 masthead names Saint Hedwig Parish alone, with its own pastor and Mass schedule (quoted in the evidence).

## Worship sites

One site with public Mass: St. Hedwig, 872 Brunswick Avenue. The bulletin's daily Masses (Monday and Friday 8 AM; Wednesday 7 PM) are "in Chapel", and Holy Day 8 AM in the chapel: a chapel at the same address with no street address of its own, so part of the one campus (see Rules settled: a chapel with no separate address is not a second church row). Its Sunday and Saturday Masses are in the church.

## Website and bulletin provider

The parish site links the printer's listing; its own /Bulletins archive stops at 19 July 2026. The row reads the listing. `fetch:check` result in research.
