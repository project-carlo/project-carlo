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

From the survey's sample (2026-11-12: `probe url` on all 76 directory websites, `visit.py
--bulletin` on 4 of the 12 that answered 403). New York, the only mapped neighbour, has no
publisher notes; the lines below borrow Paterson's where the same publishers appear.

- **LPi / ParishesOnline is the commonest embed** (14 sites link parishesonline.com, one
  4lpi.com): use `probe po` for the org, LPi id and container.
- **Duda sites** (bulletin links on `irp.cdn-website.com/<site>/files/uploaded/...`, 19
  sites): the parish uploads its own PDFs; the file names, not a publisher, date them.
- **eCatholic behind Cloudflare:** 12 sites answer `probe url` with 403 (St. Edward, Holy
  Name of Jesus Stamford, St. Peter Danbury, St. James Stratford gave `ecatholic` ids in
  `visit.py`). Use `visit.py` on the `/bulletins` page; Paterson's notes on stale
  `files.ecatholic.com` archives apply.
- **Bon Venture** (3: Our Lady of Guadalupe Danbury, Sacred Heart Stamford, St. Mary Greenwich)
  and **John Patrick Publishing** (`jppc.net`, 2: St. Elizabeth Seton, St. Joseph–St.
  Ladislaus; `church-bulletin.org` on St. Mary Stamford): see Paterson's notes.
- **Discover Mass:** Immaculate Heart of Mary, Danbury's directory website is its Discover
  Mass page. Discover Mass caps daily downloads (Scranton, Allentown).
- 39 sites returned 200 with no publisher found; read their bulletin pages.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- LPi bulletins here can be image-only apart from the ad pages (St. Mark 04/0152, Our Lady of Peace 04/0327: probe pdf reads only pages 7-8); render page 1 with parish-site-access render.py to read the masthead and Mass schedule, and note image-only in the record.
- Bon Venture and John Patrick Publishing issues here are posted on the parish's own site rather than read from the printer: Bon Venture PDFs on a Duda /bulletin page (footer 'NNNA (PK) - <parish>'), which fetch:check reads with recipe page-pdfs; JPPC issues on the eCatholic site (the jppc.net/onlinebulletins/<n>template.pdf link is the printer's template, not an issue).
- A parish site that names LPi but embeds no widget (a Wix cover gallery, St. Charles) can still have a live ParishesOnline org: try `probe po <name>-church-<zip>` before calling it no_bulletin.
- WordPress 'TNC FlipBook' (pdf-viewer-for-wordpress) bulletin pages link /pdfviewer/<slug>/ viewer pages that carry the PDF URL base64-encoded; decode it to read the issue. fetch can't collect these yet, so record the row as unsupported with fetch_gap kind viewer-wrapped-pdf.
- Some eCatholic parishes here post bulletins as site documents (ec-prod-site-cache.s3.amazonaws.com/static1/<site>/documents/...) rather than files.ecatholic.com/<id>/bulletins, so the ecatholic resolver fails; use provider other with a pinned page-pdfs recipe on the page listing them, plus a filename filter when inserts are listed alongside (Our Lady of Fatima: filename=*Year*.pdf).
- church-bulletin.org (JPPC): a parish site's Bulletins link can point at a slug that serves only JPPC's generic welcome page (St. Francis Weston's 'st-...'); try the 'saint-...' variant of the slug, and check by saving the HTML with probe get --out and grepping for bulletin/<slug>/<date>.pdf (probe get's text output drops links).
- Joomla /bulletins/<n>-<date>/file links behind Cloudflare answer 403 even to the browser context's request client; tools/browser_download.py fetch()es the file from inside the page to read an issue (render it with pdftoppm). fetch can't collect these: record unsupported, fetch_gap joomla-file-endpoint.
- Duda 'Bulletin' pages can list issues oldest first with irregular gaps (Georgetown Oratory); fetch:check's page-pdfs still picked the newest by its file-name date.
- Bon Venture sponsor pages (http://sponsors.bonventure.net/?page=<n>): fetch:check run with PLAYWRIGHT_BROWSER_CHANNEL=chrome fetched the picked PDF over https and failed TLS verification; run without the Chrome channel it fetched over http fine (Our Lady of Guadalupe Danbury, page 5008).
- A Duda bulletin page that lists an older year's block first can make page-pdfs pick last year's issue; pin a year filter (filename=*2026.pdf) and set a January revisit to update it.
- JPPC: a parish site's https://www.jppc.net/onlinebulletins/<n>template.pdf link, church-bulletin.org/<n> and church-bulletin.org/?id=<n> can all redirect to the parish's church-bulletin.org/<saint-...> page listing dated issues (St. Elizabeth Seton 9011, St. Mary Ridgefield 936); probe get the link to follow it, pin page-pdfs on the final page. These JPPC issues are image-only: render page 1 for the masthead.
- fetch:check can't date WordPress uploads named '<YYYY>.<MonD>-...pdf' (e.g. 2026.Nov15-E-News-2.pdf) and reports date/freshness unknown; the pick then relies on the page listing newest first, so set a revisit to recheck it.
- A parish site that posts its own copies of an LPi bulletin (Google Drive file links, FaithConnector /e/bulletin redirecting to faithconnector.s3.amazonaws.com/<site>/files/<sunday>.pdf) still has a live ParishesOnline org: read the ad-page footer's NN-NNNN container and `probe po <name>-church-<zip>`, and use parishes_online (St. Thomas the Apostle Norwalk, St. Thomas More Darien).
- Slugs are global: `pnpm diocese search` also lists other dioceses' live rows, and Connecticut towns that share a name with a New York town collide (Albany's live sacred-heart-stamford is Stamford NY); add -ct to the slug (sacred-heart-stamford-ct).
- A chapel the bulletin places inside or behind the parish church (St. Joseph's Chapel '(St. Mary)', a chapel 'in the rear of the rectory') goes on that church's row, with its mass-times roster entry linked there, not on a church row of its own.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches in Fairfield County (Ukrainian Eparchy of Stamford incl. St. Vladimir Cathedral and St. Basil Seminary; Melkite Eparchy of Our Lady of the Annunciation in Boston; Maronite Eparchy of St. Maron of Brooklyn; Ruthenian Eparchy of Passaic) are excluded as other-jurisdiction. (accepted by survey-review, 003-survey-review, 2026-11-12)
- A merged parish's second church or 'campus' that its schedule still lists with Mass (St. George, St. Patrick Bridgeport, St. Benedict, Sacred Heart Danbury, St. Gabriel, St. Ladislaus, St. Agnes/St. Catherine, Sacred Heart & St. Patrick Redding) is a church of that one parish row unless it publishes its own bulletin. (accepted by survey-review, 003-survey-review, 2026-11-12)
- A community housed at a parish's church with its own rector or moderator (Georgetown Oratory at Sacred Heart, Redding; Haitian quasi-parish at St. Cecilia, Stamford) is a separate parish row only if it publishes its own bulletin; otherwise its Masses are on the host parish's row. (accepted by survey-review, 003-survey-review, 2026-11-12)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-12: Survey (bridgeport-map-1): created the diocese; rosters gcatholic 92
  (89 fetched + 3 added from /churches/northamerica/ pages), directory 77, mass-times 14;
  12 batches in batches.json, all 183 entries assigned. No
  records yet, so no coverage.
