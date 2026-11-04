---
name: Our Lady of Good Counsel and Immaculate Conception, Newark
website: https://www.instagram.com/goodcounselchurch_newark/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Planning Area I
evidence:
- url: https://rcan.org/clergy-appointments-june-2025/
  seen: 2026-11-04
  quote: pastor of Our Lady of Good Counsel and
  note: 'June 2025: ''Very Reverend Jorge E. Acosta Pena, V.F., pastor of Our Lady of Good Counsel and
    Immaculate Conception, Newark, has had his term extended one year to June 30, 2026.'''
- url: https://rcan.org/clergy-appointments-may-2026/
  seen: 2026-11-04
  quote: Reverend Luis M. Garcia has been appointed administrator of Our Lady of Good Counsel and Immaculate
    Conception
  note: Effective June 18, 2026. The April 2026 post names Bishop Gregory J. Studerus temporary administrator
    from March 21, 2026; the June 23, 2026 post appoints a parochial vicar 'at Our Lady of Good Counsel
    and Immaculate Conception, Newark' from July 1, 2026.
- url: https://www.instagram.com/goodcounselchurch_newark/
  seen: 2026-11-04
  note: 'Read with parish-site-access visit.py: account ''Good Counsel & Immaculate Conception'', ''654
    Summer ave., Newark, NJ 973-482-1274'', 10 posts, highlights ''GC'' and ''IC''. No bulletin posted.
    The pastorate''s only current web presence found.'
- url: https://parishesonline.com/organization/our-lady-of-good-counsel-church-07104
  seen: 2026-11-04
  note: 'probe po: org ''Our Lady of Good Counsel Church'', 654 Summer Ave, Newark 07104-3418, LPi 0018000000QxACNAA3,
    no publications. The sibling org immaculate-conception-church-07104 (390 Woodside Ave, LPi 0018000000QxACMAA3)
    also has no publications.'
- url: http://www.olgc-ic.org
  seen: 2026-11-04
  note: 'Website given for Immaculate Conception by catholicchurch.directory. probe url: DEAD-DNS (no
    such host); the Wayback CDX has captures only to 2015 (robots.txt 404s). The old pastorate site is
    lost.'
revisit: 'Look for a bulletin from the new administrator (appointed June 2026): rcan.org finder website,
  ParishesOnline, John Patrick, the Instagram account'
revisit_after: 2027-02-01
research:
- method: probe po on both ParishesOnline orgs (our-lady-of-good-counsel-church-07104, immaculate-conception-church-07104)
  url: https://parishesonline.com/organization/our-lady-of-good-counsel-church-07104
  checked: '2026-11-04'
  outcome: not-found
  next_action: Rerun probe po on both slugs; if a container appears, read its masthead and record provider
    parishes_online
  retry_when: A source (Instagram post, a neighbour's bulletin, rcan.org) mentions a Good Counsel or Immaculate
    Conception bulletin
  revisit_after: 2027-02-01
- method: John Patrick scans (029-map/jp-1-399, jp-400-799, jp-6000-6200 tsv) grepped for good-counsel,
    immaculate, newark and 07104
  checked: '2026-11-04'
  outcome: not-found
  next_action: Grep a fresh jp_scan.sh run for 07104 and good-counsel
  retry_when: The Run's John Patrick scans are refreshed or extended past 6200
- method: Discover Mass church pages and DuckDuckGo html searches ('Good Counsel' '654 Summer'; 'Immaculate
    Conception' 'Woodside Ave' Newark; both names with facebook/bulletin/boletin); domain guesses olgcnewark.org/.com,
    icnewark.org, immaculateconceptionnewark.org, olgcnewarknj.org, ourladyofgoodcounselnewark.org (all
    DEAD-DNS); olgc-ic.org (DEAD-DNS)
  url: https://discovermass.com/church/our-lady-of-good-counsel-newark-nj/
  checked: '2026-11-04'
  outcome: not-found
  next_action: Search again for a new pastorate website or Facebook page that posts a bulletin
  retry_when: The rcan.org parish finder lists a website for directory 125 or 126
  revisit_after: 2027-02-01
bulletin_status: not-found
---

## Publisher

No bulletin found (see `research`). Our Lady of Good Counsel and Immaculate Conception, Newark, are two canonical parishes run as one pastorate: the archdiocese's clergy appointments name them together ('pastor of Our Lady of Good Counsel and Immaculate Conception, Newark', June 2025; administrator Rev. Luis M. Garcia from June 18, 2026, May 2026 post; a parochial vicar 'at Our Lady of Good Counsel and Immaculate Conception, Newark' from July 1, 2026). The directory gives both parishes one address, 654 Summer Avenue, and the pastorate's Instagram account is 'Good Counsel & Immaculate Conception'. One row is inferred from that single pastorate, office and account; no bulletin of either parish was read, so whether they would print one bulletin or two is unchecked.

## Worship sites

- Our Lady of Good Counsel Church, 654 Summer Avenue (`our-lady-of-good-counsel-newark`; directory 126, GCatholic 18494).
- Immaculate Conception Church, 390 Woodside Avenue (`immaculate-conception-newark`; directory 125, whose address is the shared 654 Summer Avenue office, and GCatholic 18491).

Mass at both rests on third-party listings (Discover Mass, catholicchurch.directory), undated, plus the archdiocese's 2026 appointments to the pastorate; see each church. Neither appears in the archdiocese's closed-or-merged records table (rcan.org/sacramental-records/, 2025-05-22).

## Website and bulletin provider

`no_bulletin`. Neither directory entry has a website. The old pastorate site www.olgc-ic.org (still given by catholicchurch.directory) does not resolve, and the Wayback CDX shows nothing after 2015. Both ParishesOnline orgs exist with no publications; Discover Mass pages for both say 'There are currently no bulletins available'; no John Patrick listing in the Run's scans is in 07104 under either name. The website recorded is the pastorate's Instagram account, its only current web presence (no bulletin posted there).

## Not yet confirmed

- Whether the pastorate publishes a bulletin at all: retry per `research` (next 2027-02-01).
- Whether a bulletin, if found, covers both churches (one row) or each parish separately (split the row).
- Current Mass times at both churches from a parish source.
