---
name: Roman Catholic Diocese of Albany
state: NY
website: https://www.rcda.org
status: exploring
gcatholic: alba4
---

## Sources

- **Find A Parish list (the directory roster):** https://www.rcda.org/parishes/parish
  (also served at `/offices/pastoral-planning/find-parish`). Plain HTML, no Cloudflare: one
  entry per worship site or apostolate (148 on 2026-09-28), each linking a detail page
  `rcda.org/parishes/parish/<slug>` with the address, phone, "Visit Our Website" link, an
  "Other Worship Sites" box (the diocese's own grouping of sites under one parish) and
  often the Mass schedule. Scraped into `rosters/directory.json`; `notes` holds the start
  of each page's text, `other_sites` the grouping. No coordinates. The page's intro says
  "126 parishes, four apostolates, and 157 worship sites".
- **GCatholic:** `rosters/gcatholic.json` (key `alba4`), 163 entries with Plus Codes.
  Includes kinds Parish (6), Chapel (3), Mission (2), Shrine (2) and one "Former Church".
- **Institutional (sacramental) records index:** https://www.rcda.org/parishes/institutional-records,
  town by town: each closed or merged parish and the parish that now holds its records.
  Says a *corporation* ended, never that a building is shut.
- **The Evangelist** (evangelist.org), the diocesan paper: dates closures and mergers.
- **Reorganization** (rcda.org/reorganization) is the diocese's Chapter 11 bankruptcy
  (filed 15 March 2023, settlement 27 March 2026), not a parish restructuring.
- **Integrated Diocesan Map:** https://maps.topographics.org/hosted/rcda (not yet read).

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.
