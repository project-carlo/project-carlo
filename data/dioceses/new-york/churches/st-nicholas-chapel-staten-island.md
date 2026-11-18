---
parish: st-teresa-of-the-infant-jesus-st-nicholas-staten-island
name: St. Nicholas Chapel
line1: Northern Blvd. at La Bau Ave.
line2: ''
city: Staten Island
state: NY
postal_code: '10301'
latitude: 40.6134409
longitude: -74.1062556
coordinates_from: osm-node
name_verified: false
address_verified: false
roster: []
evidence:
- url: https://files.ecatholic.com/6635/bulletins/20261025.pdf
  seen: 2026-10-31
  quote: 9AM MASS WHICH IS IN ST. NICHOLAS
  note: 'Page 1 Mass schedule of the 25 October 2026 issue: all Sunday Masses are at St. Teresa on Victory
    Blvd. except the 9 AM, which is in St. Nicholas Chapel, on Northern Blvd. at La Bau Ave., one block
    in from Victory Blvd. The running header on every page names the Church of Saint Teresa of the Infant
    Jesus and St. Nicholas Chapel.'
- url: https://files.ecatholic.com/6635/bulletins/20261004.pdf
  seen: 2026-10-07
  quote: NICHOLAS CHAPEL, ON NORTHERN
  note: Same page-1 schedule in the 4 October 2026 issue.
- url: https://saintteresasi.org/mass-times
  seen: 2026-10-08
  quote: ST. NICHOLAS
  note: Parish Mass Times page lists St. Nicholas Sundays 9:00 am separately from the St. Teresa schedule
    (same publisher as the bulletin, so not an independent source).
- url: https://nominatim.openstreetmap.org/lookup?osm_ids=N357586617&format=jsonv2&addressdetails=1&extratags=1
  seen: 2026-10-31
  quote: Saint Nicholas Church
  note: OSM node 357586617, amenity=place_of_worship, denomination=catholic, on Northern Boulevard (Sunnyside,
    postcode 10301) at 40.6134409, -74.1062556, between the two Labau Avenue segments. Independent of
    the parish; agrees on the name and the street. No house number in OSM.
- url: https://files.ecatholic.com/6635/bulletins/20261108.pdf
  seen: 2026-11-08
  quote: 9AM MASS WHICH IS IN ST. NICHOLAS
  note: 'Page 1 Mass schedule of the 8 November 2026 issue, unchanged: the Sunday 9 AM Mass is in St.
    Nicholas Chapel on Northern Blvd. at La Bau Ave.'
promoted: 2026-11-09
---

## Holds Mass

The 8 November 2026 St. Teresa of the Infant Jesus - St. Nicholas bulletin (eCatholic 6635), page 1, says all Sunday Masses are in St. Teresa Church on Victory Blvd. "except the 9AM Mass which is in St. Nicholas Chapel, on Northern Blvd. at La Bau Ave., one block in from Victory Blvd." The 25 October and 4 October issues and the parish Mass Times page (read 8 October) say the same. One public Sunday Mass a week, published in the parish's own bulletin, so the chapel is a church under `st-teresa-of-the-infant-jesus-st-nicholas-staten-island`.

## Name and address

Neither the official archdiocesan map nor GCatholic lists the chapel, so it has no roster link (Settled policy 3: a place with solid evidence goes in anyway). The name is the parish's own ("St. Nicholas Chapel" in the bulletin's running header and schedule); OpenStreetMap calls the building "Saint Nicholas Church", so `name_verified` stays false. The bulletin locates it at the corner of Northern Boulevard and La Bau Avenue without a house number, and that corner is stored. A Google listing says 42 Northern Blvd, and NYC Geosearch's nearest address points to the OSM node are 44 and 22 Northern Boulevard and 76 Labau Avenue; none is a parish source, so no number is stored and `address_verified` is false. Coordinates are OSM node 357586617, a Catholic place of worship on Northern Boulevard between the two Labau Avenue segments, independent of the parish. The ZIP 10301 is OSM's for the node. The parish Maps and Directions page maps only St. Teresa at 1634 Victory Boulevard; its pin is not reused here.
