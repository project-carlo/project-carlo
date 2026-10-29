---
name: Corpus Christi Parish
website: https://corpuschristilansdale.org
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1906
publication: ['url:http://sponsors.bonventure.net/?page=1906']
group: ''
evidence:
- url: http://sponsors.bonventure.net/?page=1906
  seen: 2026-10-28
  quote: Click to View Current Bulletin
  note: 'Bonventure sponsor page 1906: ''Corpus Christi, 900 Sumneytown Pike, Lansdale, PA 19446'', linking
    the parish site, a current-bulletin PDF (pdfs/1906/2026-11-01.pdf, posted ahead) and a dated archive
    back to 2025. Fetched over http:// (Bonventure sends no intermediate certificate).'
- url: http://sponsors.bonventure.net/pdfs/1906/2026-10-25.pdf
  seen: 2026-10-28
  quote: Reverend John D. Schiele
  note: '25 October 2026 issue (12 pages, text layer). Page 1: ''THIRTIETH SUNDAY IN ORDINARY TIME'',
    ''OCTOBER 25, 2026'', ''PASTOR Reverend John D. Schiele'', ''MAILING ADDRESS 900 Sumneytown Pike,
    Lansdale, PA 19446'', ''MASS SCHEDULE Daily Masses: 7:15 AM*, Saturday Masses: 7:15 AM* ... 4:30PM
    (Vigil Masses for Sunday), SUNDAY MASSES: 7:30 AM, 10:00 AM*, 11:30 AM, and 6:00 PM'', ''HOLY DAY
    MASSES: 7:30 PM (Vigil), 7:15 AM*, and 12:05 PM''.'
- url: https://corpuschristilansdale.org/resources/bulletins/
  seen: 2026-10-28
  quote: Proudly Designed and Hosted by John Patrick Publishing Company
  note: The parish site is hosted by John Patrick Publishing, but no John Patrick listing exists for it
    (ids 1-1300 scanned, none for Corpus Christi, Lansdale). The page body is empty in the REST API and
    the rendered page; the top menu's 'BULLETIN' link goes to the Bonventure sponsor page (browser link
    list, visit.py).
- url: https://archphila.org/parish/corpus-christi-lansdale/
  seen: 2026-10-28
  quote: Rev. John D. Schiele
  note: 'Directory: pastor Rev. John D. Schiele; 900 Sumneytown Pk., Lansdale 19446; parish center 215-855-1311.'
publication_reviews:
- parish: st-stanislaus-lansdale
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/1906/2026-10-25.pdf
    seen: 2026-10-28
    note: Corpus Christi's 25 October 2026 issue names its own pastor, Rev. John D. Schiele, at 900 Sumneytown
      Pike, with its own Mass schedule (Sunday 7:30, 10, 11:30 AM and 6 PM); it is a Bonventure issue,
      not the John Patrick one.
  - url: https://www.church-bulletin.org/bulletin/saint-stanislaus-roman-catholic-church-lansdale-pa-19446/2026-10-25.pdf
    seen: 2026-10-28
    note: St. Stanislaus's masthead names St. Stanislaus alone, Pastor Rev. Patrick J. Brady, with different
      Mass times (Sunday 7, 9, 11 AM, 1 PM Spanish).
---

## Publisher

Corpus Christi Parish, Lansdale (Rev. John D. Schiele, Pastor) publishes its bulletin through Bonventure, page 1906 (`sponsors.bonventure.net/?page=1906`), which the site's BULLETIN menu link names. It has no John Patrick listing although its site is John Patrick hosted. This is an `other` row (`page-pdfs` on the Bonventure page, over `http://`) as Allentown and Harrisburg record Bonventure parishes. The Bonventure page lists the next Sunday's issue (1 November 2026) before the date, so freshness can read `future`.

## Worship sites

One church, Corpus Christi Church, 900 Sumneytown Pike. The page-1 Mass schedule gives one set of times (asterisked Masses are livestreamed); no mission or chapel is named. The school (Corpus Christi School, ccslansdale.org) is not a worship site.

## Website and bulletin provider

corpuschristilansdale.org is a WordPress site hosted by John Patrick Publishing. `probe url` found no publication id; its Bulletins page is empty. The site header box is labelled "Mass Times (Summer)" (Sunday 7:30 AM, 10 AM, 6 PM, Saturday vigil 4:30 PM); the 25 October bulletin adds an 11:30 AM Sunday Mass, so the box is a seasonal schedule.

## Fetch check

`fetch:check` (2026-10-28) with `page-pdfs` on the Bonventure page picked `pdfs/1906/2026-11-01.pdf`, posted ahead of its date: transport ok, PDF, freshness `future` (-4 days), identity `unverified` (no expected identity supplied). Its page 1 text names 'Reverend John D. Schiele' as Pastor, so it is Corpus Christi's. The current 25 October issue (2026-10-25.pdf) is the fallback if future issues are rejected.

## Not yet confirmed

Pages 2-12 of the bulletin were not read.
