---
name: St. Clare (Rosedale)
website: https://stclare-queens.org/bulletins
bulletin_provider: other
provider_id: page-pdfs https://stclare-queens.org/bulletins
publication: []
group: Deanery Q9 (Queens East)
evidence:
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTEvMDIvNzYycDJiNzJwMF9Ob3ZlbWJlcl8xc3RfMjAyNl9zdGNsYXJlLnBkZiJdXQ/November%201st%2C%2C%202026%20--stclare.pdf
  seen: 2026-11-06
  quote: 'Sundays: 8am & 11:00am Masses'
  note: '1 November 2026 issue (7 pages, text). Page 1 masthead ''St. Clare Catholic Church / The Very
    Reverend Daniel O. Kingsley, Pastor / Address: 137-35 Brookville Boulevard, Rosedale, NY 11422'';
    Mass Schedule ''Monday-Saturday: 8:30am Saturday Vigil: 5pm''. No other church is named; St. Pius
    X does not appear in the issue (grep ''Pius'': 0). No LPi or Church Bulletin Inc. footer: the parish
    produces it.'
- url: https://stclare-queens.org/bulletins
  seen: 2026-11-06
  note: 'Tilma bulletins page (server-rendered), cards newest first: ''November 1st,, 2026 --stclare.pdf'',
    October 25th, 18th, 11th, 4th, September 27th... weekly back to July 2026, each a files.tilmaplatform.com
    PDF.'
research:
- method: fetch:check page-pdfs on the Tilma bulletins page
  url: https://stclare-queens.org/bulletins
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks the 8 November 2026 issue
  retry_when: After the 8 November 2026 issue is posted
  revisit_after: 2026-11-10
bulletin_status: available
---

## Publisher

St. Clare publishes its own weekly bulletin and posts it on its Tilma site's bulletins page. I read the 1 November 2026 issue (read 2026-11-06): page 1 masthead "St. Clare Catholic Church / The Very Reverend Daniel O. Kingsley, Pastor / Address: 137-35 Brookville Boulevard, Rosedale, NY 11422". The issue has no LPi or Church Bulletin Inc. footer, so the parish makes it itself; no publication id exists beyond the page.

## Worship sites

One church. Page 1's Mass Schedule gives "Monday-Saturday: 8:30am Saturday Vigil: 5pm / Sundays: 8am & 11:00am Masses" and names no other place. Fr. Kingsley is also pastor of St. Pius X, Rosedale, but this issue never mentions St. Pius X, which has its own row (`st-pius-x-rosedale`) and its own bulletin page. St. Clare Catholic Academy (137-25 Brookville Blvd) is a school. The directory, the deanery list (Q9), GCatholic 16697 and Mass finder 628 list this one church.

## Website and bulletin provider

`other`, `page-pdfs https://stclare-queens.org/bulletins` (Tilma; the PDFs are on files.tilmaplatform.com). `fetch:check` (2026-11-06) resolved "page-pdfs on https://stclare-queens.org/bulletins: current" and picked the 1 November 2026 issue (issue date 2026-11-01, freshness fresh), the newest on the page; that is the recipe recorded. GCatholic's website for the church, stclareqns.com, is an older domain; the directory and the bulletin give stclare-queens.org.

## Not yet confirmed

That fetch picks the 8 November issue once it is posted: see `research`.
