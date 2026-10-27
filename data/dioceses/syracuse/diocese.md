---
name: Roman Catholic Diocese of Syracuse
state: NY
website: https://www.syracusediocese.org
status: promoted
gcatholic: syra0
city_aliases:
  Port Crane: Sanitaria Springs
promoted: 2026-10-27
---

Seven counties of central New York: Onondaga (Syracuse), Oneida (Utica, Rome), Madison,
Oswego, Cortland, Chenango and Broome (Binghamton). Explored in full on 2026-09-26, region
by region; every entry of the diocese's own parish-finder map and of GCatholic's list is a
church, an exclusion or an open question. Promoted into `data/parishes.csv` and
`data/churches.csv` on 2026-09-26; see the *Log* for the numbers.

## Sources

- **Parish finder (the directory roster):** https://www.syracusediocese.org/parishfinder,
  an eCatholic Mass-times map, read with the parish-site-access skill's `finder.py` into
  `rosters/directory.json` (202 entries). One entry per site, with the finder's map pin,
  address, phone and website. 71 entries are "<Name> (Closed)" with no address; many
  "Parish @ Church" names give the diocese's own grouping. Websites are often stale (renamed
  or dead domains), and some pins are wrong (the St. Charles pin sits on the former
  St. Ann's). Behind Cloudflare: `visit.py` loads it, usually on the first try.
- **Alphabetical parish list:** https://www.syracusediocese.org/parishes. Lines such as
  "St. Agnes, Brewerton (CLOSED - See Divine Mercy ...)" or "St. Cecilia, Solvay (See St.
  Marianne Cope Parish ...)" give the successor of every closed or merged parish. Each
  successor's page (`syracusediocese.org/<parish>`) has the church and office addresses,
  clergy, and "Sacramental records for X are retained here" lines: the best closed-parish
  index there is. Several closed parishes on this list are in neither roster (St. Bridget
  Solon, St. Patrick Norwich, St. Agnes Vernon Center, St. Catherine Vernon, Immaculate
  Conception Hamilton, St. Ann Brookfield, St. Anthony Morrisville, St. John Chrysostom
  Hawkinsville, and the Oswego County missions at Redfield, Boylston, Colosse, Little France
  and Mexico). They are not recorded: nothing places a building for them in 2026.
- **GCatholic:** `rosters/gcatholic.json` (key `syra0`), 151 entries with Plus Codes on the
  building. It omits the cathedral and the Basilica of the Sacred Heart, and includes eight
  Eastern Catholic churches (marked `rite`). Some addresses are a side street or an office.
- **Decrees:** the diocese's news stream
  (`syracusediocese.org/aggregateStream/NEWS?startItem=0&numberItems=400`, in `visit.py`
  with `--links --match decree`) lists every merger and relegation decree. A
  `syracusediocese.org/documents/...` PDF answers 403 to plain fetches, but the same file is
  at `files.ecatholic.com/31250/documents/<same path>`. Most decree PDFs are scans.
- **The Catholic Sun** (thecatholicsun.com, the diocesan paper) prints decrees in full with
  addresses and effective dates. Readable only in `visit.py` (WP Engine blocks curl).
- **Rome Sentinel** (romesentinel.com, fetchable with curl) dates Rome and Oneida closures.
- **Christ the Good Shepherd's heritage pages** (christthegoodshepherd.org/history-of-*)
  date the Oswego closures.
- **Discover Mass / MassTimes data** is stale for closures (it still showed a Friday Mass
  at North Bay): use it to find bulletins, not schedules.
- **Pastoral planning:** the Bishop's 2024 letter on parish configurations ("Bishop Letter
  Parish Configurations 5.26.24", linked from St. Margaret, Homer's site on
  files.ecatholic.com/1066) was not read; it would be the place to start a structure audit.

### Bulletin publishers here

About half the parishes are on LPi/ParishesOnline; the rest are Discover Mass, eCatholic,
John Patrick Publishing (church-bulletin.org) and self-hosted pages (WordPress, Duda,
Weebly, Designrr flipbooks). Things worth knowing:

- **Image-only bulletins are common.** Roughly one in five has pages with no text layer:
  St. Augustine (Baldwinsville), St. Mary of the Lake (Skaneateles), the Marathon/Whitney
  Point community, St. Ann (Manlius), St. Patrick (Chittenango), St. Rose (North Syracuse),
  St. Anthony and Assumption (Syracuse), Spirit of Hope (Oneida, a 31 MB scan in 2026), the
  Binghamton containers 03/0543 and 06/0167, St. Mary's (Oswego) and St. John (Camden).
  They were read by rendering the pages (`render.py`), and the pipeline will have to read
  them as images too. Evidence notes say when a page is an image.
- **`ecatholic:31250` is the diocese's own eCatholic site**, not a parish. Tools report it
  on any parish page that links a diocesan PDF.
- **John Patrick Publishing:** `jppc.net/onlinebulletins/<id>template.pdf` and
  `church-bulletin.org/<id>` redirect to `church-bulletin.org/<slug>`, which lists dated
  PDFs at `/bulletin/<slug>/<YYYY-MM-DD>.pdf` (Camillus, Christ the Good Shepherd, Camden).
  Recorded as `other` with `url:<church-bulletin page>`. The pipeline's `other` fetcher
  does not follow these yet.
