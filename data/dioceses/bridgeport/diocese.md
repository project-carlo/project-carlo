---
name: Roman Catholic Diocese of Bridgeport
state: CT
website: https://www.bridgeportdiocese.org
status: exploring
gcatholic: brid0
---

Fairfield County, Connecticut, the whole county and nothing else: Bridgeport, Stamford,
Norwalk and Danbury are the cities; Greenwich, Fairfield, Westport, Trumbull, Stratford,
Shelton, Ridgefield, Newtown and the smaller towns make up the rest. It borders the
Archdiocese of Hartford (New Haven and Litchfield counties) to the east and north and the
Archdiocese of New York (Westchester, Putnam and Dutchess counties) to the west; Long Island
Sound is the south. The diocesan directory lists 77 entries (2026-11-12): about 73 canonical
parishes, plus the Georgetown Oratory (Redding), St. Margaret's Shrine (Bridgeport), the
Haitian quasi-parish Notre Dame du Perpétuel Secours (Stamford) and St. Timothy Chapel
(Greenwich). There is no family, cluster or pastorate system: each parish has its own
pastor, and only one priest is named for two parishes (Fr. Leonel Medeiros: Our Lady of
Aparecida, Bethel, and Immaculate Heart of Mary, Danbury). Consolidation has been parish by
parish, leaving merged parishes with two churches or "campuses" (Cathedral Parish: St.
Augustine and St. Patrick; St. Charles Borromeo with St. George; St. Mary, Stamford with St.
Benedict; St. Peter, Danbury with Sacred Heart of Jesus; St. Cecilia–St. Gabriel; St.
Catherine–St. Agnes; St. Joseph and St. Ladislaus; Sacred Heart & St. Patrick, Redding).
Shared bulletins are most likely inside those parishes, between parishes and the
communities housed at their address (the Georgetown Oratory, the Haitian quasi-parish), and
in the November 2025 Holy Family–St. Emery merger. The 2026 "pilot parishes" are a renewal
programme (The One), not a regrouping.

## Sources

- **Parish directory (Find a Parish / Mass Times):** https://www.bridgeportdiocese.org/mass-times/,
  a WordPress JetEngine listing whose data is the `parishes` post type at
  https://www.bridgeportdiocese.org/wp-json/wp/v2/parishes?per_page=100 (77 posts, read
  2026-11-12): address, town, pastor, phone and a Mass-time table with notes; the page's cards
  add the website. Imported as roster `directory` (scratch/bridgeport-map-1/tools/bridgeport_directory.py).
  One entry per parish, not per church, and no coordinates. Current on pastors (it already
  shows the Holy Family–St. Emery merger) and good for websites; two entries share an
  address with another (Sts. Cyril & Methodius and St. Mary, Bridgeport, both at 79 Church
  Street; the Haitian quasi-parish at St. Cecilia's 1184 Newfield Avenue; the Georgetown
  Oratory at Sacred Heart, 30 Church Street, Redding). The Haitian entry's website is a 2016 PDF on
  an old diocesan host.
