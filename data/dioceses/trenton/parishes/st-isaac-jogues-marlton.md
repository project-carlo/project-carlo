---
name: Church of St. Isaac Jogues
website: https://cosij.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053
publication: ['url:https://www.church-bulletin.org/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053',
  'ecatholic:13541']
group: Cohort 26 (Moorestown, Mount Laurel, Marlton)
evidence:
- url: https://www.church-bulletin.org/bulletin/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (Solemnity of All Saints), image-only (probe pdf: no extractable
    text), so pages 1-2 were read from renders. Page 1 masthead ''ROMAN CATHOLIC CHURCH OF ST. ISAAC JOGUES,
    MARLTON, NEW JERSEY'', ''REV. JAMES SMITH, PASTOR'', ''DEACON JOHN SCANLON''; ''Parish Address 349
    Evesboro-Medford Rd., Marlton, NJ 08053'', ''Phone: (856) 797-0999'', ''Website: cosij.org''; Weekly
    Masses Tuesday-Friday 8:30am (Monday Communion Service), Friday 7:00pm (Ordinary Form of the Mass
    in Latin), Saturday 5:00pm, Sunday 9:00am and 11:00am. It names this parish alone.'
- url: https://www.church-bulletin.org/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053
  seen: 2026-10-30
  note: John Patrick Publishing listing 637 ('The Roman Catholic Church of Saint Isaac Jogues, Marlton,
    NJ 08053'); latest edition 1 November 2026 (links the 2026-11-01, 10-25, 10-18 and 10-11 PDFs).
- url: https://cosij.org/bulletins
  seen: 2026-10-30
  quote: 20261025.pdf
  note: The parish's own eCatholic site (id 13541; plain fetch answers 403, read in the browser). Its
    Bulletins page links files.ecatholic.com/13541/bulletins/20261025.pdf as the newest issue (20261018
    ... below). That PDF is byte-identical to the listing's 2026-10-25.pdf (md5 23749c166f39a6e8ceb4242580aa1751,
    8,396,720 bytes). The listing already has 1 November.
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese trenton --parish st-isaac-jogues-marlton (headed Chrome); page-pdfs
    on the John Patrick listing
  url: https://www.church-bulletin.org/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
publication_reviews:
- parish: st-john-neumann-mount-laurel
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-roman-catholic-church-of-saint-isaac-jogues-marlton-nj-08053/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Isaac Jogues: its masthead names the Church
      of St. Isaac Jogues alone at 349 Evesboro-Medford Rd with Rev. James Smith, Pastor, and gives Masses
      Sat 5:00pm and Sun 9:00 and 11:00am. St. John Neumann''s bulletin has a different pastor (Fr. Michael
      Dunn), address (560 Walton Ave.), staff and Mass times (Sat 4:00pm, Sun 8:00 and 10:00am), and comes
      from separate listings (637 and 6000) and eCatholic sites (13541 and 2914). The 2017 one-pastor
      linkage no longer holds.'
---

## Publisher

St. Isaac Jogues (Marlton) publishes its own weekly bulletin through John Patrick Publishing (listing 637 on church-bulletin.org) and mirrors each issue on its own eCatholic site (13541). The 1 November 2026 issue is image-only; rendered page 1 is headed 'Church of St. Isaac Jogues, Marlton, New Jersey' with Rev. James Smith as pastor and gives one Mass schedule.

## Linkage with St. John Neumann

The January 2017 decisions linked St. Isaac Jogues and St. John Neumann under one pastor (dioceseoftrenton.org/decisions). The current bulletins no longer show that: St. John Neumann's names Rev. Fr. Michael Dunn as its pastor, St. Isaac Jogues' Rev. James Smith, each with its own staff, Mass times and listing. The linkage is therefore not a shared bulletin; the rows are separate (see `publication_reviews`). Cohort 26 also contains Our Lady of Good Counsel, Moorestown, with its own bulletin (listing 676).

## Worship sites

One church, 349 Evesboro-Medford Road (see `st-isaac-jogues-marlton`). The cover also lists an 'Adoration Chapel of the Sacred Heart' open 8am-8pm daily, which is prayer, not Mass, and is part of the parish center.

## Website and bulletin provider

The directory's site cosij.org is an eCatholic site (stisaacjogues.org, GCatholic's, moved there). Its Bulletins page's newest issue is 25 October, a week behind the John Patrick listing's 1 November, so the row reads the listing (the Run's rule: the channel with the latest issue) and keeps ecatholic:13541 in `publication`.
