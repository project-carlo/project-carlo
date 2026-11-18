---
name: St. Thomas More
reason: closed
line1: 87 Mystic Rd.
city: North Stonington
state: CT
postal_code: 06359
decided: 2026-11-14
roster: ['directory:st-thomas-more-north-stonington', 'gcatholic:22327', 'locator-map:saint-thomas-more-church-north-stonington']
evidence:
- url: https://www.norwichdiocese.org/Portals/dioceseofnorwich/CMAdmin/Parishes_CCD9Mar26.pdf
  seen: 2026-11-14
  quote: 'CLOSED: For inquiries or records, contact St. Michael, Pawcatuck'
  note: St. Thomas More (Est. 1967), 87 Mystic Rd., 06359-1514 entry of the Diocese of Norwich List of
    Parishes (March 6, 2026).
- url: https://container.parishesonline.com/bulletins/04/0504/20261115B.pdf
  seen: 2026-11-14
  note: The November 15, 2026 Holy Cross Community bulletin (St. Michael, St. Mary, St. Patrick) schedules
    Mass only at St. Michael, St. Mary and St. Patrick; grep 'Thomas More' finds nothing in its 12 pages.
- url: https://gcatholic.org/churches/usa-01/22327
  seen: 2026-11-14
  note: GCatholic still lists 'St. Thomas More', 87 Mystic Rd., North Stonington, as a church, with no
    closure.
- url: https://www.google.com/maps/d/viewer?mid=1VTpfhm6bXf8ZfwM_tX0Ikl--m9E8l7a5
  seen: 2026-11-14
  note: The diocese's older locator map still lists 'Saint Thomas More Church', 87 Mystic Road, yoked
    with St. Mary and St. Michael, linking parishesonline.com/find/st-thomas-more-church; probe po of
    that slug found no organization.
parish: holy-cross-community-stonington
---

## Why it is excluded

The diocese's List of Parishes (March 6, 2026) gives "St. Thomas More (Est. 1967), 87 Mystic Rd. ... CLOSED: For inquiries or records, contact St. Michael, Pawcatuck". The successor's current bulletin (Holy Cross Community, container 04/0504, November 15, 2026) lists Mass at St. Michael, St. Mary and St. Patrick and doesn't name St. Thomas More. This applies the diocese's accepted rule for churches the list marks closed. No source dates the last Mass, so `last_mass` is empty. GCatholic and the older locator map still list it, without Mass times.

## What would change this

A Holy Cross Community bulletin or St. Michael's site scheduling a Mass at 87 Mystic Road. A dated last Mass, from an older 04/0504 issue or a diocesan notice, would fill `last_mass`.
