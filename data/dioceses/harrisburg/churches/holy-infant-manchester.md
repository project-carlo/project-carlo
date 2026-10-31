---
parish: holy-infant-manchester
name: Holy Infant
line1: 535 Conewago Creek Rd
line2: ''
city: Manchester
state: PA
postal_code: '17345'
latitude: 40.078934
longitude: -76.747876
coordinates_from: diocese-directory
name_verified: true
address_verified: false
roster: ['directory:holy-infant-manchester', 'gcatholic:23714']
evidence:
- url: https://www.hbgdiocese.org/parishes/holy-infant-manchester/
  seen: 2026-10-19
  note: 'Listed in Diocese of Harrisburg: Find a Parish, Church or Mass Time as ''Holy Infant Church'',
    535 Conewago Creek Rd, Manchester, PA, 17345; kind: Parish in Manchester'
- url: https://gcatholic.org/churches/usa-03/23714
  seen: 2026-10-19
  quote: 34 3rd St., York Haven, Pennsylvania 17370-8922
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Harrisburg as ''Holy Infant'',
    34 3rd St., York Haven, PA, 17370; kind: Church'
- url: https://www.fataonline.com/bulletin/bulletin-661792005981.pdf
  seen: 2026-10-19
  quote: 535 Conewago Creek Rd * Manchester, PA 17345
  note: 18 October 2026 issue, page 1, with "WEEKEND MASSES Saturday Vigil 5:00 PM Sunday 8:00 AM & 11:00
    AM".
- url: https://nominatim.openstreetmap.org/reverse?lat=40.1105625&lon=-76.7163125&format=json
  seen: 2026-10-19
  quote: Believers in Christ Community Church
  note: OpenStreetMap at GCatholic's Plus Code for 23714 (87G5476M+6F, York Haven) - way 667593921, place
    of worship, "37, Pennsylvania Avenue, York Haven". The building GCatholic pins is now another congregation's
    (inferred; no sale notice read).
promoted: 2026-10-20
---

## Holds Mass

Yes. The 18 October 2026 Holy Infant bulletin gives Saturday 5:00 pm and Sunday 8:00 and
11:00 am, with weekday Masses, and its calendar puts each Mass in "Church".

## Name and address

The diocesan directory ("Holy Infant Church", 535 Conewago Creek Rd, Manchester 17345)
and the bulletin agree on the address.
GCatholic's entry (23714, "Holy Infant") gives 34 3rd St., York Haven 17370, the former
church, with a Plus Code on a building OpenStreetMap now calls "Believers in Christ
Community Church". So only one independent source (the directory) backs the current
address: address_verified is false. Coordinates are the diocesan directory's pin
(40.078934, -76.747876), not GCatholic's, which is on the York Haven building about 4.5 km
away. Run `pnpm geocode` or check OSM to confirm the pin.
