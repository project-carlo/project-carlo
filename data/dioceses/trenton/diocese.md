---
name: Roman Catholic Diocese of Trenton
state: NJ
website: https://dioceseoftrenton.org
status: exploring
gcatholic: tren1
city_aliases:
  Point Pleasant Boro: Point Pleasant Borough
  Princeton Jct: Princeton Junction
  Millstone Twp: Millstone Township
  Barnegat Township: Barnegat
---

Four counties of central New Jersey: Mercer (Trenton, Hamilton and Yardville, Ewing and West
Trenton, Lawrenceville, Princeton, West Windsor, Hightstown, Hopewell, Pennington, Titusville),
Burlington (Willingboro, Beverly, Riverside, Delran, Riverton, Cinnaminson, Maple Shade,
Moorestown, Mount Laurel, Marlton, Medford, Tabernacle, Mount Holly, Hainesport, Browns Mills,
Burlington, Bordentown, Florence, Roebling, New Egypt, Wrightstown), Monmouth (Freehold,
Howell, Farmingdale, Manalapan, Marlboro, Colts Neck, Holmdel, Middletown, Keansburg, Keyport,
Matawan, Red Bank, Rumson, Long Branch, Eatontown, Asbury Park, Neptune, Belmar, Spring Lake,
Manasquan) and Ocean (Point Pleasant, Brick, Lakewood, Jackson, Toms River, Lavallette and the
Seaside barrier island, Bayville, Forked River, Barnegat, Long Beach Island, Little Egg Harbor).
Neighbours: Camden to the south (mapped by the factory, Run camden-map-1), Philadelphia across
the Delaware (mapped, Run philadelphia-map-1), Metuchen to the north (not mapped).

