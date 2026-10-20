---
name: Roman Catholic Diocese of Harrisburg
state: PA
website: https://www.hbgdiocese.org
status: promoted
gcatholic: harr0
city_aliases:
  Mt Carmel: Mount Carmel
  Blue Ridge Smt: Blue Ridge Summit
  East Pennsboro: Enola
  East York: York
  York Haven: Manchester
  Bonneauville: Gettysburg
promoted: 2026-10-20
---

Fifteen counties of south-central Pennsylvania: Dauphin (Harrisburg), Cumberland, Perry,
Lebanon, Lancaster, York, Adams, Franklin, Juniata, Mifflin, Snyder, Union, Northumberland,
Montour and Columbia. It borders Scranton to the north and Allentown to the east. The diocese
has no families or clusters. Most parishes have one church and print their own bulletin; a few
print one for a parish and its mission, and several pairs share a pastor but not a bulletin.
Explored in full on 2026-10-19/20 in six regions, one agent each, followed by a cross-region
pass. See the *Log* for the numbers.

## Sources

- **Parish directory (the `directory` roster):** https://www.hbgdiocese.org/parishes/
  ("Find a Parish, Church or Mass Time"), a WordPress page listing 96 entries by county, each
  linking `/parishes/<slug>/` with the address, a Google Maps embed (coordinates), weekend and
  weekday Masses, contacts and a "Website" link. Plain HTML; a browser user agent is enough
  with curl. Scraped on 2026-10-19 into `rosters/directory.json` (`mass_times` holds the
  page's text up to "Parish History"). Detail-page titles are truncated with "…", so names
  come from the list. Missions are listed as their own entries ("Mission in Benton").
  Lykens' map pin repeats New Oxford's; Sacred Heart, Lancaster and Sacred Heart, Spring
  Grove have no pin.
  The directory gives office addresses for some churches (St. Francis Xavier, Gettysburg; St.
  Joseph, Hanover; St. Patrick, Carlisle; St. Joseph, Mechanicsburg; Our Lady of Hope; St.
  Joseph, Berwick; Elizabethtown), and its Mass times are often stale (Lykens, Holy Trinity,
  St. Philip, Mother Cabrini, St. Rose). Several of its websites are dead, parked or moved:
  divineredeemerpa.weconnect.com ("Temporarily Unavailable"), goodshepherd-parish.com (parked;
  now thegoodshep.org), saintpaulsinannville.org (now annvillecatholic.org),
  corpuschristichbgpa.org (now cburgcatholic.org), and New Freedom's is blank (sjbnf.org).
- **GCatholic:** `rosters/gcatholic.json` (key `harr0`), 103 entries with Plus Codes, 7 of
  them Eastern Catholic (six Ukrainian, of the Archeparchy of Philadelphia, and St. Ann,
  Harrisburg, Ruthenian).
  GCatholic omits the cathedral, the Basilica of the Sacred Heart (Conewago Chapel), Holy
  Trinity (Columbia) and Our Lady of Good Counsel (Marysville), and keeps old buildings: St.
  Joseph, 236 Baltimore St, Hanover (razed after 1963), Sacred Heart, 146 N Main St, Spring
  Grove, and Holy Infant's former church at 34 3rd St, York Haven (now another
  congregation's). Some street numbers differ from the bulletins (St. Patrick and St. Rose,
  York; Holy Spirit, Palmyra; St. Benedict and St. Cecilia, Lebanon; Danville). Two Plus Codes
  are off: Our Lady of Lourdes, New Holland sits on a Baptist church about 2.2 km away, and
  Benton's is the town centre; OpenStreetMap was used for both.
- Clusters / families of parishes: none. Shared pastors are recorded in `group`.
- Mass times: each directory page gives weekend and weekday Masses; there is no separate
  diocese-wide Mass-times list.
- **Closed parishes and where their records went:**
  https://www.hbgdiocese.org/parishes/closed-parishes-and-records-locations/ ("AS OF NOVEMBER
  21, 2024"). Headings are the parishes holding the records, with the ended parishes under
  each (Holy Family under St. Francis of Assisi; Sacred Heart, Williamstown under Lykens; Sacred
  Heart and St. Lawrence under the cathedral). It says a parish ended, not that a building
  closed. `recheck` cannot read it (the server drops its user agent); curl and a browser can.
- Pastoral plan / closure announcements: none found. Bishop Senior's letter of 23 May 2026
  put San Juan Bautista and St. Anthony, Lancaster under one pastor from 20–21 June 2026,
  saying they "remain proper canonical parishes".
