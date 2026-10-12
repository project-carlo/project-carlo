import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useDocumentMeta } from "@/hooks/useDocumentMeta";
import {
  ANALYTICS_DASHBOARD_API_PATH,
  type AnalyticsDashboardData,
  type AnalyticsRow,
} from "@/lib/analyticsReports";
import { fillDays, niceMax, rowCount, rowLabel, type DayTotals } from "@/lib/analyticsDashboard";
import { cn } from "@/lib/utils";

/** The periods offered; any 1–90 works in the URL. */
const PERIODS = [7, 30, 90];

const numbers = new Intl.NumberFormat("en-US");
const dayLabel = new Intl.DateTimeFormat("en-US", {
  weekday: "short",
  month: "short",
  day: "numeric",
  timeZone: "UTC",
});
const shortDay = new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", timeZone: "UTC" });

class DashboardError extends Error {
  constructor(
    message: string,
    /** 0 when Cloudflare Access sent the request to its sign-in page. */
    readonly status: number,
  ) {
    super(message);
  }
}

async function fetchDashboard(days: string, host: string): Promise<AnalyticsDashboardData> {
  const params = new URLSearchParams({ days });
  if (host) params.set("host", host);
  // Access answers an expired sign-in with a redirect to its own login page,
  // which fetch can't follow across origins; "manual" turns it into an
  // opaque answer the page can recognize and reload for.
  const res = await fetch(`${ANALYTICS_DASHBOARD_API_PATH}?${params}`, { redirect: "manual" });
  if (res.type === "opaqueredirect") throw new DashboardError("Your sign-in has expired.", 0);
  if (!res.ok) {
    let message = `The dashboard answered HTTP ${res.status}.`;
    try {
      message = ((await res.json()) as { error?: string }).error ?? message;
    } catch {
      // Not JSON: keep the status.
    }
    throw new DashboardError(message, res.status);
  }
  return (await res.json()) as AnalyticsDashboardData;
}

/**
 * The visitor analytics `pnpm analytics` prints, as a page that reads well on
 * a phone: visits by day, then each ranked report. It lives at
 * /admin/analytics behind Cloudflare Access, and the Worker checks Access's
 * sign-in again before it answers (docs/analytics.md). It records no
 * pageview of its own (AppLayout).
 */
