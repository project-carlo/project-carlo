---
name: Holy Cross Parish
website: https://holycrossrumson.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/holy-cross-roman-catholic-church-rumson-nj-07760
publication: ['url:https://www.church-bulletin.org/holy-cross-roman-catholic-church-rumson-nj-07760']
group: Cohort 16 (Red Bank, Rumson, Fair Haven)
evidence:
- url: https://www.church-bulletin.org/bulletin/holy-cross-roman-catholic-church-rumson-nj-07760/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (the Solemnity of All Saints), image-only (probe pdf: no
    extractable text), so pages 1-2 were rendered and read. Page 1 masthead: ''HOLY CROSS PARISH, Rev.
    Michael Lankford-Stokes, Pastor, holycrossrumson.org'', 30 Ward Avenue, Rumson, NJ 07760. Page 2 (footer
    ''#623 Holy Cross Parish'') lists the Liturgy: Weekday Mass 9:00am, Saturday Vigil 5:00pm, Sunday
    Masses 8:00 am, 10:30 am & 5:00 pm. It names Holy Cross alone; no other Cohort 16 parish is in it.'
- url: https://www.church-bulletin.org/holy-cross-roman-catholic-church-rumson-nj-07760
  seen: 2026-10-30
  note: John Patrick Publishing listing 623 ('Holy Cross Roman Catholic Church, Rumson, NJ 07760'); latest
    edition 1 November 2026 (per tools/jppc-trenton.tsv and the listing page, which links the 2026-11-01
    and 2026-10-25 PDFs).
- url: https://holycrossrumson.org/bulletin
  seen: 2026-10-30
  quote: Click here for this week's bulletin or choose from the archive below.
  note: 'The parish''s own Bulletins page (eCatholic site 37867; read with the browser, probe url answers
    403) links church-bulletin.org/623/<date>.pdf for each Sunday from 7 December 2025 to 25 October 2026
    in its archive: the same John Patrick listing, not a separate bulletin. ecatholic:37867 is therefore
    the site host, not a publication.'
research:
- method: pnpm fetch:check --diocese trenton --parish holy-cross-rumson (headed Chrome); page-pdfs on
    the John Patrick listing
  url: https://www.church-bulletin.org/holy-cross-roman-catholic-church-rumson-nj-07760
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 2026-11-01 issue (freshness ''future'':
    the coming Sunday''s issue, posted early, which the playbook treats as current)'
bulletin_status: available
---

## Publisher

Holy Cross Parish, Rumson publishes its own weekly bulletin through John Patrick Publishing (listing 623 on church-bulletin.org). The 1 November 2026 issue is an image-only PDF; its rendered page 1 masthead reads "HOLY CROSS PARISH, Rev. Michael Lankford-Stokes, Pastor" and page 2 gives the parish's Mass schedule (weekday 9:00 am, Saturday vigil 5:00 pm, Sunday 8:00 am, 10:30 am and 5:00 pm). It names Holy Cross alone, with its own staff list, so it is a single-parish row; Cohort 16's other parishes (Nativity, St. James, the Oratory) each publish their own issue under a different listing (627, 618, 544) with a different pastor. The parish's own Bulletins page offers the same John Patrick PDFs (`church-bulletin.org/623/<date>.pdf`), so there is no second channel to choose between.

## Worship sites

One church, 30 Ward Avenue, Rumson (see `holy-cross-rumson`). The bulletin's schedule and the parish's Liturgy page list the Church only. The bulletin's calendar mentions "SJMR" (a parish meeting room) for meetings, not Mass. Church hours on page 2: "Weekends: Open for Masses Only".

## Website and bulletin provider

The site is eCatholic (`ecatholic:37867`, seen on the Bulletins page) but its bulletins are the John Patrick listing's, so the row is `other` with `page-pdfs` on the listing, as the Co-Cathedral and St. Gabriel do. `probe url` on holycrossrumson.org answers 403 (bot block); the browser loads it.

## Not yet confirmed

Nothing outstanding; see the fetch check recorded below.
