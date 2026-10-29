---
name: Holy Innocents Parish
website: https://www.holyinnocentsrc.org
bulletin_provider: other
provider_id: page-pdfs https://www.holyinnocentsrc.org/bulletin
publication: ['url:https://www.holyinnocentsrc.org/bulletin']
group: ''
evidence:
- url: https://www.holyinnocentsrc.org/s/2026_10_25.pdf
  seen: 2026-10-29
  note: '25 October 2026 issue (12 pages; page 1 has a garbled text layer, so read from a render at 70
    dpi; page 2 and later have text, page 10 is an image). Cover: ''Holy Innocents Parish, 1337 E. Hunting
    Park Ave. Philadelphia, PA 19124'', Rectory 215-743-2600, Pastor Rev. Thomas M. Higgins. MASS SCHEDULE
    box: Saturday vigil 4:30 PM (English) and 6:30 PM (Spanish); Sunday 7:30 AM and 10:00 AM, 12:00 PM
    (Spanish), 5:00 PM (Vietnamese); ''At St. Joan of Arc Worship Site: 9:00 AM (English), 11:30 AM (Spanish)'';
    Holy Days; weekdays 6:30 AM and 8:00 AM. Footer: ''Worship Site St. Joan of Arc: 3546 Frankford Ave.,
    Phila., PA 19134 Phone: 215-535-4641'' and ''Holy Innocents is the current Parish Site for the former
    Ascension of Our Lord, St. Joachim, and Mater Dolorosa Parishes''. No Mass line names St. Joachim
    or Mater Dolorosa.'
- url: https://www.holyinnocentsrc.org/bulletin
  seen: 2026-10-29
  quote: Click the cover image below to view the current week's bulletin.
  note: Squarespace page; its PDF links are /s/2026_MM_DD.pdf, one per Sunday of 2026 (2026_01_04 to 2026_11_01
    listed as dates in the archive menu), the cover image for 'Sunday, November 1, 2026' on top. The archive
    links are not in date order in the page source, so the recipe's first link needs the fetch check.
- url: https://www.holyinnocentsrc.org/massschedule
  seen: 2026-10-29
  quote: 'At St. Joan of Arc Worship Site: 9:00 AM (English) 11:30 AM (Spanish)'
  note: Parish Mass Schedule page, matching the 25 October bulletin box.
- url: https://archphila.org/parish/holy-innocents-philadelphia/
  seen: 2026-10-28
  quote: 'Worship Site: St. Joan of Arc Church'
  note: 'Directory page (updated 3 months before): L St. and Hunting Park Ave., rectory 1337 E. Hunting
    Park Ave. 19124-4938, website holyinnocentsrc.org, Pastor Rev. Thomas M. Higgins; Mass times as the
    bulletin.'
promoted: 2026-10-29
bulletin_status: available
---

## Publisher

Holy Innocents publishes its own weekly PDF on its Squarespace site (`/bulletin`, files `/s/2026_MM_DD.pdf`), not through John Patrick Publishing: no listing for it is in `raw/jppc-pa.json` (listing 221, 'Saint Joachim Catholic Church', 19124, belongs to a merged parish and has no editions). The row is `other`, `page-pdfs` on the site's bulletin page.

## Worship sites

Two with Mass in the current bulletin: the parish church (Hunting Park Ave.) and the St. Joan of Arc worship site (3546 Frankford Ave., 19134; Sunday 9:00 AM English and 11:30 AM Spanish). St. Joachim (Church St.) and Mater Dolorosa (Ruan St.) appear on the cover only as former parishes merged in 2013 (Ascension of Our Lord too, 2012, whose church is outside this batch). Mater Dolorosa's church was relegated in 2016 (excluded); St. Joachim's church is undecided (open). See those records.

## Fetch check

`fetch:check` (2026-10-29) with `page-pdfs` on `/bulletin` picked `/s/2026_11_01.pdf`, next Sunday's issue posted early (the page's top cover reads 'Sunday, November 1, 2026'): transport ok, PDF, 12 pages, page 2 text is Holy Innocents' parish information. Identity `unverified` (no expected identity supplied) and issue date/freshness `unknown`, because the file name `2026_11_01` has underscores the date reader does not take, so a later check can't tell a stale pick from a current one; the page lists newest first and the 25 October file is the previous Sunday's. It printed no `recipe` line, as `provider_id` already holds it.
