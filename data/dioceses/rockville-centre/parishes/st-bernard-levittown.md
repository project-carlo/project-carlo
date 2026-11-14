---
name: St. Bernard's Roman Catholic Church
website: https://www.stbernardchurch.org/news-events/bulletin
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stbernardchurch.org/news-events/bulletin']
group: ''
evidence:
- url: https://www.stbernardchurch.org/news-events/bulletin/716-november-8-2026/file
  seen: 2026-11-12
  quote: 'Saturday: 5:00 p.m.'
  note: 'Page 1 of the 8 November 2026 issue (PDF title Bernard11-8.pdf, made in Word, 14 MB; downloaded
    through Chrome with tools/browser_get.py because probe get answers 403). Spiritual Life: Sunday Mass
    schedule Saturday 5:00 p.m., Sunday 8:00am, 10:00am, 12noon; Urdu Mass second Sunday 2:00 p.m. "in
    the church"; weekday Mass 8am in the Church. Mission statement names "St. Bernard''s parish family"
    and "the Levittown Community".'
- url: https://www.stbernardchurch.org/news-events/bulletin
  seen: 2026-11-12
  note: 'Solutio (Joomla) bulletin list, read with visit.py (probe url answers 403): 716-november-8-2026,
    715-november-1-2026, 714-october-25-2026; each issue page redirects to .../file, the PDF.'
bulletin_status: available
fetch_gap:
  kind: joomla-file-endpoint
  seen: 2026-11-12
  note: 'Solutio (Joomla) site. fetch:check on 2026-11-12 found the 8 November post but failed: "No PDF
    links found on bulletin post page: .../716-november-8-2026/file" (the post redirects to the PDF, which
    answers 403 outside a browser). Chrome downloads it.'
  url: https://www.stbernardchurch.org/news-events/bulletin/716-november-8-2026/file
---

## Publisher

St. Bernard, 3100 Hempstead Turnpike, Levittown publishes its own weekly bulletin, made in Word by the parish (PDF title "Bernard11-8.pdf"; no printer's id, ad pages or LPi/John Patrick marks). The 8 November 2026 issue (`https://www.stbernardchurch.org/news-events/bulletin/716-november-8-2026/file`, read 2026-11-12) gives the Mass schedule for one church: Saturday 5:00 p.m.; Sunday 8:00am, 10:00am and 12noon; an Urdu (Pakistan) Mass on the second Sunday at 2:00 p.m. "in the church"; weekday Mass 8am in the Church. Its Mass intentions for 7-8 November follow the same times.

The diocese's Mass-times page (roster `mass-times:church-of-st-bernard-levittown`, read 2026-11-12) gives an older schedule (Sunday 7:30, 9:00, 10:30, Noon and 5:30 PM, weekdays 7:00 and 9:00 AM, Spanish 7:30 PM Saturdays). The parish's current bulletin is followed.

## Worship sites

One: the church at 3100 Hempstead Turnpike (`st-bernard-levittown-church`). The diocesan locator (directory:34), GCatholic (16871) and the Mass-times page list only this building, and the bulletin places every Mass "in the Church".

## Website and bulletin provider

stbernardchurch.org (the locator's link) is a Solutio (Joomla) site. It answers 403 to `probe url` and `probe get`, including the issue PDFs at `/news-events/bulletin/<n>-<month>-<d>-<yyyy>/file`; Chrome (visit.py, tools/browser_get.py) loads them. GCatholic's link, stbernardslevittown.org, did not resolve on 2026-11-12 (DEAD-DNS). No printer listing was found: the issue is a parish-made Word PDF. Following the diocese's settled rule for Solutio sites, the row is `unsupported` with `fetch_gap` `joomla-file-endpoint`.

## Not yet confirmed

Nothing about the parish or church. When a collector reads Solutio `/file` PDFs, set `bulletin_provider: other`, run `fetch:check` and clear `fetch_gap`.
