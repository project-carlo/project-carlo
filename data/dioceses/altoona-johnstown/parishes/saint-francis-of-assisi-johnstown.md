---
name: Saint Francis of Assisi Parish, Johnstown
website: https://www.stfrancisofassisijohnstown.com/bulletin-3/
bulletin_provider: other
provider_id: dated-post https://www.stfrancisofassisijohnstown.com/bulletin-3/
publication: ['url:https://www.stfrancisofassisijohnstown.com/bulletin-3/']
group: ''
evidence:
- url: https://www.stfrancisofassisijohnstown.com/wp-content/uploads/2026/10/Bulletin-October-18-2026.pdf
  seen: '2026-10-21'
  quote: Pastor – Fr. Anthony Francis Spilka, OFMConv.
  note: 'Masthead of the 18 Oct 2026 issue, page 1 (4 pages, text layer): "THE FAITH COMMUNITY OF ST. FRANCIS OF ASSISI", "St. Francis of Assisi, 120 Barron Avenue, Johnstown, PA 15906", rectory 814-539-1632. It names St. Francis alone; Mass schedule "MASS SCHEDULE – Monday – 9:00AM, Tuesday – 6:15PM, Wednesday – Saturday – 9:00AM" and "Saturday Vigil– 4:00PM, Sunday – 7:30AM & 9:30AM". Grep for Gregory, Barnabas, Elue and Clement finds nothing.'
- url: https://www.stfrancisofassisijohnstown.com/bulletin-3/
  seen: '2026-10-21'
  note: 'Parish WordPress site. Its Bulletin page /bulletin-3/ lists one child page per issue (bulletin-october-18-2026, bulletin-october-11-2026, bulletin-october-4-2026, ...), each embedding wp-content/uploads/2026/10/Bulletin-<Month>-<D>-2026.pdf. The server answers HTTP 500 to every request while still rendering the page (verdict HTTP5XX in `probe url`; headed Chrome shows the content); curl gets 406 (Mod_Security).'
- url: https://parishesonline.com/organization/st-francis-of-assisi-church-15906
  seen: '2026-10-21'
  note: '`probe po st-francis-of-assisi-church-15906`: organization "St. Francis of Assisi Church", 120 Barron Ave, website stfrancisofassisijohnstown.com, empty ("this organization does not publish a bulletin here now"): not a channel.'
- url: https://www.dioceseaj.org/parishes/
  seen: '2026-10-21'
  note: 'Directory: Saint Francis of Assisi Parish, Johnstown, 120 Barron Avenue 15906, homepage stfrancisofassisijohnstown.com; Masses Sat 4:00 PM, Sun 11:00 AM, Mon 9:00, Tue 6:15 PM, Wed-Fri 9:00 AM, First Friday 5:00 PM. The directory gives Sunday 11:00 AM; the bulletin gives Sunday 7:30 AM and 9:30 AM (the bulletin is the later source and the parish''s own).'
---

## Publisher

Saint Francis of Assisi (pastor Fr. Anthony Francis Spilka, OFMConv.) publishes its own weekly bulletin as a PDF on its WordPress site, `stfrancisofassisijohnstown.com`, one page per issue under `/bulletin-3/`. The 18 Oct 2026 issue (read 2026-10-21) is headed "THE FAITH COMMUNITY OF ST. FRANCIS OF ASSISI" and carries only this parish's Masses. It is a self-hosted bulletin (`other`, `page-pdfs` recipe on the Bulletin page).

**Shared-bulletin check (batch 15 lead):** the 18 Oct issue contains no mention of Sts. Gregory, Barnabas, Fr. Elue or St. Clement (text-layer grep, 2026-10-21), so it does not carry the no-bulletin Sts. Gregory and Barnabas row.

**Site quirk:** the server returns HTTP 500 (and 406 to plain curl) while still delivering the page body; `probe url` reports HTTP5XX, headed Chrome reads it.

## Worship sites

One: St. Francis of Assisi, 120 Barron Avenue (see `churches/saint-francis-of-assisi-johnstown.md`). The Activity Center at 134 Barron Avenue is a hall, not a Mass site.

## Website and bulletin provider

`other`, recipe `dated-post https://www.stfrancisofassisijohnstown.com/bulletin-3/`: `fetch:check` on 2026-10-21 picked Bulletin-October-18-2026.pdf ("dated-post ...: current"). The unpinned guess (`page-pdfs`) picked a 2021 testimonial PDF listed first, so the recipe is needed. `website` is the Bulletin page; `publication` is that page's URL.
