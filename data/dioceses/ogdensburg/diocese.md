---
name: Roman Catholic Diocese of Ogdensburg
state: NY
website: https://www.rcdony.org
status: promoted
gcatholic: ogde0
promoted: 2026-10-17
---

The North Country: Clinton, Essex, Franklin, St. Lawrence, Jefferson, Lewis and Hamilton
counties and the Old Forge/Inlet corner of Herkimer. The diocese has no family or cluster
list. Its structure is spread across its directory's "Worship sites" lines and the parishes'
own "Catholic Community of ..." names, and many rural parishes publish one bulletin for two
to five churches. It was explored in full on 2026-09-30, in eight regions with one agent
each, followed by a cross-region pass. See the *Log*.

## Sources

- **Parish directory (`rosters/directory.json`):** https://www.rcdony.org/directory/parishes.html
  is a Nicepage site in plain HTML, with no Cloudflare. It has 100 church links to 78 detail
  pages, `rcdony.org/parish/<slug>`, one section per worship site. Each section has the
  address, a "Worship sites:" line (the diocese's grouping), phone, website, pastor and
  mailing address.
  - **Roster ids:** the id is the page slug, with `-N` for the Nth site on a page.
  - **Hogansburg:** the Hogansburg page (St. Regis Mission, Akwesasne) gives only a Quebec
    address and was added by hand.
  - **No Mass times, and no coordinates.**
  - **The "group" field is sparse and unreliable for structure.** Gouverneur/Edwards/Star
    Lake, Canton/Potsdam/Colton, Brushton/Hopkinton/North Bangor/St. Regis Falls and
    Clayton/Alexandria Bay each publish one bulletin, but the directory gives no group for
    them or splits them.
  - **Street numbers often disagree with the parish's own by a few digits.** Examples:
    Canton 66/68, Potsdam 17/20, Cathedral 415/401, Peru 3029/3035, Rouses Point 140/138.
    Each case is written up in the church record, with the flag left false.
  - **Some website links are dead or wrong:**
    - `sj-sm.org` (Carthage) is dead, and `stcyrils.org` gives 403 or a TLS error.
    - `stbernards.church` returned 502 with an expired certificate on 2026-09-30.
    - `fultonchaincatholic.rcdony.org` (Inlet) is an old link.
    - Several entries have no website at all: Chazy, West Chazy, Dannemora, Redford, Keene,
      Lake Pleasant, Wells, Harrisville and Lisbon.
  - **Omissions:** it leaves out every closed church and oratory, and a few current worship
    sites: the Holy Ghost Chapel (Tupper Lake) and the Tabernacle (Thousand Island Park).
- **Parish Bulletins page:** https://www.rcdony.org/directory/parish-bulletins.html lists one
  link per town and is the best single lead list. It is partly stale:
  - **A for-sale domain:** Elizabethtown's link is `wewe4.org`, and the PDF there answers
    HTTP 441.
  - **Dead or old links:** Gabriels points to the dead `stbernards.church`, and Keeseville
    to an old ParishesOnline account name.
  - **Towns with no link, or "#":** Altona, Champlain, Chateaugay, Constableville, Croghan,
    Fort Covington, Inlet, Morrisonville, Sackets Harbor, Saranac Lake, and every Hamilton
    County church.
  - **Diocese-hosted PDFs:** three small parishes' bulletins are rolling PDFs on rcdony.org
    itself (`images/Harrisvillebulletin-1.pdf`, `images/SR-SSPJbulletin.pdf` for
    Heuvelton/Lisbon, and `images/ourladylourdes.pdf` for Schroon Lake). These are the
    parish rows' websites.
- **GCatholic (`rosters/gcatholic.json`, key `ogde0`, 126 entries):**
  - **It omits the cathedral** (its own entry is #2086).
  - **It still lists nearly every closed church and oratory as "Church":** Philadelphia,
    Theresa, Deferiet, La Fargeville, Bombay, Hogansburg, Holy Name (Tupper Lake),
    Bloomingdale, Lake Clear, St. Joseph (Massena), Raymondville, North Lawrence, and the
    Malone missions.
  - **Some addresses are copied from another church.** Philadelphia and Theresa both show
    Evans Mills's "8408 S Main St".
  - **Some addresses belong to the parish office**, not the church (Brownville, St. Agnes,
    Notre Dame Ogdensburg). Some Plus Codes land on the wrong building (Elizabethtown, on a
    credit union; Westport, on the Protestant Federated Church).
  - **St. William, Long Point, is not Catholic:** it is filed under "Long Lake" and is now
    non-denominational.
  - **Under a burst of requests** it serves a "One moment, please..." / "Loader" page. Since
    2026-09-30 `recheck` retries once and then reports such a page as unreachable.
- **Wikipedia, "List of churches and parishes in the Diocese of Ogdensburg":** good for
  missions, oratories and mergers that neither roster explains. It covers Sciota, West Peru,
  Coopersville, Cumberland Head and Deferiet. Too coarse for current Mass.
- **Closure and news sources:**
  - **Watertown Daily Times** (nny360.com): paywalled articles keep their body
    ROT47-scrambled in the raw HTML. A browser (`visit.py --text`) shows the text, but
    `recheck` can't find quotes from those articles.
  - **WWNY, the Adirondack Daily Enterprise and the Press-Republican:** the Enterprise is
    reachable through dailygazette.com URLs.
  - **Parish history pages:** `standres.org/#history` is especially good, with Malone's
    mergers and its 2007 mission closures.
  - **Chancery decrees:** the 2019 decrees are posted on `rivercatholics.org/parish-consolidation`
    as files.ecatholic.com PDFs.
  - **The 2018 pastoral plan** for the Chateaugay area is at `ccfcatholics.com/pastoral-plan`.
  - **North Country Catholic** (northcountrycatholic.org), the diocesan weekly, had little
    on the closures.
  - **Blocked or dead:** Malone Telegram and some nny360 URLs 404, and web.archive.org is
    blocked from the sandbox.
- **The diocese's 2026 "Rapid Pre-Pack Chapter 11" letter** is bankruptcy news, not a parish
  reorganization.
- **Discover Mass and catholicmasstime.org list stale times** (Saturday Mass at St. George,
  Burke; St. Lawrence, North Lawrence). They were used only for places with nothing better,
  and those records say so.

### Bulletin publishers here

Of the 36 parish rows, 14 are ParishesOnline, 11 eCatholic and 11 `other`.

- **eCatholic sites are behind Cloudflare.** Every eCatholic parish site here is behind
  Cloudflare (`probe url` HTTP 403). `visit.py` loads them in 1 to 8 tries; spsmshcatholic.org's
  home page never loaded, but its /bulletins page did. Their dated files at
  `files.ecatholic.com/<id>/bulletins/YYYYMMDD.pdf` fetch with plain curl. River Catholics
  (21398) is the exception: it uploads free-form "September 27 2026.pdf" documents under
  `/documents/2026/9/`, which `issues.py ecatholic` does not find.
- **Rolling PDFs overwritten weekly** (`other`):
  - Cape Vincent: `cvrchparish.org/files/bulletin.pdf`.
  - Waddington/Madrid: `mwcatholics.org/files/bulletin.pdf`.
  - Old Forge/Inlet: `fultonchaincatholics.org/files/bulletin.pdf`.
  - The three rcdony.org PDFs above.
  - Heuvelton/Lisbon's PDF was still the 13 September issue on 30 September.
- **Other self-hosted hosts:**
  - Ellenburg (`cathcommsbse.org`) posts a new file name weekly on its home page.
  - Southern Lewis County uses Weebly.
  - Carthage/Copenhagen has its own bulletins.html page.
  - Lake Placid uses John Patrick Publishing (`church-bulletin.org/saint-agnes-saint-brendan-lake-placid-ny-12946`).
- **Image-only bulletins are common, roughly one in three.** Read them with `render.py`;
  the pipeline will have to read them as images.
  - Blessed Sacrament, Watertown (06/0117): pages 1–6.
  - St. Bernard, Saranac Lake (06/0140): pages 1–4.
  - Ticonderoga (03/0940): pages 1–3.
  - Norfolk/Norwood/Brasher Falls (ecatholic 15674).
  - KAW (35001), Mooers Forks/Altona (17009) and Champlain (15646).
  - Lowville (19929), in most issues.
  - Carthage/Copenhagen.
  - Lake Placid, in some issues.
  - Our Lady of Grace (5458): the masthead is an image.
- **Broken text layers:** OLSH Watertown (06/0110) triplicates its masthead and
  letter-spaces its schedule, and Canton/Potsdam (04/0642) letter-spaces page 2. Quotes are
  copied in the extracted form.
- **ParishesOnline account names are old.** Blessed Sacrament's account is "St. Patrick's
  Church" (`st-patricks-`). Brushton's account lists two of its four churches. Massena's LPi
  footer still names St. Joseph. Read the masthead.
- **Coming changes:** Ogdensburg and Canton are moving their bulletins from Publisher to
  Canva, and Lowville is changing its publishing system from 4 October 2026 (`revisit` on
  its row).

### Fetch check (2026-10-17, after re-promotion)

The rows were promoted again on 2026-10-17 after main gained fetch-only parishes, so every
Ogdensburg parish is `fetch_only`: its bulletins are fetched weekly but not extracted or shown
until the flag is cleared. `fetch:check` over all 36 rows that day: **36 ok, none blocked**
(the five eCatholic sites Cloudflare blocked on 30 September all loaded). Each pick was
checked by hand:

- **This week's issue (18 October)** for 30 rows: all 14 ParishesOnline, 8 of the 11
  eCatholic, and 8 `other` (Cape Vincent, Old Forge, Waddington and Harrisville by the
  content of their overwritten PDFs; Carthage, Ellenburg and Lake Placid by date; River
  Catholics by its link text, as the file is misnamed "October 11 2026 -1.pdf").
- **The newest posted, a week old (11 October)**, for Chateaugay (18168), Mooers Forks
  (17009) and Tupper Lake (15094): `issues.py` found no 18 October file for any of them yet;
  and Schroon Lake's overwritten PDF.
- **Stale at the source:** Southern Lewis County's page lists nothing after 13 September,
  and Heuvelton/Lisbon's PDF is still the 13 September issue (Last-Modified 14 September,
  still the diocese's link for both towns). `fetch` downloads both addresses again each week,
  so a new issue is picked up when the parish posts it.

Recipes are pinned on all 11 `other` rows (each record says what its recipe picked), and a
second run with them pinned picked the same 11 files. Cape Vincent, Old Forge, Carthage and
Waddington are new replay fixtures, so 11 Ogdensburg sites are recorded.

## Rules settled for this diocese

- **Two rows stay separate although both bulletins print the same Masses,** because each has
  its own live channel (the Albany Saratoga Springs precedent). Each pair has one pastor,
  and the pipeline will see some Masses twice.
  - **Schroon Lake and Ticonderoga:** Our Lady of Lourdes posts its own PDF, and the
    Southern Adirondack Catholic Community bulletin (03/0940) also lists it. `audit` flags
    this group.
  - **Champlain and Rouses Point:** St. Mary's, Champlain (ecatholic 15646) and St. Patrick's,
    Rouses Point (15896).
  - **OLSH Watertown and the River Catholics:** OLSH's bulletin (06/0110) prints the
    River Catholics' Masses too.
- **Shared pastors don't make shared bulletins.** Croghan and Harrisville (Fr. Morgan)
  publish separately. From 1 November 2026, Massena's pastor also takes Waddington/Madrid,
  and mwcatholics.org says the parishes "will be linked". `revisit` on `st-marys-waddington`:
  merge only if its PDF stops and the Massena bulletin carries both.
- **An oratory with no regular Mass is `closed`,** with the year or month in `last_mass` when
  a source gives no day (for example St. Joseph, Massena, 2017; St. Rita, Deferiet,
  2019-06). "Oratory" here means the parish keeps the building for weddings and funerals.
  A closure dated only by a plan stays `open`: All Saints, Mineville (last regular Mass
  2025-10-25, "on track to shutter").
- **An open church whose parish publishes nothing readable is `no-bulletin`.** That covers
  Chazy, West Chazy, Dannemora, Redford, and the Olmstedville/Indian Lake/Blue Mountain Lake
  parish, whose eCatholic site has an empty Bulletin page. Lake Pleasant and Wells, with no
  site and a login-walled Facebook page, are `open`. Several of these probably post a
  bulletin on Facebook, which can't be read without a login.
- **Summer chapels in a current bulletin's schedule are churches.** These include
  Thousand Island Park, Redwood, Westport, St. Joseph (Essex), Glenfield and Rosiere. Their
  *Holds Mass* section says which season.
- **Care-home, senior-residence, prison and monastery Masses are not churches** without a
  statement that the public may attend. That covers Elderwood (Lake Placid), Mercy (Tupper
  Lake), United Helpers and Partridge Knoll (Canton), Champlain Valley Senior Community
  (Willsboro) and St. Dismas (Clinton Correctional). The Precious Blood monastery's daily
  Mass is `open`.
- **The St. Regis Mission at Akwesasne is `other-jurisdiction`.** It is on the Quebec side
  and belongs to the Diocese of Valleyfield, although the directory lists it under
  Hogansburg.

## Log

- 2026-10-17: Re-promoted as fetch-only after merging main (36 parishes, 92 churches,
  unchanged). `fetch:check`: 36 of 36 ok; 11 recipes pinned (see "Fetch check (after
  re-promotion)"). Two rows are stale at the source: Southern Lewis County and
  Heuvelton/Lisbon.
- 2026-09-30: Explored the whole diocese. I scraped the diocese's parish directory into
  `rosters/directory.json` (101 entries) and fetched GCatholic's list (126). Both were
  split into eight regions, researched in parallel, and followed by a cross-region pass.
  That pass settled Deferiet (in the Lewis region's list, belonging to Black River's
  parish), normalized oratories to `closed`, and added year-only `last_mass` dates.
  - **Result:** 36 parish rows (14 ParishesOnline, 11 eCatholic, 11 other) and 92 churches.
  - **Exclusions:** 29 — 18 closed, 7 no-bulletin, 2 no-public-mass, 1 other-jurisdiction
    and 1 other (St. William, Long Point).
  - **Open questions:** 13.
  - **Coverage:** directory 101/101, GCatholic 126/126. Two churches are in no roster: the
    Holy Ghost Chapel and the Tabernacle.
  - **Audit:** one group spans rows (Southern Adirondack), with separate bulletins recorded.
  - **Promoted.**
  - **Fetch-check:** a live `fetch:check` of the 36 rows first found 24 ok, 8 blocked
    (eCatholic sites behind Cloudflare), 4 failing and 3 picking the wrong PDF. The resolver
    fixes cover these cases:
    - A website that is itself the PDF.
    - Ellenburg's dated "Download File" links.
    - Lake Placid's church-bulletin.org listing.
    - Weebly's numbered folders, which were read as a date.
    - River Catholics' "20026" typo.
    - Weekly-overwritten PDFs, which `fetch` now downloads again.

    After them, every non-eCatholic row resolves to its current bulletin. Seven sites are
    replay fixtures. Five eCatholic sites stayed Cloudflare-blocked through three sandbox
    runs: Chateaugay, Oswegatchie, Our Lady of Grace, Champlain and Rouses Point. For each,
    `issues.py` confirmed a current issue at `files.ecatholic.com/<id>/bulletins/`.
