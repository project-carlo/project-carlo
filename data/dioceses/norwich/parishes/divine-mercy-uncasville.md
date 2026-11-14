---
name: Divine Mercy Parish
website: https://www.divinemercyfaithcommunity.org/weekly-bulletin.html
bulletin_provider: unsupported
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1498
publication: ['url:http://sponsors.bonventure.net/?page=1498']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1498/2026-11-15.pdf
  seen: 2026-11-14
  quote: Welcome to Divine Mercy Parish
  note: 'Page 1 of the November 15, 2026 bulletin: Divine Mercy Parish, office 22 Maple Avenue, Uncasville;
    names Saint John the Evangelist Church (22 Maple Avenue, Uncasville), Our Lady of Perpetual Help Church
    (63 Old Norwich Road, Quaker Hill) and Our Lady of the Lakes Church (752 Norwich-Salem Turnpike, Oakdale),
    with one Mass schedule coded SJE, OLPH, OLL.'
- url: https://www.divinemercyfaithcommunity.org/weekly-bulletin.html
  seen: 2026-11-14
  quote: Click the above link to see the recent bulletin
  note: The parish site's Weekly Bulletin page links sponsors.bonventure.net/?page=1498 for its bulletins.
- url: http://sponsors.bonventure.net/?page=1498
  seen: 2026-11-14
  note: 'probe url (http; https fails certificate verification): Bonventure ''Our Sponsors'' page linking
    the dated issue pdfs/1498/2026-11-15.pdf.'
- url: https://www.norwichdiocese.org/Portals/dioceseofnorwich/CMAdmin/Parishes_CCD9Mar26.pdf
  seen: 2026-11-14
  note: 'Diocese of Norwich List of Parishes (March 6, 2026): St. John the Evangelist, Uncasville, merged
    with Our Lady of Perpetual Help, Quaker Hill, and Our Lady of the Lakes, Oakdale (Divine Mercy Parish);
    website www.divinemercyfaithcommunity.org.'
research:
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese norwich --parish divine-mercy-uncasville,
    with the recipe page-pdfs http://sponsors.bonventure.net/?page=1498
  url: http://sponsors.bonventure.net/?page=1498
  checked: '2026-11-14'
  outcome: access-blocked
  next_action: Rerun fetch:check; if it picks this week's issue, set bulletin_provider other and clear
    fetch_gap
  retry_when: The fetcher downloads http links as given, or sponsors.bonventure.net serves a verifiable
    certificate chain
bulletin_status: available
fetch_gap:
  kind: tls-certificate-unverified
  seen: 2026-11-14
  note: fetch:check resolves page-pdfs on the Bonventure sponsors page and picks pdfs/1498/2026-11-15.pdf,
    but downloads it over https and fails with CERTIFICATE_VERIFY_FAILED (unable to get local issuer certificate);
    the same PDF reads over http with probe pdf.
  url: http://sponsors.bonventure.net/pdfs/1498/2026-11-15.pdf
---

## Publisher

Divine Mercy Parish (St. John the Evangelist, Uncasville; Our Lady of Perpetual Help, Quaker Hill; Our Lady of the Lakes, Oakdale, merged per the diocese's List of Parishes, March 6, 2026) publishes one weekly bulletin through Bonventure, a bulletin and ad printer. The November 15, 2026 issue (http://sponsors.bonventure.net/pdfs/1498/2026-11-15.pdf, read 2026-11-14) has on page 1 "Welcome to Divine Mercy Parish", the office at 22 Maple Avenue, Uncasville, and the three churches with their addresses.

## Worship sites

Three churches, all in the November 15, 2026 page 1 schedule: Saturday Vigil 4:00 pm SJE, 5:00 pm OLL; Sunday 8:00 and 9:30 am OLPH, 8:00 and 10:15 am OLL, 11:00 am SJE; weekday Masses at all three. The diocese lists no other church in this parish.

## Website and bulletin provider

The parish's Weebly site (divinemercyfaithcommunity.org) has a Weekly Bulletin page that links the Bonventure sponsors page http://sponsors.bonventure.net/?page=1498, which links the current issue as pdfs/1498/<YYYY-MM-DD>.pdf. The host fails certificate verification over https and answers over http (probe url and probe pdf read it that way on 2026-11-14).

fetch:check (2026-11-14) resolves the recipe `page-pdfs http://sponsors.bonventure.net/?page=1498` to the November 15, 2026 issue but downloads it over https and fails certificate verification, so the row is `unsupported` with a `fetch_gap` until the fetcher can collect it. The recipe is kept in `provider_id` for that day.

## Not yet confirmed

Whether the fetcher can be made to read this host (see research).
