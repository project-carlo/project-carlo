---
name: St. Thomas Aquinas, Newark
reason: closed
line1: 40 Ludlow Street
city: Newark
state: NJ
postal_code: '07114'
decided: 2026-11-04
roster: ['directory:137', 'gcatholic:18514']
evidence:
- url: https://rcan.org/sacramental-records/
  seen: 2026-11-04
  quote: Saint Thomas Aquinas
  note: 'Archdiocese''s ''Location of Records for Closed or Merged Parishes'' table (page modified 2025-05-22):
    row ''Saint Thomas Aquinas | Newark | Closed | Blessed Sacrament, Elizabeth''.'
- url: https://rcan.org/planning-area-i/
  seen: 2026-11-04
  note: The We Are His Witnesses planning areas (rcan.org/planning-area-a..k, modified 2026-01-08; transcribed
    in scratch/newark-map-1/tools/planning-areas-2026-01.tsv) list 213 parishes; none is St. Thomas Aquinas.
    Area I lists the Newark parishes (Blessed Sacrament-St. Charles ... St. Stanislaus) and area K Blessed
    Sacrament, Elizabeth; 'Aquinas' occurs on neither page.
- url: https://parishesonline.com/organization/st-thomas-aquinas-church-07114
  seen: 2026-11-04
  note: 'probe po: org ''St. Thomas Aquinas Church'', 40 Ludlow St, Newark (lpi:0018000000QxAB7AAN), ''no
    publications: this organization does not publish a bulletin here now''.'
- url: https://discovermass.com/church/st-thomas-aquinas-newark-nj/
  seen: 2026-11-04
  quote: There are currently no bulletins available for St. Thomas Aquinas.
  note: 'COVID-era page (''Mass Times during COVID-19''), Mass times Saturday 5:30pm, Sunday 9:30am, 11:00am:
    undated and stale.'
- url: https://rcan.org/parishes/
  seen: 2026-11-04
  note: The archdiocese's parish map data still carries 'St. Thomas Aquinas Parish', 40 Ludlow Street,
    Newark, NJ 07114 (id 137), with no website; GCatholic 18514 (last updated 2025-12-21) also still lists
    the church.
---

## Why it is excluded

The archdiocese's table of records for closed or merged parishes (rcan.org/sacramental-records/, modified 2025-05-22, read 2026-11-04) has the row 'Saint Thomas Aquinas | Newark | Closed | Blessed Sacrament, Elizabeth'. The archdiocese's January 2026 planning areas, which list all 213 parishes, omit it. Nothing current shows Mass at 40 Ludlow Street: the ParishesOnline org at that address publishes nothing, the Discover Mass page has no bulletins and only COVID-era times, and the 2023-2025 bulletins of Blessed Sacrament, Elizabeth (container 04/1050, monthly issues read pages 1-3) don't mention it. Wikipedia's list of the archdiocese's churches says 'closed in 2024', but its cited source (rcan.org/archives/) gives no date, so `last_mass` is empty.

The archdiocese's parish map (directory entry 137) and GCatholic (18514) still list St. Thomas Aquinas at 40 Ludlow Street. I followed the records table because it states the closure and the newer planning areas agree; the map entry carries no website or contact beyond the address, and lists of this kind keep closed parishes.

## What would change this

A current bulletin or archdiocesan page showing Mass at 40 Ludlow Street (for example a Blessed Sacrament, Elizabeth schedule naming it as a worship site). A closure date or last-Mass announcement would fill `last_mass`.
