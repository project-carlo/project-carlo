---
name: Roman Catholic Diocese of Buffalo
state: NY
website: https://www.buffalodiocese.org
status: promoted
gcatholic: buff0
promoted: 2026-11-24
---

## Sources

- Parish directory: the diocesan parish finder (`rosters/directory.json`, 167 entries). Current and
  geocoded, but it names canonical parishes as well as buildings. It also lists social-service
  sites: the seven St. Gianna Molla outreach centers are excluded as `no-public-mass`.
- GCatholic: `rosters/gcatholic.json` (216 entries). Good addresses and full-precision Plus Codes.
  It still carries many churches closed since 2007, and Eastern Catholic churches of other
  jurisdictions.
- Clusters / families of parishes: the April 2026 Family of Parishes masterlist
  (`rosters/families.json`). The best source for canonical structure, but it lags on closures,
  and a family is not a bulletin: most families publish one, some several.
- Mass times: the diocese's three weekend Mass-times pages (`rosters/mass-times.json`). They
  lag in both directions (Queen of Angels was still listed after its last Mass).
- Closed parishes and where their records went: https://www.buffalodiocese.org/sacramental-records/.
  An end year there means the parish merged; it does not mean the building closed (St. John the
  Baptist, Boston ends in 2025 and still has Mass).
- Pastoral plan / closure announcements: the Road to Renewal summary sheet of 13 September 2024
  (Renewal-Timeline-and-Summary-20240913.pdf). Its "merging and closing" lists are a plan: East
  Arcade, St. Hyacinth, Wilson and SS. Peter and Paul (Jamestown) are on them and still hold Mass.
  Closures are taken from bulletins, decrees and family sites instead.
- Bishop's decrees: families post them on their own sites (reduction to profane use, merger,
  relegation). Most are scanned PDFs with no text layer; read them with parish-site-access
  `render.py`. Wikipedia's list (next item) links about 30 of them.
- Wikipedia, "List of churches in the Diocese of Buffalo": a closed-churches table whose "Closed"
  column is the year of the last Mass, with notes on sales and later use. It is a secondary source
  (some rows cite nothing, e.g. Cassadaga), used here for old closures no primary source dates,
  and its wikitext (`action=raw`) is the quickest way to the decrees it cites.

## Rules settled for this diocese

- A worship site counts as a church only if a current (September 2026) bulletin or the
  community's own site shows Mass there. Where the bulletin names a site but its text does not
  tie times to it (Bread of Life, Fields of Grace), the diocesan Mass-times pages supply the times.
- The Genesee–Wyoming section of the 2024 summary is headed "Parishes/sites merged and closed"
  (past tense), but that heading also covers whole parishes whose churches still hold Mass
  (St. George, St. Brigid, Ascension). Only its entries marked "site" (Elba, East Bethany,
  Strykersville, Perry, Silver Springs, Corfu) are read as closed buildings. Each of those is also
  absent from its family's current bulletin.
- A plan plus absence from a bulletin goes in open/, not excluded/. (The seven PR 14 cases,
  St. James Depew, Divine Mercy, St. Joseph Lockport, Panama, Cassadaga, Portville and
  St. Francis Tonawanda, were all closed on stated sources on 2026-11-16; see the Log.)
- Places that hold public Mass but publish no bulletin: Our Lady of Hope, St. Joseph University
  Parish and St. Andrew Kim were kept as `no_bulletin` parish rows, following Rochester's live
  `holy-apostles` row, so their churches stayed on the map. Superseded 2026-10-07: a `no_bulletin`
  row is now kept in the records but left off the site (README, Settled policy 4); St. Joseph
  University turned out to publish a bulletin and St. Andrew Kim had closed (see the Log).
  Syracuse excluded a similar place (Alibrandi) instead. The difference is that these three were
  already live churches in PR 14 and have their own church buildings in the diocesan roster.
  The UB Newman Center, once excluded as `no-bulletin`, became a church of
  `st-joseph-university-buffalo` on 2026-10-07, whose bulletin prints its Masses.
- Owner's decision, 2026-11-16: a place whose public Mass is listed online (its own site,
  Facebook, the diocese's pages) but which publishes no bulletin stays open/unresolved, not
  excluded as `no-bulletin`, because a feature to show such places is coming. Each record says
  where its times are published (URL, date seen, quote) in evidence and in a *Mass times
  published* section. A place that never had a parish row goes in `open/` (a parish row needs a
  website): Holy Family (Sanborn, reopened from `excluded/`), Niagara University's chapel, the
  Canisius and St. Bonaventure University chapels, Mt. Irenaeus and the Infant Jesus Shrine. Our
  Lady of Hope keeps its `no_bulletin` parish row, which is already unresolved and off the site.
  The feature landed as source schedules (`website_schedule` rows, docs/source-schedules-plan.md),
  which cite only the place's own website or Facebook page, never the diocese's lists. On
  2026-11-24 Mt. Irenaeus and the Canisius and St. Bonaventure chapels moved to it (see the Log).
