---
name: St. Joseph, St. Mary and St. Michael Parishes
website: https://www.watch4deercatholic.church/bulletins
bulletin_provider: other
provider_id: page-pdfs https://www.watch4deercatholic.church/bulletins
publication: ['url:https://www.watch4deercatholic.church/bulletins#st-joseph-lucinda']
group: 'Partnered (decree 2023-10-30): St. Joseph, Lucinda; St. Mary, Crown; St. Michael, Fryburg; one
  pastor, Very Rev. Brandon Kleckner'
evidence:
- url: https://www.watch4deercatholic.church/_files/ugd/652cd4_13fd3a7e73404cec94add8fe58972a01.pdf
  seen: 2026-10-23
  quote: 'Mailing Address: P.O. Box 9, Lucinda, PA, 16235 • (814) 226-7288'
  note: 'Issue of 4 October 2026 (27th Sunday of Ordinary Time; the bulletins page''s link text is ''10-4-26''),
    page 1 masthead: ''Saint Joseph Parish, Lucinda, PA / Saint Mary Parish, Crown, PA / Saint Michael
    Parish, Fryburg, PA / Saint Ann Mission, Marienville, PA / www.watch4deercatholic.church''. The names
    sit in two columns, so the quote is the clean line below them. Text-layer PDF, 8 pages (PDF producer
    metadata: John Patrick Publishing). The same page 1 carries ''Fr. Brandon Kleckner, Pastor'' and a
    joint stewardship box (''Saint Joseph: $2,970 / Saint Michael: $2,581 / Saint Mary: $2,612'').'
- url: https://www.watch4deercatholic.church/_files/ugd/652cd4_ab7e5ca270e74ef49351928140f62e69.pdf
  seen: 2026-10-23
  note: 'Issue of 18 October 2026 (29th Sunday of Ordinary Time, link text ''10-18-26'', PDF created 2026-10-15),
    the newest on the bulletins page. Image-only PDF (no text layer): page 1 rendered at 60 dpi shows
    the same four-name masthead (''Saint Joseph Parish Lucinda, PA / Saint Mary Parish Crown, PA / Saint
    Michael Parish Fryburg, PA / Saint Ann Mission Marienville, PA / www.watch4deercatholic.church / 29th
    Sunday of Ordinary Time''); page 3 shows one Mass Intentions box for all four churches.'
- url: https://www.watch4deercatholic.church/bulletins
  seen: 2026-10-23
  note: Wix page, HTML lists 26 PDF links in `_files/ugd/652cd4_*.pdf`, grouped by month, link text a
    date (10-4-26, 10-11-26, 10-18-26, 9-6-26 ... 5-31-26), newest month first but dates ascending within
    a month. One list for the whole partnership; no per-church lists.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  note: 'Clergy list updated 8/7/2026 (read by the surveyor, see diocese.md): Kleckner is pastor of Fryburg,
    Lucinda and Crown. The bulletin staff box names ''Fr. Brandon Kleckner, Pastor'' and ''Fr. John Nwankwo,
    Parochial Vicar''.'
promoted: 2026-10-23
research:
- method: fetch:check --diocese erie --parish st-joseph-lucinda (page-pdfs recipe on the bulletins page)
  url: https://www.watch4deercatholic.church/bulletins
  checked: '2026-10-23'
  outcome: found
  next_action: None. Identity and issue date read 'unknown' to the checker only because the 18 October
    issue has no text layer; the masthead and date were read from the rendered pages.
  retry_when: If the checker's pick stops being the newest dated link (the page sorts dates ascending
    within a month), re-read the page order
bulletin_status: available
---

## Publisher

One bulletin covers all four places. The 4 October 2026 issue (page 1) and the 18 October 2026 issue (page 1, rendered) carry one masthead naming 'Saint Joseph Parish, Lucinda', 'Saint Mary Parish, Crown', 'Saint Michael Parish, Fryburg' and 'Saint Ann Mission, Marienville' with www.watch4deercatholic.church, one pastor (Fr. Brandon Kleckner) and a single Mass Intentions box that lists every Mass at every church. The three parishes were partnered by decree of 2023-10-30 (batch plan; the decree itself was not re-read here). The directory gives all three the same website and phone, (814) 226-7288. One row, `group` records the partnership.

The Discover Mass page for Lucinda says no bulletins (diocese.md), so the parish site is the only channel. No per-parish bulletin exists on the site: the bulletins page has one list.

## Worship sites

Four churches have public Mass in the current bulletin: St. Joseph, Lucinda (Sat 4 pm in even months, Sun 9:30 am, Fri 8:30 am); St. Mary, Crown/Leeper (Sat 6 pm, Sun 8 am, Mon and Wed 8:30 am); St. Michael, Fryburg (Sun 11 am, Sat 4 pm in odd months, Tue and Thu 8:30 am); St. Ann Mission, Marienville (Thu 6 pm). St. Ann is the mission of St. Mary in the diocese's city list ('secondary mission church' under St. Mary Parish (Crown)); it has no parish row of its own. No other church of the three parishes appears in the bulletin's Mass Intentions or on the parish site's Church Addresses page (which lists the four).

## Website and bulletin provider

`other`, recipe `page-pdfs https://www.watch4deercatholic.church/bulletins` (Wix site; the PDFs are plain `_files/ugd/` links in the page HTML, no browser needed). `fetch:check` on 2026-10-23 picked the 18 October 2026 issue (4.6 MB, `ok`, `pdf`), which is the current bulletin; its identity and issue date report 'unknown' to the checker because the PDF is scanned images (the 4 October and earlier issues have text layers, mostly; 11 October is also image-only). The directory lists the home page (watch4deercatholic.church) as the website; the bulletins page is stored so the recipe has a stable list.

## Not yet confirmed

Image-only issues mean automatic masthead and date checks can't confirm identity or freshness; the issue list on the page is the freshness evidence. Mass counts in odd and even months alternate between St. Joseph and St. Michael on Saturdays at 4 pm (directory) and should be read in a bulletin for the month needed.
