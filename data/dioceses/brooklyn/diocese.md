---
name: Roman Catholic Diocese of Brooklyn
state: NY
website: https://dioceseofbrooklyn.org
status: exploring
gcatholic: broo0
---

The Diocese of Brooklyn is the boroughs of Brooklyn (Kings County) and Queens (Queens County),
all of it New York City: about 4.8 million people, "172 parishes and 211 churches" by the
diocese's own count (parish directory, read 2026-11-05). Postal cities are Brooklyn for the
whole of Kings County, and the Queens neighbourhood names (Jamaica, Flushing, Astoria, Long
Island City, Ridgewood, the Rockaways, ...) for Queens. Its neighbours are the Archdiocese of
New York (Manhattan, the Bronx and Staten Island, across the East River and the Narrows) and
the Diocese of Rockville Centre (Nassau County, east of Queens). There are no families or
clusters of parishes. Since 2023 the diocese is divided into four regions (Brooklyn West and
East, Queens West and East) and 22 deaneries (B1-B11, Q1-Q11); a deanery is a consultation
group, not a pastorate, though the bishop's 2024 reconfiguration letter has deaneries
coordinating Mass schedules. What decides shared bulletins here is (1) canonical mergers,
which the diocese names by joining the old names ("Holy Family - St. Laurence"), often
keeping two churches, and sometimes still listing the old parishes apart for a while after
the decree; and (2) priests who are pastor or administrator of two or three parishes (13 such
assignments in the priests' directory, 2026-11-05). Every batch's `why` names the ones that
touch it.

## Sources

- **Parish directory:** https://dioceseofbrooklyn.org/directories/parishes/ (page modified
  2026-05-06, read 2026-11-05). One block per parish: linked name (the homepage), office
  street address, phone. 172 entries, matching the page's own "172 parishes". Imported as
  roster `directory` by `scratch/brooklyn-map-1/tools/directory.py`. No coordinates. Good
  for the canonical list and homepages; merged parishes appear once under the joined name
  with the office address, so their other churches aren't listed. It lags on mergers:
  Resurrection-Ascension and Our Lady of the Angelus (merged 2023), Christ the King and
  St. Mary Magdalene (merged 2024), and Good Shepherd-Resurrection and Resurrection are still
  separate entries. Three parishes have no website link (Most Precious Blood-Ss. Simon and
  Jude, Our Lady Queen of Martyrs, Ss. Peter and Paul-Epiphany).
- **Deanery directory:** https://dioceseofbrooklyn.org/directories/deaneries/ (modified
  2026-06-06, read 2026-11-05). Parishes by deanery with addresses. Imported as roster
  `deaneries` (`group` = deanery and region) by `tools/deaneries.py`; 175 entries. Has
  errors: B8's list gives St. Michael-St. Malachy (East New York) and Our Lady of Perpetual
  Help (South Ozone Park), where St. Michael and the Basilica of OLPH (Sunset Park) belong;
  Q1 gives Immaculate Conception, Jamaica (also in Q7) where Astoria's would be; Q10 ends with
  the diocesan offices and the Immaculate Conception Center (Douglaston). It still lists
  Mary Queen of Heaven, Our Lady of Refuge and Corpus Christi alone beside their merged
  parishes.
- **Mass finder:** https://mass.dioceseofbrooklyn.org/all (read 2026-11-05), a page per place
  at `/places/<id>` with address, Mass and confession times. 173 places, nearly one per
  parish; a merged parish's place is named "Parish (main church)". Imported as roster
  `massfinder` by `tools/massfinder-fetch.sh` + `tools/massfinder.py` (coordinates from the
  list, address from each page). Some times look like placeholder data: St. Rose of Lima,
  Brooklyn shows a 2:00pm Filipino Mass and "Followed by potluck brunch". Don't take a
  schedule from it without the parish's own; use it for coordinates and extra places
  (it lists Holy Innocents, St. Gertrude, Our Lady of Lourdes chapel, St. Teresa). A few
  addresses are wrong (St. Martin de Porres: "2 Floral Parkway, Floral Park").
- **GCatholic:** key `broo0`, https://gcatholic.org/churches/local/broo0, roster `gcatholic`
  (218 entries, fetched 2026-11-05). Lists old churches of merged parishes individually
  (Holy Rosary, St. Peter Claver, St. Cecilia, St. John Cantius, Epiphany, ...), which
  makes it the best list of buildings to check for closures, and ten Eastern Catholic or
  Coptic churches (Ukrainian, Melkite, Syro-Malankara, Armenian, Romanian, Coptic), all in
  batch `eastern-catholic`. Some of its entries share an address with a Latin church
  (St. Ann, Flushing; St. Basil at the Immaculate Conception Center).
