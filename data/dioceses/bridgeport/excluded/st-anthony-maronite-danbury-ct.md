---
name: St. Anthony
reason: other-jurisdiction
line1: 17 Granville Ave.
city: Danbury
state: CT
postal_code: 06810
decided: 2026-11-12
roster: ['gcatholic:17014']
evidence:
- url: https://gcatholic.org/churches/usa-01/17014
  seen: 2026-11-12
  quote: Maronite Diocese of Saint Maron of Brooklyn
  note: GCatholic lists the jurisdiction as the Maronite Diocese of Saint Maron of Brooklyn, within the
    territory of the Roman Diocese of Bridgeport.
---

## Why it is excluded

GCatholic's page for St. Anthony, 17 Granville Ave., Danbury (read 2026-11-12 with `probe get`) gives "Jurisdiction: Maronite Diocese of Saint Maron of Brooklyn" and "Location: within the territory of the Roman Diocese of Bridgeport". So it belongs to the Maronite Eparchy of St. Maron of Brooklyn, not to the Diocese of Bridgeport, and this dataset's Bridgeport records don't carry it. The survey-review rule in `diocese.md` (*Rules settled*, 003-survey-review, 2026-11-12) excludes Fairfield County's Eastern Catholic churches as other-jurisdiction.

Checked as well (2026-11-12): neither the diocese's directory roster (`rosters/directory.json`) nor its Mass-times roster (`rosters/mass-times.json`) lists this church or its address. Whether it holds public Divine Liturgy now was not checked, and neither was whether it publishes a bulletin; the exclusion rests on jurisdiction alone.

## What would change this

A decision to map Eastern Catholic eparchies in their own right. That would be done under the eparchy, not under Bridgeport.
