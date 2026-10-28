---
parish: st-john-the-baptist-holy-angels-newark
name: St. John the Baptist
line1: 200 East Main Street
line2: ''
city: Newark
state: DE
postal_code: '19711'
latitude: 39.6838865
longitude: -75.745333
coordinates_from: nominatim
name_verified: false
address_verified: false
roster: []
evidence:
- url: http://sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf
  seen: 2026-10-27
  quote: St. John Church
  note: 'Cover of the 25 October 2026 issue: ''St. John Church, East Main & North Chapel Streets, Newark,
    Delaware 19711'' with ''Monday, Tuesday, Thursday, Friday, Saturday 8:00 am (English); Sunday 7:30
    & 10:30 am (English)''; Confessions Saturday 8:30 am.'
- url: https://nominatim.openstreetmap.org/reverse?lat=39.6838865&lon=-75.745333&format=json
  seen: 2026-10-27
  note: 'OpenStreetMap way 369296520 (Nominatim search ''St John the Baptist Catholic Church Newark Delaware''):
    ''St. John the Baptist Roman Catholic Church, 200, East Main Street, Lumbrook, Newark ... 19717''.
    North Chapel Street is at 39.6859, -75.7461, so the building is at the East Main and North Chapel
    corner the bulletin names.'
promoted: 2026-10-27
---

## Holds Mass

The 25 October 2026 bulletin of St. John - Holy Angels Parish lists St. John Church, East Main & North Chapel Streets, with Mass Monday, Tuesday, Thursday, Friday and Saturday at 8:00 am and Sunday at 7:30 and 10:30 am. The diocese directory's times for its 'St. John the Baptist' entry (Sun 7:30 and 10:30; Mon, Tue, Thu, Fri, Sat 8:00; Thu 19:00) match these weekday and Sunday times, though the directory pins that entry at 82 Possum Park Road, which is Holy Angels (see holy-angels-newark).

## Name and address

Neither roster has this building: the diocese directory and GCatholic each carry one entry for the parish, at 82 Possum Park Road. The bulletin gives only the cross streets 'East Main & North Chapel Streets, Newark, Delaware 19711'. The street number and coordinates come from OpenStreetMap (200 East Main Street, postcode 19717, 39.6838865, -75.745333), which sits at that corner. Sources disagree on the postcode (bulletin 19711, OSM 19717); I used the bulletin's. `name_verified` and `address_verified` stay false: a second independent source for the street number (the parish website's About page, or the diocese) was not read. Coordinates are an OSM way centre via Nominatim, so `pnpm geocode` could refine them.
