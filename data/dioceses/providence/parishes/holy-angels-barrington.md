---
name: Holy Angels
website: https://www.holyangelschurchri.org/bulletin.html
bulletin_provider: other
provider_id: page-pdfs https://www.holyangelschurchri.org/bulletin.html
publication: ['url:https://www.holyangelschurchri.org/bulletin.html']
group: St. Luke and Holy Angels, Barrington (one pastor)
evidence:
- url: https://www.holyangelschurchri.org/uploads/1/3/6/6/136604749/holy_angels_bulletin__10_.pdf
  seen: 2026-11-14
  quote: OCTOBER 11 , 2026
  note: 'The issue the site''s Bulletin page links on 14 November 2026 (4 pages, text). Page 1: ''Holy
    Angels Church / 341 Maple Avenue, Barrington, RI 02806 / Weekend Mass / Saturday - 4:00 pm (Vigil)
    / Sunday - No Mass / Weekday Mass / Tuesday, Thursday - 12:05 pm'', then St Luke''s schedule, then
    ''Holy Angels Parish / 341 Maple Avenue / Barrington, Rhode Island 02806 ... Pastor / Fr. Marcel Taillon''.
    Page 3: ''Mass Intentions for the week / Saturday, October 10, 4:00pm ... Tuesday, October 13. 12:05pm
    ... Saturday, October 17, 4:00pm'' (Holy Angels Masses only).'
- url: https://www.holyangelschurchri.org/bulletin.html
  seen: 2026-11-14
  note: 'probe get: the Weebly ''Bulletin'' page links one PDF, /uploads/1/3/6/6/136604749/holy_angels_bulletin__10_.pdf
    (the file is replaced under a new number, not dated).'
- url: https://dioceseofprovidence.org/parishfinder
  seen: 2026-11-14
  note: 'Finder entry 12114 ''Holy Angels'', 341 Maple Ave., Barrington: ''Parochial Administrator: Rev.
    Marcel L. Taillon''; Saturday 4:00 PM; Tue Thu 12:05 PM. Read in a browser (details.json of 001-survey).'
revisit: Is Holy Angels' own bulletin still published? On 2026-11-14 its Bulletin page linked the 11 October
  2026 issue. If it is still stale, merge into st-luke-barrington (whose bulletin prints Holy Angels'
  schedule).
revisit_after: 2026-12-15
research:
- method: fetch:check with page-pdfs on the Bulletin page
  url: https://www.holyangelschurchri.org/bulletin.html
  checked: '2026-11-15'
  outcome: found
  next_action: Recheck that the Bulletin page posts an issue newer than 11 October 2026
  retry_when: After 2026-12-15, or when St. Luke's bulletin stops printing Holy Angels' schedule
bulletin_status: available
---

## Publisher

Holy Angels, Barrington posts its own bulletin on its Weebly site (https://www.holyangelschurchri.org/bulletin.html). The issue linked on 14 November 2026 is dated "OCTOBER 11 , 2026" (https://www.holyangelschurchri.org/uploads/1/3/6/6/136604749/holy_angels_bulletin__10_.pdf, 4 pages, text): page 1 heads "Holy Angels Parish / 341 Maple Avenue / Barrington, Rhode Island 02806" with "Pastor Fr. Marcel Taillon" and prints both Holy Angels' and St. Luke's schedules; page 3 gives Mass intentions for Holy Angels' Masses only (Saturday 4:00pm, Tuesday and Thursday 12:05pm).

Fr. Taillon is pastor of St. Luke and administrator here. St. Luke's own John Patrick bulletin (15 November 2026 issue) is a different, 12-page document headed "St. Luke's Parish", which also prints Holy Angels' schedule. I kept two rows because two documents with two mastheads exist (see `publication_reviews` on st-luke-barrington). This is a judgement: Holy Angels' latest posted issue is five weeks older than St. Luke's, so it may be irregular or lapsing.

## Worship sites

Holy Angels church, 341 Maple Ave. (finder 12114, GCatholic 22330). Nothing else.

## Website and bulletin provider

`other` with the recipe `page-pdfs https://www.holyangelschurchri.org/bulletin.html`. The page links a single PDF whose name carries no date. fetch:check on 2026-11-15 downloaded https://www.holyangelschurchri.org/uploads/1/3/6/6/136604749/holy_angels_bulletin__10_.pdf (text PDF; issue date and freshness 'unknown'), the 11 October 2026 issue read above: the right document, but not this week's.

## Not yet confirmed

Whether Holy Angels still issues its own bulletin weekly: the page linked the 11 October 2026 issue on 14 November 2026. Recheck the Bulletin page after 2026-12-15; if it still shows an October issue while St. Luke's continues weekly with Holy Angels' schedule, merge this row into st-luke-barrington and move the church there.
