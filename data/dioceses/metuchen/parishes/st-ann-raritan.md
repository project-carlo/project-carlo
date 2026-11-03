---
name: St. Ann
website: https://www.stannparish.com
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:22511']
group: Raritan Oratory
evidence:
- url: https://files.ecatholic.com/22511/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: G60661 (JR) St Ann Church (Raritan, NJ)
  note: 'Bon Venture code line on the ad pages (5-6) of the 1 November 2026 issue (6 pages; pages 1-4
    are images). Page 1, rendered, is the masthead: ''The Catholic Church of St. Ann'', ''St. Ann Church,
    45 Anderson Street, Raritan, NJ 08869'', ''Rev. Thomas Odorizzi, C.O., Parish Pastor'', ''V. Rev.
    Jeffrey Calia, C.O., Provost'', ''ALL SAINTS November 1, 2026''. Its ''Lord''s Day Mass Schedule''
    lists every Raritan Oratory church: St. Ann Church Sunday 7:30, 10:30 am, 12:00 and 5:00 pm, weekdays
    8:00 am, Saturday 9:00 am, alongside St. Joseph, Holy Trinity and the Shrine of Blessed Sacrament.'
- url: https://www.stannparish.com/bulletins
  seen: 2026-11-02
  quote: The Catholic Church of St. Ann
  note: eCatholic site 22511, loaded with visit.py (probe url said DEAD-DNS, probe get 403, and the browser
    verdict SPAM-SQUAT, though the title is 'The Catholic Church of St. Ann - Raritan, NJ' and the pages
    are parish pages). The Bulletin page lists weekly files at files.ecatholic.com/22511/bulletins/<YYYYMMDD>.pdf,
    newest 1 November 2026.
promoted: 2026-11-03
bulletin_status: available
publication_reviews:
- parish: st-joseph-raritan
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/22569/bulletins/20261101.pdf
    seen: 2026-11-02
    quote: The Roman Catholic Community of Saint Joseph
    note: The 1 November 2026 St. Joseph issue is published by St. Joseph on its own eCatholic site (22569);
      its masthead names 'The Roman Catholic Community of Saint Joseph, 16 East Somerset Street' with
      Rev. Kevin P. Kelly, C.O. as Administrator and the parish's own phone and email.
- parish: holy-trinity-bridgewater
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/22534/bulletins/20261101.pdf
    seen: 2026-11-02
    quote: THE CHURCH OF THE HOLY TRINITY HAS AS ITS MISSION
    note: The 1 November 2026 Holy Trinity issue is published by Holy Trinity, Bridgewater on its own
      eCatholic site (22534, Bon Venture account G60610 'Holy Trinity, Bridgewater'); its masthead names
      60 Maple Street and Very Rev. Jeffrey M. Calia, C.O. as Pastor, with its own office.
- parish: shrine-chapel-of-the-blessed-sacrament-raritan
  decision: separate
  evidence:
  - url: https://files.ecatholic.com/26980/bulletins/20261101.pdf
    seen: 2026-11-02
    quote: SHRINE CHAPEL OF THE BLESSED SACRAMENT
    note: The 1 November 2026 shrine issue is published by the Shrine Chapel of the Blessed Sacrament
      on its own eCatholic site (26980); its masthead names the Shrine Chapel with Very Rev. Jeffrey M.
      Calia, C.O. as Shrine Rector, its own office and its own Mass intentions.
---

## Publisher

St. Ann, 45 Anderson Street, Raritan, publishes its own weekly bulletin on its eCatholic site (22511), printed by Bon Venture (account G60661, 'St Ann Church (Raritan, NJ)', on the ad pages). The 1 November 2026 issue (read 2026-11-02) is image-only on pages 1-4; page 1, rendered, has the masthead 'The Catholic Church of St. Ann', '45 Anderson Street, Raritan, NJ 08869', 'Rev. Thomas Odorizzi, C.O., Parish Pastor' and 'V. Rev. Jeffrey Calia, C.O., Provost'.

## Shared bulletin with the other Oratory parishes?

The batch asked whether the three Oratory-staffed parishes (St. Ann, St. Joseph, Holy Trinity) share a bulletin. They don't. Each has its own eCatholic site and weekly archive, and the 1 November 2026 issues have different mastheads and Bon Venture accounts: St. Ann G60661 (22511), Holy Trinity G60610 (22534), St. Joseph (22569, masthead 'The Roman Catholic Community of Saint Joseph'), and the Shrine Chapel of the Blessed Sacrament has a fourth (26980). Every one of them prints the same combined Raritan Oratory Mass schedule for all four churches, so the schedule alone doesn't tell them apart; the mastheads, contact details and intentions do. See `publication_reviews`.

## Worship sites

One church, St. Ann, 45 Anderson Street (directory:24534, gcatholic:18636). The combined schedule on page 1 also lists St. Joseph Church, Holy Trinity Church and the Shrine of Blessed Sacrament; each of those publishes its own bulletin and is a church of its own row (`st-joseph-raritan`, `holy-trinity-bridgewater`, `shrine-chapel-of-the-blessed-sacrament-raritan`). St. Ann Classical Academy (40 Second Avenue), on the masthead, is the parish school, not a Mass site.

## Website and bulletin provider

Website https://www.stannparish.com (finder, GCatholic and masthead). `probe url` said DEAD-DNS and `probe get` 403 on 2026-11-02 (the probe network problem the playbook notes); `visit.py` loaded it as eCatholic site 22511 with the title 'The Catholic Church of St. Ann - Raritan, NJ' but a SPAM-SQUAT verdict. The pages are the parish's own (Mass times, Bulletin archive, parish forms and flyers), so the verdict is a false positive, probably from event words such as 'Gala tickets'. Provider `ecatholic`.

## Fetch check

`pnpm fetch:check` on 2026-11-02 picked https://files.ecatholic.com/22511/bulletins/20261101.pdf (the 1 November 2026 issue): transport ok, PDF, issue date inferred 2026-11-01, freshness fresh, identity unverified by the tool; I read that issue myself (evidence above).

## Not yet confirmed

Nothing open. Recheck can only find the ad-page code line in the PDF text, since the masthead and schedule pages are images.
