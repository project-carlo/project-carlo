---
name: Saint Anselm Parish
website: https://www.stanselmparish.com
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=10314
publication: ['url:http://sponsors.bonventure.net/?page=10314']
group: ''
evidence:
- url: http://sponsors.bonventure.net/?page=10314
  seen: 2026-10-29
  quote: Click to View Current Bulletin
  note: 'Bon Venture sponsor page 10314: ''St. Anselm Church, 12670 Dunks Ferry Road, Philadelphia, PA
    19154'', linking the parish website, a current-bulletin PDF (pdfs/10314/2026-10-25.pdf) and a weekly
    archive back to January 2026 and earlier. Fetched over http:// (Bon Venture sends no intermediate
    certificate). The parish home page links this page (''sponsors.bonventure.net/?page=10314'', seen
    with visit.py).'
- url: http://sponsors.bonventure.net/pdfs/10314/2026-10-25.pdf
  seen: 2026-10-29
  quote: 12670 DUNKS FERRY ROAD
  note: '25 October 2026 issue (12 pages, text layer, md5 ded4ceb808fe5cf88ca5a5109846fdab). Page 1: ''Saint
    Anselm Parish, 12670 DUNKS FERRY ROAD, PHILADELPHIA, PA 19154'', ''Thirtieth Sunday in Ordinary Time,
    October 25, 2026'', Parish Center 215-637-3525, ''Rev. Jeffrey M. Stecz ... Pastor'', Rev. Bernard
    O. Ekeagwu Parochial Vicar. MASS SCHEDULE: Saturday vigil 4:30 PM; Sunday 8:00 AM, 10:00 AM and 12:00
    NOON; Monday-Friday 8:30 AM; Saturday 8:00 AM. Names this parish alone.'
- url: https://www.stanselmparish.com/bulletins
  seen: 2026-10-29
  note: 'eCatholic 24649 /bulletins (visit.py, Chrome; probe url answers 403): the newest bulletin file
    is files.ecatholic.com/24649/bulletins/20220109.pdf, 9 January 2022, so the archive stopped nearly
    five years ago. The home page ''WEEKLY BULLETIN'' heading links the Bon Venture page. Its only current
    PDF on the home page is a ''St. Lukes Open Flyer''.'
- url: https://www.church-bulletin.org/saint-anselm-church-philadelphia-pa-19154
  seen: 2026-10-29
  note: 'John Patrick listing ''Saint Anselm Church'', Philadelphia, PA 19154 (12670 Dunks Ferry Road,
    215-637-3525): no editions, only the daily-readings widget. The parish prints with Bon Venture, not
    John Patrick.'
- url: https://archphila.org/parish/st-anselm-philadelphia/
  seen: 2026-10-28
  quote: Rev. Jeffrey Stecz
  note: Directory Pastor line; Mass times match the bulletin (Sat 4:30 PM; Sun 8, 10 AM, Noon; weekdays
    8:30 AM; Saturday 8 AM).
research:
- method: probe url (403), visit.py on the home page and /bulletins in Chrome, John Patrick listing, Bon
    Venture sponsor page and 25 October issue
  url: http://sponsors.bonventure.net/?page=10314
  checked: '2026-10-29'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: st-christopher-philadelphia
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/10314/2026-11-01.pdf
    seen: 2026-10-29
    note: The 1 November 2026 masthead (page 1) names Saint Anselm Parish, 12670 Dunks Ferry Road, Philadelphia
      19154, pastor Rev. Jeffrey M. Stecz; Bon Venture sponsor page 10314.
  - url: http://sponsors.bonventure.net/pdfs/1904/2026-11-01.pdf
    seen: 2026-10-29
    note: The 1 November 2026 masthead (page 1) names Saint Christopher parish and school alone, with
      its own sacraments box; Bon Venture sponsor page 1904.
- parish: corpus-christi-lansdale
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/10314/2026-11-01.pdf
    seen: 2026-10-29
    note: The 1 November 2026 masthead (page 1) names Saint Anselm Parish, 12670 Dunks Ferry Road, Philadelphia
      19154, pastor Rev. Jeffrey M. Stecz; Bon Venture sponsor page 10314.
  - url: http://sponsors.bonventure.net/pdfs/1906/2026-11-01.pdf
    seen: 2026-10-29
    note: The 1 November 2026 issue is the bulletin for Corpus Christi Parish, Lansdale (page 1 lists
      pastor Rev. John D. Schiele and its own staff); Bon Venture sponsor page 1906. Only the bonventure.net
      host is shared.
---

## Publisher

Saint Anselm Parish's current bulletin is a **Bon Venture Services** issue: sponsor page 10314 lists dated `pdfs/10314/<yyyy-mm-dd>.pdf` files, newest 25 October 2026 (text layer, masthead and Mass schedule quoted above), and the parish home page links that page. The parish's eCatholic archive (24649) stopped on 9 January 2022 and its John Patrick listing has no editions, which is why the survey found no bulletin. The row is `other`, `page-pdfs http://sponsors.bonventure.net/?page=10314`.

## Worship sites

One: St. Anselm Church, 12670 Dunks Ferry Road. The Mass schedule lists no other place. The 'Spirituality Center Chapel' in the bulletin is for Monday adoration and a rosary and benediction, with no Mass line; St. Anselm School (stanselmschoolphila.com) is a school.

## Website and bulletin provider

stanselmparish.com is the parish's eCatholic site (id 24649; `probe url` answers 403 and the site loads in Chrome). It hosts no current bulletin, so `ecatholic:24649` is not a publication id here. Recipe `page-pdfs http://sponsors.bonventure.net/?page=10314`, which lists next Sunday's PDF early (freshness may read `future`).

## Fetch check

`fetch:check` (2026-10-29) with the pinned `page-pdfs` recipe picked `pdfs/10314/2026-10-25.pdf` on the Bon Venture page: transport ok, PDF, fresh (issue age 4 days, date observed in the document text); identity `unverified` because the check is given no expected identity (masthead and Mass schedule read above). It printed no `recipe` line, as the pinned `provider_id` already holds it.