- **Families / clusters:** none exist. Use the merger decrees and the priests' directory.
- **Priests' directory (shared pastors):** https://dioceseofbrooklyn.org/priests/ (read
  2026-11-05). Each priest's "Current Assignment". The page shows nine and loads the rest by
  POST (`admin-ajax.php`, action `loadmore`); `tools/priests.py` reads all 343. Explicit
  multi-parish pastors: OL Angels + St. Andrew the Apostle + St. Anselm (Bay Ridge); OLPH +
  St. Teresa of Avila-St. Anthony of Padua (South Ozone Park); St. Bernadette + St. Frances
  Cabrini; St. Rita + St. Patrick (Long Island City); St. Mary Star of the Sea and St. Gertrude
  (Far Rockaway, one parish); Sacred Hearts & St. Stephen + St. Mary Star of the Sea (Carroll
  Gardens); St. Edmund + St. Brendan; St. Raphael + St. Teresa (Woodside); St. Clare + St. Pius
  X (Rosedale); St. Thomas Aquinas + OL Help of Christians; St. Michael + St. Agatha (Sunset
  Park); St. Charles Borromeo + Cathedral Basilica of St. James; American Martyrs + Holy
  Family (Fresh Meadows). A shared pastor is a lead for one bulletin, not proof.
- **Merger decrees:** posts on dioceseofbrooklyn.org (WordPress search "merger decree"):
  St. Augustine-St. Francis Xavier and Christ the King-St. Mary Magdalene (posted 2024-09-24,
  effective 2024-07-01), Incarnation-St. Gerard Majella (posted 2024-12-23),
  Resurrection Ascension-Our Lady of the Angelus (posted 2025-09-10, effective 2023-01-01).
  Each says "The Parish shall have two churches for worship". The decrees page
  (https://dioceseofbrooklyn.org/decrees/) renders no list without JavaScript; older mergers
  aren't posted.
- **Closed parishes and where their records went:** Archives "List of Parishes",
  https://dioceseofbrooklyn.org/offices/diocesan-archives/parishes/ (read 2026-11-05). Every
  parish ever, Brooklyn then Queens, with founding year, mergers ("Merged with St. Martin of
  Tours, 2007"), closures and where the records are. Good for dating a merger; says nothing
  about whether a building still has Mass. Also two PDFs, "Chronological List of Brooklyn /
  Queens Parishes and Schools" (2019), linked from it.
- **Pastoral plan:** Bishop Brennan's letter "Reconfiguring for the Future to Address Resource
  Challenges" (dated 2024-06-07): a three-stage reconfiguration of "collaborating, partnering,
  or merging", deanery-level Mass-schedule changes from fall 2024. A plan; check bulletins
  for what happened.

### Bulletin publishers here

- **Tilma parish sites are common.** 47 of the directory's 169 homepages are
  `<name>-brooklyn.org` / `-queens.org` and load from Tilma; Tilma also runs custom domains
  (e.g. `bsjh.org`). `probe url` reports them `ok` with no platform and no publisher. The
  bulletins page (`/bulletins`) is server-rendered and lists cards "Bulletin for Sunday,
  <date>" newest first, each linking a PDF at
  `files.tilmaplatform.com/system/resources/<token>/<file>.pdf` (custom domains serve
  `<site>/system/resources/<token>/` instead). Record `other` with a `page-pdfs
  https://<site>/bulletins` recipe, `fetch:check` it, and confirm the pick is this week's
  issue. A card for the coming week can be posted before its file (it links
  `/bulletins/null`), so fetch picks the previous issue: record a research recheck after the
  weekend, not a gap. Newer Tilma "webstudio" sites (`api.tilmaplatform.com`, `/cgi/asset/`
  paths) render `/bulletins` in JavaScript, so `probe get` shows no cards: the homepage HTML
  embeds `latestBulletinData` with the Bulletins collection's `totalCount`, and `visit.py`
  shows the cards (or "NOTHING TO SHOW"). Tilma is only the host; check who prints the PDF:
  - `/bulletins` can redirect to `parishesonline.com/organization/<slug>` (`probe get`
    shows it as `final_url`; `probe url` lists no bulletin links): `probe po` that slug, and
    the row is `parishes_online`;
  - files named `YYYYMMDDB.pdf` (LPi's naming) are a reposted LPi issue: `probe po
    <name>-church-<zip>` finds the live container and the row is `parishes_online`, not a
    Tilma recipe;
  - an ad-page footer "THE CHURCH BULLETIN INC., 200 DALE ST." with a `#NNN` number is The
    Church Bulletin Inc. (West Babylon), which has no online container: keep `other`
    page-pdfs with no publication id. Its page 1 is often an image; `render.py` it for the
    masthead and Mass times.
- **LPi / ParishesOnline.** Some parishes embed it; many self-hosted, Tilma, WordPress,
  Squarespace or GoDaddy PDFs are LPi issues in disguise. Grep the last page for the footer
  `<Parish> | 03-NNNN` (or `<Parish>, <Town>, NY 04-NNNN`): the prefix is the container
  group, so `03-NNNN` is po-container 03/NNNN and `04-NNNN` is 04/NNNN; read it from the
  footer, don't assume 03. File names say the same: `03-NNNN.MMDD.pdf`, and Squarespace's
  `/s/03-0NNNNMMDDYY.pdf` pads the number to 5 digits (`03-04068` is 03/4068). `probe po`
  on the org gives a `parishes_online` row with real publication ids. A repost can have
  every page an image and the footer pages cut (GoDaddy `img1.wsimg.com/blobby/go/...`), so
  no number shows: try `probe po <name>-church-<zip>`, then the bare `<name>-church` slug
  (some orgs have no zip suffix). Try that before the browser for a site that answers 403
  too. LPi front pages are often images: `render.py` pages 1-2 for masthead and Mass
  times. ParishesOnline also holds empty orgs (no issues) for parishes that self-publish,
  slugs like `<name>-11385` / `<name>-church-11385`: an org with no issues is not a
  publication id and doesn't make the parish a `parishes_online` row.
- **eCatholic sites** answer 403 to `probe url`; `visit.py` gives the `ecatholic:<id>`, and
  `issues.py ecatholic` reads the issues from `files.ecatholic.com` without a browser. A
  merged parish can post one bulletin on each former parish's eCatholic site: compare
  page-1 mastheads, keep one row and record both ecatholic ids as its publication ids.
- **John Patrick Publishing** sites link `jppc.net/onlinebulletins/<id>template.pdf`:
  record `other` with `page-pdfs https://church-bulletin.org/<id>` (`fetch:check` resolves
  it). Its issues can be all images: `render.py` them.
- **WordPress.** With no bulletin menu, list the PDF uploads newest first with `probe get
  '<site>/wp-json/wp/v2/media?mime_type=application/pdf&per_page=50'` to find and date the
  last bulletin posted.
  - Flipbook plugins hide the PDF from the HTML. dFlip (`flipbook-dflip-lite`): grep the
    page for `"source":` in `window.option_df_*` for the file URLs. 3D FlipBook (`div
    class="_3d-flip-book" data-id=N`): no URL in the HTML. For both, a pinned `page-pdfs
    <bulletin page>` recipe resolves the current upload in `fetch:check`, even for one fixed,
    weekly-overwritten PDF the unpinned resolver misses ("No bulletin page link found").
  - Multisite (uploads under `/wp-content/uploads/sites/<n>/`) drops `probe url`, `probe
    pdf` and `render.py` connections (UNREACHABLE, RemoteDisconnected) but loads in
    `visit.py` and fetch. The bulletin page is `/important-information/bulletin/`, newest
    first. Download with `tools/fetch-pdf.py` (run without `python -I`, which hides
    `pdf_extract`) and give `render.py` the local file. `visit.py` can call such a site
    SPAM-SQUAT when betting spam is injected into a working parish homepage: if the address,
    bulletin page and weekly PDFs are the parish's own, keep it as the website and note the
    compromise.
- **Joomla DOCman lists** (`/news/bulletin/<n>-<title>/file`, class
  `docman_track_download`) answer 403 to probes and fetch. The link's `title` attribute
  gives the file name (often the LPi `03-NNNN.MMDD.pdf` form above);
  `tools/browser-pdf.py` downloads the file through the browser.
- **Self-hosted bulletin pages.** `fetch:check` gives a page that keeps one stale file
  `ok` with freshness `unknown`, not `stale`: check the issue date yourself before pinning.
  - Files named `MMDDYY.pdf` (no year) in a non-chronological archive table fool the
    unpinned resolver into a past year's file; pin the homepage's "This Week's Bulletin"
    link with a digit filter (`page-pdfs <home> filename=[0-9][0-9][0-9][0-9][0-9][0-9].pdf`).
  - One fixed file behind a redirect (`/bulletin` -> `/files/bulletin.pdf`) fails
    `fetch:check` when the redirect URL is the website; set website to the homepage and
    `fetch:check` resolves to recipe `redirected-pdf <site>/bulletin` (freshness still
    `unknown`).
- **Google Drive.** A `drive/folders/<id>` page serves only its first 50 files in name
  order, so `drive-folder` can pick a years-old issue. List the whole folder with
  `drive.google.com/embeddedfolderview?id=<id>#list` to see whether it is kept current
  before pinning it. Google Sites pages can embed each issue as a Drive file preview (iframe
  `data-src` `drive.google.com/file/d/<id>/preview`) with no folder or PDF link: fetch can't
  resolve that, so the row is unsupported with `fetch_gap` kind `drive-preview-embed`; read
  the issue through `drive.google.com/uc?id=<id>&export=download`.
- **JavaScript-only sites** (Next.js `/_next/static` chunks, Vite `/assets/index-*.js`) whose
  bulletin menu has no links in the HTML: grep the JS bundle for `drive.google.com`,
  `docs.google.com/spreadsheets` or `supabase.co` to find where the issues live. When the
  link exists only in JS, the row is unsupported with a `fetch_gap`.
- **Other blocked or odd sites:** some parish sites answer 403 to `probe url` (try `probe
  po` as above, then parish-site-access `visit.py`), and some redirect off-site; read the
  target first.
- **Finding a current site.** When the directory's homepage is dead or parked, the parish's
  Discover Mass page (`discovermass.com/church/<name>-<town>-ny/`) names its current website
  even when it lists no bulletins.
- The neighbouring Archdiocese of New York has only one mapped parish (a self-hosted
  bulletin page) and no publisher notes yet; Rockville Centre isn't mapped.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- A Tilma /bulletins page whose newest card is months old still passes fetch:check ('first-listed', freshness unknown, not stale): read the newest card's date, and if no issue has been posted for months record the row no_bulletin with bulletin_status not-found and a research recheck, keeping the page-pdfs recipe in the research next_action.
- Some Tilma parish themes list /bulletins as '<Month DD, YYYY> / Download Bulletin' cards (not 'Bulletin for Sunday, <date>'), with PDFs at <site>/system/resources/<token>/: grep the page text for the dates, not the 'Bulletin for' wording.
- A Tilma /bulletins page that is months stale can still sit beside a live LPi container: run probe po <name>-church-<zip> before recording no_bulletin (sfdsparish.org's last card 23 Aug 2026; container 03/4055 current).
- A Joomla DOCman bulletin list (403 to probes and fetch) whose files are the parish's own Word PDFs with no LPi footer and no ParishesOnline org with issues is unsupported with fetch_gap kind joomla-docman-file-403; read the issues with tools/browser-pdf.py.
- Some self-made bulletins posted on Tilma have a text layer in a shifted font encoding ('3KRQH' for 'Phone', digits dropped), so probe pdf greps miss Mass times and fetch:check reports issue-date conflicts: render.py page 1 for the masthead and take per-church Mass assignments from the site's /mass-times page.
- John Patrick Publishing's church-bulletin.org/<id> page (redirects to a slug page) links each issue as church-bulletin.org/bulletin/<slug>/YYYY-MM-DD.pdf, while the jppc.net <id>template.pdf link answers HTML to probe pdf: read issues from the slug URLs, and record url:<slug page> as the publication id.
- Wix bulletin pages can show the issue only as a slideshow of hash-named static.wixstatic.com JPEGs with empty alt text (no PDF, no date): page-pdfs and page-images both fail, so the row is unsupported with fetch_gap kind wix-image-slideshow. Read the slides at static.wixstatic.com/media/<id>~mv2.jpg, and use tools/frames-requests.py to list them.
- Parishes that share a pastor can each print both churches' Mass schedules on page 1 of separate bulletins: compare mastheads, intentions and collections before merging, and record a separate review.
- Diocesan WordPress-multisite parish sites post each issue as <mon><d>_<yyyy>_<parish>_compressed.pdf: some are LPi reposts (probe po <name>-church-<zip> finds the live container), others self-made with no cover page and no LPi footer (record other with page-pdfs on /important-information/bulletin/ or /weekly-bulletin/).
- Tilma sites that repost an LPi issue under a date name (110826.pdf) instead of LPi's YYYYMMDDB.pdf can still keep LPi's naming on some older cards: check a few cards' file names, or run probe po <name>-church-<zip>, before recording a Tilma page-pdfs row.
- An LPi repost on a diocesan WordPress-multisite site whose ParishesOnline org slug can't be found by probe po (name-church-zip variants all empty) can be recorded other with page-pdfs on the site's bulletin page and po-container:<a/b> as its publication id, with a research item to find the org later.
- A parish whose weekly bulletin is a Constant Contact email newsletter (Tilma webstudio homepage 'Bulletins & News' card linking conta.cc/<id> -> myemail.constantcontact.com/<title>.html?soid=...) has no PDF: record unsupported with fetch_gap kind constant-contact-html-newsletter; its old Tilma /bulletins archive may still list years-old PDFs that page-pdfs would wrongly pick.
- Tilma sites can repost a John Patrick Publishing issue as '<id>-<Parish> MM-DD-YYYY.pdf' (page-8 footer '<id> <Parish>, Brooklyn, NY (B)' and 'John Patrick Publishing Company'), with no jppc.net link: record other with page-pdfs https://church-bulletin.org/<id>, which posts each issue days before the Tilma page does.
- A Tilma webstudio /bulletins page whose Bulletins collection is empty (totalCount 0) can still show cards from an embedded ParishesOnline widget (publicationWidget?type=bulletin&id=<lpi id>): tools/frames-requests.py lists the iframe, and probe po <lpi id> gives the parishes_online row.
- Diocesan WordPress-multisite sites can repost an LPi issue with its ad pages cut (no 04-NNNN footer left, only '©LPi' on the cover art); the ParishesOnline org may have no zip suffix (st-saviour-church), so try probe po <name>-church as well as <name>-church-<zip>.
- A ParishesOnline org slug can be a shortened parish name (Holy Name of Jesus is holy-name-church-11215): when <full-name>-church-<zip> is empty, try dropping the 'of <...>' part; WordPress reposts named '<...>-Account-03-NNNN.pdf' give the container number directly.

## Rules settled for this diocese

Proposals are in `scratch/brooklyn-map-1/survey.json` for survey-review.

- A merger decree that keeps 'two churches for worship' is a lead, not a row decision: a merged parish's churches are one parish row only when the current bulletin covers both, and a pre-merger parish the directory still lists separately is reconciled to the merged row (roster link) rather than given its own row unless it still publishes its own bulletin. (accepted by survey-review, 002-survey-review, 2026-11-06)
- The Mass finder (mass.dioceseofbrooklyn.org) is not evidence for a Mass schedule or for a church having Mass; use it for coordinates and as a lead for places. Schedules come from the parish's bulletin or site. (accepted by survey-review, 002-survey-review, 2026-11-06)
- Eastern Catholic and Coptic churches GCatholic lists in Brooklyn and Queens are excluded as other-jurisdiction (their eparchies), each with a source naming the eparchy; they are not mapped under Brooklyn. (accepted by survey-review, 002-survey-review, 2026-11-06)
- The JFK airport chapel (Our Lady of the Skies) and similar chaplaincy chapels count as worship sites if they have public Mass; with no bulletin they go to excluded/ as no-bulletin, not closed. (accepted by survey-review, 002-survey-review, 2026-11-06)
- Cemetery chapels are treated the same way: one with public Mass listed on its Catholic Cemeteries page (`ccbklyn.org/our-cemeteries/<name>/`) and no bulletin is excluded as no-bulletin. GCatholic lists only St. John's, but the Holy Cross and Mount St. Mary pages may list Masses too. (map batch `q6-middle-village`, 2026-11-06)
- The diocesan archives' List of Parishes, which also lists chapels and apostolates with "Closed YYYY" notes, is a source for a chapel's listed status and contacts, not evidence that it has Mass. (map batch `q6-rego-park-elmhurst`, 2026-11-06)

## Log

- 2026-11-05: Survey. Rosters: directory 172, deaneries 175, massfinder 173, gcatholic 218
  (738 entries). Plan: 53 batches in `batches.json` (52 of 2-4 directory parishes, one
  eastern-catholic), first `q11-ridgewood`; one deanery entry excluded (the diocesan
  offices). No records written; coverage not run.
