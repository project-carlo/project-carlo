---
parish: holy-cross-philadelphia
name: Holy Cross
line1: 140 East Mount Airy Avenue
line2: ''
city: Philadelphia
state: PA
postal_code: '19119'
latitude: 40.0616875
longitude: -75.1891875
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:19070', 'directory:holy-cross-philadelphia']
evidence:
- url: https://gcatholic.org/churches/usa-03/19070
  seen: 2026-10-28
  quote: E Mount Airy Ave. & Chew Ave., Philadelphia, Pennsylvania 19119
  note: 'Listed in GCatholic: churches of the Roman Catholic Archdiocese of Philadelphia as ''Holy Cross'',
    E Mount Airy Ave. & Chew Ave., Philadelphia, PA, 19119; kind: Church'
- url: https://archphila.org/parish/holy-cross-philadelphia/
  seen: 2026-10-28
  note: 'Listed in Archdiocese of Philadelphia: Directory of Parishes as ''Holy Cross'', E. Mt. Airy Ave.
    between Chew Ave. and Boyer St., Philadelphia, PA, 19119; kind: Parish; group: Philadelphia Northwest'
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-community-of-holy-cross-philadelphia-pa-19119/2026-10-25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (image-only, rendered), page 1: ''Holy Cross Catholic Church, Our Catholic
    community in Mount Airy''; Mass Schedule Sundays 9:00am, 11:00 am, 6:00pm, Saturday Vigil 5:00 pm,
    Tuesday-Friday 8:00 AM; ''Church Address 140 East Mount Airy Ave, Philadelphia PA 19119'', ''Office
    Hours & Address 154 East Mount Airy Ave''.'
- url: https://holycrossphl.org/
  seen: 2026-10-29
  quote: 'Sunday: 9am, 11am, and 6pm'
  note: Home page Mass Times, Saturday 5pm, weekdays Tuesday-Friday 8am.
- url: https://nominatim.openstreetmap.org/search?format=jsonv2&q=Holy+Cross+Church+East+Mount+Airy+Avenue
  seen: 2026-10-29
  note: OSM place_of_worship 'Holy Cross Catholic Church, 154, East Mount Airy Avenue' at 40.06155, -75.18900,
    about 20 m from GCatholic's pin; 140 East Mount Airy Avenue is a separate house point at 40.06177,
    -75.18921.
---

## Holds Mass

Yes, currently. The 25 October 2026 bulletin (image-only, rendered) lists Saturday vigil 5:00 pm, Sunday 9:00 am, 11:00 am and 6:00 pm, Tuesday-Friday 8:00 AM and holy days 8:00 AM and 7:00 PM; the parish site's Mass Times page gives the same.

## Name and address

The name is 'Holy Cross' in the directory, GCatholic and OSM, and 'Holy Cross Catholic Church' on the bulletin masthead, so `name_verified` is true. The address is not settled across sources: the bulletin gives 'Church Address 140 East Mount Airy Ave' and 'Office Hours & Address 154 East Mount Airy Ave'; the directory gives 'Parish Office: 154 E. Mt. Airy Avenue' and the church only as 'E. Mt. Airy Ave. between Chew Ave. and Boyer St.'; GCatholic gives 'E Mount Airy Ave. & Chew Ave.'; OSM puts the church node at 154. I followed the bulletin (140) as the church and left `address_verified` false. Coordinates are GCatholic's Plus Code (87G63R66+M8), within about 20 m of OSM's church node.
