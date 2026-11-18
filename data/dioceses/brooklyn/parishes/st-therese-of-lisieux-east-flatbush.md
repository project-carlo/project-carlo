---
name: St. Therese of Lisieux (East Flatbush)
website: https://stthereseoflisieuxchurch.org/
bulletin_provider: other
provider_id: page-pdfs https://stthereseoflisieuxchurch.org/weekly-bulletin/ filename=*compressed*.pdf
publication: []
group: Deanery B7 (Brooklyn East)
evidence:
- url: http://stthereseoflisieuxchurch.org/wp-content/uploads/sites/81/2026/11/nov8_2026_sttherese_compressed.pdf
  seen: 2026-11-06
  quote: 4402 Avenue D
  note: '8 November 2026 issue (Thirty-Second Sunday in Ordinary Time), 8 pages, downloaded with tools/fetch-pdf.py.
    Page 1 masthead: Church Address 4402 Avenue D, Brooklyn, N.Y. 11203; Rectory 824 East 45th Street;
    Rev. Liju Augustine, Pastor & DRE; Mass schedule Monday-Friday 9AM, Saturday 12PM and 5PM Vigil, Sunday
    9AM and 11AM (English), 1PM (Creole). No other church or chapel is named.'
- url: http://stthereseoflisieuxchurch.org/wp-content/uploads/sites/81/2026/11/nov8_2026_sttherese_compressed.pdf
  seen: 2026-11-06
  quote: 'FOR ADVERTISING: THE CHURCH BULLETIN INC. 200 DALE ST. W. BABYLON NY 11704-1104'
  note: 'Ad-page footer ''#162'': printed by The Church Bulletin Inc.; no ParishesOnline container.'
- url: https://stthereseoflisieuxchurch.org/weekly-bulletin/
  seen: 2026-11-06
  note: 'Diocesan WordPress multisite (uploads/sites/81) bulletin page, read with visit.py (probe url
    gets RemoteDisconnected): an Event Request Form PDF first, then nov8_2026_sttherese_compressed.pdf,
    nov1, oct25, oct18 ... newest first.'
- url: https://parishesonline.com/organization/st-therese-of-lisieux-church-11203
  seen: 2026-11-06
  note: 'probe po: an LPi org ''St. Therese of Lisieux Church'', 4402 Avenue D, Brooklyn, LPi id 0018000000QxB6kAAF,
    with no container and no issues; not this bulletin''s publication id.'
promoted: 2026-11-12
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs https://stthereseoflisieuxchurch.org/weekly-bulletin/
    filename=*compressed*.pdf
  url: https://stthereseoflisieuxchurch.org/weekly-bulletin/
  checked: '2026-11-06'
  outcome: found
bulletin_status: available
---

## Publisher

St. Therese of Lisieux, East Flatbush, publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "#162") and posted on the parish's diocesan-multisite WordPress site. The 8 November 2026 issue (read 2026-11-06, 8 pages) has on page 1 "Church Address 4402 Avenue D Brooklyn, N.Y. 11203", the rectory at 824 East 45th Street, and Rev. Liju Augustine, Pastor & DRE.

An LPi org exists for the parish (`st-therese-of-lisieux-church-11203`, 4402 Avenue D) with no container and no issues; it is not a publication id.

## Worship sites

One: the church at 4402 Avenue D (corner of Troy Avenue). The page 1 schedule lists Monday-Friday 9AM, Saturday 12PM and 5PM Vigil, Sunday 9AM and 11AM (English) and 1PM (Creole), with no other church or chapel. The directory, the deanery list, GCatholic 16786 and Mass finder 1167 list this one church, at 1281 Troy Avenue.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stthereseoflisieuxchurch.org/weekly-bulletin/ filename=*compressed*.pdf`. The filter keeps the resolver off the Event Request Form PDF listed above the issues; every issue so far is named `<mon><d>_<yyyy>_<parish>_compressed.pdf` (with typos such as `oct11_20026_stterese_compressed-1.pdf`). The site drops `probe url` and `probe pdf` connections; `visit.py`, `tools/fetch-pdf.py` and fetch read it. No publication id: The Church Bulletin Inc. has no online container.

## Not yet confirmed

Nothing open. If an issue is posted without `compressed` in its file name, the filter would skip it; recheck the file names if fetch picks a stale issue.
