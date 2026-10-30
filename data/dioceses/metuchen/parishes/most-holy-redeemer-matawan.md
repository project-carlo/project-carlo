---
name: Most Holy Redeemer
website: https://www.mhr-parish.org
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2238
publication: ['url:http://sponsors.bonventure.net/?page=2238']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/2238/2026-10-25.pdf
  seen: 2026-10-30
  quote: REV. CHESTER H. CARINA
  note: 'Page 1 of the 25 October 2026 issue (8 pages, text PDF): masthead ''The Catholic Community of
    Most Holy Redeemer, 133 Amboy Road, Old Bridge Township, Matawan, NJ 07747-6816'', Pastor Rev. Chester
    H. Carina, Founding Pastor Rev. Joseph L. Desmond; ''Saturday 5:00 p.m.; Sunday 8:00, 10:00 and 11:30
    a.m.; Weekdays Monday, Tuesday, Wednesday, Friday - 8:00 a.m. & Saturday - 9:00 a.m.''. Names no other
    parish.'
- url: https://www.mhr-parish.org/bulletins
  seen: 2026-10-30
  quote: August 27, 2023
  note: 'The parish''s own eCatholic (id 15478) Bulletin page is a frozen archive: its newest file is
    files.ecatholic.com/15478/bulletins/20230827.pdf. Its top-menu ''Bulletin'' link goes to sponsors.bonventure.net/?page=2238
    instead. issues.py ecatholic 15478 found no Sunday-dated issue for 18 October to 1 November 2026 (403
    each).'
- url: http://sponsors.bonventure.net/?page=2238
  seen: 2026-10-30
  note: 'Bonventure listing for page 2238 (over http://; https fails certificate verification): links
    pdfs/2238/2026-11-01.pdf as the newest issue. The 25 October and 1 November PDFs both download (3.8
    MB and 9.4 MB).'
bulletin_status: available
---

## Publisher

Most Holy Redeemer (133 Amboy Road, Matawan, in Old Bridge Township) publishes its own weekly bulletin through Bonventure (`sponsors.bonventure.net/?page=2238`), reached from the 'Bulletin' item in its website's menu. The 25 October 2026 issue (8 pages, text layer) names Rev. Chester H. Carina as Pastor and gives Saturday 5:00 p.m.; Sunday 8:00, 10:00 and 11:30 a.m.; weekdays 8:00 a.m. (9:00 a.m. Saturday). The finder's clergy line (Carina pastor, Desmond in residence) matches the masthead (Desmond as Founding Pastor). The bulletin mentions a 'Daily Mass Chapel' and a 'Reconciliation Room', which are rooms in the parish's own buildings at 133 Amboy Road; I did not find a separate Mass site.

## Worship sites

One church, 133 Amboy Road (`most-holy-redeemer-matawan`; directory:24519, gcatholic:18612 'Holy Redeemer'). The two rosters agree on the address. A grep of the bulletin for 'Sacred Heart' found nothing.

## Website and bulletin provider

The finder gives https://www.mhr-parish.org (eCatholic id 15478, probe url ok). GCatholic gives http://www.mostholyredeemerchurch.org, which redirects off-site to The Seminal Church (probe url: REDIRECT-OFFSITE, 2026-10-30) and is not the parish. The eCatholic archive stopped in August 2023, so id 15478 does not identify the current bulletin; it is not recorded in `publication`. Provider `other`, recipe `page-pdfs http://sponsors.bonventure.net/?page=2238`, as the Allentown Bonventure rows use.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs` on http://sponsors.bonventure.net/?page=2238 and picked `pdfs/2238/2026-11-01.pdf` (8 pages, 9.4 MB): transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `future` (two days ahead). Publication identity was not machine-checked; a grep of that issue finds 'CARINA' twice and I read the 25 October masthead myself. Recipe recorded: `page-pdfs http://sponsors.bonventure.net/?page=2238`.

## Not yet confirmed

Nothing open. The only gap is the freshness status `future`, which is the publisher posting the next Sunday's issue early.
