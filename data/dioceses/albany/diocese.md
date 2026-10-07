---
name: Roman Catholic Diocese of Albany
state: NY
website: https://www.rcda.org
status: promoted
gcatholic: alba4
promoted: 2026-10-07
---

Fourteen counties of eastern New York: Albany, Schenectady, Rensselaer, Saratoga, Warren,
Washington, Columbia, Greene, Montgomery, Fulton, Schoharie, Otsego, most of Delaware and
part of Herkimer. The diocese describes itself as "126 parishes, four apostolates, and 157
worship sites". Explored in full on 2026-09-28 in nine regions, one agent each, followed by
a cross-region pass. Every entry of the diocese's Find A Parish list and of GCatholic's list
is now a church, an exclusion or an open question. See the *Log* for the numbers.

## Sources

- **Find A Parish list (the directory roster):** https://www.rcda.org/parishes/parish
  (also served at `/offices/pastoral-planning/find-parish`). Plain HTML, no Cloudflare. It
  has one entry per worship site or apostolate (148 on 2026-09-28). Each links a detail page
  `rcda.org/parishes/parish/<slug>` giving the address, phone, a "Visit Our Website" link, an
  "Other Worship Sites" box (the diocese's own grouping of sites under one parish) and often
  the Mass schedule. Scraped into `rosters/directory.json`: `notes` holds the start of each
  page's text, `other_sites` the grouping. No coordinates.
  - **Mass times are often stale.** Holy Spirit, East Greenbush; IC Glenville; Fatima
    Delanson; Cobleskill; Stamford; Margaretville; St. Cecilia, Fonda; the Cohoes parishes;
    and others differ from the current bulletin.
  - **Website links are often dead or moved.** holyspiritchurcheg.org is now hsceg.org;
    stmaryscrescent.org is now .com; christ-our-light.org and churchofstambrose.org are
    DEAD-DNS; St. Joseph, Troy's link is a 404; Mater Christi's is malformed.
  - **Some entries are duplicates or offices.** directory:343 is an old entry for St. Peter,
    Stillwater. directory:768 is the Mechanicville parish centre, which has a chapel with
    Thursday Mass.
- **GCatholic:** `rosters/gcatholic.json` (key `alba4`), 163 entries with Plus Codes.
  - **It omits the cathedral.** The cathedral's coordinates are ParishesOnline's point.
  - **It includes eight Eastern Catholic churches:** Ukrainian, Ruthenian and Maronite.
  - **Some entries are former churches:** Lexington's is marked "(now secular)", Hunter's
    "(now not in use)".
  - **Some addresses are wrong.** A few Plus Codes land on the wrong building: Annunciation,
    Ilion and St. Peter, Delhi, where OSM was used instead. Stamford's ZIP is mistyped
    "1890".
- **Institutional (sacramental) records index:**
  https://www.rcda.org/parishes/institutional-records. It lists, town by town, each closed
  or merged parish and the parish that now holds its records. That says a *corporation*
  ended, never that a building is shut. Several of its rows link to trashed rcda.org pages
  (`/!trash/...`), which a flattened text copy loses. About 60 closed parishes in the index
  are in neither roster and in no current bulletin. They were not given records: nothing
  places a building with Mass for them in 2026. They are listed as leads in the successor
  parishes' *Worship sites*.
- **The Evangelist** (evangelist.org), the diocesan paper, dates closures, for example St.
  James, North Creek (closing Mass 27 October 2024).
- **Times Union** and the **Daily Gazette** (dailygazette.com) date Albany and Schenectady
  closures (Sacred Heart, Albany; St. Mary, Schenectady). The **Schenectady County
  Historical Society church list** (schenectadyhistory.org/churches/directory.html) is a third
  address source for Schenectady and marks closures "[CLOSED]".
- **Reorganization** (rcda.org/reorganization) is the diocese's Chapter 11 bankruptcy (filed
  15 March 2023, settlement 27 March 2026), not a parish restructuring.
- **Integrated Diocesan Map:** https://maps.topographics.org/hosted/rcda (not read).

### Bulletin publishers here

Of the 87 parish rows, 37 are ParishesOnline, 16 eCatholic, 6 Discover Mass and 28 `other`:
self-hosted pages, the diocese's parish mini-sites, Wix, Weebly, WordPress and Google Sites.

- **Some ParishesOnline bulletins are printed into two containers.**
  - The Cathedral and Historic St. Mary's publish one bulletin through 03/0408 and 04/0782.
  - St. Clare and Christ Our Light publish one bulletin through 03/1389 and 03/1011.
  - The editorial pages are identical and only the ad page differs, so the file hashes
    differ. Both sets of ids are on the one row.
