---
name: Roman Catholic Diocese of Norwich
state: CT
website: https://www.norwichdiocese.org
status: promoted
gcatholic: norw0
promoted: 2026-11-14
---

Four counties of eastern Connecticut, plus Fishers Island, New York: **New London** (Norwich,
New London, Groton, Mystic, Stonington and Pawcatuck, Waterford, Montville and Uncasville,
the Lymes and Niantic, Colchester, Lebanon, Jewett City, Preston, Voluntown), **Windham**
(Willimantic, Putnam, Thompson, Pomfret, Brooklyn, Danielson, Plainfield and Moosup,
Canterbury), **Tolland** (Rockville and Vernon, Tolland, Ellington, Somers, Stafford Springs,
Coventry, Storrs and Mansfield, Bolton, Columbia, Hebron, Ashford) and **Middlesex**
(Middletown, Cromwell, Portland, East Hampton and Moodus, Haddam, Durham, Middlefield,
Killingworth, Chester, Essex, Old Saybrook, Westbrook, Clinton). Neighbours: the Archdiocese
of Hartford to the west, Springfield and Worcester (Massachusetts) to the north, Providence
(Rhode Island) to the east, and Rockville Centre across the Sound from Fishers Island. None of
them is mapped yet (2026-11-14). The diocese's "Reorganization" page
(norwichdiocese.org/Reorganization, read 2026-11-14) is its confirmed joint Chapter 11 plan
for abuse claims, not a parish restructuring.

**How it is organised.** About **50 canonical parishes and some 74 open places** in four
deaneries (the March 2026 list below: 88 entries less 14 marked closed, so 71 churches, 2
missions and 1 chapel; count made from it, the diocese states no figure. The locator map has
75, the same 74 plus closed St. Thomas More; GCatholic has 73 open Latin churches and omits the
cathedral). Two
kinds of grouping, both named in the list:

- **Merged parishes** with several churches: St. Andre Bessette (Plainfield, Moosup,
  Canterbury), St. Therese of Lisieux (Putnam, Pomfret, North Grosvenordale, Quinebaug),
  Corpus Christi (two Willimantic churches and Sagrado Corazon, Windham), Our Lady Queen of
  Peace (Coventry, Storrs), Good Shepherd (Columbia, Hebron), Guardian Angels (Colchester,
  Lebanon), Blessed Sacrament (Rockville, Tolland), Our Lady of Mercy (Durham, Middlefield),
  St. John Paul II (East Hampton, Moodus), St. Teresa of Calcutta (Chester, Essex), St. Pio
  (Old Saybrook, Westbrook), Divine Mercy (Uncasville, Quaker Hill, Oakdale), St. Brendan the
  Navigator (two New London churches, Waterford, Fishers Island) and St. Michael (Pawcatuck,
  Stonington). Each probably publishes one bulletin, but that is for the map jobs to read.
- **Yoked parishes** that keep their own corporation under one pastor: Baltic, Occum and
  Taftville (the "Saint Anne cluster", one website); the three Groton-area parishes (a
  "Tri-Parish Community" bulletin on ParishesOnline); Jewett City, Preston and Voluntown;
  St. Joseph Norwich with Sacred Heart Norwichtown; St. Mary with Ss. Peter & Paul, Norwich;
  St. Agnes Niantic with St. Matthias East Lyme; Higganum with Killingworth; St. John with
  St. Sebastian, Middletown; St. Maurice, Bolton with Good Shepherd. These are where shared
  bulletins are most likely and are recorded as `group` in `rosters/directory.json`.

Missions with Mass: Our Lady of Lourdes, Hampton (of Brooklyn), St. John, Fitchville (of
Sacred Heart, Norwichtown) and the summer St. Francis Chapel, Crescent Beach (of St. Agnes).
The survey (Run norwich-map-1, 2026-11-14) planned nine batches in `batches.json`.

## Sources

