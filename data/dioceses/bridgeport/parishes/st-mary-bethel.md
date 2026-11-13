---
name: St. Mary
website: https://www.stmarybethel.org/
bulletin_provider: other
provider_id: page-pdfs https://www.stmarybethel.org/bulletina2119c88 filename=*2026.pdf
publication: ['url:https://www.stmarybethel.org/bulletina2119c88']
group: ''
evidence:
- url: https://irp.cdn-website.com/3668ad53/files/uploaded/Bulletin+November+1+2026.pdf
  seen: 2026-11-12
  quote: 26 Dodgingtown Road, Bethel, CT 06801
  note: 'Page 1 of the 1 November 2026 issue (10 pages; page 6 has no text): ''Saint Mary Parish'', ''November
    1, 2026 All Saints Day'', ''Father Corey V. Piccinino, Pastor''. Page 3 (''St. Mary Catholic Church'')
    lists Masses Saturday 4:30, Sunday 7:00, 8:30, 11:00 and weekdays 9:00. Names no other church.'
- url: https://www.stmarybethel.org/bulletina2119c88
  seen: 2026-11-12
  note: Duda bulletin page (probe get) lists 91 PDFs on irp.cdn-website.com/3668ad53, named '9010 <Month>
    <D> <YYYY>.pdf' (2025 issues first, then 2026 newest first); the newest is 'Bulletin November 1 2026.pdf',
    with no 25 October or 8 November file. http://church-bulletin.org/9010 redirects to church-bulletin.org/saint-mary-parish-bethel-ct-06801,
    which lists no issues.
revisit: In January 2027 change the provider_id filter from filename=*2026.pdf to the new year's (*2027.pdf)
  and rerun fetch:check
revisit_after: 2027-01-04
research:
- method: probe get on the Duda bulletin page
  url: https://www.stmarybethel.org/bulletina2119c88
  checked: '2026-11-12'
  outcome: not-found
  next_action: Rerun fetch:check; if the newest is still 1 November, look for a moved bulletin page on
    stmarybethel.org or a church-bulletin.org issue
  retry_when: After 2026-11-22
  revisit_after: 2026-11-23
bulletin_status: available
---

## Publisher

St. Mary, Bethel publishes its own weekly bulletin and uploads it to its Duda site. The 1 November 2026 issue (`https://irp.cdn-website.com/3668ad53/files/uploaded/Bulletin+November+1+2026.pdf`, read 2026-11-12) has on page 1 "Saint Mary Parish, November 1, 2026, All Saints Day, 26 Dodgingtown Road, Bethel, CT 06801" with Father Corey V. Piccinino as pastor, and page 3 ("St. Mary Catholic Church") lists the week's Masses. It names no other church. The `9010` prefix of earlier file names matches the JPPC short link `church-bulletin.org/9010`, which leads to an empty St. Mary page there: probably John Patrick Publishing's account number, not checked further.

## Worship sites

- `st-mary-bethel`: page 3 lists Saturday 4:30pm, Sunday 7:00, 8:30 and 11:00am, and weekdays and Saturday 9:00am. A 2 November Mass "at the Cemetery" is a one-off and not recorded as a worship site. The diocese's directory (directory:1314) and GCatholic (22021) list this one church.

## Website and bulletin provider

`stmarybethel.org` is a Duda site; its bulletin page (`/bulletina2119c88`) links the parish's PDFs on `irp.cdn-website.com/3668ad53/files/uploaded/`. On 2026-11-12 it listed 2025 issues first, then 2026 newest first; the newest was `Bulletin+November+1+2026.pdf` (no 25 October or 8 November issue posted). Provider `other`, pinned `page-pdfs` on that page.

`fetch:check` on 2026-11-12 with the bare page recipe picked `9010+November+16+2025.pdf` (stale, 361 days), because the page lists the 2025 issues first. With the filter `filename=*2026.pdf` (recipe `page-pdfs https://www.stmarybethel.org/bulletina2119c88 filename=*2026.pdf`) it picked `https://irp.cdn-website.com/3668ad53/files/uploaded/Bulletin+November+1+2026.pdf`, the 1 November 2026 issue read above (`first-listed, dated 2026-11-01`, freshness `fresh`; identity unverified as reported, masthead checked by hand). The filter names the year, so it must be changed in January 2027 (see `revisit`).

## Not yet confirmed

The newest posted issue was 11 days old on 2026-11-12 and the parish skips weeks; see research for the retry.
