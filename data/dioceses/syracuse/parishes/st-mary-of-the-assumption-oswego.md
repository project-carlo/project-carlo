---
name: St. Mary of the Assumption Parish & Shrine
website: https://stmarysoswego.com/
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:26344']
group: ''
evidence:
- url: https://files.ecatholic.com/26344/bulletins/20260920.pdf
  seen: 2026-09-26
  note: 'The 20 September 2026 issue, 4 pages. Its text is drawn as outlines (no text layer), so it was
    read rendered in Chrome. Page-1 masthead: "Saint Mary of the Assumption Parish & Shrine", "Institute
    of Christ the King Sovereign Priest", "Address: 103 West 7th Street, Oswego, NY 13126", "Website:
    www.stmarysoswego.com"; Mass Times: "Sunday: 9:00 a.m. Low Mass, 11:00 a.m. High Mass", weekdays except
    Thursday 7:30 a.m., Thursday 12:10 p.m., First Fridays an additional 6:00 p.m. No other church appears.'
- url: https://stmarysoswego.com/
  seen: 2026-09-26
  quote: 103 W. 7th St. Oswego NY 13126
  note: The parish's eCatholic site, which answers plain fetches with 403; read in a browser (parish-site-access
    visit.py). Embeds eCatholic site id 26344, with a Bulletins page at /bulletins.
- url: https://discovermass.com/church/st-mary-of-the-assumption-oswego-ny/
  seen: 2026-09-26
  quote: St. Mary became a Personal Parish in May 2020, dedicated to the Extraordinary form of the Mass.
    In 2021, it was elevated to a Diocesan Shrine. In 2025 care of St Mary's was entrusted to the ICKSP.
  note: Discover Mass (MassTimes.org) listing, 103 W 7th St. It lists no bulletins.
- url: https://institute-christ-king.org/news/1854-opening-mass-for-new-apostolate-in-oswego-ny-st-mary-of-the-assumption-shrine
  seen: 2026-09-26
  quote: opened its newest apostolate, St. Mary of the Assumption Shrine in Oswego, New York
  note: The Institute's announcement of its first Solemn High Mass there on Sunday, 15 June (2025, per
    Discover Mass).
promoted: 2026-09-26
---

## Publisher

St. Mary of the Assumption is a personal parish for the Latin Mass (since May 2020) and a diocesan
shrine (since 2021), in the care of the Institute of Christ the King Sovereign Priest since June 2025.
It publishes its own weekly bulletin through eCatholic (site 26344). I read the 20 September 2026 issue
(the 27 September one was not up yet, 403): the masthead is St. Mary's alone, with its own address and
Mass schedule. It was part of the 2019 Oswego merger plan, but the diocese withdrew it (the 2020 merger
decree names only St. Joseph, St. Paul, St. Peter and St. Stephen), and it has nothing to do with
Christ the Good Shepherd's bulletin.

## Worship sites

One: `churches/st-mary-of-the-assumption-oswego.md`.

## Website and bulletin provider

stmarysoswego.com is the parish's eCatholic-hosted site (the directory's website for it; GCatholic's
stmarysoswego.org is an older domain). It embeds eCatholic site id 26344; issues are at
files.ecatholic.com/26344/bulletins/YYYYMMDD.pdf. The PDFs have no text layer (outlined fonts), so
`probe pdf` and `issues.py` read nothing; the pipeline's extraction sends the PDF itself to the model,
which reads the rendered page, so this should not stop extraction, but it is worth watching on the
first run.

## Not yet confirmed

That the pipeline extracts this bulletin despite the missing text layer (first weekly run).
