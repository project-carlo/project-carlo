---
name: Divine Mercy
website: https://divinemercy-brooklyn.org/
bulletin_provider: other
provider_id: page-pdfs https://divinemercy-brooklyn.org/bulletins
publication: ['url:https://divinemercy-brooklyn.org/bulletins']
group: Deanery B1 (Brooklyn West)
evidence:
- url: https://divinemercy-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTEvMDQvNjQ3N3Q3b2JtOF9Ob3ZlbWJlcl84XzIwMjZfYnVsbGV0aW4ucGRmIl1d/November%208%202026%20bulletin.pdf
  seen: 2026-11-07
  quote: 219 CONSELYEA STREET, BROOKLYN NY 11211
  note: '8 November 2026 bulletin (5 pages), page 1 masthead names DIVINE MERCY PARISH, BROOKLYN NEW YORK,
    with three church columns: ST. NICHOLAS, 26 OLIVE STREET (Sunday 10:45AM Misa en Espanol, Wednesday
    6:30PM); ST. CECILIA, 84 HERBERT STREET (Sunday 9:30AM English Mass, Monday 11:30AM English Mass,
    St. Cecilia Chapel (Herbert St)); ST. FRANCIS, 219 CONSELYEA STREET (Saturday 5PM, Sunday 12PM, Monday-Friday
    9AM). Rev. Mike Vricella, Administrator. No LPi, John Patrick or Church Bulletin Inc. footer; self-made.'
- url: https://divinemercy-brooklyn.org/bulletins
  seen: 2026-11-07
  quote: November 08, 2026
  note: 'Tilma /bulletins cards newest first, weekly: November 08, November 01, October 25, October 18,
    October 11, October 04, 2026.'
- url: https://mass.dioceseofbrooklyn.org/places/291
  seen: 2026-11-07
  note: Mass finder place 291 Divine Mercy Parish lists All Worship Sites St. Francis of Paola (219 Conselyea
    Street), St. Nicholas (26 Olive Street), St. Cecilia (84 Herbert Street); used only as a lead for
    places.
promoted: 2026-11-12
research:
- method: pnpm fetch:check with page-pdfs https://divinemercy-brooklyn.org/bulletins
  url: https://divinemercy-brooklyn.org/bulletins
  checked: '2026-11-07'
  outcome: found
  next_action: If fetch returns an issue more than two weeks old, read the /bulletins cards; the parish
    has posted weekly.
  revisit_after: 2027-02-01
bulletin_status: available
---

## Publisher

Divine Mercy Parish (the 2011 merger of St. Francis of Paola, St. Nicholas and St. Cecilia) publishes its own weekly bilingual bulletin as a PDF on its Tilma site, https://divinemercy-brooklyn.org/bulletins. The 8 November 2026 issue (5 pages, read 2026-11-07) has the page 1 masthead "DIVINE MERCY PARISH, BROOKLYN NEW YORK", the parish office at "219 CONSELYEA STREET, BROOKLYN NY 11211", 718-387-0256, and Rev. Mike Vricella, Administrator. No LPi, John Patrick or Church Bulletin Inc. footer: the parish makes it itself (staff list: "Carina Sciangula, Social Media/Bulletin").

## Worship sites

Three churches, each a column of the page 1 schedule:

- St. Nicholas, 26 Olive Street: Sunday 10:45AM Misa en Español, Wednesday 6:30PM Misa en Español.
- St. Cecilia, 84 Herbert Street: Sunday 9:30AM English Mass, Monday 11:30AM English Mass ("ST. CECILIA CHAPEL (HERBERT ST)").
- St. Francis (of Paola), 219 Conselyea Street: Saturday 5PM, Sunday 12PM, Monday-Friday 9AM English Mass.

The same issue announces events after "the 10:45am Mass" at St. Nicholas (15 November) and the St. Cecilia feast after "the 9:30am" (22 November). The directory and deanery list give only the parish at 219 Conselyea Street; GCatholic lists all three as churches (16711, 16759, 16695) and the Mass finder (291) lists the same three worship sites.

## Website and bulletin provider

`other` with the recipe `page-pdfs https://divinemercy-brooklyn.org/bulletins`. The cards are weekly (8 Nov, 1 Nov, 25 Oct, 18 Oct, 11 Oct, 4 Oct 2026). `fetch:check` on 2026-11-07 resolved "page-pdfs on https://divinemercy-brooklyn.org/bulletins: first-listed" and downloaded the 8 November 2026 issue (dated from the file name; the resource token decodes to an upload of 2026/11/04).

## Not yet confirmed

Whether the Monday 11:30AM St. Cecilia Mass is in the church or a chapel in the building is not said beyond "ST. CECILIA CHAPEL (HERBERT ST)"; either way it is the 84 Herbert Street site, which also has the Sunday 9:30AM Mass.
