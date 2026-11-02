---
name: St. Cecilia
website: https://www.stceciliaparish.net
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2137
publication: ['url:http://sponsors.bonventure.net/?page=2137']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/2137/2026-11-01.pdf
  seen: 2026-11-02
  quote: 10 KINGSTON LANE • MONMOUTH JUNCTION, NJ 08852
  note: 'Page 1 of the 1 November 2026 issue (16 pages; pages 9 to 11 are images): ''ST. CECILIA ... The
    Catholic Community of 10 KINGSTON LANE • MONMOUTH JUNCTION, NJ 08852'', ''Rev. Charles T. O’Connor
    ----- Pastor'', Mass Schedule ''Saturday 5:00 pm; Sunday 8:30 & 11:00 am; Weekdays Monday, Wednesday,
    Thursday & Friday 8:00 am; Tuesday 7:00 pm; Holy Days 8:00 am, 12:15 & 7:00 pm''. Names no other church.'
- url: https://www.stceciliaparish.net/
  seen: 2026-11-02
  quote: BULLETINS
  note: The parish's eCatholic site (id 22492) has a top-menu 'Bulletins' item that links to http://sponsors.bonventure.net/?page=2137
    (visit.py --follow). The eCatholic id is the website's; no bulletin is hosted under it.
- url: http://sponsors.bonventure.net/?page=2137
  seen: 2026-11-02
  quote: pdfs/2137/2026-11-01.pdf
  note: 'Bonventure listing for account 2137 (HTML source): links pdfs/2137/2026-11-01.pdf, 2026-10-25,
    2026-10-18, 2026-10-11 ... one per Sunday, newest first.'
bulletin_status: available
publication_reviews:
- parish: most-holy-redeemer-matawan
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2137/2026-11-01.pdf
    seen: 2026-11-02
    note: The 1 November 2026 masthead names St. Cecilia, 10 Kingston Lane, Monmouth Junction alone, with
      its own Mass times and pastor Rev. Charles T. O’Connor. Bonventure account 2137 is a separate account
      from Most Holy Redeemer, Matawan's (?page=2238); the shared host is a hosting account, not a shared
      bulletin.
- parish: immaculate-conception-spotswood
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2137/2026-11-01.pdf
    seen: 2026-11-02
    note: The 1 November 2026 masthead names St. Cecilia, 10 Kingston Lane, Monmouth Junction alone, with
      its own Mass times and pastor Rev. Charles T. O’Connor. Bonventure account 2137 is a separate account
      from Immaculate Conception, Spotswood's (?page=2152); the shared host is a hosting account, not
      a shared bulletin.
---

## Publisher

St. Cecilia, 10 Kingston Lane, Monmouth Junction, publishes its own weekly bulletin through Bonventure (sponsors.bonventure.net account 2137). Page 1 of the 1 November 2026 issue (read 2026-11-02) is headed 'ST. CECILIA ... The Catholic Community of 10 KINGSTON LANE, MONMOUTH JUNCTION, NJ 08852' and names 'Rev. Charles T. O’Connor, Pastor', which matches the finder's pastor line. It names no other church or parish.

## Worship sites

One church, 10 Kingston Lane (directory:24509, gcatholic:18645). The masthead's Mass schedule lists one site; the finder's Mass list for this entry is empty.

## Website and bulletin provider

Website: https://www.stceciliaparish.net (eCatholic site 22492; `probe url` says DEAD-DNS and `probe get` 403, the browser loads it). Its 'Bulletins' menu item points to the Bonventure listing, as at Most Holy Redeemer, Matawan, so the provider is `other` with recipe `page-pdfs http://sponsors.bonventure.net/?page=2137`, and the eCatholic id isn't recorded as a publication.

## Not yet confirmed

Nothing about identity or the Mass schedule. The Mass schedule was read from the bulletin masthead, not the eCatholic site's own Mass page.

## Fetch check

`pnpm fetch:check` on 2026-11-02 resolved `page-pdfs http://sponsors.bonventure.net/?page=2137` and picked `pdfs/2137/2026-11-01.pdf`: transport ok, PDF (7.2 MB), issue date 2026-11-01 inferred from the file name, freshness `fresh` (1 day). Identity isn't checked by the tool; I read the masthead myself (above). No `recipe` line was printed, so the pinned recipe stays as set.
