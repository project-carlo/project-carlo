---
name: St. Joseph Parish
website: https://oilcitycatholic.com
bulletin_provider: discover_mass
provider_id: oil-city-catholic-community-oil-city-pa
publication: ['discovermass:oil-city-catholic-community-oil-city-pa']
group: Pastor pro tempore Rev. Daniel Hoffman, also pastor of St. Titus, Titusville; one parochial vicar
  (Rev. Festus Okoye) for both (clergy PDF 8/7/2026); each parish publishes its own bulletin, so two rows
evidence:
- url: https://discovermass.com/church/oil-city-catholic-community-oil-city-pa/
  seen: 2026-10-23
  quote: 'Saturday Vigil: 4:00 pm'
  note: 'Current bulletin of the page (cover class ''bulletin-cover X-|2026-10-18|...|3172''): 8-page
    issue of 18 October 2026, 29th Sunday in Ordinary Time, page 1 masthead ''St. Joseph Church / 35 Pearl
    Avenue, Oil City, PA, 16301 | 814.677.3020 | www.oilcitycatholic.org''; footer ''View this bulletin
    online at www.DiscoverMass.com''. Mass Times: Saturday Vigil 4:00 pm, Sunday 8:00am & 9:45 am, weekdays
    (St. Joseph) Mon, Wed, Fri 8:30 am, Tues. & Thur. 12:10 pm.'
- url: https://discovermass.com/church/oil-city-catholic-community-oil-city-pa/
  seen: 2026-10-23
  quote: Fr. Daniel Hoffman, Pastor
  note: 'Last-page ''Parish Ministry Team'' of the 18 October 2026 issue: ''Fr. Daniel Hoffman, Pastor
    ... Fr. Festus Okoye, Parochial Vicar ... Deacon Assistant, Kevin Harmon''.'
- url: https://oilcitycatholic.com/Bulletins.html
  seen: 2026-10-23
  note: The parish site's Bulletins nav entry carries an onClick `location.assign('https://discovermass.com/church/oil-city-catholic-community-oil-city-pa/#bulletins')`
    (in the HTML source, not visible text); probe url finds discovermass:oil-city-catholic-community-oil-city-pa.
    The page lists 12 issues, 2 August to 18 October 2026, all downloaded 2026-10-23.
- url: https://www.eriercd.org/images/directoryclergy.pdf
  seen: 2026-10-23
  quote: Pastor, pro tempore
  note: 'Clergy list updated 8/7/2026: ''Hoffman, Rev. Daniel R. ... Pastor, pro tempore ... St. Joseph,
    Oil City'' (and Pastor, St. Titus, Titusville); the directory''s St. Joseph record names Hoffman as
    pastor and Okoye as parochial vicar, though its locator still says ''Rev. John L. Miller''.'
research:
- method: PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese erie --parish st-joseph-oil-city
    --expected-identity 'Oil City' --expected-issue-date 2026-10-18
  url: https://discovermass.com/church/oil-city-catholic-community-oil-city-pa/
  checked: '2026-10-23'
  outcome: found
  next_action: 'None. Transport ok, PDF, identity matched; issue date and freshness ''unknown'' because
    the masthead date is split by the layout (read by hand: 18 October 2026, number 3172). The Discover
    Mass download cap applies: fetch:check worked after 12 issue downloads the same day.'
  retry_when: fetch:check reports not_pdf (daily download cap)
publication_reviews:
- parish: st-titus-titusville
  decision: separate
  evidence:
  - url: https://container.parishesonline.com/bulletins/14/1175/20261025B.pdf
    seen: 2026-10-23
    quote: Regular Mass Schedule
    note: St. Titus's 25 October 2026 issue (LPi container 14/1175, 4 pages, own masthead 'Saint Titus
      Roman Catholic Church, 513 West Main Street, Titusville', own Regular Mass Schedule, own offertory
      and readings) is a different document from St. Joseph's Discover Mass number 3172 (8 pages, masthead
      St. Joseph Church, 35 Pearl Avenue, different Mass times and intentions). Both are signed by the
      same pastor ('Fr. Dan') in near-identical welcome letters, but each describes its own parish. St.
      Titus's liturgy schedule printed '8:30 AM at St. Joseph' style cross-references through 29 March
      2026 and none since. Each masthead names only its own church.
---

## Publisher

St. Joseph Parish, Oil City (parish site oilcitycatholic.com, 'Oil City Catholic') publishes its own weekly bulletin on Discover Mass, church page `oil-city-catholic-community-oil-city-pa` (page title 'St Joseph Parish'). The current issue read 2026-10-23 is dated 18 October 2026 (Discover Mass bulletin number 3172, 8 pages, masthead 'St. Joseph Church, 35 Pearl Avenue, Oil City, PA'). The page carries 12 weekly issues, 2 August to 18 October 2026; the 25 October issue was not posted yet. Downloads are capped per IP per day, so `fetch:check` reads it once and the text checks here were done on files saved in the scratch folder.

The parish site's Bulletins menu entry is an `onClick` location.assign to that Discover Mass page (not a PDF listing). The directory and the site's own footer give `oilcitycatholic.com`; the bulletin's masthead prints `oilcitycatholic.org`, which the sandbox cannot reach (proxy refused), so the parish site is recorded as `.com`.

## Shared pastor, separate bulletin (St. Titus, Titusville)

Fr. Daniel Hoffman is pastor of St. Titus and pastor pro tempore of St. Joseph, with one parochial vicar (Fr. Festus Okoye) for both (clergy PDF 8/7/2026). The bulletins are separate publications: St. Titus's LPi container 14/1175 and St. Joseph's Discover Mass number 3172 have different mastheads, Mass schedules and intentions (see `publication_reviews`). St. Titus's liturgy schedule did print St. Joseph's Mass times ('8:30 AM at St. Joseph') in every issue to 29 March 2026; St. Joseph's bulletin never prints a St. Titus Mass schedule (it advertises church-directory photo days at both churches on 26-29 October 2026).

## Worship sites

- **St. Joseph, 35 Pearl Ave., Oil City**: the parish church; the only church whose Mass times the bulletin prints.
- **St. Venantius, 403 Main St., Rouseville**: secondary church of this parish in the 6 October 2026 directory; no Mass in the 12 issues read. In `open/` (see `st-venantius-rouseville`).
- **Closed and relegated, now excluded as `closed`:** Assumption of the Blessed Virgin Mary, 7 Pulaski St. (relegated 2019-07-19), Our Lady Help of Christians, 564 Colbert Ave. (relegated 2020-07-19) and St. Stephen, 21 State St. (relegated 2024-03-18); see the three `excluded/` records. The 18 October 2026 bulletin refers to 'salvaged items from St. Stephen's Church' and fund-raisers of St. Stephen **School** (a school, separate from the closed church).

## Not yet confirmed

- **Weekday Mass times differ from the directory.** The bulletin says Mon, Wed and Fri 8:30 am, Tuesday and Thursday 12:10 pm; the directory and parish site say Mon and Fri 12:10 pm, Wed 8:30 am (and the Discover Mass page Mon/Tue/Thu 12:10, Wed/Fri 8:30). The bulletin was followed. The weekend times agree (Sat 4 pm; Sun 8 and 9:45).
- **A stale text layer.** The 2 August 2026 issue's Mass-intention panel still shows the week of 26 April 2026 (hidden text) including 'Thursday, April 30th 6:00pm @ St. Venantius'. Not a current Mass.
