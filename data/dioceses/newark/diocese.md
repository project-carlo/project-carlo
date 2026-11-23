---
name: Roman Catholic Archdiocese of Newark
state: NJ
website: https://www.rcan.org
status: promoted
gcatholic: newa0
promoted: 2026-11-05
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

Tools named here are in `scratch/newark-map-1/tools/`. `probe get --out` resolves a relative
path from the worktree root: pass an absolute path.

- **Start a site with `probe url`**: it lists a page's publishers and builder. Open `parish-site-access`'s `visit.py` when it says HTTP4XX or
  NO-PARISH-WORDS or finds no publications. When `visit.py` hangs, `quick_snap.py` loads with
  hard time limits. After UNREACHABLE ('EOF') or `probe pdf`'s RemoteDisconnected, run
  fetch:check (headed) before any `fetch_gap`.
- **Finding a site:** a parish can move domain while the directory and GCatholic keep the
  old one; read the current issue's masthead website line, the ParishesOnline org's website
  field or a JP listing's 'Visit Parish Website' link (when every domain is dead, the listing
  can be the row's website). Guess domains
  (`sjb<town>.org`, `<name><town>nj.org`) and confirm the masthead address. The Wikipedia API (`w/api.php?action=query&list=search&srsearch=…`,
  then `prop=extracts&explaintext=1`) gives merger histories; Bing searches only the first
  word. DuckDuckGo answers `probe get` with a bot check, but
  `visit.py --text` on `html.duckduckgo.com/html/?q=…` returns results. catholicchurch.directory
  keeps old parish domains. A directory entry in no
  other list can be a parish's office across a town line: `diocese search` the name and read
  its JP listing's website and masthead before creating a row.
- **A site that is down or lost:** the Wayback CDX (`probe get
  http://web.archive.org/cdx/search/cdx?url=<host>&matchType=prefix&fl=timestamp,statuscode,length`)
  and `archive.org/wayback/available?url=<domain>` answer when `web.archive.org` gives 429. The CDX dates a lapse:
  ~930-byte captures are an LPi WeConnect site's "temporarily unavailable" page, and the last
  larger capture (`id_` URL) shows the old site. `quick_snap.py` or `visit.py` on
  `web.archive.org/web/<year>/<url>` opens a copy (its HTML can give an eCatholic id).
- **Image-only issues are common** (John Patrick, LPi, eCatholic): read pages 1–2 with
  `render.py` and cite the masthead by note; so is a PDF whose text reads as glyph codes
  (`/0/1/2/i255/…`). A PDF the probe proxy can't reach opens with `visit.py --screenshot`
  (`#page=N&zoom=50`).
- **Read the footer of a self-hosted bulletin** for the printer's code (formats below)
  before deciding the publisher. A parish's own archive or eCatholic and GoDaddy
  (`img1.wsimg.com/blobby/…`) reposts of an LPi bulletin can lag the publisher's listing by
  years: record the publisher, not the copy. A parish can also change printer without changing its links: when an LPi container stops while the parish still
  says "take a bulletin", look for a John Patrick listing.
