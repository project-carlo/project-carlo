---
name: St. Philomena Parish
website: http://stphilspa.com/
bulletin_provider: parishes_online
provider_id: st-philomena-church
publication: ['po-org:st-philomena-church', 'lpi:0018000000Qc2OpAAJ', 'po-container:03/0559']
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/03/0559/20261025B.pdf
  seen: 2026-10-28
  quote: |-
    SAINT PHILOMENA PARISH - 1898
    SAINT CYRIL OF ALEXANDRIA
    CATHOLIC CHURCH
    LANSDOWNE PA
    OCTOBER 25TH, 2026
  note: 'Page 1 of the 25 October 2026 issue (4 pages, text layer): the masthead names Saint Philomena
    Church, 41 E Baltimore Avenue, Lansdowne PA 19050, 610-622-2420, www.stphilspa.com, with one Mass
    Schedule: ''Saturday | 8:00am, 5:15pm Vigil; Sunday | 7:30am, 10:00am, 12:00pm''; weekdays Monday-Saturday
    8:00am. Pastor Reverend Paul A. Castellani. The 1 November 2026 issue (container 03/0559, 2026-11-01)
    is identical in layout.'
- url: https://parishesonline.com/organization/st-philomena-church
  seen: 2026-10-28
  note: 'probe po st-philomena-church: ParishesOnline org ''St. Philomena Church'', 41 E Baltimore Ave,
    Lansdowne, website stphilspa.com, ids po-org:st-philomena-church, lpi:0018000000Qc2OpAAJ, po-container:03/0559;
    latest issue 2026-11-01, then 10-25, 10-18, 10-11, 10-04, 09-27.'
- url: https://stphil-lans.solutiosoftware.com/
  seen: 2026-10-28
  quote: Schedule of Masses
  note: 'Parish site (Solutio; stphilspa.com is a frame around it; probe url and probe get answered 403
    here and the page loaded in Chrome). ''Latest Bulletin October 25'' links the ParishesOnline file
    https://container.parishesonline.com/bulletins/03/0559/20261025B.pdf. Its Mass schedule: Monday -
    Saturday 8:00 a.m.; Saturday vigil 5:15 p.m.; Sunday 7:30, 10:00 a.m., 12:00 Noon. It links the school
    ''SS. Cyril & Philomena'' and names no second church.'
- url: https://archphila.org/parish/st-philomena-lansdowne/
  seen: 2026-10-28
  quote: 'Merged with St. Cyril of Alexandria, East Lansdowne: 2013'
  note: 'Directory: Pastor Rev. Paul A. Castellani; 41 E. Baltimore Ave.; Mass times as in the bulletin;
    page updated 2 years ago.'
promoted: 2026-10-29
---

## Publisher

St. Philomena Parish publishes its weekly bulletin through ParishesOnline (organization `st-philomena-church`, container 03/0559). The 25 October 2026 issue is headed 'Saint Philomena Parish - 1898 / Saint Cyril of Alexandria Catholic Church / Lansdowne PA' and lists one church, 'Saint Philomena Church, 41 E Baltimore Avenue', with one Mass Schedule. The parish site links that container file as its 'Latest Bulletin'. The John Patrick scan found no listing for St. Philomena, and none is needed.

## Worship sites

One: St. Philomena Church. St. Cyril of Alexandria, East Lansdowne (merged into St. Philomena in 2013) is named in the masthead's heritage line but has no Mass: it was relegated to profane use effective 2021-01-11, and its decree says it has not been used as a regular church since Christmas 2018 (see `excluded/st-cyril-of-alexandria-east-lansdowne`). ParishesOnline also has an organization for St. Cyril (`st-cyril-of-alexandria-church-19050`) that publishes nothing.

## Website and bulletin provider

stphilspa.com is a frameset around stphil-lans.solutiosoftware.com (Solutio), which links the ParishesOnline PDF. `fetch` reads the row by `provider_id` `st-philomena-church`.

## Fetch check

fetch:check (2026-10-28) resolved the ParishesOnline publication page and picked the 2026-11-01 issue (container 03/0559): transport ok, PDF, freshness `future` (the container posted next Sunday's file four days early; its page 1 masthead names Saint Philomena Church and is read above), publication identity `unverified` (not matched by the checker). The 25 October issue is the latest dated on or before the check; if future-dated issues are ever rejected, the `other` fallback would need a different channel, since there is no John Patrick listing.

## Not yet confirmed

Pages 2-4 of the issue were not read beyond the Pastor's letter.
