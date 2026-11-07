---
name: Holy Trinity Chapel (Trinity Chapel)
revisit: 'Read a Holy Trinity Parish bulletin''s Mass schedule for Mass at Trinity Chapel, 12 N Jerome
  Ave. (GCatholic: 100 N Jerome Ave.), Margate, once a collector or browser read gets past the parish''s
  Solutio /file links (the parish row is unsupported, fetch_gap joomla-file-endpoint), or ask the parish
  office (609-822-7105)'
revisit_after: 2027-01-31
roster: ['gcatholic:18904']
evidence:
- url: https://www.holytrinitydownbeach.org/about-us/our-churches
  seen: 2026-10-29
  quote: Located at 12 N. Jerome Ave., Margate, NJ, 08402.
  note: The parish site's 'Our Churches' page lists 'Trinity Chapel' with Blessed Sacrament, Epiphany
    and St. James. The home page lists Trinity Chapel, 12 N Jerome Ave, Margate, NJ, 08402, with no WEEKEND
    MASS, DAILY MASS or other schedule block, unlike the other three.
- url: https://gcatholic.org/churches/usa-03/18904
  seen: 2026-10-29
  quote: 100 N Jerome Ave., Margate City, New Jersey 08402
  note: 'GCatholic (last updated 2025.12.21): ''Chapel of the Holy Trinity'', type Chapel, group Holy
    Trinity Parish, ''Mission of: Church of the Blessed Sacrament'', Plus Code 87F78FHW+G4 (130 m from
    Blessed Sacrament). No Mass times.'
- url: https://catholicstarherald.org/summertime-masses-added-at-south-jersey-shore-parishes-2026/
  seen: 2026-10-29
  note: The summer guide (2026-05-22) lists the parish's three churches and no chapel.
parish: holy-trinity-downbeach
line1: 12 N Jerome Ave.
city: Margate City
state: NJ
postal_code: 08402
research:
- method: Read the parish home page, Our Churches and contact pages in the browser; searched them for
    any Mass at the chapel
  url: https://www.holytrinitydownbeach.org/about-us/our-churches
  checked: '2026-10-29'
  outcome: not-found
  next_action: Read a bulletin (blocked from the sandbox, see the parish record) for a Mass at the chapel;
    its Mass & Liturgies schedule page, linked from the Bulletin page, answered 404
  retry_when: A Holy Trinity bulletin can be read, or the parish's schedule page is restored
- method: 'Hand refresh against main: visit.py on the home page (Mass times for St. James, Blessed Sacrament
    and Epiphany; Trinity Chapel listed with its address and no times) and on the Mass & Other Liturgies
    Schedule page linked from the Bulletin page (still 404); Catholic Star Herald REST search ''Trinity
    Chapel Margate'''
  url: https://www.holytrinitydownbeach.org/
  checked: '2026-11-07'
  outcome: not-found
  next_action: Read a bulletin once its /file links can be fetched, or ask the parish office
  retry_when: A Holy Trinity bulletin can be read, or the parish's schedule page is restored
---

## What is known

The parish site lists a fourth site, 'Trinity Chapel', at 12 N Jerome Ave., Margate, beside Blessed Sacrament; GCatholic lists a 'Chapel of the Holy Trinity' at 100 N Jerome Ave., Margate, as a mission of Blessed Sacrament. The street numbers differ (12 vs 100) and the two are presumably the same place. The parish's home page gives Mass times for St. James, Blessed Sacrament and Epiphany only; the chapel has no schedule on it, on the Our Churches page or in the summer guide.

## Why it is not decided

Nothing read says Mass is, or is not, celebrated at the chapel: the home page's silence is absence, not a statement, and the parish bulletin (which would show chapel Masses, weekday or Holy Day) could not be read. The parish's own Mass & Liturgies schedule page is a dead link (404, 2026-10-29). If a bulletin lists Mass there, it becomes a church row; if it says the chapel is a private or adoration chapel, it goes to excluded as no-public-mass.
