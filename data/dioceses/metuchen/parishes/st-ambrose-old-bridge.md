---
name: St. Ambrose
website: https://www.saintambroseparish.com
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/601
publication: ['url:https://www.church-bulletin.org/saint-ambrose-parish-old-bridge-nj-08857']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-ambrose-parish-old-bridge-nj-08857/2026-10-25.pdf
  seen: 2026-10-30
  note: 'Page 1 of the 25 October 2026 issue (6 pages, all images; read as a render): masthead ''Saint
    Ambrose Parish, Roman Catholic Church'', ''The Very Rev. John C. Grimes, Pastor'', ''Rev. Tholitho,
    Parochial Vicar'', Parish Office phone 732-679-5666, 83 Throckmorton Lane, Old Bridge, New Jersey
    08857, saintambroseparish.com. Names no other church. No text layer, so this URL can''t be rechecked
    by quote.'
- url: https://www.saintambroseparish.com/
  seen: 2026-10-30
  quote: Saturday 9:00AM Confessions at 3:45PM 5:00PM Saturday  Vigil Mass Sunday Mass 8:00AM, 10:00AM
    and 12:00NOON
  note: 'Home page Mass schedule: daily 6:30AM and 9:00AM, Saturday 9:00AM, vigil 5:00PM, Sunday 8:00,
    10:00 and 12:00 noon, Filipino Mass 3rd Sundays 2pm.'
- url: https://www.jppc.net/onlinebulletins/601template.pdf
  seen: 2026-10-30
  note: Linked from the parish home page as the bulletin (probe url, visit.py). It returns HTML; church-bulletin.org/601
    redirects to the listing 'Saint Ambrose Parish, Old Bridge, NJ 08857', latest edition 2026-11-01.
research:
- method: Rendered page 1 of the 2026-10-25 church-bulletin.org PDF; pdftotext on all pages
  url: https://www.church-bulletin.org/bulletin/saint-ambrose-parish-old-bridge-nj-08857/2026-10-25.pdf
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: Quote the Mass schedule from a text issue if one appears; for now the parish home page
    carries the schedule
  retry_when: A later church-bulletin.org issue has a text layer
bulletin_status: available
---

## Publisher

St. Ambrose Parish, 83 Throckmorton Lane, Old Bridge, publishes its own weekly bulletin through John Patrick Publishing (id 601). The parish's eCatholic site (`ecatholic:15973`) links `jppc.net/onlinebulletins/601template.pdf` as its bulletin; the probes find no bulletin PDFs under the eCatholic id, so the id is the website's and isn't recorded as a publication. `church-bulletin.org/601` redirects to the listing for 'Saint Ambrose Parish, Old Bridge, NJ 08857'. The 25 October 2026 issue is image-only; its page 1 (rendered) names 'The Very Rev. John C. Grimes, Pastor' and 'Rev. Tholitho, Parochial Vicar', and no other church. Both match the finder's pastor line (Rev. John C. Grimes); the finder's parochial vicar is Rev. Martin Espinoza, so that line is stale or differs.

## Worship sites

One church, 83 Throckmorton Lane (directory:24520, gcatholic:18633). The parish home page's Mass schedule (read 2026-10-30) lists Saturday vigil, Sunday, daily, monthly Padre Pio and Filipino Masses with no second site. The finder also lists a 'Coptic Christian Roman Catholic Mass; St. Anthony Room'. That is a Mass inside this parish's own building: the St. Anthony Room is a St. Ambrose parish space (the home page puts the Saturday men's group there). It is not a separate place with its own church record. The home page's schedule doesn't mention the Coptic Mass, so its day and time are unconfirmed; the Coptic Catholic community belongs to the Eparchy of Saint Mary Queen of Peace, not this diocese, which I took from general knowledge, not a source read here.

## Website and bulletin provider

Website: https://www.saintambroseparish.com (eCatholic site 15973; the finder gives none, GCatholic gives http://www.saintambroseparish.com). The bulletin is on John Patrick, provider `other` with recipe `page-pdfs https://church-bulletin.org/601`, as for the other John Patrick parishes here.

## Not yet confirmed

The Mass schedule in the bulletin itself: pages 2 to 6 of the 25 October issue have no text layer and I rendered only page 1. The schedule was taken from the parish home page. Day and time of the Coptic Catholic Mass are not found.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs https://church-bulletin.org/601` and picked `bulletin/saint-ambrose-parish-old-bridge-nj-08857/2026-11-01.pdf`: transport ok, PDF, issue date 2026-11-01 inferred from the file name, freshness `future` (John Patrick posts the coming Sunday early), identity unverified by the tool (image-only issue). I read the 25 October masthead myself (above). No `recipe` line was printed, so the pinned recipe stays as set.\n
