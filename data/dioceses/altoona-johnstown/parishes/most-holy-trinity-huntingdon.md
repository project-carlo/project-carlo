---
name: Most Holy Trinity Parish, Huntingdon
website: https://mhtcc.org/bulletins/
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://mhtcc.org/bulletins/']
group: ''
evidence:
- url: https://mhtcc.org/wp-content/uploads/2026/10/Most-Holy-Trinity-Church-Bulletin-%E2%80%93-October-18-2026.pdf
  seen: 2026-10-21
  quote: 'Rev. Mark Reid: Administrator'
  note: 'Newsletter for 18 October 2026 (3 pages, text layer; read with curl and a Chrome user agent, because probe pdf is refused). Page 1 masthead: "Most Holy Trinity Catholic Church" with "524 Mifflin Street, Huntingdon, PA 16652". Page 2 lists Saturday 24 October "Anticipated Mass 4:00 PM" and Sunday 25 October "10:30 AM", and weekday Masses at 11:00 AM on Monday, Wednesday and Friday. The word "Dudley" does not occur anywhere in it, and the only "Immaculate" is the closing prayer ("Through your Holy and Immaculate Conception").'
- url: https://mhtcc.org/bulletins/
  seen: 2026-10-21
  note: 'The parish site''s Bulletins page (WordPress, SiteGround) lists one dated PDF per week or two: 18 Oct, 4 Oct, 27 Sep, 20 Sep, 13 Sep, 6 Sep, 30 Aug, 23 Aug, 9 Aug and 2 Aug 2026, all at /wp-content/uploads/YYYY/MM/Most-Holy-Trinity-Church-Bulletin-%E2%80%93-<Month>-<D>-2026.pdf. No publisher id (visit.py --bulletin: "bulletin PDFs but no publisher id: looks self-hosted").'
- url: https://mhtcc.org/sacraments-liturgies/about-us/
  seen: 2026-10-21
  quote: Mass Schedules
  note: 'Parish site: "Saturday – 4:00 PM  Sunday – 10:30 AM  Monday – 11:00 AM (Daily Chapel)  Wednesday – 11:00 AM (Daily Chapel)  Friday – 11:00 AM (Daily Chapel)"; Confession Saturday 3:00 PM.'
- url: https://discovermass.com/church/most-holy-trinity-huntingdon-pa/
  seen: 2026-10-21
  quote: There are currently no bulletins available for Most Holy Trinity.
  note: 'A Discover Mass page exists but carries no bulletin and no Visit Website link, so it is not a live channel.'


---

## Publisher

Most Holy Trinity Catholic Church, Huntingdon publishes its own weekly newsletter on its own
WordPress site. The issue read on 2026-10-21 is the one for 18 October 2026, whose masthead
reads "Most Holy Trinity Catholic Church, 524 Mifflin Street, Huntingdon, PA 16652", with
"Rev. Mark Reid: Administrator" first in the Pastoral Team box. Its Mass Intentions are for
Huntingdon only (Saturday 4:00 PM anticipated Mass, Sunday 10:30 AM, weekday 11:00 AM) and it
does not name Dudley or Immaculate Conception Parish.

**Huntingdon and Dudley: two bulletins (or at least, not one).** The lead said both
parishes share a pastor, Rev. Mark R. Reid. That is plausible but this bulletin does not say
it: Dudley appears nowhere in the 18 October issue, and Dudley's own channels are separate
(see parishes/immaculate-conception-dudley). With no joint bulletin, the rows stay separate.

## Worship sites

One church, Most Holy Trinity (churches/most-holy-trinity-huntingdon), the weekend and weekday
Mass site named in the bulletin and on the parish site. The diocese directory adds a Sunday
6:00 PM Mass "at Juniata College" (a campus Mass in Tussey Hall, academic year only); neither
the bulletin nor the parish site lists it, so it is not a church of this parish. It is in
open/juniata-college-tussey-hall-huntingdon.

## Website and bulletin provider

`bulletin_provider: other`, `website: https://mhtcc.org/bulletins/` (the diocese directory's
homepage is https://mhtcc.org/, which links to it). `publication: url:https://mhtcc.org/bulletins/`.
The site links its PDFs with `http://` URLs. The first `pnpm fetch:check --diocese
altoona-johnstown --parish most-holy-trinity-huntingdon` on 2026-10-21 picked this week's issue
but crashed sending the decoded file name (it has an en dash, "Bulletin – October 18") as the
`Referer` header; the fetch code now percent-encodes it. Rerun the same day it returned `ok`:
"page-pdfs on https://mhtcc.org/bulletins/: current", the 18 October 2026 PDF (1,212,516 bytes,
fetched over `http://`), recipe `page-pdfs`. A plain-http fetch of that PDF with another user
agent has been seen to get a SiteGround sgcaptcha page (HTTP 202, 265 bytes) instead.

## Not yet confirmed

Whether Fr. Reid also serves Dudley is not shown by any
bulletin read here.
