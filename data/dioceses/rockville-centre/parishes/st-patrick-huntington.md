---
name: St. Patrick
website: https://stpathuntington.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stpathuntington.org/bulletin']
group: ''
evidence:
- url: https://stpathuntington.org/bulletin/751-november-15-2026-thirty-third-sunday-in-ordinary-time/file
  seen: 2026-11-13
  note: 'Issue for November 15, 2026 (20 pages, Creator PScript5.dll; downloaded through Chrome). Page
    1 masthead ''Church of St. Patrick / 400 Main Street Huntington, New York (631)-385-3311 | www.stpathuntington.org
    / THIRTY THIRD SUNDAY IN ORDINARY TIME | NOVEMBER 15, 2026'', ''From Our Pastor, Msgr. Camp''. MASS
    SCHEDULE: Sunday 7:30 AM, 8:45 AM, 10:00 AM, 11:30 AM, 5:30 PM; Saturday 8:30 AM, Vigil 5:00 PM; Monday-Friday
    7:15 AM, 9:00 AM, 12:00 PM. No printer named; no other place of Mass.'
- url: https://stpathuntington.org/bulletin
  seen: 2026-11-13
  note: 'Joomla (Solutio-style) bulletin list read with visit.py, newest first: 751-november-15-2026-thirty-third-sunday-in-ordinary-time,
    750-november-8-2026-..., 749-november-1-2026-solemnity-of-all-saints ..., each linking /file, the
    PDF. www.stpatrickchurchhunt.org (the diocesan locator''s link) redirects to stpathuntington.org.'
research:
- method: 'Looked for a printer listing: the issue''s PDF metadata (Creator PScript5.dll, Producer BitMiracle
    Docotic) and text name no printer, LPi or John Patrick'
  url: https://stpathuntington.org/bulletin/751-november-15-2026-thirty-third-sunday-in-ordinary-time/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Joomla (Solutio-style) site. fetch:check on 2026-11-13 (provider other, unpinned) found the 15
    November post but failed: "No PDF links found on bulletin post page: https://stpathuntington.org/bulletin/751-november-15-2026-thirty-third-sunday-in-ordinary-time/file"
    (the /file URL is the PDF and answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://stpathuntington.org/bulletin/751-november-15-2026-thirty-third-sunday-in-ordinary-time/file
---

## Publisher

St. Patrick, Huntington makes its own weekly bulletin and posts it on its Joomla site. The issue for November 15, 2026 (`https://stpathuntington.org/bulletin/751-november-15-2026-thirty-third-sunday-in-ordinary-time/file`, 20 pages, downloaded through Chrome 2026-11-13) opens with "Church of St. Patrick / 400 Main Street Huntington, New York" and "THIRTY THIRD SUNDAY IN ORDINARY TIME | NOVEMBER 15, 2026", and a letter "From Our Pastor, Msgr. Camp". Its MASS SCHEDULE gives Sunday 7:30, 8:45, 10:00, 11:30 AM and 5:30 PM; Saturday 8:30 AM and Vigil 5:00 PM; Monday-Friday 7:15 AM, 9:00 AM and 12:00 PM. No printer is named (Creator PScript5.dll).

## Worship sites

One: the church at 400 Main Street (`st-patrick-huntington-church`). The schedule names no other place. The diocesan locator (directory:128), GCatholic (16864) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

The parish's site is now stpathuntington.org; the locator's and GCatholic's www.stpatrickchurchhunt.org redirects there. `probe url` answered 403; `visit.py` read it. Its `/bulletin` list links `/bulletin/<n>-<date and title>/file`, the PDF, which answers 403 outside a browser, as on the diocese's Solutio sites. No printer listing exists, so following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Joomla `/file` PDFs.
