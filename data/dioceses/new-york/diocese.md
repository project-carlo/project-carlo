---
name: Archdiocese of New York
state: NY
website: https://www.archny.org
status: promoted
gcatholic: newy0
city_aliases:
  Southeast: Brewster
  Town of Southeast: Brewster
promoted: 2026-11-09
---

Ten counties: Manhattan, the Bronx and Staten Island in New York City, then Westchester, Putnam,
Rockland, Orange, Dutchess, Ulster and Sullivan up the Hudson. Brooklyn and Queens are the
Diocese of Brooklyn, Long Island is Rockville Centre, Albany is north, Bridgeport (Connecticut)
east and Paterson and Newark (New Jersey) west and south. The 2015 "Making All Things New"
mergers and later decrees joined many parishes, but a merged parish often still prints one
bulletin per former parish, or lists Mass at every old church: the official map's long
colon-separated titles are a grouping lead, not a bulletin list. Manhattan and the Bronx carry
Spanish, Polish, Croatian, Slovenian, Albanian, Korean and other language communities, some in
churches whose parish was merged away.

Mapped October 7-11, 2026 by a long session that ran before the onboarding factory existed,
then finished November 8-9 by six follow-up map jobs (Westchester, upstate, Manhattan in two,
the Bronx, Staten Island) and a reconcile, following the factory's stages.

## Sources

- **Official parish map (the `directory` roster):** https://www.archny.org/map/parishes, 326
  locations read October 6, 2026 from the server-rendered `div[data-pf-item]` elements (CMS
  id, title, street address, coordinates, homepage, `archny.org/places/` page). Locations, not
  publishers: a merged parish keeps one pin per old church. Missing websites, ZIP-only
  localities and absent Mass tags don't imply closure; a pin can be the office or another
  frontage of the complex.
- **GCatholic:** key `newy0`, `rosters/gcatholic.json`, 426 entries enriched from each church
  page (address, Plus Code, website, rite, history). It includes Eastern Catholic churches,
  old canonical names, demolished and sold buildings, and stale domains. A merger in a history
  field doesn't mean the building stopped holding Mass.
- **Decrees:** the decree list on https://www.archny.org/parish-planning (latest July 2, 2026, read
  November 9; the older `posts/decisions-of-the-office-...` page now answers 404). Read the decree's operative paragraphs, not its title: a merger
  decree that names the new parish's churches is evidence about a building it leaves out (St.
  John Baptist de la Salle, Staten Island). A decree doesn't date a last Mass, and some were
  rescinded (Holy Trinity, Mamaroneck: 2018, rescinded 2020).
- **Closures:** no archdiocese-wide list. Manhattan closures and relegations are dated in The
  Good Newsroom (archdiocesan news: final Masses) and on sthughofcluny.org (Society of St. Hugh
  of Cluny; it answers HTTP 500 with the full page, so `probe get` fails and `visit.py` reads
  it). Unknown last-Mass days stay unknown.
- **Addresses:** where sources disagree, read the OSM building's address tags (not its name tag).
  A parish's own number can be its school's (St. Francis of Assisi, Baychester Avenue), and a
  GCatholic pin can land on a parking lot.
- **NYC PLUTO:** `data.cityofnewyork.us/resource/64uk-42ks.json?bbl=<bbl>` (BBL from
  `geosearch.planninglabs.nyc`) gives a city building's owner and class: M1 a church, W2 a
  parochial school. A cheap independent check on what a building is.
- **Bulletins and parish sites** settle the publisher and the worship buildings: each record
  quotes a dated issue.

### Bulletin publishers here

eCatholic hosts about 125 rows, John Patrick (church-bulletin.org) about 30, LPi/ParishesOnline
about 25, Bon Venture about 15; the rest are parish sites (WordPress, Squarespace, Wix).

- **Before calling a parish late, search church-bulletin.org and parishesonline.com for it.**
  Seven rows whose own archive lagged 3-8 weeks had the current issue on a church-bulletin.org
  listing their site no longer linked, or never had. A `jppc.net/onlinebulletins/<n>template.pdf`
  link gives the listing.
