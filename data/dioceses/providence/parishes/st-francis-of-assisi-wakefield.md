---
name: St. Francis of Assisi
website: http://sponsors.bonventure.net/?page=3118
bulletin_provider: unsupported
provider_id: page-pdfs http://sponsors.bonventure.net/?page=3118
publication: ['url:http://sponsors.bonventure.net/?page=3118']
group: ''
evidence:
- url: http://sponsors.bonventure.net/pdfs/3118/2026-11-15.pdf
  seen: 2026-11-15
  quote: Sunday ---------------------------------------- 8:00 am* and 10:00 am
  note: 15 November 2026 issue, 8 pages. Page 1 masthead 'SAINT FRANCIS OF ASSISI WAKEFIELD' and 'THE
    PARISH FAMILY OF ... SAINT ROMUALD MATUNUCK'; Father Albert D. Ranallo, Pastor; Masses at 'Saint Francis
    Church' (Mon, Tue, Thu, Fri 7:00 am; Saturday 4:30 pm; Sunday 9:00 am and 11:00 am) and 'Saint Romuald
    Chapel' (Saturday 5:30 pm*, Sunday 8:00 am* and 10:00 am; '*Summer only (Memorial Day weekend through
    Labor Day Weekend)'). Page 1 footer '(c) 2022 Bon Venture Services, LLC'.
- url: https://stfranciswakefield.com/about/bulletin/
  seen: 2026-11-15
  quote: Click to view the bulletin
  note: The parish site's Bulletin page links the bulletin cover image to https://sponsors.bonventure.net/?page=3118,
    which lists dated issues pdfs/3118/YYYY-MM-DD.pdf newest first (2026-11-15, 2026-11-08, ...).
bulletin_status: available
fetch_gap:
  kind: tls-certificate-unverified
  seen: 2026-11-15
  note: 'The bulletin is the current PDF on bonventure.net''s sponsors page (?page=3118, links pdfs/3118/<YYYY-MM-DD>.pdf).
    fetch:check on 2026-11-15 (provider other, page-pdfs on http://sponsors.bonventure.net/?page=3118)
    picked https://sponsors.bonventure.net/pdfs/3118/2026-11-15.pdf (''fresh'') but the download failed:
    ''SSL: CERTIFICATE_VERIFY_FAILED ... unable to get local issuer certificate''. Over http the page
    and PDF load (probe get, probe pdf).'
  url: http://sponsors.bonventure.net/pdfs/3118/2026-11-15.pdf
---

## Publisher

St. Francis of Assisi, Wakefield publishes a weekly bulletin through Bon Venture Services. The 15 November 2026 issue (http://sponsors.bonventure.net/pdfs/3118/2026-11-15.pdf) has on page 1 the masthead "SAINT FRANCIS OF ASSISI WAKEFIELD" with "THE PARISH FAMILY OF ... SAINT ROMUALD MATUNUCK", Father Albert D. Ranallo, Pastor, and the Mass schedule for "Saint Francis Church" (weekdays except Wednesday 7:00 am, Saturday 4:30 pm, Sunday 9:00 am and 11:00 am) and "Saint Romuald Chapel" (Saturday 5:30 pm and Sunday 8:00 am in summer only, Sunday 10:00 am).

## Worship sites

Two: St. Francis of Assisi Church, 128 High St., Wakefield, and St. Romuald Chapel, 61 Atlantic Ave., Matunuck. Page 2 of the 15 November 2026 issue lists 10:00am intentions under a separate heading for Sunday 15 and 22 November, which is the chapel's year-round Sunday Mass. The finder (12220) gives the same chapel and times in its entry for this parish; GCatholic lists only the church (22437) and neither roster has a separate entry for the chapel.

## Website and bulletin provider

The parish site's Bulletin page (https://stfranciswakefield.com/about/bulletin/) links its cover image to the Bon Venture sponsors page http://sponsors.bonventure.net/?page=3118, which lists every issue as pdfs/3118/YYYY-MM-DD.pdf, newest first. `fetch:check` on 2026-11-15 with `other` / `page-pdfs http://sponsors.bonventure.net/?page=3118` picked https://sponsors.bonventure.net/pdfs/3118/2026-11-15.pdf, the issue read above, but the download failed certificate verification (the server sends an incomplete chain; the same gap is recorded on Bon Venture parishes in Hartford). So the row is `unsupported` with fetch_gap `tls-certificate-unverified`; the `page-pdfs` recipe is kept in provider_id for when a collector handles it.

## Not yet confirmed

Nothing about the parish is open; the row waits for a collector that can download Bon Venture's https PDFs (see fetch_gap).
