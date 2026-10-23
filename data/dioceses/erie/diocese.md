---
name: Roman Catholic Diocese of Erie
state: PA
website: https://www.eriercd.org
status: exploring
gcatholic: erie0
city_aliases:
  Leeper: Crown
  Crossingville: Edinboro
  Grassflat: Frenchville
  Drifting: Morrisdale
  Sartwell: Eldred
  Pardoe: Mercer
  Frenchtown: Guys Mills
  Rasselas: Wilcox
  Hammett: Erie
  Lawrence Park: Erie
  Canadohta Lake: Union City
  Mageetown: Centerville
  Crates: Mayport
---

Thirteen counties of north-western Pennsylvania: Erie (Erie, North East, Corry, Girard), Crawford
(Meadville, Titusville, Cambridge Springs, Conneaut Lake), Mercer (Sharon, Hermitage,
Farrell, Grove City, Greenville, Mercer), Venango (Oil City, Franklin), Warren, Forest, Clarion,
Jefferson (Brookville, Punxsutawney, Brockway), Clearfield (Clearfield, DuBois, Houtzdale), Elk
(St. Marys, Ridgway, Johnsonburg), Cameron (Emporium), McKean (Bradford, Kane, Smethport) and
Potter (Coudersport). It borders Buffalo (New York) to the north, Scranton to the east,
Altoona-Johnstown to the south-east, Greensburg and Pittsburgh to the south, and Youngstown (Ohio)
to the west. Eastern Catholic churches of the Byzantine Catholic Metropolia of Pittsburgh (and
one Ukrainian) sit in the territory.

