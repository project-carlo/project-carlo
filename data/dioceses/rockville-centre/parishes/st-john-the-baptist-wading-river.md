---
name: St. John the Baptist
website: https://sjbwr.org/
bulletin_provider: other
provider_id: page-pdfs https://sjbwr.org/ filename=*_stjohnbaptwr*.pdf
publication: ['url:https://sjbwr.org/#st-john-the-baptist']
group: ''
evidence:
- url: https://sjbwr.org/wp-content/uploads/sites/19/2026/11/nov8_2026_stjohnbaptwr_compressed_compressed.pdf
  seen: 2026-11-13
  note: '8 November 2026 issue (16 pages, Creator Affinity 3.3.3, Producer iLovePDF; the text layer is
    symbol soup, so pages were read from renders). Page 1 cover (image): ''ST. JOHN THE BAPTIST CHURCH,
    1488 NORTH COUNTRY RD, WADING RIVER, NY 11792, SUNDAY, NOVEMBER 8, 2026''. Page 2: ''Pastor: Father
    Ralph Sommer''. Page 11 Mass intentions: Saturday 5:15 pm; Sunday 8:00 am and 10:30 am; Monday-Thursday
    8:30 am. Back page: ''#157 FOR ADVERTISING: THE CHURCH BULLETIN INC.''.'
- url: https://sjbwr.org/
  seen: 2026-11-13
  note: Home page (visit.py; probe url gets no answer) links the current issue, wp-content/uploads/sites/19/2026/11/nov8_2026_stjohnbaptwr_compressed_compressed.pdf;
    the 'General Information' page /archived-bulletins/ holds only 1978-1993 issues. WordPress media search
    for 'stjohnbaptwr' lists uploads named <mon><day>_<year>_stjohnbaptwr*.pdf (nov8, nov1, oct11, sept6
    2026 ...).
promoted: 2026-11-13
bulletin_status: available
---

## Publisher

St. John the Baptist, 1488 North Country Road, Wading River publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#157 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 8 November 2026 issue (`https://sjbwr.org/wp-content/uploads/sites/19/2026/11/nov8_2026_stjohnbaptwr_compressed_compressed.pdf`, read 2026-11-13; 16 pages) has the cover "ST. JOHN THE BAPTIST CHURCH, 1488 NORTH COUNTRY RD, WADING RIVER, NY 11792, SUNDAY, NOVEMBER 8, 2026" and names Father Ralph Sommer, Pastor (page 2). No other parish is named; `group` is empty. The text layer is garbled (Affinity export run through iLovePDF), so these were read from page renders.

## Worship sites

One. The Mass intentions on page 11 run Saturday 5:15 pm, Sunday 8:00 and 10:30 am, and Monday to Thursday 8:30 am, and the issue names no place but "Saint John's Church" (page 9). All Masses are counted at the church (`st-john-the-baptist-wading-river-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church.

## Website and bulletin provider

The diocese lists www.sjbwr.org and GCatholic www.stjohnthebaptistchurch.org, which redirects to sjbwr.org (a Red Penguin WordPress site; `probe url` gets no answer, `visit.py` reads it). The home page links the current issue as a self-hosted PDF named `<mon><day>_<year>_stjohnbaptwr…pdf`; the "archived bulletins" page holds only 1978-1993 issues. The row is `other` pinned with `page-pdfs https://sjbwr.org/ filename=*_stjohnbaptwr*.pdf`, which keeps the home page's other PDFs (calendars, forms) out. `fetch:check` (2026-11-13) picked the 8 November issue, the newest posted ("page-pdfs on https://sjbwr.org/: first-listed"), and reported the issue date unknown and "First page has no extractable text": the cover and text layer need OCR downstream.

## Not yet confirmed

The parish does not upload every week (media uploads include 8 and 1 November, 11 October and 6 September 2026), so the home page can stay on an older issue for a while.
