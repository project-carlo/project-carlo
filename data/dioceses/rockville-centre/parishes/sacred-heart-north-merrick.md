---
name: Sacred Heart
website: https://www.sacredheartnm.org/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.sacredheartnm.org/news/bulletin']
group: ''
evidence:
- url: https://www.sacredheartnm.org/news/bulletin/347-november-8-2026/file
  seen: 2026-11-13
  quote: Rev. Stephen Brigandi, Pastor
  note: '8 November 2026 issue (12 pages; PDF title SHNM11-8.pdf, made in Microsoft Publisher by the parish;
    downloaded through Chrome with tools/browser_get.py). Page 1 cover (read as an image; its text layer
    doubles letters): ''Roman Catholic Church of the Sacred Heart, 720 Merrick Ave, North Merrick, NY
    11566, Phone: 516-379-1356''. Page 2 staff: Rev. Stephen Brigandi, Pastor; ''Parish Website: Sacredheartnm.org''.
    Page 3 Mass intentions: Monday-Friday 9AM; Saturday, November 14, 2026 5PM; Sunday, November 15, 2026
    8AM, 10AM, 12PM, 5PM. Reconciliation Saturday 4:00PM ''in the church''.'
- url: https://www.sacredheartnm.org/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py (probe url answers 403): 347-november-8-2026,
    346-november-1-2026, 345-october-25-2026, newest first.'
- url: https://www.hearttoheartparish.org
  seen: 2026-11-13
  note: The domain GCatholic and the drvc.org Mass-times page link redirects to payadong.top, a Vietnamese
    betting site ('Lu88 payadong'); probe url verdict SPAM-SQUAT. Not the parish's site.
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: ''No PDF
    links found on bulletin post page: .../347-november-8-2026/file'' (the post is the PDF, which answers
    403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://www.sacredheartnm.org/news/bulletin/347-november-8-2026/file
---

## Publisher

The Roman Catholic Church of the Sacred Heart, 720 Merrick Avenue, North Merrick publishes its own weekly bulletin, made by the parish in Microsoft Publisher (PDF title "SHNM11-8.pdf"; no printer's id or LPi/John Patrick marks). The 8 November 2026 issue (`https://www.sacredheartnm.org/news/bulletin/347-november-8-2026/file`, 12 pages, read 2026-11-13) has the cover "Roman Catholic Church of the Sacred Heart, 720 Merrick Ave, North Merrick, NY 11566" (page 1, read as an image because its text layer doubles letters) and names Rev. Stephen Brigandi, Pastor (page 2). The bulletin prints no schedule box; its Mass intentions (page 3) give Monday-Friday 9AM, Saturday 5PM and Sunday 8AM, 10AM, 12PM and 5PM.

The drvc.org Mass-times page gives Saturday 5:00 PM, Sunday 8:00 AM, 10:00 AM and Noon, weekdays 9:00 AM; the bulletin adds a 5PM Sunday Mass.

## Worship sites

One: the church at 720 Merrick Avenue (`sacred-heart-north-merrick-church`). The bulletin names no other building. The drvc.org Mass-times page lists this church twice, once under Merrick (`mass-times:church-of-the-sacred-heart-merrick`) and once under North Merrick (`mass-times:church-of-the-sacred-heart-north-merrick`), with the same schedule and site; both entries are this church. The diocesan locator (directory:27) and GCatholic (16892) list only this one.

## Website and bulletin provider

The locator links sacredheartnm.org, which the bulletin also names. GCatholic and the Mass-times page link hearttoheartparish.org, which on 2026-11-13 redirected to a Vietnamese betting site (payadong.top; `probe url` SPAM-SQUAT), a squatted domain. sacredheartnm.org is a Solutio (Joomla) site: `/news/bulletin` lists the issues newest first, each a `/news/bulletin/<n>-<date>/file` PDF that answers 403 outside a browser (Chrome downloads it). The parish makes the bulletin itself, so there is no printer's listing; the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`, following the diocese's rule for Solutio sites. `fetch:check` (2026-11-13) failed: "No PDF links found on bulletin post page".

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
