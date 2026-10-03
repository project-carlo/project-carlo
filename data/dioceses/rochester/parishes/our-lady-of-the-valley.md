---
name: Our Lady of the Valley Parish
website: https://www.olv14843.org
bulletin_provider: other
provider_id: page-pdfs https://www.olv14843.org/about/bulletins/
publication:
- url:https://www.olv14843.org/about/bulletins/
group: ''
evidence:
- url: https://www.olv14843.org/wp-content/uploads/20261004.pdf
  seen: '2026-10-02'
  quote: OUR LADY OF THE VALLEY PARISH
  note: 'Week of 4 October 2026 bulletin, page 1: "OUR LADY OF THE VALLEY PARISH ... 27 Erie Avenue • Hornell, NY
    14843 ... https://olv14843.org". Same masthead in the 27 September issue.'
- url: https://www.olv14843.org/wp-content/uploads/20261004.pdf
  seen: '2026-10-02'
  quote: WEEKEND MASSES Saturday 4:30 pm St. Ann Sunday 6:45 am & 10:45 am St. Ann Sunday 8:45 am St. Mary
- url: https://www.olv14843.org/about/bulletins/
  seen: '2026-10-02'
  note: 'Parish Bulletins page: one PDF per week at https://www.olv14843.org/wp-content/uploads/YYYYMMDD.pdf (20261004,
    20260927, 20260920 ... back to 20260621). `probe url`/visit.py --bulletin finds no publisher id: self-hosted.'
- url: https://www.olv14843.org/about/
  seen: '2026-10-02'
  quote: includes the churches of St. Ann and St. Mary's. Masses are celebrated at both St. Ann's Church in Hornell,
    and St. Mary's Church in Rexville.
- url: https://ps.dor.org/directory/our-lady-of-the-valley-parish/
  seen: '2026-10-02'
  quote: Our Lady of the Valley, a multi-site parish, Hornell, Rexville, New York, Steuben County
promoted: 2026-10-02
---

## Publisher

Our Lady of the Valley Parish, Hornell, publishes its own weekly bulletin, a PDF on its WordPress site. The 4 October 2026 masthead (page 1) is "OUR LADY OF THE VALLEY PARISH, 27 Erie Avenue, Hornell". Its Mass schedule lists St. Ann (Hornell) and St. Mary (Rexville) only. One row; the diocese groups nothing else with it.

## Worship sites

Two: `st-anns` (Hornell: Saturday 4:30 pm, Sunday 6:45 and 10:45 am, weekdays 12:10 pm) and `st-marys-rexville` (Sunday 8:45 am). GCatholic's St. Ignatius (343 Canisteo St., Hornell) and St. Joachim (Canisteo) are excluded as closed (`excluded/st-ignatius-hornell`, `excluded/st-joachim-canisteo`: the parish's own page names only St. Ann and St. Mary; the Catholic Courier says St. Joachim closed in 2005). The sacramental index also lists St. Mary, Greenwood as merged; it is on no schedule. The parish's chapel of adoration ("formerly St. Ann's Convent Chapel", open 6 am-7 pm) is not a Mass site.

## Website and bulletin provider

www.olv14843.org is the parish's own site and is live; its Bulletins page (`/about/bulletins/`) links the weekly PDFs, so `bulletin_provider: other` with `publication: url:https://www.olv14843.org/about/bulletins/`, no provider_id. The Parish Locator links ourladycv.org instead: that domain still answers HTTP 200 but serves an empty page (last modified 15 February 2025; no parish text, so `probe url` says NO-PARISH-WORDS), so it is a dead former site and not used. The bulletin PDFs have text.

Fetch recipe `page-pdfs https://www.olv14843.org/about/bulletins/`, pinned 2026-10-03: on the pages recorded in `tests/fixtures/fetch/our-lady-of-the-valley.json.gz` the resolver found https://www.olv14843.org/wp-content/uploads/20260927.pdf this way, dated that week.

## Not yet confirmed

Nothing.
