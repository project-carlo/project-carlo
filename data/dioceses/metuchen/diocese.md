---
name: Roman Catholic Diocese of Metuchen
state: NJ
website: https://diometuchen.org
status: promoted
gcatholic: metu0
city_aliases:
  Woodbridge Township: Woodbridge
  Old Bridge Township: Old Bridge
  Hillsborough Township: Hillsborough
  Piscataway Township: Piscataway
  Plainsboro Township: Plainsboro
  Oxford Township: Oxford
promoted: 2026-11-07
---

Four counties of central and northwestern New Jersey: Middlesex (New Brunswick, Perth Amboy,
Edison, Woodbridge, Metuchen, Old Bridge, Sayreville), Somerset (Somerville, Bridgewater,
Raritan, Manville, Bernardsville), Hunterdon (Flemington, Lambertville, Clinton area) and Warren
(Phillipsburg, Washington, Hackettstown, Belvidere). The chancery is at 146 Metlars Lane,
Piscataway. It borders Newark (northeast), Paterson (north), Trenton (south), and across the
Delaware Allentown, Scranton and Philadelphia. GCatholic names those six neighbours; of them, only
Allentown is mapped. On its *About* page (read 2026-10-30) the diocese counts "90 Parishes" and
"15 Eastern Church parishes under the jurisdiction of their own bishops". Its 2024–2025 annual
report says "the 89 parishes". The difference is the North Plainfield merger of July 2025 (below).

**How it is organised.** There are eight deaneries (Cathedral, County Seat, Forsgate, Middlebrook,
Morris Canal, Raritan Bay, Round Valley, Somerset Hills), which the parish finder uses as its
categories. No families, clusters or pastorates were found. Instead, a dozen parishes
formed by earlier mergers keep several churches. Divine Mercy (Carteret), Good Shepherd
(Hopelawn), Most Holy Name of Jesus and St. John Paul II (Perth Amboy), Holy Family and the
Parish of the Visitation (New Brunswick), Transfiguration of the Lord (Highland Park/Edison),
Christ the Redeemer (Manville), St. Anthony of Padua (Port Reading/Woodbridge), St. John the
Evangelist (Lambertville/Stockton) and St. Elizabeth–St. Brigid (Far Hills/Peapack) list their
worship sites in the finder. GCatholic gives "parish 2010" (Holy Family, Carteret) and
"parish 2012" (three Perth Amboy/Hopelawn churches) for some of these. So shared bulletins are most
likely (a) inside a merged parish, (b) between the few pairs the finder gives one pastor (Belvidere/
Oxford, Iselin/Woodbridge, Frenchtown/Milford), and (c) among the three Raritan Oratory parishes.

## Sources

- **Parish finder (the `directory` roster):** https://diometuchen.org/parishfinder, an eCatholic
  map behind Cloudflare (`probe url` gets 403; parish-site-access `finder.py` reads it). Read
  2026-10-30: 91 pins, 90 parish entries (St. Elizabeth–St. Brigid has one pin per church,
  24487 and 25192). Each entry's *Details* tab gives the clergy and, for merged parishes, a
  "Worship Site(s):" list. Its Sunday Mass schedule names the church for each Mass in a note.
  `rosters/directory.json` keeps these as `deanery`, `clergy`, `finder_detail` and
  `mass_locations` (scraper: `scratch/metuchen-map-1/tools/finder_details.py` and
  `enrich_directory.py`). Good for: the parish list, deaneries, worship sites, and which
  church each Mass is at. How far to trust it:
  - **It lags on mergers.** St. Joseph (24517) and St. Luke (24518), North Plainfield still have
    their own entries and administrators. The bishop's decree (diometuchen.org/news/
    merger-of-st-joseph-st-luke-parishes, dated 30 May 2025, read 2026-10-30) merged them
    "effective July 1, 2025" with the name "Sts. Joseph and Luke". www.SJNP.org now redirects to
    sjlnp.org.
  - **Its clergy lines are partly stale.** It names Msgr. Joseph G. Celano as pastor of both
    Immaculate Conception, Somerville and St. Peter the Apostle, New Brunswick, but St. Peter's
    25 October 2026 bulletin (files.ecatholic.com/21126/bulletins/20261025.pdf, p. 2) reads
    "Rev. Michael Tabernero, Pastor". St. Philip and St. James carries a "(NOTE: Rev. Kusek
    effective in October 2019)". Treat a pastor shared in the finder as a lead, not a fact.
  - Its pins are parish offices or main churches. A merged parish's secondary churches have no
    pin, only lines in the Details text (hence the `worship-sites` roster).
  - Websites: 16 entries have none. The domains for Sacred Heart (South Amboy), St. Joseph
    (Carteret) and St. Theodore (Port Murray) don't resolve. St. Joseph, Raritan's
    `*.weconnect.com` address is unreachable. Several redirect to a new site (OLM South Bound
    Brook to Google Sites, St. Joseph Millstone to sjmillstone.com).
