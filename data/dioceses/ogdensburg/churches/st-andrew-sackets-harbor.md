---
parish: eastern-lake-ontario-catholics
name: St. Andrew's Church
line1: 107 Woolsey Street
line2: ''
city: Sackets Harbor
state: NY
postal_code: '13685'
latitude: 43.9450625
longitude: -76.1173125
coordinates_from: gcatholic-plus-code
name_verified: true
address_verified: false
roster: ['gcatholic:18245', 'directory:sackets-harbor']
evidence:
- url: https://gcatholic.org/churches/usa-02/18245
  seen: 2026-09-30
  quote: 200 E Main St., Sackets Harbor, New York 13685
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Ogdensburg as ''St. Andrew'',
    200 E Main St., Sackets Harbor, NY, 13685; kind: Church'
- url: https://www.rcdony.org/parish/sackets-harbor
  seen: 2026-09-30
  note: Listed in Diocese of Ogdensburg parish directory as "St. Andrew's Church", 107 Woolsey Street,
    Sackets Harbor, NY, 13685
- url: https://container.parishesonline.com/bulletins/03/1493/20260927B.pdf
  seen: 2026-09-30
  quote: St. Andrew's 107 Woolsey Street Sackets Harbor, NY 13685
  note: Masthead, page 1, 27 September 2026 issue.
- url: https://container.parishesonline.com/bulletins/03/1493/20260927B.pdf
  seen: 2026-09-30
  quote: 10:30 am (SA)
  note: 'Page 2, liturgy schedule: Sunday 10:30 am (SA = St. Andrews in Sackets Harbor) and Thursday 8:30
    am (1 October). Page 3: "Weekly Coffee Hour after 10:30 Mass" and a food pantry Thursdays 11am-1pm.'
- url: https://nominatim.openstreetmap.org/search?format=jsonv2&q=107+Woolsey+Street,+Sackets+Harbor,+NY
  seen: 2026-09-30
  note: Nominatim knows both "107, Woolsey Street" and "200, East Main Street" in Sackets Harbor (43.9452,
    -76.1177 and 43.94516, -76.11736), both within about 40 m of the GCatholic Plus Code point, so they
    are probably two addresses of one corner building; nothing in OSM says which is the church.
---

## Holds Mass

Yes. The 27 September 2026 Eastern Lake Ontario Catholics bulletin (page 2, key "SA = St. Andrews
in Sackets Harbor") lists Sunday 10:30 am and Thursday 8:30 am, repeated for 3-4 October; page 3
announces a coffee hour after the 10:30 Mass and page 5 confessions after the 10:30 Mass on the
first Sunday of the month. The parish site's "Normal Mass Schedule" agrees.

## Name and address

**Disagreement on the street.** The bulletin masthead and the diocese's directory say 107 Woolsey
Street; GCatholic says 200 E Main St. (its website field, saintandrewsackets.org, is a dead domain).
OpenStreetMap has an address point for each within about 40 m of GCatholic's Plus Code, so they are
probably two street addresses of one building on the corner of Woolsey and East Main, but I could not
confirm that. I followed the bulletin and the directory (107 Woolsey), kept GCatholic's Plus Code
coordinates, and left `address_verified` false. `name_verified` is true (bulletin, directory,
GCatholic).
