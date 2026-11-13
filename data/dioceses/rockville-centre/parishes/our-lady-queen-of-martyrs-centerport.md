---
name: Our Lady Queen of Martyrs
website: https://www.olqmparish.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.olqmparish.org/news/bulletin']
group: ''
evidence:
- url: https://www.olqmparish.org/news/bulletin/552-november-8-2026/file
  seen: 2026-11-13
  quote: 'Daily: Monday through Thursday at 12 PM'
  note: 'Issue for November 8, 2026 (10 pages, Creator Canva, downloaded through Chrome). Page 1 masthead:
    ''Our Lady Queen of Martyrs / 53 Prospect Rd 631-757-8184 Centerport, NY 11721 www.olqmparish.org'';
    MASS SCHEDULE: ''Daily: Monday through Thursday at 12 PM / No Daily Mass on Friday / Saturday at 9:00AM
    & 5:00 PM / Sunday at 8 AM, 10 AM & 12 PM''. Intentions for Saturday, November 7 to Sunday, November
    15. Baptisms listed for OLQM and for St. Philip Neri; no other place of Mass. No printer named.'
- url: https://www.olqmparish.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py, newest first: 552-november-8-2026, 542-november-1-2026,
    529-october-25-2026 ..., each linking /file, the PDF.'
research:
- method: 'Looked for a printer listing: the issue''s PDF metadata (Creator: Canva) and text name no printer,
    LPi or John Patrick'
  url: https://www.olqmparish.org/news/bulletin/552-november-8-2026/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (provider other, unpinned) found the 8 November
    post but failed: "No PDF links found on bulletin post page: https://www.olqmparish.org/news/bulletin/552-november-8-2026/file"
    (the /file URL is the PDF and answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://www.olqmparish.org/news/bulletin/552-november-8-2026/file
publication_reviews:
- parish: st-philip-neri-northport
  decision: separate
  evidence:
  - url: https://www.olqmparish.org/news/bulletin/552-november-8-2026/file
    seen: 2026-11-13
    note: The November 8, 2026 masthead names Our Lady Queen of Martyrs, 53 Prospect Rd, Centerport alone,
      with its own Mass schedule and intentions (10 pages, made in Canva).
  - url: https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file
    seen: 2026-11-13
    note: The November 8, 2026 issue's masthead names The Parish of St. Philip Neri, 15 Prospect Avenue,
      Northport, a separate 12-page bulletin printed by The Church Bulletin Inc. (#181).
---

## Publisher

Our Lady Queen of Martyrs, Centerport makes its own weekly bulletin in Canva and posts it on its Solutio (Joomla) site. The issue for November 8, 2026 (`https://www.olqmparish.org/news/bulletin/552-november-8-2026/file`, 10 pages, downloaded through Chrome 2026-11-13) opens with the masthead "Our Lady Queen of Martyrs / 53 Prospect Rd ... Centerport, NY 11721" and the MASS SCHEDULE "Daily: Monday through Thursday at 12 PM / No Daily Mass on Friday / Saturday at 9:00AM & 5:00 PM / Sunday at 8 AM, 10 AM & 12 PM". No printer is named.

The parish shares its pastor and staff with St. Philip Neri, Northport (the June 2023 appointments named Fr. Robert Holz pastor of both; the St. Philip Neri bulletin of November 8, 2026 names Father Adrian McHugh, Pastor, and lists both parishes' Mass times). The OLQM bulletin also lists St. Philip Neri baptisms. But the two parishes publish separate bulletins with their own mastheads (this one Canva-made, St. Philip Neri's printed by The Church Bulletin Inc.), recorded as a `separate` review with `st-philip-neri-northport`.

## Worship sites

One: the church at 53 Prospect Road (`our-lady-queen-of-martyrs-centerport-church`). The bulletin's schedule names no other place of Mass. The diocesan locator (directory:106), GCatholic (16823) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

www.olqmparish.org is a Solutio (Joomla) site (`probe url` answered 403; `visit.py` read it). Its `/news/bulletin` list links `/news/bulletin/<n>-<month>-<d>-<yyyy>/file`, the PDF, which answers 403 outside a browser. The issue is parish-made (Canva), so there is no printer listing. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` PDFs.
