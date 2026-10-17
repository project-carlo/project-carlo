---
parish: epiphany-sayre
name: Our Lady of Perpetual Help
line1: 3418 Chapel Road
line2: ''
city: Milan
state: PA
postal_code: '18831'
latitude: 41.905227
longitude: -76.628878
coordinates_from: diocese-directory
name_verified: true
address_verified: false
roster: ['directory:155-2', 'gcatholic:24038']
evidence:
- url: https://www.dioceseofscranton.org/find-a-mass/
  seen: 2026-10-16
  note: Coordinates from the diocese's Find a Mass card for "Our Lady of Perpetual Help Church" (data-latitude
    41.905227, data-longitude -76.628878).
- url: https://www.dioceseofscranton.org/find-a-parish/epiphany-parish-sayre
  seen: 2026-10-16
  note: 'Listed in Diocese of Scranton Find a Parish: worship sites as ''Our Lady of Perpetual Help Church'',
    Chapel Road, Milan, PA, 18831; kind: worship-site; group: Epiphany Parish'
- url: https://gcatholic.org/churches/usa-03/24038
  seen: 2026-10-16
  quote: Ridgebury, Pennsylvania 16925
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Scranton as ''Our Lady of Perpetual
    Help'', Ridgebury, PA, 16925; kind: Church'
- url: https://discovermass.com/church/church-of-the-epiphany-sayre-pa/
  seen: 2026-10-16
  quote: 'Our Lady of Perpetual Help (OLPH): … 3418 Chapel Road … Milan, PA 18831 … 6:00 pm (OLPH) Ridgebury'
  note: Masthead and Mass Schedule of the 18 October 2026 Epiphany bulletin.
promoted: 2026-10-17
---

## Holds Mass

Yes, Saturday 6:00 pm. The 18 October 2026 Epiphany bulletin's Mass Schedule lists "Saturday:
(Vigil) ... 6:00 pm (OLPH) Ridgebury", and its masthead gives OLPH's address. The diocesan
finder also has Saturday 6:00 pm.

## Name and address

- The Epiphany bulletin: "Our Lady of Perpetual Help (OLPH): 3418 Chapel Road, Milan, PA 18831",
  with the Mass listed as "(OLPH) Ridgebury".
- The diocesan finder: "Our Lady of Perpetual Help Church, Chapel Road, Milan, PA 18831" (no
  number).
- GCatholic: "Our Lady of Perpetual Help", "Ridgebury, Pennsylvania 16925", no street and no
  Plus Code.

All three are one place: the chapel stands in Ridgebury Township with a Milan (18831) mailing
address. The street number comes from the bulletin only, so `address_verified` is false; the
name agrees in all three, so `name_verified` is true. No coordinates: GCatholic has no Plus
Code and Nominatim found no match for the address or the name on 2026-10-16; `pnpm geocode`
will fill them after promotion.
