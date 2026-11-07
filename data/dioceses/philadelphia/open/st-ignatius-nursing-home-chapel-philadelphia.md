---
name: St. Ignatius Nursing Home Chapel
revisit: 'Find out whether the weekday 9:30 AM Mass the directory gives at St. Ignatius Nursing Home''s
  chapel still happens and whether the public may attend: call St. Ignatius of Loyola (215-386-5065) or
  the nursing home, or read a later bulletin. A public weekday Mass makes it a church row under St. Ignatius;
  a residents-only or no Mass makes it an exclusion (no-public-mass).'
revisit_after: 2027-01-31
roster: []
evidence:
- url: https://archphila.org/parish/st-ignatius-of-loyola-philadelphia/
  seen: 2026-10-28
  quote: Monday through Friday, 9:30 AM (St. Ignatius Nursing Home Chapel, 4401 Haverford Ave.)
  note: 'Directory page for St. Ignatius of Loyola (updated 11 months before 2026-10-28): its weekday
    Mass is in the nursing home''s chapel.'
- url: https://www.church-bulletin.org/bulletin/saint-ignatius-of-loyola-philadelphia-pa-19104/2026-11-08.pdf
  seen: 2026-11-07
  quote: 'Nursing Home Monthly Mass: 9:30am 1st Wednesday of the Month (West Park Nursing & Rehab)'
  note: 'St. Ignatius''s 8 November 2026 issue (text layer), page 1 Mass schedule: no weekday Mass at
    all, only this monthly nursing-home Mass; page 4 prays for ''the residents of West Park Rehab Center
    and Centennial Village''. The 25 October 2026 issue read the same.'
- url: https://nominatim.openstreetmap.org/search?format=jsonv2&q=4401+Haverford+Avenue+Philadelphia
  seen: 2026-11-07
  note: OSM has 'St. Ignatius Nursing Home, 4401 Haverford Avenue, Mill Creek, West Philadelphia, 19139'
    (the ZIP used here). A search for 'West Park Nursing' found nothing, so whether the bulletin's West
    Park Nursing & Rehab is this building under a new name is not read.
parish: st-ignatius-of-loyola-philadelphia
line1: 4401 Haverford Ave.
city: Philadelphia
state: PA
postal_code: '19139'
research:
- method: Compared the directory's weekday Mass at the nursing home chapel with the 25 October and 8 November
    2026 St. Ignatius bulletins (probe pdf, grep for Nursing, West Park, Haverford, Weekday, Daily) and
    looked the facility up in OSM
  url: https://www.church-bulletin.org/bulletin/saint-ignatius-of-loyola-philadelphia-pa-19104/2026-11-08.pdf
  checked: '2026-11-07'
  outcome: not-found
  next_action: Call the parish office (215-386-5065) or the nursing home, or read a later bulletin
  retry_when: A bulletin lists a weekday Mass at the chapel, or the office says who may attend
---

## What is known

The archdiocese's directory page for St. Ignatius of Loyola (updated about 11 months before 2026-10-28) puts the parish's weekday Mass, Monday to Friday 9:30 AM, in St. Ignatius Nursing Home's chapel at 4401 Haverford Ave. The parish's own bulletin (25 October and 8 November 2026) lists no weekday Mass anywhere, only a 'Nursing Home Monthly Mass: 9:30am 1st Wednesday of the Month (West Park Nursing & Rehab)', and prays for the residents of West Park Rehab Center and Centennial Village. OSM still names the building at 4401 Haverford Ave. St. Ignatius Nursing Home; no source read says whether West Park Nursing & Rehab is the same place under a new name.

## Why it is not decided

No source says whether a weekday Mass is still said in the chapel, or whether anyone other than residents may attend. A Mass for a care home's residents is not a public worship site (the README's `no-public-mass` covers hospital chapels), but a public weekday Mass would make the chapel a church row under St. Ignatius. The directory's schedule is older than the bulletin, and the bulletin wins a disagreement, but its silence on weekday Mass is absence, not a statement. Map batch `west-philadelphia` raised it as a flag; the hand refresh against main (2026-11-07) made it this record, so the PR lists it.
