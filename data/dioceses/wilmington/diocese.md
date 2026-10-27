---
name: Roman Catholic Diocese of Wilmington
state: DE
website: https://cdow.org
status: exploring
gcatholic: wilm0
city_aliases:
  St Michaels: St. Michaels
  Kent Island: Chester
  Ocean Pines: Berlin
  Oak Orchard: Millsboro
  Golden Hill: Church Creek
---

All of Delaware (New Castle, Kent and Sussex counties: Wilmington, Newark, New Castle,
Middletown, Dover, Milford, Georgetown, Seaford and the beaches at Lewes, Rehoboth and Bethany)
and the nine counties of Maryland's Eastern Shore (Cecil, Kent, Queen Anne's, Talbot,
Caroline, Dorchester, Wicomico, Somerset and Worcester: Elkton, Chestertown, Easton,
Cambridge, Salisbury, Ocean City). Neighbours: Philadelphia across the Pennsylvania line,
Harrisburg (Lancaster County borders Cecil County), Baltimore across the Susquehanna and the
Bay, Camden across the Delaware, and Richmond on Virginia's Eastern Shore; of these only
Harrisburg is mapped. The state here is `DE`, but 34 of the directory's 79 entries are in
Maryland.

The diocese has **no families, clusters or pastorates**. Its 56 parishes (cdow.org/deaneries,
modified 2026-05-26) sit in six deaneries (City, Brandywine Hundred, New Castle, Iron Hill,
Central, Ocean); since Easter 2026 the "United in Christ" plan works through the deaneries on
shared programmes and Mass schedules, not mergers. Shared bulletins are likely in three
places: a parish with **missions** (most Eastern Shore parishes, and St. Joseph, Middletown;
the summer guide names each "mission of ..."); parishes the diocese names together
("Saint Michael the Archangel/Mary Mother of Peace", "St. Mary & Holy Savior Parish", "St
Francis de Sales & Holy Redeemer parish"; the three **Downtown Catholic** parishes in
Wilmington, "individual parishes administered by the one pastoral team"); and a few pairs
under **one pastor** named in the clergy appointments (below). `batches.json` keeps each of
these in one batch.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (the `directory` roster):** cdow.org's "Find A Parish" map,
  https://cdow.org/find-a-parish/, a WordPress "dpi_gis" plugin page that carries every
  entry in the HTML as `<li data-module="parishes" data-name data-address data-latitude
  data-website data-mass-times ...>` (no API call; plain curl with a browser user agent).
  Scraped 2026-10-27 by `scratch/wilmington-map-1/tools/cdow_finder.py`: 79 entries (the page
  also holds 33 schools and 4 jobs, skipped). It lists **churches**, not parishes: missions
  are entries of their own with the parent's website, and some names carry the parish
  ("Holy Savior. St. Mary & Holy Savior Parish"). Good for building pins (all within about
  0.2 km of GCatholic's except the three noted below), Mass times (`mass_times`, decoded
  from the map; Sunday = day 0), and the current parish website. Quirks: St. Francis de
  Sales, Salisbury is in twice (`directory:184`, 413 Wicomico St, no Masses; `directory:175`,
  535 Riverside Dr); the map's own deanery ids are all 0, so `deanery` is joined from the
  deaneries page by name and town. Some websites are wrong: Holy Cross, Dover's is a spam
  page (sub.ireland724.info); Middletown's, St. Mary of the Immaculate Conception's and
  Cambridge's are catholicmasses.org listings, Berlin's a catholicindex.org listing, St. Jude,
  North East's a county churches page, and Corpus Christi's is St. Matthew's site. The
  cathedral, Dover AFB and the two Ukrainian churches are listed; Christ Our King, Our Lady
  of the Highways and St. Joseph's former Middletown church are not.
