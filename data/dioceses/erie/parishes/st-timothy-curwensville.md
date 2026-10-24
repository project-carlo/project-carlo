---
name: St. Timothy Parish
website: https://www.sttimbon.org
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: ''
evidence:
- url: https://www.sttimbon.org/weeklybulletin.php
  seen: 2026-10-23
  quote: No Bulletin found
  note: 'The parish''s own site (diocese-hosted template, page title ''St. Timothy, Curwensville and St.
    Bonaventure, Grampian Parish'') has a weeklybulletin.php that answers 200 and reads ''No Bulletin
    found.'' It is not linked from the menu (About Us, Join Us, Religious Education, Sacraments, Ways
    to Give, Child Protection, CSA 2026); the home page shows only Mass times and a Facebook link. probe
    url: publications [] and bulletin_links [].'
- url: https://discovermass.com/church/saint-timothy-curwensville-pa/
  seen: 2026-10-23
  quote: There are currently no bulletins available for Saint Timothy.
  note: 'Discover Mass pages exist for both churches and neither carries a bulletin. The St. Bonaventure
    page (st-bonaventure-grampian-pa) says ''There are currently no bulletins available for St. Bonaventure.''
    Their Mass times are stale (St. Timothy: Sat 4:00pm, Sun 8:30am, Mon-Thu 9:00am; St. Bonaventure:
    Sun 11:00am), unlike the diocese''s.'
- url: https://parishesonline.com/organization/st-timothy-church-16833
  seen: 2026-10-23
  note: 'probe po st-timothy-church-16833 (LPi 0018000000QxBkvAAF, 306 Walnut St) and st-bonaventure-church-16838
    (LPi 0018000000QxBlJAAV, 461 Main St): both ''no publications: this organization does not publish
    a bulletin here now''. Search API near both towns (distance 6-8 mi) found only these two Catholic
    organizations.'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Administrator ....................................................................... St. Timothy
    Parish, Curwensville
  note: 'Clergy list updated 8/7/2026: Detisch, VF, Very Rev. John J., ''Pastor ... St. Tobias, Brockway''
    and ''Administrator ... St. Timothy Parish, Curwensville''. The directory''s own pastor field for
    St. Timothy is blank on the detail page and says Rev. Stephen L. Collins in the locator; the clergy
    list shows Collins retired at Christ the King, Houtzdale.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: 'Parochial Administrator: Very Reverend John Detisch, VF'
  note: 'Printable directory dated Oct. 22, 2026: St. Timothy Parish, Curwensville, 306 Walnut St., with
    ''St. Bonaventure Church, Secondary Church'' under it: ''Saturday: 4 p.m. at St. Timothy; Sunday:
    11 a.m.''. The web detail page 20710 says Saturday 4 p.m. and Sunday 11 a.m. at St. Bonaventure; daily
    none.'
- url: https://www.eriercd.org/images/sections/bishop/pdf/DECREE%20-%20Merging%20St.%20Bonaventure%20Grampian%20into%20St.%20Timothy%20Curwensville%20letterhead.pdf
  seen: 2026-10-23
  quote: This decree is effective December 2, 2023, the beginning of Advent.
  note: 'Decree 6: ''Saint Bonaventure church in Grampian shall become a secondary mission church of Saint
    Timothy Parish.'' Mass on Sundays and holy days is permitted there.'
- url: https://www.legacy.com/us/obituaries/theprogressnews/name/mary-brock-obituary?id=60455516
  seen: 2026-10-23
  quote: Mass of Christian Burial will be said at the St. Timothy Roman Catholic Church, Curwensville
    on Friday, Jan. 9, 2026 at 11 a.m. with the Very Reverend John J. Detisch, V.F. as celebrant.
  note: Funeral Mass at St. Timothy in 2026 with Detisch as celebrant (the funeral home's page also names
    interment in St. Bonaventure Cemetery). Shows the church is in use; not a schedule.
- url: https://www.facebook.com/pages/St-Timothys-Roman-Catholic-Church/113877895310105
  seen: 2026-10-23
  note: Linked from sttimbon.org; the page says 'Unofficial Page' and shows an event post only; no bulletin.