- **Holy Spirit, Hamilton dates its eCatholic files by the Friday** before the Sunday
  (`20260925.pdf` for 27 September); `issues.py ecatholic --day fri`.
- **LPi generic inserts:** some ParishesOnline pages list only LPi's generic weekly insert
  (`generic-publications/pol/<date>GB.pdf`); that is not a parish bulletin (St. Patrick,
  Taberg).
- **Proxy trouble:** sacredheartbasilicasyr.org, mhrsyracuse.org and
  ourladyofpompei-stpeters.org (GoDaddy) answer 502 through the sandbox proxy most of the
  time; retry.

## Rules settled for this diocese

- **Eastern Catholic churches** in GCatholic's list are excluded as `other-jurisdiction`:
  they are Catholic, but belong to their eparchies (eight: Ruthenian, Ukrainian, Melkite,
  Maronite).
- **A "(Closed)" finder entry whose building is still a church** (the parish closed or
  merged, the building became the successor's church) is linked to that church row, not
  excluded: e.g. St. Therese → All Saints, Immaculate Conception (Fulton) → Holy Trinity,
  St. Ann (Binghamton) → Holy Trinity, St. Paul (Oswego) → Christ the Good Shepherd. The
  church record says which building it is and on what evidence.
- **A "(Closed)" entry is excluded as `closed`** only when the diocese's list says CLOSED
  *and* the successor's current schedule has no Mass there; both are quoted. Where a
  dated source for the last Mass was found it is in `last_mass`; the others carry the
  "closed without last_mass" warning.
- **A church with no Mass now for a stated temporary reason** keeps its row with a dated
  `revisit` when it is still the parish's church (St. Charles, Syracuse: renovation), and is
  excluded as `closed` when the parish has moved on and is "weighing options" (St. Patrick,
  Oneida: unsafe ceiling since December 2024). Both are written up in their records.
- **Shared pastors don't make shared bulletins.** Several priests serve two or three
  parishes (Baldwinsville, Camillus/Jordan, Manlius/Fayetteville, Cazenovia/Chittenango,
  the Kurgan and Foley groups in Syracuse, Norwich, Vestal/Endicott); each is one row per
  bulletin actually published, recorded under a `group` so `audit` checks it.
- **Campus ministries and chapels with public Mass** are churches under the parish whose
  bulletin prints their schedule (Colgate Memorial Chapel, Hall Newman Center in Oswego,
  O'Heron Newman Hall in Cortland), or `no-bulletin` exclusions when nobody prints it
  (Alibrandi Center at Syracuse University, Newman House at Binghamton University).

## Log

- 2026-09-25: Rebuilt the example in the one-file-per-record format. Fetched the GCatholic
  roster. Confirmed the cathedral's bulletin (ParishesOnline container 06/0091, weekly
  through 2026-09-27) and pinned its publication ids. Holy Spirit's bulletin could not be read
  (Cloudflare); its four churches are recorded from GCatholic, the 2020 merger report and OSM,
  with Mass not confirmed. Excluded the Syracuse University Catholic Center as `no-bulletin`
  (public Mass, nothing published) rather than as "not a parish". Coverage: 5 of 151
  GCatholic entries accounted for.
- 2026-09-26: Explored the whole diocese. Imported the diocese's parish-finder map as
  `rosters/directory.json` (202 entries), split both rosters into eight regions by town, and
  researched them in parallel (one agent per region, then a cross-region pass). Result: 73
  parish rows (36 ParishesOnline, 23 self-hosted or other, 8 Discover Mass, 6 eCatholic), 122
  churches, 85 exclusions (66 closed, 9 no-bulletin, 8 other-jurisdiction, 1 not-catholic,
  1 other: the Truxton oratory, open for prayer without Mass) and 1 open question
  (Transfiguration Monastery, Windsor). Coverage: directory 202/202, GCatholic 151/151; three
  churches are in no roster (Colgate Memorial Chapel, Hall Newman Center in Oswego, O'Heron
  Newman Hall in Cortland). `audit`: 14 shared-pastor groups, each with separate bulletins
  recorded. `recheck`: every quote found except on pages behind Cloudflare
  (syracusediocese.org and six parish sites, each noted as read in a browser) and one
  Designrr flipbook. Corrected Holy Spirit's merger from 2020 to 1 July 2026 (the articles
  are dated June 2026; the weekdays fit both years). Promoted.
- 2026-10-07: Audited the churches the site showed with no Mass. St. Mary's Oratory, Jamesville
  (last Mass found 9 October 2025; Holy Hours since) moved to `open/` with `diocese question`.
  Stay church rows with no Mass this week: St. Charles, Syracuse (closed for renovation since
  August), St. Mary of Mount Carmel, Florence (one Mass a year), and O'Heron Newman Hall and St.
  Lawrence, DeRuyter (weekly Masses that the 4 October Cortland bulletin did not print; the site
  reads only each parish's latest bulletin). Holy Cross, DeWitt has posted nothing since its 6
  September issue. Promoted.
- 2026-10-27: St. Mary, Irish Ridge turned from `excluded/` (closed) into a church row: the
  parish's All Souls' Day Mass is held there (3 November 2025, 2 November 2026), the trigger its
  exclusion named. Noted on Prince of Peace (North Endicott) that its bulletin's "CHF" adoration
  is at Church of the Holy Family, Endwell, another parish. Promoted. Coverage: directory 202/202;
  GCatholic 151/151.
