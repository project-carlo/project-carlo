---
name: St. Joseph
website: https://stjosephsbabylon.org/news-events/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stjosephsbabylon.org/news-events/bulletin']
group: ''
evidence:
- url: https://stjosephsbabylon.org/news-events/bulletin/420-november-8-2026/file
  seen: 2026-11-13
  quote: St. Joseph Roman Catholic Church
  note: 'Page 1 masthead of the November 8, 2026 issue names St. Joseph Roman Catholic Church, 39 North
    Carll Avenue, Babylon alone (downloaded through Chrome). Masses: Monday - Saturday 8:00 AM; Saturday
    5:00 PM Vigil; Sunday 7:00 AM, 9:00 AM, 10:30 AM, 12:00 PM, 10:00 AM (Spanish) in Nolan Hall. Printed
    by The Church Bulletin Inc., West Babylon (#198); Creator Acrobat PDFMaker for Word.'
- url: https://stjosephsbabylon.org/news-events/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py: 420-november-8-2026, 419-november-1-2026,
    418-november-25-2026 (labelled October 25, 2026), each linking /file, the PDF.'
research:
- method: 'Looked for a printer listing: the issue''s back page names The Church Bulletin Inc., West Babylon
    (#198), which posts no bulletins online (playbook); PDF metadata Creator Acrobat PDFMaker for Word;
    no LPi or John Patrick id in the text'
  url: https://stjosephsbabylon.org/news-events/bulletin/420-november-8-2026/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../420-november-8-2026/file" (the /file URL is the PDF and answers
    403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://stjosephsbabylon.org/news-events/bulletin/420-november-8-2026/file
---

## Publisher

St. Joseph, 39 North Carll Avenue, Babylon publishes its own weekly bulletin, printed with advertising by The Church Bulletin Inc. of West Babylon (back page "#198 FOR ADVERTISING: THE CHURCH BULLETIN INC."). The November 8, 2026 issue (`https://stjosephsbabylon.org/news-events/bulletin/420-november-8-2026/file`, 16 pages, read 2026-11-13) has the masthead "St. Joseph Roman Catholic Church" and one schedule: Monday-Saturday 8:00 AM; Saturday 5:00 PM Vigil; Sunday 7:00 AM, 9:00 AM, 10:30 AM and 12:00 PM, and 10:00 AM in Spanish in Nolan Hall (the home page says the O'Connell Room).

## Worship sites

One: the church at 39 North Carll Avenue (`st-joseph-babylon-church`); Nolan Hall and the Adoration Chapel are rooms of the parish plant, not separate sites. The diocese's Mass-times page (2026-11-12) also lists an "Oak Beach Mission Church (St. Joseph parish mission church)", linked to this parish's site. Neither the 8 November issue, the summer issues of 28 June and 2 August 2026, the parish home page nor a site search for "oak beach" (0 results) mentions it, and the Mass-times entry's schedule (weekday 9:00 and 11:30 AM, eight Sunday Masses with "Chapel" and "Youth Mass") cannot be a beach chapel's; it is in `open/` as `oak-beach-mission-church` until a summer bulletin settles it.

## Website and bulletin provider

stjosephsbabylon.org is a Solutio (Joomla) site; its `/news-events/bulletin` list links `/news-events/bulletin/<n>-<month>-<d>-<yyyy>/file`, which answers 403 outside a browser while Chrome downloads it. The printer posts nothing online, so there is no listing to collect from. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Whether the Oak Beach mission still has summer Mass (see `open/oak-beach-mission-church`). When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
