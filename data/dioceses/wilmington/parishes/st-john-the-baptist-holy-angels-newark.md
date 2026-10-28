---
name: St. John the Baptist - Holy Angels
website: https://stjohn-holyangels.com/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2103
publication: ['url:http://sponsors.bonventure.net/?page=2103']
group: Iron Hill Deanery
evidence:
- url: http://sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf
  seen: 2026-10-27
  quote: ST. JOHN - HOLY ANGELS PARISH
  note: 'Cover of the 25 October 2026 issue (bilingual; read with pdftotext from a copy saved through
    Chrome, since https sponsors.bonventure.net fails Python TLS verification): ''ST. JOHN - HOLY ANGELS
    PARISH, 82 Possum Park Road, Newark, Delaware 19711, 302-731-2200''; Mass lists for two churches,
    ''St. John Church East Main & North Chapel Streets'' and ''Holy Angels Church 82 Possum Park Road''.
    Pastor Rev. Carlos Ochoa; associates Rev. Michael A. Preston and Rev. Manuel J. Quiceno.'
- url: https://stjohn-holyangels.com/
  seen: 2026-10-27
  quote: Bulletin
  note: 'Browser read (plain probe url got HTTP 403): the home page''s ''Bulletin Here'' button links
    http://sponsors.bonventure.net/?page=2103, whose bulletin link is /pdfs/2103/2026-10-25.pdf.'
publication_reviews:
- parish: holy-rosary-claymont
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf
    seen: 2026-10-27
    quote: ST. JOHN - HOLY ANGELS PARISH
    note: 'St. John - Holy Angels, Newark''s 25 October 2026 issue (Bonventure page 2103): the page 1
      masthead names St. John - Holy Angels Parish, 82 Possum Park Road, Newark.'
  - url: http://sponsors.bonventure.net/pdfs/2100/2026-10-25.pdf
    seen: 2026-10-27
    quote: Holy Rosary Church
    note: 'Holy Rosary, Claymont''s 25 October 2026 issue (Bonventure page 2100): the masthead names Holy
      Rosary Church, 3200 Philadelphia Pike, Claymont, and the issue names no other parish''s Mass schedule.'
- parish: our-lady-of-lourdes-seaford
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf
    seen: 2026-10-27
    quote: ST. JOHN - HOLY ANGELS PARISH
    note: 'St. John - Holy Angels, Newark''s 25 October 2026 issue (Bonventure page 2103): the page 1
      masthead names St. John - Holy Angels Parish, 82 Possum Park Road, Newark.'
  - url: http://sponsors.bonventure.net/pdfs/2167/2026-10-25.pdf
    seen: 2026-10-27
    quote: Our Lady of Lourdes
    note: 'Our Lady of Lourdes, Seaford''s 25 October 2026 issue (Bonventure page 2167): page 1''s masthead
      names Our Lady of Lourdes Roman Catholic Church with its own weekend Masses.'
- parish: sacred-heart-chestertown
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf
    seen: 2026-10-27
    quote: ST. JOHN - HOLY ANGELS PARISH
    note: 'St. John - Holy Angels, Newark''s 25 October 2026 issue (Bonventure page 2103): the page 1
      masthead names St. John - Holy Angels Parish, 82 Possum Park Road, Newark.'
  - url: http://sponsors.bonventure.net/pdfs/2169/2026-10-25.pdf
    seen: 2026-10-27
    quote: Sacred Heart
    note: 'Sacred Heart, Chestertown''s 25 October 2026 issue (Bonventure page 2169): its masthead names
      Sacred Heart, and its weekend Mass counts (p.4) list Sacred Heart and St. John only.'
---

## Publisher

St. John the Baptist - Holy Angels is one parish that publishes one bilingual weekly bulletin, hosted by Bonventure (page 2103). The 25 October 2026 cover is headed 'ST. JOHN - HOLY ANGELS PARISH' and lists Mass for two churches. The staff list names Rev. Carlos Ochoa, Pastor, with two associate pastors and a deacon.

## Worship sites

Two churches, both in Newark: St. John Church (East Main & North Chapel Streets; Mass Monday, Tuesday, Thursday to Saturday 8:00 am, Sunday 7:30 and 10:30 am) and Holy Angels Church (82 Possum Park Road; Spanish and English Masses: Tuesday and Thursday 7:00 pm Spanish, Wednesday 8:30 am, Saturday 4:00 pm, last Saturday 6:00 pm bilingual children's Mass, Sunday 9:00 am English and 7:00, 11:00 am, 1:00 and 7:00 pm Spanish). The diocese directory (directory:120) and GCatholic (gcatholic:19338, 'St. John the Baptist-Holy Angels') each list one building, at 82 Possum Park Road, which is Holy Angels and the parish centre. Neither roster has St. John's own church; its record is not linked to a roster entry. The directory's Mass times (Sun 7:30, 10:30; weekday 8:00; Thu 19:00; Sat 8:00) are St. John's, not Holy Angels'.

## Website and bulletin provider

`other`, pinned to the Bonventure page with `http://` (see diocese.md, Bonventure). stjohn-holyangels.com answers plain probes with HTTP 403 but loads in Chrome.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-john-the-baptist-holy-angels-newark` (2026-10-27): picked sponsors.bonventure.net/pdfs/2103/2026-10-25.pdf (3.0 MB); transport ok, document type PDF, freshness fresh (2 days). The tool leaves identity 'unverified'; the masthead read above settles it. The pinned recipe is already in `provider_id`, so no new recipe is recorded.

## Not yet confirmed

Nothing outstanding on the bulletin. Reconcile may want to know that the two rosters hold one entry for a parish with two churches.
