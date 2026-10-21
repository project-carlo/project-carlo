---
name: Roman Catholic Diocese of Altoona-Johnstown
state: PA
website: https://www.dioceseaj.org
status: exploring
gcatholic: alto0
---

Eight counties of west-central Pennsylvania: Blair (Altoona), Cambria (Johnstown, Ebensburg),
Bedford, Centre (State College), Clinton, Fulton, Huntingdon and Somerset. It borders Erie to
the north-west, Pittsburgh and Greensburg to the west, Harrisburg to the east, and Scranton
and Erie to the north. The diocese has no families or clusters: most parishes have one
church, and many share a pastor with one to three neighbours ("linked" parishes), which is
where shared bulletins are likely.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory:** `rosters/directory.json`, scraped 2026-10-21 from the nine pages of
  https://www.dioceseaj.org/parishes/ (WordPress `daj_parish` and `daj_church` posts; the REST
  API answers 401). 87 parishes and 93 churches; six parishes list two churches (Holy Spirit,
  Lock Haven; Our Lady of Mount Carmel, Altoona; Our Lady Queen of Angels, Central City;
  Prince of Peace, Northern Cambria; Queen of Archangels, Clarence; Sts. Gregory and
  Barnabas, Johnstown). A single-church parish's church post has no name or address, so the
  roster entry takes the parish's. Each entry has the directory's Mass times, pastor, phone and
  (for 55 parishes) a homepage. Pastors are the best lead for shared bulletins.
- **GCatholic:** `rosters/gcatholic.json` (key `alto0`), 109 entries with Plus Codes. 15 of
  them (ids 17xxx) are Byzantine or other Eastern Catholic churches in the territory
  (Eparchy of Passaic / Archeparchy of Pittsburgh): `other-jurisdiction`. GCatholic still lists
  churches the directory has dropped (St. Joseph, Carrolltown; St. Boniface, Hastings; St. John
  chapel, Central City; Our Lady of the Sacred Heart and St. Joseph, Portage; St. Mary,
  Meyersdale), each to be settled from a bulletin.
- **Clusters / families of parishes:** none. The diocese's site has no grouping or pastoral
  plan page (sitemaps checked 2026-10-21).
- **Mass times:** only in the directory entries above.
- **Closed parishes and where their records went:** no page found on dioceseaj.org
  (page and post sitemaps checked 2026-10-21).
- **Pastoral plan / closure announcements:** none found; the news posts (36 in the sitemap)
  mention no closures or mergers.

### Bulletin publishers here

Carried over from Harrisburg, Scranton and Allentown; correct it as this diocese shows
otherwise.

- **J.S. Paluch on Discover Mass** printed half of Harrisburg. Its `?s=` search is broken
  (PHP fatal error, 2026-10-21). Its sitemaps (`discovermass.com/wp-sitemap-posts-item-{1..11}.xml`)
  list every church page: grep the town there (slugs can be unguessable: St. Mary, Altoona is
  `st-mary-immaculate-conception-altoona-pa`). Probe on the bare host (200 = exists, 404 =
  not; `www.` 301s). A church page's "Visit Website" link often gives the homepage the
  directory lacks. Many pages here say "no bulletins available" (St. Joseph, Bellwood; St.
  Matthew, Tyrone; St. Therese): not live channels. One bulletin under a parish slug and a
  chapel slug (Mount Carmel and `our-lady-of-assumption-altoona-pa`) is one row with both ids.
- **Directory homepages are often dead or stale** (sttheresealtoona.com dead DNS,
  stmatthewtyrone.org SSL failure; the live sites are sainttheresealtoona.org and
  stmatthewtyrone.com). Directory Mass times lag too (Tyrone 10:00 vs bulletin 10:30). A page can exist
  with "no bulletins available" (St. Mark and Holy Rosary, Altoona): not a live channel. St.
  Gregory, MacDonaldton's directory homepage is a Discover Mass page. One joint bulletin can appear under several
  church slugs: record every slug. Discover Mass caps downloads per IP per day (a 134-byte
  "Maximum number of files downloaded today" reply, which `fetch:check` reports as
  `not_pdf`); its text layer is often garbled, and quotes keep the garble. Cite the church
  page, not a tokenised download link.
- **eCatholic** sites sit behind Cloudflare: `https://www.<domain>/bulletins` usually opens in
  headed Chrome (parish-site-access) when the homepage is challenged.
- **LPi / ParishesOnline:** many parishes keep empty organizations, which are not fold-ins
  (all four Altoona ones checked are empty). The search API
  (`https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=..&longitude=..&distance=3`)
  lists organizations near a point.
- **Wix** (St. Mary, Altoona's "The Marian"): the PDF name on `filesusr.com` changes weekly;
  `page-pdfs` on the site reads it.
- **Bon Venture** (`sponsors.bonventure.net/?page=<id>`, PDFs at `pdfs/<id>/<YYYY-MM-DD>.pdf`):
  broken https chain, use `http://`. **John Patrick Publishing** (`church-bulletin.org/<id>`):
  a listing with no PDFs is not a live channel. **FATA Online** (`fataonline.com/bulletins/
  <code>`): fixed "View Current Bulletin" link plus dated archive.
- **webparish.com/aj/<name>/** is an old diocesan hosting scheme (St. Clare of Assisi,
  Johnstown; GCatholic's St. Mary, Hollidaysburg). Some of its pages are now stubs pointing
  to a parish's newer site: follow the pointer before treating it as the bulletin's home.
- **GoDaddy site builder** (PDFs on `img1.wsimg.com/blobby/...`; St. Mary & St. Michael,
  Hollidaysburg) resets the sandbox's connections intermittently: `probe url` may fail every
  time and `fetch:check` several times before passing. Rerun it; `curl` on the PDF blobs works.
- **eCatholic** is common here: St. Catherine, Duncansville (37641), Our Lady of Lourdes (29859),
  St. Therese (37141), St. Joseph, Bellwood (40290), St. Matthew, Tyrone (37833). Cloudflare
  403s curl and `recheck`; headed Chrome (`visit.py`) opens them, sometimes on the second try,
  and `issues.py ecatholic ecatholic:<id>` then reads the PDFs without a browser. Some date
  files by the Saturday (St. Therese: `20261017.pdf` is the 18 Oct issue; `--day sat`).
- **Image-only bulletins** are common in the region (St. John, Lakemont's WordPress scans).
  `pdftoppm -r 100 -f 1 -l 1 -png` renders a page to read; the evidence is then a note, not a
  quote, and says so.
- **The directory's street addresses can be wrong**: St. John, Lakemont is 344 Baynton Ave in
  the directory but 309 Lotz Ave in its bulletin, its site and GCatholic. Check against a
  second source before verifying.
- **Self-hosted `page-pdfs` sites:** the cathedral (dated PDFs at altoonacathedral.org/bulletin/),
  Sacred Heart (one fixed `/bulletin/bulletin.pdf` overwritten weekly: check the issue date).
- **Both cathedrals may be missing from the GCatholic roster**: GCatholic links the Altoona
  cathedral at `gcatholic.org/churches/northamerica/2439`, outside the list the roster reads.
  Cite that page directly.
- `tools/fill_record.py` fills evidence and body into a new record (see the tools README).
- `pnpm diocese search` does not search rosters: an empty result says nothing about them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.