- **Mass times:** the same posts' Mass-time notes name a parish's second worship sites ("At
  St. George campus", "St. Benedict campus", "At Fairfield University's Egan Chapel"). The 14
  named sites are roster `mass-times`, `group` = the parish whose schedule names them. Notes
  saying only "In chapel", "Lower Church" or "Upper Church" are rooms of the main church and
  are left out. A per-parish JSON is at `/wp-json/custom/v1/mass-times?parish_id=<post id>`.
- **GCatholic:** key `brid0`, https://gcatholic.org/churches/local/brid0, roster `gcatholic`
  (92 entries, 2026-11-12: 84 diocesan and 8 "Other Churches Within the Diocesan Territory").
  `roster fetch` returned 89: it skips churches GCatholic files under
  `/churches/northamerica/<id>` (St. Augustine Cathedral 2046, Basilica of St. John the
  Evangelist 4950, St. Vladimir Cathedral 2416), which were added from their own pages by
  scratch/bridgeport-map-1/tools/gcatholic_add_northamerica.py. Re-run it after any refetch. Lists churches still on it after mergers (St. George and St.
  Patrick, Bridgeport; Holy Family and St. Emery, Fairfield; St. Benedict, Stamford; Sacred
  Heart, Danbury; St. Ladislaus, Norwalk; St. Agnes, Greenwich), and Holy Trinity, Sherman,
  which the directory doesn't list. It omits St. Francis of Assisi (Weston), Our Lady of Aparecida
  (Bethel), Sacred Heart (Georgetown) and St. Catherine of Siena (Riverside). Eight entries
  are Eastern Catholic, in other jurisdictions: Ukrainian Eparchy of Stamford (St. Vladimir
  Cathedral and St. Basil Seminary, Stamford; Protection of the BVM, Bridgeport), Melkite Eparchy of Our Lady of the Annunciation
  in Boston (St. Ann and Mother of God of Tenderness, Danbury), Maronite Eparchy of St. Maron
  of Brooklyn (St. Anthony, Danbury), Ruthenian Eparchy of Passaic (St. Nicholas, Danbury;
  St. John the Baptist, Trumbull). St. John Fisher Seminary is the diocese's own.
- **Clusters / families of parishes:** none. The site has no cluster or family list; a
  `pilot-parishes` post type (April 2026) holds only renewal-programme resources. The
  directory's pastor field is the only clergy-sharing source (one shared pastor, above);
  the clergy pages (https://www.bridgeportdiocese.org/clergy-and-religious/home/) were not read.
- **Closed parishes and where their records went:** no list found. Known: Holy Family–St.
  Emery (Fairfield) merged into Assumption (Fairfield), St. Ann and St. Peter (Bridgeport) on
  1 November 2025, with regular Mass at Holy Family to end 4 January 2026
  (https://www.bridgeportdiocese.org/holy-family-st-emery-parish-to-merge-with-assumption-parish-fairfield-st-peter-parish-and-st-ann-parish/,
  2025-11-03); "St. Emery to be Erected as an Oratory"
  (https://www.bridgeportdiocese.org/st-emery-to-be-erected-as-an-oratory/, 2025-10-01; body
  not readable with `probe get`).
- **Pastoral plan / closure announcements:** none found by the site search (wp-json search
  for "cluster", "pastoral plan", "merger", "consolidat", 2026-11-12) beyond the above.

### Bulletin publishers here

From the survey's sample (2026-11-12) and the map batches since. New York, the only mapped
neighbour, has no publisher notes; Paterson's notes cover the same publishers.

- **LPi / ParishesOnline** is the commonest publisher (parishesonline.com or 4lpi.com
  links): use `probe po` for the org, LPi id and container. A parish site that names LPi
  without a widget (a Wix cover gallery), or posts its own copies of the LPi bulletin
  (Google Drive links; FaithConnector `/e/bulletin` redirecting to
  `faithconnector.s3.amazonaws.com/<site>/files/<sunday>.pdf`), still has a live org: read
  the ad-page footer's `NN-NNNN` container, try `probe po <name>-church-<zip>`, and record
  `parishes_online` rather than no_bulletin or the copy. Issues here are often image-only
  apart from the ad pages (`probe pdf` reads only pages 7-8): render page 1 with
  parish-site-access `render.py` for the masthead and schedule, and note image-only in the
  record.
- **Duda sites** (`irp.cdn-website.com/<site>/files/uploaded/...`): the parish uploads its
  own PDFs; file names, not a publisher, date them. Use fetch:check with recipe
  `page-pdfs` on the `/bulletin` page; it picks the newest by file-name date even when the
  list runs oldest first with gaps. A page that lists an older year's block first can make
  it pick last year's issue: pin a year filter (`filename=*2026.pdf`) and set a January
  revisit to update it.
- **eCatholic behind Cloudflare** (403 to `probe url`): use `visit.py` on the `/bulletins`
  page; Paterson's notes on stale `files.ecatholic.com` archives apply. Some sites post
  bulletins as site documents
  (`ec-prod-site-cache.s3.amazonaws.com/static1/<site>/documents/...`) rather than
  `files.ecatholic.com/<id>/bulletins`, and the ecatholic resolver fails on them: use
  provider other with a pinned `page-pdfs` recipe on the page listing them, plus a filename
  filter when inserts are listed alongside (`filename=*Year*.pdf`).
- **Bon Venture:** issues are read from the parish's own site, typically PDFs on a Duda
  `/bulletin` page (footer `NNNA (PK) - <parish>`), which `page-pdfs` reads. Bon Venture
  sponsor pages (`http://sponsors.bonventure.net/?page=<n>`) work too, but run fetch:check
  there without `PLAYWRIGHT_BROWSER_CHANNEL=chrome`: with the Chrome channel it fetched the
  PDF over https and failed TLS verification; without it, http worked.
- **John Patrick Publishing (JPPC):** a `jppc.net/onlinebulletins/<n>template.pdf` link is
  the printer's template, not an issue. That link, `church-bulletin.org/<n>` and
  `church-bulletin.org/?id=<n>` can each redirect to the parish's
  `church-bulletin.org/<saint-...>` page listing dated issues: `probe get` the link to
  follow it and pin `page-pdfs` on the final page. A slug that serves only JPPC's generic
  welcome page (`st-...`) usually has a `saint-...` variant. `probe get`'s text output drops
  links, so check with `probe get --out` and grep the HTML for
  `bulletin/<slug>/<date>.pdf`. Some parishes instead post JPPC issues on their eCatholic
  site. JPPC issues are image-only: render page 1 for the masthead.
- **Discover Mass** caps daily downloads (Scranton, Allentown).
- **WordPress sites:**
  - *TNC FlipBook* (pdf-viewer-for-wordpress) pages link `/pdfviewer/<slug>/` viewers that
    carry the PDF URL base64-encoded; decode it to read the issue. fetch can't collect
    these: record unsupported, fetch_gap `viewer-wrapped-pdf`.
  - *Download Monitor* lists (`/download/<id>/` redirecting to
    `wp-content/uploads/dlm_uploads/...pdf`) aren't read by `page-pdfs`; if the home page
    links the newest PDF directly, pin `page-pdfs` there and set a revisit.
  - Uploads named `<YYYY>.<MonD>-...pdf` (`2026.Nov15-E-News-2.pdf`) are undatable to
    fetch:check (date/freshness unknown), so the pick relies on the page listing newest
    first: set a revisit to recheck it.
- **Joomla** `/bulletins/<n>-<date>/file` links behind Cloudflare answer 403 even to the
  browser context's request client; `tools/browser_download.py` fetch()es the file from
  inside the page (render with `pdftoppm`). fetch can't collect these: record unsupported,
  fetch_gap `joomla-file-endpoint`.
- **Slugs are global:** `pnpm diocese search` lists other dioceses' rows too, and
  Connecticut towns that share a New York town's name collide (Albany has
  `sacred-heart-stamford`, Stamford NY). Add `-ct` to the slug.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches in Fairfield County (Ukrainian Eparchy of Stamford incl. St. Vladimir Cathedral and St. Basil Seminary; Melkite Eparchy of Our Lady of the Annunciation in Boston; Maronite Eparchy of St. Maron of Brooklyn; Ruthenian Eparchy of Passaic) are excluded as other-jurisdiction. (accepted by survey-review, 003-survey-review, 2026-11-12)
- A merged parish's second church or 'campus' that its schedule still lists with Mass (St. George, St. Patrick Bridgeport, St. Benedict, Sacred Heart Danbury, St. Gabriel, St. Ladislaus, St. Agnes/St. Catherine, Sacred Heart & St. Patrick Redding) is a church of that one parish row unless it publishes its own bulletin. (accepted by survey-review, 003-survey-review, 2026-11-12)
- A community housed at a parish's church with its own rector or moderator (Georgetown Oratory at Sacred Heart, Redding; Haitian quasi-parish at St. Cecilia, Stamford) is a separate parish row only if it publishes its own bulletin; otherwise its Masses are on the host parish's row. (accepted by survey-review, 003-survey-review, 2026-11-12)
- A chapel the bulletin places inside or behind a parish church (in the church, or 'in the rear of the rectory') goes on that church's row, with its mass-times roster entry linked there, not on a church row of its own. (map batch `stamford-central`, 2026-11-12)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-12: Survey (bridgeport-map-1): created the diocese; rosters gcatholic 92
  (89 fetched + 3 added from /churches/northamerica/ pages), directory 77, mass-times 14;
  12 batches in batches.json, all 183 entries assigned. No
  records yet, so no coverage.
