---
name: St. John, Newark
website: https://www.njsk.org/mass-schedule-sj
bulletin_provider: no_bulletin
provider_id: ''
publication: ['po-org:st-john-church-07102', 'lpi:0018000000QxACJAA3', 'discovermass:st-john-newark-nj']
group: Planning Area I
evidence:
- url: https://parishesonline.com/organization/st-john-church-07102
  seen: 2026-11-04
  note: 'probe po: org ''St. John Church'', 22 Mulberry Street, Newark 07102, lpi 0018000000QxACJAA3,
    website none, no publications (''this organization does not publish a bulletin here now'').'
- url: https://discovermass.com/church/st-john-newark-nj/
  seen: 2026-11-04
  note: Discover Mass listing 'St. John', 22 Mulberry St., 973-623-0822; a COVID-era notice and 'Sunday
    1:00pm'; its Bulletins tab holds no issues (only the form to request bulletins).
- url: https://www.njsk.org/mass-schedule-sj
  seen: 2026-11-04
  quote: English Mass 7:30 am
  note: 'St. John''s Soup Kitchen''s site (the parish''s own outreach, 22 Mulberry Street) gives the only
    schedule found: ''SUNDAYS English Mass 7:30 am Main Church - 22 Mulberry Street … This schedule will
    start after Labor Day Weekend (September 8)''. Its Squarespace JSON gives updatedOn 1722262520755
    (29 July 2024), so it dates from 2024. No bulletin link.'
- url: https://rcan.org/clergy-appointments-december-2021/
  seen: 2026-11-04
  quote: appointed pastor of Saint Patrick Pro Cathedral, Newark and Saint John Parish, Newark effective
    September 8, 2021 and ending June 30, 2027
revisit: Look again for a bulletin from St. John or one shared with St. Patrick Pro-Cathedral once the
  2021-27 pastorate ends; recheck the Sunday schedule (the only one found dates from 2024).
revisit_after: 2027-07-01
research:
- method: probe po on st-john-church-07102; Discover Mass listing; John Patrick scans (029-map jp-*.tsv)
    grepped for Newark, 07102 and John; St. Patrick's site and JP listing 672 for a shared bulletin; DuckDuckGo
    html search for the church's address
  url: https://parishesonline.com/organization/st-john-church-07102
  checked: '2026-11-04'
  outcome: not-found
  next_action: Ask through the rectory number or reread St. Patrick's site and JP 672 for a bulletin covering
    St. John; if one appears, merge into or set the provider for this row
  retry_when: St. Patrick or St. John posts a bulletin, or a new pastor is appointed after the current
    term (ends 2027-06-30)
  revisit_after: 2027-07-01
bulletin_status: not-found
---

## Publisher

No bulletin found. The ParishesOnline org 'St. John Church' (22 Mulberry Street) publishes nothing now, and the Discover Mass listing's Bulletins tab is empty. No John Patrick listing matches Newark 07102 apart from St. Patrick's Pro-Cathedral (672), which shows only readings. The parish has no website of its own: the directory (131) and GCatholic (18507) give none. Its outreach site, St. John's Soup Kitchen (njsk.org), gives a Mass schedule page and is the `website` here because it is the only page the parish's schedule appears on.

St. John shared its pastor with St. Patrick Pro-Cathedral (rcan.org, December 2021, until 30 June 2027) and its phone, (973) 623-0822, so the batch looked for one bulletin covering both and found none. St. Patrick's own schedule does not list St. John, so the two are kept as separate `no_bulletin` rows rather than merged on the shared pastor alone.

## Worship sites

`st-john-newark`, 22 Mulberry Street: the soup kitchen's page (Squarespace JSON updated 29 July 2024) gives 'SUNDAYS English Mass 7:30 am Main Church - 22 Mulberry Street'.

## Website and bulletin provider

`no_bulletin` (Settled policy 4: kept in the records, off the site). Ids from ParishesOnline and Discover Mass are kept in `publication` so a later bulletin there is matched to this row.

## Not yet confirmed

The Sunday 7:30 am Mass is from a 2024 page; no 2026 source states St. John's schedule. Whether St. Patrick's Facebook or Instagram posts a bulletin covering both was not checked.
