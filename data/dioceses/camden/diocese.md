---
name: Roman Catholic Diocese of Camden
state: NJ
website: https://camdendiocese.org
status: promoted
gcatholic: camd0
city_aliases:
  Somers Poin: Somers Point
  Haddon Twp: Haddon Township
  Gloucester: Gloucester City
  Margate: Margate City
promoted: 2026-11-07
---

The six southernmost counties of New Jersey: Camden (Camden, Cherry Hill, Pennsauken,
Collingswood, Haddonfield, Lindenwold, Berlin, Atco, Sicklerville), Gloucester (Woodbury,
Deptford, Sewell, Glassboro, Clayton, Swedesboro, Mullica Hill, Williamstown), Salem (Salem,
Pennsville, Carneys Point, Woodstown, Elmer), Cumberland (Vineland, Millville, Bridgeton),
Atlantic (Atlantic City, the Downbeach towns of Ventnor, Margate and Longport, Brigantine,
Absecon, Galloway, Egg Harbor Township, Hammonton, Mays Landing) and Cape May (Ocean City, Sea
Isle City, Avalon, Stone Harbor, Cape May Court House, the Wildwoods, Cape May). Neighbours:
Trenton to the north and east (Burlington and Ocean counties; not mapped), Philadelphia across
the Delaware River and Wilmington across the Delaware Bay (both mapped by the factory, Runs
philadelphia-map-1 and wilmington-map-1).

