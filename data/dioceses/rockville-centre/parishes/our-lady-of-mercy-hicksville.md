---
name: Our Lady of Mercy Roman Catholic Church
website: https://www.ourladyofmercy.org/Bulletin.php
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.ourladyofmercy.org/Bulletin.php']
group: ''
evidence:
- url: https://www.ourladyofmercy.org/BulletinArchive/Current.pdf
  seen: 2026-11-12
  quote: Sunday, November 8, 2026
  note: 'Page 2 of the 8 November 2026 issue ("OLM Weekly", 8 pages; Last-Modified 6 Nov 2026), Masses
    for the Week: Sunday 7:30, 9:00, 10:30 AM, 12:00 PM, 5:30 PM; Saturday 14 November "4:30 PM Parishioners
    of Our Lady of Mercy". The file is overwritten weekly, so this quote holds only for that issue. Downloaded
    through Chrome (tools/browser_get.py): the server''s TLS chain is incomplete and probe get refuses
    it.'
- url: https://www.ourladyofmercy.org/BulletinArchive/Current.pdf
  seen: 2026-11-12
  note: 'Page 1 of the same issue (its text layer is font-scrambled; read rendered): masthead "OUR LADY
    OF MERCY ROMAN CATHOLIC CHURCH, 500 S. OYSTER BAY ROAD • HICKSVILLE • NEW YORK"; Celebrations of the
    Eucharist Saturday 8:00 AM and 4:30 PM, Sunday 7:30, 9:00, 10:30 AM, 12:00 NOON and 5:30 PM, weekdays
    7:00 and 9:00 AM. One church only.'
- url: https://www.ourladyofmercy.org/Bulletin.php
  seen: 2026-11-12
  note: The parish's Bulletin page (read with visit.py) links BulletinArchive/Current.pdf, Previous.pdf
    and FeastInnocents.pdf; no publisher id.
bulletin_status: available
fetch_gap:
  kind: tls-incomplete-chain
  seen: 2026-11-12
  note: 'The server sends an incomplete TLS certificate chain. fetch:check''s page-pdfs resolver picked
    BulletinArchive/Current.pdf but the download failed: CERTIFICATE_VERIFY_FAILED, unable to get local
    issuer certificate. Chrome completes the chain and downloads the 8 November 2026 issue.'
  url: https://www.ourladyofmercy.org/BulletinArchive/Current.pdf
---

## Publisher

Our Lady of Mercy, 500 South Oyster Bay Road, Hicksville publishes its own weekly bulletin, "OLM Weekly", on its own site. The 8 November 2026 issue (`https://www.ourladyofmercy.org/BulletinArchive/Current.pdf`, 8 pages, served 2026-11-12 with Last-Modified 6 November) has the masthead "OUR LADY OF MERCY ROMAN CATHOLIC CHURCH" with the Oyster Bay Road address, and its Mass schedule (page 1) and Masses for the Week (page 2) are for this one church: Saturday 8:00 AM and 4:30 PM, Sunday 7:30, 9:00, 10:30 AM, 12:00 noon and 5:30 PM, weekdays 7:00 and 9:00 AM. These agree with the diocese's Mass-times page.

## Worship sites

One: the church at 500 South Oyster Bay Road (`our-lady-of-mercy-hicksville-church`). The diocesan locator (directory:21), GCatholic (16861) and the Mass-times page list only this building, and the bulletin names no other place. The bulletin mentions an "Upper Church" for confession: the same building.

## Website and bulletin provider

Self-hosted: the Bulletin page `https://www.ourladyofmercy.org/Bulletin.php` links `BulletinArchive/Current.pdf` (this week's issue, overwritten weekly) and `Previous.pdf`. `probe url`, `probe get` and `probe pdf` all fail on this host with "certificate verify failed: unable to get local issuer certificate" (the server sends an incomplete chain; plain http redirects to https). Chrome loads it, so the site was read with visit.py and the PDF downloaded with the Run's `tools/browser_get.py`. Page 1's text layer is a scrambled font (shifted glyph codes), so page 1 has to be read as an image; pages 2-8 have normal text. `fetch` can't download it (see *Not yet confirmed*), so the row is `unsupported` with `fetch_gap` `tls-incomplete-chain`.

## Not yet confirmed

Nothing about the parish or its church. The row is `unsupported` only because `fetch` can't download from this host: `fetch:check` on 2026-11-12 resolved `page-pdfs` to `BulletinArchive/Current.pdf` and failed with "certificate verify failed: unable to get local issuer certificate". When a collector completes the chain (or the parish fixes its certificate), set `bulletin_provider: other`, rerun `fetch:check`, record its recipe and clear `fetch_gap`.
