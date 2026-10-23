---
name: Roman Catholic Diocese of Pittsburgh
state: PA
website: https://diopitt.org
status: exploring
gcatholic: pitt1
---

Six counties of south-western Pennsylvania: Allegheny (Pittsburgh and its boroughs: McKeesport,
Bethel Park, Monroeville, Coraopolis, Sewickley), Beaver (Aliquippa, Beaver, Beaver Falls,
Ambridge), Butler (Butler, Cranberry, Slippery Rock), Lawrence (New Castle, Ellwood City),
Washington (Washington, Canonsburg, Charleroi, California) and Greene (Waynesburg). It borders
Erie to the north, Greensburg to the east, Wheeling-Charleston (WV) to the south and west, and
Steubenville and Youngstown (OH) to the west. The "On Mission for the Church Alive!" plan
(begun 2015) put the old parishes into groupings that were then merged, mostly on 2020-07-01,
2021-01-04 and 2021-07-01, with later single mergers (St. Augustine, Beaver Falls 2023-01-02;
St. Pio of Pietrelcina 2024-01-01; Saints Francis and Clare 2026). The diocese now lists 59
parishes (56 parish pages: the "Shrines of Pittsburgh" page covers four canonical parishes),
nearly all with two to six churches. There are no families or clusters above the parish: a
merged parish is the unit, and most publish one bulletin for all their churches (to be
confirmed by the scouts). Shared bulletins across parishes are likely only where a source names
a link: St. James and St. Katharine Drexel (one pastor, one website and one "Catholic Partner
Parishes" bulletin) and the four Shrines of Pittsburgh parishes.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory:** `rosters/directory.json`, 169 entries, scraped 2026-10-23 from the 56
  parish pages linked from https://diopitt.org/alphabetical-list-of-current-parishes and
  https://diopitt.org/list-of-current-churches (eCatholic site 16469 behind Cloudflare; read in
  headed Chrome with parish-site-access `visit.py`; scrapers in `scratch/map-pittsburgh/tools`).
  One entry per church in each page's "Weekend Mass Schedule by Church Building", with the
  weekend Mass lines, the parish website and phone, and the Clergy Team. Best list of current
  worship sites and the canonical structure (group = parish). Eleven churches are listed with
  "No Masses Scheduled" (Madonna of Jerusalem; Incarnation of the Lord; Corpus Christi,
  McKeesport; St. Joan of Arc; St. Ann, Bulger; Sacred Heart, Claysville; Mother of Good
  Counsel; St. Stephen, Hazelwood; St. Joseph, Duquesne; St. Rita, Munhall; St. Patrick, Strip
  District "Sunday Masses at Saint Stanislaus Church"): the bulletin decides each. Campus Masses
  appear as entries without an address (W&J College Newman Center; California University of PA,
  whose address comes from the Mass Finder) or with one (Slippery Rock Newman Center). Websites
  as listed, not checked; St. Pio and Saints Francis and Clare pages give none. The church list
  links St. Blaise and St. Monica to /beaver-falls-chippewa-darlington-midland, which 404s;
  /saintaugustineparish has them. Coordinates are the Mass Finder's pins (158 of 169).
- **Mass Finder:** `rosters/massfinder.json`, 168 entries, read 2026-10-23 from
  https://diopitt.org/massfinder with parish-site-access `finder.py`. The same churches as the
  directory minus the eleven no-Mass ones, plus parish-level pins with no address whose ids are
  the parishes' eCatholic site ids (23091 Shrines of Pittsburgh = pghshrines.org, 22384 St.
  Padre Pio, 22104 St. Raphael, 21737/35656 Archangel Gabriel, 26316 Blessed Trinity, 33326 St.
  Augustine), and two non-parish entries (FEST Pittsburgh, Pittsburgh Central Deanery). Lags:
  it still names St. Clare of Assisi and St. Francis of Assisi parishes (now Saints Francis and
  Clare) and lists Holy Redeemer, Ellwood City and Holy Trinity, Robinson, which the parish
  pages don't.
- **GCatholic:** `rosters/gcatholic.json` (key `pitt1`; `pitt0` is the Ruthenian
  Metropolitanate), 273 entries with Plus Codes. 41 are Eastern Catholic (27 Ruthenian, 9
  Ukrainian, 3 Maronite, 1 Romanian, 1 Syro-Malabar), `other-jurisdiction`. Of the 232 Latin
  entries about 155 are directory churches under the same name; the rest are churches of
  predecessor parishes, many probably closed, plus St. Paul Seminary (40411), St. Paul of the
  Cross Monastery (47063), the Pittsburgh Oratory (60863, St. Philip Neri) and St. Anthony
  shrine (24219 = St. Anthony Chapel, Troy Hill). Its `history` field gives merger dates
  ("merged to All Saints 2021.07.01") but never says a building closed except for its four
  "Former Church" entries. It lists St. Maria Goretti three times (24336-24338). Strong on
  addresses; weak on closures.
