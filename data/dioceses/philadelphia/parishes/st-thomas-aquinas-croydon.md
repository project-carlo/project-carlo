---
name: St. Thomas Aquinas Parish
website: https://www.staq.org
bulletin_provider: other
provider_id: page-pdfs https://www.church-bulletin.org/saint-thomas-aquinas-parish-croydon-pa-19021
publication: ['ecatholic:2517', 'url:https://www.church-bulletin.org/saint-thomas-aquinas-parish-croydon-pa-19021']
group: ''
evidence:
- url: https://www.church-bulletin.org/saint-thomas-aquinas-parish-croydon-pa-19021
  seen: 2026-10-29
  quote: Latest Edition
  note: John Patrick listing 77 (church-bulletin.org/?id=77), 'Saint Thomas Aquinas Parish', Croydon,
    PA 19021; latest edition October 25, 2026.
- url: https://files.ecatholic.com/2517/bulletins/20261025.pdf
  seen: 2026-10-29
  note: 'Newest file on the parish eCatholic /bulletins page (seen in Chrome; probe url answers 403).
    Byte-identical (md5 d75cee961999fc2e8cc25a7e4b3ccf46, 8 pages, image-only) to the listing''s 2026-10-25.pdf.
    Rendered page 1: ''St. Thomas Aquinas Parish / Established July 1, 2014 / Joining The Parishes of
    St. Thomas Aquinas (1922 - 2014) & St. Elizabeth Ann Seton (1976 - 2014) / 601 Bristol Pike, Croydon,
    PA 19021''; ''MASS SCHEDULE Saturday Vigil: 4:30 PM; Sundays: 9:00 AM and 11:00 AM; Monday - Friday:
    8:30 AM (Chapel at 126 Walnut Ave.); Holydays: 8:30 AM, 12 Noon and 7:00 PM''.'
- url: https://www.staq.org/about-our-parish
  seen: 2026-10-29
  quote: St Elizabeth Ann Seton (1976-2014)
  note: 'Parish eCatholic site (ecatholic:2517): the page names the two merged parishes by their years
    and gives one address, 601 Bristol Pike; its Mass and Confession Times page lists Sat 4:30 PM, Sun
    9:00 and 11:00 AM and weekday Mass in the Chapel, with no mention of Park Avenue.'
- url: https://archphila.org/parish/st-thomas-aquinas-croydon/
  seen: 2026-10-28
  quote: 'Merged with St. Elizabeth Ann Seton, Bensalem: 2014'
  note: 'Directory: Rev. David A. Fernandes; 601 Bristol Pike; ''Weekdays, 8:30 AM (Chapel, 126 Walnut
    Ave.)''.'
- url: https://www.church-bulletin.org/bulletin/saint-thomas-aquinas-parish-croydon-pa-19021/2026-11-08.pdf
  seen: 2026-11-07
  note: '8 November 2026 issue on John Patrick listing 77, page 1 rendered (image-only): masthead ''St.
    Thomas Aquinas Parish, Established July 1, 2014, Joining The Parishes of St. Thomas Aquinas (1922
    - 2014) & St. Elizabeth Ann Seton (1976 - 2014), 601 Bristol Pike, Croydon, PA 19021''; Mass schedule
    Saturday Vigil 4:30 PM, Sundays 9:00 AM and 11:00 AM, Monday-Friday 8:30 AM (Chapel at 126 Walnut
    Ave.). It names no Mass at Park Ave.'
promoted: 2026-10-29
research:
- method: Rendered pages 1-2 of the 25 October 2026 issue; compared md5 of the eCatholic and listing copies;
    read the parish's About and Mass-times pages in Chrome
  url: https://files.ecatholic.com/2517/bulletins/20261025.pdf
  checked: '2026-10-29'
  outcome: found
- method: 'Hand refresh against main: fetch:check (ecatholic) picked the 25 October 2026 issue; visit.py
    on https://www.staq.org/bulletins listed nothing newer, while the John Patrick listing 77 had 1 and
    8 November; switched the row to other with page-pdfs on the listing and re-ran fetch:check'
  url: https://www.church-bulletin.org/saint-thomas-aquinas-parish-croydon-pa-19021
  checked: '2026-11-07'
  outcome: found
  next_action: None; if the listing goes silent while staq.org/bulletins carries new issues, switch back
    to ecatholic
  retry_when: ''
bulletin_status: available
---

## Publisher

St. Thomas Aquinas Parish, Croydon (Rev. David A. Fernandes, Pastor) publishes the same issue on its eCatholic site and on John Patrick listing 77: the 25 October 2026 files are byte-identical (md5 d75cee96...). The PDF is image-only; rendered, page 1's masthead is 'St. Thomas Aquinas Parish, Established July 1, 2014, Joining The Parishes of St. Thomas Aquinas (1922-2014) & St. Elizabeth Ann Seton (1976-2014), 601 Bristol Pike, Croydon' with one Mass schedule, and page 2 has Mass intentions and the lectors for 31 October and 1 November. It names this parish alone.

## Worship sites

St. Thomas Aquinas Church, 601 Bristol Pike, with the weekday Mass in the parish chapel at 126 Walnut Ave. (one weekday Mass 'Chapel at 126 Walnut Ave.'; a chapel on the parish's own property, not a separate church row). The directory calls St. Elizabeth Ann Seton (1200 Park Ave., Bensalem) a worship site, but the bulletin and the parish site list no Mass there: see the open record `st-elizabeth-ann-seton-bensalem`.

## Website and bulletin provider

`https://www.staq.org` is eCatholic (2517), and the parish posts the same file on John Patrick listing 77 (both publication ids are recorded). On 2026-11-07 (hand refresh against main) the eCatholic /bulletins page stopped at 25 October 2026 while the listing had 1 and 8 November, so the row reads the listing: `other` with `page-pdfs https://www.church-bulletin.org/saint-thomas-aquinas-parish-croydon-pa-19021`, as the diocese's other John Patrick rows do.

## Not yet confirmed

Whether Mass is ever celebrated at Park Avenue (see open record).

## Fetch check

`fetch:check` (2026-10-29) with the `ecatholic` provider picked `files.ecatholic.com/2517/bulletins/20261025.pdf`: transport ok, PDF, fresh; identity `unverified` because the PDF has no text layer, so the masthead was read by hand above. On 2026-11-07, with `ecatholic` it picked the 25 October issue again (13 days old, eCatholic not updated since); with the listing recipe it picked `church-bulletin.org/bulletin/saint-thomas-aquinas-parish-croydon-pa-19021/2026-11-08.pdf` (transport ok, PDF, this Sunday's issue; page 1 rendered by hand shows the St. Thomas Aquinas masthead).
