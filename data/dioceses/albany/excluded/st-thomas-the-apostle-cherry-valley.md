---
name: St. Thomas the Apostle Church
reason: no-bulletin
line1: 1 Church St.
city: Cherry Valley
state: NY
postal_code: '13320'
decided: 2026-09-28
roster: ['gcatholic:18151', 'directory:311']
evidence:
- url: https://stthomascv.com/
  seen: 2026-09-28
  quote: Sunday Mass 10:00 AM
  note: 'The parish''s own site (home page): "Mass & Confession Sunday Mass 10:00 AM Confession Half-hour
    before Mass"; church at 1 Church St., Cherry Valley, NY 13320-3569; Kateri Hall at 13 Church St. Undated.'
- url: https://stthomascv.com/bulletin-full.html
  seen: 2026-09-28
  quote: 5th Sunday of Easter — May 3rd, 2026
  note: 'The site''s only bulletin: an HTML page built from data embedded in the page (window.STTHOMAS_BULLETINFULL_FALLBACK),
    "updated_at":"2026-05-03". Rendered in a browser (visit.py) it shows "Updated: 2026-05-03". No PDF;
    the data/bulletin_full.json file app.js asks for answers 404. Its Mass Schedule section: "Sunday:
    10:00 AM"; "May 3rd Prayer Service being held in absence of a priest."'
- url: https://parishesonline.com/organization/st-thomas-the-apostle-church-13320
  seen: 2026-09-28
  note: 'ParishesOnline organization "St. Thomas the Apostle Church" (LPi 0018000000Qx7OgAAJ), 24 Maple
    Ave, Cherry Valley: probe po reports no publications.'
- url: https://discovermass.com/church/st-thomas-the-apostle-cherry-valley-ny/
  seen: 2026-09-28
  note: 'Discover Mass listing: no bulletins listed (issues.py).'
- url: https://gcatholic.org/churches/usa-02/18151
  seen: 2026-09-28
  quote: 1 Church St., Cherry Valley, New York 13320
  note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Albany as ''St. Thomas the Apostle'',
    1 Church St., Cherry Valley, NY, 13320; kind: Church'
- url: https://www.rcda.org/parishes/parish/st-thomas-apostle-church-cherry-valley-ny
  seen: 2026-09-28
  note: Listed in Diocese of Albany Find A Parish list as 'St. Thomas the Apostle Church', 1 Church St.,
    Cherry Valley, NY, 13320
revisit: Check stthomascv.com/bulletin-full.html (its 'Updated:' date) and ParishesOnline org st-thomas-the-apostle-church-13320
  for a current bulletin; if either is kept up weekly, make this a parish row with the church.
revisit_after: 2027-01-15
---

## Why it is excluded

St. Thomas the Apostle, Cherry Valley is open: its own site's home page (read 2026-09-28) gives
"Sunday Mass 10:00 AM" at 1 Church Street, and the diocese's directory gives the same Sunday
10:00 am Mass. It is excluded only because it publishes nothing current the pipeline could
read (`no-bulletin`, not `closed`):

- The site's "Bulletin" is an HTML page, not a PDF, and it has not changed since the 3 May 2026
  issue ("5th Sunday of Easter — May 3rd, 2026", "Updated: 2026-05-03"), five months stale.
- Its ParishesOnline organization (st-thomas-the-apostle-church-13320) has no publications, and
  its Discover Mass listing has no bulletins.
- St. Joseph the Worker, Richfield Springs (whose deacon, Richard Brown, also writes for the
  Cherry Valley page, and whose prayer list shares names with it) does not mention Cherry
  Valley in its 27 September 2026 bulletin (grep for "Cherry", "Thomas", "Sharon": none).

The 3 May page also notes a Sunday "Prayer Service being held in absence of a priest", so Mass
here may not be every week; the directory and home page still say it is.

The institutional-records index says the records of St. Mary's, Sharon Springs are held here;
that building is in no roster.

## What would change this

A bulletin kept current on the site (weekly "Updated" dates) or on ParishesOnline: then this
becomes a parish row (`bulletin_provider: other` or `parishes_online`) with the church. See
`revisit`.
