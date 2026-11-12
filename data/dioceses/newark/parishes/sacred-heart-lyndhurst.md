---
name: Sacred Heart, Lyndhurst
website: https://www.sacredheartlynd.org/church/
bulletin_provider: other
provider_id: page-pdfs https://www.sacredheartlynd.org/church/28229-2/ filename=26-*.pdf
publication: ['url:https://www.sacredheartlynd.org/church/28229-2/']
group: ''
evidence:
- url: https://www.sacredheartlynd.org/church/wp-content/uploads/2026/11/26-11-08.pdf
  seen: 2026-11-03
  quote: SACRAMENT OF THE EUCHARIST - M ASS SCHEDULE
  note: 'Page 1 masthead of the 8 November 2026 issue (5 pages, text layer, the parish''s own layout with
    no publisher footer): ''Sacred Heart Church, A Roman Catholic Community, 324 Ridge Road, Lyndhurst,
    NJ 07071'' (letter-spaced in the text layer), served by Rev. Theesmas Pankiraj, pastor; parish office
    615 New Jersey Ave. Mass schedule: Sunday 7:30am, 9:00am, 10:30am, 12:00pm, 1:30pm (Spanish); Monday-Friday
    12:00pm in the church; Saturday 9:00am in the church and 5:00pm in church (Anticipated). No other
    worship site is named.'
- url: https://www.sacredheartlynd.org/church/28229-2/
  seen: 2026-11-03
  quote: Parish Bulletin for November 8, 2026
  note: The Bulletin-Calendar page lists weekly issues as wp-content/uploads/<yyyy>/<mm>/26-MM-DD.pdf
    (26-11-08, 26-11-01, 26-10-25 …), after five flyers (SHC-5K-2026-Bulletin_L2.pdf, 2026-SPRING-Raffle-Bulletin_L1.pdf
    and others).
revisit: Update provider_id's filename filter to the 2027 file names (27-MM-DD.pdf) once the first 2027
  issue is posted.
revisit_after: 2026-12-28
promoted: 2026-11-05
bulletin_status: available
---

## Publisher

The parish produces its own bulletin and posts it on its WordPress site; no printer's footer appears in the issue. I read the 8 November 2026 issue (5 pages, text layer, posted 2 November): page 1 reads "Sacred Heart Church, A Roman Catholic Community, 324 Ridge Road, Lyndhurst, NJ 07071", served by Rev. Theesmas Pankiraj (pastor) and Rev. Cesar Chen (parochial vicar).

## Worship sites

One church, `sacred-heart-lyndhurst`. The page-1 schedule gives Sunday 7:30, 9:00, 10:30 AM, 12:00 PM and 1:30 PM (Spanish), weekdays 12:00 PM "in the church", and Saturday 9:00 AM and 5:00 PM (anticipated) "in church". Sacred Heart School (620 Valley Brook Ave) and the parish office (615 New Jersey Ave) are named, but no Mass there. The archdiocese directory (108) and GCatholic (18473) each list only this church.

## Website and bulletin provider

The website is the directory's https://www.sacredheartlynd.org/church/. Its Bulletin-Calendar page (/church/28229-2/) links each issue as `26-MM-DD.pdf`, after several flyers whose names contain "Bulletin" (SHC-5K-2026-Bulletin_L2.pdf), so the recipe filters on the `26-` prefix: `page-pdfs https://www.sacredheartlynd.org/church/28229-2/ filename=26-*.pdf`. The prefix is the year, so the filter needs `27-*.pdf` from January 2027 (revisit).

Fetch check (2026-11-03, headed): ok, PDF, resolved `page-pdfs on https://www.sacredheartlynd.org/church/28229-2/: first-listed` and picked uploads/2026/11/26-11-08.pdf, the 8 November 2026 issue read above (posted a week ahead). Issue date and freshness read `unknown`: fetch can't read a date from `26-11-08` and the letter-spaced masthead, but page 1 ends "November 8, 2026", so the pick is the newest issue. Identity `unverified` only because no expected identity is supplied. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

The filename filter carries the year: change it to `27-*.pdf` (or a two-year glob) once the parish posts its first 2027 issue.
