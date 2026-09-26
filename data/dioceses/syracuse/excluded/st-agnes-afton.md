---
name: St. Agnes
reason: closed
line1: 14 Spring St.
city: Afton
state: NY
postal_code: '13730'
decided: 2026-09-26
roster: ['gcatholic:17976', 'directory:33081']
evidence:
- url: https://gcatholic.org/churches/usa-02/17976
  seen: 2026-09-25
  quote: 14 Spring St., Afton, New York 13730
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''St. Agnes'', 14
    Spring St., Afton, NY, 13730; kind: Mission'
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: 'Listed in Diocese of Syracuse parish finder (Mass-times map) as ''St. Agnes Mission (Closed)'',
    Afton, NY; kind: closed'
- url: https://discovermass.com/church/st-john-the-evangelist-bainbridge-ny/
  seen: 2026-09-26
  quote: 'Note: St. John''s Mission Church of St. Agnes (Afton) is permanently closed.'
  note: The mother church's Discover Mass (MassTimes) listing, whose Mass times give only "Sunday 9:30am"
    at St. John's.
- url: https://www.syracusediocese.org/st-john-the-evangelist-bainbridge
  seen: 2026-09-26
  quote: Sacramental Records for St. Agnes Mission, Afton are retained here.
  note: The successor's page on the diocese site (read with visit.py). The diocese's parish list (syracusediocese.org/parishes,
    read 2026-09-26) has "St. Agnes Mission, Afton (CLOSED - See St. John the Evangelist, Bainbridge)".
- url: https://discovermass.com/church/st-agnes-catholic-church-afton-ny/
  seen: 2026-09-26
  quote: St. Agnes is a Mission Church of St. John the Evangelist (Bainbridge).
  note: St. Agnes's own Discover Mass listing still shows "Sunday 8:30am" under a COVID-era notice; stale,
    and contradicted by the mother church's listing above.
- url: https://www.openstreetmap.org/node/357649627
  seen: 2026-09-26
  note: OSM place_of_worship "Saint Agnes Catholic Church", Spring Street, Afton 13730 (the building;
    OSM does not record use).
---

## Why it is excluded

St. Agnes, Afton, was the mission church of St. John the Evangelist, Bainbridge. Two sources say
it is closed:

- the diocese's parish list (read 2026-09-26): "St. Agnes Mission, Afton (CLOSED - See St. John the
  Evangelist, Bainbridge)", and its parish finder lists "St. Agnes Mission (Closed)"; St. John's page
  keeps "Sacramental Records for St. Agnes Mission, Afton";
- the mother church's Discover Mass (MassTimes) listing: "St. John's Mission Church of St. Agnes
  (Afton) is permanently closed", with Mass times for St. John's only.

The diocese's statement is about the canonical mission; the Discover Mass note, which comes from the
parish's own MassTimes listing, is about the church, and the mother church's schedule there has no
Afton Mass. St. John's itself publishes no bulletin (`excluded/st-john-the-evangelist-bainbridge.md`),
so I could not check a current bulletin, and St. Agnes's own Discover Mass page still shows a
COVID-era "Sunday 8:30am", which I read as stale. No closing date was found, so `last_mass` is empty;
the parish's Google site still listed St. Agnes as a Mass site in 2020, so the closure is after that.

## What would change this

Nothing expected. See `revisit` for dating it.
