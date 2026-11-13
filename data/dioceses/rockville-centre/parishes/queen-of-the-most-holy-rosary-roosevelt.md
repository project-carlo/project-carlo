---
name: Queen of the Most Holy Rosary
website: https://www.qtmhr.com/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.qtmhr.com/news/bulletin#queen-of-the-most-holy-rosary']
group: ''
evidence:
- url: https://www.qtmhr.com/news/bulletin/337-32nd-sunday-in-ordinary-time-2026/file
  seen: 2026-11-13
  note: 'Issue ''32nd Sunday in Ordinary Time 2026'' (8 November; 7 pages; uploaded 5 Nov). Its text layer
    is garbled (subset fonts), so page 1 was rendered and read as an image: cover ''Queen of the Most
    Holy Rosary, Celebrating 100 Years, Roosevelt, New York'', 196 W Centennial Ave. Roosevelt NY 11575,
    www.qtmhr.com; MASS SCHEDULE Monday-Friday 8:00AM; Friday 7:00PM Spanish; Saturday 9:00AM, 5:30PM;
    Sunday 9:00AM, 11:00AM; 7:00AM, 12:30PM Spanish; Parish Staff Rev. Rony Fabien, Pastor; Rev. Cesar
    Bejarano, OFM; Dcn. Hernst Bellevue; Dcn. Clinton Lewis, Emeritus; in residence Rev. Anthony Kannampuzha.
    Downloaded through Chrome (tools/browser_get.py).'
- url: https://www.qtmhr.com/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin page, read with parish-site-access visit.py (probe url answers 403):
    issues newest first as /news/bulletin/<n>-<title>/file, the newest 337-32nd-sunday-in-ordinary-time-2026,
    then 336-31st..., 335-29th...'
research:
- method: fetch:check, page-pdfs on the Solutio bulletin page and unpinned
  url: https://www.qtmhr.com/news/bulletin
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check once a collector reads Solutio /file links
  retry_when: pnpm diocese gaps shows a collector for joomla-file-endpoint
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13, pinned (page-pdfs on /news/bulletin) and unpinned,
    failed: "No PDF links found on bulletin page: https://www.qtmhr.com/news/bulletin". The issues are
    /news/bulletin/<n>-<title>/file links, which Chrome downloads with tools/browser_get.py. The issue
    is made in-house (PDF Creator PScript5/Acrobat Distiller); no printer listing.'
  url: https://www.qtmhr.com/news/bulletin/337-32nd-sunday-in-ordinary-time-2026/file
publication_reviews:
- parish: st-martha-uniondale
  decision: separate
  evidence:
  - url: https://www.qtmhr.com/news/bulletin/337-32nd-sunday-in-ordinary-time-2026/file
    seen: 2026-11-13
    note: The 8 November 2026 masthead names Queen of the Most Holy Rosary, Roosevelt alone, with its
      own Mass schedule and staff (page 1, read as an image).
  - url: https://saintmartha.org/news/bulletin/509-32nd-sunday-in-ordinary-time-2026/file
    seen: 2026-11-13
    note: 'The 8 November 2026 masthead names St. Martha alone: ''Visit www.saintmartha.org'', Fr. Rony
      Fabien, Pastor, and its own Mass collection list.'
---

## Publisher

Queen of the Most Holy Rosary, Roosevelt publishes its own weekly bulletin, posted on its Solutio (Joomla) site. The newest issue on 2026-11-13, `https://www.qtmhr.com/news/bulletin/337-32nd-sunday-in-ordinary-time-2026/file` (7 pages, 32nd Sunday in Ordinary Time, 8 November 2026), has a garbled text layer, so its cover was rendered and read as an image: "Queen of the Most Holy Rosary, Celebrating 100 Years, Roosevelt, New York", 196 W Centennial Ave., and under Parish Staff "Rev. Rony Fabien. Pastor", "Rev. Cesar Bejarano. OFM", Dcn. Hernst Bellevue and Dcn. Clinton Lewis, Emeritus. Its Mass Schedule: Monday-Friday 8:00AM; Friday 7:00PM Spanish; Saturday 9:00AM, 5:30PM; Sunday 9:00AM, 11:00AM, and 7:00AM, 12:30PM Spanish. The PDF was made in-house (Creator PScript5, Acrobat Distiller); it carries no printer's name.

## Worship sites

One: the church at 196 West Centennial Avenue (`queen-of-the-most-holy-rosary-roosevelt-church`). The schedule names no other place. The diocesan locator (directory:25), GCatholic (16907) and the drvc.org Mass-times page list only this church.

## Shared pastor with St. Martha

Fr. Rony Fabien is pastor of both this parish and St. Martha, Uniondale (`st-martha-uniondale`), and Deacon Hernst Bellevue serves both. They publish two bulletins: the 8 November 2026 issues are separate files on separate sites (qtmhr.com issue 337, saintmartha.org issue 509) with different covers, staff lists and schedules; this one names Queen of the Most Holy Rosary alone. St. Martha's issue of the same Sunday advertises a Spanish Advent retreat "at the Queen of the Most Holy Rosary Parish located at 196 West Centennial Ave in Roosevelt" as another parish's venue. So two rows, recorded as `separate` in `publication_reviews`.

## Website and bulletin provider

qtmhr.com is the link the locator, GCatholic and the Mass-times page all give. `probe url` answers 403; visit.py reads it. The bulletin page lists issues newest first as `/news/bulletin/<n>-<title>/file`, which Chrome downloads (tools/browser_get.py) but `fetch:check` can't: on 2026-11-13, pinned and unpinned, it reported "No PDF links found on bulletin page". The row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, following the diocese's rule for Solutio sites with no printer listing. The text layer is garbled, so a collector would also need to read the pages as images.

## Not yet confirmed

The drvc.org Mass-times page gives a different Sunday schedule (7:00 AM Spanish, 9:00, 10:30 AM, Noon, 12:30 PM Spanish, 1:15 PM Spanish); the bulletin's is followed. Nothing else open.
