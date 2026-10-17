---
name: Roman Catholic Diocese of Scranton
state: PA
website: https://www.dioceseofscranton.org
status: promoted
gcatholic: scra0
promoted: 2026-10-17
---

Eleven counties of northeastern Pennsylvania: Lackawanna (Scranton), Luzerne (Wilkes-Barre,
Hazleton, Pittston, Nanticoke), Wayne, Pike, Monroe, Susquehanna, Wyoming, Bradford, Tioga,
Sullivan and Lycoming (Williamsport). The diocese reorganised its parishes in 2008–2010
("Called to Holiness and Mission"), so most canonical parishes today carry new names and
several worship sites.

## Sources

- **Parish directory (the `directory` roster):** https://www.dioceseofscranton.org/find-a-parish/
  lists 98 canonical parishes ("98 Parishes Found"). Each parish's detail page
  (`/find-a-parish/<slug>`) has a *Worship Sites* section with every church's name, address
  and Mass times. `rosters/directory.json` is those worship sites (137 entries, one per site,
  `group` = the parish, `mass_times` = the page's text for that site), scraped with plain
  `curl` on 2026-10-16 (no Cloudflare). No per-site coordinates. Its Mass times are often
  stale against the bulletins (Queen of Peace, Good Shepherd, St. Augustine, Wyalusing,
  Eagles Mere, Elkland, Nativity BVM, St. Joachim, Goretti, St. Monica, St. Mary Help of
  Christians), and some addresses are the parish office's (Canton, Dushore, Our Lady of the
  Abingtons). A site listed with no Mass times may be kept for funerals and weddings only
  (St. Clare, Scranton: "Available for Funerals, Baptisms & Weddings").
- **Mass times:** https://www.dioceseofscranton.org/find-a-mass/ ("138 Worship Sites Found",
  read 2026-10-16) is the same data as the finder's worship sites, one card per site with
  `data-latitude`/`data-longitude` and the Mass table; it supplied coordinates for churches
  GCatholic doesn't place. It has one site the parish pages omit: "Saint John Neumann
  Shrine", Sugar Ridge (Sts. Philip and James, under Immaculate Heart of Mary, Dushore).
- **GCatholic:** `rosters/gcatholic.json` (key `scra0`), 193 entries with Plus Codes. 31 are
  Eastern Catholic (marked `rite`: Ruthenian, Ukrainian, Maronite, Melkite), and one
  (St. Thomas More, 1625 N Main Ave) is an Ordinariate parish.
  It omits the cathedral and St. Ann's Basilica, keeps churches closed in the consolidations,
  and its `group` (canonical parish) is often stale: it still lists Holy Spirit Parish
  (Glen Lyon, suppressed January 2026), Our Lady of Perpetual Help and other pre-merger
  parishes. Several street numbers disagree with the parishes' own (recorded per church).
