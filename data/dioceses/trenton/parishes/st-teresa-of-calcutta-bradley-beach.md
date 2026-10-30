---
name: The Parish of Saint Teresa of Calcutta
website: https://www.stocp.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720
publication: ['url:https://www.church-bulletin.org/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720']
group: Cohort 19 'Gathered as One' (Bradley Beach, Avon, Belmar)
evidence:
- url: https://www.church-bulletin.org/bulletin/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720/2026-11-01.pdf
  seen: 2026-10-30
  note: '12-page issue dated 1 November 2026 (All Saints Day), image-only (probe pdf: no extractable text),
    so pages 1-2 were read from renders. Page 1 masthead: ''St. Teresa of Calcutta Parish / One Parish
    Family with Two Churches'', Ascension Church, 501 Brinley Avenue, Bradley Beach, NJ 07720, and St.
    Elizabeth Church, 424 Lincoln Avenue, Avon By the Sea, NJ 07717. Page 2, ''The Parish of Saint Teresa
    of Calcutta'': Pastor Rev. Erin Brown, Parochial Vicar Fr. Sudheesh, parish office 501 Brinley Ave,
    732-774-0456. It names both former parishes'' churches under one pastor and one Mass schedule (page
    2, below).'
- url: https://www.church-bulletin.org/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720
  seen: 2026-10-30
  note: John Patrick Publishing listing 687, 'The Parish of Saint Teresa of Calcutta, Bradley Beach, NJ
    07720'; latest edition 1 November 2026, issues weekly back to at least 4 October (2026-10-04 ... 2026-11-01).
    All five recent issues are image-only.
- url: https://www.stocp.org/
  seen: 2026-10-30
  note: 'probe url: HTTP 200, WordPress site ''Parish of St. Teresa of Calcutta - 501 Brinley Avenue Bradley
    Beach, NJ 07720''; its bulletin link is https://www.jppc.net/onlinebulletins/687template.pdf, the
    other bulletin links are forms (registration, ministries, funeral guidelines). No second channel.'
research:
- method: Rendered pages 1-2 of the 1 Nov 2026 issue (render.py) and read the masthead and Mass blocks;
    compared against GCatholic's separate Ascension and St. Elizabeth entries
  url: https://www.church-bulletin.org/bulletin/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: None
- method: pnpm fetch:check --diocese trenton --parish st-teresa-of-calcutta-bradley-beach (headed Chrome)
  url: https://www.church-bulletin.org/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 1 November 2026 issue (freshness future:
    the coming Sunday issue, posted early); publication identity unverified because no expected identity
    is supplied'
bulletin_status: available
publication_reviews:
- parish: st-rose-belmar
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-parish-of-saint-teresa-of-calcutta-bradley-beach-nj-07720/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Teresa of Calcutta Parish with Ascension and St. Elizabeth
      only, under Rev. Erin Brown; St. Rose, Belmar's own bulletin (Bon Venture 2155) has Msgr. Edward
      J. Arnister as pastor.
---

## Publisher

The Parish of Saint Teresa of Calcutta (Bradley Beach) publishes one weekly bulletin through John Patrick Publishing (listing 687). The 1 November 2026 issue is image-only; its rendered page 1 is headed 'St. Teresa of Calcutta Parish, One Parish Family with Two Churches' and shows Ascension Church (501 Brinley Avenue, Bradley Beach) and St. Elizabeth Church (424 Lincoln Avenue, Avon By the Sea). Page 2 gives one pastor, Rev. Erin Brown, one parish office and one Mass schedule covering both churches. The 2017 plan's merger of Ascension, Bradley Beach and St. Elizabeth, Avon is therefore one bulletin and one row; the two former parishes have no bulletin of their own (GCatholic's St. Elizabeth website stelizabethavon.com has no DNS; Ascension has none listed).

## Worship sites

Two churches, both with Mass in the 1 November schedule: Ascension (Saturday 5:00 pm, Sunday 8:00 and 10:00 am, Monday/Wednesday/Friday 8:00 am) and St. Elizabeth (Saturday 4:00 pm, Sunday 9:00 and 10:30 am, Tuesday/Thursday/Saturday 8:00 am). Rows `ascension-bradley-beach` and `st-elizabeth-avon-by-the-sea`. GCatholic lists both as separate parishes' churches (stale); the finder lists one pin for the merged parish at 501 Brinley Avenue.

## Website and bulletin provider

stocp.org is live and links the John Patrick listing as its bulletin, so the row is `other` with `page-pdfs` on the listing. Cohort 19 neighbour St. Rose, Belmar prints its own bulletin (Bon Venture 2155) with a different pastor and masthead, so it is a separate row.

## Not yet confirmed

Nothing outstanding. The issue pages are images, so the quoted words come from renders and are recorded as notes.
