---
name: St. Pius X (Rosedale)
website: https://stpiusx-queens.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q9 (Queens East)
evidence:
- url: https://stpiusx-queens.org/bulletins
  seen: 2026-11-06
  note: Tilma bulletins page (server-rendered), cards newest first; the newest is 'p 06-28-26.pdf' (uploaded
    2026-06-26), then 06-21-26, 06-14-26 ... weekly from 01-18-26. No card after 28 June 2026, and no
    'Bulletin for' card pending (/bulletins/null).
- url: https://stpiusx-queens.org/system/resources/W1siZiIsIjIwMjYvMDYvMjYvNTc3and0MXY4MV9wXzA2XzI4XzI2LnBkZiJdXQ/p%2006-28-26.pdf
  seen: 2026-11-06
  quote: SUNDAY, JUNE 28TH, 2026
  note: 'Newest posted issue (6 pages, text). Page 1 is the intentions page, no masthead: ''MASSES FOR
    THE WEEK'' with Saturday 5:00, Sunday 10:00 and 1:00, weekdays 9:00, for 20-27 June 2026; page 3 ''From
    Fr. Kingsley''. No other church named, St. Clare not mentioned (grep ''Clare'': 0); no LPi or Church
    Bulletin Inc. footer.'
- url: https://stpiusx-queens.org/about/mass-times
  seen: 2026-11-06
  quote: 'Haitian Creole: 1 p.m.'
  note: 'Parish site Mass Times: Monday - Friday English 9 a.m.; Saturday English 5 p.m. (Vigil); Sunday
    English 10 a.m., Haitian Creole 1 p.m.'
- url: https://parishesonline.com/organization/st-pius-x-church-11422
  seen: 2026-11-06
  note: 'probe po: org ''St. Pius X Church'' (lpi 0018000000QxBA1AAN) has no issues; an empty org, not
    a publication id.'
- url: https://discovermass.com/church/st-pius-x-rosedale-ny/
  seen: 2026-11-06
  note: Discover Mass listing exists; its HTML links no bulletin and no website.
research:
- method: probe get of the Tilma bulletins page, then fetch:check page-pdfs https://stpiusx-queens.org/bulletins
  url: https://stpiusx-queens.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: 'Reread /bulletins for a card newer than 28 June 2026; if issues resume, set bulletin_provider
    other with provider_id ''page-pdfs https://stpiusx-queens.org/bulletins'' and rerun fetch:check (on
    2026-11-06 it resolved ''page-pdfs ... : first-listed'' and picked p 06-28-26.pdf, freshness unknown).
    Also check the St. Clare bulletin for a combined issue under the shared pastor and the parish''s social
    media for posted bulletins.'
  retry_when: A bulletin newer than 28 June 2026 appears on the parish site, or St. Clare's bulletin starts
    carrying St. Pius X
  revisit_after: 2026-12-07
bulletin_status: not-found
---

## Publisher

St. Pius X made its own weekly bulletin and posted it on its Tilma site's bulletins page through the 28 June 2026 issue; nothing has been posted since (checked 2026-11-06, over four months later). The newest issue, "SUNDAY, JUNE 28TH, 2026" (`p 06-28-26.pdf`, read 2026-11-06), opens with the week's Mass intentions rather than a masthead and has a page 3 letter "From Fr. Kingsley"; it has no publisher footer. The Very Rev. Daniel O. Kingsley is also pastor of St. Clare, Rosedale, but St. Clare's 1 November 2026 bulletin does not mention St. Pius X, so St. Clare's bulletin does not cover this church. ParishesOnline's `st-pius-x-church-11422` org is empty and Discover Mass links no bulletin.

## Worship sites

One church, 148-10 249th Street. The June issue's intentions and the parish site's Mass Times page (read 2026-11-06) agree: Monday-Friday 9 a.m., Saturday 5 p.m. (Vigil), Sunday 10 a.m. and 1 p.m. (Haitian Creole). The directory, deanery list (Q9), GCatholic 16767 and Mass finder 819 list this one church.

## Website and bulletin provider

`no_bulletin` for now: no current bulletin was found, and the bulletins page still serves the June issue, which `fetch:check` (2026-11-06, as `other` with `page-pdfs https://stpiusx-queens.org/bulletins`) picked as "first-listed" with freshness `unknown`, so it would have gone live with a four-month-old issue. The website is kept as the bulletins page, where issues would reappear; the recipe above reads it if they do.

## Not yet confirmed

Whether St. Pius X still publishes a bulletin anywhere (a paper-only issue, social media, or a combined issue with St. Clare): see `research` (recheck after 2026-12-07).
