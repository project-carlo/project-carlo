#!/usr/bin/env node
// UI performance benchmark for the web app.
//
//   pnpm --filter web perf                 # run every scenario, print a table
//   pnpm --filter web perf --save mine     # also write perf/results/mine.json
//   pnpm --filter web perf --compare mine
//
// The harness serves the production build, throttles the CPU (default 4x) so
// main-thread work is visible above timer noise, stubs every off-origin request
// (map tiles, place search) so nothing depends on the network, and runs each
// scenario in a fresh browser context N times, reporting the median.
import { chromium } from "@playwright/test";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { instrumentationSource } from "./instrument.mjs";
import { stubOffOrigin } from "./network.mjs";
import { scenarios } from "./scenarios.mjs";
import { startStaticServer } from "./static-server.mjs";
import { formatComparison, formatSummary } from "./report.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));
const WEB_ROOT = resolve(HERE, "..");
const RESULTS_DIR = join(HERE, "results");

function parseArgs(argv) {
  const options = {
    runs: 5,
    cpuThrottle: 4,
    scenario: null,
    save: null,
    compare: null,
    json: null,
    headed: false,
    dist: null,
  };
  // A missing or non-numeric value used to become NaN, which silently ran zero
  // measured iterations and reported an empty scenario. Fail loudly instead.
  const positiveNumber = (flag, raw) => {
    const value = Number(raw);
    if (!Number.isFinite(value) || value <= 0) {
      throw new Error(`${flag} needs a positive number (got ${raw ?? "nothing"})`);
    }
    return value;
  };
  const requireValue = (flag, raw) => {
    if (raw === undefined) throw new Error(`${flag} needs a value`);
    return raw;
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => argv[(i += 1)];
    switch (arg) {
      case "--runs": options.runs = positiveNumber(arg, next()); break;
      case "--cpu": options.cpuThrottle = positiveNumber(arg, next()); break;
      case "--scenario": options.scenario = requireValue(arg, next()); break;
      case "--save": options.save = requireValue(arg, next()); break;
      case "--compare": options.compare = requireValue(arg, next()); break;
      case "--json": options.json = requireValue(arg, next()); break;
      case "--dist": options.dist = requireValue(arg, next()); break;
      case "--headed": options.headed = true; break;
      case "--help":
        printHelp();
        process.exit(0);
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return options;
}

function printHelp() {
  console.log(`UI performance benchmark

Usage: node perf/bench.mjs [options]

  --runs <n>        Repetitions per scenario (default 5; median is reported)
  --cpu <n>         CPU throttling multiplier (default 4; 1 disables)
  --scenario <name> Run only one scenario (${scenarios.map((s) => s.name).join(", ")})
  --save <name>     Write perf/results/<name>.json
  --compare <name>  Compare against perf/results/<name>.json
  --json <path>     Write the raw result JSON to an explicit path
  --dist <path>     Measure this build directory instead of apps/web/dist
  --headed          Run with a visible browser window
`);
}

function resultPath(name) {
  return name.endsWith(".json") ? resolve(name) : join(RESULTS_DIR, `${name}.json`);
}

async function runScenario(browser, scenario, { origin, cpuThrottle }) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1,
    // Keeps the map's tile grid, and therefore the marker set on screen,
    // identical between runs.
    reducedMotion: "reduce",
  });
  await context.addInitScript(instrumentationSource());
  await stubOffOrigin(context, origin);

  const page = await context.newPage();
  const client = await context.newCDPSession(page);
  await client.send("Performance.enable");
  if (cpuThrottle > 1) {
    await client.send("Emulation.setCPUThrottlingRate", { rate: cpuThrottle });
  }

  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));

  // Engine counters are cumulative for the page, so interaction scenarios
  // re-baseline them (via `markCdpBaseline`) once the app has finished loading;
  // load scenarios leave the baseline at context creation and measure startup.
  let before = await cdpMetrics(client);
  const markCdpBaseline = async () => {
    before = await cdpMetrics(client);
  };
  let result;
  try {
    result = await scenario.run({ page, origin, client, markCdpBaseline });
  } finally {
    const after = await cdpMetrics(client);
    result = result ?? { metrics: {}, detail: {} };
    result.metrics = {
      ...result.metrics,
      scriptMs: round((after.ScriptDuration - before.ScriptDuration) * 1000),
      layoutMs: round((after.LayoutDuration - before.LayoutDuration) * 1000),
      recalcStyleMs: round((after.RecalcStyleDuration - before.RecalcStyleDuration) * 1000),
      jsHeapMb: round(after.JSHeapUsedSize / (1024 * 1024)),
      domNodes: after.Nodes,
    };
    await context.close();
  }

  if (errors.length > 0) {
    throw new Error(`page errors during "${scenario.name}":\n${errors.join("\n")}`);
  }
  return result;
}