- **Worship sites (the `worship-sites` roster):** 25 entries built from the finder's Details
  lists (12 parishes), plus two places named only in Mass notes: "La Asuncion" (Spanish
  Masses of Most Holy Name of Jesus; GCatholic gives La Asuncion at 777 Cortlandt St) and
  "Sacred Heart Chapel" (a 9:30 AM Sunday Mass of OLPH, Bernardsville; no address). `group` is
  the parent parish. These are mostly the same buildings as GCatholic entries. St. Mary of Mount
  Virgin, New Brunswick is in no other roster, and GCatholic's "St. Lucy Filippini" (National
  Shrine, 190 Sanford St) has that church's address.
- **GCatholic (the `gcatholic` roster):** key `metu0`, fetched 2026-10-30. 123 entries: 107
  Latin, and 16 Eastern Catholic (`rite`: Ruthenian 9, Ukrainian 5 (one "Former Church"),
  Maronite 1, Syro-Malabar 1). It **omits the cathedral** (St. Francis of Assisi, Metuchen). It
  keeps churches of merged parishes that the finder no longer lists:
  - Sacred Heart (67 Fitch St) and St. Elizabeth of Hungary (119 Washington Ave), Carteret,
    beside Divine Mercy's Holy Family.
  - Holy Spirit (580 Hazel Ave) and St. Mary (104 Center St), Perth Amboy. GCatholic puts Holy
    Spirit under Good Shepherd Parish and St. Mary under Parish of St. John Paul II.

  It gives three shrines: Blessed Sacrament (50 W Somerset St, Raritan, shrinechapel.com), Our
  Lady of Fatima (674 Mountain View Rd E, Washington; the World Apostolate of Fatima shrine)
  and St. Lucy Filippini (above). Where the finder and GCatholic disagree on addresses:
  - St. Ladislaus, New Brunswick: 215 Somerset St (finder) or 40 Plum St (GCatholic).
  - Blessed Sacrament, Martinsville: the finder's worship site is 1890 Washington Valley Rd,
    while its pin and GCatholic give 852 Newmans Ln.
  - St. James, Woodbridge: 369 Amboy Ave (finder) or 148 Grenville St (GCatholic).
  - GCatholic puts St. Elizabeth in Peapack, not Far Hills, and Our Lady of Victories in
    Baptistown, where the finder says Frenchtown.

  Many of its websites are old (`*.4lpi.com`, `*.parishesonline.com`, comcast.net).
- **Clusters / families of parishes:** none. The diocese uses deaneries and canonical mergers;
  no family or cluster list was found on diometuchen.org. The finder's own clergy lines are the
  only diocese-wide shared-pastor source.
  - The finder gives one pastor to St. Patrick, Belvidere and St. Rose of Lima, Oxford (Rev.
    David J. Pekola; one website, stpatrickrose.org), and names him for Our Lady of Victories,
    Sayreville too. The Belvidere/Oxford line is the stale one: Our Lady of Victories' 25 October
    2026 masthead names "Rev. David J. Pekola, Pastor", while the 1 November 2026 St. Patrick and
    St. Rose of Lima masthead (container 04/0870) names "Reverend Charles A. Sabella Pastor"
    (map batches `sayreville-parlin` and `belvidere-oxford-blairstown`).
  - St. Cecelia, Iselin and St. James, Woodbridge (Rev. Thomas Naduviledathu, SDV).
  - Our Lady of Victories, Frenchtown and St. Edward the Confessor, Milford (Fr. Bede Kim).
  - St. Ann and St. Joseph, Raritan and Holy Trinity, Bridgewater are staffed by the Raritan
    Oratory (CO).
- **Mass times:** no separate diocese-wide Mass-times page; the finder's per-parish schedule is
  it (the `directory` roster's `mass_locations`). It also shows Masses in other languages and
  places (Coptic Catholic Mass in St. Ambrose's "St. Anthony Room", Old Bridge; Kiswahili and
  Tagalog monthly at St. Matthew, Edison).
- **Clergy list:** none found apart from the finder. ParishSOFT (metuchen.parishsoftfamilysuite.com)
  needs a login.
- **Closed parishes and where their records went:** no diocesan list found.
- **Pastoral plan / closure announcements:** none found. "One Church Together" is a 2023–24
  devotional campaign, not a plan. The diocese's news stream (aggregateStream/NEWS, 241 items
  back to about 2021, read 2026-10-30) has one structural item, the North Plainfield merger
  above. The earlier mergers (2010–2012 in Carteret and Perth Amboy) predate it. The diocesan
  paper *The Catholic Spirit* (catholicspirit.com) printed the decrees but answers 403 to
  `probe get`. Date those mergers and closures from the bulletins, GCatholic's history field or
  local news.

### Bulletin publishers here

From the survey's probes of the finder websites (2026-10-30) and the map batches since:

- **eCatholic** hosts most parish sites; they answer `probe url` directly. **A site id is the
  website's, not proof the bulletin is there:** a Bulletin page can embed an LPi id (St. Matthew,
  Edison), say only "Click Here" to a ParishesOnline org, or link only a John Patrick template;
  follow the link with `visit.py --links` and record the publisher it reaches. **`ecatholic:21916`
  is the diocese's own site:** don't record it. Read issues with `issues.py ecatholic` at
  `files.ecatholic.com/<id>/bulletins/<YYYYMMDD>.pdf`; it answers 403 for a site that doesn't name
  its files by the Sunday date, so read the real names with `visit.py --links`. A Bulletin page
  can be a frozen archive while the menu's "Bulletin" item points to the live publisher: check
  the newest file's date and don't record a stale id.
