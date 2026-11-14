---
name: St. Elizabeth Ann Seton
website: https://steas.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://steas.org/news/bulletin']
group: ''
evidence:
- url: https://steas.org/news/bulletin/108-november-15-2026/file
  seen: 2026-11-13
  note: 'Issue for November 15, 2026, Thirty-third Sunday in Ordinary Time (15 pages, Creator Canva; downloaded
    through Chrome with browser_get.py, probe get answers 403). Page 1 masthead ''St. Elizabeth Ann Seton
    ROMAN CATHOLIC CHURCH ... 800 Portion Road, Lake Ronkonkoma, New York 11779''. Mass Schedule: Saturday
    Evening 5:00 PM; Sunday 9:00 AM and 11:00 AM; Weekday Monday to Thursday at 9:00 AM; no other place.
    Pastor Stephen Pietrowski. No printer, LPi footer or 4lpi.com link.'
- url: https://steas.org/news/bulletin
  seen: 2026-11-13
  note: 'Joomla (Solutio-style) bulletin list read with visit.py (probe url answers 403), newest first:
    ''108-november-15-2026/file'', ''107-november-8-2026/file'', ''106-november-1-2026/file'' ...'
research:
- method: 'Looked for a printer listing: the 15 November issue''s metadata (Creator Canva) and text name
    no printer, no LPi footer and no 4lpi.com link'
  url: https://steas.org/news/bulletin/108-november-15-2026/file
  checked: '2026-11-13'
  outcome: not-found
  next_action: Set bulletin_provider other once a collector reads Solutio /file PDFs, then run fetch:check
  retry_when: A Solutio /file collector lands or the parish moves its bulletin to another host
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  url: https://steas.org/news/bulletin/108-november-15-2026/file
  note: The Solutio (Joomla) Bulletin page lists one issue per Sunday, newest 'November 15, 2026' (/news/bulletin/108-november-15-2026/file),
    read with visit.py on 2026-11-13. The /file links carry no .pdf name and answer 403 to probe get;
    fetch:check (other, unpinned) reported resolve_failed 'No PDF links found on bulletin post page'.
    Chrome (browser_get.py) downloads the PDF.
---

## Publisher

St. Elizabeth Ann Seton, Lake Ronkonkoma, publishes its own weekly bulletin (Canva, no printer named). The 15 November 2026 issue (`https://steas.org/news/bulletin/108-november-15-2026/file`, 15 pages, read 2026-11-13 through Chrome) is headed "St. Elizabeth Ann Seton ROMAN CATHOLIC CHURCH", "800 Portion Road, Lake Ronkonkoma, New York 11779", and names Stephen Pietrowski, Pastor.

## Worship sites

One: the church at 800 Portion Road (`st-elizabeth-ann-seton-lake-ronkonkoma-church`). The issue's Mass Schedule (Saturday Evening 5:00 PM; Sunday 9:00 AM and 11:00 AM; Monday to Thursday 9:00 AM) names no other place, and the diocesan locator, GCatholic and the drvc.org Mass-times page list only this church.

## Website and bulletin provider

steas.org is a Joomla (Solutio-style) site; `/news/bulletin` lists issues newest first, each linking a `/file` PDF that answers 403 to `probe get` and downloads in Chrome. The issue is self-made (Canva) with no printer listing to read instead, so under this diocese's settled rule for Solutio sites the row is `unsupported` with fetch_gap `joomla-file-endpoint`: fetch:check (2026-11-13) reported "No PDF links found on bulletin post page".

## Not yet confirmed

Nothing about the parish. The row goes live when a collector reads Solutio `/file` PDFs; see research.
