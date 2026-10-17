---
name: Ascension Parish and St. Katharine Drexel Parish
website: https://apskdp.org/community/weekly-bulletin/
bulletin_provider: other
provider_id: ''
publication: ['url:https://apskdp.org/community/weekly-bulletin/']
group: Ascension Parish; Saint Katharine Drexel Parish
evidence:
- url: https://apskdp.org/wp-content/uploads/Bulletin-10.11.26.pdf
  seen: 2026-10-16
  quote: 133E (BC) - Ascension/Saint Katharine Drexel, Forest City
  note: 'Page 6 (the only page with a text layer), the publisher''s footer. Page 1 of the 11 October
    2026 issue is an image (read by rendering it, parish-site-access render.py), so it cannot be quoted
    for recheck. Its masthead reads "ASCENSION PARISH and ST. KATHARINE DREXEL PARISH, 612 Hudson Street,
    Forest City, PA 18421", and its Mass Schedule box on the same page: "Saturday Vigil Mass 4:00 PM St. Joseph; Sunday Masses 8:00
    AM St. Juliana, 9:30 AM St. Joseph, 11:00 AM St. James; Daily Mass Monday, Wednesday (Friday - Communion
    service only) 8:30 AM St. Joseph; Tuesday, Thursday 9:00 AM St. James".'
- url: https://apskdp.org/community/weekly-bulletin/
  seen: 2026-10-16
  quote: Download this week’s bulletin! October 11, 2026 October 4, 2026 September 27, 2026
  note: The parish site's bulletin page, linking one PDF per Sunday at wp-content/uploads/Bulletin-<M>.<D>.<YY>.pdf
    (latest 11 October 2026).
- url: https://apskdp.org/
  seen: 2026-10-16
  quote: 'Saturday Vigil: 4:00 p.m. St. Joseph, Forest City'
  note: 'Homepage weekend schedule, same as the bulletin: Sunday 8:00 a.m. St. Juliana, Rock Lake; 9:30
    a.m. St. Joseph, Forest City; 11:00 a.m. St. James, Pleasant Mount.'
---

## Publisher

The two canonical parishes of Forest City (Ascension Parish, whose church is St. Joseph,
Forest City) and Pleasant Mount (Saint Katharine Drexel Parish: St. James, Pleasant Mount
and St. Juliana, Rock Lake) share one pastor (Rev. Arun Lakra), one office at 612 Hudson
Street, one website (apskdp.org, which the diocese's finder gives for both) and one weekly
bulletin. The 11 October 2026 issue's masthead reads "Ascension Parish and St. Katharine
Drexel Parish" and its Mass Schedule covers all three churches. The bulletin is printed by
Bon Venture Services (page 6 footer "133E (BC) - Ascension/Saint Katharine Drexel, Forest
City"). One bulletin, so one row for both canonical parishes.

## Worship sites

Three, each in the bulletin's Mass Schedule (11 October 2026) and on the homepage:

- St. Joseph, Forest City (`st-joseph-forest-city`): Saturday 4:00 pm, Sunday 9:30
  am, Monday and Wednesday 8:30 am.
- St. James, Pleasant Mount (`st-james-pleasant-mount`): Sunday 11:00 am,
  Tuesday and Thursday 9:00 am.
- St. Juliana, Rock Lake (`saint-juliana-pleasant-mount`): Sunday 8:00 am.

The diocese's finder lists exactly these three sites for the two parishes. GCatholic's St.
John the Baptist at 306 Susquehanna St., Forest City is a Ruthenian (Byzantine) church
outside the Latin diocese, excluded as `other-jurisdiction`
(`excluded/st-john-the-baptist-forest-city.md`).

## Website and bulletin provider

apskdp.org/community/weekly-bulletin/ is the parish's own WordPress page, linking a PDF per
Sunday at `wp-content/uploads/Bulletin-<M>.<D>.<YY>.pdf`; `probe url` on www.apskdp.org found
it (redirects to apskdp.org). No ParishesOnline, eCatholic or Discover Mass id: Discover Mass
has church pages for St. James and St. Juliana but lists no issues. Hence `other`, with the
bulletin page as the publication.

**The bulletin's pages 1 to 5 are images with no text layer** (probe pdf: readable page 6
only, the advertisers' page), so the pipeline has to read it as images. No `fetch:check`
recipe pinned yet: run it after promotion; `page-pdfs` on the bulletin page should be the
collector.

## Not yet confirmed

Nothing for structure. The quote from the masthead can only be re-checked by rendering
the page.
