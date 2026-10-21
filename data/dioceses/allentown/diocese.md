---
name: Roman Catholic Diocese of Allentown
state: PA
website: https://www.allentowndiocese.org
status: promoted
gcatholic: alle0
promoted: 2026-10-19
---

Five counties of eastern Pennsylvania: Lehigh (Allentown), Northampton (Bethlehem, Easton),
Berks (Reading), Carbon and Schuylkill (Pottsville and the coal region). It borders
Scranton to the north. Many coal-region parishes were consolidated in 2008, so several now
have more than one worship site, and some directory entries are worship sites of another
parish ("... Worship Site for ... Parish").

## Sources

- **Parish map (the `directory` roster):** https://www.allentowndiocese.org/maps/parishes,
  the same "places" platform as the Archdiocese of New York's directory. Plain HTML, no
  Cloudflare. 87 entries, each with `data-lat`/`data-lng` and a `/places/<slug>` page giving
  the address, phone, website, pastor and weekend Masses. Scraped with `curl` on
  2026-10-18 into `rosters/directory.json` (`mass_times` holds the page's text). Mixes
  parishes and worship sites; eleven free-form addresses were normalised by hand.
- **GCatholic:** `rosters/gcatholic.json` (key `alle0`), 130 entries with Plus Codes, 26 of
  them Eastern Catholic (marked `rite`: Ruthenian, Ukrainian, Maronite, Syriac). Keeps
  churches closed in the 2008 consolidations.
  The map lags: it listed Our Lady of Good Counsel, Bangor eight months after its last Mass
  and still lists St. Vincent de Paul, Girardville (closed January 2026). It gives parish
  offices rather than churches in places (Our Lady of Mercy, St. Anthony and Mt. Carmel in the
  Slate Belt/Easton; St. John XXIII at the closed St. Jerome, 266 W Broad), its pins can be
  a kilometre off (St. Paul and St. Thomas More, Allentown; St. Joseph, Sheppton carries
  Ringtown's), and its pastors and Mass times are often stale. Many of its websites are dead
  or squatted: every `*.weconnect.com` site answers "Temporarily Unavailable" (Slatington,
  Holy Trinity Whitehall, Queenship of Mary), and olhcparish.net, saintjohnfisherparish.com,
  sspeterpaul.com, minersvillecatholic.com, stmaryrdg.com and sjcreading.com are parked,
  squatted, for sale or gone. It does list secondary worship sites inside the parent's
  entry (Ss. Peter & Paul Chapel, Tower City under Most Blessed Trinity).
- **GCatholic:** `rosters/gcatholic.json` (key `alle0`), 130 entries with Plus Codes, 26 of
  them Eastern Catholic (marked `rite`: Ruthenian, Ukrainian, Maronite, Syriac). Keeps
  churches closed in the 2008 consolidations (six in Shenandoah alone), omits the cathedral,
  and has some wrong street numbers (Summit Hill, the Nesquehoning shrine, Lake Harmony about
  1.7 km off). Its "St. Francis of Assisi", Nesquehoning is typed as a shrine with its Plus
  Code on the Diocesan Shrine of St. Therese (the former Our Lady of Mount Carmel). Where the
  map and GCatholic disagree, GCatholic's Plus Codes match OpenStreetMap.
- Clusters / families of parishes: the diocese has none. Several parishes share a pastor;
  the canonical parish (or the shared pastor) is the `group`.
- Mass times: each `/places/` page lists weekend Masses; there is no separate diocese-wide
  Mass-times page.
- **News for dating closures:** AD Today (ad-today.com, the diocese's news site; readable
  with curl) for mergers and closures (Minersville's Holy Family, 1 July 2020; St. Stephen,
  Port Carbon, 2020; St. Lawrence, Catasauqua, 2022). The Shenandoah Sentinel
  (shensentinel.com, searchable with `?s=`) for the coal region, the Times News (tnonline.com)
  for Carbon County, Lehigh Valley Public Media / lehighvalleynews.com for the Slate Belt,
  GoReadingBerks parish histories for Reading.
- Closed parishes and where their records went: no diocesan list found. The 2008
  restructuring closed 47 parishes; closures since then are dated from the news above.

### Bulletin publishers here

72 parish rows: 47 `other`, 10 Discover Mass, 8 ParishesOnline, 4 eCatholic, 3 `no_bulletin`
(St. Elizabeth of Hungary, Pen Argyl, whose newest posted issue is 11 January 2026; St.
Margaret, Reading; St. Teresa of Calcutta, Mahanoy City).

- **John Patrick Publishing** prints 19 bulletins here: seven in Berks (Holy Guardian Angels,
  St. Ignatius, St. Peter the Apostle, Kutztown, Hamburg, Douglassville, St. Columbkill), the
  cathedral and St. Paul (Allentown) and St. John the Baptist (Whitehall), Holy Ghost, St. Anne,
  the Easton twins, Bath and St. Rocco in Northampton, Palmerton and Summit Hill in Carbon, and
  Divine Mercy, Shenandoah. Parish sites link
  `jppc.net/onlinebulletins/<id>template.pdf`, which redirects to the listing at
  `church-bulletin.org/<slug>` (also `/?id=<id>`), with dated PDFs. Scanning
  `church-bulletin.org/?id=1..1200` for Berks ZIP codes found listings for sites that block
  the sandbox (St. Columbkill, id 238). It answers 406 to a bare "Mozilla/5.0" user agent;
  plain curl works. Rows read the listing with a pinned `page-pdfs` recipe.
- **Bon Venture** (`sponsors.bonventure.net/?page=<id>`, over `http://`): Lehighton (1572),
  Shillington (1920), St. Thomas More (1838), St. Joseph the Worker, Orefield (1599), Our Lady
  of Perpetual Help, Bethlehem (1588; its eCatholic site posts the bulletin there) and St. Jane
  Frances de Chantal, Easton (1817).
- **J.S. Paluch on Discover Mass:** ten rows, mostly Reading and Bethlehem. Twinned parishes
  each have their own Discover Mass page and their own bulletin.
- **Empty channels are not fold-ins.** Many parishes keep ParishesOnline organizations from
  old accounts with no publications (St. Matthew, St. Patrick, St. Clare, Holy Cross and
  others in Schuylkill; `-church-<zip>` slugs in Northampton), and Discover Mass has pages
  with no bulletins. ParishesOnline's own church search
  (`parishesonline.com/search?searchLocation=<town, PA>&...&searchType=organization`) finds
  live org slugs when a parish domain is dead (Holy Family, Minersville).
- **Image-only bulletins** (the pipeline must read them as images): Holy Guardian Angels,
  St. Ignatius, St. Columbkill, Bally, St. Paul (Allentown), the Easton twins, Summit Hill,
  Most Blessed Trinity (Tremont), St. Joseph the Worker (Frackville), and Divine Mercy since
  30 August 2026. St. Catharine of Siena, Reading prints its schedule only as an image.
- **Sites that need a browser or block the sandbox:** the Cloudflare eCatholic sites
  (bvm-northampton, my-olph, sttheresaotcj, sacredheartbethlehem); stjanesofeastonpa.com
  (StackProtect blocks curl and Chrome); olmcroseto.org, peterandpaulchurch.com (Lehighton),
  strichard.org and stjw.org reset plain connections; scsreading.org and goreadingberks.com
  answer 406 without a browser user agent.

### Fetch check (2026-10-18/19, before promotion)

`fetch:check` then read only `data/parishes.csv` (it now takes `--diocese`), so each
region ran `fetch_check.check_fetch(parishes_csv=...)` on a temporary CSV built from `parishes/`, under
`xvfb-run` with `PLAYWRIGHT_BROWSER_CHANNEL=chrome`. Of the 69 rows with a provider, **68
resolve and 67 pick the newest posted issue** (18 October, or 11 October where that is the
newest). Recipes printed by the check are pinned on the `other` rows whose pick was checked
by hand.

- **Wix cards (fixed):** St. Charles Borromeo, Ashland and St. Joseph the Worker, Frackville
  list each issue as a Wix card (date, Sunday, "View" link to a hash-named PDF); the resolver
  picked the header's "Coat of Arms" PDF. An undated PDF link now takes the one date in its
  card (`role="listitem"`), and `page-pdfs` reads a page again after a moment when its first
  read is no bulletin (Frackville's cards sometimes render late). Both now pick 18 October
  and are pinned.
- **One issue behind:** Our Lady of Mount Carmel, Roseto's homepage linked the 11 October
  issue on 18–19 October while the 18 October one was already in its media library; the
  resolver reads the homepage correctly. Not pinned; re-check.
- **Not read:** Incarnation of Our Lord, Bethlehem: the pick is right, but its server sends
  an incomplete TLS chain and the download fails (revisit 2026-10-26).

## Rules settled for this diocese

- **Eastern Catholic churches** (Ruthenian: Archeparchy of Pittsburgh / Eparchy of Passaic;
  Ukrainian: Archeparchy of Philadelphia; Maronite; Syriac) are excluded as
  `other-jurisdiction`, as in Scranton, Syracuse and Rochester. The Syriac Our Lady of Mercy,
  Allentown uses Immaculate Conception's building, which keeps its own church row.
- **Shared pastors don't make shared bulletins.** Holy Rosary/Sacred Heart and St. Joseph/
  St. Paul (Reading), Holy Infancy/Incarnation (Bethlehem), Sts. Simon & Jude/Our Lady Help
  of Christians, St. Peter Coplay/St. John Stiles, Immaculate Conception/Sacred Heart
  (Allentown) and St. Charles Borromeo/St. Joseph the Worker (Ashland/Frackville) each print
  their own. Rows that print one bulletin for several churches: Assumption BVM/Queenship of
  Mary (Northampton); St. Anthony/Our Lady of Mercy (Easton); Catholic Churches of Jim Thorpe;
  St. Joseph, Summit Hill with the Nesquehoning shrine; St. John XXIII/St. Richard; St. Mary
  Ringtown/St. Joseph Sheppton; All Saints McAdoo with Weatherly; St. Clare with Holy Cross,
  New Philadelphia; Holy Family, Minersville (St. Matthew and St. Michael); St. Peter the
  Apostle with Sts. Cyril & Methodius and St. Catharine of Siena with St. Mary (Reading);
  Annunciation BVM, Catasauqua with St. John Fisher; Holy Ghost, Bethlehem with St. Stephen of
  Hungary Oratory, Allentown.
- **A seasonal worship site keeps its row** with a dated revisit: St. Casimir, Shenandoah has
  Sunday Mass from summer through September; from October Divine Mercy moves it to its main
  church "due to high cost of oil".
- **A shrine with public Mass but no bulletin and no parish of its own** is excluded
  `no-bulletin` (the Padre Pio Centre, Barto).
- **A church no current schedule lists, with no source saying it closed,** goes to `open/`
  (St. Mary Magdalen, Lost Creek; Annunciation BVM, Frackville; Ss. Peter and Paul, Allentown,
  promised two Masses a year after its 2021 merger into St. Elizabeth).

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-19: Promoted: 69 parishes (fetch-only) and 84 churches; the three no_bulletin rows
  and their churches stay in the records only. `recheck`: 450 quotes found, none missing; 12
  sources unreachable from the sandbox (olmcroseto.org resets, incarnationofourlord.org's
  incomplete TLS chain, scsreading.org's proxy 502, one eCatholic PDF cut short) and one
  parked page (olhcparish.net, cited as dead).
- 2026-10-19: Explored the whole diocese in six regions (Lehigh; Northampton; Berks; Carbon
  with Slatington; north Schuylkill; south Schuylkill), one agent each, then a cross-region
  pass. Result: 72 parish rows (47 other, 10 Discover Mass, 8 ParishesOnline, 4 eCatholic, 3
  no_bulletin), 87 churches, 45 exclusions (26 other-jurisdiction, 18 closed, 1 no-bulletin)
  and 3 open questions. Coverage: directory 87/87, GCatholic 130/130; one church is in no
  roster (Ss. Peter & Paul Chapel, Tower City, under Most Blessed Trinity). `audit`: three
  groups span rows, each with separate bulletins recorded. Fetch check: 68 of 69 rows with a
  provider resolve, after a resolver change for Wix cards (see above). Six closures carry no
  `last_mass` because no source dates them.
- 2026-10-18: Initialised. Fetched GCatholic (130 entries) and scraped the diocesan parish
  map (87 entries) as `rosters/directory.json`.
