---
name: Roman Catholic Diocese of Brooklyn
state: NY
website: https://dioceseofbrooklyn.org
status: exploring
gcatholic: broo0
---

The Diocese of Brooklyn is the boroughs of Brooklyn (Kings County) and Queens (Queens County),
all of it New York City: about 4.8 million people, "172 parishes and 211 churches" by the
diocese's own count (parish directory, read 2026-11-05). Postal cities are Brooklyn for the
whole of Kings County, and the Queens neighbourhood names (Jamaica, Flushing, Astoria, Long
Island City, Ridgewood, the Rockaways, ...) for Queens. Its neighbours are the Archdiocese of
New York (Manhattan, the Bronx and Staten Island, across the East River and the Narrows) and
the Diocese of Rockville Centre (Nassau County, east of Queens). There are no families or
clusters of parishes. Since 2023 the diocese is divided into four regions (Brooklyn West and
East, Queens West and East) and 22 deaneries (B1-B11, Q1-Q11); a deanery is a consultation
group, not a pastorate, though the bishop's 2024 reconfiguration letter has deaneries
coordinating Mass schedules. What decides shared bulletins here is (1) canonical mergers,
which the diocese names by joining the old names ("Holy Family - St. Laurence"), often
keeping two churches, and sometimes still listing the old parishes apart for a while after
the decree; and (2) priests who are pastor or administrator of two or three parishes (13 such
assignments in the priests' directory, 2026-11-05). Every batch's `why` names the ones that
touch it.

## Sources

- **Parish directory:** https://dioceseofbrooklyn.org/directories/parishes/ (page modified
  2026-05-06, read 2026-11-05). One block per parish: linked name (the homepage), office
  street address, phone. 172 entries, matching the page's own "172 parishes". Imported as
  roster `directory` by `scratch/brooklyn-map-1/tools/directory.py`. No coordinates. Good
  for the canonical list and homepages; merged parishes appear once under the joined name
  with the office address, so their other churches aren't listed. It lags on mergers:
  Resurrection-Ascension and Our Lady of the Angelus (merged 2023), Christ the King and
  St. Mary Magdalene (merged 2024), and Good Shepherd-Resurrection and Resurrection are still
  separate entries. Three parishes have no website link (Most Precious Blood-Ss. Simon and
  Jude, Our Lady Queen of Martyrs, Ss. Peter and Paul-Epiphany).
- **Deanery directory:** https://dioceseofbrooklyn.org/directories/deaneries/ (modified
  2026-06-06, read 2026-11-05). Parishes by deanery with addresses. Imported as roster
  `deaneries` (`group` = deanery and region) by `tools/deaneries.py`; 175 entries. Has
  errors: B8's list gives St. Michael-St. Malachy (East New York) and Our Lady of Perpetual
  Help (South Ozone Park), where St. Michael and the Basilica of OLPH (Sunset Park) belong;
  Q1 gives Immaculate Conception, Jamaica (also in Q7) where Astoria's would be; Q10 ends with
  the diocesan offices and the Immaculate Conception Center (Douglaston). It still lists
  Mary Queen of Heaven, Our Lady of Refuge and Corpus Christi alone beside their merged
  parishes.
- **Mass finder:** https://mass.dioceseofbrooklyn.org/all (read 2026-11-05), a page per place
  at `/places/<id>` with address, Mass and confession times. 173 places, nearly one per
  parish; a merged parish's place is named "Parish (main church)". Imported as roster
  `massfinder` by `tools/massfinder-fetch.sh` + `tools/massfinder.py` (coordinates from the
  list, address from each page). Some times look like placeholder data: St. Rose of Lima,
  Brooklyn shows a 2:00pm Filipino Mass and "Followed by potluck brunch". Don't take a
  schedule from it without the parish's own; use it for coordinates and extra places
  (it lists Holy Innocents, St. Gertrude, Our Lady of Lourdes chapel, St. Teresa). A few
  addresses are wrong (St. Martin de Porres: "2 Floral Parkway, Floral Park").
- **GCatholic:** key `broo0`, https://gcatholic.org/churches/local/broo0, roster `gcatholic`
  (218 entries, fetched 2026-11-05). Lists old churches of merged parishes individually
  (Holy Rosary, St. Peter Claver, St. Cecilia, St. John Cantius, Epiphany, ...), which
  makes it the best list of buildings to check for closures, and ten Eastern Catholic or
  Coptic churches (Ukrainian, Melkite, Syro-Malankara, Armenian, Romanian, Coptic), all in
  batch `eastern-catholic`. Some of its entries share an address with a Latin church
  (St. Ann, Flushing; St. Basil at the Immaculate Conception Center).
- **Families / clusters:** none exist. Use the merger decrees and the priests' directory.
- **Priests' directory (shared pastors):** https://dioceseofbrooklyn.org/priests/ (read
  2026-11-05). Each priest's "Current Assignment". The page shows nine and loads the rest by
  POST (`admin-ajax.php`, action `loadmore`); `tools/priests.py` reads all 343. Explicit
  multi-parish pastors: OL Angels + St. Andrew the Apostle + St. Anselm (Bay Ridge); OLPH +
  St. Teresa of Avila-St. Anthony of Padua (South Ozone Park); St. Bernadette + St. Frances
  Cabrini; St. Rita + St. Patrick (Long Island City); St. Mary Star of the Sea and St. Gertrude
  (Far Rockaway, one parish); Sacred Hearts & St. Stephen + St. Mary Star of the Sea (Carroll
  Gardens); St. Edmund + St. Brendan; St. Raphael + St. Teresa (Woodside); St. Clare + St. Pius
  X (Rosedale); St. Thomas Aquinas + OL Help of Christians; St. Michael + St. Agatha (Sunset
  Park); St. Charles Borromeo + Cathedral Basilica of St. James; American Martyrs + Holy
  Family (Fresh Meadows). A shared pastor is a lead for one bulletin, not proof.
