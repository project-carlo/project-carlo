---
name: St. Mary Magdalen
website: https://www.smmchurch.org/
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-mary-magdalen-church-wilmington-de-19803
publication: ['url:https://www.church-bulletin.org/saint-mary-magdalen-church-wilmington-de-19803']
group: Brandywine Hundred Deanery
evidence:
- url: https://www.church-bulletin.org/bulletin/saint-mary-magdalen-church-wilmington-de-19803/2026-10-25.pdf
  seen: 2026-10-27
  note: 'Page 1 (image only, no text layer; rendered and read) of the 25 October 2026 issue: masthead
    ''SAINT MARY MAGDALEN CATHOLIC CHURCH'', 7 Sharpley Road, Wilmington, DE 19803; ''PARISH CLERGY Rev.
    Msgr. Steven P. Hurley, V.G. Pastor'', Deacons Howard Eck and Justin Pollio; Mass schedule ''Saturday
    - 4:30pm Vigil Mass; Sunday - 8:30am & 10:30am; Weekday Mass Tuesday, Wednesday, Thursday, Saturday
    - 8:30am; First Friday - 8:30am''. Names this parish alone.'
- url: https://church-bulletin.org/?id=318
  seen: 2026-10-27
  quote: Saint Mary Magdalen Church Bulletin
  note: Redirects to the church-bulletin.org listing of dated weekly PDFs, newest 2026-10-25; the parish's
    'Bulletins & Worship Aids' page links it ('here.').
- url: https://www.smmchurch.org/sunday-bulletins-worship-aids
  seen: 2026-10-27
  note: 'Parish page (eCatholic site 6923): holds seasonal worship aids (Corpus Christi, Holy Trinity,
    Pentecost, Ascension 2026 PDFs) and links the John Patrick listing for the weekly bulletin; no weekly
    bulletins are hosted in eCatholic.'
publication_reviews:
- parish: st-ann-st-thomas-wilmington
  decision: separate
  evidence:
  - url: https://www.church-bulletin.org/bulletin/saint-mary-magdalen-church-wilmington-de-19803/2026-10-25.pdf
    seen: 2026-10-27
    note: 'St. Mary Magdalen''s 25 October 2026 issue (page 1, rendered): masthead for this parish alone,
      pastor Msgr. Steven P. Hurley, Saturday vigil 4:30pm; no St. Ann or St. Thomas content seen on pages
      1-2. Checked 2026-10-27: St. Mary Magdalen''s rendered masthead names that parish alone; the St.
      Ann / St. Thomas file never names St. Mary Magdalen or Msgr. Hurley.'
  - url: https://files.ecatholic.com/38453/bulletins/20261025.pdf
    seen: 2026-10-27
    quote: Rev. James Lentini
    note: 'The same-week St. Ann and St. Thomas issue: different publisher, pastor (Rev. James Lentini),
      schedules and Mass intentions.'
---

## Publisher

St. Mary Magdalen prints its own weekly bulletin through John Patrick Publishing, listed at church-bulletin.org/saint-mary-magdalen-church-wilmington-de-19803 (the parish site's bulletins page links `church-bulletin.org/?id=318`). The 25 October 2026 issue's cover names this parish alone, with its own pastor, Rev. Msgr. Steven P. Hurley, V.G., and its own Mass schedule. The issues are scanned images, so the text layer is empty; page 1 was rendered and read.

## Worship sites

One church, 7 Sharpley Road. The bulletin's schedule lists nothing else. Mass in the diocese map is Sun 8:30 and 10:30, Sat 4:30 pm and 8:30 am, Tue-Fri 8:30; the bulletin cover gives the Saturday vigil at 4:30pm and weekday Mass Tuesday, Wednesday, Thursday and Saturday at 8:30am, plus First Friday (the map also has every Friday).

## Shared pastor check

St. Thomas's pastor administered St. Mary Magdalen from October 2025 to April 2026 (diocese.md, from The Dialog). It now has its own pastor and its own bulletin, separate from the St. Ann and St. Thomas the Apostle bulletin (see publication_reviews), so it is its own row.

## Website and bulletin provider

smmchurch.org is an eCatholic site (id 6923) but the weekly bulletin is on church-bulletin.org, so the resolver reads the listing page with a `page-pdfs` recipe. The fetch check is recorded below.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-mary-magdalen-wilmington` (2026-10-27): the pinned `page-pdfs` recipe picked `2026-10-25.pdf` (7.7 MB), fresh (2 days), transport ok. Document type PDF with the note 'First page has no extractable text': every recent issue is a scanned image, so reading Mass times needs image rendering or OCR. Identity 'unverified' by the tool; the rendered cover settles it.

## Not yet confirmed

The issue PDFs are image-only, so the pipeline's text extraction may have to fall back to images (see the fetch check).