The diocese has **no families or clusters**. Its units are canonical parishes, each with its
parish church and, often, "secondary mission churches" (at least one weekend Mass) and
"secondary churches" (no weekend Mass; Mass at least on the patronal feast), the definitions the
2023–2024 deanery plans use. A 2023–2024 restructuring, deanery by deanery, merged many small
parishes into a neighbour (their churches became secondary churches) and **"partnered"** pairs and
triples of parishes under one pastor by decree (Erie city: five partnerships effective
2024-07-09; St. Marys; Lucinda/Crown/Fryburg; Meadville/Frenchtown). Partnered parishes and a
parish with its secondary churches are where shared bulletins are likely; parishes with one pastor
and one website (stjoseph-sacredheart.org, cpoecc.org, watch4deercatholic.church,
stspeterphilip.com, SharonCatholic.org, ihmercer.org, hcsjchurches.org) most of all.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (`rosters/directory.json`, 128 entries)**, scraped 2026-10-23 by
  `scratch/map-erie/tools/scrape_directory.py` from three eriercd.org sources keyed by one numeric
  record id (no Cloudflare; plain curl works):
  - the alphabetical list https://www.eriercd.org/parish-church.php (124 cards, each linking a
    detail page `<Kind><id>-<Name>.html` with physical and mailing address, clergy and Mass
    times);
  - the Find Parish/School locator's JSON (POST to https://www.eriercd.org/doegetjson.php with
    `lat`, `lng`, `radius`, `pa=true`; 119 records), which adds coordinates, a record type
    (`Parish` 78, `Mission` 28, `Church` 22 across the roster) and a `GroupID` naming each record's
    parent or partner parish record (kept as `locator_group_id`; `group` is that record's name);
  - the "List by city" page https://www.eriercd.org/directoryparishesandchurches.html, which puts
    secondary churches under their parish ("secondary mission church", "See St. Agnes Parish") and
    names partners ("partnered with St. Philip Parish, Linesville") (kept as `city_list_*`).
  One entry per record: a parish record is also its parish church. Gaps between the three: St.
  Patrick, Franklin and St. Luke, Youngsville are only in the locator; seven secondary churches
  (DuBois's four, Centerville, ...) are missing from the locator; **four city-list records have
  detail pages that 302 to index.php** (inactive records with no address): Holy Family, Erie; Our
  Lady of Fatima, Corry/Canadohta Lake; St. Brigid, Meadville; St. Joseph, Mount Jewett (listed
  under Smethport). All four have relegation decrees (below). **The pastor fields are unreliable**:
  the locator, the detail pages and the clergy list disagree (St. Bernard, Bradford: locator
  "Rev. Raymond C. Gramata", detail page "Rev. John Jacquel"; St. John the Baptist, Erie: locator
  "Rev. John B. Jacquel", detail page "Rev. James Piszker"). Use the clergy PDF for pastors. The
  `GroupID` is also wrong at least once (St. Anthony, Cambridge Springs and St. Bernadette,
  Saegertown sit under St. Stephen of Hungary, Erie; both belong to Our Lady of the Lake,
  Edinboro). Mass times are the directory's, not a bulletin's. Ten records have no website.
- **Printable directory** https://www.eriercd.org/images/directoryparishchurch.pdf, dated
  "Oct. 6, 2026" (59 pages, text layer): the same parishes and churches by town, with pastor,
  staff, Mass schedule and the secondary-church status of each church ("Secondary Mission",
  "Secondary Church", "See St. Titus Parish, Titusville"). Newer than the web pages and omits the
  four inactive records. Not imported as a roster (same entries); read it for a parish's status
  and schedule. It differs from the web city list on some statuses (St. Bernadette, Saegertown:
  "Secondary Mission" vs "secondary church without mission status").
- **Clergy list** https://www.eriercd.org/images/directoryclergy.pdf ("Updated 8/7/2026", 18
  pages): every priest and deacon with numbered assignments ("Pastor … 1) St. Philip, Linesville;
  2) St. Peter, Conneautville"). **The source for shared pastors.** Multi-parish pastors in it:
  Boyd (IHM Mercer, St. Columbkille Stoneboro); Curry OSB (St. Mary, Sacred Heart, St. Marys);
  S. Detisch (St. John Girard, Holy Cross Fairview); J. Detisch (pastor St. Tobias Brockway,
  administrator St. Timothy Curwensville); Glover (St. Stanislaus, Our Mother of Sorrows, Erie);
  Hamlett (Linesville, Conneautville); Hoffman (pastor St. Titus Titusville, pastor pro tempore St.
  Joseph Oil City); Holland (St. Charles New Bethlehem, St. Eusebius East Brady); Kleckner
  (Fryburg, Lucinda, Crown); Miller (Notre Dame Hermitage, St. Bartholomew Sharpsville); Piszker
  (St. John the Baptist, Holy Trinity, Erie); Power (St. Joseph, St. Anthony, Sharon); Richards (Our
  Lady of Mt. Carmel, St. Luke, Erie); Schmolt (Christ the King Houtzdale, St. Agnes Morrisdale;
  his vicar also serves St. Basil Coalport); Schreiber (St. Joseph/Bread of Life, Sacred Heart of
  Jesus, Erie); G. Whitman (Good Shepherd West Middlesex, Our Lady of Fatima Farrell). The web
  clergy page (https://www.eriercd.org/clergy.php) lists residences, not assignments.
- **GCatholic (`rosters/gcatholic.json`, key `erie0`, 150 entries)** with Plus Codes. Nine are
  Eastern Catholic (`rite`: eight Ruthenian, ids 17xxx; one Ukrainian, 17410 Annunciation, Ramey):
  `other-jurisdiction` once each page's jurisdiction is read. It **omits the cathedral** (St. Peter,
  230 W 10th St). It still lists at least 20 churches the decrees relegated or the directory
  dropped (Mount Calvary, St. Mary of the Immaculate Conception and Holy Family in Erie; Oil City's
  Assumption, Our Lady Help of Christians and St. Stephen; Sharon's Sacred Heart and St. Stanislaus
  Kostka–Holy Trinity; St. Adalbert, Farrell; St. Elizabeth, Corry; St. Joseph, DuBois and Mount
  Jewett; Lewis Run; Brandy Camp; DeLancey; Walston; Rasselas; Canadohta Lake; St. Brigid,
  Meadville). Its St. John the Evangelist, Girard is at 101 Olin Ave, the church relegated in 2022;
  the directory gives 1001 Main St E. Three GCatholic-only institutional entries: Mary, Seat of
  Wisdom Chapel (Gannon University), St. Mark Seminary, Mount St. Benedict Monastery. GCatholic's
  header says "94 parishes, 26 missions"; the directory has 78 parish records.
- **Clusters / families of parishes:** none. The structure is in the directory's city list and
  `GroupID`, the partnering decrees and the clergy PDF.
- **Mass times:** only the directory (web detail pages and the printable PDF). No separate
  Mass-times page; "Find Mass times" links to the locator.
- **Closed and merged parishes: the decrees page** https://www.eriercd.org/bishop/decrees.html
  (74 PDFs, plain HTTP, text layers; one image-only: "Oil City Parishes.pdf"). Merger decrees
  (mostly effective 2017-02-13 and 2023–2024), partnering decrees and **"relegating … to profane
  but not sordid use" decrees, which close a church building** with an effective date: St. Brigid,
  Meadville (2026-02-02); Holy Family, Erie (2025-12-29); St. Joseph, Mount Jewett (2025-03-10);
  Mount Calvary, Erie (2025); Our Lady of Fatima, Canadohta Lake (2024-08-14); St. Stephen, Oil
  City (2024); Our Mother of Perpetual Help, Lewis Run (2023-07-01); St. John the Evangelist,
  Girard (old church, 2022); St. Anthony, Walston (2021-05-03); St. Adalbert, Farrell
  (2020-09-20); Ss. John and Stephen, James City (2020-09-13); Holy Cross, Brandy Camp
  (2020-07-26); Our Lady Help of Christians, Oil City (2020-07-19); St. Adrian, DeLancey
  (2020-02-16; the survey first gave Anita's date); St. Joseph, Anita (2020-01-26); St. Elizabeth, Corry and St. Joseph, DuBois (2019-12-01); Assumption
  BVM, Oil City (2019-07-19); St. Stanislaus Kostka, Sharon (2019); Sacred Heart, Sharon
  (2018-03-25); Holy Cross, Rasselas (2017-09-07). St. Francis of Assisi, Bradford became a
  secondary church with no Sunday Mass by decree. Read the decree itself for each exclusion and cite the decree PDF URL, not decrees.html; a
  relegation decree states that the building closed, and gives the date. The decree list was read
  on 2026-10-23, with dates taken from each PDF's text (`scratch/map-erie/raw/decree_summary.txt`).
- **Pastoral plan:** https://www.eriercd.org/planning-deaneries.html: final plans for the
  Clearfield and Bradford deaneries (October 2023), McKean/Potter/Warren (news release
  2023-10-17), the DuBois Holy Spirit merger (2023-10-07) and Erie County (April 2024). They list
  each parish's churches and which lose weekend Mass (Grassflat, Hawk Run, Mount Jewett, Galeton,
  Austin). No final plan was published for the Oil City, Greenville (Mercer) or Elk/Jefferson
  areas beyond the decrees. Plans, not facts: check the bulletin.
- **Discover Mass:** almost every church here has a Discover Mass page
  (`scratch/map-erie/raw/dm/dm_pa_all.txt` lists the Pennsylvania slugs from the 2026-10-23
  sitemaps), including closed ones (Mount Calvary, St. Adalbert, St. Elizabeth Corry), campus pages
  (Gannon University, Mercyhurst College, Allegheny College) and one Romanian Byzantine church in
  Hermitage (`st-john-the-baptistromanian-byzantin-hermitage-pa`) that no roster has. A page is not
  a channel: three of four sampled (Lucinda, St. Julia, Coudersport) say "no bulletins available";
  the cathedral's is live (bulletin number 3511).

### Bulletin publishers here

Which publishers print this diocese's bulletins, how to read each, and which sites block the
sandbox and where their bulletins are instead. Agents researching parishes start here, so
keep it current rather than a log.

From `probe url` on the directory's 66 distinct websites (2026-10-23):

- **Diocese-hosted parish sites with `weeklybulletin.php`** are the commonest pattern (about 20:
  stlawrencealbion.org, cpoecc.org, stbernardcatholic.org, stthomastheapostle.church, ...; footer
  "Diocese of Erie 429 East Grandview Blvd."). The page lists one PDF per issue at
  `images/weeklybulletin/<md5>.pdf`: the file name carries no date, the link text and `title` do
  ("October 11, 2026"); `scratch/map-erie/tools/weeklybulletin_issues.sh <site>` lists them. Its PDFs can be image-only print-to-PDF scans (St. Leo Magnus, Ridgway): render page 1.
  The page can also list inserts and flyers (hash file names too): the first-listed file is the
  issue only when no insert sits above it (cpoecc.org), so re-run `fetch:check` on a later week.
  A `page-pdfs <site>/weeklybulletin.php` recipe passes `fetch:check`
  (St. Lawrence, Albion). Not every such page is the bulletin: hcsjchurches.org's holds only
  faith-formation fliers. Check how far behind the page runs (Albion's newest on 2026-10-23 was 11
  October). Some of these sites also embed a ParishesOnline org (hcsjchurches.org,
  stelizabethsmethport.org, ststanserie.org, stgregoryparish.info): compare the two before
  choosing a provider. An unlinked `weeklybulletin.php` can say "No Bulletin found." while the bulletin is on
  Discover Mass, sometimes under both the parish's and its mission's slug (St. Charles, New
  Bethlehem). A template site with no
  `weeklybulletin.php` may have a Bulletin menu entry that is a JavaScript `location.assign` to
  `parishesonline.com/find/<slug>`: read the nav HTML. `dioceseoferie.org/<Name>/` is the same host, with case-sensitive paths (`/HolyRosary/`
  works where `/holyrosary/` 404s) (Holy Rosary, Johnsonburg 403s
  probe url; St. Charles, New Bethlehem shows no bulletin links).
- **A diocese-hosted `weeklybulletin.php` page can repost a partner's ParishesOnline issue or
  a sister site's PDF** byte for byte (Our Mother of Sorrows = St. Stanislaus 14/1710, md5 over
  four weeks; St. Thomas Corry / St. Teresa): compare hashes before giving the page its own row.
  Conversely, when the container is an image-only ad edition, the site's text-layer PDF is the
  better `other` source; keep the container id in `publication` (St. Thomas, Corry).
