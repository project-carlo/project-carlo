---
name: St. Joseph
website: https://www.stjoekp.com/about/weekly-bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stjoekp.com/about/weekly-bulletin']
group: ''
evidence:
- url: https://www.stjoekp.com/about/weekly-bulletin/349-nov-8-2026-thirty-second-sunday-in-ordinary-time-year-a/file
  seen: 2026-11-13
  note: 'Issue for Sunday, November 8 (20 pages, Creator Adobe Acrobat Pro 2020; downloaded through Chrome
    with browser_get.py). Page 1 ''Parish Hours & Contact: 59 Church Street, Kings Park, NY 11754 ...
    Website: www.stjoekp.com''. ''THE HOLY SACRIFICE OF THE MASS: Saturday: 5 PM vigil; Sunday: 7:30 AM,
    9 AM, 10:30 AM, 12 Noon & 5 PM; Weekday: 7 AM & 8:45 AM''. The Nazareth Chapel (Parish Center) is
    named only for Friday adoration and confessions. Page 17 ''Pastor: Rev. Peter J. Dugandzic''. Back
    page ''#173 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON''.'
- url: https://www.stjoekp.com/about/weekly-bulletin
  seen: 2026-11-13
  note: 'Joomla (Solutio-style) Weekly Bulletin list read with visit.py, newest first: ''349-nov-8-2026-...'',
    ''348-nov-1-2026-solemnity-of-all-saints-year-a'', ... each linking /file. Found by a DuckDuckGo search;
    stjosephskp.org (the locator''s, GCatholic''s and Mass-times page''s link) fails with a certificate
    for another host name (www.stjosephskp.org: Hostname mismatch; Chrome ERR_CERT_COMMON_NAME_INVALID).'
research:
- method: 'Looked for a printer listing: the 8 November issue is printed by The Church Bulletin Inc.,
    West Babylon (#173), which posts no bulletins online; no LPi footer or 4lpi.com link'
  url: https://www.stjoekp.com/about/weekly-bulletin/349-nov-8-2026-thirty-second-sunday-in-ordinary-time-year-a/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
- method: fetch:check (provider other, unpinned, via tools/fc_unsupported.sh)
  url: https://www.stjoekp.com/about/weekly-bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check once a Solutio /file collector lands
  retry_when: A Solutio /file collector lands
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  url: https://www.stjoekp.com/about/weekly-bulletin/349-nov-8-2026-thirty-second-sunday-in-ordinary-time-year-a/file
  note: The Solutio (Joomla) Weekly Bulletin page lists one issue per Sunday, newest 'November 8, 2026
    - Thirty-Second Sunday in Ordinary Time, Year A' (/about/weekly-bulletin/349-.../file), read with
    visit.py on 2026-11-13. The /file links carry no .pdf name; Chrome (browser_get.py) downloads the
    PDF. See research for the fetch:check result.
---

## Publisher

St. Joseph, Kings Park, publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#173 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts none online. The newest issue posted on 2026-11-13, for Sunday 8 November 2026 (`https://www.stjoekp.com/about/weekly-bulletin/349-nov-8-2026-thirty-second-sunday-in-ordinary-time-year-a/file`, 20 pages), gives "59 Church Street, Kings Park, NY 11754", "Website: www.stjoekp.com" and "Pastor: Rev. Peter J. Dugandzic".

## Worship sites

One: the church at 59 Church Street (`st-joseph-kings-park-church`). The issue's "THE HOLY SACRIFICE OF THE MASS" (Saturday 5 PM vigil; Sunday 7:30 AM, 9 AM, 10:30 AM, 12 Noon & 5 PM; weekdays 7 AM & 8:45 AM) names no other place. The Nazareth Chapel in the Parish Center is named only for Friday adoration and confessions, not Mass, so it has no record. The diocesan locator, GCatholic and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

`stjosephskp.org`, the link the locator, GCatholic and the Mass-times page give, fails on 2026-11-13: its certificate is for another host name (`probe get`: Hostname mismatch; Chrome: ERR_CERT_COMMON_NAME_INVALID). A DuckDuckGo search found the parish's current site, `stjoekp.com`, which the bulletin names. It is a Joomla (Solutio-style) site whose Weekly Bulletin page lists issues newest first as `/file` links; Chrome downloads them. The printer has no listing to read instead, so under this diocese's settled rule for Solutio sites the row is `unsupported` with fetch_gap `joomla-file-endpoint`.

fetch:check (2026-11-13, provider `other` for the check) reported resolve_failed "No PDF links found on bulletin post page" for the 8 November `/file` link.

## Not yet confirmed

Nothing about the parish. The row goes live when a collector reads Solutio `/file` PDFs; see research.
