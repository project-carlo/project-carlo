---
name: Roman Catholic Archdiocese of Hartford
state: CT
website: https://archdioceseofhartford.org
status: promoted
gcatholic: hart0
promoted: 2026-11-14
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
  - The homepage's "Archdiocese at a Glance" (https://archdioceseofhartford.org/, read
    2026-11-14) says "92 Parishes & Missions": the finder's 93 units with St. Matthew and
    St. Gregory the Great counted as one (see *Clergy directory*).
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

From `probe url` of all 98 sites the finder links (2026-11-13), and the map batches since:

- **Most parish sites are diocese-built WordPress (diocesanweb.org, "beacon"):** 77 of 98.
  The bulletin is on a `/bulletins/` (sometimes `/bulletin/`, `/weekly-bulletin/` or
  `/current-bulletin/`) page: a PDF uploaded to
  `cdn.diocesanweb.org/beacon/<site>/wp-content/uploads/<YYYY>/<MM>/` (file names vary by
  parish, e.g. `November-15-2026.pdf`), a ParishesOnline publication widget
  (`publicationWidget?type=bulletin&id=...`), or a link to church-bulletin.org or LPi.
  - The same pages and the yearly archives also link forms (cemetery rules, sponsor
    certificates) and *Branches on the Vine* (`Branches*.pdf`, the archdiocese's weekly
    news, not a parish bulletin). Unfiltered `page-pdfs` can pick either as first-listed:
    check the pick and pin the page plus a filename glob for the parish's own files
    (`filename=Bulletin-*.pdf`).
  - Uploads named `<YYYYMMDD>B.pdf` are LPi bulletins re-hosted: grep the ad pages for
    `4lpi.com` to get the container line ("St. Paul, Kensington, CT 03-0062"), find the org
    with `probe po` and a guessed slug (`<name>-church-<zip>`), and record
    `parishes_online` rather than `page-pdfs`. Uploads named
    `<NN>-<NNNN>-<Month>-<D>-<YYYY>.pdf` are LPi too: the prefix is the container
    (`03-0025` = 03/0025), so `probe container` finds the org directly. `probe pdf` reads 3
    pages by default and the container line is on an ad page near the end: pass
    `--pages <page_count>`.
  - A stale or empty bulletins page doesn't mean no bulletin: the parish's ParishesOnline
    org may be live and unlinked. Try `probe po` with guessed slugs (`<name>-parish`,
    `<name>-<zip>`) before calling it not found.
  - Mastheads laid out in church columns come out interleaved from `probe pdf`: download
    with `probe get --out` and read page 1 with `pdftotext -layout` to tie each Mass time
    to its church. `--out` resolves a relative path from the repository root, not the
    shell's directory: pass an absolute path inside your scratch folder.
  - Parish history pages (`/<church>-church/`) can date a church's closure; see *Rules
    settled*. Archdiocesan decrees and "Bulletin Blurb" notices on these sites are scanned
    images or PDFs: render them to read the effective date.
