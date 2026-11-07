---
name: Basilian Fathers of Mariapoch (former monastery church)
reason: other-jurisdiction
line1: 360 Monastery Ln.
city: Matawan
state: NJ
postal_code: '07747'
decided: 2026-10-30
roster: ['gcatholic:37947']
evidence:
- url: https://gcatholic.org/churches/usa-03/37947
  seen: 2026-10-30
  quote: now Magnolia Visitor Center
  note: 'GCatholic''s page, ''Former Monastery of the Basilian Fathers of Mariapoch (Hungarian)'', marked
    ''(now secular)'', Type: Former Church, Rite: Hungarian (Byzantine), Jurisdiction: Ukrainian Metropolitan
    Archdiocese of Philadelphia, ''within the territory of the Roman Diocese of Trenton'', 360 Monastery
    Ln., Matawan, New Jersey 07747, last updated 2025.12.21. The page gives no date for the last liturgy.'
- url: https://html.duckduckgo.com/html/?q=Magnolia+Visitor+Center+Matawan+360+Monastery+Lane+Basilian+Mariapoch
  seen: 2026-10-30
  note: 'One DuckDuckGo search: only GCatholic and business-directory aggregators (Yelp, MapQuest, Chamber
    of Commerce; some at ''329 Monastery Ln'') mention the monastery; no result describes a current liturgy
    or the Magnolia Visitor Center. Directory pages are not evidence of worship.'
research:
- method: GCatholic page read, plus one DuckDuckGo search for the visitor center and the monastery; OSM
    nominatim search for '360 Monastery Ln Matawan NJ' returned no result.
  url: https://gcatholic.org/churches/usa-03/37947
  checked: '2026-10-30'
  outcome: not-found
  next_action: Find a second source for the visitor center (Aberdeen Township or Monmouth County pages)
    and a date the liturgy ended; add last_mass.
  retry_when: A local source names the Magnolia Visitor Center or the monastery's closing
---

## Why it is excluded

GCatholic lists 360 Monastery Ln., Matawan as the 'Former Monastery of the Basilian Fathers of Mariapoch', rite Hungarian (Byzantine), type 'Former Church', marked '(now secular)', with the history 'now Magnolia Visitor Center'. Its jurisdiction there is the Ukrainian Metropolitan Archdiocese of Philadelphia, within the territory of the Diocese of Trenton, not a church of the Diocese of Trenton. That alone excludes it as `other-jurisdiction`, whether or not it is still open.

I did not record it as `closed`: the batch's rule allows 'other-jurisdiction or closed on what its source says', but the only source says the building is 'former' and 'now secular' with no date for the last liturgy, and a closed exclusion needs a `last_mass`. Neither the Diocese of Trenton's finder nor any Mass listing I found names a liturgy there, and the directory aggregators that still show the monastery (some at '329 Monastery Ln') say nothing about worship. I found no second source for the visitor center. See `research`.

## What would change this

A bulletin or local news item showing a public liturgy at 360 Monastery Ln. (unlikely given GCatholic's note) would make it an open place under its own eparchy, still not the diocese's. A dated closing would change the reason to `closed`.