- **Church buildings of consolidated parishes** (the diocese's closed/merged list):
  https://www.dioceseofscranton.org/wp-content/uploads/2025/07/Consolidated-Parishes-updated-7-2-25.pdf
  (and the July 2024 edition, `.../2024/07/Consolidated-Parishes-12-20-23-updated-as-of-July-1-2024.pdf`).
  Lists each town's churches; "(closed <date>)" marks a closure, a bare date
  ("(11/2010)") a consolidation with the building still in use. Pages 4–7 of the 2024 edition
  have broken font encoding (render the pages). It is wrong at least twice: Holy Redeemer,
  Falls ("closed 9/2010") and Sacred Heart, Weston ("closed 2021") both have Sunday Mass in
  their current bulletins.
- **Diocesan news** (dioceseofscranton.org, the Catholic Light) reports closing Masses,
  decrees and suppressions with dates: St. Adalbert, Glen Lyon; Sacred Heart of Mary,
  Jermyn; St. Michael, Simpson; Nativity and Holy Name of Jesus, Scranton.
- **Hazleton clergy's city-wide Mass schedule**, effective 3 August 2026, on sscmparish.com:
  the only current schedule for St. Pius of Pietrelcina's churches.
- Clusters / families: the diocese does not run a family system. Several pairs of parishes
  share a pastor and, often, a bulletin; the finder's canonical parish is the `group`.

### Bulletin publishers here

76 parish rows: 44 `other` (self-hosted, Bon Venture, John Patrick, Google Drive), 19
ParishesOnline, 7 Discover Mass, 3 eCatholic, 3 `no_bulletin`.

- **Bon Venture Services** (`sponsors.bonventure.net/?page=<id>`, one PDF per Sunday at
  `pdfs/<id>/<YYYY-MM-DD>.pdf`, with an archive menu) prints ten bulletins here
  (St. John Paul II, Divine Mercy, Mary Mother of God, St. Ignatius/Holy Family, St. Jude,
  St. Robert Bellarmine/Holy Cross, St. Matthew, St. Luke, Queen of Peace, St. Ann/St.
  Boniface). Its https certificate chain is broken server-side (curl and Python fail
  verification; the pipeline falls back to the source URL); rows use `http://`. Many issues
  are image PDFs. A scan of ids 1–10400 for the 11 October 2026 issue found 145 parishes, 22
  in Pennsylvania.
- **J.S. Paluch on Discover Mass:** one joint bulletin can appear under several church slugs
  (the three Pike County parishes): record every slug as a publication. Download links carry a
  per-request token; cite the church page.
- **John Patrick Publishing** (church-bulletin.org): Christ the King, Archbald.
- **Pilot Bulletins** (thebostonpilot.com/bcd): St. Therese/St. Frances Cabrini. The embed
  page meta-refreshes to a viewer; the PDF is at `bcd/Bulletins/<YYMMDD>/<ED>_<YYMMDD>.pdf`.
- **Google Sites + Drive** (Freeland/Drums, Conyngham, Most Holy Trinity Susquehanna): yearly
  "2026-bulletins" pages that will likely move in January (revisits 2027-01-15).
- **Hosts seen:** `cdn.diocesanweb.org/crossroads/<site>/` WordPress (file names are the
  liturgical Sunday, not a date), `files.mychurchwebsite.net/c<id>/`, Wix, Squarespace,
  DotNetNuke (Plains: `LinkClick.aspx?fileticket=` links, one mislabelled with a 2017 issue),
  3D FlipBook (St. Thomas More: PDF only in base64 `FB3D_CLIENT_DATA`), FlipHTML5 of scanned
  JPEGs (St. Ann's Basilica), PDF Embedder (Our Lady of Victory, Tannersville: PDF only in the
  base64 `pdfemb-data` parameter).
- **Image-only bulletins are common:** Christ the King, Abington Catholic, Visitation BVM,
  Saint Carlo Acutis, St. John Vianney (page 1), St. Paul (pages 1–6), Sts. Cyril &
  Methodius (pages 1–3), Ascension/St. Katharine Drexel (pages 1–5), Our Lady of Victory,
  Most Holy Trinity (a Google Doc export), St. Mary, Waymart (one Squarespace JPEG, no PDF),
  Plains. Read by rendering pages; the pipeline must read them as images.
- **eCatholic sites that bypass the bulletin feature:** St. Monica uploads bulletins as
  documents (its /bulletins feed stops in May 2025; file names contain spaces); St. Maria
  Goretti's eCatholic site embeds a ParishesOnline widget.
- **Unreachable from the sandbox:** nepacatholic.com and nativitybvmparish.com (GoDaddy;
  PDFs on img1.wsimg.com download fine), sfkparish.com, St. Patrick, Milford's site, holyannunciation.com
  (down all session), olophparish.org (Cloudflare every load), stleos-holyrosary.org and
  Mary, Mother of God's site (refuse plain fetchers).

### Fetch check (2026-10-17, before promotion)

`fetch:check` reads only `data/parishes.csv`, so it was run on the unpromoted rows by calling
`fetch_check.check_fetch(parishes_csv=...)` on a temporary CSV built from `parishes/`, one
parish at a time, under `xvfb-run` with `PLAYWRIGHT_BROWSER_CHANNEL=chrome`. Of the 73 rows
with a provider, **61 resolved** (all 19 ParishesOnline, 7 Discover Mass and 3 eCatholic,
and 32 of 44 `other`), after pinning two recipes (St. Ignatius: Bon Venture over `http://`;
Seton: its archive page) and fixing a crash on recipe URLs with spaces (St. Monica). Two of the 61 picked the
wrong issue, and twelve rows were not read at all:

- **Wrong or misdated picks:** St. John Bosco reads "10/4-27th Sunday" as 2027 and picks the
  previous issue; Our Lady of Peace's file names (`10.4.26.pdf`) can't be dated and it picked
  a "Parish Consolidation" PDF; Nativity, Duryea picks the right file (11 October) but dates
  it 2026-03-04.
- **Formats the resolver doesn't read (8):** Our Lady of Victory, Tannersville (PDF Embedder
  `pdfemb-data`), St. Thomas More, Lake Ariel (3D FlipBook), St. Ann's Basilica (FlipHTML5 of
  JPEGs), St. Mary, Waymart (one JPEG), Most Holy Trinity, Susquehanna (Google Doc), Plains
  (DotNetNuke `LinkClick` posts), St. Rita, Gouldsboro (Net Driven JavaScript page whose
  static HTML embeds a 2024 PDF), Wyalusing (Cloudflare on every load).
