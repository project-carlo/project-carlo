---
name: Roman Catholic Archdiocese of Philadelphia
state: PA
website: https://archphila.org
status: promoted
gcatholic: phil0
city_aliases:
  Buckingham: Doylestown
promoted: 2026-11-07
---

The City and County of Philadelphia and the four suburban counties of southeastern
Pennsylvania: Bucks (Doylestown, Bristol, Levittown, Bensalem, Newtown, Quakertown), Chester
(West Chester, Coatesville, Phoenixville, Kennett Square, Downingtown), Delaware (Media,
Chester, Upper Darby, Havertown, Drexel Hill) and Montgomery (Norristown, Lansdale, Pottstown,
Abington, Conshohocken, King of Prussia). Neighbours: Allentown to the north (Berks, Lehigh and
Northampton counties) and Harrisburg to the west (Lancaster County), both mapped; Wilmington to
the south (Delaware and Cecil County, mapped); Trenton and Camden across the Delaware in New
Jersey (not mapped). The Ukrainian Catholic Archeparchy of Philadelphia has its see in the city
and churches across the territory.

The directory counts **218 open parishes** (2026-10-28), of which about 89 are in the city.
They sit in four episcopal regions and **14 deaneries** (two each in Delaware, Chester and Bucks,
three in Montgomery, five in the city), plus a separate list of parishes with a Hispanic
apostolate. There are **no families, clusters or pastorates**. Shared bulletins are likely in
three places: (1) **worship sites** of parishes merged in the 2012–2014 Pastoral Planning Area
(PPA) consolidations, which the directory names on the surviving parish's page ("Worship Site:
St. Louis Church, Yeadon"); many have since been relegated to profane use, and closures continue
(St. Hedwig, Chester on 2026-01-01; Immaculate Conception, Marcus Hook on 2026-07-19);
(2) **pairs under one pastor or one Parish Life Director**, which the directory's "Pastor:" lines
name explicitly (14 pairs and one trio, listed below); and (3) the few parishes with **missions or
chapels** (St. Malachy, Cochranville "Attended from" Parkesburg; Holy Saviour, Norristown's
chapel in Plymouth Township). Since 2025 the archdiocese has appointed lay and deacon **Parish
Life Directors** to parishes without a resident pastor ("Trust and Hope"); one of them leads two
parishes, which may already share a bulletin. `batches.json` keeps every such group in one batch.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (the `directory` roster):** https://archphila.org/parish/ ("Archdiocesan
  Parishes", linked from the Office for Parish Service and Support's parishes page, which the
  queue gave), an A-Z list on 9 pages of 346 entries: **218 open parishes and 128 closed ones**
  (marked `closedparish`, with their years, e.g. "St. Adalbert (Polish) (1904-2019)"). Each has a
  `/parish/<slug>/` page: deanery, the church's address as free text (often an intersection,
  "19th and Wallace Sts."), rectory address, website, Pastor (or Parochial Administrator or
  Parish Life Director), staff, Mass times, confessions, worship sites and chapels under *Other
  Parish Information*, and "Page last updated N months/years ago". Scraped 2026-10-28 by
  `scratch/philadelphia-map-1/tools/archphila_directory.py`; the parish post type is not in
  the site's REST API, and the site answers **HTTP 503 to bursts** (one page at a time with
  back-off took about an hour). One entry per **parish**, not per church: worship sites are only
  named in the text. No coordinates; addresses are not geocodable as given, so take building
  addresses and pins from GCatholic or OSM. City entries give no town in the address and suburban
  ones no ZIP in the A-Z list (taken from the rectory address). Quirks: Sacred Heart of Jesus,
  Tullytown is listed as open with no pastor, Mass times, website or deanery; "Mision Santa
  Maria, Madre De Dios", Avondale has no Mass times and only a "Donation Center" address; Holy
  Redeemer (Chinese), St. Malachy, Cochranville and St. Vincent de Paul have no deanery; nine
  parishes give no website (St. John Paul II, Divine Mercy, St. Ambrose, St. Veronica, the
  Oratory, St. Agnes-St. John Nepomucene, and the three just named). Pages are often a year or
  more old, so Mass times can be stale. Good for the parish list, pastors and staff, and leads
  to worship sites; not for addresses or current Mass.
