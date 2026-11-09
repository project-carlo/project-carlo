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
- url: https://iccbronx.org/documents/2026/11/080E_2026_11_08.pdf
  seen: 2026-11-09
  quote: Sunday, November 8, 2026
  note: 'November 8, 2026 issue picked by fetch:check (page-pdfs on https://iccbronx.org/bulletin), 8
    pages. Page 1 is an image, read from a rendering: masthead Immaculate Conception Catholic Church,
    754 East Gun Hill Road, Bronx, New York 10467, 32nd Sunday in Ordinary Time, November 08, 2026, with
    the Mass schedule. The quote is from the page 2 Mass intentions.'
promoted: 2026-10-08
research:
- method: fetch:check (scratch/nyc/fetch-check-1109.json) downloaded the parish-domain PDF (3.05 MB, status
    ok); probe pdf read pages 2-8 and render.py page 1
  url: https://iccbronx.org/documents/2026/11/080E_2026_11_08.pdf
  checked: '2026-11-09'
  outcome: found
  next_action: 'None: the page-pdfs recipe downloads the current issue from the parish domain; the October
    HTTP 403 did not recur'
---

## Publisher

The September 27, 2026 linked issue identifies Immaculate Conception, Gun Hill Road, Bronx and supplies the quoted Mass schedule/dated intentions.

## Worship sites

The linked worship site [Immaculate Conception](../churches/immaculate-conception-bronx-16195.md) at 754 Gun Hill Rd. has affirmative public Mass evidence. The image masthead gives 754 East Gun Hill Road; GCatholic shortens the street to Gun Hill Road. This is not the Melrose parish. 

## Website and bulletin provider

The parish bulletin page was inspected October 7, 2026 in saved local Chrome and the separate T3 preview tab. The page is /bulletin (singular), not the generic eCatholic /bulletins endpoint. Its own-domain document link is resolved by the page-pdfs recipe in the October 7 saved-page replay. The same document at files.ecatholic.com/14517/documents/2026/9/080E_2026_09_27.pdf was downloaded and its masthead read visually. The publication ID still identifies this eCatholic-hosted bulletin; provider other selects the actual document listing. Replay results are saved in scratch/bronx1-resolver-check.json.

## Not yet confirmed

Settled 2026-11-09: fetch:check's page-pdfs recipe on https://iccbronx.org/bulletin downloaded the November 8, 2026 issue from the parish domain (iccbronx.org/documents/2026/11/080E_2026_11_08.pdf). Its image-only cover, read from a rendering, carries the Immaculate Conception, 754 East Gun Hill Road masthead. The October 403 on the parish-domain PDF did not recur.
