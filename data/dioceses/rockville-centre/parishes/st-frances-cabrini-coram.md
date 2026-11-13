---
name: St. Frances Cabrini
website: https://sfccoram.org/weekly-bulletin/
bulletin_provider: unsupported
provider_id: page-pdfs https://sfccoram.org/weekly-bulletin/ filename=SFC_Bulletin_2026*.pdf
publication: ['url:https://sfccoram.org/weekly-bulletin/']
group: ''
evidence:
- url: https://sfccoram.org/wp-content/uploads/sites/13/2026/11/SFC_Bulletin_20261115.pdf
  seen: 2026-11-13
  quote: 134 Middle Country Road, Coram, NY 11727
  note: '15 November 2026 issue (24 pages, Creator Microsoft Publisher 2019; no printer''s mark; downloaded
    in Chrome, probe get could not connect). Page 1 masthead: ''Saint Frances Cabrini R.C. Church, 134
    Middle Country Road, Coram, NY 11727''; ''Father Charles Mangano, Parish Administrator''; We Celebrate
    the Eucharist: Saturday 5:00 PM; Sunday 8:00 AM, 9:30 AM (Family Mass) & 11:00 AM, 1:00 PM (Spanish);
    Weekdays Monday through Thursday 8:00 AM; First Saturday 9:00 AM.'
- url: https://sfccoram.org/weekly-bulletin/
  seen: 2026-11-13
  note: 'WordPress (multisite, uploads/sites/13) Weekly Bulletin page read in visit.py (probe url: RemoteDisconnected):
    links SFC_Bulletin_<yyyymmdd>.pdf issues, not in date order (20261101, 20261108, 20261115, 20261004
    ...).'
- url: https://sfccoram.org/weekly-bulletin/
  seen: 2026-11-13
  note: 'fetch:check 2026-11-13: unpinned page-pdfs picked https://sfccoram.org/wp-content/uploads/sites/13/2023/11/SFC_Bulletin_20231119.pdf
    (link text ''November 19''); with filename=SFC_Bulletin_2026*.pdf it picked SFC_Bulletin_20261115.pdf,
    url_date 2026-11-15.'
research:
- method: fetch:check with and without a filename glob on the Weekly Bulletin page
  url: https://sfccoram.org/weekly-bulletin/
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check without a glob once the resolver prefers full filename dates over yearless
    link text; then set provider other and clear the gap
  retry_when: fetch's page-pdfs date choice changes, or the parish prunes old issues from the page
bulletin_status: available
fetch_gap:
  kind: link-text-date-misread
  seen: 2026-11-13
  note: The Weekly Bulletin page lists about 358 issues back to 2023, each linked with a yearless month-day
    text ('November 19'). fetch:check (2026-11-13) on the unpinned page picked SFC_Bulletin_20231119.pdf
    as 'current' (the 2023 link text read as 19 Nov 2026). With filename=SFC_Bulletin_2026*.pdf it picks
    SFC_Bulletin_20261115.pdf (url_date 2026-11-15), but that glob stops matching new issues in January
    2027, and a multi-year glob meets the same misread each November. A collector that prefers the filename's
    full date over yearless link text would read it.
  url: https://sfccoram.org/weekly-bulletin/
---

## Publisher

St. Frances Cabrini, 134 Middle Country Road, Coram makes its own weekly bulletin (15 November 2026 issue, `https://sfccoram.org/wp-content/uploads/sites/13/2026/11/SFC_Bulletin_20261115.pdf`, downloaded in Chrome 2026-11-13: 24 pages, Creator Microsoft Publisher 2019, no printer's mark). The page 1 masthead reads "Saint Frances Cabrini R.C. Church, 134 Middle Country Road, Coram, NY 11727" and names "Father Charles Mangano, Parish Administrator".

## Worship sites

One row: the church at 134 Middle Country Road (`st-frances-cabrini-coram-church`). "We Celebrate the Eucharist" (Saturday 5:00 PM; Sunday 8:00 AM, 9:30 AM (Family Mass), 11:00 AM, 1:00 PM (Spanish); Monday through Thursday 8:00 AM; First Saturday 9:00 AM) names no other place. The diocesan locator (directory:94), GCatholic (16828) and the Mass-times page list the same one church.

## Website and bulletin provider

sfccoram.org is WordPress; `probe url` and `probe get` could not connect (RemoteDisconnected) but `visit.py`, Chrome and `fetch:check` read it. The Weekly Bulletin page links about 358 `SFC_Bulletin_<yyyymmdd>.pdf` issues back to 2023, newest year first but out of date order within it, each with link text naming only the month and day ("November 19"). Unpinned, `fetch:check` (2026-11-13) picked the 19 November 2023 issue as current, reading its link text as 19 November 2026. With `filename=SFC_Bulletin_2026*.pdf` it picks the 15 November 2026 issue, but that glob stops matching in January, and a glob spanning years meets the same misread each November. So the row is `unsupported` with `fetch_gap` `link-text-date-misread`, keeping the working 2026 recipe in `provider_id`.

## Not yet confirmed

Nothing open.