- **hbgdiocese.org** is fussy about clients: it answers some browser user agents with 403 or an
  HTTP/2 error and plain curl with a page, or the other way round, and drops `recheck`'s.
  Quotes from it are kept as notes where `recheck` can't reach it.

### Bulletin publishers here

88 parish rows: 39 Discover Mass, 24 `other`, 14 eCatholic, 9 ParishesOnline, 2 `no_bulletin`
(St. Matthew, Dauphin, whose bulletin is undated images on a Google Sites page; Our Lady of
Mount Carmel, Mount Carmel, whose ParishesOnline organization has no issues).

- **J.S. Paluch on Discover Mass** prints almost half the diocese, often for parishes whose
  own sites are behind Cloudflare. `discovermass.com/?s=<town or ZIP>` finds a church page
  when the parish site is blocked. Discover Mass caps downloads per IP per day: after many
  downloads from one address it answers each further file with a 134-byte "Maximum number of
  files downloaded today", which `fetch:check` reports as `not_pdf`. That is the cap, not the
  row. Its text layer is often garbled (doubled letters, split words); quotes keep the garble.
- **eCatholic:** 14 rows, every one behind Cloudflare (`CNAME cf.sites.ecatholic.com`). The
  homepage was challenged on most loads, but `https://www.<domain>/bulletins` usually opened
  first time in headed Chrome, and which sites were blocked changed from day to day. The
  fetch resolver read all of them. Some file an issue under a weekday date (Lykens's 18
  October issue is `20261015.pdf`).
- **LPi / ParishesOnline:** 9 rows. Many parishes keep empty ParishesOnline organizations
  (most Lancaster and northern parishes, the Korean community, the Ukrainian churches): not
  fold-ins. The ParishesOnline search API (`/prod/search?searchType=organization&...&latitude=
  &longitude=`) lists organizations near a point.
- **John Patrick Publishing** (`church-bulletin.org/<id>`): St. Andrew, Waynesboro (253),
  Holy Spirit, Palmyra (230), St. Catherine, Quarryville (256) and Assumption BVM, Lancaster
  (242). Listings with no PDFs (Dallastown 250, St. James 231, St. Leo 219, St. Philip 251)
  are not live channels.
- **FATA Online** (`fataonline.com/bulletins/<code>`), new to the dataset: Holy Infant,
  Manchester and St. John the Baptist, New Freedom (and FATA Printing for others). Each page
  has a fixed "View Current Bulletin" link and a dated archive; plain curl works.
- **Bon Venture** (`sponsors.bonventure.net/?page=<id>`): Queen of the Most Holy Rosary,
  Elysburg (2112); it prints Bonneauville's too, which the parish posts itself.
- **Self-hosted:** WordPress (Basilica, St. Vincent de Paul, Bonneauville, St. Francis of
  Assisi, St. Bernard, St. Leo, Holy Trinity), Duda (Abbottstown, Seven Sorrows, St. Anne,
  Fairfield), Wix (Orrtanna; the revivingtogether.com flipbooks for Mother Cabrini and St.
  Patrick, Trevorton), Squarespace (San Juan Bautista, Benton), Joomla (St. Lawrence), WP File
  Download (St. Rita).
- **Image-only bulletins** (the pipeline must read them as images): St. Matthew (no PDF at
  all), Abbottstown, St. Mary's York (pp. 1–6), St. Andrew, St. Leo, St. James, St. Anthony,
  Assumption BVM Lancaster, Holy Spirit, Divine Redeemer (pp. 1–7), Holy Angels, Milton,
  Catawissa, St. Columba (18 Oct), and page 1 of Seven Sorrows; San Juan Bautista's is half
  images.
