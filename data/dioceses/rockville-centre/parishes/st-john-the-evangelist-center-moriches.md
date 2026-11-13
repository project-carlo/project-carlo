---
name: St. John the Evangelist
website: http://www.stjohntheevangelistcm.com/sjecm/bulletin-archives
bulletin_provider: unsupported
provider_id: ''
publication: ['url:http://www.stjohntheevangelistcm.com/sjecm/bulletin-archives#st-john-the-evangelist']
group: ''
evidence:
- url: http://www.stjohntheevangelistcm.com/bulletins/bulletin_11_15_26.pdf
  seen: 2026-11-13
  quote: 25 Ocean Avenue, Center Moriches, New York, 11934-3968
  note: '15 November 2026 issue (24 pages, Adobe Acrobat Pro 2020; the same file is served as /bulletins/bulletin.pdf
    this week). Page 1 masthead: ''St. John the Evangelist Roman Catholic Church'', ''November 15, 2026'';
    Reverend Patrick M. Riegger, Pastor. Page 2 ''Masses for the Week'': Saturday 8:00 AM, 5:00 PM, 7:30
    PM (Spanish); Sunday 8:00 AM, 10:00 AM, 12:00 Noon, 6:00 PM; Monday 7:00 AM, 12:00 Noon. Back page:
    ''#263 FOR ADVERTISING: THE CHURCH BULLETIN INC.''.'
- url: http://www.stjohntheevangelistcm.com/sjecm/bulletin-archives
  seen: 2026-11-13
  note: 'Bulletin archive page (probe get): links /bulletins/bulletin.pdf (current) and dated issues /bulletins/bulletin_<m>_<d>_<yy>.pdf
    from 2025 to bulletin_11_15_26.pdf (one misnamed bulletin_11_81_26.pdf, presumably 8 November).'
research:
- method: fetch:check on the home page and pinned page-pdfs on the archive page; probe url on https://www.stjohntheevangelistcm.com/
  url: http://www.stjohntheevangelistcm.com/sjecm/bulletin-archives
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Set provider other with page-pdfs on the archive page once fetch's browser may load plain-http
    pages (or the parish serves https), then run fetch:check
  retry_when: fetch allows http navigation, or https://www.stjohntheevangelistcm.com/ presents a valid
    certificate
bulletin_status: available
fetch_gap:
  kind: http-only-site
  seen: 2026-11-13
  note: 'The site answers only on plain http (https presents a certificate for another host: ''Hostname
    mismatch''). fetch:check on 2026-11-13 failed before reading any page: ''Page.goto: net::ERR_BLOCKED_BY_CLIENT
    at http://www.stjohntheevangelistcm.com/'' (unpinned) and at /sjecm/bulletin-archives (pinned page-pdfs).
    probe get reads the page and PDFs over http.'
  url: http://www.stjohntheevangelistcm.com/bulletins/bulletin.pdf
---

## Publisher

St. John the Evangelist, 25 Ocean Avenue, Center Moriches publishes its own weekly bulletin, printed by The Church Bulletin Inc., West Babylon (back page "#263 FOR ADVERTISING: THE CHURCH BULLETIN INC."), which posts no copies online; the parish posts its own copy. The 15 November 2026 issue (`http://www.stjohntheevangelistcm.com/bulletins/bulletin_11_15_26.pdf`, also served this week as `/bulletins/bulletin.pdf`; read 2026-11-13; 24 pages, text layer readable) has the masthead "St. John the Evangelist Roman Catholic Church", "November 15, 2026", "25 Ocean Avenue, Center Moriches, New York, 11934-3968" and names Reverend Patrick M. Riegger, Pastor. No other parish is named; `group` is empty.

## Worship sites

One. Page 2's "Masses for the Week" lists Saturday 8:00 AM, 5:00 PM and 7:30 PM (Spanish), Sunday 8:00 AM, 10:00 AM, 12:00 Noon and 6:00 PM, and weekdays 7:00 AM and 12:00 Noon, with no place named; the Spanish notice puts the Saturday 7:30 Mass "en la iglesia". The Seton Chapel in the parish convent appears only for Exposition ("in Seton Chapel (Convent) Monday through Friday 3:00 - 7:00 PM"), a prayer group and an Altar of Remembrance, not for Mass, and Our Lady's Chapel is inside the church. All Masses are counted at the church (`st-john-the-evangelist-center-moriches-church`). The diocesan locator, GCatholic and the diocese's Mass-times page list only this church.

## Website and bulletin provider

www.stjohntheevangelistcm.com is a hand-built site served only over plain http: `probe url` on https fails with "Hostname mismatch, certificate is not valid for 'www.stjohntheevangelistcm.com'". The home page links `/bulletins/bulletin.pdf` (the current issue, overwritten weekly) and the archive page `/sjecm/bulletin-archives`, which also lists dated copies `bulletin_<m>_<d>_<yy>.pdf`. `fetch:check` (2026-11-13) failed before reading anything, on the home page unpinned and on the archive page pinned with `page-pdfs`: "Page.goto: net::ERR_BLOCKED_BY_CLIENT at http://…" (the fetch browser refuses plain-http navigation). The row is `unsupported` with `fetch_gap` `http-only-site`; the archive page is the website because its dated filenames let a collector choose by date.

## Not yet confirmed

Nothing open about the parish; the row waits on fetch reading plain-http pages, or on the parish fixing https.
