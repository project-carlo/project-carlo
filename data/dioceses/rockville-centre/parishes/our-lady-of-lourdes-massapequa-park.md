---
name: Our Lady of Lourdes
website: https://ourladyoflourdesmp.org/bulletins
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://ourladyoflourdesmp.org/bulletins']
group: ''
evidence:
- url: https://ourladyoflourdesmp.org/bulletins/176-november-15-2026/file
  seen: 2026-11-13
  quote: OUR LADY OF LOURDES PARISH
  note: 'Page 2 header of the November 15, 2026 issue (downloaded through Chrome; probe get answers 403).
    Mass Times: Monday through Friday 8:00 A.M.; Saturday 8:00 A.M and 5:00 P.M.; Sunday 7:30, 9:00, 10:30
    A.M., 12:30 P.M. Made in InDesign; the back page reads #209 FOR ADVERTISING: THE CHURCH BULLETIN INC.,
    W. BABYLON.'
- url: https://ourladyoflourdesmp.org/bulletins
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py: 176-november-15-2026, 175-november-8-2026,
    174-november-1-2026, each linking /file, the PDF.'
- url: https://www.thechurchbulletininc.com/html/weekly_bulletins.html
  seen: 2026-11-13
  note: 'The printer''s Weekly Bulletins page has only its navigation menu: no parish listing or issue
    links to collect instead.'
research:
- method: Looked for the printer's online listing (The Church Bulletin Inc., West Babylon, named on the
    issue's back page)
  url: https://www.thechurchbulletininc.com/html/weekly_bulletins.html
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 15 November post but failed: "No PDF
    links found on bulletin post page: .../176-november-15-2026/file" (the /file URL is the PDF and answers
    403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://ourladyoflourdesmp.org/bulletins/176-november-15-2026/file
---

## Publisher

Our Lady of Lourdes, 855 Carmans Road, Massapequa Park publishes its own weekly bulletin, laid out in InDesign by the parish and printed by The Church Bulletin Inc. of West Babylon (back page: "#209 FOR ADVERTISING: THE CHURCH BULLETIN INC."). The November 15, 2026 issue (`https://ourladyoflourdesmp.org/bulletins/176-november-15-2026/file`, read 2026-11-13) heads each page "OUR LADY OF LOURDES PARISH"; page 2 gives one Mass schedule: Monday-Friday 8:00 A.M.; Saturday 8:00 A.M. and 5:00 P.M.; Sunday 7:30, 9:00, 10:30 A.M. and 12:30 P.M. Page 1's text layer is garbled (subset fonts); it decodes to "Our Lady of Lourdes Roman Catholic Church - Massapequa Park NY".

The diocese's Mass-times page (2026-11-12) gives a Wednesday 8:00 PM Mass and no Sunday 12:30; the bulletin is the parish's current word and is followed.

## Worship sites

One: the church at 855 Carmans Road (`our-lady-of-lourdes-massapequa-park-church`). The diocesan locator (directory:20), GCatholic (16881) and the Mass-times page list only this building; the bulletin's schedule names no other place. The "Chapel" on page 4 holds the sanctuary candle, inside the parish; no separate Mass site is named.

## Website and bulletin provider

The locator's ollmp.org redirects to https://ourladyoflourdesmp.org/ (visit.py, 2026-11-13), a Solutio (Joomla) site. Its `/bulletins` list links `/bulletins/<n>-<month>-<d>-<yyyy>/file`, which answers 403 to `probe get`; Chrome downloads it. The printer's site has no online bulletins. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
