#!/usr/bin/env node
// Diagnostic companion to bench.mjs: records a V8 CPU profile of one scenario's
// interaction phase and prints the hottest functions by self time.
//
//   node perf/profile.mjs --scenario time-slider-drag [--top 25] [--out profile.cpuprofile]
//
// Use it to find out *why* a scenario is slow; use bench.mjs to find out whether
// a change helped.
import { chromium } from "@playwright/test";
import { existsSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { instrumentationSource } from "./instrument.mjs";
import { stubOffOrigin } from "./network.mjs";
import { scenarios } from "./scenarios.mjs";
import { startStaticServer } from "./static-server.mjs";

const WEB_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const args = process.argv.slice(2);
const options = { scenario: "time-slider-drag", top: 25, cpu: 4, out: null };
for (let i = 0; i < args.length; i += 1) {
  const next = () => args[(i += 1)];
  if (args[i] === "--scenario") options.scenario = next();
  else if (args[i] === "--top") options.top = Number(next());
  else if (args[i] === "--cpu") options.cpu = Number(next());
  else if (args[i] === "--out") options.out = next();
}

const scenario = scenarios.find((s) => s.name === options.scenario);
if (!scenario) {
  console.error(`Unknown scenario: ${options.scenario}`);
  process.exit(1);
}

const dist = join(WEB_ROOT, "dist");
if (!existsSync(join(dist, "index.html"))) {
  console.error("No build found at apps/web/dist. Run `pnpm --filter web build` first.");
  process.exit(1);
}

const server = await startStaticServer({ root: dist });
const browser = await chromium.launch({
  headless: true,
  executablePath: process.env.PERF_CHROMIUM_PATH || undefined,
  args: ["--no-sandbox"],
});
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
await context.addInitScript(instrumentationSource());
// Same stubbing as bench.mjs, so the profile reflects the workload the
// benchmark measures rather than Leaflet's tile-failure path.
await stubOffOrigin(context, server.origin);

const page = await context.newPage();
const client = await context.newCDPSession(page);
await client.send("Profiler.enable");
if (options.cpu > 1) {
  await client.send("Emulation.setCPUThrottlingRate", { rate: options.cpu });
}

// Scenarios call markCdpBaseline once the app has loaded, which is exactly
// where the profile should start.
let profiling = false;
await scenario.run({
  page,
  origin: server.origin,
  client,
  markCdpBaseline: async () => {
    await client.send("Profiler.setSamplingInterval", { interval: 200 });
    await client.send("Profiler.start");
    profiling = true;
  },
});

const { profile } = profiling
  ? await client.send("Profiler.stop")
  : { profile: { nodes: [], samples: [], timeDeltas: [] } };
await browser.close();
await server.close();

const selfTime = new Map();
const byId = new Map(profile.nodes.map((node) => [node.id, node]));
for (let i = 0; i < profile.samples.length; i += 1) {
  const node = byId.get(profile.samples[i]);
  if (!node) continue;
  const { functionName, url, lineNumber } = node.callFrame;
  const key = `${functionName || "(anonymous)"} @ ${shorten(url)}:${lineNumber + 1}`;
  selfTime.set(key, (selfTime.get(key) ?? 0) + (profile.timeDeltas[i] ?? 0) / 1000);
}

function shorten(url) {
  if (!url) return "(native)";
  return url.replace(/^https?:\/\/[^/]+/, "");
}

const total = [...selfTime.values()].reduce((sum, value) => sum + value, 0);
console.log(`\nCPU profile — ${scenario.name} (${options.cpu}x throttle), ${total.toFixed(0)} ms sampled\n`);
for (const [name, ms] of [...selfTime.entries()].sort((a, b) => b[1] - a[1]).slice(0, options.top)) {
  console.log(`${ms.toFixed(1).padStart(9)} ms  ${((ms / total) * 100).toFixed(1).padStart(5)}%  ${name}`);
}

if (options.out) {
  writeFileSync(resolve(options.out), JSON.stringify(profile));
  console.log(`\nWrote ${resolve(options.out)}`);
}
