---
name: St. Rose of Lima (Kensington)
website: https://stroseoflimabrooklyn.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery B8 (Brooklyn West)
evidence:
- url: https://stroseoflimabrooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMDIvMnowcWZ2YW9sZl8xMC4wNC4yMDI2X2ZpbmFsdjEucGRmIl1d/10.04.2026_finalv1.pdf
  seen: 2026-11-06
  quote: 7:00 p.m.– Anticipated Mass (Spanish)
  note: '4 October 2026 issue (Twenty-Seventh Sunday in Ordinary Time), 3 pages, text layer, self-made
    (no LPi, John Patrick or Church Bulletin Inc. footer). Page 1: Saint rose of lima church, 269 Parkville
    Ave, Brooklyn, NY 11230; Rev. Canon Grzegorz [Stasiak], Pastor; Rev. Joseph Bassey; Rev. Sergiy Emanuel.
    Sunday 8:30 a.m. (Spanish), 10:00 a.m. (English), 11:30 a.m. (Polish), 2:00 p.m. (Filipino, 2nd Sunday
    of the month); Monday-Friday 9:00 a.m. (English), 7:00 p.m. (Spanish); Saturday 9:00 a.m. (English),
    5:00 p.m. and 7:00 p.m. (Spanish) Anticipated. No other church or chapel is named.'
- url: https://stroseoflimabrooklyn.org/bulletins
  seen: 2026-11-06
  quote: October 04, 2026
  note: 'Tilma bulletins page, newest first: October 04, September 27, 20, 13, 06, August 30 ... The files
    carry upload stamps in batches: 2026-04-23, 05-05, 05-14, 05-29, 06-11, 08-20 (seven issues), 10-02
    (six issues, 29 August-4 October). No issue after 4 October was posted by 2026-11-06.'
- url: https://parishesonline.com/organization/st-rose-of-lima-church-11230
  seen: 2026-11-06
  note: 'probe po: ParishesOnline org ''St. Rose of Lima Church'', 269 Parkville Ave, Brooklyn, lpi 0018000000QxB7tAAF,
    with no publications; not a publication id (the parish self-publishes).'
revisit: No issue after 4 October 2026 was posted by 2026-11-06; the parish uploads in batches (last batch
  2026-10-02). Reread /bulletins and rerun fetch:check.
revisit_after: 2026-11-23
research:
- method: Tilma bulletins page read for the newest card, upload stamps decoded; fetch:check (headed Chrome)
    on page-pdfs https://stroseoflimabrooklyn.org/bulletins picked the 4 October 2026 issue, freshness
    stale (33 days)
  url: https://stroseoflimabrooklyn.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reread /bulletins; when an issue dated within two weeks is posted, set bulletin_provider
    other with provider_id 'page-pdfs https://stroseoflimabrooklyn.org/bulletins', bulletin_status available,
    and rerun fetch:check
  retry_when: The parish's next batch upload (gaps between uploads have run 2-10 weeks)
  revisit_after: 2026-11-23
- method: probe po st-rose-of-lima-church-11230, st-rose-of-lima-roman-catholic-church-11230, st-rose-of-lima-church
  checked: '2026-11-06'
  outcome: not-found
  next_action: Recheck the 11230 org for issues at the revisit
  retry_when: No Tilma upload by the revisit date
  revisit_after: 2026-11-23
bulletin_status: not-found
publication_reviews:
- parish: holy-spirit-borough-park
  decision: separate
  evidence:
  - url: https://stroseoflimabrooklyn.org/system/resources/W1siZiIsIjIwMjYvMTAvMDIvMnowcWZ2YW9sZl8xMC4wNC4yMDI2X2ZpbmFsdjEucGRmIl1d/10.04.2026_finalv1.pdf
    seen: 2026-11-06
    quote: 269 Parkville Ave, Brooklyn, NY 11230
    note: The 4 October 2026 masthead names Saint Rose of Lima church alone, 269 Parkville Ave, with its
      own Mass times; Holy Spirit is not mentioned anywhere in the issue.
  - url: https://www.holyspiritbrooklyn.org/wp-content/uploads/2026/11/HOLYSPIRIT.11-08-26-year_A_DB.pdf
    seen: 2026-11-06
    quote: Rev. Fr. Joseph Bassey, Parochial Vicar from St. Rose of Lima Church
    note: The 8 November 2026 masthead names Holy Spirit Roman Catholic Church alone, 1712 45th St., with
      its own Mass times; the only link is the shared parochial vicar Rev. Joseph Bassey, who is also
      on St. Rose's staff list.
---

## Publisher

St. Rose of Lima, Kensington publishes its own weekly bulletin, laid out by the parish (3 pages, no LPi, John Patrick or Church Bulletin Inc. footer) and posted as PDFs on its Tilma site. The 4 October 2026 issue (read 2026-11-06, the newest posted) has on page 1 "Saint rose of lima church", 269 Parkville Ave, Brooklyn, NY 11230, with Rev. Canon Grzegorz [Stasiak], Pastor, Rev. Joseph Bassey and Rev. Sergiy Emanuel.

## Worship sites

One. The page 1 schedule lists Sunday 8:30 a.m. (Spanish), 10:00 a.m. (English), 11:30 a.m. (Polish) and 2:00 p.m. (Filipino, 2nd Sunday), Monday-Friday 9:00 a.m. and 7:00 p.m. (Spanish), Saturday 9:00 a.m., 5:00 p.m. and 7:00 p.m. (Spanish), with no other church or chapel. The directory, the deanery list, GCatholic 16775 and Mass finder 1058 all give the one church at 269 Parkville Avenue. The Mass finder's times for place 1058 look like sample data (a 'potluck brunch' note, per the batch plan) and were not used (diocese rule: the finder is not schedule evidence).

Rev. Joseph Bassey also serves Holy Spirit (`holy-spirit-borough-park`), whose masthead calls him "Parochial Vicar from St. Rose of Lima Church"; each parish publishes its own bulletin naming itself alone, recorded as a `separate` review.

## Website and bulletin provider

`no_bulletin` for now, under the diocese's rule for stale Tilma pages: on 2026-11-06 the newest issue on `/bulletins` was 4 October 2026, and `fetch:check` on `page-pdfs https://stroseoflimabrooklyn.org/bulletins` picked it with freshness stale (33 days). The ParishesOnline org `st-rose-of-lima-church-11230` exists but has no issues, so there is no live container beside it. The parish does still publish: it uploads in batches (six issues on 2026-10-02, seven on 2026-08-20 after a ten-week gap), so a new batch is likely; the recipe to restore is in research.

## Not yet confirmed

Whether issues after 4 October 2026 will be posted. See research: reread `/bulletins` after 2026-11-23 and restore `other` with the page-pdfs recipe once a current issue is up.
