---
name: Resurrection
website: https://coresrcc.com/news/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://coresrcc.com/news/bulletin']
group: ''
evidence:
- url: https://coresrcc.com/news/bulletin/411-33rd-sunday-in-ordinary-time-november-15th-2026/file
  seen: 2026-11-13
  note: 'Pages 1-2 of the 15 November 2026 issue, read as images (12 pages; PDF Creator Affinity 3.3.3,
    Producer Acrobat Distiller; downloaded through Chrome with tools/browser_get.py; the text layer is
    symbol soup). Masthead: ''The R.C. Church of the RESURRECTION, 50 Granny Road Farmingville, NY 11738
    ... www.coresrcc.com'', ''Thirty-Third Sunday in Ordinary Time, November 15, 2026''. Page 2 MASS SCHEDULE:
    Monday-Thursday 9:00 AM; Saturday 5:00 PM English, 7:00PM Spanish; Sunday 9:00 AM English, 10:30 AM
    Portuguese, 12:00 PM English, 5:00 PM Spanish. Back page: ''#125 FOR ADVERTISING: THE CHURCH BULLETIN
    INC., 200 DALE ST., W. BABYLON''.'
- url: https://coresrcc.com/news/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin list read with visit.py (probe url answers 403): newest first, 411-33rd-sunday-in-ordinary-time-november-15th-2026,
    410-32nd-sunday-in-ordinary-time-november-8th-2026, 409-all-saints-day-november-1st-2026.'
- url: https://resurrectionrcchurch.org
  seen: 2026-11-13
  note: The domain the diocesan locator and GCatholic link redirects to https://coresrcc.com/ (probe url).
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 15 November post but failed: ''No
    PDF links found on bulletin post page: .../411-33rd-sunday-in-ordinary-time-november-15th-2026/file''
    (the post is the PDF, which answers 403 outside a browser). Chrome downloads it with tools/browser_get.py.'
  url: https://coresrcc.com/news/bulletin/411-33rd-sunday-in-ordinary-time-november-15th-2026/file
publication_reviews:
- parish: st-sylvester-medford
  decision: separate
  evidence:
  - url: https://coresrcc.com/news/bulletin/411-33rd-sunday-in-ordinary-time-november-15th-2026/file
    seen: 2026-11-13
    note: The 15 November 2026 masthead names The R.C. Church of the Resurrection, 50 Granny Road, Farmingville,
      alone, with its own Mass schedule (Saturday 5:00 PM, 7:00 PM Spanish; Sunday 9:00, 10:30 Portuguese,
      12:00, 5:00 PM Spanish).
  - url: https://customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/0018000000Qx82rAAB/publications/1794001654588-03-1145%20-%20November%208%20bulletin%20with%20Ads.pdf
    seen: 2026-11-13
    note: 'The 8 November 2026 St. Sylvester bulletin serves St. Sylvester, Medford alone: its staff (Rev.
      Gius Garcia, Pastor) and Masses (Saturday 5:00pm; Sunday 7:30, 9:00, 11:00 am, Vietnamese 3:00 pm),
      mentioning Resurrection only for a Holy Hour there.'
---

## Publisher

Resurrection, 50 Granny Road, Farmingville publishes its own weekly bulletin, laid out by the parish (PDF Creator "Affinity 3.3.3") and printed by The Church Bulletin Inc., West Babylon (back page "#125 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no listing online. The 15 November 2026 issue (`https://coresrcc.com/news/bulletin/411-33rd-sunday-in-ordinary-time-november-15th-2026/file`, 12 pages, read 2026-11-13 as images of pages 1-2, because the text layer is symbol soup) has the masthead "The R.C. Church of the RESURRECTION, 50 Granny Road Farmingville, NY 11738". Mass schedule: Monday-Thursday 9:00 AM; Saturday 5:00 PM (English) and 7:00 PM (Spanish); Sunday 9:00 AM (English), 10:30 AM (Portuguese), 12:00 PM (English) and 5:00 PM (Spanish).

The batch brief says Resurrection and St. Sylvester, Medford share a pastor (June 2025). Their bulletins are separate: each has its own masthead and Mass schedule, St. Sylvester's is laid out in Publisher and uploaded to ParishesOnline, and it mentions Resurrection only for a Holy Hour there (see `publication_reviews`). The pastor's name was not read in this issue (only pages 1-2 were rendered). The drvc.org Mass-times page gives the same weekend schedule.

## Worship sites

One: the church at 50 Granny Road (`resurrection-farmingville-church`). The schedule names no other building. The diocesan locator (directory:75), GCatholic (16842) and the Mass-times page list only this church.

## Website and bulletin provider

The locator and GCatholic link resurrectionrcchurch.org, which redirects to coresrcc.com, the site the masthead gives. It is a Solutio (Joomla) site (403 to `probe url`; read with `visit.py`): `/news/bulletin` lists the issues newest first, each a `/news/bulletin/<n>-<title>/file` PDF that Chrome downloads with tools/browser_get.py. The printer posts nothing online, so following the diocese's rule for Solutio sites the row is `unsupported` with `fetch_gap` `joomla-file-endpoint` (see the gap note for the fetch:check result).

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
