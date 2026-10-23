---
name: St. Thomas the Apostle Parish
website: https://www.thomastheapostle.net
bulletin_provider: parishes_online
provider_id: saint-thomas-the-apostle-parish
publication: ['po-org:saint-thomas-the-apostle-parish', 'lpi:0018000000Qc2VYAAZ', 'po-container:14/0675',
  'po-org:christ-the-light-of-the-world-st-joseph-st-agnes-holy-trinity-parishes', 'lpi:0018000000Qx7pfAAB',
  'po-org:st-maximilian-kolbe-and-st-agnes-church', 'lpi:0018000000Qx7s0AAB', 'po-org:st-rita-church-15120',
  'lpi:0018000000Qx7s1AAB', 'po-org:holy-trinity-church-15122', 'lpi:0018000000Qx7plAAB', 'po-org:resurrection-church-15122',
  'lpi:0018000000Qx7pkAAB']
group: Saint Thomas the Apostle Parish
evidence:
- url: https://container.parishesonline.com/bulletins/14/0675/20261025B.pdf
  seen: 2026-10-23
  quote: Saint Thomas the Apostle Parish, Munhall, PA 14-0675
  note: '25 October 2026 issue (container 14/0675, 16 pages; pages 1-12 are images, so the quote is the
    LPi ad-page footer on page 13). Rendered page 1: masthead ''ST. THOMAS THE APOSTLE PARISH'' with the
    Sunday Mass schedule (Saturday Vigil 4:00pm St. Therese, 5:30pm Holy Trinity; Sunday 7:30am St. Therese,
    9:00am St. Agnes, 10:30am St. Max, 11:15am St. Therese). Page 2 ''Worship Sites'' lists six churches:
    Holy Trinity, St. Agnes, St. Joseph, St. Maximilian Kolbe, St. Rita, St. Therese. Page 3 intentions
    give weekday Masses only at St. Agnes, St. Therese, Holy Trinity and St. Max for 24 Oct-1 Nov.'
- url: https://parishesonline.com/organization/saint-thomas-the-apostle-parish
  seen: 2026-10-23
  note: 'probe po: org ''Saint Thomas the Apostle Parish'', 1 Saint Therese Ct, Munhall 15120, LPi 0018000000Qc2VYAAZ,
    container 14/0675, latest issue 2026-10-25. Five older orgs (christ-the-light-of-the-world-st-joseph-st-agnes-holy-trinity-parishes,
    st-maximilian-kolbe-and-st-agnes-church, st-rita-church-15120, holy-trinity-church-15122, resurrection-church-15122)
    all list the same container and the same 2026-10-25 issue, so they are old predecessor orgs of one
    bulletin. st-joseph-church-15110 has no publications and is not a channel.'
- url: https://www.thomastheapostle.net/bulletin
  seen: 2026-10-23
  note: Read in headed Chrome (probe url gets 403). The site (eCatholic 23932, not recorded as a publication
    id) links its 'WEEKLY BULLETIN' to the ParishesOnline org saint-thomas-the-apostle-parish; there is
    no eCatholic bulletin archive.
- url: https://diopitt.org/saint-thomas-the-apostle-homestead
  seen: 2026-10-23
  quote: On July 1, 2020, the eight parishes were formally merged to create the new St. Thomas the Apostle
    Parish.
  note: 'Diocese history page (read in headed Chrome): eight parishes merged on 2020-07-01; nine buildings
    initially stayed open; closures are quoted in the excluded records.'
- url: https://container.parishesonline.com/bulletins/14/0675/20260125B.pdf
  seen: 2026-10-23
  quote: No. St. Joseph and St. Rita remain worship sites of St. Thomas the Apostle Parish.
  note: '25 January 2026 issue, page 6 (Mass Schedule Change FAQ): the new schedule dropped Sunday Mass
    at St. Joseph and St. Rita; see their church records.'
research:
- method: Compared the mastheads and LPi footers of the 25 October 2026 issue under the six ParishesOnline
    orgs listed by probe po; read the parish site bulletin link in headed Chrome.
  url: https://container.parishesonline.com/bulletins/14/0675/20261025B.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: None; one container 14/0675 serves every org.
- method: pnpm fetch:check --diocese pittsburgh --parish saint-thomas-the-apostle-munhall (headed Chrome)
  url: https://container.parishesonline.com/bulletins/14/0675/20261025B.pdf
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Transport ok, document type pdf, picked the 2026-10-25 issue (freshness ''future''
    two days early, as expected for ParishesOnline); publication identity is ''unverified'' only because
    no expected identity is given: the masthead was read by hand (rendered page 1).'
bulletin_status: available
---

## Publisher

St. Thomas the Apostle Parish (formed 1 July 2020 from eight parishes: Christ the Light of the World, St. Joseph, Resurrection, Holy Trinity, St. Agnes, St. Maximilian Kolbe, St. Rita and St. Therese of Lisieux, per https://diopitt.org/saint-thomas-the-apostle-homestead, read 2026-10-23) publishes one weekly bulletin on ParishesOnline, container 14/0675. The 25 October 2026 issue (https://container.parishesonline.com/bulletins/14/0675/20261025B.pdf) names the parish alone on its page 1 masthead and its ad-page footers read 'Saint Thomas the Apostle Parish, Munhall, PA 14-0675'. Pages 1-12 are images with no text layer; read from renderings. One parish office (1 St. Therese Court, Munhall, 412-462-8161). Text-layer issues of 10 May 2026 (page 1 worship-sites box) and 4 January 2026 show the same six-church masthead.

Six older ParishesOnline orgs for the predecessor parishes all resolve to this container (probe po 2026-10-23); all are recorded in `publication`. The parish is not paired with any other parish bulletin: the pastor, Rev. James Bachner, is listed for this parish only on the diocese page.

## Worship sites

The six churches in the bulletin's worship-sites box (25 Oct 2026, page 2): Holy Trinity and St. Agnes (West Mifflin), St. Joseph (Duquesne), St. Maximilian Kolbe (Homestead), St. Rita and St. Therese of Lisieux (Munhall). Only four hold weekly Mass now (St. Therese, Holy Trinity, St. Agnes, St. Max). Sunday Mass ended at St. Joseph and St. Rita when a new schedule took effect the weekend of 31 January-1 February 2026 (issue of 1 February, page 4: 'Our new Mass schedule takes effect this weekend'); the parish FAQ (25 January 2026) says both 'remain worship sites' and keep their feast-day and predecessor-anniversary Masses, so both are church rows (Rule 2): St. Joseph had a Mass on 19 March 2026, St. Rita on 22 May 2026. Three further buildings of predecessor parishes closed and are in `excluded/`: St. Hedwig and Holy Name (Duquesne) and Resurrection (West Mifflin). Holy Spirit, West Mifflin belongs to the Triumph of the Holy Cross parish and was recorded by an earlier scout.

## Website and bulletin provider

thomastheapostle.net is an eCatholic site behind Cloudflare (probe url 403; headed Chrome reads it). Its Mass-times page lists the same four churches with weekday Masses. The bulletin lives on ParishesOnline: provider_id `saint-thomas-the-apostle-parish`. The Mass Finder and the directory name the parish 'Saint Thomas the Apostle Parish'.

## Not yet confirmed

Nothing open on structure. Whether St. Joseph or St. Rita will hold further feast Masses is for the bulletin to show (see their records).