- **Finding a parish's ParishesOnline organization.** Parish sites often don't link it.
  Search the web (`site:parishesonline.com` plus the name), or guess the slug
  `<name>-<zip>` against the API (e.g. `st-cecilia-church-12068`,
  `sacred-heart-church-12845`). The API's `organizations?search=` ignores its argument.
- **parishes.rcda.org/<Name>/** hosts small diocese-built parish sites (Our Sunday Visitor
  templates). There are about fifteen: Delanson, Middleburgh, Morris, Sidney, Worcester,
  Nassau, St. Anthony Troy, St. Jude, St. Francis Albany, Holy Mother and Child, Fort Edward,
  Johnstown, Broadalbin and others.
  - **File names:** `bulletin.php` lists `bulletins/<YYYY>/<Month>_<DD>[@<Sunday name>].pdf`.
    The `@` suffix can be wrong.
  - **Some sites overwrite one file** (`bulletin.pdf`) instead; one had not changed since
    March 2020 (New Lebanon).
  - **HTTPS resets about one request in three.** Retry, or use http.
  - **Next Sunday's issue often posts late.**
- **Image-only bulletins are common, about one in five.**
  - ParishesOnline: 03/0820 (Together in Unity), 03/0807 (St. Ambrose), 04/0246 (St. Thomas,
    Delmar), 03/0420 (Fort Edward), 03/0901, 04/0815, 03/0292, 04/0926, 04/0527 and 04/0808
    (Mater Christi); and 04/0923's page 1.
  - eCatholic: 33341 (St. Mary, Amsterdam) and 11351 (St. Vincent de Paul, Albany).
  - Self-hosted: Holy Spirit and Holy Trinity (Gloversville/Johnstown) and St. Anthony, Troy.
  - They were read with `render.py`; the pipeline will have to read them as images.
- **Some text layers are broken.** Annunciation/OLQA, St. Mary Waterford and St. Clement's
  are letter-spaced or split words. Holy Trinity, Hudson (03/0174) sets am/pm in a symbol
  font. Quotes copy the text as extracted.
- **Formats the `other` resolver was taught for Albany (28 September 2026):**
  - **Google Drive files:** St. Lucy/St. Bernadette, Altamont and St. John the Baptist,
    Walton link one Drive *file* per Sunday, not a folder. The files download from
    `drive.google.com/uc?export=download&id=<id>`. Walton's site is also behind a
    SiteGround captcha.
  - **rcda.org download links:** St. Joan of Arc's issues are `download_file/view/<n>`
    links that redirect to the PDF.
  - **Year folders:** parishes.rcda.org's `2025/September_28.pdf` is last year's.
  - **Listings oldest first:** St. Joseph, Troy and Our Lady of the Americas list their
    issues oldest first.
  - **A stale first bulletin page:** Northern Points' "Bulletins" is a 2017 page beside
    "2026 Bulletins".
  - **An undated "Bulletin" link after other PDFs:** St. Mary, Glens Falls's single
    rolling Wix PDF.
- **Still unread in the sandbox:** Holy Family, Little Falls (eCatholic 28690) uploads its
  bulletins as documents under `/documents/<y>/<m>/`, listed on `/2026-bulletins`; its
  `/bulletins` page is empty. As `other`, the resolver should follow the homepage's "Holy
  Family & St. Joseph Bulletin" link there. Cloudflare blocked every fetch-check load of
  it, so that is untested.
- **Some parish sites link a weekly worship aid that looks like a bulletin**
  (stpetersaratoga.com, stedwardsny.org). The real bulletin is in the LPi widget on the same
  page.
- **Sites that need a real browser.** Many eCatholic sites are behind Cloudflare; `visit.py`
  got through for all but transfigurationparish.net. The Northern Points Weebly site answers
  without Cloudflare at blessedsacramentbolton.org. Wix and Weebly file hosts answer 429 to
  rapid `probe pdf`; space the requests.

## Rules settled for this diocese

- **Shared pastors don't make shared bulletins.** Roughly twenty priests serve two or three
  parishes that each publish their own bulletin; each is one row per bulletin actually read,
  recorded under a `group` where `audit` should keep checking them.
  - Fr. Resila: Amsterdam, Hagaman, Fonda.
  - Fr. Busch: Lake George, Queensbury, Warrensburg.
  - Fr. Mijas: Margaretville, Stamford.
  - Fr. Carlino: St. Anthony and St. John the Evangelist, Schenectady.
  - The Cohoes pair.
  - Blessed Sacrament and the Our Lady of the Americas shrine.
  - All Saints and Mater Christi.
  - The Saratoga Springs, Delmar/Altamont/Voorheesville, Round Lake/Mechanicville and
    Clifton Park/Crescent groups.
- **Rows that share one bulletin:**
  - St. Stanislaus + Mt. Carmel, Amsterdam.
  - Holy Spirit (Gloversville) + Holy Trinity (Johnstown).
  - The Cathedral + St. Mary's.
  - St. Clare + Christ Our Light.
  - Holy Spirit + Sacred Heart, East Greenbush/Castleton.
  - St. John & St. Joseph + St. Mary, Rensselaer.
  - St. Jude + St. Michael.
  - OLV Troy + the Grafton mission.
  - Walton/Delhi/Downsville.
  - The Battenkill cluster (Hoosick Falls, Cambridge, Salem), under
    `immaculate-conception-hoosick-falls`, whose masthead names Immaculate Conception alone.
  - Notre Dame-Visitation, Schuylerville + St. Joseph, Greenwich.
- **Saratoga Springs stays two rows.** St. Clement's Discover Mass bulletin is now headed
  "The Catholic Community of Saratoga Springs" and prints St. Peter's Masses too, but St.
  Peter's own container 03/1111 is live. `revisit` is on St. Peter's.
- **Ravena stays its own row** in the Hudson Valley Vicariate West network: it posts its own
  edition. Recheck after the new pastor starts on 10–11 October 2026.
- **Apostolates:**
  - **Black Catholic:** linked to the St. Joan of Arc church, whose bulletin it shares.
  - **Spanish:** linked to the Our Lady of the Americas shrine, its Sunday Spanish Mass and
    bilingual bulletin.
  - **Vietnamese:** linked to its listed address, Sacred Heart, Albany (open).
  - **Korean:** excluded as `no-bulletin`. There is Sunday Mass at 17 Exchange St., but it
    posts only a weekly .pptx on a Daum forum.
- **Eastern Catholic churches** in GCatholic's list are `other-jurisdiction` (eight).
- **An open church whose only published schedule is page text, or a years-old bulletin,** is
  `no-bulletin`: New Lebanon, Stephentown, Cherry Valley, Rosa Mystica shrine (Edmeston), St.
  Pius X (Loudonville), the Korean community. It is never `closed`.
- **Summer chapels and mission churches with no Mass in any current bulletin** are open
  questions with a dated revisit, not closures: Hague, Lake George's St. Mary's of the Lake,
  Lake Luzerne, Ashland, Elka Park, Berlin, Stottville. Nothing in hand states that any of
  them closed.

## Log

- 2026-09-28: Explored the whole diocese. Scraped the diocese's Find A Parish list into
  `rosters/directory.json` (148 entries) and fetched GCatholic's (163). Split both by county
  into nine regions and researched them in parallel, then did a cross-region pass: St.
  Joseph, Greenwich went from `no-bulletin` to a church once the Schuylerville bulletin was
  found under its Discover Mass page, and Cambridge and Salem were put under the Hoosick Falls
  (Battenkill) bulletin.
  - **Result:** 87 parish rows (37 ParishesOnline, 28 other, 16 eCatholic, 6 Discover Mass)
    and 142 churches.
  - **Exclusions:** 18 — 8 other-jurisdiction, 6 no-bulletin, and 4 closed (St. James,
    North Creek 2024; St. Mary, Schenectady 2009; Hunter; Lexington).
  - **Open questions:** 8.
  - **Coverage:** directory 148/148, GCatholic 163/163. `audit`: every group spanning rows
    has separate bulletins recorded.
  - **Promoted.**
  - **Fetch-check:** a live `fetch:check` of the 87 rows first found 8 failing and 4
    picking the wrong PDF. After the resolver fixes, every row resolves to its current
    bulletin except eCatholic sites that Cloudflare blocked in the sandbox. Which sites
    were blocked varied from run to run (4 to 11 of 16), and each resolved on another
    run, except two blocked on all three: All Saints, Albany (eCatholic) and Holy Family,
    Little Falls (`other`). Nine sites are replay fixtures.
- 2026-10-07: Audited the churches the site showed with no Mass. Walton, Delhi and Downsville
  (`st-john-the-baptist-walton`) never fetched as `other`: the site builds its bulletin list in
  the browser from a Drive folder, so the row now reads that folder (`google_drive`,
  `drive-folder` recipe; resolves to the 11 October issue). Christ the King, Albany had been read
  from a ParishesOnline "Special" issue; `fetch` now prefers the regular bulletin. Promoted.
