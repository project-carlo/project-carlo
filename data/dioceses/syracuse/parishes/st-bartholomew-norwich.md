---
name: Church of St. Bartholomew
website: https://www.stbartsnorwich.com/weekly-bulletin.html
bulletin_provider: other
provider_id: ''
publication: ['url:https://www.stbartsnorwich.com/weekly-bulletin.html']
group: Rev. Daniel Caughey (Norwich, Sherburne, New Berlin)
evidence:
- url: https://designrr.page/?id=519517&token=2260469323&type=FP&h=2374
  seen: 2026-09-26
  quote: Church of St. Bartholomew September 27, 2026
  note: 'The 27 September 2026 bulletin, the document the Weekly Bulletin page embeds (a Designrr flipbook,
    rendered with parish-site-access visit.py; a plain fetch returns only the title "27September2026").
    Page 1 gives "LORD''S DAY MASSES Saturday (Vigil) 4:00 p.m. (October-March) Sunday 8:30 a.m. WEEKDAY
    LITURGIES Mass: Tuesday and Thursday at 9:00 a.m." and "73 East Main, Norwich, NY 13815".'
- url: https://www.stbartsnorwich.com/weekly-bulletin.html
  seen: 2026-09-26
  quote: 'Weekly Bulletin Week of: September 27, 2026'
  note: The parish's bulletin page, with one Designrr link per issue in its archive (weekly from 4 January
    2026) and archive pages for 2021-2025.
- url: https://www.stbartsnorwich.com/
  seen: 2026-09-26
  quote: Saturday Masses begin again at St. Bartholomew's Church on October 3rd at 4 PM.
  note: The parish homepage (www.stbartsnorwichny.com redirects here). Pastor Rev. Daniel M. Caughey.
- url: https://www.syracusediocese.org/st-bartholomew-norwich
  seen: 2026-09-26
  quote: 'Website: stbartsnorwich.com'
  note: 'The diocese''s page (read with visit.py): church 73 East Main Street, office 30 Pleasant Street.'
---

## Publisher

St. Bartholomew's in Norwich publishes its own weekly bulletin. I read the 27 September 2026 issue
(rendered in a browser): page 1 is headed "Church of St. Bartholomew", gives only this church's
schedule (Sunday 8:30 am; Saturday 4 pm vigil October–March; Tuesday and Thursday 9 am) and its own
telephone and address, 73 East Main. It shares a pastor, Fr. Daniel Caughey, and an office address
(30 Pleasant Street) with St. Paul's, but St. Paul's bulletin is a different publication with its own
masthead, finances and intentions, so they are two rows. GCatholic's shared website for the two,
stpaulstbart.com, no longer resolves.

## Worship sites

One: St. Bartholomew's, 73 East Main Street (`churches/st-bartholomew-norwich.md`). The parish
center next door (81 East Main) houses religious education and the soup kitchen; it is not a worship
site.

## Website and bulletin provider

stbartsnorwich.com/weekly-bulletin.html shows the current issue in an embedded Designrr flipbook
(designrr.page/?id=…&token=…) and lists every 2026 issue as a Designrr link. There is no PDF: the
flipbook is rendered by JavaScript. Provider `other`, publication `url:` the bulletin page. The
directory's homepage stbartsnorwichny.com redirects to stbartsnorwich.com (the `REDIRECT-OFFSITE`
verdict in `probe url` is this rename, not a squat: same parish, same content).

## Not yet confirmed

Whether the pipeline's `other` fetcher can read a Designrr flipbook; if not, this row needs a
Designrr reader or a browser render, and should be flagged when promoted.
