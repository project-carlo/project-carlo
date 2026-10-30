---
name: Parish of St. John Neumann
website: https://www.parishofstjohnneumann.org/index.php/sunday-bulletins
bulletin_provider: other
provider_id: page-pdfs https://www.parishofstjohnneumann.org/index.php/sunday-bulletins filename=bulletin*.pdf
publication: ['url:https://www.parishofstjohnneumann.org/index.php/sunday-bulletins#st-john-neumann']
group: St. John Neumann Parish
evidence:
- url: https://www.parishofstjohnneumann.org/images/bulletin2026/bulletin102526.pdf
  seen: 2026-10-29
  quote: Parish of St. John Neumann
  note: 'Text-layer PDF (12 pages) read with probe pdf. Page 1: ''October 25, 2026 - Thirtieth Sunday
    in Ordinary Time MASS SCHEDULE'', for ''St. John of God Church 680 Town Bank Road North Cape May,
    NJ 08204 Weekend Masses: Saturday 4pm & Sunday 10am Daily Mass 9am'' and ''St. Raymond Church 800
    Bayshore Road Villas, NJ 08251 Weekend Masses: Sunday 8am (English) Sunday 12pm (Spanish) Sunday 6pm
    (Spanish)''. Page 2: ''Reverend Jaime Hostios ... Pastor'', office 609-884-1656. Names this parish
    alone.'
- url: https://www.parishofstjohnneumann.org/index.php/sunday-bulletins
  seen: 2026-10-29
  quote: Sunday Bulletins
  note: The parish's own Joomla page lists every Sunday bulletin by date ('October 25, 2026 - 30th Sunday
    in Ordinary Time', newest) in 'Sunday Bulletins 2026' and 'Sunday Bulletins 2025' tabs. Each entry
    is a Joomla weblink (/index.php/component/weblinks/weblink/213-october-25-2026-...?task=weblink.go)
    that redirects (301) to /images/bulletin2026/bulletin102526.pdf. It carries no other parish's bulletin.
- url: https://www.parishofstjohnneumann.org/index.php/sunday-bulletins
  seen: 2026-10-29
  quote: New Schedule as of September 10, 2026!
  note: 'The page''s sidebar lists both churches'' Mass times, the same as the 25 October bulletin: St.
    John of God Saturday 4pm, Sunday 10am, daily 9am; St. Raymond Sunday 8am English, 12pm and 6pm Spanish,
    First Saturday 9am, Thursday 7pm Spanish.'
- url: http://www.parishofstjohnneumann.org
  seen: 2026-10-29
  note: 'The directory''s website redirects to https://www.parishofstjohnneumann.org/ (probe url: ok,
    title ''Welcome to the Parish of St. John Neumann''). stjohnneumann.org is the National Shrine in
    Philadelphia, not this parish.'
research:
- method: fetch:check with recipes page-pdfs (default), linked-issue-page, dated-post and redirected-pdf
    on the Sunday Bulletins page; curl -I on the weblink hrefs
  url: https://www.parishofstjohnneumann.org/index.php/sunday-bulletins
  checked: '2026-10-29'
  outcome: unsupported-format
  next_action: Add a collector (or extend page-pdfs) that follows Joomla weblink '?task=weblink.go' redirects
    to /images/bulletin2026/bulletinMMDDYY.pdf and picks the newest; until then the pinned recipe filename=bulletin*.pdf
    fails loudly rather than fetching the Religious Education calendar the unpinned page-pdfs picks first.
  retry_when: A collector can follow Joomla weblink redirects, or the parish links its PDFs directly
bulletin_status: unsupported-format
---

## Publisher

The Parish of St. John Neumann (North Cape May; the merger of St. John of God and St. Raymond, Villas) publishes its own weekly bulletin on its Joomla site, parishofstjohnneumann.org, under Sunday Bulletins. The 25 October 2026 issue (text layer, 12 pages; read 2026-10-29) is headed 'Parish of St. John Neumann' on its Mass-intentions page, lists the Mass schedule of both churches on page 1 and names Rev. Jaime Hostios as pastor on page 2. It is no other parish's bulletin; Our Lady Star of the Sea, Cape May publishes separately.

## Worship sites

Two, each with its own church record: St. John of God (680 Town Bank Road, North Cape May) and St. Raymond (800 Bayshore Road, Villas). The bulletin and the parish's schedule list Mass at both in October, so neither is seasonal.

## Website and bulletin provider

`other`, with the Sunday Bulletins page as website and recipe. Its links are Joomla weblink redirects rather than .pdf hrefs; the pipeline's collectors don't follow them (see research): the unpinned default picks the Religious Education calendar, so the recipe pins `filename=bulletin*.pdf` to fail loudly. The newest issues are reachable by hand: the weblink for 25 October 301s to /images/bulletin2026/bulletin102526.pdf, and bulletin110126.pdf already answered 200 on 2026-10-29, though the page didn't list it yet. The directory's website (parishofstjohnneumann.org) is current. GCatholic lists the same site on St. John of God.

## Not yet confirmed

The bulletin is real, current and read, but `fetch:check` can't resolve it from the site (research). The parish row stays `other` until a collector can follow the redirects.
