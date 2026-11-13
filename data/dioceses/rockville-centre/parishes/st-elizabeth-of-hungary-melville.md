---
name: St. Elizabeth of Hungary
website: https://stelizabeth.org/parish-life/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stelizabeth.org/parish-life/bulletin']
group: ''
evidence:
- url: https://stelizabeth.org/parish-life/bulletin/56-november-8-2026/file
  seen: 2026-11-13
  quote: Weekdays (Monday to Thursday) at 9:30am
  note: 'Issue for Sunday, November 8, 2026 (17 pages, Creator and Producer Canva; downloaded through
    Chrome). Page 1: ''Sunday, November 8, 2026 / THIRTY-SECOND SUNDAY IN ORDINARY TIME / 175 Wolf Hill
    Road, Melville, NY 11747 / 631-271-4455 ~ www.stelizabeth.org''; Pastoral Team ''Father Irinel Racos,
    Pastor''. Celebration of the Eucharist: ''Weekdays (Monday to Thursday) at 9:30am / Saturday at 5:00pm
    (Vigil for Sunday) / Sunday at 9:00am and 11:30am''. No printer named; no other place of Mass.'
- url: https://stelizabeth.org/parish-life/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py, newest first: 56-november-8-2026, 55-november-1-2026,
    54-october-25-2026 ..., each linking /file, the PDF.'
research:
- method: 'Looked for a printer listing: the issue''s PDF metadata (Creator: Canva) and text name no printer,
    LPi or John Patrick'
  url: https://stelizabeth.org/parish-life/bulletin/56-november-8-2026/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (provider other, unpinned) found the 8 November
    post but failed: "No PDF links found on bulletin post page: https://stelizabeth.org/parish-life/bulletin/56-november-8-2026/file"
    (the /file URL is the PDF and answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://stelizabeth.org/parish-life/bulletin/56-november-8-2026/file
---

## Publisher

St. Elizabeth of Hungary, Melville makes its own weekly bulletin in Canva and posts it on its Solutio (Joomla) site. The issue for November 8, 2026 (`https://stelizabeth.org/parish-life/bulletin/56-november-8-2026/file`, 17 pages, downloaded through Chrome 2026-11-13) opens with "Sunday, November 8, 2026 / THIRTY-SECOND SUNDAY IN ORDINARY TIME / 175 Wolf Hill Road, Melville, NY 11747" and names Father Irinel Racos, Pastor. Its "Celebration of the Eucharist" gives weekdays (Monday to Thursday) 9:30am, Saturday 5:00pm (Vigil) and Sunday 9:00am and 11:30am. No printer is named.

## Worship sites

One: the church at 175 Wolf Hill Road (`st-elizabeth-of-hungary-melville-church`). The bulletin names no other place of Mass. The diocesan locator (directory:95), GCatholic (16884) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

stelizabeth.org answered 403 to `probe url` and loaded in `visit.py`. Its `/parish-life/bulletin` list links `/parish-life/bulletin/<n>-<month>-<d>-<yyyy>/file`, the PDF, which answers 403 outside a browser. The issue is parish-made (Canva), so there is no printer listing. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` PDFs.
