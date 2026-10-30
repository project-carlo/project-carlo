---
name: St. Barnabas Parish
website: https://stbarnabasbayville.com/
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/6048
publication: ['url:https://www.church-bulletin.org/saint-barnabas-parish-community-bayville-nj-08721']
group: Cohort 25 (Bayville, Forked River)
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-barnabas-parish-community-bayville-nj-08721/2026-11-01.pdf
  seen: 2026-10-30
  quote: ST. BARNABAS COMMUNITY A Roman Catholic Parish 33 WOODLAND ROAD * PO BOX I * BAYVILLE, NEW JERSEY
    08721-0320
  note: 'Masthead (page 1) and page 2 of the 1 November 2026 issue (12 pages, scanned images with no text
    layer; read from renders). Page 2: ''Fr. Carlos Florez, Servant/Pastor'', ''PARISH OFFICE --- 732-269-2208'',
    MASS SCHEDULE ''DAILY: Monday - Friday 8:00 am; SATURDAY 4:00 pm; SUNDAY 8:00, 10:00 & 12 Noon (Spanish)''.
    Names this parish alone.'
- url: https://www.church-bulletin.org/saint-barnabas-parish-community-bayville-nj-08721
  seen: 2026-10-30
  quote: Saint Barnabas Parish Community Bulletin
  note: John Patrick Publishing listing 6048 on church-bulletin.org (tools/jppc-trenton.tsv had it with
    no edition; now carries issues 2026-09-06 to 2026-11-01), PDFs at /bulletin/saint-barnabas-parish-community-bayville-nj-08721/<yyyy-mm-dd>.pdf.
- url: https://stbarnabasbayville.com/news/bulletin
  seen: 2026-10-30
  note: Parish Solutio site (finder website stbarnabasbayville.com; plain fetch answers 403, the browser
    loads it). Its Bulletin page lists numbered issues to '1250-november-1-2026' (/file), the same Sunday
    as the listing; the /file PDFs are the 403 ones.
- url: https://dioceseoftrenton.org/parishfinder
  seen: 2026-10-30
  note: Finder pin directory:14640 'St. Barnabas Parish', 33 Woodland Rd, Bayville 08721-1919, (732) 269-2208,
    website stbarnabasbayville.com; one pin for the parish. GCatholic's website for it (sbrcc.com) is
    the old one.
research:
- method: fetch:check on the row (page-pdfs church-bulletin.org/6048), 1 November 2026 issue
  url: https://www.church-bulletin.org/bulletin/saint-barnabas-parish-community-bayville-nj-08721/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: 'None while the row picks the current issue: it resolves to the 1 November file (future
    freshness, posted before its date); identity is unverified only because the 12 pages are scanned images
    with no text. Read the masthead from a render if the pick changes.'
  retry_when: A text-layer issue appears, or the pick stops being the newest dated listing PDF
- method: pnpm diocese probe url / recheck on the parish's own Solutio site
  url: https://stbarnabasbayville.com/news/bulletin
  checked: '2026-10-30'
  outcome: access-blocked
  next_action: 'Read the site with parish-site-access visit.py (done 2026-10-30: the Bulletin page lists
    issues to 1 Nov 2026, the same Sunday as the listing); its /file PDFs answer 403 to plain fetch, so
    the row reads the John Patrick listing'
  retry_when: Plain fetch of the parish site stops answering 403, or the listing stops carrying the newest
    issue
bulletin_status: available
---

## Publisher

St. Barnabas Parish (Bayville) publishes its own weekly bulletin through John Patrick Publishing (listing 6048 on church-bulletin.org). The 1 November 2026 issue (every recent issue is image-only) has a masthead, read from a render of page 1, reading "St. Barnabas Community, A Roman Catholic Parish, 33 Woodland Road, Bayville", and page 2 gives Fr. Carlos Florez as pastor and one Mass schedule. It names no other parish. Cohort 25's other parish, St. Pius X (Forked River), prints its own bulletin under its own masthead and pastor (see its row), so the cohort is two rows by the *Rules settled*.

## Worship sites

One church, St. Barnabas, 33 Woodland Road (`st-barnabas-bayville`). The Spanish Mass is the 12 noon Sunday Mass in the same schedule.

## Website and bulletin provider

stbarnabasbayville.com is a Solutio CMS site (Bulletin page `/news/bulletin`), 403 to plain fetch and loaded with visit.py. Its issues' `/file` PDFs are blocked like the other Solutio sites, so the row reads the John Patrick listing, which carries the same Sunday. The listing had no edition when the survey scanned ids (Run tools, 2026-10-30 ids 6000-6110); the current one is there now.

## Not yet confirmed

Nothing outstanding.
