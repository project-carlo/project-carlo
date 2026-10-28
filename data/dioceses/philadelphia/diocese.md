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
  directory parish: 167 (Old St. Mary's, below), 286 "Saint Miriam Parish & School", Flourtown,
  and 241 "The National Shrine of Saint Rita of Cascia" (19146), which publishes its own issue. It is
  a lead, not a match: confirm the listing's name and the cover. Listings outlive their parish's
  move to another publisher (76 of the 269 have no edition at all; 12 directory parishes match
  only such a listing, e.g. St. Bartholomew 73, St. Charles Borromeo 130 and 287, St. John
  Fisher, St. Barbara, St. Cyprian, St. William), and a listing's
  name can join two parishes (116, "The Roman Catholic Church of Saint Timothy and Saint
  Bartholomew") or keep a relegated church (167, "Old Saint Mary Church & Holy Trinity Church").
  Record the row as `other` with `page-pdfs https://www.church-bulletin.org/<slug>`, as
  Allentown, Harrisburg and Wilmington do. Never guess a slug: a wrong one returns the generic
  home page with HTTP 200. church-bulletin.org answers 406 to a bare "Mozilla/5.0" user agent;
  plain curl works. In Wilmington many covers were scanned images: render page 1 with
  parish-site-access `render.py` to read the masthead.
- **eCatholic:** several sites (St. Anselm 24649, St. Genevieve 38659, St. Christopher 16547,
  St. Anne 34036, St. Anastasia 12297, St. Barbara 21577, St. Francis de Sales, Lenni 2405)
  answered plain `probe url` on 2026-10-28, but most link a John Patrick listing rather than
  hosting the bulletin: an eCatholic id alone is not the publication. A home page's first PDF can
  be a flyer (St. Anselm's "St. Lukes Open Flyer").
- **Self-hosted:** Squarespace (St. Augustine: `/bulletins`, files
  `/s/210-Bulletin_October-25-2026.pdf`), Wix (`/_files/ugd/<hash>.pdf`: St. Dorothy, St. Francis
  of Assisi, Norristown, Epiphany, Plymouth Meeting, which also links John Patrick 091), WordPress
  bulletin pages (St. Denis `/bulletinandworshipaids/`, St. Hilary, St. Andrew, Drexel Hill,
  Holy Innocents, St. Dominic). St. Bernard's site is a bare Wix page (stbernard-mayfair.wixsite.com).
- **A shared WordPress host that answered HTTP 500 to everyone:** saintfrancescabrini.net,
  annunciationbvmchurch.org, sainthelenaparish.net, scbdh.org and epiphanychurch.church all
  resolve to 69.16.220.73 (nginx) and gave 500 to `probe url` and to Chrome on 2026-10-28. Try
  again later; meanwhile find their John Patrick listings (St. Charles Borromeo, Drexel Hill is
  220, Annunciation BVM 127).
- **TLS:** holynameofjesus-fishtown.org failed certificate verification on 2026-10-28 (try
  `http://`, or its John Patrick listing).
- **ParishesOnline / LPi:** not seen on the sampled sites, but LPi has organizations here
  (st-john-the-evangelist-church-19107, st-patrick-church-19401). Its search API lists
  organizations near a point:
  `https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=<lat>&longitude=<lon>&distance=6`.
  As elsewhere, empty organizations are not fold-ins: read the masthead.
- **J.S. Paluch / Discover Mass:** not seen on the sampled sites. If a row uses it, Discover Mass
  caps downloads per IP per day (a 134-byte "Maximum number of files downloaded today" reply,
  which `fetch:check` reports as `not_pdf`): that is the cap, not the row.
- **archphila.org** answers 503 when read quickly: pause between requests and retry.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin
publishers here* and *Rules settled*. Every map job reads them.

- A parish's own eCatholic /bulletins page links files.ecatholic.com/<site id>/bulletins/<yyyymmdd>.pdf; where the parish also has a John Patrick listing the two PDFs are byte-identical (St. Agnes, SS. Peter and Paul), so use the `ecatholic` row and record the JPPC listing as a second publication id.
- A John Patrick listing with no editions (a daily-readings page only, e.g. St. Maximilian Kolbe 124) means the parish publishes elsewhere: check its own eCatholic /bulletins archive. Conversely an eCatholic archive that stops (SS. Simon and Jude, last 2025-02-16) means the JPPC listing is the current channel.
- John Patrick PDFs here have no text layer (probe pdf shows 0 readable pages): render page 1 (and page 2 for the Mass schedule) with parish-site-access render.py to read the masthead; fetch:check then reports publication_identity 'unverified' by design.
- Plain curl of an eCatholic /bulletins page gets a Cloudflare 'Just a moment' stub; `probe get <url> --out file` returns the full page with the PDF links.
- The directory's `group` ('Chester County West') is the deanery, not a family; `audit` flags every row sharing it, so record separate peer reviews from the mastheads and leave `group` empty. `diocese write` rejects `roster` on a parish record; roster links live on church records.
- A parish whose eCatholic files sit under /documents/ rather than /bulletins/ (St. Ann, Phoenixville) makes the `ecatholic` resolver pick a stale issue (2016); use an `other` row with `page-pdfs` on its byte-identical John Patrick listing and keep the ecatholic id in `publication`.
- A Squarespace bulletin page whose issue links end in `/file` (St. Mary of the Assumption, Phoenixville; HTTP 403 to probe url/get, readable with visit.py) gives `page-pdfs` no .pdf links; read the parish's John Patrick listing instead.
- A parish site's 'Current Bulletin' image can link jppc.net/onlinebulletins/<id>template.pdf (St. Basil, Kimberton): the listing id is the current channel even when the site's own archive stopped a year earlier.
- Nominatim via `probe get` (format=jsonv2, q=<church name> <town>) returns OSM place_of_worship nodes with names for coordinates; a bare street address returns only a street.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (Ukrainian Archeparchy of Philadelphia, Ruthenian, Syro-Malabar, Syro-Malankara, Maronite, Armenian) are excluded as `other-jurisdiction`, as in every neighbouring diocese. A Latin parish church an Eastern community also uses keeps its own row (St. Albert the Great, Huntingdon Valley, with the Syro-Malabar mission). (accepted by survey-review, 003-survey-review, 2026-10-28)
- **Shared pastors and Parish Life Directors don't make shared bulletins.** A pair or trio named under one pastor or PLD on the directory (14 pairs and the cathedral trio) is one row only when one current bulletin covers each member; compare mastheads and Mass schedules, not contact lines or staff. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A worship site of a merged parish** keeps a church row under the parish whose current bulletin or Mass schedule lists Mass there. The directory's 'Worship site of …' line (on either parish's page) is a lead, not evidence of current Mass, and a closed parish page's 'Formerly located at …' is only its address line. A relegation decree or CatholicPhilly report is the closure source: exclude `closed` with `last_mass` from the bulletin, or the decree's effective date when no bulletin gives it. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **Seminary, monastery, abbey, retreat-house and adoration chapels** (St. Charles Borromeo Seminary and its chapels, the Visitation Monastery, Daylesford Abbey, the St. Carlo Acutis shrine at Malvern Retreat House, the Sacre Coeur adoration chapel) get a church row under a parish when that parish's bulletin lists their public Mass; a parish row of their own if the house publishes a readable bulletin; otherwise they are excluded `no-public-mass` (private or community-only Mass) or `no-bulletin` (public Mass, but no bulletin lists it), following README Settled policy 4. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A campus Mass the parish bulletin lists every week gets a church row** (Villanova's St. Thomas of Villanova church, the Penn Newman Center's St. Bede chapel under St. Agatha-St. James, Temple's Newman chaplaincy), as in Harrisburg; a campus ministry that publishes only by email or semester newsletter is excluded `no-bulletin`. (accepted by survey-review, 003-survey-review, 2026-10-28)
- **A shrine in a parish church is that church's row** (the Cathedral and Shrine of St. Katharine Drexel; St. Peter the Apostle and the Neumann Shrine; St. Jude, Chalfont; St. Anne). A shrine in a former parish church is decided like a worship site: a church row under the parish whose bulletin lists its Masses, a parish row of its own when it publishes its own bulletin, or excluded `no-bulletin` when it has public Mass and no bulletin lists it. (accepted by survey-review, 003-survey-review, 2026-10-28)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-28: Survey (job 001, Run philadelphia-map-1). Rosters: `directory` 218 open parishes,
  `gcatholic` 293 (28 Eastern Catholic), `worship-sites` 29. `batches.json`: 59 batches (57 of
  2–5 parishes, two Eastern Catholic), 540 roster entries, none excluded; `first_batch`
  west-chester. No records yet.
