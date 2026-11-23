---
name: Roman Catholic Diocese of Paterson
state: NJ
website: https://rcdop.org
status: promoted
gcatholic: pate0
promoted: 2026-11-07
---

Three counties of northern New Jersey: Passaic (Paterson, Passaic, Clifton, Wayne, West
Milford), Morris (Morristown, Parsippany, Dover, Madison, the Lake Hopatcong towns) and Sussex
(Newton, Sparta, Vernon). It borders the Archdiocese of Newark (Bergen and Essex counties) to the
east and south, Metuchen (Somerset) to the south, the Archdiocese of New York (Orange County) to
the north, and across the Delaware Scranton (Pike, Monroe) and Allentown (Northampton) to the
west. About 105 canonical parishes in twelve deaneries (rcdop.org/deaneries); the chancery is
in Madison. There is no family or cluster system: parishes are single units with their own
pastor, and mergers have been one parish at a time (St. Brendan & St. George, Clifton 2011;
Sacred Heart & Our Lady Queen of the Most Holy Rosary, Dover 2018; Our Lady of Fatima & St.
Nicholas, Passaic 2022; Padre Pio Parish, Paterson, from St. Bonaventure and Our Lady of
Pompei, 12 April 2026; Our Lady of the Valley & Holy Cross, Wayne, undated). Shared
bulletins are most likely where one priest is pastor of two parishes (Sandyston/Montague,
Oak Ridge/Stockholm) and in merged parishes that kept both churches. Paterson, Passaic and
Clifton are dense city parishes with Spanish, Polish, Italian and other language Masses.

## Sources

- **Parish finder (the `directory` roster):** https://rcdop.org/parishfinder, an eCatholic map
  behind Cloudflare (`probe url` gets 403). Read 2026-11-04 in headed Chrome (parish-site-access
  `visit.py --html`, `finder.py`) and `scratch/paterson-map-1/tools/finder_times.py`, which adds
  each site's Mass schedule (`mass_times`) and details text (`notes`). 117 pins. **The pin id is
  the parish's eCatholic site id** where the parish site is on eCatholic (Padre Pio 39965,
  Our Lady of the Valley 11969, St. Stephen Paterson 33773, the sampled Sussex and Morris
  sites), so it is a strong lead for `ecatholic:<id>` (Sacred Heart, Dover is an exception:
  pin 5701, site 25510). The finder carries stale pins: three for Our Lady of Consolation,
  Wayne (11364 and old eCatholic sites 660, 700), two each for Our Lady of Fatima Highland
  Lakes, Holy Spirit Pequannock, St. Catherine of Bologna Ringwood and St. Stephen Passaic,
  separate pins for St. Bonaventure and Our Lady of Pompei beside Padre Pio Parish, the
  pre-merger St. Nicholas Passaic (14090), two schools (Saint Luke Academy, St. Gerard
  Majella School) and Prince of Peace Chapel (William Paterson University campus ministry).
  Its Mass times were current for Padre Pio (matching the parish's own site); its details
  text is decades old (CCD enrollment figures), so don't quote it.
- **GCatholic:** `rosters/gcatholic.json` (key `pate0`), 122 entries with Plus Codes, fetched
  2026-11-04. It omits the cathedral (St. John the Baptist, Paterson) and Our Lady of the Holy
  Angels, Little Falls; keeps St. Casimir, Paterson (closed 2018), Holy Cross, Wayne, Our Lady
  of the Holy Rosary, Dover, St. Nicholas, Passaic and St. George, Paterson as their own
  churches; and lists 6 Eastern Catholic churches (Ruthenian Holy Wisdom Flanders and St.
  Michael cathedral chapel Woodland Park; Ukrainian St. Nicholas Passaic and St. John the
  Baptist Whippany; Melkite St. Ann Woodland Park; Armenian Sacred Heart Little Falls) and
  religious houses (St. Mary's Abbey Morristown, St. Paul's Abbey Newton, Holy Face Monastery
  Clifton, Our Lady of the Holy Spirit Sanctuary Branchville), two shrines (Blessed Miriam
  Teresa, Convent Station; St. Joseph, Stirling) and the FSSP Our Lady of Fatima Chapel,
  Pequannock. Its websites are often old domains.
- **Deanery lists:** https://rcdop.org/deaneries and one page per deanery (`/paterson-1`,
  `/clifton-deanery`, `/sussex-deanery`, ...), read 2026-11-04: 108 parish names in 12
  deaneries. Not imported (no addresses; the finder covers the same parishes). Stale: they
  still list Holy Cross and Our Lady of the Valley, Our Lady of Fatima and St. Nicholas, and
  St. Bonaventure and Our Lady of Pompei separately. Good for the canonical parish count.
