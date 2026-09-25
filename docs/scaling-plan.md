# Project Carlo — Scaling Plan

When does shipping the whole dataset to the browser (the frontend snapshot:
SQLite queried with sql.js until Phase 2's first step, now gzipped JSON) stop
working, and what should replace it? This plan works from measurements,
favours the simplest option that holds, and keeps the site on static hosting
for as long as it can.

## Summary

- **The map breaks first, not the database.** Leaflet draws every church as a
  DOM marker. At ~1,300 churches, dragging the time slider takes 260 ms from
  input to paint; today it takes 32 ms. The snapshot's share of that is a few
  milliseconds. Fix the map before touching the data layer, starting at
  **~500 churches**.
- **The single snapshot is fine to ~2,000–3,000 churches** (~0.5–0.8 MB
  gzipped, about 1 s to parse on a mid-range phone). Past that, split it into
  static per-region files the map fetches as the viewport moves. It stays
  static, so it still costs nothing.
- **Nationally (~20,000 churches)** one snapshot is not viable: 5 MB download,
  about 5 s of parsing on a phone, and ~190 MB of JS heap. The one-page-per-church
  prerender also passes the Workers Free limit of 20,000 files. Regional shards
  plus Workers Paid ($5/month) cover this without a database server.
- **A server database (D1) is only worth it when users start writing data**
  (accounts, corrections, saved churches), not for read performance.

## How it works today

The measurements below were taken before Phase 2's first step, when the
snapshot was a gzipped SQLite file (`frontend.snapshot`) opened with sql.js.
It is now column-oriented JSON; see [Phase 2](#phase-2--slim-the-payload-cheap-buys-23).

- The weekly pipeline writes `frontend.json.gz`: every church and event, as
  gzipped column-oriented JSON, built by `src/pdf_extract/extract_frontend_db.py`
  (its docstring has the format).
- `apps/web/src/api.ts` downloads and gunzips it, and `apps/web/src/lib/snapshot.ts`
  decodes **every** church and event into JS objects once; filters run in JS on
  every filter change (`collectMapItems`).
- `apps/web/src/components/ChurchMap.tsx` renders one react-leaflet `<Marker>`
  (an SVG `divIcon`) per matching church, with no viewport culling or clustering.
- `scripts/prerender.ts` writes one static HTML page per church, plus
  `churches/index.html` and `sitemap.xml`. Everything is served as Workers
  static assets (no Worker script).

Current data (live snapshot, 2026-09-25): **132 churches, 62 parishes, 850
events**. As SQLite that was 37 KB gzipped (128 KB raw), about 280 bytes per
church gzipped, and the sql.js wasm (660 KB raw / 320 KB gzipped) was bigger
than the data until ~1,000 churches. As JSON it is 14 KB gzipped, about
100 bytes per church.

## Measurements

The live snapshot was scaled 10×, 40× and 150× with synthetic churches:
random names, cities and coordinates across the US, and the real event mix
per church with jittered times. Gzipped size per church came out the same as
the real snapshot (34 KB vs 37 KB at 1×).

### Data layer alone

This is Node on a fast server CPU running the app's own code path: gunzip,
open in sql.js, map rows to objects with `computeNextOccurrence`, then
`collectMapItems`. A mid-range phone is roughly 4× slower.

| Scale | Churches | Events | Snapshot (gz / raw) | Open + load into JS | Slider step (P50 / max) | JS heap |
| --- | ---: | ---: | --- | ---: | --- | ---: |
| today | 132 | 850 | 34 KB / 148 KB | 44 ms | 0.2 / 5 ms | 10 MB |
| 10× | 1,320 | 8,500 | 325 KB / 1.1 MB | 220 ms | 2 / 8 ms | 17 MB |
| 40× | 5,280 | 34,000 | 1.3 MB / 4.4 MB | 500 ms | 6 / 21 ms | 40 MB |
| 150× (~national) | 19,800 | 127,500 | 4.8 MB / 17 MB | 1.55 s | 37 / 75 ms | 188 MB |

About 75–80% of load time goes to turning rows into JS objects (`getAsObject()`
plus `computeNextOccurrence`), not to opening the database.

### Whole app in the browser

This used the repo's perf harness (`pnpm --filter web perf`) on full production
builds of each snapshot: Chromium, 4× CPU throttle, median of 3 runs.

| Scale | Markers visible | Blocking during load | DOM nodes | Slider paint P50 / P95 | Blocking during 24-step drag |
| --- | ---: | ---: | ---: | --- | ---: |
| today | 1.85 s | 0.3 s | 2,700 | 32 / 44 ms | 0 ms |
| 10× | 3.85 s | 2.2 s | 23,400 | 260 / 431 ms | 6.9 s |
| 40× | never ready (harness timed out at 30 s) | — | — | — | — |

At 40× with **no** CPU throttling it took 8.1 s to show markers, with an
87,000-node DOM and a 2.2 s longest task. In the same conditions the data
layer took ~0.5 s of that.

### Build and hosting

| Scale | Files in `dist/` | `churches/index.html` | `sitemap.xml` | Prerender time |
| --- | ---: | ---: | ---: | ---: |
| today | 206 | small | small | seconds |
| 40× | 5,354 | 1.4 MB | 0.7 MB | — |
| 150× | ~19,900 | 4.6 MB | 2.7 MB | 35 s |

Relevant Cloudflare limits:

- Workers Free allows 20,000 static asset files per version; Paid ($5/month)
  allows 100,000. Each file can be up to 25 MiB.
- Static asset requests are free and unmetered on both plans.
- A sitemap file holds at most 50,000 URLs.

## Thresholds

| Churches | Roughly | What breaks | Action |
| ---: | --- | --- | --- |
| < 500 | a few dioceses | nothing | none |
| ~500–1,000 | a large state's worth of dioceses | map: slider and filter changes start dropping frames | **Phase 1**: fix the map |
| ~2,000–3,000 | a few states | snapshot passes ~0.5–0.8 MB gzipped and ~1 s to parse on a phone, and every visitor pays for the whole dataset | **Phase 2**: slim the payload; **Phase 3**: regional shards |
| ~15,000–20,000 | national | 20,000-file limit on Workers Free; 5 MB snapshot; ~190 MB heap, which risks mobile Safari killing the tab; 4.6 MB church index page | Phase 3 plus Workers Paid, and a church index split by state |

## Options

These are ordered from simplest to most involved. Each one stays useful after
the next one is added.

### Phase 1 — Draw only what's on screen (needed at ~500 churches)

This change is to the map only; the data layer stays as it is.

- **Viewport culling.** Render markers only for churches inside the current
  map bounds plus some padding, and update on `moveend`. The default view is
  zoom 11, a single metro area, so this alone keeps the DOM at tens of markers
  regardless of total size.
- **Clustering at low zoom.** Use [`supercluster`](https://github.com/mapbox/supercluster)
  (small and fast; indexing 20,000 points takes tens of ms) to collapse pins
  into counts when zoomed out. Popups only exist for markers that are actually
  rendered.
- Canvas markers (`preferCanvas` / `L.circleMarker`) are an alternative to
  culling. They would lose the current SVG pin design, so culling plus
  clustering is the better fit.

To verify, re-run the perf harness against a synthetic 10× build. The target
is slider paint P50 back under ~50 ms at 1,320 churches.

### Phase 2 — Slim the payload (cheap, buys ~2–3×)

These keep the one-file model while reducing cost per church:

- **Done: drop sql.js in favour of compact JSON.** The app already copied every
  row into JS arrays, so SQLite in the browser only added 320 KB of gzipped wasm
  and slow row mapping. The snapshot is now column-oriented JSON
  (`frontend.json.gz`): parallel arrays, repeated strings (event types, kinds,
  weekdays, dates, notes, cities) as indexes into a table of values, event ids
  as differences, and times as minutes. `extract_frontend_db.py` writes it,
  `verify-frontend-snapshot` reads it, and the app and the prerender decode it
  with the same code (`apps/web/src/lib/snapshot.ts`); `api.ts` has no SQL.
- **Split map data from detail data.** The map and filters need id, name,
  coordinates and a compact event list. Notes, `page_number`, `bulletin_url`,
  `homepage_url` and addresses are only needed on the church page, and the
  prerendered HTML already contains them. Load those per church on navigation
  instead.
  Not done yet: in the benchmark below it cut load time by only 5–20% at
  1,000+ churches (and not at all today), and the map popup and the search
  list need addresses too.
- **Done: compute `next_occurrence` lazily**, only for events something shows.
- **Done** (with the first step): no sql.js wasm files are copied into
  `public/` any more, which took 2.8 MB off the deploy.

#### Measured: JSON vs querying SQLite in the browser

Before switching, three data layers were benchmarked on the live snapshot and
the synthetic 10×/40×/150× ones (Chromium, 4× CPU throttle, median of 3 runs),
each checked to give identical results to the sql.js code: the sql.js one
(copy every row into JS once), **A** (JSON decoded into memory), and **B**
(keep sql.js, but run a SQL query on every filter change instead of copying
the rows).

| Churches | Download, gzipped (sql.js + data → A) | Load until the first map query returns (sql.js → A) | Slider step P50 (sql.js / A / best B) |
| ---: | --- | --- | --- |
| 132 | 370 KB → 16 KB | 280 → 39 ms | 0.4 / 0.7 / 1.2 ms |
| 1,320 | 670 KB → 97 KB | 690 → 150 ms | 5 / 4 / 8 ms |
| 5,280 | 1.65 MB → 340 KB | 2.2 → 0.43 s | 24 / 24 / 35 ms |
| 19,800 | 5.3 MB → 1.2 MB | 7.1 → 1.5 s | 124 / 130 / 164 ms |

- **A** loads 3–5× faster. Filtering takes as long as before, within noise,
  since the filter code is the same. The church page's first render is faster
  too (6 → 1 ms today), and there is no 22 MB wasm heap.
- **B** was slower on every filter change, at every size: the map needs nearly
  every row on each change, and crossing the wasm boundary for each row costs
  more than filtering plain objects in JS.

### Phase 3 — Regional static shards (the main answer, needed at ~2,000–3,000 churches)

The idea is to keep everything as immutable static files on Cloudflare, but
stop sending everyone the whole country:

- **`index.json`**, which is always loaded: per church, only id, slug, name,
  lat/lng and a small bitmask of event types. At national scale that is
  ~150–250 KB gzipped. It feeds the search typeahead and clustering, and it
  lists which shards exist and each one's bounding box. If national-scale name
  search makes it too big, the search index can load separately, when the
  search box gets focus.
- **`shards/<key>.json`**: events for one region. The key can be a diocese or
  state, or a fixed lat/lng grid cell (for example 1°×1°, which is simplest
  because the map can compute which cells it needs from its bounds). The map
  fetches the shards overlapping the viewport and caches them. Filtering and
  the time slider stay client-side over the loaded shards, so interaction
  stays instant.
- **Content-hashed file names** (`shards/<key>.<hash>.json`) listed in the
  index can be cached `immutable`, and only the index revalidates. A weekly run
  that changes one diocese then invalidates only that diocese's shard.
- **Church pages** stay prerendered. Split `churches/index.html` into
  per-state pages; the SEO plan's city pages fit this too. Past ~50,000 URLs,
  split the sitemap as well.
- **Hosting**: move to Workers Paid ($5/month) before about 19,000 prerendered
  pages. Serving church pages from a Worker instead would avoid that but adds a
  runtime and costs more complexity than the $5 saves.

The pipeline barely changes: `extract_frontend_db.py` writes a directory
instead of one file, and R2 publishing and rollback work as they do now,
since a run's output is still a set of write-once files.

### Alternative: one SQLite file over HTTP range requests (not recommended)

`sql.js-httpvfs` lets the browser query a large static SQLite file by fetching
only the pages it needs. It avoids sharding, but it needs a web worker and
depends on how Range requests and caching behave on the host. It also makes
many small sequential round trips per query, which feels slower than a few
shard fetches. Since the app filters in JS anyway, shards fit the access
pattern better.

### Alternative: a query API on Cloudflare D1 (only when writes arrive)

D1 is SQLite behind a Worker, so the snapshot's two tables (`church` and
`event`) carry over almost unchanged.

- **Cost**: on Free, 5M rows read and 100k rows written per day, plus 100k
  Worker requests per day. On Paid ($5/month), 25B reads and 50M writes per
  month are included.
- **Watch out**: a national weekly load (~130k event rows) is more than Free's
  100k writes per day on its own, so this effectively needs Paid.
- **Worse for this app**: every filter change becomes a network round trip
  (50–150 ms), where it is instant today. So you would still fetch by viewport
  and filter client-side, which is Phase 3 with a server added. Publishing also
  loses the "atomic pointer swap to an immutable run" property; you would need
  per-run tables or D1 Time Travel to roll back.
- **Worth it when**: the site accepts user writes (corrections, feedback,
  accounts, saved churches), data updates more often than deploys, or server
  full-text search across the whole country is needed.

Hosted Postgres (Neon, Supabase) offers nothing D1 doesn't for this workload,
and it adds a second vendor.

## Recommended sequence

1. **Now**: nothing is needed for today's data. Before coverage reaches
   ~500 churches, do Phase 1 (viewport culling and clustering) and check it
   with the perf harness on a synthetic 10× snapshot.
2. **At ~1,500 churches, or a snapshot over ~400 KB gzipped**: finish Phase 2
   by splitting map data from detail data (sql.js is already gone).
3. **At ~2,500 churches**: do Phase 3, regional static shards. Move to
   Workers Paid before ~19,000 prerendered pages.
4. **Only when the product needs user-written data**: add D1 behind a Worker
   for that data. Schedules can stay on static shards.
