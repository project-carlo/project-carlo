---
name: Most Holy Trinity - St. Mary
website: https://www.trinity-stmary.org/
bulletin_provider: other
provider_id: page-pdfs https://www.trinity-stmary.org/past-bulletins
publication: ['url:https://www.trinity-stmary.org/past-bulletins']
group: Deanery B1 (Brooklyn West)
evidence:
- url: https://www.trinity-stmary.org/_files/ugd/da068c_0336a29d1a4348a394c4227b1340c734.pdf
  seen: 2026-11-07
  quote: NOVEMBER 8, 2026
  note: '8 November 2026 bulletin (5 pages, Canva, created 2026-11-04). Page 1: 32ND SUNDAY IN ORDINARY
    TIME, NOVEMBER 8, 2026, team led by Friar Rick Richard Riccioli, OFM Conv., Pastor; welcome text names
    Most Holy Trinity Church near Montrose Avenue, joined by St. Mary''s, united in 2007 as Most Holy
    Trinity-St. Mary Parish. The Mass intentions page gives Sunday 8:00 AM (POL), 9:30 AM (ENG), 11:00
    AM (ESP), 12:30 PM (ENG), weekdays 8:30 AM, with no other church named. Contact block: Parish Office
    718-384-0215, 153 Johnson Avenue Door B, trinity-stmary.org. No LPi, John Patrick or Church Bulletin
    Inc. footer; self-made.'
- url: https://www.trinity-stmary.org/past-bulletins
  seen: 2026-11-07
  quote: november 8, 2026
  note: 'Wix Past Bulletins page lists weekly issues newest first: November 8, November 1, October 25,
    October 18, October 11, October 4, 2026, and back through August. The /bulletin page shows the current
    issue in a certifiedcode.io PDF viewer iframe whose pdfUrl is the same ugd file.'
research:
- method: pnpm fetch:check with page-pdfs https://www.trinity-stmary.org/past-bulletins
  url: https://www.trinity-stmary.org/past-bulletins
  checked: '2026-11-07'
  outcome: found
  next_action: If fetch returns an issue more than two weeks old, read the Past Bulletins list; the parish
    has posted weekly.
  revisit_after: 2027-02-01
bulletin_status: available
---

## Publisher

Most Holy Trinity - St. Mary (St. Mary's united with Most Holy Trinity in 2007), a Conventual Franciscan parish, publishes its own weekly trilingual (English, Spanish, Polish) bulletin, made in Canva, on its Wix site. The 8 November 2026 issue (5 pages, read 2026-11-07, https://www.trinity-stmary.org/_files/ugd/da068c_0336a29d1a4348a394c4227b1340c734.pdf) has on page 1 "32ND SUNDAY IN ORDINARY TIME", "NOVEMBER 8, 2026" and the parish team under Friar Rick (Richard Riccioli, OFM Conv.), Pastor; its welcome text names "Most Holy Trinity Church" near Montrose Avenue, "later joined by St. Mary's, established for Irish immigrants, these two communities were united in 2007 as Most Holy Trinity–St. Mary Parish". The contact block gives the parish office at 153 Johnson Avenue Door B, 718-384-0215, trinity-stmary.org. There is no name masthead beyond that and no LPi, John Patrick or Church Bulletin Inc. footer.

## Worship sites

One church, Most Holy Trinity, 138 Montrose Avenue. The issue's Mass intentions page gives Sunday 8:00 AM (Polish), 9:30 AM (English), 11:00 AM (Spanish) and 12:30 PM (English), weekdays 8:30 AM, and a Wednesday and Friday 7:00 PM Mass, with no other church named. The former St. Mary's church is not named as a Mass site in the issue, and no roster lists it: the directory, the deanery list, GCatholic 16622 ("Holy Trinity and St. Mary", 138 Montrose Ave.) and the Mass finder 321 all give 138 Montrose Avenue only.

## Website and bulletin provider

`other` with the recipe `page-pdfs https://www.trinity-stmary.org/past-bulletins`. The site's /bulletin page shows only the current issue in a certifiedcode.io PDF viewer iframe (no link in the HTML, so the resolver finds no PDF there); the Past Bulletins page links each issue as a Wix `_files/ugd/<id>.pdf`. `fetch:check` on 2026-11-07 resolved "page-pdfs on https://www.trinity-stmary.org/past-bulletins: current" and downloaded https://www.trinity-stmary.org/_files/ugd/da068c_0336a29d1a4348a394c4227b1340c734.pdf, the 8 November 2026 issue. GCatholic's website mhtbrooklyn.org answers but has no parish words in its HTML (probe url NO-PARISH-WORDS, 2026-11-07); the directory's trinity-stmary.org is current.

## Not yet confirmed

Nothing open for the row. Where the former St. Mary's church stood and what became of it was not researched: no roster entry names it, and the bulletin names no Mass there.
