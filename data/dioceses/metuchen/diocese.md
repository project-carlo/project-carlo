---
name: Roman Catholic Diocese of Metuchen
state: NJ
website: https://diometuchen.org
status: exploring
gcatholic: metu0
city_aliases:
  Woodbridge Township: Woodbridge
  Old Bridge Township: Old Bridge
  Hillsborough Township: Hillsborough
  Piscataway Township: Piscataway
  Plainsboro Township: Plainsboro
  Oxford Township: Oxford
---

Four counties of central and northwestern New Jersey: Middlesex (New Brunswick, Perth Amboy,
Edison, Woodbridge, Metuchen, Old Bridge, Sayreville), Somerset (Somerville, Bridgewater,
Raritan, Manville, Bernardsville), Hunterdon (Flemington, Lambertville, Clinton area) and Warren
(Phillipsburg, Washington, Hackettstown, Belvidere). The chancery is at 146 Metlars Lane,
Piscataway. It borders Newark (northeast), Paterson (north), Trenton (south), and across the
Delaware Allentown, Scranton and Philadelphia. GCatholic names those six neighbours; of them, only
Allentown is mapped. On its *About* page (read 2026-10-30) the diocese counts "90 Parishes" and
"15 Eastern Church parishes under the jurisdiction of their own bishops". Its 2024–2025 annual
report says "the 89 parishes". The difference is the North Plainfield merger of July 2025 (below).

**How it is organised.** There are eight deaneries (Cathedral, County Seat, Forsgate, Middlebrook,
Morris Canal, Raritan Bay, Round Valley, Somerset Hills), which the parish finder uses as its
categories. No families, clusters or pastorates were found. Instead, a dozen parishes
formed by earlier mergers keep several churches. Divine Mercy (Carteret), Good Shepherd
(Hopelawn), Most Holy Name of Jesus and St. John Paul II (Perth Amboy), Holy Family and the
Parish of the Visitation (New Brunswick), Transfiguration of the Lord (Highland Park/Edison),
Christ the Redeemer (Manville), St. Anthony of Padua (Port Reading/Woodbridge), St. John the
Evangelist (Lambertville/Stockton) and St. Elizabeth–St. Brigid (Far Hills/Peapack) list their
worship sites in the finder. GCatholic gives "parish 2010" (Holy Family, Carteret) and
"parish 2012" (three Perth Amboy/Hopelawn churches) for some of these. So shared bulletins are most
likely (a) inside a merged parish, (b) between the few pairs the finder gives one pastor (Belvidere/
Oxford, Iselin/Woodbridge, Frenchtown/Milford), and (c) among the three Raritan Oratory parishes.

## Sources

- **Parish finder (the `directory` roster):** https://diometuchen.org/parishfinder, an eCatholic
  map behind Cloudflare (`probe url` gets 403; parish-site-access `finder.py` reads it). Read
  2026-10-30: 91 pins, 90 parish entries (St. Elizabeth–St. Brigid has one pin per church,
  24487 and 25192). Each entry's *Details* tab gives the clergy and, for merged parishes, a
  "Worship Site(s):" list. Its Sunday Mass schedule names the church for each Mass in a note.
  `rosters/directory.json` keeps these as `deanery`, `clergy`, `finder_detail` and
  `mass_locations` (scraper: `scratch/metuchen-map-1/tools/finder_details.py` and
  `enrich_directory.py`). Good for: the parish list, deaneries, worship sites, and which
  church each Mass is at. How far to trust it:
  - **It lags on mergers.** St. Joseph (24517) and St. Luke (24518), North Plainfield still have
    their own entries and administrators. The bishop's decree (diometuchen.org/news/
    merger-of-st-joseph-st-luke-parishes, dated 30 May 2025, read 2026-10-30) merged them
    "effective July 1, 2025" with the name "Sts. Joseph and Luke". www.SJNP.org now redirects to
    sjlnp.org.
  - **Its clergy lines are partly stale.** It names Msgr. Joseph G. Celano as pastor of both
    Immaculate Conception, Somerville and St. Peter the Apostle, New Brunswick, but St. Peter's
    25 October 2026 bulletin (files.ecatholic.com/21126/bulletins/20261025.pdf, p. 2) reads
    "Rev. Michael Tabernero, Pastor". St. Philip and St. James carries a "(NOTE: Rev. Kusek
    effective in October 2019)". Treat a pastor shared in the finder as a lead, not a fact.
  - Its pins are parish offices or main churches. A merged parish's secondary churches have no
    pin, only lines in the Details text (hence the `worship-sites` roster).
  - Websites: 16 entries have none. The domains for Sacred Heart (South Amboy), St. Joseph
    (Carteret) and St. Theodore (Port Murray) don't resolve. St. Joseph, Raritan's
    `*.weconnect.com` address is unreachable. Several redirect to a new site (OLM South Bound
    Brook to Google Sites, St. Joseph Millstone to sjmillstone.com).