- **Hosts that close the sandbox's connection (4):** holynameofmary.com, nepacatholic.com,
  ourladyofhope.us, stjosephsmatamoras.com (the proxy logs `ws_closed_mid_exchange` after
  the TLS hello). They may work from the pipeline's own runner.

Every row stays `other` with its evidence: each publishes a current bulletin, so none is
`no_bulletin`.

### Fetch check (2026-10-17, after promotion)

`fetch:check` over the 44 `other` rows, before and after resolver changes made for them:
**32 resolved before, 38 after**, and the picks that were wrong are now this week's issue.
The changes, all general (unit-tested, and replayed against the 77 other dioceses'
`other`/`google_drive` sites recorded the same day with no pick changed):

- **Dates:** an ordinal after a date is the Sunday's number ("10/4-27th Sunday", St. John
  Bosco); Weebly's `/uploads/3/4/1/2/<site>/` folders are no date (Nativity, Duryea); "+" is a
  space in file names ("10+18+26.pdf", Our Lady of Peace); a year before the month or joined
  by "_" is the issue's ("bulletin-2022-october-23", "Bulletin_October 12_2025": St. Michael
  the Archangel had picked a 2022 issue as this week's).
- **Choosing:** a first PDF neither dated nor labelled "bulletin" (Our Lady of Peace's
  "Parish Consolidation") gives way to the newest recent issue when the page lists a dated
  series.
- **Formats:** base64 JSON viewer settings (PDF Embedder `pdfemb-data`, Our Lady of Victory;
  3D FlipBook `FB3D_CLIENT_DATA`, St. Thomas More); Google Docs, exported as PDF (Most Holy
  Trinity); DotNetNuke `LinkClick.aspx` tickets (Plains); Pilot Bulletins embed links, read
  as their dated PDF (St. Therese had picked a registration form); GoDaddy `nebula.wsimg.com`
  file links (Milford, untested live); and a recipe-only `page-images` collector, with `fetch`
  storing an image bulletin as a one-page PDF (St. Mary, Waymart).

