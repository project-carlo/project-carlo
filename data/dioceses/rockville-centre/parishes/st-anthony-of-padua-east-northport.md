---
name: St. Anthony of Padua
website: https://saintanthonyofpadua.org/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://saintanthonyofpadua.org/bulletin']
group: ''
evidence:
- url: https://saintanthonyofpadua.org/bulletin/317-november-1-2026/file
  seen: 2026-11-13
  note: 'Issue for November 1, 2026 (24 pages, Creator Canva, Producer Acrobat Distiller; downloaded through
    Chrome). Page 1 masthead ''St. Anthony of Padua / ROMAN CATHOLIC CHURCH / 20 Cheshire Place, East
    Northport, New York 11731 / November 1, 2026''; PASTORAL STAFF ''Rev. Edward Sheridan, Pastor'', ''Rev.
    Allan Arneaud, Associate Pastor / St. Francis of Assisi, Greenlawn''; WEEKDAY MASSES ''Monday - Friday
    6:30 am / 9:00 am'', ''Saturday Morning 8:30 am''; WEEKEND MASSES ''Saturday Evening 5:00 pm'', Sunday
    ''7:15 am'', ''8:15 am (Spanish Mass -Upper Church)'', ''9:30 am (Family Liturgy)'', ''11:00 am (Choir
    Mass)'', ''5:00 pm''. Pages carry ''#217 FOR ADVERTISING: THE CHURCH BULLETIN INC.'''
- url: https://saintanthonyofpadua.org/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py, newest first: 317-november-1-2026, 316-october-25-2026,
    315-october-11-2026 ..., each linking /file, the PDF. No November 8 issue was listed on 2026-11-13.'
research:
- method: 'Looked for a printer listing: the issue is printed by The Church Bulletin Inc., West Babylon
    (''#217''), which posts no bulletins online (diocese.md playbook)'
  url: https://saintanthonyofpadua.org/bulletin/317-november-1-2026/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 (provider other, unpinned) failed: "No PDF links
    found on bulletin page: https://saintanthonyofpadua.org/bulletin/file" (it followed the list''s ''Download
    selected'' link; each issue''s /file URL is the PDF and answers 403 outside a browser). Chrome downloads
    it with tools/browser_get.py.'
  url: https://saintanthonyofpadua.org/bulletin/317-november-1-2026/file
publication_reviews:
- parish: st-francis-of-assisi-greenlawn
  decision: separate
  evidence:
  - url: https://saintanthonyofpadua.org/bulletin/317-november-1-2026/file
    seen: 2026-11-13
    note: 'The November 1, 2026 masthead names St. Anthony of Padua, 20 Cheshire Place, East Northport
      alone, with its own Mass schedule (The Church Bulletin Inc. #217).'
  - url: https://container.parishesonline.com/bulletins/03/4100/20261115B.pdf
    seen: 2026-11-13
    note: The November 15, 2026 masthead names St. Francis of Assisi, 29 Northgate Dr., Greenlawn alone,
      with its own Masses, under the same pastor (LPi container 03/4100).
---

## Publisher

St. Anthony of Padua, East Northport has its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon ("#217 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts each issue on its Solutio site. The newest on 2026-11-13, `https://saintanthonyofpadua.org/bulletin/317-november-1-2026/file` (24 pages, downloaded through Chrome), opens with "St. Anthony of Padua / ROMAN CATHOLIC CHURCH / 20 Cheshire Place, East Northport, New York 11731 / November 1, 2026" and lists weekday Masses Monday-Friday 6:30 and 9:00 am, Saturday 8:30 am, and weekend Masses Saturday 5:00 pm, Sunday 7:15 am, 8:15 am (Spanish Mass, Upper Church), 9:30 am, 11:00 am and 5:00 pm.

Its pastor, Rev. Edward Sheridan, is also pastor of St. Francis of Assisi, Greenlawn (that parish's November 15, 2026 masthead), and the staff list names "Rev. Allan Arneaud, Associate Pastor / St. Francis of Assisi, Greenlawn". St. Francis publishes its own bulletin through LPi (container 03/4100), so they are two rows, recorded as a `separate` review with `st-francis-of-assisi-greenlawn`.

## Worship sites

One: the church at 20 Cheshire Place (`st-anthony-of-padua-east-northport-church`). The Spanish Mass is in the "Upper Church", part of the same building. The schedule names no other place. The diocesan locator (directory:140), GCatholic (16836) and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

saintanthonyofpadua.org (GCatholic and the drvc.org Mass-times page link it; the locator links stant-northport.solutiosoftware.com, the same Solutio account) answered 403 to `probe url` and loaded in `visit.py`. Its `/bulletin` list links `/bulletin/<n>-<month>-<d>-<yyyy>/file`, the PDF, which answers 403 outside a browser. The printer has no online listing, so following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`. One file name differs from the date pattern (`311-anthonyenpt9-6`, the September 6 issue).

## Not yet confirmed

Nothing open about the parish; the row waits on a collector for Solutio `/file` PDFs.
