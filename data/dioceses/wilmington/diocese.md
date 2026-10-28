---
name: Roman Catholic Diocese of Wilmington
state: DE
website: https://cdow.org
status: exploring
gcatholic: wilm0
city_aliases:
  St Michaels: St. Michaels
  Kent Island: Chester
  Ocean Pines: Berlin
  Oak Orchard: Millsboro
  Golden Hill: Church Creek
---

All of Delaware (New Castle, Kent and Sussex counties: Wilmington, Newark, New Castle,
Middletown, Dover, Milford, Georgetown, Seaford and the beaches at Lewes, Rehoboth and Bethany)
and the nine counties of Maryland's Eastern Shore (Cecil, Kent, Queen Anne's, Talbot,
Caroline, Dorchester, Wicomico, Somerset and Worcester: Elkton, Chestertown, Easton,
Cambridge, Salisbury, Ocean City). Neighbours: Philadelphia across the Pennsylvania line,
Harrisburg (Lancaster County borders Cecil County), Baltimore across the Susquehanna and the
Bay, Camden across the Delaware, and Richmond on Virginia's Eastern Shore; of these only
Harrisburg is mapped. The state here is `DE`, but 34 of the directory's 79 entries are in
Maryland.

The diocese has **no families, clusters or pastorates**. Its 56 parishes (cdow.org/deaneries,
modified 2026-05-26) sit in six deaneries (City, Brandywine Hundred, New Castle, Iron Hill,
Central, Ocean); since Easter 2026 the "United in Christ" plan works through the deaneries on
shared programmes and Mass schedules, not mergers. Shared bulletins are likely in three
places: a parish with **missions** (most Eastern Shore parishes, and St. Joseph, Middletown;
the summer guide names each "mission of ..."); parishes the diocese names together
("Saint Michael the Archangel/Mary Mother of Peace", "St. Mary & Holy Savior Parish", "St
Francis de Sales & Holy Redeemer parish"; the three **Downtown Catholic** parishes in
Wilmington, "individual parishes administered by the one pastoral team"); and a few pairs
under **one pastor** named in the clergy appointments (below). `batches.json` keeps each of
these in one batch.

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.

- **Parish directory (the `directory` roster):** cdow.org's "Find A Parish" map,
  https://cdow.org/find-a-parish/, a WordPress "dpi_gis" plugin page that carries every
  entry in the HTML as `<li data-module="parishes" data-name data-address data-latitude
  data-website data-mass-times ...>` (no API call; plain curl with a browser user agent).
  Scraped 2026-10-27 by `scratch/wilmington-map-1/tools/cdow_finder.py`: 79 entries (the page
  also holds 33 schools and 4 jobs, skipped). It lists **churches**, not parishes: missions
  are entries of their own with the parent's website, and some names carry the parish
  ("Holy Savior. St. Mary & Holy Savior Parish"). Good for building pins (all within about
  0.2 km of GCatholic's except the three noted below), Mass times (`mass_times`, decoded
  from the map; Sunday = day 0), and the current parish website. Quirks: St. Francis de
  Sales, Salisbury is in twice (`directory:184`, 413 Wicomico St, no Masses; `directory:175`,
  535 Riverside Dr); the map's own deanery ids are all 0, so `deanery` is joined from the
  deaneries page by name and town. Some websites are wrong: Holy Cross, Dover's is a spam
  page (sub.ireland724.info); Middletown's, St. Mary of the Immaculate Conception's and
  Cambridge's are catholicmasses.org listings, Berlin's a catholicindex.org listing, St. Jude,
  North East's a county churches page, and Corpus Christi's is St. Matthew's site. The
  cathedral, Dover AFB and the two Ukrainian churches are listed; Christ Our King, Our Lady
  of the Highways and St. Joseph's former Middletown church are not.
- **Deaneries:** https://cdow.org/deaneries/ (modified 2026-05-26) names 56 parishes, one
  line each ("Saint Michael the Archangel/Mary Mother of Peace, Georgetown, DE"), in six
  deaneries; this is the diocese's own parish count. All 56 match a directory entry; the 23
  directory entries it doesn't name are missions, the two Ukrainian churches and Dover AFB.
  **Disagreement:** Bishop Koenig's "United in Christ" update (The Dialog, 2026-03-26,
  https://thedialog.org/featured/bishop-koenigs-united-in-christ-update-going-beyond-pre-established-boundaries-experimenting-with-joint-pastoral-initiatives/)
  announces the six-deanery realignment "effective Easter Sunday, April 5, 2026" and lists
  the City Deanery as eight parishes, **without St. Mary of the Immaculate Conception and
  St. Patrick**, which the later deaneries page still lists. Nothing found yet says either
  was merged or suppressed; the downtown batch checks.
