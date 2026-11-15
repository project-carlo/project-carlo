---
name: St. John the Evangelist
website: https://saintjohnriverhead.org/news-events/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://saintjohnriverhead.org/news-events/bulletin#st-john-the-evangelist']
group: ''
evidence:
- url: https://saintjohnriverhead.org/news-events/bulletin/249-november-15-2026/file
  seen: 2026-11-13
  quote: 546 St. John’s Place Riverhead, NY 11901
  note: '15 November 2026 issue (8 pages, Adobe Acrobat, downloaded in Chrome; no advertisers and no printer
    mark). Page 1 masthead: ''St. John the Evangelist R.C. Church''; Pastor Fr. Gonzalo Oajaca Lopez.
    MASS SCHEDULE: Saturday 4:30 PM; Sunday 7:00, 9:00, 11:00 AM; 6:00 PM in Spanish; Monday, Wednesday
    & Thursday 8:00 AM; Tuesday & Friday 12:10 PM.'
- url: https://saintjohnriverhead.org/news-events/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list (visit.py; probe url gets 403): newest first, ''pdf November 15,
    2026'' -> /news-events/bulletin/249-november-15-2026/file, then November 8, November 1 ...'
research:
- method: pdftotext of the 15 November 2026 issue for a printer mark (4lpi.com, LPi footer, John Patrick,
    Church Bulletin Inc.); visit.py of the site for an embedded publisher
  url: https://saintjohnriverhead.org/news-events/bulletin
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set a real provider once a collector reads Solutio /file PDFs (joomla-file-endpoint), then
    run fetch:check
  retry_when: fetch gains a collector for Solutio /file links
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (as provider other, unpinned) found the 15 November
    post and failed: ''No PDF links found on bulletin post page: .../249-november-15-2026/file'' (the
    /file link is the PDF, which Chrome downloads with tools/browser_get.py). The bulletin is parish-made
    (no printer), so there is no other listing.'
  url: https://saintjohnriverhead.org/news-events/bulletin/249-november-15-2026/file
---

## Publisher

St. John the Evangelist, 546 St. John's Place, Riverhead publishes its own weekly bulletin, made in-house (8 pages, no advertisers, no printer's mark). The 15 November 2026 issue (`https://saintjohnriverhead.org/news-events/bulletin/249-november-15-2026/file`, downloaded in Chrome 2026-11-13; Adobe Acrobat, text layer readable) has the page 1 masthead "St. John the Evangelist R.C. Church, 546 St. John’s Place Riverhead, NY 11901" and names Fr. Gonzalo Oajaca Lopez, Pastor. No other parish is named; `group` is empty. St. Isidore, Riverhead, publishes its own bulletin on its own site (`st-isidore-riverhead`).

## Worship sites

One. The masthead's "MASS SCHEDULE - EUCHARIST" (Saturday 4:30 PM; Sunday 7:00, 9:00, 11:00 AM and 6:00 PM in Spanish; Monday, Wednesday and Thursday 8:00 AM; Tuesday and Friday 12:10 PM) names no second place, so all Masses are at the church (`st-john-the-evangelist-riverhead-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church for the parish.

## Website and bulletin provider

saintjohnriverhead.org is a Solutio (Joomla) site (`probe url` gets 403; `visit.py` reads it). /news-events/bulletin lists issues newest first, each linking straight to its `/file` PDF. The bulletin is parish-made, so there is no printer's listing; following the diocese's rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

`fetch:check` (2026-11-13, as provider `other`) found the 15 November post and failed: "No PDF links found on bulletin post page".

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` links.