- **Clusters / families of parishes:** none above the parish. The predecessor list
  (https://diopitt.org/alphabetical-list-of-current-and-predecessor-parishes, read 2026-10-23,
  parsed to `scratch/map-pittsburgh/raw/predecessors.json`) maps 248 former and current
  parishes merged since 2016 to their successor, with phone and old website: good for placing a
  GCatholic church under its current parish, says nothing about whether the building is open.
  Its "N/A - In Grouping 113/114/334" entries are stale (113 became St. Pio, 334 St. Augustine;
  114 is the Shrines of Pittsburgh, still four canonical parishes).
- **Shared pastors:** the Clergy Team on each parish page. Only one priest is pastor of two
  parishes: Rev. Edward L. Yuhas, St. James (Washington) and St. Katharine Drexel (both pages,
  2026-10-23). The Shrines team ("Team Ministry", Rev. Thomas G. Kadlick) serves four parishes.
  Appointments: "Clergy Official" posts (https://diopitt.org/clergy-official).
- **Mass times:** the parish pages' weekend lines (pages say the bulletin has weekday Masses and
  confessions) and the Mass Finder.
- **Closed parishes and where their records went:** the predecessor list above; the diocese's
  per-parish history pages (https://diopitt.org/saint-maria-goretti,
  https://diopitt.org/our-lady-of-the-angels, https://diopitt.org/saint-augustine-beaver-falls ...,
  reached from "The history of our parishes") give merger dates and which church "remained open
  to serve the new parish": good leads for `excluded/` records, but a plan or merger is not a
  closure; read the bulletin.
- **Pastoral plan / closure announcements:** "On Mission for the Church Alive!"
  (https://diopitt.org/onmission); merger news on diopitt.org/news and in the press (AP: 61
  parishes into 15, "from 152 to 106"; EWTN "next round": 26 into 8). The parish territories map
  (files.ecatholic.com/16469/documents/2026/6/..."Parishes as of July 1 2026".pdf) is an image.
  Not read in full; the scouts use it per parish.

### Bulletin publishers here

Which publishers print this diocese's bulletins, how to read each, and which sites block the
sandbox and where their bulletins are instead. Agents researching parishes start here, so
keep it current rather than a log.

Seeded 2026-10-23 from a probe of the 56 parish websites and ~35 ParishesOnline orgs, and from
Greensburg's playbook next door.

