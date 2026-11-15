---
name: Our Lady of Mercy (Forest Hills)
website: https://mercyhills.org/important-information/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://mercyhills.org/important-information/bulletin/
publication: []
group: Deanery Q6 (Queens West)
evidence:
- url: http://mercyhills.org/wp-content/uploads/sites/75/2026/10/nov1_2026_mercyhills_compressed-1.pdf
  seen: 2026-11-06
  quote: 'Sunday: 8:30 A.M., 10:00 A.M., 12:00 P.M.'
  note: '1 November 2026 issue (8 pages, text). Page 1 masthead names Our Lady of Mercy, 70-01 Kessel
    Street, Forest Hills, NY 11375, Rev. Frank Schwarz, Pastor, dated ''Sunday, November 1, 2026''; Sunday
    Masses Saturday 4:00 PM and Sunday 8:30, 10:00, 12:00; weekdays Monday to Saturday 9:00 A.M. Ad-page
    footer ''#150 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY''. Downloaded
    with tools/fetch-pdf.py (probe pdf is refused by this host).'
- url: https://mercyhills.org/important-information/bulletin/
  seen: 2026-11-06
  note: 'WordPress multisite page (uploads under /wp-content/uploads/sites/75/); probe url gets RemoteDisconnected,
    visit.py loads it. PDFs newest first: nov1_2026_mercyhills_compressed-1.pdf, MercyFH10-25.pdf, oct18_2026_mercyhills_compressed.pdf,
    oct11_..., Oct4_..., sept27_... weekly.'
- url: https://parishesonline.com/organization/our-lady-of-mercy-church-11375
  seen: 2026-11-06
  note: 'probe po: ParishesOnline org ''Our Lady of Mercy Church'' (lpi 0018000000QxB9dAAF) has no publications;
    an empty org, not this bulletin''s id.'
promoted: 2026-11-12
research:
- method: fetch:check page-pdfs on the bulletin page
  url: https://mercyhills.org/important-information/bulletin/
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks the 8 November 2026 issue, whatever its file name
  retry_when: After the 8 November 2026 issue is posted
  revisit_after: 2026-11-09
bulletin_status: available
---

## Publisher

Our Lady of Mercy publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "#150 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST."), and posts it on its own site's bulletin page. I read the 1 November 2026 issue (read 2026-11-06): page 1 has the masthead "Our Lady of Mercy / 70-01 Kessel Street, Forest Hills, NY 11375", Rev. Frank Schwarz, Pastor, and the date "Sunday, November 1, 2026". The Church Bulletin Inc. has no online container. ParishesOnline holds an org `our-lady-of-mercy-church-11375` with no issues: an empty org, so no publication id is recorded from it.

## Worship sites

One church. The page 1 schedule gives "Saturday: 4:00 PM / Sunday: 8:30 A.M., 10:00 A.M., 12:00 P.M." and weekday Masses "Monday to Saturday: 9:00 A.M.", naming no other place. Our Lady of Mercy Catholic Academy (70-25 Kessel St.) is a school. The diocese directory, the deanery list (Q6), GCatholic 16639 and Mass finder 1134 list this one church.

## Website and bulletin provider

`other`, reading the parish's WordPress multisite bulletin page with `page-pdfs https://mercyhills.org/important-information/bulletin/`. File names vary from week to week (`nov1_2026_mercyhills_compressed-1.pdf`, `MercyFH10-25.pdf`), so no filename filter is set. `fetch:check` (2026-11-06, a Friday) resolved "page-pdfs on https://mercyhills.org/important-information/bulletin/: current" and picked `nov1_2026_mercyhills_compressed-1.pdf`, the 1 November 2026 issue and the newest on the page that day; freshness reads `unknown` because the date comes from no file-name pattern it knows. That is the recipe recorded.

## Not yet confirmed

Whether the pick moves to the 8 November issue once it is posted: see `research` (recheck after the weekend).
