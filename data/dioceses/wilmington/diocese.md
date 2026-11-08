---
name: Roman Catholic Diocese of Wilmington
state: DE
website: https://cdow.org
status: promoted
gcatholic: wilm0
city_aliases:
  St Michaels: St. Michaels
  Kent Island: Chester
  Ocean Pines: Berlin
  Oak Orchard: Millsboro
  Golden Hill: Church Creek
audit_ignore_groups:
- parishes
promoted: 2026-11-07
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

- **John Patrick Publishing** (church-bulletin.org) prints much of New Castle County and the
  upper shore. Parish sites link `jppc.net/onlinebulletins/<id>template.pdf` (or
  `church-bulletin.org/?id=<id>`), which redirects to a `church-bulletin.org/<slug>` listing
  of dated PDFs; Delaware's numbers are 300-320 and 732. Follow the redirect to learn the
  slug; never guess one, since a wrong slug returns the generic home page with HTTP 200.
  Record `page-pdfs https://www.church-bulletin.org/<slug>`, as Harrisburg and Allentown do,
  even when the parish site has its own bulletin page (it can be a week behind), and use the
  redirect when the parish site answers 403 or 500 or doesn't connect. A listing can outlive
  its parish (313, Christ Our King, lists no PDFs). A "Bulletin" button is often only an
  href to the template: quote visible text (the listing's title, the cover), not the href.
  The site answers 406 to a bare "Mozilla/5.0" agent and the sandbox refuses curl with a
  browser agent, so read it with `pnpm diocese probe get`, `probe pdf` or `visit.py`. Many
  covers are scanned images: render page 1 with `render.py` for the masthead (`fetch:check`
  still passes). A rendered cover lists each church with its times and any status line ("The
  Church is currently closed for repairs"): the current-Mass evidence for a mission or shrine.
- **LPi / ParishesOnline** prints most of the Ocean Deanery, the mid-shore and Kent
  (containers `04/xxxx`) and several northern parishes (`03/xxxx`). Sites on other platforms
  hide the link: a Wix "Bulletin" button goes to `parishesonline.com/find/<slug>` while the
  home page's only PDFs are one-page inserts; an eCatholic site can host no bulletins and link
  ParishesOnline (record the po ids, not the eCatholic id); a Duda or WeConnect page embeds
  `publicationWidget?...id=<lpi id>`, sometimes only in the page source and with the id not
  first (`publicationWidget?type=bulletin&color=gray&id=...`), so grep the HTML for `id=0018`
  and resolve it with `probe po`; quote the bulletin, not the href, which `recheck` can't find. A WeConnect `/publications` page links each issue as
  `parishesonline.com/publication-page/<org>?selectedPublication=<container url>`. Menu links
  can carry a hash suffix (`/bulletin<hash>`): use `visit.py --follow` and read `final_url`.
  The directory's website can be a sister institution's with no bulletin link (Easton's
  parish-and-schools site): try the parish's other directory entries. One container can have
  an organization account per church: record every po-org id on the one row. Org names
  joining two parishes are leads, not proof. A cover's "United in Christ" box of Mass times
  for several parishes is a deanery schedule, not a shared masthead: take the parish and staff
  from page 2 or later. Covers are often image-only, with text only on the ad pages: render
  page 1, and quote the LPi footer ('Parish, City, DE 03-NNNN') as the text naming the
  container; for each church's times render the cover's Mass box or the Mass-intentions page,
  which adds the seasonal sites in summer. `probe pdf --grep` returns pages 1-3 whether or not
  they match: find a notice's page with `--pages N`. In `fetch:check`, freshness `future` is
  normal (issues go up before their weekend), and a cover printing two dates gives issue_date
  `conflict` for a correct pick. Don't take coordinates from an org's own pin (one was about
  3 km off).
- **eCatholic** (about 14 sites): most answered plain `probe url` here; those behind
  Cloudflare answer 403 and load with `visit.py`, and `issues.py ecatholic` reads the files
  without a browser. The weekly issues are `/<id>/bulletins/YYYYMMDD.pdf` on the /bulletins
  page, often up before their Sunday (`fetch:check` freshness `future`); a home page's first PDF link can be a Mass insert under `/documents/`. Some sites host
  no eCatholic bulletins and link John Patrick, FATA Online or ParishesOnline instead: pin
  that listing with `page-pdfs` and leave the eCatholic id out of `publication`. A parish on
  eCatholic and LPi can serve one issue on both (St. Joseph on the Brandywine): compare the
  issues and record both ids on one row. A file can carry a sister parish's pages (St. Ann's
  holds St. Thomas's): read page 1. A /bulletins list can stop months early: before calling
  it stale, check the home page's bulletin link, which can be only an image link to another
  publisher (Bonventure); the `?t=<ms>` upload stamps on the file links show whether a
  parish posts in batches. When a parish domain fails TLS in curl and Chrome
  (ERR_CERT_COMMON_NAME_INVALID), its Wayback copy still shows the eCatholic id, and the
  bulletin's letterhead can name the working domain.
- **J.S. Paluch on Discover Mass** (`discovermass:<church slug>`): a listing can serve the
  same issue as the parish's own copy, re-laid-out (12 pages against 10, the text oddly
  spaced): when the parish site carries the issue, pin that copy and keep the listing in
  `publication` only. Discover Mass caps downloads per IP per day: a 134-byte "Maximum number
  of files downloaded today" reply, which `fetch:check` reports as `not_pdf`, is the cap, not
  the row; retry after the reset.
- **Bonventure** (`sponsors.bonventure.net`, from OSV/Duda, eCatholic and GoDaddy sites, the
  last a stub page with one "CLICK HERE" button): `probe url` misses the link and some sites
  answer 403; `visit.py --text --links` shows "Bulletin" going to
  `sponsors.bonventure.net/?page=<n>`, with issues at `/pdfs/<n>/<YYYY-MM-DD>.pdf` whose page
  1 names the parish (text layer). The https host fails TLS verification from Python but
  loads in Chrome: use `http://` in recipes and evidence (`page-pdfs
  http://sponsors.bonventure.net/?page=<n>`), and `tools/browser_download.py` for the https
  file. A Bon Venture ad footer ("D86910 (JB) - <parish>") only means it sells the ads; the
  PDF can be self-hosted.
- **FATA Online** (`fataonline.com/bulletins/<code>`, linked from an eCatholic site): record
  `page-pdfs http://fataonline.com/bulletins/<code>`. File names carry no date, so
  `fetch:check` reports `unverified`: take identity and date from the cover. The Mass boxes'
  church names can be in an image layer, leaving only the times in the text: render page 1 to
  see the churches, and quote trustee or calendar lines.
- **Self-hosted:** Duda sites list weekly PDFs on /bulletins as
  `irp.cdn-website.com/<site>/files/uploaded/<date>.pdf`, newest first, so `page-pdfs
  <bulletins page>` needs no filter; but a Duda bulletins page can be abandoned while the home
  page links the live bulletin elsewhere (St. Hedwig's stops in December 2024; it is John
  Patrick). A page linking `/images/Bulletin_<M.D.YY>.pdf` lists them oldest first; `page-pdfs`
  with `filename=Bulletin_*.pdf` still picks the newest. A WordPress archive that also lists
  forms and calendars needs a filename filter (`filename=Bulletin-*.pdf`). A WordPress page
  can list dated posts that each wrap the PDF in an iframe, with no PDF link on the listing:
  record `dated-post <bulletins page>`, not `page-pdfs`, and confirm the uploads with
  `/wp-json/wp/v2/media?mime_type=application/pdf`; a check run while the newest post is
  going up can fail once with `NoBulletin`, so rerun it before recording a block. A site that
  answers 403 to curl can list the same dated files in the browser (holycrossdover.org).
- **HTML-only bulletins:** a "Bulletin" menu item can lead to a page whose slug doesn't say
  bulletin (a Wix `/fr-dan-s-corner`), so read the menu labels and hrefs in the page source,
  not only links named for bulletins. Weekly announcements as HTML text with no PDF or image
  are `bulletin_provider: unsupported` with `fetch_gap` kind `html-only-bulletin` (README,
  *What to flag*), not `no_bulletin`.
- **Sites that fail in the browser too:** many roster websites are dead old domains; read
  the parish's working domain or its publisher instead. A site down in one session can load
  later the same day (visitstfrancis.org, map 024): try again before recording a block, then
  look for the bulletin on a publisher (parish-site-access skill).

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- **Eastern Catholic churches** (St. Nicholas, Wilmington and St. Basil the Great, Chesapeake City, both Ukrainian) are excluded as `other-jurisdiction`, as in every other diocese here. (accepted by survey-review, 002-survey-review, 2026-10-27) Confirm the jurisdiction on the eparchy's or ordinariate's own list (Archeparchy of Philadelphia: ukrcatholic.org/parishes, formerly ukrarcheparchy.us; the Archdiocese for the Military Services is milarch.org, not archmil.org, which is Milwaukee) and on GCatholic's 'Jurisdiction:' line, which names the Military Services archdiocese for the Dover AFB chapel; dover.af.mil answers 403 to curl but loads with `visit.py` (map 027, batch `other-jurisdiction`, 2026-10-27; whether a base chapel is better `no-public-mass` is flagged to the owner).
- **Shared pastors don't make shared bulletins.** A pair under one pastor (St. Ann and St. Thomas the Apostle; Holy Child and St. Helena; St. John the Beloved and St. Catherine of Siena; St. Polycarp and St. Dennis; Immaculate Conception, Elkton and St. Thomas More Oratory) is one row only when one current bulletin covers both. (accepted by survey-review, 002-survey-review, 2026-10-27) Both outcomes occur: Holy Child and St. Helena print two bulletins under Fr. Carrier (map 003, 2026-10-27); St. Ann's eCatholic file has carried St. Thomas's pages since at least 26 July 2026 while sainttom.org's own bulletins page went stale in June (map 004, 2026-10-27). Check the sister parish's homepage "bulletins" link, not only its own bulletins page, and read page 1 of the file. A shared associate printed on both covers is no different: Holy Family and Resurrection (Rev. Francis Okorie) print separate John Patrick bulletins, 308 and 310 (map 008, batch `newark-hockessin`, 2026-10-27). Immaculate Conception, Elkton and St. Thomas More Oratory (Fr. Jasper) are separate too: the Newman Center publishes only a semester newsletter and limits Mass to the university community, and Immaculate Conception's bulletin never mentions it (map 012, batch `elkton-newark-oratory`, 2026-10-27; whether its Mass counts as public is the owner's call, flagged by that batch). St. Polycarp and St. Dennis print separate John Patrick bulletins (301 and 732) although St. Dennis's cover gives St. Polycarp's office and livestream as contacts: compare mastheads and Mass schedules, not contact lines (map 016, batch `smyrna-galena-chestertown`, 2026-10-27). Holy Cross, Dover and Immaculate Conception, Marydel are one row: one cover headed by both names with a Mass box each, one staff list, and a pastor's column to one "collaborative Parish community" (map 018, batch `dover-milford`, 2026-10-27). St. Mary Refuge of Sinners, Cambridge and Our Lady of Good Counsel, Secretary share a pastor but print separately (map 020, batch `talbot-dorchester`, 2026-10-27).
- **A seasonal worship site keeps its church row** with a dated `revisit` for its next season: St. Andrew, Ocean City ('seasonal mission of St. Luke – open May 23 – Sept. 6'), St. Mary Star of the Sea, Church Creek ('Memorial Day weekend through late September'), and St. Mary Star of the Sea, Ocean City if its Sunday Mass is summer-only. (accepted by survey-review, 002-survey-review, 2026-10-27) Sources can disagree on the season: for Church Creek the bulletin says Memorial Day through Labor Day weekend, the parish site to the last Sunday in September; record each source's dates and don't pick (map 020, batch `talbot-dorchester`, 2026-10-27). A summer-guide season note can be wrong: it marks St. Mary Star of the Sea, Ocean City's Sunday 7 AM '(Memorial Day – Labor Day)', but the November bulletin and the parish's Mass-times page show it year-round, so that church is not seasonal. Read an off-season bulletin before making a church seasonal (map 026, batch `ocean-city`, 2026-10-27).
- **A directory Mass time is not proof of a weekly Mass.** A chapel's single time in the `directory` roster can be one annual Mass (St. Patrick Chapel, Conowingo: 'Sat 10:00' is the 12 September annual Mass; the bulletin says 'As Announced'), so check the bulletin before recording a time as weekly. (map 014, batch `cecil-good-shepherd`, 2026-10-27; whether such a chapel stays a church with no weekly times is flagged to the owner by that batch) The roster's other per-church details are no better: a two-church parish's entry can merge both churches' Mass slots (St. Benedict, Ridgely lists St. Elizabeth's Friday and Saturday times), a reopened mission can show none (St. Peter, Queenstown; map 019, batch `mid-shore-north`, 2026-10-27), and a mission's ZIP can be the parent's, in the directory and in GCatholic (St. Michaels given Easton's 21601 by both, Cordova by GCatholic; map 020, batch `talbot-dorchester`, 2026-10-27). Take each church's Mass times and ZIP from the bulletin's schedule block, which prints each church's address. Read the heading over each time there: a bulletin's devotions list can give a mission a weekly service that is not Mass (Our Lady of Guadalupe, Frankford: a Friday 6:30 PM Spanish prayer service and rosary; map 022, batch `sussex-beaches`, 2026-10-27).

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: Hand refresh of Run wilmington-map-1 (PR #170) against main: merged main and
  reran reconcile and integrate by hand under main's current rules. Records: 50 parish rows
  (48 with a bulletin `fetch` collects; St. Thomas More Oratory `no_bulletin`; Holy Name of
  Jesus, Pocomoke now `unsupported`, `fetch_gap` `html-only-bulletin`: its "Bulletin" is a
  weekly HTML page), 77 churches, 6 excluded, 1 open. Our Lady of the Highways, Childs went
  from open/ to excluded (`other`): the Oblates' pages show it is a roadside statue on I-95.
  Coverage: directory 79/79 accounted for (72/76 modelled), GCatholic 80/80 (70/74),
  summer guide 34/34 (34/34); one church in no roster (St. John the Baptist, Newark). No
  merges or moves. Audit with today's pairing: 116 candidate pairs, 16 with content-supported
  `separate` reviews; the other 100 come only from the deanery `group`s (no publisher-account
  or host pairs), which share programmes here, not bulletins, so no reviews were written for
  them. `fetch:check` on all 48 rows (`scratch/wilmington-map-1/refresh/`): 39 picked the 8
  November issue (St. Joseph, Wilmington current again) and St. Luke the 15 November one;
  Holy Cross/Marydel, Our Lady of Lourdes, St. Elizabeth and Good Shepherd the 1 November
  one; St. Ann, Bethany Beach the 8 November one now that Discover Mass's cap reset; St.
  Paul, Delaware City failed once and picked the 8 November issue on a rerun. Not current: St. Paul, Wilmington (2 August, 97 days; no other channel
  found) and Holy Child (18 October; the container has posted nothing since), each with a
  dated `research` retry.

- 2026-10-27: Reconciled (job 028, Run wilmington-map-1) after 19 map batches (6 to 18
  roster entries each, usually 8 to 10). Records: 50 parish rows (48 with a bulletin; St.
  Thomas More Oratory and Holy Name of Jesus, Pocomoke `no_bulletin`), 77 churches, 5
  excluded, 2 open. Coverage: directory 79/79 accounted for (72/76 modelled), GCatholic
  80/80 (70/75), summer guide 34/34 (34/34); one church in no roster (St. John the Baptist,
  Newark, explained in its record). No merges or moves: every batch flag was an owner
  question or already recorded. The audit's real candidates (shared-pastor pairs and the
  four Bonventure-hosted parishes) are now 16 content-supported `separate` reviews; its
  other 1,112 pairs come only from the deanery `group`s and GCatholic's empty group (`,` on
  all 80 entries). `fetch:check` on all 48 rows: 48 distinct files; 38 this week's issue,
  five next week's (`future`), St. Luke's two-date cover (`conflict`), Good Shepherd
  undated (24-25 October on the cover); not current: St. Paul, Wilmington (2 August, 86
  days), St. Joseph, Wilmington (11 October, 16 days), and St. Ann, Bethany Beach (Discover
  Mass daily cap; retry from 2026-10-28).

- 2026-10-27: Initialised (factory survey, Run wilmington-map-1). Rosters: GCatholic (80
  entries), the cdow.org parish map as `directory` (79), the Summer Vacation Mass Guide as
  `summer-guide` (34). Planned 19 map batches in `batches.json` (193 entries, none excluded).
  No records yet.
