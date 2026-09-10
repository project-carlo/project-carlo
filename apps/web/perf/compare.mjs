#!/usr/bin/env node
// Compare two saved benchmark results:
//   node perf/compare.mjs baseline candidate
// Names resolve to perf/results/<name>.json; explicit paths also work.
import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { formatComparison } from "./report.mjs";

const RESULTS_DIR = join(dirname(fileURLToPath(import.meta.url)), "results");

function load(name) {
  const path = name.endsWith(".json") ? resolve(name) : join(RESULTS_DIR, `${name}.json`);
  if (!existsSync(path)) {
    console.error(`No result file at ${path}`);
    process.exit(1);
  }
  return JSON.parse(readFileSync(path, "utf8"));
}

const [baseline, candidate] = process.argv.slice(2);
if (!baseline || !candidate) {
  console.error("Usage: node perf/compare.mjs <baseline> <candidate>");
  process.exit(1);
}

console.log(formatComparison(load(baseline), load(candidate)));
