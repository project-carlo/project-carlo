---
name: Cathedral of St. Francis of Assisi
website: https://www.stfranciscathedral.org
bulletin_provider: discover_mass
provider_id: st-francis-of-assisi-cathedral-metuchen-nj
publication: ['discovermass:st-francis-of-assisi-cathedral-metuchen-nj']
group: ''
evidence:
- url: https://discovermass.com/church/st-francis-of-assisi-cathedral-metuchen-nj/
  seen: 2026-11-02
  quote: Nov 1, 2026
  note: 'Discover Mass church page ''St. Francis of Assisi Cathedral'': ''Current Bulletin Nov 1, 2026'',
    archive Oct 25, Oct 18, Oct 11, Oct 4, 2026. Read with issues.py discovermass; download links are
    tokenised and capped per IP per day, so the church page is cited.'
- url: https://discovermass.com/church/st-francis-of-assisi-cathedral-metuchen-nj/
  seen: 2026-11-02
  note: 'The 1 November 2026 issue (12 pages, all text): page 1 Mass schedule ''Saturday Vigil ... 5:00pm;
    Sunday 8:00, 10:00, 12:00pm and 5:00pm; Monday-Friday 7:00, 8:00am, 12:10pm; Saturday 8:00am''; page
    2 directory ''CATHEDRAL OF ST. FRANCIS OF ASSISI 548 Main St. Metuchen, NJ 08840'', ''Parish Office
    Address 45 Library Place Metuchen'', ''Very Rev. Timothy A. Christy Rector'', ''View this bulletin
    online at www.DiscoverMass.com''. Names no other church.'
- url: https://www.stfranciscathedral.org/
  seen: 2026-11-02
  quote: https://discovermass.com/church/st-francis-of-assisi-cathedral-metuchen-nj/
  note: The cathedral's own site (Thrillshare/Apptegy, not eCatholic) has a 'Bulletin' button linking
    to the Discover Mass church page.
bulletin_status: available
---

## Publisher

The Cathedral of St. Francis of Assisi, Metuchen, publishes its own weekly bulletin through Discover Mass (church slug `st-francis-of-assisi-cathedral-metuchen-nj`). The Discover Mass church page (read 2026-11-02) lists 'Current Bulletin Nov 1, 2026' and weekly issues back to 4 October. The 1 November 2026 issue (12 text pages, read with `issues.py discovermass`) gives the Mass schedule on page 1 and, on page 2, the directory 'CATHEDRAL OF ST. FRANCIS OF ASSISI 548 Main St. Metuchen, NJ 08840', parish office 45 Library Place, and 'Very Rev. Timothy A. Christy, Rector' (the finder's rector line agrees). It names no other church or parish.

## Worship sites

One church, the cathedral at 548 Main Street (directory:24462). The bulletin's Mass schedule covers one building. GCatholic's Metuchen list omits the cathedral (see `diocese.md`, *Sources*), so there is no GCatholic entry to link.

## Website and bulletin provider

Website: https://www.stfranciscathedral.org, the cathedral's Thrillshare site (`probe url` said DEAD-DNS on 2026-11-02, a known false result here; `probe get` loaded it). Its 'Bulletin' button links the Discover Mass church page, so the provider is `discover_mass` with the church slug as `provider_id`.

## Not yet confirmed

Nothing about identity or the Mass schedule. Discover Mass caps downloads per IP per day, so a `fetch:check` failure reported as `not_pdf` is the cap, not a missing bulletin.

## Fetch check

`pnpm fetch:check` on 2026-11-02 visited the Discover Mass church page, took its 'Current Bulletin' link (the 1 November 2026 issue) and downloaded a 13.9 MB PDF: transport ok, document PDF; issue date and freshness `unknown` because the tokenised download URL carries no date. The church page lists that link as 'Nov 1, 2026', the current Sunday. Identity isn't checked by the tool; I read the issue's directory myself (above).
