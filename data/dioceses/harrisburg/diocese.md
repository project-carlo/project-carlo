---
name: Roman Catholic Diocese of Harrisburg
state: PA
website: https://www.hbgdiocese.org
status: exploring
gcatholic: harr0
---

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.
Fill this in as you find them (see data/dioceses/README.md, "Sources").

- **Parish directory (the `directory` roster):** https://www.hbgdiocese.org/parishes/
  ("Find a Parish, Church or Mass Time"), a WordPress page listing 96 entries by county, each
  linking `/parishes/<slug>/` with the address, a Google Maps embed (coordinates), weekend and
  weekday Masses, contacts and a "Website" link. Plain HTML; a browser user agent is enough
  with curl. Scraped on 2026-10-19 into `rosters/directory.json` (`mass_times` holds the
  page's text up to "Parish History"). Detail-page titles are truncated with "…", so names
  come from the list. Missions are listed as their own entries ("Mission in Benton").
  Lykens' map pin repeats New Oxford's; Sacred Heart, Lancaster and Sacred Heart, Spring
  Grove have no pin.
- **GCatholic:** `rosters/gcatholic.json` (key `harr0`), 103 entries with Plus Codes, 7 of
  them Eastern Catholic (Ukrainian, Ruthenian).
- Clusters / families of parishes:
- Mass times:
- Closed parishes and where their records went:
- Pastoral plan / closure announcements:

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-19: Initialised. Fetched GCatholic (103 entries) and scraped the diocesan parish
  finder (96 entries) as `rosters/directory.json`.
