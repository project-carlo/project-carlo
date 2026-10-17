/**
 * Prints what visitors did on the site, from the Analytics Engine dataset the
 * Worker writes (see docs/analytics.md): visits and pageviews by day, the top
 * pages, where visitors came from, and what they did. The reports are shared
 * with the dashboard at /admin/analytics (src/lib/analyticsReports.ts).
 *
 *   pnpm analytics                       # the last 7 days on projectcarlo.com
 *   pnpm analytics --days 30
 *   pnpm analytics --host my-branch-project-carlo.example.workers.dev
 *   pnpm analytics --sql "SELECT blob7, SUM(_sample_interval) AS n FROM project_carlo_events WHERE blob1 = 'search_select' GROUP BY blob7 ORDER BY n DESC"
 *
 * Needs CLOUDFLARE_ACCOUNT_ID and a CLOUDFLARE_API_TOKEN with the "Account
 * Analytics: Read" permission, from the environment or the repo's .env.
 */
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { parseArgs } from "node:util";
import {
  analyticsReports,
  parseReportOptions,
  queryAnalytics,
  type AnalyticsRow,
} from "../src/lib/analyticsReports";
import { SITE_ORIGIN } from "../src/lib/seo";

const ROOT_ENV = resolve(import.meta.dirname, "..", "..", "..", ".env");

const { values } = parseArgs({
  options: {
    days: { type: "string", default: "7" },
    host: { type: "string", default: new URL(SITE_ORIGIN).hostname },
    limit: { type: "string", default: "15" },
    sql: { type: "string" },
  },
});

const options = parseReportOptions({
  days: values.days,
  host: values.host,
  limit: values.limit,
  defaultHost: new URL(SITE_ORIGIN).hostname,
});
if ("error" in options) throw new Error(`--${options.error}`);

if (existsSync(ROOT_ENV)) process.loadEnvFile(ROOT_ENV);
const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
const apiToken = process.env.CLOUDFLARE_API_TOKEN;
if (!accountId || !apiToken) {
  throw new Error(
    "Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN (with Account Analytics: Read) " +
      "in the environment or the repo's .env.",
  );
}
const credentials = { accountId, apiToken };

function printTable(title: string, rows: AnalyticsRow[]): void {
  console.log(`\n${title}`);
  if (rows.length === 0) {
    console.log("  (nothing yet)");
    return;
  }
  const columns = Object.keys(rows[0]);
  const cells = rows.map((row) => columns.map((column) => String(row[column] ?? "")));
  const widths = columns.map((column, i) =>
    Math.max(column.length, ...cells.map((line) => line[i].length)),
  );
  const format = (line: string[]) =>
    "  " + line.map((cell, i) => (i === 0 ? cell.padEnd(widths[i]) : cell.padStart(widths[i]))).join("  ");
  console.log(format(columns));
  for (const line of cells) console.log(format(line));
}

if (values.sql) {
  printTable("Query", await queryAnalytics(values.sql, credentials));
  process.exit(0);
}

const { host, days } = options;
console.log(`${host}, last ${days} day${days === 1 ? "" : "s"}`);
const reports = analyticsReports(options);
const results = await Promise.all(reports.map((report) => queryAnalytics(report.sql, credentials)));
reports.forEach((report, i) => printTable(report.title, results[i]));