- **ParishesOnline (LPi)** appears on 32 sites, often as an org link beside a self-uploaded
  PDF, and behind the `<YYYYMMDD>B.pdf` uploads above. Org slugs found: see
  `scratch/hartford-map-1/001-survey/probe-all.tsv`. Org names are often older than the
  parish (St. Junipero Serra's is `st-margaret-mary-church-06074`), and one org can be
  linked from two parishes' sites: read the masthead. A guessed slug can belong to a
  same-named parish in another state (`st-marianne-cope-parish` is Solvay, NY): check the
  org address `probe po` gives before using it. `render.py`'s browser closes on very large
  scanned issues (~90 MB): `probe get --out` into an empty folder and render with
  `pdftoppm -f 1 -l 1 -r 80 -jpeg`.
  - Slugs also come as `<name>-roman-catholic-church` with no ZIP. A parish the finder
    lists with no website can still publish here: search DuckDuckGo for `<church> <town> CT
    bulletin` to surface its container PDFs, find the org with `probe po`, and record the
    org page as the website. When a finder or GCatholic domain is squatted, the org's
    website field gives the current domain.
  - A merged parish can keep publishing under an older member's org with a new container:
    follow the new parish site's org link and probe the org, not the old container; the
    predecessor sites keep stale bulletin pages.
  - Two orgs can serve one container: when `probe po` shows the same container under two
    orgs, make one row and record both orgs' po-org and lpi ids.
- **church-bulletin.org / jppc.net:** linked from diocesanweb pages as
  `church-bulletin.org/?id=<n>`. Unpinned `fetch:check` prints recipe `linked-issue-page`
  and picks `church-bulletin.org/bulletin/<slug>/<date>.pdf`, which can be a scan while the
  parish's own diocesanweb upload of the same issue has text: compare before pinning.
  Unpinned, it can also reach the issue through an unrelated site page (`/kids-bulletin/`).
  Pin `page-pdfs https://www.church-bulletin.org/<slug>` (the `?id=<n>` redirect target,
  newest first), or, where the parish page also links
  `parish.jppc.net/wp-content/churchuploads/<id>-BULL-<MM-DD-YYYY>.pdf` uploads (these
  have text), `page-pdfs <parish bulletins page> filename=*-BULL-*.pdf`: names vary in
  case and digits, and the resolver orders by the file-name date, not page order.
- **bonventure.net** (`sponsors.bonventure.net/?page=<id>`, PDFs at
  `pdfs/<id>/<YYYY-MM-DD>.pdf`): `page-pdfs` resolves the current issue, but the https
  download fails certificate verification (incomplete chain); `probe get` works over http.
  Record `bulletin_provider: unsupported` with fetch_gap kind `tls-certificate-unverified`.
- **Solutio (Joomla) sites:** bulletins at `/bulletin/<n>-<title>/file`, which answer 403 to
  probes. `visit.py --screenshot` of the `/file` link shows page 1 in Chrome's PDF viewer,
  enough for the masthead. Record them `unsupported` with gap `joomla-file-endpoint`.
- **Others seen once or twice:** Discover Mass, Wix or similar (nbcatholics.org,
  stelizabethofthetrinity.org). Wix and Weebly file hosts answer 429 to rapid `probe pdf`;
  space the requests. A parish posting its bulletin only as photos in a public Facebook
  group is `unsupported` with gap `facebook-group-images` (`visit.py` reads the post text;
  the images sit behind the login overlay).
- **Needs a real browser** (`probe url` said NO-PARISH-WORDS or 4xx at survey):
  stmatthewrcc.com, ourlady-stpatrick.org, olsparishchurch.org.
- **Parish finder links for quasi-parishes and ethnic communities** can point into another
  parish's site, sometimes to an old history page. Search `html.duckduckgo.com` for the
  community's own domain before treating it as covered by that parish's bulletin.
- **Dating a closure** (sources, not publishers): for churches the 2017 plan closed with
  no decree, the Hartford Courant's 7 May 2017 `list-of-parish-closures-and-mergers-by-town`
  gives the plan for every town, and `probe get` of `html.duckduckgo.com/html/?q=...`
  ("courant.com <church> final Mass") finds dated local reports (Courant June 2017 "final
  regular Mass" articles, the Suffield Observer). For a later end, run `probe container
  <a/b> --from <date> --weeks 160 --step 8 --all --pages 1`, see where the church leaves
  the schedule, then narrow with `--weeks 8 --all --pages 3` to find the announcement.
  A relegation decree recites the parish's merger decree and earlier relegations of its
  sibling churches: read decree page 1 when dating a merged parish's other churches.
  A merged parish's lapsed old site (now a domain auction page) still shows in DuckDuckGo
  with its `LO.ashx?name=~/Bulletins/...` PDFs, and Wayback may hold none: the snippets
  say what to look for in the live parish's issues, but are not quotable evidence.
- From the neighbours: Albany found image-only ParishesOnline bulletins common (about one in
  five), and one bulletin printed into two LPi containers with only the ad page differing.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- A church relegated to profane use by a published archdiocesan decree is excluded as closed, dated to the decree unless a bulletin gives the last Mass, even if the parish finder or GCatholic still lists it; check the parish's current bulletin first for a continuing Mass there. (accepted by survey-review, 002-survey-review, 2026-11-13)
- A shared pastor named in the clergy directory puts the two parishes in one batch and in a shared audit group, but makes one row only if a current bulletin covers both (as Albany settled). (accepted by survey-review, 002-survey-review, 2026-11-13)
- The eleven Eastern Catholic churches GCatholic lists (rite set) are other-jurisdiction exclusions (Stamford Ukrainian, Passaic Ruthenian, St. Maron of Brooklyn, St. Thomas Syro-Malabar of Chicago). (accepted by survey-review, 002-survey-review, 2026-11-13)
- A church the 2017 pastoral plan closed with no decree is dated by a dated local report of its final Mass; the Courant's 2017 closures list is the plan, not proof of the date. (map batches `north-suburbs` and `hartford-city`, 2026-11-13)
- A closure date on the parish's own history page is recorded as `last_mass` even when it is years before the relegation decree, and the decree is cited as well. (map batch `east-hartford-glastonbury`, 2026-11-13)
- Whether a church is in use is decided from the Mass schedule and every church section of
  the Mass intentions, not the masthead's church list, which can keep a church closed years
  earlier. Before excluding a church missing from page 1, grep two years of issues for
  `<name> Church`: a merged parish can hold a weekly intentions-only Mass or a feast-day
  public Mass in a church with no listed weekly Mass. (map batches
  `meriden-wallingford-cheshire`, `hamden-north-haven-shoreline` and `waterbury`,
  2026-11-14)
- A church missing from a merger decree's list of the new parish's sacred edifices is no
  longer that parish's, but is recorded as open unless a source dates its closure. (map
  batch `new-haven-east-haven`, 2026-11-14)
- A church the 2017 plan closed that holds Mass again is open: check the current schedule
  before applying a 2017 closure report. (map batch `west-haven-milford`, 2026-11-14)
- GCatholic Plus Codes are sometimes ~500 m off the building: where the finder pin and the
  ParishesOnline org's address agree, use them. (map batch `lower-naugatuck-valley`,
  2026-11-14)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-14: Reconcile (factory run hartford-map-1) after 17 map batches (11 to 32 roster
  entries each, usually 20-27). Coverage: directory 167/167 accounted for, 148/158 modelled;
  GCatholic 229/229, 146/163 modelled. Records: 89 parishes (82 fetchable, 5 `unsupported`,
  2 `no_bulletin`), 158 churches, 66 exclusions, 8 open. No merges or moves: the audit's two
  shared-pastor pairs (Naugatuck; Canaan/Winsted) have content-supported `separate` reviews.
  The 8 open records each had one more check (bulletins, archdiocese news API, searches);
  none settled. `fetch:check`: 82 rows, all the right parish's latest posted issue; St.
  Catherine (1 Nov) and St. Francis, New Britain (25 Oct, fortnightly) lag on their sites.

- 2026-11-13: Survey (factory run hartford-map-1). Rosters: directory 167, gcatholic 229.
  Batch plan in `batches.json`: 17 batches, `north-suburbs` first. No parish records yet.
