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
  common; `probe url` reports them `ok` with no platform or publisher. `/bulletins` is
  server-rendered, cards newest first, worded "Bulletin for Sunday, <date>" or, in some
  themes, "<Month DD, YYYY> / Download Bulletin" (grep for the dates), each linking a PDF
  under `files.tilmaplatform.com/system/resources/<token>/` or `<site>/system/resources/`.
  Record `other` with `page-pdfs https://<site>/bulletins`, `fetch:check` it, and read the
  newest card's date yourself: a page months stale still passes (`first-listed`, freshness
  `unknown`). If stale, `probe po <name>-church-<zip>` first (a live LPi container can sit
  beside it); with none, record `no_bulletin`, status `not-found`, a research recheck, and
  keep the recipe in its next_action. A card for the coming week can precede its file
  (`/bulletins/null`), so fetch picks the previous issue: recheck after the weekend, not a
  gap. Webstudio sites (`api.tilmaplatform.com`, `/cgi/asset/`) render `/bulletins` in JS:
  the homepage HTML embeds `latestBulletinData` with the collection's `totalCount`, and
  `visit.py` shows the cards. Tilma is only the host; check who prints the PDF:
  - `/bulletins` redirecting to `parishesonline.com/organization/<slug>` (`final_url` in
    `probe get`), or a webstudio page with `totalCount` 0 showing an embedded
    `publicationWidget?type=bulletin&id=<lpi id>` (`tools/frames-requests.py` lists the
    iframe): `probe po` the slug or id; the row is `parishes_online`.
  - LPi reposts: files named `YYYYMMDDB.pdf`, or date names (`110826.pdf`) with LPi's
    naming left on older cards, so check several cards: `probe po` finds the container and
    the row is `parishes_online`.
  - John Patrick reposts `<id>-<Parish> MM-DD-YYYY.pdf` (last-page footer `<id> <Parish>,
    Brooklyn, NY` and "John Patrick Publishing Company"): use the JPP recipe below, which
    gets each issue days before Tilma.
  - Footer "THE CHURCH BULLETIN INC., 200 DALE ST." with `#NNN`: The Church Bulletin Inc.,
    no online container: keep `other` page-pdfs with no publication id.
  - Self-made PDFs whose text layer is in a shifted font ('3KRQH' for 'Phone', digits
    dropped): greps miss Mass times and `fetch:check` reports issue-date conflicts;
    `render.py` page 1 for the masthead and take per-church Masses from `/mass-times`.
  - A webstudio "Bulletins & News" card linking `conta.cc/<id>` is a Constant Contact email
    newsletter, no PDF: unsupported, `fetch_gap` kind `constant-contact-html-newsletter`.
    The old `/bulletins` archive may still list years-old PDFs page-pdfs would pick.
- **LPi / ParishesOnline.** Many self-hosted, Tilma, WordPress, Squarespace or GoDaddy PDFs
  are LPi issues in disguise. Grep the last page for `<Parish> | 03-NNNN` (or `<Parish>,
  <Town>, NY 04-NNNN`): the prefix is the container group, so read it, don't assume 03.
  File names say the same: `03-NNNN.MMDD.pdf`, `<...>-Account-03-NNNN.pdf`, Squarespace's
  `/s/03-0NNNNMMDDYY.pdf` (5-digit pad: `03-04068` is 03/4068). Reposts can have the ad
  pages cut or every page an image, leaving no number (only "©LPi" on the cover art). Then
  try `probe po` on `<name>-church-<zip>`, `<name>-church`, and a shortened name dropping
  "of <...>" (Holy Name of Jesus is `holy-name-church-11215`); do this before the browser
  for a site that answers 403. If the container number is known but no org is found,
  record `other` page-pdfs on the bulletin page with `po-container:<a/b>` as publication
  id and a research item to find the org. Front pages are often images: `render.py` pages
  1-2. An org with no issues (self-publishing parishes have them) is not a publication id.
- **eCatholic sites** answer 403 to `probe url`; `visit.py` gives the `ecatholic:<id>`, and
  `issues.py ecatholic` reads `files.ecatholic.com` without a browser. A merged parish can
  post one bulletin on each former parish's site: compare mastheads, keep one row with both
  ids.
