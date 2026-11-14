---
name: Roman Catholic Archdiocese of Hartford
state: CT
website: https://archdioceseofhartford.org
status: exploring
gcatholic: hart0
---

Three counties of central and western Connecticut: Hartford, New Haven and Litchfield. The
main towns are Hartford, New Haven, Waterbury, New Britain, Bristol, Meriden, West Hartford,
Manchester, Hamden, Milford and Torrington. Neighbours: Norwich (east: Middlesex, Tolland and
the shore east of Madison), Bridgeport (south-west: Fairfield County), Springfield (north:
Massachusetts), the Archdiocese of New York (west: Dutchess County) and Albany (Columbia
County, at the north-west corner). There are no families, clusters or pastorates. Since the
2017 pastoral plan (GCatholic's counts drop from 212 parishes in 2015 to 127 in 2017) and
later mergers (one by decree in March 2026), most towns have one canonical parish with
several worship sites, named "<Parish>: <Church>" in the diocese's finder (Blessed
Michael McGivney, New Haven has eight churches; St. Francis of Assisi, New Britain five). One
merged parish usually means one bulletin. The likely shared bulletins across parishes are where
one priest is pastor of two parishes (four pairs, see *Sources*) or where a quasi-parish shares
a parish's site. The finder lists 167 worship sites in about 93 parishes, quasi-parishes,
missions, a shrine and an oratory. GCatholic lists 229 churches, about 55 of them not in the
finder: mostly churches closed or merged away, plus eleven Eastern Catholic churches.

## Sources

- **Parish finder (directory roster):** https://archdioceseofhartford.org/parishes/, read
  2026-11-13. One WordPress page (diocesanweb "dpi_gis" map) carrying every worship site in
  `data-*` attributes: name, address, coordinates, email, phone, website and a Mass schedule.
  Scraped with `scratch/hartford-map-1/tools/hartford_directory.py` into
  `rosters/directory.json` (167 entries). `group` is the parish name before the colon, so it is
  the canonical parish, which is the grouping most likely to share a bulletin.
  - Good for: the current canonical structure (names reflect the recent mergers and renamings), addresses,
    coordinates.
  - **It lists churches relegated by decree:** Immaculate Conception, Southington (relegation
    decree 27 Oct 2025) is still St. Luke Parish's fourth church.
  - **Website links are often old domains:** Assumption and Holy Rosary, Ansonia redirect to
    olvansonia.org; Incarnation and Christ the King to wethersfieldcatholic.org; St. Therese,
    Granby to stpgranby.org; middsouthcatholic.org to carloacutisct.org; St. Peter Claver to
    .org. Dead or blocked at survey: smsgparish.org/stgregory/ (404), bscwaterbury.com,
    holytrinityhartford.org, sscyrilmethodiushartford.org/en (404), stjoachimct.org (403).
    St. Francis Xavier, New Milford's website field is an email address. Our Lady of Fatima,
    Hartford's only link is a Facebook group.
  - Spelling slips in parish names (North America Martyrs, St. Franics, St. Pio of Peitrelcina,
    St. Maximilan Kolbe) are normalised in `group` by the scraper.
  - The Mass schedule (`mass_times`) is the diocese's own; how stale it is is unchecked.
- **GCatholic:** `rosters/gcatholic.json`, key `hart0`, 229 entries, fetched 2026-11-13.
  - **It is pre-merger:** it lists about 45 Roman churches the finder doesn't (closed, merged
    or relegated, e.g. St. Rose and Our Lady of Peace, East Hartford, both relegated by decree;
    Sacred Heart, St. Peter, St. Luke, St. Lawrence O'Toole and St. Anne–Immaculate Conception,
    Hartford; St. Lucy, St. Margaret, St. Joseph, SS. Peter and Paul, St. Stanislaus Kostka,
    Waterbury). Absence from the finder is a lead, not a closure.
  - **It omits the cathedral** (Cathedral of St. Joseph, Hartford).
  - **Eleven Eastern Catholic churches** carry a `rite`: Ukrainian (Ansonia, Glastonbury,
    Hartford, New Britain, New Haven, Terryville), Ruthenian (Meriden, New Britain), Maronite
    (Torrington, Waterbury), Syro-Malabar (Hartford).
  - Non-parish entries: the Abbey of Regina Laudis (Bethlehem), the Dominican monastery (North
    Guilford), the Legion of Christ college (Cheshire), the Knights of Columbus Museum (New
    Haven), the Lourdes shrine (Litchfield).
