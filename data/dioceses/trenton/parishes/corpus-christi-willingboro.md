---
name: Corpus Christi Parish
website: https://ccnj.church
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/corpus-christi-parish-willingboro-nj-08046
publication: ['url:https://www.church-bulletin.org/corpus-christi-parish-willingboro-nj-08046', 'ecatholic:13717']
group: Cohort 1 (Willingboro, Beverly)
evidence:
- url: https://www.church-bulletin.org/bulletin/corpus-christi-parish-willingboro-nj-08046/2026-11-01.pdf
  seen: 2026-10-30
  quote: "Corpus Christi Parish \nWillingboro, New Jersey"
  note: '6-page issue for All Saints, Sunday 1 November 2026, text layer. Masthead names Corpus Christi
    Parish alone (Rev. John J. Testa, pastor; Rectory 63 Sylvan Lane; website www.ccnj.church). Masses:
    daily M-F 8:00am, Saturday 4:00pm, Sunday 9:00am and 11:00am. Page 2 prints only this parish''s intentions.'
- url: https://www.church-bulletin.org/corpus-christi-parish-willingboro-nj-08046
  seen: 2026-10-30
  note: 'John Patrick Publishing listing 6035 (''Corpus Christi Parish, Willingboro, NJ 08046''): latest
    edition 1 November 2026, with 18 and 25 October behind it.'
- url: https://ccnj.church/bulletins
  seen: 2026-10-30
  note: The parish's eCatholic site (id 13717; plain fetch answers 403, read in the browser) lists files.ecatholic.com/13717/bulletins/<yyyymmdd>.pdf
    from 20260726 to 20261018. The file named 20261018 is the issue for Sunday 25 October (its page 1
    reads 'Sunday, October 25, 2026'; created 19 Oct 2026), so the filename is the upload week. The listing's
    18 October file is a different PDF (md5 fb33841e..., 6 pages), and the listing has 1 November, so
    the listing is the current channel.
promoted: 2026-10-30
research:
- method: pnpm fetch:check --diocese trenton --parish corpus-christi-willingboro (headed Chrome); page-pdfs
    on the John Patrick listing
  url: https://www.church-bulletin.org/corpus-christi-parish-willingboro-nj-08046
  checked: '2026-10-30'
  outcome: found
  next_action: None
bulletin_status: available
publication_reviews:
- parish: jesus-the-good-shepherd-beverly
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/corpus-christi-parish-willingboro-nj-08046/2026-11-01.pdf
    seen: 2026-10-30
    quote: "Corpus Christi Parish \nWillingboro, New Jersey"
    note: 'Bulletin for Corpus Christi Parish (row corpus-christi-willingboro), read by its map batch:
      6-page issue for All Saints, Sunday 1 November 2026, text layer. Masthead names Corpus Christi Parish
      alone (Rev. John J. Testa, pastor; Rectory 63 Sylvan Lane; website www.ccnj.church). Masses: daily
      M-F 8:00am, Saturday 4:00pm, Sunday 9:00am and 11:00am. Page 2 prints only this parish''s intentions.'
  - url: https://www.church-bulletin.org/bulletin/the-parish-community-of-jesus-the-good-shepherd-beverly-nj-08010/2026-10-25.pdf
    seen: 2026-10-30
    quote: 805 Warren Street
    note: 'Bulletin for Jesus the Good Shepherd Parish (row jesus-the-good-shepherd-beverly), read by
      its map batch: 8-page issue of 25 October 2026 (text layer, trilingual English/Spanish/Portuguese).
      Cover: ''The Parish of Jesus, the Good Shepherd'', 805 Warren Street, Beverly NJ 08010; Mass Saturday
      vigil 5 PM and Sunday 9 AM (English), Sunday 11 AM (Spanish), Saturday 7:30 PM (Portuguese), daily
      Tuesday-Friday 9 AM. Page 2: ''Fr. Jorge Antonio Bedoya. Pastor''. Page 8 footer: ''511 Jesus The
      Good Shepherd, Riverside, NJ (b) John Patrick Publishing Company''. No mention of St. Peter or any
      second church.'
---

## Publisher

Corpus Christi Parish, Willingboro (Cohort 1 with Jesus the Good Shepherd, Beverly; the July 2024 cohort list prints 'Cohort 1 Corpus Christi, Willingboro'). It publishes its own bulletin, printed by John Patrick Publishing as listing 6035. The same parish's eCatholic site (13717) carries PDFs a week behind, so the row reads the listing and keeps the eCatholic id in `publication`. The cohort is not a shared bulletin: the 1 November 2026 masthead names Corpus Christi alone, and Jesus the Good Shepherd publishes its own (listing 511).

One worship site: Corpus Christi Church, 11 South Sunset Road. The rectory and office are at 63 Sylvan Lane, which is the address the diocesan finder pins.
