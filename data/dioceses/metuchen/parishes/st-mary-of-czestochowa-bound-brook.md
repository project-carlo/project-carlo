---
name: St. Mary of Czestochowa
website: http://www.stmarys-boundbrook.com
bulletin_provider: other
provider_id: page-pdfs http://www.stmarys-boundbrook.com/Bulletin
publication: ['url:http://www.stmarys-boundbrook.com/Bulletin']
group: ''
evidence:
- url: http://www.stmarys-boundbrook.com/UploadFiles/Bulletins/2026-10-25.pdf
  seen: 2026-10-30
  quote: 180D - St. Mary of Czestochowa Church, Bound Brook, NJ
  note: 'Page 5 of the 25 October 2026 issue (5 pages; the advertiser page is the only one with a readable
    text layer): the publisher''s code line names St. Mary of Czestochowa Church alone.'
- url: http://www.stmarys-boundbrook.com/UploadFiles/Bulletins/2026-10-25.pdf
  seen: 2026-10-30
  note: 'Page 1 is an image (rendered and read 2026-10-30). The masthead reads ''St. Mary of Czestochowa
    Church, Established 1914, 201 Vosseller Avenue, Bound Brook, New Jersey 08805, Rev. John Stec, Administrator''.
    Mass schedule: Saturday eve 5:00 p.m. (English); Sunday 9:00 a.m. (English) and 11:00 a.m. (Polish);
    holy days vigil 7:00 p.m., holy day 9:00 a.m. (English) and 7:00 p.m. (Polish); weekday Mass 8:30
    a.m. (English).'
- url: http://www.stmarys-boundbrook.com/Bulletin
  seen: 2026-10-30
  quote: '2026-10-25'
  note: The parish's own Bulletin page lists one PDF per Sunday (to 2026-11-01, newest first) at ../UploadFiles/Bulletins/<YYYY-MM-DD>.pdf,
    back to 2023.
research:
- method: fetch:check page-pdfs on the parish Bulletin page, plus probe pdf and a rendered page 1
  url: http://www.stmarys-boundbrook.com/UploadFiles/Bulletins/2026-10-25.pdf
  checked: '2026-10-30'
  outcome: unsupported-format
  next_action: Check with the pipeline's image/OCR reading whether page 1 (an image) yields the Mass schedule;
    until then Mass times for this parish rely on a rendered read
  retry_when: The pipeline reads image-only bulletin pages, or the parish posts a text-layer bulletin
bulletin_status: available
---

## Publisher

St. Mary of Czestochowa (201 Vosseller Avenue, Bound Brook) publishes its own weekly bulletin, hosted as PDFs on its own site. The 25 October 2026 issue is five pages; only page 5 has a readable text layer (an advertisement page whose footer reads "180D - St. Mary of Czestochowa Church, Bound Brook, NJ"). I rendered page 1 and read it as an image: the masthead names St. Mary of Czestochowa Church and Rev. John Stec, Administrator, with one Mass schedule (Saturday 5:00 p.m.; Sunday 9:00 a.m. English and 11:00 a.m. Polish; weekdays 8:30 a.m.). Greps of the 25 October and 1 November issues for Joseph and Mercy found nothing, so it is not shared with St. Joseph or Our Lady of Mercy.

The finder lists Rev. John Stec as Administrator, which the bulletin confirms.

## Worship sites

One church, 201 Vosseller Avenue (`st-mary-of-czestochowa-bound-brook`; directory:24473, gcatholic:18675). No other place is named.

## Website and bulletin provider

The finder gives http://www.stmarys-boundbrook.com. GCatholic gives www.stmarys-boundbrook.org, which does not resolve (probe url, 2026-10-30, checked with and without www). The site's Bulletin page lists the PDFs. Provider `other`, recipe `page-pdfs http://www.stmarys-boundbrook.com/Bulletin`.

## Fetch check

`pnpm fetch:check` on 2026-10-30 resolved `page-pdfs` on http://www.stmarys-boundbrook.com/Bulletin and picked `UploadFiles/Bulletins/2026-11-01.pdf` (6 pages, 1.8 MB): transport ok, PDF, issue date 2026-11-01 inferred from the file name only ("First page has no extractable text"), freshness `future` (two days ahead). Because page 1 is an image, the pipeline's text extraction can't read the masthead or Mass schedule from this PDF; the pick is the newest file on the parish's own Bulletin page, and I verified the parish by rendering page 1 of the 25 October issue. A grep of the 1 November issue for Czestochowa finds the page-5 publisher line.

## Not yet confirmed

The schedule text comes from an image page, so the bulletin's own text layer can't be read by the pipeline's text extraction; see the fetch check below and the research entry.
