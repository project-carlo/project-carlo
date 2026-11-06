---
name: St. Clement Pope (Jamaica)
website: https://stclementpopechurch.org/
bulletin_provider: other
provider_id: page-pdfs https://stclementpopechurch.org/?page_id=1466
publication: []
group: Deanery Q9 (Queens East)
evidence:
- url: https://stclementpopechurch.org/wp-content/uploads/2026/10/BulletinCover-and-insertNov12026.pdf
  seen: 2026-11-06
  quote: St. Clement Pope Church
  note: '1 November 2026 issue (PubKeep PDF, 4 pages, page 4 an image). Page 1 masthead: ''St. Clement
    Pope Church'', ''141-11 123rd Avenue, Jamaica, New York 11436'', ''Served by the Society of Divine
    Vocations'', Rev. Fr. Christogonus Iwunze, S.D.V-Pastor; ''Sunday, November 1, 2026''; ''Holy Mass
    is Offered Saturday 5 PM, Sunday 9:30 AM (English), Sunday 12:30 PM (Igbo), Daily Masses (In the Church)
    Monday to Friday 8:30 AM''.'
- url: https://stclementpopechurch.org/
  seen: 2026-11-06
  note: Homepage (read with visit.py; probe url gets RemoteDisconnected) links the bulletin PDFs from
    /wp-content/uploads/, newest BulletinCover-and-insertNov12026.pdf, then Bulletin10252026.pdf, Bulletin-10112026.pdf,
    Bulletin-07052026.pdf; file names vary week to week.
bulletin_status: available
---

## Publisher

St. Clement Pope publishes its own weekly bulletin as PDFs on its WordPress site. The 1 November 2026 issue (read 2026-11-06 through `tools/fetch-pdf.py`) has the masthead "St. Clement Pope Church", 141-11 123rd Avenue, Jamaica, New York 11436, "Served by the Society of Divine Vocations", Rev. Fr. Christogonus Iwunze, S.D.V-Pastor. No LPi footer or Church Bulletin Inc. page; the PDF is made with PubKeep.

## Worship sites

One church. The 1 November 2026 issue gives Saturday 5 PM, Sunday 9:30 AM (English) and 12:30 PM (Igbo), and "Daily Masses (In the Church) Monday to Friday 8:30 AM"; the week's intentions are all at those times. The diocese's parish and deanery directories, GCatholic 16698 and Mass finder place 4 list only this church.

## Website and bulletin provider

`other`, recipe `page-pdfs https://stclementpopechurch.org/?page_id=1466` as printed by `fetch:check` on 2026-11-06, which picked the 1 November 2026 issue (BulletinCover-and-insertNov12026.pdf). The website is the homepage stclementpopechurch.org (the directory's link and the masthead's website), which also links the PDFs. The host refuses `probe url` and `probe pdf` (RemoteDisconnected) but answers the browser and the pipeline's fetcher. Posting is irregular (no 18 October 2026 file is listed) and file names vary (`Bulletin-MMDDYYYY.pdf`, `BulletinMMDDYYYY.pdf`, `BulletinCover-and-insertNov12026.pdf`), so fetch:check reports the freshness as unknown; the pick was checked by hand.

## Not yet confirmed

Nothing open.