- Eastern Catholic churches in the territory are excluded as `other-jurisdiction`, each confirmed
  on its GCatholic page (Ukrainian Stamford, Ruthenian Passaic, Maronite Brooklyn).

## Log

- 2026-09-26: Re-expressed PR 14's Buffalo rows (72 parishes, 151 churches, written straight into
  the CSVs) as records, then promoted them.
  - Parishes: 46, one per bulletin. PR 14's family-level rows that were one bulletin became one
    parish; its rows for churches that share a family bulletin (for example the Light of Christ
    and Bread of Life churches) were merged. Fourteen Holy Helpers, Queen of Heaven and
    St. John Vianney share the Blessed Family #7 bulletin.
  - Churches: 146, each with Mass evidence quoted from a September 2026 bulletin where the text
    layer allowed, and otherwise an OCR or reading note.
  - PR 14 churches that are no longer churches here: St. Anthony (Fredonia) closed on
    31 August 2026 and is excluded. Blessed Mother Teresa of Calcutta (now St. James, Depew),
    Divine Mercy (Niagara Falls), Sacred Heart (Portville) and St. Francis of Assisi (Tonawanda)
    are in open/.
  - Renamed: St. George (West Falls) is now the Memorare Chapel. St. Bridget (Newfane) and
    Our Lady of the Rosary (Wilson) are St. Brendan on the Lake sites.
  - 33 exclusions (24 closed, each on a stated source; the seven Gianna centers; two
    `no-bulletin`) and 7 open records. Cassadaga, Lockport St. Joseph and Panama moved from PR 14's
    "closed" to open/ because no source states that they closed.
  - Coverage: directory 167/167 accounted for; families 146/151; mass-times 141/145;
    GCatholic 174/216.
  - Not yet accounted for (GCatholic): mostly churches closed before 2020 that GCatholic still
    lists (All Saints, Coronation, Holy Angels, St. Bernard, St. Clare, St. Lawrence in Buffalo;
    Andover, Bolivar, Blasdell, St. Augustine Depew, St. Andrew Kenmore, St. Anthony Lackawanna,
    Limestone, Medina Sacred Heart, St. Raphael, Middleport, Darien Center, Bennington Center,
    Corfu, Rushford, St. Agatha Buffalo, Le Roy St. Joseph and others). Also Eastern Catholic
    churches of other jurisdictions (St. Nicholas Buffalo, OLPH Lackawanna, St. Basil Lancaster,
    Protection of the BVM Niagara Falls, St. John Maron Williamsville, and probably St. Mary and
    St. Joseph in Olean), which belong in excluded/ as `other-jurisdiction` once each GCatholic
    page is checked. Unmatched families and mass-times entries are parish-level names
    (Our Lady of Charity, St. Vincent de Paul and Holy Family, Niagara Falls) that were not tied
    to one building.
  - Unconfirmed, noted on the records: 16 disputed addresses (`address_verified` false); St. Jude
    the Apostle (North Tonawanda), which is reported merged by an August 2026 decree but still
    has scheduled Masses; and the St. John Kanty recourse.
- 2026-10-07: Audited the churches the site showed with no Mass. St. Joseph University publishes a
  ParishesOnline bulletin after all (the Campus Ministry Family, container 14/1703; pages 1-6 are
  images): the row is `parishes_online` now, and the UB Newman Center, whose Masses that bulletin
  prints, moved from `excluded/` to a church of it. St. Andrew Kim, Tonawanda closed on 31 March
  2025 (the community's own notices; sold to O'Hara High School): excluded as closed, parish row
  deleted. Our Lady of Hope stays `no_bulletin` (checked its own site, ParishesOnline, Discover
  Mass and the Holy Cross bulletin), which now keeps it off the site (README, Settled policy 4).
  Bread of Life's page limit is 12 (`data/bulletin_page_limits.csv`): Ss. Peter & Paul's page is
  11. St. Charles Borromeo (Olcott, summer), St. Adalbert (about four Masses a year) and St.
  Pacificus (occasional) stay church rows with no Mass this week. Promoted.
