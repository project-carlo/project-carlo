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

- **Tilma parish sites** (`<name>-brooklyn.org` / `-queens.org`, and custom domains) are
  common; `probe url` reports them `ok` with no platform. `/bulletins` lists cards newest
  first (grep for the dates), each linking a PDF under `.../system/resources/<token>/`.
  Record `other` with `page-pdfs https://<site>/bulletins`, `fetch:check` it, and read the
  newest card's date yourself: a page months stale still passes (freshness `unknown`). The
  token base64-decodes to the upload date (`2026/10/02/...`): a parish posting in batches
  every 2-10 weeks looks stale between them, so recheck after its usual gap. If it has
  stopped, `probe po` first (LPi bullet); with no container, record `no_bulletin`, status
  `not-found`, a research recheck, and keep the recipe in its next_action. A card for the
  coming week can precede its file (`/bulletins/null`): recheck after the weekend. An issue
  with no name masthead (page 1 only intentions, readings, a schedule): identify it by its
  host site and a schedule matching the site's Mass Times page, and say so in the record.
  Webstudio sites (`api.tilmaplatform.com`) render it in JS: the homepage's
  `latestBulletinData` has `totalCount`; `visit.py` shows the cards. Tilma is only the host;
  check who prints the PDF:
  - `/bulletins` redirecting to `parishesonline.com/organization/<slug>` (`final_url` in
    `probe get`), or a webstudio page with `totalCount` 0 embedding
    `publicationWidget?type=bulletin&id=<lpi id>` (`tools/frames-requests.py`): `probe po`
    the slug or id; the row is `parishes_online`.
  - LPi reposts: `YYYYMMDDB.pdf`, or date names (`110826.pdf`) with LPi's naming on older
    cards, so check several: `probe po` finds the container; row `parishes_online`.
  - John Patrick reposts `<id>-<Parish> MM-DD-YYYY.pdf` (last-page footer `<id> <Parish>,
    Brooklyn, NY`, "John Patrick Publishing Company"): use the JPP recipe below.
  - **The Church Bulletin Inc.** (footer "THE CHURCH BULLETIN INC., 200 DALE ST." with
    `#NNN`), here or on any host: no online container, so `other` page-pdfs with no
    publication id. The `#NNN` is per parish: different numbers and mastheads support a
    `separate` review.
  - Self-made PDFs with a shifted-font text layer ('3KRQH' for 'Phone') defeat greps and
    `fetch:check`'s dates: `render.py` page 1, take Masses from `/mass-times`.
  - A webstudio card linking `conta.cc/<id>` is a Constant Contact newsletter, no PDF:
    unsupported, `fetch_gap` kind `constant-contact-html-newsletter`. The old `/bulletins`
    archive may still list years-old PDFs page-pdfs would pick.
- **LPi / ParishesOnline.** Many self-hosted, Tilma, WordPress, Squarespace or GoDaddy PDFs
  are LPi issues in disguise. Grep the last page for `<Parish> | 03-NNNN` (or `<Parish>,
  <Town>, NY 04-NNNN`): the prefix is the container group, so read it. File names say the
  same: `03-NNNN.MMDD.pdf`, `<...>-Account-03-NNNN.pdf`, Squarespace's
  `/s/03-0NNNNMMDDYY.pdf` (5-digit pad: `03-04068` is 03/4068). Reposts can lose the number
  (ad pages cut, pages as images, only "©LPi" on the cover). Org slugs vary: try
  `<name>-church-<zip>`, `<name>-roman-catholic-church-<zip>`, `<name>-church`, the name
  without "of <...>" (`holy-name-church-11215`), and the directory's full name slugged as-is
  with no zip (`shrine-church-of-our-lady-of-solace`). Do this before the browser for a 403
  site, and before calling a stale eCatholic, Tilma or self-hosted archive a stop: a
  container can start beside it. Container number known but no org: `other` page-pdfs with
  `po-container:<a/b>` as publication id and a research item. Front pages are often images
  (`render.py` pages 1-2). An org with no issues is not a publication id.
