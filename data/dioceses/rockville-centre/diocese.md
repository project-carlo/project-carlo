---
name: Roman Catholic Diocese of Rockville Centre
state: NY
website: https://www.drvc.org
status: exploring
gcatholic: rock2
---

The whole of Long Island east of New York City: Nassau County (Hempstead, Garden City,
Freeport, Long Beach, Glen Cove, Hicksville, Massapequa, Great Neck, Port Washington) and Suffolk
County (Huntington, Babylon, Islip, Brentwood, Smithtown, Patchogue, Port Jefferson, Riverhead,
the North and South Forks, Shelter Island and the Fire Island communities). The chancery is in
Rockville Centre; the cathedral is St. Agnes. GCatholic (read 2026-11-12) names its neighbours as
Brooklyn (Queens, to the west), New York (across Long Island Sound) and Norwich (Connecticut,
across the Sound). Only New York is mapped, for one parish. GCatholic counts 132 parishes (2022).
The diocese's deanery list (2025-10-20) names 133.

**How it is organised.** There are two vicariates (Western, Eastern) and seven deaneries (South
Nassau, East Nassau, North Nassau, 110 Corridor, South Central Suffolk, North Central Suffolk,
East End). No diocesan family, cluster or pastorate list was found, and the diocese's site has no
merger or closure announcements. Almost every parish has one church and its own pastor and
website. Shared bulletins are most likely where the clergy appointments or a shared website put
parishes together:

- **Five Towns:** St. Joseph (Hewlett), St. Joachim (Cedarhurst) and Our Lady of Good Counsel
  (Inwood) have one pastor and one site (5townsparishesny.com). The pastor's booklet says they
  "are still three separate Canonical and Corporate entities".
- **Long Beach ("Beach Catholic"):** St. Ignatius Martyr, St. Mary of the Isle and Our Lady of
  the Miraculous Medal (Point Lookout) share beachcatholic.com and their parochial vicars.
- **Glen Cove:** St. Patrick, St. Rocco and St. Hyacinth (Glen Head) have one pastor from the
  Canonry of Saint Leopold (June 2025) and share glencovecatholic.org. Until June 2026 one
  parochial vicar also served St. Boniface Martyr, Sea Cliff.
- **New Hyde Park:** Holy Spirit and Notre Dame (newhydeparkcatholic.com, shared vicar).
- **North Fork:** one pastor for Sacred Heart and Our Lady of Ostrabrama (Cutchogue), St. Agnes
  (Greenport) and St. Patrick (Southold) since June 2025, and one parochial vicar from June
  2026. Sacred Heart has a mission in Mattituck.
- **Centerport and Northport:** Our Lady Queen of Martyrs and St. Philip Neri have one pastor
  (June 2025).
- **Patchogue:** one administrator for Our Lady of Mount Carmel and St. Francis de Sales (June
  2025). Their parochial vicar also served St. Joseph the Worker, East Patchogue.
- **Farmingville and Medford:** Resurrection and St. Sylvester have one pastor (June 2025).
- **Roosevelt and Uniondale:** Fr. Rony Fabien is pastor of both Queen of the Most Holy Rosary
  and St. Martha (second terms named in 2026 and 2025).
- **Shared parochial vicars only:** St. Hedwig (Floral Park) with St. Ladislaus (Hempstead), St.
  Mary (East Islip) with St. Peter (Islip Terrace), and St. Anthony (East Northport) with St.
  Francis (Greenlawn), all in June 2025.
- **East Hampton and Montauk:** from 2026-09-23 Most Holy Trinity's pastor is also pastor of
  St. Therese of Lisieux. Most Holy Trinity has a mission, St. Peter, Amagansett.

Missions and chapels: St. Peter (Amagansett), Our Lady of Good Counsel (Mattituck), Lakeview
Mission (West Hempstead), St. Joseph's Oak Beach mission (Babylon), and three summer churches on
Fire Island (Ocean Beach, Saltaire, Davis Park). Eastern Catholic churches in the territory
(Ukrainian, Ruthenian, Syro-Malabar, Syro-Malankara) belong to their own eparchies.

## Sources