export function AnalyticsDashboardPage() {
  useDocumentMeta({ title: "Visitor analytics · Project Carlo", noindex: true });
  const [params, setParams] = useSearchParams();
  const days = params.get("days") ?? "7";
  const host = params.get("host") ?? "";

  const query = useQuery({
    queryKey: ["analytics-dashboard", days, host],
    queryFn: () => fetchDashboard(days, host),
    placeholderData: keepPreviousData,
    retry: (count, error) => !(error instanceof DashboardError) && count < 2,
  });
  const data = query.data;

  const choose = (key: "days" | "host", value: string) => {
    const next = new URLSearchParams(params);
    next.set(key, value);
    setParams(next, { replace: true });
  };

  return (
    <main className="min-h-svh bg-paper px-4 pt-6 pb-12">
      <div className="mx-auto flex max-w-3xl flex-col gap-6">
        <header className="flex flex-col gap-3">
          <div>
            <h1 className="font-display text-[1.75rem] leading-[1.1] text-ink">Visitor analytics</h1>
            <p className="font-serif text-sm text-ink-soft">
              {data ? `${data.host}, last ${data.days} day${data.days === 1 ? "" : "s"}` : "Loading…"}
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <div role="group" aria-label="Period" className="flex rounded-sm border border-rule-strong">
              {PERIODS.map((period) => (
                <button
                  key={period}
                  type="button"
                  aria-pressed={days === String(period)}
                  onClick={() => choose("days", String(period))}
                  className={cn(
                    "min-h-9 px-3 font-serif text-sm lining-nums",
                    days === String(period) ? "bg-ink text-paper" : "text-ink hover:bg-paper-deep",
                  )}
                >
                  {period} days
                </button>
              ))}
            </div>
            {data && data.hosts.length > 1 ? (
              <label className="flex min-w-0 items-center gap-2 font-serif text-sm text-ink-soft">
                Site
                <select
                  value={data.host}
                  onChange={(event) => choose("host", event.target.value)}
                  className="min-h-9 max-w-[16rem] min-w-0 rounded-sm border border-rule-strong bg-paper px-2 text-ink"
                >
                  {[...new Set([data.host, ...data.hosts])].map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </label>
            ) : null}
          </div>
        </header>

        {query.error ? <DashboardProblem error={query.error} onRetry={() => void query.refetch()} /> : null}

        {data ? (
          // A new period or site keeps the old numbers, dimmed, until the new ones arrive.
          <div className={cn("flex flex-col gap-6 transition-opacity", query.isPlaceholderData && "opacity-50")}>
            <Dashboard data={data} />
          </div>
        ) : null}
      </div>
    </main>
  );
}

function DashboardProblem({ error, onRetry }: { error: Error; onRetry: () => void }) {
  const status = error instanceof DashboardError ? error.status : -1;
  const signIn = status === 0 || status === 403;
  return (
    <div role="alert" className="flex flex-col items-start gap-2 border-l-2 border-rubric pl-3">
      <p className="font-serif text-base text-ink">{error.message}</p>
      {signIn ? (
        <button type="button" onClick={() => window.location.reload()} className="rubric-link font-serif text-sm">
          Sign in again
        </button>
      ) : status === 503 ? (
        <p className="font-serif text-sm text-ink-soft">See “The dashboard” in docs/analytics.md.</p>
      ) : (
        <button type="button" onClick={onRetry} className="rubric-link font-serif text-sm">
          Try again
        </button>
      )}
    </div>
  );
}

function Dashboard({ data }: { data: AnalyticsDashboardData }) {
  const daily = fillDays(data.reports.find((r) => r.key === "daily")?.rows ?? [], data.days);
  const visits = daily.reduce((sum, day) => sum + day.visits, 0);
  const pageviews = daily.reduce((sum, day) => sum + day.pageviews, 0);
  const ranked = data.reports.filter((r) => r.key !== "daily");

  return (
    <>
      <dl className="grid grid-cols-3 gap-3">
        <StatTile label="Visits" value={numbers.format(visits)} />
        <StatTile label="Pageviews" value={numbers.format(pageviews)} />
        <StatTile label="Pages per visit" value={visits ? (pageviews / visits).toFixed(1) : "–"} />
      </dl>
      <DailyChart days={daily} />
      <div className="grid gap-x-8 gap-y-6 sm:grid-cols-2">
        {ranked.map((report) => (
          <RankedReport key={report.key} reportKey={report.key} title={report.title} rows={report.rows} />
        ))}
      </div>
      <p className="font-serif text-xs text-ink-faint">
        The same reports as <code>pnpm analytics</code>. Days are in UTC.
      </p>
    </>
  );
}

function StatTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-0.5 border-t border-rule-strong pt-2">
      <dt className="font-serif text-xs text-ink-soft">{label}</dt>
      <dd className="font-display text-[1.625rem] leading-none text-ink lining-nums">{value}</dd>
    </div>
  );
}

/**
 * Visits per day as columns. Hovering or tapping a day (or focusing it) shows
 * its numbers above the chart; the table under it has them all.
 */