- **eCatholic sites** answer 403 to `probe url`; `visit.py` gives the `ecatholic:<id>`, and
  `issues.py ecatholic` reads `files.ecatholic.com` without a browser. Archive links carry
  `?t=<ms epoch>` upload stamps: decode them to tell a batch uploader from a stop. A merged
  parish can post one bulletin on each former parish's site: compare mastheads, keep one row
  with both ids.
- **John Patrick Publishing**: `church-bulletin.org/<id>` redirects to a slug page listing
  `church-bulletin.org/bulletin/<slug>/YYYY-MM-DD.pdf` in date order, about a week before
  parish sites repost them; the sites' `jppc.net/onlinebulletins/<id>template.pdf` answers
  HTML to `probe pdf`. Record `other` with `page-pdfs https://church-bulletin.org/<id>` and
  publication `url:<slug page>`; the PDFs are often images (`render.py`). A slug page
  listing no PDFs (a merged parish's old job) is dormant, not a publication id.
- **WordPress.** With no bulletin menu, list PDF uploads newest first with `probe get
  '<site>/wp-json/wp/v2/media?mime_type=application/pdf&per_page=50'`.
  - Flipbooks hide the PDF. dFlip: grep `"source":` in `window.option_df_*`. 3D FlipBook
    (`_3d-flip-book`): no URL in the HTML. A pinned `page-pdfs <bulletin page>` resolves
    both, even one weekly-overwritten PDF the unpinned resolver misses.
  - Diocesan multisite (`/wp-content/uploads/sites/<n>/`): issues at
    `/important-information/bulletin/`, `/bulletin/` or `/weekly-bulletin/`, named
    `<mon><d>_<yyyy>_<parish>_compressed.pdf`: LPi reposts, Church Bulletin Inc. or
    self-made, all `other` page-pdfs on that page unless LPi; fetch dates them from the file
    name. A form PDF can list above the issues: pin `filename=*compressed*.pdf`. Probes drop
    the connection; `visit.py` and fetch work, and `tools/fetch-pdf.py` (not `python -I`)
    downloads the file to `render.py`. `visit.py` may call one SPAM-SQUAT for injected
    betting spam: if address, bulletin page and PDFs are the parish's own, keep it and note
    it.
- **Joomla DOCman lists** (`docman_track_download`) answer 403 to probes and fetch;
  `tools/browser-pdf.py` downloads the file the link's `title` names. Non-LPi files are
  `fetch_gap` kind `joomla-docman-file-403`.
- **Wix**: a slideshow of `static.wixstatic.com/media/<id>~mv2.jpg` slides (no PDF, no date;
  `tools/frames-requests.py` lists them) is `fetch_gap` kind `wix-image-slideshow`. A blog
  of issues (`/post/<slug>` with a 'Download PDF' widget) gets its URL only from a
  click-time API: `fetch_gap` kind `wix-blog-file-download`; `tools/click-requests.py` gives
  the `ugd/<id>.pdf`, readable at `<site>/_files/ugd/<id>.pdf`.
- **Self-hosted pages.** `fetch:check` calls one stale file `ok`, freshness `unknown`: check
  the date. `MMDDYY.pdf` names in an unordered archive fool the resolver: pin the homepage
  link with `filename=[0-9][0-9][0-9][0-9][0-9][0-9].pdf`. A fixed file behind a redirect
  (`/bulletin` -> `/files/bulletin.pdf`): set the website to the homepage (`fetch:check`
  resolves `redirected-pdf`). Framesets (`<frame src=links.htm>`) hide the link: pin
  `page-pdfs <site>/<menu frame>.htm`. A page on `http://www.` linking `https://`
  bare-domain PDFs with a mismatched certificate can't be fetched (no http fallback):
  `fetch_gap` kind `https-pdf-link-cert-mismatch`, recipe in the research next_action.
- **Google Drive.** `drive/folders/<id>` serves its first 50 files in name order, so
  `drive-folder` can pick a years-old issue: list it all with
  `drive.google.com/embeddedfolderview?id=<id>#list` before pinning. Google Sites linking
  each issue as `drive.google.com/file/d/<id>/view` work as `other` `page-pdfs
  <site>/bulletins` (read the date yourself); `/preview` embeds are unsupported, `fetch_gap`
  kind `drive-preview-embed`, readable via `uc?id=<id>&export=download`.
- **JavaScript-only sites** (`/_next/static`, `/assets/index-*.js`): grep the bundle for
  `drive.google.com`, `docs.google.com` or `supabase.co`; a JS-only link is a `fetch_gap`.
- **Shared pastors.** Parishes sharing a pastor can each print both churches' Mass times, an
  'In partnership with <other>' line and both rectories on page 1 of separate bulletins:
  compare schedules, intentions and collections, not the masthead, before merging, and
  record the review.
- **Finding a current site.** When the directory's homepage is dead or parked, Discover Mass
  (`discovermass.com/church/<name>-<town>-ny/`) names the current website. For 403s or
  off-site redirects try `probe po`, then `visit.py`; read the target.
- **The Tablet** (thetablet.org) asks for a login after a few paragraphs; its API
  (`wp-json/wp/v2/posts?search=<words>&_fields=link,date,title`) lists dated articles on
  closures and sales, and `probe get` on an article returns the opening paragraphs to quote.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Proposals are in `scratch/brooklyn-map-1/survey.json` for survey-review.

- A merger decree that keeps 'two churches for worship' is a lead, not a row decision: a merged parish's churches are one parish row only when the current bulletin covers both, and a pre-merger parish the directory still lists separately is reconciled to the merged row (roster link) rather than given its own row unless it still publishes its own bulletin. (accepted by survey-review, 002-survey-review, 2026-11-06)
- The Mass finder (mass.dioceseofbrooklyn.org) is not evidence for a Mass schedule or for a church having Mass; use it for coordinates and as a lead for places. Schedules come from the parish's bulletin or site. (accepted by survey-review, 002-survey-review, 2026-11-06)
- Eastern Catholic and Coptic churches GCatholic lists in Brooklyn and Queens are excluded as other-jurisdiction (their eparchies), each with a source naming the eparchy; they are not mapped under Brooklyn. (accepted by survey-review, 002-survey-review, 2026-11-06)
- The JFK airport chapel (Our Lady of the Skies) and similar chaplaincy chapels count as worship sites if they have public Mass; with no bulletin they go to excluded/ as no-bulletin, not closed. (accepted by survey-review, 002-survey-review, 2026-11-06)
- Cemetery chapels are treated the same way: one with public Mass listed on its Catholic Cemeteries page (`ccbklyn.org/our-cemeteries/<name>/`) and no bulletin is excluded as no-bulletin. GCatholic lists only St. John's, but the Holy Cross and Mount St. Mary pages may list Masses too. (map batch `q6-middle-village`, 2026-11-06)
- The diocesan archives' List of Parishes, which also lists chapels and apostolates with "Closed YYYY" notes, is a source for a chapel's listed status and contacts, not evidence that it has Mass. (map batch `q6-rego-park-elmhurst`, 2026-11-06)
- When a Mass finder place page for a merged parish lists its churches under 'All Worship Sites' but the roster line pairs one church's street with another's pin, link the massfinder entry to the church at its pin and give the other church its own record from the page's address. (map batch `b10-bensonhurst`, 2026-11-06)
- A GCatholic church left over from a merger may be a reused building under a new name: search its street address (`probe get` on `html.duckduckgo.com/html/?q=...`) and The Tablet before treating it as closed or as part of the merged parish. (map batch `b1-greenpoint`, 2026-11-07)

## Log

- 2026-11-05: Survey. Rosters: directory 172, deaneries 175, massfinder 173, gcatholic 218
  (738 entries). Plan: 53 batches in `batches.json` (52 of 2-4 directory parishes, one
  eastern-catholic), first `q11-ridgewood`; one deanery entry excluded (the diocesan
  offices). No records written; coverage not run.