- **Clergy directory:** https://archdioceseofhartford.org/clergy-staff-directory/, read
  2026-11-13 (83 pastors and administrators). It names each priest's office. Explicit
  shared pastors, as the source words them:
  - "Pastor, St. Francis Xavier Parish, New Milford & Our Lady of Perpetual Help Parish,
    Washington Depot" (Rev. Carlos A. Castrillon).
  - "Pastor, St. Martin of Tours Parish, Canaan & St. Joseph Parish, Winsted" (Rev. Bruce
    Czapla, O.F.M.).
  - "Pastor, Mary, Mother of the Church Parish, Waterbury & St. Basil the Great Parish,
    Wolcott" (Msgr. Thomas M. Ginty).
  - "Pastor, St. Francis of Assisi Parish, Naugatuck & St. Vincent Ferrer Parish, Naugatuck"
    (Rev. John Kuzhikottayil, S.D.B.).
  - It also names "St. Matthew and St. Gregory the Great Parish, Forestville": the finder's
    St. Matthew (Forestville) and St. Gregory the Great (Bristol) are listed as two parishes but
    the clergy list treats them as one.
- **Families / clusters:** none. The canonical parishes in the finder are the grouping.
- **Decrees (Public Notices):** https://archdioceseofhartford.org/category/news/public-notices/
  (also the WordPress API, `/wp-json/wp/v2/posts?search=decree`). Read 2026-11-13: relegation
  of Immaculate Conception, Southington and of St. Rose, East Hartford (both 27 Oct 2025);
  merger of St. Ambrose (North Branford/Northford) and St. Elizabeth of the Trinity (North
  Haven), 22 Mar 2026 (now St. Pier Giorgio Frassati); relegation of Our Lady of Peace, East
  Hartford, 11 Apr 2026; name change of the Middlebury–Southbury parish (to St. Carlo Acutis),
  effective 29 Aug 2026. The current site starts in 2025: the 2017 pastoral plan's decrees are
  not on it.