- **Closed parishes (the directory's 128 closed entries; `raw/dir/all.json`):** each page says
  where the "Spiritual records are kept" (the parish it merged into) and, for 29, that the church
  is still a "Worship site of …" or holds "Mass at …". Those 29 are the **`worship-sites`
  roster**, each with its host parish in `group`. These pages are 2–10 years old and lag
  relegations: St. Hedwig's still gives "Mass at St. Hedwig Chapel, Sundays, 9:15 AM" though the
  church was relegated effective 2026-01-01. Four give their address as "Formerly located at
  …" (St. Alice; St. Augustine and Our Lady of Mount Carmel, Bridgeport; Holy Spirit, Sharon
  Hill): that is the page's address line, not a closure statement. St. Laurence's own page
  (updated about four months before 2026-10-28) still lists "Worship Site: St. Alice Church
  (Vietnamese only)" with a Sunday "Vietnamese: 10:00 AM [at St. Alice Church]". Read the host
  parish's own page and bulletin as well. They are leads to check, not current worship sites. The other 99 closed entries are
  not in a roster; GCatholic lists the churches that matter (below).
- **GCatholic:** `rosters/gcatholic.json` (key `phil0`), 293 entries, 263 with Plus Codes, **28
  Eastern Catholic** (`rite`: 15 Ukrainian incl. the Basilian monastery at Fox Chase Manor, 6
  Ruthenian, 3 Syro-Malabar, 2 Maronite, 1 Syro-Malankara, 1 Armenian). It lists churches,
  not parishes, so it carries most worship sites and many closed churches without saying so:
  of its 265 Latin entries, 212 pair with a directory parish and most of the other 53 are
  churches of merged parishes (St. Adalbert, St. George, Mother of Divine Grace, Nativity BVM and Our Lady
  Help of Christians for St. John Paul II alone), several relegated years ago (it notes some:
  "relegated to profane use 2019.07" for Holy Trinity, Our Lady of Ransom and St. Rose of Lima).
  It **omits** the cathedral, Old St. Mary's, St. Peter the Apostle (Neumann Shrine) and St. John
  the Evangelist (13th St.). Its "St. Michael the Archangel, E Mount Airy Ave. & Chew Ave." sits at
  Holy Cross, Mount Airy's corner; its "Visitation of the Child Jesus, E Lehigh Ave. & B St." is
  Visitation BVM's address; its Our Lady of Guadalupe is in Buckingham (the directory: Doylestown).
  It also lists St. Charles Borromeo Seminary and two Wynnewood chapels, the Visitation
  Monastery (City Ave.), Daylesford Abbey, a St. Carlo Acutis shrine at Malvern Retreat House and
  a "Sacre Coeur" perpetual adoration chapel in Havertown (dedicated 2026-06-12). Only 17 entries
  have a website.
- **Relegation decrees:** https://archphila.org/features/parish-planning-initiatives/ (read
  2026-10-28) links every relegation of a church "to profane but not sordid use" since 2015 as a
  signed PDF, with the PPA number: Immaculate Conception, Levittown, St. Joseph the Worker,
  Fallsington, Incarnation, Holy Saviour (Linwood), St. Gertrude (2015); Sts. Cosmas and Damian,
  St. Cecilia (Coatesville), Mater Dolorosa, St. John of the Cross, St. Madeleine Sophie and
  St. Therese, St. Augustine (Bridgeport), the old Assumption BVM, West Grove (2016); Our Lady Help
  of Christians, St. Leo, St. Stanislaus Kostka (Chester County), Our Lady of the Holy Souls
  (2018); Our Lady of Ransom, St. Rose of Lima (2019); Holy Trinity (decree 2019, withdrawn
  2020, relegated again from 2023-01-23); Immaculate Conception (Philadelphia) and St. Cyril of
  Alexandria (2020); Holy Spirit, Sharon Hill (2021); Sacred Heart, Phoenixville, the original
  St. Philip Neri, East Greenville and St. Peter Claver (2023); Immaculate Heart of Mary, Chester
  (2024). Later ones are announced on CatholicPhilly only: St. Hedwig, Chester (effective
  2026-01-01, posted 2025-11-18) and Immaculate Conception, Marcus Hook (effective 2026-07-19,
  posted 2026-06-09). The same page links the 2012–2014 merger announcements
  (`wp-content/uploads/2015/01/Announcements201{2,3,4}.pdf`) and the merger decrees of
  2016–2017. A decree dates a closure; read the parish's bulletin for the last Mass.
