---
name: Sacred Heart Parish
website: http://www.trentonsacredheart.org/
bulletin_provider: other
provider_id: page-pdfs http://www.trentonsacredheart.org/weekly-bulletin/
publication: ['url:http://www.trentonsacredheart.org/weekly-bulletin/']
group: Cohort 9
evidence:
- url: http://www.trentonsacredheart.org/storage/November%201%202026.pdf
  seen: 2026-10-30
  quote: HOLY CROSS CHURCH, 233 ADELINE STREET, TRENTON, NEW JERSEY 08611
  note: '1 November 2026 issue, 6 pages, text layer. Page 1 masthead: ''SACRED HEART PARISH FOUNDED 1814'',
    ''SACRED HEART CHURCH, 343 SOUTH BROAD STREET, TRENTON, NEW JERSEY 08608'' and ''HOLY CROSS CHURCH,
    233 ADELINE STREET''; pastor Rev. Msgr. Dennis A. Apoldite. SACRED HEART CHURCH: Monday, Tuesday,
    Wednesday and Friday 12:10 Noon, Saturday 5:15 PM, Sunday 9:00 and 11:15 AM. HOLY CROSS CHURCH: Saturday
    4:00 PM, Sunday 10:00 AM, 12:00 Noon Polish. Mass intentions use ''SH'' and ''HC'' for the two churches.'
- url: http://www.trentonsacredheart.org/weekly-bulletin/
  seen: 2026-10-30
  quote: /storage/November 1 2026.pdf
  note: Weekly Bulletin page of the parish's own site (the page's href; it lists dated PDFs newest first,
    1 November back to 13 August 2026).
- url: http://www.trentonsacredheart.org/worship-schedule/
  seen: 2026-10-30
  quote: Holy Cross Church
  note: 'Worship Schedule: Sacred Heart Church Saturday 5:15 pm, Sunday 9:00 am and 11:15am, weekdays
    Monday, Tuesday, Wednesday & Friday 12:10pm; Holy Cross Church Saturday 4:00 pm, Sunday 10:00 Gospel
    Mass, 12:00 Noon Polish Mass.'
research:
- method: probe url and probe get on the site's Weekly Bulletin page; probe pdf on the 1 November 2026
    issue; fetch:check
  url: http://www.trentonsacredheart.org/weekly-bulletin/
  checked: '2026-10-30'
  outcome: found
  next_action: None.
- method: pnpm fetch:check --diocese trenton --parish sacred-heart-trenton (headed Chrome); page-pdfs
    on /weekly-bulletin/
  url: http://www.trentonsacredheart.org/weekly-bulletin/
  checked: '2026-10-30'
  outcome: found
  next_action: It picked 'November 1 2026.pdf' (the 1 November 2026 issue, the coming Sunday's, freshness
    'future'); document type pdf; identity left 'unverified' by the tool (no expected identity), read
    by hand from the masthead. Recipe recorded in provider_id.
bulletin_status: available
publication_reviews:
- parish: our-lady-of-good-counsel-west-trenton
  decision: separate
  evidence:
  - url: http://www.trentonsacredheart.org/storage/November%201%202026.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Parish alone (pastor Rev. Msgr. Dennis A. Apoldite),
      with its own Mass schedule for Sacred Heart and Holy Cross churches.
  - url: https://www.church-bulletin.org/bulletin/our-lady-of-good-counsel-west-trenton-nj-08628/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (rendered page 1) names Our Lady of Good Counsel alone (pastor
      Fr. Ariel Robles, 137 West Upper Ferry Road), with its own Mass schedule. (John Patrick 533)
- parish: incarnation-st-james-ewing
  decision: separate
  evidence:
  - url: http://www.trentonsacredheart.org/storage/November%201%202026.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Parish alone (pastor Rev. Msgr. Dennis A. Apoldite),
      with its own Mass schedule for Sacred Heart and Holy Cross churches.
  - url: https://container.parishesonline.com/bulletins/04/0399/20261101B.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Incarnation-St. James Parish alone (pastor Fr. Stanley DeBoe,
      O.SS.T.), with its own Mass schedule for Incarnation and St. James churches. (ParishesOnline 04/0399)
- parish: st-hedwig-trenton
  decision: separate
  evidence:
  - url: http://www.trentonsacredheart.org/storage/November%201%202026.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead names Sacred Heart Parish alone (pastor Rev. Msgr. Dennis A. Apoldite),
      with its own Mass schedule for Sacred Heart and Holy Cross churches.
  - url: https://www.church-bulletin.org/bulletin/saint-hedwig-parish-trenton-nj-08638/2026-11-01.pdf
    seen: 2026-10-30
    note: The 1 November 2026 masthead (page 2) names Saint Hedwig Parish alone (pastor Rev. Can. Dr.
      Jacek W. Labinski, 872 Brunswick Ave.), with its own Mass schedule. (John Patrick 592)
---

## Publisher

Sacred Heart Parish, Trenton, Cohort 9 (July 2024 list; the 2017 numbering had it in Cohort 10), publishes its own bulletin as dated PDFs on its own site (/weekly-bulletin/, files under /storage/). The 1 November 2026 masthead names Sacred Heart Parish alone, with two churches (quoted in the evidence). It has no John Patrick listing or other printer's page.

The parish absorbed two others in the 2017 decisions (https://dioceseoftrenton.org/decisions, read 2026-10-30): Divine Mercy ("Merger Model of Divine Mercy and Sacred Heart, no later than July 1, 2017") and Blessed Sacrament-Our Lady of the Divine Shepherd ("Merger Model ... with Sacred Heart, no later than July 1, 2018, with Gospel Mass transferred to Sacred Heart"). The Monitor reported both ("Last year, Sacred Heart Parish merged with Divine Mercy Parish and the merger resulted in Sacred Heart Parish having two worship sites ... Sacred Heart and Holy Cross Church", and the Bellevue Avenue church's closing, 'Trenton faithful look ahead to a new day', event date 2018; the site's REST date is the 2019-07-29 migration).

## Worship sites

Two churches with public Mass in the current bulletin: Sacred Heart, 343 South Broad Street (`sacred-heart-trenton`) and Holy Cross, 233 Adeline Street (`holy-cross-trenton`, which is GCatholic's 'Divine Mercy'). Not here: Blessed Sacrament-Our Lady of the Divine Shepherd, 716 Bellevue Avenue (`excluded/blessed-sacrament-olds-trenton`, closed 2018). The 1 November bulletin's sacramental-records list still names "Blessed Sacrament Church, Our Lady of Divine Shepherd Church, ... and Divine Mercy Parish" as record-holders, which isn't a Mass listing.

## Website and bulletin provider

The row reads the site's Weekly Bulletin page (`page-pdfs`). File names carry the date and some extras ("October 18 2026 - for web.pdf", "CYO THANK YOU - pdf.pdf"): see research for what `fetch:check` picked.