revisit: Look again for a St. Timothy / St. Bonaventure bulletin (sttimbon.org weeklybulletin.php, Discover
  Mass pages saint-timothy-curwensville-pa and st-bonaventure-grampian-pa, ParishesOnline orgs st-timothy-church-16833
  and st-bonaventure-church-16838, and whether the St. Tobias bulletin starts carrying the Curwensville
  Mass times).
revisit_after: 2027-01-23
research:
- method: probe url sttimbon.org; sttimbon.org/weeklybulletin.php; probe po for both ParishesOnline orgs;
    ParishesOnline search API near Curwensville and Grampian; Discover Mass pages for both churches; web
    search (DuckDuckGo via visit.py) for the parish's bulletin; Facebook page opened in headed Chrome
  url: https://www.sttimbon.org/weeklybulletin.php
  checked: '2026-10-23'
  outcome: not-found
  next_action: Re-run those checks; also look for a parish Facebook posting of a bulletin PDF and ask
    whether a John Patrick / Bon Venture bulletin exists for 306 Walnut St. A bulletin found at any of
    them becomes this row's provider.
  retry_when: sttimbon.org lists a bulletin, a Discover Mass or ParishesOnline channel appears for either
    church, or the St. Tobias bulletin starts printing the Curwensville Mass schedule
  revisit_after: 2027-01-23
- method: grep of the 25 Oct 2026 St. Tobias bulletin (Discover Mass 3520) and the 25 Oct 2026 St. Francis
    of Assisi, Clearfield bulletin (3101) for Timothy, Bonaventure, Curwensville, Grampian
  checked: '2026-10-23'
  outcome: not-found
  next_action: Neither neighbouring bulletin carries St. Timothy's or St. Bonaventure's Mass times, so
    they are not the home of a shared bulletin. Re-grep the St. Tobias bulletin if the retry trigger above
    fires.
  retry_when: A later St. Tobias issue names Curwensville or Grampian
bulletin_status: not-found
---

## Publisher

No bulletin found. St. Timothy Parish, Curwensville (306 Walnut St., 16833; merged with St. Bonaventure, Grampian, effective 2 December 2023) has a diocese-hosted website, sttimbon.org, whose hidden `weeklybulletin.php` says 'No Bulletin found.' Both Discover Mass pages say no bulletins are available, both ParishesOnline organizations are empty, and web search found no bulletin. So the row is `no_bulletin` (kept in the records, left off the site until a bulletin turns up).

The pastoral link is real: the clergy list (8/7/2026) makes Very Rev. John J. Detisch, V.F. administrator of St. Timothy and pastor of St. Tobias, Brockway (about 23 miles to the north-west). It does not make one bulletin: the St. Tobias issue of 25 October 2026 (Discover Mass 3520) never names Timothy, Bonaventure, Curwensville or Grampian and carries only its own Mass intentions. See st-tobias-brockway.

## Worship sites

Two churches publicly celebrate Mass according to the diocese's printable directory of 22 October 2026: St. Timothy (306 Walnut St., Curwensville), Saturday 4 p.m., and St. Bonaventure (461 Main St., Grampian, a secondary church after the 2023 decree), Sunday 11 a.m. Confession Saturday 3:15-3:50 p.m. at Timothy and Sunday 10:30 a.m. at Bonaventure. That is the only current schedule found (the diocese, not a bulletin); Discover Mass's own times for the two churches are out of date and disagree. The St. Timothy and St. Bonaventure churches are filed under this row. Nothing else in the directory is under it.

## Website and bulletin provider

`website` is sttimbon.org (alive, 200, the parish's own). No provider recipe can be set. `weeklybulletin.php` is the first thing to re-check.

## Not yet confirmed

- Whether a bulletin exists anywhere (see `research` and `revisit`).
- Whether Saturday 4 p.m. at Timothy and Sunday 11 a.m. at Bonaventure are the only weekend Masses now; the directory is the only source and a bulletin would settle it.