- **ParishesOnline** orgs embedded on parish sites: st-john-the-baptist-church-16504 (on both
  stjohn-holyrosary-erie.org and holytrinityrc.org), st-stanislaus-our-mother-of-sorrows-churches,
  sacred-heart-church-16508, st-mary-of-grace-st-agatha-st-brigid-churches, st-mary-sacred-heart-
  churches, holy-cross-catholic-church, saint-james-roman-catholic-church, st-boniface-church-16509,
  st-gregory-church, st-elizabeth-of-hungary; containers 14/1173 (St. Callistus) and 14/1154 (St.
  Thomas, Corry); LPi ids on stjuliaerie.com, sainttitus.com, saintbartholomews.com. When a parish site is
  blocked even in headed Chrome, the search API (below) at the parish's coordinates with
  `distance=15` finds its org, and the org's `website` field matching the blocked domain is good
  identity evidence (St. Patrick, Franklin; Holy Redeemer, Warren). Org names
  record past groupings ("st-mary-of-grace-st-agatha-st-brigid"): read the masthead. A
  partnership can have two org records on one container (St. John/Holy Trinity, 14/0962):
  compare containers with `probe po`. `probe pdf` reads 4 pages by default; pass `--pages`
  (or `pdftotext -layout`) for an 8-page issue's Mass columns. A ligature read as U+FFFD
  ("Baptist") breaks `fetch:check --expected-identity`: use another masthead word; when the
  parish name is a graphic, use the town or the pastor's surname (Blessed Sacrament:
  `Pinczewski`). Up to
  three org records can alias one container (St. Joseph/Sacred Heart/St. Paul, 14/1876): record
  every org id on the row. GCatholic's parish websites here are often dead or squatted.