- **John Patrick Publishing**: `church-bulletin.org/<id>` redirects to a slug page listing
  `church-bulletin.org/bulletin/<slug>/YYYY-MM-DD.pdf`; the sites' `jppc.net/onlinebulletins/
  <id>template.pdf` answers HTML to `probe pdf`. Record `other` with `page-pdfs
  https://church-bulletin.org/<id>` and publication `url:<slug page>`; read the slug PDFs,
  often all images (`render.py`).
- **WordPress.** With no bulletin menu, list PDF uploads newest first with `probe get
  '<site>/wp-json/wp/v2/media?mime_type=application/pdf&per_page=50'`.
  - Flipbooks hide the PDF. dFlip: grep `"source":` in `window.option_df_*`. 3D FlipBook
    (`_3d-flip-book`): no URL in the HTML. A pinned `page-pdfs <bulletin page>` resolves
    both, even one weekly-overwritten PDF the unpinned resolver misses.
  - Diocesan multisite (`/wp-content/uploads/sites/<n>/`): issues at
    `/important-information/bulletin/` or `/weekly-bulletin/`, named
    `<mon><d>_<yyyy>_<parish>_compressed.pdf`, either LPi reposts (above) or self-made
    (`other` page-pdfs on that page). `probe url`, `probe pdf` and `render.py` drop the
    connection; `visit.py` and fetch work. Download with `tools/fetch-pdf.py` (not `python
    -I`) and `render.py` the file. `visit.py` may call one SPAM-SQUAT for injected betting
    spam: if address, bulletin page and PDFs are the parish's own, keep it and note it.
- **Joomla DOCman lists** (`docman_track_download`) answer 403 to probes and fetch; the
  link's `title` gives the file name, `tools/browser-pdf.py` downloads it. LPi files go
  `parishes_online`; the parish's own PDFs (no footer, no org with issues) are unsupported,
  `fetch_gap` kind `joomla-docman-file-403`.
- **Wix** pages can show the issue only as a slideshow of hash-named
  `static.wixstatic.com/media/<id>~mv2.jpg` slides (no PDF, no date): unsupported,
  `fetch_gap` kind `wix-image-slideshow`; `tools/frames-requests.py` lists the slides.
- **Self-hosted pages.** `fetch:check` calls one stale file `ok`, freshness `unknown`:
  check the date before pinning. `MMDDYY.pdf` names in an unordered archive fool the
  resolver: pin the homepage link with `filename=[0-9][0-9][0-9][0-9][0-9][0-9].pdf`. A
  fixed file behind a redirect (`/bulletin` -> `/files/bulletin.pdf`): set the website to
  the homepage and `fetch:check` resolves `redirected-pdf <site>/bulletin`.
- **Google Drive.** `drive/folders/<id>` serves its first 50 files in name order, so
  `drive-folder` can pick a years-old issue: list it all with
  `drive.google.com/embeddedfolderview?id=<id>#list` before pinning. Google Sites embedding
  each issue as `drive.google.com/file/d/<id>/preview` is unsupported, `fetch_gap` kind
  `drive-preview-embed`; read it via `drive.google.com/uc?id=<id>&export=download`.
- **JavaScript-only sites** (Next.js `/_next/static`, Vite `/assets/index-*.js`): grep the
  bundle for `drive.google.com`, `docs.google.com/spreadsheets` or `supabase.co`. A link
  that exists only in JS makes the row unsupported with a `fetch_gap`.
- **Shared pastors.** Parishes sharing a pastor can each print both churches' Mass times on
  page 1 of separate bulletins: compare mastheads, intentions and collections before
  merging, and record the review.
- **Finding a current site.** When the directory's homepage is dead or parked, Discover
  Mass (`discovermass.com/church/<name>-<town>-ny/`) names the current website. Sites
  answering 403 or redirecting off-site: try `probe po`, then `visit.py`; read the target.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- eCatholic archive links carry ?t=<ms epoch> upload stamps: when the newest issue is stale, decode them to tell a batch-uploading parish (many issues posted the same day) from one that stopped; and probe po <name>-church-<zip> or <name>-roman-catholic-church-<zip>, since a parish's LPi container can start beside a stale eCatholic or Tilma archive.
