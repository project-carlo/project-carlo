---
parish: st-francis-of-assisi-albany
name: St. Francis of Assisi, South End Community (former St. Ann)
line1: 93 Fourth Avenue
line2: ''
city: Albany
state: NY
postal_code: '12202'
latitude: 42.6391243
longitude: -73.7574696
coordinates_from: osm-node
name_verified: true
address_verified: false
roster: ['directory:379']
evidence:
- url: https://www.rcda.org/parishes/parish/st-francis-assisi-parish-albany-ny
  seen: 2026-09-28
  note: Listed in Diocese of Albany Find A Parish list as 'St. Francis of Assisi, South End Community',
    95 Fourth Ave., Albany, NY, 12202
- url: https://container.parishesonline.com/bulletins/04/0736/20260927B.pdf
  seen: 2026-09-28
  quote: Mass 10:30 am St. Francis (South End)
  note: '"Confession and Mass Schedule", page 4 of the 27 September 2026 issue. Masthead: "South End 93
    Fourth Avenue,Albany".'
- url: https://www.openstreetmap.org/way/534744722
  seen: 2026-09-28
  quote: addr:housenumber 93 addr:postcode 12202 addr:state NY addr:street Fourth Avenue amenity place_of_worship
  note: OpenStreetMap way 534744722, named "Church of Saint Ann".
- url: https://nominatim.openstreetmap.org/reverse?lat=42.63909&lon=-73.75772&format=json&zoom=18
  seen: 2026-09-28
  note: Nominatim puts 95 Fourth Avenue on the untagged building next door (way 541998350); the church
    outline (way 534744722) is centred at 42.63912, -73.75747.
- url: https://discovermass.com/church/st-john-st-ann-now-south-end-community-of-st-francis-of-assisi-parish-albany-ny/
  seen: 2026-09-28
  note: Discover Mass names the listing "St. John-St. Ann (Now South End Community of St. Francis of Assisi
    Parish)".
promoted: 2026-09-28
---

## Holds Mass

Yes. The 27 September 2026 St. Francis of Assisi bulletin lists "Mass 10:30 am St. Francis
(South End)" every Sunday. (The same issue's intentions list the South End 10:30 am Mass
under "Sat." dates, 13 and 20 September; the schedule box says Sunday, and so does the
directory, so Sunday is taken as right.)

## Name and address

The building is the former St. Ann's church of the St. John-St. Ann parish (OpenStreetMap
names it "Church of Saint Ann"; Discover Mass "St. John-St. Ann (Now South End Community ...)";
the institutional-records index sends St. Ann's, St. John's and St. John's-St. Ann's records to
this community). `name_verified` is true: the directory and the bulletin both call it St.
Francis of Assisi's South End community.

**The street number disagrees:** the bulletin masthead and OpenStreetMap's church outline say
**93** Fourth Avenue; the diocese's directory says **95** Fourth Ave. ("At Franklin St."). The
record follows the bulletin and OSM, since OSM puts the church at 93 and an untagged building
at 95, but `address_verified` stays false. Coordinates are OSM's church outline (way
534744722). No GCatholic entry exists for this church.
