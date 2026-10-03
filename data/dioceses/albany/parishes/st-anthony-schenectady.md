---
name: St. Anthony's Church
website: https://stanthonyschurch.net/bulletin.htm
bulletin_provider: other
provider_id: page-pdfs
publication: ['url:https://stanthonyschurch.net/bulletin.htm']
group: ''
evidence:
- url: https://stanthonyschurch.net/bulletin/09-27-26.pdf
  seen: 2026-09-28
  quote: SUNDAY MASS CELEBRATED AT 8:30 AM & 11:45 AM (SPANISH), & 4:00 PM
  note: Page 1 of the 27 September 2026 issue; the same page gives '331 Seward Place - Schenectady, NY
    12305', pastor Rev. Richard A. Carlino, and 'NO DAILY MASS'.
- url: https://stanthonyschurch.net/bulletin/09-27-26.pdf
  seen: 2026-09-28
  quote: SAINT ANTHONY'S CHURCH Sunday, September 27, 2026
  note: Page 2 heading.
- url: https://stanthonyschurch.net/bulletin.htm
  seen: 2026-09-28
  note: The parish's bulletin page lists PDFs named bulletin/MM-DD-YY.pdf, weekly through 09-27-26 on
    2026-09-28.
promoted: 2026-09-28
---

## Publisher

St. Anthony's Church, 331 Seward Place, publishes its own weekly bulletin as PDFs on its own
site. The 27 September 2026 issue's page 1 gives the address, pastor Rev. Richard A. Carlino,
and "Sunday Mass celebrated at 8:30 am & 11:45 am (Spanish), & 4:00 pm", "No daily Mass".

Fr. Carlino is also pastor of St. John the Evangelist, and the two share a secretary and a
religious-education program, but St. John's publishes a different bulletin (its own 27
September 2026 issue at sjechurch.com/bulletin/09-27-26.pdf, with its own masthead and Mass
schedule), so they are separate rows.

## Worship sites

One: `st-anthony-schenectady`. It carries the Spanish-language Sunday Mass (11:45 am); the
Hispanic community's devotions in the bulletin are held here too. The directory note that
St. John's weekday Masses are "Celebrated at St. Anthony's" is not in either current bulletin
(St. Anthony's says "No daily Mass").

## Website and bulletin provider

stanthonyschurch.net is the parish's own static site; its bulletin page lists the PDFs as
bulletin/MM-DD-YY.pdf. `bulletin_provider: other`, and `website` is that bulletin page so the
pipeline reads the list directly.

Fetch recipe `page-pdfs`, pinned 2026-10-03: on the pages recorded 2026-10-03
(`tests/fixtures/fetch/st-anthony-schenectady.json.gz`) the resolver found
https://stanthonyschurch.net/bulletin/10-04-26.pdf this way, dated that week.

## Not yet confirmed

Nothing.
