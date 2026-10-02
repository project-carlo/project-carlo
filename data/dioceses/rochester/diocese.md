---
name: Roman Catholic Diocese of Rochester
state: NY
website: https://www.dor.org
status: promoted
gcatholic: roch0
promoted: 2026-10-02
---

Twelve counties of western and central New York: Monroe (Rochester), Livingston, Ontario,
Wayne, Seneca, Cayuga, Yates, Steuben, Schuyler, Chemung (Elmira), Tompkins (Ithaca) and
Tioga. The diocese describes itself as 85 parishes. Rochester was the pipeline's first
diocese: its rows were written straight into `data/parishes.csv` and `data/churches.csv`
before diocese records existed, and had never been audited. On 2026-10-02 every live row was
adopted here as a record (same slug, so fetch fixtures and events still match), audited
against a current bulletin in six regions, one agent each, and the rest of the diocese's lists
accounted for. See the *Log* for the numbers.

## Sources

- **Diocesan Directory of Parishes (the best diocesan list):** https://ps.dor.org/directory/,
  a W2DC directory (9 list pages, 90 listings, "Latest update: 1/27/25", "all of the 85
  parishes"). Plain HTML, no Cloudflare, quotable. Each listing
  (`ps.dor.org/directory/<slug>/`) has an "Address:" block with one line per worship site or
  office, clergy and a Mass schedule. Scraped into `rosters/parish-directory.json`, one entry
  per address, named after the listing (the parish), not the building.
  - **Addresses are often offices,** not churches: St. Mary, Geneseo (13 North St is the
    office), St. Luke's "49 Stanley" (the church is 46), Good Shepherd, Henrietta (the sold
    campus, still given as St. Marianne Cope's office), Owego's 309 Front St.
  - **Descriptions lag the address block:** stale pastors (St. Benedict), stale Sunday times,
    Red Creek 6291 vs 6927, St. Agnes "120 Prospect". St. Marianne Cope's text says all Masses
    are at St. Joseph, Rush, which closed in April 2024.
  - **Some listings are junk:** "Holy Family – CLOSED" with no address; St. Mary Our Mother,
    Horseheads at "816 East Broad Street, Rochester"; St. Louis, Pittsford filed in Fairport;
    the Elmira listing still has the closed Ss. Peter and Paul (as 161 High St).
- **Parish Locator and Mass Times (stale):**
  https://www.dor.org/parishes-campuses-cemeteries/parish-locator-and-mass-times/, an HTML
  table of worship sites under headers naming the parish and the diocese's site number (#N),
  plus an "Individual" block of monasteries, Newman centres and Eastern churches. Scraped into
  `rosters/directory.json` (168 rows; ids `<site number>-<site name>`). Years out of date:
  - It lists churches closed since 2005–2021 (Elmira's Lourdes, Ss. Peter and Paul, St.
    Casimir, St. Charles; St. Joseph, Rush; Canisteo) and marks open ones "No Mass" (Newark
    Valley, Apalachin) or "Sacraments Only" (Savannah).
  - Dead or moved links: rc.net/rochester/stjerome (503), holytrinityweb.com, ourladycv.org,
    sjcpenfield.com (parked), marymarthaauburn.org (for sale).
  - Wrong addresses: St. Rose, Lima is given a Brooklyn address ("130 Beach 84th St … 11230
    … Kings"); St. Lawrence "1000 St Lawrence School"; Newark Valley "24 John St" (28 Rock
    St); several house numbers off by a few.
  - Group names collide ("Holy Family" is both the Dansville community and Auburn's former
    cluster; "St. Patrick's", "Holy Cross", "St. Catherine of Siena" recur), so `audit`
    reports groups spanning rows that are unrelated bulletins.
- **GCatholic:** `rosters/gcatholic.json` (key `roch0`), 165 entries with Plus Codes. It
  includes Eastern Catholic churches (Ukrainian, Melkite) and the Ordinariate, still groups
  Elmira churches under parishes that merged in 2021–2023, and carries dead parish domains
  (gatescatholiccommunity.org, holyname-greece.org, stjosephsrush.org) and a junk website
  field ("http://Wolcott"). Plus Codes are usually on the building; exceptions are St. Joseph
  the Carpenter, Campbell (464 m off), St. Benedict, Odessa (671 m), Weedsport and Cato
  (~230–300 m). It swaps the towns of Holy Spirit (Webster) and St. Joseph (Penfield), and
  puts St. Leo, Hilton on Lake Ave.
- **Sacramental-records index (closed and merged parishes):**
  https://www.dor.org/learning-and-living-your-faith/sacraments/sacramental-records/, a table
  of about 145 former parishes and the parish that now holds their records. It says a
  corporation ended, never that a building is shut; St. Ann, Owasco and St. Patrick, Aurora
  are on it and still hold Mass. Parishes on it that are in no roster and no current schedule
  were not given records (St. Andrew, Dundee; Star of the Sea, Greece; St. Feehan, Chili; St.
  Patrick, Mumford; St. Francis, Catatonk; St. Pius X, Van Etten; St. Mary, Greenwood; St.
  Matthias, Atlanta; St. William, Cameron Mills; Cuylerville; Groveland; West Bloomfield;
  Conesus Lake; and others).
- **Campus ministry list:** https://ps.dor.org/pastoral-services-offices-and-ministries/campuses/
  names the parish that serves each campus.
- **News:** the **Catholic Courier** (catholiccourier.com) dates most closures (Corning and
  Painted Post, Elmira 2021, Holy Family Auburn 2024). It sits behind a SiteGround/Cloudflare
  captcha: read it with the parish-site-access `visit.py`; `recheck` reports its quotes as
  no-text. **WHAM** (13wham.com) and **WETM** (mytwintiers.com) cover Gates and Elmira and
  can be fetched with curl.
- **"Churches of Rochester"** (packetduck.duckdns.org/churches/) is a hobbyist site with a
  status, address and closure history per church. Good for leads and house numbers, weak as
  evidence on its own.
- **OpenStreetMap:** `overpass-api.de` resets from the sandbox; `overpass.private.coffee` and
  Nominatim work.

### Bulletin publishers here

About half the rows are ParishesOnline (LPi, containers `06/xxxx` and a few `03/` and
`04/`); the rest are eCatholic, Discover Mass, Google Drive folders and self-hosted pages.

- **Image-only bulletins are common.** Pages with no text layer: Nativity/SEAS, Brockport
  (06/0124); St. Martin de Porres (06/0401); St. Marianne Cope's cover; Holy Spirit/St.
  Joseph's (06/0030, pages 1–9); St. Paul's, Webster; Sts. Mary & Matthew; St. Luke (06/0103,
  pages 1–5); Ss. Isidore & Maria Torribia (04/0677, pages 1–3); St. John Vianney, Bath (all);
  Blessed Trinity, Owego (06/0156); St. Catherine of Siena, Ithaca (03/1311); summer 2026 St.
  Maximilian Kolbe issues. They were read with `render.py`, and evidence `note`s (not
  `quote`s) say so. The pipeline has to read them as images.
- **Broken text layers:** St. Benedict, Canandaigua and St. Peter's, Clifton Springs are
  letter-spaced; quotes copy the extracted text.
- **Cloudflare:** holyspirit-saintjoseph.org stayed blocked even in the browser (its bulletin
  is read from ParishesOnline); theparishoftheholyfamily.org, sttheodoreschurch.com,
  stleohilton.org, stjohnschurchspencerport.org, netcatholic.org, stcathofsiena.org and
  cornellcatholic.org need `visit.py`. pittsfordmendoncatholic.org needs JavaScript.
- **A false squatter alarm:** stpaulsrcc.org is flagged SPAM-SQUAT by `probe url`: the live
  WordPress site carries a hidden block of casino links (it was hacked), alongside the
  current bulletins. The site is the parish's.
- **eCatholic sites that don't host the bulletin:** stlouischurch.org (ecatholic:29150) posts
  its bulletin on ParishesOnline instead.
- **Elmira** posts its bulletin in a DFlip flipbook on elmiracatholic.org (`other`); the same
  bulletin is ParishesOnline container 06/0115, whose organization slug was not found.
- **Sacred Heart, Auburn's** bulletin page has the slug `bulletin__trashed`.
- **All Saints, Corning** held every Mass in the gym at 158 State St in September–October
  2026; the church is 155.
- **Rate limits:** catholicparisheswwc.org answers 429 to rapid fetches.
- **Fetch-check in the sandbox:** Playwright 1.58 looks for Chromium build 1208, the sandbox
  ships 1194. Point `PLAYWRIGHT_BROWSERS_PATH` at a directory whose
  `chromium-1208/chrome-linux64` is a symlink to `/opt/pw-browsers/chromium-1194/chrome-linux`
  (plus empty `INSTALLATION_COMPLETE` and `DEPENDENCIES_VALIDATED` files) and run under
  `xvfb-run`.

## Rules settled for this diocese

- **Adopted rows keep their slugs,** even where the name has moved on (`holy-family` is now
  St. Jude the Apostle Church; `st-mary-star-of-sea` is St. Rose of Lima, Sodus Point; `st-ann`
  is Owasco). Fetch replay fixtures and pipeline events are keyed on them.
- **Clusters with one bulletin are one row:** Holy Spirit + St. Joseph's, Penfield
  (masthead "HOLY SPIRIT - ST. JOSEPH'S"; sjcpenfield.com is parked); St. Mary's, Ss. Mary &
  Martha and Our Lady of the Snow, Auburn (06/0329, five churches); the seven Eastern Wayne
  churches (06/0326); St. Katharine Drexel + St. Maximilian Kolbe; Blessed Trinity + St.
  Patrick, Tioga; N.E.T. Catholic.
- **Shared collaboratives don't make shared bulletins.** "Roc Catholics Northwest" (St.
  Charles Borromeo, St. John, St. Lawrence, St. Mark's, St. Leo, and Holy Cross / Our Mother of
  Sorrows) is recorded in `group`; each member publishes its own bulletin.
