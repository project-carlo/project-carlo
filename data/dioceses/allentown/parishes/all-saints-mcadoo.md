---
name: All Saints Parish
website: https://sites.google.com/view/asphome/2026-bulletins
bulletin_provider: other
provider_id: page-pdfs https://sites.google.com/view/asphome/2026-bulletins
publication:
- url:https://sites.google.com/view/asphome/2026-bulletins
group: All Saints Parish
evidence:
- url: https://drive.google.com/uc?export=download&id=1HoghqYb35YkcCXkfEF7b2N7bcZxOKHOs
  seen: 2026-10-18
  quote: All Saints Church 21 North Cleveland St. McAdoo, PA 18237
  note: Page 1 masthead of the 18 October 2026 issue (Google Drive file 1HoghqYb35YkcCXkfEF7b2N7bcZxOKHOs,
    linked as "10/18-29th Sunday in Ordinary Time" on the 2026 Bulletins page). The masthead names both
    churches.
- url: https://drive.google.com/uc?export=download&id=1HoghqYb35YkcCXkfEF7b2N7bcZxOKHOs
  seen: 2026-10-18
  quote: Weekend Mass (All Saints Church) Saturday … 4:00 PM Sunday … 8:00 AM (Our Lady of Lourdes Church)
    Sunday … 10:30 AM
  note: Page 1 "MASS SCHEDULE" of the same issue. Daily Mass is at All Saints only.
- url: https://drive.google.com/uc?export=download&id=1HoghqYb35YkcCXkfEF7b2N7bcZxOKHOs
  seen: 2026-10-18
  quote: 'Our Lady of Lourdes Church 318 Plane St. Weatherly, PA 18255 All Saints Parish Pastor: Rev.
    Barnabas Shayo A.J.'
- url: https://sites.google.com/view/asphome/2026-bulletins
  seen: 2026-10-18
  quote: 10/18-29th Sunday in Ordinary Time
  note: 'The parish site''s "2026 Bulletins" page: one Google Drive file link per Sunday, grouped by month,
    newest month first (10/4, 10/11, 10/18 were posted on 18 October; 10/25 is listed with no link yet).'
- url: http://churchofallsaintsparish.org
  seen: 2026-10-18
  note: 'The domain printed in the bulletin ("Website: churchofallsaintsparish.org") answers http with
    a 301 to https://sites.google.com/view/asphome/home; its https certificate fails verification from
    the sandbox.'
revisit: In January 2027, check that the bulletins page is still https://sites.google.com/view/asphome/2026-bulletins
  (the 2025 archive moved under it as /2026-bulletins/2025-bulletins); if the parish starts a new yearly
  page, update website and the provider_id recipe.
revisit_after: 2027-01-15
---

## Publisher

All Saints Parish, McAdoo publishes one weekly bulletin for its two churches. The 18 October
2026 issue (Volume #20, Issue #42, a Google Drive PDF linked from the parish's Google Sites
"2026 Bulletins" page) has a page 1 masthead naming "All Saints Church, 21 North Cleveland St.,
McAdoo" and "Our Lady of Lourdes Church, 318 Plane St., Weatherly", and one Mass schedule:
All Saints Saturday 4 pm and Sunday 8 am (and every weekday Mass), Our Lady of Lourdes Sunday
10:30 am. Page 3's Mass intentions mark each Mass "All Saints" or "Our Lady Of Lourdes".
The diocese's parish map lists the parish and "Our Lady of Lourdes Church Worship Site for
All Saints Parish" with the same Masses.

## Worship sites

- `all-saints-mcadoo` (21 N. Cleveland St., McAdoo).
- `our-lady-of-lourdes-weatherly` (318 Plane St., Weatherly, Carbon County). The parish map
  says "All Saints is the repository for records of Our Lady of Lourdes, Weatherly": the
  Weatherly parish was merged into All Saints but its church is still a worship site.

No other building is named in the bulletin. GCatholic's two Eastern Catholic churches in
McAdoo (St. Michael, Ruthenian; Patronage of the Mother of God, Ukrainian) are separate
jurisdictions (`excluded/`). The bulletin's candle list names former McAdoo parishes
(St. Bartholomew, Sts. Cyril & Methodius, St. Kunegunda & St. Stephen, St. Patrick) as shrines
inside All Saints Church, not as buildings; no roster lists them.

## Website and bulletin provider

`other`. The bulletins are Google Drive files (one `drive.google.com/file/d/<id>/view` link
per Sunday) listed on https://sites.google.com/view/asphome/2026-bulletins, so the row reads
that page directly (the resolver takes Drive file links as PDFs). The diocese's map gives the
site's home page; the bulletin's own "churchofallsaintsparish.org" redirects there.
`fetch_check_rows.py` on 2026-10-18 picked the 18 October file ("page-pdfs on
https://sites.google.com/view/asphome/2026-bulletins: current"), which is this week's issue,
so its recipe is pinned as `provider_id`. The issue is a text PDF.

## Not yet confirmed

Whether the bulletins page keeps its address in 2027 (see `revisit`).