- **Deaneries:** https://cdow.org/deaneries/ (modified 2026-05-26) names 56 parishes, one
  line each ("Saint Michael the Archangel/Mary Mother of Peace, Georgetown, DE"), in six
  deaneries; this is the diocese's own parish count. All 56 match a directory entry; the 23
  directory entries it doesn't name are missions, the two Ukrainian churches and Dover AFB.
  **Disagreement:** Bishop Koenig's "United in Christ" update (The Dialog, 2026-03-26,
  https://thedialog.org/featured/bishop-koenigs-united-in-christ-update-going-beyond-pre-established-boundaries-experimenting-with-joint-pastoral-initiatives/)
  announces the six-deanery realignment "effective Easter Sunday, April 5, 2026" and lists
  the City Deanery as eight parishes, **without St. Mary of the Immaculate Conception and
  St. Patrick**, which the later deaneries page still lists. Nothing found yet says either
  was merged or suppressed; the downtown batch checks.
- **GCatholic:** `rosters/gcatholic.json` (key `wilm0`), 80 entries with Plus Codes for 77.
  Omits the cathedral; keeps Christ Our King, Wilmington (closed November 2016, now a funeral
  home: The Dialog, 2020-07-30), St. Joseph's former church at 15 W Cochran St., Middletown
  (typed "Former Church") and Our Lady of the Highways, Childs (a shrine). Marks St. Nicholas,
  Wilmington and St. Basil the Great, Chesapeake City "Ukrainian"; lists Our Lady of Perpetual
  Help, Dover AFB as a "Community". **Three Plus Codes are rotated:** its Corpus Christi
  (19322) is on Holy Child, Naamans Rd; its Holy Family (19323) on Corpus Christi, Elsmere;
  its Holy Child (19321) on Holy Family, Newark. Use the directory pin or OSM for these, and
  check Our Lady of Guadalupe, Frankford, whose two pins are about 24 km apart. Many of its
  websites are old domains: of the 73 entries with one, probed 2026-10-27, 42 answered; six
  domains have no DNS (holycrossnet.org, stjohn-stbernadette.org, stmaryscambridge.org,
  stpetertheapostlede.org, immaculateconceptionmarydel.com, mosstp.org); stannsbethany.org,
  stmaryoftheassumption.com, stmarys-holysavior.com, iccparish.org and smspwilmington.com
  didn't answer, the last redirecting to a web-design firm on a first try;
  ccparishwilmington.org is a parked "/lander"; stjudeslewesde.org redirects to an unrelated
  site. Prefer the directory's websites. GCatholic's town names match the directory's except
  Corpus Christi (GCatholic and the deaneries page: Elsmere; directory: Wilmington); the
  deaneries page also puts St. Joseph on the Brandywine in Wilmington, the others in
  Greenville.
- **Mass times (the `summer-guide` roster):** "Summer Vacation Mass Guide",
  https://cdow.org/find-a-parish/summer-vacation-mass-guide/ ("Mass time information is up
  to date as of May 12, 2026"), the coastal and Eastern Shore churches only: 32 churches
  plus two summer-only Mass sites of St. Edmond, Rehoboth (its Parish Hall, and Rehoboth
  Elementary School), 34 entries. The best source here for **which parish a mission belongs
  to**: "St. Rose of Lima (mission of St. Joseph, Middletown, DE)", "St. Andrew (seasonal
  mission of St. Luke – open May 23 – Sept. 6)", "St. Mary Star of the Sea (the Tubman
  Chapel) (mission of St. Mary Refuge of Sinners, Cambridge)"; `group` holds that parent.
  It also says St. Peter, Queenstown was "Reopening July 4, 2026 following renovation".
  Weekend times are summer's. Parsed by `scratch/wilmington-map-1/tools/summer_guide.py`.
  The finder's `mass_times` are the only year-round diocesan Mass times; there is no other
  Mass-times list.
