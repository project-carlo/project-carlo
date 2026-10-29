---
parish: blessed-virgin-mary-darby
name: St. Louis Church
line1: W Cobbs Creek Pkwy
line2: ''
city: Yeadon
state: PA
postal_code: '19050'
latitude: 39.9340625
longitude: -75.2451875
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:19267', 'worship-sites:st-louis-yeadon']
evidence:
- url: https://container.parishesonline.com/bulletins/04/0756/20261025B.pdf
  seen: 2026-10-28
  note: '25 October 2026 BVM bulletin (image pages, page 1 rendered), Eucharistic Liturgy box: ''Sundays:
    9:30 AM St. Louis, Yeadon''. No street address for St. Louis appears on page 1.'
- url: https://www.bvm-darby.com/
  seen: 2026-10-28
  note: 'BVM home page Mass Schedule: ''Sunday: 9:30 am mass at St. Louis''; ''Weekday Mass ... No daily
    at St. Louis''.'
- url: https://archphila.org/parish/st-louis-yeadon/
  seen: 2026-10-28
  quote: Worship site for Blessed Virgin Mary Parish, Darby.
  note: 'Closed-parish page ''St. Louis (1928-2013)'': address ''W. Cobbs Creek Pkwy., Yeadon'', ''Spiritual
    records are kept at Blessed Virgin Mary Church, Darby'', ''Mass Times: Sundays, 9:30 AM''; page updated
    7 years ago. The Sunday 9:30 time agrees with the current bulletin.'
- url: https://gcatholic.org/churches/usa-03/19267
  seen: 2026-10-28
  quote: W Cobbs Creek Pkwy., Yeadon, Pennsylvania 19050
  note: GCatholic 'St. Louis', first recorded 1928.10, phone +1 (610) 623-0553, Plus Code 87F6WQM3+JW
    (39.93406, -75.24519). It is not marked closed.
research:
- method: Nominatim place search (4 phrasings of St. Louis Church, Yeadon / Cobbs Creek Parkway) and a
    bounded viewbox search for 'church' around 39.934,-75.245; GCatholic page and directory page read
  checked: '2026-10-28'
  outcome: not-found
  next_action: Find the church's street number from a parish page or a bulletin line that prints it, or
    an OSM node, and set address_verified once two sources agree
  retry_when: OSM maps the church or a BVM bulletin issue prints St. Louis's address
---

## Holds Mass

Yes, one Sunday Mass. The 25 October 2026 bulletin of Blessed Virgin Mary Parish (page 1, image, rendered) lists 'Sundays: 9:30 AM St. Louis, Yeadon'; the parish's own home page says 'Sunday: 9:30 am mass at St. Louis' and 'No daily at St. Louis'. St. Louis Parish (1928-2013) merged into Blessed Virgin Mary; the directory names the church a worship site of BVM, and GCatholic lists it without a closure note. It has no bulletin of its own and no John Patrick or ParishesOnline listing, so it is a church row under BVM's bulletin.

## Name and address

Name agreed by the bulletin, the BVM site, the directory and GCatholic. The street number is not given by any source read: the directory has 'W. Cobbs Creek Pkwy., Yeadon' and GCatholic 'W Cobbs Creek Pkwy., Yeadon, Pennsylvania 19050' (the ZIP is GCatholic's alone). Nominatim found no church by name (several queries, 2026-10-28), so `address_verified` stays false. Coordinates are GCatholic's Plus Code 87F6WQM3+JW. A later pass could read a street number from the church's own page or a bulletin line, which the BVM bulletin doesn't print.
