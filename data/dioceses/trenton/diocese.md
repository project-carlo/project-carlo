---
name: Roman Catholic Diocese of Trenton
state: NJ
website: https://dioceseoftrenton.org
status: promoted
gcatholic: tren1
city_aliases:
  Point Pleasant Boro: Point Pleasant Borough
  Princeton Jct: Princeton Junction
  Millstone Twp: Millstone Township
  Barnegat Township: Barnegat
promoted: 2026-10-30
---

Four counties of central New Jersey: Mercer (Trenton, Hamilton and Yardville, Ewing and West
Trenton, Lawrenceville, Princeton, West Windsor, Hightstown, Hopewell, Pennington, Titusville),
Burlington (Willingboro, Beverly, Riverside, Delran, Riverton, Cinnaminson, Maple Shade,
Moorestown, Mount Laurel, Marlton, Medford, Tabernacle, Mount Holly, Hainesport, Browns Mills,
Burlington, Bordentown, Florence, Roebling, New Egypt, Wrightstown), Monmouth (Freehold,
Howell, Farmingdale, Manalapan, Marlboro, Colts Neck, Holmdel, Middletown, Keansburg, Keyport,
Matawan, Red Bank, Rumson, Long Branch, Eatontown, Asbury Park, Neptune, Belmar, Spring Lake,
Manasquan) and Ocean (Point Pleasant, Brick, Lakewood, Jackson, Toms River, Lavallette and the
Seaside barrier island, Bayville, Forked River, Barnegat, Long Beach Island, Little Egg Harbor).
Neighbours: Camden to the south (mapped by the factory, Run camden-map-1), Philadelphia across
the Delaware (mapped, Run philadelphia-map-1), Metuchen to the north (not mapped).

