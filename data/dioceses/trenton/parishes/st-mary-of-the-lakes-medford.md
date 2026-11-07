---
name: St. Mary of the Lakes Parish
website: https://www.smlparish.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-of-the-lakes-catholic-church-medford-nj-08055
publication: ['url:https://www.church-bulletin.org/saint-mary-of-the-lakes-catholic-church-medford-nj-08055',
  'ecatholic:12486']
group: 'Cohort 3 (Disciples in Action: Medford, Tabernacle, Marlton)'
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-of-the-lakes-catholic-church-medford-nj-08055/2026-11-01.pdf
  seen: 2026-10-30
  note: '16-page issue dated 1 November 2026 (All Saints Day), image-only (probe pdf: no extractable text),
    so page 1 was read from a render. Masthead ''St. Mary of the Lakes CATHOLIC CHURCH AND SCHOOL'', ''Parish
    Office 40 Jackson Road, Medford, New Jersey 08055'', ''Reverend Gregg Abadilla, Administrator'', ''Reverend
    Kevin Hrycenko, Parochial Vicar'' and three deacons; Weekend Mass Saturday Vigil 5:30pm, Sunday 7:30am,
    9:00am, 10:30am and 12:00pm; Daily Mass Mon-Fri 7:15am, Mon-Sat 9:00am. It names this parish alone.'
- url: https://www.church-bulletin.org/saint-mary-of-the-lakes-catholic-church-medford-nj-08055
  seen: 2026-10-30
  note: John Patrick Publishing listing 556 ('Saint Mary of the Lakes Catholic Church, Medford, NJ 08055');
    latest edition 1 November 2026 (links the 2026-11-01 and 2026-10-25 PDFs).
- url: https://www.smlparish.org/bulletins
  seen: 2026-10-30
  quote: October 25, 2026
  note: The parish's own eCatholic site (id 12486; plain fetch answers 403, read in the browser). Its
    Bulletins page links files.ecatholic.com/12486/bulletins/20261025.pdf as the newest issue (20261018,
    20261011 ... below it). That PDF is byte-identical to the listing's 2026-10-25.pdf (md5 8f2b5ceb56a52c3d17ee98d3ca5e483f,
    10,554,511 bytes). The listing already has 1 November; the site's newest is 25 October. The homepage's
    Bulletin links include https://www.jppc.net/onlinebulletins/0556template.pdf.
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese trenton --parish st-mary-of-the-lakes-medford (headed Chrome); page-pdfs
    on the John Patrick listing
  url: https://www.church-bulletin.org/saint-mary-of-the-lakes-catholic-church-medford-nj-08055
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
publication_reviews:
- parish: holy-eucharist-tabernacle
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/church-of-the-holy-eucharist-tabernacle-nj-08088/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for Holy Eucharist: the cover names the Church of
      the Holy Eucharist alone at 520 Medford Lakes Road, with its own phone 609-268-8383 and a message
      signed by Fr. McClane; its parish site gives Saturday vigil 5:00pm, Sunday 8:30 and 10:30am. Different
      pastor, staff and Mass times from the other Cohort 3 parishes.'
- parish: st-joan-of-arc-marlton
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/church-of-saint-joan-of-arc-marlton-nj-08053/2026-11-01.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is the bulletin for St. Joan of Arc: the cover names the Church of
      St. Joan of Arc alone at 100 Willow Bend Rd, with its own phone 856-983-0077; page 2 gives Pastor
      Fr. Richard D. LaVerghetta, Saturday vigil 5:30PM, Sunday 7:30, 9, 10:30am and 12pm. Different pastor,
      staff and Mass times from the other Cohort 3 parishes.'
---

## Publisher

St. Mary of the Lakes (Medford) publishes one weekly bulletin through John Patrick Publishing (listing 556 on church-bulletin.org) and mirrors each issue on its own eCatholic site (12486). The 1 November 2026 issue is image-only; its rendered page 1 is headed 'St. Mary of the Lakes Catholic Church and School' with Rev. Gregg Abadilla as administrator and gives one Mass schedule. Holy Eucharist (Tabernacle) and St. Joan of Arc (Marlton), the other Cohort 3 parishes, each publish under their own masthead, pastor and Mass times (listings 602 and 520), so the cohort is not a shared bulletin.

## Worship sites

One church, St. Mary of the Lakes, 40 Jackson Road (see `st-mary-of-the-lakes-medford`). The masthead also gives the parish school at 196 Route 70, Medford, but the Mass schedule names no other building (the Friday 9:00am Mass is 'Fridays at School', on the same schedule line, and the school has no street address of its own as a Mass site; treated as part of the parish's activity, not a second church). GCatholic (18780) and the diocese's finder (14568) list the same single site.

## Website and bulletin provider

The directory's site (smlparish.org) is an eCatholic site whose Bulletins page links dated files.ecatholic.com/12486/bulletins PDFs. The 25 October PDF is byte-identical on both channels, and the John Patrick listing already has 1 November, so the row reads the listing (the Run's rule: the channel with the latest issue) and keeps ecatholic:12486 in `publication`. Plain fetch of smlparish.org answers 403; the browser loads it.

## Not yet confirmed

'Fridays at School' (9:00am Friday Mass) was read from the masthead only; if the school's chapel turns out to be a separate public Mass site, it would need its own church row. Next step: read a text-layer issue or the site's Mass Times page.
