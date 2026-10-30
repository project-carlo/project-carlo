---
name: Our Lady of Good Counsel Parish
website: https://olgcc.net/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/our-lady-of-good-counsel-west-trenton-nj-08628
publication: ['url:https://www.church-bulletin.org/our-lady-of-good-counsel-west-trenton-nj-08628']
group: Cohort 9
evidence:
- url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
  seen: 2026-10-30
  note: '1 November 2026 issue, 8 pages, image-only (no text layer); I rendered page 1. Masthead: ''Our
    Lady of Good Counsel'', ''www.olgcc.net'', ''November 1, 2026'', ''Tel: 609-882-3277'', pastor Fr.
    Ariel Robles; picture caption ''Our Lady of Good Counsel church, 137 West Upper Ferry Road, West Trenton''.
    One MASS SCHEDULE: Monday-Friday 7:30 am, Saturday 8:00 am; weekend Saturday 5:00 pm, Sunday 8:30
    am and 10:30 am; Holy Days 7:30 AM, 12 Noon & 7:00 PM. No other church or parish is named.'
- url: https://www.church-bulletin.org/our-lady-of-good-counsel-west-trenton-nj-08628
  seen: 2026-10-30
  quote: Latest Edition November 1, 2026
  note: John Patrick Publishing listing 533 (church-bulletin.org/?id=533), weekly archive; the 18 and
    25 October issues are also image-only.
- url: https://olgcc.net/
  seen: 2026-10-30
  quote: https://www.jppc.net/onlinebulletins/533template.pdf
  note: 'Parish site (WordPress) links the John Patrick bulletin 533, which redirects to the listing above.
    It also embeds ecatholic:14277, the diocese''s own site (not this parish''s), and ecatholic:13541
    (St. Isaac Jogues''s id, a diocesan embed): neither is recorded in publication.'
promoted: 2026-10-30
research:
- method: probe url on olgcc.net, probe pdf and render.py on the 1 November 2026 listing issue
  url: https://www.church-bulletin.org/our-lady-of-good-counsel-west-trenton-nj-08628
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese trenton --parish our-lady-of-good-counsel-west-trenton (headed Chrome)
  url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: It picked the 1 November 2026 issue (image-only pdf, freshness 'future'); identity 'unverified'
    by the tool, read by rendering page 1.
bulletin_status: available
publication_reviews:
- parish: incarnation-st-james-ewing
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Our Lady of Good Counsel alone (pastor
      Fr. Ariel Robles, 137 West Upper Ferry Road), with its own Mass schedule. (John Patrick 533)
  - url: https://container.parishesonline.com/bulletins/04/0399/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Incarnation-St. James Parish alone (pastor Fr. Stanley DeBoe,
      O.SS.T.), with its own Mass schedule for Incarnation and St. James churches. (ParishesOnline 04/0399)
- parish: sacred-heart-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Our Lady of Good Counsel alone (pastor
      Fr. Ariel Robles, 137 West Upper Ferry Road), with its own Mass schedule. (John Patrick 533)
  - url: http://www.trentonsacredheart.org/storage/November%201%202026.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Parish alone (pastor Rev. Msgr. Dennis A. Apoldite),
      with its own Mass schedule for Sacred Heart and Holy Cross churches.
- parish: st-hedwig-trenton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Our Lady of Good Counsel alone (pastor
      Fr. Ariel Robles, 137 West Upper Ferry Road), with its own Mass schedule. (John Patrick 533)
  - url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 2) names Saint Hedwig Parish alone (pastor Rev. Can. Dr.
      Jacek W. Labinski, 872 Brunswick Ave.), with its own Mass schedule. (John Patrick 592)
- parish: st-isaac-jogues-marlton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
    seen: 2026-10-30
    note: 'Bulletin for Our Lady of Good Counsel Parish (row our-lady-of-good-counsel-west-trenton), read
      by its map batch: 1 November 2026 issue, 8 pages, image-only (no text layer); I rendered page 1.
      Masthead: ''Our Lady of Good Counsel'', ''www.olgcc.net'', ''November 1, 2026'', ''Tel: 609-882-3277'',
      pastor Fr. Ariel Robles; picture caption ''Our Lady of Good Counsel church, 137 West Upper Ferry
      Road, West Trenton''. One MASS SCHEDULE: Monday-Friday 7:30 am, Saturday 8:00 am; weekend Saturday
      5:00 pm, Sunday 8:30 am and 10:30 am; Holy Days 7:30 AM, 12 Noon & 7:00 PM. No other church or parish
      is named.'
  - url: https://www.church-bulletin.org/bulletin/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053/2026-11-01.pdf
    seen: 2026-10-30
    note: 'Bulletin for Church of St. Isaac Jogues (row st-isaac-jogues-marlton), read by its map batch:
      12-page issue dated 1 November 2026 (Solemnity of All Saints), image-only (probe pdf: no extractable
      text), so pages 1-2 were read from renders. Page 1 masthead ''ROMAN CATHOLIC CHURCH OF ST. ISAAC
      JOGUES, MARLTON, NEW JERSEY'', ''REV. JAMES SMITH, PASTOR'', ''DEACON JOHN SCANLON''; ''Parish Address
      349 Evesboro-Medford Rd., Marlton, NJ 08053'', ''Phone: (856) 797-0999'', ''Website: cosij.org'';
      Weekly Masses Tuesday-Friday 8:30am (Monday Communion Service), Friday 7:00pm (Ordinary Form of
      the Mass in Latin), Saturday 5:00pm, Sunday 9:00am and 11:00am. It names this parish alone.'
---

## Publisher

Our Lady of Good Counsel Parish, West Trenton (in Ewing Township), Cohort 9 with Incarnation-St. James (July 2024 cohort list). It publishes its own bulletin through John Patrick Publishing (listing 533). The 1 November 2026 issue is image-only; I rendered page 1 and read the masthead and the Mass schedule (quoted in the evidence). It names this parish alone, with one church, and no neighbouring parish.

The 2017 *Faith in Our Future* decisions put Our Lady of Good Counsel and Incarnation-St. James on a "Collaborative Model" (https://dioceseoftrenton.org/decisions, Cohort 9, read 2026-10-30), not a linkage: Incarnation-St. James has a different pastor (Fr. Stanley DeBoe, O.SS.T.) and its own ParishesOnline bulletin (see `incarnation-st-james-ewing`), so the two are separate rows.

## Worship sites

One church: Our Lady of Good Counsel, 137 West Upper Ferry Road (`our-lady-of-good-counsel-west-trenton`). GCatholic lists it as 'Our Lady of Good Counsel, Ewing' (18714), the finder as West Trenton: one building, two municipal names.

## Website and bulletin provider

The parish site links the printer's listing, so the row reads the listing (`page-pdfs`), and its newest file is the coming Sunday's issue. `fetch:check` result recorded in research.

## Not yet confirmed

The text of the Mass schedule beyond page 1 (weekday and Holy Day variations) wasn't read; the page-1 schedule is the parish's whole schedule.
