---
name: Holy Name of Mary
website: https://www.hnomary.org/about-us/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.hnomary.org/about-us/bulletin']
group: ''
evidence:
- url: https://www.hnomary.org/about-us/bulletin/36-november-8-2026/file
  seen: 2026-11-12
  quote: 9:00am Parishioners of Holy Name of Mary
  note: 'The 8 November 2026 issue (13 pages, downloaded in Chrome; pdfinfo Creator "Microsoft Publisher
    for Microsoft 365") is Holy Name of Mary''s own: page 1 Mass intentions give weekdays 12:10pm (Mon-Thu)
    and 8:30am (Fri-Sat), Saturday 5:00pm, Sunday 15 November 7:45am, 9:00am, 11:00am and 1:00pm; page
    2 is the pastor''s letter "Blessed be the Holy Name of Mary!".'
- url: https://www.hnomary.org/about-us/bulletin
  seen: 2026-11-12
  note: 'Solutio Bulletin page read in visit.py (probe url: 403): one /file link per Sunday, newest "November
    8, 2026" (36-november-8-2026/file), then November 1, October 25 ... September 6, with more pages.'
research:
- method: pdfinfo of the 8 November 2026 issue and visit.py of hnomary.org for a printer (LPi, ParishesOnline,
    John Patrick)
  url: https://www.hnomary.org/about-us/bulletin
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
    links found on bulletin post page: .../36-november-8-2026/file" (the /file link is the PDF, which
    Chrome downloads with tools/browser_get.py). The issue is made in Microsoft Publisher; no printer
    listing.'
  url: https://www.hnomary.org/about-us/bulletin/36-november-8-2026/file
---

## Publisher

Holy Name of Mary, 55 East Jamaica Avenue, Valley Stream publishes its own weekly bulletin on its Solutio (Joomla) site. The 8 November 2026 issue (`https://www.hnomary.org/about-us/bulletin/36-november-8-2026/file`, 13 pages, downloaded in Chrome on 2026-11-12) is made in Microsoft Publisher. Page 1 lists the week's Mass intentions: Monday-Thursday at 12:10pm, Friday and Saturday at 8:30am, Saturday at 5:00pm, and Sunday 15 November at 7:45am, 9:00am ("Parishioners of Holy Name of Mary"), 11:00am and 1:00pm (Fr. Gustavo, the Spanish Mass hour on the drvc.org Mass-times page). Page 2 is the pastor's letter, "Blessed be the Holy Name of Mary!". The issue names no other parish.

## Worship sites

One: the church at 55 East Jamaica Avenue (`holy-name-of-mary-valley-stream-church`). The diocesan locator (directory:9), GCatholic (16927) and the Mass-times page list only this building, and the issue gives no other place of Mass.

## Website and bulletin provider

hnomary.org is the diocesan locator's link and loads in `visit.py` (`probe url`: 403). GCatholic's and the Mass-times page's hnom.org did not answer (`probe url` timeout, 2026-11-12). The Bulletin page lists one Solutio `/file` link per Sunday. `fetch:check` (2026-11-12) found the 8 November post and failed: "No PDF links found on bulletin post page". The PDF's metadata and the site show no printer, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish. The row goes live once a collector reads Solutio `/file` PDFs (see research).
