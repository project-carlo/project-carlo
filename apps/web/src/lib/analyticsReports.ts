/**
 * The visitor-analytics reports, as SQL for the Analytics Engine dataset the
 * Worker writes (docs/analytics.md), and the client that runs them. Shared by
 * `pnpm analytics` (scripts/analytics-report.ts), which prints them, and the
 * Worker's dashboard endpoint (worker/index.ts), which the dashboard page
 * (src/views/AnalyticsDashboardPage.tsx) draws, so the two always agree.
 */

export const ANALYTICS_DATASET = "project_carlo_events";

/** The Worker route the dashboard page reads; behind Cloudflare Access. */
export const ANALYTICS_DASHBOARD_API_PATH = "/api/admin/analytics";

/** Where the dashboard page lives; behind Cloudflare Access too. */
export const ANALYTICS_DASHBOARD_PATH = "/admin/analytics";

/** Analytics Engine keeps three months of data. */
export const MAX_REPORT_DAYS = 90;

export type AnalyticsRow = Record<string, string | number>;

export interface ReportOptions {
  /** The host that served the pages: projectcarlo.com or a preview's. */
  host: string;
  days: number;
  /** Rows per ranked report. */
  limit: number;
}

export interface AnalyticsReport {
  /** Stable name the dashboard draws each report by. */
  key: ReportKey;
  title: string;
  sql: string;
}

export type ReportKey =
  | "daily"
  | "pages"
  | "landing"
  | "referrers"
  | "campaigns"
  | "countries"
  | "devices"
  | "actions"
  | "churches"
  | "outbound";

/** What the dashboard endpoint answers with. */
export interface AnalyticsDashboardData {
  host: string;
  days: number;
  /** Hosts with pageviews in the last three months, busiest first. */
  hosts: string[];
  reports: { key: ReportKey; title: string; rows: AnalyticsRow[] }[];
}

export interface AnalyticsCredentials {
  accountId: string;
  /** A token with Account → Account Analytics → Read. */
  apiToken: string;
}

/**
 * Checks report options from a command line or a query string, before any of
 * them reach SQL: `days` and `limit` whole numbers, `host` a hostname. Returns
 * the options, or what's wrong with them.
 */
export function parseReportOptions(raw: {
  days?: string | null;
  host?: string | null;
  limit?: string | null;
  defaultHost: string;
}): ReportOptions | { error: string } {
  const days = Number(raw.days ?? "7");
  const limit = Number(raw.limit ?? "15");
  const host = (raw.host || raw.defaultHost).toLowerCase();
  if (!Number.isInteger(days) || days < 1 || days > MAX_REPORT_DAYS) {
    return {
      error: `days must be a whole number from 1 to ${MAX_REPORT_DAYS} (the dataset keeps three months).`,
    };
  }
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) {
    return { error: "limit must be a whole number from 1 to 100." };
  }
  if (!/^[a-z0-9.-]{1,253}$/.test(host)) return { error: `host isn't a hostname: ${host}` };
  return { host, days, limit };
}

/**
 * The reports, in the order they're shown. Analytics Engine samples heavy
 * traffic, so counts sum each row's _sample_interval (how many events it
 * stands for) rather than COUNT(). Ranked reports name their count column
 * `count` and put it last; every column before it is a label.
 */
