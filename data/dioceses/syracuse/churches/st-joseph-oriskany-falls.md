---
parish: holy-spirit-hamilton
name: St. Joseph's Church
line1: 229 Main St.
line2: ''
city: Oriskany Falls
state: NY
postal_code: '13425'
latitude: 42.9388125
longitude: -75.4645625
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:18016', 'directory:33143']
evidence:
- url: https://gcatholic.org/churches/usa-02/18016
  seen: 2026-09-25
  quote: 229 Main St., Oriskany Falls, New York 13425-0131
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''St. Joseph'', 229
    Main St., Oriskany Falls, NY, 13425'
- url: https://www.romesentinel.com/news/route-20-catholic-churches-holy-spirit-parish-merger/article_66a992b3-2d7e-4d30-b659-9116c53bb9c1.html
  seen: 2026-09-25
  quote: St. Joseph’s Church, 229 Main St. in Oriskany Falls
  note: The Rome Sentinel's report (18 June 2026) of the merger decree, effective 1 July 2026, naming the four churches of Holy Spirit Parish.
- url: https://www.openstreetmap.org/way/603072533
  seen: 2026-09-25
  note: 'OSM: a building at 229 Main Street, 13425.'
- url: https://files.ecatholic.com/39636/bulletins/20260925.pdf
  seen: 2026-09-26
  quote: 6:00 pm   Vigil Mass at St. Joseph’s
  note: Holy Spirit Parish bulletin, 27 September 2026 (file dated 25 September), page 1 Mass schedule
    and masthead.
- url: https://www.syracusediocese.org/holy-spirit-parish-waterville
  seen: 2026-09-26
  quote: 227 Main Street
  note: behind Cloudflare; read in a browser (parish-site-access visit.py). The diocese's parish page
    for Holy Spirit, listing its four churches with physical addresses.
---

## Holds Mass

Yes: Saturday 6:00 pm vigil, in Holy Spirit Parish's bulletin for 27 September 2026 (eCatholic 39636,
file 20260925.pdf, page 1), whose masthead names this church among the parish's four.
This settles the earlier "not confirmed" (the 2025 Route 20 Catholic PDF that a search summary
had cited is no longer needed).

## Name and address

GCatholic and the Rome Sentinel both give 229 Main St., and OSM has a building at 229 Main Street about 30 m from GCatholic's Plus Code, which was the basis for `address_verified`. Coordinates are GCatholic's Plus Code, decoded.

**Since this record was first written, the diocese's parish page (read 2026-09-26) has given 227 Main Street**, against 229 from GCatholic, the Sentinel and OSM's building. Three sources still say 229, so it is modelled there, but `address_verified` is now false because the sources disagree. The name matches the bulletin's and the Rome Sentinel's (independent), so
`name_verified` is true.
