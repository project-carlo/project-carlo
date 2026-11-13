---
name: Our Lady of Czestochowa - St. Casimir (South Slope)
website: http://olcbrooklyn.org/
bulletin_provider: other
provider_id: page-pdfs http://olcbrooklyn.org/
publication: []
group: Deanery B4 (Brooklyn West)
evidence:
- url: http://olcbrooklyn.org/p.pdf
  seen: 2026-11-06
  quote: 183 - 25th Street Brooklyn, N.Y. 11232
  note: 'The site''s one bulletin file, holding the 8 November 2026 issue (''Sunday November 8, 2026 Niedziela,
    8 listopada 2026''; 8 pages, 4 with text, self-made, no LPi or Church Bulletin Inc. footer). Page
    1 masthead (rendered; the title is an image) ''Our Lady of Czestochowa ~ St. Casimir Church'', pastor
    ''Rev. Janusz Dymek Ph.D. Pastor''; SCHEDULE OF MASSES: weekdays 7:00 AM Polish, 12:10 PM English;
    Sundays 8:00 AM, 11:00 AM & 6:30 PM Polish, 9:30 AM English; Saturday 7:00 AM Polish (and the site
    lists 5:00pm Vigil Mass in English).'
- url: http://olcbrooklyn.org/
  seen: 2026-11-06
  note: 'Parish homepage (one page, hand-built HTML): ''Bulletin'' links p.pdf; Masses: Sunday POL 8:00am,
    11:00am, 6:30pm, ENG 9:30am; Saturday POL 7:00am, ENG 5:00pm - Vigil Mass; contact 183 25th Street,
    Brooklyn, NY 11232.'
promoted: 2026-11-12
research:
- method: fetch:check other on the homepage
  url: http://olcbrooklyn.org/
  checked: '2026-11-06'
  outcome: found
- method: 'Reconcile: headed fetch:check (PLAYWRIGHT_BROWSER_CHANNEL=chrome under xvfb) failed twice with
    ''net::ERR_BLOCKED_BY_CLIENT at http://olcbrooklyn.org/''; the same check without the Chrome channel
    picked http://olcbrooklyn.org/p.pdf, whose text has ''November 8, 2026'''
  url: http://olcbrooklyn.org/p.pdf
  checked: '2026-11-12'
  outcome: found
  next_action: If the production fetch runs headed Chrome, check that it reaches this plain-http site;
    https://olcbrooklyn.org/ gave no answer
  retry_when: A weekly fetch reports resolve_failed for this parish
bulletin_status: available
---

## Publisher

The parish publishes its own weekly bilingual (Polish/English) bulletin and posts it on its homepage as one file, `p.pdf`, overwritten each week. I read it on 2026-11-06, when it held the 8 November 2026 issue: page 1 masthead "Our Lady of Czestochowa ~ St. Casimir Church", "183 - 25th Street Brooklyn, N.Y. 11232", pastor Rev. Janusz Dymek. The masthead title and pages 2, 3, 5 and 8 are images (read with render.py); there is no publisher footer, so no publication id.

## Worship sites

One church, at 183 25th Street. The issue's SCHEDULE OF MASSES (weekdays 7:00 AM Polish and 12:10 PM English; Sundays 8:00, 11:00 AM and 6:30 PM Polish, 9:30 AM English; Saturday 7:00 AM Polish) names no other building; the homepage adds the 5:00pm English Saturday Vigil. The diocese's directories, GCatholic 16630 and Mass finder 1128 list only this address; no source I read names a separate St. Casimir building.

## Website and bulletin provider

`other`, recipe `page-pdfs http://olcbrooklyn.org/`. `fetch:check` (2026-11-06) picked `http://olcbrooklyn.org/p.pdf` ("page-pdfs on http://olcbrooklyn.org/: titled"), transport ok, a PDF; issue date and freshness `unknown`, because the file name carries no date and the issue date sits beside the image masthead. I read the file the same day: it is the 8 November 2026 issue. As one fixed, weekly-overwritten file, staleness can only be checked by reading the date line on page 1.

## Not yet confirmed

Nothing open.
