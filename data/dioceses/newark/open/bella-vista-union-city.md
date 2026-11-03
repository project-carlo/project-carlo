---
name: Bella Vista (Saturday Spanish Mass, Sts. Joseph and Michael)
revisit: 'Find where ''Bella Vista'' is and whether its Saturday 4:00PM Spanish Mass is open to the public:
  ask or read the Sts. Joseph and Michael site or a later bulletin; if a parish-schedule Mass at a public
  place, make it a church row of ss-joseph-and-michael-union-city, otherwise exclude as no-public-mass.'
revisit_after: 2026-12-01
roster: []
evidence:
- url: https://container.parishesonline.com/bulletins/03/0699/20261101B.pdf
  seen: 2026-11-03
  quote: 4:00PM (Español - Bella Vista)
  note: Page 1 Mass schedule, Saturday; page 2 'Your Sacrificial Giving' lists a separate collection '4:00PM
    (BELLA VISTA) $40'. No address given.
- url: https://nominatim.openstreetmap.org/search?q=Bella+Vista+Union+City+NJ&format=json
  seen: 2026-11-03
  note: OSM's only match is 'Bella Vista Apartments, West Street, Union City' (way 585532302, 40.7669765,
    -74.0341191), a residential building.
- url: https://www.ssjmnj.org/
  seen: 2026-11-03
  note: The parish homepage lists 'Saturday 8:30 am & 5:30 pm in English 4:00 pm & 7:00 pm in Spanish'
    without saying where the 4:00 pm Mass is.
parish: ss-joseph-and-michael-union-city
line1: West Street
city: Union City
state: NJ
postal_code: 07087
research:
- method: probe pdf grep of the 1 November 2026 bulletin for 'Bella'; parish homepage text; Nominatim
    search
  url: https://container.parishesonline.com/bulletins/03/0699/20261101B.pdf
  checked: '2026-11-03'
  outcome: not-found
  next_action: Read the parish site's other pages (calendar, I'm new here) with visit.py, or a later bulletin,
    for the Bella Vista address and who may attend
  retry_when: A later Sts. Joseph and Michael bulletin or site page mentions Bella Vista
---

## What is known

The Sts. Joseph and Michael bulletin of 1 November 2026 lists, among its Saturday Masses, '4:00PM (Español - Bella Vista)', and reports a separate collection from that Mass ($40 on 31 October). The parish homepage gives the 4:00 pm Spanish Mass without a place. OSM's only 'Bella Vista' in Union City is the Bella Vista Apartments on West Street, a residential building, probably senior housing; no source read says so.

## Why it is not decided

No source gives the address or says whether the Mass is open to the public. A Mass for residents of an apartment building would be `no-public-mass`; a public parish Mass there would be a church row. Neither is stated, so this stays open until the parish says where it is.
