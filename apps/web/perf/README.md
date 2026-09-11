# UI performance benchmark

A repeatable harness for the question "does the map still feel fast?".

It serves the production build, drives the interactions that matter with real
DOM events, and reports how long each one took to reach the screen — plus how
much the main thread was blocked while it happened.

```bash
pnpm --filter web test:e2e:install  # once: the harness drives Playwright's Chromium
pnpm --filter web build             # the harness measures dist/, not the dev server
pnpm --filter web perf              # run everything, print a table
pnpm --filter web perf --save mine
# …change some code, rebuild…
pnpm --filter web perf --compare mine
```

`perf/results/baseline.json` and `optimized.json` are the reference runs
recorded when this harness landed; they stay in git, and every other
`--save <name>` is ignored, so pick a name of your own rather than overwriting
them.

## What it measures

| Scenario | What it exercises |
| --- | --- |
| `cold-load` | First visit: navigation → pins on screen (FCP, LCP, blocking time, bytes) |
| `time-slider-drag` | 24 consecutive time-filter changes — the heaviest interactive path |
| `service-type-switch` | Mass / Confession / Adoration, 3 cycles (the whole pin set turns over) |
| `day-toggle` | Weekday chips on and off across the week |
| `search-typing` | One keystroke at a time into the search box |
| `parish-popup-and-nav` | Opening a pin's popup, then the client-side route to the parish page |

Each interaction scenario reports:

- **paintP50 / P95 / max** — input event → the next frame actually painted.
  This is what a user feels; P95 is where jank shows up.
- **sync** — work done synchronously inside the event handler, before the
  browser can do anything else.
- **blocking / longTask** — total blocking time and long-task totals during the
  burst (the same definition web-vitals uses: time over 50 ms per task).
- **settle** — how long after the last input the main thread and DOM kept
  working, which catches expensive work deferred into a React transition.
- **script / layout / recalcStyle / jsHeap / domNodes** — engine counters read
  from CDP, re-baselined after page load so they cover only the interaction.

## Why it is built this way

- **Production build, not the dev server.** Dev-mode React and unbundled
  modules have entirely different performance characteristics.
- **Everything off-origin is stubbed.** Map tiles resolve to a 1×1 PNG and
  place search returns 503, so no run depends on the network.
- **4× CPU throttling** (`--cpu`) lifts main-thread work above timer noise and
  approximates a mid-range laptop under load. `--cpu 1` disables it.
- **Interactions are dispatched from inside the page.** A Playwright round-trip
  costs about as much as the interactions being measured, so the driver only
  starts a scripted burst and collects the numbers afterwards.
- **Five runs per scenario, median reported**, each in a fresh browser context,
  after one unmeasured warm-up run.

## Options

```
--runs <n>        Repetitions per scenario (default 5)
--cpu <n>         CPU throttling multiplier (default 4)
--scenario <name> Run a single scenario
--save <name>     Write perf/results/<name>.json
--compare <name>  Diff against perf/results/<name>.json
--json <path>     Write raw results elsewhere
--dist <path>     Measure another build directory (e.g. one built from main)
--headed          Watch it run
```

`node perf/compare.mjs <baseline> <candidate>` diffs two saved runs without
re-measuring.

To compare against another revision, build it somewhere else and point `--dist`
at it — measuring both on the same machine, back to back, is the only way the
numbers mean anything:

```bash
git stash && pnpm --filter web build && cp -r apps/web/dist /tmp/base-dist
git stash pop && pnpm --filter web build
pnpm --filter web perf --dist /tmp/base-dist --save baseline
pnpm --filter web perf --save candidate --compare baseline
```

## Finding out *why* something is slow

```bash
node perf/profile.mjs --scenario time-slider-drag --top 25
```

Records a V8 CPU profile of the scenario's interaction phase and prints the
hottest functions by self time. Build with `pnpm exec vite build --minify false`
first if you want readable names, and `--out profile.cpuprofile` writes a file
you can open in Chrome DevTools.

## Reading the results

`results/baseline.json` and `results/optimized.json` are the before/after of the
map-rendering work described in the PR that added this harness. Absolute numbers
depend on the machine, so only compare runs recorded on the same one; the
percentage changes are what travel.

This is deliberately not wired into CI: shared runners are too noisy for
millisecond-level timings to gate a merge on. Run it locally when you touch the
map, the filters, or the data layer.

## Environment

Set `PERF_CHROMIUM_PATH` to use a Chromium other than the one Playwright
downloaded (useful in containers that ship their own browser).