The diocese has **62 parishes** (the homepage, read 2026-10-29: "approximately 475,000 Catholics
in 62 parishes"; the same count after the 2017 Camden mergers). There are **no families,
clusters or pastorates**. Instead, most parishes are **mergers** of the 2009–2011 "diocesan-wide
reconfiguration of parishes" (Notre Dame de la Mer, 2010, was "the ninth merger" in it:
Catholic Star Herald, 2020-02-27), followed by Camden County consolidations in 2014, Atlantic City's in 2015 (four
parishes into the Parish of St. Monica) and the City of Camden's in 2017. A merged parish usually
keeps two to five of its former churches as worship sites under one name, so **one parish, one
bulletin, several churches** is the common shape here, and GCatholic's `group` names the merged
parish for most of them. Shared bulletins between *different* parishes are unlikely: the
assignments name one pastor per parish, and the one priest found serving two (Rev. Michael J.
Matveenko, pastor of St. Mary and administrator of St. Thomas More, Cherry Hill) leaves two
separate bulletins (Rules settled). Expect closed or sold former churches (St. John
Bosco, Millville, sold 2020; St. Anne, Westville, relegated 2024; St. Bernard, Dorothy, "currently
not open"). Shore parishes in Atlantic and Cape May counties add summer Masses and seasonal
churches. The old directory gives deanery numbers (1–6 and 9); nothing current uses them.
`batches.json` keeps each merged parish's churches in one batch, and neighbours in a town
together.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (the `directory` roster):** the diocese's "Parish/School Locator",
  https://www.camdendiocese.org/psl/, a WordPress **Store Locator Plus** map (not WP Store
  Locator, so `roster fetch wpsl` doesn't apply). One POST to `wp-admin/admin-ajax.php` with
  `action=csl_ajax_onload` returns every location as JSON; scraped 2026-10-29 by
  `scratch/camden-map-1/tools/slp_locator.py`: 102 locations, of which 37 are schools, academies
  and two retreat centres (dropped), leaving **65: the 62 parishes, Mater Ecclesiae, Berlin (a
  Traditional Latin Mass "Mission" with a Rector) and two Korean Catholic missions** (St. Andrew
  Kim, Absecon; St. Yi Yunil, Westville). One entry per **parish**, at its main church or office
  address; worship sites aren't listed. **It is old:** every entry's `sl_lastupdated` is 2015,
  many pastors are years out of date (it gives Rev. Raymond Gormley for both Holy Child and
  Incarnation; the 2026 assignments name others), and many websites are dead or moved (below).
  The description carries a deanery number ("Deanery 1" to "Deanery 6", once "Deanery 9"; some entries two) and the
  pastor, kept as `deanery` and `clergy`. Good for the parish list and names (the diocese's own
  "St. Mary, The Catholic Church of", "St. Maximilian Kolbe The Parish of" are inverted) and
  coordinates; not for pastors, websites or structure. Quirks: "Somers Poin"; St. Charles
  Borromeo is given as Washington Township (the 2026 assignments say Sicklerville); St. Yi Yunil
  is at 1219 Delsea Dr., Westville, where GCatholic puts it at St. Mary, Cherry Hill.
- **GCatholic:** `rosters/gcatholic.json` (key `camd0`), 119 entries with Plus Codes: 115 Latin
  churches, plus **4 Eastern Catholic** (Ukrainian: St. Michael, Cherry Hill; St. Nicholas,
  Millville; Sts. Peter and Paul, Williamstown. Maronite: Our Lady Star of the East,
  Pleasantville). It lists **churches**, with the merged parish in `group` ("St. Damien Parish"),
  so it is the best list of worship sites, but its groups are stale: it still has the
  pre-2014 St. Rita of Cascia Parish and Community of Emmaus, the pre-2017 St. Josephine Bakhita
  Parish, and "Blessed" Teresa of Calcutta. It **omits** the Cathedral and St. Joseph
  Pro-Cathedral (Camden) and St. Elizabeth, Goshen. It includes the Monastery of the Perpetual
  Rosary chapel (Camden), Our Lady of the Highway, Sea and Air shrine (Pomona), the Holy Trinity
  chapel, Margate, and churches with no group (St. Mary, Salem; Queen of the Apostles,
  Pennsville) that are presumably St. Gabriel the Archangel's. Its websites are older still
  than the directory's (see the publishers section).
- **Mass times (the `summer-guide` roster):** "Summertime Masses added at South Jersey shore
  parishes" (Catholic Star Herald, 2026-05-22,
  https://catholicstarherald.org/summertime-masses-added-at-south-jersey-shore-parishes-2026/),
  whose schedule is one image
  (https://catholicstarherald.org/wp-content/uploads/2026/05/Summer-Mass-Schedule-2026-1.jpg),
  hand-transcribed 2026-10-29 into `scratch/camden-map-1/tools/summer_guide_2026.json`: **32
  churches** in Atlantic and Cape May counties, each under its parish (`group`), with summer
  weekend times. It is the only list naming the worship sites of the shore's merged parishes from
  the diocese's side, and it has St. Elizabeth, Goshen (Our Lady of the Angels, Sunday 10:15 AM),
  which is in no other roster, St. Agnes Mission, Cape May Point, and St. Bernard Mission Church,
  Dorothy marked "Currently not open". It leaves out Hammonton, Collings Lakes and St. Andrew Kim.
  Its seasonal notes ("June 29th to Labor Day Weekend", "Memorial Day to Labor Day") are
  summer-only; read an off-season bulletin before calling a church seasonal. There is no
  diocese-wide year-round Mass-times list (the site's /mass-times/ page is a 2009 news post).
- **Clusters / families of parishes:** none. **Shared pastors:** the assignments name none,
  but a parish administrator can serve a second parish: St. Thomas More, Cherry Hill's masthead
  names Rev. Michael J. Matveenko, pastor of St. Mary, Cherry Hill, as its administrator; both
  publish their own bulletins (Rules settled). The directory's Matveenko for St. Charles Borromeo
  is out of date (its 25 October 2026 bulletin names Rev. Thomas A. Newton). The 2025 and 2026
  priest assignments (Catholic Star Herald, 2025-05-17
  https://catholicstarherald.org/bishop-williams-announces-priest-assignments-personnel-changes/
  and 2026-05-02 https://catholicstarherald.org/83106-2/, effective 2026-07-01) name every pastor
  to one parish. They also record that Sacred Heart, Camden's pastor is "Episcopal Vicar for the
  City of Camden", that the Parish of St. Monica and Holy Spirit, Mullica Hill have parochial
  vicars or a co-pastor, and that Our Lady of the Lakes has a summer administrator. The site's
  "Clergy List" (camdendiocese.org/clergylist/) is the abuse disclosure list, not a directory.
- **Mergers and closures (no diocesan list; the Catholic Star Herald):** catholicstarherald.org
  is WordPress and its REST API answers `probe get`
  (`/wp-json/wp/v2/posts?search=<words>&_fields=date,title,slug`, then
  `?slug=<slug>&_fields=date,link,content` piped to `tools/csh_post.py`). Decrees found:
  establishment of Holy Cross, Bridgeton (2010-09-09), Christ the Redeemer, Atco (2010-10-08),
  St. Joseph the Worker (2011-09-08), St. Maximilian Kolbe (2011-11-10); "Camden County parish
  consolidation plan approved" (2014-05-08: "The Emmaus Catholic Community of Mount Ephraim will
  now be joined with St. Rose of Lima Parish, Haddon Heights. Mary Mother of the Church, now part
  of St. Rita's Parish, Bellmawr, will join with St. Joachim's Parish … St. Francis Church,
  Barrington … will become part of St. Rose of Lima Parish", effective 2014-06-30); the merger
  into the Parish of St. Monica, Atlantic City (2015-06-11; the directory: "As of July 1, 2015
  the former parishes of St. Michael, St. Monica, St. Nicholas of Tolentine, Our Lady Star of the
  Sea in Atlantic City merged"); "Diocese announces reorganization of Camden parishes"
  (2017-07-06: St. Joseph into the Cathedral, St. Anthony of Padua into St. Joseph Pro-Cathedral,
  St. Josephine Bakhita into Sacred Heart, effective 2017-07-31, "all affected churches will
  remain open for normal worship, unless and until determined otherwise", "there are now 62
  parishes"); the relegation of St. Anne, Westville, part of St. Joachim (decree 2024-05-28);
  and "Saint John Bosco Chapel pays homage to former parish church" (2026-02-05: the former St.
  John Bosco Church, Millville "was closed and sold in 2020"; a new chapel on the All Saints
  campus hosts daily Mass). Search titles there for "Decree" before calling a church closed.
  A merger decree ends a parish, not a church: the 2017 one kept every church open.
- **Pastoral plan:** none current found. The diocese is out of Chapter 11 (plan confirmed
  2024-03-14; /reorganization/ is about the bankruptcy, not parishes).
- **Other jurisdictions in the territory:** GCatholic's four Eastern Catholic churches (above),
  all in batch `eastern-catholic`. The Korean missions are Latin and diocesan (the directory lists
  them with a deanery), so they are not other-jurisdiction.

### Bulletin publishers here

From `probe url` on the rosters' 108 websites and the browser (2026-10-29). Use the
directory's website before GCatholic's: many of both are dead, moved or hijacked (spam
redirects, empty templates), so read one before storing it. Find a moved site with a
duckduckgo.com/html search through `probe get`, and check the address on the page: a guessed
domain can be a same-named parish elsewhere.

- **John Patrick Publishing** prints about half the diocese. Parish sites link
  `jppc.net/onlinebulletins/<id>template.pdf` or `church-bulletin.org/?id=<id>`, which
  redirect to a `church-bulletin.org/<slug>` listing of dated PDFs (New Jersey ids run in the
  500s–600s and 6000s). Record `page-pdfs https://www.church-bulletin.org/<slug>`. Don't guess
  a slug: a wrong one returns the generic home page with HTTP 200, and a slug is right only if
  its page lists `/bulletin/<slug>/<date>.pdf` links. Find the id from a site footer "Hosted
  by John Patrick Publishing", an issue's back-page footer or PDF title, or the prefix of a
  parish's own file names; otherwise `tools/jp_ids_500_700.tsv` (the Run's id-to-slug sweep of
  ids 500–700), `curl -sIL https://church-bulletin.org/<id>` for a 6000s id, then a search for
  `church-bulletin.org <parish> <town> NJ` (or `<parish> <street> bulletin` when the parish's
  own site is dead). **Look for the listing whenever a parish's own site can't be read or
  doesn't link its bulletin.** The listing beats a parish's own copy that lags (by a week or by
  years), starts with something else (a registration form) or names files irregularly: its
  uniform dated names keep `fetch:check`'s pick reliable. A listing with no `/bulletin/`
  editions means the parish publishes elsewhere; merged parishes' old per-church codes survive
  empty, so an id hit is not a live bulletin until its listing shows editions. **Most issues
  are image-only:** `probe pdf` returns no text and `fetch:check` still reports ok with the
  URL's date; render pages 1–2 with `render.py` for the masthead and Mass schedule (`probe pdf
  --pages N` reads the first N pages, not page N). church-bulletin.org answers 406 to a bare
  "Mozilla/5.0" user agent: use plain curl, `probe pdf` or `visit.py`.
- **LPi / ParishesOnline:** a parish site's org link or widget gives the org slug, and `probe
  po <slug>` the container. A WeConnect (LPi) or Duda site can embed `publicationWidget?id=<lpi
  id>` without `probe url` reporting it: grep the page source for `publicationWidget?` (the
  18-character id can start `0018…` or `001C…`), pass it to `probe po <id>`, and record
  `lpi:<id>` with `po-org:` and `po-container:`. Issues are posted before their Sunday, so
  freshness `future` is not a wrong pick. Image-only issues read on page 1 through `render.py`;
  `fetch:check` then reports the date inferred and identity unverified. Issues over
  `fetch:check`'s 25 MB inspection limit report only the PDF signature as `document_type`,
  which is not an error. With no org slug, record the parish's own page that posts the same
  issues as `page-pdfs` and keep `po-container:` (PDFs listed out of date order still give the
  newest; percent-encode spaces in names for `probe pdf`). A
  page that only embeds `widget.parishesonline.com/publications?id=<40 hex>` shows nothing
  while the widget answers 502, which also hides the org; a search for the parish and
  `container.parishesonline.com` finds the container from its PDFs, but `probe po` can't take a
  container, so with no slug and no page listing the PDFs the row is `unsupported` with
  `fetch_gap` `po-org-unknown` (hand refresh, 2026-11-07).
- **eCatholic:** an eCatholic id is the publication only when `/bulletins` lists current
  `files.ecatholic.com/<id>/bulletins/` PDFs. Some sites link another publisher instead, and an
  eCatholic copy can lag its printer's by weeks: compare its newest issue with the parish's Bon
  Venture or John Patrick listing first (Rules settled). The `/mass-times` page has the
  schedule and the staff page the priests' roles, which a bulletin grep doesn't give; a
  masthead's street numbers can differ from GCatholic's.
- **Bon Venture** (`sponsors.bonventure.net/?page=<account>`) serves six parishes here. A
  DuckDuckGo search for `sponsors.bonventure.net` with the parish's name, school or town finds
  a page the parish site hides; check the page header's street address, because same-named
  parishes elsewhere have their own accounts. Record `page-pdfs
  http://sponsors.bonventure.net/?page=<n>` over `http://` (the https host fails TLS
  verification in Python). Each account is its own bulletin: write a separate peer review for
  each pair of parishes on the host.
- **Self-hosted sites.** Read the file's first page before taking a site's first PDF as the
  bulletin: it can be a USCCB calendar, a registration form or a link to "thekidsbulletin.com".
  *Wix:* one `_files/ugd/` PDF replaced weekly, which can lag a Sunday or more; its cover names
  the Sunday, not a date, so `fetch:check` reports date and freshness unknown: date it from the
  Mass intentions. *Duda:* pages hide their PDF links from `probe get`'s text, so read the
  hrefs from plain curl of the page source; dated file names let `page-pdfs` pick the newest,
  even when the page's address or heading names an old year; PDFs on `irp.cdn-website.com` can
  have a garbled text layer (`fetch:check` reports the date unknown though the newest is
  picked): render page 1 and date it from the file name. *Fixed-name PDFs* overwritten weekly
  (`currbulletin3.pdf`): with no dated name `fetch:check` reports date and freshness `unknown`
  though the pick is right. *Joomla Weblinks* lists (hrefs
  `/index.php/component/weblinks/weblink/<id>-<title>?task=weblink.go`) 301 to each PDF, but no
  collector follows them and an unpinned `page-pdfs` picks another PDF on the page: the row is
  `unsupported` with `fetch_gap` `joomla-weblink-redirect` (hand refresh, 2026-11-07). Check
  the newest file's date before making a parish row: a mission's site can have stopped years
  ago.
- **Solutio CMS (Joomla) sites** link issues as `/bulletin/<n>-<date>/file` or
  `/home/bulletins/<id>-<date>/file`, with no `.pdf`, and answer 403 to plain fetches:
  `fetch:check` says `resolve_failed` under any recipe and `probe pdf` gets 403. Look for the
  parish's John Patrick listing first (two Solutio parishes have one). With none, `visit.py`
  still shows the bulletin list, the per-church pages (`/churches/<id>-<name>`, with Mass
  times), the home page's schedule and the staff page: map the churches from those pages, say
  no bulletin was read, and make the row `unsupported` with `fetch_gap` `joomla-file-endpoint`
  (hand refresh, 2026-11-07). `visit.py` on a Solutio home page can hang past its timeout while
  subpages load in seconds: go straight to them.
- **Sites `probe url` can't read** (403, JavaScript, a closed connection, a frameset's
  few-hundred-byte shell): use `visit.py`, `render.py` and `fetch:check`; the browser renders
  framed sites and can show a publisher link `probe url` missed. A Zumu Software frameset
  keeps its menu in `onclick` handlers: save `visit.py --html` and grep `location='…'` for the
  page paths. Don't try to get past a bot block: the sandbox denied a script downloading a
  blocked URL through the stealth browser and a curl with a spoofed User-Agent (map batches
  `collingswood-haddon` and `downbeach-linwood`). Leave the check `access-blocked` with a
  retry trigger.
- **Web search is rationed:** duckduckgo.com/html answers a bot challenge after a few
  searches, bing.com returns junk for exact-phrase queries, and the sandbox denies driving the
  stealth browser through a search engine's bot check (map batch
  `atco-sicklerville-williamstown`). Spend searches on finding a site or listing; date a
  closure from the Catholic Star Herald REST search and the parish's pages. nj.com answers 403
  to `probe get`, but `visit.py --text` renders its articles (hand refresh, 2026-11-07): quote
  one noting it was read in the browser; a search snippet is only a `note:` (map batch
  `salem-county-mullica-hill`).
- **J.S. Paluch / Discover Mass:** not seen here. Discover Mass caps downloads per IP per day
  (a 134-byte "Maximum number of files downloaded today" reply, which `fetch:check` reports as
  `not_pdf`): that is the cap, not the row.
- **Eastern Catholic eparchies:** confirm a GCatholic Eastern church on the eparchy's own list
  (ukrcatholic.org/parishes reads with `probe get`; stmaron.org's alphabetical pages,
  `/parishes-c` etc., with plain curl). GCatholic can list a church the eparchy no longer
  does, and its Eastern sites no longer resolve.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches in the territory (three Ukrainian, one Maronite) are excluded as other-jurisdiction, as in every neighbouring diocese. (accepted by survey-review, 002-survey-review, 2026-10-29)
- A merger decree ends a parish, not a church. A former parish church of a merged parish keeps a church row under the merged parish when its current bulletin or Mass schedule lists Mass there; it is excluded closed only on a source that says so (relegation decree, sale, or the bulletin's last Mass), with last_mass. A church a current source calls 'currently not open' is not closed: grep the parent parish's bulletins for its name first. One with dated public Masses there gets a church row with a revisit for the next dates (St. Bernard, Dorothy: St. Vincent de Paul's bulletins list Masses on 6 Sept, 4 Oct, 29 Nov and 25 Dec 2026, though the summer guide says 'Currently not open'); open/ is for one with no Mass found. (accepted by survey-review, 002-survey-review, 2026-10-29; the 'currently not open' clause amended by reconcile, 034-reconcile, 2026-10-29, on map batch `hammonton-mays-landing`'s finding)
- The Korean Catholic missions (St. Andrew Kim, Absecon; St. Yi Yun Il) are Latin and diocesan, not other-jurisdiction: a church row under the parish whose bulletin lists their Mass, a parish row of their own if they publish a readable bulletin, otherwise excluded no-bulletin (README Settled policy 4). (accepted by survey-review, 002-survey-review, 2026-10-29)
- A seasonal shore church keeps its church row with a dated revisit for its next season (Wilmington's rule). Before calling a church seasonal, check the summer guide against an off-season bulletin's masthead ('Masses celebrated Memorial Day-Labor Day') or the parish's own 'Winter Schedule' page with a no-Mass line; the guide gives no dates, so take them from that source and set `revisit_after` just after the season opens. The same sources show which churches are year-round: there the guide's times are only the summer additions. (accepted by survey-review, 002-survey-review, 2026-10-29; extended by map batches `ocean-city-marmora-sea-isle`, `avalon-court-house` and `wildwood-cape-may`, 2026-10-29)
- Monastery and shrine chapels follow Philadelphia's rule: a church row under a parish whose bulletin lists their public Mass, a parish row if they publish their own bulletin, otherwise excluded no-public-mass or no-bulletin. A GCatholic 'Mission of' a parish whose bulletin has no Mass line for it is excluded no-public-mass, with the pages searched and the absence described in research; one the diocese's own news reports closed is excluded closed with `last_mass` from that article (Monastery of the Perpetual Rosary, Camden). (accepted by survey-review, 002-survey-review, 2026-10-29; extended by map batches `galloway-absecon` and `camden-city`, 2026-10-29)
- A shared pastor is not a shared bulletin. Parishes whose mastheads name one priest as pastor of one and administrator of the other keep separate rows when each publishes its own bulletin with its own masthead and Mass times (St. Mary and St. Thomas More, Cherry Hill). The assignments name pastors only, so read both mastheads before calling two parishes one. (map batch `cherry-hill`, 2026-10-29)
- A merged parish's churches come from its current bulletin's masthead (the whole address block and page 1 Mass-schedule column) and its own Mass-schedule page, not the rosters: a church listed there with Mass gets a church row even when no roster has it (St. Luke, Stratford), and so does a new daily-Mass chapel on a parish's campus (the home page names one the bulletin calls only 'the chapel'). A church named only in a bulletin's Sanctuary Lights or intentions is not a place of Mass: read the parish's own page for it before counting it. Nor is a building the bulletin lists only under 'OPEN FOR PRIVATE PRAYER' and its page 1 schedule omits, even on a 'Places of Worship' page: it is excluded no-public-mass. (map batch `runnemede-blackwood-lindenwold`, 2026-10-29; extended by map batches `vineland`, `millville-newfield`, `hammonton-mays-landing` and `avalon-court-house`, 2026-10-29)
- Before filing a merged parish's former church in open/ or closed, read the merger's establishment decree: the 2009–2011 decrees name the worship sites the new parish keeps, and a decree's list of uniting parishes untangles a GCatholic place name that is only a mailing address. Decrees, and the relegation decrees that date later closures, are on camdendiocese.org (`/wp-json/wp/v2/search?search=<word>`, then `/wp-json/wp/v2/posts/<id>`; `search=relegation`) and in the Catholic Star Herald's decree posts. The 2014 Camden County decree PDFs answer 404: use the 2014 articles. (map batches `woodbury-paulsboro` and `salem-county-mullica-hill`, 2026-10-29; extended by map batches `gloucester-bellmawr-haddon-heights` and `bridgeton`, 2026-10-29)
- A GCatholic church of a merged parish that the current bulletin and Mass schedule omit is dated closed from a Catholic Star Herald article (its REST search on the parish and the town), with the article's merger plan for the worship sites kept when no decree text names them. A closed church needs a source saying it is closed, not a date: with an article saying so and the current bulletin omitting it, it is excluded closed with `last_mass` left empty when nothing gives the date, as README's `closed` row allows (St. Monica, Atlantic City). Before filing such a church open or closed, search the Star Herald's REST posts and the Bishop's Schedule for its name: a regular ethnic-apostolate Mass the weekly bulletin never lists keeps it a church of the parish (St. Francis de Sales, Barrington, Igbo Catholic Apostolate; the batch flagged that choice for review). (map batch `atlantic-city-brigantine`, 2026-10-29; extended by map batch `gloucester-bellmawr-haddon-heights`, 2026-10-29; the no-date clause by reconcile, 034-reconcile, 2026-10-29)
- When a parish posts its printer's issues on its own platform too, the row reads the printer's listing if the parish copy runs behind it, even by a week, and keeps the parish copy's id in `publication` (St. Rose of Lima: John Patrick 646 over eCatholic 35649). (reconcile, 034-reconcile, 2026-10-29)
- A church a current bulletin lists with Mass stays under that parish even when an older merger decree named it a worship site of another (St. Elizabeth, Goshen: Our Lady of the Angels' bulletin and site list it; the 2011 Kolbe decree named it). (reconcile, 034-reconcile, 2026-10-29)

## Seeding precedents

Seed questions `seed-review` settled that no rule covered: the situation, the choice and the parishes. Later reviews in this diocese follow them; only the owner turns one into a rule.

- Add the Immaculate Conception holy-day Masses (Dec 7 4:30 PM vigil at St. Joseph, Dec 8 7 PM Spanish at the Cathedral)? → Leave out. Against the lean. POLICY, Dates: the newest bulletin's Holy Days box (8c167dcd p1: '12:05pm Bilingual, 7pm Español Catedral, 4:30pm Vigil Mass St. Joseph Polish') gives no date, and Dec 8 would be projected from the calendar. The only date, 'December 7th', comes from the website, whose Sunday times are stale (10:00 vs 10:15, 11:30 vs 12 pm), so R6 doesn't let it pin the date. Across this batch, undated holy-day boxes are settled as excluded (this seed's s19, christ-the-redeemer s16, infant-jesus s21), and update mode will read the December issues that date them. Hard because Dec 8, 2026 is certainly a holy day and the box's times are probably right. (cathedral-of-the-immaculate-conception-camden s20; 057-seed-review, 2026-11-19)
- Tuesday/Wednesday confession 'following 8:00 am Mass' is listed as held at St. Isidore, but those Masses are at the Sacred Heart High School Chapel. Add 8:30 AM confession at St. Isidore? → Leave out. Lean kept. a9cdc270 p1 says 'Reconciliation held at ST. ISIDORE THE FARMER CHURCH Tuesday-Saturday: Following 8:00 am Mass', but the Tuesday-Wednesday 8:00 Mass is at the Sacred Heart High Chapel (same box), so 'following' it at St. Isidore can't be right as printed. The likely place is the unlisted school chapel (R23), and a wrong place is worse than none. (christ-the-good-shepherd-vineland s15; 057-seed-review, 2026-11-19)
- Adoration at St. Isidore runs from after the Thursday 8:00 AM Mass until 7:45 AM Friday (overnight). Record it as Thursday 8:30 AM-11:59 PM plus Friday 12:00-7:45 AM? → Split at midnight. Lean kept. a9cdc270 p1: 'ADORATION (at ST. ISIDORE'S) Begins after the Thursday 8:00 am Mass until Friday at 7:45 am'. The start is R10's 8:30 AM. Splitting at midnight states the printed hours exactly, since one slot can't cross midnight. (christ-the-good-shepherd-vineland s26; 057-seed-review, 2026-11-19)
- Keep the Sunday 7:30, 9:00 and 11:00 AM Masses year-round, or follow the website's summer schedule? → Year-round; leave the summer times to update mode. Lean kept. The intentions of both issues (c7f61855 p6: Sunday 7:30, 9:00, 11:00 AM on Nov 15 and 22) settle the Sunday Masses now. The website's summer split is labelled 'through June 15, 2025', and summer is seven months away, so update mode will read the summer change from the bulletins. (christ-the-king-haddonfield s7; 057-seed-review, 2026-11-19)
- Add the website's summer Sunday 8:00 and 10:00 AM Masses (June 22-Labor Day)? → Leave out; update mode will read the summer bulletins. Lean kept, matching group sunday-summer: summer-only Masses that are out of season at as_of and come only from the website are left to update mode. The same call was made for st-maximilian-kolbe-marmora s11 and matches notre-dame-de-la-mer's settled R33 exclusions. (christ-the-king-haddonfield s10; 057-seed-review, 2026-11-19)
- Add the website's Sunday Confessions (8:45 and 10:45 AM Labor Day-June 30; 9:45 AM July 1-Labor Day)? → Yes, Labor Day approximated as the start of September. Lean kept. R6: the confession page ('Confessions are heard on Sundays at 8:45 & 10:45 AM (Labor Day to June 30), 9:45 AM (July 1 to Labor Day)') is the parish's own. It fits the 9:00 and 11:00 Masses in the intentions, and no bulletin prints a confession time to contradict it. A September 1 start overstates the season by a few days at most. The 9:45 summer time comes along with its group, a minor inconsistency with leaving out the summer Masses. (christ-the-king-haddonfield s12; 057-seed-review, 2026-11-19)
- Add the Thanksgiving Day 9:00 AM Mass on Thursday, November 26? → Thursday, Nov 26, 9:00 AM. Lean kept. The website's standing schedule says 'Weekday Mass Monday – Friday 8 AM. Thanksgiving Day 9 AM', a recurring holiday line rather than a dated 2025 item. Nov 26 is after as_of, and the weekly Thursday 8 AM stays (R17). Thin, since no bulletin yet prints it. (christ-the-king-haddonfield s16; 057-seed-review, 2026-11-19)
- Weekday 7 AM Mass: 'No 7 a.m. Mass from Memorial Day through early September'. Record it as September through May? → Mon-Fri 7 AM, September-May. Lean kept. f90eb20b p1 prints 'Monday - Friday 7 a.m. and 8:30 a.m. (No 7 a.m. Mass from Memorial Day through early September)'. September-May is the nearest month season (POLICY, Weekly qualifiers) and is right now. It overstates only late May and early September. (church-of-the-incarnation s1; 057-seed-review, 2026-11-19)
- Keep Saturday 3-4 PM Confession at St. Francis, printed only in the Nov 8 bulletin? → Saturdays 3:00-4:00 PM. Lean kept. 5c3f2a19 p7 gives a standing notice, 'Confessions Every Saturday of the month from 3pm – 4pm at St. Francis of Assisi Church'. The newest issue prints no confession time of any kind, so it omits rather than contradicts. R36 needs two older issues and only one is stored. (divine-mercy-vineland s20; 057-seed-review, 2026-11-19)
- Add the Friday 7-8 PM Confession at St. Teresa that only the website lists? → Fridays 7-8 PM, during Adoration. Lean kept. R6: the website says 'Come join us every Friday at Saint Teresa Church Adoration and Confessions from 7-8PM'. Its other times match both bulletins, and the Friday 7 PM Adoration is in the newest box (bce0d99a p3). The Confessions paragraph's silence about Friday is a missing mention, not a conflict. (holy-child-runnemede s20; 057-seed-review, 2026-11-19)
- Add the December 12 Advent Holy Hour, which invites liturgical ministers and their families? → Leave out. Lean kept. bce0d99a p6 titles it 'Advent Holy Hour for Liturgical Ministers' and invites lectors, sacristans, EMHCs, cantors, servers 'and their families'. POLICY leaves out services the bulletin limits to a group or holds by invitation, and no end time is given. (holy-child-runnemede s21; 057-seed-review, 2026-11-19)
- Add Friday 9 AM-5 PM Adoration in Our Lady of Guadalupe Chapel, and at which church? → Leave out. Lean kept. 324bb165 p3: 'Adoration is held in Our Lady of Guadalupe Chapel on Fridays from 9:00 a.m. - 5:00 p.m.' No source places the chapel, the parish also has a convent (745 Third St.) and a rectory (334 Beech Ave.) at other addresses, and `seed church` finds no such chapel. POLICY: a chapel whose location is unclear is left out. (infant-jesus s22; 057-seed-review, 2026-11-19)
- Add the website's Sunday 11:00-11:15 AM Confession at St. John Vianney? → Leave out. Lean kept. The newest Reconciliation box (324bb165 p1) gives 'Saturdays 9:00-9:30 AM; 2:30-3:30 PM at St. Margaret Church' and nothing on Sunday. The website page that adds Sunday 11:00-11:15 also misplaces the 6:45 Mass and omits the Saturday 8:30, so it is partly stale (R6). (infant-jesus s23; 057-seed-review, 2026-11-19)
- Add the website's First Friday 7:30 AM confession? → Leave out. Lean kept. Only the website gives 'First Friday --7:30 AM Confession', and its other confession minutes differ from both bulletins. The weekly Friday 7:40-7:55 AM confession (s16, c5cdb3b2 p1) already covers first Fridays. (mater-ecclesiae-berlin s27; 057-seed-review, 2026-11-19)
- Add the website's Saturday 4:00-4:55 PM confession before the 5:00 PM Mass? → Saturdays 4:00-4:55 PM. Lean kept. R6: the current homepage gives 'Saturday 5:00 pm: Anticipated Low Mass ... Confessions: 4:00 pm to 4:55 pm'. The bulletin's per-day list (c5cdb3b2 p1) prints the 5:00 PM Mass with no confession line, a missing mention rather than a conflict. Its minutes may be a little off, like the site's other confession times. (mater-ecclesiae-berlin s28; 057-seed-review, 2026-11-19)
- Add the website's Tuesday Adoration, 9 AM-6 PM in Assumption Church? → Tuesdays 9 AM-6 PM. Lean kept. Both bulletins (8b499ad3 p2) announce 'Extended Adoration Hours on Tuesdays', which confirms Tuesday hours are current, and the website gives them as 9am-6pm in the Church of the Assumption (R6). (notre-dame-de-la-mer s22; 057-seed-review, 2026-11-19)
- Add Tuesday Benediction at 7 PM in Assumption Church (website only)? → Leave out. Lean kept. Website only. 'followed by Benediction, beginning at 7pm' leaves an hour's gap after the 6 PM end, and the page says the Benediction service is 'coming soon'. (notre-dame-de-la-mer s23; 057-seed-review, 2026-11-19)
- Add the website's Mon, Wed, Thu, Fri Adoration, 9 AM-1 PM in the St. Joseph Room, Assumption Church? → Leave out. Against the lean. The only source is the website line 'See Sign up Sheet for Monday Wednesday Thursday Friday Adoration from 9am until 1pm in the Saint Joseph Room', under 'NEW ADORATION SCHEDULE ... SIGN UP SHEET - COMING SOON', which reads as a schedule still being staffed. The bulletins confirm only Tuesday. 'Extended' Tuesday hours don't establish 9-1 on the other days. Including it would also overlap the settled third-Monday Holy Hour (s13). (notre-dame-de-la-mer s24; 057-seed-review, 2026-11-19)
- Our Lady of Grace Chapel is in Lindenwold, entered through the old Spanish Office; is it on the St. Lawrence grounds (135 N. White Horse Pike)? → Yes: record at St. Lawrence. Lean kept. bb415c6f p4 calls it 'Our Lady of Grace Chapel, Lindenwold, NJ', and St. Lawrence is the parish's only church in Lindenwold. p1 says 'Enter the Chapel through the old Spanish Office'. The current Hispanic office is at 55A Warwick Rd., Stratford (p9), so the old one points to the St. Lawrence/Shrine buildings. (our-lady-of-guadalupe-lindenwold s14; 057-seed-review, 2026-11-19)
- The weekend Mass schedule and Saturday afternoon confessions name no church. Which church are they at? → St. Agnes. Lean kept. The newest box (53744ff8 p1) names a church only for the Spanish Masses (St. Jude). Every Christmas and New Year Mass is 'St. Agnes Church' (p7), the tree lighting after the 4:30 Mass ends at the parish center (St. Agnes's address), and youth walk from the 6:00 PM Mass to the parish center. Missing: any line naming the church for the English weekend Masses. (our-lady-of-hope-blackwood s3; 057-seed-review, 2026-11-19)
- The weekday Masses, Saturday 9 AM Mass, Friday Adoration, and Monday/Saturday-morning confessions name no church. Which church are they at? → St. Agnes. Lean kept, with thin evidence. 53744ff8 p1 gives 'MONDAY-FRIDAY: 8:00AM AND 9:00AM', Friday exposition 'following 9AM Mass' and confessions with no church. The p7 penance schedule names no church either. The parish office is at St. Agnes and nothing places weekday services at St. Jude. Missing: whether the two weekday Masses are at different churches. (our-lady-of-hope-blackwood s9; 057-seed-review, 2026-11-19)
- Is the St. John Neumann Adoration Chapel (open daily 5:30am-9pm) at St. Mary Church, 32 Carroll Ave? If so, add its daily hours as Adoration there. → Daily 5:30 AM-9:00 PM at St. Mary. Against the lean, to decide this the same way as our-lady-of-sorrows-linwood s12 and st-peter-merchantville s17. In each, a one-church parish's own Adoration chapel is printed in its schedule box with no other address. 0b01819a p1 lists 'ST. JOHN NEUMANN ADORATION CHAPEL Open Daily: 5:30am-9:00pm' in the box whose only address is St. Mary Church's 32 Carroll Ave. p3 calls it the 'Eucharistic Adoration Chapel' (R38), and a 'St. John Neumann Chapel Light' is sponsored beside the Sanctuary Light. The lean's worry, that it might be off-site, has no evidence behind it. No exposition is claimed. (our-lady-of-peace-williamstown s21; 057-seed-review, 2026-11-19)
- Add the parish's perpetual Adoration (24 hours a day, 7 days a week) at Our Lady of Sorrows church? → Every day, all day. Lean kept. 07859944 p1 prints 'Our Lady of Sorrows Church / A Perpetual Eucharistic Adoration Parish, 24 hours a day, 7 days a week / 724 Maple Avenue', with a current adorer roster ('Adorers Needed: Thursday - 3:00 am'). It is a one-church parish, decided the same way as Williamstown and Merchantville. 00:00-23:59 is the format's nearest to continuous. (our-lady-of-sorrows-linwood s12; 057-seed-review, 2026-11-19)
- Weekly confessions are printed 'When Fr. Pinzon is presiding at Mass'. Include them as weekly slots? → Include weekly. Lean kept. 032b5867 p5 prints the confession times in the regular schedule box 'When Fr. Pinzon is presiding at Mass', and he is the pastor who presides most weeks. The batch includes hedged printed schedules with the hedge in a note (st-michael-the-archangel-clayton s11, s14). (our-lady-of-the-lakes-collings-lakes s11; 057-seed-review, 2026-11-19)
- Add Saturday Adoration after the 8:00 AM Mass (from 8:30 AM, no end time)? → Saturdays from 8:30 AM. Lean kept, though hard. e2f4fe60 p10 prints 'Weekday Monday - Saturday 8:00 AM / Rosary and Adoration after 8:00 AM Mass', and the website's Mass Schedule says Monday-Saturday too. The same page's Eucharistic Adoration list gives only 'Monday through Friday 8:30 AM to 9:30 AM'. Two lines include Saturday and one is silent on it. R10 gives 8:30 AM, and no end is printed. (st-andrew-the-apostle-gibbsboro s20; 057-seed-review, 2026-11-19)
- Add the Holy Childhood Association's Monday 7-8 PM hour 'before the Blessed Sacrament' as weekly Adoration? → Leave out. Lean kept. The Holy Childhood Association's Monday hour 'before the Blessed Sacrament' is a group's meeting with no place given, never called Adoration or a Holy Hour, and printed in the newest issue only. (st-charles-borromeo-sicklerville s19; 057-seed-review, 2026-11-19)
- Record the December 16 Advent Penance Service at St. Augustine as a Confession? → Confession Dec 16 6:00 PM. Lean kept. POLICY counts Penance as Confession, and an Advent Penance Service at St. Augustine is the parish's communal celebration of the sacrament. Its 6:00 PM start is when penitents should come. Missing: an explicit mention of individual confessions. (st-damien-ocean-city s30; 057-seed-review, 2026-11-19)
- Add the website's weekday confession times? Its Penance page gives both 5:00 PM and 9:00 AM (after Mass) Monday-Saturday, and no bulletin prints confessions. → Leave out. Lean kept. Neither bulletin prints confessions, and the website's Penance page gives both 5:00 PM and 9:00 AM Monday-Saturday on one page. R6 can't settle a time the site contradicts itself on. (st-joseph-pro-cathedral-camden s14; 057-seed-review, 2026-11-19)
- Add the Thanksgiving Children's Mass on Tue Nov 24 at SVP? The bulletin gives only the class block 3:45-5:00, not the Mass's start. → Leave out. Lean kept. Only the class block '3:45-5:00' is printed, not the Mass's start. POLICY skips events without a definite start time. (st-joseph-the-worker-haddon-township s20; 057-seed-review, 2026-11-19)
- Immaculate Conception: are the 7 PM Masses on Monday Dec 7 (vigil) or Tuesday Dec 8? → Monday, December 7, 7 PM. Lean kept, though the print contradicts itself. 6e5f96a2 p6 says 'Holy Day of Obligation MONDAY, DECEMBER 7, 2026', with 'Novena: SATURDAY, NOV 28 - SUNDAY, DEC 6' ending the day before it, and then 'MASS MONDAY 12/8' (in 2025, Dec 8 was a Monday, so the line looks carried over). Three of the four signals say Monday, Dec 7, and evening Masses fit a vigil. Update mode should confirm from the December issues. (st-mary-of-mount-carmel-hammonton s24; 057-seed-review, 2026-11-19)
- Add St. Casimir's summer Sunday 9:00 AM Mass (Memorial Day to Labor Day)? → Leave out. Against the lean. The bulletins (db9c55c4) say only that St. Casimir has Masses Memorial Day-Labor Day, and the 9:00 AM time is on the homepage alone. A summer-only, website-only Mass that is out of season at as_of is left to update mode, as in christ-the-king-haddonfield s10 and notre-dame-de-la-mer's settled R33 exclusions. A June 1-August 31 season would also be an invented boundary (R33). (st-maximilian-kolbe-marmora s11; 057-seed-review, 2026-11-19)
- Include the Confession times marked '* If Fr. Goyette is Available'? → Include with note. Lean kept. f8284d21 p1 prints the times in the regular Confession box ('Friday: 7:40-8:10 PM at Nativity*', '* If Fr. Goyette is Available'), and he is the pastor. Included with the hedge in a note, as in our-lady-of-the-lakes s11. (st-michael-the-archangel-clayton s11; 057-seed-review, 2026-11-19)
- Include Sunday Confession 'after most 10:30 AM Mass' at Nativity (11:30 AM per POLICY)? → Sundays 11:30 AM with note. Lean kept. f8284d21 p1: 'Sun. after most 10:30 AM Mass at Nativity', in the regular box of both issues. R10 puts it at 11:30 AM, with the hedge in the note. (st-michael-the-archangel-clayton s14; 057-seed-review, 2026-11-19)
- Include Monday-Friday Adoration 7:15 AM-8:00 PM in the parish Adoration Chapel at St. Peter? → Mon-Fri 7:15 AM-8:00 PM. Lean kept. 'EXPOSITION OF THE BLESSED SACRAMENT: Monday – Friday: 7:15 a.m. – 8:00 p.m. (Church opens 7:10 a.m.)' on the homepage, the Nov 8 pastor's letter and the newest bulletin's 'Adoration Chapel: See Website' (f465bcf5 p1) tie the chapel to the one church, St. Peter. Decided the same way as Linwood and Williamstown. (st-peter-merchantville s17; 057-seed-review, 2026-11-19)
- Record the Adoration Chapel closures on November 26 and 27 (only if weekday Adoration is kept)? → Record both closures. Lean kept. The weekday Adoration is included, and the newest bulletin says 'CHAPEL IS CLOSED November 26 and 27' (R16). (st-peter-merchantville s22; 057-seed-review, 2026-11-19)
- Saturday confession at St. Vincent de Paul: the bulletin's 4:00-4:30 PM or the website's 4:00-4:45 PM? → 4:00-4:30 PM (bulletin). Lean kept (C8 sets no lean). Both dated weekly issues (657ad45c p1: 'Saturday 4:00 pm to 4:30 pm') give 4:30. The website's 4:45 is the older, undated source. (st-vincent-de-paul-mays-landing s9; 057-seed-review, 2026-11-19)
- Add the Thanksgiving Day Mass, Thu Nov 26 9 AM, at St. Vincent de Paul Church? → Nov 26 9:00 AM at St. Vincent de Paul. Lean kept. St. Vincent de Paul is the only church with any printed schedule, since St. Bernard Mission has none in either bulletin or on the website. The weekly Thursday 7 AM stays (R17). (st-vincent-de-paul-mays-landing s10; 057-seed-review, 2026-11-19)
- Add the Confirmation Mass with Bishop Sullivan, Sun Nov 22 12:30 PM, at St. Vincent de Paul Church? → Nov 22 12:30 PM at St. Vincent de Paul. Lean kept. POLICY closes only Masses the bulletin limits, and the Confirmation Mass notice doesn't limit it. Placed at St. Vincent de Paul for the same reason as s10. (st-vincent-de-paul-mays-landing s11; 057-seed-review, 2026-11-19)
- Which church holds the Wednesday 4-6 PM confessions on the Rectory Porch? → St. Mary Magdalen, rectory porch. Lean kept. a5db9a60 p1: 'Wednesday: 4:00PM - 6:00PM - Rectory Porch'. The rectory is on the 621 Dock St. grounds shared by both listed sites (POLICY: on the same grounds belongs to that church). It is attached to the parish church with the porch in the note. (the-parish-of-all-saints s17; 057-seed-review, 2026-11-19)
- Where is the first-Saturday 9:00 AM Purgatorial Society Mass? → St. Mary Magdalen. Lean kept. a5db9a60 p1 lists '1st Saturday of each month, 9:00am Purgatorial Society Mass' above the weekend Masses. Only the weekday Masses are marked 'in the chapel', so the rest default to the church. (the-parish-of-all-saints s18; 057-seed-review, 2026-11-19)
- Where is the Thanksgiving Day 9:00 AM Mass on November 26? → St. Mary Magdalen. Lean kept. A parish-wide Thanksgiving Mass with a food blessing goes to the church. Only the weekday Masses are marked as being in the chapel. (the-parish-of-all-saints s19; 057-seed-review, 2026-11-19)
- Where are the Immaculate Conception Masses (Dec 7 4 PM vigil, Dec 8 7 PM)? → St. Mary Magdalen. Lean kept. The holy-day vigil at the weekend vigil time, followed by the Grand Illumination, goes to the church, as for s18 and s19. These are dated notices, unlike the undated holy-day boxes left out elsewhere. (the-parish-of-all-saints s20; 057-seed-review, 2026-11-19)
- Is the Saturday 4:15 PM vigil an 'evening Mass' with confessions 3:45-4:05 PM before it? → Saturdays 3:45-4:05 PM. Lean kept. ee67b72f p2: 'A priest is available for confessions 30 minutes prior to all evening Masses, Monday through Saturday. The last confession will be heard 10 minutes prior'. A Saturday vigil is an evening Mass in the usual sense, and the website repeats the line under OLSS, which has the 4:15. (the-parish-of-saint-monica s29; 057-seed-review, 2026-11-19)


## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: Hand refresh against main (no factory job: the Run's PR #175 was ~87 commits behind). Coverage unchanged: directory 65/65 accounted for (63 churches, 1 excluded, 1 open), GCatholic 119/119 (96, 13, 10), summer guide 32/32; 63 parish rows, 107 churches, 15 excluded, 11 open. No merges or moves; `audit --fetch` found only the six Bon Venture accounts' 15 pairs, all settled by their `separate` reviews. `fetch:check` on all 63 rows: 59 ok (8 November issues, St. Joachim and All Saints 1 November), 4 resolve_failed, now `unsupported` with a `fetch_gap`, so `promote` takes them and their churches off the site: Holy Cross, Bridgeton and Holy Trinity, Downbeach (`joomla-file-endpoint`), St. Bridget University Parish (`po-org-unknown`), St. John Neumann (`joomla-weblink-redirect`). Tried each `open/` record once more (8 November bulletins, Star Herald searches); none settled. Read the 2016 nj.com article in the browser: Queen of the Apostles' final Sunday Mass was 2016-08-28. Condensed the playbook (publishers 19.6 → 8.7 KB, rules 9.0 → 6.6 KB: two rules merged into one, eight reworded).
- 2026-10-29: Reconciled (034-reconcile) after 24 map batches of 4 to 15 roster entries (usually 8 to 11). Coverage: directory 65/65 accounted for (63 churches, 1 excluded, 1 open), GCatholic 119/119 (96, 13, 10), summer guide 32/32 (32 churches); 63 parish rows, 107 churches (8 in no roster), 15 excluded, 11 open. No merges or church moves: the audit's only candidates were the six Bon Venture accounts, each with its own masthead, now with separate peer reviews for every pair. St. Rose of Lima moved from its eCatholic copy to its John Patrick listing (646). `fetch:check` on all 63 rows: 59 ok (current or a week old; St. Padre Pio and Our Lady of Perpetual Help, Galloway post a week late), 4 resolve_failed (Holy Cross, Holy Trinity: Solutio 403; St. Bridget: ParishesOnline widget 502; St. John Neumann: Joomla weblinks). Corrected the intro and Sources on shared pastors; amended the 'currently not open' rule and integrated the map jobs' lessons.
- 2026-10-29: Initialised (factory survey, Run camden-map-1). Rosters: GCatholic (119
  entries), the diocese's Parish/School Locator as `directory` (65, schools dropped), the 2026
  shore summer Mass schedule as `summer-guide` (32). Planned 24 map batches in `batches.json`
  (216 entries, none excluded). No records yet.