- 2026-10-27: Church-list fixes from seed drafts. Added St. Francis of Assisi Chapel, 71 Adam St.,
  Tonawanda (`st-francis-of-assisi-chapel-tonawanda`; the family's site lists it and the
  25 October bulletin has its All Souls' Mass); the former church at 150 Broad St. stays in open/.
  No rows for the Mercy Hospital chapel (South Buffalo; chaplaincy Masses in the intentions only)
  or the CCBN Central Office Chapel (16 Peter St., on Assumption's parcel; its weekday Mass moved
  to St. Margaret on 12 October); both explained in their parish records. Promoted. Coverage:
  directory 167/167; families 146/151; mass-times 141/145; GCatholic 174/216.
- 2026-11-16: Phase 1 of a check against the diocese's own lists (parish finder and weekend
  Mass-times pages, re-read 2026-11-14; the finder is unchanged since 26 September, and the
  Mass-times pages differ only in Olean's 7:30 a.m. Sunday Mass and a second spelling of Holy
  Family, Niagara Falls). St. Ambrose, Buffalo closed: the South Buffalo bulletin of 18 October
  announced "Final Mass at St. Ambrose, November 1", and from 8 November the masthead lists only
  Holy Family and St. Martin of Tours. It is excluded as closed (`last_mass` 2026-11-01) and
  removed from the live CSVs; the diocese's finder and Mass-times pages still list it. Our Lady
  of Bistrica: the diocesan pages still give three weekend Masses, but the 15 November bulletin
  says weekend Masses ended and two Tuesday 6:30 p.m. Masses a month remain, as the live schedule
  already shows; evidence added, no schedule change. SS. Columba-Brigid and St. Anthony of Padua
  ran one or two issues behind on the site: fetch-check picks each page's newest issue, and the
  parishes post after the weekly fetch, so neither is a fetch gap (noted on both records).
  Promoted. Coverage: directory 167/167; families 146/151; mass-times 141/145; GCatholic 174/216.
- 2026-11-16: Phase 2 of the check against the diocese's weekend Mass-times pages (re-read
  2026-11-16; only the Sunday-afternoon page changed since 14 November, adding St. John the Baptist,
  Lockport's third-Sunday 12:30 p.m. Spanish Mass). Combining the diocese's rows per church, 96 of
  131 live churches matched the live snapshot's Saturday-evening and Sunday Masses and 35 differed.
  Every difference was checked against the newest bulletin (15 or 22 November; SS. Columba-Brigid's
  newest is 7-8 November). One was the site's error: St. James Major, Westfield's Saturday 4:00 p.m.
  vigil runs every week, but the seed had dropped it on first Saturdays after reading the end of
  "First Saturday Masses" (a separate devotion; the 8 November issue lists the 4:00 p.m. Mass on 7
  November). It is fixed by the correction file
  `data/corrections/chautauqua-family-catholic/2026-11-16-westfield-first-saturday-vigil.json`. SS.
  Columba-Brigid differs only by its monthly bilingual Mass (last Sunday 10 a.m. instead of 9 and 11),
  which the site stores. The other 33 are the diocese's errors: wrong or old times, Masses moved to
  another church of the family, Masses it leaves out, and Greater East Buffalo's new schedule from 21
  November. Our Lady of Bistrica was recorded in phase 1. The other 32, and SS. Columba-Brigid, now
  carry the 16 November bulletin evidence (quoted, or transcribed where the page is only an image) and a
  "Diocesan Mass-times pages" section; the seasonal vigils at All Saints and St. John the Baptist,
  Lockport (January-June and July-December) and St. Joseph University's school-year 7 p.m. Mass are
  noted there. After the fix, 97 of 131 match. No church or parish rows changed (promote: no changes);
  coverage unchanged.