- **Every parish website here is diocese-provided eCatholic behind Cloudflare.** `probe url`
  got 403 on 53 of 56 (2026-10-23); `visit.py` opens them headed (6 of 6 tried). `visit.py` reports the
  site's `ecatholic:<id>` even when the bulletin is on ParishesOnline. Don't record
  `ecatholic:16469` (the diocese's own site). The Mass Finder's address-less parish pins carry
  the parish's eCatholic id. Some parish pins carry a church's street address (35656, 0,0
  coordinates), and `coverage --link` then attaches them to that church: check such links.
- **ParishesOnline is the main publisher** (containers `14/xxxx`): `probe po` on 2026-10-23
  found a live org (2026-10-25 issue; St. Paul of the Cross 10-18) for 23 of the 56 parishes;
  four more post on eCatholic and one on John Patrick; the rest are unknown. The LPi geo-search (`.data.items[]`, filter
  `categories` containing "Catholic") lists 140 Catholic orgs round the diocese, most of them
  for predecessor parishes: an old org can point at its successor's container
  (st-maria-goretti-parish and st-pio-of-pietrelcina-15201 both → 14/0730; two Prince of
  Peace/St. Mary of the Mount orgs → 14/0020) or at someone else's
  (most-precious-blood-of-jesus-parish → 14/1701, the Christ Our Savior container). Read the
  masthead before giving an id to a row. Empty orgs (saint-james-parish,
  saint-teresa-of-kolkata-parish, christ-the-divine-shepherd-parish, blessed-trinity-parish-15227,
  saint-mary-magdalene-parish, st-benedict-the-moor-church-15219, divine-mercy-parish-15222) are
  not fold-ins: those parishes publish elsewhere.
- **Find a parish's ParishesOnline org in `scratch/map-pittsburgh/raw/lpi-catholic.tsv`**, not
  by `probe po <parish name>` (when it is missing from the TSV, the parish site's /bulletin page links
  it: Most Sacred Heart, 14/1171) (bare names hit same-named orgs elsewhere: `corpus-christi-parish`
  is Winslow, Maine). Merged parishes keep one org per former church, all resolving to one
  container: record every `po-org`/`lpi` id on the one row (Corpus Christi, Bridgeville).
  A parish's eCatholic site can repost the container PDF a week later (Corpus Christi, 21066):
  same bulletin, not a second one. These archives are byte-identical to the container PDFs and
  the cheapest way to grep a year of issues (Divine Grace, St. Mark, 2026-10). Image covers put the Mass schedule on page 3 (Our Lady of
  Hope); `probe pdf --pages N` returns pages 1..N, so pick the page with `jq`.
- **`fetch:check` on ParishesOnline** reports freshness `future` about two days before the
  Sunday and `publication_identity: unverified` (no expected identity given): read the
  masthead yourself. `visit.py` prints a warning line before its JSON (`tail -n +2 | jq`).
  Run `diocese write` from the repo root.
- **eCatholic bulletins:** several parishes post on their own eCatholic site:
  `files.ecatholic.com/<id>/bulletins/<yyyymmdd>.pdf` downloads without a browser and
  `issues.py ecatholic ecatholic:<id>` finds it (20435 Catholic Partner Parishes, 21574 Christ
  the Divine Shepherd, 23303 St. Matthias, 21158 St. Teresa of Kolkata all had 20261025.pdf).
  `issues.py ecatholic --weeks N` returns only the newest issue; for older ones take the
  site's /bulletins archive links with `visit.py --links` (keep the `?t=` query).
  An eCatholic masthead can be a graphic over a letter-split text layer (22570): render page
  1, quote a clean line from an inner page. A parish site's Mass-times page can list a Mass
  (St. John Cantius's Korean Mass) that the bulletin never prints: Rules settled 1 applies.
  The 20435 text layer is letter-split ("Catholic PartnerP arishes"); quote it verbatim.
- **John Patrick Publishing** (church-bulletin.org/<slug>/, `/bulletin/<slug>/<yyyy-mm-dd>.pdf`)
  prints Saints Francis and Clare (`saints-francis-clare-parish-chicora-pa-16025`).
  `church-bulletin.org/<any-slug>` answers 200, so only a listing with PDFs is a channel.
  The parish site's own bulletin link (`church-bulletin.org/<numeric id>`, redirecting to the
  listing) is what confirms a listing is the parish's channel. Saints Francis and Clare's
  issues have a text layer until mid-August 2026 and are image-only from 2026-08-30: quote an
  older issue, render the newest.
- **Institute of Christ the King:** mostpreciousbloodparish.org redirects to
  institute-christ-king.org/pittsburgh-home; Most Precious Blood self-hosts its bulletin PDF
  there (406 to bare curl; send a browser User-Agent). LPi org
  most-precious-blood-of-jesus-parish is Christ Our Savior's container 14/1701, not MPB's.
- **Scouts: run `coverage` without `--link`.** `--link` writes roster ids into every batch's
  records; the orchestrator runs it at the end.
- **A ParishesOnline org titled "PERMANENTLY CLOSED"** (St. Cecilia, Rochester) is a dead
  predecessor account, not a church closure: the live bulletin still lists Masses there. A
  GCatholic entry named for a merged parish in another town can be a closed predecessor's
  building (gcatholic "St. Monica, Darlington" = St. Rose of Lima, closing Mass 2020-03-28).
- **diopitt.org history pages date closures** of predecessor churches ("closed in 2019", St.
  Alphonsus page on Epiphany, Boyers) while the closed church's own page can still say "remains
  open": quote the dated one and record the disagreement. diopitt.org answers 403 to `recheck`;
  `visit.py --text` stops at 4000 characters (the diopitt.org nav): pass `--chars 30000`.
  TribLive (Valley News Dispatch) names relegated churches (Guardian Angels, Natrona Heights,
  2022-10-01).
  The predecessor pages use set phrases: "closed at the time of the merger" and "remained
  open to serve the new parish"; read each predecessor's page.
  read it with `visit.py` (headed: `PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a`, and a long
  timeout: hsplc.org took over two minutes). Find a successor parish's history page by
  DuckDuckGo (holy-spirit-new-castle dates five closures).
- **Web search:** `visit.py "https://duckduckgo.com/html/?q=..." --text` works (the plain
  `duckduckgo.com/?q=` page returns only the region menu); results begin after "Past Year".
  It finds diopitt.org history pages and church-bulletin.org issues.
- **visit.py with many URLs** writes nothing until the end; give it one site at a time
  (`scratch/map-pittsburgh/tools/visit_each.sh`) or a long timeout.

Carried over from Greensburg (same region, 2026-10); correct it as this diocese shows
otherwise.

- **A parish site can repost its container's PDF**: compare the file name and masthead with
  the container before calling it a separate bulletin. One issue can sit in two LPi containers
  (separate ad editions): compare rendered pages 1-2 and record both on one row.
- **The masthead is often not on page 1** (LPi cover reflections); Canva image-only issues
  carry text only on the LPi ad page, whose footer names the parish and container. Render
  pages with `render.py` (no tesseract here). `render.py` crashes on very large image PDFs (83 MB,
  Saints Martha and Mary): curl it and `pdftoppm -r 70 -f 1 -l 3 -png`. Here too: All Saints, Butler (pages 1-13) and St. Luke, Ambridge
  (14/1208) and Our Lady of the Lakes (14/1310, footer on page 8) are images; its quotable line is the ad-page footer "All Saints Parish, Butler, PA 14-1322".
- **A ParishesOnline org page can render blank** while `probe po` still lists issues; pin
  `other` to `page-pdfs <publicationWidget URL> filename=*B.pdf`. An old org can list a stopped
  container: check its latest issue before treating it as a channel.
- **Same-pastor parishes print each other's Mass boxes** while each keeps its own live
  bulletin: separate rows while both channels are live.
- **Discover Mass (J.S. Paluch):** grep the town in `discovermass.com/wp-sitemap-posts-item-{1..11}.xml`;
  downloads are capped per IP per day (134-byte reply, `not_pdf`) and repeated page hits get
  Wordfence-blocked: read each page once. "No bulletins available" pages are not channels.
- **Occasional Masses at former churches** show only in intentions or the monthly calendar:
  grep a year of issues (`probe pdf --pages 0 --grep <town>`) before excluding a church.
- **GCatholic Plus Codes can be off the building** (one Greensburg pin was 590 m out):
  compare with the Mass Finder pin. Nominatim: send a generic User-Agent
  (`project-carlo-diocese-research`), never a personal one; it 429s after quick repeats.
- **Campus chapels** with public Mass and no bulletin went to `excluded/` as `no-bulletin` in
  Greensburg; Altoona-Johnstown put campus and shrine Masses in `open/` until a source says
  they are public. Apply whatever this diocese's *Rules settled* says.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

Settled 2026-10-23 by the map-diocese orchestrator from the survey's proposals, applying the
README's model and the Greensburg precedent:

1. **Campus, seminary, monastery and Oratory Masses.** A place whose public Mass schedule
   (in-term Masses count) is printed in a parish bulletin is a church row under that parish.
   A place with public Mass that no bulletin prints goes in `excluded/` as `no-bulletin`
   (as in Greensburg), with the source that shows the Mass. A chapel with only community or
   private Masses is `no-public-mass`. Absence of a schedule is not evidence of either: with
   nothing found, use `open/` with the next step.
2. **Churches the directory lists with "No Masses Scheduled".** The parish bulletin decides.
   Occasional Masses there (funerals and weddings aside), found in a schedule, the
   intentions or a calendar, make it a church row. `excluded/` with `reason: closed` needs a
   source that says it closed, was sold or no longer holds Mass, quoted and dated; the
   directory line alone is not one. Otherwise `open/`, with the step that would settle it.
3. **Shrines of Pittsburgh and other multi-parish teams:** rows follow bulletins (README).
   If one bulletin covers the four canonical Shrines parishes it is one row with all their
   churches; St. Anthony Chapel, Troy Hill is a church row of whichever row prints its Masses.
   St. James and St. Katharine Drexel likewise: one row only if the current mastheads show
   one bulletin covering both.
4. **Personal parishes** (Most Precious Blood, Institute of Christ the King; St. Benedict
   the Moor) are ordinary parish rows when they publish a bulletin.
5. **GCatholic predecessor churches.** The survey put 51 GCatholic entries with the nearest
   current church as a planning guess ("nearest" in `batches.md`). The scout places each by
   the predecessor list and the bulletin, not by the batch, and reports one that belongs to
   another batch's parish as a lead. A merger alone never closes a building (README).
6. **Eastern Catholic churches** (GCatholic's 41 Ruthenian, Ukrainian, Maronite, Romanian
   and Syro-Malabar entries) are `other-jurisdiction` exclusions; one record each, citing
   GCatholic's rite and eparchy.

7. **Shrines of Pittsburgh is one row** (scout 18, 2026-10-23): container 14/1226, masthead
   "SHRINES OF PITTSBURGH", covers the four canonical parishes and six sites. The directory's
   "No Masses Scheduled" hid St. Patrick's weekly Thursday Mass: Rule 2 in practice. Annual Masses
   count too (St. Stephen, Hazelwood: a September dedication Mass in the events column): grep
   September issues for the church's name. A parish site's statements page can link a closure
   decree (St. Regis, effective 2025-09-29) that diopitt.org's history page hasn't caught up with.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-23: Survey (diocese-surveyor): rosters directory 169, massfinder 168, gcatholic 273
  (610 entries); 35 scout batches in `batches.json`, all entries assigned. No records yet.
