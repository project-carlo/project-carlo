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

From `probe url` of the finder's 129 distinct homepages and `visit.py --bulletin` on twelve
of the blocked ones (2026-11-14, `scratch/providence-map-1/001-survey/probe-all.tsv`):

- **eCatholic sites behind Cloudflare are common:** 32 homepages answered 403 to `probe
  url`; all seven opened with `visit.py` loaded and were eCatholic (e.g.
  `ecatholic:17050` olcsvp.org, `ecatholic:14522` saintjohnpaulri.com). Read issues with
  `issues.py ecatholic`. `ecatholic:5523` is the diocese's own site (bulletin inserts,
  documents): don't record it on a parish.
- **ParishesOnline (LPi), region 03:** linked on 16+ sites, often beside an eCatholic id
  (St. Lucy: `po-container:03/1380`; SS. Rose and Clement: `po-container:03/0323`; St.
  Mary of the Bay: `po-org:st-mary-of-the-bay-parish`). Read the masthead, not the org name.
- **John Patrick Publishing (jppc.net / church-bulletin.org):** linked on 15 or more sites
  (St. Ann Providence, St. Matthew Cranston, St. Bernard Wickford, St. Patrick Harrisville,
  St. Joseph Pascoag, St. Eugene...). See parish-site-access for the church-bulletin.org
  layout.
- **Discover Mass:** Holy Spirit, Central Falls's finder homepage is its Discover Mass page
  (`discovermass:holy-spirit-central-falls-ri`).
- 14 homepages were UNREACHABLE to `probe url` (stbren.com and ctkri.org also failed in the
  browser); 58 loaded with no publisher on the home page: use `visit.py --bulletin`.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- An eCatholic parish site whose Bulletins page only embeds ParishesOnline issues (no files at files.ecatholic.com/<id>/bulletins) publishes on ParishesOnline: record the po-org/lpi/po-container ids and not the eCatholic site id (seen at St. Joseph, Ashton).
- John Patrick Publishing bulletins: set website to the church-bulletin.org/<slug> page (jppc.net/onlinebulletins/<id>template.pdf redirects there), provider other with recipe page-pdfs. It needs no browser even when the parish's own site can't be reached.
- A John Patrick church-bulletin.org page can carry another parish's bulletin (St. Matthew Cranston's page is titled 'Saint Matthew @ Saint Paul Church' and posts St. Paul's LPi issue). Compare its masthead with the host parish's bulletin, and record the page as an extra publication id on the host's row, not as a row of its own.
- Duda parish sites (PDFs on irp.cdn-website.com/<site>/files/uploaded/, linked from a /bulletin page in newest-first order) read with provider other and recipe page-pdfs on the /bulletin page.
- Several LPi bulletins here (St. Joseph North Scituate, St. Michael Smithfield, St. Philip Greenville) are image-only apart from the ad pages: probe pdf sees only the footer, so read the masthead and Mass schedule with render.py.
- When an LPi footer gives a container but no org slug, try probe po with '<name>-<zip>' (st-michaels-church-02917 worked); an eCatholic site that hosts the same LPi file can then be recorded on parishes_online, with the ecatholic id as a second publication id, so fetch avoids Cloudflare.
- Squarespace parish bulletin pages (PDFs at <site>/s/Web-MMDDYY.pdf, newest first) work with provider other and recipe page-pdfs, but fetch:check can't date the file names (freshness 'unknown'): confirm the issue from the Mass intentions, since the page-1 date line can be a stale template (seen at Our Lady of Mercy, East Greenwich).
- Some ParishesOnline orgs have no LPi container and carry parish-uploaded PDFs (customer-data-prod-bucket.s3.amazonaws.com/organization-uploads/<lpi id>/publications/...); probe po lists them, but the parishes_online collector fails ('No matching anchor link'): record bulletin_provider unsupported with fetch_gap kind po-user-upload (seen at Sacred Heart, West Warwick).
- An eCatholic site that posts LPi issues in its documents folder (files.ecatholic.com/<id>/documents/YYYY/MM/<date>B.pdf) rather than /bulletins: its 'Bulletin archive' link (visit.py --links --match parishesonline) gives parishesonline.com/find/<slug>, and probe po <slug> without a zip suffix returns the org (saints-john-and-paul-church).
- When a site drops probe connections (RemoteDisconnected) but fetch:check downloads its PDFs, save the issue with tools/fetch_pdf.py and read it with render.py (probe pdf takes URLs only).
- ParishesOnline org slugs here can be possessive with no ZIP (st-marthas-church, st-brendans-church). Try these when '<name>-<zip>' fails. Two old orgs can share one container after a merger: record both orgs' ids on the one row.
- church-bulletin.org/<guessed slug> answers 200 even when no bulletin exists (a generic archive page or a page with no PDFs). Only a jppc id linked from the parish site, or a page listing dated PDFs, is evidence.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Finder entries that are notices (ids 34817, 25351, 33152, 29428) are not places and are excluded from planning; nothing is recorded for them. (accepted by survey-review, 002-survey-review, 2026-11-15)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-14: survey (providence-map-1/001-survey): rosters `gcatholic` (155) and `directory` (170) fetched; 17 batches planned in `batches.json`. No records yet.
