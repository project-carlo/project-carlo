---
name: St. Rose of Lima Parish
website: http://www.srol.org
bulletin_provider: other
provider_id: page-pdfs https://www.srol.org/news-and-events/bulletins/
publication: ['url:https://www.srol.org/news-and-events/bulletins/']
group: ''
evidence:
- url: https://www.srol.org/assets/Uploads/30thbulletin2.pdf
  seen: 2026-10-28
  quote: The mission of Saint Rose of Lima Parish is to live the Gospel of Jesus Christ
  note: 'Page 1 of the 25 October 2026 issue (12 pages, text layer; printed by Bon Venture Services, footer
    "I22564 (PK) - St. Rose of Lima, North Wales"). Its Mass Schedule: Saturday Vigil 4:00 p.m.; Sunday
    8:00 a.m., 9:30 a.m. & 11:30 a.m.; Monday - Saturday 8:30 a.m.; Holy Day vigil 7:00 p.m., Holy Day
    8:30 a.m. Clergy: Rev. Bernard J. Taglianetti, Pastor.'
- url: https://www.srol.org/news-and-events/bulletins/
  seen: 2026-10-28
  quote: 'Weekly Bulletin Dated:'
  note: 'The parish''s own Bulletins page lists 11/1/2026, 10/25/2026, 10/18/2026 and 10/11/2026 as links
    to /assets/Uploads/allsaintsbulletin.pdf, 30thbulletin2.pdf, bulletin28.pdf and 28sundaybulletin2.pdf:
    irregular names, newest first, with the 1 November issue posted early.'
- url: https://archphila.org/parish/st-rose-of-lima-north-wales/
  seen: 2026-10-28
  note: 'Directory entry: Rev. Bernard J. Taglianetti, pastor; website srol.org; Mass times Saturday vigil
    5 PM, Sunday 8, 9:30, 11:30 AM, weekdays 8:30 AM. Differs from the bulletin on the vigil (5 PM vs
    4:00 p.m.).'
- url: https://www.church-bulletin.org/saint-rose-of-lima-church-philadelphia-pa-19151
  seen: 2026-10-28
  note: John Patrick listing 151, "Saint Rose of Lima Church", is Philadelphia 19151, a different parish;
    North Wales has no John Patrick listing in the 1-1300 scan (raw/jppc-pa.json).
promoted: 2026-10-29
---

## Publisher

St. Rose of Lima publishes its own weekly bulletin on its own site (srol.org), printed by Bon Venture Services. The 25 October 2026 issue's page 1 begins "The mission of Saint Rose of Lima Parish" and gives Rev. Bernard J. Taglianetti as pastor and the Mass Schedule; page 12 carries the printer's footer "St. Rose of Lima, North Wales". No other church is named.

## Worship sites

One church, 424 S. Main St. (the site footer calls it "Church"; the Parish Center is at 425 Pennsylvania Ave, the directory's rectory address). The schedule lists no other location.

## Website and bulletin provider

The Bulletins page of srol.org links each issue as `/assets/Uploads/<irregular name>.pdf`, newest first. The only John Patrick listing named St. Rose of Lima is Philadelphia's (151). The row reads the page with `page-pdfs`. `fetch:check` (2026-10-28) resolved "page-pdfs on https://www.srol.org/news-and-events/bulletins/: current" and picked `allsaintsbulletin.pdf`, the first link, which is the 1 November issue posted early (all-saints title; page 1 footer reads "Saint Rose of Lima, North Wales"). Freshness and issue date report `unknown` because the file names carry no date; the page lists newest first, so the pick follows the latest issue. No recipe was printed, as the pick came from the pinned page.

## Not yet confirmed

The pick has no machine-readable date, so a week with a late upload could leave a stale first link; the Bulletins page lists dates beside each link, which the resolver does not read.
