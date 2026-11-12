---
name: St. Joseph
website: https://stjoseph-nj.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1493
publication: ['url:http://sponsors.bonventure.net/?page=1493']
group: ''
evidence:
- url: https://stjoseph-nj.org/
  seen: 2026-11-04
  note: Read with parish-site-access visit.py (probe url gets 403). eCatholic site 24657 (the finder pin
    id); its Bulletins menu link is http://sponsors.bonventure.net/?page=1493, not an eCatholic bulletins/
    archive.
- url: http://sponsors.bonventure.net/?page=1493
  seen: 2026-11-04
  quote: 454 Germantown Road
  note: Bon Venture sponsor page 'St. Joseph Church, 454 Germantown Road, West Milford, NJ 07480'; probe
    url lists the newest issue http://sponsors.bonventure.net/pdfs/1493/2026-11-08.pdf.
- url: http://sponsors.bonventure.net/pdfs/1493/2026-11-08.pdf
  seen: 2026-11-04
  note: 'Garbled text layer; pages 1-2 rendered with render.py. Page 1 masthead: ''NOVEMBER 8, 2026'',
    ''ST. JOSEPH CHURCH'', ''THE OLDEST CATHOLIC PARISH IN NEW JERSEY!'', ''454 Germantown Road, West
    Milford, NJ 07480''. Page 2: ''Fr. Jakub Grzybowski, Pastor''; MASS TIMES: Monday, Wednesday & Friday
    6:00pm; Tuesday & Thursday 9:00am; Saturday 9:00am, 5:00pm (Vigil Mass); Sunday 8:00am, 10:00am, 12:00
    pm. No other worship site named.'
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

St. Joseph, West Milford publishes its own weekly bulletin through Bon Venture, which posts it on sponsor page 1493 (`http://sponsors.bonventure.net/?page=1493`). The newest on 4 November 2026 is the 8 November 2026 issue (`http://sponsors.bonventure.net/pdfs/1493/2026-11-08.pdf`, 12 pages). Its text layer is garbled, so pages 1-2 were rendered: page 1 reads "NOVEMBER 8, 2026", "ST. JOSEPH CHURCH", "THE OLDEST CATHOLIC PARISH IN NEW JERSEY!", "454 Germantown Road, West Milford, NJ 07480"; page 2 names Fr. Jakub Grzybowski, Pastor.

## Worship sites

- `st-joseph-west-milford`: the only church. Page 2's MASS TIMES (8 November 2026) give Monday, Wednesday & Friday 6:00pm; Tuesday & Thursday 9:00am; Saturday 9:00am and 5:00pm (Vigil Mass); Sunday 8:00am, 10:00am, 12:00pm, and name no other place.

The finder (directory:24657) and GCatholic (18986) each list this one church.

## Website and bulletin provider

The parish site `stjoseph-nj.org` is eCatholic site 24657 behind Cloudflare (read with visit.py on 2026-11-04). Its Bulletins link goes to the Bon Venture sponsor page, so the row is `other` with a page-pdfs recipe on that page (as for the diocese's other Bon Venture rows); fetch:check on 2026-11-04 picked the 8 November 2026 issue.

## Not yet confirmed

Nothing open. The cover's image-only masthead means fetch:check can't verify identity from text; the rendered page 1 does.
