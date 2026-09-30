---
name: St. Joseph's
reason: closed
line1: 22 Bayley Rd.
city: Massena
state: NY
postal_code: '13662'
decided: 2026-09-30
roster: ['gcatholic:18306']
evidence:
- {url: 'https://gcatholic.org/churches/usa-02/18306', seen: 2026-09-30, quote: '22 Bayley Rd., Massena,
    New York 13662', note: 'Listed in GCatholic: churches of the Roman Catholic Diocese of Ogdensburg
    as ''St. Joseph'', 22 Bayley Rd., Massena, NY, 13662; kind: Church'}
- {url: 'https://www.nny360.com/news/stlawrencecounty/changes-coming-to-area-catholic-communities-on-nov-1/article_03d6fbd0-b5c6-5400-a5ad-766fb7489267.html',
  seen: '2026-09-30', quote: 'St. Joseph’s, had already been changed to oratory status following a final
    Mass in 2017', note: 'Watertown Daily Times, 2 Sep 2026 (paywalled; body scrambled in the raw HTML,
    readable in a browser only, so recheck will probably not find it). Continues: "In oratory status,
    the building has been closed and does not have regular Masses scheduled. But it is available for special
    occasions such as weddings and, funerals."'}
- {url: 'https://massenacatholics.com/mass-times', seen: '2026-09-30', quote: '11:00 AM St. Mary''s Church',
  note: 'Parish Mass Times page (Cloudflare; read in a browser) lists Masses at Sacred Heart, St. Mary''s
    and St. Lawrence only; no St. Joseph''s, although the page footer still prints "St. Joseph''s, 22
    Bayley Rd., Massena".'}
- {url: 'https://container.parishesonline.com/bulletins/06/0114/20260927B.pdf', seen: '2026-09-30', quote: 'Sacred
    Heart & St. Lawrence, Massena, NY 06-0114', note: Page 5 advertiser line still reads "St. Mary & St.
    Joseph/Sacred Heart & St. Lawrence" (LPi account name); grep of the whole issue for "Bayley" finds
    nothing and the page 4 calendar has no Mass at St. Joseph's.}
- {url: 'https://www.rcdony.org/parish/massena', seen: '2026-09-30', quote: 'Worship sites: St. Mary''s
    Church - Massena Worship sites: St. Lawrence Church - Louisville', note: 'Diocesan directory lists
    St. Peter''s Parish with Sacred Heart, St. Mary''s and St. Lawrence; no St. Joseph.'}
parish: st-peters-parish-massena
---

## Why it is excluded

**St. Joseph's, 22 Bayley Rd., Massena: no regular Mass since 2017.** The Watertown Daily Times of 2 September 2026 says "One of Massena's churches, St. Joseph's, had already been changed to oratory status following a final Mass in 2017. In oratory status, the building has been closed and does not have regular Masses scheduled. But it is available for special occasions such as weddings and, funerals." The current St. Peter's Parish bulletin (27 September 2026, container 06/0114) and the parish's Mass Times page schedule no Mass there, and the diocesan directory does not list it as a worship site, but the parish website footer still prints its address and GCatholic (updated 2025-12-21) still lists it as a church affiliated with St. Mary's. It is an oratory in the diocese's sense: closed, used for weddings and funerals, so no public Mass. `last_mass` is not set because the article gives only the year, 2017; nothing was found that dates it more closely (a search of the North Country Catholic turned up nothing).

The reason is `closed` (no Mass any more) rather than `no-public-mass`: it was a parish church whose Masses stopped, not a private chapel.

## What would change this

A bulletin or schedule that lists a Mass at St. Joseph's (a wedding or funeral does not count). The North Country Catholic's 2017 report of the final Mass would give the exact date for `last_mass`.
