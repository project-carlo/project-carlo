---
name: Roman Catholic Diocese of Metuchen
state: NJ
website: https://diometuchen.org
status: promoted
gcatholic: metu0
city_aliases:
  Woodbridge Township: Woodbridge
  Old Bridge Township: Old Bridge
  Hillsborough Township: Hillsborough
  Piscataway Township: Piscataway
  Plainsboro Township: Plainsboro
  Oxford Township: Oxford
promoted: 2026-11-03
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
    David J. Pekola; one website, stpatrickrose.org), and names him for Our Lady of Victories,
    Sayreville too. The Belvidere/Oxford line is the stale one: Our Lady of Victories' 25 October
    2026 masthead names "Rev. David J. Pekola, Pastor", while the 1 November 2026 St. Patrick and
    St. Rose of Lima masthead (container 04/0870) names "Reverend Charles A. Sabella Pastor"
    (map batches `sayreville-parlin` and `belvidere-oxford-blairstown`).
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

From the survey's probes of the finder websites (2026-10-30) and the map batches since:

- **eCatholic** hosts most parish sites; they answer `probe url` directly. **A site id is the
  website's, not proof the bulletin is there:** a Bulletin page can embed an LPi id (St. Matthew,
  Edison), say only "Click Here" to a ParishesOnline org, or link only a John Patrick template;
  follow the link with `visit.py --links` and record the publisher it reaches. **`ecatholic:21916`
  is the diocese's own site:** don't record it. Read issues with `issues.py ecatholic` at
  `files.ecatholic.com/<id>/bulletins/<YYYYMMDD>.pdf`; it answers 403 for a site that doesn't name
  its files by the Sunday date, so read the real names with `visit.py --links`. A Bulletin page
  can be a frozen archive while the menu's "Bulletin" item points to the live publisher: check
  the newest file's date and don't record a stale id.
- **ParishesOnline / LPi:** containers can sit behind a `/wordpress/` redirect, and a parish
  WordPress can post LPi-named files (`20261011B-3.pdf`): look for its container. A container can
  carry the file the parish hosts on eCatholic (see *Rules settled*). To find a container, `probe
  po <name>-church-<zip>` (`st-catherine-of-siena-church-08867`); a merged parish's container can
  sit under its old member churches' slugs, so try each and record every org's ids on the one
  row. If slugs fail, search for the parish's LPi WeConnect site
  (`<name>-<aa>-<bbbb>.weconnectonline.com`): it embeds the LPi id, and `probe po <id>` gives the slug.
