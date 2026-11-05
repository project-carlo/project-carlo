---
name: Resurrection
website: https://resurrectionparishnj.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1554
publication: ['url:http://sponsors.bonventure.net/?page=1554']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1554/2026-11-01.pdf
  seen: 2026-11-04
  quote: OCTOBER 31 - NOVEMBER 01, 2026
  note: 'Page 1 masthead names Resurrection Parish, 651 MILLBROOK AVE. RANDOLPH, NJ, www.resurrectionparishnj.org,
    with its Regular Mass & Liturgy Schedule (Saturday 5:00pm; Sunday 8:45am, 11:15am & 7:00pm; Daily
    Mass Monday to Saturday 9:00am). Page 2: Pastor Fr. Yojaneider Garcia.'
- url: https://resurrectionparishnj.org/bulletins
  seen: 2026-11-04
  note: Read with parish-site-access visit.py. The page links 'Bulletins' to http://sponsors.bonventure.net/?page=1554;
    its 'Archived Bulletins' list of files.ecatholic.com/28421/bulletins/ PDFs ends with October 26, 2025.
- url: http://sponsors.bonventure.net/?page=1554
  seen: 2026-11-04
  note: Bon Venture sponsor page; probe url finds the bulletin link http://sponsors.bonventure.net/pdfs/1554/2026-11-01.pdf.
research:
- method: visit.py --links on the eCatholic /bulletins page (site id 28421)
  url: https://resurrectionparishnj.org/bulletins
  checked: '2026-11-04'
  outcome: not-found
  next_action: None needed while the Bon Venture page carries the bulletin; re-check the eCatholic archive
    only if the Bon Venture page stops updating
  retry_when: The Bon Venture page shows no issue newer than 30 days
bulletin_status: available
---

## Publisher

Resurrection Parish, Randolph publishes its own weekly bulletin through Bon Venture (sponsor page 1554). The issue for 31 October-1 November 2026 (`http://sponsors.bonventure.net/pdfs/1554/2026-11-01.pdf`, read 2026-11-04 with probe pdf; the text layer reads) has on page 1 "Resurrection Parish ... OCTOBER 31 - NOVEMBER 01, 2026 – ALL SAINTS DAY ... 651 MILLBROOK AVE. RANDOLPH, NJ", with the website www.resurrectionparishnj.org and phone 973-895-4224. Page 2 names "Pastor: Fr. Yojaneider Garcia".

## Worship sites

- `resurrection-randolph`: the only church. Page 1's "Regular Mass & Liturgy Schedule" (Saturday 5:00pm; Sunday 8:45am, 11:15am & 7:00pm; Daily Mass Monday to Saturday 9:00am) names no other place, and a grep of the issue for chapel, nursing and mission found no other worship site.

The diocese's finder (directory:28421) and GCatholic (19016) both list this one church.

## Website and bulletin provider

`resurrectionparishnj.org` is the parish's eCatholic site (site id 28421, the finder's pin id). `probe url` read it on 2026-11-04 and found the Bon Venture link. Its /bulletins page (read with visit.py) links "Bulletins" to the Bon Venture sponsor page, and below it an "Archived Bulletins" list of `files.ecatholic.com/28421/bulletins/` PDFs whose newest is 26 October 2025, so the eCatholic id is a stale archive, not this bulletin's publication, and is not recorded. Provider `other` with the recipe `page-pdfs http://sponsors.bonventure.net/?page=1554`; `fetch:check` on 2026-11-04 resolved it to `http://sponsors.bonventure.net/pdfs/1554/2026-11-01.pdf` (the 1 November 2026 issue, 3 days old: fresh). It reports identity unverified (no expected identity supplied); the masthead was checked by hand above.

## Not yet confirmed

Nothing open.