The diocese has **97 parishes** ("97 parishes", dioceseoftrenton.org/about-us, read
2026-10-30), down from 127 in 2005 and 107 in 2015 (The Monitor, 2020-06-26). They are grouped
into **30 cohorts** within eight deaneries and four county vicariates (the July 2024 cohort
list, Sources). A cohort is a collaboration group, **not a family with one bulletin**: the
January 2017 *Faith in Our Future* decisions set every cohort on a "Collaborative Model"
(parishes "remain distinct with their own pastor ... finances, census and sacramental books"),
and only some pairs or trios on a "Linkage Model" (one pastor, distinct parishes) or a
"Merger Model". So expect one parish, one bulletin as the common shape, with a merged parish
often keeping two or more churches (GCatholic's `group`), and shared bulletins where linkage
named one pastor: the Catholic Community of Hopewell Valley (St. Alphonsus, St. James, St.
George, one John Patrick listing), Sacred Heart, Bay Head with St. Pio, Lavallette (one
listing), the Cathedral with St. Joseph, Trenton and St. Isaac Jogues with St. John Neumann
(each with its own listing). The map jobs read the mastheads. `batches.json` gives each cohort
its own batch (small neighbouring cohorts combined) and the eight Eastern Catholic places one
batch.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (the `directory` roster):** the diocese's eCatholic parish finder,
  https://dioceseoftrenton.org/parishfinder, read 2026-10-30 with parish-site-access
  `finder.py` (Cloudflare refuses `probe url` and `probe get` on all of dioceseoftrenton.org;
  `visit.py` loads it). **98 pins, one per parish at its seat** (address, phone, website,
  coordinates), no worship sites, no pastors. 97 current parishes plus "St. Mary of the Lake
  Parish (now part of Our Lady of Guadalupe Parish)", Lakewood (merged 2020-07-01, The
  Monitor 2020-06-26). Two pins have no website: Korean Martyrs Parish and St. Joseph Parish,
  both Trenton. Websites are mostly current (the dead and moved ones are GCatholic's), but
  check each. Names are as the parishes style themselves ("Church of St Monica", "St. Mary R.C.
  Parish", "The Oratory Church of St. Anthony of Padua"). Good for the parish list, sites and
  coordinates; not for structure.
- **GCatholic:** `rosters/gcatholic.json` (key `tren1`; `tren0` is Trento, Italy), **136
  entries** with Plus Codes: 125 Latin churches, 3 chapels (St. Catherine, Farmingdale; Star of
  the Sea, Manasquan; St. Mary, New Monmouth) and **8 Eastern Catholic** places: St. Mary
  (Ruthenian), St. Basil (Romanian) and St. Josaphat (Ukrainian), Trenton; St. Mary (Romanian)
  and St. Nicholas (Ruthenian), Roebling; Our Lady of Perpetual Help (Ruthenian) and St.
  Stephen (Ukrainian), Toms River; the former Basilian Fathers of Mariapoch monastery, Matawan
  (Hungarian, "Former Church"). It lists **churches**, with the canonical parish in `group` for
  some, so it is the best list of worship sites, but it is **stale**: it still lists churches of
  parishes merged by the 2017 decisions as if separate (St. Mary, Bordentown, St. Clare,
  Florence and Holy Assumption, Roebling; St. Joseph and Jesus the Lord, Keyport; St. Jerome,
  West Long Branch and St. Mary, Deal; Ascension, Bradley Beach and St. Elizabeth, Avon; St.
  Catharine, Seaside Park and Our Lady of Perpetual Help, Seaside Heights; St. Andrew, Jobstown
  and Assumption, Wrightstown; St. Mary of the Lake, St. Mary and St. Anthony Claret,
  Lakewood; Divine Mercy and Blessed Sacrament-Our Lady of the Divine Shepherd, Trenton), and
  churches the decisions or The Monitor report closed (St. Peter, Riverside; Holy Spirit,
  Asbury Park). It **omits** the Cathedral (St. Mary of the Assumption, Trenton) and the
  Co-Cathedral (St. Robert Bellarmine, Freehold). Of its websites, 27 don't resolve, one is a
  spam squat (padrepionj.com) and one is parked (visitationchurch.com) (Bulletin publishers).
- **Cohorts (the diocese's grouping; not imported as a roster, since it adds no places):**
  "Parishes aligned by Cohorts/Deaneries, UPDATED JULY 2024" (header "5/13/24 updated"),
  https://files.ecatholic.com/14277/documents/2024/7/2024%20July%20-%20Updated%20%20Parish%20Cohorts%20and%20Deaneries.pdf,
  linked from dioceseoftrenton.org/planning (read 2026-10-30; text layer, `probe pdf` reads it).
  It lists all 97 parishes in 30 cohorts (1–25 from 2017, 26–30 "(new)"), with deans and
  episcopal vicars, and a few names: Cohort 3 "Disciples in Action", 6 "Lumen Christi", 8
  "Cath Community of Hopewell Valley", 19 "Gathered as One", 24 "RCCTR – Roman Catholic
  Churches of Toms River". It marks Cohort 27 (St. Vincent de Paul, Yardville and St. John the
  Baptist, Allentown) "*linkage delayed", and puts Korean Martyrs in parentheses under St. Ann,
  Lawrenceville and Immaculate Conception, Eatontown under Cohort 28. The 2021 version is on the
  same page (`/documents/2021/8/...`). `batches.json` follows it. Good for which parishes to
  research together; a cohort says nothing about bulletins.
- **Faith in Our Future decisions (pastoral plan, January 2017):**
  https://dioceseoftrenton.org/decisions (Cloudflare; `visit.py --text --chars 80000` reads it
  all), the Bishop's decisions per 2017 cohort with the working definitions of the
  collaborative, linkage and merger models. It names the **explicit linkages** (one pastor):
  St. Isaac Jogues and St. John Neumann; Christ the Redeemer and Sacred Heart, Mount Holly;
  St. James, St. Alphonsus and St. George (Hopewell Valley); the Cathedral and St. Joseph,
  Trenton; and planned ones (St. John, Allentown with St. Vincent de Paul by 2019, now "linkage
  delayed"; St. Dorothea with Precious Blood by 2019; Sacred Heart, Bay Head with St. Pio by
  2019; St. Andrew with Assumption by 2017, St. Ann, Keansburg with St. Catherine Laboure "to be
  determined", Holy Family, Union Beach with the merged Keyport parish "potential"). It names
  the **mergers** of 2017–2020 (Divine Mercy and Blessed Sacrament-OLDS into Sacred Heart,
  Trenton; St. Andrew and Assumption; Sts. Francis and Clare with St. Mary, Bordentown; St.
  Joseph and Jesus the Lord, Keyport; St. Jerome and St. Mary, Deal; Ascension and St.
  Elizabeth, Avon; St. Catharine of Siena and Our Lady of Perpetual Help, Seaside; St. Mary of
  the Lake and St. Anthony Claret, Lakewood) and church closures ("suspend all operations at St.
  Peter Church", Riverside, by July 2017; "potential suspension of operations of Holy Angels
  Church" in Hamilton). It is a plan: the 2024 cohort list shows which mergers happened as
  parishes, but whether each former church still holds Mass needs the bulletin. The planning
  page's "Parishes that Merged or Closed Since 2005" heading has nothing under it (checked
  in the page HTML, 2026-10-30), and there is no closed-parish list; the sacramental-records
  page (dioceseoftrenton.org/sacramental-records) only says records go to the absorbing
  parish.
- **Clergy:** no diocesan clergy directory. The Monitor's "Clergy Appointments" posts (2021–2026;
  `tools/monitor_search.sh "Clergy Appointments"`) are incremental and name one parish per
  priest in every post read; they don't establish any shared pastor. The linkages above come
  from the 2017 decisions; read each masthead for the current pastor.
- **The Monitor** (trentonmonitor.com, the diocesan news site): WordPress, and its REST API
  answers `probe get` (`tools/monitor_search.sh`, `tools/monitor_post.sh`). The search is
  full-text and noisy (national Catholic news is mixed in): search a parish name with the
  town, and read the post. Found: Holy Spirit Church, Asbury Park's closure (2020-12-04
  "Holy Spirit Church closure to help ensure Catholic presence in Asbury Park"; 2021-06-11
  "At closing Mass, Holy Spirit churchgoers bid farewell to iconic worship site"); the Lakewood
  merger (2020-06-26, effective 2020-07-01) and Our Lady of Guadalupe's "Holy Family School and
  Church campus" (2025-10-09).
