---
name: St. Jude the Apostle Parish
website: https://www.saintjude.church
bulletin_provider: discover_mass
provider_id: saint-jude-the-apostle-erie-pa
publication: ['discovermass:saint-jude-the-apostle-erie-pa']
group: 'Erie partnership (decree effective 2024-07-09): St. Jude the Apostle and St. Stephen of Hungary
  / San Esteban (separate pastors per clergy PDF); St. Andrew merged into St. Jude as a secondary mission
  church'
evidence:
- url: https://discovermass.com/church/saint-jude-the-apostle-erie-pa/
  seen: 2026-10-23
  quote: Rev. Joseph Petrone, Pastor
  note: 'Discover Mass church page, bulletin-current for the 25 October 2026 issue (cover class ''bulletin-cover
    X-|2026-10-25|...|3515'', bulletin number 3515). I downloaded the PDF (8 pages) and read it. Page
    1 masthead: ''THE CHURCH BULLETIN / Serving Saint Jude and San Esteban Parishes'', then three address
    blocks: ''Saint Jude Parish Church, Parish Church and Office, 2801 W. 6th Street, Erie, PA 16505'';
    ''Saint Andrew Church, Secondary Mission of Saint Jude, 1116 W. 7th Street, Erie, PA 16502''; ''Parroquia
    de San Esteban, Hispanic Apostolate, 1247 W. 21st Street, Erie, PA 16502''. Page 1 is a cover/contents
    page, with the masthead in the text layer.'
- url: https://discovermass.com/church/saint-jude-the-apostle-erie-pa/
  seen: 2026-10-23
  quote: 12:00 pm San Esteban (Español)
  note: 'Page 2 ''WEEKDAY AND WEEKEND MASS SCHEDULE'' of the 25 Oct 2026 issue: Monday 8am mass - Chapel;
    Wednesday 10:15 School Mass - Church; Thursday 8 am mass - Chapel and 6:15 pm misa - Chapel; Friday
    8 am mass - Chapel; Saturday 4:30 pm Saint Jude; Sunday 7:30 am Saint Jude, 9:00 am Saint Andrew,
    10:30 am Saint Jude, 12:00 pm San Esteban (Español). One combined schedule for all three churches;
    page 4 lists the week''s events at Saint Andrew and San Esteban. Staff block names ''Rev. Michael
    Polinek, Pastor'' for Saint Jude Parish, Saint Andrew Church and, separately, ''Saint Stephen of Hungary
    Parish, Rev. Joseph Petrone, Pastor''.'
- url: https://www.saintjude.church/bulletin/
  seen: 2026-10-23
  quote: READ THE CURRENT BULLETIN
  note: 'St. Jude''s own Bulletin page (WordPress, Divi) hosts no PDF: its READ THE CURRENT BULLETIN button
    goes to https://discovermass.com/church/saint-jude-the-apostle-erie-pa/. The page also embeds a ''Church
    Bulletin Podcast''. So one channel, Discover Mass.'
- url: https://www.hispanicapostolateerie.org
  seen: 2026-10-23
  quote: office@saintjude.church
  note: 'St. Stephen''s own site (diocese-style template, footer ''Diocese of Erie 429 East Grandview
    Blvd.'') has no bulletin link or widget (probe url: no bulletin_links, no publications): its menu
    has only Contact, Join Us, Sacraments, Ways to Give and Child Protection. Its contact block is ''St.
    Stephen of Hungary Parish/La Parroquia de San Esteban, 1237 W. 21st St.'' with St. Jude''s office
    email and phone (814) 833-0927, and Mass Times ''Sunday 12 p.m. (Spanish)'', ''Thursday at 6:15 p.m.
    - St. Jude (Spanish)''.'
- url: https://discovermass.com/church/saint-stephen-of-hungary-erie-pa/
  seen: 2026-10-23
  note: St. Stephen of Hungary's Discover Mass page exists (address 1237 W 21st St., Erie, PA 16502) but
    has no bulletin (page says no bulletins available; no bulletin-cover or bulletin-current). Same for
    https://discovermass.com/church/st-andrew-erie-pa/ (1116 W 7th St.). Neither is a channel.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor .......................................................................................
    St. Stephen of Hungary, Erie
  note: 'Clergy list ''Updated 8/7/2026'': Polinek, Rev. Michael C. is ''Pastor ... St. Jude the Apostle'';
    Petrone (Rev. Joseph A. Petrone Jr.) is ''Pastor ... St. Stephen of Hungary, Erie, c/o St. Jude the
    Apostle, 2801 West Sixth Street'' and also ''Sacramental Assistant ... St. Peter Cathedral, Erie''.
    Deacons Alvarez and Ochalek are assigned to both St. Jude and St. Stephen. The decree says one pastor
    serves both partners; the clergy PDF and the bulletin staff block name two.'
