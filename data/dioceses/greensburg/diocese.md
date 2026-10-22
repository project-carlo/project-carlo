---
name: Roman Catholic Diocese of Greensburg
state: PA
website: https://dioceseofgreensburg.org
status: exploring
gcatholic: gree1
---

## Sources

Diocese-wide lists worth reading, what each is good for, and how far to trust it here.
Fill this in as you find them (see data/dioceses/README.md, "Sources").

- Parish directory:
- GCatholic:
- Clusters / families of parishes:
- Mass times:
- Closed parishes and where their records went:
- Pastoral plan / closure announcements:

### Bulletin publishers here

Which publishers print this diocese's bulletins, how to read each, and which sites block the
sandbox and where their bulletins are instead. Agents researching parishes start here, so
keep it current rather than a log.

Carried over from Altoona-Johnstown, Harrisburg, Scranton and Allentown (2026-10); correct it
as this diocese shows otherwise.

- **J.S. Paluch on Discover Mass.** Its `?s=` search is broken; grep the town in the
  sitemaps (`discovermass.com/wp-sitemap-posts-item-{1..11}.xml`), since slugs can be
  unguessable. Probe on the bare host (200 = exists, 404 = not). A joint bulletin may sit under
  only one of its churches' slugs, so read a neighbour's masthead before calling a parish
  `no_bulletin`; record every slug that carries the issue. "No bulletins available" pages are
  not live channels. Downloads are capped per IP per day (a 134-byte "Maximum number of files
  downloaded today" reply, `not_pdf` in `fetch:check`), and repeated page hits 503 then
  Wordfence-block even headed Chrome: read each page once. The text layer is often garbled
  (quotes keep the garble); cite the church page, not a tokenised download link.
- **LPi / ParishesOnline:** empty organizations are common and are not fold-ins. The search
  API (`https://f2141mdwk2.execute-api.us-east-1.amazonaws.com/prod/search?searchType=organization&latitude=..&longitude=..&distance=3`)
  lists organizations near a point. Some containers are image-only: render pages with
  `pdftoppm` and read them (tesseract is not installed).
- **eCatholic** sites sit behind Cloudflare: `https://www.<domain>/bulletins` usually opens in
  headed Chrome (parish-site-access) when the homepage is challenged.
- **WebParish, Wix, Bon Venture** (`http://sponsors.bonventure.net/?page=<id>`, broken https
  chain), **John Patrick Publishing** (`church-bulletin.org/<id>`: any slug answers 200 with a
  generic page, and a listing with no PDFs is not live) and **FATA Online** all appeared next
  door. A Wix PDF name changes weekly: `page-pdfs` on the site reads it. A site with one child
  page per issue needs `dated-post <bulletin page>`.
- **Directory homepages and addresses go stale** (dead DNS, SSL failures; the address can be
  the rectory). Check a URL before storing it.
- **Web search in the sandbox:** `visit.py "https://duckduckgo.com/?q=..." --text`
  (parish-site-access) works; curl to DuckDuckGo or Bing returns nothing. A public Facebook
  post URL opens in headed Chrome without login (profile pages don't); cite it as a note.
- **Evidence for a `no_bulletin` church being open:** obituary snippets ("funeral Mass at
  <church>"), with the directory's Mass times. Flocknote pages are sign-up pages, not bulletins.
- **Sister parishes with one pastor** can each post their own bulletin with the same combined
  Mass rota: two rows while both channels are live.

## Rules settled for this diocese

Decisions that apply to more than one record, and who made them.

## Log

Newest first: date, what was done, and the `pnpm diocese coverage` numbers after it.
