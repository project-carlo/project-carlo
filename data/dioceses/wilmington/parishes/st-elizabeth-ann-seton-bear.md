---
name: St. Elizabeth Ann Seton
website: https://setonparish.net/
bulletin_provider: ecatholic
provider_id: '35332'
publication: ['ecatholic:35332']
group: Iron Hill Deanery
evidence:
- url: https://files.ecatholic.com/35332/bulletins/20261025.pdf
  seen: 2026-10-27
  quote: St. Elizabeth Ann Seton Parish 345 Bear Christiana Road; Bear , DE 19701
  note: 'Page 1 of the 25 October 2026 issue (6 pages, text layer): ''PASTOR: Fr. Norman Carroll'', ''Deacon
    William P. Kibler, Pastoral Associate'', ''MASS SCHEDULE: Mon, Wed & Thu: 8:30am  Tue: 6:30pm  Sat:
    4:00pm  Sun: 8:00am 10:30am'', ''Christ the Teacher School / PreK3-8, 2451 Frazer Road''. Names this
    parish alone.'
- url: https://setonparish.net/
  seen: 2026-10-27
  quote: Weekly Bulletins
  note: 'Browser (probe url gets HTTP 403): the home page embeds ecatholic:35332 and links https://setonparish.net/bulletins.'
- url: https://setonparish.net/mass-times
  seen: 2026-10-27
  quote: '1ST FRIDAY:'
  note: 'Mass Times page (browser): Saturday 4:00 PM; Sunday 8:00 AM, 10:30 AM; Monday 8:30 AM; Tuesday
    6:30 PM; Wednesday 8:30 AM; Thursday 8:30 AM; first Friday 9:00 AM.'
---

## Publisher

St. Elizabeth Ann Seton, Bear publishes its own weekly bulletin on its eCatholic site (id 35332). The 25 October 2026 issue (files.ecatholic.com/35332/bulletins/20261025.pdf, 6 pages, readable text) carries this parish's letterhead and Fr. Norman Carroll as pastor, with its Mass schedule on page 1; nothing in it names another parish. It is a separate parish from St. Joseph, Middletown (a different bulletin, no mention on either).

## Worship sites

One church, 345 Bear Christiana Road, Bear (see `churches/st-elizabeth-ann-seton-bear.md`). The diocese's directory and GCatholic list this one place and no mission.

## Website and bulletin provider

eCatholic: setonparish.net embeds site 35332 and its Weekly Bulletins page; issues are `files.ecatholic.com/35332/bulletins/<YYYYMMDD>.pdf` one per Sunday (the 1 November file answers 403, not yet posted; 25 October is the latest). The site answers 403 to curl and `probe url` and loads in the browser.

## Fetch check

`pnpm fetch:check --diocese wilmington --parish st-elizabeth-ann-seton-bear` (2026-10-27): picked files.ecatholic.com/35332/bulletins/20261025.pdf (1.8 MB); transport ok, document type PDF, freshness fresh. The tool leaves identity 'unverified'; the page 1 letterhead read above settles it.

## Not yet confirmed

Nothing outstanding. The directory shows 'Fri 09:00' as a weekly Mass; the parish's Mass Times page says first Friday only, and the bulletin lists no Friday Mass.
