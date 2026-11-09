---
name: St. Paul - Bullville
website: https://stpaulsbullville.org
bulletin_provider: unsupported
provider_id: page-pdfs https://stpaulsbullville.org/bulletins/
publication: ['url:https://stpaulsbullville.org/bulletins/']
group: ''
evidence:
- url: https://stpaulsbullville.org/wp-content/uploads/October-4.pdf
  seen: 2026-10-08
  quote: OCTOBER 4, 2026
  note: Current parish-hosted issue, page 1; downloaded from the parish bulletin page.
- url: https://stpaulsbullville.org
  seen: 2026-10-08
  quote: MASS SCHEDULE 5 p.m. Saturday and 10 a.m. Sunday.
  note: Official St. Paul Bullville homepage, read October 8, with the 2800 Route 17K contact panel.
- url: https://stpaulsbullville.org/wp-content/uploads/November-8.pdf
  seen: 2026-11-08
  quote: NOVEMBER 8, 2026
  note: Listed first on https://stpaulsbullville.org/bulletins/ on November 8, 2026; this is the current
    issue. fetch:check with page-pdfs on that page instead picked https://stpaulsbullville.org/wp-content/uploads/November-14.pdf,
    whose page 1 reads 'NOVEMBER 14, 2021'.
research:
- method: fetch:check --parish st-paul-bullville with the pinned recipe page-pdfs https://stpaulsbullville.org/bulletins/
  url: https://stpaulsbullville.org/bulletins/
  checked: '2026-11-08'
  outcome: unsupported-format
  next_action: When a collector or chooser option can take the first-listed PDF on a yearless Month-D
    archive (or reads the year from the PDF), set bulletin_provider other with that recipe, re-run fetch:check
    and clear fetch_gap once it picks this week's issue.
  retry_when: A collector for the yearless-filename-archive gap kind lands
fetch_gap:
  kind: yearless-filename-archive
  seen: 2026-11-08
  note: The /bulletins page lists every issue since about 2021 newest first as wp-content/uploads/<Month>-<D>.pdf
    with no year (November-8.pdf is the 8 November 2026 issue). The page-pdfs chooser reads each name
    as this year's date and takes the latest within a week, so on 2026-11-08 it picked November-14.pdf,
    the 14 November 2021 issue; every week an older year's file with a later day wins. Only 'first listed'
    would be right, and no recipe forces it.
  url: https://stpaulsbullville.org/bulletins/
---

## Publisher

The official St. Paul Bullville bulletin page links the parish-hosted October-4.pdf. Page 1 dates it October 4, 2026; its Mass intentions and parish council notices match the live site. This is a standalone parish-hosted publication, not an account inferred from a nearby St. Paul.

## Worship sites

The official homepage identifies St. Paul Roman Catholic Church, 2800 Route 17K, Bullville, with Saturday 5 PM and Sunday 10 AM public Mass. The current issue also reports attendance for those two services.

## Website and bulletin provider

The parish posts its weekly bulletin on /bulletins as parish-hosted PDFs named <Month>-<D>.pdf with no year, newest first, and the page keeps every issue back to about 2021. The November 8, 2026 issue (November-8.pdf) was listed first on November 8. The page-pdfs chooser reads every name as this year's date, so fetch:check picked November-14.pdf, the November 14, 2021 issue; an older year's file with a later day will win almost every week. No recipe forces the first-listed file, so the row is `unsupported` with a `yearless-filename-archive` fetch_gap until a collector can read it. The bulletin itself is current and published weekly.
