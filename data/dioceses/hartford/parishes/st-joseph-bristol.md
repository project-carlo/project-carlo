---
name: St. Joseph Parish
website: https://stjosephbristol.org/bulletins/
bulletin_provider: unsupported
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1584
publication: []
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1584/2026-11-15.pdf
  seen: 2026-11-13
  quote: 33 Queen Street, Bristol
  note: 'Page 1 masthead of the 15 November 2026 issue (6 pages, text layer; ''NOVEMBER 15, 2026''): ''ST.
    JOSEPH PARISH/PARROQUIA SAN JOSÉ'', 33 Queen Street, Bristol 06010; Mass Schedule Saturday Vigil 4:00
    PM, Sunday 8:00 AM, 10:00 AM and 12 Noon Spanish. Page 2: Pastor Fr. Iván Ramírez. No other church
    is named.'
- url: https://stjosephbristol.org/bulletins/
  seen: 2026-11-13
  note: The parish site's 'Bulletins' menu item links sponsors.bonventure.net/?page=1584, which lists
    issues up to pdfs/1584/2026-11-15.pdf. The /bulletins/ page itself shows an old self-upload (wp-content/uploads/2025/07/2025-07-27.pdf).
bulletin_status: available
fetch_gap:
  kind: tls-certificate-unverified
  seen: 2026-11-13
  note: 'The bulletin is the current PDF on bonventure.net''s sponsors page (?page=1584, links pdfs/1584/<YYYY-MM-DD>.pdf).
    fetch:check on 2026-11-13 (provider set to other for the check) resolved page-pdfs on http://sponsors.bonventure.net/?page=1584
    to https://sponsors.bonventure.net/pdfs/1584/2026-11-15.pdf (''current''), but the download failed:
    ''SSL: CERTIFICATE_VERIFY_FAILED ... unable to get local issuer certificate''. Over http the page
    and PDF load (probe get, probe pdf).'
  url: http://sponsors.bonventure.net/pdfs/1584/2026-11-15.pdf
---

## Publisher

St. Joseph Parish / Parroquia San José, Bristol publishes one weekly bulletin through bonventure.net (page 1584). The 15 November 2026 issue (6 pages, text layer) has the masthead on page 1: "ST. JOSEPH PARISH/PARROQUIA SAN JOSÉ", 33 Queen Street, Bristol, with the Mass schedule; page 2 names Fr. Iván Ramírez, Pastor.

## Worship sites

One: St. Joseph Church, 33 Queen Street (`st-joseph-bristol`; directory 49, GCatholic 22047). Saturday Vigil 4:00 PM; Sunday 8:00 AM, 10:00 AM and 12 Noon (Spanish). The issue names no other church.

## Website and bulletin provider

`unsupported`, with a `fetch_gap` of kind `tls-certificate-unverified`. The recipe `page-pdfs http://sponsors.bonventure.net/?page=1584` resolves this week's issue (`fetch:check` 2026-11-13, run with the provider set to `other`: "page-pdfs on http://sponsors.bonventure.net/?page=1584: current", `pdfs/1584/2026-11-15.pdf`), but the link resolves to https and the download fails certificate verification. Over http the PDF loads. Once the fetcher can download it, set the provider to `other` and clear the gap. The site's /bulletins/ page itself only shows an old self-uploaded issue (27 July 2025); the menu's Bulletins link goes to bonventure.

## Not yet confirmed

Nothing open about the parish's structure.
