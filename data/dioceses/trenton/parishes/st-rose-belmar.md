---
name: Church of Saint Rose
website: https://www.strosebelmar.com/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2155
publication: ['url:http://sponsors.bonventure.net/?page=2155']
group: Cohort 19 'Gathered as One' (Bradley Beach, Avon, Belmar)
evidence:
- url: http://sponsors.bonventure.net/pdfs/2155/2026-11-01.pdf
  seen: 2026-10-30
  quote: Rev. Msgr. Edward J. Arnister
  note: 'Page 1 of the 1 November 2026 issue (16 pages, text layer): ''MASS SCHEDULE / WEEKDAYS 6:45 am
    & 9:00 am / SATURDAY 5:00 pm (Vigil) / SUNDAY 7:00, 9:30, 11:30 am & 5:00 pm'', Rev. Msgr. Edward
    J. Arnister, Pastor, Rev. Dr. John Paul Del Rosario, Parochial Vicar, ''RECTORY & PARISH OFFICE 603
    Seventh Ave., Belmar, NJ 07719 p: 732-681-0512''; page 2''s header reads ''CHURCH OF SAINT ROSE -
    BELMAR, NEW JERSEY - NOVEMBER 1, 2026''. It names this parish alone.'
- url: http://sponsors.bonventure.net/?page=2155
  seen: 2026-10-30
  quote: Saint Rose Church
  note: 'Bon Venture sponsor page 2155: ''Saint Rose Church, 603 Seventh Avenue, Belmar, NJ 07719'', ''Click
    to View Current Bulletin'' and previous bulletins from 1 November 2026 back to June 2026.'
- url: https://www.strosebelmar.com/bulletin
  seen: 2026-10-30
  note: 'Read with visit.py (probe url answers 403 to strosebelmar.com). The eCatholic site (ecatholic:37219)
    is only the host: its Bulletin page''s ''Click to View Current Bulletin'' link is https://sponsors.bonventure.net/pdfs/2155/2026-11-01.pdf,
    and issues.py ecatholic 37219 found no files.ecatholic.com bulletins. The page''s Mass Schedule agrees
    with the bulletin''s.'
promoted: 2026-10-30
research:
- method: visit.py on strosebelmar.com/bulletin, then probe pdf on the linked Bon Venture issue (http://
    because sponsors.bonventure.net fails TLS verification)
  url: https://www.strosebelmar.com/bulletin
  checked: '2026-10-30'
  outcome: found
  next_action: None
- method: pnpm fetch:check --diocese trenton --parish st-rose-belmar (headed Chrome)
  url: http://sponsors.bonventure.net/?page=2155
  checked: '2026-10-30'
  outcome: found
  next_action: 'None; transport ok, document_type pdf, picks the 1 November 2026 issue (freshness future:
    the coming Sunday issue, posted early); publication identity unverified because no expected identity
    is supplied'
bulletin_status: available
publication_reviews:
- parish: st-teresa-of-calcutta-bradley-beach
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2155/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Church of Saint Rose alone, with Rev. Msgr. Edward J. Arnister
      as pastor and one Mass schedule; St. Teresa of Calcutta's bulletin (John Patrick 687) has Rev. Erin
      Brown as pastor and two churches.
---

## Publisher

Church of Saint Rose, Belmar publishes its own weekly bulletin, printed by Bon Venture (sponsor page 2155). The 1 November 2026 issue (text layer) lists Rev. Msgr. Edward J. Arnister as pastor with one Mass schedule and the rectory at 603 Seventh Avenue. It doesn't mention St. Teresa of Calcutta, Bradley Beach, the other Cohort 19 parish, which has a different pastor (Rev. Erin Brown) and its own John Patrick bulletin (687), so they are separate rows.

## Worship sites

One church, 603 Seventh Avenue (`st-rose-belmar`). The Mass schedule names no other building.

## Website and bulletin provider

strosebelmar.com is an eCatholic site that blocks `probe url` (403) but loads in the browser; its Bulletin page links the Bon Venture issue, and its eCatholic id (37219) holds no bulletin files, so it stays out of `publication`. The row is `other` with `page-pdfs` on the Bon Venture sponsor page, read over `http://`.

## Not yet confirmed

Nothing outstanding.
