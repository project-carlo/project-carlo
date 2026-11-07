---
parish: catholic-community-of-hopewell-valley
name: St. James Chapel
line1: 6 Eglantine Avenue
line2: ''
city: Pennington
state: NJ
postal_code: 08534
latitude: 40.3287017
longitude: -74.7888303
coordinates_from: osm-node
name_verified: false
address_verified: false
roster: []
evidence:
- url: https://www.church-bulletin.org/bulletin/the-catholic-community-of-hopewell-valley-hopewell-nj-08525/2026-11-01.pdf
  seen: 2026-10-30
  note: 'Read from a render by map batch hopewell (the issue is image-only). Page 1 masthead: "St. James
    Chapel * 6 Eglantine Avenue * Pennington, NJ 08534", beside "St. James Parish * 115 E. Delaware Avenue".
    Page 4, St. James column: "Weekday Mass: M, T, Th, F 9:00am Chapel  Eucharistic Service: Wed. 9:00am".
    Page 3: "St. James (Chapel) - First Fridays of the month 9:30am-8pm" adoration; rosary "after daily
    9:00am Mass in the Chapel".'
- url: https://stjamespennington.org/mass-and-confession
  seen: 2026-10-30
  note: 'Community site: weekday Mass (Mon, Tue, Thu, Fri) 9:00am in the Chapel, Eucharistic Service Wednesdays
    9:00am Chapel.'
- url: https://nominatim.openstreetmap.org/search?q=6+Eglantine+Avenue,+Pennington,+NJ&format=json
  seen: 2026-10-30
  note: OSM way 11645768 (tagged as a house, unnamed), 6 Eglantine Avenue, Pennington, at 40.3287017,
    -74.7888303, about 125 m from St. James Church's Plus Code point.
promoted: 2026-10-30
---

## Holds Mass

Yes, on weekdays. The Catholic Community of Hopewell Valley's 1 November 2026 bulletin (image-only, read from renders) prints St. James's weekday Mass as "M, T, Th, F 9:00am Chapel" with a Wednesday Eucharistic Service in the Chapel, and first-Friday adoration in "St. James (Chapel)". The parish's site gives the same. Weekend Masses are in St. James Church (`st-james-pennington`).

## Name and address

The masthead lists "St. James Chapel * 6 Eglantine Avenue * Pennington, NJ 08534" as an address of its own, apart from the church at 115 E. Delaware Avenue. No roster lists it. OSM has an unnamed building (way 11645768, tagged house) at 6 Eglantine Avenue. Its point, used for the coordinates, is about 125 m from the church's Plus Code point. Only the parish (bulletin and site, one source) names the chapel, and OSM confirms only that the number exists, so both flags are false. Whether the chapel is a separate building or a converted house on the church block hasn't been seen on site.

## Why a row

The map batch kept the chapel within St. James's row and flagged the question. Reconcile (2026-10-30) applied the diocese's settled rule (*Rules settled*: a chapel the parish lists with its own street address and daily Mass is a church row, as with St. Isidore's Assumption Chapel, New Egypt) and made it a row, so the weekday Masses "in the Chapel" have their own place. If the owner prefers chapels within ~150 m of their church to stay on the church's row, exclude this record as `other` and say so in the rule.
