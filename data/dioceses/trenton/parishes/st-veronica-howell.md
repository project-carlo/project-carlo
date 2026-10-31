---
name: St. Veronica
website: https://stveronica.com/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-veronica-church-howell-nj-07731
publication: ['url:https://www.church-bulletin.org/saint-veronica-church-howell-nj-07731#jppc-532']
group: Cohort 11 (Howell, Farmingdale)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-veronica-church-howell-nj-07731/2026-11-01.pdf
  seen: 2026-10-30
  note: 'The 1 November 2026 issue (12 pages, scanned images with no text layer, rendered and read by
    eye). The masthead on page 1 names ''ST. VERONICA CHURCH, November 1, 2026, All Saints Day, 4219 Route
    9 North, Howell, New Jersey 07731, 732-363-4200, www.stveronica.com'' and bulletin for St. Veronica
    alone. Page 2 lists the Mass times and clergy: ''Daily Masses: Mon - Fri: 7:30 AM'', ''Saturday Vigil:
    4:00 PM'', ''Sunday: 7:30 AM, 10:00 AM, 12:00 PM, 5:00 PM'', Pastor Rev. Peter James Alindogan. Image-only,
    so recheck can''t find a quote.'
- url: https://stveronica.com/past-bulletins/
  seen: 2026-10-30
  note: 'The parish''s Past Bulletins page (WordPress) links only ''https://church-bulletin.org/?id=532'',
    the John Patrick listing, and jppc.net: the parish site hosts no PDFs of its own, so the printer''s
    listing is the channel.'
- url: https://www.church-bulletin.org/saint-veronica-church-howell-nj-07731
  seen: 2026-10-30
  note: 'John Patrick listing 532 ''Saint Veronica Church'', Howell NJ 07731: dated PDFs /bulletin/saint-veronica-church-howell-nj-07731/2026-11-01.pdf,
    2026-10-25, 2026-10-18.'
promoted: 2026-10-30
publication_reviews:
- parish: st-william-the-abbot-howell
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-veronica-church-howell-nj-07731/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Veronica Church, 4219 Route 9 North, with its own Mass
      times and Pastor Rev. Peter James Alindogan; St. William the Abbot's issue of the same date is a
      different document with Rev. Thomas Maher as pastor.
- parish: st-catherine-of-siena-farmingdale
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-veronica-church-howell-nj-07731/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names St. Veronica Church, 4219 Route 9 North with its own Mass
      times and pastor; the Farmingdale parish's bulletin is a separate document published by St. Catherine
      of Siena on its own site.
---

## Publisher

St. Veronica publishes its own weekly bulletin, printed by John Patrick Publishing (listing 532, `church-bulletin.org/saint-veronica-church-howell-nj-07731`). The 1 November 2026 issue (the latest, page 1 masthead): "ST. VERONICA CHURCH, November 1, 2026, All Saints Day, 4219 Route 9 North, Howell, New Jersey 07731 . 732-363-4200 . www.stveronica.com". It is 12 pages of scanned images, so I rendered pages 1-2 and read them by eye. Page 2 gives the Mass times (below) and the pastor, Rev. Peter James Alindogan, with Rev. John Chang as parochial vicar. It names St. Veronica alone.

The diocese puts St. Veronica in Cohort 11 with St. William the Abbot (Howell) and St. Catherine of Siena (Farmingdale). The cohort is a collaboration group, not a shared bulletin: St. William's 1 November issue has its own masthead, Mass schedule and pastor (Rev. Thomas Maher), and St. Catherine's has Rev. Angelito I. Anarcon. Three pastors, three bulletins, so three rows.

## Worship sites

One church, 4215 US Highway 9 (see `st-veronica-howell`). Page 2 lists Mass only at St. Veronica; no chapel or other site. GCatholic and the finder list only this church for the parish.

## Website and bulletin provider

The parish site, stveronica.com, is WordPress; its Past Bulletins page links only the John Patrick listing (`church-bulletin.org/?id=532`), so the printer's listing is the only channel. `bulletin_provider: other` with `provider_id: page-pdfs https://www.church-bulletin.org/saint-veronica-church-howell-nj-07731` (the recipe from Trenton's playbook). `pnpm fetch:check --diocese trenton --parish st-veronica-howell` (2026-10-30) resolved `.../2026-11-01.pdf` (8.9 MB): transport ok; document type a PDF whose first page has no extractable text (image-only); issue date 2026-11-01 inferred from the URL (a two-day-ahead issue for the coming Sunday, reported as 'future' against a 14-day window); publication identity unverified because the checker has no expected identity, but I read the masthead above. `publication` is `url:<listing>#jppc-532`.

## Not yet confirmed

The issue is image-only, so the pipeline needs to read it as an image. Nothing else.