- **Worship sites (the `worship-sites` roster):** 25 entries built from the finder's Details
  lists (12 parishes), plus two places named only in Mass notes: "La Asuncion" (Spanish
  Masses of Most Holy Name of Jesus; GCatholic gives La Asuncion at 777 Cortlandt St) and
  "Sacred Heart Chapel" (a 9:30 AM Sunday Mass of OLPH, Bernardsville; no address). `group` is
  the parent parish. These are mostly the same buildings as GCatholic entries. St. Mary of Mount
  Virgin, New Brunswick is in no other roster, and GCatholic's "St. Lucy Filippini" (National
  Shrine, 190 Sanford St) has that church's address.
- **GCatholic (the `gcatholic` roster):** key `metu0`, fetched 2026-10-30. 123 entries: 107
  Latin, and 16 Eastern Catholic (`rite`: Ruthenian 9, Ukrainian 5 (one "Former Church"),
  Maronite 1, Syro-Malabar 1). It **omits the cathedral** (St. Francis of Assisi, Metuchen). It
  keeps churches of merged parishes that the finder no longer lists:
  - Sacred Heart (67 Fitch St) and St. Elizabeth of Hungary (119 Washington Ave), Carteret,
    beside Divine Mercy's Holy Family.
  - Holy Spirit (580 Hazel Ave) and St. Mary (104 Center St), Perth Amboy. GCatholic puts Holy
    Spirit under Good Shepherd Parish and St. Mary under Parish of St. John Paul II.

  It gives three shrines: Blessed Sacrament (50 W Somerset St, Raritan, shrinechapel.com), Our
  Lady of Fatima (674 Mountain View Rd E, Washington; the World Apostolate of Fatima shrine)
  and St. Lucy Filippini (above). Where the finder and GCatholic disagree on addresses:
  - St. Ladislaus, New Brunswick: 215 Somerset St (finder) or 40 Plum St (GCatholic).
  - Blessed Sacrament, Martinsville: the finder's worship site is 1890 Washington Valley Rd,
    while its pin and GCatholic give 852 Newmans Ln.
  - St. James, Woodbridge: 369 Amboy Ave (finder) or 148 Grenville St (GCatholic).
  - GCatholic puts St. Elizabeth in Peapack, not Far Hills, and Our Lady of Victories in
    Baptistown, where the finder says Frenchtown.

  Many of its websites are old (`*.4lpi.com`, `*.parishesonline.com`, comcast.net).
- **Clusters / families of parishes:** none. The diocese uses deaneries and canonical mergers;
  no family or cluster list was found on diometuchen.org. The finder's own clergy lines are the
  only diocese-wide shared-pastor source.
  - The finder gives one pastor to St. Patrick, Belvidere and St. Rose of Lima, Oxford (Rev.
    David J. Pekola; one website, stpatrickrose.org). It names him for Our Lady of Victories,
    Sayreville too, which is probably stale.
  - St. Cecelia, Iselin and St. James, Woodbridge (Rev. Thomas Naduviledathu, SDV).
  - Our Lady of Victories, Frenchtown and St. Edward the Confessor, Milford (Fr. Bede Kim).
  - St. Ann and St. Joseph, Raritan and Holy Trinity, Bridgewater are staffed by the Raritan
    Oratory (CO).
- **Mass times:** no separate diocese-wide Mass-times page; the finder's per-parish schedule is
  it (the `directory` roster's `mass_locations`). It also shows Masses in other languages and
  places (Coptic Catholic Mass in St. Ambrose's "St. Anthony Room", Old Bridge; Kiswahili and
  Tagalog monthly at St. Matthew, Edison).
- **Clergy list:** none found apart from the finder. ParishSOFT (metuchen.parishsoftfamilysuite.com)
  needs a login.
- **Closed parishes and where their records went:** no diocesan list found.
- **Pastoral plan / closure announcements:** none found. "One Church Together" is a 2023–24
  devotional campaign, not a plan. The diocese's news stream (aggregateStream/NEWS, 241 items
  back to about 2021, read 2026-10-30) has one structural item, the North Plainfield merger
  above. The earlier mergers (2010–2012 in Carteret and Perth Amboy) predate it. The diocesan
  paper *The Catholic Spirit* (catholicspirit.com) printed the decrees but answers 403 to
  `probe get`. Date those mergers and closures from the bulletins, GCatholic's history field or
  local news.

### Bulletin publishers here

From `probe url` on the 74 finder websites and `visit.py --bulletin` on 13 more (2026-10-30;
output in `scratch/metuchen-map-1/001-survey/`):

- **eCatholic** hosts most parish sites (34 distinct site ids on the probed sites). Unlike Allentown, they answered
  `probe url` directly here; only the diocese's own site and qomchurch.org returned 403. A site
  id is the website's, not proof the bulletin is there. St. Matthew, Edison's site embeds both
  `ecatholic:22680` and an LPi id, so read the bulletin page. **`ecatholic:21916` is the
  diocese's own site:** don't record it. Read issues with `issues.py ecatholic` at
  `files.ecatholic.com/<id>/bulletins/<YYYYMMDD>.pdf`.