- **Priest directory:** https://rcdop.org/priest-directory and https://rcdop.org/order-priests
  (read 2026-11-04): each priest's assignment. Explicit shared pastors: Rev. Wayne Varga,
  "Pastor, Saint Thomas the Apostle, Sandyston and Saint James the Greater, Montague"; Rev.
  Benjamin Williams, "Pastor, Saint Thomas the Apostle, Oak Ridge and Saint John Vianney,
  Stockholm". Rev. Angel J. Torres is administrator of Our Lady of Victories and parochial
  vicar of the cathedral (not a shared pastorate). Order priests: OFM at St. Mary, Pompton
  Lakes (listed as "Pompton Plains") and St. Anthony, Butler; OFM Conv. at St. John Kanty,
  Clifton; FSSP at Our Lady of Fatima Chapel, Pequannock.
- **Closed and merged parishes:** https://rcdop.org/parishes-of-the-paterson-diocese, the
  diocesan historian's chronological list (undated; latest entry the 2022 Passaic merger, so
  it predates Padre Pio). Gives St. Casimir, Paterson "closed in 2018"; St. George, Paterson
  "merged with Saint Brendan in 2011; church taken over by Saint George Syro-Malabar Parish";
  old missions closed decades ago. Says a parish ended, not that a building is shut.
- **Mass times:** the finder above is also the diocese's Mass-times search (Sunday, daily and
  holy-day schedules per pin; 96 of 117 pins carry a schedule). No separate Mass-times page.
- **News:** The Beacon, https://beaconnj.org (WordPress; `/wp-json/wp/v2/posts?search=...`
  works with `probe get`). "New pastor unites Paterson parish during historic merger"
  (2026-09-26) dates Padre Pio Parish to 12 April 2026, both churches open. Its search is
  fuzzy; no pastoral plan or closure list was found there or on rcdop.org.
- **Pastoral plan / closure announcements:** none found (rcdop.org menus, Beacon search for
  merger/closing/last Mass, 2026-11-04).

### Bulletin publishers here

From the survey's sample (2026-11-04: `probe url` on all 116 finder websites, `visit.py
--bulletin` on 12) and the map batches since. Most parishes print with Bon Venture, LPi or
John Patrick, and post the result on an eCatholic site: record the host the site's bulletin
page links, not the printer.

- **eCatholic hosts nearly every parish site,** behind Cloudflare: 95 of 116 sites answer
  `probe url` with 403; `visit.py` loads them. The finder pin id is usually the site id.
  - **visit.py faults:** a Cloudflare "502: Bad gateway" (HTTP5XX) is transient; retry
    minutes later. visit.py can also hang with no output (past 500 s) on a home page while
    the site's `/bulletins` loads at once: visit the bulletin page URL directly, not
    `--follow` from home.
  - **Read the site's menu and the `/bulletins` page's first links before running
    `issues.py`.** The `files.ecatholic.com/<site id>/bulletins/<YYYYMMDD>.pdf` archive
    (`issues.py ecatholic`, no Cloudflare) can be stale (2018–2023 in one batch) while the
    current bulletin is a Bon Venture link at the top of `/bulletins`, an embedded
    ParishesOnline publication, a JPP template link, or PDFs under
    `files.ecatholic.com/<id>/documents/<y>/<m>/` listed on a custom page
    (`/parish-bulletins`, `/parish-updates`). A page titled "Bulletins (up to 2023)" is a
    frozen archive; the top-menu "Bulletins" item may point to a Bon Venture sponsor page
    instead, or there may be no `/bulletins` page at all (then `--follow /bulletins` fails:
    read `--links`). Some sites post no Sunday-dated file: read the real file names.
  - **An archive file never posted answers 403, not 404.** When `/bulletins` stops weeks
    ago, `probe get` on the next Sundays' names confirms the parish hasn't posted.
  - **Empty `/bulletins`** (only "Bulletin" and "Archive" headings, no links): the parish
    posts nothing there, but may still publish weekly on ParishesOnline with no link from
    the site. Run `probe po <name>-church-<zip>` first (an org can also exist with no
    publications; its ids are the ones to use if issues appear) and `issues.py` (Sunday,
    `--day sat`; 403 = not posted); only then record no_bulletin with a revisit.
  - **One bulletin per language** can be posted each week as separate dated files (one
    parish: Friday English, Saturday Polish, Sunday Spanish): run `issues.py` with `--day
    fri` and `--day sat` too, and read each file's language before picking a recipe.
  - **A parish can post on two of its own site ids,** and move between them (and back-fill
    one): compare the `?t=` upload stamps on each site's `/bulletins` links to see which is
    posting now, record every site id carrying issues in publication, and set a revisit.
  - **Documents-folder bulletins:** use a page-pdfs recipe on the listing page. It dates links
    by their label or their URL-encoded file name (`Month%20D%20YYYY.pdf`), so a link with
    neither can lose to an older issue: check the pick's date. On a monthly newsletter listing ("November 2026") the first-listed pick is
    right but fetch:check reports date and freshness unknown: check by hand.
  - **No usable text layer:** some issues are scanned images (no extractable text), some
    shifted by 29 code points (`0$66(6` for MASSES, digits dropped), some broken font
    encoding. `probe pdf` can't give Mass times: render page 1 with `render.py`;
    fetch:check's identity unverified is then expected. The same holds for Bon Venture,
    LPi and John Patrick PDFs below.
  - **One-off covers:** a cover with a non-Sunday date (a pastor's birthday) gives a
    fetch:check issue-date conflict; check page 2 and the previous issue's page 1 before
    calling the pick stale.
  - **`ecatholic:5303` is the Diocese of Paterson's own site,** reported on any parish page
    that links rcdop.org. Don't record it.
- **Bon Venture** (`sponsors.bonventure.net/?page=<n>`, use `http://`; see Scranton and
  Allentown). Its ad footer ("150C (PK) - <parish> ... Bon Venture Services") also appears in
  issues the parish posts as eCatholic `bulletins/` files; that doesn't make Bon Venture the
  host. The footer code (`021C (JA)`) doesn't map to a `?page=<n>` id, and bonventure.net has
  no parish list or search: a sponsor page is found only where a site links it. Seasonal
  covers (All Saints/All Souls) replace the masthead on page 1, on eCatholic-hosted copies
  too: read address and Mass times from the previous week's page 1 or the schedule on page 2.
