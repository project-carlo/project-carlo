---
parish: st-malachy-sherburne
name: St. Malachy
line1: 29 East State Street
line2: ''
city: Sherburne
state: NY
postal_code: '13460'
latitude: 42.6784375
longitude: -75.4964375
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:18024', 'directory:33153']
evidence:
- url: https://gcatholic.org/churches/usa-02/18024
  seen: 2026-09-25
  quote: 31 E State St., Sherburne, New York 13460-0722
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''St. Malachy'', 31
    E State St., Sherburne, NY, 13460; kind: Church'
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: Listed in Diocese of Syracuse parish finder (Mass-times map) as 'St. Malachy', 31 East State Street,
    Sherburne, NY, 13460-0722
- url: https://www.stmalachysherburne.com/wp-content/uploads/2026/09/Sept-20-2026.pdf
  seen: 2026-09-26
  quote: ROMAN CATHOLIC CHURCH 29 East State Street Sherburne, NY … Saturday Vigil – 4:00 PM Sunday –
    8:30 AM Friday – 9:00 AM … Parish Office Hours at 31 East State Street
  note: Page 1 of the 19/20 September 2026 bulletin. Page 2 lists the Saturday 4:00 pm and Sunday 8:30
    am Masses of 19/20 September.
- url: https://www.syracusediocese.org/st-malachy-sherburne
  seen: 2026-09-26
  quote: Physical Address ​31 East State Street Sherburne, NY 13460
  note: The diocese's page (read with visit.py).
- url: https://www.openstreetmap.org/node/357643610
  seen: 2026-09-26
  note: OSM place_of_worship "Saint Malachy's Roman Catholic Church", Sherburne 13460, tagged with Classic
    Street (the old GNIS point, on the same block as GCatholic's Plus Code).
promoted: 2026-09-26
---

## Holds Mass

Yes, weekly. The 19/20 September 2026 bulletin gives Saturday Vigil 4 pm, Sunday 8:30 am and Friday
9 am, and its page-2 schedule lists the weekend's Masses.

## Name and address

The name is agreed (GCatholic "St. Malachy", diocese, bulletin "St. Malachy of Armagh", OSM), so
`name_verified` is true. **The street number is disputed.** The parish's own bulletin gives the church
as "29 East State Street" and, separately, "Parish Office Hours at 31 East State Street". GCatholic
(31 E State St.), the diocese's finder (31 East State Street) and its parish page ("Physical Address
31 East State Street") all give 31, which looks like the office's number. I followed the bulletin,
which distinguishes the two buildings, so `line1` is 29 East State Street; `address_verified` stays
false until an independent source (OSM, county records) gives the church's number. Coordinates are
GCatholic's Plus Code, which falls on the church block either way.
