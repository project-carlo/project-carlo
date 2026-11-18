---
name: St. Barbara (Bushwick)
website: https://stbarbara-brooklyn.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery B2 (Brooklyn East)
evidence:
- url: https://stbarbara-brooklyn.org/bulletins
  seen: 2026-11-07
  quote: Bulletin for Sunday Aug. 30, 2026
  note: Tilma bulletins page, newest first. Newest card is 30 August 2026 (token decodes to upload 2026/08/25);
    before it uploads came every 1-3 weeks back to February 2026 (08/25, 08/11, 08/04, 07/21, 07/06, 06/16,
    ...). No card after 30 August on 2026-11-07, 74 days after the last upload.
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMDgvMjUvM2txN3IyNmg3c19TdEJhcl8wOF8zMF8yNl9CdWxsZXRpbi5wZGYiXV0/StBar%2008-30-26%20Bulletin.pdf
  seen: 2026-11-07
  quote: SATURDAY AND SUNDAY MASS INTENTIONS
  note: '30 August 2026 issue (file ''StBar 08-30-26 Bulletin.pdf''), 2 pages, self-made, no name masthead:
    parish finances, liturgy notes, groups and Mass intentions; no Mass schedule and the word ''Barbara''
    does not occur. Identified by its host site and file name.'
- url: https://parishesonline.com/organization/st-barbara-church-11221
  seen: 2026-11-07
  note: 'probe po st-barbara-church-11221: St. Barbara Church, 138 Bleecker St, website stbarbara-brooklyn.org,
    lpi 0018000000QxB7aAAF; no publications. Not a publication id (an org with no issues).'
- url: https://discovermass.com/church/st-barbara-brooklyn-ny/
  seen: 2026-11-07
  note: Discover Mass church page exists but lists no bulletins (issues.py discovermass).
- url: https://stbarbara-brooklyn.org/mass-times
  seen: 2026-11-07
  quote: Saturday (Vigil Mass)
  note: 'Mass Times page: Monday-Saturday 9:20am (Spanish); Saturday vigil 7:30pm (Spanish); Sunday 9:30am
    (English), 11:00am (Spanish), 12:30pm (Bilingual). No other church named; the site''s address is 138
    Bleecker Street.'
revisit: Recheck https://stbarbara-brooklyn.org/bulletins for an issue after 30 August 2026 (and probe
  po st-barbara-church-11221).
revisit_after: 2026-11-28
research:
- method: Read the Tilma /bulletins cards and decode upload tokens; probe po st-barbara-church-11221 (and
    -church, -roman-catholic-church-11221, bare slugs); issues.py discovermass st-barbara-brooklyn-ny
  url: https://stbarbara-brooklyn.org/bulletins
  checked: '2026-11-07'
  outcome: not-found
  next_action: Reread /bulletins; if cards after 30 August 2026 appear, set bulletin_provider other with
    provider_id 'page-pdfs https://stbarbara-brooklyn.org/bulletins', run fetch:check and confirm it picks
    a current issue; else probe po st-barbara-church-11221 again
  retry_when: A bulletin card dated after 30 August 2026 appears on /bulletins, or the LPi org st-barbara-church-11221
    lists issues
  revisit_after: 2026-11-28
bulletin_status: not-found
---

## Publisher

St. Barbara posted its own short bulletin (a self-made 2-page PDF with no name masthead) on its Tilma site through 30 August 2026, uploaded every one to three weeks since February 2026. The newest card on 2026-11-07 was still "Bulletin for Sunday Aug. 30, 2026" (uploaded 25 August), 74 days earlier: longer than any earlier gap, so it is treated as stopped for now. The 30 August issue carries parish finances, groups and Mass intentions and no schedule; it is identified by its host site and its file name ('StBar 08-30-26 Bulletin.pdf'). No other channel was found: the LPi org st-barbara-church-11221 lists no issues, and the Discover Mass page lists no bulletins.

## Worship sites

One: St. Barbara Church, 138 Bleecker Street. The site's Mass Times page (read 2026-11-07) lists weekday 9:20am, Saturday vigil 7:30pm and Sunday 9:30am, 11:00am and 12:30pm Masses and names no other place.

## Website and bulletin provider

`no_bulletin`, `bulletin_status: not-found`: no current issue on 2026-11-07. If posting resumes, the recipe is `other` with `page-pdfs https://stbarbara-brooklyn.org/bulletins` (Tilma, newest first); see research.

## Not yet confirmed

Whether the bulletin has stopped or is paused. Recheck /bulletins after 2026-11-28.
