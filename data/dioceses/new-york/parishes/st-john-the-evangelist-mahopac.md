---
name: St. John the Evangelist, Mahopac
website: https://sjte.online
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1630
publication: ['url:http://sponsors.bonventure.net/?page=1630', 'url:https://sjtemahopac.flocknote.com/home/notes']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1630/2026-11-01.pdf
  seen: 2026-10-31
  quote: CHURCH OF ST. JOHN THE EVANGELIST
  note: Masthead of the 1 November 2026 issue, page 1, names St. John the Evangelist, 221 East Lake Boulevard,
    Mahopac, alone, with All Saints' Day Mass times 7:30, 9:00, 10:15, 11:30 AM and 5:30 PM. 12 pages,
    all with text.
- url: http://sponsors.bonventure.net/?page=1630
  seen: 2026-10-31
  note: Bon Venture sponsor page lists pdfs/1630/2026-11-01.pdf as the newest issue.
- url: https://sjte.online
  seen: 2026-10-31
  quote: Sunday Bulletin
  note: Parish homepage, rendered in headed Chrome; its Sunday Bulletin link goes to http://sponsors.bonventure.net/?page=1630.
- url: https://sjtemahopac.flocknote.com/home/api/mynotes
  seen: 2026-10-31
  quote: Bulletin and Mass Schedule for 11\/1\/2026
  note: Anonymous Flocknote notes feed; note 39208418 attaches 11012026 Final.pdf, the same issue as Bon
    Venture's. A second channel, not a second publisher.
- url: https://sjtemahopac.flocknote.com/note/38887047/file/656720/10112026final.pdf
  seen: 2026-10-10
  quote: 'Saturday Evening Vigil: 4:00 p.m.'
  note: October 11, 2026 full bulletin downloaded and read October 10. Masthead locates Church of St.
    John the Evangelist at 221 East Lake Boulevard.
- url: http://sponsors.bonventure.net/pdfs/1630/2026-11-08.pdf
  seen: 2026-11-08
  quote: CHURCH OF ST. JOHN THE EVANGELIST
  note: 'Masthead of the 8 November 2026 issue, page 1, names St. John the Evangelist, 221 East Lake Boulevard,
    Mahopac, alone. fetch:check on 8 November picked this issue from the pinned recipe: transport ok,
    PDF, identity matched, fresh.'
promoted: 2026-11-09
research:
- method: fetch-check resolver (main, 31 Oct) on the Flocknote notes feed, auto and dated-post
  url: https://sjtemahopac.flocknote.com/home/notes
  checked: '2026-10-31'
  outcome: unsupported-format
  next_action: None needed while Bon Venture 1630 stays current; a Flocknote collector would make this
    a fallback
  retry_when: Bon Venture 1630 stops receiving new issues
- method: headed browser on sjte.online, then fetch-check on Bon Venture page 1630
  url: http://sponsors.bonventure.net/?page=1630
  checked: '2026-10-31'
  outcome: found
- method: fetch:check --diocese new-york with the pinned Bon Venture recipe
  url: http://sponsors.bonventure.net/?page=1630
  checked: '2026-11-08'
  outcome: found
bulletin_status: available
---

## Publisher

St. John the Evangelist, Mahopac publishes its own weekly bulletin. The parish site https://sjte.online (eCatholic site 5771, readable in a headed browser on 31 October 2026) has a "Sunday Bulletin" link to Bon Venture sponsor page 1630, which lists `pdfs/1630/2026-11-01.pdf`. That 12-page issue, read 31 October, has the masthead "CHURCH OF ST. JOHN THE EVANGELIST, 221 East Lake Boulevard, Mahopac, New York 10541" with the All Saints' Day Mass times (7:30, 9:00, 10:15, 11:30 AM and 5:30 PM) and Mass intentions for 31 October to 8 November, including "7:30 P.M. Spanish Mass (Chapel)" on Saturdays. It names no other church.

The same issues are also posted as PDF attachments on the parish's Flocknote notes (latest on 31 October: "Bulletin and Mass Schedule for 11/1/2026", note 39208418; earlier, note 38887047 carried the 11 October issue). That is a second channel for one bulletin, not a second publisher.

## Worship sites

[St. John the Evangelist](../churches/st-john-the-evangelist-mahopac.md), 221 East Lake Boulevard. The bulletin's "(Chapel)" Spanish Mass is a chapel inside the parish complex; no separate building has been identified, so no second church record is made.

## Website and bulletin provider

`other`, read from Bon Venture: `page-pdfs http://sponsors.bonventure.net/?page=1630`. Bon Venture names each issue by its Sunday date, newest first. fetch:check picked `pdfs/1630/2026-11-01.pdf` on 31 October and `pdfs/1630/2026-11-08.pdf` on 8 November, each the current issue with the St. John the Evangelist masthead; automatic resolution from https://sjte.online chose the same recipe.

Until October the row was held off the site as `no_bulletin`, because the only channel found then was the Flocknote feed, which main's collectors cannot read (the feed renders no links; each note's PDF is a signed attachment). sjte.online failed TLS from the October research machine and so its Bon Venture link was not seen. The Flocknote channel no longer matters for fetching, so the row carries no `fetch_gap`.

## Not yet confirmed

The street number: the bulletin and archdiocese say 221 East Lake Boulevard, GCatholic says 225 (see the church record).
