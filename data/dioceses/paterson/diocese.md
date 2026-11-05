---
name: Roman Catholic Diocese of Paterson
state: NJ
website: https://rcdop.org
status: exploring
gcatholic: pate0
---

Three counties of northern New Jersey: Passaic (Paterson, Passaic, Clifton, Wayne, West
Milford), Morris (Morristown, Parsippany, Dover, Madison, the Lake Hopatcong towns) and Sussex
(Newton, Sparta, Vernon). It borders the Archdiocese of Newark (Bergen and Essex counties) to the
east and south, Metuchen (Somerset) to the south, the Archdiocese of New York (Orange County) to
the north, and across the Delaware Scranton (Pike, Monroe) and Allentown (Northampton) to the
west. About 105 canonical parishes in twelve deaneries (rcdop.org/deaneries); the chancery is
in Madison. There is no family or cluster system: parishes are single units with their own
pastor, and mergers have been one parish at a time (St. Brendan & St. George, Clifton 2011;
Sacred Heart & Our Lady Queen of the Most Holy Rosary, Dover 2018; Our Lady of Fatima & St.
Nicholas, Passaic 2022; Padre Pio Parish, Paterson, from St. Bonaventure and Our Lady of
Pompei, 12 April 2026; Our Lady of the Valley & Holy Cross, Wayne, undated). Shared
bulletins are most likely where one priest is pastor of two parishes (Sandyston/Montague,
Oak Ridge/Stockholm) and in merged parishes that kept both churches. Paterson, Passaic and
Clifton are dense city parishes with Spanish, Polish, Italian and other language Masses.

## Sources

- **Parish finder (the `directory` roster):** https://rcdop.org/parishfinder, an eCatholic map
  behind Cloudflare (`probe url` gets 403). Read 2026-11-04 in headed Chrome (parish-site-access
  `visit.py --html`, `finder.py`) and `scratch/paterson-map-1/tools/finder_times.py`, which adds
  each site's Mass schedule (`mass_times`) and details text (`notes`). 117 pins. **The pin id is
  the parish's eCatholic site id** where the parish site is on eCatholic (Padre Pio 39965,
  Our Lady of the Valley 11969, St. Stephen Paterson 33773, the sampled Sussex and Morris
  sites), so it is a strong lead for `ecatholic:<id>` (Sacred Heart, Dover is an exception:
  pin 5701, site 25510). The finder carries stale pins: three for Our Lady of Consolation,
  Wayne (11364 and old eCatholic sites 660, 700), two each for Our Lady of Fatima Highland
  Lakes, Holy Spirit Pequannock, St. Catherine of Bologna Ringwood and St. Stephen Passaic,
  separate pins for St. Bonaventure and Our Lady of Pompei beside Padre Pio Parish, the
  pre-merger St. Nicholas Passaic (14090), two schools (Saint Luke Academy, St. Gerard
  Majella School) and Prince of Peace Chapel (William Paterson University campus ministry).
  Its Mass times were current for Padre Pio (matching the parish's own site); its details
  text is decades old (CCD enrollment figures), so don't quote it.
- **GCatholic:** `rosters/gcatholic.json` (key `pate0`), 122 entries with Plus Codes, fetched
  2026-11-04. It omits the cathedral (St. John the Baptist, Paterson) and Our Lady of the Holy
  Angels, Little Falls; keeps St. Casimir, Paterson (closed 2018), Holy Cross, Wayne, Our Lady
  of the Holy Rosary, Dover, St. Nicholas, Passaic and St. George, Paterson as their own
  churches; and lists 6 Eastern Catholic churches (Ruthenian Holy Wisdom Flanders and St.
  Michael cathedral chapel Woodland Park; Ukrainian St. Nicholas Passaic and St. John the
  Baptist Whippany; Melkite St. Ann Woodland Park; Armenian Sacred Heart Little Falls) and
  religious houses (St. Mary's Abbey Morristown, St. Paul's Abbey Newton, Holy Face Monastery
  Clifton, Our Lady of the Holy Spirit Sanctuary Branchville), two shrines (Blessed Miriam
  Teresa, Convent Station; St. Joseph, Stirling) and the FSSP Our Lady of Fatima Chapel,
  Pequannock. Its websites are often old domains.
- **Deanery lists:** https://rcdop.org/deaneries and one page per deanery (`/paterson-1`,
  `/clifton-deanery`, `/sussex-deanery`, ...), read 2026-11-04: 108 parish names in 12
  deaneries. Not imported (no addresses; the finder covers the same parishes). Stale: they
  still list Holy Cross and Our Lady of the Valley, Our Lady of Fatima and St. Nicholas, and
  St. Bonaventure and Our Lady of Pompei separately. Good for the canonical parish count.
