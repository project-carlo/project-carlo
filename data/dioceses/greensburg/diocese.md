---
name: Roman Catholic Diocese of Greensburg
state: PA
website: https://dioceseofgreensburg.org
status: exploring
gcatholic: gree1
city_aliases:
  Marguerite: Greensburg
  South Greensburg: Greensburg
---

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.
Fill this in as you find them (see data/dioceses/README.md, "Sources").

- **Parish directory:** `rosters/directory.json`, scraped 2026-10-22 from
  https://www.dioceseofgreensburg.org/parishes/parish-directory/ (78 parishes; each
  `/parish/?LocationID=NNN` page is plain HTML after a 301) with coordinates from the parish
  map's WP Go Maps markers (`wp-json/wpgmza/v1/markers/`). 84 entries: three parishes have
  several worship sites, listed only in the Mass Times Search form (Church of the Resurrection,
  Clymer: five sites `060CS..060RS`; Our Lady of the Assumption, Coral/Lucernemines; St.
  Francis of Assisi, Masontown/Footedale). Each entry keeps pastor, clergy, weekend Mass line,
  website and the page's "Partner Parishes" field. Some pages are stale (Resurrection's base
  page shows a former pastor and "no Mass"; Apollo and East Vandergrift still name a pastor on
  leave since 2026-08).
- **GCatholic:** `rosters/gcatholic.json` (key `gree1`; `gree0` is Green Bay), 110 entries.
  24 are Byzantine Ruthenian or Ukrainian churches (ids 17xxx, 19565): `other-jurisdiction`.
  It also lists St. Walburga (39112), St. Vincent (40409, the archabbey/seminary) and a
  "Resurrection" at 596 Pineton Rd, Cameron's Bottom (24175) that no diocesan page has.
- **Clusters / families of parishes:** none. The diocese keeps every parish open (the
  bishop's 2024 pastoral letter asks for "parish partnerships"; a 2025 Catholic Accent article
  quotes his "vision of keeping all of our parishes open"). The directory's "Partner Parishes"
  field names 17 groups, mostly pairs, and many partners share one website
  (pbcatholic.org, youghcatholic.org, newkensingtoncatholic.org, stjohnstmary.org,
  partnerparishesmas.org...): shared-bulletin candidates, not decisions. Two shared websites go
  beyond the listed partners (youghcatholic.org also has St. Aloysius, Dunbar;
  newkensingtoncatholic.org also has Mount St. Peter). Several priests serve 3 to 8 parishes
  (Uniontown/Fayette 8, Connellsville/Mt. Pleasant 8, New Kensington/Apollo 6, Armstrong 5).
- **Mass times:** the directory's weekend line per parish; the Mass Times Search form lists
  the multi-site parishes' sites.
- **Closed parishes and where their records went:**
  https://www.dioceseofgreensburg.org/parishes/former-churches-directory/ lists 104 former
  churches, the latest closed in 2013. A former church is a lead for an `excluded/` record
  only when a roster still lists it.