- **Clusters / families of parishes:** none. **Shared pastors** come from the clergy
  appointments The Dialog publishes (search titles with
  `thedialog.org/wp-json/wp/v2/posts?search=appointments&search_columns=post_title`; read
  with `tools/dialog_post.py`). Explicit current pairs: St. Ann and St. Thomas the Apostle,
  Wilmington ("Pastor both of St. Ann, Wilmington and of St. Thomas the Apostle",
  2026-04-27); Holy Child and St. Helena (pastor from 14 January 2026, 2025-12-01); St. John
  the Beloved and St. Catherine of Siena (pastor from 3 September 2025, 2025-08-14);
  Immaculate Conception, Elkton and St. Thomas More Oratory ("Pastor of both", 2024-05-19);
  St. Polycarp, Smyrna and St. Dennis, Galena (2024-05-19). Shared associates: St. Matthew
  and Corpus Christi (December 2025), Holy Cross, Dover and Immaculate Conception, Marydel
  (2024–2025), Holy Family and Resurrection (June 2024). Ended: St. Thomas's pastor
  administered St. Mary Magdalen (October 2025 – April 2026); St. Benedict's administered St.
  Christopher (November 2025 – April 2026); St. Joseph on the Brandywine's administered St.
  Ann (from July 2025). The appointments say who serves where, never what a bulletin covers.
- **Closed parishes and where their records went:** no diocesan list found
  (cdow.org has a "Marriages and Baptisms Archives" page of news, not a records index).
  Closures are dated from The Dialog (thedialog.org, WordPress, readable with curl and its
  REST API; its `search` matches loosely, so add `search_columns=post_title`).
- **Pastoral plan:** "United in Christ" (pastoral letter 2023-05-19; updates 2024-05-22,
  2024-08-01, 2026-03-26), deanery-level collaboration; the Brandywine Hundred dean wrote
  that "it is not about closure – but about vibrancy" (2024-01-08). Its 2026 phase is "a
  diocesan-deanery coordination of Mass schedules", decisions to follow, so expect Mass
  times to change during 2026–27. Nothing in it closes or merges a parish.
- **Other jurisdictions in the territory:** St. Nicholas, Wilmington and St. Basil the Great,
  Chesapeake City (Ukrainian Catholic); Our Lady of Perpetual Help, the Dover Air Force Base
  chapel (436th Airlift Wing chaplaincy). All three are in the directory.

### Bulletin publishers here

From `probe url` on every roster website and the browser on 38 of them (2026-10-27); each
batch settles its own rows.

- **John Patrick Publishing** prints a good share of New Castle County and the upper shore:
  parish sites link `jppc.net/onlinebulletins/<id>template.pdf`, which redirects to a
  `church-bulletin.org/<slug>` listing of dated PDFs (Downtown Catholic 309, St. Joseph,
  Middletown 319, St. Polycarp 301, St. Margaret of Scotland 306; listings for St. Helena,
  Our Lady of Fatima 304 and St. Dennis 732). Harrisburg and Allentown read these with a
  pinned `page-pdfs` recipe; church-bulletin.org answers 406 to a bare "Mozilla/5.0" user
  agent, and plain curl works.
- **LPi / ParishesOnline** prints most of the Ocean Deanery (containers `04/xxxx`: St.
  Edmond 04/0887, St. Luke 04/0763, St. Mary & Holy Savior 04/0790, St. Mary, Cambridge
  04/0661, St. Michael/Mary Mother of Peace 04/0868, St. Jude, Lewes) and several in the
  north (Holy Child, IHM, St. John the Beloved, St. Catherine of Siena, Holy Spirit/St.
  Peter, St. Matthew/Corpus Christi, Our Mother of Sorrows/St. Peter, St. Joseph on the
  Brandywine). ParishesOnline org names that join two parishes
  (`holy-spirit-st-peter-the-apostle`, `st-matthew-parish-and-corpus-christi`,
  `our-mother-of-sorrows-st-peter-the-apostle`) are leads, not proof: read the masthead.
