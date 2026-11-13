---
name: St. Martin de Porres (Bedford-Stuyvesant)
website: https://stmartindeporresparish.org/
bulletin_provider: other
provider_id: page-pdfs https://stmartindeporresparish.org/resources/bulletins/
publication: []
group: Deanery B5 (Brooklyn East)
evidence:
- url: https://stmartindeporresparish.org/wp-content/uploads/sites/14/2026/11/nov8_2026_stmartin_compressed.pdf
  seen: 2026-11-07
  note: '8 November 2026 issue, 8 pages, image-only (no text layer; read by rendering pages 1, 2 and 8),
    self-made (no LPi, John Patrick or Church Bulletin Inc. footer; page 8 is local ads and the parish''s
    own hall photos). Page 1 masthead ''Saint Martin de Porres Parish'', 583 Throop Ave, Brooklyn, NY
    11216, Rev. Alonzo Q. Cox, Pastor; mission statement: ''formed from the tri-church unity of Holy Rosary,
    Our Lady of Victory and St. Peter Claver churches''. Mass Times box: Holy Rosary Church, 139 Chauncey
    Street, Brooklyn NY 11233, Sundays 9am / Tuesdays 11am; Our Lady of Victory Church, 583 Throop Avenue,
    Brooklyn NY 11216, Sundays 7:30am & 10:15am, Monday-Friday 8am - 9am; St. Peter Claver Church, 29
    Claver Place, Brooklyn NY 11238, Sat. 5pm / Sun. 11:30am, Monday & Wednesday 12noon, 1st Fridays 12noon.'
- url: https://stmartindeporresparish.org/resources/bulletins/
  seen: 2026-11-07
  note: 'Bulletins page on the diocesan WordPress multisite (uploads/sites/14), read with visit.py (probe
    url gets RemoteDisconnected). Newest first: nov8_2026_stmartin_compressed.pdf (uploaded 2026/11),
    nov1_2026, oct25_2026, oct18_2026, oct11_2026, oct4_2026, sept27_2026 ..., weekly.'
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://stmartindeporresparish.org/resources/bulletins/
  url: https://stmartindeporresparish.org/resources/bulletins/
  checked: '2026-11-07'
  outcome: found
bulletin_status: available
publication_reviews:
- parish: st-martin-of-tours-bushwick
  decision: separate
  evidence:
  - url: https://stmartindeporresparish.org/wp-content/uploads/sites/14/2026/11/nov8_2026_stmartin_compressed.pdf
    seen: 2026-11-07
    note: The 8 November 2026 masthead (page 1, rendered) names Saint Martin de Porres Parish, 583 Throop
      Ave, Rev. Alonzo Q. Cox, Pastor, with its own Mass times at Holy Rosary, Our Lady of Victory and
      St. Peter Claver.
  - url: https://stmartinoftours-brooklyn.org/system/resources/W1siZiIsIjIwMjYvMTEvMTIvNXN2MHFhdGdyXzExXzE1XzIwMjYucGRmIl1d/11-15-2026.pdf
    seen: 2026-11-12
    quote: SAINT MARTIN OF TOURS PARISH - R.C.C.
    note: The 15 November 2026 masthead names Saint Martin of Tours Parish, rectory 1288 Hancock Street,
      Rev. Juan D. Ruiz, Pastor, with its own Mass times (Saturday 6:30 PM, Sunday 9:00 AM, 10:30 AM,
      12:00 PM).
---

## Publisher

St. Martin de Porres Parish publishes one weekly bulletin, a self-made 8-page PDF of scanned pages (no text layer; no LPi, John Patrick or Church Bulletin Inc. footer). It is posted on the parish's site on the diocesan WordPress multisite. I read the 8 November 2026 issue (2026-11-07) by rendering pages 1, 2 and 8. The page 1 masthead reads "Saint Martin de Porres Parish", 583 Throop Ave, Brooklyn, NY 11216, with Rev. Alonzo Q. Cox, Pastor. The mission statement describes the parish as "formed from the tri-church unity of Holy Rosary, Our Lady of Victory and St. Peter Claver churches".

## Worship sites

Three. The page 1 "Mass Times" box lists:

- Holy Rosary Church, 139 Chauncey Street: Sundays 9am, Tuesdays 11am.
- Our Lady of Victory Church, 583 Throop Avenue: Sundays 7:30am and 10:15am, Monday-Friday 8am - 9am, and the first-Friday Rosary for Life "In St. Anthony's Chapel". The chapel is a devotion space, not a separate site.
- St. Peter Claver Church, 29 Claver Place: Saturday 5pm, Sunday 11:30am, Monday and Wednesday 12noon, first Fridays 12noon.

All three are in one bulletin, so the parish is one row with three churches. GCatholic files the three churches under "St. Martin of Tours Parish", which I take for its error: St. Martin of Tours is a Bushwick parish. The Mass finder's place 1152 ("St. Martin de Porres (Our Lady of Victory)") lists "Our Lady of Victory, 2 Floral Parkway, Floral Park" and is pinned there. That is Our Lady of Victory, Floral Park, in the Diocese of Rockville Centre, which has its own `excluded/` record carrying that roster entry under the settled pin rule.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stmartindeporresparish.org/resources/bulletins/`, newest first, with files named `<mon><d>_<yyyy>_stmartin_compressed.pdf` (some vary: `oct4_2026_stmartindepaures_compressed.pdf`, `aug23_20026_stmartinbll_compressed.pdf`). The issues are images, so the pipeline has to read them as images. There is no publication id: self-made, with no online container.

## Not yet confirmed

Nothing for the row.