- **Priest directory:** https://rcdop.org/priest-directory and https://rcdop.org/order-priests
  (read 2026-11-04): each priest's assignment. Explicit shared pastors: Rev. Wayne Varga,
  "Pastor, Saint Thomas the Apostle, Sandyston and Saint James the Greater, Montague"; Rev.
  Benjamin Williams, "Pastor, Saint Thomas the Apostle, Oak Ridge and Saint John Vianney,
  Stockholm". Rev. Angel J. Torres is administrator of Our Lady of Victories and parochial
  vicar of the cathedral (not a shared pastorate). Order priests: OFM at St. Mary, Pompton
  Lakes (listed as "Pompton Plains") and St. Anthony, Butler; OFM Conv. at St. John Kanty,
  Clifton; FSSP at Our Lady of Fatima Chapel, Pequannock.
- **Closed and merged parishes:** https://rcdop.org/parishes-of-the-paterson-diocese, the
  diocesan historian's chronological list (undated; latest entry the 2022 Passaic merger, so
  it predates Padre Pio). Gives St. Casimir, Paterson "closed in 2018"; St. George, Paterson
  "merged with Saint Brendan in 2011; church taken over by Saint George Syro-Malabar Parish";
  old missions closed decades ago. Says a parish ended, not that a building is shut.
- **Mass times:** the finder above is also the diocese's Mass-times search (Sunday, daily and
  holy-day schedules per pin; 96 of 117 pins carry a schedule). No separate Mass-times page.
- **News:** The Beacon, https://beaconnj.org (WordPress; `/wp-json/wp/v2/posts?search=...`
  works with `probe get`). "New pastor unites Paterson parish during historic merger"
  (2026-09-26) dates Padre Pio Parish to 12 April 2026, both churches open. Its search is
  fuzzy; no pastoral plan or closure list was found there or on rcdop.org.
- **Pastoral plan / closure announcements:** none found (rcdop.org menus, Beacon search for
  merger/closing/last Mass, 2026-11-04).

### Bulletin publishers here

From the survey's sample (2026-11-04: `probe url` on all 116 finder websites, `visit.py
--bulletin` on 12) and the map batches since. Most parishes print with Bon Venture, LPi or
John Patrick, and post the result on an eCatholic site: record the host the site's bulletin
page links, not the printer.

- **eCatholic hosts nearly every parish site,** behind Cloudflare: 95 of 116 sites answer
  `probe url` with 403; `visit.py` loads them. The finder pin id is usually the site id.
  - **visit.py faults:** a Cloudflare "502: Bad gateway" (HTTP5XX) is transient; retry
    minutes later. visit.py can also hang with no output (past 500 s) on a home page while
    the site's `/bulletins` loads at once: visit the bulletin page URL directly, not
    `--follow` from home.
  - **Read the site's menu and the `/bulletins` page's first links before running
    `issues.py`.** The `files.ecatholic.com/<site id>/bulletins/<YYYYMMDD>.pdf` archive
    (`issues.py ecatholic`, no Cloudflare) can be stale (2018–2023 in one batch) while the
    current bulletin is a Bon Venture link at the top of `/bulletins`, an embedded
    ParishesOnline publication, a JPP template link, or PDFs under
    `files.ecatholic.com/<id>/documents/<y>/<m>/` listed on a custom page
    (`/parish-bulletins`, `/parish-updates`). A page titled "Bulletins (up to 2023)" is a
    frozen archive; the top-menu "Bulletins" item may point to a Bon Venture sponsor page
    instead, or there may be no `/bulletins` page at all (then `--follow /bulletins` fails:
    read `--links`). Some sites post no Sunday-dated file: read the real file names.
  - **An archive file never posted answers 403, not 404.** When `/bulletins` stops weeks
    ago, `probe get` on the next Sundays' names confirms the parish hasn't posted.
  - **Empty `/bulletins`** (only "Bulletin" and "Archive" headings, no links): the parish
    posts nothing there. Confirm with `issues.py` (Sunday, `--day sat`; 403 = not posted)
    and `probe po <name>-church-<zip>` (an org can exist with no publications; its ids are
    the ones to use if issues appear), then record no_bulletin with a revisit.
  - **One bulletin per language** can be posted each week as separate dated files (one
    parish: Friday English, Saturday Polish, Sunday Spanish): run `issues.py` with `--day
    fri` and `--day sat` too, and read each file's language before picking a recipe.
  - **A parish can post on two of its own site ids,** and move between them (and back-fill
    one): compare the `?t=` upload stamps on each site's `/bulletins` links to see which is
    posting now, record every site id carrying issues in publication, and set a revisit.
  - **Documents-folder bulletins:** use a page-pdfs recipe on the listing page. It dates links
    only by their label, not the URL-encoded file name (`Month%20D%20YYYY.pdf`), so an
    undated label makes it pick an older issue (fetch_gap `undated-link-label`): check the
    pick's date. On a monthly newsletter listing ("November 2026") the first-listed pick is
    right but fetch:check reports date and freshness unknown: check by hand.
  - **No usable text layer:** some issues are scanned images (no extractable text), some
    shifted by 29 code points (`0$66(6` for MASSES, digits dropped), some broken font
    encoding. `probe pdf` can't give Mass times: render page 1 with `render.py`;
    fetch:check's identity unverified is then expected. The same holds for Bon Venture,
    LPi and John Patrick PDFs below.
  - **One-off covers:** a cover with a non-Sunday date (a pastor's birthday) gives a
    fetch:check issue-date conflict; check page 2 and the previous issue's page 1 before
    calling the pick stale.
  - **`ecatholic:5303` is the Diocese of Paterson's own site,** reported on any parish page
    that links rcdop.org. Don't record it.
- **Bon Venture** (`sponsors.bonventure.net/?page=<n>`, use `http://`; see Scranton and
  Allentown). Its ad footer ("150C (PK) - <parish> ... Bon Venture Services") also appears in
  issues the parish posts as eCatholic `bulletins/` files; that doesn't make Bon Venture the
  host. The footer code (`021C (JA)`) doesn't map to a `?page=<n>` id, and bonventure.net has
  no parish list or search: a sponsor page is found only where a site links it. Seasonal
  covers (All Saints/All Souls) replace the masthead on page 1, on eCatholic-hosted copies
  too: read address and Mass times from the previous week's page 1 or the schedule on page 2.
