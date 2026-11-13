---
name: St. John Cemetery chapel
reason: no-bulletin
line1: 80-01 Metropolitan Avenue
city: Middle Village
state: NY
postal_code: '11379'
decided: 2026-11-06
roster: ['gcatholic:38954']
evidence:
- url: https://ccbklyn.org/our-cemeteries/st-john-cemetery/
  seen: 2026-11-06
  quote: Masses are currently celebrated Monday – Friday at 9:30 AM
  note: The Catholic Cemeteries page for St. John Cemetery, 80-01 Metropolitan Avenue, Middle Village,
    NY 11379, under the heading 'Daily and Special Masses'; it adds that Field Masses are celebrated on
    Memorial Day and All Souls Day. The page does not name the building the weekday Mass is in.
- url: https://gcatholic.org/churches/usa-02/38954
  seen: 2026-11-05
  note: 'GCatholic 38954: St. John chapel (St. John Cemetery), 80-01 Metropolitan Ave., Middle Village,
    New York 11379, Plus Code 87G8P48M+6F (40.7156, -73.8663); website http://www.ccbklyn.org/our-cemeteries/saint-john/,
    which now answers 404 and redirects to ccbklyn.org.'
- url: https://mass.dioceseofbrooklyn.org/
  seen: 2026-11-06
  note: The Mass finder roster (every /places page, read by the survey) has no place at 80-01 Metropolitan
    Avenue or named for a cemetery; no other Brooklyn roster lists it.
---

## Why it is excluded

The chapel has public Mass but no bulletin. The Catholic Cemeteries (Saint John's Cemetery Corporation) page for St. John Cemetery, read 2026-11-06, says under "Daily and Special Masses": "Masses are currently celebrated Monday – Friday at 9:30 AM", with Field Masses on Memorial Day and All Souls Day. The page is addressed to the public (families visiting the cemetery), so the weekday Mass is treated as public, as the diocese's settled rule treats chaplaincy chapels such as the JFK airport chapel. No parish bulletin covers it: the three Middle Village and Glendale parishes' schedules (Our Lady of Hope, St. Margaret, Sacred Heart of Jesus) name only their own churches, and the cemetery publishes no bulletin; its schedule exists only as a line on its web page, which `fetch` can't read as a bulletin. So it is `no-bulletin`, not `closed` or `no-public-mass`.

The page does not say which building the Mass is in. GCatholic places its St. John chapel at the cemetery's address, 80-01 Metropolitan Avenue (the main entrance and office); that is the address recorded here.

## What would change this

A bulletin or regular published schedule naming the chapel (from the cemeteries or a parish) would make it a church row of that publisher. If the cemetery page drops the weekday Mass line, or a source says the Mass is private (for staff or religious only), the reason becomes `no-public-mass`.
