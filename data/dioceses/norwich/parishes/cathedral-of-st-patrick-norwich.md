---
name: Cathedral of St. Patrick
website: https://www.cathedralofsaintpatrick.org/Resources/Sunday-Bulletin
bulletin_provider: other
provider_id: page-pdfs https://www.cathedralofsaintpatrick.org/Resources/Sunday-Bulletin
publication: ['url:https://www.cathedralofsaintpatrick.org/Resources/Sunday-Bulletin#cathedral-of-st-patrick-norwich']
group: ''
evidence:
- url: https://www.cathedralofsaintpatrick.org/LinkClick.aspx?fileticket=yJXFp4SqP2U%3d&tabid=3023&portalid=40&mid=6178
  seen: 2026-11-14
  note: 'Page 1 (an image, read with render.py; the issue has no text layer) of the November 15, 2026
    bulletin: ''The Cathedral of Saint Patrick, 213 BROADWAY, NORWICH, CT 06360'', Rector Rev. Brian Romanowski;
    Celebration of the Eucharist: Saturday Vigil 5:00 p.m., Sunday 7:30, 9:00, 10:30 a.m. and 5:00 p.m.,
    daily Mon-Fri 7:00 a.m. and 12:00 p.m., Saturday 7:00 a.m. No other church is named.'
- url: https://www.cathedralofsaintpatrick.org/Resources/Sunday-Bulletin
  seen: 2026-11-14
  quote: November 15, 2026
  note: 'Connecting Members (DNN) Sunday Bulletin page: a Documents table of LinkClick.aspx?fileticket=
    downloads, newest first, one per Sunday from August 23 to November 15, 2026.'
promoted: 2026-11-14
research:
- method: probe pdf of the November 15, 2026 issue
  url: https://www.cathedralofsaintpatrick.org/LinkClick.aspx?fileticket=yJXFp4SqP2U%3d&tabid=3023&portalid=40&mid=6178
  checked: '2026-11-14'
  outcome: unsupported-format
  next_action: Check that the pipeline OCRs the scanned issue and gets the Mass schedule from page 1
  retry_when: The row is first extracted after promotion
bulletin_status: available
---

## Publisher

The Cathedral of St. Patrick, Norwich publishes its own bulletin on its Connecting Members (DNN) site. The November 15, 2026 issue (read 2026-11-14) is a scanned 8-page PDF with no text layer; page 1, read as an image with render.py, is headed "THE MOST REVEREND RICHARD F. REIDY, BISHOP OF NORWICH / The Cathedral of Saint Patrick / 213 BROADWAY, NORWICH, CT 06360", with Rector Rev. Brian Romanowski and Rector Emeritus Msgr. Anthony S. Rosaforte. The diocese's List of Parishes (March 6, 2026) still names Msgr. Rosaforte as rector; the bulletin is newer.

## Worship sites

Page 1's "Celebration of the Eucharist" lists the cathedral alone: Saturday Vigil 5:00 p.m.; Sunday 7:30, 9:00, 10:30 a.m. and 5:00 p.m.; Mon-Fri 7:00 a.m. and 12:00 p.m.; Saturday 7:00 a.m.; Blessed Virgin Novena Mass Monday 7:00 p.m. No mission or chapel is named. GCatholic's Norwich church list omits the cathedral; the diocese's list and locator map have it.

## Website and bulletin provider

www.cathedralofsaintpatrick.org/Resources/Sunday-Bulletin is a DNN Documents table of `LinkClick.aspx?fileticket=` links titled by date, newest first. No ParishesOnline id appears on the page and the PDF is a scan with no footer text, so the row is `other`. The bulletin is image-only: the pipeline has to read it as images.

fetch:check (2026-11-14) picked the November 15, 2026 issue with recipe page-pdfs on the Sunday Bulletin page ("current"), which is pinned in `provider_id`. It could not verify identity or date because page 1 has no text.

## Not yet confirmed

Whether the pipeline's text extraction gets the Mass times from an image-only issue; see research.