- **LPi / ParishesOnline:** an eCatholic bulletin page (e.g. `/bulletins-1`) can embed
  `parishesonline.com/publication-page/<org slug>`; record po-org/lpi/po-container from
  `probe po`, not the eCatholic site id. LPi copies carry an ad footer "<parish>, <town>,
  NJ 04-NNNN" (or "<parish> | 03-NNNN"), which gives the container.
  - **Copies on a parish site** (eCatholic `bulletins/`, Squarespace `/s/<YYYYMMDD>B.pdf`):
    try `probe po` on `<name>-church-<zip>` for the org and record parishes_online, not the
    copies. If no org slug is found, keep provider ecatholic and record po-container as a
    publication form, with research to find the org; the container can have next Sunday's
    issue before the copy.
- **John Patrick Publishing:** a `/bulletins` page links
  `jppc.net/onlinebulletins/<customer>template.pdf`, which redirects (HTML, not a PDF) to a
  `church-bulletin.org/<parish-slug>` listing of `bulletin/<slug>/<YYYY-MM-DD>.pdf` issues.
  Record `url:<listing>` and use page-pdfs on it; fetch:check dates the pick from the file
  name. Where the site links only eCatholic copies, the customer number in the footer ("6059
  <parish>, Paterson, NJ John Patrick Publishing") opens the listing via
  `https://church-bulletin.org/?id=<n>`; a guessed slug returns a generic 200 page, not 404.
- **WordPress parish sites** can post one `/bulletin/<month>-<day>-<year>/` post per issue
  with the PDF inside: fetch's dated-post recipe on the listing page picks the current
  issue. `/wp-json/wp/v2/media?mime_type=application/pdf` lists every uploaded issue with
  its upload date, which shows how often the parish posts.
- **A fixed Dropbox file** (`dropbox.com/s/<id>/Bulletin.pdf?dl=0`, seen on a Wix site): page-pdfs
  gets Dropbox's HTML preview (not_pdf). Pin `redirected-pdf <same URL>?dl=1`; fetch:check
  then reports date and freshness unknown, so check the masthead date by hand.
- **Next Sunday's issue mid-week is normal here:** fetch:check's freshness `future` (age −4
  days) on the newest file is the right pick; confirm the masthead date.
- **Discover Mass's daily download cap and Paluch joint bulletins** (Scranton, Allentown)
  haven't been seen here yet.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Melkite: Eparchy of Newton; Armenian: Eparchy of Our Lady of Nareg) and St. George, Paterson, now the Syro-Malabar parish (Eparchy of Chicago), are excluded as other-jurisdiction. (accepted by survey-review, 002-survey-review, 2026-11-04)
- A merged parish whose bulletin still lists Mass at both former parish churches is one parish row with both churches (Padre Pio: St. Bonaventure and Our Lady of Pompei). (accepted by survey-review, 002-survey-review, 2026-11-04)
- Church addresses and pins: the finder's and GCatholic's address can be the parish office, and a finder pin the office or a street geocode (one 2.7 km off). Take the church's address from the bulletin masthead, and its location from the OSM building or the GCatholic Plus Code once OSM confirms it. (map batches `randolph-succasunna` and `mount-olive-netcong`, 2026-11-04)
- Two finder pins for one parish are linked to one church: a pin with no address beside one with an address (two domains loading the same eCatholic site; the addressless pin carries the site id), or a pin with only a P.O. Box and an old schedule in its notes (a legacy entry, whose pin is not the church; take coordinates from the Plus Code). Where a Nominatim name search finds no church, a reverse lookup (zoom=18) at the Plus Code coordinates often returns the place_of_worship; Overpass via `probe get` failed. (map batches `northern-passaic` and `west-milford-vernon`, 2026-11-04)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-04: Survey (factory run paterson-map-1). Created the diocese; rosters `gcatholic`
  (122) and `directory` (117, the eCatholic parish finder with Mass times); planned 30 batches
  in `batches.json`. No parish records yet.
