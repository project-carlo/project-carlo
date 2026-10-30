---
name: The Church of St. William the Abbot
website: https://www.stwilliamtheabbot.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/the-church-of-saint-william-the-abbot-howell-nj-07731
publication: ['url:https://www.church-bulletin.org/the-church-of-saint-william-the-abbot-howell-nj-07731#jppc-566']
group: Cohort 11 (Howell, Farmingdale)
evidence:
- url: https://www.church-bulletin.org/bulletin/the-church-of-saint-william-the-abbot-howell-nj-07731/2026-11-01.pdf
  seen: 2026-10-30
  note: 'The 1 November 2026 issue (8 pages, scanned images with no text layer, rendered and read by eye).
    Page 1 masthead names ''The Church of ST. WILLIAM THE ABBOT, A Roman Catholic Church, 2740 Lakewood
    Allenwood Road, Howell, NJ'' with Mass Schedule ''Saturday: 4:00PM (Vigil) Sunday: 8:00, 10:15 & 11:45AM'',
    weekdays ''Monday & Tuesday: 9:00AM'', ''Wednesday: 9:00AM & 7:00PM'', ''Thursday, Friday & Saturday:
    9:00AM'', and ''Rev. Thomas Maher, Pastor''. The page ends ''#566'', the John Patrick listing id.
    Image-only, so recheck can''t find a quote.'
- url: https://www.stwilliamtheabbot.com/weekly-bulletin
  seen: 2026-10-30
  note: 'The parish''s Weekly Bulletin page, read in the browser: it shows no bulletin links or PDFs for
    the pipeline, so the printer''s listing is the channel.'
- url: https://www.church-bulletin.org/the-church-of-saint-william-the-abbot-howell-nj-07731
  seen: 2026-10-30
  note: 'John Patrick listing 566 ''The Church of Saint William the Abbot'', Howell NJ 07731: PDFs dated
    2026-11-01, 2026-10-25, 2026-10-18.'
promoted: 2026-10-30
publication_reviews:
- parish: st-veronica-howell
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-church-of-saint-william-the-abbot-howell-nj-07731/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names The Church of St. William the Abbot, 2740 Lakewood Allenwood
      Road, with its own Mass schedule and Rev. Thomas Maher as pastor; St. Veronica's issue of the same
      date is a different document naming Rev. Peter James Alindogan.
- parish: st-catherine-of-siena-farmingdale
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/the-church-of-saint-william-the-abbot-howell-nj-07731/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names The Church of St. William the Abbot, 2740 Lakewood Allenwood
      Road with its own Mass times and pastor; the Farmingdale parish's bulletin is a separate document
      published by St. Catherine of Siena on its own site.
---

## Publisher

St. William the Abbot publishes its own weekly bulletin, printed by John Patrick Publishing (listing 566, `church-bulletin.org/the-church-of-saint-william-the-abbot-howell-nj-07731`). The 1 November 2026 issue (the latest) is 8 scanned-image pages, rendered and read by eye. Page 1 masthead: "The Church of ST. WILLIAM THE ABBOT, A Roman Catholic Church, 2740 Lakewood Allenwood Road, Howell, NJ", Mass Schedule, and "Rev. Thomas Maher, Pastor" with two weekend assistants and three deacons. It names St. William alone.

Cohort 11 (St. Veronica, St. William, St. Catherine of Siena) is a collaboration group, not a shared bulletin: St. Veronica's 1 November issue has a different masthead, pastor (Rev. Peter James Alindogan) and Mass times, as does St. Catherine of Siena (Rev. Angelito I. Anarcon).

## Worship sites

One church, 2740 Lakewood Allenwood Road (see `st-william-the-abbot-howell`). The Mass Schedule lists no other site; GCatholic and the finder list this church alone for the parish.

## Website and bulletin provider

stwilliamtheabbot.com has a Weekly Bulletin page with no links that the pipeline can follow, so the printer's listing is the channel: `bulletin_provider: other`, `provider_id: page-pdfs https://www.church-bulletin.org/the-church-of-saint-william-the-abbot-howell-nj-07731`. `pnpm fetch:check --diocese trenton --parish st-william-the-abbot-howell` (2026-10-30) resolved `.../2026-11-01.pdf` (6.0 MB): transport ok; a PDF with no extractable text on page 1 (image-only); issue date 2026-11-01 inferred from the URL (two days ahead, reported 'future' against a 14-day window); publication identity unverified by the checker, but the masthead above names the parish. `publication` is `url:<listing>#jppc-566`.

## Not yet confirmed

The issue is image-only, so the pipeline needs to read it as an image. The parish's own Weekly Bulletin page was not examined beyond its links (it may embed a viewer); the printer's listing already carries the current issue.
