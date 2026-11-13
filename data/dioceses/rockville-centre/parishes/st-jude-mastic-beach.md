---
name: St. Jude
website: https://stjudemb.org/bulletin-archives/
bulletin_provider: other
provider_id: page-pdfs https://stjudemb.org/bulletin-archives/
publication: ['url:https://stjudemb.org/bulletin-archives/']
group: ''
evidence:
- url: https://stjudemb.org/wp-content/uploads/2026/10/ST.-JUDE-11032026.pdf
  seen: 2026-11-13
  quote: St. Jude Roman Catholic Church
  note: 'Issue for the Thirty-First Sunday in Ordinary Time, ''November 1st, 2026'' (file named 11032026;
    16 pages; PDF Creator Affinity 3.3.1, parish-made, no printer''s marks). Page 1: St. Jude Roman Catholic
    Church, 89 Overlook Drive - Mastic Beach, NY 11951; Rev. John Ryan, Pastor. Celebration of the Eucharist:
    Saturday 4:00pm Vigil; Sunday 8:00am, 10:00am Family Mass, 12:00pm, 5:00pm Spanish Mass; Daily 9:00am,
    12:00pm every Wednesday (St. Jude Novena Mass).'
- url: https://stjudemb.org/bulletin-archives/
  seen: 2026-11-13
  note: 'WordPress Bulletin Archives page (probe get): 12 PDFs, ST.-JUDE-08162026.pdf through ST.-JUDE-11032026.pdf.
    The media API (wp-json/wp/v2/media?search=JUDE) shows ST.-JUDE-11032026.pdf uploaded 2026-10-28 as
    the newest; no 8 November issue was posted by 13 November.'
revisit: Check that issues after 1 November 2026 appear on the Bulletin Archives page and that fetch:check
  picks the newest.
revisit_after: 2026-12-01
bulletin_status: available
---

## Publisher

St. Jude, 89 Overlook Drive, Mastic Beach publishes its own weekly bulletin, laid out by the parish (PDF Creator "Affinity 3.3.1"; no printer's marks). The newest posted issue, for 1 November 2026 (`https://stjudemb.org/wp-content/uploads/2026/10/ST.-JUDE-11032026.pdf`, read 2026-11-13), has the page 1 masthead "St. Jude Roman Catholic Church, 89 Overlook Drive - Mastic Beach, NY 11951" and names Rev. John Ryan, Pastor. Celebration of the Eucharist: Saturday 4:00pm Vigil; Sunday 8:00am, 10:00am (Family Mass), 12:00pm and 5:00pm (Spanish); daily 9:00am, plus 12:00pm every Wednesday (St. Jude Novena Mass).

The drvc.org Mass-times page adds Sunday 6:30 PM (Spanish) and Monday-Saturday daily Mass; the bulletin is followed.

## Worship sites

One: the church at 89 Overlook Drive (`st-jude-mastic-beach-church`). The schedule names no other building. The diocesan locator (directory:118), GCatholic (16882) and the Mass-times page list only this church.

## Website and bulletin provider

stjudemb.org is WordPress; its Bulletin Archives page links each issue as `ST.-JUDE-<MMDDYYYY>.pdf`. The row is `other` with `page-pdfs` pinned on that page.

 `fetch:check` (2026-11-13) picked `ST.-JUDE-11032026.pdf`, the newest issue posted (the 1 November issue; its filename makes `url_date` 2026-11-03), and rated it fresh.

## Not yet confirmed

The 8 November 2026 issue was not posted by 13 November (newest upload 28 October); the 1 November issue already lists Masses through 8 November. If no issue after 1 November appears by early December, check whether the parish moved its bulletin elsewhere.
