---
name: Parish of the Most Holy Name of Jesus
website: https://elmiracatholic.org
bulletin_provider: other
provider_id: ''
publication:
- url:https://www.elmiracatholic.org/news-bulletins/
- po-container:06/0115
group: ''
evidence:
- url: https://container.parishesonline.com/bulletins/06/0115/20261004B.pdf
  seen: 2026-10-02
  quote: Parish of the Most Holy Name of Jesus
  note: Page 1 masthead of the 4 October 2026 issue (ParishesOnline container 06/0115, the same bulletin
    the parish posts on its own site). Under "Our Churches" it lists only St. Mary and St. Patrick, plus
    the Adoration Chapel.
- url: https://container.parishesonline.com/bulletins/06/0115/20261004B.pdf
  seen: 2026-10-02
  quote: St. Mary, 224 Franklin St. Elmira
- url: https://container.parishesonline.com/bulletins/06/0115/20261004B.pdf
  seen: 2026-10-02
  quote: St. Patrick, 604 Park Place, Elmira
- url: https://container.parishesonline.com/bulletins/06/0115/20261004B.pdf
  seen: 2026-10-02
  quote: 'Eucharistic Adoration Chapel:'
  note: Listed with the churches, but every Mass in the "Mass Times and Intentions" on page 2 is at St.
    Mary or St. Patrick.
- url: https://www.elmiracatholic.org/wp-content/uploads/2026/09/Copy-of-9-27-26.pdf.pdf-1.pdf
  seen: 2026-10-02
  quote: Parish of the Most Holy Name of Jesus
  note: The 27 September 2026 issue as posted on the parish site (WordPress post https://www.elmiracatholic.org/2026/09/28/september-27-2026-bulletin/,
    a DFlip flipbook whose source is this PDF). Same masthead and same two churches.
- url: https://www.elmiracatholic.org/
  seen: 2026-10-02
  quote: Most Holy Name of Jesus Parish is now the the overall Parish for all Elmira City Roman Catholic
    Churches, Which consists of St. Mary’s Church on Elmira’s Southside, and St. Patrick’s Church on Elmira’s
    Northside.
  note: Homepage, read 2026-10-02.
- url: https://ps.dor.org/directory/parish-of-the-most-holy-name-of-jesus/
  seen: 2026-10-02
  quote: a multi-site parish in Elmira, New York, Chemung County
  note: The diocese Directory of Parishes (updated 1/27/25). Its description still lists six sites (St.
    Patrick, Ss. Peter and Paul, Our Lady of Lourdes, St. Casimir Church & Faith Formation Center, Perpetual
    Adoration Chapel, St. Mary) but its Mass schedule names only St. Mary and St. Patrick.
promoted: 2026-10-02
---

## Publisher

The Parish of the Most Holy Name of Jesus publishes one weekly bulletin for Elmira. The 4 October 2026
issue (ParishesOnline container 06/0115) and the 27 September issue (the PDF on the parish site) have the
same masthead, "Parish of the Most Holy Name of Jesus, Elmira, NY", and the same "Our Churches" box:
St. Mary, 224 Franklin St., and St. Patrick, 604 Park Place, with the Eucharistic Adoration Chapel at
1012 Davis St. and the Parish Office / Faith Formation Center at 1010 Davis St. All Masses on page 2 are at
those two churches (Saturday 4:00 pm St. Mary; Sunday 7:30 am and 10:30 am St. Patrick, 9:00 am St. Mary).
The diocese groups nothing here: the Directory of Parishes calls it "a multi-site parish".

## Worship sites

Two churches: `churches/st-marys-elmira.md` and `churches/st-patricks-elmira.md`. Everything else the
rosters list for this parish is accounted for:

- `excluded/eucharistic-adoration-chapel-elmira.md`: a chapel, no Mass. It was a live church row; it
  is moved out.
- `excluded/our-lady-of-lourdes-elmira.md` and `excluded/ss-peter-and-paul-elmira.md`: relegated and closed
  15 November 2021.
- `excluded/st-charles-borromeo-elmira-heights.md`: closed in early 2020 (Catholic Courier).
- `open/st-casimir-elmira.md`: unavailable for worship since at least November 2021, no source says it was
  closed or relegated, so it is open, not excluded.
- St. Nicholas, Elmira Heights, is Ukrainian: `excluded/st-nicholas-elmira-heights.md`.

## Website and bulletin provider

`elmiracatholic.org` is the parish site (WordPress). Its News/Bulletins page lists one post per Sunday, each a
DFlip flipbook of a PDF under wp-content/uploads (file names are irregular, such as
"Copy-of-9-27-26.pdf.pdf-1.pdf"), so the provider stays `other` and the publication is the bulletins page.
The same bulletin is also on ParishesOnline as container 06/0115 (its 4 October issue was up on 2026-10-02;
older issues from 2024 and 2025 are there too), recorded as a second publication id. I could not find the
organization slug for that container (`probe po` found no guess), so `parishes_online` with a
provider_id was not an option.

## Not yet confirmed

- That the `other` resolver reads the DFlip posts (not tested here). If it does not, the ParishesOnline
  organization slug for container 06/0115 is the better channel; find it from a parishesonline.com page.
