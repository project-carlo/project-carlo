import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api, pdfUrl } from "../api";
import { CommitInput } from "../components/CommitInput";
import { GeminiPanel } from "../components/GeminiPanel";
import { HelpOverlay } from "../components/HelpOverlay";
import { PdfViewer, type ScrollRequest } from "../components/PdfViewer";
import { RowEditor, type Field } from "../components/RowEditor";
import { formatDate, parseLooseDate } from "../lib/dates";
import { buildLabel, draftFromLabel, draftKey, incompleteMessage, type Draft } from "../lib/draft";
import { initHistory, pushHistory, redo, undo, type History } from "../lib/history";
import { bulletinHref, navigate } from "../lib/route";
import {
  blankRow,
  duplicateRow,
  editRow,
  expandAllPending,
  expandPending,
  fromGemini,
  handledGeminiIds,
  labelWarnings,
  sortRows,
  type Warning,
} from "../lib/rows";
import { formatDuration } from "../lib/time";
import { useTimer } from "../lib/useTimer";
import { FLAG_NAMES, type BulletinDetail, type Config, type EditorRow, type FlagName, type Status } from "../types";

interface Props {
  parish: string;
  hash: string;
  config: Config | null;
  labeler: string;
  onLabelerChange: (name: string) => void;
}

export function BulletinPage(props: Props) {
  const { parish, hash } = props;
  const [detail, setDetail] = useState<BulletinDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setDetail(null);
    setError(null);
    api
      .detail(parish, hash)
      .then((d) => !cancelled && setDetail(d))
      .catch((e: Error) => !cancelled && setError(e.message));
    return () => {
      cancelled = true;
    };
  }, [parish, hash]);

  if (error) {
    return (
      <div className="p-8">
        <p className="mb-4 text-red-700">Could not open this bulletin: {error}</p>
        <a className="btn" href="#/">
          Back to the queue
        </a>
      </div>
    );
  }
  if (!detail) return <div className="p-8 text-slate-500">Loading bulletin…</div>;
  return <BulletinEditor key={`${parish}/${hash}`} detail={detail} {...props} />;
}

const FLAG_LABELS: Record<FlagName, string> = {
  wrong_bulletin: "Wrong bulletin",
  unreadable: "Unreadable",
  no_schedule: "No schedule",
  church_missing: "Church missing",
};

type SaveState = { state: "new" | "saved" | "pending" | "saving" } | { state: "error"; message: string };

interface GeminiMemory {
  dismissed: string[];
  accepted: string[];
}

function geminiMemoryKey(parish: string, hash: string, detail: BulletinDetail): string {
  const source = detail.gemini.source;
  return `labeler:gemini:${parish}/${hash}/${source.version_dir ?? source.kind}`;
}

function loadGeminiMemory(key: string): GeminiMemory {
  try {
    const parsed = JSON.parse(localStorage.getItem(key) ?? "null");
    if (parsed && Array.isArray(parsed.dismissed) && Array.isArray(parsed.accepted)) return parsed;
  } catch {
    // A corrupt entry is just forgotten.
  }
  return { dismissed: [], accepted: [] };
}

function isTyping(el: Element | null): boolean {
  return !!el?.matches('input:not([type="checkbox"]), textarea, select, [contenteditable="true"]');
}

