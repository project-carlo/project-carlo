---
name: Roman Catholic Archdiocese of Newark
state: NJ
website: https://www.rcan.org
status: exploring
gcatholic: newa0
---

The Archdiocese of Newark covers four counties of northern New Jersey: Bergen (Hackensack,
Paramus, Ridgewood, Fort Lee), Essex (Newark, the Oranges, Montclair, Bloomfield), Hudson
(Jersey City, Bayonne, Hoboken, Union City) and Union (Elizabeth, Linden, Westfield,
Plainfield). Its neighbours are the Diocese of Paterson (Passaic, Morris, Sussex) to the west,
the Diocese of Metuchen (Middlesex, Somerset) to the south-west, and the Archdiocese of New York
(Rockland County, Staten Island and Manhattan across the Hudson) to the north and east. It has
about 213 canonical parishes and no family or cluster system: most parishes are single-church
and print their own bulletin. Shared bulletins are most likely in three places: merged parishes
that kept a second church (St. John Paul II and Blessed Miriam Teresa in Bayonne, Holy Redeemer
in West New York, Holy Cross in Harrison, Divine Mercy in Rahway, St. Teresa of Calcutta in
Montclair); pairs of parishes with one pastor (Newark's inner city, Kearny, Jersey City,
Hillside); and the "Parish Mission Partners" groups named in June 2026 (Bayonne;
Westfield-Scotch Plains; Teaneck-Bogota; Transfiguration-St. Antoninus, Newark). Newark and
Jersey City have many closures and mergers. GCatholic also lists 17 Eastern Catholic churches
in the territory.

## Sources

- **Parish directory:** https://rcan.org/parishes/ (page modified 2026-06-03, read 2026-11-03).
  The page embeds a `plPlaces` JSON list (name, address, city, coordinates, id) and one card
  per parish (website, an "english spanish" language tag on 83, search aliases). 218 entries,
  one per canonical parish rather than per church; 193 link a website. Roster `directory`,
  built by `scratch/newark-map-1/tools/rcan_directory.py`. Trust it for the canonical names and
  for the parish's own address. Known faults: St. James, Newark is listed twice (ids 130 and
  142, same address; only 142 has a website); Immaculate Heart of Mary, Newark is missing
  (it is in the planning areas and GCatholic 18492); St. Patrick & Assumption/All Saints,
  Jersey City's card has its name where the URL should be; Immaculate Conception and Our Lady
  of Good Counsel (Newark) share one address; St. Augustine, Newark's address is a PO box.
  It still lists St. Thomas Aquinas, Newark (40 Ludlow St.), which the records list counts
  as closed (see below), and St. Anthony of Padua, Newark (750 N 7th St.), which is in no
  other list. It includes the Newman Center Chapel (Montclair State) and the Institute of
  Christ the King's St. Anthony of Padua Oratory (West Orange), and omits churches that a
  merged parish kept.
