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
promoted: 2026-10-30
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

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: Hand refresh against main (no factory job: the Run's PR #175 was ~87 commits behind). Coverage unchanged: directory 65/65 accounted for (63 churches, 1 excluded, 1 open), GCatholic 119/119 (96, 13, 10), summer guide 32/32; 63 parish rows, 107 churches, 15 excluded, 11 open. No merges or moves; `audit --fetch` found only the six Bon Venture accounts' 15 pairs, all settled by their `separate` reviews. `fetch:check` on all 63 rows: 59 ok (8 November issues, St. Joachim and All Saints 1 November), 4 resolve_failed, now `unsupported` with a `fetch_gap`, so `promote` takes them and their churches off the site: Holy Cross, Bridgeton and Holy Trinity, Downbeach (`joomla-file-endpoint`), St. Bridget University Parish (`po-org-unknown`), St. John Neumann (`joomla-weblink-redirect`). Tried each `open/` record once more (8 November bulletins, Star Herald searches); none settled. Read the 2016 nj.com article in the browser: Queen of the Apostles' final Sunday Mass was 2016-08-28. Condensed the playbook (publishers 19.6 → 8.7 KB, rules 9.0 → 6.6 KB: two rules merged into one, eight reworded).
- 2026-10-29: Reconciled (034-reconcile) after 24 map batches of 4 to 15 roster entries (usually 8 to 11). Coverage: directory 65/65 accounted for (63 churches, 1 excluded, 1 open), GCatholic 119/119 (96, 13, 10), summer guide 32/32 (32 churches); 63 parish rows, 107 churches (8 in no roster), 15 excluded, 11 open. No merges or church moves: the audit's only candidates were the six Bon Venture accounts, each with its own masthead, now with separate peer reviews for every pair. St. Rose of Lima moved from its eCatholic copy to its John Patrick listing (646). `fetch:check` on all 63 rows: 59 ok (current or a week old; St. Padre Pio and Our Lady of Perpetual Help, Galloway post a week late), 4 resolve_failed (Holy Cross, Holy Trinity: Solutio 403; St. Bridget: ParishesOnline widget 502; St. John Neumann: Joomla weblinks). Corrected the intro and Sources on shared pastors; amended the 'currently not open' rule and integrated the map jobs' lessons.
- 2026-10-29: Initialised (factory survey, Run camden-map-1). Rosters: GCatholic (119
  entries), the diocese's Parish/School Locator as `directory` (65, schools dropped), the 2026
  shore summer Mass schedule as `summer-guide` (32). Planned 24 map batches in `batches.json`
  (216 entries, none excluded). No records yet.
