---
name: St. Mark-St. Margaret Mary (Sheepshead Bay)
website: https://stmarkbrooklyn.org/important-information/bulletin/
bulletin_provider: parishes_online
provider_id: st-mark-roman-catholic-church
publication: ['po-org:st-mark-roman-catholic-church', 'lpi:0018000000QxB87AAF', 'po-container:03/4066']
group: Deanery B11 (Brooklyn East)
evidence:
- url: https://container.parishesonline.com/bulletins/03/4066/20261108B.pdf
  seen: 2026-11-06
  quote: St. Mark Roman Catholic Church | 03-4066
  note: '8 November 2026 issue, 8 pages; pages 1-7 are images (read with render.py), the quote is page
    8''s LPi footer. Page 1 masthead ''The Parish of Saint Mark Saint Margaret Mary, Two Churches - One
    Community of Faith'' shows both churches with their own schedules: St. Mark Church, 2609 East 19th
    Street, Brooklyn 11235 (Saturday 5:00 p.m. Vigil, Sunday 9:00 a.m. and 12:00 p.m., weekdays 8:30 a.m.)
    and St. Margaret Mary Church, 4256 Ocean Avenue, Manhattan Beach (Sunday 10:30 a.m., Wednesday 9:30
    a.m.); Pastor Very Rev. Robert V. Macci.'
- url: https://parishesonline.com/organization/st-mark-roman-catholic-church
  seen: 2026-11-06
  note: 'probe po: org ''St. Mark Roman Catholic Church'', Ocean Ave & Avenue Z, Brooklyn 11235, lpi 0018000000QxB87AAF,
    container 03/4066, latest issue 2026-11-08.'
- url: https://parishesonline.com/organization/st-margaret-mary-church-11235
  seen: 2026-11-06
  note: 'probe po: org ''St. Margaret Mary Church'', 215 Exeter St, Brooklyn 11235, lpi 0018000000QxB86AAF,
    no publications; a leftover account of the pre-merger parish, not a publication id of this bulletin.'
- url: https://stmarkbrooklyn.org/important-information/bulletin/
  seen: 2026-11-06
  note: Diocesan WordPress multisite page (read with visit.py; probe url got RemoteDisconnected) listing
    nov8_2026_stmark2_compressed.pdf, nov1_2026_stmark_compressed.pdf, oct25_2026_stmark_compressed.pdf
    ... weekly; the 8 November file carries the same LPi footer 'St. Mark Roman Catholic Church | 03-4066'.
promoted: 2026-11-12
bulletin_status: available
---

## Publisher

The merged Parish of St. Mark-St. Margaret Mary publishes one weekly LPi bulletin, container 03/4066 (ParishesOnline org `st-mark-roman-catholic-church`), reposted on the parish's diocesan WordPress site. I read the 8 November 2026 issue (read 2026-11-06; pages 1-7 are images, drawn with render.py): page 1 masthead "The Parish of Saint Mark Saint Margaret Mary, Two Churches - One Community of Faith", Pastor Very Rev. Robert V. Macci, Parochial Vicar Fr. Michael Anyanwu; page 8 footer "St. Mark Roman Catholic Church | 03-4066".

## Worship sites

Two churches, both in the page 1 masthead with their own Mass schedules: St. Mark Church, 2609 East 19th Street (Saturday 5:00 p.m. Vigil, Sunday 9:00 a.m. and 12:00 p.m., weekdays 8:30 a.m.), and St. Margaret Mary Church, 4256 Ocean Avenue, Manhattan Beach (Sunday 10:30 a.m., Wednesday 9:30 a.m.). St. Mark Catholic Academy is a school. The directory and deanery list (B11) list the merged parish at St. Mark's address; GCatholic lists both churches (16740, 16738); the Mass finder lists the parish under St. Margaret Mary (place 1151), and no separate Mass finder place for St. Mark was found in the roster.

## Website and bulletin provider

`parishes_online`, org `st-mark-roman-catholic-church`. The directory gives `https://stmarkbrooklyn.org/`, which `probe url` could not reach (RemoteDisconnected, as the playbook notes for the diocesan multisite) but `visit.py` reads; its bulletin page reposts the LPi issues as `<mon><d>_<yyyy>_stmark_compressed.pdf`. A second ParishesOnline org, `st-margaret-mary-church-11235`, has no issues and is not recorded as a publication id. The bulletin's front pages are images: the pipeline has to read the Mass times from images. `fetch:check` (2026-11-06) resolved the ParishesOnline publication page and picked `container.parishesonline.com/bulletins/03/4066/20261108B.pdf`, the 8 November 2026 issue (freshness `future`).

## Not yet confirmed

Nothing affecting the row.