async function cdpMetrics(client) {
  const { metrics } = await client.send("Performance.getMetrics");
  return Object.fromEntries(metrics.map((m) => [m.name, m.value]));
}

function round(value) {
  return Math.round(value * 100) / 100;
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 === 0 ? (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
}

/** Median-per-metric across runs, plus spread so a noisy metric is obvious. */
function summarize(runs) {
  const names = new Set();
  for (const run of runs) for (const key of Object.keys(run.metrics)) names.add(key);
  const summary = {};
  for (const name of names) {
    const values = runs
      .map((run) => run.metrics[name])
      .filter((value) => typeof value === "number" && Number.isFinite(value));
    if (values.length === 0) continue;
    summary[name] = {
      median: round(median(values)),
      min: round(Math.min(...values)),
      max: round(Math.max(...values)),
    };
  }
  return summary;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  const dist = options.dist ? resolve(options.dist) : join(WEB_ROOT, "dist");
  if (!existsSync(join(dist, "index.html"))) {
    console.error(`No build found at ${dist}. Run \`pnpm --filter web build\` first.`);
    process.exit(1);
  }

  const selected = options.scenario
    ? scenarios.filter((s) => s.name === options.scenario)
    : scenarios;
  if (selected.length === 0) {
    console.error(`Unknown scenario: ${options.scenario}`);
    process.exit(1);
  }

  const server = await startStaticServer({ root: dist });
  const browser = await chromium.launch({
    headless: !options.headed,
    executablePath: process.env.PERF_CHROMIUM_PATH || undefined,
    args: [
      "--no-sandbox",
      // Deterministic compositing/frame pacing for measurement runs.
      "--disable-background-timer-throttling",
      "--disable-renderer-backgrounding",
      "--disable-backgrounding-occluded-windows",
      "--force-device-scale-factor=1",
    ],
  });

  const result = {
    label: options.save ?? "run",
    createdAt: new Date().toISOString(),
    config: { runs: options.runs, cpuThrottle: options.cpuThrottle, dist },
    scenarios: {},
  };

  try {
    for (const scenario of selected) {
      const runs = [];
      process.stdout.write(`▸ ${scenario.name} `);
      // One warm-up pass: the first context pays for code caching and font
      // rasterisation, which would otherwise skew the first measured run.
      await runScenario(browser, scenario, { origin: server.origin, cpuThrottle: options.cpuThrottle });
      for (let i = 0; i < options.runs; i += 1) {
        runs.push(
          await runScenario(browser, scenario, {
            origin: server.origin,
            cpuThrottle: options.cpuThrottle,
          }),
        );
        process.stdout.write(".");
      }
      process.stdout.write("\n");
      result.scenarios[scenario.name] = {
        description: scenario.description,
        summary: summarize(runs),
        runs: runs.map((run) => run.metrics),
      };
    }
  } finally {
    await browser.close();
    await server.close();
  }

  console.log(formatSummary(result));

  if (options.save || options.json) {
    const target = options.json ? resolve(options.json) : resultPath(options.save);
    mkdirSync(dirname(target), { recursive: true });
    writeFileSync(target, `${JSON.stringify(result, null, 2)}\n`);
    console.log(`\nSaved ${target}`);
  }

  if (options.compare) {
    const baselinePath = resultPath(options.compare);
    if (!existsSync(baselinePath)) {
      console.error(`\nNo baseline at ${baselinePath}`);
      process.exit(1);
    }
    const baseline = JSON.parse(readFileSync(baselinePath, "utf8"));
    console.log(`\n${formatComparison(baseline, result)}`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
