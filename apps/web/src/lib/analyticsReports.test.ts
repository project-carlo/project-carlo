import { describe, expect, it } from "vitest";
import {
  analyticsReports,
  loadAnalyticsDashboard,
  parseReportOptions,
  queryAnalytics,
} from "./analyticsReports";

const CREDENTIALS = { accountId: "acct", apiToken: "token" };

describe("parseReportOptions", () => {
  it("defaults to the last week on the given host", () => {
    expect(parseReportOptions({ defaultHost: "projectcarlo.com" })).toEqual({
      host: "projectcarlo.com",
      days: 7,
      limit: 15,
    });
  });

  it("reads what it's given", () => {
    expect(
      parseReportOptions({
        days: "30",
        host: "Branch.example.workers.dev",
        limit: "5",
        defaultHost: "projectcarlo.com",
      }),
    ).toEqual({ host: "branch.example.workers.dev", days: 30, limit: 5 });
  });

  it("falls back to the default host for an empty one", () => {
    expect(parseReportOptions({ host: "", defaultHost: "projectcarlo.com" })).toMatchObject({
      host: "projectcarlo.com",
    });
  });

  it("refuses anything that could reach the SQL unchecked", () => {
    for (const raw of [
      { days: "0" },
      { days: "91" },
      { days: "7.5" },
      { days: "7; DROP" },
      { limit: "0" },
      { limit: "1000" },
      { host: "x' OR '1'='1" },
      { host: "a b" },
    ]) {
      expect(parseReportOptions({ ...raw, defaultHost: "projectcarlo.com" })).toHaveProperty(
        "error",
      );
    }
  });
});

describe("analyticsReports", () => {
  it("scopes every report to the host and the period", () => {
    const reports = analyticsReports({ host: "projectcarlo.com", days: 30, limit: 10 });
    expect(reports.map((r) => r.key)).toEqual([
      "daily",
      "pages",
      "landing",
      "referrers",
      "campaigns",
      "countries",
      "devices",
      "actions",
      "churches",
      "outbound",
    ]);
    for (const report of reports) {
      expect(report.sql).toContain("blob3 = 'projectcarlo.com'");
      expect(report.sql).toContain("INTERVAL '30' DAY");
      expect(report.sql).toContain("SUM(_sample_interval");
    }
  });
});

/** Answers each query as the SQL API would, quoting 64-bit integers. */
function sqlApi(answer: (sql: string) => Record<string, unknown>[]): typeof fetch {
  return (async (_input: RequestInfo | URL, init?: RequestInit) => {
    const sql = String(init?.body);
    const data = answer(sql);
    const meta = Object.keys(data[0] ?? {}).map((name) => ({
      name,
      type: name === "count" || name === "visits" ? "UInt64" : "String",
    }));
    return Response.json({ meta, data, rows: data.length });
  }) as typeof fetch;
}

describe("queryAnalytics", () => {
  it("turns quoted integers into numbers", async () => {
    const rows = await queryAnalytics(
      "SELECT",
      CREDENTIALS,
      sqlApi(() => [{ page: "/", count: "42" }]),
    );
    expect(rows).toEqual([{ page: "/", count: 42 }]);
  });

  it("sends the token and reports a failure", async () => {
    let auth: string | null = null;
    const failing = (async (_input: RequestInfo | URL, init?: RequestInit) => {
      auth = new Headers(init?.headers).get("Authorization");
      return new Response("bad token", { status: 401 });
    }) as typeof fetch;
    await expect(queryAnalytics("SELECT 1", CREDENTIALS, failing)).rejects.toThrow(/HTTP 401/);
    expect(auth).toBe("Bearer token");
  });
});

describe("loadAnalyticsDashboard", () => {
  it("returns the hosts and every report in order", async () => {
    const data = await loadAnalyticsDashboard(
      { host: "projectcarlo.com", days: 7, limit: 15 },
      CREDENTIALS,
      sqlApi((sql) =>
        sql.includes("AS host, SUM") && !sql.includes("blob3 =")
          ? [{ host: "projectcarlo.com", count: "10" }]
          : [{ label: "x", count: "1" }],
      ),
    );
    expect(data.hosts).toEqual(["projectcarlo.com"]);
    expect(data.reports).toHaveLength(10);
    expect(data.reports[1]).toEqual({ key: "pages", title: "Top pages", rows: [{ label: "x", count: 1 }] });
  });
});
