---
name: St. Michael (Flushing)
website: https://stmichaelsflushing.org/
bulletin_provider: other
provider_id: page-pdfs https://stmichaelsflushing.org/bulletins
publication: []
group: Deanery Q4 (Queens East)
evidence:
- url: https://stmichaelsflushing.org/system/resources/W1siZiIsIjIwMjYvMTAvMzAvOW5zc2Q5MmVnaF8yMDI2XzExXzAxLnBkZiJdXQ/2026-11-01.pdf
  seen: 2026-11-05
  quote: The Heart of Flushing (since 1833)
  note: 1 November 2026 issue, 8 pages. Page 1 masthead names Saint Michael's Roman Catholic Church /
    Iglesia Catolica de San Miguel (and its Chinese name), 138-65 Barclay Ave, Flushing, NY 11355, www.StMichaelsFlushing.org.
    Page 2 gives the pastoral team (Pastor Rev. Vincentius Do) and one MASS SCHEDULE in English, Spanish
    and Chinese for this church alone.
- url: https://stmichaelsflushing.org/bulletins
  seen: 2026-11-05
  note: Tilma bulletins page on the parish's own domain, newest first (November 01, 2026; October 25,
    2026; ...), one card a week, each linking /system/resources/<token>/<YYYY-MM-DD>.pdf. One trilingual
    issue a week; no separate language editions are listed.
research:
- method: fetch:check with recipe 'page-pdfs https://stmichaelsflushing.org/bulletins'; picked 2026-11-01.pdf
    (1 November 2026, freshness fresh) on Thursday 5 November, before the 8 November card was posted
  url: https://stmichaelsflushing.org/bulletins
  checked: '2026-11-05'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks the 8 November issue
  retry_when: After the weekend of 7-8 November 2026
  revisit_after: 2026-11-09
bulletin_status: available
---

## Publisher

St. Michael publishes its own weekly bulletin on its Tilma site (stmichaelsflushing.org/bulletins). The 1 November 2026 issue (read 2026-11-05, the newest posted) has on page 1 "Saint Michael's Roman Catholic Church / Iglesia Católica de San Miguel" with its Chinese name, "The Heart of Flushing (since 1833)", "138-65 Barclay Ave, Flushing, NY 11355"; page 2 names Pastor Rev. Vincentius Do.

## Worship sites

One church. Page 2's MASS SCHEDULE (given in English, Spanish and Chinese) lists Monday-Saturday 8:30 AM (English), Thursday and First Friday 7:00 PM (Spanish), Saturday 5:15 PM (English) and 7:00 PM (Spanish), Sunday 9:00 AM (Spanish), 11:00 AM (English), 12:30 PM (Chinese), 2:30 PM (Spanish), and Third Sunday 7:30 AM (Tagalog), naming no other church. The rectory at 136-76 41st Avenue is an office. The diocese directory, deanery list, GCatholic 16754 and Mass finder 1107 list only this church.

## Language editions

The bulletin is a single trilingual issue (English, Spanish, Chinese); the bulletins page lists one card a week and no separate language editions.

## Website and bulletin provider

`other`, pinned to the Tilma bulletins page (`page-pdfs https://stmichaelsflushing.org/bulletins`). PDFs are served from the parish domain under /system/resources/<token>/ and named by date (2026-11-01.pdf).

## Not yet confirmed

On 2026-11-05 the newest issue posted was 1 November; see research for the recheck after the weekend.
