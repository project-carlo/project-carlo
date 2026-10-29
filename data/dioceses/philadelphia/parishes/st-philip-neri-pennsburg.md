---
name: St. Philip Neri
website: https://www.spnparish.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/church-of-saint-philip-neri-pennsburg-pa-18073
publication: ['url:https://www.church-bulletin.org/church-of-saint-philip-neri-pennsburg-pa-18073']
group: ''
evidence:
- url: https://www.church-bulletin.org/bulletin/church-of-saint-philip-neri-pennsburg-pa-18073/2026-10-25.pdf
  seen: 2026-10-29
  quote: Daily Masses are celebrated in the Saint Anne Chapel.
  note: 'John Patrick listing 59, issue of 25 October 2026 (12 pages, text layer, md5 1f9d790147a9edf4bebcfac5f5caa41c).
    Page 2 masthead ''Church of Saint Philip, Pennsburg, PA'', Rev. Michael Saban, Pastor, ''Church &
    Rectory Address: 1325 Klinerd Rd; Pennsburg 18073''; Sunday Mass Schedule Saturday vigil 4:00 PM,
    Sunday 7:30 AM and 10:00 AM; weekday Masses Monday to Friday 8AM in the Saint Anne Chapel; First Friday
    Mass 9:00 AM in Church.'
- url: https://www.church-bulletin.org/church-of-saint-philip-neri-pennsburg-pa-18073
  seen: 2026-10-29
  quote: Latest Edition
  note: Listing 59 'Church of Saint Philip Neri', Pennsburg, PA 18073; latest edition October 25, 2026.
- url: https://www.spnparish.org/pages/parish-bulletins
  seen: 2026-10-29
  note: The parish's own Parish Bulletins page (probe get HTTP 200) lists weekly files from spn-bulletin-10-26-2025.pdf
    to spn-bulletin-10-25-2026.pdf on a cloudfront host. The 25 October 2026 file is byte-identical (md5
    1f9d790147a9edf4bebcfac5f5caa41c) to the listing's, so both channels carry the same issue.
bulletin_status: available
---

## Publisher

St. Philip Neri, Pennsburg (Rev. Michael Saban, pastor) is a single-parish bulletin: John Patrick Publishing's listing 59 ('Church of Saint Philip Neri', Pennsburg, PA 18073). The 25 October 2026 issue, page 2, is headed 'Church of Saint Philip, Pennsburg, PA' with 'Church & Rectory Address: 1325 Klinerd Rd; Pennsburg 18073' and one Sunday and one weekday Mass schedule. The parish's own site posts the same files: the 25 October 2026 PDF on its Parish Bulletins page is byte-identical (md5) to the listing's.

## Worship sites

One church, `st-philip-neri-pennsburg`. Weekday Masses (Monday to Friday 8AM) are 'celebrated in the Saint Anne Chapel', and the weekday Adoration is there too; the bulletin and the directory ('Adoration in St. Anne Chapel') give it no street of its own, and the church and rectory sit at 1325 Klinerd Rd. It is treated as a room of the campus, its Masses on the church's row, per the diocese rule for a named chapel without a separate address. Not yet confirmed: whether St. Anne Chapel is a separate building (the bulletin never says); a visit to spnparish.org's 'About' pages would settle it.

The original St. Philip Neri Church in East Greenville (built 1919) is not a worship site: the archdiocese's decree (dated 9 December 2022, effective 23 January 2023) relegated it to profane but not sordid use and states 'The original church has not been used for divine worship of any kind since 1968'. It has its own excluded record (`st-philip-neri-east-greenville`). The directory still lists the parish's Religious Education Center and Catholic Family Life Center at 26 E. 6th St., East Greenville; those are offices and a hall, and the bulletin lists no Mass there.

The directory's Saturday vigil (5 PM) differs from the bulletin's (4:00 PM); the bulletin wins.

## Website and bulletin provider

`other`, reading `page-pdfs` on the John Patrick listing; the parish's own site (`spnparish.org/pages/parish-bulletins`, files `spn-bulletin-<mm>-<dd>-<yyyy>.pdf` on a cloudfront host) is an equal second channel, oldest issue listed first, so the listing is the safer newest-first channel. If the listing stops, switch the recipe to the parish page.

## Fetch check

`fetch:check` (2026-10-29, headed Chrome) with the `page-pdfs` recipe in `provider_id` picked `https://www.church-bulletin.org/bulletin/church-of-saint-philip-neri-pennsburg-pa-18073/2026-10-25.pdf`: transport ok, PDF, fresh (4 days); issue date inferred from the file name. The check printed no separate recipe; the one in `provider_id` is the one used. Identity is `unverified` only because the check is given no expected identity; the masthead was read from the file (above).
