---
name: St. Martin de Porres
website: https://stmartindpparish.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs https://stmartindpparish.org/bulletins/
publication: ['url:https://stmartindpparish.org/bulletins/']
group: ''
evidence:
- url: https://stmartindpparish.org/wp-content/uploads/2026/10/30thSundatTheGreatestCommandment.pdf
  seen: 2026-10-29
  quote: SAINT MARTIN De PORRES CATHOLIC CHURCH
  note: 'Page 1 of the 25 October 2026 issue (4 pages, text layer): ''Weekday Masses In Chapel Wednesday
    & Thursday 9 am ... First Saturday of each month: 9 am in Chapel, Sunday Mass 10 am'', ''SAINT MARTIN
    De PORRES CATHOLIC CHURCH'', ''Parochial Administrator: Fr. Wilfred Emeh'', ''2340 W. Lehigh Ave.,
    Philadelphia, PA 19132, website: stmartindpparish.org, 215.228.8330''. It names this parish alone.'
- url: https://stmartindpparish.org/bulletins/
  seen: 2026-10-29
  quote: Bulletins
  note: 'The parish''s WordPress Bulletins page (behind a bot block: answers 403 to probe url and recheck;
    read in a browser with parish-site-access visit.py; the fetch pipeline reads it with the page-pdfs
    recipe) lists PDFs under wp-content/uploads/2026/<mm>/, newest first: 30thSundatTheGreatestCommandment.pdf
    (25 October), wms2026.pdf, TheParableoftheWeddingFeast1.pdf, RosaryOctoberBulletin.pdf, September-27-2026.pdf,
    September-202026-Bulletin.pdf, September-13-2026.pdf, Sept.-6-2026.pdf, August issues. File names
    are irregular and some are not bulletins (the Rosary file); probe pdf could not read wms2026.pdf or
    TheParableoftheWeddingFeast1.pdf.'
- url: https://www.church-bulletin.org/saint-martin-de-porres-church-philadelphia-pa-19132
  seen: 2026-10-29
  note: John Patrick Publishing listing 17 'Saint Martin de Porres Church, Philadelphia, PA 19132' exists
    but has no editions.
- url: https://archphila.org/parish/st-martin-de-porres-philadelphia/
  seen: 2026-10-28
  quote: Rev. Wilfred E. Emeh (pro tem) resides at Saint Malachy Philadelphia
  note: 'Directory page (updated 11 months before): 24th and Lehigh Ave.; rectory 2340 W. Lehigh Ave.
    19132; Vigil Saturday 5 PM, Sunday 10 AM, weekdays 7 AM (directory times are older than the bulletin''s).'
promoted: 2026-10-29
publication_reviews:
- parish: st-malachy-philadelphia
  decision: separate
  evidence:
  - url: https://stmalachyphilly.org/wp-content/uploads/2026/10/St.-Malachy-Bulletin-11012026-5.pdf
    seen: 2026-10-29
    note: The 1 November 2026 masthead names Saint Malachy Parish alone, with Rev. Matthew Biedrzycki,
      Pastor, 1429 N. 11th St. and Sunday Masses at 10AM and 7PM; page 4 announces a joint Forty Hours
      with the Temple Newman Center and St. Martin de Porres but is St. Malachy's own announcement list.
  - url: https://stmartindpparish.org/wp-content/uploads/2026/10/30thSundatTheGreatestCommandment.pdf
    seen: 2026-10-29
    note: 'The 25 October 2026 issue is a bulletin for Saint Martin de Porres Catholic Church alone: its
      page-1 masthead names Parochial Administrator Fr. Wilfred Emeh, 2340 W. Lehigh Ave., and its own
      Sunday Mass at 10 am. The directory says Fr. Emeh resides at St. Malachy, which is a shared residence,
      not a shared bulletin.'
---

## Publisher

St. Martin de Porres (2340 W. Lehigh Ave., North Philadelphia) posts its own bulletin PDFs on the Bulletins page of stmartindpparish.org. The 25 October 2026 issue (page 1) carries the parish name, Parochial Administrator Fr. Wilfred Emeh, the address and phone, and a Mass schedule for this church alone. John Patrick Publishing listing 17 has no editions.

The parish shares a priest with St. Malachy (Fr. Emeh resides at St. Malachy), and both bulletins list the Temple Newman Center's Masses and a joint Forty Hours (1-3 November), but each has its own masthead and Mass schedule: see St. Malachy's `publication_reviews`.

## Worship sites

One: St. Martin de Porres Church at 24th St. and Lehigh Ave. (`churches/st-martin-de-porres-philadelphia.md`). The bulletin's Mass schedule also lists the Temple Newman Center (Monday and Friday 12:10 pm, Thursday 5 pm); that is the row filed under St. Malachy (`churches/temple-newman-center-philadelphia.md`), not a second site here. Most Precious Blood of Our Lord (2800 Diamond St., closed 1993, records here) is excluded `closed`.

## Website and bulletin provider

`other` with `page-pdfs` on the Bulletins page. The page mixes bulletins with other PDFs and gives them irregular names, so freshness comes from `fetch:check` (below).

## Not yet confirmed

The page's file names do not date every October issue: 'TheParableoftheWeddingFeast1.pdf' is the 28th Sunday's Gospel (11 October) and 'wms2026.pdf' is not a bulletin I could read (probe pdf returned no text for either). No file is named for the 4 October Sunday. `fetch:check` picks the first link, the 25 October issue, so the pick is current; its freshness reads `unknown` only because the file name carries no date.
