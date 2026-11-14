---
name: Church of the Blessed Sacrament
website: https://www.bsvs.us/news-events/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.bsvs.us/news-events/bulletin']
group: ''
evidence:
- url: https://www.bsvs.us/news-events/bulletin/203-november-8-2026/file
  seen: 2026-11-12
  quote: 201 North Central Avenue
  note: Page 1 masthead of the 8 November 2026 issue (10 pages, downloaded in Chrome; pdfinfo Creator
    "Canva") names "Church of the Blessed Sacrament" alone, Pastor Rev. Lawrence Onyegu, 201 North Central
    Avenue, Valley Stream, New York 11580, with Mass Schedule Mon-Fri 9am, Saturday 8am, Saturday 5pm,
    Sunday 8am, 11am & 12:30pm (English), 9:30am (Spanish), 2:00pm (Nigerian-Igbo).
- url: https://www.bsvs.us/news-events/bulletin
  seen: 2026-11-12
  note: 'Solutio Bulletin page read in visit.py (probe url: 403): one /file link per Sunday, newest "November
    8, 2026" (203-november-8-2026/file), back through June 28, 2026 on the first page.'
research:
- method: pdfinfo of the 8 November 2026 issue and visit.py of bsvs.us for a printer (LPi, ParishesOnline,
    John Patrick)
  url: https://www.bsvs.us/news-events/bulletin
  checked: '2026-11-12'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-12
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-12 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../203-november-8-2026/file" (the /file link is the PDF, which
    Chrome downloads with tools/browser_get.py). The issue is made in Canva; no printer listing.'
  url: https://www.bsvs.us/news-events/bulletin/203-november-8-2026/file
---

## Publisher

Blessed Sacrament, 201 North Central Avenue, Valley Stream publishes its own weekly bulletin on its Solutio (Joomla) site. Page 1 of the 8 November 2026 issue (`https://www.bsvs.us/news-events/bulletin/203-november-8-2026/file`, 10 pages, made in Canva, downloaded in Chrome on 2026-11-12) has the masthead "Church of the Blessed Sacrament" alone, with the pastor, Rev. Lawrence Onyegu, and the address 201 North Central Avenue, Valley Stream, New York 11580. Its Mass Schedule: Mon-Fri 9am; Saturday 8am and 5pm; Sunday 8am, 11am and 12:30pm (English), 9:30am (Spanish) and 2:00pm (Nigerian-Igbo). This matches the drvc.org Mass-times page (read 2026-11-12).

## Worship sites

One: the church at 201 North Central Avenue (`blessed-sacrament-valley-stream-church`). The diocesan locator (directory:4), GCatholic (16926) and the Mass-times page list only this building, and the masthead gives the Masses with no other place.

## Website and bulletin provider

bsvs.us is the diocesan locator's link and loads in `visit.py` (`probe url`: 403). GCatholic's and the Mass-times page's blessedsacramentvs.org does not resolve (`probe url`, 2026-11-12). The Bulletin page lists one Solutio `/file` link per Sunday. `fetch:check` (2026-11-12) found the 8 November post and failed: "No PDF links found on bulletin post page". The PDF's metadata and the site show no printer, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish. The row goes live once a collector reads Solutio `/file` PDFs (see research).
