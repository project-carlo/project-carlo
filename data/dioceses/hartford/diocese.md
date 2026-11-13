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

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- A church relegated to profane use by a published archdiocesan decree is excluded as closed, dated to the decree unless a bulletin gives the last Mass, even if the parish finder or GCatholic still lists it; check the parish's current bulletin first for a continuing Mass there. (accepted by survey-review, 002-survey-review, 2026-11-13)
- A shared pastor named in the clergy directory puts the two parishes in one batch and in a shared audit group, but makes one row only if a current bulletin covers both (as Albany settled). (accepted by survey-review, 002-survey-review, 2026-11-13)
- The eleven Eastern Catholic churches GCatholic lists (rite set) are other-jurisdiction exclusions (Stamford Ukrainian, Passaic Ruthenian, St. Maron of Brooklyn, St. Thomas Syro-Malabar of Chicago). (accepted by survey-review, 002-survey-review, 2026-11-13)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-13: Survey (factory run hartford-map-1). Rosters: directory 167, gcatholic 229.
  Batch plan in `batches.json`: 17 batches, `north-suburbs` first. No parish records yet.
