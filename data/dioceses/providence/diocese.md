---
name: Roman Catholic Diocese of Providence
state: RI
website: https://dioceseofprovidence.org
status: exploring
gcatholic: prov0
---

The whole state of Rhode Island: Providence, Kent, Washington, Newport and Bristol counties.
The main towns are Providence, Warwick, Cranston, Pawtucket, East Providence, Woonsocket,
Newport, Central Falls, Westerly and Bristol. Neighbours: Norwich (west: eastern
Connecticut), Worcester (north-west), Boston (north-east) and Fall River (east: Bristol
County, Massachusetts, which wraps around Tiverton and Little Compton). None of them is
mapped yet. There are no families, clusters or pastorates: the diocese is organised in
deaneries and has been merging parishes one at a time (Woonsocket 2018–2022, Pawtucket
2025–26, West Warwick and St. Agnes into St. Ann in November 2025, East Providence and
Warren in May 2026). A merged parish usually keeps one bulletin and sometimes a mission
church. Shared bulletins across canonical parishes are most likely where the finder names
one priest as pastor or administrator of two or three parishes (about twenty such sets,
written into each batch's `why` in `batches.json`). The finder lists 166 places (about 125
open parishes plus merged-away and closed ones, missions and a chapel); GCatholic lists 155
churches, four of them Eastern Catholic.

## Sources

- **Parish finder (directory roster):** https://dioceseofprovidence.org/parishfinder, read
  2026-11-14 with parish-site-access `finder.py` (eCatholic map behind Cloudflare). 170
  entries: four are notices pinned to the top (excluded in `batches.json`), 16 carry
  "CLOSED" in the name, and many more say "(merged into ...)" without it. Each popup holds
  the pastor or administrator, the legal title, dated merger and closure decrees, and the
  Mass schedule; `scratch/providence-map-1/tools/finder_details.py` extracts that text from
  a saved copy of the page. Good for: structure (the dated decree notes are the best list of
  mergers we have), shared pastors, homepages. Lags on: names (merged parishes keep their
  entries), some homepages are masstimes.org map links (Immaculate Heart of Mary, Our Lady
  of Lourdes, Sacred Heart West Warwick, St. Anthony Portsmouth) or Facebook pages, and two
  are dead domains (sainthomaschurchofprovidenceri.com, saintjosephwoonsocket.org).
- **GCatholic:** `rosters/gcatholic.json` (key `prov0`), 155 entries, fetched 2026-11-14,
  with Plus Codes. Its `group` gives the canonical parish where it differs (Holy Family for
  Our Lady of Consolation and St. Joseph, Pawtucket; St. John Paul II for St. Cecilia and
  St. Leo; Sts. Rose and Clement for St. Clement). It still lists churches the finder marks
  merged or closed (St. Brigid, St. Casimir, St. Maria Goretti, St. William, St. Jean
  Baptiste and others), two "Former Church" entries (Immaculate Conception, Westerly; St.
  Ann, Woonsocket), Portsmouth Abbey's church and Our Lady of Providence Seminary, which the
  finder doesn't list. It lacks St. Agatha, Woonsocket and several closed churches only the
  finder has.
- **Eastern Catholic churches:** four, each with a GCatholic `Jurisdiction:` line naming an
  eparchy (read 2026-11-14): St. Basil the Great, Lincoln and St. Elias, Woonsocket
  (Melkite, Newton); St. George (Maronite, St. Maron of Brooklyn); St. Michael, Woonsocket
  (Ukrainian, Stamford). The finder lists three of them (not St. Elias) and puts St. George
  at the former St. Ann church, 1493 Cranston St., Cranston, while GCatholic gives 171 Twin
  River Rd., Lincoln.
- **Clusters / families of parishes:** none. The diocese doesn't group parishes; the Office
  of Pastoral Planning page (https://dioceseofprovidence.org/office-of-pastoral-planning,
  read 2026-11-14) has a mission statement but no plan or list.
