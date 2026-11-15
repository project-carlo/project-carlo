---
name: St. Thomas & St. Timothy Parish
website: https://stastm.org/bulletins/
bulletin_provider: unsupported
provider_id: page-pdfs http://sponsors.bonventure.net/?page=1626
publication: []
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/1626/2026-11-15.pdf
  seen: 2026-11-13
  quote: 225 King Philip Drive • West Hartford, CT 06117
  note: 'Page 1 masthead of the 15 November 2026 issue ("THRITY-THIRD SUNDAY IN ORDINARY TIME November
    15, 2026"): "ST. THOMAS & ST. TIMOTHY PARISH", Pastor Rev. Michael A. Ruminski; ST. THOMAS THE APOSTLE
    CHURCH 872 Farmington Ave.; ST. TIMOTHY CHURCH 225 King Philip Drive; Mailing Address 1116 N. Main
    Street. Mass Schedule: Saturday Vigil St. Timothy 4:30 pm; Sunday St. Timothy 8:00 am, St. Thomas
    10:30 am and 5:00 pm; weekdays at both.'
- url: https://stastm.org/bulletins/
  seen: 2026-11-13
  note: The parish site's menu item "Bulletins" and its /bulletins/ page link sponsors.bonventure.net/?page=1626,
    which lists only the current issue, pdfs/1626/2026-11-15.pdf.
bulletin_status: available
fetch_gap:
  kind: tls-certificate-unverified
  seen: 2026-11-13
  note: 'The bulletin is the current PDF on bonventure.net''s sponsors page (?page=1626, links pdfs/1626/<YYYY-MM-DD>.pdf).
    fetch:check on 2026-11-13 resolved page-pdfs on http://sponsors.bonventure.net/?page=1626 to https://sponsors.bonventure.net/pdfs/1626/2026-11-15.pdf
    (''current'') but the download failed: ''SSL: CERTIFICATE_VERIFY_FAILED ... unable to get local issuer
    certificate'' (the server does not send its intermediate certificate). Over http the page and PDF
    load (probe get, probe pdf).'
  url: http://sponsors.bonventure.net/pdfs/1626/2026-11-15.pdf
---

## Publisher

St. Thomas & St. Timothy Parish, West Hartford publishes one weekly bulletin through bonventure.net (page 1626). The 15 November 2026 issue (12 pages, text layer) has the masthead on page 1: "ST. THOMAS & ST. TIMOTHY PARISH", Pastor Rev. Michael A. Ruminski, with both churches' addresses and one Mass schedule. (The text layer also carries a hidden "September 27, 2026" heading from a template; the visible heading is 15 November.)

## Worship sites

Two, both on page 1 of the 15 November 2026 issue: St. Thomas the Apostle Church, 872 Farmington Ave. (Sunday 10:30 am and 5:00 pm; Wednesday and Thursday 12:10 pm; Saturday 7:30 am; `st-thomas-the-apostle-west-hartford`) and St. Timothy Church, 225 King Philip Drive (Saturday Vigil 4:30 pm; Sunday 8:00 am; Monday, Tuesday and Friday 7:30 am; `st-timothy-west-hartford`). These are the directory's two churches of the parish (10, 5) and GCatholic's 22226 and 22227. The two parishes shared a pastor from 1 January 2021 (We-Ha, 8 January 2021) and now publish as one parish.

## Website and bulletin provider

`unsupported`, with a `fetch_gap` of kind `tls-certificate-unverified`. The recipe `page-pdfs http://sponsors.bonventure.net/?page=1626` resolves this week's issue (`fetch:check` 2026-11-13: "page-pdfs on http://sponsors.bonventure.net/?page=1626: current", `pdfs/1626/2026-11-15.pdf`), but the link resolves to https and the download fails certificate verification ("unable to get local issuer certificate"). Over http the PDF loads. Once the fetcher can download it (an http fallback or the host fixing its chain), set the provider to `other` and clear the gap.

## Not yet confirmed

Nothing open about the parish's structure.
