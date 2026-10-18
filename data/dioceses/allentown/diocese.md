---
name: Roman Catholic Diocese of Allentown
state: PA
website: https://www.allentowndiocese.org
status: exploring
gcatholic: alle0
---

Five counties of eastern Pennsylvania: Lehigh (Allentown), Northampton (Bethlehem, Easton),
Berks (Reading), Carbon and Schuylkill (Pottsville and the coal region). It borders
Scranton to the north. Many coal-region parishes were consolidated in 2008, so several now
have more than one worship site, and some directory entries are worship sites of another
parish ("... Worship Site for ... Parish").

## Sources

- **Parish map (the `directory` roster):** https://www.allentowndiocese.org/maps/parishes,
  the same "places" platform as the Archdiocese of New York's directory. Plain HTML, no
  Cloudflare. 87 entries, each with `data-lat`/`data-lng` and a `/places/<slug>` page giving
  the address, phone, website, pastor and weekend Masses. Scraped with `curl` on
  2026-10-18 into `rosters/directory.json` (`mass_times` holds the page's text). Mixes
  parishes and worship sites; eleven free-form addresses were normalised by hand.
- **GCatholic:** `rosters/gcatholic.json` (key `alle0`), 130 entries with Plus Codes, 26 of
  them Eastern Catholic (marked `rite`: Ruthenian, Ukrainian, Maronite, Syriac). Keeps
  churches closed in the 2008 consolidations.
- Clusters / families of parishes:
- Mass times: each `/places/` page lists weekend Masses; there is no separate diocese-wide
  Mass-times page.
- Closed parishes and where their records went:
- Pastoral plan / closure announcements:

## Rules settled for this diocese

- **Eastern Catholic churches** (Ruthenian: Archeparchy of Pittsburgh / Eparchy of Passaic;
  Ukrainian: Archeparchy of Philadelphia; Maronite; Syriac) are excluded as
  `other-jurisdiction`, as in Scranton, Syracuse and Rochester.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-18: Initialised. Fetched GCatholic (130 entries) and scraped the diocesan parish
  map (87 entries) as `rosters/directory.json`.