- **ParishesOnline / LPi:** Transfiguration of the Lord (`po-container:04/1001`, behind a
  `/wordpress/` redirect), St. Patrick/St. Rose (`po-container:04/0870`), Our Lady of Lourdes,
  Whitehouse Station, St. Joseph, High Bridge, St. Matthew (LPi ids). Holy Family, New
  Brunswick posts LPi-named files (`20261011B-3.pdf`) on its own WordPress. Look for its
  container.
- **John Patrick Publishing** (`jppc.net/onlinebulletins/<id>template.pdf`, which redirects to
  `church-bulletin.org/<slug>`): Sts. Joseph and Luke (685), St. Joseph, Bound Brook (557),
  Annunciation, Bloomsbury (589), St. John Neumann, Califon (652), Divine Mercy, Carteret
  (church-bulletin.org/divine-mercy-parish-carteret-nj-07008). Allentown records it as `other`
  with a pinned `page-pdfs` recipe on the listing. It answers 406 to a bare "Mozilla/5.0" user
  agent.
- **Discover Mass:** the cathedral (`discovermass:st-francis-of-assisi-cathedral-metuchen-nj`).
  Discover Mass caps downloads per IP per day (a 134-byte "Maximum number of files downloaded
  today" reply, which `fetch:check` reports as `not_pdf`), so cite the church page and the
  issue date, not a tokenised download link.
- **Self-hosted PDFs:** Christ the Redeemer (`ctrmanville.com/assets/PDF/<yyyy>/<yyyy-mm-dd>.pdf`),
  Nativity, Monroe (Wix `_files/ugd/` hashes), St. John, Dunellen (Weebly), Our Lady of Lourdes,
  Milltown (`/olol/Bulletins/`), and bulletin pages at St. Anthony of Padua, St. John Paul II,
  Corpus Christi, St. Lawrence, St. Augustine, St. Joseph Washington, St. Mary of Czestochowa,
  St. Elizabeth Ann Seton and Ss. Peter and Paul (`/English/Bulletins.html`). Our Lady of Mercy,
  South Bound Brook keeps a `church-bulletin` page on Google Sites.
- **The probes' SPAM-SQUAT verdict needs a look:** stannparish.com (St. Ann, Raritan; eCatholic
  22511) and saintthomasob.com (St. Thomas, Old Bridge) both serve parish pages but were flagged.
  Read them before treating either as squatted.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- A site's bulletin page can link only HTML viewer pages wrapping the PDF (Immaculate Motherhood LLC sites: bulletin-view?f=<name>, PDF at /bulletins/file/<name>); fetch:check guesses the wrong edition and none of the pinned recipes read it. Look for the file path in the viewer page's HTML.
- A parish can publish its bulletin as an HTML page with no PDF (St. Stephen, South River); fetch:check reports 'No PDF links found'.
- John Patrick Publishing: the jppc.net/onlinebulletins/<id>template.pdf link returns HTML, so probe pdf can't read it. Use church-bulletin.org/?id=<id>, which redirects to the listing; record it as other with `page-pdfs https://church-bulletin.org/<id>` and fetch:check picks the newest issue. The listing posts the coming Sunday's issue about two days early, so fetch:check reports freshness 'future'.
- A parish's own site can host bulletin PDFs whose page 1 is an image (St. Mary of Czestochowa, Bound Brook): probe pdf --grep only reaches the ad pages. Render page 1 with pdftoppm -r 70 -jpeg and read it, and quote the page-5 publisher code line for recheck.
- Google Sites parish pages (OLM, South Bound Brook) embed the John Patrick template link, so check the page's links for jppc.net before looking for a Drive folder.
- Finder clergy lines can be wrong either way: Sayreville's Pekola matched the parish's own masthead, while St. Stanislaus's Murphy did not (Michalowski). Check the parish's masthead for each.
- eCatholic bulletins can be all-image PDFs (OLV Sayreville, St. Stanislaus); render page 1 to read the masthead, and quote a text page or the parish website for recheck.
- A parish may post the same bulletin on its eCatholic site and on church-bulletin.org (St. Stanislaus Kostka, Sayreville); compare page-1 renders before counting two publishers, and record only the parish-hosted copy.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches in the territory (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Maronite; Syro-Malabar) are excluded as `other-jurisdiction`, as in Allentown, Scranton, Syracuse and Rochester. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A pastor the parish finder lists for two parishes is a lead, not evidence of a shared pastor or a shared bulletin: whether rows share a bulletin is decided from the current bulletins. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A GCatholic church of a merged parish that neither the finder's worship-site list nor the parish's current bulletin names goes to `open/` unless a dated source says it closed; absence from the finder alone is not a closure. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A shrine or shrine chapel with public Mass but no parish of its own and no bulletin is excluded `no-bulletin`, as in Allentown (the Padre Pio Centre, Barto); one that publishes a bulletin or a schedule the pipeline can read gets a parish row. (accepted by survey-review, 003-survey-review, 2026-10-30)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-30: Survey (factory Run metuchen-map-1). Rosters: directory 91 (90 parishes),
  gcatholic 123 (107 Latin, 16 Eastern), worship-sites 25. 29 batches in `batches.json`, first
  `south-river`. No parish, church or exclusion records yet.
