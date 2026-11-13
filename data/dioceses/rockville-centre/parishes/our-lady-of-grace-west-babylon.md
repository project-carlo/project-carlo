---
name: Our Lady of Grace
website: https://www.ourladyofgrace.net/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.ourladyofgrace.net/news/bulletin']
group: ''
evidence:
- url: https://www.ourladyofgrace.net/news/bulletin/181-november-8-2026/file
  seen: 2026-11-13
  quote: 666 Albin Avenue, West Babylon, New York 11704
  note: 'Page 1 masthead of the November 8th, 2026 issue names Our Lady of Grace Roman Catholic Church
    alone (downloaded through Chrome). We Celebrate the Eucharist: Vigil 5:00 pm Saturday; Sunday 8:00am,
    10:00am, 12:00 Noon; weekdays Monday-Friday 8:30am, Saturday 8:00am. Made in Canva by the parish;
    no printer.'
- url: https://www.ourladyofgrace.net/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py: 181-november-8-2026, 180-november-1-2026,
    178-october-25-2026, each linking /file, the PDF.'
research:
- method: 'Looked for a printer listing: the issue''s PDF metadata (Creator: Canva) and text name no printer,
    LPi or John Patrick'
  url: https://www.ourladyofgrace.net/news/bulletin/181-november-8-2026/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../181-november-8-2026/file" (the /file URL is the PDF and answers
    403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://www.ourladyofgrace.net/news/bulletin/181-november-8-2026/file
---

## Publisher

Our Lady of Grace, 666 Albin Avenue, West Babylon publishes its own weekly bulletin, a six-page Canva PDF with no printer. The November 8th, 2026 issue (`https://www.ourladyofgrace.net/news/bulletin/181-november-8-2026/file`, read 2026-11-13) has the masthead "Our Lady of Grace Roman Catholic Church" and one schedule: Saturday Vigil 5:00 pm; Sunday 8:00am, 10:00am and 12:00 Noon; weekdays Monday-Friday 8:30am and Saturday 8:00am.

The diocese's Mass-times page (2026-11-12) also lists weekday 8:00 and 9:00 AM and a Sunday 5:30 PM Mass; the current bulletin lists neither, and it is followed.

## Worship sites

One: the church at 666 Albin Avenue (`our-lady-of-grace-west-babylon-church`). The diocesan locator (directory:80), GCatholic (16930) and the Mass-times page list only this building; the bulletin's schedule names no other place.

## Website and bulletin provider

www.ourladyofgrace.net is a Solutio (Joomla) site. Its `/news/bulletin` list links `/news/bulletin/<n>-<month>-<d>-<yyyy>/file`, which answers 403 outside a browser; Chrome downloads it. The issue is parish-made (Canva), so there is no printer listing. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