- url: https://www.eriercd.org/images/directoryparishchurch.pdf
  seen: 2026-10-23
  quote: Partnered with St. Stephen of Hungary Parish/La Parroquia de San Esteban
  note: 'Printable directory dated Oct. 6, 2026: St. Jude the Apostle Parish (2801 W. 6th St.) partnered
    with St. Stephen; ''St. Andrew Church Secondary Mission'' under it; St. Stephen of Hungary Parish
    ''Partnered with St. Jude the Apostle Parish, Erie'', mailing address c/o St. Jude, website hispanicapostolateerie.org,
    ''Pastor: Reverend Joseph A. Petrone''. Its Sunday times for St. Jude (7:30, 9, 10:30) and St. Andrew
    (9:15 a.m.) differ from the 25 Oct bulletin (St. Andrew 9:00 am); the bulletin wins.'
- url: https://www.eriercd.org/Parish10310-St-Jude-the-Apostle.html
  seen: 2026-10-23
  note: 'Diocese directory record 10310 (GCatholic church 24525): parish at 2801 W. 6th St., website saintjude.church.
    Record 10315 (GCatholic 24473) St. Andrew Church is a Mission under it (city list: ''secondary church'');
    record 10314 (GCatholic 24559) is St. Stephen of Hungary Parish, ''partnered with St. Jude the Apostle
    Parish''.'
research:
- method: pnpm fetch:check --diocese erie --parish st-jude-the-apostle-erie --expected-identity 'Saint
    Jude' --expected-issue-date 2026-10-25 (headed Chrome)
  url: https://discovermass.com/church/saint-jude-the-apostle-erie-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: None. Transport ok, PDF, identity matched in first-page text; issue date 'unknown' and
    freshness unknown because the masthead date text is split by the layout. The pick is the 25 October
    2026 issue (bulletin 3515) I read.
---

## Publisher

St. Jude the Apostle Parish, Erie publishes one weekly bulletin, "The Church Bulletin", through Diocesan Publications' Discover Mass (church slug `saint-jude-the-apostle-erie-pa`). The 25 October 2026 issue (bulletin number 3515, read on 2026-10-23 from the downloaded PDF) is titled on page 1 "Serving Saint Jude and San Esteban Parishes" and gives address blocks for Saint Jude Parish Church, Saint Andrew Church ("Secondary Mission of Saint Jude") and Parroquia de San Esteban ("Hispanic Apostolate"). It prints one combined Mass schedule for the three churches.

**One row for St. Jude and St. Stephen.** St. Stephen of Hungary / San Esteban is a separate canonical parish (partnered with St. Jude by the decree of 2024-07-09; the clergy PDF gives it its own pastor, Rev. Joseph Petrone, while Rev. Michael Polinek is pastor of St. Jude). It has no bulletin of its own: its website (hispanicapostolateerie.org) has no bulletin link, its Discover Mass page carries no bulletins, and its contact block uses St. Jude's office email and phone. The only publication covering San Esteban is this joint bulletin, whose masthead names it and whose schedule lists its Sunday 12:00 pm Spanish Mass. Per the diocese rule that a partnership is one row only when a current masthead covers each partner, St. Stephen is covered, so there is no separate St. Stephen parish row. Peer review: St. Stephen has no row to compare; the determination is that no separate channel exists (checked: its own site, its Discover Mass page, the St. Jude bulletin page).

## Worship sites

Three churches, all in the bulletin's Mass schedule: St. Jude the Apostle (2801 W. 6th St.; weekday Masses are in its chapel, the Wednesday school Mass in the church), St. Andrew (1116 W. 7th St., Sunday 9:00 am, a secondary mission church under the amended merger decree of 2024-05-29, effective 2024-07-09) and St. Stephen of Hungary / San Esteban (1237 W. 21st St., Sunday 12:00 pm Spanish). The Thursday 6:15 pm Spanish Mass is held at St. Jude's chapel, not at San Esteban.

## Website and bulletin provider

`saintjude.church` (WordPress/Divi) has a Bulletin page whose only bulletin link is the Discover Mass church page, so the channel is `discover_mass` with slug `saint-jude-the-apostle-erie-pa`. The directory's GCatholic website for St. Jude (stjudeapos.org) and for St. Andrew (saintandrewerie.com) both redirect to saintjude.church (St. Andrew's own domain folded in). Discover Mass downloads are capped per IP per day, so each page was read once; the cover class number (3515) is for this slug alone and differs from the cathedral's (3511).

## Not yet confirmed

The Spanish Sunday Mass is shown as held at 'San Esteban' with the church's 1237 W. 21st St. address inferred from the schedule label and the directory; the bulletin gives 1247 W. 21st Street (see the church record).
