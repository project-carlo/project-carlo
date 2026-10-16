---
name: Roman Catholic Diocese of Scranton
state: PA
website: https://www.dioceseofscranton.org
status: exploring
gcatholic: scra0
---

Eleven counties of northeastern Pennsylvania: Lackawanna (Scranton), Luzerne (Wilkes-Barre,
Hazleton, Pittston, Nanticoke), Wayne, Pike, Monroe, Susquehanna, Wyoming, Bradford, Tioga,
Sullivan and Lycoming (Williamsport). The diocese reorganised its parishes in 2008–2010
("Called to Holiness and Mission"), so most canonical parishes today carry new names and
several worship sites.

## Sources

- **Parish directory (the `directory` roster):** https://www.dioceseofscranton.org/find-a-parish/
  lists 98 canonical parishes ("98 Parishes Found"). Each parish's detail page
  (`/find-a-parish/<slug>`) has a *Worship Sites* section with every church's name, address
  and Mass times. `rosters/directory.json` is those worship sites (137 entries, one per site,
  `group` = the parish, `mass_times` = the page's text for that site), scraped with plain
  `curl` on 2026-10-16 (no Cloudflare). No per-site coordinates. Websites are the finder's,
  unchecked. A site listed with no Mass times may be a church kept for funerals and weddings
  only (St. Clare, Scranton: "Available for Funerals, Baptisms & Weddings").
- **GCatholic:** `rosters/gcatholic.json` (key `scra0`), 193 entries with Plus Codes. 31 are
  Eastern Catholic (marked `rite`: Ruthenian, Ukrainian, Maronite, Melkite). Its list
  includes churches closed in the 2008–2010 consolidation; `group` is GCatholic's canonical
  parish when it differs from the church.
- **Mass times:** https://www.dioceseofscranton.org/find-a-mass/ (not yet read).
- **The Catholic Light** (the diocesan paper, on dioceseofscranton.org news) reports
  closures, mergers and church sales.
- Clusters / families of parishes: the diocese does not run a family system; the finder's
  canonical parish is the grouping (`group`).

## Rules settled for this diocese

- **Eastern Catholic churches** in GCatholic's list are excluded as `other-jurisdiction`
  (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Maronite: Eparchy
  of Our Lady of Lebanon; Melkite: Eparchy of Newton), as in Syracuse.
- **`group` is the finder's canonical parish name.** Where a pastor serves two canonical
  parishes, record the shared bulletin (or separate ones) with the evidence; shared pastors
  don't make shared bulletins.
- **A worship site the diocese lists only for funerals, baptisms and weddings** has no public
  Mass and is excluded as `no-public-mass` unless its parish's current bulletin shows a
  public Mass there.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-16: Initialised. Fetched GCatholic (193 entries) and scraped the diocesan finder's
  worship sites (137 entries from 98 parishes) as `rosters/directory.json`.