export function analyticsReports({ host, days, limit }: ReportOptions): AnalyticsReport[] {
  const scope = `blob3 = '${host}' AND timestamp > NOW() - INTERVAL '${days}' DAY`;
  const pageviews = `${scope} AND blob1 = 'pageview'`;

  /** Events counted by `column`, most first; `where` narrows them. */
  const breakdown = (column: string, label: string, where: string): string =>
    `SELECT ${column} AS ${label}, SUM(_sample_interval) AS count FROM ${ANALYTICS_DATASET} ` +
    `WHERE ${where} GROUP BY ${label} ORDER BY count DESC LIMIT ${limit}`;

  return [
    {
      key: "daily",
      title: "Visits and pageviews by day (UTC)",
      sql:
        `SELECT toStartOfInterval(timestamp, INTERVAL '1' DAY) AS day, ` +
        `SUM(_sample_interval * double1) AS visits, SUM(_sample_interval) AS pageviews ` +
        `FROM ${ANALYTICS_DATASET} WHERE ${pageviews} GROUP BY day ORDER BY day`,
    },
    { key: "pages", title: "Top pages", sql: breakdown("blob2", "page", pageviews) },
    {
      key: "landing",
      title: "Landing pages (where visits began)",
      sql: breakdown("blob2", "page", `${pageviews} AND double1 = 1`),
    },
    {
      key: "referrers",
      title: "Referring sites",
      sql: breakdown("blob9", "referrer", `${pageviews} AND blob9 != ''`),
    },
    {
      key: "campaigns",
      title: "Campaigns (utm_source)",
      sql: breakdown("blob10", "campaign", `${pageviews} AND blob10 != ''`),
    },
    { key: "countries", title: "Countries", sql: breakdown("blob4", "country", pageviews) },
    { key: "devices", title: "Devices", sql: breakdown("blob5", "device", pageviews) },
    {
      key: "actions",
      title: "Actions",
      sql:
        `SELECT blob1 AS event, blob6 AS kind, SUM(_sample_interval) AS count FROM ${ANALYTICS_DATASET} ` +
        `WHERE ${scope} AND blob1 != 'pageview' GROUP BY event, kind ORDER BY count DESC LIMIT ${limit * 2}`,
    },
    {
      key: "churches",
      title: "Churches picked in search",
      sql: breakdown("blob7", "church", `${scope} AND blob1 = 'search_select' AND blob6 = 'church'`),
    },
    {
      key: "outbound",
      title: "Links followed off the site",
      sql:
        `SELECT blob6 AS kind, blob7 AS host, SUM(_sample_interval) AS count FROM ${ANALYTICS_DATASET} ` +
        `WHERE ${scope} AND blob1 = 'outbound' GROUP BY kind, host ORDER BY count DESC LIMIT ${limit}`,
    },
  ];
}

/** The hosts with pageviews in the dataset's three months, busiest first. */
export const HOSTS_SQL =
  `SELECT blob3 AS host, SUM(_sample_interval) AS count FROM ${ANALYTICS_DATASET} ` +
  `WHERE blob1 = 'pageview' AND timestamp > NOW() - INTERVAL '${MAX_REPORT_DAYS}' DAY ` +
  `GROUP BY host ORDER BY count DESC LIMIT 20`;

interface SqlApiResponse {
  meta?: { name: string; type: string }[];
  data: AnalyticsRow[];
}

/**
 * Runs one query on the Analytics Engine SQL API. Numeric columns come back
 * as numbers: the API, like ClickHouse, quotes 64-bit integers in JSON.
 */
export async function queryAnalytics(
  sql: string,
  { accountId, apiToken }: AnalyticsCredentials,
  fetchImpl: typeof fetch = fetch,
): Promise<AnalyticsRow[]> {
  const res = await fetchImpl(
    `https://api.cloudflare.com/client/v4/accounts/${encodeURIComponent(accountId)}/analytics_engine/sql`,
    { method: "POST", headers: { Authorization: `Bearer ${apiToken}` }, body: sql },
  );
  const text = await res.text();
  if (!res.ok) throw new Error(`Analytics Engine answered HTTP ${res.status}: ${text.slice(0, 500)}`);
  const { meta, data } = JSON.parse(text) as SqlApiResponse;
  const numeric = new Set(
    (meta ?? []).filter((m) => /Int|Float|Decimal/.test(m.type)).map((m) => m.name),
  );
  if (numeric.size === 0) return data;
  return data.map((row) => {
    const out: AnalyticsRow = { ...row };
    for (const name of numeric) if (name in out) out[name] = Number(out[name]);
    return out;
  });
}

/** Every report, and the hosts to choose between, queried at once. */
export async function loadAnalyticsDashboard(
  options: ReportOptions,
  credentials: AnalyticsCredentials,
  fetchImpl: typeof fetch = fetch,
): Promise<AnalyticsDashboardData> {
  const reports = analyticsReports(options);
  const [hostRows, ...results] = await Promise.all([
    queryAnalytics(HOSTS_SQL, credentials, fetchImpl),
    ...reports.map((report) => queryAnalytics(report.sql, credentials, fetchImpl)),
  ]);
  return {
    host: options.host,
    days: options.days,
    hosts: hostRows.map((row) => String(row.host)),
    reports: reports.map((report, i) => ({ key: report.key, title: report.title, rows: results[i] })),
  };
}
