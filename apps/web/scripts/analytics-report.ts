/**
 * Prints what visitors did on the site, from the Analytics Engine dataset the
 * Worker writes (see docs/analytics.md): visits and pageviews by day, the top
 * pages, where visitors came from, and what they did.
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
import { SITE_ORIGIN } from "../src/lib/seo";

const DATASET = "project_carlo_events";
const ROOT_ENV = resolve(import.meta.dirname, "..", "..", "..", ".env");

type Row = Record<string, string | number>;

const { values } = parseArgs({
  options: {
    days: { type: "string", default: "7" },
    host: { type: "string", default: new URL(SITE_ORIGIN).hostname },
    limit: { type: "string", default: "15" },
    sql: { type: "string" },
  },
});

const days = Number(values.days);
const limit = Number(values.limit);
if (!Number.isInteger(days) || days < 1 || days > 90) {
  throw new Error("--days must be a whole number from 1 to 90 (the dataset keeps three months).");
}
if (!Number.isInteger(limit) || limit < 1) throw new Error("--limit must be a positive whole number.");
if (!/^[a-z0-9.-]+$/i.test(values.host)) throw new Error(`--host isn't a hostname: ${values.host}`);

if (existsSync(ROOT_ENV)) process.loadEnvFile(ROOT_ENV);
const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
const apiToken = process.env.CLOUDFLARE_API_TOKEN;
if (!accountId || !apiToken) {
  throw new Error(
    "Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN (with Account Analytics: Read) " +
      "in the environment or the repo's .env.",
  );
}

async function query(sql: string): Promise<Row[]> {
  const res = await fetch(
    `https://api.cloudflare.com/client/v4/accounts/${accountId}/analytics_engine/sql`,
    {
      method: "POST",
      headers: { Authorization: `Bearer ${apiToken}` },
      body: sql,
    },
  );
  const text = await res.text();
  if (!res.ok) throw new Error(`Analytics Engine answered HTTP ${res.status}: ${text}`);
  return (JSON.parse(text) as { data: Row[] }).data;
}

function printTable(title: string, rows: Row[]): void {
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
  printTable("Query", await query(values.sql));
  process.exit(0);
}

// Analytics Engine samples heavy traffic, so counts sum each row's
// _sample_interval (how many events it stands for) rather than COUNT().
const scope = `blob3 = '${values.host}' AND timestamp > NOW() - INTERVAL '${days}' DAY`;
const pageviews = `${scope} AND blob1 = 'pageview'`;

/** Events counted by `column`, most first; `where` narrows them. */
function breakdown(column: string, label: string, where: string): string {
  return (
    `SELECT ${column} AS ${label}, SUM(_sample_interval) AS count FROM ${DATASET} ` +
    `WHERE ${where} GROUP BY ${label} ORDER BY count DESC LIMIT ${limit}`
  );
}

const reports: [string, string][] = [
  [
    "Visits and pageviews by day (UTC)",
    `SELECT toStartOfInterval(timestamp, INTERVAL '1' DAY) AS day, ` +
      `SUM(_sample_interval * double1) AS visits, SUM(_sample_interval) AS pageviews ` +
      `FROM ${DATASET} WHERE ${pageviews} GROUP BY day ORDER BY day`,
  ],
  ["Top pages", breakdown("blob2", "page", pageviews)],
  ["Landing pages (where visits began)", breakdown("blob2", "page", `${pageviews} AND double1 = 1`)],
  ["Referring sites", breakdown("blob9", "referrer", `${pageviews} AND blob9 != ''`)],
  ["Campaigns (utm_source)", breakdown("blob10", "campaign", `${pageviews} AND blob10 != ''`)],
  ["Countries", breakdown("blob4", "country", pageviews)],
  ["Devices", breakdown("blob5", "device", pageviews)],
  [
    "Actions",
    `SELECT blob1 AS event, blob6 AS kind, SUM(_sample_interval) AS count FROM ${DATASET} ` +
      `WHERE ${scope} AND blob1 != 'pageview' GROUP BY event, kind ORDER BY count DESC LIMIT ${limit * 2}`,
  ],
  [
    "Churches picked in search",
    breakdown("blob7", "church", `${scope} AND blob1 = 'search_select' AND blob6 = 'church'`),
  ],
  [
    "Links followed off the site",
    `SELECT blob6 AS kind, blob7 AS host, SUM(_sample_interval) AS count FROM ${DATASET} ` +
      `WHERE ${scope} AND blob1 = 'outbound' GROUP BY kind, host ORDER BY count DESC LIMIT ${limit}`,
  ],
];

console.log(`${values.host}, last ${days} day${days === 1 ? "" : "s"}`);
for (const [title, sql] of reports) printTable(title, await query(sql));
