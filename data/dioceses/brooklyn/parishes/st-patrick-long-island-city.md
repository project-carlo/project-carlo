---
name: St. Patrick (Long Island City)
website: https://stpatlic.org/
bulletin_provider: other
provider_id: page-pdfs https://stpatlic.org/important-information/bulletin/
publication: []
group: Deanery Q1 (Queens West)
evidence:
- url: http://stpatlic.org/wp-content/uploads/sites/58/2026/10/nov1_2026_stpatlic_compressed.pdf
  seen: 2026-11-06
  quote: Saint Patrick Roman Catholic Church
  note: '1 November 2026 issue, 8 pages, self-published (no LPi or Church Bulletin Inc. footer); downloaded
    with tools/fetch-pdf.py (the multisite drops probe pdf). Page 1 masthead: Saint Patrick Roman Catholic
    Church, 39-38 29th St, Long Island City, NY 11101, 718-729-6060, stpatlic@yahoo.com; Rev. Felix Sanchez,
    Pastor. The schedule box for St. Patrick Church gives Saturday Vigil 5:00 pm (Eng), Sunday 9:00 am
    (Eng), 10:30am (Spa), 12:00pm (Eng), Monday-Friday 9:00 am, Tuesday 7:45pm (Spa), First Sunday 1:30
    PM (Tagalog); a second box gives St. Rita''s weekend and weekday times.'
- url: http://stpatlic.org/wp-content/uploads/sites/58/2026/10/nov1_2026_stpatlic_compressed.pdf
  seen: 2026-11-06
  quote: 9:00AM +Mary A. Holic, requested by Stephen Holic
  note: Page 2 carries St. Patrick's own Mass intentions (5:00 PM, 9:00 AM ENG, 10:30AM SPA, 12:00 PM
    ENG) and collection; page 3 'Parish Groups at St. Patrick' (a First Saturday 7:30 a.m. Hail Marys
    group 'at Chapel', a prayer group, not a Mass).
- url: https://stpatlic.org/important-information/bulletin/
  seen: 2026-11-06
  note: 'Bulletin page (parish-site-access visit.py), newest first: nov1_2026_stpatlic_compressed.pdf,
    oct25_2026, oct18_2026, oct11_2026, oct4_2026, sept27_2026 ... weekly, under /wp-content/uploads/sites/58/.'
- url: https://stpatlic.org/
  seen: 2026-11-06
  quote: St. Patrick Church / Iglesia San Patricio
  note: 'Homepage (visit.py; probe url gets RemoteDisconnected): schedules for St. Patrick and St. Rita,
    matching the bulletin.'
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://stpatlic.org/important-information/bulletin/
  url: https://stpatlic.org/important-information/bulletin/
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check after 8 November and confirm it picks that issue
  retry_when: The 8 November 2026 issue is posted
  revisit_after: 2026-11-09
bulletin_status: available
publication_reviews:
- parish: st-rita-long-island-city
  decision: separate
  evidence:
  - url: http://stpatlic.org/wp-content/uploads/sites/58/2026/10/nov1_2026_stpatlic_compressed.pdf
    seen: 2026-11-06
    note: The 1 November 2026 masthead names Saint Patrick Roman Catholic Church, 39-38 29th St, alone,
      with St. Patrick's own Mass intentions and collection; St. Rita appears only in a second Mass-schedule
      box.
  - url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMTEvMDIvM3RnYjdxMDduZV8xMS4wMS4yNl9CdWxsZXRpbi5wZGYiXV0/11.01.26%20Bulletin.pdf
    seen: 2026-11-06
    note: The 1 November 2026 masthead names Saint Rita Roman Catholic Church, 36-25 11th St, alone, in
      a separate 8-page issue on stritalic.org with St. Rita's own attendance (426) and collection ($4,473).
---

## Publisher

St. Patrick, Long Island City publishes its own weekly bulletin, self-made (no LPi footer, no Church Bulletin Inc. ad page) and posted as PDFs on its WordPress multisite. The 1 November 2026 issue (read 2026-11-06, 8 pages, downloaded with `tools/fetch-pdf.py`) has the masthead "Saint Patrick Roman Catholic Church, 39-38 29th St, Long Island City, NY 11101", Rev. Felix Sanchez, Pastor.

## Worship sites

One. The page 1 box "St. Patrick Church/ Iglesia San Patricio" gives Saturday Vigil 5:00 pm, Sunday 9:00 am (Eng), 10:30 am (Spa), 12:00 pm (Eng), Monday-Friday 9:00 am, Tuesday 7:45 pm (Spa), First Sunday 1:30 pm (Tagalog); page 2's intentions are at those times. Page 3's "2000 Hail Marys ... 7:30 a.m. at Chapel" is a prayer group, not a Mass, and names no separate building. The directory, the deanery list, GCatholic 16761 and Mass finder 1158 give the one church at 39-38 29th Street.

Fr. Sanchez is also pastor of St. Rita, Long Island City (priests' directory, 2026-11-05), and each parish's page 1 prints the other's schedule. The bulletins are separate: St. Rita posts its own issue the same week on stritalic.org with its own masthead and collection (row `st-rita-long-island-city`), recorded as a `separate` review.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stpatlic.org/important-information/bulletin/` (newest first). The site is on a WordPress multisite (uploads under `/wp-content/uploads/sites/58/`): `probe url` and `probe pdf` get RemoteDisconnected, while `visit.py`, `tools/fetch-pdf.py` and fetch load it. GCatholic's link (stpatricklic.blogspot.com) is an older site and was not used. No publication id: the issue is self-published.

## Not yet confirmed

Whether the two parishes move to one bulletin; if a later masthead names both churches, merge the rows. The 8 November issue was not yet posted on 2026-11-06; see research.
