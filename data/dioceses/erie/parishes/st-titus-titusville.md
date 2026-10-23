---
name: St. Titus Parish
website: https://www.sainttitus.com/
bulletin_provider: parishes_online
provider_id: saint-titus
publication: ['po-org:saint-titus', 'lpi:0018000000QxBk8AAF', 'po-container:14/1175']
group: 'One pastor with St. Joseph, Oil City (clergy PDF 8/7/2026: Hoffman, pastor St. Titus, pastor pro
  tempore St. Joseph); each parish publishes its own bulletin, so two rows'
evidence:
- url: https://container.parishesonline.com/bulletins/14/1175/20261025B.pdf
  seen: 2026-10-23
  quote: 513 West Main Street
  note: 'Page 1 of the 25 October 2026 issue (posted early; 30th Sunday in Ordinary Time), container 14/1175:
    masthead ''Saint Titus Roman Catholic Church'', 513 West Main Street, Titusville, PA 16354, (814)
    827-4636, www.sainttitus.com. One ''Regular Mass Schedule'' (Mon 8:30 AM, Tue 6:30 PM, Wed-Fri 8:30
    AM, Sat 4:30 PM, Sun 8:00 AM and 10:00 AM). It lists no other church. Page 4 footer: ''St. Titus Roman
    Catholic Church, Titusville, PA 14-1175''.'
- url: https://container.parishesonline.com/bulletins/14/1175/20261025B.pdf
  seen: 2026-10-23
  quote: Fr. Dan Hoffman, Pastor
  note: 'Page 2 staff list: ''PASTOR | Fr. Daniel Hoffman, PAROCHIAL VICAR | Fr. Festus Okoye, DEACON
    | Deacon Kevin Harmon''.'
- url: https://www.sainttitus.com/
  seen: 2026-10-23
  note: 'probe url: HTTP 200, embeds lpi:0018000000QxBk8AAF and a /bulletin link. probe po saint-titus:
    org saint-titus, 513 W Main St, Titusville, latest issue 2026-10-25, container 14/1175 (weekly issues
    2025-10-26 to 2026-10-25 all fetched with HTTP 200).'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor, pro tempore
  note: 'Clergy list updated 8/7/2026: ''Hoffman, Rev. Daniel R. Pastor ... St. Titus, Titusville'' and
    ''Pastor, pro tempore ... St. Joseph, Oil City''; ''Okoye, Rev. Festus Parochial Vicar ... 1) St.
    Joseph, Oil City, 2) St. Titus, Titusville''.'
promoted: 2026-10-23
research:
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese erie --parish st-titus-titusville
    --expected-identity Titus --expected-issue-date 2026-10-25
  url: https://container.parishesonline.com/bulletins/14/1175/20261025B.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched, issue date observed (25 October 2026); freshness
    'future' because the issue is posted two days early, which is expected for ParishesOnline.
---

## Publisher

St. Titus Parish publishes its own weekly bulletin through ParishesOnline / LPi: organization `saint-titus` (lpi:0018000000QxBk8AAF), container 14/1175. The 25 October 2026 issue (read 2026-10-23, posted early) is headed 'Saint Titus Roman Catholic Church', 513 West Main Street, Titusville, and prints one Mass schedule, for St. Titus alone. All 53 weekly issues from 26 October 2025 to 25 October 2026 download from the container.

## Shared pastor, separate bulletin (St. Joseph, Oil City)

Fr. Daniel Hoffman is pastor of St. Titus and pastor pro tempore of St. Joseph, Oil City, with one parochial vicar (Fr. Festus Okoye) for both (clergy PDF 8/7/2026). **That does not make one bulletin.** St. Joseph, Oil City prints its own Discover Mass bulletin (number 3172, 18 October 2026, 8 pages, masthead 'St. Joseph Church, 35 Pearl Avenue, Oil City') with its own Mass times and no St. Titus Mass schedule; the St. Titus issue has its own LPi layout. The two bulletins cross-print each other's events: St. Titus's 'Weekly Liturgy Schedule' listed Masses '8:30 AM at St. Joseph' in every issue from 26 October 2025 to 29 March 2026 (none from 5 April 2026, where Holy Week services were also at St. Joseph), and St. Joseph's 18 October 2026 issue advertises parish-directory photo days at both churches. See `st-joseph-oil-city` for its publication_reviews entry.

## Worship sites

- **St. Titus Church, 513 W. Main St., Titusville**: the parish church, with Mass daily and on the weekend.
- **St. Walburga, 120 Brook St., Titusville** and **Immaculate Conception, 17932 Wright Rd., Centerville (Mageetown)**: both are 'secondary church' of St. Titus in the 6 October 2026 printable directory (no Mass times). Neither has a recurring Mass in the 53 issues read (details in their own records): St. Walburga is excluded as `no-public-mass` (one dedication-anniversary Mass advertised for 27 October 2026), Immaculate Conception is in `open/`.

## Website and bulletin provider

`probe url https://www.sainttitus.com/` returns 200 and embeds the LPi id; the site's /bulletin page is the ParishesOnline widget. Provider `parishes_online`, org slug `saint-titus`.

## Not yet confirmed

Nothing about the publisher. Whether the two secondary churches hold any public Mass is in their records.
