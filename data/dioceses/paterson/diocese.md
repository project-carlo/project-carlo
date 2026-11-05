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

From the survey's sample (2026-11-04): `probe url` on all 116 finder websites, and
`visit.py --bulletin` on 12 of them.

- **eCatholic hosts nearly every parish site,** behind Cloudflare: 95 of 116 sites answer
  `probe url` with 403; `visit.py` loaded all 12 tried on the first pass. The bulletin is at
  `files.ecatholic.com/<site id>/bulletins/<YYYYMMDD>.pdf` (`issues.py ecatholic`), with no
  Cloudflare. The finder pin id is usually the site id. Some sites post no Sunday-dated file
  (St. Brendan & St. George 11777, Fatima & St. Nicholas 14272, St. Paul Clifton 6361 found
  nothing for 25 Oct–8 Nov): open their `/bulletins` page and read the real file names.
- **`ecatholic:5303` is the Diocese of Paterson's own site,** reported on any parish page that
  links rcdop.org. Don't record it.
- **Padre Pio Parish's PDF text is broken font encoding** (page 1 of the 1 November issue
  reads as symbols): render pages to read it.
- **Bon Venture** (`sponsors.bonventure.net`, use `http://`; see Scranton and Allentown): St.
  Paul, Clifton and Resurrection, Randolph link it.
- **John Patrick Publishing** (`jppc.net` / `church-bulletin.org`): St. Andrew the Apostle,
  Clifton and St. Joseph, Lincoln Park link it.
- **Discover Mass's daily download cap and Paluch joint bulletins** (Scranton, Allentown)
  weren't seen in the sample; expect them in a few parishes.
- **Odd sites:** olmcboonton.org redirects offsite; stscm.org (Sts. Cyril & Methodius,
  Boonton) renders in JavaScript.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- eCatholic sites here can keep a stale bulletins/<YYYYMMDD>.pdf archive (2018-2023 in this batch) while the current bulletin is elsewhere: a Bon Venture link at the top of /bulletins, or PDFs in files.ecatholic.com/<id>/documents/<y>/<m>/ listed on a custom page (/parish-bulletins, /parish-updates). Read the /bulletins page first links before running issues.py; for documents-folder bulletins use a page-pdfs recipe on the listing page.
- page-pdfs dates eCatholic documents-folder links only by their label, not by the URL-encoded file name (Month%20D%20YYYY.pdf), so an undated label makes it pick an older issue: check the date of the pick in fetch:check (fetch_gap kind undated-link-label).
- Bon Venture PDFs here often have a garbled text layer or an image-only masthead page: render page 1 with render.py to read the masthead; fetch:check then reports identity unverified, which is expected.
- ParishesOnline prints here too: an eCatholic site's bulletin page (e.g. /bulletins-1) can embed parishesonline.com/publication-page/<org slug> issues. Record po-org/lpi/po-container from probe po, not the eCatholic site id. Their pages can be image-only, so render page 1 to read the masthead.
- John Patrick Publishing here: an eCatholic /bulletins page links jppc.net/onlinebulletins/<customer>template.pdf, which redirects (HTML, not a PDF) to a church-bulletin.org/<parish-slug> listing of bulletin/<slug>/<YYYY-MM-DD>.pdf issues. Record url:<listing> and use page-pdfs on the church-bulletin.org listing; fetch:check dates the pick from the file name.
- A Bon Venture ad footer (e.g. '150C (PK) - <parish> ... Bon Venture Services') also appears in bulletins the parish posts on eCatholic; it doesn't mean Bon Venture hosts the issue. Record the host the site's bulletin page links (eCatholic bulletins/ files or a sponsors.bonventure.net/?page=<n> link).
- page-pdfs on a monthly newsletter listing (labels like 'November 2026') picks the right issue as first-listed, but fetch:check reports date and freshness unknown: check the pick by hand.
- Some eCatholic bulletins here have a text layer shifted by 29 code points (e.g. '0$66(6' for 'MASSES', digits dropped): probe pdf text can't give Mass times, so render page 1 with render.py; fetch:check reports identity unverified.
- Finder and GCatholic addresses here can be the parish office rather than the church (finder pin on the office too): take the church address from the bulletin masthead and check it against the OSM building or the GCatholic Plus Code.
- fetch:check can report an issue-date conflict when an eCatholic issue has a one-off cover with a non-Sunday date (e.g. a pastor's birthday): check the date on page 2 and the previous issue's page 1 before deciding the pick is stale.
- Finder pins here can be a street geocode rather than the church building (one 2.7 km off, another on the road way about 230 m away): prefer the GCatholic Plus Code once OSM confirms it.
- Parishes here often post next Sunday's issue mid-week: fetch:check then reports freshness 'future' (age -4 days) for the newest file, which is the correct pick; confirm the masthead date rather than treating it as an error.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Melkite: Eparchy of Newton; Armenian: Eparchy of Our Lady of Nareg) and St. George, Paterson, now the Syro-Malabar parish (Eparchy of Chicago), are excluded as other-jurisdiction. (accepted by survey-review, 002-survey-review, 2026-11-04)
- A merged parish whose bulletin still lists Mass at both former parish churches is one parish row with both churches (Padre Pio: St. Bonaventure and Our Lady of Pompei). (accepted by survey-review, 002-survey-review, 2026-11-04)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-04: Survey (factory run paterson-map-1). Created the diocese; rosters `gcatholic`
  (122) and `directory` (117, the eCatholic parish finder with Mass times); planned 30 batches
  in `batches.json`. No parish records yet.