- **GCatholic:** `rosters/gcatholic.json` (key `wilm0`), 80 entries with Plus Codes for 77.
  Omits the cathedral; keeps Christ Our King, Wilmington (closed November 2016, now a funeral
  home: The Dialog, 2020-07-30), St. Joseph's former church at 15 W Cochran St., Middletown
  (typed "Former Church") and Our Lady of the Highways, Childs (a shrine). Marks St. Nicholas,
  Wilmington and St. Basil the Great, Chesapeake City "Ukrainian"; lists Our Lady of Perpetual
  Help, Dover AFB as a "Community". **Three Plus Codes are rotated:** its Corpus Christi
  (19322) is on Holy Child, Naamans Rd; its Holy Family (19323) on Corpus Christi, Elsmere;
  its Holy Child (19321) on Holy Family, Newark. Use the directory pin or OSM for these, and
  check Our Lady of Guadalupe, Frankford, whose two pins are about 24 km apart. Many of its
  websites are old domains: of the 73 entries with one, probed 2026-10-27, 42 answered; six
  domains have no DNS (holycrossnet.org, stjohn-stbernadette.org, stmaryscambridge.org,
  stpetertheapostlede.org, immaculateconceptionmarydel.com, mosstp.org); stannsbethany.org,
  stmaryoftheassumption.com, stmarys-holysavior.com, iccparish.org and smspwilmington.com
  didn't answer, the last redirecting to a web-design firm on a first try;
  ccparishwilmington.org is a parked "/lander"; stjudeslewesde.org redirects to an unrelated
  site. Prefer the directory's websites. GCatholic's town names match the directory's except
  Corpus Christi (GCatholic and the deaneries page: Elsmere; directory: Wilmington); the
  deaneries page also puts St. Joseph on the Brandywine in Wilmington, the others in
  Greenville.
- **Mass times (the `summer-guide` roster):** "Summer Vacation Mass Guide",
  https://cdow.org/find-a-parish/summer-vacation-mass-guide/ ("Mass time information is up
  to date as of May 12, 2026"), the coastal and Eastern Shore churches only: 32 churches
  plus two summer-only Mass sites of St. Edmond, Rehoboth (its Parish Hall, and Rehoboth
  Elementary School), 34 entries. The best source here for **which parish a mission belongs
  to**: "St. Rose of Lima (mission of St. Joseph, Middletown, DE)", "St. Andrew (seasonal
  mission of St. Luke – open May 23 – Sept. 6)", "St. Mary Star of the Sea (the Tubman
  Chapel) (mission of St. Mary Refuge of Sinners, Cambridge)"; `group` holds that parent.
  It also says St. Peter, Queenstown was "Reopening July 4, 2026 following renovation".
  Weekend times are summer's. Parsed by `scratch/wilmington-map-1/tools/summer_guide.py`.
  The finder's `mass_times` are the only year-round diocesan Mass times; there is no other
  Mass-times list.
- **Clusters / families of parishes:** none. **Shared pastors** come from the clergy
  appointments The Dialog publishes (search titles with
  `thedialog.org/wp-json/wp/v2/posts?search=appointments&search_columns=post_title`; read
  with `tools/dialog_post.py`). Explicit current pairs: St. Ann and St. Thomas the Apostle,
  Wilmington ("Pastor both of St. Ann, Wilmington and of St. Thomas the Apostle",
  2026-04-27); Holy Child and St. Helena (pastor from 14 January 2026, 2025-12-01); St. John
  the Beloved and St. Catherine of Siena (pastor from 3 September 2025, 2025-08-14);
  Immaculate Conception, Elkton and St. Thomas More Oratory ("Pastor of both", 2024-05-19);
  St. Polycarp, Smyrna and St. Dennis, Galena (2024-05-19). Shared associates: St. Matthew
  and Corpus Christi (December 2025), Holy Cross, Dover and Immaculate Conception, Marydel
  (2024–2025), Holy Family and Resurrection (June 2024). Ended: St. Thomas's pastor
  administered St. Mary Magdalen (October 2025 – April 2026); St. Benedict's administered St.
  Christopher (November 2025 – April 2026); St. Joseph on the Brandywine's administered St.
  Ann (from July 2025). The appointments say who serves where, never what a bulletin covers.
