---
parish: hudson-valley-vicariate-west-catskill
name: St. Patrick
line1: 66 William St.
line2: ''
city: Catskill
state: NY
postal_code: '12414'
latitude: 42.2183125
longitude: -73.8615625
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:18127', 'directory:290']
evidence:
- url: https://gcatholic.org/churches/usa-02/18127
  seen: 2026-09-28
  quote: 157 Bridge St., Catskill, New York 12414
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Albany as ''St. Patrick'', 157
    Bridge St., Catskill, NY, 12414; kind: Church'
- url: https://www.rcda.org/parishes/parish/st-patricks-church-catskill-ny
  seen: 2026-09-28
  note: Listed in Diocese of Albany Find A Parish list as "St. Patrick's Church", 66 William Street, Catskill,
    NY, 12414
- url: https://stmaryscoxsackie.com/wp-content/uploads/2026/09/Coxsackie-Bulletin-September-27.pdf
  seen: 2026-09-28
  quote: 66 Williams Street Catskill, NY 12414 Mass Times Sunday 8:45 AM
  note: 'HVVW network bulletin cover, 27 September 2026: Sunday 8:45 am, 2nd, 4th & 5th Saturday 4 pm.'
- url: https://nominatim.openstreetmap.org/search?format=json&q=Saint+Patrick+Catskill+NY
  seen: 2026-09-28
  note: OSM way 1355047874 "Saint Patrick Catholic Church", tagged 157 Bridge Street, Catskill 12414.
    The building itself lies inside the 66 William St tax parcel (see the NYS parcel evidence).
- url: https://stpatrickathenscatskill.org/directions/
  seen: 2026-10-26
  quote: Worship Locations
  note: 'The parish''s Directions page lists under ''Worship Locations'': ''24 North Washington Street,
    Athens, New York 12015'' and ''66 William Street, Catskill, New York 12414'', then ''Network Office
    66 William Street''. Its embedded map for Catskill points at ''St Patrick''s Church'' (42.21884, -73.86306).'
- url: https://gisservices.its.ny.gov/arcgis/rest/services/NYS_Tax_Parcels_Public/MapServer/1/query?geometry=-73.8616110,42.2184013&geometryType=esriGeometryPoint&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=PARCEL_ADDR,PRIMARY_OWNER,USED_AS_DESC&returnGeometry=false&f=json
  seen: 2026-10-26
  note: 'NYS public tax parcels (2025 roll): the point of the OSM church building falls in parcel 156.18-8-8,
    ''66 William St'', owner "St Patrick''s", 1.3 acres. The parcel at 157 Bridge St (156.18-8-9) is owned
    by "St Patrick''s Rectory" and coded convent/rectory.'
promoted: 2026-09-28
---

## Holds Mass

Yes. The HVVW network bulletin of 27 September 2026 gives Sunday 8:45 am and the 2nd, 4th
and 5th Saturday 4 pm at St. Patrick's Catskill; Wednesday 8:30 am per the parish site.

## Name and address

Changed on 2026-10-26 from 157 Bridge St. to **66 William St.** The sources split:

- 66 William Street: the HVVW bulletin ("66 Williams Street"; the 27 September issue above, and
  page 2 of the 24 October issue), the parish's own Directions page, which lists it under
  "Worship Locations" as well as for the network office, and the diocese's directory. The NYS
  tax-parcel layer puts the church building (OSM way 1355047874, and GCatholic's Plus Code)
  inside the 66 William St parcel, owned by "St Patrick's".
- 157 Bridge Street: GCatholic and the address tags on the OSM church building. The NYS
  parcel at 157 Bridge St belongs to "St Patrick's Rectory" and is coded convent/rectory, so this
  looks like the rectory's address carried onto the church.

The earlier version of this record read 66 William Street as only the office's address; the
parish's "Worship Locations" list and the parcel data say it is the church's too. The street is
"William" (tax roll, parish site, directory); the bulletin's "Williams" is a misspelling. Name
flag true; address flag stays false because GCatholic and OSM still disagree. Coordinates are
GCatholic's Plus Code, on the church building, and did not change.