- **Merger decrees:** posts on dioceseofbrooklyn.org (WordPress search "merger decree"):
  St. Augustine-St. Francis Xavier and Christ the King-St. Mary Magdalene (posted 2024-09-24,
  effective 2024-07-01), Incarnation-St. Gerard Majella (posted 2024-12-23),
  Resurrection Ascension-Our Lady of the Angelus (posted 2025-09-10, effective 2023-01-01).
  Each says "The Parish shall have two churches for worship". The decrees page
  (https://dioceseofbrooklyn.org/decrees/) renders no list without JavaScript; older mergers
  aren't posted.
- **Closed parishes and where their records went:** Archives "List of Parishes",
  https://dioceseofbrooklyn.org/offices/diocesan-archives/parishes/ (read 2026-11-05). Every
  parish ever, Brooklyn then Queens, with founding year, mergers ("Merged with St. Martin of
  Tours, 2007"), closures and where the records are. Good for dating a merger; says nothing
  about whether a building still has Mass. Also two PDFs, "Chronological List of Brooklyn /
  Queens Parishes and Schools" (2019), linked from it.
- **Pastoral plan:** Bishop Brennan's letter "Reconfiguring for the Future to Address Resource
  Challenges" (dated 2024-06-07): a three-stage reconfiguration of "collaborating, partnering,
  or merging", deanery-level Mass-schedule changes from fall 2024. A plan; check bulletins
  for what happened.

### Bulletin publishers here

- **Tilma parish sites are common.** 47 of the directory's 169 homepages are
  `<name>-brooklyn.org` / `-queens.org`, and four of four sampled sites (Guardian Angel,
  IHM, St. Pius V, Queen of All Saints) load from Tilma (`files.tilmaplatform.com`). `probe
  url` reports them `ok` with no platform and no publisher. The bulletins page (`/bulletins`)
  is server-rendered and lists cards "Bulletin for Sunday, <date>" newest first, each
  linking a PDF at `files.tilmaplatform.com/system/resources/<token>/<file>.pdf`; Guardian
  Angel's file names start with a six-digit number (`259950.11.08.2026.pdf`). Try `other`
  with a `page-pdfs https://<site>/bulletins` recipe and `fetch:check` it; confirm the pick is
  this week's issue.
- **ParishesOnline appears too:** St. Fidelis (po-org `st-fidelis-church`) and St. Matthias
  (po-org `st-matthias-church-11385`) embed it.
- **Blocked or odd sites seen in the sample (2026-11-05):** stmargaretmv.com answers 403 to
  `probe url` (use parish-site-access `visit.py`); joanofarcqueens.org redirects off-site.
- The neighbouring Archdiocese of New York has only one mapped parish (a self-hosted
  bulletin page) and no publisher notes yet; Rockville Centre isn't mapped.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.

- ParishesOnline often has empty orgs (no issues) for Brooklyn parishes that self-publish, e.g. slugs <name>-11385 / <name>-church-11385; probe po can find them, but an org with no issues is not a publication id and doesn't make the parish a parishes_online row.
- A self-hosted bulletin page that keeps one stale file gets 'ok' from fetch:check with freshness 'unknown', not 'stale'; check the issue date yourself before pinning a recipe.


## Rules settled for this diocese

None yet. Proposals are in `scratch/brooklyn-map-1/survey.json` for survey-review.

- A merger decree that keeps 'two churches for worship' is a lead, not a row decision: a merged parish's churches are one parish row only when the current bulletin covers both, and a pre-merger parish the directory still lists separately is reconciled to the merged row (roster link) rather than given its own row unless it still publishes its own bulletin. (accepted by survey-review, 002-survey-review, 2026-11-06)
- The Mass finder (mass.dioceseofbrooklyn.org) is not evidence for a Mass schedule or for a church having Mass; use it for coordinates and as a lead for places. Schedules come from the parish's bulletin or site. (accepted by survey-review, 002-survey-review, 2026-11-06)
- Eastern Catholic and Coptic churches GCatholic lists in Brooklyn and Queens are excluded as other-jurisdiction (their eparchies), each with a source naming the eparchy; they are not mapped under Brooklyn. (accepted by survey-review, 002-survey-review, 2026-11-06)
- The JFK airport chapel (Our Lady of the Skies) and similar chaplaincy chapels count as worship sites if they have public Mass; with no bulletin they go to excluded/ as no-bulletin, not closed. (accepted by survey-review, 002-survey-review, 2026-11-06)

## Log

- 2026-11-05: Survey. Rosters: directory 172, deaneries 175, massfinder 173, gcatholic 218
  (738 entries). Plan: 53 batches in `batches.json` (52 of 2-4 directory parishes, one
  eastern-catholic), first `q11-ridgewood`; one deanery entry excluded (the diocesan
  offices). No records written; coverage not run.