- **Discover Mass ids** on oilcitycatholic.com, ourladyofmercychurch.org, sttobias.com and the
  cathedral. See *Sources* for the many empty pages. A parish site's own PDF can be the same
  file as the Discover Mass download (Our Lady of Peace: same size, same bulletin number 3518):
  compare size and number, and use `discover_mass` with the slug. `recheck` finds quotes from
  the issue PDF cited under the church page URL only sometimes (St. Boniface, Kersey: not
  found); safest is a quote from the church page with the bulletin text in the note. It never finds the cover-class number or page
  markup: put those in a note. `recheck` reads only the first pages, and page-1
  mastheads often extract garbled: quote a clean full line from page 1 or 2 (link text is not
  page text). A Discover Mass PDF can carry stale hidden text from an earlier week: don't read a
  name found only there as a current Mass. `fetch:check` reports issue date `unknown` when the masthead
  date is split by the layout, and ParishesOnline issues posted early show as `future`;
  neither is a failure.
- **Other hosts seen:** Wix (a bulletins page lists `_files/ugd/*.pdf` in static HTML;
  John Patrick PDFs there are often image-only, so render page 1 and the Mass Intentions page; a blog post's file-upload-viewer attachment
  has no PDF link in the HTML or feed and is minted on click: `scratch/map-erie/tools/wixlinks.py`
  clicks it with Playwright `expect_download`, after which `/_files/ugd/<id>.pdf` is public: goodshepherdwm.org, sharoncatholic.org; Wix blog
  posts per issue: latinmasserie.org), Duda (bsparisherie.org, sttobias.com, `irp.cdn-website.com`),
  WeConnect (icclarion.org, `uploads.weconnect.com/mce/<id>/2026Bulletins/<yyyy-mmdd> for
  Website.pdf`; its Bulletins page can also link the ParishesOnline container PDF: when the md5
  matches, use `parishes_online`, as for Immaculate Conception, Clarion, 14/1155), WordPress (saintjude.church, st-boniface.org, stgeorgeerie.org, thesmchurch.com).
