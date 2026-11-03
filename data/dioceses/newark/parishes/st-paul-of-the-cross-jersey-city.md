---
name: St. Paul of the Cross, Jersey City
website: https://discovermass.com/church/st-paul-of-the-cross-jersey-city-nj/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area E
evidence:
- url: https://rcan.org/parishes/
  seen: 2026-11-03
  note: 'Archdiocese directory entry 84: St. Paul of the Cross Parish, 156 Hancock Avenue, Jersey City,
    NJ 07307, with no website; GCatholic 18457 also gives none.'
- url: https://discovermass.com/church/st-paul-of-the-cross-jersey-city-nj/
  seen: 2026-11-03
  note: 'Discover Mass church page: 156 Hancock Ave, 201-798-7900; no bulletins; MassTimes.org schedule
    under a COVID-19 notice (Saturday 5:30pm; Sunday 7:00am, 8:30am, 10:10am, 11:30am, 1:00pm). Its ''Visit
    Website'' link, https://www.rcan.org/st-paul-cross-parish-jersey-city, answers HTTP 404.'
- url: https://rcan.org/clergy-appointments-july-2025/
  seen: 2026-11-03
  quote: Reverend Hermes Diaz Vargas has been appointed administrator of Saint Paul of the Cross, Jersey
    City, effective, July 15, 2025.
  note: The parish has its own administrator.
- url: https://parishesonline.com/organization/st-paul-of-the-cross-church-07307
  seen: 2026-11-03
  note: 'probe po: org ''St. Paul of the Cross Church'', lpi 0018000000QxABUAA3, no website, no issues:
    an old account, so its ids are not recorded as this bulletin''s.'
revisit: Look for St. Paul of the Cross's website or Facebook page and its bulletin; set the provider,
  read the masthead and Mass schedule, run fetch:check.
revisit_after: 2027-02-01
research:
- method: 'Website search: directory and GCatholic give none; Discover Mass''s link (rcan.org/st-paul-cross-parish-jersey-city)
    is 404; probe get on guessed domains stpaulofthecrossjc.org, stpaulofthecrossjerseycity.org, spocjc.org,
    stpaulofthecrossnj.org, stpaulofthecross.org, saintpaulofthecrossjc.org, stpaulofthecrossjc.com (no
    DNS); DuckDuckGo html (bot check) and Bing (irrelevant results)'
  checked: '2026-11-03'
  outcome: not-found
  next_action: Find the parish's website or Facebook page (call 201-798-7900, or read a neighbouring Jersey
    City Heights parish's bulletin) and read where it posts a bulletin
  retry_when: A parish website or social page is found
- method: 'Publisher listings: probe po st-paul-of-the-cross-church-07307 (empty org) and three other
    slugs; John Patrick church-bulletin.org ids 1-1100 and 6000-6400 scanned with scratch/newark-map-1/tools/jp_scan.sh
    (no listing for this parish); Discover Mass st-paul-of-the-cross-jersey-city-nj (no bulletins)'
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read the publisher from a bulletin or parish page once one is found, then set the provider
    and run fetch:check
  retry_when: A parish website or social page is found
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

Not found. Neither the directory (84) nor GCatholic (18457) gives a website; Discover Mass's 'Visit Website' link points to an rcan.org page that answers 404. The ParishesOnline org st-paul-of-the-cross-church-07307 (lpi 0018000000QxABUAA3) is empty, Discover Mass lists no bulletins, and a scan of John Patrick ids 1-1100 and 6000-6400 found no listing for the parish. See `research`.

## Worship sites

One church, `st-paul-of-the-cross-jersey-city`, the only place the directory and GCatholic list. No current Mass schedule was read.

## Website and bulletin provider

No parish website was found; the `website` is the Discover Mass church page, which at least gives the address and phone. The provider is `no_bulletin` with `bulletin_status: not-found`: a bounded search, not evidence that none is printed.

## Not yet confirmed

Whether the parish prints a bulletin, where it is posted, and the current Mass schedule. Next step: `revisit` (from 2027-02-01).
