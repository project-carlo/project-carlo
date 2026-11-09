---
name: St. Francis de Sales
website: https://stfrancis96.org/
bulletin_provider: other
provider_id: page-pdfs https://stfrancis96.org/bulletin
publication: ['url:https://stfrancis96.org/bulletin']
group: ''
evidence:
- url: https://stfrancis96.org/s/Bulletin-8-November-2026.pdf
  seen: 2026-11-08
  quote: November 8, 2026
  note: Page 1 of the 11-page 8 November 2026 issue; masthead names St. Francis de Sales; page 2 intentions
    'For the parish of St. Francis de Sales'; page 11 gives 135 East 96th Street.
- url: https://stfrancis96.org/bulletin
  seen: 2026-11-08
  quote: NOVEMBER 8, 2026
  note: First link on the bulletin page, to /s/Bulletin-8-November-2026.pdf; the next ones (November 1
    back to August 9) link Elvanto /file/<UUID>/ addresses, then June-August Squarespace /s/ PDFs.
- url: https://tithely-5e3b3d31cd9bd-316835.elvanto.net/file/dfcfb05e-a1c4-4015-a703-3a25c87cc5bb
  seen: 2026-10-31
  quote: November 1, 2026
  note: Page 1 of the 17-page 1 November 2026 issue, an Elvanto file with no .pdf in its address.
revisit: 'Check that the November 15 and 22 issues are again Squarespace /s/Bulletin-<d>-<Month>-2026.pdf
  links at the top of https://stfrancis96.org/bulletin. If the parish goes back to Elvanto /file/<UUID>/
  links, the recipe will keep picking the last Squarespace PDF: set bulletin_provider unsupported with
  fetch_gap kind extensionless-download-link.'
revisit_after: 2026-11-23
promoted: 2026-11-09
research:
- method: check_fetch on a hypothetical row, provider other, no recipe (then fetch:check on the written
    row)
  url: https://stfrancis96.org/s/Bulletin-8-November-2026.pdf
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. Francis de Sales (135 East 96th Street) publishes its own weekly bulletin, listed newest first on https://stfrancis96.org/bulletin. Issues read: October 4, 2026 (Elvanto file, read October 8: page 1 masthead Saint Francis de Sales Catholic Church), November 1, 2026 (Elvanto file, 17 pages, read October 31) and November 8, 2026 (https://stfrancis96.org/s/Bulletin-8-November-2026.pdf, 11 pages, read November 8: page 1 "November 8, 2026", page 2 Masses "For the parish of St. Francis de Sales", page 11 "135 East 96th Street"). No other church is in the schedule.

## Worship sites

One: St. Francis de Sales, 135 East 96th Street (`churches/st-francis-de-sales-new-york-city.md`). The issues give Sunday 9:00 am, 11:00 am and 12:30 pm Spanish, and weekdays 8:30 am Monday, Tuesday, Thursday and Friday.

## Website and bulletin provider

The bulletin page has carried issues in two forms. June to early August 2026 and again November 8 are Squarespace PDFs (`/s/Bulletin-8-November-2026.pdf`, `/s/_Bulletin-2-August-2026.pdf`); August 9 to November 1 are Elvanto files (`tithely-...elvanto.net/file/<UUID>/`) with no .pdf in the address, which page-pdfs skips. On October 8 and October 31 the unpinned resolver therefore took the August 2 Squarespace PDF, and linked-issue-page, dated-post and redirected-pdf found no PDF (October 31). On November 8 the newest link is a Squarespace PDF again, and page-pdfs picked it ("current"), so the row is `other` with the recipe `page-pdfs https://stfrancis96.org/bulletin` pinned.

The risk is a return to Elvanto: page-pdfs would then keep picking the November 8 file, a stale issue rather than a failure. `revisit_after` checks the next two weeks; if Elvanto links come back, the row becomes `unsupported` with `fetch_gap` kind `extensionless-download-link`.

## Not yet confirmed

Whether the parish keeps posting Squarespace PDFs after November 8 (see revisit).