- **Clusters / families of parishes:** none. **Shared pastors** come from the directory's
  "Pastor:" lines (`tools/shared_pastors.py`): Holy Trinity and St. John the Evangelist,
  Morrisville (Deacon John Teson, Parish Life Director); St. Francis de Sales, Lenni and St.
  George, Glenolden (Mr. Mark Griswold, PLD); St. James, Elkins Park and Our Lady of Hope; St.
  Joseph and Presentation BVM, Cheltenham; St. Timothy and St. Bartholomew; the cathedral, St.
  Agnes-St. John Nepomucene and St. Andrew (Lithuanian); Our Lady of Charity, Brookhaven and St.
  Rose of Lima, Eddystone; St. Anthony of Padua and St. Joseph, Ambler; Christ the King and Our
  Lady of Calvary; St. Helena, Blue Bell and St. Titus; Annunciation BVM and St. Denis,
  Havertown; St. Joseph and Our Lady of the Rosary, Coatesville; St. Gabriel, Stowe and St. Thomas
  More; St. Barbara and St. Cyprian; St. Charles Borromeo, Drexel Hill and Sacred Heart, Clifton
  Heights. The Clerical Appointments 2026 page (https://archphila.org/clerical-appointments-2026/,
  yearly pages back to 2014 under category 3 of the REST API) confirms three of them in May 2026
  ("to Pastor, Annunciation B.V.M. Parish, Havertown, while continuing as Pastor, Saint Denis
  Parish"; "to Pastor, Presentation B.V.M. Parish and Pastor, Saint Joseph Parish, Cheltenham";
  "to Pastor, Saint Thomas More Parish, Pottstown, and Parochial Administrator, Saint Gabriel
  Parish, Stowe"). The appointments say who serves where, never what a bulletin covers. "In
  residence at" another parish is not a shared pastor (St. Nicholas of Tolentine's pastor lives at
  St. Paul).
- **Parish Life Directors:** CatholicPhilly profiles (2025-12 to 2026-10) and the directory:
  St. Mary of the Assumption, Phoenixville; St. Francis de Sales, Lenni (and St. George);
  Holy Martyrs, Oreland; Holy Trinity and St. John the Evangelist, Morrisville; St. Martha
  (Philadelphia); St. Mark, Bristol; St. Gabriel (Philadelphia, from 2026-09-14); Holy Cross,
  Springfield (from 2026-10-12).
