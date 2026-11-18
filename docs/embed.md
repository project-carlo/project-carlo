# Embedding the map on a diocese's site

A diocese can show Project Carlo's Mass, Confession and Adoration finder on its
own website, set to its own territory, by pasting one snippet into an "HTML" or
"Embed" block in its CMS (WordPress, eCatholic, Squarespace, Wix and so on).
Nobody on their side writes code. Issue #122 has the background.

- [The handoff kit](#the-handoff-kit): what a diocese gets
- [How it works](#how-it-works): for whoever maintains the site
- [Keeping it working](#keeping-it-working): promises the embed depends on

## The handoff kit

Send a diocese this section, with their snippet filled in.

### 1. The snippet

Paste this into an HTML or Embed block on the page where the map should go:

```html
<iframe
  src="https://projectcarlo.com/embed?diocese=syracuse&ref=diocese-syracuse"
  style="width:100%; height:700px; border:0;"
  allow="geolocation"
  loading="lazy"
  title="Mass and Confession times">
</iframe>
```

A height of 700px suits most pages; anything from 600px up works. Keep
`allow="geolocation"`: without it the map's "Use my location" button can't ask
the visitor's browser where they are.

Snippets for the dioceses the site covers now (only those with churches on the
site; any other `diocese=` shows a "not supported yet" notice in the frame):

| Diocese | `src` |
|---|---|
| Albany | `https://projectcarlo.com/embed?diocese=albany&ref=diocese-albany` |
| Buffalo | `https://projectcarlo.com/embed?diocese=buffalo&ref=diocese-buffalo` |
| Rochester | `https://projectcarlo.com/embed?diocese=rochester&ref=diocese-rochester` |
| Syracuse | `https://projectcarlo.com/embed?diocese=syracuse&ref=diocese-syracuse` |

New York has only two churches on the site, so it isn't offered yet. Before
sending a snippet, open its `src` in a browser and check the map shows the
diocese's churches.

### 2. What it shows, and where the times come from

The map shows the diocese's churches and their Mass, Confession and Adoration
times. Visitors can search for a town or church, filter by service, day and
time, and open any church's full schedule on projectcarlo.com in a new tab.

The times are read automatically from each parish's published bulletin and
refreshed every week. They can contain mistakes, so we suggest a line beside
the map such as:

> Times are read from each parish's bulletin and can contain mistakes. Please
> confirm with the parish before you go, especially on holy days.

### 3. Corrections

_To be decided: the feedback form or an email address._ A diocese's name sits
next to the data, so it needs one clear place to report a wrong time.

### 4. Support

- It's free.
- We'll give notice before any change that affects the embed.
- Contact: _to be decided, with the corrections contact above._

## How it works

`/embed` is the home map (`src/views/HomePage.tsx` with `embed`, mounted by
`src/views/EmbedPage.tsx`; `src/lib/embed.ts` has the helpers). In the embed:

- **No masthead or site links.** The card holds the search and filters, and a
  "Powered by Project Carlo" line links to the full site's map at the same view,
  filters and `ref`, in a new tab.
- **Links open in a new tab.** Every link clicked in the embed (church pages,
  the credit, the map's attribution) opens in a new tab, never inside the
  frame: one capturing click handler on the embed's root does it
  (`src/views/EmbedPage.tsx`), so a link added later is covered too. Links to
  the site carry the embed's `ref` (or `utm_source`), so the visit is credited
  to the embed. Nothing in the embed adds a history entry: inside a frame that
  would take over the host page's back button. The map's view goes into the
  frame's own entry by `replaceState`, as on the home page, but not into the
  session's remembered map search, which the full site's "Map" links restore.
- **The host page keeps its scrolling.** The mouse wheel zooms the map only
  once it has been clicked, until the pointer leaves it, and on a touch screen
  one finger scrolls the page while two move the map (`FramedGestures` in
  `src/components/ChurchMap.tsx`).
- **`diocese=<slug>`** keeps the map and the search to that diocese's churches
  and opens the map fitted to them, instead of near the visitor's IP location.
  The slug is the diocese's folder in `data/dioceses/`. A diocese with no
  churches on the site, or a slug that names none, gets a "not supported yet"
  notice. Without `diocese=` the embed shows every church.
- **Other parameters** work as on the home page: `lat`, `lng` and `z` set where
  the map opens (overriding the diocese's fit), and `type`, `days`, `from` and
  `to` preset the filters (`src/components/filterState.ts`).
- **Analytics.** Pageviews are recorded under the path `/embed`, with `ref` (or
  `utm_source`) as the campaign and the host page's site as the referrer
  (docs/analytics.md).
- **Not for search engines.** `embed.html` (written by `scripts/prerender.ts`)
  and the page itself are `noindex`, as the page repeats the homepage.

Where a church's diocese comes from: `data/parishes.csv` has a `diocese` column,
the folder its parish's record is in, which `pnpm diocese promote` writes and
`tests/test_dioceses.py` checks. The snapshot builder
(`src/pdf_extract/extract_frontend_db.py`) reads it from the CSV when it builds
the snapshot, rather than from the database, so a deploy that serves the
published database's data (while CSV removals wait for a reviewed weekly run)
still has every church's diocese; a parish already taken off the CSV gets the
folder its record is still in. A missing CSV stops the build rather than ship
a snapshot with no church in any diocese.

To try the embed framed on another page locally, build the site, run `wrangler
dev`, and open a page from another origin with an `<iframe>` pointing at it.
Chrome's Local Network Access check blocks a public page from framing a local
server, so serve the host page locally too, or start Chrome with
`--disable-features=LocalNetworkAccessChecks`.

## Keeping it working

- **Never block framing.** Neither `apps/web/public/_headers` nor
  `apps/web/worker/index.ts` sets `X-Frame-Options` or a CSP `frame-ancestors`
  rule, and the embed depends on that. If one is ever needed, allowlist every
  embedding diocese's domains first.
- **The URL is a public contract.** Dioceses paste it into pages nobody may
  revisit for years. Keep `/embed` and its parameters (`diocese`, `ref`, `lat`,
  `lng`, `z`, `type`, `days`, `from`, `to`) working, and give notice before
  changing what the embed shows.
- **Cost.** Static assets are free on Workers, but each embed pageview sends
  one analytics batch to the Worker, and Workers Free allows 100,000 requests a
  day across the account (`wrangler.jsonc`). An embed shouldn't come close;
  check the analytics dashboard after a diocese goes live.
