---
name: Saint Peter Parish, Somerset
website: https://www.stpetersparish.com
bulletin_provider: other
provider_id: page-pdfs https://www.stpetersparish.com/bulletin.php
publication: ['url:https://www.stpetersparish.com/bulletin.php']
group: ''
evidence:
- url: https://www.stpetersparish.com/site_docs/10648.pdf
  seen: 2026-10-21
  quote: 'ORDINARY SCHEDULE - Sat. Mass: 4PM, Sun. Masses:'
  note: 'Page 1 of the 18 October 2026 issue (2 pages, text layer readable). Masthead: "ST. PETER’S CATHOLIC CHURCH", "SUNDAY, OCTOBER 18TH, 2026 - TWENTY-NINTH SUNDAY IN ORDINARY TIME", "433 WEST CHURCH STREET SOMERSET, PA. 15501", Rev. Fr. Angelo J. Patti, VF, Pastor. Names this church alone; no other worship site or parish appears.'
- url: https://www.stpetersparish.com/bulletin.php
  seen: 2026-10-21
  note: 'Self-hosted bulletin page ("Bulletin | St Peter''s Catholic Church"). Lists dated links "10/18/2026 Bulletin" (site_docs/10648.pdf), "10/11/2026 Bulletin" (10647.pdf), "10/04/2026 Bulletin" and back to August 2026, plus quarterly ministry schedules. The page HTML was read with curl.'
- url: https://discovermass.com/church/st-peter-somerset-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for St. Peter.
  note: 'Discover Mass page st-peter-somerset-pa exists (Mass times, (814) 443-6574) but its Bulletins tab is empty: not a live channel.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Diocese directory lists Saint Peter Parish, Somerset, one church, 433 West Church Street, homepage http://www.stpetersparish.com/, Masses Sat 4:00 PM; Sun 8:00 AM, 10:00 AM, 12:15 PM.'
---

## Publisher

St. Peter Parish, Somerset publishes its own weekly bulletin from its own site. The 18 October
2026 issue (`site_docs/10648.pdf`, 2 pages) has the masthead "ST. PETER’S CATHOLIC CHURCH ... 433
WEST CHURCH STREET SOMERSET, PA. 15501 ... Rev. Fr. Angelo J. Patti, VF, Pastor" and the
schedule "ORDINARY SCHEDULE - Sat. Mass: 4PM, Sun. Masses: 8AM, 10AM, & 12:15PM". It names this
church alone, and no other parish. The diocese directory lists the parish with one church and
no linked parish. (Read 2026-10-21 with `probe pdf`.)

## Worship sites

One church, St. Peter (churches/st-peter-somerset). The bulletin's weekly Mass list and the
directory (Sat 4:00 PM, Sun 8:00, 10:00 and 12:15) agree. Weekdays are 7:00 AM Monday to
Friday (the week of 18 October has "NO 7AM MASS" on one day), plus Friday 11:15 AM school Mass
per the directory. The parish school is on the same campus; it is not a separate Mass site.

## Website and bulletin provider

`https://www.stpetersparish.com/bulletin.php` is a self-hosted PHP page that links each issue
as `site_docs/<n>.pdf`, newest first, with the date in the link text. `fetch:check` on
2026-10-21 chose `page-pdfs on https://www.stpetersparish.com/bulletin.php: current`, i.e.
`https://www.stpetersparish.com/site_docs/10648.pdf` (2,514,746 bytes, the 18 October issue), so
the recipe is pinned in `provider_id`. Discover Mass has a page for the church with an empty
Bulletins tab; it is not a channel. Fr. Michael Raj Arokiasamy, HGN is listed in the masthead as a second priest of the parish.

## Not yet confirmed

Nothing.