- 2026-11-16: Phase 3, closing coverage gaps (sources read 16 November 2026).
  - The seven open/ churches: six closed on stated sources and one more on Wikipedia.
    St. James / St. Mother Teresa, Depew: last Mass 8 June 2025 (Beloved Disciples bulletin).
    St. Francis of Assisi, Tonawanda: 27 April 2025 (Tonawandas bulletin; the 71 Adam St. chapel
    stays a church). Divine Mercy, Niagara Falls: "now closed" on its own archived site by
    4 April 2025. Sacred Heart, Portville: final Mass summer 2025 (Olean Times Herald).
    St. Joseph, Lockport and Our Lady of the Snows, Panama: bishop's decrees reducing them to
    profane use, effective 2 June 2025 and 24 March 2025. Cassadaga: Wikipedia says closed in 2014
    (uncited); everything else agrees.
  - GCatholic's 42 unaccounted entries: 7 Eastern Catholic churches excluded as
    `other-jurisdiction`; 31 excluded as closed, each dated from a bulletin, a decree, the news,
    GCatholic or Wikipedia (2024-25 closings from bulletins where found: Bolivar, Andover,
    Blasdell, Lackawanna St. Anthony, OLMC Niagara Falls, St. Augustine Clarence Center); the
    Dominican nuns' monastery (moved to Ohio in 2020) and the Christ the King Seminary chapel
    (sold 2025) among them; the St. John Neumann Shrine, Kenmore excluded as `no-public-mass`
    (adoration only); Coronation, Buffalo and the Infant Jesus Shrine in open/.
  - Owner's rule (Rules, above): Holy Family (Sanborn) reopened from `excluded/` to `open/`; new
    open/ records for the Niagara University, Canisius and St. Bonaventure chapels and
    Mt. Irenaeus, each with its published Mass times; Our Lady of Hope's row records its
    published times (its site was still behind Cloudflare; ParishesOnline and Discover Mass have
    no bulletin).
  - Linked two naming artefacts: Holy Family of Jesus, Mary and Joseph (families, Mass-times) to
    St. Joseph, Niagara Falls, and Mass-times "Our Lady the Lake" to St. Patrick, Barker. Still
    unmatched: canonical parish names spread over several buildings (Our Lady of Charity,
    St. Vincent de Paul NF, St. John Neumann Strykersville, the Campus Ministry family entry).
  - No schedules changed. Coverage (accounted for): directory 167/167; families 146/151 ->
    147/151; mass-times 141/145 -> 143/145; GCatholic 174/216 -> 216/216.
- 2026-11-17: Phase 3 review fixes.
  - St. Jude the Apostle, North Tonawanda checked, because its bulletin announced a final Mass on
    4 May 2025: regular Masses did end then, the merger was appealed to Rome (October 2025), and from
    the 28 June 2026 bulletin a First Sunday 5:00 p.m. and First Friday 12:00 p.m. Mass are scheduled
    there again. The 22 November 2026 bulletin still prints both, so the church and its live schedule
    stand; its record now gives the history.
  - Wikipedia's Buffalo former-churches table gives the year a parish ended ("Parish defunct"), not
    the year of the last Mass. `last_mass` is kept only where another row dates the end of worship
    (St. Francis Xavier 2007, St. Clare 2016) and removed for St. Agatha and Immaculate Heart of Mary.
- 2026-11-24: Source schedules for three places with published Mass and no bulletin (the owner's
  rule of 16 November). Each open/ record became a `website_schedule` parish row and a church, with
  a source seed drafted from captures of its own pages (`data/seeds/<slug>.json`, captures in
  `data/seeds/captures/<slug>/`); the seeds await review in the labeler.
  - Mt. Irenaeus (`mt-irenaeus-friendship`): Sunday 11 a.m. Mass in Holy Peace Chapel, from its
    site's Mass event (listed for 22 November 2026) and Visit Us page.
  - Christ the King Chapel, Canisius (`canisius-christ-the-king-chapel`): the chapel page's
    schedule and its 2026-27 calendar (to 1 January 2027), with the Sunday 9:30 a.m. from the
    Campus Ministry page. The summer Sunday-morning Mass at Riverfest Park isn't a church.
  - University Chapel, St. Bonaventure (`st-bonaventure-university-chapel`): Sunday 11 a.m. and
    7 p.m. in Doyle Hall. The weekday Mass (McGinley-Carney Center's Great Room) and Friday
    confession (Interfaith Prayer Tower) are in other rooms and left out; rechecked by 15 April
    2027, before a summer schedule could apply.
  - Coordinates from OSM buildings for all three; addresses are the places' own.
  - Not moved, with this pass's findings on each record: Our Lady of Hope (its site still behind
    Cloudflare; its own page, saved by the Wayback Machine in October 2025, and the diocese's
    September 2025 directory agree on Saturday 4, Sunday 9 and 11), Holy Family, Sanborn (its
    times are published only by the diocese, which a source schedule can't cite), Niagara
    University's chapel (one undated page, which disagrees with the catalog on a Sunday 7 p.m.),
    the Infant Jesus Shrine (the September 2025 directory matches Discover Mass's times, but it has
    no site of its own that loads) and Coronation (no published Mass).
  - The diocese's weekend Mass-times pages are headed "updated as of May 5th, 2024"; its Official
    Catholic Directory (https://www.buffalodiocese.org/wp-content/uploads/DOB_CatholicDirectory.pdf)
    is dated September 2025 and gives Mass times per parish and shrine.
