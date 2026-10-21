---
name: Saint John the Evangelist Parish, Bellefonte
website: http://www.stkaterichurch.org/bulletin.html
bulletin_provider: other
provider_id: page-pdfs http://www.stkaterichurch.org/bulletin.html
publication: ['url:http://www.stkaterichurch.org/bulletin.html', 'url:http://www.bellefontecatholicchurch.org/']
group: ''
evidence:
- url: http://www.stkaterichurch.org/bulletins/Bulletin10.11.26.pdf
  seen: 2026-10-21
  quote: Fr. Brian Saylor, Pastor | Deacon Tom Boldin
  note: 'Page 1 of the 10 Oct 2026 / 28th Sunday issue (6 pages): the masthead carries two churches, "ST. JOHN THE EVANGELIST CATHOLIC CHURCH 134 East Bishop Street, Bellefonte, PA 16823" and "ST. KATERI TEKAKWITHA CATHOLIC CHURCH PO Box 159, 3503 Penns Valley Rd, Spring Mills, PA 16875"; MASS SCHEDULE "Saturday: 5:00 p.m.", "Sunday: 8:00 a.m. & 10:15 a.m.", "St. Kateri Church: 12:00 p.m. Sunday". Page 2 has "Masses for the week" and "St. Kateri Masses for the week" side by side. This file is byte-identical (md5 70217c01160d84af3202f9a4edb15e8e) to the copy at http://www.bellefontecatholicchurch.org/10112026b.pdf, and the 27 Sep issues (09272026.pdf on the Bellefonte site, Bulletin9.27.26.pdf on the Kateri site) are identical too (md5 e4bae6d4174e8fa2b317dff1302dbb56).'
- url: http://www.stkaterichurch.org/bulletin.html
  seen: 2026-10-21
  quote: Our most recent bulletins are available for download below.
  note: 'The Kateri site''s Weekly Bulletins page lists bulletins/Bulletin10.11.26.pdf, 10.4.26, 9.27.26 and 9.20.26 (the 9.20.26 link returns an HTML page, not a PDF). The 18 Oct issue was not posted on either site on 21 Oct (404).'
- url: http://www.bellefontecatholicchurch.org/
  seen: 2026-10-21
  quote: The Bulletins are in PDF Format.
  note: 'Bellefonte''s homepage lists 10112026b.pdf, 10042026.pdf, 09272026.pdf, 09202026.pdf, 09132026.pdf under "Bulletins". Plain https fails (certificate for another host; probe url UNREACHABLE) and, to a client without a browser user agent, the PDFs answer a 12 KB JavaScript reload page (fetch:check `not_pdf`), so the row reads the Kateri site instead.'
- url: https://www.dioceseaj.org/parishes/
  seen: 2026-10-21
  note: 'Directory lists both as separate parishes: Saint John the Evangelist Parish, Bellefonte (homepage bellefontecatholicchurch.org; Sat 5:00 PM, Sun 8:00 and 10:15 AM, weekdays) and Saint Kateri Tekakwitha Parish, Spring Mills (homepage stkaterichurch.org; Sun 12:00 PM, Tue 11:00 AM Communion Service). Both match the one bulletin.'
---

## Publisher

Saint John the Evangelist (Bellefonte) and Saint Kateri Tekakwitha (Spring Mills) are two canonical parishes with one pastor, Fr. Brian Saylor (called "Very Rev." in the batch lead; the bulletin says "Fr. Brian Saylor, Pastor"), and **one bulletin**. The 10 Oct 2026 issue (read 2026-10-21) carries both churches in its masthead and in its Mass schedule, and the same PDF is posted on both parishes' sites (identical md5 for 11 Oct and 27 Sep issues). Nothing separate is published for Spring Mills, so the Spring Mills roster entry is a worship site of this row, not a row of its own.

## Worship sites

Two churches: St. John the Evangelist, 134 East Bishop Street, Bellefonte (Sat 5:00 PM; Sun 8:00 and 10:15 AM; weekdays) and St. Kateri Tekakwitha, 3503 Penns Valley Road, Spring Mills (Sun 12:00 PM; Tuesday 11:00 AM Communion Service per the directory and the bulletin's "communion service this Tuesday"). The Oct bulletin lists a separate "St. Kateri Masses for the week" column.

## Website and bulletin provider

`other`, recipe `page-pdfs http://www.stkaterichurch.org/bulletin.html`. The Bellefonte site is the primary homepage but answers non-browser clients with a JavaScript reload page instead of the PDF (and its https certificate is for another host), so the row's website is the Kateri site's Bulletins page, which serves the same file. `pnpm fetch:check` (2026-10-21) picked `http://www.stkaterichurch.org/bulletins/Bulletin10.11.26.pdf` ("first-listed, dated 2026-10-11"), status ok. The 18 Oct issue was not yet posted on either site; `first-listed` is the newest. Both homepages are recorded as `url:` publication ids.

## Not yet confirmed

Whether the Kateri site stays current: it posted the same weeks as Bellefonte's through 11 Oct. Recheck after the 18 Oct issue appears; if the Kateri page lags Bellefonte's, switch the recipe to the Bellefonte site with a browser fetch.