- **Mass times:** only the directory pages (`mass_times`); there is no separate diocesan list
  (the site links masstimes.org). They name worship-site Masses ("St. Joan of Arc Worship Site:
  9 AM (English), 11:30 AM (Spanish)"; St. John Paul II's schedule by church) but can be years
  old.
- **Hispanic apostolate:** https://archphila.org/deanery/hispanic/ lists the parishes with one
  (`hispanic_apostolate` in the directory roster).
- **News:** CatholicPhilly (catholicphilly.com, the archdiocese's news site; WordPress, its REST
  API answers `probe get`: `/wp-json/wp/v2/posts?search=<words>&search_columns=post_title`)
  for relegations, mergers, Parish Life Directors and appointments.
- **Other jurisdictions in the territory:** the 28 Eastern Catholic GCatholic entries (above).
  A Syro-Malabar mission uses St. Albert the Great's church, Huntingdon Valley.

### Bulletin publishers here

- **John Patrick Publishing prints most of this diocese.** Sites link
  `jppc.net/onlinebulletins/<id>template.pdf` (an HTML page, not a PDF) or
  `church-bulletin.org/?id=<id>`, both leading to a `church-bulletin.org/<slug>` listing of
  `church-bulletin.org/bulletin/<slug>/<yyyy-mm-dd>.pdf` issues: record `other` with `page-pdfs
  https://www.church-bulletin.org/<slug>` (a parish with no site takes the listing as `website`).
  Find it in `raw/jppc-directory.json` (`tools/jppc_match.py`), then by name in
  `raw/jppc-pa.json`, as a listing's town can be the township or post town; never guess a slug (a
  wrong one returns the home page, HTTP 200). A listing is a lead: confirm its name, town and
  cover (a saint's name can be another parish's; an unmatched one can be Old Catholic, excluded
  `not-catholic`). About a quarter have no editions (a campus, a worship site, a merged church, or
  a parish that moved publisher): never the channel, though they can give a church's address.
  **The channel is whichever has the newest issue:** parish archives here often stop or lag a
  week or two, so open the newest entry on both. A site "Designed and Hosted by John Patrick
  Publishing" hosts no PDFs but can print elsewhere (Bon Venture). **Covers mislead:** parishes
  under one pastor or Parish Life Director share cover art, a combined Mass box or intentions and
  still publish separate issues (own masthead, page 2 and footer code, "007 St. Joseph -
  Cheltenham"); one issue headed with both parishes over one office and Mass box is one row. A
  neighbour's box on the cover, or a relegated church kept in a listing's name, is not a worship
  site: take sites from the Mass box. **Text layers vary:** check `pdftotext -l 2` (garbled
  counts as none) and quote words without the ligatures ti, tt, ff, fi. For an image-only issue
  read an older text-layer issue, or render pages 1-2 (`render.py`) and cite them in a `note`.
  `fetch:check` identity is always `unverified`, and a date inside an issue can raise an
  `issue_date` conflict: the file name's Sunday is the issue date. Take Mass times from the
  bulletin (cover or page-2 sidebar), not the directory; with no Mass box, from the parish site.
- **eCatholic:** many sites only link a listing, so an eCatholic id is not a publication; a
  `/bulletins` page with a current `files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf` is. When
  that file is the listing's issue, use an `ecatholic` row with the listing as a second `url:` id;
  when bytes differ, compare the rendered cover and Mass box (the parish's own layout leaves the
  eCatholic id out). Files under `/documents/`, or an archive that stops while the listing goes on
  (St. Thomas Aquinas, Croydon, November 2026), call for the listing's `other` row. Archives post
  next Sunday early (freshness `future`), and a home page's "Current Bulletin" can lag
  `/bulletins`. Behind Cloudflare (403 to `probe url`), `visit.py` on `/bulletins` lists PDFs that
  plain downloads fetch; a link seen only in page source goes in a `note`.
- **Self-hosted sites:** read a file's first page before calling a site a channel: Wix archives
  here often stop or hold flyers, while a nav page's jppc template link names the real channel.
  Oldest-first pages make `page-pdfs` pick a stale file, and a site's copy can be another layout
  or only the inside pages: keep the listing and record a byte-identical copy (md5) in
  `publication_reviews`. WordPress `wp-content/uploads/<yyyy>/<mm>/` PDFs with no listing read
  with `page-pdfs`; pin a WordPress.com mirror with `filename=bulletin_*.pdf`; one post per issue
  gives `page-pdfs` nothing. Undated or numbered file names leave freshness `unknown`: read the
  pick's masthead, and date a copy by its header (some are named for the upload day). A year filter (`filename=*26*`) must change each January. Don't print a Wix
  page's links whole (`grep -v parastorage`). Bulletins no collector reads are `unsupported` with
  a `fetch_gap` (README): Squarespace `/file` links, which can answer 403 to any plain client
  (`squarespace-file-403`; use a listing if there is one), Drive `/preview` iframes on a Google
  Site (`drive-preview-embed`), WordPress text posts (`html-only-bulletin`) and Mailchimp
  eBulletins (`mailchimp-html-newsletter`).
- **Bon Venture Services** (a minority printer): `other` with `page-pdfs
  http://sponsors.bonventure.net/?page=<id>`, over `http://` (no intermediate certificate); it
  lists next Sunday early. Its link can be only a menu item or button pointing offsite, which
  `probe url` misses: read the whole nav link list for bonventure.net, jppc.net or
  church-bulletin.org before calling a bulletin missing.
- **ParishesOnline / LPi** (a minority, mostly Delaware County): an empty organization is neither
  a publication id nor a fold-in, but the search API
  (`https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=<lat>&longitude=<lon>&distance=3`)
  near each church of a merged parish gives its former parishes' addresses. `probe url` any
  website an organization gives (another parish's, old or squatted). WeConnect/Duda sites embed a
  `publicationWidget` whose `id=` is the LPi id; a PDF's footer code ("Name, Town, PA 04-0708")
  names the container. A neighbour's sidebar box is not a joint masthead.
- **Discover Mass** is not a publisher here, whatever an issue's footer says.
- **Reaching sites:** retry in `visit.py` before concluding anything; it reads Solutio-framed and
  bot-blocked sites. HTTP 500s from a host several parishes share (69.16.220.73) pass in a day.
  A certificate failure can be an old host alias (record where `visit.py` lands); an expired
  certificate or a network-filter page (`cujo.io`) makes the listing the `website`, with
  `access-blocked` research. The directory's website can be a school's, a Linktree or an
  abandoned Wix site: take the site from the bulletin's footer. A merged parish can keep its pages on a school's
  site. With no site, `probe get` on
  `html.duckduckgo.com/html/?q=<parish> <town>`, and the Facebook page in `visit.py`; a search
  hit is a lead until page 1 shows the parish's address.
- **archphila.org and CatholicPhilly (closures):** archphila.org answers 503 to bursts. Decree
  PDFs before 2020 are scans: render every page (one PDF can hold two decrees); page 2 gives the
  effective date. The decree list starts in 2015 and misses some later closures, so also search
  CatholicPhilly with both its REST search (`wp-json/wp/v2/posts?search=<name>`) and its HTML
  search (`/?s=<church>+church`). OSM still tags closed churches.
- **Coordinates and addresses:** Nominatim through `probe get` (`format=jsonv2`, `q=<church>
  <town>`) finds named churches, sometimes under the township or 100 m off: check against
  GCatholic's Plus Code, the fallback. The directory's or masthead's street can be the office, and
  GCatholic's the campus school or another ZIP: follow the parish's own and leave
  `address_verified` false. GCatholic's "Mission of:" names a chapel's owner; its "first
  recorded" can be an older church; its id is not a ZIP.
- **GCatholic's campus and jurisdiction lines:** seminary and abbey entries can describe a campus
  the community left; Ordinariate entries show that Jurisdiction (rule below), and "Using the
  building: X" marks a congregation in a parish's church. `coverage --link` attaches Eastern
  entries at a Latin church's address to the Latin record, in any batch: run `git status` after
  it and keep the id only on the Eastern exclusion.
- **Eastern Catholic lists** (`probe get` reads them): https://ukrcatholic.org/parishes,
  https://www.eparchyofpassaic.com/parishes (Ruthenian), the Maronite directory linked from
  stmaron.org/directory, https://stthomasdiocese.org/parishes/ (Syro-Malabar); GCatholic's
  Jurisdiction line for the rest. Match by address and phone.

## New lessons

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (Ukrainian Archeparchy of Philadelphia, Ruthenian, Syro-Malabar, Syro-Malankara, Maronite, Armenian) are excluded as `other-jurisdiction`, as in every neighbouring diocese. A Latin parish church an Eastern community also uses keeps its own row (St. Albert the Great, Huntingdon Valley, with the Syro-Malabar mission). (accepted by survey-review, 003-survey-review, 2026-10-28)
- **Shared pastors and Parish Life Directors don't make shared bulletins.** A pair or trio named under one pastor or PLD on the directory (14 pairs and the cathedral trio) is one row only when one current bulletin covers each member; compare mastheads and Mass schedules, not contact lines or staff. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A worship site of a merged parish** keeps a church row under the parish whose current bulletin or Mass schedule lists Mass there; for a parish with no readable bulletin, its own site's Mass schedule counts. Only a Mass box line naming the place is evidence of Mass there. These are not: the directory's "Worship site of …" line on either parish's page (a lead, and stale once X's own page names no worship site and says only "Merged with …": add no church row from it); a closed parish page's "Formerly located at …" (its address line) or "Spiritual records are kept at X" (like an aggregator's "Parish-Closed" title, the parish's end, not the church's); a cover subtitle naming the site over the parish's own address; a cover drawing, "our two churches" or a history page saying Mass is celebrated there; a patronal subtitle keeping a merged parish's title; a single event Mass. When the Mass box and the parish site put every Mass at the main church and no closure source exists, leave the site in `open/`; when X's own site, masthead and Mass page name no other site, look for a decree that ended Sunday Mass there. Exclude `closed` only on a relegation decree, a news story or a bulletin that says so, with `last_mass` from the bulletin, else from the decree's or story's stated last Mass or end of regular worship, else the decree's effective date or, with no decree, the story's closing date (St. Leo, Tacony: regular worship ended 2018-01-01, decree effective 2019-01-07). (accepted by survey-review, 003-survey-review, 2026-10-28; map batches `lenni-glenolden` and `conshohocken-kop`, 2026-10-28; `bensalem-croydon`, `queen-village-bella-vista`, `bustleton-somerton`, `frankford-olney`, `holmesburg-tacony` and `cathedral`, 2026-10-29; the `last_mass` order raised by `holmesburg-tacony` and set by reconcile, 2026-10-29)
- **Personal Ordinariate churches** (the Chair of St. Peter) are excluded `other-jurisdiction`, as in Rochester and Scranton, even in a former archdiocesan parish church: St. John the Baptist holds Mass in Our Lady of Mount Carmel, Bridgeport, which is not a Sacred Heart worship site. (map batch `conshohocken-kop`, 2026-10-28)
- **Seminary, monastery, abbey, retreat-house and adoration chapels** get a church row under a parish when that parish's bulletin lists their public Mass; a parish row of their own if the house publishes a readable bulletin; otherwise they are excluded `no-public-mass` (private or community-only Mass) or `no-bulletin` (public Mass, but no bulletin lists it), following README Settled policy 4. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A campus Mass the parish bulletin lists every week gets a church row**, as in Harrisburg; a campus ministry that publishes only by email or semester newsletter is excluded `no-bulletin`. A campus Mass in two neighbouring parishes' bulletins is one church row, under the parish whose Mass box gives the fullest schedule, citing the other bulletin (Temple Newman Center under St. Malachy). (accepted by survey-review, 003-survey-review, 2026-10-28; map batch `north-central`, 2026-10-29)
- **A shrine in a parish church is that church's row** (the Cathedral and Shrine of St. Katharine Drexel). A shrine in a former parish church is decided like a worship site: a church row under the parish whose bulletin lists its Masses, a parish row of its own when it publishes its own bulletin, or excluded `no-bulletin` when it has public Mass and no bulletin lists it. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **The directory's `group` is the deanery** ('Chester County West'), not a family or cluster: leave `group` empty on parish records, since `audit` flags every row sharing a value as a possible shared bulletin, and record each parish's `publication_reviews` from the mastheads. (map batch `west-chester`, 2026-10-28)
- **Church rows follow the Mass schedule box, not the directory.** Read every location it lists: a hall or center with a weekly Sunday Mass gets a church row (Schneider Parish Center, Parkesburg), and so does a chapel with its own address and Mass. Not church rows: a directory "parish" that is a parish's own center or mission, where the bulletin puts classes and meetings but no Mass (excluded `no-public-mass` under that parish); an "Adoration Chapel" or "Chapel" in the box or under the cover's "Daily Adoration" with no Mass line (check the page-2 calendar first); a chapel named in a weekday Mass line with no address of its own, a room of the campus whose Masses go on the church's row; "Lower Church" and "Upper Church", floors of one building; a second building's address in the masthead or a footer banner, unless a Mass box or calendar lists Mass there (for an image-only issue, search older text-layer issues). (map batches `coatesville-parkesburg`, `southern-chester`, `media-wallingford` and `blue-bell-norristown`, 2026-10-28; `manayunk-roxborough`, `south-philly-east`, `morrisville-fairless-hills` and `newtown-yardley`, 2026-10-29)
- **A Mass one parish staffs at another parish's church is that church's row only.** It appears in both bulletins, but it is not a worship site of the staffing parish (St. Rocco's Sunday 2:00 PM Spanish Mass at Sacred Heart, Oxford is on Sacred Heart's church row). (map batch `southern-chester`, 2026-10-28)
- **A directory "parish" page with only a rectory address and phone**, no pastor, Mass times or website, and a "where all spiritual records are kept" link to another parish, is a former parish or worship-site entry, not a bulletin publisher: make no parish row, and decide its church as a worship site of the records parish (Sacred Heart of Jesus, Tullytown under St. Mark, Bristol). Its rectory phone can be a neighbouring church's. (map batch `bristol-levittown`, 2026-10-29)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: Hand refresh against main (PR #174, Run philadelphia-map-1, ~87 commits behind):
  main merged in, then reconcile and integrate redone by hand under main's rules. Coverage
  unchanged: `directory` 218/218 accounted for, 205/217 modelled (94%); `gcatholic` 293/293,
  212/233 (91%); `worship-sites` 29/29, 12/19 (63%); 5 churches in no roster. `coverage --link`
  added nothing (the stray Eastern ids stay off the Latin records). Four rows that publish a
  bulletin no collector reads are now `unsupported` with a `fetch_gap`: St. Catherine of
  Siena, Horsham (`squarespace-file-403`), Our Lady of Hope (`drive-preview-embed`), Holy
  Redeemer (`html-only-bulletin`) and St. Vincent de Paul (`mailchimp-html-newsletter`); 7
  rows stay `no_bulletin`. St. Thomas Aquinas, Croydon now reads its John Patrick listing
  (eCatholic stopped at 25 October). Our Lady of Hope's church is named Church of the Holy
  Child, as its masthead has it. Open records: the seminary chapel at Ambler excluded
  `no-public-mass` (its visitor policy), St. Ignatius Nursing Home's chapel added; 9 open.
  Records: 214 parish rows, 242 churches, 77 exclusions. No merges or moves; audit found no
  shared publisher account, page, document or id (its unresolved pairs are deanery groups
  only). Fetch check: 203 rows, all PDFs, all this week's or tomorrow's issue.

- 2026-10-29: Reconcile (job 081, Run philadelphia-map-1) after 59 map batches (usually 2–5
  parishes each, two Eastern Catholic). Coverage: `directory` 218/218 accounted for, 205/217
  modelled (94%); `gcatholic` 293/293, 212/233 (91%); `worship-sites` 29/29, 12/19 (63%); 5
  churches in no roster, each explained. Records: 214 parish rows (11 `no_bulletin`), 242
  churches, 76 exclusions, 9 open. No merges or moves: every audit candidate was the deanery
  `group` (cleared on 15 parish records) or a shared Bon Venture host (separate reviews added);
  separate reviews also for Good Counsel/Villanova and Ottsville/Riegelsville. Dropped six
  Eastern GCatholic ids from Latin records. Closed from CatholicPhilly stories: St. Margaret
  Mary Alacoque, Essington and Our Lady of the Blessed Sacrament (from `open/`), Our Mother of
  Sorrows and St. Callistus (new). New: Czestochowa shrine (`no-bulletin`), Holy Myrrhbearers
  (other-jurisdiction). Fetch check: 203 rows, all PDFs; 202 current (this week's issue or next
  week's posted early), St. Rocco a week behind.
- 2026-10-28: Survey (job 001, Run philadelphia-map-1). Rosters: `directory` 218 open parishes,
  `gcatholic` 293 (28 Eastern Catholic), `worship-sites` 29. `batches.json`: 59 batches (57 of
  2–5 parishes, two Eastern Catholic), 540 roster entries, none excluded; `first_batch`
  west-chester. No records yet.
