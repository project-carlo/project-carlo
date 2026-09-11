// Benchmark scenarios: the handful of interactions that decide whether this app
// feels fast — first paint of the map, dragging the time filter, switching
// service type, toggling days, typing in the search box, and opening a parish.
//
// Every scenario returns the same metric shape so runs can be diffed
// mechanically (see compare.mjs).

const HOME_READY_SELECTOR = ".leaflet-marker-icon";
const SLIDER_START = 'input[aria-label="Start time"]';
const SLIDER_END = 'input[aria-label="End time"]';
const SEARCH_INPUT = '[cmdk-input], input[aria-label^="Search for"]';

/** Steps of 30 minutes, sweeping the "from" edge across the morning. */
const SLIDER_STEPS = Array.from({ length: 24 }, (_, i) => 360 + i * 30);
const TYPED_QUERY = "saint mary";

/**
 * Run a scripted burst of interactions entirely inside the page.
 *
 * Driving each step from Node would add a Playwright round-trip (~1-2 ms) to
 * every sample, which is the same magnitude as the thing being measured.
 */
async function runBurst(page, steps, { gapMs = 32, settleQuietMs = 250 } = {}) {
  return page.evaluate(
    async ({ steps, gapMs, settleQuietMs }) => {
      const bench = window.__bench;
      const startedAt = bench.now();
      const samples = [];

      for (const step of steps) {
        const element = document.querySelector(step.selector);
        if (!element) throw new Error(`selector not found: ${step.selector}`);
        const sample = await bench.measure(() => {
          switch (step.kind) {
            case "range":
            case "text":
              bench.setInputValue(element, step.value);
              break;
            case "click":
              element.click();
              break;
            case "focus":
              element.focus();
              element.dispatchEvent(new FocusEvent("focus", { bubbles: false }));
              break;
            default:
              throw new Error(`unknown step kind: ${step.kind}`);
          }
        });
        samples.push({ ...sample, label: step.label ?? step.kind });
        if (gapMs > 0) {
          await new Promise((resolve) => setTimeout(resolve, gapMs));
        }
      }

      const settleMs = await bench.settle(settleQuietMs);
      return {
        samples,
        settleMs,
        tasks: bench.tasksSince(startedAt),
        markerCount: bench.markerCount(),
      };
    },
    { steps, gapMs, settleQuietMs },
  );
}

/** Text-content lookup for buttons, done in-page so it stays a single round-trip. */
function buttonSelector(label) {
  return `button[data-perf="${label}"]`;
}

/**
 * Tag the service-type buttons with a stable attribute. They are plain
 * text-labelled buttons in the app; the benchmark must not require the app to
 * carry test hooks, so it applies them itself after load.
 */
async function tagServiceButtons(page) {
  await page.evaluate(() => {
    for (const button of document.querySelectorAll("button")) {
      const label = (button.textContent ?? "").trim().toLowerCase();
      if (["mass", "confession", "adoration"].includes(label)) {
        button.setAttribute("data-perf", label);
      }
    }
  });
}

async function gotoHome(page, origin, { search = "", markCdpBaseline } = {}) {
  await page.goto(`${origin}/${search}`, { waitUntil: "commit" });
  await page.waitForSelector(HOME_READY_SELECTOR, { timeout: 30_000 });
  // The desktop filter panel and the search index arrive a beat after the map;
  // wait for the whole first-load burst to finish so scenario timings measure
  // the interaction and not the tail of startup.
  await page.waitForSelector(SLIDER_START, { timeout: 30_000 });
  await page.evaluate(() => window.__bench.settle(300, 10_000));
  // Startup is over: from here on, engine counters measure the interaction.
  await markCdpBaseline?.();
}

