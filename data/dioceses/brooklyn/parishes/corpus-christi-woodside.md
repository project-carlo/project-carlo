---
name: Corpus Christi (Woodside)
website: https://ccwoodsideny.org/
bulletin_provider: parishes_online
provider_id: corpus-christi-church-11377
publication: ['po-org:corpus-christi-church-11377', 'lpi:0018000000QxB9eAAF', 'po-container:03/9001']
group: Deanery Q2 (Queens West)
evidence:
- url: https://container.parishesonline.com/bulletins/03/9001/20261108B.pdf
  seen: 2026-11-06
  quote: ROMAN CATHOLIC CHURCH
  note: '8 November 2026 issue, 8 pages. Page 1 masthead ''CORPUS CHRISTI ROMAN CATHOLIC CHURCH, 31-30
    61ST STREET, WOODSIDE, NY 11377'', website ccwoodsideny.org; Schedule of Masses: Sunday 8:45 am English,
    11:00 am Español, 12:30 pm English, 3:00 pm Filipino (4th Sunday); Monday to Saturday 8:00 am; Spanish
    7:00 pm 1st Friday and 2nd Wednesday. Then ''In Partnership With: ST. SEBASTIAN ROMAN CATHOLIC CHURCH''
    (contacts only). Page 2 Mass Intentions are Corpus Christi''s own 8:00 AM weekday Masses.'
- url: https://parishesonline.com/organization/corpus-christi-church-11377
  seen: 2026-11-06
  note: 'probe po: org ''Corpus Christi Church'', lpi 0018000000QxB9eAAF, container 03/9001, website www.ccwoodsideny.org,
    address 3130 61st St, Woodside 11377-1291; weekly issues 2026-10-04 to 2026-11-08.'
- url: https://ccwoodsideny.org/bulletin/
  seen: 2026-11-06
  note: Parish site (diocesan WordPress multisite, uploads under /sites/69/; probe url UNREACHABLE, read
    with visit.py) lists weekly PDFs newest first, nov8_2026_ccwoodside.pdf2_compressed.pdf back to aug2_2026;
    the 8 Nov file has the same masthead and schedule as the container issue.
research:
- method: probe po corpus-christi-church-11377; probe container 03/9001
  url: https://parishesonline.com/organization/corpus-christi-church-11377
  checked: '2026-11-06'
  outcome: found
- method: fetch:check parishes_online org corpus-christi-church-11377 (picked 20261108B.pdf, this weekend's
    issue)
  url: https://container.parishesonline.com/bulletins/03/9001/20261108B.pdf
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: st-sebastian-woodside
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/03/9001/20261108B.pdf
    seen: 2026-11-06
    note: The 8 November 2026 masthead (page 1) names Corpus Christi Roman Catholic Church, 31-30 61st
      Street, with its own Mass schedule (Sunday 8:45, 11:00, 12:30; Mon-Sat 8:00 am) and its own weekday
      intentions; St. Sebastian appears only 'In Partnership With' as a contact block.
  - url: https://container.parishesonline.com/bulletins/03/4071/20261108B.pdf
    seen: 2026-11-06
    note: The 8 November 2026 masthead (page 1) names Saint Sebastian Roman Catholic Church, 58-02 Roosevelt
      Ave, with St. Sebastian's schedule alone (weekdays 9:00 am and 12:00 pm) and St. Sebastian's intentions
      on page 3; Corpus Christi appears only as a contact block and in the page 10 celebrant list.
---

## Publisher

Corpus Christi publishes its own weekly LPi bulletin, ParishesOnline container 03/9001 under org `corpus-christi-church-11377` (lpi 0018000000QxB9eAAF). I read the 8 November 2026 issue (read 2026-11-06): page 1 masthead "CORPUS CHRISTI ROMAN CATHOLIC CHURCH, 31-30 61ST STREET, WOODSIDE, NY 11377", its own Schedule of Masses, then "In Partnership With: ST. SEBASTIAN ROMAN CATHOLIC CHURCH" (address and contacts only). The parish site's `/bulletin/` page reposts the same issues.

Canonically Corpus Christi is part of the merged parish St. Sebastian–Corpus Christi (the diocese's directory lists only the merged parish; the 15 November 12:30 intention here is for "the parishioners of St. Sebastian-Corpus Christi"), with one pastor, Very Rev. Patrick J. West. Both bulletins print the shared 14-15 November celebrant list. But the two are distinct issues: different mastheads, schedules, weekday Mass intentions and LPi containers (03/9001 here, 03/4071 for St. Sebastian). Under the settled rule (a pre-merger parish that still publishes its own bulletin keeps its own row) this is a row of its own, with a `separate` review against `st-sebastian-woodside`.

## Worship sites

One church, Corpus Christi, 31-30 61st Street (`corpus-christi-woodside`): the masthead schedule is this church's alone. The deanery list and the Mass finder still list Corpus Christi separately; GCatholic 16602 too. No mission or chapel is named; the bulletin's other rooms (Rectory 31-30 61st St, Parish Center 31-31 60th St, "Sta. Teresa" hall) are not worship sites.

## Website and bulletin provider

`parishes_online` with provider_id `corpus-christi-church-11377`; website is the parish site, which reposts the issues on `/bulletin/`. `fetch:check` result is in research.

## Not yet confirmed

Nothing open.
