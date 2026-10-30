---
name: Parish of the Resurrection
website: https://www.resurrection2.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/resurrection-parish-delran-nj-08075
publication: ['url:https://www.church-bulletin.org/resurrection-parish-delran-nj-08075', 'ecatholic:14711']
group: Cohort 2 (Cinnaminson, Riverton, Maple Shade, Delran)
evidence:
- url: https://www.church-bulletin.org/bulletin/resurrection-parish-delran-nj-08075/2026-11-01.pdf
  seen: 2026-10-30
  note: '8-page issue dated 1 November 2026 (All Saints), image-only (probe pdf: no extractable text),
    page 1 read from a render. Masthead ''Resurrection Parish'', ''Rev. Michael A. Gentile Jr. Pastor'',
    ''260 Conrow Road Delran, New Jersey 08075''; ''Weekend Mass schedule: Saturday at 4:30 PM at Holy
    Name, Delran Sunday at 9:00 AM at St. Casimir, Riverside Sunday at 11:00AM at Holy Name, Delran'';
    ''Daily Mass schedule: 12pm-Mon.-Wed.-Fri. at Holy Name, Delran & 12pm- Tues & Thurs. at St. Casimir,
    Riverside 9:00 am Saturdays at St. Casimir, Riverside''. It names this parish alone.'
- url: https://www.church-bulletin.org/bulletin/resurrection-parish-delran-nj-08075/2026-10-25.pdf
  seen: 2026-10-30
  quote: Sunday at 9:00 AM at St. Casimir, Riverside
  note: The 25 October 2026 issue has a text layer with the same page 1 (Rev. Michael A. Gentile Jr. Pastor;
    Holy Name and St. Casimir schedule). Byte-identical (md5 6ef5c32b9c0867e8ab7714b91e4451ae) to https://files.ecatholic.com/14711/bulletins/20261025.pdf.
- url: https://www.church-bulletin.org/resurrection-parish-delran-nj-08075
  seen: 2026-10-30
  note: 'John Patrick Publishing listing 542 (''Resurrection Parish, Delran, NJ 08075''): latest edition
    1 November 2026, archive back to 2026 and earlier.'
- url: https://www.resurrection2.org/bulletins
  seen: 2026-10-30
  note: The parish's eCatholic site (id 14711; plain fetch answers 403, read in the browser) lists files.ecatholic.com/14711/bulletins/<yyyymmdd>.pdf
    from 20260802 to 20261025, so it is a week behind the listing (no 1 November issue yet).
research:
- method: pnpm fetch:check --diocese trenton --parish resurrection-delran (headed Chrome); page-pdfs on
    the John Patrick listing
  url: https://www.church-bulletin.org/resurrection-parish-delran-nj-08075
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
publication_reviews:
- parish: sacred-heart-riverton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/resurrection-parish-delran-nj-08075/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Resurrection Parish alone (pastor Rev.
      Michael A. Gentile Jr., 260 Conrow Road), with Mass at Holy Name and St. Casimir only.
  - url: https://container.parishesonline.com/bulletins/03/1347/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Church of the Sacred Heart, Riverton alone (pastor Rev. Charles
      M. Schwartz, 103 Fourth Street), with its own Mass times. (ParishesOnline container 03/1347)
- parish: st-charles-borromeo-cinnaminson
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/resurrection-parish-delran-nj-08075/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Resurrection Parish alone (pastor Rev.
      Michael A. Gentile Jr., 260 Conrow Road), with Mass at Holy Name and St. Casimir only.
  - url: http://sponsors.bonventure.net/pdfs/2203/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Saint Charles Borromeo, Cinnaminson alone (pastor Rev. Daniel
      E. Kirk, 2500 Branch Pike), with its own Mass times. (Bon Venture 2203)
- parish: our-lady-of-perpetual-help-maple-shade
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/resurrection-parish-delran-nj-08075/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Resurrection Parish alone (pastor Rev.
      Michael A. Gentile Jr., 260 Conrow Road), with Mass at Holy Name and St. Casimir only.
  - url: http://sponsors.bonventure.net/pdfs/2214/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 issue is a bulletin for Our Lady of Perpetual Help, Maple Shade alone (pastor
      Fr. Fernando Monsalve, 236 E. Main St), with its own Mass times; its footer shows the Maple Shade
      account. (Bon Venture 2214)
---

## Publisher

The Parish of the Resurrection, Delran publishes one weekly bulletin through John Patrick Publishing (listing 542 on church-bulletin.org), mirrored a week late on its eCatholic site (14711). The 1 November 2026 issue is image-only; rendered page 1 is headed 'Resurrection Parish' with Rev. Michael A. Gentile Jr. as pastor and one Mass schedule covering Holy Name (Delran) and St. Casimir (Riverside). The 25 October issue is byte-identical on both channels, so there is one bulletin; the row reads the listing, which has the latest issue (settled rule for printer-and-site channels).

## Worship sites

Two churches: Holy Name, 260 Conrow Road, Delran and St. Casimir, 502 New Jersey Avenue, Riverside (see `holy-name-delran`, `st-casimir-riverside`). Both have Mass in the current schedule. The parish site's schedule lists an 'Adoration Chapel @ Holy Name' and the 25 October bulletin a 'Reconciliation Room at Holy Name', which are inside the Holy Name building, not other churches.

## Website and bulletin provider

resurrection2.org (eCatholic 14711) answers 403 to probe url and loads in the browser. The eCatholic id is recorded in publication as the mirror; the row reads the listing.
