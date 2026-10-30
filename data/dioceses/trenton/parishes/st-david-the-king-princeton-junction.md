---
name: St. David the King Parish
website: https://stdavidtheking.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6043
publication: ['url:https://www.church-bulletin.org/saint-david-the-king-church-princeton-junction-nj-08550']
group: Cohort 7 (Princeton, West Windsor, Hightstown)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-david-the-king-church-princeton-junction-nj-08550/2026-11-01.pdf
  seen: 2026-10-30
  note: 'Page 1 of the 1 November 2026 issue (8 pages, image-only; read from a render): masthead ''THE
    CATHOLIC COMMUNITY OF ST. DAVID THE KING'', ''Letter from Fr. Jason''. Page 2 ''Mass Intentions''
    shows Masses Saturday 4 p.m. and 5:30 p.m., Sunday 9 a.m., 10:30 a.m. and 7 p.m., weekday 9 a.m. (12
    noon and 7 p.m. on All Souls'' Day, Monday 2 November) and an ''Eucharistic Holy Hour'' at Our Lady
    of Sorrows Church, Hamilton. The back cover''s printer line reads ''6043 St. David the King, Princeton
    Junction, NJ (B)''. It names this parish alone.'
- url: https://stdavidtheking.com/mass-schedule/
  seen: 2026-10-30
  quote: Saturday 4:00 PM, 5:30 PM
  note: 'The parish''s Mass Schedule page: ''Sunday 9:00 AM, 10:30 AM, 7:00 PM''; weekday and First Friday/First
    Saturday 9 AM Masses; the Saturday 5:30 PM Mass is a spoken Mass.'
- url: https://stdavidtheking.com/
  seen: 2026-10-30
  quote: 1 New Village Road | Princeton Junction NJ 08550
  note: The parish's John Patrick-built homepage; its footer reads 'Proudly Designed and Hosted by John
    Patrick Publishing Company', and its 'Weekly Bulletins' link and parish-bulletins page point to church-bulletin.org/?id=6043.
research:
- method: pnpm fetch:check --diocese trenton --parish st-david-the-king-princeton-junction (headed Chrome)
  url: https://church-bulletin.org/6043
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
---

## Publisher

St. David the King publishes its own weekly bulletin through John Patrick Publishing (listing 6043 on church-bulletin.org), and its site is a John Patrick-hosted site that links the listing. The 1 November 2026 issue is image-only (8 pages); its masthead reads 'The Catholic Community of St. David the King' and page 2 gives one Mass schedule. The parish site has no PDFs of its own: the 'Parish Bulletins' page only points at the listing.

## Worship sites

One church, 1 New Village Road (see `st-david-the-king-princeton-junction`). The bulletin and Mass Schedule page list no other place. The Holy Hour 'for our Nation' on 10 November is at Our Lady of Sorrows Church, Hamilton, a cohort-neighbour event and not this parish's site.

## Website and bulletin provider

stdavidtheking.com (finder; GCatholic's stdavidtheking.com is the same site) is the row's website; the bulletin is read from the John Patrick listing with the recipe `page-pdfs https://church-bulletin.org/6043`. diocese.md notes that other John Patrick parish sites also host their PDFs; this one doesn't.

## Not yet confirmed

The bulletin text layer is absent, so the pastor's name isn't read from the masthead ('Fr. Jason' signs the letter); the church row doesn't need it.
