---
name: Roman Catholic Diocese of Syracuse
state: NY
website: https://www.syracusediocese.org
status: exploring
gcatholic: syra0
---

An example of a diocese in progress: two parishes (one finished, one waiting on its bulletin),
five churches and four exclusions, measured against the GCatholic roster. It is not being
actively explored.

## Sources

- **Parish directory:** https://www.syracusediocese.org/parishes. Behind a Cloudflare
  challenge (HTTP 403 with `cf-mitigated: challenge`) for every non-browser client, so it has
  not been read or imported. It is reported to list closed parishes and where their records
  went, which would make it the closed-parish index too. Reading it in a real browser and
  importing it (`roster import`) is the first thing to do if this diocese is picked up.
- **GCatholic:** `rosters/gcatholic.json` (key `syra0`), 151 entries with addresses and Plus
  Codes. It **omits the cathedral** from its local churches list, and includes eight Eastern
  Catholic churches (marked `rite`) that belong to eparchies, not to this diocese.
- **Clusters / families of parishes:** not found yet.
- **Mass times:** not found yet.
- **Closed parishes:** see the parish directory above. The Catholic Sun (thecatholicsun.com,
  the diocesan paper) reports mergers and closures with dates.
- **Pastoral plan / closure announcements:** not found yet.

Parish sites here are a mix of LPi/ParishesOnline (the cathedral), eCatholic (All Saints) and
self-hosted. Several are behind Cloudflare challenges (holyspiritrcparish.org).

## Rules settled for this diocese

Eastern Catholic churches in GCatholic's list are excluded as `other-jurisdiction`: they are
Catholic, but belong to their eparchies. Recorded one at a time as they come up.

## Log

- 2026-09-25: Rebuilt the example in the one-file-per-record format. Fetched the GCatholic
  roster. Confirmed the cathedral's bulletin (ParishesOnline container 06/0091, weekly
  through 2026-09-27) and pinned its publication ids. Holy Spirit's bulletin could not be read
  (Cloudflare); its four churches are recorded from GCatholic, the 2020 merger report and OSM,
  with Mass not confirmed. Excluded the Syracuse University Catholic Center as `no-bulletin`
  (public Mass, nothing published) rather than as "not a parish". Coverage: 5 of 151
  GCatholic entries accounted for.