- **eCatholic:** the `ecatholic` collector reads only the `files.ecatholic.com/<id>/bulletins/
  <YYYYMMDD>.pdf` date path. Many sites now post issues as `/documents/YYYY/MM/` files on a
  page, leaving the date path years stale (2014, 2015, 2022 picks): use `page-pdfs` on that page,
  keep the site id in `publication`. Read the site's Bulletin link first: St. Clare (Staten
  Island) points to Bon Venture beside a 2023 archive; St. Sylvester's to LPi.
  - The `/bulletins` page can lag its files: Nativity's listed 6 September while the date path
    had every Sunday since. Probe the dated paths before calling it stale.
  - Archives pause and resume (St. Augustine, Highland: nothing August 16 to November 1). The
    `?t=` upload stamps on the links show the habit: issues uploaded together mean a late
    poster, a steady weekly upload that stops a real gap.
  - A parish can move its Bulletins page to a sibling parish's site id (Holy Cross, Callicoon
    now lists 10462): re-read the page in the browser before trusting the old id.
  - Several publishers on one site (`Bulletin St Peter-4.pdf`): one row each with a
    `filename=` glob (`?` for each space: `filename=Bulletin?St?Peter*.pdf`) and peer
    `publication_reviews` for every pair (Woodbourne, Livingston Manor, Liberty). Give the
    second and third rows a temporary distinct website, add the reviews, then set the shared URL.
  - `/newsRSS` links each item's PDF: the Cathedral's worship aid reads as
    `page-pdfs <site>/newsRSS filename=*_sun.pdf`.
- **John Patrick:** `church-bulletin.org/<slug>` lists `bulletin/<slug>/<YYYY-MM-DD>.pdf`;
  `page-pdfs` on the listing.
- **Bon Venture:** `sponsors.bonventure.net/?page=<n>`. **Use `http://`:** the https host serves
  an incomplete certificate chain, and Python's urllib fails where browsers succeed. The ad-page
  job line ("027D (JA) - St. Mary, Katonah") names the printer, but the sponsor site has no
  lookup: a sponsor page is found only where a parish site links it.
- **LPi / ParishesOnline:** `probe po <name>-church-<zip>`; the search API by coordinates
  (`/prod/search?searchType=organization&latitude=..&longitude=..&distance=1`) lists every org
  near a church. Most Manhattan and Bronx parishes have a directory-only org with no issues:
  that is "not on ParishesOnline". A container whose uploads are all covers, months apart,
  holds only the printed wrapper (Our Lady of Pompeii). An LPi number in a self-hosted file name
  (`03-0914_5-19-24.pdf`) may never be served: probe it on a date the site has. A slug search
  misses can show on a `parishesonline.com/supporter/<advertiser>` page (render it). A Discover
  Mass page saying "no bulletins available" can belong to a parish with a current container.
