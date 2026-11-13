---
name: St. Pius V (Jamaica)
website: https://stpiusv-queens.org/
bulletin_provider: no_bulletin
provider_id: ''
publication: []
group: Deanery Q9 (Queens East)
evidence:
- url: https://stpiusv-queens.org/system/resources/W1siZiIsIjIwMjYvMDUvMjIvMzEwb3g4Y3FnY19CdWxsZXRpbl8wNV8yNF8yMDI2LnBkZiJdXQ/Bulletin%2005-24-2026.pdf
  seen: 2026-11-06
  quote: Saint Pius V Roman Catholic Church      stpiusv-queens.org
  note: 'Newest bulletin on the site: 24 May 2026 issue, 2 pages, text. Page 1: ''106 –12 Liverpool Street,
    Jamaica, NY 11435'', Father Jose Carlos Da Silva, Pastor; Mass intentions Sunday Portuguese 8:30am,
    English 10:00am, Spanish 11:30am, weekdays 8:00 am, Thursday also 7:30 pm. No publisher footer: an
    in-house layout.'
- url: https://stpiusv-queens.org/bulletins
  seen: 2026-11-06
  quote: May 24, 2026
  note: 'Tilma bulletins page (server-rendered ''Download Bulletin'' cards, newest first): May 24, May
    17, May 10, May 03, April 26, 2026 ... back to January 2026. Nothing after 24 May 2026 is posted.'
- url: https://stpiusv-queens.org/
  seen: 2026-11-06
  quote: '{ time: ''10:00 AM'', language: ''English'', type: ''Sunday Mass'' },'
  note: 'Homepage Mass-times script: Sunday 8:30 AM Portuguese, 10:00 AM English, 11:30 AM Spanish; Monday-Saturday
    8:00 AM English; Thursday also 7:30 PM Spanish.'
revisit: Check stpiusv-queens.org/bulletins for an issue after 24 May 2026; if weekly issues resume, record
  other with recipe page-pdfs https://stpiusv-queens.org/bulletins and run fetch:check
revisit_after: 2027-01-15
research:
- method: probe url and probe get of the Tilma homepage and /bulletins page; probe pdf of the newest issue
  url: https://stpiusv-queens.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Re-read /bulletins for an issue newer than 24 May 2026; if found, set bulletin_provider
    other with provider_id 'page-pdfs https://stpiusv-queens.org/bulletins' and run fetch:check
  retry_when: A bulletin card dated after 24 May 2026 appears, or after 2027-01-15
- method: Discover Mass church page discovermass.com/church/st-pius-v-jamaica-ny/
  url: https://discovermass.com/church/st-pius-v-jamaica-ny/
  checked: '2026-11-06'
  outcome: not-found
  next_action: Check the parish's social media (not read) for posted bulletins
  retry_when: After 2027-01-15
bulletin_status: not-found
---

## Publisher

St. Pius V printed its own in-house bulletin, posted on its Tilma site: the 24 May 2026 issue (read 2026-11-06) has "Saint Pius V Roman Catholic Church stpiusv-queens.org", 106-12 Liverpool Street, Jamaica, Father Jose Carlos Da Silva, Pastor, and no publisher footer. The /bulletins page lists weekly issues from January to 24 May 2026 and nothing since, so on 6 November 2026 the newest posted issue is over five months old. The row is `no_bulletin` until issues resume.

## Worship sites

One church. The 24 May 2026 issue's intentions are at Sunday 8:30am (Portuguese), 10:00am (English), 11:30am (Spanish), weekdays 8:00 am and Thursday 7:30 pm; the homepage's current Mass-times script (read 2026-11-06) gives the same Sunday Masses, Monday-Saturday 8:00 AM and Thursday 7:30 PM Spanish. The diocese's parish and deanery directories, GCatholic 16766 and Mass finder place 907 list only this church.

## Website and bulletin provider

`no_bulletin`. stpiusv-queens.org is the directory's link and the bulletin's website, a Tilma site whose server-rendered /bulletins page shows "Download Bulletin" cards newest first. Following the playbook's lesson for a stale Tilma page, the row is not given the `page-pdfs` recipe now (fetch:check would pass the five-month-old file with freshness unknown); the recipe is kept in research. discovermass.com has no page for the parish (404).

## Not yet confirmed

Whether the parish still prints a weekly bulletin and posts it elsewhere (Facebook and other social media were not read). See research for the retry.
