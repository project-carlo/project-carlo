---
name: St. Catherine of Sienna
website: https://www.stcatherineofsienna.org/whats-happening/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stcatherineofsienna.org/whats-happening/bulletin#st-catherine-of-sienna']
group: ''
evidence:
- url: https://www.stcatherineofsienna.org/whats-happening/bulletin/48-november-8-2026/file
  seen: 2026-11-13
  quote: 33 New Hyde Park Road, Franklin Square, NY 11010
  note: Issue for November 8, 2026 (16 pages; PDF title CathSienna11-8.pdf, Creator Microsoft Publisher,
    Producer Acrobat Distiller, so made in-house). Page 2 (rendered; its small-caps text extracts badly)
    names Saint Catherine of Sienna Roman Catholic Church, Pastor Rev. Fr. Lennard Sabio; Mass Schedule
    Monday through Friday 8:00 A.M. and 12:10 P.M. - Church; Saturday 8:00 A.M. - Church, 4:30 P.M. (Vigil
    Mass) - SCS Chapel; Sunday - Church 7:30, 8:45, 11:30 A.M.; Sunday - SCS Chapel (in Sienna Center)
    9:45 A.M., 1:00 P.M. Downloaded through Chrome (tools/browser_get.py).
- url: https://www.stcatherineofsienna.org/whats-happening/bulletin
  seen: 2026-11-13
  note: 'Solutio (Joomla) bulletin page, read with parish-site-access visit.py (probe url answers 403):
    issues newest first as /whats-happening/bulletin/<n>-<date>/file, the newest 48-november-8-2026.'
- url: https://www.stcatherineofsienna.org/
  seen: 2026-11-13
  quote: 'Sunday: 9:45 AM and 1:00 PM at SCS Chapel / Sienna Center'
  note: 'Home page Mass schedule (read with visit.py): Saturday Vigil 4:30 PM at SCS Chapel; Sunday 7:30,
    8:45 and 11:30 AM at the Church.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-13
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-13 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../48-november-8-2026/file" (the /file link is the PDF, which
    Chrome downloads with tools/browser_get.py). The issue is made in Microsoft Publisher; no printer
    listing.'
  url: https://www.stcatherineofsienna.org/whats-happening/bulletin/48-november-8-2026/file
---

## Publisher

St. Catherine of Sienna, Franklin Square publishes its own weekly bulletin, made in Microsoft Publisher (PDF title "CathSienna11-8.pdf"); no printer's name or listing appears. The newest issue on 2026-11-13, `https://www.stcatherineofsienna.org/whats-happening/bulletin/48-november-8-2026/file` (16 pages, "November 8, 2026" on the cover), has on page 2 (rendered) the masthead "Saint Catherine of Sienna Roman Catholic Church, 33 New Hyde Park Road, Franklin Square, NY 11010", Pastor Rev. Fr. Lennard Sabio, and a Mass Schedule: Monday through Friday 8:00 A.M. and 12:10 P.M. (Church); Saturday 8:00 A.M. (Church) and 4:30 P.M. Vigil (SCS Chapel); Sunday 7:30, 8:45 and 11:30 A.M. (Church) and 9:45 A.M. and 1:00 P.M. ("Sunday - SCS Chapel (in Sienna Center)").

## Worship sites

Two: the church at 33 New Hyde Park Road (`st-catherine-of-sienna-franklin-square-church`) and the SCS Chapel in the Sienna Center (`scs-chapel-sienna-center-franklin-square-church`), which has three of the weekend Masses. The diocesan locator (directory:38), GCatholic (16845) and the drvc.org Mass-times page list only the church as a place, though the Mass-times page's schedule also names "SCS Chapel". The Adoration Chapel named in the bulletin is for adoration, not Mass.

## Website and bulletin provider

stcatherineofsienna.org is a Solutio (Joomla) site ("Site by Solutio"), the locator's and Mass-times page's link. `probe url` answers 403; visit.py reads it. Its bulletin page lists issues newest first as `/whats-happening/bulletin/<n>-<date>/file`; one is mislabelled "September 20, 2027" (41-september-20-2027). Chrome downloads the `/file` PDFs (tools/browser_get.py).

`fetch:check` (2026-11-13) found the 8 November post but failed: "No PDF links found on bulletin post page", because the `/file` link is itself the PDF. The issue is made in-house (Microsoft Publisher) and no printer listing (LPi, ParishesOnline, John Patrick) is linked, so under the diocese's rule for Solutio sites the row is `unsupported` with fetch_gap `joomla-file-endpoint`.

## Not yet confirmed

Nothing open about the bulletin; see the SCS Chapel record for its address.
