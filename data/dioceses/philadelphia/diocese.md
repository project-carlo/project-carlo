---
name: Roman Catholic Archdiocese of Philadelphia
state: PA
website: https://archphila.org
status: promoted
gcatholic: phil0
city_aliases:
  Buckingham: Doylestown
audit_ignore_groups:
- directory
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

## Seeding precedents

Seed questions `seed-review` settled that no rule covered: the situation, the choice and the parishes. Later reviews in this diocese follow them; only the owner turns one into a rule.

- Include the Spanish Advent retreat's closing Holy Hour and confessions on Sunday Nov 29, 4:00-5:00 PM? → Leave out. With the lean. The Holy Hour and confessions are the close of a registered retreat: 0a0b26fc p9 says 'El retiro incluirá dos charlas, un almuerzo y concluirá con una hora santa y la confesión. Para inscribirse, llame al: 610-235-7294', and e4506448 p9 prints the agenda line 'IGLESIA 4:00-5:00 Hora Santa y confesiones. Para inscribirse...'. Neither issue invites people who haven't registered. On a public site a wrong time is worse than a missing one (POLICY). What made it hard: the session is in the church and nothing says non-registrants are turned away. (st-agnes-west-chester s24; 033-seed-review, 2026-11-26)
- Add a First Saturday 8:45 AM Mass? → First Saturdays 8:45 AM. With the lean. 73b513ed p5 (Dec 5 calendar cell) prints '8:45 First Sat. Mass'; Saturdays have no regular 8:45 Mass, and POLICY Weekly rule 2 makes a named First Saturday slot weekly even when this month's date is given. Hard because it is printed once and the schedule box (p10) and website don't mention it; no other read issue covers a first Saturday. (st-basil-the-great-kimberton s17; 054-seed-review, 2026-11-26)
- Add First Saturday Confession at 9:15 AM? → First Saturdays 9:15 AM. With the lean, same case as s17: 73b513ed p5 Dec 5 cell '9:15 First Sat. Confession', named by its week (POLICY Weekly rule 2). Printed once; no end time. (st-basil-the-great-kimberton s18; 054-seed-review, 2026-11-26)
- Add Tuesday Adoration 9:15 AM-8:00 PM from the website? → Tuesdays 9:15 AM-8:00 PM. With the lean. The homepage (updated after Nov 24, lists Thanksgiving 2026) gives 'Adoration of the Blessed Sacrament Tuesdays: 9.15 am–8.00 pm Wednesdays: 9.15am–6.15pm', and its perpetual-adoration notice says adoration is now 'only a few days a week'. The bulletin box (73b513ed p10) lists only Wednesday, which R6 treats as a missing mention, not a conflict; its other times match the site exactly. (st-basil-the-great-kimberton s19; 054-seed-review, 2026-11-26)
- Include the Tue Nov 17 5:30 PM CGS First Communion Intention Mass? → Include Nov 17 5:30 PM. With the lean. a291b984 p3 'TUESDAY, November 17 ... 530pm - CGS First Communion Intention Mass': a Mass at the parish's one church that the bulletin doesn't limit to the group (POLICY: open unless limited). Hard because it sits among program meetings and, unlike its neighbours, names no room; the date has passed, so it has little effect on the site. (st-joseph-spring-city s21; 054-seed-review, 2026-11-26)
- Add the Dec 15 Liturgy of Penance and Reconciliation, 6:00 PM, as a confession? → Confession Dec 15 6:00 PM. With the lean. 51bbd1fc p6 Advent & Christmas Schedule: 'Tuesday, December 15 · Liturgy of Penance and Reconciliation – 6:00 PM · Confessions'. A penance service is itself a celebration of the sacrament of Penance, which POLICY counts, and it starts at the printed 6:00 PM; no end recorded. Hard because POLICY's final checks say a larger event doesn't time its components. (st-aloysius-pottstown s17; 054-seed-review, 2026-11-26)
- Add the Regnum Christi Christ the King Mass, Sun Nov 22, 4 p.m.? → Leave out. With the lean. 0fbaaa3e p3 prints '4 p.m. RC Christ the King Mass' only in the parish calendar beside Regnum Christi meetings; the same issue's Mass Intentions for Sunday Nov 22 list only 8 and 11 a.m. It reads as the movement's own Mass. The st-agnes-west-chester s24 precedent the drafter cites is a registered retreat, not this case. Hard because nothing limits it to members; the date has passed. (st-thomas-more-south-coventry s17; 054-seed-review, 2026-11-26)
- Add the First Friday 8 p.m.-2 a.m. Night of Reparation as Adoration? → Leave out. With the lean. 0fbaaa3e p1 lists 'First Fridays: 8 p.m. to 2 a.m. Evening of Reparation' under Prayer and Devotions, and p5 describes a 'Two Hearts Night of Reparation Vigil'. Neither page calls it Adoration, Exposition or a Holy Hour (POLICY), and it runs past midnight. Hard because p5 shows a monstrance; decided like st-isaac-jogues-wayne's 7:30 PM Night of Reparation (s22). (st-thomas-more-south-coventry s18; 054-seed-review, 2026-11-26)
- Weekend Adoration in the chapel: which times? → Bulletin, POLICY timing: Sat from 8:30 AM, Sun from 9:00 AM, no end. With the lean. 4d8e36d3 p1: 'Open Sat. & Sun. 7:30am exposition after the 8:00 am Mass', with no end time. POLICY times it from the Mass (Sat 8:30, Sun 9:00) with no end. The website's 'Every day 8:30 AM - 8 PM' is partly stale (its weekday exposition 'begins after the 8AM Mass', a weekday Mass that no longer exists), so its 8 PM end isn't trusted for weekends. (st-isaac-jogues-wayne s17; 054-seed-review, 2026-11-26)
- Add a first-Friday 9:00 PM Mass (Night of Reparation)? → First Fridays 9:00 PM. With the lean. 4d8e36d3 p1 lists 'Night of Reparation – 1st Friday 7:30 pm' under MASS SCHEDULE; stisaac.org gives '1st Friday Night of Reparation: Begins at 7:30 PM, Mass at 9:00 PM', which fits it (R6: a time the bulletin lacks). Its weekend, weekday and Thanksgiving times match the bulletin. Hard because the site is partly stale (Holy Day 7:30 vs the bulletin's 7:00) and its Night of Reparation page is gone. (st-isaac-jogues-wayne s21; 054-seed-review, 2026-11-26)
- Add the Christmas and New Year Masses from the standing schedule box? → Leave out. With the lean. 4d8e36d3 p1 prints 'Christmas Eve: 5 pm & 8 pm / Christmas Day: 8am, 10:30am, & 12pm / New Years Eve ...' in the year-round box with no year or dated notice, like the generic Holy Day line left out elsewhere (POLICY, Dates). December issues will print this year's schedule for update mode. Hard because Christmas falls on fixed dates and the times may well be right. (st-isaac-jogues-wayne s27; 054-seed-review, 2026-11-26)
- Add a Sunday Dec 6, 5:00 PM Teen Mass (Grotto Lighting)? → Leave out. With the lean. e1008ce5 p4: 'Grotto Lighting & Blessing Dec. 6 after the 5:00 pm Mass ... Following the Teen Mass'. Dec 6 is a Sunday, and neither p1 box nor the intentions have a Sunday 5 PM Mass, while the same page ties 'the 5:00PM Mass' to Saturday Nov 28. It may be the Saturday Dec 5 vigil, which is already weekly. Hard because a one-off Sunday Teen Mass is possible. (st-katharine-of-siena-wayne s17; 054-seed-review, 2026-11-26)
- Add the monthly Men's Gathering Mass (2nd Thursday, Sept-June, 6:30 AM, Rosemont Chapel)? → Leave out. With the lean. d3258fe2 p5: 'CALLING ALL MEN! Join Us for Our Monthly Men's Gathering Mass and Fellowship', a men's-group Mass that POLICY treats as limited to a group. It is not in the 52fe4640 p1 schedule box. Hard because it says 'invite a friend' and turns no one away. (st-thomas-of-villanova-villanova s19; 054-seed-review, 2026-11-26)
- Is St. Mary's Chapel at SS. Philip and James Church, so its weekday Adoration 9 AM-7 PM goes there? → Mon-Fri 9:00 AM-7:00 PM at the church, in St. Mary's Chapel. With the lean. 6e15f393 p1 prints 'Adoration in St. Mary's Chapel Monday through Friday: 9:00 AM - 7:00 PM' inside the church's own schedule box. sspj.net/mass-times lists the chapel's exposed Adoration with that church's Mass and Confession times and directions only to 723 E. Lincoln Hwy. No other St. Mary's chapel is listed in Exton (seed church). Hard because no page names the chapel's address. (ss-philip-and-james-exton s15; 054-seed-review, 2026-11-26)
- Add the Immaculate Conception Mass Tue Dec 8, 8:30 AM at OLC? → Dec 8 8:30 AM. With the lean. 8de65ed1 p1 standing line 'Holy Days-8:30 am (OLC) Vigil Mass-7:00 pm (OLC)'; p4 shows it applies this year: the 40 Hours 'conclude at 7:00 pm with the Vigil Mass for the Solemnity of the Immaculate Conception' on Monday Dec 7, which pins the solemnity to Tue Dec 8 (no regular Tuesday Mass). Unlike st-isaac-jogues-wayne's undated Christmas box, a current dated notice ties the holy day to this year. Hard because 'December 8' itself is never printed. (our-lady-of-consolation-parkesburg s12; 054-seed-review, 2026-11-26)
- Add the 40 Hours of Adoration, Sat Dec 5 after the 5:00 PM Mass through Mon Dec 7 at 7:00 PM? → Leave out until details are printed. With the lean. 8de65ed1 p4 announces it but says 'More details and information will be forthcoming', with no hours or place. The include option would claim overnight exposition (00:00-23:59) that nothing prints. Update mode will read the issues with the details. (our-lady-of-consolation-parkesburg s13; 054-seed-review, 2026-11-26)
- Is there a Friday 7:00 PM Spanish Mass (and the 6:30 PM confession before it)? → Leave out. With the lean. The 434f4fb7 p1 box says 'Monday through Friday 8:30am - 7:00pm (Spanish)', but both weeks' intentions (434f4fb7 p2 Fri Nov 20, c10f6a48 p2 Fri Nov 13) list only the 8:30 AM Mass on Friday, while Mon-Thu have a 7 PM. The website gives 'Mon Thu 7:00 PM Spanish'. Two sources against the box's compressed line. (st-joseph-coatesville s10; 054-seed-review, 2026-11-26)
- Add a 7:00 AM Spanish Saturday Mass? → First Saturdays 7 AM. With the lean. c10f6a48 p2 lists 'Sat., Nov. 7th ... Weekday/First Saturday 7:00 a.m. Mass in Spanish'; 434f4fb7 p2 has no 7 AM on Nov 14 or 21. The website's 'Saturday: 7:00 AM Spanish' gives no week. Only a first Saturday shows it. Hard because neither schedule box prints it. (st-joseph-coatesville s19; 054-seed-review, 2026-11-26)
- Add confession 30 minutes before the Sunday 8, 10 and 12 Masses? → Include. With the lean. c10f6a48 p5 'Confesiones: Todos los días 30 minutos antes de las misas', and the website's grid gives Sunday 7:30, 9:30 and 11:30 AM confessions. The English 'before daily Mass' (434f4fb7 p1) doesn't exclude Sundays. Timed per POLICY to end at the Mass; the website ends them at :50. (st-joseph-coatesville s32; 054-seed-review, 2026-11-26)
- Add confession before the Saturday 4:15 and 7:00 PM and Sunday 6:30 AM Masses? → Leave out. With the lean. Only the general Spanish line (c10f6a48 p5) covers these Masses; the website's confession grid, which lists the Sunday 7:30/9:30/11:30 times, gives none before them. Decided against s32 on that grid. (st-joseph-coatesville s35; 054-seed-review, 2026-11-26)
- Add the website's Christmas Mass times (Dec 24 6 PM English, 8 PM Spanish; Dec 25 10 AM English, 12 PM Spanish)? → Leave out. With the lean. The website's holy-day block may be last year's: it gives Dec 8 as 8:30 AM and 7:00 PM Spanish, while 434f4fb7 p7 prints this year's 8:30 AM, 6:00 PM and a 7:30 PM Spanish. No read bulletin prints Christmas times; update mode will read them. (st-joseph-coatesville s45; 054-seed-review, 2026-11-26)
- Keep the website's 6:30 AM Mass on December 8, given the parish dropped 6:30 AM Masses on July 1? → Leave out. With the lean. 28bc475c p4: 'New Mass Schedule - Effective July 1, 2026 ... We will no longer offer 6:30 am Masses.' The website's 'HOLY DAYS IN 2026' list also gives 6:30 am for Ascension (May, before the change), so its Dec 8 6:30 line was likely written before July 1; its 10 am and 7 pm stay (s20, s21). Hard because the list is labelled 2026 and the parish may have kept an early holy-day Mass; December bulletins will settle it. (assumption-bvm-west-grove s22; 077-seed-review, 2026-11-27)
- Saturday confession: the bulletins say 3:00-4:00 PM; the website says 3:15-4:15 PM and, in its footer, 3:15-4:00 PM. Which? → Saturdays 3:00-4:00 PM. With the lean. Both bulletins print 'Sacrament of Reconciliation Saturday afternoon 3:00 – 4pm' (95e9f617 p2, 97d70026 p2); abvmh.org contradicts itself (3:15-4:15 in the body, 3:15-4:00 in the footer) and names a Wednesday 8:30 AM Mass that no longer exists, so it is the less-maintained source. (annunciation-bvm-havertown s9; 077-seed-review, 2026-11-27)
- Count the Tuesday 7-8 PM Flame of Love Cenacle 'Holy Hour' (rosary and prayers, school building) as Adoration? → Leave out. With the lean. 95e9f617 p4: a weekly Flame of Love Cenacle 'on the first floor of our school building ... this Holy Hour where we pray the rosary and other prayers'. It is a rosary group in a school classroom with no mention of the Blessed Sacrament or exposition. Hard because POLICY counts a 'Holy Hour' as Adoration unless told the Sacrament isn't exposed. Unlike the Flame of Love Holy Hour 'in Saint Charles Borromeo Church' (st-charles-borromeo-drexel-hill s7), this one isn't in a church. (annunciation-bvm-havertown s15; 077-seed-review, 2026-11-27)
- Is the parish's Eucharistic Adoration Chapel at Sacred Heart Church, so its hours (Mon-Fri 9:00 AM-7:00 PM, Sat 9:00 AM-3:30 PM) go there? → Include at Sacred Heart Church, in the Adoration Chapel. With the lean, decided like ss-philip-and-james-exton s15. 8bc03744 p1 prints 'EUCHARISTIC ADORATION CHAPEL MONDAY - FRIDAY 9:00am - 7:00pm SATURDAY 9:00am - 3:30pm' in the church's own front-page schedule box beside its Mass times, and p7 calls it 'Our Adoration Chapel'. The parish has one church. Hard because no page gives the chapel's address and, unlike Exton, the website doesn't confirm it; no exposition claimed (R38). (sacred-heart-havertown s13; 077-seed-review, 2026-11-27)
- Add the centennial Mass of Thanksgiving, Sunday May 2, 2027, 12:00 PM, at Sacred Heart Church? → Leave out until details are printed. With the lean, as our-lady-of-consolation-parkesburg s13 left out an announced event until its details print. 8bc03744 p5 'Save the date! SUNDAY, MAY 2, 2027 12:00PM MASS OF THANKSGIVING' names no church (the reception is at Drexelbrook) and says nothing about that day's 11:30 AM Mass. Hard because a 12:00 PM time is printed and the church is the obvious venue; update mode will read the 2027 issues. (sacred-heart-havertown s19; 077-seed-review, 2026-11-27)
- Add Adoration on Mon Nov 30 at 6:00 PM (Exposition and Benediction at the Saint Francis of Assisi at Christmas evening)? → Nov 30 6:00 PM, no end. With the lean. ed63cf95 p4 'SAINT FRANCIS OF ASSISI AT CHRISTMAS NOVEMBER 30 – 6:00 P.M.', with a program that opens with 'Exposition of the Blessed Sacrament' and closes with 'Benediction', so exposition starts at the printed time; no end recorded, so the evening's length isn't copied onto it (POLICY, Final source checks). The same reasoning as st-aloysius-pottstown s17. Hard because no place is printed (one church) and POLICY warns against timing components; decided alike with our-lady-of-fatima-secane s15. (st-colman-ardmore s14; 077-seed-review, 2026-11-27)
- Record Thanksgiving week's 'One Mass' days as cancelling the other weekday Masses (Thu Nov 26 6:30 and 8:00 AM; Fri Nov 27 6:30 AM)? → Record the cancellations. With the lean. The aaa9dec5 p6 calendar says 'Nov 26 ... One Mass 9AM' and 'Nov 27 ... One Mass 8AM', and p2 says 'Thanksgiving: one Mass at 9 AM'. That states that the usual 6:30/8:00 Masses don't take place, which is more than the silent omission R17 describes. st-john-neumann-bryn-mawr s15 settled the same 'only Mass' wording as a cancellation. Hard because the word 'cancelled' isn't printed. (our-mother-of-good-counsel-bryn-mawr s21; 077-seed-review, 2026-11-27)
- Is the Divine Mercy Adoration Chapel at St. Pius X Church, so its Adoration hours go there? → Include at the church, in the chapel. With the lean, decided like ss-philip-and-james-exton s15 and sacred-heart-havertown s13. 7a674288 p2 DEVOTIONS: 'Eucharistic Adoration: Mon. thru Fri. in the Divine Mercy Adoration Chapel from 8:30a.m. to 5:00p.m., Sat. 8:30am to 4:00pm and Sun. 12p.m. to 5p.m.' in the parish's own box. The parish has one church, and nothing places the chapel elsewhere. Hard because no address is printed and the same box puts the Chaplet and Rosary 'in the Church', so the chapel may be a separate building (POLICY still counts the same grounds). (st-pius-x-broomall s25; 077-seed-review, 2026-11-27)
- Add the Over 50 Club's Tue Nov 17, 11:00 AM Mass for its deceased members? → Leave out. With the lean. The Over 50 Club's notice (7a674288 p3) announces a Mass for its deceased members on its meeting day. POLICY treats a memorial Mass as closed unless everyone is invited, and nothing invites the parish; like st-thomas-of-villanova-villanova s19, it is a group's own Mass. No place is named, and Nov 17 has passed. (st-pius-x-broomall s34; 077-seed-review, 2026-11-27)
- First Friday Holy Hour of Reparation: bulletin 7:00-8:00 PM or website 6:30-7:30 PM? → Bulletin: First Fridays 7:00-8:00 PM. With the lean. Both bulletins print 'FIRST FRIDAY AT ST. CHARLES ... 7:00-8:00PM—Holy Hour of Reparation' (dfa852f4 p1), as does the partner Sacred Heart, Clifton Heights bulletin (66ba8b2f p1 '7:00P.M. – Holy Hour'). The website's 6:30-7:30 looks stale (its office hours match the Nov 8 issue, not Nov 15) and may copy the Thursday confession line. (st-charles-borromeo-drexel-hill s9; 077-seed-review, 2026-11-27)
- Add First Saturday Exposition/Benediction at St. Charles, which the box ties only to the 8:30 AM Mass with no time? → Leave out. With the lean. dfa852f4 p1 'FIRST SATURDAY AT ST. CHARLES 8:30AM Morning Mass Exposition, Devotions, Confession and Benediction' gives no time or 'after' wording for the exposition, which comes with devotions and confession as one program (POLICY, Final source checks). The weekly Saturday 9-10 AM confession already covers that morning. Hard because POLICY would time 'after a weekday Mass' at 9:00 AM. (st-charles-borromeo-drexel-hill s10; 077-seed-review, 2026-11-27)
- Wednesday Adoration at St. Laurence: start at 9:00 AM or 9:30 AM (end 7:00 PM, Benediction)? → Wed 9:00 AM-7:00 PM. With the lean. c5b5eebc p2 'WEDNESDAY ADORATION is offered each Wednesday, 9:00AM to 7:00PM. Adoration ends with benediction' (also c25a4c91 p2) and the website 'Wednesday — 9:00AM (following 8:30AM Mass) - 7:00PM' against the p1 box's '9:30AM – 7:00PM'. Two current sources against one, and POLICY times 'after' the 8:30 weekday Mass at 9:00. Hard because the schedule box is the main schedule. (st-laurence-upper-darby s17; 077-seed-review, 2026-11-27)
- Add the Our Lady of Guadalupe patronal-feast Mass, Fri Dec 11, 7:00 PM, at St. Laurence? → Leave out. With the lean. The c25a4c91 p4 flyer 'Mass in Honor to our Patroness, Our Lady of Guadalupe ... Feast Day Social after Mass in Saint John XXIII Social Hall' names no church. It sits beside a 'Café Guadalupano' flyer from Parroquia Nuestra Señora de Guadalupe, Doylestown, whose patroness she is, and St. Laurence's patron is St. Laurence. The Nov 15 issue doesn't repeat it. Hard because the parish has a large Spanish community that may keep the feast. (st-laurence-upper-darby s19; 077-seed-review, 2026-11-27)
- Add the St. Andrew Nocturnal Adoration Society's Holy Hour, Thursday December 3, 7:30-8:30 PM, at Holy Cross? → Leave out. With the lean. e657c82e p6 'The Saint Andrew Nocturnal Adoration Society of Drexel Hill will meet Thursday, December 3 from 7:30 PM to 8:30 PM in the church' sits on a page of outside notices (St. Kevin, Cardinal O'Hara, St. Mary Polish Society), and the society is named for St. Andrew, Drexel Hill. 'The church' doesn't say which one (R32). Hard because the notice is printed in Holy Cross's bulletin, and such societies do rotate venues. (holy-cross-springfield s18; 077-seed-review, 2026-11-27)
- Is the parish's 'Chapel' (St. John Neumann Chapel) at the church, so its Sat 8:00 AM Confession and Thu 9 AM-12 Noon Adoration go there? → Include at the church, in the chapel. With the lean, decided like ss-philip-and-james-exton s15. 6461a6e7 p2 'RECONCILIATION Saturday 8:00 AM - Chapel' is in the parish's schedule box, and p4 places 'Thursday Adoration: Every Thursday, @ 9:00AM – 12:00Noon | St. John Neumann Chapel' with the parish's other devotions. The website gives 'Saturday: 8 am in Chapel', and the parish has one church. Hard because no page gives the chapel's address. (our-lady-of-fatima-secane s11; 077-seed-review, 2026-11-27)
- Add the Advent Retreat & Reconciliation's Exposition, Thu Dec 17 5:30 PM, as Adoration? → Adoration Dec 17 5:30 PM. Against the lean, to decide alike with st-colman-ardmore s14. 6461a6e7 p6 'Advent Retreat & Reconciliation ... Thursday, December 17, 2026, at 5:30 PM Program: Exposition of the Blessed Sacrament, Gospel Reading, Retreat Talk, Sacred Silence & Confessions'. Exposition is the program's first item, so it starts at the printed 5:30. The lean cited POLICY's rule that a larger event doesn't time its components, but recording only the start, with no end, copies no hours onto it. Nothing limits it to registrants (unlike st-agnes-west-chester s24). (our-lady-of-fatima-secane s15; 077-seed-review, 2026-11-27)
- Add the Advent Retreat & Reconciliation's Confessions, Thu Dec 17, from 5:30 PM? → Leave out. With the lean. On the same p6 program, 'Sacred Silence & Confessions' comes last, after exposition, a reading and a talk, so it has no start time of its own (POLICY, Final source checks). Unlike st-aloysius-pottstown s17, the penance service doesn't start at the printed time. (our-lady-of-fatima-secane s16; 077-seed-review, 2026-11-27)
- Add the Wednesday 7-8 PM Holy Hour in December? → Leave out. With the lean. sfaparish.org/adoration: 'During the month of December, There is NO Adoration following 8AM Daily Mass. Wednesday Evening 7PM Holy Hour may vary due to other seasonal events.' The site itself says the time may vary, and no read issue covers December; update mode will read the December bulletins. (st-francis-of-assisi-springfield s13; 077-seed-review, 2026-11-27)
- Was Tue Nov 17's 8:30 AM Mass moved to Notre Dame de Lourdes, as the Nov 15 intentions print? → No change: keep OLP. 961ec215 p3 lists 'Tuesday, November 17 / ND 8:30 AM' under the heading 'WEEKDAY INTENTIONS AT OUR LADY OF PEACE', with no notice. The box (p1), the website and the Tuesday Adoration line 'after 8:30 AM Mass (OLP Church)' all put Tuesday at OLP. The prior week's ND move had a stated reason, so this looks like a carried-over line (R39). The date has passed. (our-lady-of-peace-milmont-park s16; 092-seed-review, 2026-11-27)
- Add the website's Sunday 6:00 PM Mass (except June-August)? → Leave out. Left out. Both November issues print 'SUNDAY: 8:00AM & 11:00AM' in the box (852441c7 p1) and list only those Masses in the intentions, even though the website says the 6 PM runs in November. Two bulletin listings saying nothing is more than one missing mention. Hard because the website's other times match exactly. (st-joseph-collingdale s11; 092-seed-review, 2026-11-27)
- Add Praise on the Hill (2nd Friday of each month, 7:30 PM, 'Evening of Adoration, Praise and Worship, Confession and Fellowship') as Adoration starting 7:30 PM? → Second Fridays 7:30 PM, no end. Included: second Fridays 7:30 PM, no end. The 90204cc4 p4 flyer, headed 'ST. FRANCIS DE SALES CHURCH', calls it an 'Evening of Adoration' (listed first), shows a monstrance, and names its week (POLICY Weekly rule 2). Unlike the Night of Reparation (st-thomas-more-south-coventry s18), it is called Adoration. The start only is recorded, so the evening's length isn't copied onto it. Hard because the flyer prints no program order, unlike st-colman-ardmore s14 and our-lady-of-fatima-secane s15, so exposition may begin after some opening praise. (st-francis-de-sales-lenni s11; 092-seed-review, 2026-11-27)
- Record the extended Saturday, December 19 Confession, 3:00-4:30 PM, in place of the usual 3:30? → Yes, 3:00-4:30 PM that day. The parish's Advent 2026 page (weekdays match 2026; its footer schedule matches the Nov 15 bulletin) says 'an extended time on Saturday, December 19, from 3:00–4:30 pm'. This is the same page that settled the Dec 2 penance service (s14). Unlike st-joseph-coatesville s45, the page is clearly this year's. No read bulletin prints it yet. (nativity-bvm-media s20; 092-seed-review, 2026-11-27)
- Thanksgiving, Nov 26: record the 9 AM Mass in place of the 8 AM, per the website's footnote? → Yes, 9 AM instead of 8 AM. nativity-bvm.org's current schedule page: 'Mon-Sat: 8am (9am Mass on Memorial Day, July 4, Labor Day, Thanksgiving)' says the 8 AM moves to 9 AM on Thanksgiving, which names one day (Nov 26). The bulletins read don't mention it. Hard because it is a standing footnote rather than a dated notice. (nativity-bvm-media s22; 092-seed-review, 2026-11-27)
- Tuesday exposition: bulletin 12:30-3:30 PM or website 12:30-2:30 PM? → Tue 12:30-3:30 PM (bulletin). Both issues print 12:30-3:30 (221666d2 p3 'Adoration: 12:30 - 3:30 pm Tuesdays in church'; fac062a7 p3), and the p10 calendar agrees. The homepage's 2:30 sits in a block whose Dec 8 line also disagrees with the parish's own Christmas page. Bulletin over the less consistent website, in line with annunciation-bvm-havertown s9. (st-john-chrysostom-wallingford s10; 092-seed-review, 2026-11-27)
- Add the website's weekday 'Adoration of Christ in the tabernacle', Mon-Fri 9 AM-3 PM? → Leave out. Left out. Only the homepage has it, in the same sentence whose exposition hours (12:30-2:30) both bulletins contradict, so the sentence isn't reliable. No bulletin mentions it, and it reads close to the church being open for prayer (R38). Hard because R38 would count prayer before the tabernacle that the parish calls Adoration. (st-john-chrysostom-wallingford s11; 092-seed-review, 2026-11-27)
- Add a 6:00 PM Immaculate Conception Mass on Tue Dec 8 (bulletin; the website gives 9 AM instead)? → Dec 8 6:00 PM. 221666d2 p2 'Our Holy Day Vigil Mass is 5 pm on Dec. 7 and our Holy Day Masses will be at 8 am and 6 pm.' This is a specific dated notice in the newest bulletin; the 8 AM is the weekly Tuesday slot. The website disagrees with itself: its Christmas page puts the 5 PM on Dec 7, its mass-times block puts 5 PM on Dec 8. Hard because the same bulletin (p5) sends readers to that Christmas page, which was read later (Nov 27) and gives 9 AM. Advisory flag raised; the next issues will likely reprint the times. (st-john-chrysostom-wallingford s18; 092-seed-review, 2026-11-27)
- Add a 9:00 AM Immaculate Conception Mass on Tue Dec 8 (website; the bulletin gives 8 AM and 6 PM)? → Leave out. Left out, the other side of s18: the newest bulletin's notice (221666d2 p2) gives 8 am and 6 pm, and a wrong time is worse than a missing one (POLICY). Same difficulty as s18. (st-john-chrysostom-wallingford s19; 092-seed-review, 2026-11-27)
- Monday Adoration in the church: end at 6:45 PM (Benediction) or 7:00 PM? → Mondays 8:30 AM-6:45 PM. Ends 6:45 PM. Both issues' calendars (f2d93b60 p2 'Eucharistic Adoration....8:30AM - 6:45PM (C)') and the website's 'concludes with Benediction at 6:45PM' agree, against the p1 box's 8:30AM-7:00PM. 7:00 may be when the church closes. Two service-specific sources against one, as in st-laurence-upper-darby s17. (st-thomas-the-apostle-glen-mills s13; 092-seed-review, 2026-11-27)
- Add the third-Friday 4:00 PM Flame of Love Holy Hour (exposition) in the church? → Third Fridays 4:00 PM. Included: third Fridays 4:00 PM. f2d93b60 p9 (both issues): 'the third Friday at 4:00pm. Exposition of the Blessed Sacrament ... Devotion will be in the main Church', named by its week (POLICY Weekly rule 2). The Nov 20 calendar (p2) leaves it out, but it also leaves out other regular services such as Saturday confession. Unlike annunciation-bvm-havertown s15, this one has exposition and is in the church. (st-thomas-the-apostle-glen-mills s15; 092-seed-review, 2026-11-27)
- Add the website's Christmas Masses (Dec 24 4, 6, 8 PM; Dec 25 7:30, 10:00, 11:30 AM)? → Include. With the lean. The bulletin box (fc0dc17f p1) says 'schedule subject to change on certain Holydays. Check website for final schedule'. The site's Upcoming Holy Days list gives Dec 8 times that match the bulletin's holy-day line exactly, and its Thanksgiving 2026 event page shows the site is kept current. Unlike st-joseph-coatesville s45, nothing contradicts the list. Hard because the list prints no year and no bulletin read prints Christmas times. The Friday 7:00 AM weekly slot stays on Dec 25 (R17). (st-margaret-narberth s28; 110-seed-review, 2026-11-27)
- Add an Immaculate Conception Mass on Tue Dec 8 at 12:00 PM, from the website? → Dec 8 12:00 PM. With the lean. The homepage's Upcoming Holy Days ('Immaculate Conception December 8 : 7:30 AM 12:00 PM') and the standing holy-day line both give 7:30 AM and 12:00 PM, and the site's Thanksgiving times match the Nov 15 bulletin (649db1e0 p4). Hard because no bulletin read prints Dec 8 and the mass-times page's '(Dec 9)' is a 2024 leftover; the date itself comes from the homepage block. (st-matthias-bala-cynwyd s17; 110-seed-review, 2026-11-27)
- Keep Saturday's 9 AM Mass and Saturday confessions year-round, or drop them for the summer as the website's 2022-dated summer note says? → Year-round, as the bulletin prints. With the lean. Both issues' box (571b0f5c p1, fef0959c p1) prints 'Saturdays: 9:00 AM & 5:15 PM' and 'CONFESSIONS Saturdays: 8:30 - 9:00 AM; 4:00 - 5:00 PM' with no season. The website note 'Beginning Saturday June 11' fits 2022 (R6: an announcement from an earlier period), and its mid-June to Labor Day limits can't be written as months. Hard because a summer break may well recur; update mode will read the summer bulletins. (holy-saviour-norristown s10; 110-seed-review, 2026-11-27)
- Add a 10:00 AM Immaculate Conception Mass on Tue Dec 8 (website; bulletin holyday line says 8 AM and 7 PM)? → Leave out. With the lean, the other side of s16. The website's undated 'Immaculate Conception December 8 : 10:00 AM' contradicts both current bulletins' holy-day line (6c937ee6 p2, f7ef8786 p2, repeated in St. Helena's 17534561 p2), and a wrong time is worse than a missing one (POLICY). (st-titus-norristown s17; 110-seed-review, 2026-11-27)
- Add weekday Adoration in the chapel, 7:00 AM-9:00 PM, on Mondays, Tuesdays and Fridays, as the website's calendar lists it? → Mon, Tue, Fri 7:00 AM-9:00 PM. With the lean. The homepage's live calendar lists 'Adoration ... 7:00am - 9:00pm @ Chapel' on Fri Nov 27, Mon Nov 30 and Tue Dec 1. Its Masses match the schedule page exactly, and the image-only bulletins (3ad84210, checked by sheet) print no schedule, so nothing contradicts it (R6, as st-basil-the-great-kimberton s19). Hard because each weekday is seen only once. (st-eleanor-collegeville s24; 122-seed-review, 2026-11-27)
- Add weekday Adoration 7:00 AM-9:00 PM on Wednesdays and Thursdays too, which the website's calendar window doesn't reach? → Leave out. With the lean. No source shows a Wednesday or Thursday at these hours (the calendar runs Nov 27-Dec 1), and the Thursday 7 PM Divine Mercy devotions use Our Lady's chapel (3ad84210 p5). A wrong time is worse than a missing one (POLICY). (st-eleanor-collegeville s27; 122-seed-review, 2026-11-27)
- Record the Divine Mercy Adoration Chapel's public hours, daily 6 AM-9 PM, at St. Mary Church? → Daily 6 AM-9 PM in the chapel. With the lean. 0adbcd5a p5 (also d607fdb2 p5): 'open to the general public from 6am to 9pm. Scheduled adorers only from 9pm to 6am.' R46's access values don't fit: 'arrangement' hides daytime walk-ins and 'code-after-hours' claims a code nothing prints. The public hours are what a visitor can use. The chapel is on campus (one church; website 'here at St. Mary'). Hard because R46 normally wants one 24h slot (advisory flag raised). (st-mary-schwenksville s17; 122-seed-review, 2026-11-27)
- Record the Divine Mercy Adoration Chapel instead as one 24-hour chapel, by arrangement? → Leave out. Leave out. This is the other side of s17, decided there; 'arrangement' would wrongly say the public can't come 6 AM-9 PM. (st-mary-schwenksville s24; 122-seed-review, 2026-11-27)
- Add the Monday 6:00 PM 'All Souls' Day Mass' as a weekly November Mass? → Leave out. With the lean. ee619bbb p7 (Nov 16) and f0cc0a83 p7 (Nov 9) each print one dated 'All Souls' Day Mass'. Nothing prints Nov 23 or 30 or says every November Monday, so a November season would be invented (R33). The Nov 16 date is already recorded (s23). (our-lady-of-the-sacred-heart-hilltown s22; 122-seed-review, 2026-11-27)
- Saturday 8:30 AM Mass: year-round, or not in summer as the website says ('no Saturday daily Mass from May to Labor Day')? → Saturdays 8:30 AM, Sept 8-Apr 30. With the lean: Sept 8-Apr 30. The current homepage (same times as the 838277b7 p1 box) says '*there is no Saturday daily Mass from May to Labor Day'. November issues can't show a summer break, so this is a missing mention, not a conflict (R6). Unlike holy-saviour-norristown s10, the note isn't stale and names its months. Sept 8 always falls after Labor Day. (st-maria-goretti-hatfield s11; 122-seed-review, 2026-11-27)
- Add the Family Adoration & Cookout/Potluck, Thu Nov 19, 6:00 PM, as Adoration (no end)? → Nov 19 6:00 PM, no end. With the lean, decided alike with st-colman-ardmore s14 and our-lady-of-fatima-secane s15. 838277b7 p5 '6:00PM – Family Adoration & Cookout/Potluck, Chapel & Courtyard' names Adoration first, in the chapel. Only the start is recorded. Hard because it is combined with a cookout. The date has passed. (st-maria-goretti-hatfield s15; 122-seed-review, 2026-11-27)
- Saturday 8:30 AM Mass: year-round, as the bulletin and schedule page print, or not in summer as the homepage says? → Saturdays 8:30 AM year-round. With the lean: year-round. c47d2c8b p1 'Monday - Saturday: 8:30 a.m.' and the schedule page give no season. Only the homepage adds '(No Saturday 8:30am in the Summer)', which names no months, so any season would be invented (R33), as in holy-saviour-norristown s10. Unlike st-maria-goretti-hatfield s11, there are no months to write. Update mode will read the summer bulletins. (st-rose-of-lima-north-wales s10; 122-seed-review, 2026-11-27)
- Add the website's Wednesday Adoration, 9:30 AM-6:00 PM (Benediction), which pauses mid-June through Labor Day? → Wednesdays 9:30 AM-6:00 PM, Sept 8-June 14. With the lean: Sept 8-June 14. stalphonsusparish.org/adoration: 'Wednesdays, beginning at 9:30 AM and concluding with Evening Prayer and Benediction at 6:00 pm. There is no Adoration ... from mid-June through Labor Day.' The site's Mass and confession times match the f3b08d77 p1 box, so the website-only Adoration is included as in st-basil-the-great-kimberton s19. The season never claims a summer Wednesday. Hard because 'mid-June' has to be approximated. (st-alphonsus-maple-glen s15; 122-seed-review, 2026-11-27)
- Spanish Sunday confession 12:30 PM ('SA & SJ'): at the church holding that Sunday's 1:00 PM Spanish Mass, or at both churches every Sunday? → At the Spanish Mass's church (SJ 1st/3rd, SA 2nd/4th/5th). With the lean. 75ce39e5 p2: 'Confession in Spanish 12:30 PM- SA & SJ', directly under 'Spanish 1:00 PM First & Third Sunday- SJ / Second, Fourth & Fifth Sunday- SA'. One priest (Father Abel, 77f61fe9 p3) hears it and says that Mass, so it follows the Mass's church. Hard because 'SA & SJ' could be read as both every week. (st-anthony-of-padua-ambler s10; 122-seed-review, 2026-11-27)
- Limit the Tuesday 6:30 AM Mass to September-May, as the website says? → Tuesdays 6:30 AM, September-May. With the lean. stgensparish.com/sacraments: 'Tuesday : 6:30 AM English (September - May)', on a current page whose other times match b6241047 p1 exactly. A November bulletin can't show the summer break (R6). Decided alike with st-maria-goretti-hatfield s11. (st-genevieve-flourtown s15; 122-seed-review, 2026-11-27)
- Add the Immaculate Conception school Mass, Tue Dec 8, 9:00 AM ('all are welcome')? → Dec 8 9:00 AM. With the lean. b6241047 p4: 'Tuesday, December 8 – School Mass at 9am, all are welcome', dated and open (POLICY). The parish has one church with the school on campus, as st-joseph-spring-city s21. Hard because no place is named. (st-genevieve-flourtown s16; 122-seed-review, 2026-11-27)
- Add the Thu Jan 21 faith-formation session held 'within a Holy Hour format' in church, 6-7 PM, as Adoration? → Jan 21 6:00-7:00 PM. With the lean. b6241047 p3: 'Thursdays, 6-7pm ... except week 3* which will take place in church within a Holy Hour format ... January 7, 14, 21*, 28'. POLICY counts a Holy Hour as Adoration unless told the Sacrament isn't exposed. It is in the church, unlike annunciation-bvm-havertown s15's school-room Holy Hour. Hard because it is a Bible-study session and exposition isn't mentioned. (st-genevieve-flourtown s17; 122-seed-review, 2026-11-27)
- Add a 7:00 PM Mass on Tue Dec 8 from the Holy Day line, or is that line's 7PM the Dec 7 vigil? → Leave out. With the lean: leave out. The line's 7PM matches the 7:00 PM vigil printed for Mon Dec 7 (9c1694d3 p5) and may be that Mass, and a wrong time is worse than a missing one (POLICY). Hard because many parishes hold both a vigil and an evening Mass on the day. December issues will settle it. (st-philip-neri-lafayette-hill s18; 122-seed-review, 2026-11-27)
- Wednesday Adoration: bulletin 7:00 AM-6:00 PM or website 7:00 AM-7:00 PM (Benediction), in the Adoration Chapel? → Wed 7:00 AM-6:00 PM (bulletin). Both issues' calendars print 'Adoration, 7 am - 6 pm, closing with Benediction' (e2723996 p3, cbc095ec p3) on consecutive Wednesdays, against the website's 7 PM. Two current bulletin listings outweigh one website line, as in st-thomas-the-apostle-glen-mills s13. Hard because the website matches the bulletin everywhere else, so either end could be the newer one. (presentation-bvm-cheltenham s10; 137-seed-review, 2026-11-27)
- Add First Friday confessions, heard during the 6:00 PM Holy Hour? → First Fridays from 6:00 PM, during Adoration. bb047337 p1 'First Friday of the Month 6:00 p.m. Holy Hour (Exposition of the Blessed Sacrament, Confessions, ...)': confessions are part of an exposed Holy Hour, which is POLICY's one exception (Confession during Adoration takes the Adoration's times). Only the start is recorded. Unlike our-lady-of-fatima-secane s16, the confessions don't come last after a talk. luna read it the same way. (st-james-elkins-park s21; 137-seed-review, 2026-11-27)
- Add the Christmas Eve children's Mass, which follows the 3:30 PM procession to the crib? → Dec 24 at 3:30 PM, with a note. ba0b9723 p10 '3:30 p.m. Children's Procession to the Crib, immediately followed by Mass in Church', and p5 calls it 'the Childrens Christmas Eve Mass in Church on December 24th at 3:30 p.m.' The parish itself dates the Mass at 3:30, and the note says it begins with the procession. (immaculate-conception-bvm-jenkintown s21; 137-seed-review, 2026-11-27)
- Thanksgiving, Thu Nov 26: record the box's 'Holiday Mass: 8:30am' in place of the 8 AM weekday Mass? → Yes, 8:30 AM instead of 8 AM. d3d25a69 p1 gives 'Weekday Mass: 8am ... Holiday Mass: 8:30am' as a standing replacement, and Thanksgiving is the plainest case of a holiday, as nativity-bvm-media s22 recorded. Hard because the line names no holiday, Veterans Day kept its 8:00 (6a5a5ea0 p2), and R17 wants a cancellation stated. The date has passed, so it has little effect on the site. (our-lady-help-of-christians-abington s19; 137-seed-review, 2026-11-27)
- Add the Fatima pilgrimage program's Masses (Fri Nov 20, in the 7:15 PM program; Sat Nov 21, in the 12:00 AM program) at their program's start time? → Leave out. 1663da62 p9: the Nov 20 Mass is the fifth item after the 7:15 PM procession, scapular, rosary and coronation, and the Nov 21 Mass follows the 12:00 AM procession and Benediction. Neither has a start time of its own (POLICY, Final source checks), the same reasoning as our-lady-of-fatima-secane s16. Both dates have passed. (queen-of-peace-ardsley s16; 137-seed-review, 2026-11-27)
- Add the website's summer weekday schedule (June 8-Sept 7: Mass 8:00 AM, Adoration from 8:30 AM)? → Add, June 8-Sept 7. Decided alike with s7: the same homepage gives the summer 8:00 AM Mass and 'Summer Eucharistic Adoration: Monday & Wednesday 8:30AM-7PM and Friday 8:30AM-5PM'. Limiting the regular schedule without adding the summer one would leave weekdays empty in summer. (st-david-willow-grove s12; 137-seed-review, 2026-11-27)
- Count the weekly Thursday 7-8 PM Eucharistic Prayer Meeting in church as Adoration? → Thursdays 7:00-8:00 PM. Against the lean. 53d80c79 p2 (also 21501869 p2) prints 'Weekly Eucharistic Prayer Meeting Thursdays, 7:00pm to 8:00pm in church' directly under the heading 'Exposition of the Blessed Sacrament', next to the Tuesday exposition. The bulletin thus calls it exposition, which is what the st-thomas-more-south-coventry s18 Night of Reparation lacked. Hard because the website's Adoration Times page lists only Tuesday (advisory flag). (st-luke-the-evangelist-glenside s13; 137-seed-review, 2026-11-27)
- Friday 6:30 AM: a Mass (bulletin) or a Communion Service (website)? → Fridays 6:30 AM Mass. Both issues' box 'Monday, Wednesday, Friday: 6:30 AM' (53d80c79 p1, 21501869 p1) and both weeks' intentions name a Friday 6:30 Mass ('6:30 am All Souls in Purgatory', p2), as on Mass days. The website's '(Communion Service)' tag is outweighed. (st-luke-the-evangelist-glenside s9; 137-seed-review, 2026-11-27)
- Tuesday Adoration in the church: which hours and season? → Tue 9:00 AM-7:00 PM, Sept-June. Both issues print 'Tuesdays after the 8:30am Mass until 7:00pm' (p2), and p6 says sessions start 'at 7 PM after Exposition'. The bulletin's end is taken over the website's 6 PM, as st-john-chrysostom-wallingford s10 did. The website's '(September 2026 - June 2027)' is a season a November issue can't show (R6), kept as in st-alphonsus-maple-glen s15. Starts at 9:00, 30 minutes after the 8:30 Mass (R10). (st-luke-the-evangelist-glenside s12; 137-seed-review, 2026-11-27)
- Add the St. Luke School First Friday Mass, 10:30 AM, from the website calendar? → Leave out. Only the website calendar lists it ('St. Luke School First Friday Mass ... 10:30 AM Repeats every first Friday'), and nothing invites the parish. POLICY leaves out a school Mass for students. Unlike st-genevieve-flourtown s16, no 'all are welcome'. (st-luke-the-evangelist-glenside s23; 137-seed-review, 2026-11-27)
- Add the Saturday May 1, 2027, 11:00 AM First Communion Mass? → Leave out. 53d80c79 p4: a First Communion Mass for the parish's registered children, with no invitation to the parish. It is five months away; as with sacred-heart-havertown s19, update mode will read the 2027 issues. (st-luke-the-evangelist-glenside s24; 137-seed-review, 2026-11-27)
- Add the First Reconciliation, Wednesday Feb 24, 2027, 6:30 PM, as a confession? → Leave out. 53d80c79 p4 'First Reconciliation Wednesday, February 24th at 6:30pm' is the second graders' first confession, not a time open to all penitents, like the registered-group confessions left out in st-agnes-west-chester s24. (st-luke-the-evangelist-glenside s25; 137-seed-review, 2026-11-27)
- Saturday morning confession: end at 8:45 AM (bulletin) or 8:50 AM (website)? → Saturdays 8:15-8:45 AM (bulletin). Both issues' box print 8:15-8:45 (49cf51e5 p1, c0f610a3 p1), and the bulletin is the weekly-edited source, in line with annunciation-bvm-havertown s9. The five-minute gap before the 9:00 Mass matters little. (st-agnes-sellersville s12; 137-seed-review, 2026-11-27)


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
