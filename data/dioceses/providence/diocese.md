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

- **eCatholic, usually behind Cloudflare:** a homepage that answers 403 to `probe url` is
  most often eCatholic (`ecatholic:<id>`); it loads in `visit.py`. Read issues with
  `issues.py ecatholic`. `ecatholic:5523` is the diocese's own site (bulletin inserts,
  documents): never record it on a parish. Many eCatholic sites only repost LPi:
  - Bulletins page embeds ParishesOnline issues, with no files at
    `files.ecatholic.com/<id>/bulletins`: the parish publishes on ParishesOnline; record the
    po-org/lpi/po-container ids, not the eCatholic id.
  - LPi files in the documents folder (`files.ecatholic.com/<id>/documents/YYYY/MM/<date>B.pdf`):
    its "Bulletin archive" link (`visit.py --links --match parishesonline`) gives
    `parishesonline.com/find/<slug>`; `probe po <slug>` finds the org.
  - Once the LPi org is found, record the row on `parishes_online`, with the eCatholic id
    as a second publication id, so fetch avoids Cloudflare.
- **ParishesOnline (LPi), region 03:** linked on 16+ sites, often beside an eCatholic id.
  Read the masthead, not the org name or footer: a footer's account name (e.g. 'St. Clare
  St Vincent de Paul') can name a church the masthead has dropped.
  - Finding the org when the footer gives only a container, or the parish site is dead:
    `probe po` with `<name>-<zip>` (`st-michaels-church-02917`), `<name>-church-<zip>`
    (`christ-the-king-church-02881`), or a possessive slug with no ZIP
    (`st-marthas-church`). Check the org lists issues; some list none.
  - One bulletin can sit in two containers with different ad pages and footers, and two
    pre-merger orgs can share one container: compare rendered pages 1-2, then record every
    container and org id on the one row.
  - Many issues here are image-only apart from the ad pages, or have an encoded-font text
    layer (`probe pdf` calls every page readable but returns glyph codes like `/0/1 /2/3`
    and `--grep` finds nothing). Read the masthead and Mass schedule with `render.py`.
  - Orgs with no LPi container that carry parish-uploaded PDFs
    (`customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/<lpi id>/publications/...`):
    `probe po` lists them but the `parishes_online` collector fails ("No matching anchor
    link"). Record `bulletin_provider: unsupported`, fetch_gap kind `po-user-upload`.
- **John Patrick Publishing (jppc.net / church-bulletin.org):** linked on 15+ sites. Set
  website to the `church-bulletin.org/<slug>` page (`jppc.net/onlinebulletins/<id>template.pdf`
  redirects there), provider `other`, recipe `page-pdfs`; no browser needed even when the
  parish's own site can't be reached. Traps:
  - A guessed `church-bulletin.org/<slug>` answers 200 even with no bulletin (a generic
    archive page, or one with no PDFs). Only a jppc id linked from the parish site, or a
    page listing dated PDFs, is evidence.
  - A page can carry another parish's bulletin (St. Matthew Cranston's posts St. Paul's
    LPi issue). Compare its masthead with the host parish's bulletin and record the page as
    an extra publication id on the host's row, not as a row of its own.
- **Duda sites** (PDFs on `irp.cdn-website.com/<site>/files/uploaded/`, linked newest
  first from a `/bulletin` page): provider `other`, recipe `page-pdfs` on the `/bulletin`
  page.
- **Squarespace sites** (PDFs at `<site>/s/Web-MMDDYY.pdf`, newest first): provider
  `other`, recipe `page-pdfs`. `fetch:check` can't date the file names (freshness
  `unknown`), and the page-1 date line can be a stale template: confirm the issue from
  the Mass intentions.
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

- visit.py can hang past its timeout on Google Sites parish pages (sites.google-built, 'Embedded Files'); read them with probe get and check the data-code embeds for a Drive or bulletin link instead.
- When the finder's homepage is a masstimes.org map link, the parish's email domain (e.g. name@<domain>.org) or a DuckDuckGo html search (probe get https://html.duckduckgo.com/html/?q=...) can find its real site.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Finder entries that are notices (ids 34817, 25351, 33152, 29428) are not places and are excluded from planning; nothing is recorded for them. (accepted by survey-review, 002-survey-review, 2026-11-15)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-14: survey (providence-map-1/001-survey): rosters `gcatholic` (155) and `directory` (170) fetched; 17 batches planned in `batches.json`. No records yet.
