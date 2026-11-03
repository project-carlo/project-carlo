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

No mapped diocese borders Newark except New York, whose record covers one parish and names no
publishers. These lines come from a 26-site sample on 2026-11-03, the first map batches (Bergen
County) and Allentown's and other mapped dioceses' notes.

- **`probe url` says DEAD-DNS for every parish site in this sandbox.** It resolves names
  itself, and the sandbox reaches the web only through a proxy. `probe get` and
  `parish-site-access`'s `visit.py` work; `scratch/newark-map-1/tools/publisher_fingerprint.sh`
  lists the publishers a homepage mentions, but `visit.py` finds some it misses (a
  ParishesOnline org linked only from the bulletin page).
- **Image-only issues are common here** (John Patrick, LPi and eCatholic-hosted alike): read
  pages 1–2 with `render.py` and cite the masthead by note, since recheck can't find quotes
  in them.
- **The publisher's code on the ad or last page identifies a self-hosted bulletin.** Parishes
  here often post their printer's PDF on their own site; read the footer before deciding the
  publisher (formats below).
- **A publisher's widget on a parish site isn't its bulletin.** An eCatholic site can be only
  the website while the bulletin is printed elsewhere: if `issues.py` finds no
  files.ecatholic.com bulletins and the Bulletins menu links ParishesOnline, a
  church-bulletin.org/jppc.net file or sponsors.bonventure.net, record that publisher and
  leave the eCatholic id out of `publication`.
- **John Patrick Publishing** is the most common publisher. Pin
  `page-pdfs https://church-bulletin.org/<id>` (checked in Newark with several ids,
  2026-11-03); `church-bulletin.org/?id=<id>` is often a week ahead of the current issue, so
  don't pin it. A link to `jppc.net/onlinebulletins/<id>template.pdf` gives the id; so does
  the last-page footer `<id> <Parish>, <Town>, NJ (B) … John Patrick Publishing`, and a
  self-hosted copy's file name `<id><MMDDYY>.pdf` (the prefix is the id). A parish's own
  archive can stop months before the listing does, so prefer the listing. In Allentown the
  site answered 406 to a bare "Mozilla/5.0" user agent; plain curl worked.
- **Bon Venture Services:** parish sites link `sponsors.bonventure.net/?page=<id>` from a
  Bulletins menu item or image. Record provider `other` with
  `page-pdfs http://sponsors.bonventure.net/?page=<id>` and `publication: url:` that page, as
  in Scranton; it answers plain `probe get`. File names may carry a double dot
  (`2026-11-08..pdf`); fetch still reads the date. Self-hosted copies with no sponsors link
  carry the ad-page footer `<code> · (<initials>) <Parish> · <Town>, NJ … Bon Venture
  Services`; read the parish's own bulletin page with `page-pdfs`. Codes like `142E` have no
  `?page=` listing (it redirects to bonventure.net).
- **ParishesOnline / LPi:** a self-hosted LPi bulletin's ad-page footer names the container
  (`<Parish>, <Town>, NJ 03-0374` or `<Parish> | 04-0064` = `po-container:03/0374`);
  `probe container` confirms it with no org slug. When guessed org slugs fail, run `visit.py`
  on the parish's bulletin page: it reports `po-org:<slug>` (some have no zip suffix).
  Parishes elsewhere keep empty orgs from old accounts, so read the latest issue before using
  one.
- **eCatholic behind Cloudflare** answers `probe get` with 403; `visit.py` loads it, and
  fetch:check runs headed and reads these rows, so no `fetch_gap` is needed.
- **Trinity Publishing** sites (footer "Powered by Trinity Publishing Company") link one fixed
  `/images/pdf/bulletin.pdf` the parish overwrites; it can be months stale, so read the date
  on page 1 before recording it.
- **Wix and Duda parish sites** often have no bulletin page (Wix: a "WEEKEND BULLETIN" button;
  Duda, irp.cdn-website.com: an empty Google viewer) but link the PDF from the homepage:
  `page-pdfs <homepage>` (fetch:check `first-listed`) picks it. Wix `_files/ugd/` and Duda
  names carry no date, so freshness reads `unknown`: confirm the pick is the bulletin, not a
  letter linked on the same page. Other self-hosted sites (Squarespace, `/images/bulletins/
  bulletinMMDDYY.pdf`) read with `page-pdfs` on the bulletin page.
