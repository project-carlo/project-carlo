---
name: Christ the King, Jersey City
website: https://christthekingjerseycity.org/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/693
publication: ['url:https://www.church-bulletin.org/christ-the-king-roman-catholic-parish-jersey-city-nj-07304']
group: Planning Area F
evidence:
- url: https://www.church-bulletin.org/bulletin/christ-the-king-roman-catholic-parish-jersey-city-nj-07304/2026-11-01.pdf
  seen: 2026-11-03
  note: '1 November 2026 issue, 6 pages, image only (read with render.py). Page 1 masthead: ''Christ the
    King Church'', ''768 Ocean Ave, Jersey City, NJ 07304'', ''November 1, 2026 - Solemnity of All Saints'',
    ''www.christthekingjerseycity.org''; Pastor Rev. Esterminio ''Mino'' Chica; Mass Times Sunday 8AM
    and 10AM, Monday/Wednesday/Thursday/Friday 9AM. Page footers ''693-Christ the King''. Pages 1-2 name
    no other parish.'
- url: https://church-bulletin.org/693
  seen: 2026-11-03
  note: John Patrick listing 'Christ the King Roman Catholic Parish Bulletin' (slug christ-the-king-roman-catholic-parish-jersey-city-nj-07304),
    dated issues through 2026-11-01. Suffixed listings 693A, 693B, 693O, 693S, 693L show the empty archive
    page.
- url: https://christthekingjerseycity.org/
  seen: 2026-11-03
  note: 'eCatholic site (ecatholic:22793) behind Cloudflare: probe url HTTP 403, read with parish-site-access
    visit.py. ''Current Bulletin'' links https://www.jppc.net/onlinebulletins/693template.pdf; Sunday
    Mass 8:00 AM, 10:00 AM; daily Monday, Wednesday, Thursday, Friday 9:00 AM.'
bulletin_status: available
---

## Publisher

Christ the King, Jersey City publishes its own weekly bulletin, printed by John Patrick Publishing under account 693. I read the 1 November 2026 issue (6 pages, image only, rendered with render.py). The page 1 masthead says 'Christ the King Church, 768 Ocean Ave, Jersey City, NJ 07304', gives Rev. Esterminio 'Mino' Chica as pastor and one Mass schedule (Sunday 8AM and 10AM; Monday, Wednesday, Thursday, Friday 9AM). The page footers say '693-Christ the King'.

The batch plan notes that Christ the King and Our Lady of Sorrows share a pastor. This issue's pages 1 and 2 (masthead, clergy, sick and deceased lists, ministers, collections) name no other parish, and I found no John Patrick listing for Our Lady of Sorrows (suffixes 693A, B, O, S, L are empty; the Run's scan of ids 1-1000 and 6000-6060 has no Sorrows listing in Jersey City). So this row is Christ the King alone; see `our-lady-of-sorrows-jersey-city` for that parish.

## Worship sites

- Christ the King, 768 Ocean Ave (`christ-the-king-jersey-city`), the only church in the masthead. The directory (75) and GCatholic (18437) list only this church.

## Website and bulletin provider

https://christthekingjerseycity.org/ is an eCatholic site (ecatholic:22793) behind Cloudflare: `probe url` gets 403, and parish-site-access `visit.py` read it. Its 'Current Bulletin' links `jppc.net/onlinebulletins/693template.pdf`, so the eCatholic id is only the website and is left out of `publication`. The provider is `other`, read with `page-pdfs https://church-bulletin.org/693` (the dated listing, not `?id=`, per the playbook). The survey listed this domain among lost ones; it loads in the browser.

Fetch check (2026-11-03, headed): transport ok, PDF, resolved `page-pdfs on https://church-bulletin.org/693: current` and picked church-bulletin.org/bulletin/christ-the-king-roman-catholic-parish-jersey-city-nj-07304/2026-11-01.pdf, the 1 November 2026 issue read above (date from the file name); freshness fresh (2 days). Publication identity `unverified` only because the issue is image only; the masthead read above confirms it. The recipe is the one recorded in `provider_id`.

## Not yet confirmed

Nothing for this row.