- **John Patrick Publishing** (church-bulletin.org): parish sites link
  `jppc.net/onlinebulletins/<id>template.pdf`, which returns HTML (`probe pdf` can't read it).
  Record provider `other` with `page-pdfs https://church-bulletin.org/<id>`; the listing posts the
  coming Sunday about two days early, so `fetch:check` reports freshness `future`. A parish site
  can keep a frozen "This Week" `bulletin.pdf` while John Patrick posts the current issue: check
  the newest date. It answers 406 to a bare "Mozilla/5.0" user agent.
- **Bonventure** (`sponsors.bonventure.net/?page=<n>`, http only; files at `pdfs/<n>/<date>.pdf`):
  parishes' eCatholic sites only link it. Record provider `other` with `page-pdfs
  http://sponsors.bonventure.net/?page=<n>`; it posts the coming Sunday early. Each account
  number is one parish, so different accounts are separate `publication_reviews`, decided from
  mastheads. Listing ids don't follow the ad-page G-codes and many are empty;
  `tools/bonventure_scan.sh` scans an id range for a town name (about 4 s per id). A parish can
  leave its listing unlinked or post its own issues (Weebly
  `/uploads/…/<YYYY-MM-DD>-<code>web.pdf`, or names that don't match the date, such as
  `BulletinOctober4.pdf` holding 25 October): search or scan for a listing before recording no
  PDF bulletin. Parish copies can skip weeks: date them from the PDF text, and pin `page-pdfs` to
  a newest-first list ("This Week" first); `fetch:check` then reports date `unknown`.
- **Discover Mass** (`discovermass:<slug>`) caps downloads per IP per day (a 134-byte "Maximum
  number of files downloaded today" reply, `not_pdf` in `fetch:check`), so cite the church page
  and the issue date, not a tokenised link. `fetch:check` reports date and freshness `unknown`:
  confirm currency from the date the church page lists. Its church page is also the `website`
  for a parish with no site (see *Rules settled*).
- **Self-hosted PDFs** (dated paths, Wix `_files/ugd/` hashes, Weebly, plain `/Bulletins.html`):
  `page-pdfs` on the Bulletin page works; check the newest entries are real PDFs (one list held
  `.crdownload` uploads). On Wix each date label follows its PDF link, so take the date from the
  PDF text; Wix answers 429 after a few rapid downloads. Google Sites can embed the John Patrick
  template, so check for `jppc.net` first. Squarespace posts `/s/<name>.pdf`: pin a filename glob
  on the issues' common prefix; a Bulletin page linking one PDF can stop updating, so if its
  date is stale record research with a revisit, not a recipe. A self-hosted archive can date a
  worship site gone from the Mass page: grep one issue per half-year for the church name.
- **Catholic Web Company** (footer `thecatholicwebcompany.com`): no `/bulletin` page; `page-pdfs`
  on the "Events & Bulletin" page `/event` picks the newest `/uploads/docs/bulletins/<YYYYMMDD>.pdf`.
- **OSV/Duda sites** (footer `editor.osvwebsites.com`) post
  `irp.cdn-website.com/<site>/files/uploaded/<MM.DD.YYYY><suffix>.pdf`; `page-pdfs` on `/bulletin`
  picks the newest.
- **GoDaddy site builder** (PDFs at `storage.googleapis.com/production-sitebuilder-v1-0-9/…/<hash>?fileName=<name>`):
  a `filename=` glob matches the hash, not `fileName`, and a name like `Nov 7.21.pdf` parses as
  the coming 7 November; record `fetch_gap` `filename-date-misread`, not a recipe.
- **Immaculate Motherhood LLC sites** link only HTML viewers (`bulletin-view?f=<name>`) around
  `/bulletins/file/<name>`; no recipe reads them. Confirm the bulletin from the viewer's HTML and
  record `unsupported-format` and `fetch_gap` kind `viewer-wrapped-pdf`.
- **Joomla file endpoints** (`/about-us/bulletin/<n>-<title>/file`) answer 403 to `probe get`; a
  `fetch()` in Chrome (`tools/browser_get.py`) returns the PDF. Record `fetch_gap`
  `joomla-file-endpoint`.
- **SermonCloud embeds** keep bulletins as `media.notes` S3 URLs in
  `api.sermoncloud.com/<account>/sermons` (find the call with `tools/net_log.py`). Record
  `fetch_gap` `sermoncloud-api-embed`.
- **HTML-only bulletins** ("No PDF links found"): record `unsupported-format` and `fetch_gap` kind
  `html-only-bulletin` when the page is kept current (St. Stephen, South River).
- **Image-only pages** (any publisher): `probe pdf --grep` reaches only text pages. Render page 1
  (`pdftoppm -r 70 -jpeg -f 1 -l 1`) for the masthead, take the Mass schedule from the parish
  site, and for recheck quote a text page (often the ad-page code line). A text layer can be
  garbage: Bon Venture's unmapped font still leaves the code line (`<code> (CK) · <parish> •
  <town>`) readable; a shifted encoding (`Parish` as `3DULVK`) leaves `fetch:check` date `unknown`.
- **Probe quirks:** `probe url` DEAD-DNS is unreliable here (it said so for live hosts); retry
  with `probe get` and the browser. Its SPAM-SQUAT verdict can come from one word (a "Casino
  Trip"): read the page first. `probe get --out` resolves a relative path from the worktree root,
  so give `scratch/<run>/<job>/…`. `tools/ddg.sh` gets DuckDuckGo's bot challenge; `visit.py
  'https://duckduckgo.com/?q=<words>&ia=web' --links` works.
- **Finder websites and details:** a dead finder domain can redirect to a new site (read its
  id) or be spam while the bulletin still prints it; find the live site by search and confirm it
  by the masthead's address and URL. A finder pin or GCatholic address can be the rectory: check
  the Contact page and masthead.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches in the territory (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Maronite; Syro-Malabar) are excluded as `other-jurisdiction`, as in Allentown, Scranton, Syracuse and Rochester. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A pastor the parish finder lists for two parishes is a lead, not evidence of a shared pastor or a shared bulletin: whether rows share a bulletin is decided from the current bulletins. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A GCatholic church of a merged parish that neither the finder's worship-site list nor the parish's current bulletin names goes to `open/` unless a dated source says it closed; absence from the finder alone is not a closure. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A shrine or shrine chapel with public Mass but no parish of its own and no bulletin is excluded `no-bulletin`, as in Allentown (the Padre Pio Centre, Barto); one that publishes a bulletin or a schedule the pipeline can read gets a parish row. (accepted by survey-review, 003-survey-review, 2026-10-30)
- One bulletin posted both on the parish's own site (eCatholic) and on a publisher's (church-bulletin.org, a ParishesOnline container, Discover Mass or Bon Venture) is one publication: record only the parish-hosted copy, after comparing page-1 renders or `pdftotext` output and the newest dates on both (the parish page can lag the publisher by a week or more), and list both ids (`discovermass:<slug>`, `url:http://sponsors.bonventure.net/?page=<n>`). A parish whose own site only links John Patrick is recorded on John Patrick. (map batches `sayreville-parlin` and `south-amboy-matawan`, 2026-10-30; ParishesOnline added by map batch `plainsboro-south-brunswick`, 2026-11-02; date check by map batch `woodbridge-iselin`, 2026-11-02; Discover Mass and Bon Venture added by map batch `warren-watchung-martinsville`, 2026-11-03) When the parish copy is still more than a week behind the publisher's at a later check, read the publisher instead and keep every id on the row: St. Andrew, Avenel moved to `parishes_online` when its eCatholic page still had 25 October while container 04/1116 had 1 and 8 November. (reconcile, 2026-11-03)
- A parish with no website of its own gets `no_bulletin` with its Discover Mass church page as `website`, since the record needs a URL. (map batch `monroe-jamesburg`, 2026-11-02)
- A Latin church sold to an Eastern Catholic community that now holds Mass there is excluded `other-jurisdiction`, not closed; the merged parish's own history page can date the sale. (map batch `carteret-port-reading`, 2026-11-03)
- A monastery chapel with public daily Mass but no bulletin is excluded `no-bulletin` under the shrine rule above, even when it is in no roster. (map batch `flemington-readington`, 2026-11-03)
- Parishes staffed by one religious community can each print the same combined Mass schedule for all the community's churches: decide rows from mastheads and Bon Venture account codes, and give each church to the row whose masthead it is (the Raritan Oratory, whose raritanoratory.org links each parish's current site). (map batch `raritan-oratory`, 2026-11-03)
- Date evidence `seen`/`checked` by US Eastern time (`TZ=America/New_York date`), not the shell's UTC date: in the evening UTC is a day ahead and `validate` rejects the date as in the future. (map batch `south-plainfield-piscataway`, 2026-11-03)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-03: Reconcile (factory Run metuchen-map-1), after 29 map batches of usually 6 to 8
  roster entries (5 to 16). Coverage: directory 91/91 accounted for (87 modelled; 4 off the site
  as `no_bulletin`), gcatholic 123/123 (96/100 modelled, 23 excluded), worship-sites 25/25
  (23/23). Records: 88 parishes, 103 churches, 24 excluded, 0 open. No merges. St. Andrew,
  Avenel moved from its lagging eCatholic copy to ParishesOnline; the former Corpus Christi
  convent room (Latin Masses) became a church of Corpus Christi; Corpus Christi and St. Stephen,
  South River got `fetch_gap`s. Wrote `separate` reviews for the 56 Bon Venture-host pairs from
  recorded mastheads; audit: 85 candidate pairs, all separate. fetch:check: 82 of 84 rows fetched,
  2 known gaps (Joomla, SermonCloud).

- 2026-10-30: Survey (factory Run metuchen-map-1). Rosters: directory 91 (90 parishes),
  gcatholic 123 (107 Latin, 16 Eastern), worship-sites 25. 29 batches in `batches.json`, first
  `south-river`. No parish, church or exclusion records yet.
