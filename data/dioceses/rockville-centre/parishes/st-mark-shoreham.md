---
name: St. Mark
website: https://stmarkshoreham.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stmarkshoreham.org/bulletin#st-mark']
group: ''
evidence:
- url: https://stmarkshoreham.org/bulletin/432-thirty-third-sunday-ot-november-15-2026/file
  seen: 2026-11-13
  quote: 105 Randall Rd., Shoreham, NY 11786
  note: '15 November 2026 issue (16 pages, Creator Microsoft Publisher 2021, downloaded in Chrome). Page
    1 masthead: ''St. Mark Parish, R.C.'', ''November 15th, 2026''; Mass Schedule: Monday - Saturday 9:30
    am; Saturday 4:00 pm; Sunday 9:30 am - 11:15 am (the Sunday times are drawn without a text layer;
    read from a render of page 1). Back page: ''#146 FOR ADVERTISING: THE CHURCH BULLETIN INC.''.'
- url: https://stmarkshoreham.org/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''Thirty-third Sunday
    OT, November 15, 2026'' -> /bulletin/432-thirty-third-sunday-ot-november-15-2026/file, then November
    8, November 1 ...'
research:
- method: pdftotext of the 15 November 2026 issue for a printer mark (4lpi.com, LPi footer, John Patrick);
    visit.py of the site for an embedded publisher
  url: https://stmarkshoreham.org/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (as provider other, unpinned) failed: ''No PDF
    links found on bulletin page: .../bulletin/390-bulletin-may-17-2026/file'' (it followed a May 2026
    /file link, not the newest; each /file link is the PDF, which Chrome downloads with tools/browser_get.py).
    Printed by The Church Bulletin Inc. (job #146), which posts no listing.'
  url: https://stmarkshoreham.org/bulletin/432-thirty-third-sunday-ot-november-15-2026/file
---

## Publisher

St. Mark, 105 Randall Road, Shoreham publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#146 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 15 November 2026 issue (`https://stmarkshoreham.org/bulletin/432-thirty-third-sunday-ot-november-15-2026/file`, downloaded in Chrome 2026-11-13; 16 pages, Microsoft Publisher 2021) has the page 1 masthead "St. Mark Parish, R.C.", "105 Randall Rd., Shoreham, NY 11786". No other parish is named; `group` is empty.

## Worship sites

One. Page 1's Mass Schedule ("Monday - Saturday: 9:30 am / Saturday: 4:00 pm / Sunday: 9:30 am - 11:15 am"; the Sunday times have no text layer and were read from a render of the page) names no second place, so all Masses are at the church (`st-mark-shoreham-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church.

## Website and bulletin provider

The diocese and GCatholic list stmarkshoreham.org (GCatholic also www.stmarkshoreham.com, which the bulletin prints too). It is a Solutio (Joomla) site (`probe url` gets 403; `visit.py` reads it); /bulletin lists issues newest first, each linking straight to its `/file` PDF. The printer posts no listing and the issue carries no LPi or John Patrick mark, so, following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

`fetch:check` (2026-11-13, as provider `other`) failed on a May 2026 `/file` link ("No PDF links found on bulletin page: .../390-bulletin-may-17-2026/file"), so a collector will also need to choose the newest post.

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` links.
