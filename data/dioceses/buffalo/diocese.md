---
name: Roman Catholic Diocese of Buffalo
state: NY
website: https://www.buffalodiocese.org
status: promoted
gcatholic: buff0
promoted: 2026-09-26
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

## Rules settled for this diocese

- A worship site counts as a church only if a current (September 2026) bulletin or the
  community's own site shows Mass there. Where the bulletin names a site but its text does not
  tie times to it (Bread of Life, Fields of Grace), the diocesan Mass-times pages supply the times.
- The Genesee–Wyoming section of the 2024 summary is headed "Parishes/sites merged and closed"
  (past tense), but that heading also covers whole parishes whose churches still hold Mass
  (St. George, St. Brigid, Ascension). Only its entries marked "site" (Elba, East Bethany,
  Strykersville, Perry, Silver Springs, Corfu) are read as closed buildings. Each of those is also
  absent from its family's current bulletin.
- A plan plus absence from a bulletin goes in open/, not excluded/ (St. James Depew, Divine
  Mercy, St. Joseph Lockport, Panama, Cassadaga, Portville, St. Francis Tonawanda).
- Places that hold public Mass but publish no bulletin: Our Lady of Hope, St. Joseph University
  Parish and St. Andrew Kim are kept as `no_bulletin` parish rows, following Rochester's live
  `holy-apostles` row, so their churches stay on the map. Syracuse excluded a similar place
  (Alibrandi) instead. The difference is that these three were already live churches in PR 14
  and have their own church buildings in the diocesan roster. Holy Family (Sanborn) and the UB
  Newman Center, which were never church rows, stay excluded as `no-bulletin`.

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
