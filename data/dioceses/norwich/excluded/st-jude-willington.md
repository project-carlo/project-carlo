---
name: St. Jude
reason: closed
line1: 25 Old Farms Rd
city: Willington
state: CT
postal_code: 06279
decided: 2026-11-14
roster: ['directory:st-jude-willington', 'gcatholic:22323']
evidence:
- url: https://www.norwichdiocese.org/Portals/dioceseofnorwich/CMAdmin/Parishes_CCD9Mar26.pdf
  seen: 2026-11-14
  note: 'Listed in Diocese of Norwich List of Parishes (March 6, 2026) as ''St. Jude'', 25 Old Farms Rd.,
    Willington, Willington, CT; kind: Closed'
- url: https://gcatholic.org/churches/usa-01/22323
  seen: 2026-11-14
  quote: 25 Old Farms Rd., Willington, Connecticut 06279-0240
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Norwich as ''St. Jude'', 25 Old
    Farms Rd., Willington, CT, 06279; kind: Church'
- url: https://www.norwichdiocese.org/Portals/dioceseofnorwich/CMAdmin/Parishes_CCD9Mar26.pdf
  seen: 2026-11-14
  quote: 'Closed: For inquiries or records, contact St. Philip the Apostle, Ashford'
  note: St. Jude (Est. 1981), 25 Old Farms Rd., Willington entry.
- url: https://saintphilipct.com/index.php?gf-download=2026%2F11%2FBulletin-11-15-2026.pdf&form-id=4&field-id=7&hash=61b5e9f3111c570e7f63e7b68ac1e2b1b161255876b7bfda5929c2f26889b853
  seen: 2026-11-14
  note: The November 15, 2026 St. Philip bulletin schedules Mass only at St. Philip, 64 Pompey Hollow
    Rd., Ashford (pages 1 and 3); its text mentions Jude only in the email stphilipstjude@gmail.com.
- url: https://saintphilipct.com/contact-us/directions/
  seen: 2026-11-14
  quote: 25 Old Farms Road
  note: St. Philip's Directions page (footer © 2021) still lists 'S. Jude Church, 25 Old Farms Road, P.O.
    Box 240, W. Willington, CT 06279' with no Mass times; an old static page.
parish: st-philip-the-apostle-ashford
research:
- method: Grep older St. Philip bulletins (WordPress posts back to September 2019) for St. Jude's last
    Mass
  url: https://saintphilipct.com/category/bulletin/
  checked: '2026-11-14'
  outcome: access-blocked
  next_action: Open the Gravity Forms downloads of 2020-2025 issues in the browser (visit.py) or ask the
    parish office, and find the last issue scheduling Mass at St. Jude to set last_mass
  retry_when: A method that downloads older gf-download links (they answered HTTP 401 for issues of December
    2020, January 2023 and January 2025; October-November 2026 issues download)
---

## Why it is excluded

The diocese's List of Parishes (March 6, 2026) gives St. Jude, 25 Old Farms Rd., Willington as "Closed: For inquiries or records, contact St. Philip the Apostle, Ashford." The successor's current bulletin, St. Philip's November 15, 2026 issue, schedules Mass only at St. Philip, Ashford; it names Jude only in the parish email (stphilipstjude@gmail.com). Excluded as closed under the rule accepted for this diocese (survey-review, 2026-11-14).

Still naming it: GCatholic lists St. Jude as a church (website saintphilipsaintjude.org, which answers 403), and St. Philip's Directions page (footer © 2021) gives "S. Jude Church, 25 Old Farms Road ... W. Willington" without Mass times. Both are older than the diocese's list and the bulletin.

No source read dates the last Mass, so `last_mass` is empty. St. Philip's bulletin posts go back to September 2019, but issues before late 2026 answered HTTP 401 on 2026-11-14 (see research).

## What would change this

A St. Philip bulletin or the diocese listing a Mass at St. Jude, Willington. An older bulletin would date the last Mass.
