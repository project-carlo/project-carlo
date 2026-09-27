---
name: Archdiocese of New York
state: NY
website: https://www.archny.org
status: promoted
gcatholic: newy0
city_aliases:
  Southeast: Brewster
  Town of Southeast: Brewster
promoted: 2026-09-26
---

Opened for one requested parish, not as a survey of the archdiocese. `status: promoted`
means the records that exist have been written into the live CSVs. It does not mean the
archdiocese has been explored.

## Sources

- **Parish directory:** https://www.archny.org/places/ has a page per worship site (St. Lawrence
  O'Toole is https://www.archny.org/places/slot-sh-lawrence-o-toole). It gives a street address,
  a Mass schedule, and the parish homepage. For this parish it names the city as "Town of
  Southeast" rather than the postal city Brewster. Not imported; only this parish's page was
  read.
- **GCatholic:** key `newy0` (https://gcatholic.org/dioceses/diocese/newy0). The roster was not
  fetched. The two churches added here were read from their own pages, which give a street
  address and a Plus Code on the building. Church ids: St. Lawrence O'Toole 16352, Sacred
  Heart Patterson 16353.
- **Clusters / families of parishes:** not looked for. This parish's own bulletin is what
  decided the row.
- **Mass times:** the archdiocese place page above, and the parish bulletin. No diocesan
  Mass-times index was read.
- **Closed parishes and where their records went:** not looked for.
- **Pastoral plan / closure announcements:** not looked for.

## Rules settled for this diocese

Brewster is the village and the postal city; it sits in the Town of Southeast. Store Brewster.
The archdiocese's "Town of Southeast" is the same place, recorded in `city_aliases`.

A requested parish is added on its own. Do not treat that as a reason to survey the rest of
the archdiocese in the same change.

## Log

- 2026-09-26: Added St. Lawrence O'Toole and Sacred Heart (Brewster and Patterson) because the
  parish was requested. One bulletin, two churches, read from the 27 September 2026 issue.
  The GCatholic roster was not fetched, so there is no coverage number.
