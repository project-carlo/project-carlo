---
name: Perpetual Adoration Chapel (former St. James Convent)
reason: no-public-mass
line1: 123 Whittington Rd.
city: Rochester
state: NY
postal_code: '14609'
decided: 2026-10-27
roster: []
evidence:
- url: https://www.peaceofchristparish.org/perpetual-adoration
  seen: 2026-10-26
  quote: located in the former St. James Convent
  note: 'Parish page ''Perpetual Adoration'': ''The Adoration Chapel is located at 123 Whittington Road,
    Irondequiot, NY 14609, with limited street parking and a short walk from the church parking lot.''
    ''The Chapel will remained locked 24/7. Call the parish office for the numerical code to enter the
    Chapel.'' Adorers sign up for hours on adore24.io under the chapel ''St James''. No Mass is mentioned.'
- url: https://discovermass.com/church/peace-of-christ-parish-at-st-ambrose-rochester-ny/
  seen: 2026-10-26
  note: 'The 25 October 2026 issue (stored by the pipeline as bulletin 14424d94). Page 1: ''Perpetual
    Adoration, 123 Whittington Road, Call the Parish Office to Sign Up for a Time''. Page 3: ''PERPETUAL
    ADORATION CHAPEL 123 Whittington Road, Rochester, NY 14609'' with weekly events there (Tuesdays 10:00
    AM Family Friendly Holy Hour; First Tuesdays 7:00 PM Holy Hour for Vocations; rosaries) and ''ACCESS
    THE CHAPEL Call the parish office at (585) 288-5000''. The page-1 Mass schedule and the page-3 Mass
    intentions put every Mass at St. Ambrose, St. James or St. John.'
- url: https://nominatim.openstreetmap.org/reverse?lat=43.167523&lon=-77.548393&format=json&zoom=18
  seen: 2026-10-26
  note: OSM building way 1332001810, 123 Whittington Road (43.1675023, -77.5485672), about 35 m east of
    St. James Church (130 Brett Road, live row `st-james-rochester`).
parish: peace-of-christ
---

## Why it is excluded

An adoration chapel with no Mass, so not a church row (README: one church row is one place of
public Mass). Peace of Christ's Perpetual Adoration Chapel is in the former St. James Convent at
123 Whittington Road. The parish's adoration page (read 2026-10-26) describes perpetual adoration
by sign-up, with the chapel "locked 24/7" and its door code given out by the parish office, and
mentions no Mass. The 25 October 2026 bulletin lists holy hours and rosaries there, but its Mass
schedule and Mass intentions put every Mass at St. Ambrose, St. James or St. John. The evidence
for "no Mass" is that complete schedule, not a statement. Rochester excluded Elmira's adoration
chapel the same way (`excluded/eucharistic-adoration-chapel-elmira`).

The building is about 35 m east of St. James Church (OSM), "a short walk from the church parking
lot", with its own street address. Whether it counts as on St. James's grounds (so that its
adoration hours could be shown at `st-james-rochester`) is a question for whoever uses the
adoration times; I could not read Monroe County's parcel data to check.

## What would change this

A Mass scheduled in the chapel (in the bulletin or on the parish's Mass page) would make it a
church row under `peace-of-christ`.
