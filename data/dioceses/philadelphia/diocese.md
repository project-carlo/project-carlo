---
name: Roman Catholic Archdiocese of Philadelphia
state: PA
website: https://archphila.org
status: exploring
gcatholic: phil0
city_aliases:
  Buckingham: Doylestown
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

From `probe url` on 26 directory websites, the browser on 8 of them, and a scan of John Patrick
listings (2026-10-28). Each batch settles its own rows.

- **John Patrick Publishing prints most of this diocese** (the firm is local). Parish sites link
  `jppc.net/onlinebulletins/<id>template.pdf` or `church-bulletin.org/?id=<id>`, which redirect
  to a `church-bulletin.org/<slug>` listing of dated PDFs with "Latest Edition" and the parish's
  name, town and ZIP. `tools/jppc_scan.py` read ids 1–1300 on 2026-10-28: 269 listings have a
  PA 18xxx–19xxx ZIP, 193 of them with a current issue (25 October 2026), 165 in 19xxx.
  `raw/jppc-directory.json` (`tools/jppc_match.py`) pairs 184 of the 218 directory parishes with
  a listing by name and town (or a ZIP on the directory page), **172 with a current issue**: look
  the parish up there first. A listing's town can be the township or post town, not the
  directory's (St. Titus, Norristown is 95 under East Norriton; St. Thomas of Villanova is 180
  under Rosemont), so also search `raw/jppc-pa.json` by name. Three current listings match no
  directory parish: 167 (Old St. Mary's, below), 286 "Saint Miriam Parish & School", Flourtown
  (an Old Catholic community claiming the Union of Utrecht, with a "Bishop in Residence":
  excluded `not-catholic`, so read the cover and the community's own "Who We Are" page before
  taking an unmatched listing as Roman Catholic), and 241 "The National Shrine of Saint Rita of Cascia" (19146), which publishes its own issue. It is
  a lead, not a match: confirm the listing's name, town and cover (151 "St. Rose of Lima" is the
  Philadelphia parish; St. Rose of Lima, North Wales has no listing). Listings outlive their parish's
  move to another publisher (76 of the 269 have no edition at all; 12 directory parishes match
  only such a listing, e.g. St. Bartholomew 73, St. Charles Borromeo 130 and 287, St. John
  Fisher, St. Barbara, St. Cyprian, St. William), and a listing's
  name can join two parishes (116, "The Roman Catholic Church of Saint Timothy and Saint
  Bartholomew") or keep a relegated church (167, "Old Saint Mary Church & Holy Trinity Church").
  Record the row as `other` with `page-pdfs https://www.church-bulletin.org/<slug>`, as
  Allentown, Harrisburg and Wilmington do, unless the parish's own eCatholic `/bulletins/`
  archive carries the same file (below). A parish with no website of its own takes the listing
  URL as its `website` (St. Ambrose). **The current channel is whichever has the latest
  issue:** a listing with no editions (a daily-readings page only, St. Maximilian Kolbe 124;
  Mary, Mother of the Redeemer, North Wales 265, whose current issues are
  `files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf`; St. Joseph, Downingtown 138, which never
  had one; St. William 28, whose eCatholic archive is behind Cloudflare: `visit.py`, below) means
  the parish publishes elsewhere, so look at its eCatholic `/bulletins` archive first, then ParishesOnline (St. John Fisher,
  Boothwyn, below); a parish archive that
  stopped (SS. Simon and Jude's eCatholic, last 2025-02-16; St. Francis de Sales, Lenni's and
  St. Joseph, Aston's eCatholic, March 2025; St. Basil, Kimberton's own site, a
  year behind; Sacred Heart, Havertown's WordPress, last 2024-10-27; St. Isaac Jogues's
  Squarespace `/bulletins`, July 2022; Epiphany, Plymouth Meeting's Wix "Bulletin Archive",
  2025-12-28; St. Eleanor's Joomla `/resources/bulletin`, 2025-08-31, a site that answers 403 to
  `probe url` and `probe pdf` and loads in the browser) or lags by even a week (St. Gabriel, Stowe's site at 18
  October with 25 October on the listing, files differing byte for byte; St. John Neumann, Bryn
  Mawr's own text-layer copies and Our Mother of Good Counsel's eCatholic, both at 18 October;
  Our Lady of Calvary's WordPress archive at 4 October;
  St. Elizabeth, Upper Uwchlan's eCatholic; Sacred Heart, Oxford's Wix `/bulletins`; Sacred
  Heart, Clifton Heights's `/bulletins/`, two weeks behind, files `092<Month>-<day>.pdf` named
  for its listing id, with irregular suffixes and no year) leaves the listing as the channel, so
  open the newest dated entry on both.
  A site's "Current Bulletin" image linking `jppc.net/onlinebulletins/<id>template.pdf` names
  the listing, and a site whose footer reads "Designed and Hosted by John Patrick Publishing"
  hosts no PDFs of its own, even when an old self-upload archive remains (Holy Cross,
  Springfield: 2025 uploads only; its new Parish Life Director did not change the publisher),
  but it need not have a John Patrick listing either (Corpus Christi, Lansdale prints with Bon
  Venture, below). A parish absent from the scan can still self-host (St. Patrick,
  Malvern, below). **Covers mislead; compare the masthead and the page-2 Mass box.** Two
  parishes under one pastor can share the printer's cover art (Annunciation BVM and St. Denis,
  Havertown), print the same combined Mass schedule box (St. Charles Borromeo, Drexel Hill 220
  and Sacred Heart, Clifton Heights 92), print each other's schedule and one joint
  Mass-intentions list (St. Helena 43 and St. Titus 95), or carry each other's Mass times and
  rectory on the cover as "Twinned Parishes" (St. Joseph 7 and Presentation BVM 15, Cheltenham),
  or name one Parish Life Director and the same clergy on both mastheads and run a joint CYO
  (Holy Trinity 9 and St. John the Evangelist, Morrisville: 4 pages with a text layer against 8
  image-only), or share a dean who is pastor of one and administrator of the other and a vicar
  titled for both ("Our Lady of Calvary/Christ the King": staff, not a masthead), and still
  publish separate issues, with different md5 and page counts, their own mastheads and
  page 2, whose footer code names the listing ("007 St. Joseph - Cheltenham", "015 p. 2"):
  shared content is not a shared bulletin, and each church stays a row under its own parish. A **joint masthead** is: one issue
  headed "St. Anthony & St. Joseph Parishes" with both addresses, one combined Mass schedule and
  one intentions list tagged SA or SJ is one row with two churches, under whichever parish has
  the listing (240, St. Anthony of Padua, Ambler; St. Joseph, Ambler has none). So is a masthead
  setting two church titles side by side over one parish office, one pastor and one Mass box,
  even when the directory keeps two parish pages (SS. Timothy and Bartholomew 116; St.
  Bartholomew's own listing 73 has no editions). A neighbour's box
  on the cover (St. Thomas of Villanova 180 and Our Mother of Good Counsel carry each other's) is
  not a worship site of the row. A listing with no editions can belong to a campus (Villanova
  University 233) or a worship site (Notre Dame de Lourdes, Swarthmore 12, under Our Lady of
  Peace 109) whose Masses appear only in a parish's bulletin. Such a listing can still carry the
  church's own address and phone (St. Alice 38: 150 Hampden Road), useful against GCatholic's
  intersection addresses. Never guess a slug: a wrong one returns the generic
  home page with HTTP 200. church-bulletin.org answers 406 to a bare "Mozilla/5.0" user agent;
  plain curl works. **Some John Patrick PDFs have a text layer and some don't** (text: St.
  Francis of Assisi 175, St. Kevin 66, Fatima 83, St. Dorothy 209; image-only, `probe pdf`
  showing 0 readable pages: Holy Cross 24, Sacred Heart, Swedesburg 143, Mother of Divine
  Providence 27, St. Bede, Holland 103, St. Vincent de Paul, Richboro 19, Our Lady of Good
  Counsel, Southampton 6; a text layer garbled by font substitution, where `pdftotext` gives gibberish,
  counts as none: St. Patrick, Norristown 89): check `pdftotext -l 2` first. An image-only listing often has
  older issues with a text layer: `pdftotext` on one a few months back reads the masthead
  cheaply and dates a joint masthead or a change of name. For the current image-only
  issue render page 1, and page 2 for the Mass schedule, with parish-site-access `render.py`
  (or `pdftoppm -r 70 -png`, which the Read tool reads) to read the masthead, and cite what the
  render shows in a `note`, not a `quote`, which recheck can't find in a file with no text;
  `fetch:check` then reports `publication_identity` `unverified`, by design. **Take Mass times
  from the bulletin, not the directory**, whose times can be years stale (St. Joseph,
  Warrington: directory Sat 5:30 PM, Sun 7/8:30/10/11:30; bulletin Sat 4:00 PM, Sun
  7:30/9:30/11:30). They sit on the cover or in a
  page-2 sidebar (St. Eleanor 10, Sacred Heart, Royersford 13, St. Mary, Schwenksville 4), and
  some issues print no Mass box at all (St. Eleanor): then take the times from the parish site.
- **eCatholic:** several sites (St. Anselm 24649, St. Genevieve 38659, St. Christopher 16547,
  St. Anne 34036, St. Anastasia 12297, St. Barbara 21577, St. Francis de Sales, Lenni 2405)
  answered plain `probe url` on 2026-10-28. Many link a John Patrick listing rather than
  hosting the bulletin (St. Colman, Ardmore's `/bulletins` page is empty; stkevin.com,
  ecatholic:34467, is only a link page whose `/bulletins` links the jppc template; Our Lady of
  the Sacred Heart, Hilltown 38359, St. Genevieve 38659 and St. Andrew, Newtown 37063 link only
  `church-bulletin.org/?id=<n>` and no `files.ecatholic.com` PDF: an `other` row on the listing;
  holytrinitymorrisville.org embeds eCatholic id 1047 and hosts no bulletins, linking only the
  jppc template 009), so an
  eCatholic id alone is not the publication and stays out of `publication`; a `/bulletins` page
  linking a current `files.ecatholic.com/<site id>/bulletins/<yyyymmdd>.pdf` is. Where that
  file is the John Patrick issue, use an `ecatholic` row and add the listing as a second
  `url:` publication id: byte-identical (md5) for St. Agnes and SS. Peter and Paul, West
  Chester, SS. Philip and James, Exton, Maternity BVM and Sacred Heart, Royersford (25820,
  listing 13); but the two copies of one issue can also differ in
  size and text layer, so when the bytes differ compare the rendered cover and Mass box before
  calling them separate. The other way round, an eCatholic file can be the parish's own layout
  of the same Sunday and not a copy (St. Jude, Chalfont 20043: 10 pages with a text layer against
  the listing's 12 image-only pages, 18 October): leave `ecatholic:<id>` out of `publication`
  and take whichever channel is current (St. Jude's archive was a week behind: the listing,
  120). An archive can post next Sunday's file days early (Our Lady of the
  Rosary, Coatesville had 20261101 on 2026-10-28), which `fetch:check` reports as freshness
  `future`; keep the `ecatholic` row and both ids in `publication`, with the listing as the
  fallback `other` row if future issues are rejected.
  Files under `/documents/` instead of `/bulletins/` (St. Ann, Phoenixville) make the
  `ecatholic` resolver pick a stale issue (2016): use the `other` row on the John Patrick
  listing and keep `ecatholic:<id>` in `publication`. Plain curl of a `/bulletins` page gets a
  Cloudflare "Just a moment" stub, and `probe url` can answer 403 (sfdslenni.org and
  churchofstjosephaston.org on `/bulletins`, staparishgm.org; stgensparish.com answered in the
  survey and 403 to a map job the same day); `probe get <url> --out <file>`
  saves the raw body (the page with its PDF links, or the PDF), not JSON: read it with
  `tools/htmltext.py` or grep, not `jq` (`--out` is relative to the repo root, not the shell's
  directory: give `scratch/<run>/<job>/<file>`), and `visit.py` loads it otherwise (staparishgm.org
  showed its `church-bulletin.org/?id=097` link). A site that answers 403 to `probe url` and
  curl can still have a current archive: `visit.py` on `/bulletins` lists the
  `files.ecatholic.com` PDFs, which plain curl downloads, so compare md5 with the John Patrick
  issue before choosing the `ecatholic` row (stlukeglenside.org, 28474, and St. Thomas Aquinas,
  Croydon, 2517 with listing 77: byte-identical). A file found only in the page source (the
  newest `files.ecatholic.com` `href`) is not visible text: cite it in a `note`, never a
  `quote`, which recheck can't find. `probe pdf` takes URLs only; for a downloaded file use
  `render.py` or a PDF text tool. A home page's first PDF can be a flyer (St. Anselm's "St.
  Lukes Open Flyer"; its bulletin is on Bon Venture, below).
- **Self-hosted:** Squarespace (St. Augustine: `/bulletins`, files
  `/s/210-Bulletin_October-25-2026.pdf`), Wix (`/_files/ugd/<hash>.pdf`; but Wix archives here
  often stop or hold only flyers and forms: St. Dorothy's "Parish Bulletin" page links a
  registration form, St. Francis of Assisi, Norristown's newest PDF is a godparent-eligibility
  letter, Immaculate Conception, Jenkintown's only PDF is a fiscal report, St. Martin of Tours,
  New Hope's one home-page PDF is a PREP calendar and Epiphany, Plymouth
  Meeting's archive stops in December 2025, while the home page's
  "Current Bulletin" link to `jppc.net/onlinebulletins/<id>template.pdf` or
  `church-bulletin.org/?id=<id>` names the real channel, the listing (31, 91 and 145). Read the
  file's first page before calling a Wix site a bulletin channel. A Wix `/bulletins` page can
  list its issues oldest first, so `page-pdfs` on it would pick a stale file even when it holds
  a byte-identical copy of the current one: St. Hilary of Poitiers, Rydal's first `_files/ugd`
  link is 4 January 2026; use the newest-first listing, 160). St. Bernard, Mayfair's bare Wix
  site (stbernard-mayfair.wixsite.com) has a "Previous Bulletins" page running oldest first from
  7 June to next Sunday's 1 November file: keep its John Patrick listing. A plain-HTML archive ordered by
  month then year does the same (St. Ignatius, Yardley's `Bulletins/<yyyy>/Bulletin-<Month>-<dd>-<yyyy>.pdf`,
  a 10-page text-layer layout of the listing's 12-page image-only issue, not byte-identical but
  handy for reading the masthead): keep the listing, 245, as the `page-pdfs` channel. A parish's
  own copy can be named for its Friday upload date, not the Sunday (Our Lady of Consolation,
  Tacony: `October-23-2026.pdf`, a text-layer file, is the listing's image-only 25 October
  issue): date it by the issue's own header. WordPress
  bulletin pages (St. Denis `/bulletinandworshipaids/`, St. Andrew, Drexel Hill,
  Holy Innocents, St. Dominic; St. Patrick, Malvern `/bulletin/`, text-layer files
  `wp-content/uploads/<yyyy>/<mm>/<yyyymmdd>B.pdf`, which `page-pdfs` reads and no John Patrick
  listing carries; St. Joseph, Warrington `/weekly-bulletins/`, newest first,
  `wp-content/uploads/<yyyy>/<mm>/bulletin-<yyyy-mm-dd>.pdf`, likewise with no listing). A WordPress site posting one page per issue (St. Katharine of Siena) gives
  `page-pdfs` on its post index nothing, though each post links a byte-identical copy of the
  John Patrick PDF: use the listing. Likewise when a WordPress `/bulletins/` page or a Wix
  `/events/bulletins` page carries a current, byte-identical (md5) copy under irregular or hashed
  `/_files/ugd/` file names (St. Patrick, Kennett Square and listing 236; St. Mary Magdalen,
  Media; Mother of Divine Providence's WordPress `/bulletins/` and listing 27; St. Philip Neri,
  Lafayette Hill's `/bulletins/`, `shared/bulletins/<yyyy>/<mm>-<dd>-<yyyy>.pdf`, and listing 14; Our Lady of Good Counsel,
  Southampton's `/bulletin/`, newest first, `006-October-25th-2026.pdf`, and listing 6): keep the
  listing as the `page-pdfs` channel and note the copy as equal, with its md5, in
  `publication_reviews`.
  A Squarespace page whose issue links end in `/file` rather than `.pdf` gives `page-pdfs`
  nothing (St. Mary of the Assumption, Phoenixville, which also answers 403 to `probe url` and
  `probe get` and is readable with `visit.py`): use the parish's John Patrick listing. Such `/file` links can also answer 403 to every recipe
  (`page-pdfs`, `dated-post`, `linked-issue-page`, `redirected-pdf`) while an in-page `fetch()`
  in Chrome (`tools/browser_download.py`) downloads the PDF to read; with no John Patrick
  edition to fall back on, the row is `no_bulletin` with `bulletin_status: access-blocked` and a
  `revisit` (St. Catherine of Siena, Horsham, whose listing 117 is empty). Numbered
  Squarespace files with no date in the name, listed newest first (St. Mary's Quasi-Parish,
  FSSP: `/bulletin`, `/s/48-Christ-the-King-jm5e.pdf`), are read correctly by `page-pdfs`, but
  `fetch:check` freshness stays `unknown`; so does a Squarespace page posting next Sunday's file
  early under underscore names (Holy Innocents: `2026_11_01.pdf`), which is not a stale pick. A
  Weebly page linking hundreds of old, misnamed files can make `page-pdfs` take one whose name
  reads as a future date (Holy Angels: `2017_11-02.pdf` read as 2026-11-02): add
  `filename=*26*` to the recipe and rerun `fetch:check`. That filter matches only 2026 files and
  must become `*27*` in January 2027. Don't print a Wix page's `href` list whole: it
  carries thousands of characters of parastorage URLs (`grep -v parastorage`). A GoDaddy
  Website Builder `/bulletins` page links hash-named `img1.wsimg.com` PDFs whose names carry
  the date (St. Lawrence, Riegelsville): `page-pdfs` reads them and picks next Sunday's file
  early, so freshness reads `future`. A Google Sites page that embeds each Sunday as a
  `drive.google.com/file/d/<id>/preview` iframe, with no shared folder, gives `page-pdfs` no
  links (`resolve_failed`), though each file downloads by hand from
  `drive.google.com/uc?export=download&id=<id>`, newest embedded first: record `no_bulletin`
  with `bulletin_status: unsupported-format` and a `revisit` (Our Lady of Hope, Philadelphia).
- **Bon Venture Services:** a minority printer here (Corpus Christi, Lansdale; St. Rose of
  Lima, North Wales; St. Christopher, page 1904; St. Anselm). Its sponsor page `sponsors.bonventure.net/?page=<id>` lists dated
  `pdfs/<id>/<yyyy-mm-dd>.pdf`: record `other` with `page-pdfs
  http://sponsors.bonventure.net/?page=<id>`, as Allentown does, over `http://` (the server
  sends no intermediate certificate). It lists next Sunday's PDF early, so `fetch:check`
  freshness reads `future`. The link can hide on a site John Patrick hosts: Corpus Christi's
  Bulletins page is empty and only the menu's BULLETIN link, seen in `visit.py`'s link list,
  goes to the sponsor page; St. Anselm's (page 10314) is the home page's "WEEKLY BULLETIN"
  heading, while its eCatholic archive stopped in January 2022, its John Patrick listing has no
  editions and the home page's only PDF is a school flyer. On an eCatholic site it can be the
  "Weekly Parish Bulletins" menu item or "Latest Bulletin" button pointing offsite (St.
  Christopher), which `probe url` doesn't report as a bulletin link. Read the whole link list
  (the nav hrefs in the page source), not only the PDF links, for a bonventure.net, jppc.net or
  church-bulletin.org link before calling the bulletin missing. A parish can instead post the issue on its own site (srol.org:
  `/assets/Uploads` files with irregular names, newest first, next Sunday early), where
  `page-pdfs` takes the first link and freshness stays `unknown`; the last page's printer
  footer names Bon Venture.
- **A shared WordPress host that answered HTTP 500 to everyone:** saintfrancescabrini.net,
  annunciationbvmchurch.org, sainthelenaparish.net, scbdh.org and epiphanychurch.church all
  resolve to 69.16.220.73 (nginx) and gave 500 to `probe url` and to Chrome on 2026-10-28. The
  500s pass: scbdh.org (St. Charles Borromeo, Drexel Hill) answered 200 later that day and
  saintfrancescabrini.net on 2026-10-29, its Parish Bulletin page linking only the jppc template
  228. Try again later; meanwhile find their John Patrick listings (St. Charles Borromeo, Drexel
  Hill is 220, Annunciation BVM 127, St. Frances Cabrini 228).
- **The directory's website can be the wrong site:** the parish school's (Our Lady of Mount
  Carmel, Doylestown: olmcs.org is the school; the bulletin footer gives ourladymtcarmel.org) or
  a Linktree (saintvincents.net -> linktr.ee/svdprichboro, whose bulletin link is the jppc
  template: the listing is still the channel), or a redirect to an abandoned Wix site whose tab
  title is another church's (skschurch.com shows "New Faith Gospel Church"; St. Katharine of
  Siena's live site, stkatherineofsiena.org, answers 403 to `probe url` and loads in `visit.py`).
  Open the home page, and take the parish site from the bulletin's footer or page-1 website line.
- **Sites `probe url` can't reach:** retry in the browser (`visit.py`) before concluding
  anything; don't fake a browser user agent in curl, which the sandbox denies (use `probe url`,
  `probe get` or `visit.py`); parish.stnorbert.org answered "RemoteDisconnected" to `probe url` and loaded in
  Chrome (2026-10-28), holytrinitymorrisville.org answered 403 and loaded in `visit.py`, and
  stmichaellvt.org gave NO-PARISH-WORDS while `visit.py` followed its redirect to
  stmichaellvt.com and showed the jppc template 217 link. A site framed from a Solutio host (stphilspa.com ->
  stphil-lans.solutiosoftware.com) answers 403 to `probe url` and `probe get`; `visit.py` shows
  its "Latest Bulletin" link; presbvm.org (Presentation BVM, Solutio) likewise answered 403 and
  loaded in Chrome, its bulletin page linking the John Patrick template beside a stale
  self-upload archive (March 2024). holynameofjesus-fishtown.org failed certificate verification on
  2026-10-28 (try `http://`, or its John Patrick listing).
- **ParishesOnline / LPi:** a minority publisher here, found in Delaware County (St. Philomena,
  Lansdowne; Blessed Virgin Mary, Darby 04/0756; Our Lady of Perpetual Help, Morton; St. Rose,
  Eddystone 04/0708; St. John Fisher, Boothwyn 03/1236, whose John Patrick listing has no
  editions); LPi also has organizations elsewhere (st-john-the-evangelist-church-19107,
  st-patrick-church-19401). An empty organization ("no publications") exists for many parishes
  whose bulletin is John Patrick's (St. Katharine Drexel, Our Lady of Charity, St. Madeline): it
  is not a publication id.
  Sites built on WeConnect/Duda (bvm-darby.com, olphmorton.org) embed a `publicationWidget`
  whose `id=` is the 18-character LPi id, though `probe url` finds no publication on them. Their
  bulletin page can instead link a fixed-name PDF (St. Rose: `bulletin8.pdf`) whose text equals
  the container's current issue; its footer code ("Name, Town, PA 04-0708") gives the container:
  use the `parishes_online` row. A site with no embed is found with the search API near the
  church (distance=3 gave st-philomena-church):
  `https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=<lat>&longitude=<lon>&distance=6`.
  `probe po <slug or id>` then gives the container. A container's first pages can be images
  (BVM Darby pages 1–3): render page 1 for the Mass box and use the text-layer footer line
  ("Name | 04-0756", page 4) as the tie to the container. A container can post next Sunday's
  file early (St. Philomena 20261101B on 2026-10-28; freshness `future`), as eCatholic does.
  As elsewhere, empty organizations are not fold-ins: read the masthead.
- **J.S. Paluch / Discover Mass:** not seen as a publisher here. A footer "View this bulletin
  online at www.DiscoverMass.com" (St. Joseph, Downingtown's eCatholic issues; St. Joseph,
  Warrington's WordPress ones) does not make it one: each parish's own archive was current. If a row uses it, Discover Mass
  caps downloads per IP per day (a 134-byte "Maximum number of files downloaded today" reply,
  which `fetch:check` reports as `not_pdf`): that is the cap, not the row.
- **archphila.org** answers 503 when read quickly: pause between requests and retry. Its
  relegation decree PDFs are scanned images (`probe pdf` reads no text): render them. Page 2
  gives the effective date, and a decree may state the last Mass (St. Stanislaus Kostka,
  Chester County: none since 2016-07-02; the original St. Philip Neri, East Greenville: "has not
  been used for divine worship of any kind since 1968", relegated 2023-01-23) or when Sunday worship
  was suspended: quote that sentence as the closure source and take `last_mass` from it. The
  effective date is not the last Mass (St. Leo, Tacony: "not been used as a regular church for
  worship since January 1, 2018", effective 2019-01-07; Our Lady of Ransom: not a regular church
  since the 2017 merger, effective 2019-09-03). A decree that gives only a monthly Sunday Mass in
  the church's last year (Incarnation of Our Lord, given 2015-06-08, effective 2015-07-15) bounds
  `last_mass` by the effective month: record that month and say it is an upper bound. The host parish's
  own site can post the decree too, also scanned (Sacred Heart, Clifton Heights has St. Hedwig's).
  A relegated church that is in no roster is found only on the parish-planning page
  (Immaculate Heart of Mary, Chester, effective 2024-03-01): check each batch's closed
  neighbours there for decrees. For news of a church with no decree, CatholicPhilly's WordPress
  REST search (`catholicphilly.com/wp-json/wp/v2/posts?search=<name>&per_page=15&_fields=...`)
  lists its stories and event notices; an event Mass there is not a worship site (rule below).
- **Coordinates, addresses and chapel owners:** Nominatim through `probe get` (`format=jsonv2`,
  `q=<church name> <town>`) returns named OSM place_of_worship nodes, as JSON inside `probe
  get`'s `text` field (`jq '.text|fromjson'`); a bare street address returns only the street,
  though for some Delaware County churches it returns the church. It can file a church under the
  wrong post town (St. John Neumann, Bryn Mawr under Havertown), find it only under the
  township's name (St. Titus under "East Norriton", not Norristown: try both) or find nothing (Our Mother of Good Counsel): fall back to GCatholic's Plus Code. GCatholic's ZIP
  can differ from the bulletin's (St. Gabriel, Avondale: 19350 vs 19311): follow the parish's
  own and leave `address_verified` false. GCatholic's "Mission of:" line names the owner of a
  chapel whose name points elsewhere (Sacre Coeur adoration chapel: St. Denis, not Sacred Heart,
  Havertown). A historic second church named only in the Mass box ("Thursday at old St. John's
  Church", St. John the Baptist, Ottsville) takes its name from the parish history page and can
  take its address from the directory's "Cemetery:" line when the cemetery surrounds it
  (`address_verified` false, a `revisit` for the pin).
  GCatholic's seminary, abbey and chapel entries can describe a campus the community has left
  (St. Charles Borromeo Seminary moved from Overbrook to Lower Gwynedd in August 2024, closing
  the Overbrook chapels): read the institution's own site and CatholicPhilly before assuming
  Mass. GCatholic also lists Ordinariate churches among the archdiocese's (Rite "Anglican
  (Latin)", Jurisdiction "Anglican Personal Ordinariate of The Chair of Saint Peter": 500 Ford
  St., Bridgeport, the former Our Lady of Mount Carmel): read the Jurisdiction line before
  treating a former parish church as a worship site (rule below).
  The directory's and the masthead's street can be the parish office, and GCatholic's can be
  off too (St. Patrick, Malvern: office 131 Channing Ave., church 104 Channing Ave. per its
  site footer and OSM, GCatholic 126 Woodland Ave.): read the site's contact page or footer.
  GCatholic's number can be the parish school's on the same campus (St. Hilary, Rydal: 920
  Susquehanna Rd. is the school in OSM, the church 820 per bulletin, directory and OSM): query
  Nominatim for both numbers. GCatholic's "first recorded" date can belong to an older, closed
  church of the parish (St. Philip Neri, Pennsburg's 1919.10 is the East Greenville church, not
  the 1968 Pennsburg building). A GCatholic id is not a ZIP: `gcatholic:19096` is Presentation
  BVM, Cheltenham (19012), not Presentation BVM, Wynnewood (19096). Aggregators are weak
  evidence for a church's address or status: catholicindex.org is behind Cloudflare, and Church
  Finder (readable with `visit.py`) gave Sacred Heart, Tullytown an address that GCatholic and OSM
  don't. A Ukrainian GCatholic entry can share a Latin church's address, and `coverage --link`
  then attaches it to the Latin church's record, rewriting roster lists on records in other
  batches: run plain `coverage`, or check `git status` afterwards and revert what isn't yours.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin
publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (Ukrainian Archeparchy of Philadelphia, Ruthenian, Syro-Malabar, Syro-Malankara, Maronite, Armenian) are excluded as `other-jurisdiction`, as in every neighbouring diocese. A Latin parish church an Eastern community also uses keeps its own row (St. Albert the Great, Huntingdon Valley, with the Syro-Malabar mission). (accepted by survey-review, 003-survey-review, 2026-10-28)
- **Shared pastors and Parish Life Directors don't make shared bulletins.** A pair or trio named under one pastor or PLD on the directory (14 pairs and the cathedral trio) is one row only when one current bulletin covers each member; compare mastheads and Mass schedules, not contact lines or staff. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A worship site of a merged parish** keeps a church row under the parish whose current bulletin or Mass schedule lists Mass there. The directory's 'Worship site of …' line (on either parish's page) is a lead, not evidence of current Mass, and a closed parish page's 'Formerly located at …' is only its address line. A relegation decree or CatholicPhilly report is the closure source: exclude `closed` with `last_mass` from the bulletin, or the decree's effective date when no bulletin gives it. (accepted by survey-review, 003-survey-review, 2026-10-28) A closed parish page's 'Worship site of X' line is stale once X's own page names no worship site and says only 'Merged with …' (St. George, Glenolden and Holy Spirit, Sharon Hill; St. Gabriel, Norwood and St. Margaret Mary Alacoque, Essington): add no church row from it, and without a closure source leave the church `open`. (map batch `lenni-glenolden`, 2026-10-28) The line can be a decade stale: when X's own site, masthead and Mass page name no other site, look for a decree that ended Sunday Mass there (Sacred Heart, Swedesburg: St. Augustine's decree ended Sunday Mass at St. Augustine and Our Lady of Mount Carmel in January 2015). (map batch `conshohocken-kop`, 2026-10-28) A cover subtitle naming the worship site ("Our Lady of Fatima Worship Site") over the parish's own address is not evidence of Mass there: only a Mass box line naming the place is (St. Charles Borromeo, Bensalem). (map batch `bensalem-croydon`, 2026-10-29) Nor is a patronal subtitle keeping a merged parish's title ("Under the Protection of Our Lady of Ransom", Resurrection of Our Lord), whose church's decree can say regular worship ended at the merger, years before the effective date. (map batch `bustleton-somerton`, 2026-10-29) A single event Mass at an undecided church (a healing Mass at St. Joachim in a CatholicPhilly event notice) is not a worship site: without a Mass box line or a closure source, leave it in `open/`. (map batch `frankford-olney`, 2026-10-29) A closed parish page's "Spiritual records are kept at X", like an aggregator's "Parish-Closed" title (catholicchurch.directory), records the parish ending, not the church's: exclude the church `closed` only on a decree, news story or bulletin that says so. (map batch `holmesburg-tacony`, 2026-10-29)
- **Personal Ordinariate churches** (the Chair of St. Peter) are excluded `other-jurisdiction`, as in Rochester and Scranton, even in a former archdiocesan parish church: St. John the Baptist holds Mass in Our Lady of Mount Carmel, Bridgeport, which is not a Sacred Heart worship site. (map batch `conshohocken-kop`, 2026-10-28)
- **Seminary, monastery, abbey, retreat-house and adoration chapels** (St. Charles Borromeo Seminary and its chapels, the Visitation Monastery, Daylesford Abbey, the St. Carlo Acutis shrine at Malvern Retreat House, the Sacre Coeur adoration chapel) get a church row under a parish when that parish's bulletin lists their public Mass; a parish row of their own if the house publishes a readable bulletin; otherwise they are excluded `no-public-mass` (private or community-only Mass) or `no-bulletin` (public Mass, but no bulletin lists it), following README Settled policy 4. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A campus Mass the parish bulletin lists every week gets a church row** (Villanova's St. Thomas of Villanova church, the Penn Newman Center's St. Bede chapel under St. Agatha-St. James, Temple's Newman chaplaincy), as in Harrisburg; a campus ministry that publishes only by email or semester newsletter is excluded `no-bulletin`. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A shrine in a parish church is that church's row** (the Cathedral and Shrine of St. Katharine Drexel; St. Peter the Apostle and the Neumann Shrine; St. Jude, Chalfont; St. Anne). A shrine in a former parish church is decided like a worship site: a church row under the parish whose bulletin lists its Masses, a parish row of its own when it publishes its own bulletin, or excluded `no-bulletin` when it has public Mass and no bulletin lists it. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **The directory's `group` is the deanery** ('Chester County West'), not a family or cluster:
  leave `group` empty on parish records, since `audit` flags every row sharing a value as a
  possible shared bulletin, and record each parish's `publication_reviews` from the mastheads.
  Roster links go on church records (`diocese write` rejects `roster` on a parish). (map batch
  `west-chester`, 2026-10-28)

- **Church rows follow the Mass schedule box, not the directory.** Read every location the
  parish bulletin's Mass schedule lists: a parish hall or center with a weekly Sunday Mass gets a
  church row (Schneider Parish Center, Parkesburg, 11:15 AM, under Our Lady of Consolation). A
  directory "parish" that is really a parish's own center or mission name, where the bulletin
  puts classes and meetings but no Mass, is excluded `no-public-mass` under that parish
  (Mision Santa Maria, Madre de Dios, Avondale, St. Rocco's "donation center"). (map batches
  `coatesville-parkesburg` and `southern-chester`, 2026-10-28) Likewise an "Adoration Chapel" or "Chapel" in the
  schedule box with devotions but no Mass line is not a church row: check the page-2 weekly
  calendar for a Mass there first (Nativity BVM, St. Mary Magdalen, St. Thomas the Apostle). (map
  batch `media-wallingford`, 2026-10-28) A "Chapel" named in a weekday Mass line (St. Helena,
  Blue Bell's Saint Theresa Chapel) is a room of the church's campus, its Masses on the church's
  row, unless the bulletin or site gives it another address. (map batch `blue-bell-norristown`,
  2026-10-28) A "Saint X Chapel" under the cover's "Daily Adoration" is an adoration chapel, not
  a church row, unless a Mass line names it (St. Frances Cabrini, Fairless Hills: its Saint Joseph
  Chapel is in the Parish Center). A second building's address in the masthead or a footer banner
  (St. Andrew, Newtown's "Olde Church") is a venue, not a church row, unless a Mass box or
  calendar lists Mass there; when the current issue is image-only, search the listing's older
  text-layer issues for it. (map batches `morrisville-fairless-hills` and `newtown-yardley`,
  2026-10-29)
- **A Mass one parish staffs at another parish's church is that church's row only.** It
  appears in both bulletins, but it is not a worship site of the staffing parish (St. Rocco's
  Sunday 2:00 PM Spanish Mass at Sacred Heart, Oxford is on Sacred Heart's church row). (map
  batch `southern-chester`, 2026-10-28)
- **A directory "parish" page with only a rectory address and phone**, no pastor, Mass times or
  website, and a "where all spiritual records are kept" link to another parish, is a former
  parish or worship-site entry, not a bulletin publisher: make no parish row, and decide its
  church as a worship site of the records parish (Sacred Heart of Jesus, Tullytown under St.
  Mark, Bristol, left `open` until a source gives its Mass or closure). Its rectory phone can be
  a neighbouring church's (Tullytown's is the one GCatholic gives St. Ann, Bristol). (map batch
  `bristol-levittown`, 2026-10-29)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-28: Survey (job 001, Run philadelphia-map-1). Rosters: `directory` 218 open parishes,
  `gcatholic` 293 (28 Eastern Catholic), `worship-sites` 29. `batches.json`: 59 batches (57 of
  2–5 parishes, two Eastern Catholic), 540 roster entries, none excluded; `first_batch`
  west-chester. No records yet.
