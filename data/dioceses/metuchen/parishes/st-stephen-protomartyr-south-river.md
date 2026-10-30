---
name: St. Stephen Protomartyr
website: https://ststephennj.com/?page_id=17
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://ststephennj.com/?page_id=17#st-stephen-protomartyr-south-river']
group: ''
evidence:
- url: https://ststephennj.com/?page_id=17
  seen: 2026-10-30
  quote: Saint Stephen Protomartyr Catholic Church
  note: Heading of the parish's "Parish Bulletin / Boletin Parroquial" page, which gives the week's services
    for 26 October to 1 November 2026 in English and Spanish, with parish ads. It names St. Stephen alone.
- url: https://ststephennj.com/?page_id=17
  seen: 2026-10-30
  quote: 10:00 a.m. – Sts. Simon & Jude intercessory protection over us and our parish Mass in English
  note: Weekday Mass entry for Wednesday 28 October 2026 on the bulletin page.
revisit: Check whether the parish posts a PDF, or whether the pipeline reads weekly HTML bulletin pages
revisit_after: 2027-01-15
research:
- method: visit.py --links on the homepage and on ?page_id=17; probe get of the page text; pdf search
    of linked files
  url: https://ststephennj.com/?page_id=17
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: Ask whether an HTML bulletin page is acceptable to the pipeline or write a collector for
    it; fetch:check on ?page_id=17 failed with "No PDF links found on bulletin page" (2026-10-30)
  retry_when: The parish posts a PDF, or the pipeline reads weekly HTML bulletin pages
bulletin_status: unsupported-format
publication_reviews:
- parish: corpus-christi-south-river
  decision: separate
  evidence:
  - url: https://ststephennj.com/?page_id=17
    seen: 2026-10-30
    quote: Saint Stephen Protomartyr Catholic Church
    note: Bulletin page for St. Stephen Protomartyr, published by that parish on ststephennj.com, with
      its own services for 26 October to 1 November 2026.
  - url: https://corpuschristisouthriver.org/bulletins/file/2026-10-25-en.pdf
    seen: 2026-10-30
    quote: Please remember Corpus Christi Parish
    note: Bulletin for Corpus Christi, published by Corpus Christi on corpuschristisouthriver.org (25
      October 2026, 3 pages); it carries its own Mass intentions and notices.
- parish: st-mary-of-ostrabrama-south-river
  decision: separate
  evidence:
  - url: https://ststephennj.com/?page_id=17
    seen: 2026-10-30
    quote: Saint Stephen Protomartyr Catholic Church
    note: Bulletin page for St. Stephen Protomartyr, published by that parish on ststephennj.com, with
      its own services for 26 October to 1 November 2026.
  - url: https://files.ecatholic.com/11802/bulletins/20261025.pdf
    seen: 2026-10-30
    quote: Saint Mary of Ostrabrama Parish, a Roman Catholic
    note: Bulletin for St. Mary of Ostrabrama, published by that parish through eCatholic 11802 (25 October
      2026, 6 pages), with its own Mass schedule.
---

## Publisher

St. Stephen Protomartyr publishes its bulletin as a web page on its own site, ststephennj.com, not as a PDF: `?page_id=17`, "Parish Bulletin / Boletin Parroquial" (read 2026-10-30). The page gives "SERVICES THIS WEEK" (Masses, CCD classes, meetings, with the intention for each Mass, in English and Spanish), notices and a list of advertisers. The page says the bulletin "appears every week in two languages ( i n English and in Spanish )" in a paper version and online. The homepage and the page link no PDF. The Spanish page `?page_id=11` repeats the Spanish services.

It names St. Stephen alone (the pastor is Rev. John J. Szczepanik, as in the finder) and mentions St. Mary's, South Amboy only as the start of a pilgrimage. It is not shared with Corpus Christi or St. Mary of Ostrabrama.

## Worship sites

The church at 20 William St (directory:24548, gcatholic:18688). The Our Lady of Mariapocs Shrine (`?page_id=31`) is a chapel built in 2009, open 24 hours through a passage from William St, with no Mass listed; it is part of the church site.

## Website and bulletin provider

Self-hosted WordPress. `fetch:check` 2026-10-30 on `?page_id=17` failed with "NoBulletin: No PDF links found on bulletin page", so the row is `no_bulletin` for now (Settled policy 4); the bulletin is a readable HTML page.

## Not yet confirmed

Whether the pipeline can read the HTML page; see `research` and `revisit`. No regular Sunday Mass list was found apart from the week's entries (Sunday 1 November: 8:30 a.m. English; 10:00 a.m., 11:30 a.m. and 4:00 p.m. Spanish).
