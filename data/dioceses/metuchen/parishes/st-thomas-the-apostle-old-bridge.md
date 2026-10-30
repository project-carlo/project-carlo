---
name: St. Thomas the Apostle
website: https://www.saintthomasob.com
bulletin_provider: other
provider_id: page-pdfs https://www.saintthomasob.com/event
publication: ['url:https://www.saintthomasob.com/uploads/docs/bulletins']
group: ''
evidence:
- url: https://www.saintthomasob.com/uploads/docs/bulletins/20261025.pdf
  seen: 2026-10-30
  quote: Saint Thomas the Apostle Parish and School
  note: 'Page 1 of the 25 October 2026 issue (8 pages, text layer): masthead names the parish alone; Saturday
    Vigil 4:00pm, Sunday 8:00am, 10:00am and 12:00 Noon, weekdays 8:00am and 12:15pm; ''Pastor: Rev. Jerome
    A. Johnson''; Parish Office 732.251.4000; page 2 ''Parish Office : One St. Thomas Plaza, Old Bridge,
    NJ 08857''.'
- url: https://www.saintthomasob.com/event
  seen: 2026-10-30
  quote: Bulletin Downloads (PDF)
  note: The parish's Bulletin page lists /uploads/docs/bulletins/20261101.pdf, 20261025.pdf, 20261018.pdf,
    20261011.pdf, 20261004.pdf, 20260927.pdf, newest first.
bulletin_status: available
---

## Publisher

St. Thomas the Apostle Parish and School, One St. Thomas Plaza, Old Bridge, publishes its own bulletin as dated PDFs on its own site (`/uploads/docs/bulletins/<YYYYMMDD>.pdf`), listed newest first on the Bulletin page (https://www.saintthomasob.com/event), which at the 2026-10-30 reading lists issues from 20260927 to 20261101. The 25 October 2026 issue's page 1 (text layer) reads 'Saint Thomas the Apostle Parish and School', 'Pastor: Rev. Jerome A. Johnson' and one Mass schedule. It names this parish alone. The pastor matches the finder; the parochial vicars (Rozembajgier, Thippabathini) differ from the finder's (Dukru, Fellrath), so the finder's vicar line is stale.

## Worship sites

One church, One St. Thomas Plaza (directory:24521, gcatholic:18690). The bulletin's schedule gives no other site.

## Website and bulletin provider

**The SPAM-SQUAT verdict is a false positive.** `probe url http://www.saintthomasob.com` (2026-10-30) flagged one spam term, 'casino'. The page is the live parish site (title 'St. Thomas the Apostle, Old Bridge, NJ'), and the term comes from a parish event, 'Holy Name Society: Wind Creek Casino Trip' with a `casinoroulette.jpg` image, which sits beside Mass times, Bulletin and parish links. The 25 October bulletin names the site as the parish's own ('Website: www.saintthomasob.com'). The site is not squatted. Provider `other` with recipe `page-pdfs https://www.saintthomasob.com/event`; the publication id is the site's bulletin folder, since no external id exists.

## Not yet confirmed

Nothing open on identity.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs https://www.saintthomasob.com/event` and picked `uploads/docs/bulletins/20261101.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `future` (the parish posts the coming Sunday early; the 20261101 page 1 reads "Saint Thomas the Apostle Parish and School ... ALL SAINT'S NOVEMBER 1, 2026"). Identity not machine-checked; I read the 25 October masthead myself. No `recipe` line was printed, so the pinned recipe stays as set.\n