export const scenarios = [
  {
    name: "cold-load",
    description: "First visit to the map: navigation start → markers on screen.",
    async run({ page, origin }) {
      const startedAt = Date.now();
      await page.goto(`${origin}/`, { waitUntil: "commit" });
      await page.waitForSelector(HOME_READY_SELECTOR, { timeout: 30_000 });
      const markersVisibleMs = Date.now() - startedAt;
      await page.evaluate(() => window.__bench.settle(300, 15_000));

      const load = await page.evaluate(() => ({
        ...window.__bench.loadMetrics(),
        tasks: window.__bench.tasksSince(0),
        markerCount: window.__bench.markerCount(),
      }));

      return {
        metrics: {
          fcpMs: load.fcpMs,
          lcpMs: load.lcpMs,
          markersVisibleMs,
          loadEventMs: load.loadEventMs,
          blockingMs: load.tasks.blockingMs,
          longTaskMs: load.tasks.totalMs,
          longestTaskMs: load.tasks.longestMs,
          transferredKb: load.transferredKb,
        },
        detail: { markerCount: load.markerCount },
      };
    },
  },

  {
    name: "time-slider-drag",
    description:
      "Dragging the time-of-day filter: 24 consecutive value changes, the heaviest interactive path in the app.",
    async run({ page, origin, markCdpBaseline }) {
      await gotoHome(page, origin, { markCdpBaseline });
      const result = await runBurst(
        page,
        SLIDER_STEPS.map((value) => ({
          kind: "range",
          selector: SLIDER_START,
          value,
          label: `from=${value}`,
        })),
      );
      return { metrics: interactionMetrics(result), detail: { markerCount: result.markerCount } };
    },
  },

  {
    name: "service-type-switch",
    description: "Switching between Mass / Confession / Adoration (3 cycles).",
    async run({ page, origin, markCdpBaseline }) {
      await gotoHome(page, origin, { markCdpBaseline });
      await tagServiceButtons(page);
      const order = ["confession", "adoration", "mass"];
      const steps = [];
      for (let cycle = 0; cycle < 3; cycle += 1) {
        for (const type of order) {
          steps.push({ kind: "click", selector: buttonSelector(type), label: type });
        }
      }
      const result = await runBurst(page, steps, { gapMs: 120 });
      return { metrics: interactionMetrics(result), detail: { markerCount: result.markerCount } };
    },
  },

  {
    name: "day-toggle",
    description: "Toggling weekday chips on and off across the whole week.",
    async run({ page, origin, markCdpBaseline }) {
      await gotoHome(page, origin, { markCdpBaseline });
      const days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ];
      const steps = [...days, ...days].map((day) => ({
        kind: "click",
        selector: `button[aria-label="${day}"]`,
        label: day,
      }));
      const result = await runBurst(page, steps, { gapMs: 80 });
      return { metrics: interactionMetrics(result), detail: { markerCount: result.markerCount } };
    },
  },

  {
    name: "search-typing",
    description: "Typing a parish name into the search box, one keystroke at a time.",
    async run({ page, origin, markCdpBaseline }) {
      await gotoHome(page, origin, { markCdpBaseline });
      const steps = [{ kind: "focus", selector: SEARCH_INPUT, label: "focus" }];
      for (let i = 1; i <= TYPED_QUERY.length; i += 1) {
        steps.push({
          kind: "text",
          selector: SEARCH_INPUT,
          value: TYPED_QUERY.slice(0, i),
          label: `key-${i}`,
        });
      }
      const result = await runBurst(page, steps, { gapMs: 60 });
      return { metrics: interactionMetrics(result), detail: {} };
    },
  },

  {
    name: "parish-popup-and-nav",
    description:
      "Opening a map pin's popup, then following it through to the parish page (client-side route).",
    async run({ page, origin, markCdpBaseline }) {
      await gotoHome(page, origin, { markCdpBaseline });

      const popup = await page.evaluate(async () => {
        const bench = window.__bench;
        const marker = document.querySelector(".leaflet-marker-icon");
        if (!marker) throw new Error("no marker to click");
        const startedAt = bench.now();
        const sample = await bench.measure(() => {
          marker.dispatchEvent(
            new MouseEvent("mousedown", { bubbles: true, cancelable: true }),
          );
          marker.dispatchEvent(
            new MouseEvent("mouseup", { bubbles: true, cancelable: true }),
          );
          marker.dispatchEvent(new MouseEvent("click", { bubbles: true, cancelable: true }));
        });
        // The popup content mounts through a React portal after Leaflet opens
        // the popup, so wait for the anchor rather than a fixed delay.
        const deadline = bench.now() + 5000;
        while (!document.querySelector('.leaflet-popup a[href^="/churches/"]')) {
          if (bench.now() > deadline) throw new Error("popup never opened");
          await new Promise((resolve) => requestAnimationFrame(resolve));
        }
        const openedMs = bench.now() - startedAt;
        return { ...sample, openedMs, tasks: bench.tasksSince(startedAt) };
      });

      const navigation = await page.evaluate(async () => {
        const bench = window.__bench;
        const link = document.querySelector('.leaflet-popup a[href^="/churches/"]');
        if (!link) throw new Error("popup link missing");
        const startedAt = bench.now();
        link.click();
        const deadline = startedAt + 10_000;
        while (!document.querySelector("main h1.font-display")) {
          if (bench.now() > deadline) throw new Error("parish page never rendered");
          await new Promise((resolve) => requestAnimationFrame(resolve));
        }
        const contentMs = bench.now() - startedAt;
        const settleMs = await bench.settle(250);
        return { contentMs, settleMs, tasks: bench.tasksSince(startedAt) };
      });

      return {
        metrics: {
          popupPaintMs: popup.paintMs,
          popupOpenMs: popup.openedMs,
          popupBlockingMs: popup.tasks.blockingMs,
          navContentMs: navigation.contentMs,
          navSettleMs: navigation.settleMs,
          navBlockingMs: navigation.tasks.blockingMs,
        },
        detail: {},
      };
    },
  },
];

/** Turn a burst result into the metric set every interaction scenario reports. */
function interactionMetrics(result) {
  const paints = result.samples.map((s) => s.paintMs);
  const syncs = result.samples.map((s) => s.syncMs);
  return {
    paintP50Ms: percentile(paints, 50),
    paintP95Ms: percentile(paints, 95),
    paintMaxMs: Math.max(...paints),
    syncP50Ms: percentile(syncs, 50),
    syncTotalMs: syncs.reduce((sum, v) => sum + v, 0),
    settleMs: result.settleMs,
    blockingMs: result.tasks.blockingMs,
    longTaskMs: result.tasks.totalMs,
    longestTaskMs: result.tasks.longestMs,
    longTaskCount: result.tasks.count,
  };
}

export function percentile(values, p) {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const index = Math.min(
    sorted.length - 1,
    Math.max(0, Math.ceil((p / 100) * sorted.length) - 1),
  );
  return sorted[index];
}