- **eCatholic:** about 14 sites (Resurrection, St. Margaret, Seton, St. Mary of the
  Assumption, St. Mary Magdalen, St. Ann, St. Elizabeth, St. Paul, St. Joseph on the
  Brandywine, Good Shepherd, Sacred Heart, St. Christopher, beparish.com, Our Mother of
  Sorrows). Unlike Harrisburg's, most answered plain `probe url` here; resurrectionde.org
  gave HTTP 4xx and needed the browser. `issues.py ecatholic` reads the files without one.
- **J.S. Paluch on Discover Mass:** St. Ann, Bethany Beach (`discovermass:st-ann-bethany-beach-de`)
  and a lead for Holy Cross, Dover (`holy-cross-dover-de`). Discover Mass caps downloads per
  IP per day (a 134-byte "Maximum number of files downloaded today" reply, which
  `fetch:check` reports as `not_pdf`): that is the cap, not the row.
- **FATA Online** (`fataonline.com/bulletins/<code>`): Good Shepherd, Perryville links
  `GoodShepherdPerryville`. Plain curl works (Harrisburg).
- **Self-hosted:** Holy Family, Newark (`bulletin.php`), Immaculate Conception, Elkton and
  Marydel, St. Anthony of Padua (`/bulletin-archive/`), St. Hedwig and St. Edmond (Duda),
  Our Lady of Lourdes, Seaford (GoDaddy), St. John, Milford (Wix), St. John Neumann
  (weconnect), Our Lady of Good Counsel, St. Paul, Delaware City.
- **Sites that didn't load in the browser either (2026-10-27):** visitstfrancis.org (St.
  Francis de Sales, Salisbury), stjosephfrenchst.org (St. Joseph, Wilmington),
  stpatschapel.org (Conowingo) and iccparish.org (old Elkton domain). Try again later, then
  look for the bulletin on a publisher (see the parish-site-access skill).

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- A shared pastor does not mean a shared bulletin: Holy Child (LPi 03/1109) and St. Helena (church-bulletin.org) both list Rev. Michael Carrier as pastor but publish separately.
- IHM's LPi cover prints a Mass-time box for six deanery parishes; it is a deanery schedule, not a shared masthead, so read page 2 or later for the staff list.
- OSV/Duda parish sites (hrparish.com) hide the bulletin link from probe url; visit.py --links shows 'Bulletin' going to sponsors.bonventure.net/?page=<n>. Bonventure PDFs are at /pdfs/<n>/<date>.pdf.
- sponsors.bonventure.net fails TLS verification from Python (probe pdf, recheck) but loads in Chrome; use the http:// form in recipes and evidence urls, and tools/browser_download.py to read a PDF.
- church-bulletin.org 406s a bare 'Mozilla/5.0' agent; a full Chrome-style user agent works with curl.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (St. Nicholas, Wilmington and St. Basil the Great, Chesapeake City, both Ukrainian) are excluded as `other-jurisdiction`, as in every other diocese here. (accepted by survey-review, 002-survey-review, 2026-10-27)
- **Shared pastors don't make shared bulletins.** A pair under one pastor (St. Ann and St. Thomas the Apostle; Holy Child and St. Helena; St. John the Beloved and St. Catherine of Siena; St. Polycarp and St. Dennis; Immaculate Conception, Elkton and St. Thomas More Oratory) is one row only when one current bulletin covers both. (accepted by survey-review, 002-survey-review, 2026-10-27)
- **A seasonal worship site keeps its church row** with a dated `revisit` for its next season: St. Andrew, Ocean City ('seasonal mission of St. Luke – open May 23 – Sept. 6'), St. Mary Star of the Sea, Church Creek ('Memorial Day weekend through late September'), and St. Mary Star of the Sea, Ocean City if its Sunday Mass is summer-only. (accepted by survey-review, 002-survey-review, 2026-10-27)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-27: Initialised (factory survey, Run wilmington-map-1). Rosters: GCatholic (80
  entries), the cdow.org parish map as `directory` (79), the Summer Vacation Mass Guide as
  `summer-guide` (34). Planned 19 map batches in `batches.json` (193 entries, none excluded).
  No records yet.
