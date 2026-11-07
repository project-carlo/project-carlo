---
name: St. Casimir
reason: closed
line1: 147 Montgomery Street
city: Paterson
state: NJ
postal_code: '07501'
decided: 2026-11-05
roster: ['gcatholic:19002']
evidence:
- url: https://rcdop.org/parishes-of-the-paterson-diocese
  seen: 2026-11-05
  quote: 1911 Saint Casimir, Paterson closed in 2018
  note: The diocesan historian's chronological list of parishes (read with visit.py; probe get gets 403).
- url: https://gcatholic.org/churches/usa-03/19002
  seen: 2026-11-04
  note: GCatholic 19002 St. Casimir, Church, 147 Montgomery St., Paterson 07501, Plus Code 87G7WRFQ+XR;
    1911. GCatholic gives no closure.
- url: https://rcdop.org/parishfinder
  seen: 2026-11-04
  note: The diocese's parish finder (117 pins, rosters/directory.json) has no St. Casimir pin.
last_mass: '2018'
---

## Why it is excluded

The Diocese of Paterson's list of its parishes by founding year (https://rcdop.org/parishes-of-the-paterson-diocese, read 2026-11-05) has "1911 Saint Casimir, Paterson closed in 2018". The diocese's parish finder, which is also its Mass-times search, has no St. Casimir pin (checked 2026-11-04), and no other parish in this batch schedules Mass there. GCatholic (19002) still lists the church with no closure date, and OSM still has a node "Saint Casimir Roman Catholic Church, Montgomery Street" (node 357742118); neither says Mass is held there. The history says the parish closed; it doesn't say what became of the building, so `last_mass` is the year only.

## What would change this

A current schedule (a parish bulletin, the finder, a Beacon article) placing Mass in the building at 147 Montgomery Street, for instance if another parish or community now uses it.