- **Monasteries and campus ministries with public Mass and no bulletin are `no-bulletin`:**
  Abbey of the Genesee, Mount Saviour, the Pittsford Carmel, Cornell Catholic Community.
  A Newman community whose Mass is not confirmed by a current source is `open/` (SUNY
  Brockport, SUNY Geneseo).
- **Eastern Catholic churches and the Ordinariate are `other-jurisdiction`.**
- **A church with no Mass in the current schedule, but a source that still lists it and none
  that says it stopped, keeps its row with a dated `revisit`** (St. Patrick, Savannah: the
  January 2025 directory lists a Sunday Mass; St. Rose of Lima, Sodus Point: a summer chapel).
  One with no such source and nothing stating a closure goes to `open/` (St. Casimir, Elmira;
  St. Gregory, Marion; St. Bernard, Scipio Center).

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-02: Documented and audited the whole diocese, then promoted.
  - **Setup:** adopted the 62 parish and 132 church rows that had been written straight into
    the CSVs as records under their live slugs. Scraped the Parish Locator
    (`rosters/directory.json`, 168) and the Directory of Parishes
    (`rosters/parish-directory.json`, 134), and fetched GCatholic (`rosters/gcatholic.json`,
    165). Split by county into six regions (Rochester city; west Monroe; east Monroe and
    Ontario; Wayne, Seneca, Yates and Cayuga; Livingston and Steuben; Chemung, Schuyler,
    Tompkins and Tioga), researched in parallel, one agent each, then merged and linked.
  - **Result:** 63 parish rows (28 ParishesOnline, 19 other, 11 eCatholic, 3 Discover Mass,
    1 Google Drive, 1 no_bulletin) and 130 churches, each with Mass evidence from a September
    or October 2026 bulletin or schedule. Every parish has publication ids.
  - **Exclusions:** 34. 19 closed (Gates: Holy Ghost and St. Helen; Holy Name, Greece; Good
    Shepherd, Henrietta; St. Joseph, Rush; Holy Family, Auburn; St. John, Port Byron;
    Rushville; Stanley; Elmira: Lourdes, Ss. Peter and Paul, St. Charles; Corning St. Vincent;
    Painted Post; Hornell St. Ignatius; Canisteo; Rochester: Holy Redeemer, Holy Rosary, St.
    Joseph on Franklin St). 6 other-jurisdiction (Ukrainian, Melkite, Ordinariate). 6
    no-bulletin (monasteries, Cornell, UR and RIT Newman). 3 no-public-mass.
  - **Open:** 8 (St. Casimir, Elmira; St. Gregory, Marion; St. Bernard, Scipio Center; Padre
    Pio chapel; St. Ann Community; 124 Evergreen St; SUNY Brockport and Geneseo Newman).
  - **Coverage:** directory 168/168, GCatholic 165/165, Directory of Parishes 134/134. One
    church in no roster: St. John's Chapel, Geneva (Sunday 4:30 pm Mass in the Our Lady of
    Peace bulletin). `audit`: 12 groups span rows, each with separate bulletins recorded.
  - **Live rows fixed:**
    - Bulletin source: the Cathedral (`other` to ParishesOnline `the-cathedral-community`);
      Immaculate Conception, Ithaca (`other` to ParishesOnline); Brockport and
      Pittsford/Mendon websites.
    - Cabrini: its Google Drive folder is gone (now `other` at `/faq`, still failing; revisit
      2026-11-01).
    - New row for the St. Kateri Latin Mass Community, which publishes its own bulletin; St.
      Thomas the Apostle moved under it.
    - Removed churches: the Elmira adoration chapel (no Mass) and Holy Family, Auburn
      (closed 16 June 2024).
    - Wrong addresses, mostly an office number instead of the church: Geneseo, Corning,
      Wayland, Perkinsville, Retsof, St. Monica, St. Stanislaus, Savannah.
    - Wrong points: Honeoye was 18.7 km off, Aurora 23 km, Freeville 2.2 km, and six more
      150–310 m off.
    - Renamed: `holy-family` is St. Jude the Apostle; `st-mary-star-of-sea` is St. Rose of
      Lima.
  - **Fetch-check:** before promotion, 61 of the 62 live rows resolved; Cabrini failed, and
    St. Patrick's, Victor failed once and resolved on a re-run. After promotion every changed
    row resolves to its 4 October issue except Cabrini. Their replay fixtures were
    re-recorded.
  - **`recheck`:** quotes found except on Cloudflare- or captcha-blocked pages (Catholic
    Courier, some parish sites, Wix 429s) and image-only bulletins, whose readings are notes.