- **GCatholic:** key `newa0`, https://gcatholic.org/churches/local/newa0 (fetched 2026-11-03).
  257 entries: 240 Latin and 17 Eastern Catholic (7 Ruthenian, 6 Ukrainian, Melkite,
  Syro-Malabar, Syro-Malankara, Syriac). It lists churches rather than parishes, so the
  second churches of merged parishes are here: St. Andrew and St. Mary Star of the Sea,
  Bayonne; St. John Nepomucene (Guttenberg) and Our Lady of Libera and Our Lady Help of
  Christians (West New York); St. Rocco, Newark; St. Mark, Rahway. It also has chapels and
  houses (Stella Maris, Port Newark; Seton Hall's chapel; the Rosary Shrine, Summit; St. Cloud
  and Divine Mercy Hill; Redemptoris Mater seminary, Kearny; a Carmelite chapel, Paramus).
  It has no entry for the Cathedral Basilica, St. Patrick Pro-Cathedral, St. Anthony of
  Padua (Newark) or the Newman Center. It still lists churches the records list calls
  closed (Queen of Angels, Newark; St. Bridget, Jersey City, as part of a "Parish of the
  Resurrection"). St. Joseph, Demarest appears twice (280 and 274 County Rd.). The Syriac Our
  Lady of Deliverance (25653) is in Woodland Park, Passaic County, outside the archdiocese.
  Good for a second address and building coordinates; trust it least on closures.
- **Clusters / families of parishes:** none. The nearest thing is the 11 *planning areas*
  of the We Are His Witnesses plan (https://rcan.org/planning-area-a-northwest-bergen/ to
  `-k-eastern-union/`, modified 2026-01-08), which list 213 parishes by county region (A-D
  Bergen, E-F Hudson, G-I Essex, J-K Union) with a statistics workbook per parish (2025; no
  worship-site lists). Saved as `scratch/newark-map-1/tools/planning-areas-2026-01.tsv`, not
  imported as a roster: an area has 12 to 29 parishes and says nothing about bulletins, so as
  `group` it would only add noise to `audit`. It matches the directory apart from the
  differences named above and St. Anthony, East Newark (part of Holy Cross). Each area also
  has a "Pastorate Models: Round 1" PDF (2025, two draft pairings per area, marked
  confidential). These were plans only, dropped when the Cardinal "pivoted" in March 2026.
  Use them as leads, never as evidence of a grouping. Their 2024 attendance figures are
  blank for St. Anthony of Padua, Union City and St. Ann, Jersey City.
- **Shared pastors:** the rcan.org clergy appointment posts (70 posts, 2021 to Oct 2026,
  read through `wp-json/wp/v2/posts?search=clergy appointments`). There is no clergy
  directory. Explicit two-parish pastorates: Our Lady of Mount Carmel and Holy Trinity-
  Epiphany, Newark (2022, 2025); Our Lady of Good Counsel and Immaculate Conception, Newark
  (2025); St. Patrick Pro-Cathedral and St. John, Newark (2021-27); St. Benedict and
  St. Aloysius, Newark (2021-28); Our Lady of Sorrows and St. Cecilia, Kearny (2023, 2024);
  Christ the King and Our Lady of Sorrows, Jersey City (2023, 2024); Holy Cross, Harrison
  and St. Anthony, East Newark (2023, 2024); St. Catherine of Siena and Christ the King,
  Hillside (from July 2026); St. Joseph, West Orange and St. Raphael, Livingston (2022, may
  have ended); Our Lady of Mount Carmel, Jersey City's pastor administering St. Ann, Jersey
  City (Nov 2025). A shared pastor is only a reason to check for one bulletin.
- **Mass times:** no diocesan Mass-times index (rcan.org search for "mass times" and "mass
  schedule" on 2026-11-03 finds only event posts). Use parish sites and bulletins.
- **Closed parishes and where their records went:** https://rcan.org/sacramental-records/
  (modified 2025-05-22): 56 rows, 34 Merged, 20 Closed, 2 Reopened (St. Mary's and
  St. Michael, Jersey City). Saved as `scratch/newark-map-1/tools/rcan-closed-merged-2025-05.tsv`.
  As everywhere, it says a parish corporation ended, never that a building is shut. It names a
  closed St. Thomas Aquinas, Newark with its records at Blessed Sacrament, Elizabeth, but the
  directory still lists a St. Thomas Aquinas, Newark.
- **Pastoral plan / closure announcements:** We Are His Witnesses (https://rcan.org/we-are-his-witnesses/,
  launched June 2025). The June 12, 2026 letter (https://rcan.org/wahw-june-2026-letter-cardinal-tobin/)
  replaced the pastorate models with "Parish Mission Partners" and named twelve pilot parishes:
  Transfiguration and St. Antoninus (Newark); St. Henry, St. John Paul II, St. Vincent de Paul
  and Blessed Miriam Teresa Demjanovich (Bayonne); Immaculate Heart of Mary and
  St. Bartholomew (Scotch Plains), Holy Trinity and St. Helen (Westfield); St. Joseph (Bogota)
  and St. Anastasia (Teaneck). Closure decrees are posted as news: St. Andrew the Apostle,
  Bayonne (closed for worship 2024-09-22, decree 2025-05-28); St. Anthony's Church, East
  Newark (closes for worship 2026-11-23, posted 2026-10-10). Search
  `rcan.org/wp-json/wp/v2/search?search=decree` for later ones.
- **Campus ministry:** https://rcan.org/campus-ministry/ lists Newman ministries at Kean,
  Montclair State, NJCU, Ramapo, Rutgers-Newark/NJIT/ECCC and Stevens, and the chapels of
  Seton Hall, Felician, Caldwell and Saint Peter's. Only the Newman Center Chapel (Montclair)
  and Seton Hall's chapel are on a roster.
- **rcan.org's WordPress API** answers plain `probe get`: `wp-json/wp/v2/pages?slug=<slug>`
  and `wp-json/wp/v2/search?search=<words>` read any page or post without the theme.

### Bulletin publishers here

Tools named here are in `scratch/newark-map-1/tools/`.

- **Start a site with `probe url`**: it lists the publishers a
  page links and its builder. Open `parish-site-access`'s `visit.py` when it says HTTP4XX or
  NO-PARISH-WORDS or finds no publications. When `visit.py` hangs (an eCatholic homepage
  that never settles), `quick_snap.py` loads it with hard time limits.
- **Finding a site:** a parish can move domain while the directory and GCatholic keep the
  old one; when its own bulletins are stale, read the current issue's masthead website line
  and the ParishesOnline org's website field. Guess domains
  (`sjb<town>.org`, `<name><town>nj.org`) and confirm the masthead address; a 403 with 0 bytes can be eCatholic behind Cloudflare, so try
  `visit.py`. For searches, the Wikipedia API (`w/api.php?action=query&list=search&srsearch=…`,
  then `prop=extracts&explaintext=1`) gives merger histories; Bing searches only the first
  word. DuckDuckGo answers `probe get` with a bot check, but
  `visit.py --text` on `html.duckduckgo.com/html/?q=…` returns results. catholicchurch.directory keeps old parish domains. For an order's parish,
  search the order's site (`wp-json/wp/v2/search?search=<town>`). A directory entry in no
  other list can be a parish's office across a town line: `diocese search` the name and read
  its JP listing's website and masthead before creating a row.
- **A site that is down or lost:** the Wayback CDX (`probe get
  http://web.archive.org/cdx/search/cdx?url=<host>&matchType=prefix&fl=timestamp,statuscode,length`)
  and `archive.org/wayback/available?url=<domain>` answer when `web.archive.org` gives 429. The CDX dates a lapse:
  ~930-byte captures are an LPi WeConnect site's "temporarily unavailable" page, and the last
  larger capture (`id_` URL) shows the old site. `quick_snap.py` or `visit.py` on
  `web.archive.org/web/<year>/<url>` opens a copy; its HTML gives an eCatholic id
  (`files.ecatholic.com/<id>`) for `issues.py`.
- **Image-only issues are common** (John Patrick, LPi, eCatholic): read pages 1–2 with
  `render.py` and cite the masthead by note. A PDF on a host the probe proxy can't reach
  opens with `visit.py --screenshot`; add `#page=N&zoom=50` to see more of a page.
- **Read the footer of a self-hosted bulletin** for the printer's code (formats below)
  before deciding the publisher. A parish's own archive or eCatholic reposts of an LPi bulletin
  can lag the publisher's listing by years: record the publisher, not the copy, and leave the
  eCatholic id out of `publication` when it is only the website. A parish can also change
  printer without changing its links: when an LPi container stops while the parish still
  says "take a bulletin", look for a John Patrick listing.
- **John Patrick Publishing** is the most common. Pin `page-pdfs
  https://church-bulletin.org/<id>` (`?id=<id>` runs a week ahead; don't pin it). The id is
  in `jppc.net/onlinebulletins/<id>template.pdf` links, the page-8 footer `<id> <Parish>,
  <Town>, NJ (B) … John Patrick Publishing` and self-hosted names `<id><MMDDYY>.pdf`, which
  can zero-pad it (`0667bulletin…` = 667). One account can carry several bulletins as
  letter-suffixed listings (`6051O`, `6051A`) while the bare id is empty and the footer names
  every parish: pin the listing the site links, try other letters when a shared pastor or
  two-parish footer suggests a second bulletin, and read each masthead. To find an unlinked
  listing, grep the saved scans (`029-map/jp-*.tsv`; ids here run 400–799 and 6000–6060)
  for the town or zip, then run `jp_scan.sh`. A listing showing only the week's readings is
  a parish posting nothing: `no_bulletin` with research to recheck, not a `fetch_gap`; so is
  a JP-hosted site lapsed into `cgi-sys/suspendedpage.cgi` or a bare "Index of /" (its last full
  Wayback capture gives the schedule). Campus ministries can hold an empty listing: grep for
  the campus, and keep it in the exclusion's revisit.
- **Bon Venture Services:** sites link `sponsors.bonventure.net/?page=<id>`. Record provider
  `other`, `page-pdfs` and `publication: url:` on that page; names like `2026-11-08..pdf` still date. Self-hosted copies carry the footer
  `<code> · (<initials>) <Parish> · <Town>, NJ … Bon Venture Services`; codes like `142E` have
  no listing, so read the parish's bulletin page.
- **ParishesOnline / LPi:** slugs follow `<name>-church-<zip>`, sometimes without the zip's
  leading zero (`-7105`; try both); `probe po <slug>` gives org, LPi id
  and container: try it before `no_bulletin` and when a site's bulletins are old. The ad-page footer names the container (`<Parish>, <Town>, NJ 03-0374` or `<Parish> |
  04-0064` = `po-container:03/0374`; `probe container` confirms it). WeConnect (Duda) sites
  embed `publicationWidget?…&id=<18-char id>` on `/bulletin`, for `probe po <id>`. When
  guesses fail, `visit.py` on the bulletin page reports `po-org:<slug>` (some lack the zip).
  A current container whose org can't be found: keep `po-container` in `publication`,
  unsupported with fetch_gap `po-org-unknown`, and research.
  A stray template date in the text layer can make fetch:check report freshness `unknown`:
  check the file name and date line.
- **eCatholic behind Cloudflare** answers `probe get` with 403; fetch:check runs headed and
  reads it, so no `fetch_gap`. **Discover Mass** reposts on eCatholic
  (`files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf`, "©2026 Diocesan"): provider
  `ecatholic`, both `ecatholic:` and `discovermass:` ids; Discover Mass caps downloads per IP
  per day.
- **Trinity Publishing** sites link one overwritten `/images/pdf/bulletin.pdf`, often months
  stale: read page 1's date.
- **Wix and Duda:** a Duda `/bulletin` page listing dated PDFs reads with `page-pdfs` on it.
  Otherwise `page-pdfs <homepage>` (`first-listed`) picks the linked PDF, freshness
  `unknown`: confirm it is the bulletin. When a logo or coat-of-arms PDF is listed first and
  undated `_files/ugd/` names allow no glob, record unsupported with fetch_gap
  `first-pdf-not-bulletin`; when undated PDFs are labelled only "Month D" out of date order,
  `first-pdf-not-current` (watch for "coming soon" placeholders under the next date). The
  CDX for `<host>/_files/ugd/` counts uploads: lagging or abandoned? A Wix
  site that is one embedded `filesusr.com/html/<id>.html` app: `probe get` the embed for its
  links (Drive folders read with `provider_id 'drive-folder <URL>'`). **Sitelio** sites
  build links in JavaScript: `visit.py --text --links`, cite by note.
- **Other self-hosted sites** read with `page-pdfs` on the bulletin page or homepage. When
  other PDFs sit beside the issues, filter on what issue names share: Weebly hand-typed names
  (`filename=*_-_*.pdf`), 32-hex upload names (32 `?` + `.pdf`), a two-digit year prefix
  (`26-*.pdf`, set `revisit_after` in late December); freshness reads `unknown`, so add
  research to recheck the glob. Link text is not the file's date (Squarespace `/s/` links
  labelled 2026 pointing at 2025 files): check the picked name gives the issue date.
  WordPress: `wp-json/wp/v2/media?mime_type=application/pdf&per_page=20` lists uploads with
  dates (weekly or sporadic?); an archive of one post per issue reads with `provider_id
  'dated-post <archive URL>'`. Joomla `weblink.go` redirects defeat `page-pdfs` (`probe get`
  one to read it): unsupported, fetch_gap `joomla-weblink-redirect`. A Canva design
  updated in place (`canva.com/design/<id>/…/view`; `visit.py --text`, `#N` for page N):
  unsupported, fetch_gap `canva-design-viewer`, `publication url:` the design. A PDF sent
  only in Constant Contact emails: follow the site's `conta.cc` links to the newest.
- **Institute of Christ the King** oratories post at `institute-christ-king.org/bulletins-<city>`
  (dated `/images/<city>/bulletins/<yyyy>/<MMDDYYYY>.pdf`, newest first): provider `other`,
  `page-pdfs` on that page, website `<city>-home`.
- **Languages:** 83 parishes are tagged Spanish; Korean, Polish, Portuguese and Italian
  communities may print their own bulletins. Korean WordPress MangBoard boards
  (`/jubo/?vid=<n>`) post JPEG pages weekly, often Korean and English editions of one
  bulletin: one row, unsupported, fetch_gap `board-post-images`.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- GoDaddy Website Builder sites (img1.wsimg.com/blobby/... PDFs named 'November 1, 2026.pdf') can repost an LPi bulletin: grep the last page for the '<Parish>, <Town>, NJ 03-xxxx' footer and record the ParishesOnline org, not the copies.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them. None yet; the survey's
proposals are in `scratch/newark-map-1/survey.json` for `survey-review`.

- Eastern Catholic churches GCatholic lists in the territory (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Melkite: Eparchy of Newton; Syro-Malabar, Syro-Malankara, Syriac) are excluded as `other-jurisdiction`, as in Allentown, Scranton, Syracuse and Rochester. (accepted by survey-review, 002-survey-review, 2026-11-03)
- A church with a decreed future closure stays a church row, with `revisit_after` the day after its announced last Mass, and is excluded as `closed` only once that date has passed and a source confirms it (St. Anthony, East Newark: closes 2026-11-23). (accepted by survey-review, 002-survey-review, 2026-11-03)
- Campus chapels (Newman Center Chapel, Montclair State; Seton Hall's Immaculate Conception Chapel) and convent or monastery chapels (Rosary Shrine, Summit; Carmelite chapel, Paramus; St. Cloud) are church rows only when a current schedule shows Mass open to the public; otherwise `no-public-mass`. A campus ministry that posts its own bulletin is its own parish row. (accepted by survey-review, 002-survey-review, 2026-11-03)
- A DEAD-DNS verdict from `probe url` before 2026-11-03's PR #205 is not evidence that a domain is dead; confirm with `probe get` or `visit.py` before recording a lost site. Since that PR, DEAD-DNS means the proxy's resolver found no such host. (accepted by survey-review, 002-survey-review, 2026-11-03; updated by the owner for PR #205, 2026-11-03)
- A parish's Korean (or other language) community that GCatholic lists as a second entry with the same Plus Code as the parish church is linked to that one church row when the parish's schedule includes the community's Masses (GCatholic 18377/18378, St. Joseph, Demarest). (map batch `b-cresskill`, 2026-11-03)
- A Parish Mission Partners group under We Are His Witnesses (2026) is a planning collaboration, not a shared bulletin: record it in `group`, and merge partners' bulletins only when their mastheads show one (the four Westfield/Scotch Plains partners print four). (map batch `j-westfield`, 2026-11-05)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-03: Survey (factory run newark-map-1). Rosters: `gcatholic` 257, `directory` 218.
  `batches.json`: 60 batches, every roster entry assigned; `batches validate` passed. No
  parish, church or exclusion records yet.