function DailyChart({ days }: { days: DayTotals[] }) {
  const [selected, setSelected] = useState<number | null>(null);
  const top = niceMax(Math.max(...days.map((day) => day.visits)));
  const shown = days[selected ?? days.length - 1];

  return (
    <section aria-labelledby="daily-title" className="flex flex-col gap-2">
      <div className="flex flex-wrap items-baseline justify-between gap-x-3">
        <h2 id="daily-title" className="font-display text-lg text-ink">
          Visits by day
        </h2>
        <p aria-live="polite" className="font-serif text-sm text-ink-soft lining-nums">
          {dayLabel.format(new Date(shown.date))}:{" "}
          <strong className="font-semibold text-ink">{numbers.format(shown.visits)}</strong> visits,{" "}
          <strong className="font-semibold text-ink">{numbers.format(shown.pageviews)}</strong> pageviews
        </p>
      </div>

      <div className="flex gap-2">
        <div className="flex h-40 w-10 shrink-0 flex-col justify-between text-right font-serif text-xs text-ink-faint tabular-nums lining-nums">
          <span className="-translate-y-1/2">{numbers.format(top)}</span>
          <span>{numbers.format(top / 2)}</span>
          <span className="translate-y-1/2">0</span>
        </div>
        <div className="relative h-40 flex-1" onPointerLeave={() => setSelected(null)}>
          {/* Hairline gridlines at the top, middle and baseline. */}
          <div aria-hidden className="absolute inset-0 flex flex-col justify-between">
            <div className="border-t border-rule" />
            <div className="border-t border-rule" />
            <div className="border-t border-rule-strong" />
          </div>
          <div className="absolute inset-0 flex items-end gap-[2px]">
            {days.map((day, i) => (
              <button
                key={day.date}
                type="button"
                aria-label={`${dayLabel.format(new Date(day.date))}: ${day.visits} visits, ${day.pageviews} pageviews`}
                onPointerEnter={() => setSelected(i)}
                onFocus={() => setSelected(i)}
                onClick={() => setSelected(i)}
                className="group flex h-full min-w-0 flex-1 items-end justify-center focus-visible:outline-none"
              >
                <span
                  className={cn(
                    "block w-full max-w-6 rounded-t-[4px] transition-colors",
                    i === selected ? "bg-rubric-deep" : "bg-rubric group-focus-visible:bg-rubric-deep",
                  )}
                  style={{
                    height: day.visits ? `max(2px, ${(day.visits / top) * 100}%)` : 0,
                  }}
                />
              </button>
            ))}
          </div>
        </div>
      </div>
      <div className="flex justify-between pl-12 font-serif text-xs text-ink-faint lining-nums">
        <span>{shortDay.format(new Date(days[0].date))}</span>
        <span>{shortDay.format(new Date(days[days.length - 1].date))}</span>
      </div>

      <details className="font-serif text-sm text-ink-soft">
        <summary className="cursor-pointer">Table</summary>
        <table className="mt-2 w-full tabular-nums lining-nums">
          <thead>
            <tr className="text-left text-xs text-ink-faint">
              <th className="font-normal">Day</th>
              <th className="text-right font-normal">Visits</th>
              <th className="text-right font-normal">Pageviews</th>
            </tr>
          </thead>
          <tbody>
            {[...days].reverse().map((day) => (
              <tr key={day.date} className="border-t border-rule">
                <td className="py-1">{dayLabel.format(new Date(day.date))}</td>
                <td className="py-1 text-right text-ink">{numbers.format(day.visits)}</td>
                <td className="py-1 text-right text-ink">{numbers.format(day.pageviews)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </details>
    </section>
  );
}

let regionNames: Intl.DisplayNames | null = null;

/** A country code as its name, where the browser knows it. */
function countryName(code: string): string {
  try {
    regionNames ??= new Intl.DisplayNames(["en"], { type: "region" });
    return regionNames.of(code) ?? code;
  } catch {
    return code;
  }
}

/** One ranked report: a label and count a row, with a bar for the count. */
function RankedReport({ reportKey, title, rows }: { reportKey: string; title: string; rows: AnalyticsRow[] }) {
  const max = Math.max(1, ...rows.map(rowCount));
  const id = `report-${reportKey}`;
  return (
    <section aria-labelledby={id} className="flex min-w-0 flex-col gap-2">
      <h2 id={id} className="font-display text-lg text-ink">
        {title}
      </h2>
      {rows.length === 0 ? (
        <p className="font-serif text-sm text-ink-faint">Nothing yet.</p>
      ) : (
        <ol className="flex flex-col gap-2">
          {rows.map((row, i) => {
            const label = rowLabel(row);
            const count = rowCount(row);
            return (
              <li key={i} className="flex flex-col gap-1">
                <div className="flex items-baseline justify-between gap-3 font-serif text-sm">
                  <span className="min-w-0 truncate text-ink" title={label}>
                    {reportKey === "countries" ? countryName(label) : label}
                  </span>
                  <span className="shrink-0 text-ink-soft tabular-nums lining-nums">{numbers.format(count)}</span>
                </div>
                <div aria-hidden className="h-[3px] rounded-full bg-paper-deep">
                  <div className="h-full rounded-full bg-rubric" style={{ width: `${(count / max) * 100}%` }} />
                </div>
              </li>
            );
          })}
        </ol>
      )}
    </section>
  );
}
