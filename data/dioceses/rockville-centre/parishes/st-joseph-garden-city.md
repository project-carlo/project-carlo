---
name: St. Joseph
website: https://stjosephchurchgc.org/
bulletin_provider: other
provider_id: page-pdfs https://stjosephchurchgc.org/bulletin/
publication: ['url:https://stjosephchurchgc.org/bulletin/#st-joseph-garden-city']
group: ''
evidence:
- url: https://stjosephchurchgc.org/wp-content/uploads/2026/11/20261115O.pdf
  seen: 2026-11-13
  quote: 130 Fifth Street Garden City, NY 11530
  note: 'Issue for November 15, 2026 (20 pages, Canva, downloaded with tools/browser_get.py). Page 1:
    ''Church of St. Joseph / GARDEN CITY, NEW YORK / NOVEMBER 15, 2026 / MASS TIMES / SUNDAY 7:30am, 9:00am,
    10:30am, 12:30pm, 5:30pm / Auditorium: 10:00am (mid-September to June) / MONDAY - FRIDAY 8:30am, 12:15pm
    in the Church / SATURDAY 8:30am, 5:00pm (Vigil Mass)''. No other church is named.'
- url: https://stjosephchurchgc.org/bulletin/
  seen: 2026-11-13
  note: 'WordPress Bulletin page (read with parish-site-access visit.py; probe url could not connect)
    links the 2026 issues newest first: 20261115O.pdf, 32nd-Sunday-in-Ordinary-Time-Nov-8th.pdf, 20261101O-1-1.pdf,
    20261025B.pdf ...'
bulletin_status: available
---

## Publisher

St. Joseph, Garden City publishes its own weekly bulletin (made in Canva) on its WordPress site. The newest issue on 2026-11-13, `https://stjosephchurchgc.org/wp-content/uploads/2026/11/20261115O.pdf` (20 pages), opens "Church of St. Joseph / GARDEN CITY, NEW YORK / NOVEMBER 15, 2026" with the Mass times: Sunday 7:30, 9:00, 10:30 AM, 12:30 and 5:30 PM, plus "Auditorium: 10:00am (mid-September to June)"; Monday-Friday 8:30 AM and 12:15 PM "in the Church"; Saturday 8:30 AM and 5:00 PM (Vigil). The page footer reads "130 Fifth Street Garden City, NY 11530".

## Worship sites

One: the church at 130 Fifth Street (`st-joseph-garden-city-church`). The seasonal 10:00 Sunday Mass in the Auditorium is taken to be in the parish's own hall on the same campus (inferred; the bulletin gives it no address). The diocesan locator (directory:50), GCatholic (16848) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

`probe url` and `probe get` could not connect ("Remote end closed connection"); the site loads in the browser (`visit.py`) and its PDFs download with `tools/browser_get.py`. The Bulletin page lists issues newest first under mixed filenames (`<yyyymmdd>O.pdf`, `<yyyymmdd>B.pdf`, sometimes a title such as `32nd-Sunday-in-Ordinary-Time-Nov-8th.pdf`), so the provider is `other` with `page-pdfs` on that page and no filename glob.

`fetch:check` (2026-11-13) with this recipe picked `20261115O.pdf` (url_date 2026-11-15), the newest issue.

## Not yet confirmed

Nothing open.
