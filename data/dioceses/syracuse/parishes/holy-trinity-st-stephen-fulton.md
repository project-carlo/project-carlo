---
name: Holy Trinity & St. Stephen Parishes
website: https://www.holytrinity-ststephen.org
bulletin_provider: parishes_online
provider_id: holy-trinity-parish-st-stephens-parish
publication: ['po-org:holy-trinity-parish-st-stephens-parish', 'lpi:0018000000Qbz9mAAB', 'po-container:06/0241']
group: Holy Trinity & St. Stephen
evidence:
- url: https://container.parishesonline.com/bulletins/06/0241/20260920B.pdf
  seen: 2026-09-26
  quote: Holy Trinity & St. Stephen Parishes September 20, 2026
  note: 'The running head of page 3 of the 20 September 2026 issue. Page 1 says "Holy Trinity Parish and
    St. Stephen Parish come together as one community in Christ" (letter-spaced in the text layer). Page
    2 is headed "Holy Trinity & St. Stephen Parishes" and lists Masses marked (HT) and (SS): Sat 4:00
    pm (HT), Sun 8:30 am (HT), 10:30 am (SS), weekdays alternating. Page 3 gives both offices: 309 Buffalo
    Street (Holy Trinity) and the St. Stephen office. LPi footer: "Holy Trinity, Fulton, NY 06-0241".'
- url: https://container.parishesonline.com/bulletins/06/0241/20260927B.pdf
  seen: 2026-09-26
  quote: www.holytrinity-ststephen.org
  note: The 27 September 2026 issue, same format and schedule; the masthead names the joint website.
- url: https://parishesonline.com/organization/holy-trinity-parish-st-stephens-parish
  seen: 2026-09-26
  note: '`probe po 0018000000Qbz9mAAB`: organization "Holy Trinity Parish & St. Stephen''s Parish", 309
    Buffalo Street, Fulton, container 06/0241, weekly issues through 2026-09-27.'
- url: https://www.holytrinity-ststephen.org/mass-schedule
  seen: 2026-09-26
  quote: 10:30 a.m. at St. Stephen
  note: 'The parishes'' Mass page: "Saturday 4:00 p.m. at Holy Trinity Sunday 8:30 a.m. at Holy Trinity
    10:30 a.m. at St. Stephen", weekdays at both.'
- url: https://www.holytrinityfulton.org/bulletins
  seen: 2026-09-26
  note: The older domain, still serving the same LPi site; its Bulletins page embeds the ParishesOnline
    widget for this organization (visit.py found lpi:0018000000Qbz9mAAB and po-container:06/0241 there).
promoted: 2026-09-26
---

## Publisher

Holy Trinity (Fulton) and St. Stephen (Phoenix) are two canonical parishes with one pastor (Very Rev.
Joseph E. Scardella) that publish **one** weekly bulletin through ParishesOnline (LPi), container
06/0241. I read the 20 and 27 September 2026 issues: page 1 of each says "Holy Trinity Parish and St.
Stephen Parish come together as one community in Christ", page 2 is headed "Holy Trinity & St. Stephen
Parishes" and lists every Mass with (HT) or (SS), and page 3 gives both parish offices. So this is one
row with two churches. The diocese lists them as separate parishes (Holy Trinity, Fulton and
St. Stephen, Phoenix), and the directory gives each the same website.

## Worship sites

- `churches/holy-trinity-fulton.md`: 309 Buffalo Street, Fulton, the former Immaculate Conception
  church (the parish's history page says Holy Trinity was formed in 2008 "with Immaculate Conception
  church chosen as the location").
- `churches/st-stephen-phoenix.md`: 469 Main Street, Phoenix.

Holy Trinity's other two predecessors are excluded as `closed`: Holy Family and St. Michael, Fulton
(`excluded/holy-family-fulton.md`, `excluded/st-michael-fulton.md`). The diocese's alphabetical list
also has "St. Mary, Fulton (See Church of the Holy Trinity, Fulton)" without "CLOSED"; it is in no
roster, and I found no church of that name in Fulton's current schedule. The parish's "St. Mary's
School" and "St. Mary's Cemetery" belonged to Immaculate Conception, so it is probably another name for
the same parish, but that is inference.

## Website and bulletin provider

Both holytrinity-ststephen.org (the site the bulletin names) and holytrinityfulton.org (the one the
diocese directory and ParishesOnline list) serve the same LPi WeConnect site. The newer joint domain is
used as `website`. ParishesOnline is read by `provider_id`, the organization slug; the organization
lookup gives the LPi id and container, all recorded in `publication`.

## Not yet confirmed

Whether "St. Mary, Fulton" in the diocese's list is a separate building; a Fulton history source or
the parish office would settle it. It is in no roster, so no coverage depends on it.
