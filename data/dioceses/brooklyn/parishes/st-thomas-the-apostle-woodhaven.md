---
name: St. Thomas the Apostle (Woodhaven)
website: https://www.stawoodhaven.org/
bulletin_provider: unsupported
provider_id: ''
publication: []
group: Deanery Q8 (Queens West)
evidence:
- url: https://drive.google.com/uc?id=14h36ETY9J0RdYIpfTA7mxEmF-a2Mvx3i&export=download
  seen: 2026-11-06
  quote: October 25, 2026       Thirtieth Sunday in Ordinary Time
  note: 'Drive file ''sat woodhaven 10 25 26.pdf'', 7 pages, embedded on the stawoodhaven.org homepage.
    Page 1 masthead: SAINT THOMAS THE APOSTLE Roman Catholic Church, 87-19 88th Avenue, Woodhaven, NY
    11421; Rev. Francisco J. Walker, Pastor; Masses Monday-Saturday 9am (English), Thursday 7pm (Spanish),
    Saturday Vigil 5pm, Sunday 9am, 11am (English), 12:30pm (Spanish). No other church or chapel is named;
    no LPi or Church Bulletin Inc. footer.'
- url: https://www.stawoodhaven.org/
  seen: 2026-11-06
  quote: 'Sunday: 9:00 AM, 11:00 AM, 12:30 PM (Español)'
  note: 'Google Sites homepage: Mass schedule, plus two embedded Drive previews, ''sat woodhaven 10 25
    26.pdf'' and ''sta 10 18 2026.pdf''. No 1 November issue was posted on 2026-11-06. The site menu has
    no bulletin page.'
research:
- method: fetch:check (headed Chrome), unpinned and with page-pdfs https://www.stawoodhaven.org/
  url: https://www.stawoodhaven.org/
  checked: '2026-11-06'
  outcome: unsupported-format
  next_action: When a collector reads Google Drive file previews embedded in a page (drive-preview-embed),
    set provider other, run fetch:check and confirm it picks the newest issue
  retry_when: A collector for drive-preview-embed lands, or the parish posts PDF links or a Drive folder
- method: probe po on st-thomas-the-apostle-11421, st-thomas-the-apostle-church-11421, st-thomas-the-apostle-woodhaven
  checked: '2026-11-06'
  outcome: not-found
  next_action: 'None needed: the bulletin is self-published with no LPi footer'
  retry_when: An issue shows an LPi footer
bulletin_status: available
fetch_gap:
  kind: drive-preview-embed
  seen: 2026-11-06
  note: stawoodhaven.org is a Google Sites page whose homepage embeds the latest bulletins as Google Drive
    file previews (iframe data-src drive.google.com/file/d/<id>/preview, aria-label 'Drive, sat woodhaven
    10 25 26.pdf'), one file per issue, with no folder link and no bulletin page. fetch:check finds no
    bulletin page link unpinned and 'No PDF links found' with page-pdfs on the homepage. The file itself
    downloads (drive.google.com/uc?id=<id>&export=download) and is a readable 7-page PDF.
  url: https://drive.google.com/file/d/14h36ETY9J0RdYIpfTA7mxEmF-a2Mvx3i/view
---

## Publisher

St. Thomas the Apostle, Woodhaven publishes its own weekly bulletin (7 pages, no LPi or Church Bulletin Inc. footer). The 25 October 2026 issue, a Google Drive file named "sat woodhaven 10 25 26.pdf" embedded on the parish homepage (read 2026-11-06), has the page 1 masthead "SAINT THOMAS THE APOSTLE Roman Catholic Church", 87-19 88th Avenue, Woodhaven, NY 11421, with Rev. Francisco J. Walker, Pastor.

## Worship sites

One. The page 1 schedule lists daily Mass Monday-Saturday 9am (English), Thursday 7pm (Spanish), Saturday Vigil 5pm and Sunday 9am, 11am (English) and 12:30pm (Spanish), with no other church or chapel (no "chapel" or "capilla" anywhere in the issue). The directory, the deanery list, GCatholic 16789 and Mass finder 1169 all give the one church at 87-19 88th Avenue.

## Website and bulletin provider

`unsupported`, fetch gap `drive-preview-embed`. stawoodhaven.org is a Google Sites page with no bulletin page; the homepage shows the newest two issues as Drive file previews in iframes (on 2026-11-06: 25 October and 18 October). `fetch:check` found no bulletin link unpinned and "No PDF links found" with `page-pdfs https://www.stawoodhaven.org/`. Each file downloads as a PDF through `drive.google.com/uc?id=<id>&export=download`, so a collector that follows the preview iframes would read it. No publication id: the bulletin has no publisher container.

## Not yet confirmed

The 1 November issue was not yet posted on 2026-11-06, so the posting lag is unknown; recheck when a collector lands (see research).