- **List of Parishes (the directory roster):**
  https://www.norwichdiocese.org/Portals/dioceseofnorwich/CMAdmin/Parishes_CCD9Mar26.pdf,
  linked as "List of Parishes" from /Find/Parish-Communities; pages headed "March 6, 2026",
  read 2026-11-14. The diocesan Catholic Directory section, town by town: each church with
  its founding year, address, website, pastor, Mass times, and the words "Merged with" or
  "Yoked with" naming its partners, plus closed churches ("Closed - For inquiries or
  records, contact ..."). The best structural source here and fairly current (it already
  shows the merged parishes and their new websites), but:
  - **Closed churches are listed as town entries**, 14 of them (Ballouville, Dayville,
    Eagleville, East Killingly, Glasgo, North Stonington, Rogers, Scotland, Staffordville,
    Sterling, Vernon, Wauregan, West Thompson, Willington). Its "Closed" says the church
    shut; it does not give dates.
  - **Some website domains are dead or misspelled** (www.stmarycoventy.org,
    www.stmary-stthomas.community.org) or redirect (www.stlukeellington.com to
    churchofstlukect.com; Baltic/Occum/Taftville sites to saintannecluster.org).
  - Scraped into `rosters/directory.json` (88 entries) by
    `scratch/norwich-map-1/tools/norwich_parishlist.py` and `norwich_directory_fix.py`; the
    fix script records the towns the heading parser got wrong and the two repeated entries
    in the Pawcatuck block that were dropped.