Recipes are pinned on the 22 rows whose pick was checked by hand (including the
`first-listed` ones: Holy Child, St. Michael Canton, Towanda, Montoursville, Most Holy
Trinity and Hunlock Creek, each this week's issue or the only one posted), and St. Jude now
reads its Bonventure page (the homepage guess had picked a Flocknote flyer). St. Monica's
printed recipe names one week's file, so it is not pinned. Plains' "October 11, 2026" link
still serves a 2017 file (the parish's upload mistake).

Not read on the after-run (6):
- **St. Ann's Basilica:** a FlipHTML5 book of four page JPEGs; the fetch stage downloads one
  file per bulletin, so a multi-image issue needs a fetch that assembles pages into a PDF.
- **St. Rita, Gouldsboro:** the Net Driven page navigates while it is read, and its posts
  are titled by the Sunday alone and run two weeks late, which `dated-post` does not follow.
- **Our Lady of Perpetual Help, Wyalusing:** Cloudflare challenged every load.
- **Holy Name of Mary, Montrose; St. Patrick/St. Joseph, Milford; Our Lady of Hope:** the
  sites reset the sandbox's connections. Our Lady of Hope and NEPA Catholic each resolved on
  one run and were reset on another (both are pinned, to the issue they picked); the other
  two never loaded here, so they have no recipe.

## Rules settled for this diocese

- **Eastern Catholic churches and the Personal Ordinariate** are excluded as
  `other-jurisdiction` (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of
  Philadelphia; Maronite: Eparchy of Our Lady of Lebanon; Melkite: Eparchy of Newton;
  St. Thomas More, Scranton: Ordinariate of the Chair of St. Peter), as in Syracuse and
  Rochester.
- **`group` is the finder's canonical parish name.** Shared pastors don't make shared
  bulletins: St. Eulalia and St. Catherine of Siena, Resurrection and Our Lady of Lourdes,
  Towanda and Wyalusing have one pastor and separate mastheads. Pairs that print one
  bulletin are one row (Gate of Heaven/Our Lady of Victory; Sacred Heart Dupont/Queen of the
  Apostles; St. Ignatius/Holy Family; St. Therese/St. Frances Cabrini; St. Leo/St. Andrew;
  St. Robert Bellarmine/Exaltation of the Holy Cross; All Saints/St. John the Baptist; Our
  Lady of the Snows/St. Gregory; Our Lady of the Abingtons/St. Mary of the Lake/St. Patrick
  Nicholson; Cathedral/Immaculate Conception; Most Holy Trinity/St. Maximilian Kolbe;
  Immaculate Conception Freeland/Good Shepherd; Ascension/St. Katharine Drexel; Holy Name of
  Mary/St. Brigid; St. Ann/St. John Neumann/St. Vincent de Paul; St. Patrick Milford/St.
  Joseph Matamoras; St. Peter/St. Thomas the Apostle; Immaculate Conception/St. Luke
  Williamsport; St. Ann/St. Boniface; St. Jude/Our Lady Help of Christians).
- **A worship site kept only for funerals, baptisms and weddings**, or with one festival
  Mass a year on its grounds, is `no-public-mass` (St. Clare, Scranton; St. Rocco, Dunmore).
- **A current bulletin beats the consolidated-parishes list** (Holy Redeemer, Falls; Sacred
  Heart, Weston keep their rows).
- **A GCatholic-only church that no current source mentions** goes to `open/` with a dated
  revisit, not `excluded/` (St. Lawrence O'Toole, Old Forge; St. Anthony, Newfoundland; Holy
  Family, Millrift; Sacred Heart, Duryea; St. Francis of Assisi, Scranton; St. Bernadette,
  Canadensis; the former St. James, Jessup).

## Log


Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-17: After promotion, `fetch:check` over the 44 `other` rows: 32 resolved; resolver
  changes for dates, an undated first PDF, base64 viewer settings, Google Docs, DNN, Pilot
  Bulletins, GoDaddy file links and image bulletins brought it to 38, with 22 recipes pinned
  (see "Fetch check (after promotion)"). Six rows still unread.
- 2026-10-17: Explored the whole diocese in seven regions (Scranton city; north Lackawanna and
  Wyoming; Wilkes-Barre; Pittston, West Side and Back Mountain; Hazleton and Monroe; Pike, Wayne
  and Susquehanna; Bradford, Tioga, Sullivan and Lycoming), one agent each, then a
  cross-region pass. Result: 76 parish rows for 98 canonical parishes (19 ParishesOnline, 7
  Discover Mass, 3 eCatholic, 44 other, 3 no_bulletin: St. Patrick, Scranton; Prince of Peace,
  Old Forge; St. Pius of Pietrelcina, Hazleton), 137 churches, 54 exclusions (32
  other-jurisdiction, 19 closed, 2 no-public-mass, 1 not-catholic) and 9 open questions.
  Coverage: directory 137/137, GCatholic 193/193; two churches are in no roster (Holy Family
  Chapel, Williamsport; Sts. Philip and James / St. John Neumann Shrine, Sugar Ridge, from the
  Find a Mass page). `audit`: two GCatholic groups span rows, both with separate bulletins
  recorded. `recheck` per region found every quote except on pages that refuse plain
  fetchers. Coordinates for five churches GCatholic doesn't place came from the Find a Mass
  page. Fetch check: 61 of 73 rows resolve, 59 to the current issue (see above). Not yet promoted.
- 2026-10-16: Initialised. Fetched GCatholic (193 entries) and scraped the diocesan finder's
  worship sites (137 entries from 98 parishes) as `rosters/directory.json`.
