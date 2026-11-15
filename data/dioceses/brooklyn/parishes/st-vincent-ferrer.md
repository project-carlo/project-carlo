---
name: St. Vincent Ferrer
website: https://saintvincentferrer.org/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://saintvincentferrer.org/bulletin/
publication: []
group: Deanery B11 (Brooklyn East)
evidence:
- url: https://saintvincentferrer.org/wp-content/uploads/sites/94/2026/11/nov8_2026_stvincent_compressed.pdf
  seen: 2026-11-06
  quote: 'CHURCH: 925 EAST 37TH STREET, BROOKLYN'
  note: 'Page 1 masthead of the 8 November 2026 issue (8 pages): Saint Vincent Ferrer Roman Catholic Church,
    Incorporated May 17, 1923; office 1603 Brooklyn Avenue, Brooklyn, NY 11210; Pastor Very Rev. Michael
    J.S. Bruno, S.T.D. Mass schedule (read from a page 1 render, the text layer is in a shifted font with
    digits dropped): Monday-Saturday 9:00 a.m., Saturday 5:00 p.m. Vigil, Sunday 8:00 a.m. and 11:00 a.m.,
    Holy Days 9:00 a.m. No other church or chapel is named.'
- url: https://saintvincentferrer.org/wp-content/uploads/sites/94/2026/11/nov8_2026_stvincent_compressed.pdf
  seen: 2026-11-06
  quote: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY 11704-1104
  note: 'Page 8 ad-page footer ''# 104'': printed by The Church Bulletin Inc., which has no online container.'
- url: https://saintvincentferrer.org/bulletin/
  seen: 2026-11-06
  note: 'Diocesan WordPress multisite (sites/94) bulletin page, read with parish-site-access visit.py
    (probe url gets RemoteDisconnected): links nov8_2026_stvincent_compressed.pdf, then nov1, oct25, oct18,
    oct11, oct4, sept27, sept20 2026 issues.'
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://saintvincentferrer.org/bulletin/
  url: https://saintvincentferrer.org/bulletin/
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

St. Vincent Ferrer publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "# 104") and posted as PDFs on the parish's page of the diocesan WordPress multisite. The 8 November 2026 issue (read 2026-11-06, 8 pages) has the masthead "Saint Vincent Ferrer Roman Catholic Church, Incorporated May 17, 1923", church 925 East 37th Street, office 1603 Brooklyn Avenue, Brooklyn, NY 11210, with Very Rev. Michael J.S. Bruno, S.T.D., Pastor. Much of page 1's text layer is in a shifted font with digits dropped, so the staff and Mass schedule were read from a render of page 1.

## Worship sites

One. The page 1 Mass schedule lists Monday-Saturday 9:00 a.m., Saturday 5:00 p.m. Vigil Mass, Sunday 8:00 a.m. and 11:00 a.m., Holy Days 9:00 a.m., with no other church or chapel. The directory, the deanery list, GCatholic 16790 and Mass finder 1170 all give the one church (GCatholic at the office address, 1603 Brooklyn Ave).

## Website and bulletin provider

`other`, recipe `page-pdfs https://saintvincentferrer.org/bulletin/`. The site is on the diocesan multisite, which drops `probe url` connections; `visit.py` and fetch read it. There is no publication id: The Church Bulletin Inc. has no online container. Because of the shifted font, fetch may not read the issue date from the masthead; the file names carry it (nov8_2026_...).

## Not yet confirmed

Nothing outstanding.