function BulletinEditor({ detail, parish, hash, config, labeler, onLabelerChange }: Props & { detail: BulletinDetail }) {
  const churches = detail.churches;
  const churchSlugs = useMemo(() => churches.map((c) => c.slug), [churches]);
  const gemini = detail.gemini.events;

  const [history, setHistory] = useState<History<Draft>>(() => initHistory(draftFromLabel(detail.label)));
  const draft = history.present;
  const rows = draft.rows;
  const draftRef = useRef(draft);
  draftRef.current = draft;

  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [focus, setFocus] = useState<{ rowId: string; field: Field } | null>(null);
  const [viewedPage, setViewedPage] = useState<number | null>(null);
  const [scrollTo, setScrollTo] = useState<ScrollRequest | null>(null);
  const [showHelp, setShowHelp] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [save, setSave] = useState<SaveState>({ state: detail.label ? "saved" : "new" });
  const [seconds, secondsRef] = useTimer(detail.label?.seconds_spent ?? 0);

  const memoryKey = geminiMemoryKey(parish, hash, detail);
  const [memory, setMemory] = useState(() => loadGeminiMemory(memoryKey));
  const restoredAccepted = useMemo(() => new Set(loadGeminiMemory(memoryKey).accepted), [memoryKey]);
  const dismissed = useMemo(() => new Set(memory.dismissed), [memory.dismissed]);

  const lastSaved = useRef(draftKey(draft));
  const savedSeconds = useRef(detail.label?.seconds_spent ?? 0);
  const labelExists = useRef(detail.label !== null);
  const saveChain = useRef<Promise<unknown>>(Promise.resolve());
  const ctx = useRef({ parish, hash, sourceUrl: detail.bulletin.source_url, labeler });
  ctx.current = { parish, hash, sourceUrl: detail.bulletin.source_url, labeler };

  const refDate =
    draft.published_date ??
    detail.gemini.published_date ??
    detail.bulletin.published_date ??
    detail.bulletin.fetched_at?.slice(0, 10) ??
    null;

  // ── editing ──
  const update = useCallback((fn: (d: Draft) => Draft) => {
    setHistory((h) => pushHistory(h, fn(h.present)));
  }, []);
  const updateRows = useCallback(
    (fn: (rows: EditorRow[]) => EditorRow[]) => update((d) => ({ ...d, rows: fn(d.rows) })),
    [update],
  );

  const showPage = useCallback((page: number) => setScrollTo({ page, nonce: Date.now() }), []);

  const selectRow = useCallback(
    (id: string, scroll: boolean) => {
      setSelectedId(id);
      if (scroll) {
        const row = draftRef.current.rows.find((r) => r.id === id);
        if (row?.page_number) showPage(row.page_number);
      }
    },
    [showPage],
  );

  const patchRow = useCallback(
    (id: string, patch: Parameters<typeof editRow>[1]) =>
      updateRows((rs) => rs.map((r) => (r.id === id ? editRow(r, patch) : r))),
    [updateRows],
  );

  const transformRow = useCallback(
    (id: string, fn: (row: EditorRow) => EditorRow) => updateRows((rs) => rs.map((r) => (r.id === id ? fn(r) : r))),
    [updateRows],
  );

  const leaveRow = useCallback(
    (id: string) =>
      update((d) =>
        d.rows.some((r) => r.id === id && r.pending_split)
          ? { ...d, rows: d.rows.flatMap((r) => (r.id === id ? expandPending(r) : [r])) }
          : d,
      ),
    [update],
  );

  const deleteRow = useCallback(
    (id: string) => {
      const rs = draftRef.current.rows;
      const i = rs.findIndex((r) => r.id === id);
      if (i === -1) return;
      updateRows((all) => all.filter((r) => r.id !== id));
      const neighbour = rs[i + 1] ?? rs[i - 1];
      setSelectedId(neighbour?.id ?? null);
    },
    [updateRows],
  );

  const duplicate = useCallback(
    (id: string) => {
      const source = draftRef.current.rows.find((r) => r.id === id);
      if (!source) return;
      const copy = duplicateRow(source);
      updateRows((rs) => rs.flatMap((r) => (r.id === id ? [r, copy] : [r])));
      setSelectedId(copy.id);
    },
    [updateRows],
  );

  const addRow = useCallback(() => {
    const rs = draftRef.current.rows;
    const selectedIndex = rs.findIndex((r) => r.id === selectedId);
    const previous = selectedIndex >= 0 ? rs[selectedIndex] : rs[rs.length - 1];
    const row = blankRow(previous, { churches: churchSlugs, viewedPage });
    const at = selectedIndex >= 0 ? selectedIndex + 1 : rs.length;
    updateRows((all) => [...all.slice(0, at), row, ...all.slice(at)]);
    setSelectedId(row.id);
    setFocus({ rowId: row.id, field: "day" });
  }, [selectedId, churchSlugs, viewedPage, updateRows]);

  const accept = useCallback(
    (ids: string[]) => {
      const added = gemini.filter((g) => ids.includes(g.id)).map(fromGemini);
      if (!added.length) return;
      updateRows((rs) => [...rs, ...added]);
      if (added.length === 1) setSelectedId(added[0].id);
    },
    [gemini, updateRows],
  );

  const setDismissed = useCallback((id: string, on: boolean) => {
    setMemory((m) => ({
      ...m,
      dismissed: on ? [...new Set([...m.dismissed, id])] : m.dismissed.filter((x) => x !== id),
    }));
  }, []);

  useEffect(() => {
    const accepted = [...new Set([...restoredAccepted, ...rows.map((r) => r.gemini_id).filter((x): x is string => !!x)])];
    setMemory((m) => (m.accepted.length === accepted.length && m.accepted.every((a) => accepted.includes(a)) ? m : { ...m, accepted }));
  }, [rows, restoredAccepted]);

  useEffect(() => {
    localStorage.setItem(memoryKey, JSON.stringify(memory));
  }, [memory, memoryKey]);

  // ── saving ──
  const saveNow = useCallback(
    (d: Draft, opts: { keepalive?: boolean } = {}): Promise<boolean> => {
      const run = async () => {
        const key = draftKey(d);
        const secs = secondsRef.current;
        if (key === lastSaved.current && secs === savedSeconds.current && labelExists.current) return true;
        setSave({ state: "saving" });
        try {
          await api.save(buildLabel(d, { ...ctx.current, seconds: secs }), opts);
          lastSaved.current = key;
          savedSeconds.current = secs;
          labelExists.current = true;
          setSave(draftKey(draftRef.current) === key ? { state: "saved" } : { state: "pending" });
          return true;
        } catch (e) {
          setSave({ state: "error", message: (e as Error).message });
          return false;
        }
      };
      const p = saveChain.current.then(run);
      saveChain.current = p;
      return p;
    },
    [secondsRef],
  );

  useEffect(() => {
    if (draftKey(draft) === lastSaved.current) {
      setSave((s) => (s.state === "pending" ? { state: labelExists.current ? "saved" : "new" } : s));
      return;
    }
    setSave({ state: "pending" });
    const t = window.setTimeout(() => void saveNow(draftRef.current), 700);
    return () => window.clearTimeout(t);
  }, [draft, saveNow]);

  useEffect(() => {
    const id = window.setInterval(() => {
      if (labelExists.current && secondsRef.current !== savedSeconds.current && draftKey(draftRef.current) === lastSaved.current) {
        void saveNow(draftRef.current);
      }
    }, 30_000);
    return () => window.clearInterval(id);
  }, [saveNow, secondsRef]);

  useEffect(() => {
    const flush = () => {
      const d = draftRef.current;
      const dirty = draftKey(d) !== lastSaved.current;
      const timeOnly = labelExists.current && secondsRef.current !== savedSeconds.current;
      if (dirty || timeOnly) {
        void api.save(buildLabel(d, { ...ctx.current, seconds: secondsRef.current }), { keepalive: true }).catch(() => undefined);
        lastSaved.current = draftKey(d);
        savedSeconds.current = secondsRef.current;
      }
    };
    window.addEventListener("pagehide", flush);
    return () => {
      window.removeEventListener("pagehide", flush);
      flush();
    };
  }, [secondsRef]);

  const finish = useCallback(
    async (status: Extract<Status, "done" | "skipped">) => {
      (document.activeElement as HTMLElement | null)?.blur?.();
      await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 0)));
      const d = { ...draftRef.current, status, rows: expandAllPending(draftRef.current.rows) };
      const incomplete = incompleteMessage(d.rows);
      if (incomplete) {
        setMessage(`Can't mark this ${status}: ${incomplete}.`);
        return;
      }
      setHistory((h) => pushHistory(h, d));
      if (!(await saveNow(d))) return;
      try {
        const { bulletin } = await api.next({ parish, hash });
        if (bulletin) navigate(bulletinHref(bulletin.parish_slug, bulletin.content_hash));
        else navigate("#/");
      } catch (e) {
        setMessage(`Saved, but finding the next bulletin failed: ${(e as Error).message}`);
      }
    },
    [parish, hash, saveNow],
  );

  // ── keyboard ──
  const onKey = (e: KeyboardEvent) => {
    const target = e.target as HTMLElement;
    const typing = isTyping(target);
    const mod = e.ctrlKey || e.metaKey;
    const key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    if (mod && e.key === "Enter") {
      e.preventDefault();
      void finish("done");
      return;
    }
    if (mod && key === "d") {
      e.preventDefault();
      if (selectedId) duplicate(selectedId);
      return;
    }
    if (typing) return;
    if (mod && key === "z") {
      e.preventDefault();
      setHistory((h) => (e.shiftKey ? redo(h) : undo(h)));
      return;
    }
    if (mod && key === "y") {
      e.preventDefault();
      setHistory(redo);
      return;
    }
    if (mod || e.altKey || target.closest("[data-gemini-panel]")) return;
    if (e.key === "?") {
      setShowHelp((s) => !s);
      return;
    }
    if (e.key === "Escape") {
      setShowHelp(false);
      return;
    }
    if (key === "n") {
      e.preventDefault();
      addRow();
      return;
    }
    const index = rows.findIndex((r) => r.id === selectedId);
    const row = rows[index];
    if (!row) {
      if ((e.key === "ArrowDown" || key === "j") && rows.length) {
        e.preventDefault();
        selectRow(rows[0].id, true);
      }
      return;
    }
    const handled = () => e.preventDefault();
    switch (e.key === "Delete" || e.key === "Backspace" || e.key === "Enter" || e.key.startsWith("Arrow") ? e.key : key) {
      case "m":
        patchRow(row.id, { event_type: "mass" });
        return handled();
      case "c":
        patchRow(row.id, { event_type: "confession" });
        return handled();
      case "a":
        patchRow(row.id, { event_type: "adoration" });
        return handled();
      case "w":
        patchRow(row.id, { event_kind: "weekly" });
        return handled();
      case "d":
        patchRow(row.id, { event_kind: "specific_date" });
        return handled();
      case "x":
        patchRow(row.id, { cancelled: !row.cancelled });
        return handled();
      case "Delete":
      case "Backspace":
        deleteRow(row.id);
        return handled();
      case "ArrowDown":
      case "j":
        if (rows[index + 1]) selectRow(rows[index + 1].id, true);
        return handled();
      case "ArrowUp":
      case "k":
        if (rows[index - 1]) selectRow(rows[index - 1].id, true);
        return handled();
      case "Enter": {
        const missingDay = row.event_kind === "weekly" ? !row.day_of_week : !row.date;
        setFocus({ rowId: row.id, field: missingDay ? "day" : "start" });
        return handled();
      }
    }
  };
  const onKeyRef = useRef(onKey);
  onKeyRef.current = onKey;
  useEffect(() => {
    const listener = (e: KeyboardEvent) => onKeyRef.current(e);
    window.addEventListener("keydown", listener);
    return () => window.removeEventListener("keydown", listener);
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    const el = document.querySelector<HTMLElement>(`[data-row-id="${selectedId}"]`);
    el?.scrollIntoView({ block: "nearest" });
    if (el && !el.contains(document.activeElement) && !isTyping(document.activeElement) && !document.activeElement?.closest("[data-gemini-panel]")) {
      el.focus({ preventScroll: true });
    }
  }, [selectedId]);

  // ── derived ──
  const handled = useMemo(() => {
    const ids = handledGeminiIds(expandAllPending(rows), gemini);
    restoredAccepted.forEach((id) => ids.add(id));
    return ids;
  }, [rows, gemini, restoredAccepted]);

  const warnings: Warning[] = useMemo(() => {
    const list = labelWarnings(rows, {
      gemini,
      dismissed: new Set([...dismissed, ...restoredAccepted]),
      bulletinDate: refDate,
      churches: churchSlugs,
    });
    if (rows.length === 0 && !Object.values(draft.flags).some(Boolean) && (draft.status === "done" || gemini.length === 0)) {
      list.push({ message: "No events and no flag set (use No schedule if the bulletin lists none)" });
    }
    return list;
  }, [rows, gemini, dismissed, restoredAccepted, refDate, churchSlugs, draft.flags, draft.status]);

  const rowWarnings = useMemo(() => {
    const map = new Map<string, string[]>();
    for (const w of warnings) if (w.rowId) map.set(w.rowId, [...(map.get(w.rowId) ?? []), w.message]);
    return map;
  }, [warnings]);

  const incomplete = useMemo(() => incompleteMessage(rows), [rows]);
  const progress = detail.progress;
  const clearFocus = useCallback(() => setFocus(null), []);

  return (
    <div className="grid h-full grid-cols-[3fr_2fr]">
      <PdfViewer url={pdfUrl(parish, hash)} scrollTo={scrollTo} onPageChange={setViewedPage} />
      <div className="flex min-w-0 flex-col border-l border-slate-300 bg-slate-50">
        <header className="shrink-0 space-y-1.5 border-b border-slate-200 bg-white px-3 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <a href="#/" className="text-sm text-sky-700 hover:underline">
              ← Queue
            </a>
            <h1 className="truncate text-base font-semibold" title={parish}>
              <a href={detail.parish.homepage_url} target="_blank" rel="noreferrer" className="hover:underline">
                {detail.parish.name}
              </a>
            </h1>
            {config?.mode === "demo" && <span className="rounded bg-amber-200 px-1.5 text-xs font-semibold text-amber-900">DEMO</span>}
            <span className="ml-auto text-sm text-slate-600 tabular-nums" title={`${progress.done} done, ${progress.skipped} skipped, ${progress.in_progress} in progress across all ${progress.total} bulletins`}>
              <b>{progress.latest_done}</b> / {progress.latest_total} done
            </span>
            <span className="text-sm text-slate-500 tabular-nums" title="Time spent on this bulletin (paused while the tab is hidden)">
              ⏱ {formatDuration(seconds)}
            </span>
            <SaveBadge save={save} incomplete={incomplete} />
          </div>
          <ul className="space-y-0.5 text-xs text-slate-600">
            {churches.map((c) => (
              <li key={c.slug}>
                <b className="text-slate-800">{c.name}</b> · {c.address}
              </li>
            ))}
          </ul>
          <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
            <label className="flex items-center gap-1">
              <span className="text-slate-600">Bulletin date</span>
              <CommitInput
                display={draft.published_date ?? ""}
                placeholder="YYYY-MM-DD"
                className="w-28"
                testId="published-date"
                onCommit={(text) => {
                  if (!text.trim()) {
                    update((d) => ({ ...d, published_date: null }));
                    return true;
                  }
                  const date = parseLooseDate(text, detail.gemini.published_date ?? detail.bulletin.published_date);
                  if (!date) return false;
                  update((d) => ({ ...d, published_date: date }));
                  return true;
                }}
              />
            </label>
            <span className="text-xs text-slate-500">
              Gemini: {detail.gemini.published_date ? formatDate(detail.gemini.published_date) : "—"}
              {detail.gemini.published_date && detail.gemini.published_date !== draft.published_date && (
                <button
                  type="button"
                  className="ml-1 text-sky-700 underline"
                  onClick={() => update((d) => ({ ...d, published_date: detail.gemini.published_date }))}
                >
                  use
                </button>
              )}
            </span>
            <a className="truncate text-xs text-sky-700 underline" href={detail.bulletin.source_url} target="_blank" rel="noreferrer" title={detail.bulletin.source_url}>
              source
            </a>
          </div>
          <div className="flex flex-wrap items-center gap-1.5">
            {FLAG_NAMES.map((f) => (
              <button
                key={f}
                type="button"
                data-testid={`flag-${f}`}
                onClick={() => update((d) => ({ ...d, flags: { ...d.flags, [f]: !d.flags[f] } }))}
                className={`rounded-full border px-2 py-0.5 text-xs font-medium ${
                  draft.flags[f] ? "border-rose-600 bg-rose-600 text-white" : "border-slate-300 bg-white text-slate-600 hover:bg-slate-100"
                }`}
              >
                {FLAG_LABELS[f]}
              </button>
            ))}
            <span className="ml-auto flex items-center gap-1.5">
              <select
                value={draft.status}
                onChange={(e) => update((d) => ({ ...d, status: e.target.value as Status }))}
                className="rounded border border-slate-300 bg-white px-1 py-0.5 text-xs"
                title="Status"
              >
                <option value="in_progress">In progress</option>
                <option value="done">Done</option>
                <option value="skipped">Skipped</option>
              </select>
              <button className="btn py-0.5 text-xs" onClick={() => void finish("skipped")} title="Mark skipped and open the next bulletin">
                Skip
              </button>
              <button className="btn-primary py-0.5 text-xs" onClick={() => void finish("done")} title="Mark done and open the next bulletin (Ctrl+Enter)">
                Done &amp; next
              </button>
            </span>
          </div>
        </header>

        <div className="flex-1 space-y-3 overflow-y-auto p-3">
          {message && (
            <div className="flex items-start gap-2 rounded border border-amber-300 bg-amber-50 px-3 py-2 text-sm text-amber-900">
              <span className="flex-1">{message}</span>
              <button onClick={() => setMessage(null)} className="text-amber-700">
                ✕
              </button>
            </div>
          )}

          <GeminiPanel
            gemini={detail.gemini}
            churches={churches}
            handled={handled}
            dismissed={dismissed}
            onAccept={accept}
            onDismiss={setDismissed}
            onShowPage={showPage}
          />

          <section className="rounded-lg border border-slate-200 bg-white" data-testid="ground-truth">
            <header className="flex flex-wrap items-center gap-2 border-b border-slate-100 px-3 py-1.5">
              <h2 className="text-sm font-semibold">Ground truth ({rows.length})</h2>
              <span className="text-xs text-slate-500">
                <kbd>n</kbd> new row · <kbd>?</kbd> shortcuts
              </span>
              <span className="ml-auto flex items-center gap-1">
                <button className="btn py-0.5 text-xs" onClick={() => setHistory(undo)} disabled={!history.past.length} title="Undo (Ctrl+Z)">
                  Undo
                </button>
                <button className="btn py-0.5 text-xs" onClick={() => setHistory(redo)} disabled={!history.future.length} title="Redo (Ctrl+Shift+Z)">
                  Redo
                </button>
                <button className="btn py-0.5 text-xs" onClick={() => updateRows((rs) => sortRows(rs, churchSlugs))} disabled={rows.length < 2}>
                  Sort
                </button>
                <button className="btn py-0.5 text-xs" onClick={() => setShowHelp(true)}>
                  ?
                </button>
                <button className="btn-primary py-0.5 text-xs" onClick={addRow} data-testid="add-row">
                  + Row
                </button>
              </span>
            </header>
            <div className="space-y-1 p-2">
              {rows.length === 0 && (
                <p className="px-1 py-3 text-center text-sm text-slate-500">
                  Empty. Accept Gemini's rows above, or press <kbd>n</kbd> to add one.
                </p>
              )}
              {rows.map((row, i) => (
                <RowEditor
                  key={row.id}
                  row={row}
                  index={i}
                  churches={churches}
                  selected={row.id === selectedId}
                  warnings={rowWarnings.get(row.id) ?? []}
                  refDate={refDate}
                  focusField={focus?.rowId === row.id ? focus.field : null}
                  onFocusDone={clearFocus}
                  onSelect={selectRow}
                  onPatch={patchRow}
                  onTransform={transformRow}
                  onLeave={leaveRow}
                  onDelete={deleteRow}
                  onDuplicate={duplicate}
                />
              ))}
            </div>
          </section>

          {warnings.length > 0 && (
            <section className="rounded-lg border border-amber-200 bg-amber-50 px-3 py-2" data-testid="warnings">
              <h2 className="mb-1 text-xs font-semibold tracking-wide text-amber-900 uppercase">Warnings ({warnings.length})</h2>
              <ul className="space-y-0.5 text-sm text-amber-900">
                {warnings.map((w, i) => (
                  <li key={i}>
                    <button
                      type="button"
                      className="text-left hover:underline"
                      onClick={() => {
                        if (w.rowId) selectRow(w.rowId, true);
                        if (w.geminiId) document.querySelector<HTMLElement>(`[data-gemini-row="${w.geminiId}"]`)?.focus();
                      }}
                    >
                      ⚠ {w.message}
                    </button>
                  </li>
                ))}
              </ul>
            </section>
          )}

          <section className="space-y-1.5 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm">
            <label className="block">
              <span className="text-xs font-semibold tracking-wide text-slate-500 uppercase">Bulletin note</span>
              <textarea
                key={draft.note}
                defaultValue={draft.note}
                onBlur={(e) => e.target.value !== draft.note && update((d) => ({ ...d, note: e.target.value }))}
                rows={2}
                className="mt-0.5 w-full rounded border border-slate-300 px-2 py-1 text-sm"
                placeholder="Anything a later reader should know about this bulletin"
              />
            </label>
            <label className="flex items-center gap-2 text-xs text-slate-500">
              Labeler
              <input
                value={labeler}
                onChange={(e) => onLabelerChange(e.target.value)}
                className="rounded border border-slate-300 px-1.5 py-0.5 text-sm text-slate-800"
              />
            </label>
          </section>
        </div>
      </div>
      {showHelp && <HelpOverlay onClose={() => setShowHelp(false)} />}
    </div>
  );
}

function SaveBadge({ save, incomplete }: { save: SaveState; incomplete: string | null }) {
  const styles: Record<SaveState["state"], [string, string]> = {
    new: ["bg-slate-100 text-slate-500", "Not saved yet"],
    saved: ["bg-emerald-100 text-emerald-800", "Saved"],
    pending: ["bg-sky-100 text-sky-800", "Unsaved…"],
    saving: ["bg-sky-100 text-sky-800", "Saving…"],
    error: ["bg-red-100 text-red-800", "Save failed"],
  };
  const [cls, label] = styles[save.state];
  const title = "message" in save ? save.message : incomplete ? `Left out of the file until complete: ${incomplete}` : undefined;
  return (
    <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${incomplete && save.state !== "error" ? "bg-amber-100 text-amber-900" : cls}`} title={title} data-testid="save-state">
      {label}
      {incomplete && save.state !== "error" ? ` · ${incomplete}` : ""}
    </span>
  );
}