The diocese has **97 parishes** ("97 parishes", dioceseoftrenton.org/about-us, read
2026-10-30), down from 127 in 2005 and 107 in 2015 (The Monitor, 2020-06-26). They are grouped
into **30 cohorts** within eight deaneries and four county vicariates (the July 2024 cohort
list, Sources). A cohort is a collaboration group, **not a family with one bulletin**: the
January 2017 *Faith in Our Future* decisions set every cohort on a "Collaborative Model"
(parishes "remain distinct with their own pastor ... finances, census and sacramental books"),
and only some pairs or trios on a "Linkage Model" (one pastor, distinct parishes) or a
"Merger Model". So expect one parish, one bulletin as the common shape, with a merged parish
often keeping two or more churches (GCatholic's `group`), and shared bulletins where linkage
named one pastor: the Catholic Community of Hopewell Valley (St. Alphonsus, St. James, St.
George, one John Patrick listing), Sacred Heart, Bay Head with St. Pio, Lavallette (one
listing), the Cathedral with St. Joseph, Trenton and St. Isaac Jogues with St. John Neumann
(each with its own listing). The map jobs read the mastheads. `batches.json` gives each cohort
its own batch (small neighbouring cohorts combined) and the eight Eastern Catholic places one
batch.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (the `directory` roster):** the diocese's eCatholic parish finder,
  https://dioceseoftrenton.org/parishfinder, read 2026-10-30 with parish-site-access
  `finder.py` (Cloudflare refuses `probe url` and `probe get` on all of dioceseoftrenton.org;
  `visit.py` loads it). **98 pins, one per parish at its seat** (address, phone, website,
  coordinates), no worship sites, no pastors. 97 current parishes plus "St. Mary of the Lake
  Parish (now part of Our Lady of Guadalupe Parish)", Lakewood (merged 2020-07-01, The
  Monitor 2020-06-26). Two pins have no website: Korean Martyrs Parish and St. Joseph Parish,
  both Trenton. Websites are mostly current (the dead and moved ones are GCatholic's), but
  check each. Names are as the parishes style themselves ("Church of St Monica", "St. Mary R.C.
  Parish", "The Oratory Church of St. Anthony of Padua"). Good for the parish list, sites and
  coordinates; not for structure.
- **GCatholic:** `rosters/gcatholic.json` (key `tren1`; `tren0` is Trento, Italy), **136
  entries** with Plus Codes: 125 Latin churches, 3 chapels (St. Catherine, Farmingdale; Star of
  the Sea, Manasquan; St. Mary, New Monmouth) and **8 Eastern Catholic** places: St. Mary
  (Ruthenian), St. Basil (Romanian) and St. Josaphat (Ukrainian), Trenton; St. Mary (Romanian)
  and St. Nicholas (Ruthenian), Roebling; Our Lady of Perpetual Help (Ruthenian) and St.
  Stephen (Ukrainian), Toms River; the former Basilian Fathers of Mariapoch monastery, Matawan
  (Hungarian, "Former Church"). It lists **churches**, with the canonical parish in `group` for
  some, so it is the best list of worship sites, but it is **stale**: it still lists churches of
  parishes merged by the 2017 decisions as if separate (St. Mary, Bordentown, St. Clare,
  Florence and Holy Assumption, Roebling; St. Joseph and Jesus the Lord, Keyport; St. Jerome,
  West Long Branch and St. Mary, Deal; Ascension, Bradley Beach and St. Elizabeth, Avon; St.
  Catharine, Seaside Park and Our Lady of Perpetual Help, Seaside Heights; St. Andrew, Jobstown
  and Assumption, Wrightstown; St. Mary of the Lake, St. Mary and St. Anthony Claret,
  Lakewood; Divine Mercy and Blessed Sacrament-Our Lady of the Divine Shepherd, Trenton), and
  churches the decisions or The Monitor report closed (St. Peter, Riverside; Holy Spirit,
  Asbury Park). It **omits** the Cathedral (St. Mary of the Assumption, Trenton) and the
  Co-Cathedral (St. Robert Bellarmine, Freehold). Of its websites, 27 don't resolve, one is a
  spam squat (padrepionj.com) and one is parked (visitationchurch.com) (Bulletin publishers).
- **Cohorts (the diocese's grouping; not imported as a roster, since it adds no places):**
  "Parishes aligned by Cohorts/Deaneries, UPDATED JULY 2024" (header "5/13/24 updated"),
  https://files.ecatholic.com/14277/documents/2024/7/2024%20July%20-%20Updated%20%20Parish%20Cohorts%20and%20Deaneries.pdf,
  linked from dioceseoftrenton.org/planning (read 2026-10-30; text layer, `probe pdf` reads it).
  It lists all 97 parishes in 30 cohorts (1–25 from 2017, 26–30 "(new)"), with deans and
  episcopal vicars, and a few names: Cohort 3 "Disciples in Action", 6 "Lumen Christi", 8
  "Cath Community of Hopewell Valley", 19 "Gathered as One", 24 "RCCTR – Roman Catholic
  Churches of Toms River". It marks Cohort 27 (St. Vincent de Paul, Yardville and St. John the
  Baptist, Allentown) "*linkage delayed", and puts Korean Martyrs in parentheses under St. Ann,
  Lawrenceville and Immaculate Conception, Eatontown under Cohort 28. The 2021 version is on the
  same page (`/documents/2021/8/...`). `batches.json` follows it. Good for which parishes to
  research together; a cohort says nothing about bulletins.
- **Faith in Our Future decisions (pastoral plan, January 2017):**
  https://dioceseoftrenton.org/decisions (Cloudflare; `visit.py --text --chars 80000` reads it
  all), the Bishop's decisions per 2017 cohort with the working definitions of the
  collaborative, linkage and merger models. It names the **explicit linkages** (one pastor):
  St. Isaac Jogues and St. John Neumann; Christ the Redeemer and Sacred Heart, Mount Holly;
  St. James, St. Alphonsus and St. George (Hopewell Valley); the Cathedral and St. Joseph,
  Trenton; and planned ones (St. John, Allentown with St. Vincent de Paul by 2019, now "linkage
  delayed"; St. Dorothea with Precious Blood by 2019; Sacred Heart, Bay Head with St. Pio by
  2019; St. Andrew with Assumption by 2017, St. Ann, Keansburg with St. Catherine Laboure "to be
  determined", Holy Family, Union Beach with the merged Keyport parish "potential"). It names
  the **mergers** of 2017–2020 (Divine Mercy and Blessed Sacrament-OLDS into Sacred Heart,
  Trenton; St. Andrew and Assumption; Sts. Francis and Clare with St. Mary, Bordentown; St.
  Joseph and Jesus the Lord, Keyport; St. Jerome and St. Mary, Deal; Ascension and St.
  Elizabeth, Avon; St. Catharine of Siena and Our Lady of Perpetual Help, Seaside; St. Mary of
  the Lake and St. Anthony Claret, Lakewood) and church closures ("suspend all operations at St.
  Peter Church", Riverside, by July 2017; "potential suspension of operations of Holy Angels
  Church" in Hamilton). It is a plan: the 2024 cohort list shows which mergers happened as
  parishes, but whether each former church still holds Mass needs the bulletin. The planning
  page's "Parishes that Merged or Closed Since 2005" heading has nothing under it (checked
  in the page HTML, 2026-10-30), and there is no closed-parish list; the sacramental-records
  page (dioceseoftrenton.org/sacramental-records) only says records go to the absorbing
  parish.
- **Clergy:** no diocesan clergy directory. The Monitor's "Clergy Appointments" posts (2021–2026;
  `tools/monitor_search.sh "Clergy Appointments"`) are incremental and name one parish per
  priest in every post read; they don't establish any shared pastor. The linkages above come
  from the 2017 decisions; read each masthead for the current pastor.
- **The Monitor** (trentonmonitor.com, the diocesan news site): WordPress, and its REST API
  answers `probe get` (`tools/monitor_search.sh`, `tools/monitor_post.sh`). The search is
  full-text and noisy (national Catholic news is mixed in): search a parish name with the
  town, and read the post. Found: Holy Spirit Church, Asbury Park's closure (2020-12-04
  "Holy Spirit Church closure to help ensure Catholic presence in Asbury Park"; 2021-06-11
  "At closing Mass, Holy Spirit churchgoers bid farewell to iconic worship site"); the Lakewood
  merger (2020-06-26, effective 2020-07-01) and Our Lady of Guadalupe's "Holy Family School and
  Church campus" (2025-10-09).