- Tilma upload stamps: the resource token base64-decodes to the upload date ('2026/10/02/...'); a parish whose cards arrive in batches every 2-10 weeks can look stale between batches, so set the recheck after the usual gap instead of reading the gap as a stop.
- Wix blog bulletins (a /sunday-bulletin blog index, one /post/<slug> per issue with a 'Download PDF' file widget): the PDF URL comes only from a click-time Wix API, so fetch finds no PDF links; record unsupported with fetch_gap kind wix-blog-file-download. tools/click-requests.py gives the ugd/<id>.pdf, readable at <site>/_files/ugd/<id>.pdf.
- Parishes sharing a pastor here can each print 'In partnership with <other parish>' and both rectories' contacts on page 1 of their own LPi bulletins (OLA 03/4061 and St. Anselm 03/4053), while the schedules and intentions stay separate; read the schedule and intentions, not the masthead line, and record separate reviews.
- The Tablet (thetablet.org) asks for a login after a few paragraphs; its WordPress API (wp-json/wp/v2/posts?search=<words>&_fields=link,date,title) lists dated articles for closures and sales, and probe get on an article still returns the opening paragraphs to quote.
- The Church Bulletin Inc. ad-page footer number (#167, #117, #224) is per parish: different numbers plus different mastheads support a 'separate' review between neighbouring Church Bulletin Inc. rows, which have no publication id to compare.
- Mass finder place pages for merged parishes list every worship site under 'All Worship Sites', but the roster line can pair one church's street with another's pin: link the massfinder entry to the church at its pin and give the other church its own record from the page's address.
- LPi org slugs here are not always <name>-church-<zip>: Our Lady of Solace's is the directory's full name with no zip (shrine-church-of-our-lady-of-solace, 03/9994); when the zip forms miss, probe po the directory name slugged as-is before treating a stale self-hosted archive as a stop.
- Google Sites bulletin pages that link each issue as drive.google.com/file/d/<id>/view (not /preview embeds) work as `other` with `page-pdfs <site>/bulletins`: fetch resolves the newest link to uc?export=download and downloads the PDF, though issue date stays `unknown`, so read the linked date yourself.
- Diocesan-multisite issues named <mon><d>_<yyyy>_<parish>_compressed.pdf can also be The Church Bulletin Inc. issues (footer #NNN, no container): record other with page-pdfs on the /important-information/bulletin/ or /bulletin/ page and no publication id; fetch resolves it 'current' from the file name even when the masthead's text layer is a shifted font.
- Old frameset parish sites (index.html with <frame src=links.htm>) hide the bulletin link from the resolver (fetch:check NoBulletin on the homepage): pin `page-pdfs <site>/<menu frame>.htm` to reach a fixed bulletin.pdf, then check its date yourself, since freshness stays unknown.
- John Patrick slug pages (church-bulletin.org/<id>) post each issue about a week before parish sites repost it, and list issues in date order where a Tilma page may group cards by month; a merged parish's former JPP job can survive as a slug page listing no PDFs, which is a dormant bulletin, not a publication id.
- Diocesan-multisite bulletin pages (/weekly-bulletin/) can list a non-bulletin PDF (an event request form) above the issues; pin page-pdfs with filename=*compressed*.pdf so the first-listed pick is the newest issue.
- Tilma bulletin issues can have no name masthead (St. Michael – St. Malachy's page 1 is intentions, readings and one Mass schedule): identify the issue by its hosting site and a schedule that matches the site's Mass Times page, and say so in the record, since fetch:check leaves publication identity unverified.
- Self-hosted bulletin pages served over http://www. can link PDFs as absolute https:// bare-domain URLs whose certificate fails (hostname mismatch); fetch has no http fallback, so record unsupported with fetch_gap kind https-pdf-link-cert-mismatch and keep the page-pdfs recipe in the research next_action.

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