- **Parish Locator Map (`rosters/locator-map.json`, 75 entries):** the Google My Map
  embedded on /Find/Parish-Communities
  (https://www.google.com/maps/d/viewer?mid=1VTpfhm6bXf8ZfwM_tX0Ikl--m9E8l7a5), read through
  its KML export 2026-11-14 by `tools/norwich_map_kml.py`. **Stale**: pastors from before
  the mergers, old websites and old cluster names (it still puts St. Joseph in a "Joint
  Norwich Catholic Cluster"). It lists the open churches only, without coordinates. Good for
  an older second website per church and nothing else.
- **GCatholic (`rosters/gcatholic.json`, key `norw0`, 86 entries):** Plus Codes per
  building. It **omits the Cathedral of St. Patrick**, still lists closed churches without
  saying so (St. Joseph Eagleville, St. Thomas More North Stonington, St. Margaret Scotland,
  Sacred Heart Vernon, Sacred Heart Wauregan, St. Joseph Staffordville, St. Jude Willington,
  St. Joseph Dayville), puts Fishers Island in "CT", and calls the Fitchville mission
  "St. John, Bozrah". It adds three Eastern Catholic churches (St. Mary Ukrainian,
  Colchester; Protection of the BVM Ukrainian, Willimantic; St. Ann Melkite, Waterford),
  Holy Apostles College and Seminary (Cromwell) and the Marian Friary of Our Lady of
  Guadalupe (Griswold).
- **Clergy:** the List of Parishes names each pastor. Every shared pastor matches a merged or
  yoked group in it; no priest spans two groups (checked 2026-11-14).
- **Full Group Directory** (https://www.norwichdiocese.org/Find/Full-Group-Directory, read
  2026-11-14): religious houses, retreat centres, hospitals and the Coast Guard Academy.
  Leads for chapels that may have public Mass (Enders Island, Holy Family Motherhouse
  Baltic, Sacred Heart on the Lake Higganum, Marian Fathers Thompson); named in the batches.
- **Mass times:** /Masses lists only livestreamed Masses; there is no diocesan Mass-times
  finder. Use the List of Parishes and the bulletins.
- **Closed parishes and records:** only the List of Parishes' "Closed" entries; no separate
  sacramental-records index was found.
- **Pastoral plan:** none linked from the site's menus (not searched further). The mergers
  above are already in effect in the March 2026 list.

### Bulletin publishers here

From probing parish sites on 2026-11-14 and the map batches since; no neighbouring diocese
is mapped to learn from. Many parish sites here, whatever builds them, only link a
ParishesOnline bulletin: look for the LPi container before you record the site's own builder.

- **ParishesOnline / LPi is the most common.** Org slugs here follow `<name>-<zip>`
  (`blessed-sacrament-parish-06066`, `st-luke-church-06029`); when a parish site hides the
  id, or its domain is dead or disconnected, `probe po` a guessed slug to get the
  `provider_id`, and the org's website field then gives the parish's current site.
  - **Several orgs can share one container**, even for parishes with different pastors:
    `probe po` every org a parish site or the locator map links, and record every org and
    lpi id on the one row whose container they share.
  - **The locator map's `parishesonline.com/find/` links can be dead orgs** with no
    publications: if `probe po` finds none, look for a self-hosted bulletin on the parish's
    own site, and keep the dead org in evidence, not publication.
  - **The PDF footer names the container** (`<Parish> | 03-0263`) when no page shows an id.
  - **Some PDFs have a shifted text layer**: each character 29 code points low, digits
    lost. Decode with `chr(ord(c)+29)` to read the masthead, store no verbatim quote, and
    add a research item on whether the pipeline gets Mass times.
- **Image-only bulletins** (some LPi containers' first pages, the Cathedral's DNN
  `LinkClick` scans): `probe pdf` finds no text. Read page 1 with `render.py`, quote only
  from text pages, and add an unsupported-format research item on whether the pipeline
  OCRs them.
- **Connecting Members (DNN) sites**, the diocese's own builder: the bulletin is at
  `/Resources/Bulletin` or `/Resources/Sunday-Bulletin`, either a hosted scan or an LPi
  bulletin whose widget id is embedded on that page though `probe url` on the home page
  sees none.
- **eCatholic sites answer 403 to `probe url`** and open in `visit.py`. Here they only link
  a ParishesOnline bulletin; the eCatholic bulletin path answers 403 every week. Map them
  as `parishes_online` and keep the eCatholic site id out of publication.
- **Duda** (`irp.cdn-website.com`): the ParishesOnline widget id is only on `/bulletin`, not
  the home page; `probe url` the bulletin page.
- **Servant Keeper** (servantpc `fw2`) sites render in JavaScript, so `probe get` and
  `probe url` see only templates: open them with `visit.py`. Their bulletin page can embed
  ParishesOnline publication links that give the org and container.
- **Weebly:** the addresses in the List of Parishes fail TLS only in their `www.` form; the
  bare `<name>.weebly.com` answers. St. John Middletown's `/area-parish-bulletins.html`
  links the ParishesOnline orgs of every Middletown-Old Saybrook deanery parish: a quick
  way to their ids.
- **WordPress, one post per issue:** pin `dated-post <category or bulletin page>`. Where the
  PDFs are Gravity Forms `index.php?gf-download=` links, fetch:check's guessed recipe pins
  one week's post instead, and older links answer HTTP 401, so back issues can't date a
  closure.
- **Bonventure** (`sponsors.bonventure.net/?page=<id>`, issues `pdfs/<id>/<YYYY-MM-DD>.pdf`)
  reads over http only; the fetcher upgrades to https and fails certificate verification.
  Map it unsupported with `fetch_gap` kind `tls-certificate-unverified` and keep the
  page-pdfs recipe in `provider_id`.
- **Others seen:** Wix `_files/ugd/` PDFs, Squarespace `/bulletin`, a self-hosted dated
  folder of PDFs.
- **Lapsed domains** can belong to a same-named church elsewhere (one GCatholic website is
  now an English Anglican parish), not only to the squatters the README warns of: read the
  page before you use a GCatholic or locator-map website.
- **Discover Mass:** not seen yet. If it appears, it caps downloads per IP per day (134-byte
  replies), as other dioceses found.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.


## Rules settled for this diocese

Proposed in the survey manifest (`scratch/norwich-map-1/survey.json`) and accepted by
`survey-review`.

- A church the diocese's List of Parishes (March 6, 2026) marks 'Closed - For inquiries or records, contact ...' may be excluded with reason closed on that wording, when no current bulletin of the successor parish lists Mass there; last_mass left empty unless another source dates it. (accepted by survey-review, 002-survey-review, 2026-11-14)
- The three Eastern Catholic churches GCatholic lists in the territory (St. Mary Ukrainian, Colchester; Protection of the BVM Ukrainian, Willimantic; St. Ann Melkite, Waterford) are excluded as other-jurisdiction. (accepted by survey-review, 002-survey-review, 2026-11-14)

## Log

- 2026-11-14: reconcile (Run norwich-map-1). Nine batches ran (eight regional of 22-39
  roster entries, about 8-13 places each, plus the 3 Eastern Catholic exclusions). Coverage
  100% of all three rosters: directory 88/88, gcatholic 86/86, locator-map 75/75; modelled
  70/74 of the directory's not-excluded entries (the other four are the `unsupported` Divine
  Mercy's churches and open St. Francis Chapel). Records: 42 parish rows (41 collectable, 1
  `unsupported`), 74 churches, 24 exclusions, 2 `open/`. No merges or moves. Recorded
  `separate` reviews for St. John and St. Sebastian, Middletown, against the five Middlesex
  parishes their "area/deanery parish bulletins" pages link. `fetch:check` picked a current
  issue for all 41 collectable rows. Corrected the intro's open-church count (68 to 74).
- 2026-11-14: survey (Run norwich-map-1). Rosters: directory 88, gcatholic 86, locator-map
  75 (249 entries). Nine batches in `batches.json`, first `tolland-north`; `batches
  validate` passed. No parish records yet.