- **Mass times:** no diocese-wide Mass-times list found (the site has the finder only).
- **Other jurisdictions in the territory:** GCatholic's eight Eastern Catholic places (above),
  all in batch `eastern-catholic`. Korean Martyrs is a Latin parish of the diocese (on the finder
  and in Cohort 7), not other-jurisdiction.

### Bulletin publishers here

Use the finder's website before GCatholic's, and verify both.

- **John Patrick Publishing prints most of this diocese.** Sites link
  `jppc.net/onlinebulletins/<id>template.pdf` or `church-bulletin.org/?id=<id>`, which redirect to
  a `church-bulletin.org/<slug>` listing of dated PDFs (`/bulletin/<slug>/<yyyy-mm-dd>.pdf`). Look the parish up in `scratch/trenton-map-1/tools/jppc-trenton.tsv`,
  and grep the `.jsonl` scans beside it by name or ZIP (the tsv's ZIP filter misses some); reload a
  listing with `probe url`, since the scan's "no edition" can be out of date. A listing still empty
  is dead, or only hosts the parish's website while it prints elsewhere, sometimes under the same
  number: read the homepage's links before calling a parish bulletin-less. A listing's name can join
  two parishes: read the masthead. Record `other` with `page-pdfs https://www.church-bulletin.org/<slug>`.
  Many parishes post the same PDFs on their own site, often a week or months behind: compare md5 for
  the same Sunday, take the channel with the latest issue (*Rules settled*), keep the other's id in
  `publication`, and prefer the text layer only when both are equally current. An eCatholic site
  whose Bulletins page links `church-bulletin.org` PDFs is only the host. Many issues are image-only,
  and a listing can switch between text and image week to week: render pages 1–3 (1–4 for a joint
  masthead) with `render.py`, cite what you read as a `note` with no `quote`, and check the Mass
  lines are the schedule, not Mass intentions. A font-garbled text layer floods the context: `probe
  pdf --grep` first, then render page 1. `fetch:check` passes an image-only issue with identity
  `unverified`, gives the coming Sunday's issue `future` freshness (it is current), and can report a
  date `conflict` from a stale template date or the next week's readings: the cover date and file
  name settle it. `probe pdf --pages N` reads the first N pages and prints font warnings before the
  JSON (cut to the first `{`).
- **eCatholic:** an id is the bulletin only when `/bulletins` lists current
  `files.ecatholic.com/<id>/bulletins/` PDFs. Many sites here keep a frozen or empty `/bulletins`
  while the homepage's "Bulletin" link (sometimes only a "Weekly Bulletin" menu item) goes to a John
  Patrick listing, a Bon Venture page or ParishesOnline: list it with `visit.py --links --match .`
  before trusting the id, and keep a frozen archive's id out of `publication`.
  A `/bulletins` file name can be the upload week, not the issue date (take the masthead's), and the
  newest can lag the printer's listing by a week. A site that posts current issues as
  `/documents/<yyyy>/<m>/` uploads on another page while `/bulletins` is old is `other` with
  `page-pdfs` on that page, keeping the eCatholic id. One site can answer on every member parish's
  domain: use the domain the masthead prints. **`ecatholic:14277` is the diocese's own site**: never
  record it. A site that answers 403 to `probe url` still lists its PDFs in `visit.py`, and they
  fetch with `probe get`; a `/contact-us` page lists each worship site's address.
- **LPi / ParishesOnline:** `probe po <lpi id>` gives the org and container; with no id on the
  site, try `probe po` on a slug of the parish's name and ZIP, then the name alone, and a web search
  for its bulletin (a dead site can still have a container). The footer's number is the container
  ("03-4119" = 03/4119). The org's issue list can lag the container: try the coming Sunday's file
  name. An issue over `fetch:check`'s 25,000,000-byte limit is checked by signature only: read the
  parish site's smaller copy with `page-pdfs` if it has one, keeping the ParishesOnline ids, and
  otherwise confirm the masthead from a neighbouring issue. A cover can keep a stale template date
  beside the real one (a date `conflict`; the file name settles it). WeConnect (LPi) sites list the
  container's issues or upload PDFs to `uploads.weconnect.com/mce/<hash>/`.
- **Bon Venture:** issues are `sponsors.bonventure.net/pdfs/<n>/<yyyy-mm-dd>.pdf`, listed on
  `?page=<n>`. The link is often only on the homepage (a menu item, an image, or a button's
  `onclick` `window.open`: save the HTML with `visit.py --html` and grep for `bonventure.net`) while
  the site's own archive is stale or the site (eCatholic, Solutio) is only the host. Record `page-pdfs
  http://sponsors.bonventure.net/?page=<n>` and give `probe pdf` `http://` URLs (https fails
  certificate verification). Same-named parishes have their own accounts: check the header's
  address. The coming Sunday's issue is often not posted yet (404): take the latest date from the
  sponsor page. Text layers vary week to week or garble headings: cite the nearest readable
  masthead. A cover crediting "Bon Venture Services" names the printer only.
- **Solutio CMS** (`/news/bulletin/<n>-<date>`, `/get-connected/bulletin/<n>-<date>/file`): the
  `/file` PDFs answer 403 to `probe get`, `render.py` and `fetch:check`. Find the parish's John
  Patrick listing or Bon Venture page first, then read the site with `visit.py`; a stale Solutio
  archive can still link the printer's current listing.
- **Self-hosted and other sites:** read the file before taking a site's first PDF as the bulletin
  (registration forms come first on some), and give a page that links other PDFs a filename glob
  (`filename=bulletin*.pdf`). Squarespace and Duda pages can hide their PDF links from `probe get`:
  list them with `visit.py --links`. A hand-edited page can list stale links first: run `fetch:check`
  on its current and past-bulletins pages and pin the one that picks this week's issue. When no
  recipe does (links that aren't PDFs, such as Joomla `weblink.go` redirects or ASP
  `opendoc.asp?b_id=` downloads; HTML-only Constant Contact emails; undated links with last week's
  first), the row is `unsupported` with a `fetch_gap` (hand refresh, 2026-11-07; `pnpm diocese gaps`
  lists the kinds).
- **Google Drive:** a Google Sites page can embed a Drive folder: `visit.py --links` lists the
  files; record `google_drive` with `drive-folder https://drive.google.com/drive/folders/<id>` (the
  id from the embed's `folderview?id=`). The folder isn't strictly newest-first: check the pick's
  date. One post per issue, each linking a Drive file, has no recipe.
- **Discover Mass / J.S. Paluch:** prints no bulletin here; its church pages work as a directory (a
  merged parish's old name on its second church, a language community at its host church). It caps
  downloads per IP per day (a 134-byte reply `fetch:check` reports as `not_pdf`).
- **Blocked, dead and hijacked sites:** Cloudflare refuses `probe url` on dioceseoftrenton.org and
  many parish sites; `visit.py` reads most. Don't try to get past a block another way. `diocese
  recheck` can't verify a quote from a site that refuses plain fetch: quote the printer's issue, or
  record the browser read as a `note`. A site that fails TLS in every client gets the printer's
  listing as its website and an access-blocked research item; a site that is down ("temporarily
  unavailable") gets research with a retry, not a gap. A disconnected domain (Wix "Reconnect Your
  Domain") has no site: find its channel in the Wayback copy and its printer elsewhere. Many of
  GCatholic's websites here are dead, moved or squatted (a gambling redirect, a joke "church" blog,
  a finder e-mail on a parked domain): read the page text before storing a domain.
- **Eastern Catholic eparchies:** confirm a GCatholic Eastern church on its eparchy's list before
  excluding it; the Eparchy of Passaic's finder is JavaScript (403 to `probe get`): read it with
  `finder.py`.
- **Web search and The Monitor:** duckduckgo.com/html answers a bot challenge after a few searches;
  spend them on a site, a listing or a closure. The Monitor's REST search dates closures, but its
  dates for 2017-era stories can be the 2019-07-29 migration: take the event date from the story and
  check the weekday gives the year. When a parish-name search finds nothing, search the town;
  obituaries and feast-day stories state mergers and worship sites. A general web search found three
  closures (2016, 2017, 2021) the REST search had missed (hand refresh, 2026-11-07).

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches GCatholic lists in the territory are excluded as other-jurisdiction once confirmed on their eparchy's list; the former Basilian monastery, Matawan, as other-jurisdiction or closed on what its source says. (accepted by survey-review, 002-survey-review, 2026-10-30)
- A cohort or a linkage (one pastor) is not a shared bulletin. Parishes keep separate rows when each publishes its own bulletin with its own masthead; they are one row only when a current masthead names them together. (accepted by survey-review, 002-survey-review, 2026-10-30)
- A merger ends a parish, not a church: a former parish church of a 2017-2020 merger keeps a church row under the merged parish when its current bulletin or Mass schedule lists Mass there, and is excluded closed only on a source that says so (closing Mass, relegation, sale), with last_mass. (accepted by survey-review, 002-survey-review, 2026-10-30) Weekday Mass can move between a parish's churches week to week: read the whole Mass block, and keep both rows while the weekend schedule lists both. A church a merged parish's masthead lists, when its Mass schedule names no church, stays in `open/` until a source assigns it a Mass or dates a closing. (map batches `burlington-bordentown` and `keyport-matawan-union-beach-holmdel`, 2026-10-30)
- A seasonal shore church keeps its church row with a dated revisit for its next season, on an off-season bulletin or the parish's own winter schedule. (accepted by survey-review, 002-survey-review, 2026-10-30) Of the places the survey named (Long Beach Island, the Seaside/Lavallette barrier island, Deal, Manasquan's Star of the Sea chapel), only Long Beach Island's island churches close for the winter; the others list year-round Masses (Deal's revisit only reads its summer schedule). Before treating a church as seasonal, compare its Mass line in a winter issue (November, or January-March) with a summer one, and read the parish's seasonal schedule block and Mass page; a church marked CLOSED off-season but listed with summer Mass keeps its row with a spring revisit. (reconcile, 045-reconcile, 2026-10-30; map batches `spring-lake-sea-girt-manasquan`, `long-branch-west-long-branch`, `bay-head-lavallette-seaside` and `barnegat-lbi-little-egg-harbor`, 2026-10-30)
- When a parish's printer's listing (John Patrick, Bon Venture) and its own site carry the same bulletin, the row reads whichever channel has the latest issue, keeping the other's id in publication. (accepted by survey-review, 002-survey-review, 2026-10-30)
- A church's coordinates come from GCatholic's Plus Code or an OSM address lookup (nominatim via `probe get`), compared with each other, not from the finder's pin alone: a pin can be kilometres off or sit by another of the parish's churches, open or closed. Match a finder entry to a church by address, ZIP+4 (compared within one source), phone, an OSM house lookup and the Plus Code, not by the pin. A single OSM point needs the Plus Code beside it: a named node can be hundreds of metres off. (map batches `holmdel-marlboro-colts-neck`, `red-bank-rumson-fair-haven`, `willingboro-beverly`, `asbury-park-neptune-bradley-beach-belmar` and `long-branch-west-long-branch`, 2026-10-30)
- A slug for a common saint's name can already be another diocese's live row (st-john-the-baptist-allentown is Allentown, PA): run `pnpm diocese search` before writing a record and add the state when it collides (`st-john-the-baptist-allentown-nj`). (map batch `hamilton-yardville-allentown`, 2026-10-30)
- Weekday Masses a bulletin lists at a cohort neighbour's church, or a linked parish's whole schedule printed in another's bulletin, neither make a shared bulletin nor add a church to that parish; the church stays with its own parish. Linked parishes that each print a bulletin, even with one combined Mass table, keep separate rows when md5, mastheads and Mass intentions for the same Sunday differ, with `separate` publication_reviews (create both rows before the review). (map batches `holmdel-marlboro-colts-neck`, `trenton-cathedral-city` and `eatontown-monmouth-beach-wayside`, 2026-10-30)
- GCatholic's three chapels (St. Catherine, Farmingdale; Star of the Sea, Manasquan; St. Mary, New Monmouth) keep a church row when the parish bulletin lists public Mass there, weekday Mass included. The Mass may appear only in the schedule block, or under another name (St. Mary, New Monmouth is a named shrine's Mass line): grep the bulletin for "Chapel" and the site for the chapel's street address before excluding one. (map batches `howell-farmingdale` and `middletown-keansburg-atlantic-highlands`, 2026-10-30)
- A chapel a parish lists for daily Mass with no street address of its own is part of the church's campus, not a second church row. A chapel the parish lists with its own street address and daily Mass is a church row (St. Isidore the Farmer, New Egypt's Assumption Chapel, 76 Evergreen Rd). (map batches `jackson-lakehurst-whiting` and `mount-holly-browns-mills-new-egypt`, 2026-10-30)
- When a bulletin's street number differs from the finder's and GCatholic's, look each up in OSM (nominatim) for the named place of worship (the masthead's can be a neighbouring house); use the masthead's number, record the others, and leave `address_verified` false while they disagree. Every source's address can be the parish office or rectory: take the church's from the bulletin's own church line or the site's Contact page. (map batches `princeton-west-windsor-hightstown`, `ewing-west-trenton-trenton-north`, `bay-head-lavallette-seaside` and `brick-lakewood`, 2026-10-30)
- A language community styled a parish on the finder or GCatholic that worships in another parish's church, with its Masses in the host's bulletin (Korean Martyrs at St. Michael, Trenton), gets no church row of its own: link all its roster entries to the host's church row. (map batch `lawrenceville-korean-martyrs`, 2026-10-30)
- A GCatholic entry is matched to a church by street address, not name: one with no live site, or under a merged-away parish's name, can be a merged parish's present church, an absorbed campus or its second church under the old name ("Divine Mercy" is Sacred Heart, Trenton's Holy Cross Church), and one carrying another parish's website can be its mission. Before excluding one, read the Mass schedule of every church the host's bulletin names, and match by phone, the old bulletin header and Discover Mass's name. (map batches `ewing-west-trenton-trenton-north`, `bay-head-lavallette-seaside`, `brick-lakewood` and `toms-river`, 2026-10-30)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: Hand refresh against main (PR #179, branch `refresh/trenton-map-1`): main merged in,
  then a reconcile and an integrate by hand under main's rules, no new batches (the 30 map batches
  of 2026-10-30 stand). Coverage: directory 98/98 accounted for (94 modelled as churches on the
  site), GCatholic 136/136 (116 of the 122 non-excluded modelled). 93 parish rows, 4 of them
  `unsupported` with a `fetch_gap` (Immaculate Conception, Eatontown `extensionless-download-link`;
  Epiphany, Brick `joomla-weblink-redirect` and St. Catharine, Holmdel
  `constant-contact-html-newsletter`, both `no_bulletin` until now; St. Mary, Colts Neck
  `first-pdf-not-current`), 125 churches, 14 exclusions, 3 open. Three `open/` records became
  closed exclusions on sources found by web search: Holy Angels, Hamilton (last Mass 2 July 2017),
  Christ the Redeemer, Mount Holly (23 May 2021) and Our Lady of Peace, Normandy Beach (closed
  after Sandy, demolished 2016). Renamed `st-joseph-millstone` to `st-joseph-millstone-township`
  (parish and church), since Metuchen's St. Joseph, Millstone takes that slug. Nothing merged or
  moved. `audit --fetch`: 239 pairs, all `separate` (5 new reviews for the two rows that left
  `no_bulletin`). `fetch:check` on all 91 rows it read: 86 picked the 8 November issue; St. John
  Neumann, Mount Laurel's eCatholic site was a week behind its John Patrick listing, so the row now
  reads the listing (rechecked: 8 November); St. Mary, Colts Neck and Immaculate Conception became
  `unsupported` (above); St. Dorothea's site was down and Precious Blood's page still ends at 25
  October (both in `research`). The playbook's two sections were condensed to their targets.
- 2026-10-30: Reconcile (045-reconcile) after 30 map batches (4-12 roster entries each, usually
  about 8). Coverage: directory 98/98 accounted for (96 modelled as churches on the site),
  GCatholic 136/136 (118 of the 125 non-excluded modelled). 93 parish rows (2 `no_bulletin`:
  Epiphany, Brick; St. Catharine, Holmdel), 125 churches, 11 exclusions, 6 open. Nothing merged
  or moved between parishes. St. Paul, Princeton now reads John Patrick listing 694 (the latest
  issue, per the settled rule). St. James Chapel, 6 Eglantine Avenue, Pennington became a church
  row under the settled chapel rule. Princeton's campus ministry (Aquinas Institute) went to
  `open/`. The 180 unresolved audit pairs (cohort neighbours, 130 of them on the shared Bon
  Venture host, and two pairs from stray eCatholic embeds) got `separate` reviews citing both
  rows' masthead evidence. `fetch:check` on all 91 bulletin rows: 90 picked their parish's 25 Oct or
  1 Nov issue (St. Francis, LBI's 1 Nov file is misdated by the resolver as 1 Jan); Immaculate
  Conception, Eatontown can't be collected (extensionless `opendoc.asp` links). The seasonal-shore rule now
  says which places were found year-round.
- 2026-10-30: Initialised (factory survey, Run trenton-map-1). Rosters: the diocese's parish
  finder as `directory` (98 pins: 97 parishes and the merged St. Mary of the Lake), GCatholic
  (136 entries, 8 of them Eastern Catholic). Planned 30 map batches in `batches.json` from the
  July 2024 cohort list (234 entries, none excluded). No records yet.
