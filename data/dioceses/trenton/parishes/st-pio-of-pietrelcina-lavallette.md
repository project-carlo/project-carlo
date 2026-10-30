---
name: St. Pio of Pietrelcina Parish and Church of the Sacred Heart
website: https://stpioparish.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-pio-of-pietrelcina-church-of-the-sacred-heart-lavallette-nj-08735
publication: ['url:https://www.church-bulletin.org/saint-pio-of-pietrelcina-church-of-the-sacred-heart-lavallette-nj-08735']
group: Cohort 21 (Bay Head, Lavallette, Seaside)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-pio-of-pietrelcina-church-of-the-sacred-heart-lavallette-nj-08735/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (Solemnity of All Saints), image-only (probe pdf: no extractable
    text); read from renders of pages 1-2. Page 1 masthead shows two parishes side by side: ''Church of
    the Sacred Heart, 751 Main Avenue, Bay Head, NJ 08742'' and ''Saint Pio of Pietrelcina, 103 Washington
    Avenue, Lavallette, NJ 08735'', each with its own Mass Times. Page 2 directory: ''Rev. Joseph G. Hlubik,
    Pastor'' with one parochial vicar, deacon and staff for both, ''THE ADMINISTRATIVE OFFICE FOR BOTH
    PARISHES IS LOCATED AT SAINT PIO PARISH CENTER'', a separate Sacred Heart rectory/office, and separate
    contributions columns for Sacred Heart and Saint Pio. The masthead names both parishes together.'
- url: https://www.church-bulletin.org/bulletin/saint-pio-of-pietrelcina-church-of-the-sacred-heart-lavallette-nj-08735/2026-08-02.pdf
  seen: 2026-10-30
  note: 'Page 1 of the 2 August 2026 issue (image-only, read from a render) has the same two-parish masthead
    and summer Mass Times for the same two churches only: Sacred Heart Sat 5:00pm, Sun 7:15, 8:30, 10:30,
    daily 8:30; Saint Pio Sat 5:00pm, Sun 7:30, 9:00, 10:30, daily 8:30 ''(in the Chapel)''. The bulletin''s
    shape did not change between summer and November.'
- url: https://sacredheartbayhead.com/
  seen: 2026-10-30
  note: 'probe url: Bay Head''s own site (title ''Church of the Sacred Heart – 751 Main Avenue Bay Head,
    New Jersey 08742''; the finder''s pin directory:14637 ''Sacred Heart Church'', 751 Main Ave, Bay Head
    08742-5340) links https://www.jppc.net/onlinebulletins/6003template.pdf as its bulletin, the same
    listing as St. Pio''s site; its other PDF link is a registration form, not a bulletin.'
- url: https://stpioparish.com/
  seen: 2026-10-30
  note: 'probe url: St. Pio''s site (title ''St. Pio of Pietrelcina – 103 Washington Ave. Lavallette,
    NJ 08735''; the finder''s pin directory:14656 ''St. Pio of Pietrelcina Parish'', 103 Washington Ave,
    Lavallette 08735-2351) links jppc.net/onlinebulletins/6003template.pdf; its footer says ''Visit our
    linked Parish: Church of the Sacred Heart''. Hosted by John Patrick Publishing Company.'
- url: https://trentonmonitor.com/2025/02/13/st-pio-parish-celebrates-refresh-of-101-year-old-chapel/
  seen: 2026-10-30
  quote: pastor of the linked parishes of St. Pio, Lavallette, and Sacred Heart, Bay Head
  note: 'The Monitor, 13 February 2025: one pastor, two canonical parishes (the 2017 linkage), which the
    masthead now prints as one bulletin.'
promoted: 2026-10-30
research:
- method: 'church-bulletin.org listings by id (jppc-trenton.tsv and the two jsonl scans): 6003 ''Saint
    Pio of Pietrelcina & Church of the Sacred Heart'' (Lavallette 08735) has editions to 1 November 2026;
    6002 ''Church of the Sacred Heart - Saint Pio of Pietrelcina'' (Bay Head 08742) is a dead listing
    with no edition.'
  url: https://www.church-bulletin.org/church-of-the-sacred-heart-saint-pio-of-pietrelcina-bay-head-nj-08742
  checked: '2026-10-30'
  outcome: found
  next_action: None; 6002 is not recorded in publication because it carries no bulletin.
- method: 'pnpm fetch:check --diocese trenton --parish st-pio-of-pietrelcina-lavallette (headed Chrome,
    page-pdfs on the church-bulletin.org listing): picked .../2026-11-01.pdf; transport ok, document_type
    pdf, freshness future (the coming Sunday, posted early), identity unverified by the tool because the
    issue is image-only; identity and parishes read from renders of pages 1-2 instead.'
  url: https://www.church-bulletin.org/saint-pio-of-pietrelcina-church-of-the-sacred-heart-lavallette-nj-08735
  checked: '2026-10-30'
  outcome: found
  next_action: None; the pick is the current bulletin. No `recipe` line was printed (the stored page-pdfs
    provider_id already resolves).
bulletin_status: available
---

## Publisher

One bulletin serves both canonical parishes, so this is one row with Bay Head's and Lavallette's churches. John Patrick Publishing's listing 6003, "Saint Pio of Pietrelcina & Church of the Sacred Heart" (Lavallette, NJ 08735), posts dated PDFs on church-bulletin.org; the newest, 1 November 2026, is a 12-page image-only issue, read from renders of pages 1-2. Its masthead prints both parishes with their addresses and Mass times, page 2 gives one pastor (Rev. Joseph G. Hlubik), one parochial vicar and shared deacon and staff, and the administrative office "for both parishes" at the St. Pio Parish Center, though each parish keeps its own office line, trustees and collection columns. That is a current masthead naming the parishes together, so one row (see `diocese.md`, *Rules settled*). The earlier job's lead is confirmed: Bay Head's own listing 6002 has no edition, and both parishes' sites link 6003.

## Structure

The 2017 *Faith in Our Future* decisions planned a Linkage Model for Sacred Heart and St. Pio "no later than July 1, 2019"; the Monitor (13 February 2025) still calls them "linked parishes" under one pastor. They are two canonical parishes, not merged; the row keeps both as the homes of its churches.

## Website and bulletin provider

The row uses St. Pio's site (the Lavallette address is the one the listing is filed under); sacredheartbayhead.com carries the same link to 6003 and is not a second channel. `other` with `page-pdfs` on the listing, the only current channel found (neither site hosts copies). The first PDFs on both sites are registration forms, not bulletins.

## Worship sites

Three: Sacred Heart, Bay Head; St. Pio of Pietrelcina Church, 1100 Grand Central Avenue, Lavallette; St. Bonaventure Chapel, 1206 Grand Central Avenue, Lavallette, where weekday Mass is said (`sacred-heart-bay-head`, `st-pio-of-pietrelcina-church-lavallette`, `st-bonaventure-chapel-lavallette`). GCatholic's Our Lady of Peace, Normandy Beach is in `open/our-lady-of-peace-normandy-beach`.
