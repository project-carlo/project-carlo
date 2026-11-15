---
name: Blessed Sacrament – St. Sylvester
website: https://blessedsacrament-stsylvester.org/bulletins
bulletin_provider: no_bulletin
provider_id: ''
publication: ['url:https://blessedsacrament-stsylvester.org/bulletins']
group: Deanery B6 (Brooklyn East)
evidence:
- url: https://blessedsacrament-stsylvester.org/bulletins
  seen: 2026-11-06
  quote: Bulletin for Sunday, Aug 02, 2026
  note: 'Tilma bulletins page, newest card first: ''Bulletin for Sunday, Aug 02, 2026'', then Jul 26,
    Jul 19, Jul 12, Jul 05, Jun 28, Jun 21 (31 cards). The resource tokens decode to upload dates 2026/07/06,
    07/09, 07/29 and 08/03: weekly-to-three-weekly uploads that stopped after 3 August 2026.'
- url: https://files.tilmaplatform.com/system/resources/W1siZiIsIjIwMjYvMDgvMDMvMnNweDZ4YXJ6OV9CbFNhY0JrbHluOF8yLnBkZiJdXQ/BlSacBklyn8-2.pdf
  seen: 2026-11-06
  quote: Parish of Blessed Sacrament
  note: 'Newest posted issue, 2 August 2026 (8 pages, self-made: no LPi, John Patrick or Church Bulletin
    Inc. mark). Page 1 masthead names both churches: ''Blessed Sacrament 198 Euclid Avenue'' and ''Saint
    Sylvester 265 McKinley Avenue'', each with its own Mass*Misas schedule; ''Rev . Jose Henríquez, Pastor'';
    ''August 02, 2026''. Page 2 gives ''Mass Intentions @ Saint Sylvester'' and ''Mass Intentions @ Blessed
    Sacrament''.'
- url: https://parishesonline.com/organization/blessed-sacrament-church-11208
  seen: 2026-11-06
  note: 'probe po: org ''Blessed Sacrament Church'', 198 Euclid Ave, has no issues; st-sylvester-church-11208
    (''St. Sylvester Church'', 265 McKinley Ave.) has none either. Empty orgs, not publication ids. blessed-sacrament-st-sylvester,
    blessed-sacrament-st-sylvester-church-11208 and blessed-sacrament-roman-catholic-church-11208 don''t
    exist.'
- url: https://blessedsacrament-stsylvester.org/mass-times
  seen: 2026-11-06
  quote: St. Sylvester Mass Times
  note: The site's Mass Times page lists current schedules for both Blessed Sacrament and St. Sylvester.
revisit: Check the Tilma /bulletins page for a card newer than 2 August 2026; if current, set other with
  page-pdfs https://blessedsacrament-stsylvester.org/bulletins and run fetch:check.
revisit_after: 2026-12-06
research:
- method: Read the Tilma /bulletins page, homepage and /announcements; decoded upload stamps; probe po
    on blessed-sacrament-church-11208, st-sylvester-church-11208 and slug variants; fetch:check with page-pdfs
    on /bulletins
  url: https://blessedsacrament-stsylvester.org/bulletins
  checked: '2026-11-06'
  outcome: not-found
  next_action: Reread /bulletins for a card newer than 2 August 2026 and probe po blessed-sacrament-church-11208
    for issues; if the Tilma page is current again, set bulletin_provider other with recipe page-pdfs
    https://blessedsacrament-stsylvester.org/bulletins and run fetch:check (on 2026-11-06 it picked the
    2 August issue, freshness stale, 96 days).
  retry_when: After 2026-12-06, or when the parish site shows a new bulletin card
  revisit_after: 2026-12-06
bulletin_status: not-found
---

## Publisher

The parish self-publishes one weekly bulletin for both its churches on its Tilma site, but the newest card on `/bulletins` (read 2026-11-06) is "Bulletin for Sunday, Aug 02, 2026": nothing has been posted for three months. I read that issue (8 pages, no publisher mark): the page 1 masthead names "Blessed Sacrament 198 Euclid Avenue" and "Saint Sylvester 265 McKinley Avenue", each with its own Mass schedule, under one staff (Rev. Jose Henríquez, Pastor), and page 2 carries Mass intentions for both churches. The upload stamps (2026/07/06 to 2026/08/03) show irregular weekly uploads that then stopped.

## Worship sites

Two churches, both with Mass now, which answers the directory's two phone lines: Blessed Sacrament, 198 Euclid Avenue (Sunday 8:30, 9:45, 11:15, 12:45; Saturday 7:15pm Spanish; weekdays 8:30am and 7:15pm), and St. Sylvester (Saturday 5:30pm bilingual, Sunday 10:00am Spanish, weekdays 9:30am). The 2 August bulletin and the site's current Mass Times page (read 2026-11-06) give these schedules. The Mass finder's place 201 lists both under "All Worship Sites"; it is a lead, not schedule evidence.

## Website and bulletin provider

`no_bulletin`, following the playbook for a months-stale Tilma page: `fetch:check` with `page-pdfs https://blessedsacrament-stsylvester.org/bulletins` (2026-11-06) picked the 2 August issue and reported freshness stale (96 days). ParishesOnline has empty orgs for both churches (`blessed-sacrament-church-11208`, `st-sylvester-church-11208`), and the old domain blessedsacrament-brooklyn.org that the Blessed Sacrament org names no longer resolves (DEAD-DNS). When an issue is posted again, the row is `other` with that recipe (see research).

## Not yet confirmed

Whether the parish still prints a bulletin it no longer posts (or posts it elsewhere, such as social media, not checked): recheck after 2026-12-06.