- **Mass times:** no diocese-wide Mass-times list found (the site has the finder only).
- **Other jurisdictions in the territory:** GCatholic's eight Eastern Catholic places (above),
  all in batch `eastern-catholic`. Korean Martyrs is a Latin parish of the diocese (on the finder
  and in Cohort 7), not other-jurisdiction.

### Bulletin publishers here

From `probe url` on the 174 distinct websites in the two rosters, `visit.py --bulletin` on 20
that refused it or showed no publisher, and John Patrick listing scans (2026-10-30). Each batch
settles its own rows. Use the finder's website before GCatholic's, and verify both.

- **John Patrick Publishing prints most of this diocese**, as in Camden and Philadelphia.
  Parish sites link `jppc.net/onlinebulletins/<id>template.pdf` or `church-bulletin.org/?id=<id>`,
  which redirect to a `church-bulletin.org/<slug>` listing of dated PDFs
  (`/bulletin/<slug>/<yyyy-mm-dd>.pdf`). **Look the parish up in
  `scratch/trenton-map-1/tools/jppc-trenton.tsv` first**: 67 listings with ZIPs in the four
  counties (from Philadelphia's scan of ids 1–1300, 2026-10-28, and this Run's of 6000–6110,
  2026-10-30), 48 with a current edition. Ids here run 510–696 and 6000–6048. A listing with no
  edition is a dead or moved one, not a bulletin (Bay Head's own 6002, St. John the Baptist,
  Allentown 548, St. Theresa 545, Divine Mercy 629, Blessed Sacrament-OLDS 583, St. Michael,
  Trenton 530, "St. Ann & St. Michael", Lawrenceville 562). A listing's name can join two
  parishes ("The Catholic Community of Hopewell Valley" 547; "Saint Pio of Pietrelcina & Church
  of the Sacred Heart" 6003): read the masthead for its members. Record the row as `other` with
  `page-pdfs https://www.church-bulletin.org/<slug>`. When a parish also posts the issues on its
  own site, take whichever channel has the latest issue (Camden's and Philadelphia's rule: the
  parish copy often lags). Most issues in Camden were image-only: render pages 1–2 with
  `render.py` when `probe pdf` returns no text. church-bulletin.org answers 406 to a bare
  "Mozilla/5.0" user agent; plain curl and `probe pdf` work.
- **eCatholic:** common (ids seen: Sacred Heart, Mount Holly 14457; St. Isaac Jogues 13541;
  Corpus Christi 13717; St. Ann, Lawrenceville 20164; Holy Cross 37867; OLS-St. Anthony 2974;
  Resurrection 14711; St. Mary of the Lakes 12486; St. Benedict 39277 or 15175; St. Catharine,
  Holmdel 35015; St. John, Lakehurst 25374; St. Joseph, Millstone 11159; St. Leo 14276; St. Mary,
  Colts Neck 33474; St. Rose, Belmar 37219; St. Dominic 40144; St. Gregory 2431; St. Luke 36011;
  St. Peter 35377; St. Theresa 5085; Visitation 6597; St. Paul 28530; the Hopewell Valley
  parishes 22670). An eCatholic id is the bulletin only when `/bulletins` lists current
  `files.ecatholic.com/<id>/bulletins/` PDFs; several of these sites link a John Patrick listing
  instead. **`ecatholic:14277` is the Diocese of Trenton's own site**, embedded wherever a
  parish links a diocesan PDF (Our Lady of Good Counsel, West Trenton's olgcc.net shows it):
  don't record it. Read issues with parish-site-access `issues.py ecatholic`.
- **LPi / ParishesOnline:** St. Rose of Lima, Freehold (`lpi:0018000000Qx8o4AAB`), St. Anselm,
  Wayside (`lpi:0018000000Qx8nnAAB`), St. Ann, Keansburg (`lpi:0018000000Qx8pMAAR`, on a Duda
  `/bulletin9ab2b387` page). `probe po <lpi id>` gives the org and container. WeConnect (LPi)
  sites: St. Dorothea (bulletins on `uploads.weconnect.com/mce/<hash>/Bulletin DOR <date>.pdf`),
  and GCatholic's old stanselm.weconnect.com and holyspiritasburypk.weconnect.com.
- **Bon Venture:** St. Joseph, Toms River (`sponsors.bonventure.net/?page=3204`, found by
  `visit.py --bulletin` from its Solutio site). Camden found Our Lady of Perpetual Help, Maple
  Shade's account (2214). Record `page-pdfs http://sponsors.bonventure.net/?page=<n>` over
  `http://`; check the header's address, since same-named parishes have their own accounts.
- **Solutio CMS sites** (`/news/bulletin/<n>-<date>`, `/get-connected/bulletin/<n>-<date>/file`,
  `/parish-events/bulletin`, `/bulletin/7-latest-bulletin`): St. Mary, Barnegat; St. Barnabas,
  Bayville; Our Lady of Perpetual Help, Maple Shade; Our Lady Queen of Peace, Hainesport; St.
  Pius X, Forked River; St. Joseph, Toms River. In Camden their `/file` PDFs answered 403 to
  `probe get`, `render.py` and `fetch:check`: look for the parish's John Patrick listing or
  Bon Venture page first (St. Mary 563, St. Pius X 590 are current), and only then read the
  site with `visit.py`. St. Mary, Barnegat's list also has Word-document entries.
- **Self-hosted and other platforms:** St. John the Baptist, Allentown posts dated PDFs under
  `/sjrc/News & Bulletins/` ("October 25, 2026 Bulletin.pdf"); St. Stephen, Toms River
  (Ukrainian) `ststephenchurch.us/staging/pdf/Bul.<Month><d>,<yyyy>.pdf`; St. Catherine of Siena,
  Farmingdale on a `becdn.net` host ("84885-OCT-25-2026-BULLETIN.pdf"); St. Catherine Laboure's
  `bulletin.htm`; Immaculate Conception, Eatontown's `WeeklyBulletin/list.asp`; Epiphany's
  Joomla `/index.php/sunday-bulletins` (Camden: Joomla weblinks lists don't collect; pin a
  filename); St. Aloysius links a Constant Contact PDF; Duda (`irp.cdn-website.com`: St.
  Katharine Drexel, St. Gabriel), Squarespace (Our Lady of Perpetual Help-St. Agnes, St. Francis,
  LBI) and WordPress sites. Read the file before taking a site's first PDF as the bulletin (Sacred
  Heart, Bay Head's and St. Pio's first PDFs are registration forms).
- **Discover Mass / J.S. Paluch:** not seen in the survey. If a row uses it, Discover Mass caps
  downloads per IP per day (a 134-byte "Maximum number of files downloaded today" reply that
  `fetch:check` reports as `not_pdf`): that is the cap, not the row.
- **Sites that refused the probes (2026-10-30):** 18 domains answered 403 to `probe url`.
  momapnj.org and stcatharine-stmargaret.com refused the browser too (use John Patrick 513 for
  St. Catharine-St. Margaret; Mother of Mercy has no listing in the scan). Eleven loaded in
  `visit.py` (strobert.cc, jesusthegoodshepherd.org, olgcnj.org, stjosephtomsriver.org,
  seaswhiting.org, stmarkseagirt.com, stbarnabasbayville.com, churchofstpius.org,
  olphparish.com, ourladyqop.org, stmarybarnegat.com). Five GCatholic-only sites weren't tried
  in the browser (catholicchurchasburypark.org, churchofstdominic.com,
  churchoftheassumption.com, divineword.org, stpaulsprinceton.org); the finder's sites for those
  parishes are the ones to use.
  svdpnj.org failed TLS verification (try `http://` or the John Patrick listing 6044);
  lbisaintfrancis.org, smlcmt.net and stlukes-nj.org timed out (old GCatholic sites; the finder's
  are current). JavaScript-rendered (NO-PARISH-WORDS): holyfamily.us, saintpetersonline.org,
  stmarysbordentown.org. Don't try to get past a bot block: Camden's map jobs had a script
  downloading through the stealth browser and a curl with a spoofed User-Agent refused.
- **Dead, moved or hijacked domains (2026-10-30), all from GCatholic:** no DNS:
  divinemercyoftrenton.org, nativitychurchnj.web.officelive.com, standrewsjobstown.org,
  stannchurch.catholicworld.info, stelizabethavon.com, stmary.shoresurfer.com,
  sttheresa-littleeggharbor.com, avmbcc.org, cbs-olds.org, christthekingparishlongbranch.org,
  churchofstpiusx.net, holyinnocentschurch.com, jewelbythesea.org, olatrenton05.org,
  olqponline.org, stagnesnj.com, stcatharinesiena.com, stdorothea.org, stjames-nj.org,
  stjosephkeyport.com, stmarycoltsneck.com, stmaryofthelake.org, stmichaels-westend.com,
  stmichaelstrenton.com, stsfnc.org, thechurchofstgeorge.org, ukrcathchurch.com.
  **padrepionj.com** (St. Bonaventure, Lavallette) redirects to a gambling spam site and
  **visitationchurch.com** to a domain-sale page: don't store either. Moved:
  IncarnationStJames.com → incarnationstjames.org; churchofepiphany.org → churchofepiphanynj.org;
  mycorpuschristichurch.com → ccnj.church; parishofsacredheart.org → sacredheartmh.org;
  stisaacjogues.org → cosij.org; stmarychurchnj.org → mmog.church.
- **Eastern Catholic eparchies:** confirm a GCatholic Eastern church on the eparchy's own list
  before excluding it (Camden: Ukrainian ukrcatholic.org/parishes, which `probe get` reads; the
  Ruthenian churches are the Eparchy of Passaic's, the Romanian the Eparchy of St. George in
  Canton's). Their street numbers can differ from GCatholic's.
- **Web search is rationed** (Camden): duckduckgo.com/html answers a bot challenge after a few
  searches; spend searches on finding a site or listing, and use The Monitor's REST search to
  date closures.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-30: Initialised (factory survey, Run trenton-map-1). Rosters: the diocese's parish
  finder as `directory` (98 pins: 97 parishes and the merged St. Mary of the Lake), GCatholic
  (136 entries, 8 of them Eastern Catholic). Planned 30 map batches in `batches.json` from the
  July 2024 cohort list (234 entries, none excluded). No records yet.
