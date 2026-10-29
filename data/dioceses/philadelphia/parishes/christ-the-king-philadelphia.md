---
name: Christ the King Parish
website: https://www.christthekingparish.net
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/christ-the-king-church-philadelphia-pa-19114
publication: ['url:https://www.church-bulletin.org/christ-the-king-church-philadelphia-pa-19114']
group: ''
evidence:
- url: https://www.church-bulletin.org/christ-the-king-church-philadelphia-pa-19114
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 150, 'Christ the King Church', Philadelphia, PA 19114 (3252 Chesterfield
    Road, 215-632-1144); latest edition October 25, 2026, then October 18 and 11.
- url: https://www.church-bulletin.org/bulletin/christ-the-king-church-philadelphia-pa-19114/2026-10-25.pdf
  seen: 2026-10-29
  quote: Father John F. Babowitch, Parochial Administrator
  note: '25 October 2026 issue (8 pages, text layer, md5 84450197394bd6336fddb6372a2bda13). Page 1 masthead
    ''Christ the King Church, Morrell Park, Philadelphia, PA, FOUNDED 1963'', Father Ryan Nguyen Parochial
    Vicar, rectory 3252 Chesterfield Road, 215-632-1144, www.christthekingparish.net. MASSES box: Saturday
    vigil 5:00 PM, Sunday 8:00 AM and 10:00 AM (in person and Facebook Live), weekdays Monday-Saturday
    8:00 AM, holydays vigil 7:00 PM and 8:00 AM. Names this parish alone; Our Lady of Calvary is not mentioned.'
- url: https://www.christthekingparish.net
  seen: 2026-10-29
  note: 'probe url 200: title ''Christ the King Parish - 3252 Chesterfield Road Philadelphia, PA 19114'';
    the only bulletin link is the jppc.net/onlinebulletins/150template.pdf template (listing 150); no
    PDFs of its own.'
- url: https://archphila.org/parish/christ-the-king-philadelphia/
  seen: 2026-10-28
  quote: Rev. John F. Babowitch (Parochial Administrator, pro tem) in residence at Our Lady of Calvary,
    Philadelphia
  note: Directory Pastor line. Its Mass times add a Sunday Noon Mass (Sat 5 PM; Sun 8, 10 AM, Noon) that
    the 25 October bulletin's Masses box does not list.
research:
- method: Read listing 150, the 25 October text layer and the parish home page; compared with listing
    203's issue
  url: https://www.church-bulletin.org/christ-the-king-church-philadelphia-pa-19114
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: our-lady-of-calvary-philadelphia
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/christ-the-king-church-philadelphia-pa-19114/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead names Christ the King Church alone, with its own Masses box (Sat
      5:00 PM; Sun 8:00 and 10:00 AM). 8 pages, md5 84450197394bd6336fddb6372a2bda13.
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-calvary-philadelphia-pa-19154/2026-10-25.pdf
    seen: 2026-10-29
    note: The 25 October 2026 masthead names Our Lady of Calvary, 11024 Knights Road, alone, with its
      own Mass Schedule (Sat 5:00 p.m.; Sun 6:30, 8:00, 10:00 a.m., 12:00 Noon). 6 pages, md5 04fdbf107f6366d0a3d0de3d47b0b8a5.
      A different PDF.
---

## Publisher

Christ the King Parish prints with John Patrick Publishing: listing 150 (`church-bulletin.org/?id=150`) has an issue for 25 October 2026 with a text layer, and the parish home page links only the jppc template for 150. The row is `other`, `page-pdfs` on the listing. The issue's masthead and Masses box name this parish alone.

**One bulletin or two with Our Lady of Calvary?** Two. Rev. John F. Babowitch is Parochial Administrator here and pastor of Our Lady of Calvary, where he lives (directory: 'in residence at Our Lady of Calvary'), and Rev. Ryan Nguyen is vicar of both; each parish still publishes its own issue under its own listing (150 and 203): different mastheads, different page counts (8 and 6), different Mass schedules and different md5. This issue never mentions Calvary's Masses, and Calvary's issue lists Fr. Nguyen as 'Our Lady of Calvary/Christ the King' but carries no Christ the King Mass times. See `publication_reviews`.

## Worship sites

One: Christ the King Church, Morrell Ave. and Chesterfield Rd. (rectory 3252 Chesterfield Road). The Masses box lists no other place; the issue's other 'mission' mentions are the parish mission statement and World Mission Sunday.

## Website and bulletin provider

christthekingparish.net is the parish's own site and hosts no bulletin files, only the John Patrick template link. Recipe `page-pdfs https://www.church-bulletin.org/christ-the-king-church-philadelphia-pa-19114`.

## Not yet confirmed

The directory (updated 'three weeks ago' on 2026-10-28) lists a Sunday Noon Mass; the bulletin's Masses box says 8:00 and 10:00 AM only. The church follows the bulletin.

## Fetch check

`fetch:check` (2026-10-29) with the pinned `page-pdfs` recipe picked `2026-10-25.pdf` on listing 150: transport ok, PDF, fresh (issue age 4 days, date inferred from the listing's file name); identity `unverified` because the check is given no expected identity (masthead and Mass schedule read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