- **Shared pastors:** from the finder popups only (2026-11-14). The printed Official
  Diocesan Directory (https://dop.directory/, 2025 edition) is sold, not online.
- **Mass times:** in the finder popups (no separate Mass-times page). The finder warns
  "Please contact each parish directly for updated Holy Mass times".
- **Closed parishes and where their records went:** in the finder popups: each closed or
  merged entry says where its sacramental records are held. Decree dates there run from
  1998 to 2026-05-11.
- **Pastoral plan / closure announcements:** diocesan news posts
  (`dioceseofprovidence.org/news/...`), linked from some finder popups (St. Madeleine
  Sophie into St. Catherine of Siena, 2023).

### Bulletin publishers here

From `probe url` of the finder's 129 distinct homepages (survey, 2026-11-14) and the map
batches since. About a quarter of homepages answer 403 or don't load to `probe url`; open
them with `visit.py --bulletin` before concluding there is no bulletin.

- **Finding a site or its old issues:** when the finder's homepage is only a masstimes.org
  map link, try the parish's email domain or a DuckDuckGo search (`probe get
  'https://html.duckduckgo.com/html/?q=...'`; `site:` finds sub-pages too). When a site is
  down (Cloudflare 522), the Wayback CDX API (`probe get
  'https://web.archive.org/cdx/search/cdx?url=<domain>/*&output=json&filter=statuscode:200&collapse=urlkey'`)
  lists its old bulletin files and dates the last issue posted.
- **eCatholic, usually behind Cloudflare:** a homepage that answers 403 to `probe url` is
  most often eCatholic (`ecatholic:<id>`); it loads in `visit.py`. Read issues with
  `issues.py ecatholic`. `ecatholic:5523` is the diocese's own site (bulletin inserts,
  documents): never record it on a parish. `visit.py --text` drops tab-panel content
  (e.g. a 'Daily Schedules' page): save `visit.py --html <file>` and grep that. `visit.py`
  can hang on a homepage whose sub-pages load: find the sub-pages by search and visit
  them directly. Many eCatholic sites only repost LPi:
  - Bulletins page embeds ParishesOnline issues, with no files at
    `files.ecatholic.com/<id>/bulletins`: the parish publishes on ParishesOnline; record the
    po-org/lpi/po-container ids, not the eCatholic id.
  - LPi files in the documents folder (`files.ecatholic.com/<id>/documents/YYYY/MM/<date>B.pdf`):
    its "Bulletin archive" link (`visit.py --links --match parishesonline`) gives
    `parishesonline.com/find/<slug>`; `probe po <slug>` finds the org.
  - Once the LPi org is found, record the row on `parishes_online`, with the eCatholic id
    as a second publication id, so fetch avoids Cloudflare.
- **ParishesOnline (LPi), mostly region 03:** linked on 16+ sites, often beside an
  eCatholic id. Read the masthead, not the org name or footer: a footer's account name
  (e.g. 'St. Clare St Vincent de Paul') can name a church the masthead has dropped.
  - Finding the org when the footer gives only a container, or the parish site is dead:
    `probe po` with `<name>-<zip>` (`st-michaels-church-02917`), `<name>-church-<zip>`
    (`christ-the-king-church-02881`), `<name>-church`, or a possessive slug with no ZIP
    (`st-marthas-church`). Check the org lists issues; some list none. Not every container
    is region 03: when a 03 guess fails, try `probe container 04/<n>`.
  - One bulletin can sit in two containers with different ad pages and footers, and two
    pre-merger orgs can share one container: compare rendered pages 1-2, then record every
    container and org id on the one row.
  - Many issues here are image-only apart from the ad pages, or have an encoded-font text
    layer (`probe pdf` calls every page readable but returns glyph codes like `/0/1 /2/3`
    and `--grep` finds nothing). Read the masthead and Mass schedule with `render.py`.
  - The text layer can hold a stale page under the current image (a 2023 date on page 1),
    so `fetch:check` reports a date conflict: render page 1 and date the issue from the
    inner pages.
  - A mission or occasional-use church the weekly schedule omits can appear in the
    Christmas Eve Masses: grep the issue for the Sunday before Christmas for its name.
  - Orgs with no LPi container that carry parish-uploaded PDFs
    (`customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/<lpi id>/publications/...`):
    `probe po` lists them but the `parishes_online` collector fails ("No matching anchor
    link"). Record `bulletin_provider: unsupported`, fetch_gap kind `po-user-upload`.
- **John Patrick Publishing (jppc.net / church-bulletin.org):** linked on 15+ sites. Set
  website to the `church-bulletin.org/<slug>` page (`jppc.net/onlinebulletins/<id>template.pdf`
  redirects there), provider `other`, recipe `page-pdfs`; no browser needed even when the
  parish's own site can't be reached. Current issues are often image-only, but older
  issues on the page can have text layers: `probe pdf --grep` across them finds merger
  or closure letters to quote. Traps:
  - A guessed `church-bulletin.org/<slug>` answers 200 even with no bulletin (a generic
    archive page, or one with no PDFs). Only a jppc id linked from the parish site, or a
    page listing dated PDFs, is evidence.
  - A page can carry another parish's bulletin (St. Matthew Cranston's posts St. Paul's
    LPi issue). Compare its masthead with the host parish's bulletin and record the page as
    an extra publication id on the host's row, not as a row of its own.
  - A parish with an eCatholic site may also post the same issue, with a text layer, at
    `files.ecatholic.com/<id>/bulletins/YYYYMMDD.pdf`: read or date it with `issues.py
    ecatholic --grep`, and record the eCatholic id as a second publication id.
- **WordPress sites** whose bulletin page is linked only as `?page_id=N`: find it with
  `probe get <site>/wp-json/wp/v2/pages?search=bulletin`, or list PDFs newest first with
  `/wp-json/wp/v2/media?mime_type=application/pdf`. A bulletin posted only as a Word
  `.doc` can't be fetched (`fetch_pdf.py` says 'Not a PDF'): read it with
  `tools/fetch_raw.py` + `tools/doc_text.py`, record `unsupported`, fetch_gap
  `word-doc-bulletin`.
- **Duda sites** (PDFs on `irp.cdn-website.com/<site>/files/uploaded/`, linked newest
  first from a `/bulletin` page): provider `other`, recipe `page-pdfs` on the `/bulletin`
  page.
- **Squarespace sites** (PDFs at `<site>/s/Web-MMDDYY.pdf`, newest first): provider
  `other`, recipe `page-pdfs`. `fetch:check` can't date the file names (freshness
  `unknown`), and the page-1 date line can be a stale template: confirm the issue from
  the Mass intentions.
- **Wix sites** (PDFs at `_files/ugd/<acct>_<hash>.pdf`): `page-pdfs` picks the header's
  'Bulletin' link to the current issue, but hashed names and image-only pages leave
  freshness `unknown`: date the issue by rendering page 2.
- **GoDaddy-builder sites** (PDFs on `img1.wsimg.com`) posting English and Spanish
  editions each week: `page-pdfs` with `filename=English*.pdf` picks the English issue
  even on an oldest-first page.
- **Weebly pages embedding each week's bulletin as a Canva design** (iframe
  `canva.com/design/<id>/<key>/view?embed`): `visit.py --text` on the `/view` URL returns
  the full text (masthead, Mass times). Record `unsupported`, fetch_gap
  `canva-design-viewer`.
- **Google Sites** ('Embedded Files'): `visit.py` can hang past its timeout; read them
  with `probe get` and check the data-code embeds for a Drive or bulletin link.
- **Bon Venture** (`sponsors.bonventure.net/?page=<id>`, often linked only from a cover
  image on the parish's bulletin page): `page-pdfs` finds the current
  `pdfs/<id>/YYYY-MM-DD.pdf`, but the https download fails certificate verification.
  Record `bulletin_provider: unsupported`, fetch_gap `tls-certificate-unverified`, keeping
  the `page-pdfs` recipe in `provider_id`.
- **Discover Mass:** some finder homepages are a Discover Mass page
  (`discovermass:<slug>`).
- **Sites that drop probe connections** (RemoteDisconnected) while `fetch:check` downloads
  their PDFs: save the issue with `tools/fetch_pdf.py` and read it with `render.py`
  (`probe pdf` takes URLs only).

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Finder entries that are notices (ids 34817, 25351, 33152, 29428) are not places and are excluded from planning; nothing is recorded for them. (accepted by survey-review, 002-survey-review, 2026-11-15)
- A finder entry for a parish merged away can keep its pre-merger Mass times below the merger note: those times are not evidence of Mass. Check each church against the successor's current bulletin. (map batch `pawtucket-central-falls`, 2026-11-16)
- Eastern Catholic churches in the territory (GCatholic and the finder list them) are excluded as `other-jurisdiction`. When one now worships in a closed Latin church's building, the Latin church's roster entries go on the Eastern church's record, not a `closed` record, since the building still holds public Mass (e.g. St. Ann Cranston, now St. George Maronite). (map batch `eastern-catholic`, 2026-11-16)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-16: reconcile (providence-map-1/023-reconcile) after 17 map batches (usually 17-22 roster entries each; 8-30). Coverage: directory 166/170 accounted for (the 4 left are the finder's notice entries, per *Rules settled*), modelled 112/141; gcatholic 155/155, modelled 107/130. Records: 103 parishes (8 no_bulletin, 5 unsupported), 126 churches, 31 excluded, 8 open. No merges or moves: Holy Angels, Barrington kept separate from St. Luke (its own 11 October issue is still posted; revisit 2026-12-15); the St. Anthony, Pawtucket / St. Francis Xavier lead was already answered (separate mastheads). Audit: 10 candidate pairs, all with content-supported separate reviews. fetch:check: 90 rows, all transport ok; 5 not current, each stale at the publisher and already carrying a revisit (Holy Angels 11 Oct, St. John the Baptist Pawtucket 25 Oct, St. Thomas Warren 25 Oct, St. Patrick Providence 1 Nov, St. Rocco 8 Nov). City View Manor's open record gained its address (99 Goldsmith Ave., public housing).
- 2026-11-14: survey (providence-map-1/001-survey): rosters `gcatholic` (155) and `directory` (170) fetched; 17 batches planned in `batches.json`. No records yet.