- **LPi / ParishesOnline:** an eCatholic bulletin page (e.g. `/bulletins-1`) can embed
  `parishesonline.com/publication-page/<org slug>`; record po-org/lpi/po-container from
  `probe po`, not the eCatholic site id. LPi copies carry an ad footer "<parish>, <town>,
  NJ 04-NNNN" (or "<parish> | 03-NNNN"), which gives the container.
  - **Copies on a parish site** (eCatholic `bulletins/`, Squarespace `/s/<YYYYMMDD>B.pdf`):
    try `probe po` on `<name>-church-<zip>` for the org and record parishes_online, not the
    copies. If no org slug is found, keep provider ecatholic and record po-container as a
    publication form, with research to find the org; the container can have next Sunday's
    issue before the copy.
- **John Patrick Publishing:** a `/bulletins` page links
  `jppc.net/onlinebulletins/<customer>template.pdf`, which redirects (HTML, not a PDF) to a
  `church-bulletin.org/<parish-slug>` listing of `bulletin/<slug>/<YYYY-MM-DD>.pdf` issues.
  Record `url:<listing>` and use page-pdfs on it; fetch:check dates the pick from the file
  name. Where the site links only eCatholic copies, the customer number in the footer ("6059
  <parish>, Paterson, NJ John Patrick Publishing") opens the listing via
  `https://church-bulletin.org/?id=<n>`; a guessed slug returns a generic 200 page, not 404.
  The eCatholic copies can lag the listing by weeks while `/bulletins` still looks live:
  whenever the footer gives a customer number, compare the listing's newest date before
  choosing ecatholic.
- **WordPress parish sites** can post one `/bulletin/<month>-<day>-<year>/` post per issue
  with the PDF inside: fetch's dated-post recipe on the listing page picks the current
  issue. `/wp-json/wp/v2/media?mime_type=application/pdf` lists every uploaded issue with
  its upload date, which shows how often the parish posts. Where `/bulletins/` only links
  per-year pages (`/2025-2/`, `/2026-2/`), fetch can't resolve from it: pin page-pdfs on
  the current year's page and set a revisit for early January to repin to the new year's.
- **A fixed Dropbox file** (`dropbox.com/s/<id>/Bulletin.pdf?dl=0`, seen on a Wix site): page-pdfs
  gets Dropbox's HTML preview (not_pdf). Pin `redirected-pdf <same URL>?dl=1`; fetch:check
  then reports date and freshness unknown, so check the masthead date by hand.
- **Next Sunday's issue mid-week is normal here:** fetch:check's freshness `future` (age −4
  days) on the newest file is the right pick; confirm the masthead date.
- **Discover Mass's daily download cap and Paluch joint bulletins** (Scranton, Allentown)
  haven't been seen here yet.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- Eastern Catholic churches (Ruthenian: Eparchy of Passaic; Ukrainian: Archeparchy of Philadelphia; Melkite: Eparchy of Newton; Armenian: Eparchy of Our Lady of Nareg) and St. George, Paterson, now the Syro-Malabar parish (Eparchy of Chicago), are excluded as other-jurisdiction. (accepted by survey-review, 002-survey-review, 2026-11-04)
- A merged parish whose bulletin still lists Mass at both former parish churches is one parish row with both churches (Padre Pio: St. Bonaventure and Our Lady of Pompei). (accepted by survey-review, 002-survey-review, 2026-11-04)
- Church addresses and pins: the finder's and GCatholic's address can be the parish office, and a finder pin the office or a street geocode (one 2.7 km off). Take the church's address from the bulletin masthead, and its location from the OSM building or the GCatholic Plus Code once OSM confirms it. (map batches `randolph-succasunna` and `mount-olive-netcong`, 2026-11-04)
- Two finder pins for one parish are linked to one church: a pin with no address beside one with an address (two domains loading the same eCatholic site; the addressless pin carries the site id), or a pin with only a P.O. Box and an old schedule in its notes (a legacy entry, whose pin is not the church; take coordinates from the Plus Code). Where a Nominatim name search finds no church, a reverse lookup (zoom=18) at the Plus Code coordinates often returns the place_of_worship; Overpass via `probe get` failed. (map batches `northern-passaic` and `west-milford-vernon`, 2026-11-04)

## Seeding precedents

Seed questions `seed-review` settled that no rule covered: the situation, the choice and the parishes. Later reviews in this diocese follow them; only the owner turns one into a rule.

- Is there a Wednesday 8:30 AM Mass? → Only Wednesday Nov 18, 8:30 AM. Newest 43581f4d p2 lists 'Wednesday, November 18 2026 8:30am - Jayda Garcia- Nina Bello' beside the 12:05pm Mass. The Nov 11 8:30 (3e90e7ca p2) was the stated arrangement for the office-closed holiday, so only one week is unexplained, which isn't R35 recurrence. Recorded as a dated Mass; the weekly 12:05 stays. (annunciation-bvm-wayne s16; 082-seed-review, 2026-11-23)
- Add Advent Monday confessions 7-8 PM in December? → Mondays in December 7-8 PM. 43581f4d p4: 'Advent Confessions Every Monday in December'; the website's Holy Hour page gives 7-8 PM. The current bulletin confirms the program, and the times fit. Missing: a time printed in the bulletin itself. (annunciation-bvm-wayne s17; 082-seed-review, 2026-11-23)
- Include the 9 AM Mass on Friday, December 11, part of the parish's paid, registration Advent Celebration for Women? → Leave out. A paid women's event that requires registration. POLICY leaves out a Mass limited to a group, and the flyer names no venue. The weekly Friday 7:30 AM Mass is unaffected. (corpus-christi-chatham-township s21; 082-seed-review, 2026-11-23)
- Add a Thursday 12:00 PM Mass, listed only in the intentions? → Leave out. Hard. Thursday 12:00 PM is in both weeks' intentions (50f8368d p2, edd641af p2), but only under the generic 'Parishioners of Holy Trinity' line that every weekday carries. The p1 box (Wed/Fri) and the website's full weekday list (Mon, Tue noon; Wed, Fri 7:30 PM) both omit Thursday, so R39/C1 read it as a template line. Mon/Tue noon differ because the website confirms them. (holy-trinity-passaic s13; 082-seed-review, 2026-11-23)
- Keep weekly Tuesday 7-8 PM Adoration (page 3 of the newest issue says Thursday)? → Keep Tuesday 7-8 PM. Hard. The newest issue contradicts itself: its p1 box says 'Adoration Every Tuesday evening from 7:00 pm to 8:00 pm' (as do the Oct 25 issue 27313264 p1 and the website), but a new p3 box (bcaa5d02) reads 'Adoration of the Blessed Sacrament ... Every Thursday 7:00 – 8:00 pm'. Kept Tuesday per the lean because three sources agree. The p3 box may announce a move, and the next bulletin should settle it. (our-lady-of-fatima-highland-lakes s12; 082-seed-review, 2026-11-23)
- Add weekly Thursday 7-8 PM Adoration (page 1 and the website say Tuesday)? → Leave out. The Thursday box appears once (bcaa5d02 p3), against p1 of both issues and the website. Answered the same way as s12; if Adoration moved, swap the two. (our-lady-of-fatima-highland-lakes s13; 082-seed-review, 2026-11-23)
- Add the website's Monday 7-8 PM Confession? → Leave out. The bulletins' Reconciliation line gives only 'Saturdays 3:30 - 4:00 pm' (bcaa5d02 p1). The website's Monday 7-8 PM sits beside the Dec 8 holy-day entry and may be a one-time service. (our-lady-of-fatima-highland-lakes s14; 082-seed-review, 2026-11-23)
- Add Adoration in the chapel Monday to Saturday 8:30-9:00 AM, after the 8 AM Mass, given only by the website? → Mon-Sat 8:30-9:00 AM. Homepage widget: 'Adoration Times M S a 8:30 AM to 9:00 AM Join us in the Chapel immediately after the 8am Mass.' 'M S a' is the same widget's garbled 'Mon Sat', and the Mass it follows is Mon-Sat 8:00 (16a89f74 p6). The widget is current (it lists December 8). R6. (our-lady-of-good-counsel-pompton-plains s17; 082-seed-review, 2026-11-23)
- Does the weekly Wednesday 7 PM Spanish Mass, followed by Exposition, continue? → Leave out. Nov 8 issue 03440903 p9: 'Misa semanal los miércoles a las 19:00 h, seguida de la Exposición'. The newest, 16a89f74 p9, replaces that line with 'Hora Santa Segundo miércoles de mes'. No Wednesday 7 PM is in the intentions, and the website's Spanish page gives only Sunday 1 PM. This is a change. (our-lady-of-good-counsel-pompton-plains s23; 082-seed-review, 2026-11-23)
- Thursday Adoration ends at 6:45 PM (bulletin) or 6:30 PM (website)? → Thu 8:00 AM-6:45 PM. Both bulletins print Thursday 8:00 am – 6:45 pm. The website's 6:30 PM is the only other source; the bulletins are newer and repeated. (our-lady-of-lourdes-paterson s12; 082-seed-review, 2026-11-23)
- Monday evening Adoration: the schedule box says 7-8 PM in the Chapel (85 Whippany Rd, not listed), but the weekly calendars put it in the Church (Nov 9 at 6-7 PM, Nov 16 at 7-8 PM). Include it weekly at the Church? → Mondays 7-8 PM at the Church. The box (1366c786 p1) says 'Adoration of the Blessed Sacrament (Chapel) Monday 7:00-8:00 PM', but both weekly calendars put it in the Church ('Monday, November 16 - 7:00-8:00 PM: Eucharistic Adoration (Church)' 1366c786 p2; Nov 9 6:00-7:00 PM Church, 696adc5a p2). Two consecutive weeks in the Church read as a move. The time comes from the box and the newest calendar. Hard because the standing box still says Chapel. (our-lady-of-mercy-whippany s15; 082-seed-review, 2026-11-23)
- Add website-only Adoration, 12:00-3:00 PM in the church, on every day? → Leave out. Only the website's Adoration tab gives this: no day, and labeled 'Perpetual' yet 12:00-3:00 PM. Neither bulletin (Nov 8, Nov 15) mentions Adoration. The days and whether it continues are unknown. (our-lady-of-the-holy-angels-little-falls s17; 082-seed-review, 2026-11-23)
- Is the Wednesday, November 18, 7:00 PM Mass (intentions only, incl. 'Deceased members of KOC Marquette 588') a public Mass to list? → Include the dated Mass. 40961e3d p2: 'Wed. 11/18 ... 7:00 Spec. Int. Ryan Peach / Deceased members of KOC Marquette 588'. A dated evening Mass at the parish church with several intentions. The Nov 11 intentions (e617f58d p2) have no evening Mass, so it is dated, not weekly. (our-lady-of-the-lake-sparta s16; 082-seed-review, 2026-11-23)
- Add daily Adoration in the St. Carlo Acutis Adoration Chapel (2nd floor of the parish office), 8 AM-8 PM? → Daily 8 AM-8 PM in the chapel. e617f58d p5: 'St. Carlo Acutis Adoration Chapel (2nd floor of the parish offices) Days: Monday through Sunday Hours: 8:00 AM-8:00 PM'; the website homepage says 'Adoration Hours: Daily, 8 AM-8 PM'. R38: a chapel on site with current hours. (our-lady-of-the-lake-sparta s17; 082-seed-review, 2026-11-23)
- Saturday confession: 4:30-5:00 PM (homepage) or 4:15-4:45 PM (reconciliation page)? → Saturdays 4:30-5:00 PM. The homepage gives 'Reconciliation Times Saturday : 4:30 PM to 5:00 PM In the Church' beside this week's events and Mass times that match the bulletin. The 4:15-4:45 is in a religious-ed note whose dates may be from an earlier year. Missing: any bulletin confession time. (our-lady-of-the-magnificat-kinnelon s12; 082-seed-review, 2026-11-23)
- Add First Friday Adoration in the chapel, 8:45 AM (after the 8:15 Mass) to 5:00 PM with Benediction? → First Fridays 8:45 AM-5:00 PM. Website: 'Adoration begins after the 8:15am Mass on the First Friday of the month and continues throughout the day, ending with Benediction at 5pm.' R10 sets the start at 8:45. The homepage's other content matches the newest bulletin. R6. (our-lady-of-the-magnificat-kinnelon s13; 082-seed-review, 2026-11-23)
- Is the Monday 7-8 PM Holy Hour weekly from September to May, like the Monday Confession it goes with? → Mondays 7-8 PM, Sept.-May. Both weekly calendars carry 'Holy Hour & Confession' Monday 7-8 pm, and the box gives the Monday confession as 'Sept. - May' (b0003821 p1). The Holy Hour goes with it. (our-lady-of-the-mountain-long-valley s18; 082-seed-review, 2026-11-23)
- Add Confession after each weekday Mass, on request ('after daily Mass, ask the priest')? → Weekdays 10:00 AM, on request. b0003821 p1 Reconciliation: 'First Saturday: 9:00 - 10:00 am, or after daily Mass, ask the priest.' Included per C5 at R10's time, 10:00 AM after the 9:30 Mass. (our-lady-of-the-mountain-long-valley s19; 082-seed-review, 2026-11-23)
- Include the Sunday, November 15 5:00 PM Mass that appears only in the intentions? → Leave out. Only '5:00pm Private Intention' (b0003821 p2), with no Sunday 5 PM in the Mass Schedule. It reads as a private Mass (C1). (our-lady-of-the-mountain-long-valley s24; 082-seed-review, 2026-11-23)
- Saturday confession before the 5 PM Mass: which time? The website gives two. → Sat 4:30-4:45 PM. Neither bulletin prints a confession time. The website's widget (4:30-4:45) and Schedules page (4:00-4:45) overlap at 4:30-4:45, which both support. (our-lady-star-of-the-sea-lake-hopatcong s10; 082-seed-review, 2026-11-23)
- Add the Confession at the Nov 28 Advent Mini Retreat (10:15 AM)? → Nov 28 10:15 AM. 49b00228 p6: Advent Mini Retreat, 'Saturday, November 28th' ... '10:15 am Quiet Reflection & Confession'. 'Please join us'. The registration is check-in at the church vestibule with a free-will donation, so the retreat is open. Nov 28 2026 is a Saturday, so the '2025' is a typo. (sacred-heart-clifton s23; 082-seed-review, 2026-11-23)
- Add the website's Monday 7-8 PM confessions? → Leave out. Against the lean. Both bulletins (b9ab31d9 p1, 03e02641 p1) say 'CONFESSIONS Saturday 9:00 am. Other times by appointment'. The website's Monday 7-8 PM names no church, and its only note is Lenten ('no confessions Monday March 9th due to the Lenten Retreat'). It would also overlap the Monday 7 PM Spanish Mass, so it reads as a Lent schedule left on the site. The lean placed it at Sacred Heart only by inference (R32). (sacred-heart-holy-rosary-dover s24; 082-seed-review, 2026-11-23)
- Add the perpetual Adoration chapel at Holy Rosary, which needs registration and an access code? → Leave out. b9ab31d9 p1: 'PERPETUAL ADORATION Held at Our Lady Queen of the Most Holy Rosary. Call to register'; the website says 'Call office to register and receive access code'. Not open to walk-in visitors. (sacred-heart-holy-rosary-dover s25; 082-seed-review, 2026-11-23)
- Keep the Friday Holy Hour after the 8:30 AM Mass (9:00 AM), printed only in the older issue's schedule box? → Fridays 9:00 AM. Nov 8 issue 4e367ed6 p1: 'Holy Hour & Exposition of the Blessed Sacrament: Every Friday ... Following the 8:30 AM Mass'. The newest, 11e71d2b, is a Fall Festival issue without the schedule box, so its silence isn't a change. R10 gives 9:00 AM. The same call as st-mary-denville s18. (st-ann-parsippany s13; 082-seed-review, 2026-11-23)
- Keep Saturday Confession at 4:00 PM, printed only in the older issue's schedule box? → Saturdays 4:00 PM. 4e367ed6 p1: 'Celebration of Reconciliation: Every Saturday ... 4:00 PM'. The newest is the festival issue without the schedule box, the same omission as s13. (st-ann-parsippany s14; 082-seed-review, 2026-11-23)
- Include weekday Confession after the 12:05 PM Mass (on request to the priest) at 12:35 PM? → Mon-Fri 12:35 PM, after the 12:05 PM Mass. Both bulletins (fdc6d123 p2): 'PENANCE Available on weekdays after the 12:05 pm Mass. Please inform the officiating priest'. C5: included at R10's 12:35 PM. (st-christopher-parsippany s11; 082-seed-review, 2026-11-23)
- Add the Knights of Columbus' second-Tuesday 6:30 PM Adoration & Benediction at St. Thomas? → Leave out. Against the lean. 11295d5a p4: 'The Knights of Columbus ... meets every second Tuesday of the month in the Father Lewis Center. The meeting starts at 7 p.m. preceded by Eucharistic Adoration at 6:30.' It is presented as the opening of a council meeting, and the calendar's 'STC' code also covers that meeting in the Lewis Center, so it is a members' event at an unclear venue (R32). (st-james-st-thomas-montague s14; 082-seed-review, 2026-11-23)
- The schedule box lists 'Spanish: 7:00 pm' under Weekend Masses without a day. Add it, and on which day? → Sunday 7:00 PM. Hard. d027577d p2 box under 'Weekend Masses': Saturday 5:30 pm; Sunday 8:00, 10:15, 12:00; 'Polish: 9:00 am' (a Sunday Mass, per the website); 'Spanish: 7:00 pm'. The line follows the Sunday lines, so Sunday is the best reading. Missing: the printed day, and any intention or website mention. (st-joseph-lincoln-park s17; 082-seed-review, 2026-11-23)
- Add the youth ministry's Monday, November 16, 6:30 PM 'Mass & Bagels'? → Leave out. A youth-ministry flyer for 'Mass & Bagels' with no place given; the Monday intentions (p1) list only the 9:00 am Mass. It reads as a youth gathering, and the date has passed. (st-joseph-mendham s13; 082-seed-review, 2026-11-23)
- Add Adoration after the Saturday 5:00 PM vigil Mass (6:00 PM by POLICY)? → Saturdays 6:00 PM. Both bulletins, p1: 'Adoration of The Most Blessed Sacrament After each Mass on the weekends'. That covers the Saturday 5:00 PM vigil, and POLICY, Times puts it at 6:00 PM. The website listing only Sunday is a missing mention (R6). (st-joseph-newton s17; 082-seed-review, 2026-11-23)
- First-Friday Adoration and Benediction: which start time? → First Fridays 12:30-3:00 PM. The bulletins name first-Friday Adoration (R12). The standing Mass Times page says 12:30 PM to 3:00 PM. The event page's 12:35 comes with 'Mass at 12:05pm', which contradicts the bulletin's 12:15 Mass. (st-joseph-newton s18; 082-seed-review, 2026-11-23)
- Does 'Daily: 15 minutes before Mass' confession include the Saturday 7:00 AM Mass (6:45-7:00 AM)? → Saturdays 6:45-7:00 AM. Box (37466dde p2): Confession 'Daily: 15 minutes before Mass'. The Saturday 7:00 AM Polish Mass is a morning daily Mass listed apart from the vigil, so 'daily' covers it. (st-joseph-passaic s22; 082-seed-review, 2026-11-23)
- Does 'Daily: 15 minutes before Mass' confession include the third-Friday 6:00 PM Mass (5:45-6:00 PM)? → Leave out. The first-Friday 6 PM Mass gets its own confession window, so 'Daily' means the regular morning Masses. POLICY, Times: a general before-Mass line doesn't cover a monthly special Mass. (st-joseph-passaic s23; 082-seed-review, 2026-11-23)
- Is the 6:30 PM Healing Mass a monthly second-Wednesday Mass, or record only the announced December 9 one? → Second Wednesdays 6:30 PM. Dated notices for Nov 11 and Dec 9, both second Wednesdays, announce a 6:30 PM Mass with healing prayers, and the devotions box gives 'Prayers for healing 2nd Wednesday of month 6:30 PM'. Two consecutive months fit a monthly Mass (R12). (st-joseph-passaic s24; 082-seed-review, 2026-11-23)
- The Nov 15 bulletin's intentions list Wednesday Nov 18 Mass at 8:00 AM, while its schedule box says Wednesdays 8:30 am. Add a dated 8:00 AM Mass on Nov 18? → Dated Mass Wed Nov 18 8:00 AM (weekly 8:30 kept). 3fe81c15 p2 lists Wed Nov 18 at 8:00 AM against the box's Wednesday 8:30. R17/R40: record the dated listing and keep the weekly 8:30, with no cancellation printed. The date has passed. (st-jude-the-apostle-hamburg s8; 082-seed-review, 2026-11-23)
- Saturday confession: 4:00-4:45 PM (bulletins) or 4:00-4:30 PM (website)? → 4:00-4:45 PM. 0c9514fb p1 (image) and the Nov 8 issue print 'Saturday (4:00-4:45 pm)'; only the homepage says 4:30. The bulletin is printed weekly. (st-lawrence-the-martyr-chester s22; 082-seed-review, 2026-11-23)
- Cancel Adoration in Thanksgiving week (Thu Nov 26 - Fri Nov 27)? → Cancel those dates. The homepage schedule says 'There will be no adoration during the week of Thanksgiving.' The chaplet 'during Adoration' on Nov 26 looks like a recurring event template, not a dated notice. (st-lawrence-the-martyr-chester s29; 082-seed-review, 2026-11-23)
- Add Monday Exposition after the 8:00 AM Mass (8:30 AM, no end time)? → Mondays 8:30 AM. Nov 8 issue 618aa6ab p1: 'Exposition Mondays following the 8:00 am Mass'. The newest issue has a feast-day cover and no schedule box, so its silence isn't a change. R10 gives 8:30 AM. The same call as st-ann-parsippany s13. (st-mary-denville s18; 082-seed-review, 2026-11-23)
- First Friday Nocturnal Adoration: the sources give 9 PM-2 AM (bulletin), 9 PM-3 AM (website home) and 8 PM-2 AM (ministry page). Which? → First Fridays 9 PM-2 AM. Nov 8 issue 618aa6ab p1: 'Nocturnal Adoration First Friday, 9:00 pm to Saturday 2:00 am'. The website pages give 9pm-3am and 8pm-2am. The bulletin agrees with each page on one end, so its hours are the best-supported (C8). (st-mary-denville s19; 082-seed-review, 2026-11-23)
- Saturday confession: 3:30-4:30 PM or 3:30-4:00 PM? → 3:30-4:30 PM. The newest cover box (9592856f p1) and the website give 3:30-4:30; the 3:30-4:00 on p2 is a repeated inside line. The start is the same either way (C8). (st-michael-netcong s12; 082-seed-review, 2026-11-23)
- Add weekday confession after the 10 AM Mass (website only)? → Leave out. Both bulletins say daily confession is by appointment. Only the website offers it after the 10 AM Mass, and the bulletins are the newer, service-specific source. (st-michael-netcong s14; 082-seed-review, 2026-11-23)
- Add weekday Adoration from the website (not in either bulletin)? → Mon-Fri 10:30 AM-7:00 PM. Website: 'Adoration Weekdays 10:30am - 7:00pm'. Its paragraph adds the Thursday Church exposition 'will conclude at 7 PM with a Solemn Blessing' and 'a Solemn Blessing ... in the chapel every Monday, Tuesday, Wednesday, and Friday at 6:45 PM'. That supports 7:00 over the widget's 7:30. The site is current (2026 appeal, matching Mass times). R6/R38. (st-michael-netcong s20; 082-seed-review, 2026-11-23)
- First Friday Adoration 8:30 AM-7 PM is 'Except during the Summer months'. Which months count as summer? → September through June (no July, August). Both boxes say 'Except during the Summer months' without naming them. July-August is the usual parish summer, and the Dec 4 flyer shows it running now. Missing: the months; the choice matters only next June. (st-paul-clifton s16; 082-seed-review, 2026-11-23)
- Dec 12 lists '5:00 am Mañanitas' among the Guadalupe feast Masses. Is it a Mass? → Leave out (Mañanitas is the dawn serenade, not a Mass). '5:00 am Mañanitas' is the traditional dawn serenade to Our Lady, followed by a 7:00 Mass. Not called a Mass. (st-paul-clifton s24; 082-seed-review, 2026-11-23)
- Wednesday 1 PM Adoration: the bulletins add 'See you in September.' Include it as running now? → Wednesdays 1:00-2:00 PM. Both bulletins print Wednesday 1 pm Adoration with a leftover 'See you in September', and September is past. The website lists Wednesday 1:00-2:00 PM with no pause. R6. (st-rose-of-lima-east-hanover s17; 082-seed-review, 2026-11-23)
- Add the Nov 18, 7:00 PM Knights of Columbus Mass of Remembrance, and where? → Leave out. The intentions give no church for the line, unlike the other Wednesday lines (R32). It is a Knights' memorial Mass with no open invitation, and the date has passed. (st-thomas-st-john-oak-ridge s24; 082-seed-review, 2026-11-23)
- Wednesday weekday Mass: 12:10 PM (schedule box, website) or 9:00 AM (intentions both weeks)? → Wednesdays 12:10 PM. Hard. The p1 box (e57a5f3b, image) lists each weekday separately, with 'Wednesday | 12:10pm', and the website agrees. The p3 intentions give 'Wednesday - November 18 9:00am | Kathy Gast' and Nov 11 9:00am (Veterans Day). Kept the standing schedule. The named Wednesday 9:00 intentions two weeks running may be a real change, so the next bulletin should be checked. (st-virgil-morris-plains s9; 082-seed-review, 2026-11-23)


## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-07: The date parser now reads URL-encoded file names, which closed
  `undated-link-label`: Notre Dame of Mt. Carmel, Cedar Knolls is `other` with `page-pdfs`, and
  promoted (`fetch_only`). Coverage: directory 117/117 accounted for (107/114 modelled),
  gcatholic 122/122 (102/109). 0 `unsupported` rows.

- 2026-11-05: Reconcile (factory run paterson-map-1, 30 map batches of 6-12 roster entries,
  usually 8). Coverage: directory 117/117 accounted for (106/114 modelled), gcatholic 122/122
  (101/109); one church in no roster (Carnevale Center, Pompton Lakes, from the bulletin). 105
  parish rows (7 `no_bulletin`, 1 `unsupported`), 111 churches, 16 exclusions, 1 `open/`
  (Our Lady of Fatima church, Passaic, still undecided). No merges and no moves: audit --fetch
  found no candidate pairs, the St. Mary's Abbey row stands, and nothing read puts St. Michael,
  Paterson under the Cathedral. fetch:check on 97 rows: all downloaded. Not current: Holy Spirit
  Pequannock (the site posts LPi copies 1-3 weeks late), Highland Lakes, Ringwood, Sts. Cyril &
  Methodius Clifton and St. Rose East Hanover (1 November not yet posted), Branchville and
  St. John Kanty (nothing since 11 October).

- 2026-11-04: Survey (factory run paterson-map-1). Created the diocese; rosters `gcatholic`
  (122) and `directory` (117, the eCatholic parish finder with Mass times); planned 30 batches
  in `batches.json`. No parish records yet.
