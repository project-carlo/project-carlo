---
name: Immaculate Conception, Gun Hill Road, Bronx
website: https://iccbronx.org/bulletin
bulletin_provider: other
provider_id: page-pdfs https://iccbronx.org/bulletin
publication: ['ecatholic:14517']
group: Immaculate Conception, Gun Hill Road, Bronx
evidence:
- url: https://files.ecatholic.com/14517/documents/2026/9/080E_2026_09_27.pdf
  seen: 2026-10-07
  quote: Immaculate Conception Catholic Church
  note: Latest linked issue inspected October 7, 2026; masthead visually read on rendered page 1 where
    the text layer omits it.
- url: https://files.ecatholic.com/14517/documents/2026/9/080E_2026_09_27.pdf
  seen: 2026-10-07
  quote: |-
    Saturday, September 26, 2026

    5:30 pm
  note: Dated vigil Mass intention in the saved actual issue text, not a recurring timetable heading.
revisit: Confirm live PDF downloading for the page-pdfs collector; direct parish-domain PDF answered HTTP
  403, while the identical eCatholic files-host document was read successfully.
revisit_after: 2026-10-14
promoted: 2026-10-08
---

## Publisher

The September 27, 2026 linked issue identifies Immaculate Conception, Gun Hill Road, Bronx and supplies the quoted Mass schedule/dated intentions.

## Worship sites

The linked worship site [Immaculate Conception](../churches/immaculate-conception-bronx-16195.md) at 754 Gun Hill Rd. has affirmative public Mass evidence. The image masthead gives 754 East Gun Hill Road; GCatholic shortens the street to Gun Hill Road. This is not the Melrose parish. 

## Website and bulletin provider

The parish bulletin page was inspected October 7, 2026 in saved local Chrome and the separate T3 preview tab. The page is /bulletin (singular), not the generic eCatholic /bulletins endpoint. Its own-domain document link is resolved by the page-pdfs recipe in the October 7 saved-page replay. The same document at files.ecatholic.com/14517/documents/2026/9/080E_2026_09_27.pdf was downloaded and its masthead read visually. The publication ID still identifies this eCatholic-hosted bulletin; provider other selects the actual document listing. Replay results are saved in scratch/bronx1-resolver-check.json.

## Not yet confirmed

The collector selects the correct document, but direct download from the parish domain was blocked with HTTP 403 during research. Verify live downloading or a supported stable files-host rewrite before promotion; never call the bulletin absent because that download is blocked.