- **Sites that block the sandbox:** the eCatholic sites (above); sjy.org and
  stpatrickyork.org (bulletins on Discover Mass); sacredheartbasilica.com (SiteGround
  "sgcaptcha" over http, drops `recheck`'s user agent); Bonneauville's "One moment, please…"
  check (its `/wp-json/wp/v2/media` lists the files); stcatherinepa.com; fssp.com.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** are excluded as `other-jurisdiction`, as in every other
  diocese here. The Ukrainian mission in Lancaster uses St. John Neumann's building, which
  keeps its own church row.
- **Shared pastors don't make shared bulletins.** Lykens / Millersburg; Mother Cabrini, Our
  Lady of Hope and St. Patrick, Trevorton (one website, three bulletins); St. Mary's and St.
  Joseph, Berwick; Holy Trinity and St. Peter, Columbia; San Juan Bautista and St. Anthony,
  Lancaster each print their own. **Rows that print one bulletin for several churches:**
  Immaculate Conception, Fairfield with St. Rita, Blue Ridge Summit (two counties, one
  masthead); St. Mark, Greencastle with St. Luke, Mercersburg; Our Lady of Good Counsel,
  Marysville with St. Bernadette, Duncannon; Assumption BVM, Lebanon with Our Lady of Fatima,
  Jonestown; Sacred Heart, Lewisburg with St. George, Mifflinburg; Sacred Heart, Lewistown
  with St. Jude, Mifflintown; St. Patrick, Carlisle (its church, the downtown shrine, St.
  Eleanor Regina and the Dickinson College Mass); St. Francis Xavier, Gettysburg (historic
  church, Xavier Center, Gettysburg College); St. Peter, Elizabethtown (new and historic
  churches). A mission that prints its own bulletin is its own row (Christ the King, Benton).
- **A campus Mass the parish bulletin lists every week gets a church row**, even in a
  non-Catholic chapel or a hall (Christ Chapel, Gettysburg College; Allison Hall, Dickinson).
  A campus ministry that publishes only by email is excluded `no-bulletin` (Rooke Chapel,
  Bucknell).
- **A seasonal site keeps its row** with a dated revisit (St. Eleanor Regina, Pine Grove
  Furnace: Sunday 11:30 from Memorial Day to Labor Day).
- **A place with public Mass that no readable source publishes** is excluded `no-bulletin`
  (Our Lady of Refuge, Doylesburg; the Saint Peter Son Korean community, Enola; Holy Family
  Chapel, Lancaster, whose Tuesday Latin Mass only the Lancaster Latin Mass Community's site
  lists). Adoration chapels without Mass, nursing-home, hospital and school Masses, and
  private convent Masses (St. Clement's Mission House, Ephrata) get no record.
- **A church the diocese lists as an ended parish, with no source saying the building
  closed,** goes to `open/` (Sacred Heart, Williamstown).

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-20: Fetch check (`fetch_check.check_fetch` on a temporary CSV of every row, under
  `xvfb-run` with `PLAYWRIGHT_BROWSER_CHANNEL=chrome`): all 86 rows with a provider resolve and
  download. The 47 non-Discover Mass rows ran together; the Discover Mass rows were checked by
  the region agents and, for the nine the daily cap had refused, again once it cleared. Four
  pick the newest posted issue rather than this week's, because it is the newest the parish
  has posted (Holy Angels and Holy Trinity, 11 October; St. Anne and Sacred Heart, Lewistown,
  4 October), each with a revisit. Undated picks (FATA's "View Current Bulletin", the
  revivingtogether.com flipbooks, Orrtanna's titled link, Bonneauville's newest post) were
  checked against the issue by hand. Promoted: 86 parishes (fetch-only) and 99 churches; the
  two no_bulletin rows and their churches stay in the records only.
- 2026-10-20: Explored the whole diocese in six regions (Adams and the Hanover area; York
  and Franklin; Lancaster; Dauphin and Perry; Lebanon and Cumberland; the northern counties),
  one agent each, then a cross-region pass. Result: 88 parish rows (39 Discover Mass, 24
  other, 14 eCatholic, 9 ParishesOnline, 2 no_bulletin), 101 churches, 15 exclusions (7
  other-jurisdiction, 4 closed, 4 no-bulletin) and 2 open questions (Sacred Heart,
  Williamstown; the Carmelite monastery, Elysburg). Coverage: directory 96/96, GCatholic
  103/103. Five churches are in no roster: Xavier Center and Christ Chapel (Gettysburg),
  Historic St. Peter (Elizabethtown), Mother of Holy Purity Chapel (Wrightsville, under St.
  Peter, Columbia) and Allison Hall (Dickinson College). `audit`: four shared-pastor groups
  span rows, each with separate bulletins recorded. Two closures carry no `last_mass`
  because no source dates them. Resolver changes in this PR: a link titled "This Week's
  Bulletin" now beats a bare "Bulletin" (Orrtanna), and a bulletin whose http link answers
  with something other than a PDF is retried over https (the Basilica).
- 2026-10-19: Initialised. Fetched GCatholic (103 entries) and scraped the diocesan parish
  finder (96 entries) as `rosters/directory.json`.
