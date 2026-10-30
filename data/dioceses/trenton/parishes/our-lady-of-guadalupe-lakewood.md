---
name: Our Lady of Guadalupe Parish
website: https://olglakewood.org/
bulletin_provider: other
provider_id: page-pdfs http://sponsors.bonventure.net/?page=2195
publication: ['url:http://sponsors.bonventure.net/?page=2195']
group: Cohort 22 (Brick and Lakewood)
evidence:
- url: http://sponsors.bonventure.net/pdfs/2195/2026-11-01.pdf
  seen: 2026-10-30
  quote: Rev. Guilherme Andrino, S.V.D., Pastor
  note: 'The 1 November 2026 issue (12 pages, text layer) is a bulletin for Our Lady of Guadalupe alone,
    trilingual (English, Spanish, Polish). Page 1 is the Mass schedule: Holy Family Church (HF) 1139 East
    County Line Road; St. Mary of the Lake (SML) church and office, 43 Madison Avenue; St. Anthony Claret
    (SAC), 780 Ocean Avenue; Saturday vigil 4:00 pm Holy Family and 5:00 pm St. Anthony Claret; Sunday
    8:00 am, 12:30 pm and 3:00 pm Holy Family, 10:30 am St. Anthony Claret, 9:30 am (Polish) and 11:30
    am St. Mary of the Lake; daily 9:00 am St. Mary of the Lake Monday-Saturday, 7:00 pm St. Anthony Claret
    Tuesday-Friday.'
- url: http://sponsors.bonventure.net/?page=2195
  seen: 2026-10-30
  quote: Click to View Current Bulletin
  note: Bon Venture sponsor page 2195, headed Our Lady of Guadalupe, 43 Madison Avenue, Lakewood, NJ 08701;
    previous bulletins listed weekly from 1 November 2026.
- url: https://olglakewood.org/
  seen: 2026-10-30
  note: 'Read in the browser (visit.py --links). The home page links https://sponsors.bonventure.net/?page=2195;
    the site (WordPress, no publication id) has no bulletin archive of its own: its Parish Weekly News
    page is announcements. Its Mass and Confession Schedule page lists Holy Family Church, St. Anthony
    Claret Church and St. Mary of The Lake Church.'
- url: https://trentonmonitor.com/2025/10/09/in-aftermath-of-fire-lakewood-pastor-reminds-parishioners-that-god-is-with-us/
  seen: 2026-10-30
  quote: wrapping in the Holy Family School and Church campus
  note: 'The Monitor, 9 October 2025: Our Lady of Guadalupe was created in 2020 by the merger of St. Mary
    of the Lake and St. Anthony Claret, wrapping in the Holy Family School and Church campus; the Holy
    Family school building on East County Line Road burned on 3 October 2025.'
research:
- method: visit.py --links on olglakewood.org; probe url on Bon Venture 2195; probe pdf --grep on the
    1 November 2026 issue; Monitor REST search
  url: http://sponsors.bonventure.net/?page=2195
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: Bon Venture 2195 is the bulletin channel. The John Patrick scans (ids 1-1300, 6000-6110)
    list no Lakewood parish.'
- method: pnpm fetch:check --diocese trenton --parish our-lady-of-guadalupe-lakewood (headed Chrome);
    page-pdfs on http://sponsors.bonventure.net/?page=2195
  url: http://sponsors.bonventure.net/pdfs/2195/2026-11-01.pdf
  checked: '2026-10-30'
  outcome: found
  next_action: 'None: it picked the 1 November 2026 issue (text layer; coming Sunday, ''future'' freshness);
    its page 1 names Our Lady of Guadalupe.'
bulletin_status: available
publication_reviews:
- parish: st-dominic-brick
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2195/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 1) names Our Lady of Guadalupe, Lakewood, alone, with pastor
      Rev. Guilherme Andrino, S.V.D. and the Mass times of its three churches. (Bon Venture 2195)
  - url: http://sponsors.bonventure.net/pdfs/4139/2026-10-25.pdf
    seen: 2026-10-30
    note: The 25 October 2026 masthead (page 1) names the Church of Saint Dominic and Diocesan Shrine
      of Saint Carlo Acutis, 250 Old Squan Road, Brick, alone, with pastor Rev. Brian Patrick Woodrow
      and its own Mass times. (Bon Venture 4139)
- parish: visitation-brick
  decision: separate
  evidence:
  - url: http://sponsors.bonventure.net/pdfs/2195/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 1) names Our Lady of Guadalupe, Lakewood, alone, with pastor
      Rev. Guilherme Andrino, S.V.D. and the Mass times of its three churches. (Bon Venture 2195)
  - url: https://files.ecatholic.com/6597/bulletins/20261101.pdf
    seen: 2026-10-30
    note: 'The 1 November 2026 issue is a bulletin for the Church of the Visitation alone (page 2: pastor
      Very Rev. Edward H. Blanchett, 755 Mantoloking Road), with its own Mass times. (eCatholic 6597 =
      John Patrick 574)'
---

## Publisher

Our Lady of Guadalupe Parish, Lakewood (Cohort 22). It publishes one bulletin, printed by Bon Venture (sponsor page 2195), linked from the parish homepage. The 1 November 2026 issue's page 1 is the combined Mass schedule for three churches under one pastor, Rev. Guilherme Andrino, S.V.D. (page 2). The parish was created 1 July 2020 by merging St. Mary of the Lake and St. Anthony Claret (The Monitor, 26 June 2020), and the Monitor of 9 October 2025 says it also wrapped in "the Holy Family School and Church campus".

## Worship sites

Three churches, all listed in the bulletin's Mass schedule and on the parish site's Mass and Confession Schedule: St. Mary of the Lake (43 Madison Ave, with the parish office), St. Anthony Claret (780 Ocean Ave) and Holy Family (1139 East County Line Rd). The roster entries map as follows: directory:14652 and gcatholic:18779 are St. Mary of the Lake, gcatholic:18736 is St. Anthony Claret, and gcatholic:18818 (GCatholic's "St. Mary of the Lake", 1141 E County Line Rd, affiliated with "Church of St. Mary") is the Holy Family site, by its street, not a fourth church. directory:26652 is the merged parish's own finder pin (two addresses, no coordinates; its phone is St. Mary of the Lake's). The Holy Family school building is not a worship site (burned 3 October 2025).

## Website and bulletin provider

olglakewood.org holds no bulletin archive; the printer's Bon Venture page is read with a page-pdfs recipe. The finder's website is the row's website.

## Not yet confirmed

The Bon Venture issues were not compared with a second channel; no John Patrick listing exists for Lakewood in the scans.
