---
parish: st-catherine-of-sienna-franklin-square
name: SCS Chapel (Sienna Center)
line1: 990 Holzheimer Street
line2: ''
city: Franklin Square
state: NY
postal_code: '11010'
latitude: 40.7084355
longitude: -73.676519
coordinates_from: osm-node
name_verified: true
address_verified: false
roster: []
evidence:
- url: https://www.stcatherineofsienna.org/whats-happening/bulletin/48-november-8-2026/file
  seen: 2026-11-13
  note: 'Page 2 of the November 8, 2026 bulletin (rendered): Saturday 4:30 P.M. (Vigil Mass) - SCS Chapel;
    ''Sunday - SCS Chapel (in Sienna Center)'' 9:45 A.M., 1:00 P.M. The Mass intentions (text) list ''Sienna
    Center 4:30 P.M.'', ''Sienna Center 9:45 A.M.'', ''Sienna Center 1:00 P.M.''.'
- url: https://www.stcatherineofsienna.org/
  seen: 2026-11-13
  quote: 'Sunday: 9:45 AM and 1:00 PM at SCS Chapel / Sienna Center'
  note: 'Home page Mass schedule (read with visit.py); also ''Saturday Vigil: 4:30 PM at SCS Chapel''.'
- url: https://www.drvc.org/mass-times/
  seen: 2026-11-13
  note: 'DRVC Mass-times entry for St. Catherine of Sienna: ''Saturday (for Sunday): 4:30 PM SCS Chapel
    / Sunday Mass: 7:30 AM, 8:45 AM, 11:30 AM Church / 9:45 AM, 1:00 PM SCS Chapel''.'
- url: https://nominatim.openstreetmap.org/search?q=990+Holzheimer+Street+Franklin+Square&format=json
  seen: 2026-11-13
  note: 'OSM: ''Saint Catherine of Siena School, 990, Holzheimer Street, Franklin Square'' (node 357584074,
    40.7084355, -73.6765190), about 70 m west of the church.'
revisit: Confirm the Sienna Center's address (a parish page, a bulletin notice or the diocese) and that
  the SCS Chapel is in the 990 Holzheimer Street building.
revisit_after: 2027-01-15
research:
- method: Parish site contact and about pages, the November 8, 2026 bulletin, and OSM search for 'Sienna
    Center Franklin Square'
  url: https://www.stcatherineofsienna.org/get-connected/contact-us-directions
  checked: '2026-11-13'
  outcome: not-found
  next_action: Look for an address given for the Sienna Center in later bulletins or parish event notices
  retry_when: A bulletin or page gives the Sienna Center's street address
---

## Holds Mass

Yes, three weekend Masses. Page 2 of the St. Catherine of Sienna bulletin for November 8, 2026 (`https://www.stcatherineofsienna.org/whats-happening/bulletin/48-november-8-2026/file`, read 2026-11-13, rendered) lists "Saturday ... 4:30 P.M. (Vigil Mass) - SCS Chapel" and "Sunday - SCS Chapel (in Sienna Center) 9:45 A.M., 1:00 P.M."; the issue's Mass intentions list those Masses under "Sienna Center". The parish home page ("Sunday: 9:45 AM and 1:00 PM at SCS Chapel / Sienna Center") and the drvc.org Mass-times page agree. It is a separate room from the church, with its own Masses, so it is its own row, as Albany's All Saints Parish Center Chapel is. No roster lists it as a place.

## Name and address

The name is the bulletin's and the home page's ("SCS Chapel", "Sienna Center"); two parish sources and the diocese's Mass-times page use it. The address is inferred, not read: no source checked gives the Sienna Center's street address. The parish office is at 990 Holzheimer Street (parish contact page), and OSM puts "Saint Catherine of Siena School, 990, Holzheimer Street" about 70 m west of the church; the Sienna Center, where the parish also holds its Mass Book sign-ups, is probably that building. Coordinates are that OSM node. `address_verified` stays false until a source names the address (see `revisit`).
