import { useEffect, useMemo, useState } from "react";
import { api } from "../api";
import { bulletinHref, navigate } from "../lib/route";
import type { BulletinSummary, Config, Progress } from "../types";

const STATUS_STYLE: Record<BulletinSummary["status"], string> = {
  unlabeled: "bg-slate-100 text-slate-600",
  in_progress: "bg-sky-100 text-sky-800",
  done: "bg-emerald-100 text-emerald-800",
  skipped: "bg-zinc-200 text-zinc-700",
};

const STATUS_LABEL: Record<BulletinSummary["status"], string> = {
  unlabeled: "Unlabeled",
  in_progress: "In progress",
  done: "Done",
  skipped: "Skipped",
};

interface Props {
  config: Config | null;
  labeler: string;
  onLabelerChange: (name: string) => void;
}

export function QueuePage({ config, labeler, onLabelerChange }: Props) {
  const [bulletins, setBulletins] = useState<BulletinSummary[] | null>(null);
  const [progress, setProgress] = useState<Progress | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [parish, setParish] = useState(() => localStorage.getItem("labeler:queue-parish") ?? "");
  const [status, setStatus] = useState("");
  const [latestOnly, setLatestOnly] = useState(false);

  useEffect(() => {
    api
      .bulletins()
      .then((r) => {
        setBulletins(r.bulletins);
        setProgress(r.progress);
      })
      .catch((e: Error) => setError(e.message));
  }, []);

  useEffect(() => localStorage.setItem("labeler:queue-parish", parish), [parish]);

  const parishes = useMemo(() => {
    const seen = new Map<string, string>();
    for (const b of bulletins ?? []) seen.set(b.parish_slug, b.parish_name);
    return [...seen.entries()].sort((a, b) => a[1].localeCompare(b[1]));
  }, [bulletins]);

  const shown = (bulletins ?? []).filter(
    (b) =>
      (!parish || b.parish_slug === parish) &&
      (!status || b.status === status) &&
      (!latestOnly || b.rank === 0),
  );

  const openNext = async () => {
    try {
      const { bulletin } = await api.next(undefined, parish || undefined);
      if (bulletin) navigate(bulletinHref(bulletin.parish_slug, bulletin.content_hash));
      else setError(parish ? "Every bulletin of this parish is labeled." : "Every bulletin is labeled.");
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="mx-auto flex h-full max-w-6xl flex-col p-6">
      <header className="mb-4 flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-semibold">Bulletin labeler</h1>
        {config?.mode === "demo" && (
          <span className="rounded bg-amber-200 px-2 py-0.5 text-xs font-semibold text-amber-900" title="Generated demo data; labels go to data/labeler-demo/labels">
            DEMO DATA
          </span>
        )}
        {config && (
          <span className="text-xs text-slate-500" title={config.classifier_version}>
            Labels saved to <code>{config.labels_dir}</code>
            {config.mode === "live" && (config.remote ? " · R2 connected (read-only)" : " · local files only")}
          </span>
        )}
        <label className="ml-auto flex items-center gap-2 text-sm text-slate-600">
          Labeler
          <input
            value={labeler}
            onChange={(e) => onLabelerChange(e.target.value)}
            className="rounded border border-slate-300 bg-white px-2 py-1 text-sm"
            placeholder="Your name"
          />
        </label>
      </header>

      {progress && (
        <div className="mb-4 rounded-lg border border-slate-200 bg-white p-4">
          <div className="mb-2 flex flex-wrap items-baseline gap-x-4 gap-y-1">
            <span className="text-2xl font-semibold tabular-nums">
              {progress.latest_done} / {progress.latest_total} done
            </span>
            <span className="text-sm text-slate-500">each parish's latest bulletin</span>
            <span className="ml-auto text-sm text-slate-600 tabular-nums">
              {progress.done} done · {progress.in_progress} in progress · {progress.skipped} skipped · {progress.unlabeled} unlabeled
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded bg-slate-100">
            <div
              className="h-full bg-emerald-500"
              style={{ width: `${progress.latest_total ? (100 * progress.latest_done) / progress.latest_total : 0}%` }}
            />
          </div>
        </div>
      )}

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <select value={parish} onChange={(e) => setParish(e.target.value)} className="rounded border border-slate-300 bg-white px-2 py-1 text-sm" data-testid="parish-filter">
          <option value="">All parishes</option>
          {parishes.map(([slug, name]) => (
            <option key={slug} value={slug}>
              {name}
            </option>
          ))}
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value)} className="rounded border border-slate-300 bg-white px-2 py-1 text-sm">
          <option value="">Any status</option>
          {Object.entries(STATUS_LABEL).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
        <label className="flex items-center gap-1.5 text-sm text-slate-600">
          <input type="checkbox" checked={latestOnly} onChange={(e) => setLatestOnly(e.target.checked)} />
          Latest per parish only
        </label>
        <span className="text-sm text-slate-500">{shown.length} bulletins</span>
        <button className="btn-primary ml-auto" onClick={() => void openNext()} data-testid="next-unlabeled">
          Next unlabeled →
        </button>
      </div>

      {error && <div className="mb-3 rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">{error}</div>}
      {!bulletins && !error && <p className="text-slate-500">Loading…</p>}

      <div className="flex-1 overflow-y-auto rounded-lg border border-slate-200 bg-white">
        <table className="w-full text-sm">
          <thead className="sticky top-0 bg-slate-50 text-left text-xs tracking-wide text-slate-500 uppercase">
            <tr>
              <th className="px-3 py-2">Parish</th>
              <th className="px-3 py-2">Bulletin date</th>
              <th className="px-3 py-2">Fetched</th>
              <th className="px-3 py-2">Recency</th>
              <th className="px-3 py-2">Gemini</th>
              <th className="px-3 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((b) => (
              <tr
                key={`${b.parish_slug}/${b.content_hash}`}
                className="cursor-pointer border-t border-slate-100 hover:bg-sky-50"
                onClick={() => navigate(bulletinHref(b.parish_slug, b.content_hash))}
              >
                <td className="px-3 py-1.5">
                  <a href={bulletinHref(b.parish_slug, b.content_hash)} className="font-medium text-slate-800 hover:underline">
                    {b.parish_name}
                  </a>
                </td>
                <td className="px-3 py-1.5 tabular-nums">{b.published_date ?? "—"}</td>
                <td className="px-3 py-1.5 text-slate-500 tabular-nums">{b.fetched_at?.slice(0, 10) ?? "—"}</td>
                <td className="px-3 py-1.5 text-slate-500">{b.rank === 0 ? "latest" : `${b.rank} back`}</td>
                <td className="px-3 py-1.5 text-slate-500">{b.processed_at ? "processed" : "—"}</td>
                <td className="px-3 py-1.5">
                  <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${STATUS_STYLE[b.status]}`}>{STATUS_LABEL[b.status]}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
