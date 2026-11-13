---
name: St. Francis of Assisi-St. Blaise (Crown Heights)
website: https://parishesonline.com/organization/st-francis-of-assisi-st-blaise-church
bulletin_provider: parishes_online
provider_id: st-francis-of-assisi-st-blaise-church
publication: ['po-org:st-francis-of-assisi-st-blaise-church', 'lpi:0018000000Qc1KRAAZ', 'po-container:03/9992']
group: Deanery B5 (Brooklyn East)
evidence:
- url: https://container.parishesonline.com/bulletins/03/9992/20261108B.pdf
  seen: 2026-11-09
  quote: 8:30 a.m.Monday to Saturday in the Church
  note: '8 November 2026 LPi issue (4 pages). Page 1 masthead ''St. Francis of Assisi-St. Blaise Parish''
    in Prospect Lefferts Gardens; Very Rev. Thomas F. Vassalotti, Pastor; Parish Office 319 Maple Street,
    Brooklyn, NY 11225; WEBSITE: www.sfa-stb.org. MASS SCHEDULE: Weekdays 8:30 a.m. Monday to Saturday
    in the Church; Sunday Vigil 5:00p.m. English; Sunday 9:00 a.m. & 12:30 p.m. English, 11:00 a.m. Spanish,
    5:00 p.m. Haitian Kreyol. One church only; grep ''Ignatius'' and ''Carroll'' over all 4 pages finds
    nothing.'
- url: https://parishesonline.com/organization/st-francis-of-assisi-st-blaise-church
  seen: 2026-11-09
  note: 'probe po: org ''St. Francis of Assisi / St. Blaise Church'', 319 Maple St, Brooklyn, New York,
    11225, lpi 0018000000Qc1KRAAZ, container 03/9992, weekly issues 2026-10-04 through 2026-11-08; org
    website https://www.sfa-stb.org/.'
- url: https://www.sfa-stb.org/
  seen: 2026-11-09
  quote: Unfortunately, this site is temporarily unavailable.
  note: The directory's website answers 200 with a host 'Temporarily Unavailable' page and no parish content,
    so the row's website is the ParishesOnline org page.
- url: https://dioceseofbrooklyn.org/offices/diocesan-archives/parishes/
  seen: 2026-11-05
  quote: Merged with St. Ignatius, 2011
  note: 'Archives List of Parishes: ''St. Francis of Assisi, Crown Heights (1898). Renamed St. Francis
    of Assisi-St. Blaise in 1980. Merged with St. Ignatius, 2011.'''
promoted: 2026-11-12
research:
- method: probe url and probe get on the directory website
  url: https://www.sfa-stb.org/
  checked: '2026-11-09'
  outcome: access-blocked
  next_action: Re-read sfa-stb.org; if it is back, check for a bulletin link and other worship sites,
    and consider setting it as the website
  retry_when: The site no longer shows the host 'Temporarily Unavailable' page
  revisit_after: 2027-02-01
- method: fetch:check (headed), parishes_online org st-francis-of-assisi-st-blaise-church
  url: https://container.parishesonline.com/bulletins/03/9992/20261108B.pdf
  checked: '2026-11-09'
  outcome: found
bulletin_status: available
---

## Publisher

St. Francis of Assisi-St. Blaise publishes a weekly LPi bulletin (ParishesOnline org `st-francis-of-assisi-st-blaise-church`, container 03/9992; LPi's file names call it 03-0417). The 8 November 2026 issue (read 2026-11-09, 4 pages) has the masthead "St. Francis of Assisi-St. Blaise Parish" in Prospect Lefferts Gardens on page 1, with Very Rev. Thomas F. Vassalotti, Pastor, and the parish office at 319 Maple Street, Brooklyn, NY 11225. The issue has no LPi footer number; the container was found through a search result for `container.parishesonline.com/bulletins/03/9992/20260419B.pdf`, and `probe po` ties the org to it.

## Worship sites

One church. The page 1 schedule gives weekday Mass "8:30 a.m.Monday to Saturday in the Church" and Sunday Masses at 5:00 p.m. vigil, 9:00 a.m., 11:00 a.m. (Spanish), 12:30 p.m. and 5:00 p.m. (Haitian Kreyol), with no second church; grep 'Ignatius' and 'Carroll' finds nothing. That church is `churches/st-francis-of-assisi-st-blaise-crown-heights`, 319 Maple St.

Ruled out: St. Ignatius, 1101 Carroll St. (gcatholic:16720), merged into this parish in 2011 (diocesan archives). The Tablet (1 November 2017) says a homeless shelter was built on the former site of St. Ignatius Church: `excluded/st-ignatius-crown-heights`. The old St. Blaise church (closed 1980, archives) is in no roster and was not recorded.

## Website and bulletin provider

`parishes_online`, org `st-francis-of-assisi-st-blaise-church` (latest issue 8 November 2026). The directory's site, sfa-stb.org, showed only a host "Temporarily Unavailable" page on 2026-11-09, so the website is the ParishesOnline org page. Discover Mass has no bulletins for this parish.

## Not yet confirmed

Whether sfa-stb.org comes back (research item, revisit after 2027-02-01).