- **Failed `probe url`:** HTTP 403 for holyredeemerwarren.com, steulaliacoudersport.org,
  stpatrickfranklin.org, weareholyspirit.com, dioceseoferie.org/holyrosary (try headed
  `visit.py`); DEAD-DNS for catholic-meadville.com and steulaliacouderport.org (a directory typo);
  olp.org fails TLS on the bare host (try `www.`), and the reverse
  happens too (sainthippolytechurch.com: certificate mismatch on `www.`, bare host works); saintpatrickparisherie.org resets the
  connection.

Carried over from Altoona-Johnstown, Greensburg, Scranton and Buffalo (2026-10); correct it as
this diocese shows otherwise.

- **J.S. Paluch on Discover Mass.** Its `?s=` search is broken; grep the town in the sitemaps
  (`discovermass.com/wp-sitemap-posts-item-{1..11}.xml`; slugs here are mixed `saint-` and `st-`).
  Probe on the bare host (200 = exists, 404 = not). A joint bulletin may sit under only one of its
  churches' slugs; record every slug that carries the issue. "No bulletins available" pages are not
  live channels. Downloads are capped per IP per day (a 134-byte "Maximum number of files
  downloaded today" reply, `not_pdf` in `fetch:check`), and repeated page hits 503 then
  Wordfence-block even headed Chrome: read each page once. The current issue is
  `<a id='bulletin-current' href='…download.php?bulletin=…'>`, and the cover image class carries the
  bulletin number (`bulletin-cover X-|2026-10-25|<ts>|3511`): two slugs with one number are one
  bulletin. Cite the church page, not a tokenised download link.
- **LPi / ParishesOnline:** empty organizations are common and are not fold-ins; an old org can
  list a stopped container (check its latest issue). The search API
  (`https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=..&longitude=..&distance=3`)
  lists organizations near a point. Masthead often not on page 1; image-only pages: render with
  `render.py` or `pdftoppm` (installed here) and say so in the evidence note. When the first
  pages are images (St. James, 14/1107: pages 1-6), `fetch:check` identity reads `unknown`;
  cite the last page's text-layer footer (`<Parish> | 14-NNNN`) for `recheck`. `fetch:check`
  inspects at most 25 MB (Punxsutawney's 25 Oct issue was over); that limits the check, not
  the weekly fetch. A parish site can
  repost its container's PDF (compare file name and masthead). One issue can sit in two containers
  (separate ad editions): compare pages, record both. A widget's `publicationWidget?id=` shared by
  two sites means one bulletin.
- **eCatholic** sites sit behind Cloudflare: `https://www.<domain>/bulletins` usually opens in
  headed Chrome (parish-site-access); `files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf`
  downloads plainly. Here: weareholyspirit.com (Holy Spirit, DuBois) serves its bulletins at
  `/bulletin` (singular) as `files.ecatholic.com/<id>/documents/...` PDFs, which the eCatholic
  resolver (`/bulletins` only) misses: use `other` with `page-pdfs
  https://www.weareholyspirit.com/bulletin`. The printable directory states each church's
  secondary status and schedule, and Mass Intentions lines tag each Mass with its building:
  grep a run of issues for a building before deciding it has only a feast-day Mass.
- **Partners and one-pastor parishes:** a parish domain redirecting to its partner's site is a
  fold-in, not a squat; sister parishes with one pastor can each post their own bulletin with the
  same combined Mass rota (two rows while both channels are live); same-pastor parishes print each
  other's Mass boxes while keeping their own bulletin. Read the partner's masthead before calling a
  parish `no_bulletin`.
- **John Patrick Publishing** (`church-bulletin.org/<slug>`: any slug answers 200 with a generic
  page; a listing with no PDFs is not live), **Bon Venture** (`http://sponsors.bonventure.net/?page=<id>`,
  broken https chain), **WebParish**, **FATA Online** appeared next door.
- **Directory homepages and addresses go stale** (dead DNS, SSL failures, rectory or old-church
  addresses). Check a URL before storing it.
- **Web search in the sandbox:** `visit.py "https://duckduckgo.com/?q=..." --text` works; curl to
  DuckDuckGo or Bing returns nothing. A public Facebook post URL opens in headed Chrome without
  login (profile pages don't); cite it as a note.
- **Evidence for a `no_bulletin` church being open:** obituary snippets ("funeral Mass at
  <church>"), with the directory's Mass times. Flocknote pages are sign-up pages, not bulletins.
- **Former churches can keep occasional Mass** (feast-day or funeral Masses at a "secondary
  church"): grep a year of issues for the town before excluding. A relegation decree, by contrast,
  states the building no longer serves for worship.
- **Geocoding:** Nominatim answers (generic User-Agent `project-carlo-diocese-research`, ~1 request
  a second); Overpass resets connections. GCatholic Plus Codes are usually on the building; the
  directory's locator pins are the diocese's and can sit on a former church (St. John,
  Girard: the pin is on the relegated Olin Ave building).
- **Pin a recipe** for template sites after `fetch:check` (`page-pdfs <site>/weeklybulletin.php`),
  and check `source_url` is this week's issue, not a sidebar PDF.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (Ruthenian: Archeparchy of Pittsburgh; Ukrainian:
  Archeparchy of Philadelphia; the Romanian church in Hermitage) are excluded as
  `other-jurisdiction` once each one's jurisdiction is read, as in every other diocese here
  (orchestrator, 2026-10-23).
- **Shared pastors and partnering decrees don't make shared bulletins.** A partnership
  (Erie city, St. Marys, Lucinda/Crown/Fryburg, Meadville/Frenchtown, ...) is one row only
  when a current masthead covers each partner; a partner with its own live channel and
  distinct content is its own row. Record the partnership in `group` (orchestrator,
  2026-10-23).
- **Pastors come from the clergy PDF** ("Updated 8/7/2026"), not the directory's pastor
  fields, which disagree with each other (orchestrator, 2026-10-23).
- **A relegation decree closes a church** ("relegating … to profane but not sordid use"):
  exclude it as `closed`, citing the decree PDF, once the parish's current bulletin or Mass
  schedule has been checked and does not list it (say which issue). `last_mass` is the
  closing Mass when a bulletin or news item dates it, otherwise the decree's effective
  month, and the note says which. A merger decree alone closes nothing: a church of a merged
  parish stays a church row while a current schedule lists Mass there (orchestrator,
  2026-10-23).
- **Secondary churches.** A church with a recurring public Mass in the current bulletin or
  schedule (weekend, weekday, monthly or seasonal) is a church row under the row whose
  bulletin lists it. One whose only Masses are the patronal feast (and, under the 2016 merger
  decrees, the dedication anniversary), funerals and weddings, stated by a current source, is
  `no-public-mass` (St. Walburga, Titusville), as Scranton settled (St. Clare, St.
  Rocco). One no current source describes goes to `open/` with a revisit at its patronal
  feast (orchestrator, 2026-10-23).
- **A GCatholic-only church that no current source mentions and no decree closed** goes to
  `open/` with a dated revisit, not `excluded/` (as in Scranton).
- **Campus and institutional chapels** follow Altoona-Johnstown and Harrisburg: a campus
  Mass a parish bulletin lists every week is a church row under that parish; one a source
  calls public but no readable bulletin lists is `excluded/ no-bulletin`; one no source
  calls public goes to `open/`. Seminary and monastery chapels are `no-public-mass` unless a
  source invites the public to a scheduled Mass (orchestrator, 2026-10-23).
- **St. Hedwig, Erie (Latin Mass)** and any other apostolate follow the one-bulletin rule:
  its own regular bulletin makes it its own row, even though canonically it is a secondary
  church of St. Stanislaus. Blog posts or announcements alone are not a bulletin
  (orchestrator, 2026-10-23). **Exception while unreadable:** a bulletin the pipeline can't
  fetch (St. Hedwig's is a Wix blog attachment whose PDF URL is minted on click) doesn't get
  its own row. When another row's bulletin prints the church's Mass times every week, the
  church sits under that row, and the unreadable bulletin goes to `open/` with a retry
  trigger (St. Hedwig under St. Stanislaus, 2026-10-23).

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- **2026-10-23**, survey (diocese-surveyor): created the diocese, imported the GCatholic roster
  (150) and the directory roster (128), read the clergy PDF, decrees page and deanery plans, probed
  the 66 directory websites, and planned 26 scout batches in `batches.json` (all 278 roster entries
  assigned; `batches validate` passed). No records yet.