- **WordPress sites:** `/wp-json/wp/v2/media?mime_type=application/pdf` shows the newest issue and
  its upload date; `dated-post` reads `/category/bulletin/` (St. Lawrence O'Toole). Some hosts
  (sacredheartsi.org, stbernardswp.com, sjbny.org) refuse `probe pdf`/`probe get` while
  fetch:check downloads: judge those by file name and fetch:check.
- **Viewer pages:** `page-pdfs` reads DearFlip and similar viewer settings only when the page's
  ordinary PDF anchors give nothing: a `filename=` glob that excludes stale anchors makes it fall
  through (St. Anthony, Sullivan Street: `filename=[!b]*[0-9].pdf`).
- **Year-less file names:** on a multi-year archive (`November-14.pdf`), `page-pdfs` reads every
  date as this year and an older year's later Sunday wins. If no other link gives the year, it's
  `unsupported` `yearless-filename-archive` (St. Paul, Bullville).
- **No collector yet (`unsupported` + `fetch_gap`):** Flocknote HTML notes (Rye, Immaculate Heart
  of Mary Scarsdale; `<group>.flocknote.com/home/api/mynotes` lists notes without a login),
  Mailchimp (St. Malachy: take `u=`/`id=` from an old issue for `us<N>.campaign-archive.com/
  home/?u=..&id=..`), Constant Contact (St. Paul the Apostle), OneDrive folders (Katonah), a
  full issue beside a same-dated supplement (Sullivan St. Francis Xavier), a first PDF that's a
  form (Our Lady of Sorrows, White Plains). Open the parish's own site before marking one:
  Mahopac's linked a Bon Venture page.
- **Dates:** an issue can keep an old template heading (St. Teresa's October 4 issue had a 2021
  header), and a parser can read `Bulletin 100426.pdf` as 2010. Read the masthead.
- **Access:** sites that gave `probe url` a Cloudflare 403 in October all read in headed Chrome
  (`visit.py`) in November. A 403 or TLS failure is never evidence of closure.

## New lessons

Lessons map jobs reported, as written, for the next `integrate` to merge into *Bulletin publishers here* and *Rules settled*. Every map job reads them.


## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

- The owner asked for the whole archdiocese on October 7, 2026; the September single-parish
  scope doesn't limit it. (owner, 2026-10-07)
- Brewster is the village and postal city, in the Town of Southeast: store Brewster; "Town of
  Southeast" is a `city_aliases` entry. (map, 2026-09-26)
- The worship building and the bulletin decide records, not the names in a canonical title. A
  shared pastor doesn't combine separate current bulletins. (map, 2026-10-08)
- Sunday Mass in a separate school building or gym is public Mass, a church under its parish
  (St. Peter, Poughkeepsie; St. Patrick School, Staten Island); a school-only listing isn't.
  (map, 2026-10-08; upstate follow-up, 2026-11-08)
- Repeated dedications in one city get disambiguated slugs and their own roster links (Staten
  Island's St. Joseph at Poplar Avenue and at Tompkins Avenue). (map, 2026-10-08)
- Eastern Catholic roster entries at the same address as a mapped Latin church (Holy Spirit,
  Cortlandt Manor; St. Francis, Mount Kisco) are coverage aliases of that church; elsewhere
  they're excluded `other-jurisdiction`. Same-name churches at different addresses stay
  separate (Latin St. Mary, Grand Street vs. the Ruthenian St. Mary, East 15th). (map,
  2026-10-08)
- A church its parish says is temporarily suspended (St. John the Baptist, Manhattan, repairs;
  St. Michael, Manhattan, boiler) is excluded `other`, not closed, with no invented last-Mass
  date. (map, 2026-10-11)
- A building a decree keeps for occasional (anniversary, patronal) Masses, with no Mass in any
  of the year's bulletins, not even its feast week, is excluded `other` (St. John Neumann and
  St. Paul, Staten Island). (Staten Island follow-up, 2026-11-09; owner to confirm)
- Chapels of religious houses count only where a current source shows public Mass. The Sisters
  of Life chapels in Lower Manhattan (St. Andrew; Our Lady of the Rosary, Seton Shrine) and
  Sacred Heart, Sparkill (lent to an Orthodox congregation) are excluded `no-public-mass`.
  (Westchester and Manhattan follow-ups, 2026-11-08/09)
- A parish with public Mass whose bulletin has stopped (archive months stale, or empty) is a
  `no_bulletin` row with its churches and a dated retry, not an open record. (follow-up brief,
  2026-11-08)
- Nobody contacts parishes. A place no web source settles stays `open/` with an evidence-based
  revisit (an archive upload, a dated decree, a schedule change), not "ask the office".
  (follow-up brief, 2026-11-08)

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.

- 2026-11-09: Follow-up Run (by hand, in the factory's stages) on the old session's leftovers
  after merging main twice. Six map jobs (Westchester, upstate, Manhattan A and B, the Bronx,
  Staten Island) worked through the 86 `open/` records and the `*-fetch-connector` questions
  with no contact to parishes (19 stay open, each with an evidence-based revisit); a reconcile re-checked every row that wasn't picking a current issue,
  fixed bodies that still linked deleted `open/` records, and cleared October revisits that
  today's fetch:check answered. `st-joseph-middletown` became `st-joseph-middletown-ny`
  (Wilmington took the slug). Bon Venture recipes switched to `http://`. Thirteen rows moved to
  church-bulletin.org or ParishesOnline listings where their own archive lagged. The old
  register `research-followup.md` was folded in here and deleted. `batches.json` added (64
  county batches of about five publishers). Coverage: directory 326/326 accounted for
  (286/323 modelled), gcatholic 426/426 (282/334); six churches in no roster.
  262 parish rows (231 live; 23 `no_bulletin`, 8 `unsupported`), 337 churches (301 live), 93 exclusions, 19 `open/`.
  fetch:check on the 231 live rows: all downloaded; 9 pick an issue two or more weeks old
  (parishes that post late, each with a dated retry), the rest the current or next issue.
- 2026-10-11: The old session's follow-up: of 171 open questions, 89 resolved and 82 kept
  open (connectors, unidentified chapels, "ask the office"). 227 publishers, 291 churches, 78
  exclusions, 86 open; six publishers held off the site as `no_bulletin`. Promoted 221
  publishers / 283 churches. Coverage: directory 326/326, gcatholic 426/426.
- 2026-10-08: First archdiocese-wide pass (186 publishers, 237 churches, 43 exclusions, 171
  open questions) and the October 7 policy that `no_bulletin` rows stay off the site.
- 2026-09-26: Added St. Lawrence O'Toole and Sacred Heart (Brewster and Patterson), the
  requested parish: one bulletin, two churches, from the 27 September 2026 issue.
