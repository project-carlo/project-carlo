---
name: Roman Catholic Diocese of Camden
state: NJ
website: https://camdendiocese.org
status: exploring
gcatholic: camd0
city_aliases:
  Somers Poin: Somers Point
  Haddon Twp: Haddon Township
  Gloucester: Gloucester City
  Margate: Margate City
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
parish for most of them. Shared bulletins between *different* parishes are unlikely: no
source found names a pastor of two parishes. Expect closed or sold former churches (St. John
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
- **Clusters / families of parishes:** none. **Shared pastors:** none found. The 2025 and 2026
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

From `probe url` on the 108 distinct websites in the two rosters, the browser on three sites
that refused it, and a check of John Patrick redirects and two ParishesOnline containers
(2026-10-29). Each batch settles its own rows. Use the directory's website before GCatholic's,
and verify both.

- **John Patrick Publishing** prints a good share of the diocese, as in Philadelphia and
  Wilmington. Parish sites link `jppc.net/onlinebulletins/<id>template.pdf` or
  `church-bulletin.org/?id=<id>`, which redirect to a `church-bulletin.org/<slug>` listing of
  dated PDFs (seen: St. Peter, Merchantville 502; Our Lady of Peace, Williamstown 525; Our Lady of
  the Angels 564; Divine Mercy, Vineland 633; St. Gianna, Northfield 636; St. Thomas, Brigantine
  661; Holy Spirit, Mullica Hill 6006; St. Joseph, Sea Isle City 6028; St. Mary, Gloucester 6049).
  New Jersey ids run in the 500s–600s and 6000s. Plain curl `-L` on the template URL lands on
  the listing (checked for 502, 636, 6006 and 6028); never guess a slug, since a wrong one returns
  the generic home page with HTTP 200. Record `page-pdfs https://www.church-bulletin.org/<slug>`.
  Neighbours' lessons: the listing beats a parish's own copy when that copy lags; a listing with
  no editions means the parish publishes elsewhere; many issues are image-only (render page 1 with
  parish-site-access `render.py`); church-bulletin.org answers 406 to a bare "Mozilla/5.0" user
  agent, so use plain curl, `probe pdf` or `visit.py`.
- **LPi / ParishesOnline:** St. Katharine Drexel (04/0903, a text-layer masthead naming the
  church and Drexel Hall) and St. Joseph Pro-Cathedral (`po-org:st-joseph-pro-cathedral`,
  03/0810; issues to 2026-11-01). St. Mary of Mount Carmel, Hammonton has an old
  `stmarymtcarmelhammonton.parishesonline.com` subdomain (TLS fails) and an eCatholic site; check
  which is current. Issues are posted before their Sunday, so `fetch:check` freshness `future`
  is not a wrong pick. A WeConnect/Duda site can embed `publicationWidget?id=<lpi id>` without
  `probe url` reporting it: grep the page source for `id=0018`.
- **eCatholic:** St. Mary of Mount Carmel, Hammonton (33982), St. Clare of Assisi (23165), St.
  Rose of Lima (35649; `strosenj.com` redirects to `strosenj.org`). An eCatholic id is the
  publication only when `/bulletins` lists current `files.ecatholic.com/<id>/bulletins/` PDFs;
  some sites link John Patrick or another publisher instead.
- **Self-hosted and other platforms:** Wix (Our Lady of Perpetual Help, Galloway: a
  `_files/ugd/` PDF; Most Precious Blood `/bulletins`; Mary, Mother of Mercy and St. Brendan
  `/bulletin9ab2b387`, a Duda/Wix hash suffix), WordPress (Holy Family, Sewell `/weekly-bulletin/`;
  Infant Jesus; Our Lady of Sorrows `/bulletins/`; Our Lady of Hope `/current-bulletin/`;
  Mater Ecclesiae `/bulletin/`), and fixed-name PDFs (Mary, Queen of All Saints:
  `maryqueenofallsaints.org/currbulletin3.pdf`). Christ the Good Shepherd's bulletin page is
  `/2022-bulletins/`: check it is current. Read the file's first page before taking a site's
  first PDF as the bulletin (Our Lady of the Blessed Sacrament's is the USCCB calendar, St.
  Stephen's a registration form, Seton's a link to "thekidsbulletin.com").
- **Sites `probe url` couldn't read (2026-10-29):** 403 to `probe url`: holytrinitydownbeach.org
  (loads in the browser, bulletin at `/news/bulletin`), christourlight.net (browser:
  `/home/bulletins`), parishholycross.org (the browser run failed; retry), lakescatholic.com,
  stteresaofcalcuttanj.org, churchofscb.org (where saint-charles-borromeo.org redirects).
  JavaScript-rendered (NO-PARISH-WORDS): ladystarofthesea.org, sacredheartcamden.org,
  stanthonycamden.org, stjoenj.net. Use parish-site-access `visit.py`.
- **Dead, moved or hijacked domains (2026-10-29):** no DNS: blessedteresanj.org, ctratco.com,
  christtheshepherd.com, churchofstbridget.com, olssparish.com, saintmonicanac.org,
  sacredheartcamden.net, stclareofassisiparish.org, stjosephsomerspoint.com, stjosephwkr.org,
  stmarysgloucester.org, theparishofallsaints.org, theparishofsaintrita.org, walk2emmaus.com,
  parishofstmichaelthearchangel.org, and the Eastern sites stmichaelscherryhill.com,
  stnicholasmillville.com, ourladystaroftheeast.org. accatholic.org (St. Monica) closed the
  connection. **parishofstmichaelthearchangel.com** (the directory's, St. Michael, Clayton)
  redirects to a spam site (thestudiotrack.com), and **stelizabethannseton.com** (GCatholic's
  for Seton) lands on an ISP's unsafe-site warning: don't store either. Moved:
  stjosephtheworker.net → sjwparish.net; saint-charles-borromeo.org → churchofscb.org;
  notredamedelamer.org/notredame/ answers 404 (try the bare domain); acswebnetworks.com/incarnation
  answers 404 (incarnation-church.org is current).
- **J.S. Paluch / Discover Mass:** not seen in the survey. If a row uses it, Discover Mass caps
  downloads per IP per day (a 134-byte "Maximum number of files downloaded today" reply, which
  `fetch:check` reports as `not_pdf`): that is the cap, not the row.
- **Bon Venture:** not seen in the survey. If a site links `sponsors.bonventure.net/?page=<n>`,
  record `page-pdfs http://sponsors.bonventure.net/?page=<n>` over `http://` (the https host
  fails TLS verification in Python).

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- John Patrick bulletins on church-bulletin.org may be image-only (St. Joseph, Somers Point, id 617): probe pdf returns no text, so render page 1 with parish-site-access render.py; fetch:check still reports the PDF as ok.
- A parish's dead directory website can be found with a duckduckgo.com/html search via `probe get`; verify the address on the page before storing it (St. Joseph moved from .com to .org).
- St. Katharine Drexel's ParishesOnline PDF is about 37 MB, over fetch:check's 25 MB inspection limit, so document_type reports only the PDF signature; this is not an error.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches (St. Michael, Cherry Hill; St. Nicholas, Millville; Sts. Peter and Paul, Williamstown, Ukrainian; Our Lady Star of the East, Pleasantville, Maronite) are excluded as other-jurisdiction, as in every neighbouring diocese. (accepted by survey-review, 002-survey-review, 2026-10-29)
- A merger decree ends a parish, not a church. A former parish church of a merged parish keeps a church row under the merged parish when its current bulletin or Mass schedule lists Mass there; it is excluded closed only on a source that says so (relegation decree, sale, or the bulletin's last Mass), with last_mass. A church a current source calls 'currently not open' (St. Bernard, Dorothy) goes in open/ with a revisit, not closed. (accepted by survey-review, 002-survey-review, 2026-10-29)
- The Korean Catholic missions (St. Andrew Kim, Absecon; St. Yi Yun Il) are Latin and diocesan, not other-jurisdiction: a church row under the parish whose bulletin lists their Mass, a parish row of their own if they publish a readable bulletin, otherwise excluded no-bulletin (README Settled policy 4). (accepted by survey-review, 002-survey-review, 2026-10-29)
- A seasonal shore church keeps its church row with a dated revisit for its next season (Wilmington's rule); the summer guide's season notes are checked against an off-season bulletin before a church is called seasonal (St. Casimir, Woodbine; St. Agnes, Cape May Point; St. Thomas, Brigantine's 'June 29th to Labor Day' schedule). (accepted by survey-review, 002-survey-review, 2026-10-29)
- Monastery and shrine chapels (Monastery of the Perpetual Rosary, Camden; Our Lady of the Highway, Sea and Air, Pomona) follow Philadelphia's rule: a church row under a parish whose bulletin lists their public Mass, a parish row if they publish their own bulletin, otherwise excluded no-public-mass or no-bulletin. (accepted by survey-review, 002-survey-review, 2026-10-29)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-29: Initialised (factory survey, Run camden-map-1). Rosters: GCatholic (119
  entries), the diocese's Parish/School Locator as `directory` (65, schools dropped), the 2026
  shore summer Mass schedule as `summer-guide` (32). Planned 24 map batches in `batches.json`
  (216 entries, none excluded). No records yet.
