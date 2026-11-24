---
name: Infant Saviour - Pine Bush
website: https://infantsaviour.org
bulletin_provider: other
provider_id: page-pdfs https://church-bulletin.org/4023
publication: ['url:https://church-bulletin.org/4023']
group: ''
evidence:
- url: https://church-bulletin.org/4023/2026-10-04.pdf
  seen: 2026-10-08
  quote: "Church of the Infant Saviour \n22 Holland Avenue, Pine Bush, NY 12566"
  note: October 4, 2026 JPPC 4023 bulletin, page 1, publisher masthead.
- url: https://church-bulletin.org/4023/2026-10-04.pdf
  seen: 2026-10-08
  quote: "Saturday Evening: 5PM-Pine Bush \nSunday: 8:00 AM – Walker Valley \n9:30AM & 11:15AM – Pine\
    \ Bush"
  note: October 4, 2026 issue, page 1; distinguishes Pine Bush from Walker Valley.
- url: https://church-bulletin.org/4023
  seen: 2026-10-08
  quote: October 11, 2026 Bulletin
  note: Pinned page-pdfs collector replayed against the complete freshly fetched HTTP HTML, without homepage
    discovery. It selected the already-posted October 11 issue; the selected PDF downloaded HTTP 200 with
    six pages. This is an HTTP snapshot replay plus direct PDF download, not a live browser fetch:check.
- url: https://www.church-bulletin.org/bulletin/church-of-the-infant-saviour-pine-bush-ny-12566/2026-10-11.pdf
  seen: 2026-10-08
  note: Complete October 11 issue downloaded and read. Holy Rosary image-only page 1 was rendered and
    visually read; the other issues have extractable text. Future issue already posted on October 8, not
    a claim that October 11 Masses occurred.
promoted: 2026-10-11
---

## Publisher

The October 4, 2026 JPPC 4023 issue, page 1, names Church of the Infant Saviour, 22 Holland Avenue, Pine Bush, and prints one timetable explicitly divided between Pine Bush and Our Lady of the Valley in Walker Valley. The current dated issue supersedes the failed old template URL.

## Worship sites

Infant Saviour: Saturday 5 PM, Sunday 9:30/11:15 AM, daily 8 AM Monday-Saturday. Our Lady of the Valley: Sunday 8 AM in Walker Valley. Pine Bush and Walker Valley are distinct physical worship venues; the Walker Valley timetable must not be assigned to Pine Bush.

## Website and bulletin provider

The supported recipe is `page-pdfs https://church-bulletin.org/4023`. It starts at the parish-specific JPPC archive, not at a general parish homepage, and pins the collector. On October 8, 2026, replay of the complete freshly fetched archive HTML through the repository resolver selected `https://www.church-bulletin.org/bulletin/church-of-the-infant-saviour-pine-bush-ny-12566/2026-10-11.pdf` as current (October 11, already posted). The selected file downloaded HTTP 200, six pages, and its actual parish content was checked. Holy Rosary page 1 was read visually because its pages are scans; no image-only-text extraction claim is made. The other issues contain readable text.

The initial abbreviated Mozilla user agent received HTTP 406 from these JPPC pages; a complete current Chrome user agent with HTML Accept/Accept-Language headers returned the genuine archive and PDF. Holy Rosary also loaded in owned T3 tab tab_4. This access distinction is not a publisher failure. The test used HTTP snapshots and direct PDF downloads, not another browser or a live fetch:check. No CSV promotion is performed here.
