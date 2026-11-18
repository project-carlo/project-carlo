---
name: Mary, Mother of the Church (East New York)
website: http://www.marymotherofthechurchbklyn.org/
bulletin_provider: unsupported
provider_id: ''
publication: []
group: Deanery B6 (Brooklyn East)
evidence:
- url: http://www.marymotherofthechurchbklyn.org/downloads/bulletin/November%201,%202026.pdf
  seen: 2026-11-07
  quote: MARY MOTHER OF THE CHURCH PARISH
  note: '1 November 2026 issue (file ''November 1, 2026.pdf''; the masthead misprints ''Sunday November
    2, 2026 XXXI Sunday in Ordinary Time''), 8 pages, 6 with text. The page 1 masthead names two churches
    with their own schedules: St. Gabriel the Archangel, 749 Linwood Street (Sunday 8:00 AM Spanish, 11:00
    AM English, 12:30 PM Spanish; Saturday 5:00 PM; weekdays 8:30 AM) and St. John Cantius, 479 New Jersey
    Avenue (Sunday 9:30 AM English, 11:00 AM Spanish; Thursday 7:00 PM Spanish); Pastor Fr. Edward Mason;
    ''Two Churches ... One Parish Family''. No LPi, John Patrick or Church Bulletin Inc. marks in the
    text layer: a self-made bulletin.'
- url: http://www.marymotherofthechurchbklyn.org/bulletin.php
  seen: 2026-11-07
  quote: Download this week's bulletin
  note: Bulletin page links one current issue, https://marymotherofthechurchbklyn.org/downloads/bulletin/November
    1, 2026.pdf. The https:// bare domain fails certificate verification (hostname mismatch); the http://www.
    form serves the same file.
revisit: Rerun fetch:check with the page-pdfs recipe once the certificate or the fetcher changes (see
  research).
revisit_after: 2027-01-15
research:
- method: fetch:check (headed Chrome) on recipe page-pdfs http://www.marymotherofthechurchbklyn.org/bulletin.php
  url: http://www.marymotherofthechurchbklyn.org/bulletin.php
  checked: '2026-11-07'
  outcome: unsupported-format
  next_action: Set bulletin_provider other with provider_id 'page-pdfs http://www.marymotherofthechurchbklyn.org/bulletin.php',
    rerun fetch:check and clear the fetch_gap once it downloads the current issue
  retry_when: fetch falls back to http:// on a certificate failure, or the site's certificate is fixed
    or its links change to http://www.
bulletin_status: available
fetch_gap:
  kind: https-pdf-link-cert-mismatch
  seen: 2026-11-07
  note: bulletin.php (served over http://www.) links each issue as an absolute https://marymotherofthechurchbklyn.org/downloads/bulletin/<Month
    D, YYYY>.pdf; the bare domain's certificate is not valid for that hostname, so fetch's download fails
    (CERTIFICATE_VERIFY_FAILED) and has no http fallback. The same file downloads over http://www.marymotherofthechurchbklyn.org/downloads/bulletin/.
    fetch:check resolved page-pdfs http://www.marymotherofthechurchbklyn.org/bulletin.php 'current' (2026-11-01)
    before the download failed.
  url: http://www.marymotherofthechurchbklyn.org/downloads/bulletin/November%201,%202026.pdf
---

## Publisher

Mary, Mother of the Church (the 2007 merger of St. Gabriel and St. John Cantius, per the batch plan's archives note) publishes one self-made weekly bilingual bulletin (no LPi, John Patrick or Church Bulletin Inc. marks in the text layer) on its own site. The 1 November 2026 issue (read 2026-11-07, 8 pages, pages 7-8 images) has the masthead "MARY MOTHER OF THE CHURCH PARISH ... PARROQUIA MARIA MADRE DE LA IGLESIA", Pastor Fr. Edward Mason, office at 749 Linwood St; the masthead date misprints "November 2, 2026" for the 1 November issue named in the file.

## Worship sites

Two, each with its own schedule in the 1 November masthead ("Two Churches ... One Parish Family"):

- St. Gabriel the Archangel, 749 Linwood Street: Sunday 8:00 AM Spanish, 11:00 AM English, 12:30 PM Spanish; Saturday 5:00 PM; Monday, Tuesday, Wednesday and Friday 8:30 AM.
- St. John Cantius, 479 New Jersey Avenue: Sunday 9:30 AM English, 11:00 AM Spanish; Thursday 7:00 PM Spanish.

Page 2 lists the intentions under both ("SAINT GABRIEL ~ SAN GABRIEL ST. JOHN CANTIUS ~ SAN JUAN CANCIO"). St. John Cantius is not closed: GCatholic 16723 lists it under the parish, and the bulletin still has Sunday Mass there. The directory, deanery list and Mass finder 1124 give only the Linwood Street address.

## Website and bulletin provider

`unsupported`, `fetch_gap` kind `https-pdf-link-cert-mismatch`. The bulletin page (http://www.marymotherofthechurchbklyn.org/bulletin.php) links only the current issue, replaced weekly, but as an absolute `https://marymotherofthechurchbklyn.org/...` URL whose certificate does not match the hostname. On 2026-11-07 `fetch:check` with recipe `page-pdfs http://www.marymotherofthechurchbklyn.org/bulletin.php` resolved the 1 November issue as current, then failed to download it (CERTIFICATE_VERIFY_FAILED). The same file reads over `http://www.`. That recipe is the one to restore when the fetcher or the site changes. No publication id: the bulletin has no online container.

## Not yet confirmed

Pages 7-8 have no text layer (likely ads); a printer's footer there, if any, was not read.
