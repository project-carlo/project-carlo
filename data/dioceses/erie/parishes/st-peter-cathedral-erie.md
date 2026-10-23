---
name: St. Peter Cathedral Parish
website: https://www.stpetercathedral.com
bulletin_provider: discover_mass
provider_id: saint-peter-erie-pa
publication: ['discovermass:saint-peter-erie-pa']
group: ''
evidence:
- url: https://discovermass.com/church/saint-peter-erie-pa/
  seen: 2026-10-23
  quote: Mass Intentions
  note: 'Discover Mass church page ''Saint Peter Cathedral'' (230 W 10th St., Erie, PA 16501): bulletin-current
    is the 25 October 2026 issue, cover class ''bulletin-cover X-|2026-10-25|...|3511'' (bulletin number
    3511). I downloaded the PDF (8 pages) and read it. Page 1 is an image-only cover (rendered at 60 dpi):
    ''St. Peter Cathedral / THIRTIETH SUNDAY IN ORDINARY TIME / October 25, 2026''. Pages 4-8 are the
    cathedral''s own: Mass Intentions for 26 Oct-1 Nov at 6:30, 8:00, 12:10 and 5:15 weekdays, Saturday
    8:00 am and 4:00 pm, Sunday 6:30, 8:30, 11:00; ''From the Rector''s Desk''; staff list.'
- url: https://discovermass.com/church/saint-peter-erie-pa/
  seen: 2026-10-23
  quote: Very Rev. Michael P. Ferrick, V.F.
  note: 'Staff block of the 25 Oct 2026 issue: ''Cathedral Rectory Office, 230 West 10th Street, Erie,
    PA 16501, 814-453-6677''; ''Most Rev. Lawrence T. Persico J.C.L. ... Bishop of Erie''; ''Very Rev.
    Michael P. Ferrick, V.F. ... Rector''; ''Rev. Joe Petrone ... in Residence''. Content concerns the
    cathedral only (no partner parish is named).'
- url: https://www.stpetercathedral.com/
  seen: 2026-10-23
  note: 'Cathedral''s own WordPress/Avada home page embeds the current bulletin cover (dpi_bulletin_cover_wrapper)
    linking to a bulletins.discovermass.com download; no PDF of its own and no other bulletin link (curl
    of the home page, grep ''bulletin''). One channel: Discover Mass.'
- url: https://www.eriercd.org/Parish10317-St-Peter-Cathedral.html
  seen: 2026-10-23
  note: 'Diocese directory record 10317: St. Peter Cathedral Parish, 230 W. 10th St., Erie, PA 16501,
    website http://www.stpetercathedral.com, one parish record with no partner or secondary church (locator_group_id
    10317).'
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Rector .............................................................................................
    St. Peter Cathedral, Erie
  note: 'Clergy list ''Updated 8/7/2026'': Ferrick, VF, Very Rev. Michael P. is Rector, St. Peter Cathedral.
    Rev. Joseph A. Petrone Jr., pastor of St. Stephen of Hungary, is also ''Sacramental Assistant ...
    St. Peter Cathedral''; that does not make the bulletins shared (the cathedral bulletin names no San
    Esteban).'
research:
- method: pnpm fetch:check --diocese erie --parish st-peter-cathedral-erie --expected-identity Ferrick
    --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://discovermass.com/church/saint-peter-erie-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok (2,928,552 bytes), document type PDF, the same file I read. Identity
    and issue date report 'unknown' only because page 1 is an image-only cover (no extractable text);
    I rendered it and read 'St. Peter Cathedral ... October 25, 2026'. A recurring unknown here is expected;
    rendering page 1 is the check.
publication_reviews:
- parish: st-jude-the-apostle-erie
  decision: separate
  evidence:
  - url: https://discovermass.com/church/saint-peter-erie-pa/
    seen: 2026-10-23
    quote: Very Rev. Michael P. Ferrick, V.F.
    note: '25 Oct 2026 cathedral issue (number 3511): cathedral cover and staff, cathedral Mass intentions
      only.'
  - url: https://discovermass.com/church/saint-jude-the-apostle-erie-pa/
    seen: 2026-10-23
    quote: 12:00 pm San Esteban (Español)
    note: '25 Oct 2026 St. Jude issue (number 3515): masthead ''Serving Saint Jude and San Esteban Parishes'';
      schedule for Saint Jude, Saint Andrew and San Esteban only. Different numbers, covers, staff and
      schedules.'
---

## Publisher

St. Peter Cathedral Parish, Erie publishes its own weekly bulletin through Diocesan Publications' Discover Mass (church slug `saint-peter-erie-pa`; its own site embeds the same channel). I read the 25 October 2026 issue (bulletin number 3511) on 2026-10-23: the image-only cover reads 'St. Peter Cathedral, Thirtieth Sunday in Ordinary Time, October 25, 2026' and the staff block names 'Very Rev. Michael P. Ferrick, V.F. ... Rector' at 230 West 10th Street. The content is about the cathedral alone.

**Not the St. Jude bulletin.** The cathedral is a separate parish with its own rector; Rev. Joseph Petrone (pastor of St. Stephen of Hungary, which shares the St. Jude bulletin) is a sacramental assistant here and 'in Residence' in the staff list, but this masthead and Mass schedule name only the cathedral and the St. Jude issue (number 3515) names only Saint Jude, Saint Andrew and San Esteban. Two issues, two mastheads, one Sunday.

## Worship sites

One church, the cathedral at 230 W. 10th St. The issue's schedule lists weekday Masses at 6:30 am, 8:00 am, 12:10 pm and 5:15 pm, Saturday 8:00 am and 4:00 pm (vigil), Sunday 6:30 am, 8:30 am and 11:00 am, matching the diocese directory. No other building is named for Mass. GCatholic lists the cathedral as church 2523 (https://gcatholic.org/churches/northamerica/2523), outside its Erie roster export, which is why no roster entry carries it.

## Website and bulletin provider

`stpetercathedral.com` (WordPress/Avada; directory `http://` redirects to https) embeds the Discover Mass cover and download for the current issue, so the provider is `discover_mass` with slug `saint-peter-erie-pa`. Discover Mass downloads are capped per IP per day, so the page was read once.

## Not yet confirmed

Nothing open for the row itself.
