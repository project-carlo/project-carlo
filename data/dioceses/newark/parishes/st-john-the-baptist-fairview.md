---
name: St. John the Baptist, Fairview
website: https://www.sjbfairview.org/
bulletin_provider: other
provider_id: page-pdfs https://www.sjbfairview.org/bulletin
publication: ['url:https://www.sjbfairview.org/bulletin']
group: Planning Area D
evidence:
- url: https://irp.cdn-website.com/a088fbb0/files/uploaded/November+1-+2026.pdf
  seen: 2026-11-03
  quote: St. John the Baptist Church
  note: '1 November 2026 issue (3 pages, text layer, parish-made; no publisher footer). Page 1 masthead:
    ''239 Anderson Ave, Fairview, NJ 07022'', ''St. John the Baptist CATHOLIC CHURCH'', Pastor Fr. Antonio
    Santana dos Santos, SAC, W | www.sjbfairview.org. English Mass Sunday 10:00am, Monday, Wednesday &
    Friday 7:30 am; Spanish: Vigilia del Sábado 7:00pm, Domingo 8:00am, 12:00pm & 7:00pm, Lunes a Viernes
    7:00pm, Sábado 10:00 am. Page 2: ''WEEK OF NOVEMBER 1, 2026''. Page 3: ''239 Anderson Ave., Fairview,
    NJ''.'
- url: https://www.sjbfairview.org/bulletin
  seen: 2026-11-03
  note: Duda site (irp.cdn-website.com). The bulletin page lists, newest first, 'Sunday November 1 2026
    All Saints Day' (November+1-+2026.pdf), 'Sunday October 25, 2026' and 'Sunday October 18, 2026' (read
    with visit.py --links; probe get sees the same three links).
- url: https://www.sjbfairview.org/
  seen: 2026-11-03
  quote: Church of St. John the Baptist
  note: 'Parish homepage: ''Anderson Avenue, Fairview, New Jersey 0702[2]''; Mass Times section and a
    Bulletin menu item (/bulletin, /es/bulletin).'
research:
- method: Wayback availability API for sjbfairview.org and sjbfairview.org/bulletin at 2023-02-01 (probe
    get archive.org/wayback/available)
  url: http://archive.org/wayback/available?url=sjbfairview.org&timestamp=20230201
  checked: '2026-11-03'
  outcome: not-found
  next_action: 'Only if the 2023 arrangement with St. Cecilia, Englewood matters: look for a 2023 St.
    Cecilia bulletin naming St. John the Baptist'
  retry_when: The St. Cecilia, Englewood batch finds 2023 issues
bulletin_status: available
---

## Publisher

St. John the Baptist, Fairview, makes its own weekly bilingual English/Spanish bulletin (3 pages, no publisher footer) and posts it on its Duda site. I read the 1 November 2026 issue: page 1 masthead '239 Anderson Ave, Fairview, NJ 07022', 'St. John the Baptist CATHOLIC CHURCH', Pastor Fr. Antonio Santana dos Santos, SAC, www.sjbfairview.org, with one Mass schedule for one church; page 2 'WEEK OF NOVEMBER 1, 2026'.

The roster note says the parish had a temporary administrator from St. Cecilia, Englewood, in January 2023. Now it has its own pastor and its own bulletin: the 1 November issue does not mention St. Cecilia or Englewood (grep 'Cecilia': no hits), and it is not printed by any publisher another parish uses. For 2023 nothing was found: the Wayback Machine has no snapshot of sjbfairview.org (see research), so whether it shared St. Cecilia's bulletin then is unknown and does not affect the row today.

## Worship sites

- St. John the Baptist, 239 Anderson Avenue (`st-john-the-baptist-fairview`): Saturday 7:00pm (Spanish); Sunday 8:00am, 12:00pm and 7:00pm (Spanish), 10:00am (English); weekdays 7:30am Monday, Wednesday and Friday (English) and 7:00pm Monday to Friday (Spanish); Saturday 10:00am (Spanish).

The directory (44) and GCatholic (18404) list only this church.

## Website and bulletin provider

The directory gives no website; https://www.sjbfairview.org/ is the parish's Duda site (found by trying names; its homepage and bulletin both give the church's address). Its /bulletin page lists dated PDFs newest first on irp.cdn-website.com, so the provider is `other`, read with `page-pdfs https://www.sjbfairview.org/bulletin`. The file names carry the date ('November+1-+2026.pdf').

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://www.sjbfairview.org/bulletin: current` and picked irp.cdn-website.com/a088fbb0/files/uploaded/November+1-+2026.pdf, the 1 November 2026 issue read above (date 2026-11-01); freshness fresh (2 days). Publication identity `unverified` only because no expected identity is supplied; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Whether the parish shared St. Cecilia, Englewood's bulletin in 2023 (see research); it has no bearing on the current row.
