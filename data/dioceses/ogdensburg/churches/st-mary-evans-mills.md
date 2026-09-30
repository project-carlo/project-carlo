---
parish: river-catholics-evans-mills
name: St. Mary's Church
line1: 8422 S. Main Street
line2: ''
city: Evans Mills
state: NY
postal_code: '13637'
latitude: 44.0851875
longitude: -75.8090625
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:18275', 'directory:evans-mills']
evidence:
- url: https://gcatholic.org/churches/usa-02/18275
  seen: 2026-09-30
  quote: 8408 S Main St., Evans Mills, New York 13637
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Ogdensburg as ''St. Mary'', 8408
    S Main St., Evans Mills, NY, 13637; kind: Church'
- url: https://www.rcdony.org/parish/evans-mills
  seen: 2026-09-30
  note: Listed in Diocese of Ogdensburg parish directory as "St. Mary's Church", 8422 S. Main Street,
    Evans Mills, NY, 13637
- url: https://files.ecatholic.com/21398/documents/2026/9/September%2027%202026.pdf
  seen: 2026-09-30
  quote: St. Mary's 8:00 AM
  note: Page 1, Sunday schedule, 27 September 2026 issue of River Catholics.
- url: https://files.ecatholic.com/21398/documents/2026/9/September%2027%202026.pdf
  seen: 2026-09-30
  quote: St. Mary's (9:15am) - Andrew Kilcer
  note: 'Page 2: Thursday 1 October 9:15 am; Sunday 27 September 8:00 am (Regina Barczykowski) and 4 October
    8:00 am.'
- url: https://files.ecatholic.com/21398/documents/2026/9/September%2027%202026.pdf
  seen: 2026-09-30
  quote: St. Mary's/St. Paul's 8422 S. Main Street, Evans Mills, NY 13637
  note: Page 1, "Parish Office". The same page prints "St. Mary's Church, Inc. 1920".
- url: https://rivercatholics.org/contact-us
  seen: 2026-09-30
  note: 'Parish site (read with visit.py): "St. Mary''s Church 8422 S Main St. Evans Mills, NY 13637"
    under "Parish Addresses"; the parish office is also 8422 S. Main Street.'
- url: https://files.ecatholic.com/21398/documents/2019/7/Parish%20Consolication%20DioCESE%20OF%20OGDENSBURG.pdf
  seen: 2026-09-30
  quote: St. Mary's Church 8408 South Main Street Evans Mills, New York 13637
  note: Page 1, the 6 March 2019 chancery letter to Msgr. Aucoin, addressed to the church at 8408 South
    Main Street.
- url: https://nominatim.openstreetmap.org/search?format=jsonv2&q=8408+South+Main+Street,+Evans+Mills,+NY
  seen: 2026-09-30
  note: OpenStreetMap has address nodes for both "8408, South Main Street" (44.0851750, -75.8093897) and
    "8422, South Main Street" (44.0851949, -75.8093627), 3 m apart; the GCatholic Plus Code point is 44.0851875,
    -75.8090625.
promoted: 2026-09-30
---

## Holds Mass

Yes. The 27 September 2026 River Catholics bulletin lists Sunday 8:00 am (page 1 schedule and page 2
intentions) and Thursday 1 October 9:15 am at St. Mary's, and Sunday 4 October 8:00 am; the same
Sunday and Thursday Masses appear in the OLSH bulletin of the same date ("8:00am - St. Mary's",
"9:15am - St. Mary's"). Confessions first Sunday of the month 7:30-7:50 am.

## Name and address

**Disagreement on the street number.** The diocese's directory, the parish site's "Parish Addresses"
and the bulletin's parish-office line say 8422 S. Main Street; GCatholic and the 2019 chancery letter
addressed to "St. Mary's Church" say 8408 South Main Street (GCatholic's Philadelphia and Theresa
entries copy this address, but for Evans Mills it is the parish's own). OpenStreetMap has address nodes
for both numbers 3 m apart, i.e. they are two numbers on one lot, probably the church (8408) and the
office/rectory (8422), but nothing says which is which. I used the parish's current 8422, kept
GCatholic's Plus Code coordinates and left `address_verified` false. `name_verified` is true
(bulletin, directory, GCatholic, parish site and the 1920-incorporation line all say St. Mary's).
