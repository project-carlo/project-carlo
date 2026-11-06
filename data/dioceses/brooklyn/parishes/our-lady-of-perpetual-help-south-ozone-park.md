---
name: Our Lady of Perpetual Help (South Ozone Park)
website: https://olphchurch.net/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://olphchurch.net/bulletin/
publication: []
group: Deanery Q8 (Queens West)
evidence:
- url: https://olphchurch.net/wp-content/uploads/sites/96/2026/10/nov1_2026_olphqns_compressed.pdf
  seen: 2026-11-06
  note: '1 November 2026 issue, 6 pages, all scanned images (rendered with render.py). Page 1 cover: ''Our
    Lady of Perpetual Help Roman Catholic Church, The Solemnity of All Saints, November 1, 2026''. Page
    2 box: ''MASS SCHEDULE - HORARIO DE MISAS Monday-Friday: 8:30 a.m. Saturday: 8:30 a.m. & 5:00 p.m.
    Sunday: 8:30 a.m., 10:30 a.m. & 12:00 p.m. (Español)''; Rectory 111-50 115th Street, South Ozone Park,
    NY 11420; Confessions Saturday 4:00-4:45 p.m.; Pastoral Staff Rev. Thomas W. Ahern, Pastor. No other
    church or chapel is named.'
- url: https://olphchurch.net/bulletin/
  seen: 2026-11-06
  note: 'Bulletin page on a WordPress multisite (uploads under /wp-content/uploads/sites/96/), newest
    first: nov1_2026_olphqns_compressed.pdf, oct25, oct18, oct11, oct4, sept27... The site refuses probe
    url (RemoteDisconnected) but loads in visit.py and fetch.'
- url: https://parishesonline.com/organization/our-lady-of-perpetual-help-church-11420
  seen: 2026-11-06
  note: 'probe po: ParishesOnline org ''Our Lady of Perpetual Help Church'' (lpi 0018000000QxB9wAAF, 11150
    115th St) has no publications, so it is not a publication id for this row.'
revisit: Rerun fetch:check after the weekend and confirm it picks the 8 November 2026 issue (freshness
  is reported unknown for these image-only files).
revisit_after: 2026-11-10
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://olphchurch.net/bulletin/
  url: https://olphchurch.net/bulletin/
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 8 November and confirm it picks that issue; freshness is unknown
    because the issue is images and the file name (nov1_2026_...) is not a date fetch reads
  retry_when: The 8 November issue is posted
  revisit_after: 2026-11-10
bulletin_status: available
publication_reviews:
- parish: st-mary-gate-of-heaven-ozone-park
  decision: separate
  evidence:
  - url: https://olphchurch.net/wp-content/uploads/sites/96/2026/10/nov1_2026_olphqns_compressed.pdf
    seen: 2026-11-06
    note: The 1 November 2026 masthead names Our Lady of Perpetual Help alone, with its own Mass schedule
      at 111-50 115th Street and Rev. Thomas W. Ahern as pastor.
  - url: https://container.parishesonline.com/bulletins/03/4068/20261108B.pdf
    seen: 2026-11-06
    note: 'The other bulletin: The 8 November 2026 masthead names Saint Mary Gate of Heaven Parish alone,
      103-12 101st Avenue, with Rev. Baltazar Sánchez Alonzo as pastor and its own Mass schedule (LPi
      container 03/4068).'
- parish: st-teresa-of-avila-st-anthony-of-padua-south-ozone-park
  decision: separate
  evidence:
  - url: https://olphchurch.net/wp-content/uploads/sites/96/2026/10/nov1_2026_olphqns_compressed.pdf
    seen: 2026-11-06
    note: The 1 November 2026 masthead names Our Lady of Perpetual Help alone, with its own Mass schedule
      at 111-50 115th Street and Rev. Thomas W. Ahern as pastor.
  - url: https://www.stasap.org/wp-content/uploads/2026/10/2026-11-03-Bulletin-1.pdf
    seen: 2026-11-06
    note: 'The other bulletin: The 1 November 2026 masthead names The Parish of St. Teresa of Avila -
      St. Anthony of Padua and lists only St. Anthony and St. Teresa churches, with Very Rev. Thomas W.
      Ahern as pastor.'
---

## Publisher

Our Lady of Perpetual Help, South Ozone Park, publishes its own weekly bulletin as image-only PDFs on its WordPress site. The 1 November 2026 issue (read 2026-11-06, 6 pages, rendered with render.py) has the cover "Our Lady of Perpetual Help Roman Catholic Church ... November 1, 2026". Page 2 has the Mass schedule, the rectory at 111-50 115th Street and the Pastoral Staff, headed "Rev. Thomas W. Ahern, Pastor". No printer's footer was read; only pages 1-2 were rendered.

Fr. Ahern is also pastor of St. Teresa of Avila - St. Anthony of Padua (priests' directory, 2026-11-05). That parish publishes its own bulletin, whose masthead names only its two churches; the two bulletins differ in staff lists, Mass times and confession times (here Saturday 4:00-4:45 p.m.). They stay two rows; see `publication_reviews`.

## Worship sites

One. Page 2's "MASS SCHEDULE - HORARIO DE MISAS" lists Monday-Friday 8:30 a.m., Saturday 8:30 a.m. and 5:00 p.m., and Sunday 8:30 a.m., 10:30 a.m. and 12:00 p.m. (Español), all with no other church named. The directory, the deanery list (which carries the parish twice, under Q8 and B8), GCatholic 16645 and Mass finder 1136 give the one church at 111-50 115th Street. Our Lady of Perpetual Help Catholic Academy (111-10 115th Street) is a school, not a worship site.

## Website and bulletin provider

`other`, recipe `page-pdfs https://olphchurch.net/bulletin/` (newest first). On 2026-11-06 `fetch:check` picked `nov1_2026_olphqns_compressed.pdf`, the current issue, with freshness `unknown`: the pages are images and the file name has no date fetch reads. The directory's `https://olphchurch.net/` is the same site. The empty ParishesOnline org `our-lady-of-perpetual-help-church-11420` is not a publication id. The pipeline needs OCR to read the Mass times.

## Not yet confirmed

The next weekly pick (8 November): see research.
