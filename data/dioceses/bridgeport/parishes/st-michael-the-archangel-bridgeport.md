---
name: St. Michael the Archangel
website: https://www.stmichaelbridgeport.com/bulletin/
bulletin_provider: unsupported
provider_id: ''
publication: ['url:https://www.stmichaelbridgeport.com/bulletin/#st-michael-the-archangel']
group: ''
evidence:
- url: https://www.stmichaelbridgeport.com/wp-content/uploads/2026/11/November-15-2026.pdf
  seen: 2026-11-12
  quote: 310 Pulaski St., Bridgeport, CT 06608
  note: 'Page 1 masthead of the 15 November 2026 issue: ''St. Michael the Archangel'', Conventual Franciscan
    Friars, Fr. Norbert M. Siwinski, pastor. Holy Masses: Sunday 7:00 (PL), 8:30 (PL), 10:00 (EN), 11:30
    am (PL); Mon, Wed, Fri, Sat 8:00 am (PL); Fri 9:00 am (EN); Tue, Wed, Thu 7:00 pm (PL); Saturday 4:00
    pm (EN). Names no other church.'
- url: https://www.stmichaelbridgeport.com/bulletin/
  seen: 2026-11-12
  note: WordPress Bulletins page listing weekly issues newest first (November 15, 2026 back to spring
    2026), each a 'View PDF' link to /pdfviewer/<month-day-year>/ (TNC FlipBook PDF viewer); the viewer
    page carries the file URL base64-encoded, e.g. wp-content/uploads/2026/11/November-15-2026.pdf.
- url: https://www.stmichaelbridgeport.com/welcome/chapel-of-mercy/
  seen: 2026-11-12
  quote: The chapel is housed in the former convent building, which now serves as a Polish school
  note: Mother of Mercy (Ostrobramska) Chapel, dedicated 2024, 'a place of fervent prayer, parish gatherings,
    and daily Eucharistic celebrations', on the parish property.
research:
- method: fetch:check (headed) on the Bulletins page
  url: https://www.stmichaelbridgeport.com/bulletin/
  checked: '2026-11-12'
  outcome: unsupported-format
  next_action: Run fetch:check again and set provider other with its recipe
  retry_when: A collector reads TNC FlipBook (pdf-viewer-for-wordpress) viewer pages or viewer-wrapped-pdf
    gaps
bulletin_status: unsupported-format
fetch_gap:
  kind: viewer-wrapped-pdf
  seen: 2026-11-12
  url: https://www.stmichaelbridgeport.com/wp-content/uploads/2026/11/November-15-2026.pdf
  note: 'WordPress /bulletin/ lists issues newest first as ''View PDF'' links to TNC FlipBook viewer pages
    (/pdfviewer/november-15-2026/); the PDF URL is only in the viewer page, base64-encoded (aHR0cHM6Ly93d3cuc3RtaWNoYWVsYnJpZGdlcG9ydC5jb20v...).
    fetch:check: ''No PDF links found on bulletin post page''. A collector would decode the viewer''s
    base64 file URL, or try /wp-content/uploads/<yyyy>/<mm>/<Month>-<d>-<yyyy>.pdf.'
---

## Publisher

St. Michael the Archangel, Bridgeport (Conventual Franciscans, Polish and English) posts its own weekly bulletin on its WordPress site. The 15 November 2026 issue (`https://www.stmichaelbridgeport.com/wp-content/uploads/2026/11/November-15-2026.pdf`, read 2026-11-12 with probe pdf; pages 1-3 have text) has the masthead "St. Michael the Archangel, 310 Pulaski St., Bridgeport, CT 06608" with Fr. Norbert M. Siwinski, pastor, and its Mass schedule; it names no other parish.

## Worship sites

- `st-michael-the-archangel-bridgeport`: the church at 310 Pulaski Street (directory:1333, GCatholic 22001).

The parish's Mother of Mercy (Ostrobramska) Chapel, dedicated 2024, is in the former convent building on the parish property and hosts "daily Eucharistic celebrations" (site, read 2026-11-12). The bulletin's schedule does not say which Masses are held there, and it is on the same campus, so it is part of this church's site rather than a separate church row (same treatment as an upper/lower church).

## Website and bulletin provider

Provider `unsupported` with a `viewer-wrapped-pdf` fetch gap: the bulletin is current and weekly, but no collector reads it yet. The Bulletins page `https://www.stmichaelbridgeport.com/bulletin/` lists issues newest first. Each 'View PDF' links a TNC FlipBook viewer page (`/pdfviewer/november-15-2026/`) whose PDF URL is base64-encoded in the page; the files themselves are under `/wp-content/uploads/<yyyy>/<mm>/<Month>-<d>-<yyyy>.pdf`. `fetch:check` on 2026-11-12 failed: "No PDF links found on bulletin post page" (it followed the viewer page). No publisher id exists for this self-hosted bulletin.

The publication id is the site's bulletin page in the `url:` form, so `validate` can catch another row carrying the same bulletin.

## Not yet confirmed

Which of the scheduled Masses are in the Ostrobramska Chapel rather than the church (it doesn't change the rows).
