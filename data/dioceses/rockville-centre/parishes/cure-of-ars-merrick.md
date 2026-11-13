---
name: Curé of Ars
website: https://cureofarschurch.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://cureofarschurch.org/news/bulletin']
group: ''
evidence:
- url: https://cureofarschurch.org/news/bulletin/1206-november-8-2026-thirty-second-sunday-in-ordinary-time/file
  seen: 2026-11-13
  note: 'Page 1 of the 8 November 2026 issue, read as an image (24 pages; PDF Creator Affinity 3.3.3,
    the parish''s own layout; downloaded through Chrome with tools/browser_get.py; the text layer is garbled,
    so page 1 was rendered with render.py). Masthead: ''The Parish Family of Curé of Ars ... 2323 Merrick
    Avenue, Merrick, NY 11566 ... www.cureofarschurch.org''; Msgr. Francis J. Caldwell, Pastor. Mass Schedule:
    Saturday Vigil 4:00pm; Sunday 7:30 AM, 9:30 AM, 11:30 AM and 1:00 PM; every Monday 7:30pm; Tuesday-Friday
    9:00am. Adoration ''in the Divine Mercy Chapel''.'
- url: https://cureofarschurch.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py (probe url answers 403): newest first, 1206-november-8-2026-thirty-second-sunday-in-ordinary-time/file,
    1203-november-1-2026-all-saints-day/file, 1200-october-25-2026-...; 24 pages of weekly issues.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: ''No PDF
    links found on bulletin post page: .../1206-november-8-2026-thirty-second-sunday-in-ordinary-time/file''
    (the post is the PDF, which answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://cureofarschurch.org/news/bulletin/1206-november-8-2026-thirty-second-sunday-in-ordinary-time/file
---

## Publisher

Curé of Ars, 2323 Merrick Avenue, Merrick publishes its own weekly bulletin, laid out by the parish (PDF Creator "Affinity 3.3.3"; no printer's id or LPi/John Patrick marks). The 8 November 2026 issue (`https://cureofarschurch.org/news/bulletin/1206-november-8-2026-thirty-second-sunday-in-ordinary-time/file`, 24 pages, read 2026-11-13) has the page 1 masthead "The Parish Family of Curé of Ars ... 2323 Merrick Avenue, Merrick, NY 11566" and names Msgr. Francis J. Caldwell, Pastor. Its Mass Schedule: Saturday Vigil 4:00pm; Sunday 7:30 AM, 9:30 AM, 11:30 AM and 1:00 PM; every Monday 7:30pm; Tuesday-Friday 9:00am. The PDF's text layer is garbled (subset fonts), so page 1 was rendered and read as an image.

The drvc.org Mass-times page (roster `mass-times:church-of-cure-of-ars-merrick`) gives an older schedule (Saturday 5:00 pm, weekday 7:00 and 9:00 AM); the bulletin is followed.

## Worship sites

One: the church at 2323 Merrick Avenue (`cure-of-ars-merrick-church`). The bulletin's schedule names no other building; the "Divine Mercy Chapel" it mentions is where Adoration is held, with no Mass listed there. The diocesan locator (directory:6), GCatholic (16885) and the Mass-times page list only this church.

## Website and bulletin provider

The locator and GCatholic link cureofarschurch.net, which does not resolve; the Mass-times page and the masthead give cureofarschurch.org. It is a Solutio (Joomla) site: `/news/bulletin` lists the issues newest first, each a `/news/bulletin/<n>-<date>/file` PDF that answers 403 outside a browser (Chrome downloads it with tools/browser_get.py). No printer's listing exists, since the parish lays out the bulletin itself, so the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, following the diocese's rule for Solutio sites. `fetch:check` (2026-11-13) failed: "No PDF links found on bulletin post page".

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