- **Parish locator (the `directory` roster):** https://www.drvc.org/maps/, a WP Google Map Gold
  map. Its places are JSON embedded in the page; `probe get` reads it. Read 2026-11-12: 139
  places, one per church, with address, coordinates, county, town and website. It has no
  grouping and no clergy. Good for the church list and coordinates. Its websites are often old
  domains that now redirect (ollmp.org → ourladyoflourdesmp.org, pothc.org → holycrossrc.org,
  stpatrickchurchhunt.org → stpathuntington.org, resurrectionrcchurch.org → coresrcc.com), and
  three no longer resolve (cureofarschurch.net, sscyrilandmethodius.org, stpetersnyit.org).
  Slips: Blessed Sacrament (id 4) has town "Suffolk" though it is in Valley Stream, Nassau (the
  scraper uses the map's municipality instead); Sacred Heart, Cutchogue (id 104) links
  sacredheartnm.org, the North Merrick parish's site (its own is sacredheartolgc.org). Entry 68
  is the Syro-Malankara St. Vincent de Paul Cathedral, Elmont, which the Latin St. Vincent de Paul
  parish also uses. Scraper: `scratch/rockville-centre-map-1/tools/locator.py`.
- **GCatholic (the `gcatholic` roster):** key `rock2`, fetched 2026-11-12: 142 entries. 133 of
  them match the directory one to one. GCatholic does **not** list St. Agnes Cathedral, Our Lady of
  Poland and the Basilica of the Sacred Hearts of Jesus and Mary (both Southampton), Our Lady of
  Good Counsel (Mattituck), Our Lady Star of the Sea (Saltaire) or Lakeview Mission. It adds nine
  entries the directory lacks: seven Eastern Catholic churches (rite given: Ukrainian St. Vladimir,
  Hempstead; Holy Family, Lindenhurst; St. John the Baptist, Riverhead; the St. Josaphat
  monastery, Glen Cove; Ruthenian Resurrection, Smithtown, and St. Andrew the Apostle, Westbury;
  Syro-Malabar St. Mary, West Hempstead, "Using the building: Church of St. Thomas the Apostle"),
  the Shrine of Our Lady of the Island (Eastport) and the Immaculate Conception Seminary
  (Huntington). Its St. Vincent de Paul, Elmont (16839) is the Latin parish, "Using the building:
  St. Vincent de Paul Malankara Cathedral".
- **Mass times (the `mass-times` roster):** https://www.drvc.org/mass-times/ (WordPress page
  15718, modified 2026-10-21), "Mass Schedules by Parish", alphabetical by town: 139 church
  headings with schedules. A hand-edited page, and older than its date suggests: many links are
  to dead or superseded domains, several link another parish's site (it is safer to match on the
  town), and 14 link only the old drvc.org parish listing. It lists Sacred Heart, North Merrick
  twice (under Merrick and North Merrick) and St. Isidore, Riverhead twice (the second for its
  3:30 pm Sunday Latin Mass), and it is the only list with St. Joseph's Oak Beach mission. It
  omits Lakeview Mission and two of the Fire Island churches. For St. Vincent de Paul, Elmont it
  gives only "Sunday: 8:45 AM". A trailing list of Traditional Latin Mass parishes (St. Isidore,
  St. Matthew Dix Hills) was not imported. Scraper:
  `scratch/rockville-centre-map-1/tools/masstimes.py`.
- **Deaneries:** https://www.drvc.org/vicariates-deaneries/ (modified 2025-10-20) lists the 133
  parishes by deanery. It is the closest thing to a current parish list and still names St.
  Vincent de Paul, Elmont. Deaneries are not bulletin groupings, so they are not in `group`.
- **Clergy appointments:** the bishop's lists at
  https://www.drvc.org/the-following-official-appointments-and-announcements-have-been-made-by-the-most-reverend-john-o-barres-bishop-o-f-rockville-centre-unless-otherwise-noted-all-are-effective-june-24-2026/
  (a 5-page image-only PDF served at that URL, dated June 24, 2026; read by rendering the pages)
  and the June 24, 2025 list (same form, 8 pages); the June 2023 list was not read. Between them
  they name the shared pastors and vicars above. It is the best evidence here of which parishes work as one. It is evidence
  of shared clergy, not of a shared bulletin.
- **Five Towns booklet:**
  https://www.5townsparishesny.com/uploads/1/5/4/3/154337448/the_status_progress_and_development_of_the_parishes_of_the_five_townss_english.pdf
  (undated, read 2026-11-12). The pastor's three-year plan for the three Five Towns parishes;
  they remain separate canonical parishes.