- **John Patrick Publishing** is the most common. Pin `page-pdfs
  https://church-bulletin.org/<id>` (`?id=<id>` runs a week ahead; don't pin it). The id is
  in `jppc.net/onlinebulletins/<id>template.pdf` links, the page-8 footer `<id> <Parish>,
  <Town>, NJ (B) … John Patrick Publishing` and self-hosted names `<id><MMDDYY>.pdf`, which
  can zero-pad it (`0667bulletin…` = 667). One account can carry several bulletins as
  letter-suffixed listings (`6051O`, `6051A`) while the bare id is empty and the footer names
  every parish: pin the listing the site links, try other letters, and read each masthead. To find an unlinked
  listing, grep the saved scans (`029-map/jp-*.tsv`; ids here run 400–799 and 6000–6060)
  for the town or zip, then run `jp_scan.sh`. A listing showing only the week's readings is
  a parish posting nothing: `no_bulletin` with research to recheck, not a `fetch_gap`; so is
  a JP-hosted site lapsed into `cgi-sys/suspendedpage.cgi` or a bare "Index of /" (its last full
  Wayback capture gives the schedule). Campus ministries can hold an empty listing: grep for
  the campus, and keep it in the exclusion's revisit.
- **Bon Venture Services:** sites link `sponsors.bonventure.net/?page=<id>`. Record provider
  `other`, `page-pdfs` and `publication: url:` on that page. Self-hosted copies carry the footer
  `<code> · (<initials>) <Parish> · <Town>, NJ … Bon Venture Services`; codes like `142E` have
  no listing, so read the parish's bulletin page.
- **ParishesOnline / LPi:** slugs follow `<name>-church-<zip>`, sometimes without the zip's
  leading zero (`-7105`; try both); `probe po <slug>` gives org, LPi id
  and container: try it before `no_bulletin` and when a site's bulletins are old. The ad-page footer names it (`<Parish>, <Town>, NJ 03-0374` or `<Parish> |
  04-0064` = `po-container:03/0374`; `probe container` confirms it). WeConnect (Duda) sites
  embed `publicationWidget?…&id=<18-char id>` on `/bulletin`, for `probe po <id>`. When
  guesses fail, `visit.py` on the bulletin page reports `po-org:<slug>` (some lack the zip).
  A current container whose org can't be found: keep `po-container` in `publication`,
  unsupported with fetch_gap `po-org-unknown`, and research.
- **eCatholic behind Cloudflare** answers `probe get` with 403; fetch:check runs headed and
  reads it, so no `fetch_gap`; `visit.py --html` saves such a page to grep (the Eparchy of
  Passaic's tabbed parish list). A monthly issue dated its first Sunday
  ('Sundays of November 1st, 8th…') makes later weeks 403 and can read stale mid-month: add
  research to recheck after the next issue. **Discover Mass** reposts on eCatholic
  (`files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf`, "©2026 Diocesan"): provider
  `ecatholic`, both `ecatholic:` and `discovermass:` ids; downloads are capped per IP per day.
- **Trinity Publishing** sites link one overwritten `/images/pdf/bulletin.pdf`: read page 1's date.
- **Wix and Duda:** a Duda `/bulletin` page listing dated PDFs reads with `page-pdfs` on it.
  Otherwise `page-pdfs <homepage>` (`first-listed`) picks the linked PDF, freshness
  `unknown`: confirm it is the bulletin. When a logo or coat-of-arms PDF is listed first and
  undated `_files/ugd/` names allow no glob, record unsupported with fetch_gap
  `first-pdf-not-bulletin`; when undated PDFs are labelled only "Month D" out of date order,
  `first-pdf-not-current`. The CDX for `<host>/_files/ugd/` counts uploads. A Wix
  site that is one embedded `filesusr.com/html/<id>.html` app: `probe get` the embed for its
  links (Drive folders read with `provider_id 'drive-folder <URL>'`). **Sitelio** sites
  build links in JavaScript: `visit.py --text --links`, cite by note.
- **Other self-hosted sites** read with `page-pdfs` on the bulletin page or homepage. When
  other PDFs sit beside the issues, filter on what issue names share: Weebly hand-typed names
  (`filename=*_-_*.pdf`), 32-hex upload names (32 `?` + `.pdf`), a two-digit year prefix
  (`26-*.pdf`, set `revisit_after` in late December); freshness reads `unknown`, so add
  research to recheck the glob. Link text is not the file's date: check the picked name.
  WordPress: `wp-json/wp/v2/media?mime_type=application/pdf&per_page=20` lists uploads with
  dates (weekly or sporadic?; `visit.py --text` if the proxy can't reach it). One post
  per issue: pin `provider_id 'dated-post <category URL>'`; unpinned, fetch:check stays on
  the newest post it found. Joomla `weblink.go` redirects defeat `page-pdfs` (`probe get`
  one to read it): unsupported, fetch_gap `joomla-weblink-redirect`. A Canva design
  updated in place (`canva.com/design/<id>/…/view`; `visit.py --text`, `#N` for page N):
  unsupported, fetch_gap `canva-design-viewer`, `publication url:` the design. A PDF sent
  only in Constant Contact emails: follow the site's `conta.cc` links to the newest.
- **Institute of Christ the King** oratories post at `institute-christ-king.org/bulletins-<city>`
  (dated `/images/<city>/bulletins/<yyyy>/<MMDDYYYY>.pdf`, newest first): provider `other`,
  `page-pdfs` on that page, website `<city>-home`.
- **Languages:** Korean, Polish, Portuguese and Italian communities may print their own
  bulletins. Korean WordPress MangBoard boards
  (`/jubo/?vid=<n>`) post JPEG pages weekly, often Korean and English editions of one
  bulletin: one row, unsupported, fetch_gap `board-post-images`.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- Planning areas don't go in `group` (see *Sources*): 171 rows carried `Planning Area <letter>`, and `audit` paired every member of each area (993 unresolved pairs). Reconcile cleared them on 2026-11-05; `group` holds only the Parish Mission Partners groups, whose pairs have masthead-supported `separate` reviews. (reconcile, 2026-11-05)
- A parish site behind Cloudflare that never loads can still give its publisher through the Wayback `id_` capture of its homepage: St. Mary, Rutherford's linked Bon Venture page 1558. (reconcile, 2026-11-05)

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them. None yet; the survey's
proposals are in `scratch/newark-map-1/survey.json` for `survey-review`.

- Eastern Catholic churches GCatholic lists in the territory (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Melkite: Eparchy of Newton; Syro-Malabar, Syro-Malankara, Syriac) are excluded as `other-jurisdiction`, as in Allentown, Scranton, Syracuse and Rochester. (accepted by survey-review, 002-survey-review, 2026-11-03)
- A church with a decreed future closure stays a church row, with `revisit_after` the day after its announced last Mass, and is excluded as `closed` only once that date has passed and a source confirms it (St. Anthony, East Newark: closes 2026-11-23). (accepted by survey-review, 002-survey-review, 2026-11-03)
- Campus chapels (Newman Center Chapel, Montclair State; Seton Hall's Immaculate Conception Chapel) and convent or monastery chapels (Rosary Shrine, Summit; Carmelite chapel, Paramus; St. Cloud) are church rows only when a current schedule shows Mass open to the public; otherwise `no-public-mass`. A campus ministry that posts its own bulletin is its own parish row. (accepted by survey-review, 002-survey-review, 2026-11-03)
- A DEAD-DNS verdict from `probe url` before 2026-11-03's PR #205 is not evidence that a domain is dead; confirm with `probe get` or `visit.py` before recording a lost site. Since that PR, DEAD-DNS means the proxy's resolver found no such host. (accepted by survey-review, 002-survey-review, 2026-11-03; updated by the owner for PR #205, 2026-11-03)
- A parish's Korean (or other language) community that GCatholic lists as a second entry with the same Plus Code as the parish church is linked to that one church row when the parish's schedule includes the community's Masses (GCatholic 18377/18378, St. Joseph, Demarest). (map batch `b-cresskill`, 2026-11-03)
- A Parish Mission Partners group under We Are His Witnesses (2026) is a planning collaboration, not a shared bulletin: record it in `group`, and merge partners' bulletins only when their mastheads show one (the four Westfield/Scotch Plains partners print four). (map batch `j-westfield`, 2026-11-05)
- A convent or monastery chapel with public Mass but no bulletin is a church row under its own
  `no_bulletin` parish row, so it stays in the records while promote leaves it off the site
  (Rosary Shrine, Summit). (map batch `j-summit`, 2026-11-05)

## Seeding precedents

Seed questions `seed-review` settled that no rule covered: the situation, the choice and the parishes. Later reviews in this diocese follow them; only the owner turns one into a rule.

- Record the Forty Hours exposition (Nov 20 after the 7 PM Mass to Nov 22 4 PM, except during Masses) as dated Adoration? → Leave out. Lean kept. Forty Hours runs Nov 20 to Nov 22 4 PM, broken by every Mass. It can't be written as dated entries without inventing day boundaries, and it is over by the time the seed loads. (blessed-miriam-teresa-demjanovich-bayonne s23; 170-seed-review, 2026-11-23)
- The Sunday Portuguese Mass: 6:00 PM (weekly intentions) or 7:00 PM (schedule box and website)? → Sundays 6:00 PM. Lean kept. The dated intentions for Nov 8 and Nov 15 both say 6:00 PM. They are re-edited each week, while the box and website repeat a template (the website still has the old 8:00 AM weekday Mass). Hard: the box in both issues says 7:00 PM. (christ-the-king-hillside s12; 170-seed-review, 2026-11-23)
- Add First Friday Adoration after the 8:30 AM Mass? → First Fridays 9:00 AM. Lean kept. The standing box in both issues puts First Friday Adoration after the 8:30 AM Mass, so R10 times it at 9:00 AM. Neither week holds a first Friday (R11). (christ-the-king-hillside s13; 170-seed-review, 2026-11-23)
- Is the Nov 22 evening Portuguese Mass cancelled for the installation? → Cancel Nov 22 6:00 PM. Lean kept. The newest issue says only one Mass (11 AM) on Nov 22 for the installation, which cancels the evening Portuguese Mass. The time is 6:00 PM, to match the s12 answer. Treated like the other 'only one Mass that day' notices in this batch. (christ-the-king-hillside s16; 170-seed-review, 2026-11-23)
- Is the Mother of Mercy Adoration Chapel at the Corpus Christi church grounds (record its Adoration there)? → Include Mon, Tue, Thu 1-11 PM at Corpus Christi. Lean kept. The parish calls it Eucharistic Adoration with fixed hours (R38). The website puts the parish's chapel at 215 Kipp Ave, on the church's block (260 Boulevard at Kipp). Treated like the other own-chapel-without-an-address cases in this batch: include with a note. (corpus-christi-hasbrouck-heights s14; 170-seed-review, 2026-11-23)
- Saturday Confession: the p1 box says 3:00-3:45 PM, the p3 Sacraments Schedule says 3:00 to 4:00 PM. Which end time? → 3:00-3:45 PM. Lean kept. The p1 Mass Schedule box says 3:00-3:45 PM, which ends before the 4:00 PM Vigil. The p3 3:00-4:00 PM looks like a rounded figure. (divine-mercy-rahway s20; 170-seed-review, 2026-11-23)
- The 2:00 PM Sunday Chinese Mass (all but the second Sunday) names no church. Which church is it at? → Holy Cross. Lean kept. Every Mass except St. Anthony's 12:30 is at Holy Cross, and the website's St. Anthony schedule lists only the 12:30. What was missing: no source names the church. (holy-cross-harrison s13; 170-seed-review, 2026-11-23)
- Add the Saturday 8:30 PM Neo-Catechumenate Liturgy as a public Mass? → Leave out. Lean kept. A Neocatechumenal Way Saturday Eucharist is the Way's communities' own celebration. It has no intentions and is not on the website's weekend list. I decided all six Neocatechumenal Masses in this batch the same way (left out). (holy-family-nutley s14; 170-seed-review, 2026-11-23)
- Add First Friday Adoration, 2:00 to 7:00 PM, in the Mother Cabrini Chapel of the Parish Center? → First Fridays 2-7 PM. Lean kept. The website looks current: its third-Saturday Holy Hour matches both bulletins' Nov 21 entry. Mother Cabrini Chapel is the parish's own chapel, and a Chapel Sanctuary Lamp is among the church's memorials. Hard: no address is given for the Parish Center. (holy-family-nutley s20; 170-seed-review, 2026-11-23)
- Add the third-Saturday Holy Hour for Life, 12:00 to 1:00 PM? → Third Saturdays 12-1 PM. Lean kept. Both bulletins' calendars print it on Nov 21, a third Saturday, and the website gives the monthly pattern and end time. The location is decided as in s20. (holy-family-nutley s21; 170-seed-review, 2026-11-23)
- Add the Rosary Altar Society's first-Monday 7:00 PM Mass? → Leave out. Lean kept. This is a society's meeting Mass and not in the Mass Schedule. November's moved to the second Monday, so the first-Monday pattern is not dependable. (holy-rosary-jersey-city s15; 170-seed-review, 2026-11-23)
- Is the early Sunday Spanish Mass at 8:30 AM or 8:20 AM? → 8:30 AM. Lean kept. The newest issue's own intentions, the older box, the older intentions and the website all say 8:30, so the lone 8:20 in the newest box is a typo. (holy-rosary-st-michael-elizabeth s15; 170-seed-review, 2026-11-23)
- The website lists a First Friday 9:00 AM devotion to the Sacred Heart under 'Eucharist Adoration & Devotions'. Is it Adoration? → Leave out. Lean kept. Only the website names it, as a Sacred Heart devotion under a heading that also covers plain devotions. No exposition or Benediction is stated (POLICY: a devotion not called Adoration is left out). (holy-spirit-union s22; 170-seed-review, 2026-11-23)
- The website lists a First Saturday 9:00 AM devotion to the Immaculate Heart of Mary under 'Eucharist Adoration & Devotions'. Is it Adoration? → Leave out. Lean kept, on the same reasoning as s22: a website-only devotion with no exposition stated. (holy-spirit-union s23; 170-seed-review, 2026-11-23)
- Include the St. Michael Brotherhood Holy Hour (Wed Nov 18, 7–8 PM, Convent Chapel, 20 Pangborn Pl), billed for young men? → Leave out. Against the lean. It is billed to young men ('all young men welcome') by the St. Michael Brotherhood. I left out every men-only or age-group event in this batch alike (st-gabriel men's Mass, little-flower men's gathering, river-edge 55+ Mass). It is also already past (Nov 18). (holy-trinity-hackensack s30; 170-seed-review, 2026-11-23)
- Add Saturday 8:00 AM Adoration before the 8:30 AM Mass? → Saturdays 8:00 AM. Lean kept. The Nov 8 issue words it as a standing weekly schedule, and the Nov 15 issue drops the whole page-2 notice box for a full-page letter rather than cancelling it. What was missing: a second week printing it. (holy-trinity-westfield s14; 170-seed-review, 2026-11-23)
- Is the Sunday mid-morning Mass at 10:00 AM or 11:00 AM? → Sundays 10:00 AM. Lean kept. The ministers' schedules (Oct 24-Nov 15), the Nov 22 and 29 socials after the 10am Mass, and the website (11am only Memorial Day-Labor Day) say 10 AM. The box's 11am looks like the summer schedule left in place. Hard: the Nov 1 and Nov 15 intentions say 11am. (immaculate-conception-norwood s4; 170-seed-review, 2026-11-23)
- Is the Thanksgiving Mass Wednesday Nov 25 or Thursday Nov 26 at 7 PM? → Wednesday, November 25, 7:00 PM. Lean kept. Both notices give the 25th, and the list's weekday (Wednesday) agrees with the date. A 7 PM Thanksgiving Eve Mass is the usual pattern. (immaculate-conception-norwood s12; 170-seed-review, 2026-11-23)
- Are the Immaculate Conception Triduum Masses at 7 PM, as the bulletin says? → 7:00 PM (bulletin). Lean kept. The bulletin's dated 2026 notice says 7 PM on all three days. The website box is probably last year's. (immaculate-conception-norwood s13; 170-seed-review, 2026-11-23)
- Keep Thursday 7:30 PM Exposition, printed only in the Oct 25 issue? → Thursdays 7:30 PM. Lean kept. It is in the parish's standing Sept-May schedule box (Oct 25), whose Masses the website confirms. The newest issue prints no regular schedule at all, so its silence says nothing. (immaculate-heart-of-mary-newark s35; 170-seed-review, 2026-11-23)
- Tue/Thu/Fri Adoration: until 2 pm (bulletins) or 1 pm (website)? → 9 am - 2 pm. Lean kept. Both current bulletins (Nov 8 and Nov 15) say 2 pm. The website page carries pandemic-era material, so its 1 pm is likely the older hours. (immaculate-heart-of-mary-scotch-plains s20; 170-seed-review, 2026-11-23)
- Add the Rosary Altar Society's annual Mass, Tue Dec 1 at 6:30 PM? → Leave out. Lean kept. The Mass opens the Rosary Altar Society's ticketed party, and no venue is given for the Mass itself. Decided like the other society Masses in this batch (left out). (immaculate-heart-of-mary-scotch-plains s23; 170-seed-review, 2026-11-23)
- First-Friday Adoration 'comenzando con la santa misa a las 7:00pm': at what time should it be listed? → First Fridays 7:30 PM (after the 7:00 PM Mass). Lean kept. 'Comenzando con la santa misa a las 7:00pm': exposition follows the Mass, which R10 times 30 minutes after a weekday Mass starts, so 7:30 PM. (immaculate-heart-of-mary-st-patrick-elizabeth s17; 170-seed-review, 2026-11-23)
- Add a dated Mass on Friday Dec 4 at 6:30 AM (First Friday Fellowship men's gathering)? → Leave out. Lean kept. It is a men's group gathering whose Mass has no start time of its own. Decided like the other men-only events in this batch. (little-flower-berkeley-heights s17; 170-seed-review, 2026-11-23)
- Include the 10 AM School Mass on December 8 (Immaculate Conception) in the main church? → Include. Lean kept. The Korean holy day table (p6) puts it in the main church with no limit to students. POLICY: a Mass with a school is open unless the bulletin limits it. (madonna-fort-lee s25; 170-seed-review, 2026-11-23)
- Add a First Friday 7:00 PM Mass? → First Fridays 7 PM. Lean kept. The Nov 1-8 intentions list a 7:00 PM Mass under 'FIRST FRIDAY NOVEMBER 6'. It fits the box, where First Friday Adoration and confession end at 6:50 PM, and nothing contradicts it (C1 does not apply). (most-holy-name-garfield s18; 170-seed-review, 2026-11-23)
- Record the Eucharistic Chapel's Mon-Sat 7 AM-7 PM hours as Adoration? → Leave out. Lean kept. The chapel's hours are listed apart from 'Eucharistic Adoration'. No source calls them Adoration or says where the chapel is (POLICY: a chapel merely open for prayer is not Adoration). (most-holy-name-garfield s19; 170-seed-review, 2026-11-23)
- Do the 'Weekdays' 7:30 AM confessions include Saturday? → Saturday 7:30 AM too. Lean kept. The box's 'Weekdays' Masses run on Saturday per the intentions, so its 'Weekdays' confession includes Saturday. I read 'weekdays' the same way for st-ann-jersey-city, st-rocco and st-vincent-de-paul-bayonne. (most-sacred-heart-of-jesus-wallington s24; 170-seed-review, 2026-11-23)
- Add the website's First Friday overnight Adoration, 7 PM to 7 AM? → Leave out. Lean kept. It is website-only, on a page dated 2025-01-02, and the current homepage schedule (updated 2026-08) omits it. (most-sacred-heart-of-jesus-wallington s28; 170-seed-review, 2026-11-23)
- The weekday 7 AM Mass is dropped 'during the summer months', which the bulletin never dates. How should it be recorded? → Mon-Fri 7 AM every week, no season. Lean kept. 'Summer months' is undated, so R15 gives no season. The Mass is current in both bulletins, and update mode will read the summer change. (notre-dame-north-caldwell s10; 170-seed-review, 2026-11-23)
- Include the Saturday 12:30-2:00 PM confessions with a visiting Opus Dei priest, which need sign-up on the parish website? → Include, with a sign-up note. Lean kept. It is a fixed weekly public window printed in both bulletins. The sign-up reserves a place in it, which is not 'by appointment' with no time. (our-lady-mother-of-the-church-woodcliff-lake s10; 170-seed-review, 2026-11-23)
- Include the Saturday 8:00 PM Neocatechumenal Way Eucharist as a public Mass? → Leave out (Neocatechumenal community's own Eucharist). Lean kept. It is labelled the Neocatechumenal Way's Eucharist and has no intentions. Decided like every Neocatechumenal Mass in this batch (left out). (our-lady-mother-of-the-church-woodcliff-lake s11; 170-seed-review, 2026-11-23)
- The box prints 'Confessions after Mass' under the 7:00 AM weekday Mass. Add Mon-Sat confession at 7:30 AM (POLICY: 30 min after a weekday Mass)? → Mon-Sat 7:30 AM, after the 7:00 AM Mass. Lean kept. 'Confessions after Mass' sits directly under the 7:00 AM weekday Mass, so R10 gives 7:30 AM on its six days. (our-lady-of-czestochowa-harrison s20; 170-seed-review, 2026-11-23)
- Saturday Exposition: ends 3:30 PM or 3:00 PM? → Saturdays 10:00 AM-3:30 PM. Lean kept. The newest English text and the Nov 8 Spanish both say 3:30pm. The newest Spanish '3:00' lacks am/pm and looks like a dropped digit. (our-lady-of-fatima-north-bergen s16; 170-seed-review, 2026-11-23)
- Sunday Confession at 5:00 PM (weekly calendar) or 5:30 PM (front-page box)? → Sundays 5:00 PM. Lean kept. The 'This Week at OLGC' calendar is re-edited each issue and says 5:00 pm every Sunday, while the 5:30 front box is a fixed template. (our-lady-of-good-counsel-washington-township s12; 170-seed-review, 2026-11-23)
- Add the Holy Days box's OLG 12:30 PM Mass on December 8 (Immaculate Conception)? → Dec 8 12:30 PM at OLG. Lean kept. The English Holy Days box prints the OLG 12:30 PM holy-day Mass every week, and Dec 8 is the next holy day the bulletin announces. (our-lady-of-grace-and-st-joseph-hoboken s22; 170-seed-review, 2026-11-23)
- Is the 7:00 PM First Friday Healing Mass (Dec 4) a monthly first-Friday Mass, or one date? → Monthly, first Fridays. Lean kept. POLICY, Weekly or dated rule 2: a service named for a week of the month ('First Friday Healing Mass') is weekly with weeks_of_month even when this month's date is given, unless it says one-time. Hard: it is printed once, on a flyer with a guest prayer team. (our-lady-of-lourdes-mountainside s16; 170-seed-review, 2026-11-23)
- Record the website calendar's 'NO ADORATION' on Thursday, November 26 (Thanksgiving)? → Cancel Nov 26 Adoration. Lean kept. The parish's own calendar otherwise matches the bulletin's Monday and Thursday Adoration and plainly says NO ADORATION on Nov 26. The R16 scope covers it. (our-lady-of-lourdes-mountainside s18; 170-seed-review, 2026-11-23)
- Record the second-Friday 3:00 PM Divine Mercy Chaplet, listed under Eucharistic Adoration, as Adoration? → Leave out. Lean kept. The line names only a Divine Mercy Chaplet, with no exposition or end time. The website's Adoration times omit it (R24: a devotion). (our-lady-of-mercy-park-ridge s26; 170-seed-review, 2026-11-23)
- Include the Monday, December 7, 7:00 PM Mass (Rosary Society meeting Mass, eve of the Immaculate Conception)? → Include Dec 7 7:00 PM Mass. Lean kept. The schedule box gives 7:00pm Holy Day vigil Masses, and Dec 8 2026 is a Tuesday, so the Dec 7 7 PM Mass is the public vigil. The Rosary Society only meets after it. (our-lady-of-mount-carmel-lyndhurst s13; 170-seed-review, 2026-11-23)
- During the 40 Hours Devotion (Nov 18-21), what Adoration hours should be listed? → 9:00 AM - 6:00 PM. Lean kept. The notice says the church is 'open for private prayer and adoration ... until 6:00pm', and a 40 Hours is continuous exposition. Hard: it is unclear whether exposition ends at the noon Benediction. (our-lady-of-mount-carmel-newark s22; 170-seed-review, 2026-11-23)
- Include the Saturday 6:30 PM Neocatechumenal Mass in the Church Hall? → Leave out. Against the lean. A Neocatechumenal Way Mass is the Way's communities' own Eucharist, even when the box prints it. I decided all six such Masses in this batch alike (holy-family-nutley, woodcliff-lake, st-columba, st-francis-de-sales-lodi, st-peter-belleville: all left out). The lean rested only on nothing restricting it. (our-lady-of-mount-carmel-oratory-montclair s10; 170-seed-review, 2026-11-23)
- Add the November 21, 11 AM Anointing of the Sick as a Mass? → Mass on November 21 at 11:00 AM. Lean kept. The parish homepage post calls it 'a mass of anointing of the sick' with all welcome. The RSVP is only for the luncheon. (our-lady-of-peace-new-providence s20; 170-seed-review, 2026-11-23)
- Add first-Saturday Exposition of the Blessed Sacrament after the 8:45 AM Mass (no clock time given)? → Leave out. Lean kept. Exposition is one component of the First Saturday devotion, after the prayers, Chaplet and Rosary. POLICY, Final source checks: the Mass's time does not set a component's time. (our-lady-of-the-blessed-sacrament-roseland s12; 170-seed-review, 2026-11-23)
- Saturday afternoon Confession ends at 3:45 (page 1) or 3:40 (page 2)? → Sat 3:00-3:45 PM. Lean kept. It is the front-page sacrament schedule, the parish's headline listing. The start time is the same either way. (our-lady-of-victories-harrington-park s31; 170-seed-review, 2026-11-23)
- Weekday 5:30 PM Mass: the website says none from mid May to mid September. Record it with a season? → Mid-September to mid-May. Lean kept. The homepage, whose schedule otherwise matches the bulletin, says there is no 5:30 PM Mass 'from mid May to mid Sept'. The 15th approximates 'mid', and the season is exact for the months ahead. (queen-of-peace-north-arlington s23; 170-seed-review, 2026-11-23)
- Cancel the regular Friday 8:00 AM Mass on Nov 27 (day after Thanksgiving), when the bulletin lists a 9am Mass? → Cancel 8 AM on Nov 27. Lean kept. The bulletin's standing rule moves 8am to 9am on holidays, and it treats Nov 27 as one (9am Mass, office closed). That is a stated move, not an inferred one (R17). (sacred-heart-bloomfield s21; 170-seed-review, 2026-11-23)
- Include weekday confession after the 12:00 PM Mass, offered upon request, at 12:30 PM? → Mon-Fri 12:30 PM, upon request. Lean kept. Per C5, confession after Mass on request gets POLICY's time: 12:30 PM after the 12:00 PM weekday Mass. (sacred-heart-lyndhurst s14; 170-seed-review, 2026-11-23)
- On first Fridays, is the regular Friday 6:30 PM Mass still held, or replaced by the 6:30 PM Holy Hour and 7:30 PM Mass? → Fridays 6:30 PM except first Fridays. Lean kept. Per C4, the First Friday 6:30 PM Holy Hour takes the regular Mass's hour, with Mass following at 7:30 PM. (sacred-heart-of-jesus-irvington s10; 170-seed-review, 2026-11-23)
- The box says 'Week Days: 7:30 A.M.' but both weeks' intentions list only the 6:30 PM Mass on Tuesday and Friday. Add a 7:30 AM Mass on Tuesday and Friday? → Leave out. Lean kept. Both weeks' intentions list only the 6:30 PM Mass on Tuesday and Friday. That reads as the evening Mass replacing the morning one on those days. (sacred-heart-of-jesus-irvington s11; 170-seed-review, 2026-11-23)
- Add confession 20 minutes before each weekend Mass, which only the website gives? → Leave out. Lean kept. It is website-only. Both bulletins' Schedule of Events list each Saturday's 9:00-9:30 confession and never a pre-Mass one, and it is unclear which churches 'all the weekend Masses' covers. (st-adalbert-sts-peter-paul-elizabeth s13; 170-seed-review, 2026-11-23)
- Add a first-Friday 7:00 PM Mass at St. Adalbert, which only the website gives? → First Fridays 7:00 PM. Lean kept. The website's other times match both bulletins exactly, and neither bulletin's week holds a first Friday, so they can't contradict it (R6, R11). (st-adalbert-sts-peter-paul-elizabeth s18; 170-seed-review, 2026-11-23)
- Add the website's seasonal Benediction devotions (October, May, June) at St. Adalbert? → Include as seasonal Adoration. Lean kept. Benediction devotions on the website, whose times otherwise match the bulletins; the season keeps them to the stated months. What was missing: no bulletin can confirm them in November. (st-adalbert-sts-peter-paul-elizabeth s19; 170-seed-review, 2026-11-23)
- Where are the Dec 11 Guadalupe Exposition (8 PM) and Vigil Mass (9 PM)? → St. Aedan's Church. Lean kept. A vigil Mass with mariachis until midnight points to the church, not the small center chapel. What was missing: the program names no place. (st-aedan-jersey-city s25; 170-seed-review, 2026-11-23)
- Where is the Dec 12 Guadalupe 7 PM Mass (after the parishes' pilgrimage)? → St. Aedan's Church. Lean kept. A five-parish pilgrimage Mass would fill the church. The program places only the fiesta, in the Hudson Catholic cafeteria. (st-aedan-jersey-city s27; 170-seed-review, 2026-11-23)
- Add Adoration 9-10 AM on the other Saturdays, as the website says? → Leave out (bulletin says 1st Saturday only). Lean kept. Both current bulletins limit Eucharistic Adoration to the 1st Saturday, and that newer, specific statement wins over the website's every Saturday. (st-aloysius-jersey-city s21; 170-seed-review, 2026-11-23)
- Cancel the 7:00 and 8:30 AM Masses on Thanksgiving, November 26? → Cancel (only one Mass that day). Lean kept. 'One Mass will be celebrated' on Thanksgiving replaces the usual two Thursday Masses. I decided every 'only one Mass that day' notice in this batch as a cancellation. (st-aloysius-jersey-city s23; 170-seed-review, 2026-11-23)
- Are confessions also heard after the Saturday 7:00 AM Mass? → Saturdays 7:30 AM. Lean kept. The bulletin groups Saturday 7 AM with the Monday-Saturday daily Masses. I read 'weekday' to include Saturday here, as for wallington, st-rocco and st-vincent-de-paul-bayonne. (st-ann-jersey-city s14; 170-seed-review, 2026-11-23)
- Include first-Friday Adoration 1:00-2:00 PM, which the bulletin says is 'generally' held? → First Fridays 1:00-2:00 PM. Lean kept. It is a standing timed monthly line in both issues. 'Generally' hedges the occasional skip, not the time. (st-anne-fair-lawn s18; 170-seed-review, 2026-11-23)
- Include Tuesday Adoration 8:30 AM-12:00 PM with Benediction at the 'Little House'? → Tuesdays 8:30 AM-12:00 PM at the church. Lean kept. The website lists it in the church's weekday schedule as 'following' the 8 AM Mass, so the Little House is taken to be on the grounds. Hard: no source gives its address. (st-anthony-of-padua-belleville s22; 170-seed-review, 2026-11-23)
- Include confession 'by request, after Mass' on mornings (Sun-Sat) at the times POLICY works out? → Include, by request after the morning Mass. Lean kept. Per C5, 'by request, after Mass' is timed by R10 at 9:30 after the 9:00 AM Mass. (st-bernard-st-stanislaus-plainfield s13; 170-seed-review, 2026-11-23)
- Add confession on request after each weekday Mass (Mon-Fri 7:30 and 8:30 AM)? → After weekday Masses, on request. Lean kept. Per C5, confession on request after each weekday Mass is timed by R10. (st-casimir-newark s20; 170-seed-review, 2026-11-23)
- Add Saturday 5:00-6:00 PM Confession at the church (website only)? → Saturdays 5:00-6:00 PM. Lean kept. The website's schedule matches every Mass in the Nov 15 bulletin. The bulletin box lists only the confession windows tied to the Mon/Tue/Fri Spanish Masses, which is an omission, not a conflict (R6). (st-catherine-of-siena-hillside s24; 170-seed-review, 2026-11-23)
- Where are the Saturday 4:00-5:00 PM confessions: the church or the Parish Center chapel? → St. Cecilia Church. Lean kept. It runs up to the 5:00 PM vigil at the church, and the box labels chapel services 'Chapel'. (st-cecilia-kearny s14; 170-seed-review, 2026-11-23)
- Include the Neocatechumenal Way's Saturday 6:00 PM and 8:00 PM Eucharistic Liturgies as public Masses at St. Columba? → Leave out. Lean kept. These are Neocatechumenal Way Eucharists under the Way's heading, never in the intentions. Decided like every Neocatechumenal Mass in this batch. (st-columba-newark s10; 170-seed-review, 2026-11-23)
- Include the Saturday 8:30 AM Mass, which the website places in the convent chapel? → Saturdays 8:30 AM, convent chapel. Lean kept. It is a public parish Mass in the intentions each Saturday, in the parish's own convent. Treated like the other own-convent chapels in this batch. Hard: no address for the convent. (st-francis-de-sales-lodi s19; 170-seed-review, 2026-11-23)
- Include the Saturday 8:30 PM Neocatechumenal Way Mass? → Leave out. Lean kept. It is the Neocatechumenal communities' own Eucharist, never in the intentions. Decided like every Neocatechumenal Mass in this batch. (st-francis-de-sales-lodi s20; 170-seed-review, 2026-11-23)
- Cancel the 7:30 AM weekday Mass on Thanksgiving Day, Thursday Nov 26, 2026? → Cancel Nov 26 7:30 AM. Lean kept. 'Friday ... will ALSO be at 9:00 AM and not at 7:30 AM' says Thanksgiving's Mass likewise replaces the 7:30. Consistent with the batch's other one-Mass holiday cancellations. (st-francis-of-assisi-ridgefield-park s17; 170-seed-review, 2026-11-23)
- Add a weekly Thursday 7:00 PM Mass? It appears only as a blank line in the Mass intentions. → Leave out. Lean kept. A blank 7:00 pm intentions line contradicts the p1 box, whose weekday Masses are mornings only. The same list also carries a non-Mass devotion (R39). (st-francis-xavier-newark s31; 170-seed-review, 2026-11-23)
- Add the Knights' Men's Mass on Saturday, November 21 at 8:00 AM? → Leave out. Lean kept. It is the Knights' men's Mass and is not in the Nov 21 intentions. Decided like the other men-only events. (st-gabriel-the-archangel-saddle-river s17; 170-seed-review, 2026-11-23)
- Add a first-Friday Holy Hour after the 8 PM Mass (8:30 PM by POLICY)? → First Fridays 8:30 PM. Lean kept. The standing p1 line in both issues reads 'Holy Hour: 1st Friday after 8 pm Mass', which R10 times at 8:30 PM. (st-james-newark s15; 170-seed-review, 2026-11-23)
- Add a first-Friday 8 PM Mass, implied only by the Holy Hour line? → First Fridays 8 PM. Against the lean. The same standing line in both issues ('1st Friday after 8 pm Mass') states a first-Friday 8 PM Mass. Including the Holy Hour it is timed from (s15) while leaving out the Mass would be inconsistent. Friday's 8 PM Rosary is on a non-first Friday. (st-james-newark s16; 170-seed-review, 2026-11-23)
- Wednesday Adoration: the schedule box says 10 AM-5 PM, the weekly announcements say after the 9:30 AM Mass to 6:30 PM. Which hours? → Wednesdays 10:00 AM-6:30 PM. Lean kept. The dated weekly announcement repeats 'until 6:30' in both issues, tied to the 6:30 chaplet before the 7 PM Mass. The 5 PM box matches a stale website. (st-john-paul-ii-bayonne s22; 170-seed-review, 2026-11-23)
- Add a Christmas 'Midnight Mass' on December 25 at 12:00 AM? → Leave out. Lean kept. Named only in an envelope appeal with no clock time. Update mode will read the Christmas schedule. (st-john-paul-ii-bayonne s23; 170-seed-review, 2026-11-23)
- Record the Perpetual Eucharistic Adoration Chapel as Adoration all day, every day (00:00-23:59) at St. John the Apostle Church? → Every day 12:00 AM-11:59 PM. Lean kept. The website says 'Perpetual Adoration 24 hours a day' in 'St. John the Apostle's Adoration Chapel' (sign-up updated 9/17/2026), and the parish has one address, 1805 Penbrook Terrace. (st-john-the-apostle-linden s19; 170-seed-review, 2026-11-23)
- Is 'Sunday: Adoration & Masses will be in the Church from 9 am until 1 pm' a Sunday Adoration time? → Leave out. Lean kept. The line spans the Sunday Masses and reads as services moving to the Church. No exposition hours are stated apart from the Masses. (st-john-the-baptist-jersey-city s22; 170-seed-review, 2026-11-23)
- Add the Christmas Eve 10 PM 'Midnight Mass' mentioned in the raffle notice? → Dec 24 10 PM Mass. Lean kept. A clear date and time (Dec 24, 10 PM) at the parish's only church. Unlike st-john-paul-ii-bayonne s23, a clock time is printed. (st-john-the-baptist-jersey-city s24; 170-seed-review, 2026-11-23)
- Add the monthly Tagalog Mass at 5:30 PM, and on which Sunday? → Leave out. Lean kept. The website contradicts itself (first vs third Sunday), and the newest issue covers a third Sunday with no 5:30 PM Mass in its intentions. (st-john-the-evangelist-bergenfield s36; 170-seed-review, 2026-11-23)
- Keep the first-Sunday 11:30-11:50 AM Confession, which now coincides with the 11:30 AM Spanish Mass? → Leave out. Lean kept. The line matched the former 12:00 Spanish Mass and now overlaps the 11:30 Mass itself, so it is stale. (st-joseph-bogota s14; 170-seed-review, 2026-11-23)
- Which weekday Adoration hours at St. Joseph? → Exposition 8:30-9:30 AM. Lean kept. Exposition 8:30-9:30 'open to public' is the hour both pages support. The 8:30-2 Adoration Chapel hours need the chapel located (POLICY, Churches and chapels). (st-joseph-bogota s15; 170-seed-review, 2026-11-23)
- Add the Advent evening Mass, Mondays and Tuesdays 7 PM from November 30 through Advent? → Mon & Tue 7 PM, Nov 30-Dec 24. Lean kept. The start date (Nov 30) is printed, and the season ends with Advent this year. Hard: Advent's dates move, so the season won't fit 2027, but it is exact for the period this seed covers. (st-joseph-bogota s21; 170-seed-review, 2026-11-23)
- Friday morning Adoration ends at 7:25 or 7:30 AM? → Fridays 7:00-7:25 AM. Lean kept. The specific p2 Adoration notice says 7:25, which closes exposition before the 7:30 AM Mass. (st-joseph-east-rutherford s14; 170-seed-review, 2026-11-23)
- Friday morning Confession ends at 7:25 or 7:30 AM? → Fridays 7:00-7:25 AM. Lean kept. The front-page box says 7-7:25, and the priest says the 7:30 AM Mass. (st-joseph-east-rutherford s15; 170-seed-review, 2026-11-23)
- Add Confession after each Mass, at the time POLICY works out from Before and after Holy Mass? → Leave out. Lean kept. 'Before and after Holy Mass' describes general availability, not a timed window. Unlike the C5 cases, it is not an after-Mass request line. (st-joseph-hackensack s15; 170-seed-review, 2026-11-23)
- On Fri Nov 27 the bulletin says 'One Mass will be celebrated at 9:00 a.m.' Record the usual 8:30 AM and 7 PM Masses that day as cancelled? → Cancel that date. Lean kept. 'One Mass will be celebrated at 9:00 a.m.' on Nov 27, and the intentions list only 9:00am. Consistent with the batch's other one-Mass holiday cancellations. (st-joseph-of-the-palisades-west-new-york s37; 170-seed-review, 2026-11-23)
- Add Confession after each Mass, which the bulletin says 'may be requested after Mass'? → After each Mass on request (POLICY timing). Lean kept. Per C5, 'may be requested after Mass' is on request, not by appointment, and is timed by R10. (st-lawrence-weehawken s13; 170-seed-review, 2026-11-23)
- Is the Thursday 7 PM 'Grupo De Oración Hora Santa' a public Holy Hour (Adoration) at St. Leo Church? → Leave out. Against the lean. It is a prayer group's Thursday meeting in the calendar, with no exposition, end time or place stated; the other Thursday groups meet in the rectory basement. POLICY leaves out an event whose location is unclear, and calling a group's Hora Santa Adoration is not enough. (st-leo-elmwood-park s11; 170-seed-review, 2026-11-23)
- Was there a 7 PM Mass on Tuesday, November 17? → Leave out. Lean kept. Only the Rosary flyer mentions the Mass. The same bulletin's calendar and intentions (12:10 PM only) do not, and the date has passed. (st-leo-elmwood-park s12; 170-seed-review, 2026-11-23)
- Is St. Boniface Chapel at St. Mary's church (254 Second St), so its Monday and Wednesday evening Adoration belongs there? → Include at St. Mary's. Lean kept. St. Boniface Chapel is listed under the church's address in the DAILY MASSES box, and a group meets there 'after 7AM Mass', so it is on site. (st-mary-jersey-city s21; 170-seed-review, 2026-11-23)
- Add the Immaculate Conception (Tue Dec 8) Masses at 12 noon and 7 PM? → Dec 8 at 12 noon and 7 PM. Lean kept. The holy-day box's 'Monday, December 8' is carried over from 2025. Its 'Tuesday' line is Dec 8, 2026. (st-mary-rutherford s13; 170-seed-review, 2026-11-23)
- Confessions Mon, Tue, Thu, Fri: the bulletin (both issues) gives 9-12 and 2-6 with 'Suggest to call first'; the website gives 10-11:30 and 3-6 'or by appointment'. Which hours? → Bulletin hours. Lean kept. The bulletin hours are printed identically in both issues and are newer than the undated web page. 'Suggest to call first' is kept as a note (C5). (st-michael-newark s21; 170-seed-review, 2026-11-23)
- Include the Mon-Fri 12:00 noon Mass 'at the convent building' at St. Nicholas? → Mon-Fri 12:00 PM at St. Nicholas. Against the lean. This is the parish's only weekday Mass, in its own convent: the time is certain in both bulletins, the intentions and the website. I treated it like the other own-convent and own-chapel venues without an address in this batch (st-paul-the-apostle-jc, st-stanislaus-kostka, st-francis-de-sales-lodi, st-rose-of-lima): include with a note. Leave out if the convent is not at 122 Ferry St. (st-nicholas-jersey-city s6; 170-seed-review, 2026-11-23)
- Add a weekly Thursday 7:00 PM Mass from the blank intentions line? → Leave out. Lean kept. A blank intentions line contradicts the p3 Eucharist schedule and website, which give noon only (R39, C1). Decided like st-francis-xavier-newark s31. (st-nicholas-jersey-city s11; 170-seed-review, 2026-11-23)
- Include the Mon–Sat 8 AM Mass in the parish's (convent) chapel, and Confession 7:30 before it, at St. Paul the Apostle? → Include at St. Paul the Apostle. Lean kept. The bulletin treats 'the Chapel' as a parish venue beside the Church and Social Center, and the intentions list 8:00AM daily. Treated like the other own-convent chapels in this batch. (st-paul-the-apostle-jersey-city s13; 170-seed-review, 2026-11-23)
- Add the First Friday 7:30 PM Spanish Holy Hour at St. Peter's church? → First Fridays 7:30 PM at St. Peter. Lean kept. The parish schedule box names the Convent Chapel only where it applies (Wednesday). The Holy Hour has no place stated, so it is at the church. (st-peter-belleville s16; 170-seed-review, 2026-11-23)
- Add the Saturday 7:30 PM 'NCW Eucharist' as a public Mass? → Leave out. Lean kept. 'NCW Eucharist' appears only in Parish Events, never in the Mass box or intentions. Decided like every Neocatechumenal Mass in this batch. (st-peter-belleville s20; 170-seed-review, 2026-11-23)
- Add the Advent confessions, 20 minutes before each Mass, November 29 - December 23? → Advent only (Nov 29 - Dec 23). Lean kept. '20 minutes before Mass' is a definite time, and the season fits this Advent exactly. Same handling as st-joseph-bogota's Advent Mass. (st-peter-the-apostle-river-edge s28; 170-seed-review, 2026-11-23)
- First Friday Adoration in the chapel: which hours? → 10:00 AM - 3:00 PM. Lean kept. The website's standing Masses page gives a clock time (10:00 AM - 3:00 PM). Hard: its Dec 4 event page says 'following the 9am Mass' (9:30). (st-peter-the-apostle-river-edge s37; 170-seed-review, 2026-11-23)
- Add the 55+ parishioners' Mass on Tuesday, November 17 at 11:30 AM? → Leave out. Against the lean. It is 'for our 55+ Parishioners' with a lunch. I left out every event billed to an age or men's group alike (holy-trinity-hackensack, st-gabriel, little-flower). C7 needs a heading saying all events are open, and there is none. It is also past (Nov 17). (st-peter-the-apostle-river-edge s38; 170-seed-review, 2026-11-23)
- Tuesday 6:00 PM Mass: the schedule says to check the bulletin for it; Nov 10 had one, Nov 17 did not. Add it weekly? → Leave out (not every Tuesday; update mode records dated ones). Lean kept. Both sources say to check the week's schedule. Nov 10 had it and Nov 17 did not, so a weekly slot would be false (R33). (st-rocco-st-brigid-union-city s13; 170-seed-review, 2026-11-23)
- Confession after the Saturday 9:00 AM Mass? The bulletin says 'after 9:00am weekdays', the website 'daily after the 9 am Mass'. → Saturday 9:30 AM. Lean kept. The website says 'daily after the 9 am Mass', and Saturday has a 9 AM Mass. Same 'weekdays' reading as wallington and st-ann. (st-rocco-st-brigid-union-city s20; 170-seed-review, 2026-11-23)
- Include the Mon/Tue/Wed/Fri 6-7 PM Adoration 'in rectory chapel' at St. Rose of Lima church? → Include at the church, note Rectory chapel. Lean kept. The bulletin gives one address (11 Gray St) for the parish and rectory, so the rectory chapel is on the grounds. What was missing: an explicit rectory address. (st-rose-of-lima-newark s12; 170-seed-review, 2026-11-23)
- On first Thursdays and Fridays, does the 6:30-7:30 PM Confession replace the regular 6:30-6:55 PM one? → Yes: regular 6:30-6:55 PM on other weeks only. Lean kept. Per C4, the first-week 6:30-7:30 window covers the regular 6:30-6:55 one, so the regular one runs on the other weeks only. (st-stanislaus-kostka-garfield s35; 170-seed-review, 2026-11-23)
- Include the convent Adoration Chapel's Mon-Sat 7 AM-7 PM hours at St. Stanislaus Kostka Church? → Include at the church, noted as the convent chapel. Lean kept. It is the parish's own convent Adoration Chapel, in the box of both bulletins and on the website (R38), with no other address. Treated like the other own-convent chapels. (st-stanislaus-kostka-garfield s39; 170-seed-review, 2026-11-23)
- Confession before the Monday and Friday 7 PM Masses (6:30-7:00 PM)? The homepage says half hour before each Mass, Mon-Sun; the sacraments page says Mon-Sat 7:00-7:25am, when there is no Mon/Fri Mass. → 6:30-7:00 PM. Lean kept. The homepage's Mass block matches the current bulletins' 7 PM Mon/Fri Masses. The sacraments page's 7 AM is written for a morning schedule. (st-stanislaus-newark s24; 170-seed-review, 2026-11-23)
- Pope Francis Hall is 'below the Parish Office' at 1 Munn Street, not the church's 30 N Fullerton Ave address. Include the Mon-Fri 12:00 PM daily Mass at Immaculate Conception? → Include at Immaculate Conception, note Pope Francis Hall. Lean kept. It is the parish's only weekday Mass, in Pope Francis Hall 'below the Parish Office' at 1 Munn St. That is taken to be the church campus at 30 N Fullerton Ave. Hard: a different street address. Leave out if the hall is a separate site. (st-teresa-of-calcutta-montclair s7; 170-seed-review, 2026-11-23)
- Add weekday Confession after each weekday Mass ('After All Masses. Always Upon Request')? → After each weekday Mass (30 min after it starts). Lean kept. Per C5, 'After All Masses. Always Upon Request' is on request, not by appointment, and is timed by R10. (st-theresa-kenilworth s20; 170-seed-review, 2026-11-23)
- Monday Adoration ends at 6:15 PM (weekly calendar) or 6:30 PM (schedule box)? → Mondays 12:30-6:15 PM in the Chapel. Lean kept. The dated Monday listing in both weeks says 6:15 PM, which ends before the 6:30 PM Mass. (st-theresa-kenilworth s31; 170-seed-review, 2026-11-23)
- Add the website's Spanish Mass, third Sundays 3:00 PM, which the bulletins never print? → Third Sundays 3:00 PM (Spanish). Lean kept. The website is current (this week's reflection, (c) 2026) and lists the Spanish Mass with the Italian one the bulletins confirm. Hard: the Nov 15 (third Sunday) intentions omit it, though a Spanish Mass may carry no intention. (st-theresa-kenilworth s32; 170-seed-review, 2026-11-23)
- Does 'Adoration after 8am week day masses until 9am' include Saturday? → Saturday 8:30-9:00 AM too. Lean kept. The box lists Saturday 8am under Daily Mass (Monday - Saturday), so 'week day masses' includes it. Same reading as the batch's other weekday-Saturday questions. (st-vincent-de-paul-bayonne s18; 170-seed-review, 2026-11-23)
- First Friday all-night Adoration runs from after the 7 PM Mass to the 8 AM Saturday Mass. How should it be recorded? → First Fridays from 7:30 PM, no end time. Lean kept. Both bulletins (1f306ea7 p3, 107ef15e p3) print 'Every First Friday of the month ... all night Adoration ... begins following the 7:00PM Mass on Friday and concludes with Holy Mass at 8:00AM on Saturday'. It is a standing monthly service, so R10 times its start at 7:30 PM. An end of 08:00 on a Friday slot would read as ending before it starts, so the slot has no end and a note gives the end. s28 now skips first Fridays, so leaving this out would leave first Fridays with no evening Adoration. Option 1's label ('the weekly slot covers its start') is no longer true. This differs from the Forty Hours precedent, which was a one-time event already over and had no clean start. Hard: the format can't show an end time on the next day. (st-theresa-of-the-child-jesus-linden s34; 171-seed-review, 2026-11-23)


## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-05: Reconcile (factory run newark-map-1), after 60 map batches of usually 8 roster entries (4 to 10). Coverage: `directory` 218/218 accounted for, 186/216 modelled (86%); `gcatholic` 257/257, 190/225 modelled (84%). No merges. Linked directory:134 (St. Anthony of Padua's Newark office) to `st-anthony-of-padua-belleville`; listed `st-augustine-newark` in `st-columba-newark`'s worship sites (the batch had already made it that row's church). St. Mary, Rutherford found on Bon Venture page 1558 (was `no_bulletin`); St. Anthony of Padua, Belleville repinned to John Patrick 644. Cleared the planning-area `group` on 171 rows, set the Teaneck-Bogota and Transfiguration-St. Antoninus partner groups, recorded `separate` reviews for the four Bayonne partners: audit 38 pairs, all separate. Six `open/` records retried, none settled. Fetch check: 184 rows, 180 ok on the first run, 3 more on retry; Presentation (Upper Saddle River) still times out in the browser; stale as documented: Holy Family (Union City), Our Lady of the Valley (Orange), St. Stanislaus (Newark), St. Mary (Plainfield).

- 2026-11-03: Survey (factory run newark-map-1). Rosters: `gcatholic` 257, `directory` 218.
  `batches.json`: 60 batches, every roster entry assigned; `batches validate` passed. No
  parish, church or exclusion records yet.
