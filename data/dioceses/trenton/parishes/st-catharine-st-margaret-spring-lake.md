---
name: The Parish of St. Catharine and St. Margaret
website: https://www.scsmsl.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-parish-of-saint-catharine-and-saint-margaret-spring-lake-nj-07762
publication: ['url:https://www.church-bulletin.org/the-parish-of-saint-catharine-and-saint-margaret-spring-lake-nj-07762',
  'ecatholic:30561']
group: Cohort 29 (Spring Lake, Sea Girt, Manasquan)
evidence:
- url: https://www.church-bulletin.org/bulletin/the-parish-of-saint-catharine-and-saint-margaret-spring-lake-nj-07762/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (Solemnity of All Saints), image-only (probe pdf: no extractable
    text), so pages 1-2 were read from renders. Page 1 masthead: ''THE PARISH OF St. Catharine & St. Margaret'';
    Parish Directory ''Pastor Very Rev. Damian McElroy, Parochial Vicar Rev. John Large'', three-plus
    deacons; Mass Schedule lists ''ST. CATHARINE CHURCH, 215 Essex Avenue'' (Monday, Tuesday, Thursday
    & Friday 12:00pm; Wednesday 9:00am and 12:00pm (St. Catharine Chapel); Saturday 5:00pm; Sunday 9:00am
    and 12:00pm) and ''ST. MARGARET CHURCH, 300 Ludlow Avenue'' (Saturday 4:00pm; Sunday 8:00am and 10:00am).
    Footer www.scsmsl.org | 732-449-5765. It names this parish alone.'
- url: https://www.church-bulletin.org/the-parish-of-saint-catharine-and-saint-margaret-spring-lake-nj-07762
  seen: 2026-10-30
  note: John Patrick Publishing listing 513 ('The Parish of Saint Catharine and Saint Margaret, Spring
    Lake, NJ 07762'); latest edition 1 November 2026 (tools/jppc-trenton.tsv and the listing, which links
    the 2026-11-01 and 2026-10-25 PDFs).
- url: https://www.scsmsl.org/bulletins
  seen: 2026-10-30
  quote: Bulletin
  note: The parish's own eCatholic site (ecatholic:30561; the page is the 'Bulletin Archive' with one
    link per Sunday from 4 January to 25 October 2026 to files.ecatholic.com/30561/bulletins/<yyyymmdd>.pdf).
    Its 25 October 2026 PDF is byte-identical to the John Patrick listing's 2026-10-25.pdf (same md5 and
    size, 7,935,577 bytes), so the two channels carry one bulletin; John Patrick already has 1 November,
    the site's newest is 25 October.
- url: https://www.scsmsl.org/mass-times
  seen: 2026-10-30
  quote: St. Catharine Chapel (Wed)
  note: 'The parish''s Mass Times page: Saturday 4:00 PM St. Margaret, 5:00 PM St. Catharine; Sunday 8:00
    and 10:00 AM St. Margaret, 9:00 AM and 12:00 PM St. Catharine; daily Mass 12:00 PM at St. Catharine
    Church (Mon, Tue, Thu, Fri) or St. Catharine Chapel (Wed), plus Wednesday 9:00 AM at St. Catharine
    Chapel.'
- url: https://www.stcatharine-stmargaret.com/
  seen: 2026-10-30
  note: The directory's website for this parish (finder pin 14605). It refused probe url and the browser
    on 2026-10-30; the bulletin footer and the working site are scsmsl.org, so the row uses that.
research:
- method: pnpm fetch:check --diocese trenton --parish st-catharine-st-margaret-spring-lake (headed Chrome);
    page-pdfs on the John Patrick listing
  url: https://www.church-bulletin.org/the-parish-of-saint-catharine-and-saint-margaret-spring-lake-nj-07762
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the current issue (freshness future: the
    coming Sunday issue, posted early)'
bulletin_status: available
---

## Publisher

The Parish of St. Catharine and St. Margaret (Spring Lake) publishes one weekly bulletin through John Patrick Publishing (listing 513 on church-bulletin.org) and posts the same PDF on its own eCatholic site. The 1 November 2026 issue is image-only; its rendered page 1 is headed "THE PARISH OF St. Catharine & St. Margaret" with Very Rev. Damian McElroy as pastor and Rev. John Large as parochial vicar, and gives one Mass schedule for both churches. St. Mark, Sea Girt and St. Denis, Manasquan (the other Cohort 29 parishes) each publish under their own masthead, pastor and listing (613; Bon Venture 2095), so Cohort 29 is not a shared bulletin.

## Worship sites

Two churches: St. Catharine Church, 215 Essex Avenue, and St. Margaret Church, 300 Ludlow Avenue (see `st-catharine-spring-lake`, `st-margaret-spring-lake`); both appear on page 1's Mass schedule and the parish's Mass Times page. GCatholic lists them as two entries (18741, 18809) and the directory as one parish pin at 215 Essex Ave. "St. Catharine Chapel" (Wednesday 9:00 AM and noon Mass) is listed under St. Catharine Church's address in the bulletin; no street address of its own turned up in the bulletin or the parish's pages (the parish-history page has no chapel text), so it is recorded as part of St. Catharine's site, not a third church. A Mass-times page or visit that gave the chapel its own address would make it one.

## Website and bulletin provider

The directory's website (stcatharine-stmargaret.com) refused `probe url` and the browser on 2026-10-30. The parish's working site is scsmsl.org (the bulletin footer), an eCatholic site (30561) whose Bulletins page links dated PDFs; its 25 October PDF is byte-identical to John Patrick's. Following the Run's rule, the row reads whichever channel has the latest issue, the John Patrick listing (it already has 1 November), and keeps `ecatholic:30561` in `publication`.

## Not yet confirmed

Nothing outstanding beyond the chapel's address.
