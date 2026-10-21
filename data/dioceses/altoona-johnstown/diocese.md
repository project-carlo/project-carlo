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
- **Clergy list:** https://www.dioceseaj.org/clergy/ lists every priest with his parishes:
  the quickest way to settle which parishes share a pastor. The `/daj_parish/<slug>/` pages are
  JS-rendered and carry no pastor text; `/bishops-appointments-2/` 403s after many requests.
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
  directory lacks. A joint bulletin may sit under only one of its churches' slugs (Our Lady
  Queen of Angels, Central City carries the issue for Holy Family, Hooversville and All Saints,
  Boswell, whose own pages are empty): a no-homepage parish can be a worship site of a
  neighbour's row, so read the neighbours' mastheads before calling it `no_bulletin`. Many pages here say "no bulletins available" (St. Joseph, Bellwood; St.
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
- **ParishesOnline** prints St. Patrick, Newry (14/0551), St. Clement, Johnstown (14/1971, image
  pages) and St. John Vianney/Transfiguration (14/1788). tesseract is not installed: render pages
  with `pdftoppm` and read them.
- **`dated-post <bulletin page>`** reads a site with one child page per issue (St. Francis of
  Assisi, Johnstown, /bulletin-3/; unpinned `page-pdfs` picked a 2021 PDF). Empty orgs: Roaring
  Spring, Williamsburg and the four Altoona ones.
- **Small parishes with no bulletin anywhere** (St. Thomas More, Roaring Spring; St. Joseph,
  Williamsburg; Dudley; Shade Gap; all four of Fr. Wolfe's south Somerset parishes): `no_bulletin`
  rows with their Facebook pages noted (login wall in the sandbox). Discover Mass pages with an
  empty Bulletins tab and empty ParishesOnline orgs are common. Flocknote group pages
  (`<name>.flocknote.com`) are sign-up pages, not bulletins, and render their title in JS
  (evidence as a note). catholicindex.org and findglocal.com now challenge curl; a DuckDuckGo
  snippet via `visit.py` reads them.
- **Evidence for a `no_bulletin` church being open**: obituary snippets ("funeral Mass at
  <church>", via `tools/ddg.sh "<query>"`), alongside the directory and Discover Mass times.
  Discover Mass pages 503 and then Wordfence-block even headed Chrome after repeated hits:
  read each once.
- **Name look-alikes elsewhere:** church-bulletin.org "Saints Philip and James" is Exton;
  `parishbulletins.com/bulletins/065` is Guelph, Ontario. Check the town before using one.
- **The directory's address can be the rectory** (St. Gregory, MacDonaldton shows Sts. Philip
  and James's 247 High St, Meyersdale).
- **Web search in the sandbox:** `visit.py "https://duckduckgo.com/?q=..." --text` works;
  curl to DuckDuckGo or Bing returns nothing. `church-bulletin.org/<any-slug>` answers 200 with a
  generic page, so a 200 there proves nothing.
- **WebParish is live for several parishes** (St. Thomas, Bedford; St. Anthony and St. Elizabeth
  Ann Seton, Windber, `PDFs MMDDYY.pdf` and `SEAS<YYYY-MM-DD>Bulletin.pdf`). A parish's own
  domain can redirect to its WebParish site (stelizabethannsetonwindber.com). For a parish with
  no directory homepage, a DuckDuckGo search (`uv run python visit.py "https://duckduckgo.com/?q=..."`)
  finds these. Sister parishes with one pastor can each post a bulletin listing the same
  combined Mass rota (Windber): two rows while both channels are live.
- For St. Thomas, Bedford: the CHURCH BULLETIN button goes to
  `webparish.com/aj/<name>/index.php?PG=upcomingevents`, which lists
  `webparish.com/pdfs/Bulletin-M-D-YYYY.pdf`; `page-pdfs` on that page reads it.
- **Weebly** (fultoncatholic.com) posts `/uploads/.../YYYY-MM-DD.pdf` and uploads late (the 18
  Oct issue was not up on 21 Oct): `newest-recent` is then expected, not a fault.
- **2MHost** (stjohneverettpa.org) uses `<base href>`; the fetch code honours it since batch 7.
- **`probe pdf` can't take a URL with spaces**: pass `%20`.
- **Two homepages, one bulletin:** the two Cresson parishes' separate Weebly sites both point at
  one ParishesOnline org (14/1078). Follow each site's "Weekly Bulletin" link before making two rows.
- **Word bulletins** (St. Michael, Saint Michael: Weebly `/uploads/.../MM-DD-YYYY_webbulletin.docx`):
  the pipeline has no `.docx` reader, so `fetch:check` fails at download; `no_bulletin` with the
  URL pattern recorded. Franciscan-staffed parishes here (OFM Conv., TOR) often post image-only
  or Word bulletins.
- `tools/fill_record.py` appends evidence after the last evidence line even when a key such as
  `parish:` follows the list (as `new excluded --parish` writes it): move `parish:` above
  `evidence:` first.
- **Campus and shrine Masses** (Mount Aloysius College; Saint Francis University's chapel; the
  Loretto shrine's summer Sunday Mass) go to `open/` until a source says they are public.
- **One pastor, one bulletin is common in Cambria**: Fr. Nale's stjic.org bulletin carries all
  four of his parishes (Summerhill, New Germany, South Fork, Wilmore), whose own Discover Mass
  pages are empty. Directory Mass times lag the bulletin there by up to two hours.
- **Nominatim** `q=<church name>+<town>` finds church nodes where `street=` fails.
- **Nominatim** answers through the sandbox (`nominatim.openstreetmap.org/search?street=..&city=..
  &state=..&format=json`, with a user agent): use it to tell which of two GCatholic points is
  the building. Overpass resets the connection. GCatholic has duplicates here (Seven Dolors,
  Beans Cove is both 23816 and 148968).
- **webparish.com/aj/<name>/** answers 406 (Mod_Security) to curl; headed Chrome needs the
  explicit `/index.php`. It is an old diocesan hosting scheme (St. Clare of Assisi,
  Johnstown; GCatholic's St. Mary, Hollidaysburg). Some of its pages are now stubs pointing
  to a parish's newer site, or dead stubs with nothing (Roaring Spring, Williamsburg): follow
  the pointer before treating it as the bulletin's home.
- **A page that links a Word calendar before its PDFs** (saintbenedictschurch.com, Carrolltown)
  makes `page-pdfs` pick the `.docx` (`not_pdf`); use the Discover Mass copy. That GoDaddy site
  fails https (certificate) and works over `http://www.`. An eCatholic homepage can point its
  Bulletins menu at Discover Mass (Nicktown): read its links with `visit.py --links`.
- **Discover Mass's daily cap** blocks raw curl before the pipeline's own fetch
  (`tools/browser_get.py`) is refused: use that to read a cover. `recheck` gets 503s there.
- **GCatholic-only entries can be open missions**: St. Joseph Mission, Carrolltown (Mass a few
  times a year, own site sjmc1830.com) is in no directory. Absence from the directory settles
  nothing.
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
- **Partner bulletins:** in Johnstown both no-homepage parishes in batch 12 (St. Patrick; St.
  Michael) are carried in their pastor's other parish's bulletin. Read the partner's cover
  first. A parish domain redirecting to the partner's site (stpatrickjtown.com → the
  cathedral; `probe url` says REDIRECT-OFFSITE) is a fold-in, not a squat.
- **Duda** (the Johnstown cathedral, `irp.cdn-website.com`) resets curl intermittently; retry.
  Its `/welcome#WeeklyBulletin` lists `files/uploaded/YYYY-MM-DD.pdf` (not always zero-padded).
  omostoday.com (WordPress/Elementor) posts scanned issues: render with `pdftoppm`.
- **Two parishes on one site** (St. Therese and St. Anne, sttheresejohnstown.com, one PDF each
  per week): recipes can't filter by file name, so each row points at a different page whose
  list puts its own PDF first (homepage vs `/bulletins/`), with `#fragment` publication ids to
  keep them distinct. Fragile: re-check both picks if the site reorders.
- **WordPress PDF Embedder** (Visitation BVM, Johnstown, found by DuckDuckGo) turns PDF links
  into canvases; `page-pdfs <site>/category/<cat>/feed/` reads the RSS feed instead.
- **Third-party Mass-time aggregators** (catholicmasstime.org, catholicchurch.directory)
  disagree with each other and the directory: never a second source.
- **An eCatholic id on a site doesn't mean the bulletin is there**: standrewjohnstown.org is
  eCatholic (36351) but its bulletin folder is empty and its Bulletins menu goes to Discover Mass.
- **Self-hosted, odd hosts:** SiteGround WordPress (mhtcc.org, Huntingdon; stbenedictchurch.org,
  Johnstown; `tools/browser_get.py <page> <pdf> <out>` downloads a PDF through Chrome) drops `probe pdf`
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
