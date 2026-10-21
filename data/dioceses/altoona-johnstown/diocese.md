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
- **ParishesOnline** prints St. Patrick, Newry (container 14/0551). Empty orgs: Roaring
  Spring, Williamsburg and the four Altoona ones.
- **Small parishes with no bulletin anywhere** (St. Thomas More, Roaring Spring; St. Joseph,
  Williamsburg; Dudley; Shade Gap; all four of Fr. Wolfe's south Somerset parishes): `no_bulletin`
  rows with their Facebook pages noted (login wall in the sandbox). Discover Mass pages with an
  empty Bulletins tab and empty ParishesOnline orgs are common. Flocknote group pages
  (`<name>.flocknote.com`) are sign-up pages, not bulletins, and render their title in JS
  (evidence as a note). catholicindex.org and findglocal.com now challenge curl; a DuckDuckGo
  snippet via `visit.py` reads them.
- **Name look-alikes elsewhere:** church-bulletin.org "Saints Philip and James" is Exton;
  `parishbulletins.com/bulletins/065` is Guelph, Ontario. Check the town before using one.
- **The directory's address can be the rectory** (St. Gregory, MacDonaldton shows Sts. Philip
  and James's 247 High St, Meyersdale).
- **Web search in the sandbox:** `visit.py "https://duckduckgo.com/?q=..." --text` works;
  curl to DuckDuckGo or Bing returns nothing. `church-bulletin.org/<any-slug>` answers 200 with a
  generic page, so a 200 there proves nothing.
- **WebParish still live** for St. Thomas, Bedford: the CHURCH BULLETIN button goes to
  `webparish.com/aj/<name>/index.php?PG=upcomingevents`, which lists
  `webparish.com/pdfs/Bulletin-M-D-YYYY.pdf`; `page-pdfs` on that page reads it.
- **Weebly** (fultoncatholic.com) posts `/uploads/.../YYYY-MM-DD.pdf` and uploads late (the 18
  Oct issue was not up on 21 Oct): `newest-recent` is then expected, not a fault.
- **2MHost** (stjohneverettpa.org) uses `<base href>`; the fetch code honours it since batch 7.
- **`probe pdf` can't take a URL with spaces**: pass `%20`.
- **Nominatim** answers through the sandbox (`nominatim.openstreetmap.org/search?street=..&city=..
  &state=..&format=json`, with a user agent): use it to tell which of two GCatholic points is
  the building. Overpass resets the connection. GCatholic has duplicates here (Seven Dolors,
  Beans Cove is both 23816 and 148968).
- **webparish.com/aj/<name>/** is an old diocesan hosting scheme (St. Clare of Assisi,
  Johnstown; GCatholic's St. Mary, Hollidaysburg). Some of its pages are now stubs pointing
  to a parish's newer site, or dead stubs with nothing (Roaring Spring, Williamsburg): follow
  the pointer before treating it as the bulletin's home.
- **GoDaddy site builder** (PDFs on `img1.wsimg.com/blobby/...`; St. Mary & St. Michael,
  Hollidaysburg) resets the sandbox's connections intermittently: `probe url` may fail every
  time and `fetch:check` several times before passing. Rerun it; `curl` on the PDF blobs works.
- **eCatholic** is common here: St. Catherine, Duncansville (37641), Our Lady of Lourdes (29859),
  St. Therese (37141), St. Joseph, Bellwood (40290), St. Matthew, Tyrone (37833). Cloudflare
  403s curl and `recheck`; headed Chrome (`visit.py`) opens them, sometimes on the second try,
  and `issues.py ecatholic ecatholic:<id>` then reads the PDFs without a browser. Some date
  files by the Saturday (St. Therese: `20261017.pdf` is the 18 Oct issue; `--day sat`).
- **Wix image bulletins** (St. Anne, Davidsville): one JPEG per week on the Bulletin page,
  alt text `MMDDYYYY.jpg`; `page-images <page>` reads it (the date parser takes MMDDYYYY since
  batch 9). St. Peter, Somerset: PHP `bulletin.php` linking `site_docs/<n>.pdf`. New Baltimore:
  WordPress, posts about a week late.
- **Self-hosted, odd hosts:** SiteGround WordPress (mhtcc.org, Huntingdon) drops `probe pdf`
  and plain-http curl (RemoteDisconnected or an sgcaptcha page); use https with a Chrome user
  agent, or `visit.py --bulletin`. Homestead (scosmu.org, Mount Union) resets https; `http://www.`
  works, PDFs named `<Month>_<D>.pdf` on its About-Us page.
- **findglocal.com/US/<town>/<id>/<page>** mirrors a Facebook page's posts and Mass times
  without a login: useful evidence for `no_bulletin` parishes (Dudley).
- **College campus Masses** (Juniata College, Tussey Hall) appear in the directory's Mass
  times but in no bulletin: `open/` until someone confirms they are public.
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
