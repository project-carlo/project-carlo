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

- **J.S. Paluch on Discover Mass** printed half of Harrisburg. `discovermass.com/?s=<town or
  ZIP>` finds a church page when the parish site is blocked; St. Gregory, MacDonaldton's
  directory homepage is a Discover Mass page. One joint bulletin can appear under several
  church slugs: record every slug. Discover Mass caps downloads per IP per day (a 134-byte
  "Maximum number of files downloaded today" reply, which `fetch:check` reports as
  `not_pdf`); its text layer is often garbled, and quotes keep the garble. Cite the church
  page, not a tokenised download link.
- **eCatholic** sites sit behind Cloudflare: `https://www.<domain>/bulletins` usually opens in
  headed Chrome (parish-site-access) when the homepage is challenged.
- **LPi / ParishesOnline:** many parishes keep empty organizations, which are not fold-ins.
  The search API (`/prod/search?searchType=organization&...&latitude=&longitude=`) lists
  organizations near a point.
- **Bon Venture** (`sponsors.bonventure.net/?page=<id>`, PDFs at `pdfs/<id>/<YYYY-MM-DD>.pdf`):
  broken https chain, use `http://`. **John Patrick Publishing** (`church-bulletin.org/<id>`):
  a listing with no PDFs is not a live channel. **FATA Online** (`fataonline.com/bulletins/
  <code>`): fixed "View Current Bulletin" link plus dated archive.
- **webparish.com/aj/<name>/** hosts at least St. Clare of Assisi, Johnstown: a diocesan
  hosting scheme to look at on the first parish that uses it.
- **Image-only bulletins** are common in the region; read them by rendering pages and say so.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.
