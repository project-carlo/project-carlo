---
name: St. Martin of Tours
website: https://stmartinamityville.com/bulletins/
bulletin_provider: unsupported
provider_id: page-pdfs https://stmartinamityville.com/bulletins/
publication: ['url:https://stmartinamityville.com/bulletins/']
group: ''
evidence:
- url: https://stmartinamityville.com/wp-content/uploads/2026/11/11-8-26-martintours.pdf
  seen: 2026-11-13
  quote: 37 Union Avenue, Amityville, NY 11701
  note: 'Page 1 of the November 8, 2026 issue: masthead ''The Church of ST. MARTIN OF TOURS, AMITYVILLE,
    NEW YORK'', one parish. EUCHARIST MASS SCHEDULE: Monday - Friday 8:30AM; Saturday Vigil 5:00PM; Sunday
    Masses 9:00AM, 10:30AM, 12 NOON. Made in Microsoft Publisher by the parish (Bulletin Editor smtbulletin@gmail.com).'
- url: https://stmartinamityville.com/bulletins/
  seen: 2026-11-13
  note: 'WordPress Bulletins page read with visit.py: self-hosted PDFs 11-8-26-martintours.pdf, 11-1-26-martintours.pdf,
    10-25-26-martintours.pdf and earlier, under /wp-content/uploads/.'
research:
- method: fetch:check with page-pdfs on the Bulletins page
  url: https://stmartinamityville.com/bulletins/
  checked: '2026-11-13'
  outcome: unsupported-format
  next_action: Rerun fetch:check; when it dates 11-<d>-26-martintours.pdf correctly (or from the page-1
    text), set bulletin_provider other and clear fetch_gap
  retry_when: The filename date parser stops reading month names inside words, or the parish renames its
    files
bulletin_status: available
fetch_gap:
  kind: filename-date-misread
  seen: 2026-11-13
  note: 'fetch:check (page-pdfs on /bulletins/) picks the right file, 11-8-26-martintours.pdf (the 8 November
    issue), but dates it 2026-03-26 from the file name: the date parser reads the ''mar'' of ''martintours''
    as March, so every issue (11-1-26-, 10-25-26-martintours.pdf) gets 2026-03-26 and fails freshness
    as stale. The PDFs download fine.'
  url: https://stmartinamityville.com/wp-content/uploads/2026/11/11-8-26-martintours.pdf
---

## Publisher

St. Martin of Tours, 37 Union Avenue, Amityville publishes its own weekly bulletin, made in Microsoft Publisher (page 1 names a Bulletin Editor, smtbulletin@gmail.com; no printer). The November 8, 2026 issue (`https://stmartinamityville.com/wp-content/uploads/2026/11/11-8-26-martintours.pdf`, read 2026-11-13) has the masthead "The Church of ST. MARTIN OF TOURS, AMITYVILLE, NEW YORK" and one Eucharist Mass Schedule: Monday-Friday 8:30 AM; Saturday Vigil 5:00 PM; Sunday 9:00 AM, 10:30 AM and 12 Noon.

The diocese's Mass-times page (2026-11-12) also lists a Sunday 5:00 PM Mass and Saturday 8:30 AM; the current bulletin lists neither, and it is followed.

## Worship sites

One: the church at 37 Union Avenue (`st-martin-of-tours-amityville-church`). The diocesan locator (directory:124), GCatholic (16806) and the Mass-times page list only this building; the bulletin's schedule names no other place. The parish school (smtschool.org) is listed for its office only.

## Website and bulletin provider

The locator links stmartinamityville.com, the site the bulletin itself names ("Parish Website www.stmartinamityville.com"). Its WordPress `/bulletins/` page lists self-hosted PDFs named `<m>-<d>-<yy>-martintours.pdf`. The Mass-times page links stmartinschurch.net, an older WordPress site whose home page still links a 5 March 2023 bulletin (`3-5-23-martintours.pdf`); it is not used.

`fetch:check` on 2026-11-13 picked the right file with page-pdfs on `/bulletins/` but dated it 2026-03-26 from its name (the parser reads the "mar" of "martintours" as March) and failed it as stale. `probe pdf` on the same URL got RemoteDisconnected; Chrome and fetch:check download it. The row is therefore `unsupported` with `fetch_gap` `filename-date-misread`; the recipe that picks the file is kept in `provider_id`.

## Not yet confirmed

Nothing about the parish or church. See `research` for when to put the row live.