- **Clusters / families of parishes:** none published. drvc.org's search finds no cluster,
  merger, pastorate or closure pages (searched 2026-11-12).
- **Closed parishes and where their records went:** not found on drvc.org.
- **Pastoral plan / closure announcements:** none found. The diocese's news is dominated by its
  Chapter 11 reorganisation, which has no parish closures in it that the site states.

### Bulletin publishers here

From the survey's probes of 130 parish websites (2026-11-12) and the map batches since.

- **Reaching sites:** `probe url` returned 403 for 46 sites and could not connect to 25
  ("egress proxy: EOF", RemoteDisconnected); in `visit.py` 17 of 18 such sites loaded
  normally, and `fetch:check` reads them too. A probe failure alone is not a fetch gap: use
  `visit.py --bulletin` and download PDFs with `tools/browser_get.py <url> <out>`.
- **Fetch gaps seen here** (row `unsupported`, recipe kept in `provider_id`): an incomplete TLS
  chain (`probe get`: "unable to get local issuer certificate"; http redirects to https) is
  `tls-incomplete-chain`; a page `fetch:check` lists but whose PDFs answer 403 to it and to
  `probe get` (self-hosted WordPress, e.g. olvfpny.org; Chrome gets them) is
  `pdf-download-403`; a Cloudflare challenge on every `visit.py` run and in `fetch:check`
  ("blocked NoBulletin"), with no copy on another host, is `cloudflare-challenge` plus
  access-blocked research and a revisit date.
- **Filename dates:** fetch's parser reads month names inside words (`11-8-26-martintours.pdf`
  dates as 2026-03-26, "mar"). Check `url_date` in `fetch:check`; if the right file gets a
  wrong date, the row is `unsupported` with `filename-date-misread`.
- **Reading PDFs:** check `pdfinfo` Creator first. Canva PDFs can be image-only or carry the
  Mass schedule as an image; PScript5/Acrobat Distiller issues (common on Solutio) can have a
  subset-font text layer that `pdftotext` turns to symbol soup. When `probe pdf --grep` finds
  no Mass or the text is garbled, render pages 1-2 with `render.py`.
