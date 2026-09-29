---
name: Holy Family Parish
website: https://holyfamilylittlefalls.org
bulletin_provider: other
provider_id: ''
publication: ['ecatholic:28690', 'url:https://holyfamilylittlefalls.org/2026-bulletins']
group: ''
evidence:
- url: https://files.ecatholic.com/28690/documents/2026/9/HF%20-%20SJ%20Bulletin%20September%2027%202026%20copy.pdf
  seen: 2026-09-28
  quote: ST. JOSEPH CHURCH MASS TIMES Sunday 8 a.m.
  note: 'Page 1 of the 27 September 2026 issue: ''HOLY FAMILY PARISH MASS TIMES Saturday 4 p.m. Sunday
    10 a.m. Sunday 12 p.m. …'' then St. Joseph Church''s; ''Holy Family Parish | St. Joseph Church Pastor:
    Fr. Brian Slezak''.'
- url: https://files.ecatholic.com/28690/documents/2026/9/HF%20-%20SJ%20Bulletin%20September%2027%202026%20copy.pdf
  seen: 2026-09-28
  quote: Holy Family Parish 763 E. Main Street Little Falls, NY 13365
  note: Page 2 heading; page 3 is headed 'St. Joseph Church 31 N. Helmer Avenue Dolgeville, NY 13329'.
- url: https://holyfamilylittlefalls.org/2026-bulletins
  seen: 2026-09-28
  quote: HOLY FAMILY/ST. JOSEPH - September 27
  note: 'The parish''s eCatholic site (behind Cloudflare; read with visit.py 2026-09-28): the ''2026 Bulletins''
    page links each week''s PDF under files.ecatholic.com/28690/documents/<yyyy>/<m>/HF - SJ Bulletin
    <Month> <D> <yyyy>.pdf.'
- url: http://parishes.rcda.org/stjosephsdolgeville/
  seen: 2026-09-28
  note: St. Joseph Dolgeville's address in the diocese's directory; on 2026-09-28 it redirected (visit.py)
    to holyfamilylittlefalls.org.
promoted: 2026-09-28
---

## Publisher

Holy Family Parish, Little Falls and St. Joseph Church, Dolgeville (one pastor, Fr. Brian
Slezak; one office at 763 E. Main St.) publish one weekly bulletin, titled "HOLY FAMILY/ST.
JOSEPH" on the parish site. The 27 September 2026 issue's page 1 gives both churches' Mass
times; page 2 is Holy Family's and page 3 St. Joseph's, with a combined intentions list
marking each Mass "HOLY FAMILY" or "ST. JOSEPH". St. Joseph's own old address
(parishes.rcda.org/stjosephsdolgeville) now redirects to the Holy Family site, so there is no
second channel.

## Worship sites

- `holy-family-little-falls`: Saturday 4 pm, Sunday 10 am and 12 pm (the noon Mass is the
  Traditional Latin Mass; "NO MASS" on 27 September), weekdays.
- `st-joseph-dolgeville`: Sunday 8 am.

The Institutional Records index gives Holy Family the records of Sacred Heart, St. Joseph
and St. Mary, Little Falls (merged into Holy Family in 1992 per GCatholic); those buildings are
in neither roster, and were not researched.

## Website and bulletin provider

holyfamilylittlefalls.org is eCatholic (site 28690) behind Cloudflare, but it does **not**
post bulletins the standard eCatholic way: `/bulletins` exists with no PDFs, and
`files.ecatholic.com/28690/bulletins/<date>.pdf` answers 403. The PDFs are uploaded as
documents (`files.ecatholic.com/28690/documents/2026/9/HF - SJ Bulletin September 27 2026
copy.pdf`) and linked from the "2026 Bulletins" page, which the homepage links as "Holy
Family & St. Joseph Bulletin". So `bulletin_provider` is `other`, with the homepage as
`website` for the resolver to follow to the year's page. The eCatholic site id is kept as a
publication. File names are not date-stamped and sometimes carry "copy" or "-1" suffixes.

## Not yet confirmed

Whether the pipeline's `other` resolver picks the newest PDF from the 2026 Bulletins page
(the newest is listed first). In January 2027 the site will presumably add a "2027
Bulletins" page.
