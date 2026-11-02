---
name: St. Cecelia
website: https://www.stcecelia.com
bulletin_provider: ecatholic
provider_id: ''
publication: ['ecatholic:22597']
group: ''
evidence:
- url: https://files.ecatholic.com/22597/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: ST. CECELIA CHURCH
  note: 'Page 1 of the 1 November 2026 issue (16 pages, text) is the masthead: ''45 Wilus Way, Iselin,
    NJ 08830'', ''GPS—Use 51 Vernam St, Iselin NJ 08830'', phone 732-283-2300, www.stcecelia.com, ''ST.
    CECELIA CHURCH November 1, 2026 All Saints Day''. Page 2''s Parish Directory names ''Fr. Deniskingsley
    Nwagwu, SDV Pastor'' and ''Fr. Nidhin Jose, SDV Parochial Vicar''.'
- url: https://files.ecatholic.com/22597/bulletins/20261101.pdf
  seen: 2026-11-02
  quote: 11:30am & 1:30pm (Spanish)
  note: 'Page 11 Mass Schedule: ''Mon.-Fri.: 7:00 am and 9:15 am'', ''Sat. 8:00 am'', ''4:30pm ,Vigil
    Mass'', ''Sunday Mass: 7:30am, 9:30am, 11:30am & 1:30pm (Spanish)''. The issue names no other worship
    site; its only St. James mention is an ''8th Grade Retreat at St. James Church'' on 19 November (calendar,
    page 11).'
- url: https://www.stcecelia.com/bulletins
  seen: 2026-11-02
  quote: November 1, 2026
  note: eCatholic site 22597 (loaded with visit.py; probe url said DEAD-DNS and probe get 403). Its Bulletin
    page lists weekly files named by Sunday date at files.ecatholic.com/22597/bulletins/<YYYYMMDD>.pdf,
    newest 1 November 2026.
bulletin_status: available
---

## Publisher

St. Cecelia, 45 Wilus Way, Iselin, publishes its own weekly bulletin on its eCatholic site (22597). The 1 November 2026 issue (read 2026-11-02) has the masthead 'ST. CECELIA CHURCH' with the Wilus Way address on page 1, and page 2 names 'Fr. Deniskingsley Nwagwu, SDV Pastor' and 'Fr. Nidhin Jose, SDV Parochial Vicar'.

## Shared bulletin with St. James, Woodbridge?

The batch asked whether St. Cecelia and St. James share a bulletin because the parish finder lists Rev. Thomas Naduviledathu, SDV as pastor of both. They don't: each has its own eCatholic site (22597 here, 27749 for St. James) and its own weekly issues. The 1 November 2026 St. Cecelia issue names Fr. Deniskingsley Nwagwu, SDV as pastor and gives only St. Cecelia's Mass schedule, while the same day's St. James issue (page 2) names 'Fr. Thomas Naduviledathu, SDV' as its pastor. The finder's clergy line for St. Cecelia is out of date. Both parishes are served by the Vocationist Fathers (SDV), which explains the shared order but not a shared bulletin. See `parishes/st-james-woodbridge`.

## Worship sites

One church, 45 Wilus Way (directory:24499, gcatholic:18644). The bulletin's Mass schedule (page 11) is for this church alone. An 'Adoration Chapel' is mentioned in the bulletin; it is part of the parish, not a separate Mass site.

## Website and bulletin provider

Website https://www.stcecelia.com (the finder's and GCatholic's domain; the masthead prints www.stcecelia.com). `probe url` said DEAD-DNS and `probe get` answered 403 on 2026-11-02; the browser loaded it as eCatholic site 22597, whose Bulletin page lists the weekly PDFs by Sunday date. Provider `ecatholic`.

## Fetch check

`pnpm fetch:check` on 2026-11-02 picked https://files.ecatholic.com/22597/bulletins/20261101.pdf (the 1 November 2026 issue): transport ok, PDF, issue date observed, freshness fresh (1 day), identity unverified by the tool; I read that issue myself (evidence above).

## Not yet confirmed

Nothing open.