- **Solutio (Joomla) sites** are common. They post issues at `/news/bulletin/<n>-<date>` or
  `/news-events/bulletin` (some on `*.solutiosoftware.com`). Their `/file` PDFs answer 403 to
  `probe get` but download with `browser_get.py`; read the Creator (Word/Publisher means
  self-made; a printer's means look for its listing) before looking for a ParishesOnline or
  John Patrick listing, then follow the rule below. Issue names starting `lpi-bulletin-…` mean
  LPi prints it (Sacred Heart Cutchogue; its container is not `sacred-heart-church-11935`).
  List items with a "default" icon instead of "pdf" may redirect `/file` to a Canva design
  viewer (`canva.com/design/<id>/view`): open one in `visit.py` to see `final_url`, read pages
  as screenshots (`view#N`), and record `fetch_gap` `canva-design-viewer`.
- **ParishesOnline / LPi** is reachable (`probe po`): e.g. `lpi:0018000000Qc1NlAAJ`
  (container 03/0634). Slugs like `<name>-church-<zip>` often miss here; use the LPi id the
  site embeds or the 4lpi.com link.
- **eCatholic** sites sit behind Cloudflare (403 to `probe url`, fine in `visit.py`); issues
  at `files.ecatholic.com/<id>/bulletins/<YYYYMMDD>.pdf`.
- **John Patrick Publishing** (jppc.net, church-bulletin.org): the listing is
  `church-bulletin.org/<name-town-st-zip>`, issues `/bulletin/<id>/<YYYY-MM-DD>.pdf`. Record
  provider `other` with `page-pdfs` on the listing, which picks the current issue. Some issues
  are image-only scans: read them with `render.py`.
- **The Church Bulletin Inc., West Babylon** (back page "#<n> FOR ADVERTISING: THE CHURCH
  BULLETIN INC.") prints several bulletins here but posts none online
  (thechurchbulletininc.com has no listing): there is no printer listing to collect from; use
  the parish's own copy.
- **Discover Mass:** `download.php?bulletin=<token>` URLs change token on every visit. Identify
  the issue `fetch:check` picked by the date on its page 1 (`probe pdf --pages 1`), not the URL.
- **Edlio** (`*.files.edl.io` PDFs, `/apps/pages/index.jsp?uREC_ID=…`): the home page may link
  a stale issue. Pin `page-pdfs` on the Bulletin page, which lists issues newest first with the
  date only in link text (paths carry the upload date); `fetch:check` reports issue date
  unknown, so confirm its pick by the link text.
- **Self-hosted** PDFs on WordPress, Wix, Squarespace and Weebly are the most common case.
  Wix lists issues on `/current-bulletin` or yearly `/2026-bulletins` pages; where only the
  home page links the current issue (a hashed `/_files/ugd/*.pdf`), unpinned fetch can pick
  another page's PDF, so pin `page-pdfs` on the page that links the bulletin. A WordPress site
  with no archive page still lists its uploads at
  `/wp-json/wp/v2/media?search=<word>&_fields=source_url` (via `visit.py` if `probe get` is
  blocked); use it to choose a filename glob for `page-pdfs` on the home page.
- **LPi WeConnect:** `*.weconnect.com` sites rendered without parish words here (in Allentown
  every one answered "Temporarily Unavailable").
- **Dead parish domains:** when `probe get` gets 429 from web.archive.org, `visit.py` still
  reads the Wayback CDX list (`web.archive.org/cdx/search/cdx?url=<domain>/*&collapse=timestamp:6`)
  and snapshots; use them to date the lapse and the last Mass schedule.
- **Fire Island:** oceanbeachcatholic.org posts one seasonal bulletin PDF for Our Lady of the
  Magnificat (a summer parish); its Saltaire and Davis Park pages answer 404.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- flipbook.so: some Solutio bulletin /file links redirect to flipbook.so/flip/<id> viewers (title gives the issue date) serving only .webp page images on storage.googleapis.com, no PDF; visit.py --text reads the text layer; fetch:check answers resolve_failed, so record unsupported with fetch_gap flipbook-so-viewer.
- LPi-printed parishes on eCatholic sites with 'No bulletin found' (e.g. a Drive archive instead) are usually on ParishesOnline as <name>-<zip> with 'st' (church-of-st-mary-11030), even when the bulletin says 'Saint'; try probe po on those slug forms.
- GoDaddy Website Builder sites list bulletin PDFs on img1.wsimg.com/blobby/go/<site>/downloads/<uuid>/<name>.pdf, often oldest first; page-pdfs on the bulletin page still picks the newest by the filename date (St. Edward, Syosset).
- LPi copies posted on Solutio sites can carry Creator Canva (St. Hugh): grep the PDF for '4lpi.com' or the footer '<Org name> | 03-NNNN' before treating the issue as parish-made; the footer gives the container.
- When <name>-church-<zip> misses on ParishesOnline, try the LPi footer's org name slugified with no zip (St. Hugh of Lincoln Roman Catholic Church -> st-hugh-of-lincoln-roman-catholic-church).
- fetch:check refuses unsupported rows; tools/fc_unsupported.sh sets provider other for the check and restores unsupported.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Where an Eastern Catholic community uses a Latin parish's church (Syro-Malankara St. Vincent de Paul Cathedral / Latin St. Vincent de Paul, Elmont; Syro-Malabar St. Mary / St. Thomas the Apostle, West Hempstead), the church row belongs to the Latin parish if the Latin parish still has public Mass there. The Eastern community's roster entry goes in excluded/ as other-jurisdiction and names the shared building. If the Latin parish no longer has Mass in the building, the building goes in excluded/ as other-jurisdiction. (accepted by survey-review, 002-survey-review, 2026-11-13)
- A Solutio (Joomla) parish site whose /news/bulletin/<n>-<date>/file PDFs answer 403 is not on its own a reason for no_bulletin. First look for the printer's listing (LPi id or ParishesOnline org, John Patrick). If there is none, record the site and make the row unsupported with fetch_gap joomla-file-endpoint, as Camden and Trenton do. (accepted by survey-review, 002-survey-review, 2026-11-13)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-12: Survey (factory run rockville-centre-map-1). Rosters: gcatholic 142, directory 139,
  mass-times 139. 20 batches in `batches.json`. No records yet.
