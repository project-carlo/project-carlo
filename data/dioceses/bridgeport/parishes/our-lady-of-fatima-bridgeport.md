---
name: Our Lady of Fatima
website: https://olf-bridgeport.org/
bulletin_provider: other
provider_id: page-pdfs https://olf-bridgeport.org/ filename=*Year*.pdf
publication: ['ecatholic:24410']
group: ''
evidence:
- url: https://ec-prod-site-cache.s3.amazonaws.com/static1/olf45bridgeport.org/documents/2026/11/33rd32Sunday32in32Ordinary32Time32Year32A322026.pdf
  seen: 2026-11-12
  quote: Igreja Nossa Senhora de Fátima
  note: 'Page 1 of the 15 November 2026 bulletin (2 pages): ''Our Lady of Fatima Church'', 429 Huntington
    Road, Bridgeport, CT 06608; Pastor Rev. Ivanildo Celestino dos Santos; Saturday Vigil 6:00 p.m. Português;
    Sunday 8:00, 9:30 a.m. Português, 11:00 a.m. English; Monday-Thursday 6:45 p.m., Friday 8:00 a.m.
    Page 2: Mass intentions 14-22 November. No ''Good Counsel'' or ''Ortega'' (grep).'
- url: https://olf-bridgeport.org/
  seen: 2026-11-12
  note: 'eCatholic site (ecatholic:24410; probe url 403, read with visit.py). The home page links each
    week''s ''Bulletin'' and ''Insert'' as eCatholic documents, e.g. ''November 15 2026 Bulletin'' (documents/2026/11/33rd
    Sunday in Ordinary Time Year A 2026.pdf) and ''November 15 2026 Insert'' (documents/2026/11/111526b.pdf,
    a 2-page list of names); none under files.ecatholic.com/24410/bulletins/ (issues.py: 403 for 25 Oct-15
    Nov 2026).'
revisit: Check fetch:check still picks the current bulletin after the Christmas 2026 issues (filename
  filter *Year*.pdf).
revisit_after: 2027-01-05
bulletin_status: available
---

## Publisher

Our Lady of Fatima, Bridgeport (the Portuguese parish in the North End) posts a weekly two-page bulletin plus an insert as documents on its eCatholic site (`ecatholic:24410`), linked from the home page as "<date> Bulletin" and "<date> Insert". The 15 November 2026 bulletin (`https://ec-prod-site-cache.s3.amazonaws.com/static1/olf45bridgeport.org/documents/2026/11/33rd32Sunday32in32Ordinary32Time32Year32A322026.pdf`, read 2026-11-12) is headed "Our Lady of Fatima Church / Igreja Nossa Senhora de Fátima, 429 Huntington Road, Bridgeport, CT 06608", names Rev. Ivanildo Celestino dos Santos, Pastor, and gives one schedule: Saturday Vigil 6:00 p.m. (Portuguese); Sunday 8:00 and 9:30 a.m. (Portuguese) and 11:00 a.m. (English); Monday-Thursday 6:45 p.m., Friday 8:00 a.m.

## Worship sites

One church, `our-lady-of-fatima-bridgeport`. The bulletin doesn't name the Our Lady of Good Counsel chapel on Ortega Avenue (grep), which GCatholic places under St. Andrew.

## Website and bulletin provider

The parish doesn't use eCatholic's bulletin folder: `files.ecatholic.com/24410/bulletins/<date>.pdf` answered 403 for 25 October-15 November 2026 (issues.py). Its issues are eCatholic documents named after the Sunday ("33rd Sunday in Ordinary Time Year A 2026.pdf", "All Saints Year A 2026.pdf"), with a separate insert each week whose file names vary ("111526b.pdf", "10252632Insert32in32Word...").

`fetch:check` with provider `ecatholic` on 2026-11-12 failed ("No matching anchor link found ... at https://olf-bridgeport.org/bulletins"), since it looks for `files.ecatholic.com` links. So the row is `other` with the pinned recipe `page-pdfs https://olf-bridgeport.org/ filename=*Year*.pdf`: the home page lists bulletins and inserts newest first, and the filter keeps the bulletins, whose names carry the lectionary year, and drops the inserts. `fetch:check` with it on 2026-11-12 picked the 15 November 2026 bulletin (`.../documents/2026/11/33rd32Sunday32in32Ordinary32Time32Year32A322026.pdf`; issue date unknown to fetch, identity unverified as reported; masthead checked by hand above).

## Not yet confirmed

The filter depends on the parish's naming habit: a feast-day issue named without "Year" (Christmas, say) would be skipped and an older issue picked. Recheck the pick after Christmas 2026; if it misses, widen the filter or record a fetch_gap.
