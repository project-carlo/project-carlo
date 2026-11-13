---
name: St. Philip Neri
website: https://stphil-northport.solutiosoftware.com/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://stphil-northport.solutiosoftware.com/news/bulletin']
group: ''
evidence:
- url: https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file
  seen: 2026-11-13
  note: 'Issue posted as ''November 8'' (12 pages, Creator Canva, Producer Acrobat Distiller; downloaded
    through Chrome). Page 1 masthead ''The Parish of St. Philip Neri ... Established in 1894'' (its date
    line still reads ''The Feast of All Saints ~ November 1, 2026'', but the Mass intentions run Mon.
    Nov. 9 to Sun. Nov. 15). ''Weekend Masses here at St. Philip Neri / Vigil Mass: 5:00PM ... Sunday:
    8:00AM, 9:30AM & 11:30AM''; ''Our Lady Queen of Martyrs / Vigil Mass: 5:00PM / Sundays: 8:00AM, 10:00AM
    & 12:00PM''; ''Weekday Mass Tuesday-Friday: 9:00AM / Monday-Thursday: 12:00PM at OLQM''. Pastor Father
    Adrian McHugh, Associate Pastor Father Michael Lombardi. Parish Information: ''15 Prospect Avenue,
    Northport, NY 11768''. Back page: ''#181 FOR ADVERTISING: THE CHURCH BULLETIN INC.'''
- url: https://stphil-northport.solutiosoftware.com/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py, newest first: 393-november-8, 392-november-1-1,
    391-october-25 (a ''default'' icon, not ''pdf''), 390-november-1, 389-october-18 ..., each linking
    /file. stphilipnerinpt.org (the diocese''s link) redirects here; www.spnpt.org (the bulletin''s web
    address) answered 403 to probe url.'
research:
- method: 'Looked for a printer listing: the issue is printed by The Church Bulletin Inc., West Babylon
    (back page ''#181''), which posts no bulletins online (diocese.md playbook)'
  url: https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (provider other, unpinned) found the 8 November
    post but failed: "No PDF links found on bulletin post page: https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file"
    (the /file URL is the PDF and answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file
publication_reviews:
- parish: our-lady-queen-of-martyrs-centerport
  decision: separate
  evidence:
  - url: https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file
    seen: 2026-11-13
    note: 'The November 8, 2026 masthead names The Parish of St. Philip Neri, 15 Prospect Avenue, Northport,
      with its own intentions; it lists OLQM''s Mass times as the sister parish''s (12 pages, The Church
      Bulletin Inc. #181).'
  - url: https://www.olqmparish.org/news/bulletin/552-november-8-2026/file
    seen: 2026-11-13
    note: The November 8, 2026 masthead names Our Lady Queen of Martyrs, 53 Prospect Rd, Centerport alone,
      with its own Mass schedule and intentions (10 pages, made in Canva).
---

## Publisher

St. Philip Neri, Northport has its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#181 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts each issue on its Solutio site. The issue posted as "November 8" (`https://stphil-northport.solutiosoftware.com/news/bulletin/393-november-8/file`, 12 pages, downloaded through Chrome 2026-11-13) opens with "The Parish of St. Philip Neri ... Established in 1894"; its cover date line was not updated ("The Feast of All Saints ~ November 1, 2026"), but its Mass intentions run Monday, November 9 to Sunday, November 15. Page 1 gives "Weekend Masses here at St. Philip Neri / Vigil Mass: 5:00PM ... Sunday: 8:00AM, 9:30AM & 11:30AM" and "Weekday Mass Tuesday-Friday: 9:00AM", and the parish address "15 Prospect Avenue, Northport, NY 11768".

The parish shares its pastor (Father Adrian McHugh in this issue; Fr. Robert Holz was named pastor of both in June 2023) and associate with Our Lady Queen of Martyrs, Centerport, and page 1 also lists OLQM's weekend and weekday Masses. OLQM publishes its own bulletin, though (its November 8, 2026 issue is a separate 10-page Canva document with its own masthead and intentions), so they are two rows, recorded as a `separate` review with `our-lady-queen-of-martyrs-centerport`. OLQM's church belongs to that row.

## Worship sites

One: the church (`st-philip-neri-northport-church`). The schedule's only other place is OLQM, which has its own bulletin. The diocesan locator (directory:131), GCatholic (16893) and the drvc.org Mass-times page list only this church for the parish.

## Website and bulletin provider

stphilipnerinpt.org redirects to stphil-northport.solutiosoftware.com, a Solutio (Joomla) site. Its `/news/bulletin` list links `/news/bulletin/<n>-<month>-<d>/file`, the PDF, which answers 403 outside a browser. One item (391-october-25) carries a "default" icon rather than "pdf" and may be a Canva viewer. The printer has no online listing, so following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`. File names carry no year (`393-november-8`), so a future collector must take the year from the masthead or upload date.

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` PDFs.
