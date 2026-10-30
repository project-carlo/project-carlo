---
name: Holy Family Parish
website: https://www.holyfamily.us/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2213
publication: ['url:http://sponsors.bonventure.net/?page=2213']
group: Cohort 14 (Keyport, Matawan, Union Beach, Holmdel)
evidence:
- url: http://sponsors.bonventure.net/pdfs/2213/2026-11-01.pdf
  seen: 2026-10-30
  quote: REV. MATTHEW J. PFLEGER
  note: '1 November 2026 issue (8 pages, text layer; the ad pages 7-8 are font-garbled). Page 1: "Holy
    Family Catholic Church", weekend Mass intentions at 5:00 PM (Saturday) and 8:00, 9:30 and 11:00 AM
    (Sunday); page 2 staff list: Pastor Rev. Matthew J. Pfleger, Parochial Vicar Rev. Francis Cheruparampil,
    VC, and "HOLY FAMILY CHURCH CHAPEL" Wednesday adoration 8:30 AM to noon; page 4: "8:00 a.m. Mass"
    for First Saturdays, "here at Holy Family Parish". Weekday intentions at 8:00 AM. It names Holy Family
    alone.'
- url: http://sponsors.bonventure.net/?page=2213
  seen: 2026-10-30
  quote: 727 Highway 36 (P.O. Box 56)
  note: Bon Venture sponsor page 2213, headed "Holy Family Catholic Church, 727 Highway 36 (P.O. Box 56)
    • Keyport, NJ 07735 website"; previous bulletins listed weekly from 1 November 2026.
- url: https://www.holyfamily.us/hfs/
  seen: 2026-10-30
  note: 'Read in the browser (probe url: NO-PARISH-WORDS, JavaScript redirect to /hfs/). Zumu site, "HOLY
    FAMILY PARISH, 727 Highway 36, Union Beach, NJ 07735", rectory 732-264-1484; its "Parish Bulletins"
    button opens http://sponsors.bonventure.net/?page=2213 (onclick in the page HTML).'
research:
- method: pnpm fetch:check --diocese trenton --parish holy-family-union-beach (headed Chrome); page-pdfs
    on Bon Venture sponsor page 2213
  url: http://sponsors.bonventure.net/?page=2213
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 1 November 2026 issue (coming Sunday, "future" freshness, the current
    issue); identity unverified because the check had no expected identity.'
bulletin_status: available
---

## Publisher

Holy Family Parish, Union Beach (Cohort 14). It publishes its own weekly bulletin, printed by Bon Venture (sponsor page 2213, issues `sponsors.bonventure.net/pdfs/2213/<yyyy-mm-dd>.pdf`). The 1 November 2026 issue names Holy Family alone, with pastor Rev. Matthew J. Pfleger. Our Lady of Fatima, Keyport has a different pastor (Rev. Rene Pulgarin) and its own ParishesOnline bulletin, so the 2017 plan's "potential" linkage with the merged Keyport parish has not made one bulletin: the two are separate rows.

## Worship sites

One church, Holy Family, 727 Highway 36. The bulletin's "Holy Family Church Chapel" (Wednesday adoration) has no street address of its own and is part of the campus (see Rules settled). GCatholic (18704) and the finder (14598) list the one place. The sponsor page's address says Keyport (the post office mailing address); the site and finder say Union Beach.

## Website and bulletin provider

`fetch:check` (2026-10-30, headed Chrome) picked the 1 November 2026 issue, status ok.

holyfamily.us is a Zumu site that `probe url` reads as NO-PARISH-WORDS (JavaScript redirect to `/hfs/`); the browser loads it. The bulletin is on Bon Venture, not on the site; the sponsor page's header shows the address and parish name. Row: `other` with `page-pdfs` on the sponsor page.

## Not yet confirmed

The bulletin has no printed Mass-times block that was read; the times come from the Mass intentions list (Saturday 5:00 PM; Sunday 8:00, 9:30, 11:00 AM; weekdays 8:00 AM). The site's own Mass-times page was not found.
