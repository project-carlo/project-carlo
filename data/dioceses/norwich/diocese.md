---
name: Roman Catholic Diocese of Norwich
state: CT
website: https://www.norwichdiocese.org
status: exploring
gcatholic: norw0
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

**How it is organised.** About **50 canonical parishes and some 68 open churches** in four
deaneries (the March 2026 list below; count made from it, the diocese states no figure). Two
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

From probing 45 parish sites on 2026-11-14 (`probe url`, then `visit.py` for the 403s); no
neighbouring diocese is mapped to learn from.

- **ParishesOnline / LPi is the most common.** Containers and ids seen: Groton tri-parish
  03/0770 (org `tri-parish-community-of-sacred-heart-our-lady-of-lourdes-st-mary`), Mystic
  04/0504, St. Teresa of Calcutta 03/0729 (lpi:0018000000QbzzxAAB), St. Brendan
  lpi:0018000000QxAEWAA3, St. Edward lpi:0018000000Qx96BAAR, St. Therese
  lpi:0018000000Qc2DZAAZ; orgs `st-columba-church-06237` (Good Shepherd),
  `st-agnes-and-st-matthias-catholic-church`, `st-mary-church-of-the-visitation` (Clinton),
  `st-peter-church-6441` (Higganum). The locator map links more `parishesonline.com/find/`
  orgs (Putnam, Danielson, Norwichtown, Taftville, Occum, Preston, Moodus, Brooklyn and
  Hampton, North Stonington). Account names may carry old members.
- **eCatholic sites answer 403 to `probe url`** and open in `visit.py`: St. John Cromwell
  25247, St. Mary Portland 5153, St. Mary of Czestochowa Middletown 5434, St. Joseph
  Rockville 25042; Sacred Heart Groton's site also 403s (it embeds ParishesOnline).
- **Connecting Members (DNN) sites**, the diocese's own builder: the Cathedral and Blessed
  Sacrament, with the bulletin at `/Resources/Bulletin` or `/Resources/Sunday-Bulletin`.
- **Others:** Wix `_files/ugd/` PDFs (catholicwindham.org), Squarespace
  (saintannecluster.org `/bulletin`), WordPress one post per issue (saintphilipct.com
  `/category/bulletin/`), a self-hosted dated folder (saintjosephnorwich.com
  `/bulletins/2025-2026YearA/<date> <Sunday>.pdf`), Duda (stlawrencechurch.com).
- **Unreachable:** the Weebly addresses the list gives for St. John and St. Sebastian,
  Middletown fail TLS; GCatholic gives saintjohnchurchmiddletown.com and
  stsebastianct.org. guardianangelsparishofcolchester.org answers 404 at its root;
  St. Francis Middletown (stfrancisct.com) answered 500.
- **Discover Mass:** not seen yet. If it appears, it caps downloads per IP per day (134-byte
  replies), as other dioceses found.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- Connecting Members (DNN) parish sites may carry LPi bulletins without an id probe url sees: the PDF footer gives the container ('<Parish> | 03-0263') and the bulletin page can embed the LPi widget id; ParishesOnline org slugs here follow '<name>-<zip>' (blessed-sacrament-parish-06066, st-luke-church-06029, all-saints-church-06072, st-edward-church-06076), so probe po a guessed slug to get the provider_id.
- WordPress one-post-per-issue sites whose PDFs are Gravity Forms 'index.php?gf-download=' links: pin 'dated-post <category/bulletin page>'; fetch:check's guessed recipe pins one week's post page instead. Older gf-download links answer HTTP 401, so back issues can't be read to date closures.
- eCatholic sites here (Cromwell 25247, Portland 5153, St. Mary of Czestochowa 5434) only link a ParishesOnline bulletin: the eCatholic bulletin path answers 403 every week, so map them as parishes_online and keep the eCatholic site id out of publication.
- The Weebly addresses in the diocese's list fail TLS only in their www. form; the bare <name>.weebly.com answers. St. John Middletown's /area-parish-bulletins.html links ParishesOnline orgs for every Middletown-Old Saybrook deanery parish, which is a quick way to find their ids.
- Some LPi bulletin PDFs here have a text layer in a shifted font encoding (each character 29 code points low, digits lost): decode with chr(ord(c)+29) to read the masthead, store no verbatim quote, and add a research item on whether the pipeline gets Mass times.
- Servant Keeper (servantpc 'fw2') parish sites render in JavaScript: probe get/probe url see only templates, so open them with visit.py; jnccfaith.org's /parish-bulletin embeds ParishesOnline publication-page links that give the org and container.
- Some bulletins here are image-only (the Cathedral's DNN LinkClick scans; LPi 03/0123 pages 1-5): probe pdf finds no text, so read page 1 with render.py, quote only from text pages, and add an unsupported-format research item on whether the pipeline OCRs them.
- Bonventure bulletins (sponsors.bonventure.net/?page=<id>, issues pdfs/<id>/<YYYY-MM-DD>.pdf) read over http only; the fetcher upgrades to https and fails certificate verification, so map them unsupported with fetch_gap kind tls-certificate-unverified and keep the page-pdfs recipe in provider_id.
- Several ParishesOnline org accounts can point at one container (Groton tri-parish + Our Lady of Lourdes on 03/0770; St. Michael Pawcatuck + St. Patrick Mystic on 04/0504, though they have different pastors): probe po each org a parish site or the locator map links, and record every org/lpi id on the one row whose container they share.
- The locator map's parishesonline.com/find links can point at dead org accounts (st-james-parish-06239 has no publications): probe po each, and if empty look for a self-hosted bulletin on the parish's own site; keep the dead org in evidence, not publication.
- Duda (irp.cdn-website.com) parish sites here carry the ParishesOnline widget id only on /bulletin, not the home page: probe url the bulletin page to get the lpi id.


## Rules settled for this diocese

None yet. Proposed in the survey manifest (`scratch/norwich-map-1/survey.json`) for
`survey-review`.

- A church the diocese's List of Parishes (March 6, 2026) marks 'Closed - For inquiries or records, contact ...' may be excluded with reason closed on that wording, when no current bulletin of the successor parish lists Mass there; last_mass left empty unless another source dates it. (accepted by survey-review, 002-survey-review, 2026-11-14)
- The three Eastern Catholic churches GCatholic lists in the territory (St. Mary Ukrainian, Colchester; Protection of the BVM Ukrainian, Willimantic; St. Ann Melkite, Waterford) are excluded as other-jurisdiction. (accepted by survey-review, 002-survey-review, 2026-11-14)

## Log

- 2026-11-14: survey (Run norwich-map-1). Rosters: directory 88, gcatholic 86, locator-map
  75 (249 entries). Nine batches in `batches.json`, first `tolland-north`; `batches
  validate` passed. No parish records yet.
