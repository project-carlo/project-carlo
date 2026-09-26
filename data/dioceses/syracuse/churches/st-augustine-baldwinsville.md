---
parish: st-augustine-baldwinsville
name: St. Augustine's Church
line1: 7333 O'Brien Rd.
line2: ''
city: Baldwinsville
state: NY
postal_code: '13027'
latitude: 43.1251875
longitude: -76.3003125
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: true
roster: ['gcatholic:17984', 'directory:33098']
evidence:
- url: https://container.parishesonline.com/bulletins/06/0074/20260927B.pdf
  seen: 2026-09-26
  quote: 'St. Augustine’s Weekend Masses Sunday: 10:30 AM'
  note: 'Text quote from the St. Mary of the Assumption bulletin of 27 September 2026 (page 1), which prints
    the three Baldwinsville parishes'' schedules; St. Augustine''s own bulletin (04/0667) gives the same
    on page 2, but that page is an image (see the note below).'
- url: https://container.parishesonline.com/bulletins/04/0667/20260927B.pdf
  seen: 2026-09-26
  note: 'St. Augustine''s own bulletin, 27 September 2026, read as rendered images (pages 1-6 have no text
    layer): page 1 "St. Augustine’s Church", "7333 O’Brien Road, Baldwinsville, New York 13027"; page 2
    "Mass Times", St. Augustine''s: Weekend Mass Sunday 10:30am, Weekday Mass Wednesday 10:00am.'
- url: https://www.openstreetmap.org/node/357583861
  seen: 2026-09-26
  note: 'OSM place_of_worship "Saint Augustines Church" on Obrien Road, 13027 (Nominatim reverse lookup
    of the GCatholic Plus Code); no house number.'
- url: https://gcatholic.org/churches/usa-02/17984
  seen: 2026-09-25
  quote: 7333 O’Brien Rd., Baldwinsville, New York 13027-9134
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Syracuse as ''St. Augustine'',
    7333 O’Brien Rd., Baldwinsville, NY, 13027; kind: Church'
- url: https://www.syracusediocese.org/parishfinder
  seen: 2026-09-26
  note: Listed in Diocese of Syracuse parish finder (Mass-times map) as 'St. Augustine', 7333 O'Brien
    Road, Baldwinsville, NY, 13027-9532
---

## Holds Mass

Yes, weekly. St. Augustine's bulletin of 27 September 2026 (page 2, an image) gives Sunday
10:30am and Wednesday 10:00am here; the St. Mary of the Assumption bulletin of the same date and
the joint schedule on bvillecatholic.org give the same times.

## Name and address

The parish's bulletin masthead ("7333 O’Brien Road, Baldwinsville, New York 13027"), its
ParishesOnline organization, GCatholic and the diocese's finder all give 7333 O'Brien Road, and
OSM has the church on O'Brien Road (no number), so `address_verified` is true. The postal town
is Baldwinsville; OSM puts it in Seneca Knolls, Town of Van Buren. The name is "St. Augustine’s
Church" in the bulletin masthead, "St. Augustine" in GCatholic and the diocese, "Saint Augustines
Church" in OSM: `name_verified` is true. Coordinates are GCatholic's Plus Code, decoded, which
lands on the OSM church node.
