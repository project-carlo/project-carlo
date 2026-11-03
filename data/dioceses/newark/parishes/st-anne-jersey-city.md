---
name: St. Anne, Jersey City
website: http://stannesjc.com/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area E
evidence:
- url: http://stannesjc.com/aabulletins.htm
  seen: 2026-11-03
  quote: January 10, 2016
  note: 'GCatholic''s website for the parish, still online: a FrontPage-era site (''1904 - 2017''), whose
    Bulletins page lists issues from 10 January 2016 to Bul170101B.pdf (1 January 2017). That issue''s
    page 8 footer: ''St. Anne''s, Jersey City, NJ 04-1043'' (LPi).'
- url: http://www.saintanne1904.org/
  seen: 2026-11-03
  note: 'The directory''s website: probe get returns a gambling page titled ''BOB303 … Tempat Nongkrong
    Gaming'' and visit.py is redirected off-site: the domain has been squatted. The Wayback snapshot of
    14 March 2026 (web.archive.org/web/20260314132408id_/https://www.saintanne1904.org/) shows the parish''s
    Wix site ''SAINT ANNE ROMAN CATHOLIC CHURCH (1904), 3545 JOHN F. KENNEDY BOULEVARD'' with COVID-era
    content and no bulletin links (Mass schedule there: Mon-Sat 7AM; Sat 5 P.M., sábado 7 P.M.; Sunday
    8, 10 A.M., 12 P.M.).'
- url: https://parishesonline.com/organization/st-anne-church-07307
  seen: 2026-11-03
  note: 'probe po: org ''St. Anne Church'', website www.stannesjc.com, lpi 0018000000Qc0B6AAJ, no issues;
    probe container 04/1043 (the 2017 footer) found nothing for the last 3 Sundays. An old account, so
    its ids are not recorded as this bulletin''s.'
- url: https://discovermass.com/church/st-annes-jersey-city-nj/
  seen: 2026-11-03
  note: 'Discover Mass page ''St. Annes'', 3545 Kennedy Blvd., (201) 360-0838: no bulletins; MassTimes.org
    schedule under a COVID-19 notice (Saturday 9:00am, 5:30pm, 7:00pm (Spanish); Sunday 8:00am, 10:00am,
    12:00pm).'
revisit: Look for St. Anne's current website or Facebook page and its bulletin; set the provider, read
  the masthead and Mass schedule, run fetch:check.
revisit_after: 2027-02-01
research:
- method: 'Parish websites: stannesjc.com (stale, last bulletin 1 January 2017), saintanne1904.org (squatted;
    Wayback 14 March 2026 snapshot has no bulletin); probe get on guessed domains stannejc.org, saintannejc.org,
    stannejerseycity.org, stannesjerseycity.org, stannejc.com (no DNS)'
  url: http://stannesjc.com/aabulletins.htm
  checked: '2026-11-03'
  outcome: not-found
  next_action: Find the parish's current website or Facebook page (call (201) 360-0838 or read a neighbouring
    parish's bulletin for a link) and read where it posts a bulletin
  retry_when: A current parish website or social page is found
- method: 'Publisher listings: probe po st-anne-church-07307 (empty org) and four other slugs; probe container
    04/1043 (none in 3 Sundays); John Patrick church-bulletin.org ids 1-1100 and 6000-6400 scanned with
    scratch/newark-map-1/tools/jp_scan.sh (no St. Anne, Jersey City listing); Discover Mass st-annes-jersey-city-nj
    (no bulletins)'
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read the publisher from a current bulletin or parish page once one is found, then set the
    provider and run fetch:check
  retry_when: A current parish website or social page is found
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

Not found. No current bulletin for St. Anne, 3545 Kennedy Boulevard, was found on 2026-11-03. Its old site stannesjc.com (GCatholic's link) stops at the 1 January 2017 bulletin, printed then by LPi (footer 'St. Anne's, Jersey City, NJ 04-1043'); that container and the ParishesOnline org st-anne-church-07307 (lpi 0018000000Qc0B6AAJ) have no current issues. The directory's saintanne1904.org now serves a gambling page; its 14 March 2026 Wayback copy was a parish Wix site with COVID-era content and no bulletin. No John Patrick listing (ids 1-1100, 6000-6400) or Discover Mass bulletin was found. See `research`.

## Worship sites

One church, `st-anne-jersey-city`, the only place the directory (86) and GCatholic (18450) list for the parish. No current Mass schedule was read, so whether a bulletin would name other sites is unconfirmed.

## Website and bulletin provider

The website is GCatholic's http://stannesjc.com/, the parish's own old site, which is still online; the directory's saintanne1904.org is squatted and is not used. The provider is `no_bulletin` with `bulletin_status: not-found`: a bounded search, not evidence that none is printed.

## Not yet confirmed

Whether St. Anne prints a bulletin now, and its current Mass schedule. Next step: `revisit` (from 2027-02-01).