- **Closed parishes and where their records went:** no diocesan list found
  (cdow.org has a "Marriages and Baptisms Archives" page of news, not a records index).
  Closures are dated from The Dialog (thedialog.org, WordPress, readable with curl and its
  REST API; its `search` matches loosely, so add `search_columns=post_title`).
- **Pastoral plan:** "United in Christ" (pastoral letter 2023-05-19; updates 2024-05-22,
  2024-08-01, 2026-03-26), deanery-level collaboration; the Brandywine Hundred dean wrote
  that "it is not about closure – but about vibrancy" (2024-01-08). Its 2026 phase is "a
  diocesan-deanery coordination of Mass schedules", decisions to follow, so expect Mass
  times to change during 2026–27. Nothing in it closes or merges a parish.
- **Other jurisdictions in the territory:** St. Nicholas, Wilmington and St. Basil the Great,
  Chesapeake City (Ukrainian Catholic); Our Lady of Perpetual Help, the Dover Air Force Base
  chapel (436th Airlift Wing chaplaincy). All three are in the directory.

### Bulletin publishers here

From `probe url` on every roster website and the browser on 38 of them (2026-10-27); each
batch settles its own rows.

- **John Patrick Publishing** prints a good share of New Castle County and the upper shore:
  parish sites link `jppc.net/onlinebulletins/<id>template.pdf`, which redirects to a
  `church-bulletin.org/<slug>` listing of dated PDFs (Downtown Catholic 309, St. Joseph,
  Middletown 319, St. Polycarp 301, St. Margaret of Scotland 306; listings for St. Helena,
  Our Lady of Fatima 304 and St. Dennis 732; St. Mary Magdalen's too; St. Hedwig 317, whose
  home page links `church-bulletin.org/?id=317`, which redirects the same way). Record it as
  `page-pdfs https://www.church-bulletin.org/<slug>`, as Harrisburg and Allentown do. To
  find which parish a number is, `curl -L` the template URL and read the slug it lands on
  (Delaware's are 300-320 and 732); never guess a slug, since a wrong one returns the generic
  home page with HTTP 200. A listing can outlive its parish (313, Christ Our King, lists no
  PDFs). A parish site's link to the template is often only an href on a "Bulletin" button:
  quote visible text (the listing's title, the cover) as evidence, not the href.
  church-bulletin.org answers 406 to a bare "Mozilla/5.0" user agent; plain curl (the
  survey) and a full Chrome-style agent (map 003) worked, but in maps 004 and 012 the
  sandbox refused curl with a spoofed agent, here and on other sites, so use plain curl,
  `probe pdf` or `visit.py`. When the parish site itself answers 403 or 500 to curl, or
  doesn't connect at all (saintpolycarp.org, stdennischurch.org on 2026-10-27), the
  jppc.net template redirect still gives the listing. Pin the listing even when the parish
  site has its own bulletin page: that page can be a week behind (St. Joseph, Middletown).
  Many covers are scanned images (St. Mary Magdalen's whole file; page 1 of St. Margaret's,
  Holy Family's, Resurrection's and St. Joseph, Middletown's): `probe pdf` finds no text
  there, so render page 1 with parish-site-access `render.py` to read the masthead;
  `fetch:check` still passes. A rendered cover can list each church with its times and a
  status line ("The Church is currently closed for repairs", St. Francis Xavier Shrine),
  which is the current-Mass evidence for a mission or shrine. Some
  eCatholic sites (Resurrection) link their bulletin to the church-bulletin.org listing and
  host no eCatholic files: see that bullet.
- **LPi / ParishesOnline** prints most of the Ocean Deanery (containers `04/xxxx`: St.
  Edmond 04/0887, St. Luke 04/0763, St. Mary & Holy Savior 04/0790, St. Mary, Cambridge
  04/0661, St. Michael/Mary Mother of Peace 04/0868; St. Jude, Lewes and St. Francis de
  Sales, Salisbury are 03/1013 and 03/1207), the mid-shore and
  Kent (Our Mother of Sorrows/St. Peter 04/0487, Sts. Peter and Paul, Easton 04/0450, St.
  John/St. Bernadette, Milford 04/0120) and several in the north (Holy Child, IHM, St. John
  the Beloved, St. Catherine of Siena, Holy Spirit/St. Peter, St. Matthew/Corpus Christi,
  St. Joseph on the Brandywine). Parish sites on other platforms hide the link: a Wix
  site's Bulletin button goes to `parishesonline.com/find/<slug>` while the home page's only
  PDF links are one-page inserts (stjohnsmilford.com); an eCatholic site can host no
  bulletins and link ParishesOnline (sorrowsparish.org, 11311: record the po ids, not the
  eCatholic id); a Duda or WeConnect (LPi's own platform) bulletins page can embed
  `publicationWidget?id=<lpi id>`, and `probe po` resolves the id to the container.
  `probe url` reports it as `lpi:<id>` on some sites (St. Mary, Cambridge; smammop.com;
  visitstfrancis.org) but not others, where the widget is only in the page source
  (stedmond.org/bulletins, stjudelewes.org): grep the HTML for `publicationWidget?id=`, and
  quote the bulletin rather than the href, which recheck can't find. Such sites' menu links
  can carry a hash suffix (smammop.com/mass-schedulef0423bfb,
  stjudelewes.org/bulletin<hash>): use `visit.py --follow` and read `final_url` rather than
  guessing the path. The directory's website can be a sister institution's with no bulletin link
  (Easton's ssppeaston.org is the parish-and-schools site): look at the parish's other
  directory entries for its own site (ssppeastonmd.org). One container can have an
  organization account for each church (St. John, Milford 19963 and St. Bernadette,
  Harrington 19952 both serve 04/0120): record every po-org id on the one row.
  ParishesOnline org names that join two parishes
  (`holy-spirit-st-peter-the-apostle`, `st-matthew-parish-and-corpus-christi`,
  `our-mother-of-sorrows-st-peter-the-apostle`, `st-michael-mary-mother-of-peace-parish`)
  are leads, not proof: read the masthead.
  A cover can print a "United in Christ" deanery Mass-time box naming several parishes
  (Immaculate Heart of Mary's lists six): that is a deanery schedule, not a shared masthead,
  so take the parish and staff from page 2 or later. Covers are often image-only, with text
  only on the ad pages at the end (St. John the Beloved 03/1288, St. Catherine 03/1410; no
  text on pages 1-5 of Our Mother of Sorrows 04/0487, 1-6 of St. Edmond 04/0887, 1-9 of St.
  Francis de Sales 03/1207): render page 1 with `render.py` for the masthead, and quote the
  LPi footer ('Parish, City, DE 03-NNNN' or 'Parish | 04-NNNN') as the text that names the
  container. For each church's current Mass times, render the Mass-schedule box on the
  cover or the Mass-intentions page (page 3 of St. Michael/Mary Mother of Peace's, one
  column per church); summer issues add the seasonal sites to the box (St. Edmond).
  `probe pdf --grep` returns pages 1-3 whether or not they match, so find a notice's page
  with `--pages N`. Issues go up before their weekend, so
  `fetch:check` freshness `future` (St. Catherine's 20261101 on 2026-10-27) is not a wrong
  pick. Don't take coordinates from a ParishesOnline org's own pin (St. Catherine's is about
  3 km off).
- **eCatholic:** about 14 sites (Resurrection, St. Margaret, Seton, St. Mary of the
  Assumption, St. Mary Magdalen, St. Ann, St. Elizabeth, St. Paul, St. Joseph on the
  Brandywine, Good Shepherd, Sacred Heart, St. Christopher, beparish.com, Our Mother of
  Sorrows). Unlike Harrisburg's, most answered plain `probe url` here, but sites behind
  Cloudflare answer 403 to curl and `probe url` (resurrectionde.org, setonparish.net,
  stjosephmiddletown.com, goodshepherdcecilmd.org's inner pages) and load in the browser,
  where `visit.py` reads /mass-times and /church-addresses. `issues.py ecatholic` reads the files without one.
  A home page's first PDF link can be a Mass insert (`files.ecatholic.com/<id>/documents/...`,
  beparish.com's Holy Week schedule), not the bulletin: the weekly issues are
  `/<id>/bulletins/YYYYMMDD.pdf` on the /bulletins page. Some of these sites host no bulletins on eCatholic and link another publisher instead:
  the John Patrick listing (Resurrection: site 5398's files answer 403 for every Sunday) or
  FATA Online (Good Shepherd, 17337), or ParishesOnline (see that bullet). Pin that listing with `page-pdfs` and leave the
  eCatholic id out of `publication`. Issues go up before their Sunday, so `fetch:check` freshness `future` (St.
  Mary of the Assumption, 20261101 on 2026-10-27) is not a wrong pick.
  A parish in both this list and LPi's can serve one issue on both (St. Joseph on the
  Brandywine: eCatholic 30639 and container 03/4127): compare the issues and record both
  ids on one row. A file can also carry a sister parish's pages (St. Ann's 38453 holds St.
  Thomas's): read page 1. A site's /bulletins list can stop months early (St. Paul,
  Wilmington: last file 2 August 2026; Sacred Heart, Chestertown's stops at 27 September):
  before calling it stale, check the home page's bulletin link for another publisher; it can
  be only an image link on the /bulletin page (Sacred Heart's goes to Bonventure). When a parish domain fails TLS in curl and Chrome
  (ERR_CERT_COMMON_NAME_INVALID), its Wayback copy (`archive.org/wayback/available?url=...`)
  still shows the eCatholic id, and the bulletin's letterhead can name the working domain
  (St. Joseph, Wilmington: stjosephfrenchst.org fails, sjfschurch.org is the same site 14048).
- **J.S. Paluch on Discover Mass:** St. Ann, Bethany Beach (`discovermass:st-ann-bethany-beach-de`)
  and Holy Cross, Dover (`holy-cross-dover-de`), whose listing serves the same issue as
  the parish's own copy (12 pages against 10, the text oddly spaced): when the parish site
  carries the issue, pin the copy plain curl reads and keep the listing in `publication`
  only. Discover Mass caps downloads per
  IP per day (a 134-byte "Maximum number of files downloaded today" reply, which
  `fetch:check` reports as `not_pdf`): that is the cap, not the row.
- **Bonventure** (OSV/Duda parish sites, e.g. hrparish.com, Holy Rosary, Claymont; St.
  John-Holy Angels, 2103; Sacred Heart, Chestertown, 2169, linked from an eCatholic site;
  Our Lady of Lourdes, Seaford, 2167, from a GoDaddy site whose bulletin page is a stub with
  one "CLICK HERE" button): `probe url` misses the bulletin link, and a site can answer 403
  to curl (St. John-Holy Angels); `visit.py --text --links` in the browser shows "Bulletin"
  going to `sponsors.bonventure.net/?page=<n>`, and the PDF's page 1 names the parish
  (it has a text layer). Issues are at
  `/pdfs/<n>/<YYYY-MM-DD>.pdf`. The
  https host fails TLS verification from Python (`probe pdf`, `recheck`) but loads in
  Chrome: use the `http://` form in recipes and evidence (`page-pdfs
  http://sponsors.bonventure.net/?page=<n>`), and `tools/browser_download.py` if you need
  the https file. A Bon Venture ad footer on a bulletin's last pages ("D86910 (JB) - St.
  Anthony of Padua") only means Bon Venture sells the ads; the PDF can be self-hosted.
- **FATA Online** (`fataonline.com/bulletins/<code>`): Good Shepherd, Perryville links
  `GoodShepherdPerryville` from its eCatholic site. Plain curl works (Harrisburg). Record
  `page-pdfs http://fataonline.com/bulletins/<code>`. File names carry no date, so
  `fetch:check` reports `unverified`: take identity and date from the cover. A cover can
  put the church names of its Mass boxes in an image layer, leaving only the times in the
  text: render page 1 to see which churches it lists, and quote trustee or calendar lines
  from the text.
- **Self-hosted:** Holy Family, Newark (`bulletin.php`), Immaculate Conception, Elkton,
  Holy Cross/Immaculate Conception, Marydel (Weebly, iccmarydel.org/bulletin.html; Holy
  Cross's own holycrossdover.org, which the directory doesn't give, answers 403 to curl but
  lists the same dated files in the browser), St. Anthony of Padua (`/bulletin-archive/`), St. John Neumann (weconnect), Our Lady of Good Counsel,
  Secretary, St. Paul, Delaware City. Duda sites list weekly PDFs on /bulletins as
  `irp.cdn-website.com/<site>/files/uploaded/<date>.pdf`, newest first, so `page-pdfs
  <bulletins page>` needs no filter (iccelkton.org); but a Duda bulletins page can be
  abandoned while the home page links the live bulletin elsewhere (St. Hedwig's stops in
  December 2024; it is John Patrick 317). A Duda-style page linking
  `/images/Bulletin_<M.D.YY>.pdf` lists them oldest first; `page-pdfs` filtered to
  `filename=Bulletin_*.pdf` still picks the newest (Our Lady of Good Counsel, Secretary). A WordPress archive page that also lists forms and
  calendars needs a filename filter (St. Anthony of Padua: `page-pdfs
  https://sapde.org/bulletin-archive/ filename=Bulletin-*.pdf`). A WordPress bulletins
  page can list dated posts (category "bulletin") that each wrap a PDF, with no PDF link on
  the listing: record `dated-post <bulletins page>`, not `page-pdfs` (St. Paul, Delaware
  City), and confirm the uploads with the site's
  `/wp-json/wp/v2/media?mime_type=application/pdf`.
- **HTML-only bulletins:** a site's "Bulletin" menu item can lead to a page whose slug
  doesn't say bulletin (Holy Name of Jesus, Pocomoke's Wix site: `/fr-dan-s-corner`), so
  read the menu labels and hrefs in the page source, not only links named for bulletins. A
  page of weekly announcements as HTML text with no PDF or image is `no_bulletin` with
  `bulletin_status: unsupported-format` (map 024; whether to support such pages is flagged
  to the owner).
- **Sites that didn't load in the browser either (2026-10-27):** stpatschapel.org
  (Conowingo); stjosephfrenchst.org and
  iccparish.org are dead old domains (St. Joseph and Immaculate Conception read on
  sjfschurch.org and iccelkton.org); saintpolycarp.org and stdennischurch.org failed in
  curl and the browser (both on John Patrick, see that bullet). Try again later before
  recording a site as blocked: visitstfrancis.org (St. Francis de Sales, Salisbury), down in
  the survey, loaded for map 024 the same day. Then look for the bulletin on a publisher
  (see the parish-site-access skill).

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- A summer-guide season note can be wrong: St. Mary Star of the Sea, Ocean City's Sunday 7 AM is marked '(Memorial Day – Labor Day)' but the November bulletin and the parish Mass-times page (which lists it in both seasons) show it year-round, so read the off-season bulletin before making a church seasonal.
- A Duda/WeConnect bulletins page's LPi widget can be written `publicationWidget?type=bulletin&color=gray&id=<lpi id>` (id not first): grep `id=0018` and run `probe po <lpi id>` (St. Luke 0018000000Qc275AAB, St. Mary & Holy Savior 0018000000Qx8zFAAR). A WeConnect site (stjohnneumannrcc.com /publications) links parishesonline.com/publication-page/<org>?selectedPublication=<container url> per issue.
- An LPi cover can print two dates ('October 25, 2026 / November 1, 2026'), which makes fetch:check report issue_date `conflict` for a correct current pick.
- Eastern Catholic parishes: confirm the jurisdiction on the eparchy's own parish list (Archeparchy of Philadelphia: ukrcatholic.org/parishes, formerly ukrarcheparchy.us) and on GCatholic's 'Jurisdiction:' line.
- GCatholic's 'Jurisdiction:' line names the Archdiocese for the Military Services for a base chapel; dover.af.mil answers 403 to curl/probe url but loads with visit.py.
- Note: archmil.org is the Archdiocese of Milwaukee; the Military Services archdiocese is milarch.org.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (St. Nicholas, Wilmington and St. Basil the Great, Chesapeake City, both Ukrainian) are excluded as `other-jurisdiction`, as in every other diocese here. (accepted by survey-review, 002-survey-review, 2026-10-27)
- **Shared pastors don't make shared bulletins.** A pair under one pastor (St. Ann and St. Thomas the Apostle; Holy Child and St. Helena; St. John the Beloved and St. Catherine of Siena; St. Polycarp and St. Dennis; Immaculate Conception, Elkton and St. Thomas More Oratory) is one row only when one current bulletin covers both. (accepted by survey-review, 002-survey-review, 2026-10-27) Both outcomes occur: Holy Child and St. Helena print two bulletins under Fr. Carrier (map 003, 2026-10-27); St. Ann's eCatholic file has carried St. Thomas's pages since at least 26 July 2026 while sainttom.org's own bulletins page went stale in June (map 004, 2026-10-27). Check the sister parish's homepage "bulletins" link, not only its own bulletins page, and read page 1 of the file. A shared associate printed on both covers is no different: Holy Family and Resurrection (Rev. Francis Okorie) print separate John Patrick bulletins, 308 and 310 (map 008, batch `newark-hockessin`, 2026-10-27). Immaculate Conception, Elkton and St. Thomas More Oratory (Fr. Jasper) are separate too: the Newman Center publishes only a semester newsletter and limits Mass to the university community, and Immaculate Conception's bulletin never mentions it (map 012, batch `elkton-newark-oratory`, 2026-10-27; whether its Mass counts as public is the owner's call, flagged by that batch). St. Polycarp and St. Dennis print separate John Patrick bulletins (301 and 732) although St. Dennis's cover gives St. Polycarp's office and livestream as contacts: compare mastheads and Mass schedules, not contact lines (map 016, batch `smyrna-galena-chestertown`, 2026-10-27). Holy Cross, Dover and Immaculate Conception, Marydel are one row: one cover headed by both names with a Mass box each, one staff list, and a pastor's column to one "collaborative Parish community" (map 018, batch `dover-milford`, 2026-10-27). St. Mary Refuge of Sinners, Cambridge and Our Lady of Good Counsel, Secretary share a pastor but print separately (map 020, batch `talbot-dorchester`, 2026-10-27).
- **A seasonal worship site keeps its church row** with a dated `revisit` for its next season: St. Andrew, Ocean City ('seasonal mission of St. Luke – open May 23 – Sept. 6'), St. Mary Star of the Sea, Church Creek ('Memorial Day weekend through late September'), and St. Mary Star of the Sea, Ocean City if its Sunday Mass is summer-only. (accepted by survey-review, 002-survey-review, 2026-10-27) Sources can disagree on the season: for Church Creek the bulletin says Memorial Day through Labor Day weekend, the parish site to the last Sunday in September; record each source's dates and don't pick (map 020, batch `talbot-dorchester`, 2026-10-27).
- **A directory Mass time is not proof of a weekly Mass.** A chapel's single time in the `directory` roster can be one annual Mass (St. Patrick Chapel, Conowingo: 'Sat 10:00' is the 12 September annual Mass; the bulletin says 'As Announced'), so check the bulletin before recording a time as weekly. (map 014, batch `cecil-good-shepherd`, 2026-10-27; whether such a chapel stays a church with no weekly times is flagged to the owner by that batch) The roster's other per-church details are no better: a two-church parish's entry can merge both churches' Mass slots (St. Benedict, Ridgely lists St. Elizabeth's Friday and Saturday times), a reopened mission can show none (St. Peter, Queenstown; map 019, batch `mid-shore-north`, 2026-10-27), and a mission's ZIP can be the parent's, in the directory and in GCatholic (St. Michaels given Easton's 21601 by both, Cordova by GCatholic; map 020, batch `talbot-dorchester`, 2026-10-27). Take each church's Mass times and ZIP from the bulletin's schedule block, which prints each church's address. Read the heading over each time there: a bulletin's devotions list can give a mission a weekly service that is not Mass (Our Lady of Guadalupe, Frankford: a Friday 6:30 PM Spanish prayer service and rosary; map 022, batch `sussex-beaches`, 2026-10-27).

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-10-27: Initialised (factory survey, Run wilmington-map-1). Rosters: GCatholic (80
  entries), the cdow.org parish map as `directory` (79), the Summer Vacation Mass Guide as
  `summer-guide` (34). Planned 19 map batches in `batches.json` (193 entries, none excluded).
  No records yet.