- **ParishesOnline / LPi:** containers can sit behind a `/wordpress/` redirect, and a parish
  WordPress can post LPi-named files (`20261011B-3.pdf`): look for its container. A container can
  carry the file the parish hosts on eCatholic (see *Rules settled*). To find a container, `probe
  po <name>-church-<zip>` (`st-catherine-of-siena-church-08867`); a merged parish's container can
  sit under its old member churches' slugs, so try each and record every org's ids on the one
  row. If slugs fail, search for the parish's LPi WeConnect site
  (`<name>-<aa>-<bbbb>.weconnectonline.com`): it embeds the LPi id, and `probe po <id>` gives the slug.
- **John Patrick Publishing** (church-bulletin.org): parish sites link
  `jppc.net/onlinebulletins/<id>template.pdf`, which returns HTML (`probe pdf` can't read it).
  Record provider `other` with `page-pdfs https://church-bulletin.org/<id>`; the listing posts the
  coming Sunday about two days early, so `fetch:check` reports freshness `future`. A parish site
  can keep a frozen "This Week" `bulletin.pdf` while John Patrick posts the current issue: check
  the newest date. It answers 406 to a bare "Mozilla/5.0" user agent.
- **Bonventure** (`sponsors.bonventure.net/?page=<n>`, http only; files at `pdfs/<n>/<date>.pdf`):
  parishes' eCatholic sites only link it. Record provider `other` with `page-pdfs
  http://sponsors.bonventure.net/?page=<n>`; it posts the coming Sunday early. Each account
  number is one parish, so different accounts are separate `publication_reviews`, decided from
  mastheads. Listing ids don't follow the ad-page G-codes and many are empty;
  `tools/bonventure_scan.sh` scans an id range for a town name (about 4 s per id). A parish can
  leave its listing unlinked or post its own issues (Weebly
  `/uploads/…/<YYYY-MM-DD>-<code>web.pdf`, or names that don't match the date, such as
  `BulletinOctober4.pdf` holding 25 October): search or scan for a listing before recording no
  PDF bulletin. Parish copies can skip weeks: date them from the PDF text, and pin `page-pdfs` to
  a newest-first list ("This Week" first); `fetch:check` then reports date `unknown`.
- **Discover Mass** (`discovermass:<slug>`) caps downloads per IP per day (a 134-byte "Maximum
  number of files downloaded today" reply, `not_pdf` in `fetch:check`), so cite the church page
  and the issue date, not a tokenised link. `fetch:check` reports date and freshness `unknown`:
  confirm currency from the date the church page lists. Its church page is also the `website`
  for a parish with no site (see *Rules settled*).
- **Self-hosted PDFs** (dated paths, Wix `_files/ugd/` hashes, Weebly, plain `/Bulletins.html`):
  `page-pdfs` on the Bulletin page works; check the newest entries are real PDFs (one list held
  `.crdownload` uploads). On Wix each date label follows its PDF link, so take the date from the
  PDF text; Wix answers 429 after a few rapid downloads. Google Sites can embed the John Patrick
  template, so check for `jppc.net` first. Squarespace posts `/s/<name>.pdf`: pin a filename glob
  on the issues' common prefix; a Bulletin page linking one PDF can stop updating, so if its
  date is stale record research with a revisit, not a recipe. A self-hosted archive can date a
  worship site gone from the Mass page: grep one issue per half-year for the church name.
- **Catholic Web Company** (footer `thecatholicwebcompany.com`): no `/bulletin` page; `page-pdfs`
  on the "Events & Bulletin" page `/event` picks the newest `/uploads/docs/bulletins/<YYYYMMDD>.pdf`.
- **OSV/Duda sites** (footer `editor.osvwebsites.com`) post
  `irp.cdn-website.com/<site>/files/uploaded/<MM.DD.YYYY><suffix>.pdf`; `page-pdfs` on `/bulletin`
  picks the newest.
- **GoDaddy site builder** (PDFs at `storage.googleapis.com/production-sitebuilder-v1-0-9/…/<hash>?fileName=<name>`):
  a `filename=` glob matches the hash, not `fileName`, so it can't filter these. `page-pdfs` on
  the Bulletins page picks the newest, dating each link from its name. `fetch:check` can't read
  that name for its issue-date check, so confirm the issue from the PDF.
- **Immaculate Motherhood LLC sites** link only HTML viewers (`bulletin-view?f=<name>`) around
  `/bulletins/file/<name>`; no recipe reads them. Confirm the bulletin from the viewer's HTML and
  record `unsupported-format` and `fetch_gap` kind `viewer-wrapped-pdf`.
- **Joomla file endpoints** (`/about-us/bulletin/<n>-<title>/file`) answer 403 to `probe get`; a
  `fetch()` in Chrome (`tools/browser_get.py`) returns the PDF. Record `fetch_gap`
  `joomla-file-endpoint`.
- **SermonCloud embeds** keep bulletins as `media.notes` S3 URLs in
  `api.sermoncloud.com/<account>/sermons` (find the call with `tools/net_log.py`). Record
  `fetch_gap` `sermoncloud-api-embed`.
- **HTML-only bulletins** ("No PDF links found"): record `unsupported-format` and `fetch_gap` kind
  `html-only-bulletin` when the page is kept current (St. Stephen, South River).
- **Image-only pages** (any publisher): `probe pdf --grep` reaches only text pages. Render page 1
  (`pdftoppm -r 70 -jpeg -f 1 -l 1`) for the masthead, take the Mass schedule from the parish
  site, and for recheck quote a text page (often the ad-page code line). A text layer can be
  garbage: Bon Venture's unmapped font still leaves the code line (`<code> (CK) · <parish> •
  <town>`) readable; a shifted encoding (`Parish` as `3DULVK`) leaves `fetch:check` date `unknown`.
- **Probe quirks:** `probe url` DEAD-DNS is unreliable here (it said so for live hosts); retry
  with `probe get` and the browser. Its SPAM-SQUAT verdict can come from one word (a "Casino
  Trip"): read the page first. `probe get --out` resolves a relative path from the worktree root,
  so give `scratch/<run>/<job>/…`. `tools/ddg.sh` gets DuckDuckGo's bot challenge; `visit.py
  'https://duckduckgo.com/?q=<words>&ia=web' --links` works.
- **Finder websites and details:** a dead finder domain can redirect to a new site (read its
  id) or be spam while the bulletin still prints it; find the live site by search and confirm it
  by the masthead's address and URL. A finder pin or GCatholic address can be the rectory: check
  the Contact page and masthead.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches in the territory (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Maronite; Syro-Malabar) are excluded as `other-jurisdiction`, as in Allentown, Scranton, Syracuse and Rochester. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A pastor the parish finder lists for two parishes is a lead, not evidence of a shared pastor or a shared bulletin: whether rows share a bulletin is decided from the current bulletins. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A GCatholic church of a merged parish that neither the finder's worship-site list nor the parish's current bulletin names goes to `open/` unless a dated source says it closed; absence from the finder alone is not a closure. (accepted by survey-review, 003-survey-review, 2026-10-30)
- A shrine or shrine chapel with public Mass but no parish of its own and no bulletin is excluded `no-bulletin`, as in Allentown (the Padre Pio Centre, Barto); one that publishes a bulletin or a schedule the pipeline can read gets a parish row. (accepted by survey-review, 003-survey-review, 2026-10-30)
- One bulletin posted both on the parish's own site (eCatholic) and on a publisher's (church-bulletin.org, a ParishesOnline container, Discover Mass or Bon Venture) is one publication: record only the parish-hosted copy, after comparing page-1 renders or `pdftotext` output and the newest dates on both (the parish page can lag the publisher by a week or more), and list both ids (`discovermass:<slug>`, `url:http://sponsors.bonventure.net/?page=<n>`). A parish whose own site only links John Patrick is recorded on John Patrick. (map batches `sayreville-parlin` and `south-amboy-matawan`, 2026-10-30; ParishesOnline added by map batch `plainsboro-south-brunswick`, 2026-11-02; date check by map batch `woodbridge-iselin`, 2026-11-02; Discover Mass and Bon Venture added by map batch `warren-watchung-martinsville`, 2026-11-03) When the parish copy is still more than a week behind the publisher's at a later check, read the publisher instead and keep every id on the row: St. Andrew, Avenel moved to `parishes_online` when its eCatholic page still had 25 October while container 04/1116 had 1 and 8 November. (reconcile, 2026-11-03)
- A parish with no website of its own gets `no_bulletin` with its Discover Mass church page as `website`, since the record needs a URL. (map batch `monroe-jamesburg`, 2026-11-02)
- A Latin church sold to an Eastern Catholic community that now holds Mass there is excluded `other-jurisdiction`, not closed; the merged parish's own history page can date the sale. (map batch `carteret-port-reading`, 2026-11-03)
- A monastery chapel with public daily Mass but no bulletin is excluded `no-bulletin` under the shrine rule above, even when it is in no roster. (map batch `flemington-readington`, 2026-11-03)
- Parishes staffed by one religious community can each print the same combined Mass schedule for all the community's churches: decide rows from mastheads and Bon Venture account codes, and give each church to the row whose masthead it is (the Raritan Oratory, whose raritanoratory.org links each parish's current site). (map batch `raritan-oratory`, 2026-11-03)
- Date evidence `seen`/`checked` by US Eastern time (`TZ=America/New_York date`), not the shell's UTC date: in the evening UTC is a day ahead and `validate` rejects the date as in the future. (map batch `south-plainfield-piscataway`, 2026-11-03)

## Seeding precedents

Seed questions `seed-review` settled that no rule covered: the situation, the choice and the parishes. Later reviews in this diocese follow them; only the owner turns one into a rule.

- The intentions list a 9:00 AM Tuesday Mass both weeks, but the Mass Times box and website skip Tuesday. Add a weekly Tuesday 9 AM Mass? → Leave out. Left out, as leaned. Both issues' Mass Times box (ca85718a p1, 4e52deaa p1: 'Mon., Wed., Thurs., Fri. - 9 AM') and the website skip Tuesday on purpose. The only Tuesday 9 AM evidence is two weeks of intentions, which may be a private Mass. C1 is a candidate rule and doesn't decide this, but the public schedule clearly leaves Tuesday out. (annunciation-bloomsbury s11; 072-seed-review, 2026-11-20)
- Add the First Saturday Holy Hour (a Cenacle hour after the 9 AM Mass) as Adoration, 9:30-10:30 AM? → First Saturdays 9:30-10:30 AM. Included at 9:30-10:30, as leaned. The box (ca85718a p1) says 'First Sat. - 9 AM and Holy Hour', and POLICY counts a Holy Hour as Adoration unless the bulletin says the Sacrament is not exposed, which it doesn't. R10 starts it 30 minutes after the 9 AM Saturday-morning Mass, and 'hour' gives the end. What made it hard: p2 calls it a Cenacle hour (Marian consecration), which may have no exposition. (annunciation-bloomsbury s12; 072-seed-review, 2026-11-20)
- Add the Faith Formation early-session Advent Penance Service (Dec 9, 4:30-5:15 PM)? → Leave out. Left out, as leaned. 59aa4025 p7 labels the 4:30-5:15 session 'Faith Formation Advent Penance Service (early session)', i.e. for the children's program. The public parish service at 6:30 PM the same evening is already recorded (s19). (assumption-of-the-blessed-virgin-mary-hackettstown s20; 072-seed-review, 2026-11-20)
- Which church holds the Tuesday 7 PM Spanish Mass: St. Joseph (schedule box, website) or Sacred Heart (intentions)? → St. Joseph. St. Joseph, as leaned. The schedule box in both issues (e51d96a3 p1, 9f5cc4b4 p1: '7:00pm: Tues. (St. Joseph, Spanish)') and the website ('TUESDAY EVENINGS St. Joseph (Spanish)') agree. Only the intentions say (SH), probably copied from the Wednesday line. (holy-family-new-brunswick s20; 072-seed-review, 2026-11-20)
- Add the website's Monday 7 PM Holy Hour with Adoration at St. Joseph? → Leave out. AGAINST the lean: left out. Only the worship page gives the Monday 7 PM Holy Hour, and no bulletin mentions any Adoration. That page is shown stale: the bulletins contradict its Thursday Hungarian Mass and First Saturday Mass (both excluded in this seed), and it still carries a 2019 Ash Wednesday schedule. R6 says to watch for exactly this, and a wrong time is worse than a missing one. The rule I applied across the batch: a website-only service goes in only when the page otherwise fits the bulletins. (holy-family-new-brunswick s21; 072-seed-review, 2026-11-20)
- Add First Friday Adoration at Sacred Heart after the 8:00 AM Mass (8:30 AM, no end time)? → Leave out. Left out, as leaned. It comes from the same stale page, it is availability only 'while devotees are present', and it has no end. (holy-family-new-brunswick s22; 072-seed-review, 2026-11-20)
- Add the 7:00 PM Confession at the Nov 16 Men's Worship Night (men of the parish invited)? → Leave out. Left out, as leaned. The flyer (60c49def p4) addresses the Men's Worship Night to the parish's men. Confession shares a 7:00 PM block with Night Prayer and Reflection (POLICY, Final source checks: a larger event doesn't time its parts). The date, Nov 16, has also passed. (nativity-of-our-lord-monroe s15; 072-seed-review, 2026-11-20)
- Add the Immaculate Conception holy day Masses (vigil Mon Dec 7 7 PM; Tue Dec 8 9 AM and 12 PM)? → Include. Included (the whole dec8 group), as leaned. The Nov 8 issue (34f2510a p6) pins the date: 'NEXT HOLY DAY OF OBLIGATION ... Tuesday, December 8, 2026'. The standing box (9685f19b p1) gives the parish's own holy-day times: 'Holy Days of Obligation 7:00 pm (Vigil); 7:00, 9:00 am; 12:00 & 7:00 pm'. The website repeats them, with exceptions named only for Christmas and Jan 1. Pairing a schedule with a printed date isn't projecting a date. What made it hard: no issue prints the times right beside the date. (our-lady-of-fatima-piscataway s31; 072-seed-review, 2026-11-20)
- Add Eucharistic Adoration on Monday, December 7, 5-7 PM (a first Monday, while the standing schedule says second Mondays)? → Dec 7, 5-7 PM. Included as a dated exception (R40), as leaned. The flyer (f1e353a1 p6) plainly prints 'December 7th 2026 5:00pm - 7:00 pm'. The second-Monday slot (Dec 14) is unchanged, so if Dec 7 is a misprint, only this one dated entry is wrong. (our-lady-of-peace-north-brunswick s12; 072-seed-review, 2026-11-20)
- Add First Friday Adoration 9 AM–6 PM (Benediction) from the website? → First Fridays 9:00 AM–6:00 PM. Included at 9 AM-6 PM, as leaned. Two pages of the parish's site agree (homepage '1st Friday 9:00 AM to 6:00 PM'; the First Friday page, '6 pm Benediction'), and the site's other times fit the bulletins (Sunday 12:00, holy days). The bulletins can't show it: the Oct 25 box (e4d9adc3 p1, checked) lists no Adoration, and neither issue's week holds a first Friday. Missing: the page says 'following the 9:00 am Mass' while the weekday Mass is 6:45 AM, so maybe a first-Friday 9 AM Mass exists, maybe a stale phrase. (our-lady-of-victories-sayreville s21; 072-seed-review, 2026-11-20)
- First Friday All Night Vigil Adoration: which hours? → Leave out. AGAINST the lean: left out. Both boxes (80eba28c p4, 27f015b7 p4) give the hours of the whole All Night Vigil (9:00PM-2:30AM in one, 8PM-2AM in the other). Exposition is only one part of an order of Mass, Rosary, Scapular, Exposition, Stations and Confessions. POLICY, Final source checks says a larger event's hours don't time its components, and s19 already excludes the vigil's Mass and Confessions for that reason. The two boxes also disagree. (st-ambrose-old-bridge s20; 072-seed-review, 2026-11-20)
- Add a dated 8:30 AM Mass at St. Anthony on Friday, November 27 (website only)? → Leave out. Left out, as leaned. The only evidence is a passing mention in a Rosary notice on the homepage ('following 8:30am Mass note time change'), and no bulletin prints a Nov 27 time. Adding 8:30 without cancelling 7:30 would list two Masses. The Nov 22 bulletin, which update mode reads, should settle it. (st-anthony-of-padua-port-reading s16; 072-seed-review, 2026-11-20)
- Record the Advent Penance Service confessions (Thu Dec 17, 6-7 PM, 'throughout the school') at St. Augustine's? → Dec 17 6-7 PM at the church, note In the school. Included at the church with the note, as leaned. 30c30584 p3: 'Thursday, December 17th, from 6PM to 7PM ... 20 priests throughout the school to hear confessions'. The school cafeteria hosts the breakfast after the 8 and 10 AM Masses (p10), so the school is on the church campus. Missing: no bulletin prints the school's address. (st-augustine-of-canterbury-kendall-park s15; 072-seed-review, 2026-11-20)
- Add the website's Sunday 1:00 PM Adoration (no end time)? → Leave out. Left out, as leaned. Only the website gives it, with no end and no place. Both bulletins' Adoration heading (bfb31847 p1) lists only 'First Friday: 3:45-6:45 pm (October-May)', so the bulletins point against a weekly Sunday Adoration. (st-bartholomew-east-brunswick s18; 072-seed-review, 2026-11-20)
- Add a weekly Sunday 1:30 PM Spanish Mass? → Every Sunday 1:30 PM (Spanish). Included weekly, as leaned. The parish's current Mass Schedule page lists 'Sunday ... 1:30 PM Spanish'. The intentions (2b86ce78 p3) print only Masses that have an intention, so the 1:30 Mass missing on 11/8 and 11/22 is only a missing mention: on 11/15 it had an intention and is listed. (st-cecelia-iselin s38; 072-seed-review, 2026-11-20)
- Record the website calendar's 'No Mass Today' for Friday, Nov 27 (day after Thanksgiving) as a cancellation of the 8:00 AM Mass? → Cancel Fri Nov 27 8:00 AM Mass. Cancellation recorded, as leaned. The parish's own calendar has a dedicated dated event, '- No Mass Today - Friday, November 27, 2026'. It is service-specific and the bulletins say nothing either way. That differs from port-reading s16, where the only evidence was a passing mention. (st-cecilia-monmouth-junction s14; 072-seed-review, 2026-11-20)
- Add Monday 5:00 PM Confession as weekly, given the bulletin says 'MOST Mondays'? → Every Monday 5:00 PM. Included weekly, as leaned. Both issues and the website give 'MOST Mondays at 5:00 PM [see inside for this Monday's schedule]', and both issues confirmed their Monday (5537af85 p5, a5f93f1c p5). Each bulletin states the week's exception, so update mode can record the skipped Mondays. Hard because 'MOST' is hedged availability with no rule. (st-elizabeth-ann-seton-three-bridges s11; 072-seed-review, 2026-11-20)
- The Sunday 10:30 AM Mass is printed '10:30 AM - GYM'. Include it at St. James, noting the gym? → Include, note In the gym. Included at St. James with the gym note, as leaned. Both issues print '10:30 AM - GYM', the intentions list it (20553ec5 p2), and the website gives it as a regular Sunday Mass. The school gym is on the church's own campus (200 vs 184 S. Finley Ave), so it is a room of the parish grounds, not a separate site (POLICY, Churches and chapels). (st-james-basking-ridge s5; 072-seed-review, 2026-11-20)
- OLRF Thursday confession: which time? → 7:00-7:20 PM. 7:00-7:20 PM, as leaned. OLRF's own Thursday notice (e7d36730 p8) lists 'CONFISSOES - 7:00 - 7:20PM / SANTA MISSA - 7:30PM / ADORACAO ... 8:00 PM / GRUPO DE ORACAO ... 8:30PM'. That fits the box's pattern of 20 minutes of confession before each Mass. The p1 box's 'OLRF: Thursday, 8:30 - 9:00 PM' falls in the prayer group's time. (st-john-paul-ii-perth-amboy s42; 072-seed-review, 2026-11-20)
- Add Saturday Adoration after the 8 AM Mass, given only by the website? → Leave out. Left out, as leaned. The page also names a 'Tuesday ... 8:45 AM Mass' that no longer exists (weekday Masses are 7:00 and 8:30), so it is stale. Neither bulletin mentions Adoration, and no end is given. (st-john-vianney-colonia s24; 072-seed-review, 2026-11-20)
- Is the Thursday morning/midday Mass at 12:00 PM, 8:00 AM, or none? → Thursdays 12:00 PM. Thursdays 12:00 PM, as leaned. The Oct 29 intentions (f34e48d9 p7: '11:30AM Adoration 12:00 PM+ Eusebio Guerra') and the website ('Thursday : 12:00 PM English') agree. The box's 'Monday to Friday: 8:00 AM' is the only contrary evidence, and neither week has a Thursday 8 AM intention. (st-joseph-carteret s16; 072-seed-review, 2026-11-20)
- Is the Friday weekday Mass at 8:00 AM (bulletin) or 12:00 PM (website)? → Fridays 8:00 AM. Fridays 8:00 AM, as leaned. The box in both issues and the Oct 30 intentions (f34e48d9 p7: 'FRIDAY October 30th 8:00 AM') agree, and the jury-duty week moved it to 7 AM, not noon. The website's Friday 12:00 PM stands alone. (st-joseph-carteret s17; 072-seed-review, 2026-11-20)
- Add the weekly Thursday 6:00-7:00 PM Holy Hour? → Thursdays 6:00-7:00 PM. Included, as leaned. The Oct 29 intentions (f34e48d9 p7: '6:00 PM Holy Hour') and the website's recurring event ('Holy Hour Thursday, November 19, 2026, 6:00 PM - 7:00 PM Repeats every Thursday Location: St. Joseph Church') agree. The newest issue's Thursday was the disrupted jury-duty week. (st-joseph-carteret s18; 072-seed-review, 2026-11-20)
- Include the Saturday drive-up confessions, 'typically between 10:00 and 11:00 AM'? → Saturdays 10:00-11:00 AM, drive-up. Included, as leaned. Both issues print 'Drive-up Confessions are offered every Saturday morning, typically between 10:00 and 11:00 AM' (4d80c88a p1). It is the parish's only confession time, and the caveat covers occasional funeral and baptism moves. (st-joseph-millstone s11; 072-seed-review, 2026-11-20)
- Immaculate Conception English Mass at St. Joseph: the bulletin's Holy Days line says '7:00 pm Vigil Mass'; the website says December 8, 7:00 AM. Which, if either? → Dec 7 7:00 PM vigil. Dec 7 7:00 PM vigil, as leaned. Both issues' standing line (722b21ab p1, b1c81bf8 p1) prints '7:00 pm Vigil Mass—St. Joseph (English)', and the website dates the holy day Dec 8. Hard because the website's 'Immaculate Conception December 8 : 7:00 AM English' conflicts. It may be the vigil with AM/PM or the day confused (its 7:30 PM Spanish entry matches the bulletin). If the owner trusts the website, switch to option 1. (st-joseph-raritan s13; 072-seed-review, 2026-11-20)
- Add a weekly Friday 9 AM Mass on Fridays other than the first? → Leave out (dated Friday Masses come from each bulletin). Left out, as leaned. The box (4ad515af p1, 'Please check the schedule for Friday Masses') and the website ('For other Fridays check bulletin') both say Friday Masses vary. Each week's dated Friday Mass comes from its bulletin. (st-jude-blairstown s14; 072-seed-review, 2026-11-20)
- Wednesday 7:30 PM Spanish Mass: the bulletin lists it with no season, the website says Labor Day - Memorial Day. Record it with a September-May season? → Wednesdays 7:30 PM, September-May. September-May season, as leaned. The website, which otherwise matches the bulletin line for line, limits the Mass to 'Labor Day - Memorial Day'. Year-round would be wrong all summer, while September-May is off by only a few days at each end. (st-magdalen-de-pazzi-flemington s14; 072-seed-review, 2026-11-20)
- Add Spanish confession after the Sunday Spanish Mass (contact the priest)? → Leave out. AGAINST the lean: left out. The line (ca9b13c6 p2) reads 'CONFESIONES EN ESPAÑOL: _ está dispuesto después de la misa dominical. Por favor comuníquese con él.' It names neither the Mass nor the priest; the name is a blank template field. C5 times confession after a named Mass, but here the 1:30 PM Mass is a guess and the blank name suggests a stale template. A wrong time is worse than a missing one. (st-matthew-the-apostle-edison s16; 072-seed-review, 2026-11-20)
- Is Adoration cancelled on Friday, Nov 27 (day after Thanksgiving)? → Cancelled Nov 27. Cancelled Nov 27, as leaned. The website's Thanksgiving Holiday Schedule (seen Nov 20) is newer than the Nov 15 bulletin's 'closed only on Thursday'. It is holiday-specific ('No Adoration on Thu, Nov 26 and Fri, Nov 27') and also changes Friday's Masses, which s30-s32 already follow. (st-philip-and-st-james-phillipsburg s33; 072-seed-review, 2026-11-20)
- Add the website's 9:00 AM December 8 Mass labelled 'School Mass'? → Include Dec 8 9:00 AM. Included, as leaned. The parish's public holy-day list gives '9:00 AM English School Mass' alongside its other Dec 8 Masses, and nothing limits it to students. POLICY: a Mass held with a school is open unless the bulletin limits it. (st-stanislaus-kostka-sayreville s16; 072-seed-review, 2026-11-20)
- Sunday Spanish Mass: 9:30 at St. Mary's, 9:00 at St. Mary's, or leave out (website puts it at St. John's, not on the church list)? → Sundays 9:30 AM at St. Mary of Mount Virgin. Sundays 9:30 at St. Mary of Mount Virgin, as leaned. The weekend box in both issues (2333c920 p1) lists 'Sunday ... 9:30 a.m. (in Spanish)' under St. Mary of Mount Virgin. St. John the Baptist, where the website puts it, is now listed as Elijah's Promise Soup Kitchen, so the website looks stale. Hard because the intentions give 9:00 for Nov 15 and 22: if a later bulletin's box moves to 9:00, update mode will follow. (visitation-new-brunswick s7; 072-seed-review, 2026-11-20)
- Record the first-Tuesday 7 PM Latin Mass as its own slot? → Leave out: the weekly Tuesday 7 PM Mass already covers it. Left out, as leaned. The first-Tuesday 7 PM Latin Mass is the weekly Tuesday 7 PM Mass in St. Mary's chapel (s26), so a second slot would duplicate it. (visitation-new-brunswick s27; 072-seed-review, 2026-11-20)
- Friday Adoration in St. Mary's Chapel: until 5:30 PM or 6:00 PM? → Fridays 8:30 AM-5:30 PM. Fridays 8:30 AM-5:30 PM, as leaned (C8 lets me lean either way). The schedule box (2333c920 p1: 'Friday from 8:30-5:30 p.m. @ St. Mary's Chapel') gives an explicit clock end. The p4 notice's 6:00 is the outer bound, and ending early is the safer error. (visitation-new-brunswick s30; 072-seed-review, 2026-11-20)
- Add Adoration after the Friday 7 PM Spanish Mass (website only)? → Leave out. Left out, as leaned. Only the website mentions Exposition after the Friday 7 PM Mass, with no end, and the bulletins' Friday Adoration ends at 5:30/6:00. The same site also misplaces the Sunday Spanish Mass (s7). (visitation-new-brunswick s31; 072-seed-review, 2026-11-20)


## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: The date parser now reads a two-digit year after a period, which closed
  `filename-date-misread`: St. Theodore, Port Murray is `other` with `page-pdfs` again, and
  promoted (`fetch_only`). Coverage: directory 91/91 accounted for (85/91 modelled), gcatholic
  123/123 (94/100), worship-sites 25/25 (23/23).

- 2026-11-03: Owner review: the five parishes with a `fetch_gap` are now `bulletin_provider:
  unsupported` (a published bulletin no collector reads yet), which keeps them and their
  churches off the site. Queenship of Mary, St. Charles Borromeo and St. Theodore were `other`
  and came out of the live CSVs; Corpus Christi and St. Stephen, South River were
  `no_bulletin`. Coverage: directory 91/91 accounted for (84 modelled), gcatholic 123/123
  (93/100 modelled), worship-sites 25/25 (23/23).

- 2026-11-03: Reconcile (factory Run metuchen-map-1), after 29 map batches of usually 6 to 8
  roster entries (5 to 16). Coverage: directory 91/91 accounted for (87 modelled; 4 off the site
  as `no_bulletin`), gcatholic 123/123 (96/100 modelled, 23 excluded), worship-sites 25/25
  (23/23). Records: 88 parishes, 103 churches, 24 excluded, 0 open. No merges. St. Andrew,
  Avenel moved from its lagging eCatholic copy to ParishesOnline; the former Corpus Christi
  convent room (Latin Masses) became a church of Corpus Christi; Corpus Christi and St. Stephen,
  South River got `fetch_gap`s. Wrote `separate` reviews for the 56 Bon Venture-host pairs from
  recorded mastheads; audit: 85 candidate pairs, all separate. fetch:check: 82 of 84 rows fetched,
  2 known gaps (Joomla, SermonCloud).

- 2026-10-30: Survey (factory Run metuchen-map-1). Rosters: directory 91 (90 parishes),
  gcatholic 123 (107 Latin, 16 Eastern), worship-sites 25. 29 batches in `batches.json`, first
  `south-river`. No parish, church or exclusion records yet.