- **Discover Mass** didn't appear in the sample. Where it does, it caps downloads per IP
  per day (a 134-byte "Maximum number of files" reply in Altoona-Johnstown and Harrisburg).
- **Languages:** 83 parishes are tagged Spanish. Korean, Polish, Portuguese (Ironbound) and
  Italian communities may print bulletins in their own language.
- **Lost domains** (survey, not yet mapped): stfxp.com (St. Francis Xavier, Newark) redirects
  to nabatara.org (HTTP 522); saintnicholaschurch.org answers with 499 bytes and
  stjosephroselle.com with a "Temporarily Unavailable" page; christthekingjerseycity.org and
  holyrosarychurch.com returned nothing.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- Sitelio/mywebsitebuilder parish sites (components.mywebsitebuilder.com/sitelio) build their text and links with JavaScript, so probe get and publisher_fingerprint.sh show nothing; visit.py --text --links reveals the bulletin link (St. Joseph, Lodi linked parishesonline.com/find/<org>). Cite such pages by note, since recheck can't see the text.
- When a parish site is down, the Wayback availability API (probe get http://archive.org/wayback/available?url=<domain>) answers when web.archive.org/web/... gives HTTP 429, and an id_ snapshot shows the site's bulletin menu and Mass times; snapshot fetches hit 429 again after one or two requests, so get the page you need first.
- An LPi bulletin's text layer can carry a stray template date (e.g. 'March 15, 2026') next to the issue date, so fetch:check reports issue_date conflict and freshness unknown even when the pick is current; check the file name and the issue's own date line before treating it as stale.
- An eCatholic parish site can repost its LPi bulletin under files.ecatholic.com/<id>/documents/<yyyy>/<m>/<yyyymmdd>B.pdf (the LPi file name) with nothing under /bulletins/: read the ad-page footer for the container and record parishes_online, leaving the eCatholic id out of publication.
- A self-hosted bulletin page that also lists flyers named '*Bulletin*' needs a filename filter on the issue names; a filter on a two-digit year prefix (26-*.pdf) must be updated each January, so set revisit_after late December.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them. None yet; the survey's
proposals are in `scratch/newark-map-1/survey.json` for `survey-review`.

- Eastern Catholic churches GCatholic lists in the territory (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Melkite: Eparchy of Newton; Syro-Malabar, Syro-Malankara, Syriac) are excluded as `other-jurisdiction`, as in Allentown, Scranton, Syracuse and Rochester. (accepted by survey-review, 002-survey-review, 2026-11-03)
- A church with a decreed future closure stays a church row, with `revisit_after` the day after its announced last Mass, and is excluded as `closed` only once that date has passed and a source confirms it (St. Anthony, East Newark: closes 2026-11-23). (accepted by survey-review, 002-survey-review, 2026-11-03)
- Campus chapels (Newman Center Chapel, Montclair State; Seton Hall's Immaculate Conception Chapel) and convent or monastery chapels (Rosary Shrine, Summit; Carmelite chapel, Paramus; St. Cloud) are church rows only when a current schedule shows Mass open to the public; otherwise `no-public-mass`. A campus ministry that posts its own bulletin is its own parish row. (accepted by survey-review, 002-survey-review, 2026-11-03)
- In this sandbox `probe url`'s DEAD-DNS verdict is not evidence that a domain is dead; confirm with `probe get` or `visit.py` before recording a lost site. (accepted by survey-review, 002-survey-review, 2026-11-03)
- A parish's Korean (or other language) community that GCatholic lists as a second entry with the same Plus Code as the parish church is linked to that one church row when the parish's schedule includes the community's Masses (GCatholic 18377/18378, St. Joseph, Demarest). (map batch `b-cresskill`, 2026-11-03)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-03: Survey (factory run newark-map-1). Rosters: `gcatholic` 257, `directory` 218.
  `batches.json`: 60 batches, every roster entry assigned; `batches validate` passed. No
  parish, church or exclusion records yet.
