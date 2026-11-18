---
name: St. Theresa & St. Christopher
website: http://sponsors.bonventure.net/?page=4286
bulletin_provider: unsupported
provider_id: page-pdfs http://sponsors.bonventure.net/?page=4286
publication: ['url:http://sponsors.bonventure.net/?page=4286']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/4286/2026-11-15.pdf
  seen: 2026-11-15
  quote: 9:30am at Saint Christopher
  note: 15 November 2026 issue, 6 pages. Page 1 masthead 'The Catholic Faith Communities of Saint Theresa
    & Saint Christopher' (decorative font; the text layer drops letters), '265 Stafford Road | Tiverton,
    RI 02878' and '1554 Main Road | Tiverton, RI 02878'; 'Rev. Phillip J. Dufour, Pastor'; trustees of
    both Saint Theresa Parish and St. Christopher Parish; '33rd Sunday in Ordinary Time ~ November 15,
    2026 ~'; Weekend Masses Saturday 4:00pm at Saint Theresa, Sunday 8:00am at Saint Theresa, 9:30am at
    Saint Christopher, 11:00am at Saint Theresa; weekdays Monday-Wednesday 8:00am at Saint Theresa, Thursday
    8:00am at Saint Christopher.
- url: https://sstandctiverton.org/bulletins
  seen: 2026-11-15
  note: Parish Squarespace site's Bulletins page links http://sponsors.bonventure.net?page=4286, which
    lists dated issues pdfs/4286/YYYY-MM-DD.pdf newest first (2026-11-15, 2026-11-08, 2026-11-01...).
bulletin_status: available
fetch_gap:
  kind: tls-certificate-unverified
  seen: 2026-11-15
  note: 'The bulletin is the current PDF on bonventure.net''s sponsors page (?page=4286, links pdfs/4286/<YYYY-MM-DD>.pdf).
    fetch:check on 2026-11-15 (provider other, page-pdfs on http://sponsors.bonventure.net/?page=4286)
    picked https://sponsors.bonventure.net/pdfs/4286/2026-11-15.pdf (''fresh'') but the download failed:
    ''SSL: CERTIFICATE_VERIFY_FAILED ... unable to get local issuer certificate''. Over http the page
    and PDF load (probe get, probe pdf).'
  url: http://sponsors.bonventure.net/pdfs/4286/2026-11-15.pdf
---

## Publisher

St. Theresa and St. Christopher, Tiverton, two canonical parishes under one pastor (Rev. Phillip J. Dufour, finder 12222 and 12224), publish one weekly bulletin through Bon Venture (sponsors page 4286). The 15 November 2026 issue (http://sponsors.bonventure.net/pdfs/4286/2026-11-15.pdf), page 1, is headed "The Catholic Faith Communities of Saint Theresa & Saint Christopher", gives both addresses (265 Stafford Road and 1554 Main Road, Tiverton), "Rev. Phillip J. Dufour, Pastor", the trustees of both parishes, and one Mass schedule for both churches.

## Worship sites

- St. Theresa, 265 Stafford Rd.: Saturday 4:00pm, Sunday 8:00am and 11:00am, Monday-Wednesday 8:00am.
- St. Christopher, 1554 Main Rd.: Sunday 9:30am, Thursday 8:00am.

The finder and GCatholic list these two buildings (12222/22439, 12224/22441) and nothing else for this pair. (The finder's St. Christopher entry gives 265 Stafford Road, the shared office, and Saturday 4:30 PM "at St. Theresa Church"; the bulletin's schedule is the current one.)

## Website and bulletin provider

The parish site's Bulletins page (https://sstandctiverton.org/bulletins) links the Bon Venture sponsors page http://sponsors.bonventure.net/?page=4286, which lists every issue as pdfs/4286/YYYY-MM-DD.pdf, newest first. `fetch:check` on 2026-11-15 with `other` / `page-pdfs http://sponsors.bonventure.net/?page=4286` picked https://sponsors.bonventure.net/pdfs/4286/2026-11-15.pdf, the issue read above, but the download failed certificate verification. So the row is `unsupported` with fetch_gap `tls-certificate-unverified`, as the playbook settles for Bon Venture; the `page-pdfs` recipe is kept in provider_id for when a collector handles it.

## Not yet confirmed

Nothing about the parish is open; the row waits for a collector that can download Bon Venture's https PDFs (see fetch_gap).
