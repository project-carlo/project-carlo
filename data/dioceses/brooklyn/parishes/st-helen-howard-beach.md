---
name: St. Helen (Howard Beach)
website: https://sthelen.org/important-information/bulletin/
bulletin_provider: other
provider_id: page-pdfs https://sthelen.org/important-information/bulletin/
publication: []
group: Deanery Q8 (Queens West)
evidence:
- url: https://sthelen.org/wp-content/uploads/sites/101/2026/10/nov1_2026_sthelen_compressed.pdf
  seen: 2026-11-06
  quote: 'Sunday Masses:        5:00PM Saturday; 8:00AM, 9:30AM, 11:00AM & 5:00PM'
  note: '1 November 2026 issue (8 pages, text). Page 1 masthead ''SAINT HELEN / ROMAN CATHOLIC CHURCH
    / 15710 83rd Street, Howard Beach, NY 11414'', Rev. Robert B. Adamo, KCHS, Pastor; ''Weekday Masses:
    Monday to Saturday: 9:00AM''; intentions headed ''Sunday, November 1, 2026''. Ad-page footer ''#185
    FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST., W. BABYLON, NY''. Downloaded with tools/fetch-pdf.py
    (probe pdf is refused by this host).'
- url: https://sthelen.org/important-information/bulletin/
  seen: 2026-11-06
  note: 'WordPress multisite page (uploads under /wp-content/uploads/sites/101/); probe url gets RemoteDisconnected,
    visit.py loads it. PDFs newest first: nov1_2026_sthelen_compressed.pdf, oct25_..., oct18_..., oct11_...,
    oct4_..., sept27_..., weekly back to july26_2026. The homepage carries injected Slovak and French
    betting-site text (visit.py reports SPAM-SQUAT), but the parish''s own content, address and bulletins
    are still served: a compromised page, not a squatted domain.'
- url: https://parishesonline.com/organization/st-helen-church-11414
  seen: 2026-11-06
  note: 'probe po: ParishesOnline org ''St. Helen Church'' (lpi 0018000000QxB9tAAF) has no publications;
    an empty org, not this bulletin''s id.'
research:
- method: fetch:check page-pdfs on the bulletin page
  url: https://sthelen.org/important-information/bulletin/
  checked: '2026-11-06'
  outcome: found
  next_action: Rerun fetch:check and confirm it picks the 8 November 2026 issue, whatever its file name
  retry_when: After the 8 November 2026 issue is posted
  revisit_after: 2026-11-09
bulletin_status: available
---

## Publisher

St. Helen publishes its own weekly bulletin, printed by The Church Bulletin Inc. (West Babylon; ad-page footer "#185 FOR ADVERTISING: THE CHURCH BULLETIN INC., 200 DALE ST."), and posts it on its own site's bulletin page. I read the 1 November 2026 issue (read 2026-11-06): page 1 has the masthead "SAINT HELEN / ROMAN CATHOLIC CHURCH / 15710 83rd Street, Howard Beach, NY 11414", Rev. Robert B. Adamo, KCHS, Pastor, and intentions from "Sunday, November 1, 2026". The Church Bulletin Inc. has no online container. ParishesOnline holds an org `st-helen-church-11414` with no issues: an empty org, so no publication id is recorded from it.

## Worship sites

One church. Page 1 gives "Sunday Masses: 5:00PM Saturday; 8:00AM, 9:30AM, 11:00AM & 5:00PM" and "Weekday Masses: Monday to Saturday: 9:00AM", naming no other place. St. Helen Catholic Academy is a school. The diocese directory, the deanery list (Q8), GCatholic 16719 and Mass finder 1154 list this one church.

## Website and bulletin provider

`other`, reading the parish's WordPress multisite bulletin page with `page-pdfs https://sthelen.org/important-information/bulletin/`. The homepage now carries injected betting-site text (visit.py's verdict is SPAM-SQUAT), but the domain still serves the parish's own pages and weekly bulletins, so it is the parish's site, compromised rather than lapsed. File names follow `<mon><day>_2026_sthelen_compressed.pdf` most weeks but vary (`ST-HELEN-AUGUST-23-2026.pdf`, `aug30_2026_sthelen.pdfrevised.pdf`), so no filename filter is set. `fetch:check` (2026-11-06, a Friday) resolved "page-pdfs on https://sthelen.org/important-information/bulletin/: current" and picked `nov1_2026_sthelen_compressed.pdf`, the 1 November 2026 issue and the newest on the page that day; freshness reads `unknown` because the date comes from no file-name pattern it knows. That is the recipe recorded.

## Not yet confirmed

Whether the pick moves to the 8 November issue once it is posted: see `research` (recheck after the weekend). If the site's owner loses the domain, the bulletin may move: recheck where the directory points.
