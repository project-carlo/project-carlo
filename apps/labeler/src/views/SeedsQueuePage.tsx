import { useEffect, useState } from "react";
import { api } from "../api";
import { navigate, seedHref } from "../lib/route";
import { nextSeedToReview } from "../lib/seeds";
import { SEED_STATUS_LABEL, SEED_STATUS_STYLE } from "../lib/seedStatus";
import type { Config, SeedQueueRow } from "../types";

interface Props {
  config: Config | null;
  labeler: string;
  onLabelerChange: (name: string) => void;
}

export function SeedsQueuePage({ config, labeler, onLabelerChange }: Props) {
  const [seeds, setSeeds] = useState<SeedQueueRow[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState("");

  useEffect(() => {
    api
      .seeds()
      .then((r) => setSeeds(r.seeds))
      .catch((e: Error) => setError(e.message));
  }, []);

  const shown = (seeds ?? []).filter((s) => !status || s.status === status);
  const counts = new Map<string, number>();
  for (const s of seeds ?? []) counts.set(s.status, (counts.get(s.status) ?? 0) + 1);
  const nextToReview = nextSeedToReview(seeds ?? []);

  return (
    <div className="mx-auto flex h-full max-w-6xl flex-col p-6">
      <header className="mb-4 flex flex-wrap items-center gap-3">
        <a href="#/" className="text-sm text-sky-700 hover:underline">
          ← Bulletins
        </a>
        <h1 className="text-xl font-semibold">Seeds</h1>
        {config?.mode === "demo" && (
          <span className="rounded bg-amber-200 px-2 py-0.5 text-xs font-semibold text-amber-900">DEMO DATA</span>
        )}
        {config && (
          <span className="text-xs text-slate-500">
            Seed files in <code>{config.seeds_dir}</code>
          </span>
        )}
        <label className="ml-auto flex items-center gap-2 text-sm text-slate-600">
          Reviewer
          <input
            value={labeler}
            onChange={(e) => onLabelerChange(e.target.value)}
            className="rounded border border-slate-300 bg-white px-2 py-1 text-sm"
            placeholder="Your name"
          />
        </label>
      </header>

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded border border-slate-300 bg-white px-2 py-1 text-sm">
          <option value="">Any status</option>
          {Object.entries(SEED_STATUS_LABEL).map(([value, label]) => (
            <option key={value} value={value}>
              {label} ({counts.get(value) ?? 0})
            </option>
          ))}
        </select>
        <span className="text-sm text-slate-500">{shown.length} parishes</span>
        <button
          className="btn-primary ml-auto"
          disabled={!nextToReview}
          onClick={() => nextToReview && navigate(seedHref(nextToReview.parish_slug))}
          data-testid="next-seed"
        >
          Next to review →
        </button>
      </div>

      {error && <div className="mb-3 rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">{error}</div>}
      {!seeds && !error && <p className="text-slate-500">Loading…</p>}
      {seeds && seeds.length === 0 && (
        <p className="text-slate-500">
          No seed files yet. An agent drafts them with the <code>seed-parishes</code> skill (<code>pnpm seed</code>).
        </p>
      )}

      <div className="flex-1 overflow-y-auto rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead className="sticky top-0 bg-slate-50 text-left text-xs tracking-wide text-slate-500 uppercase">
            <tr>
              <th className="px-3 py-2">Parish</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2 text-right">Open</th>
              <th className="px-3 py-2 text-right">Slots</th>
              <th className="px-3 py-2 text-right">Calls</th>
              <th className="px-3 py-2">As of</th>
              <th className="px-3 py-2">Database</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((s) => (
              <tr
                key={s.parish_slug}
                className="cursor-pointer border-t border-slate-100 hover:bg-sky-50"
                onClick={() => navigate(seedHref(s.parish_slug))}
                title={s.problem ?? s.blocked_reason ?? s.summary}
              >
                <td className="px-3 py-1.5">
                  <a href={seedHref(s.parish_slug)} className="font-medium text-slate-800 hover:underline">
                    {s.parish_name}
                  </a>
                  {s.church_list_issues > 0 && (
                    <span className="ml-2 text-xs text-slate-500" title="Churches or chapels the bulletins name that the church list lacks">
                      {s.church_list_issues} for the church list
                    </span>
                  )}
                </td>
                <td className="px-3 py-1.5">
                  <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${SEED_STATUS_STYLE[s.status]}`}>{SEED_STATUS_LABEL[s.status]}</span>
                </td>
                <td className="px-3 py-1.5 text-right tabular-nums">{s.open_questions || "—"}</td>
                <td className="px-3 py-1.5 text-right tabular-nums">{s.included}</td>
                <td className="px-3 py-1.5 text-right text-slate-500 tabular-nums">
                  {s.calls ? `${s.calls} · $${s.cost_usd.toFixed(3)}` : "—"}
                </td>
                <td className="px-3 py-1.5 text-slate-500 tabular-nums">{s.as_of?.slice(0, 10) ?? "—"}</td>
                <td className="px-3 py-1.5 text-slate-500">{s.loaded ? "loaded" : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
