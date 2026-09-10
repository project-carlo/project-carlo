// Console formatting for benchmark results and A/B comparisons.

/** Metrics where a bigger number is better (none today, but kept explicit). */
const HIGHER_IS_BETTER = new Set();

const UNITS = {
  jsHeapMb: "MB",
  longTaskCount: "",
  markerCount: "",
  domNodes: "",
  transferredKb: "KB",
};

function unit(metric) {
  return metric in UNITS ? UNITS[metric] : "ms";
}

function pad(value, width) {
  return String(value).padEnd(width);
}

function padStart(value, width) {
  return String(value).padStart(width);
}

export function formatSummary(result) {
  const lines = [
    "",
    `UI benchmark — ${result.config.runs} runs/scenario, ${result.config.cpuThrottle}x CPU throttle`,
    "",
  ];
  for (const [name, scenario] of Object.entries(result.scenarios)) {
    lines.push(`${name}  ${scenario.description ? `— ${scenario.description}` : ""}`);
    const rows = Object.entries(scenario.summary);
    const width = Math.max(...rows.map(([metric]) => metric.length));
    for (const [metric, stats] of rows) {
      lines.push(
        `  ${pad(metric, width)}  ${padStart(stats.median, 9)} ${pad(unit(metric), 3)}` +
          `  (min ${stats.min}, max ${stats.max})`,
      );
    }
    lines.push("");
  }
  return lines.join("\n");
}

/**
 * Side-by-side diff of two runs. Percentages are relative to the baseline
 * median; "better" means lower unless the metric is in HIGHER_IS_BETTER.
 */
export function formatComparison(baseline, candidate) {
  const lines = [
    `Comparison — baseline "${baseline.label}" vs "${candidate.label}"`,
    "",
  ];
  for (const [name, scenario] of Object.entries(candidate.scenarios)) {
    const baseScenario = baseline.scenarios[name];
    if (!baseScenario) continue;
    lines.push(name);
    const metrics = Object.keys(scenario.summary);
    const width = Math.max(...metrics.map((m) => m.length));
    for (const metric of metrics) {
      const before = baseScenario.summary[metric]?.median;
      const after = scenario.summary[metric]?.median;
      if (before == null || after == null) continue;
      const delta = after - before;
      const pct = before === 0 ? 0 : (delta / before) * 100;
      const improved = HIGHER_IS_BETTER.has(metric) ? delta > 0 : delta < 0;
      const marker = Math.abs(pct) < 2 ? "  " : improved ? "✓ " : "✗ ";
      lines.push(
        `  ${marker}${pad(metric, width)}  ${padStart(before, 9)} → ${padStart(after, 9)} ` +
          `${pad(unit(metric), 3)}  ${padStart(`${pct >= 0 ? "+" : ""}${pct.toFixed(1)}%`, 8)}`,
      );
    }
    lines.push("");
  }
  return lines.join("\n");
}