- **Closed parishes and where their records went:** not found on the current site.
- **Pastoral plan:** the 2017 plan (212 to 127 parishes by GCatholic's yearly counts) and the later merger rounds have no
  page on the current site. The Catholic Transcript (catholictranscript.org) covered them; not
  read.

### Bulletin publishers here

From `probe url` of all 98 sites the finder links (2026-11-13):

- **Most parish sites are diocese-built WordPress (diocesanweb.org, "beacon"):** 77 of 98.
  The bulletin is on a `/bulletins/` (sometimes `/bulletin/` or `/weekly-bulletin/`) page.
  Either a PDF uploaded to `cdn.diocesanweb.org/beacon/<site>/wp-content/uploads/<YYYY>/<MM>/`
  (St. Ann, Avon: `2026/11/November-15-2026.pdf`; St. Jeanne Jugan: `20261115B.pdf`) or a
  ParishesOnline publication widget (McGivney's `publicationWidget?type=bulletin&id=...`).
  File names vary by parish. Other diocesanweb PDFs on the same host are forms and notices,
  not bulletins.
- **ParishesOnline (LPi)** appears on 32 sites, often as an org link beside a self-uploaded PDF.
  Org slugs found: see `scratch/hartford-map-1/001-survey/probe-all.tsv`. Some org names are
  older than the parish: St. Junipero Serra's is `st-margaret-mary-church-06074`; North
  American Martyrs' is `...-st-marys-and-st-rose-churches`, also linked from the St. Isaac
  Jogues quasi-parish's page; Mary, Mother of the Church and St. Basil both link
  `st-basil-the-great-mary-mother-of-the-church-st-leo`.
- **Others seen once or twice:** church-bulletin.org / jppc.net (St. Francis of Assisi,
  Naugatuck; Our Lady of Mercy, Plainville), bonventure.net (St. Thomas and St. Timothy; St.
  Joseph, Bristol), eCatholic (St. Paul, Kensington), Discover Mass (St. Peter Claver), Wix or
  similar (nbcatholics.org, stelizabethofthetrinity.org).
- **Needs a real browser** (`probe url` said NO-PARISH-WORDS or 4xx): stmatthewrcc.com,
  saintvincentferrerchurch.org, ourlady-stpatrick.org, olsparishchurch.org, stjoachimct.org.
- From the neighbours: Albany found image-only ParishesOnline bulletins common (about one in
  five), and one bulletin printed into two LPi containers with only the ad page differing.
  Wix and Weebly file hosts answer 429 to rapid `probe pdf`; space the requests.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- 'Branches on the Vine' PDFs (Branches*.pdf) on diocesanweb parish sites are the archdiocese's weekly news, not a parish bulletin; when a bulletins page mixes them in, pin page-pdfs with a filename glob for the parish's own files (e.g. filename=Bulletin-*.pdf).
- diocesanweb 'current-bulletin' and yearly-archive pages also link forms (cemetery rules, sponsor certificates); unfiltered page-pdfs can pick one as first-listed, so check the pick and pin the page plus a filename glob.
- For churches the 2017 pastoral plan closed with no decree, html.duckduckgo.com/html/?q=... via probe get finds local reports (Hartford Courant June 2017 'final regular Mass' articles, the Suffield Observer) that date the last Mass.
- bonventure.net (sponsors.bonventure.net/?page=<id>, PDFs at pdfs/<id>/<YYYY-MM-DD>.pdf): page-pdfs resolves the current issue but the https download fails certificate verification (incomplete chain); probe get works over http. Record bulletin_provider unsupported with fetch_gap kind tls-certificate-unverified.
- diocesanweb sites linking church-bulletin.org/?id=<n>: unpinned fetch:check prints recipe linked-issue-page and picks church-bulletin.org/bulletin/<slug>/<date>.pdf, which can be scanned while the parish's own diocesanweb upload of the same issue has text; compare before pinning.
- render.py's browser closes on very large scanned LPi PDFs (~90 MB); download with probe get --out into an empty folder and render with pdftoppm -f 1 -l 1 -r 80 -jpeg instead.
- A diocesanweb bulletins page can be stale or empty while the parish's ParishesOnline org is live and unlinked: try probe po with guessed org slugs (<name>-parish, <name>-<zip>) before calling a bulletin not found.
- Hartford Courant 7 May 2017 'list-of-parish-closures-and-mergers-by-town' gives the 2017 plan for every town. It is a plan, not proof, so pair it with a dated report found by searching html.duckduckgo.com for 'courant.com <church> final Mass'.
- A guessed ParishesOnline slug can belong to a same-named parish elsewhere (st-marianne-cope-parish is Solvay, NY); check the org address from probe po before using it.
- diocesanweb mastheads laid out in church columns come out interleaved from probe pdf; download with probe get --out and read page 1 with pdftotext -layout to tie each Mass time to its church.
- When the parish finder's link for a quasi-parish or ethnic community points into another parish's site, it may be an old history page: search html.duckduckgo.com for the community's own domain (East Hartford's Ghanaian quasi-parish has its own diocesanweb site) before treating it as covered by that parish's bulletin.
- diocesanweb parish history pages (/<church>-church/) can date a church's closure years before its relegation decree; record that as last_mass and cite the decree as well. Archdiocesan decrees and 'Bulletin Blurb' notices are scanned images or PDFs, so render them to read the effective date.
- pnpm diocese probe get --out resolves a relative path from the repository root, not the shell's directory: always pass an absolute path inside the scratch folder.
- diocesanweb sites that upload <YYYYMMDD>B.pdf files are hosting LPi bulletins: grep the ad pages for '4lpi.com' to get the container (e.g. 'St. Paul, Kensington, CT 03-0062'), then probe po a guessed org slug (<name>-church-<zip>) and record parishes_online rather than page-pdfs.
- Solutio (Joomla) sites (/bulletin/<n>-<title>/file, 403 to probes) open in visit.py with --screenshot of the /file link, which shows page 1 in Chrome's PDF viewer for the masthead; record them unsupported with gap joomla-file-endpoint.
- To date when a church's Mass ended, run probe container <a/b> --from <date> --weeks 160 --step 8 --all --pages 1 and look for where it leaves the schedule, then narrow the gap with --weeks 8 --all --pages 3 to find the announcement.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- A church relegated to profane use by a published archdiocesan decree is excluded as closed, dated to the decree unless a bulletin gives the last Mass, even if the parish finder or GCatholic still lists it; check the parish's current bulletin first for a continuing Mass there. (accepted by survey-review, 002-survey-review, 2026-11-13)
- A shared pastor named in the clergy directory puts the two parishes in one batch and in a shared audit group, but makes one row only if a current bulletin covers both (as Albany settled). (accepted by survey-review, 002-survey-review, 2026-11-13)
- The eleven Eastern Catholic churches GCatholic lists (rite set) are other-jurisdiction exclusions (Stamford Ukrainian, Passaic Ruthenian, St. Maron of Brooklyn, St. Thomas Syro-Malabar of Chicago). (accepted by survey-review, 002-survey-review, 2026-11-13)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-13: Survey (factory run hartford-map-1). Rosters: directory 167, gcatholic 229.
  Batch plan in `batches.json`: 17 batches, `north-suburbs` first. No parish records yet.