- **Pastoral plan / closure announcements:** the 2023-2027 strategic plan has no merger or
  cluster list (it speaks of regionalizing outreach and records disagreement "about parish
  consolidation"). The 14 "Official" posts since 2023 only reassign clergy. The 12
  faith-formation regions are catechesis regions, not bulletin groups.

### Bulletin publishers here

Which publishers print this diocese's bulletins, how to read each, and which sites block the
sandbox and where their bulletins are instead. Agents researching parishes start here, so
keep it current rather than a log.

- **ParishesOnline is the main publisher here** (containers `14/xxxx`), even where a parish
  site self-hosts the PDFs (pbcatholic.org's uploads ran two weeks behind its container). The
  LPi geo-search (`.data.items[]`, `distance=6`) around a town lists every organization,
  including second organizations of partners that share one container: `probe po` each and
  compare containers. Partner pairs go both ways: St. Bruno and St. Paul share 14/1234; Our
  Lady of Grace and St. Benedict keep their own. Canva image-only issues carry text only on the
  LPi ad page, whose footer ("St. Paul and St. Bruno Parishes - South Greensburg, PA 14-1234")
  is a recheckable quote; render page 1 for the masthead.
- **Diocese-hosted WordPress parish sites** share one template, bulletin at
  `/bulletin/read-our-weekly-bulletins/`. Some answer 403 to `probe url`
  (blessedsacramentcathedral.org); headed `visit.py --bulletin` reads them.

- **A parish site can repost its container's PDF** (stjohnlatrobe.org's
  `14-1543-October-25-2026.pdf`, one child post per issue; Holy Family's Wix `_files/ugd/` copy):
  compare the file name and masthead with the container before calling it a separate bulletin.
  Empty LPi orgs left from old pairings (`st-john-the-evangelist-st-rose`) are not fold-ins.
- **GCatholic keeps minor basilicas off the diocese list** (St. Vincent is
  `gcatholic.org/churches/northamerica/0772`), so they have no gcatholic roster id; decode its
  Plus Code with `pdf_extract.dioceses.rosters.decode_plus_code`. Campus chapels with public
  Mass and no bulletin go in `excluded/` as `no-bulletin` (Saint Vincent College's Mary,
  Mother of Wisdom Chapel).
- **Sites that drop `probe url` and `recheck` connections** ("RemoteDisconnected":
  stvincentbasilica.org) may still answer plain curl; quote the bulletin instead.

- **Self-hosted pairs:** some partners have empty LPi orgs and self-host one shared bulletin
  (stmartinstjoseph.org: 403 to plain fetches, `dated-post https://www.stmartinstjoseph.org/bulletin/bulletins/`
  headed; saintcecilia.net: `page-pdfs`, file names carry the Wednesday upload date).
- **Geocoding:** Overpass resets connections from the sandbox; Nominatim reverse works but its
  house numbers are interpolated, not evidence. Send a generic User-Agent
  (`project-carlo-diocese-research`), never a personal email or name.

- **Filter `dated-post` on template sites with `filename=[0-9]*.pdf`**: unfiltered it can
  pick a sidebar PDF (`Calendar.pdf` at saint-edward.org) and still report "ok"; issue files
  here start with a date (`MMDD189.pdf`, `MMDDYY.pdf`, `MM-DD-YY-<n>OT.pdf`). The issue PDF is
  in each post's dFlip data with escaped slashes (`sed 's#\\/#/#g'`, grep `uploads/2026/`).
  Month-named issues (`October-25-2026.pdf`, mpcatholicchurches.org) need
  `filename=*-20??.pdf` instead. A doubled-letter text layer ("SSaattuurrddaayy") still
  passes `recheck` when quoted verbatim.
  stannerostraver.org's weekly `Bulletin-announcement-*.pdf` is the diocese's announcement
  packet, not a bulletin.
- **Pin a recipe on diocese-template sites.** Unpinned, `fetch:check` guesses
  `page-pdfs <home>/` and picks the diocese's footer privacy-policy PDF while reporting "ok":
  pin `dated-post <site>/bulletins/` and check `source_url`. These sites post one dFlip
  flipbook per issue whose PDF (`wp-content/uploads/<yyyy>/<mm>/*.pdf`) downloads plainly even
  where the page answers 403.
- **A ParishesOnline org page can render blank** while `probe po` still lists issues
  (st-james-church-15670, 2026-10-22), and the PO fetch then fails; re-check before blaming
  the row. LPi org coordinates can be ~15 km off: use the GCatholic Plus Code.
- **Partnerships change faster than the directory.** The "Official" appointment posts
  (plain HTML, e.g. https://www.dioceseofgreensburg.org/official-june-20-2026/) date splits
  the "Partner Parishes" field hasn't caught up with (St. Sylvester left St. Ambrose/St.
  Matthew in July 2026).

- **One issue in two LPi containers** (separate ad editions: 14/0550 and 14/1783 for
  Delmont/Export/Murrysville): compare rendered pages 1-2, record both containers on one row.
  The "Partner Parishes" field can under-report a group (Mother of Sorrows has none listed but
  shares that bulletin): check same-pastor parishes' mastheads too.
- **Empty LPi orgs for parishes that publish elsewhere** (st-barbara-church-15636; St. Barbara
  is on Discover Mass): the parish site's "Bulletin" menu link shows the real channel.
- `tools/fill_record.py` fills a just-created record from a small spec file.

- **Diocese-template sites (`*.wpengine`) that 403 `probe url`** often answer curl with a
  browser User-Agent (seasnh.org). Reposted container issues keep the container's file names
  (`14-1083.MM.DD.YYYY.pdf`, Squarespace `/s/20261025B.pdf`). The GCatholic Plus Code and the
  directory pin agree within ~20 m here; LPi org points don't. The directory/GCatholic address
  can be an old office (Sacred Heart, Jeannette: 504 Cowan Ave vs the masthead's 310 N 7th St).

- **Same-pastor parishes print each other's Mass boxes** (Perryopolis's Discover Mass issue
  carries Monessen's and Belle Vernon's) while each keeps its own live bulletin: separate rows.
  GCatholic can list a parish twice (old main church + current church, Epiphany 24169/24178).
  Discover Mass's current issue is `<a id='bulletin-current' href='…download.php?bulletin=…'>`:
  one page curl plus one download. Some template sites 403 even a browser User-Agent
  (saintflorian.org, sjbperry.org) but open headed.

- **eCatholic** (youghcatholic.org = 36088): 403 to `probe url` and curl, opens headed;
  `files.ecatholic.com/<id>/bulletins/<Saturday yyyymmdd>.pdf` downloads plainly, and the
  plain `ecatholic` fetch works headed. Diocesan-printed eCatholic issues (footer "View this
  bulletin online at www.DiscoverMass.com") also sit on Discover Mass under one church's slug:
  record both ids on the row. Their text layer alternates clean/letter-spaced week to week.
  Nominatim answers 429 after two quick requests.

- **Directory websites can all redirect to one unlisted shared site** (four Uniontown domains
  → faysouth.org, 14/1769 covering seven churches): `curl -L` with a browser User-Agent shows
  the target where `probe url` gets 403. GCatholic Plus Codes can be off the building (St.
  Joseph, Uniontown ~590 m): compare with the directory pin and OSM.

- **If `visit.py` hangs with no output**, `tools/headed_open.py` (a plain
  `launch_stealth_browser` script) opens the page in seconds. An old ParishesOnline org can
  list a stopped container (st-hubert-church-15474 → 14/1792, last issue 2023-10-22): check its
  latest issue before treating it as a channel; a dead predecessor's ids go on the row that
  took its churches.

- **Quick shared-bulletin test:** compare the `publicationWidget?id=` each parish site embeds
  (smmlb.org and newkensingtoncatholic.org both embed 001RP00000lUmSRYA0, container 14/2000).
  GCatholic's parish websites can be squatted (mountsaintpeter.org) or dead.

- **Discover Mass bulletin number** is in the cover image class
  (`bulletin-cover X-|2026-10-25|<ts>|3024`): two slugs with one number are one bulletin, and
  template-site file names often end in it (`10182026-3396.pdf`). `recheck` on a church page
  downloads ~12 issues and matches pypdf text, which is often letter-spaced: test quotes with
  `web.pdf_pages`/`quote_found` locally first. Former churches can keep occasional Mass as
  chapels (Guardian Angels, Nicholson Run): grep pastor's letters for "Chapel".
- **Discover Mass here:** many parishes have empty church pages ("Shucks! There are no
  bulletins available"), not channels. One issue can sit under both partners' slugs as
  byte-identical files (Apollo/East Vandergrift): compare MD5s, record both slugs on one row.
  evcatholic.org (Wix) challenges curl on its homepage, but `/bulletins` answers.

- **John Patrick Publishing is live here:** a "Current Bulletin" link to
  `jppc.net/onlinebulletins/<id>template.pdf` redirects to `church-bulletin.org/<parish-slug>`,
  which lists `/bulletin/<slug>/<yyyy-mm-dd>.pdf`; unpinned `page-pdfs` on it picks the newest.
  Recent issues may have no text layer (render page 1; quote an older issue). Discover Mass can
  run a week ahead of a parish's own repost: compare newest dates before choosing a provider.

- **Template-site post dates:** `wp-json/wp/v2/posts?per_page=3&_fields=date,slug` answers
  curl with a browser User-Agent and shows whether a site is behind its container or just
  posts on Saturday.

- **Occasional Masses at former churches** show only in intentions or the monthly calendar,
  not the Mass box: grep a year of issues (`probe pdf --pages 0 --grep <town>`) to find and
  date them (St. Patrick, Cameron's Bottom). The Former Churches Directory lists suppressed
  parish corporations whose buildings can still hold Mass. A ZIP+4 suffix equal to the
  "street number" (250 First St / 15731-0250) is an old mailing address, not the building.

Carried over from Altoona-Johnstown, Harrisburg, Scranton and Allentown (2026-10); correct it
as this diocese shows otherwise.

- **J.S. Paluch on Discover Mass.** Its `?s=` search is broken; grep the town in the
  sitemaps (`discovermass.com/wp-sitemap-posts-item-{1..11}.xml`), since slugs can be
  unguessable. Probe on the bare host (200 = exists, 404 = not). A joint bulletin may sit under
  only one of its churches' slugs, so read a neighbour's masthead before calling a parish
  `no_bulletin`; record every slug that carries the issue. "No bulletins available" pages are
  not live channels. Downloads are capped per IP per day (a 134-byte "Maximum number of files
  downloaded today" reply, `not_pdf` in `fetch:check`), and repeated page hits 503 then
  Wordfence-block even headed Chrome: read each page once. The text layer is often garbled
  (quotes keep the garble); cite the church page, not a tokenised download link.
- **LPi / ParishesOnline:** empty organizations are common and are not fold-ins. The search
  API (`https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=..&longitude=..&distance=3`)
  lists organizations near a point. Some containers are image-only: render pages with
  `pdftoppm` and read them (tesseract is not installed).
- **eCatholic** sites sit behind Cloudflare: `https://www.<domain>/bulletins` usually opens in
  headed Chrome (parish-site-access) when the homepage is challenged.
- **WebParish, Wix, Bon Venture** (`http://sponsors.bonventure.net/?page=<id>`, broken https
  chain), **John Patrick Publishing** (`church-bulletin.org/<id>`: any slug answers 200 with a
  generic page, and a listing with no PDFs is not live) and **FATA Online** all appeared next
  door. A Wix PDF name changes weekly: `page-pdfs` on the site reads it. A site with one child
  page per issue needs `dated-post <bulletin page>`.
- **Directory homepages and addresses go stale** (dead DNS, SSL failures; the address can be
  the rectory). Check a URL before storing it.
- **Web search in the sandbox:** `visit.py "https://duckduckgo.com/?q=..." --text`
  (parish-site-access) works; curl to DuckDuckGo or Bing returns nothing. A public Facebook
  post URL opens in headed Chrome without login (profile pages don't); cite it as a note.
- **Evidence for a `no_bulletin` church being open:** obituary snippets ("funeral Mass at
  <church>"), with the directory's Mass times. Flocknote pages are sign-up pages, not bulletins.
- **Sister parishes with one pastor** can each post their own bulletin with the same combined
  Mass rota: two rows while both channels are live.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.
