import { memo } from "react";
import type { Church, EditorRow, EventType, WeekOfMonth } from "../types";
import { describeDays, formatDate, parseDates, parseDays, shortDay } from "../lib/dates";
import {
  ALL_BUT_LAST_NOTE,
  NUMBERED_WEEKS,
  WEEK_LABELS,
  allBut,
  allButWeek,
  describeSeason,
  describeWeeks,
  parseSeason,
  toggleWeek,
} from "../lib/pattern";
import { rowProblems, setDates, setDays } from "../lib/rows";
import { formatTime, parseLooseTime } from "../lib/time";
import { CommitInput } from "./CommitInput";

export type Field = "day" | "start" | "end" | "page" | "note" | "season";

type Patch = Partial<Omit<EditorRow, "id" | "origin" | "gemini_id">>;

interface Props {
  row: EditorRow;
  index: number;
  churches: Church[];
  selected: boolean;
  warnings: string[];
  refDate: string | null;
  focusField: Field | null;
  onFocusDone: () => void;
  onSelect: (id: string, scroll: boolean) => void;
  onPatch: (id: string, patch: Patch) => void;
  onTransform: (id: string, fn: (row: EditorRow) => EditorRow) => void;
  /** Focus left the row: a pending multi-day row becomes one row per day. */
  onLeave: (id: string) => void;
  onDelete: (id: string) => void;
  onDuplicate: (id: string) => void;
  /** Weekly row becomes that weekday of the bulletin's week. */
  onMakeDated: (id: string) => void;
}

const TYPES: { value: EventType; key: string; label: string }[] = [
  { value: "mass", key: "M", label: "Mass" },
  { value: "confession", key: "C", label: "Confession" },
  { value: "adoration", key: "A", label: "Adoration" },
];

const ORIGIN_STYLE = {
  human: { bar: "bg-slate-400", label: "Entered by hand" },
  gemini: { bar: "bg-violet-500", label: "Accepted from Gemini" },
  "gemini-edited": { bar: "bg-amber-500", label: "Accepted from Gemini, then edited" },
} as const;

function Seg<T extends string>({
  value,
  options,
  onChange,
}: {
  value: T;
  options: { value: T; key: string; label: string; title?: string }[];
  onChange: (v: T) => void;
}) {
  return (
    <div className="flex overflow-hidden rounded border border-slate-300">
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          tabIndex={-1}
          title={o.title ?? `${o.label} (${o.key.toLowerCase()})`}
          onClick={() => onChange(o.value)}
          className={`px-1 py-0.5 text-xs font-semibold ${
            value === o.value ? "bg-sky-600 text-white" : "bg-white text-slate-500 hover:bg-slate-100"
          }`}
        >
          {o.key}
        </button>
      ))}
    </div>
  );
}

function WeeksPicker({
  weeks,
  onChange,
  onAllButLast,
}: {
  weeks: WeekOfMonth[];
  onChange: (weeks: WeekOfMonth[]) => void;
  onAllButLast: () => void;
}) {
  const skipped = allButWeek(weeks);
  const chip = (active: boolean) =>
    `px-1.5 py-0.5 text-xs ${active ? "bg-sky-600 text-white" : "bg-white text-slate-600 hover:bg-slate-100"}`;
  return (
    <div className="flex items-center gap-1" title="Weeks of the month">
      <div className="flex overflow-hidden rounded border border-slate-300">
        <button type="button" tabIndex={-1} className={chip(weeks.length === 0)} onClick={() => onChange([])}>
          Every
        </button>
        {[...NUMBERED_WEEKS, "last" as const].map((w) => (
          <button
            key={w}
            type="button"
            tabIndex={-1}
            className={`${chip(!skipped && weeks.includes(w))} border-l border-slate-200`}
            onClick={() => onChange(toggleWeek(skipped ? [] : weeks, w))}
          >
            {WEEK_LABELS[w]}
          </button>
        ))}
      </div>
      <select
        tabIndex={-1}
        value={skipped ?? ""}
        onChange={(e) => {
          const w = e.target.value as WeekOfMonth | "";
          if (!w) return onChange([]);
          const list = allBut(w);
          if (list) onChange(list);
          else onAllButLast();
        }}
        className={`rounded border px-1 py-0.5 text-xs ${skipped ? "border-sky-600 bg-sky-50 text-sky-800" : "border-slate-300 bg-white text-slate-600"}`}
        title='"All but" one week. "All but last" cannot be stored as weeks; it goes in the note.'
      >
        <option value="">All but…</option>
        {[...NUMBERED_WEEKS, "last" as const].map((w) => (
          <option key={w} value={w}>
            All but {WEEK_LABELS[w]}
          </option>
        ))}
      </select>
    </div>
  );
}

export const RowEditor = memo(function RowEditor({
  row,
  index,
  churches,
  selected,
  warnings,
  refDate,
  focusField,
  onFocusDone,
  onSelect,
  onPatch,
  onTransform,
  onLeave,
  onDelete,
  onDuplicate,
  onMakeDated,
}: Props) {
  const missing = new Set(rowProblems(row));
  const weekly = row.event_kind === "weekly";
  const pendingCount = (weekly ? row.pending_split?.days : row.pending_split?.dates)?.length ?? 0;
  const summary = [
    weekly && row.weeks_of_month.length > 0 ? describeWeeks(row.weeks_of_month) : null,
    weekly && row.season ? describeSeason(row.season) : null,
    row.note,
  ]
    .filter(Boolean)
    .join(" · ");
  const patch = (p: Patch) => onPatch(row.id, p);
  const origin = ORIGIN_STYLE[row.origin];

  return (
    <div
      data-row-id={row.id}
      data-testid={`row-${index}`}
      tabIndex={-1}
      onMouseDown={(e) => {
        if (!(e.target as HTMLElement).closest("input,select,button")) {
          e.preventDefault();
          (e.currentTarget as HTMLElement).focus();
        }
        onSelect(row.id, true);
      }}
      onFocus={() => onSelect(row.id, false)}
      onBlur={(e) => {
        // Switching windows blurs too; only a move elsewhere in the page ends the row.
        if (!e.currentTarget.contains(e.relatedTarget as Node | null) && document.hasFocus()) onLeave(row.id);
      }}
      className={`relative rounded border py-1 pr-1.5 pl-3 outline-none ${
        selected ? "border-sky-500 bg-sky-50 ring-1 ring-sky-500" : "border-slate-200 bg-white hover:border-slate-300"
      }`}
    >
      <div className={`absolute top-0 bottom-0 left-0 w-1.5 rounded-l ${origin.bar}`} title={origin.label} />
      <div className="flex items-center gap-1 *:shrink-0">
        <span className="w-4 text-right text-xs text-slate-400 tabular-nums">{index + 1}</span>
        <select
          value={row.church_slug}
          onChange={(e) => patch({ church_slug: e.target.value })}
          className={`w-0 min-w-14 flex-1 rounded border px-0.5 py-0.5 text-sm ${missing.has("church") ? "border-amber-400 bg-amber-50" : "border-slate-300 bg-white"}`}
          title={churches.find((c) => c.slug === row.church_slug)?.name ?? "Church"}
        >
          <option value="">— church —</option>
          {churches.map((c) => (
            <option key={c.slug} value={c.slug}>
              {c.name}
            </option>
          ))}
          {row.church_slug && !churches.some((c) => c.slug === row.church_slug) && (
            <option value={row.church_slug}>{row.church_slug} (not in parish)</option>
          )}
        </select>
        <Seg value={row.event_type} options={TYPES} onChange={(v) => patch({ event_type: v })} />
        <Seg
          value={row.event_kind}
          options={[
            { value: "weekly", key: "W", label: "Weekly" },
            {
              value: "specific_date",
              key: "D",
              label: "Dated",
              title: "Dated (d): place a weekly row on that weekday of the bulletin's week",
            },
          ]}
          onChange={(v) => (v === "specific_date" ? onMakeDated(row.id) : patch({ event_kind: v }))}
        />
        {weekly ? (
          <CommitInput
            display={row.pending_split?.days ? describeDays(row.pending_split.days) : shortDay(row.day_of_week)}
            placeholder="Sun"
            title="Day; several days (Mon-Fri, Sat & Sun) make one row each once you leave the row"
            className="w-[5.5rem]"
            missing={missing.has("day")}
            autoFocus={focusField === "day"}
            onFocused={onFocusDone}
            testId="day-input"
            onCommit={(text) => {
              const days = text.trim() ? parseDays(text) : [];
              if (!days) return false;
              onTransform(row.id, (r) => setDays(r, days));
              return true;
            }}
          />
        ) : (
          <CommitInput
            display={row.pending_split?.dates ? row.pending_split.dates.map(formatDate).join("; ") : formatDate(row.date)}
            placeholder="10/5"
            title={`${row.date ? `${row.date}. ` : ""}Date: 10/5 or Oct 5; several dates (10/2; 10/9) make one row each once you leave the row`}
            className="w-[5.5rem]"
            missing={missing.has("date")}
            autoFocus={focusField === "day"}
            onFocused={onFocusDone}
            testId="date-input"
            onCommit={(text) => {
              const dates = text.trim() ? parseDates(text, refDate) : [];
              if (!dates) return false;
              onTransform(row.id, (r) => setDates(r, dates));
              return true;
            }}
          />
        )}
        {pendingCount > 1 && (
          <span
            className="rounded bg-sky-100 px-1 text-xs font-semibold text-sky-800"
            title={`Becomes ${pendingCount} rows, one per ${weekly ? "day" : "date"}, when you leave this row`}
            data-testid="pending-split"
          >
            ×{pendingCount}
          </span>
        )}
        <CommitInput
          display={formatTime(row.start_time)}
          placeholder="start"
          title="Start: 530p, 5:30, 17:30, noon"
          className="w-[4.5rem]"
          missing={missing.has("start time")}
          autoFocus={focusField === "start"}
          onFocused={onFocusDone}
          testId="start-input"
          onCommit={(text) => {
            const t = parseLooseTime(text);
            if (!t) return false;
            patch({ start_time: t });
            return true;
          }}
        />
        <span className="text-slate-400">–</span>
        <CommitInput
          display={formatTime(row.end_time)}
          placeholder="end"
          title="End (optional)"
          className="w-[4.5rem]"
          testId="end-input"
          onCommit={(text) => {
            if (!text.trim()) {
              patch({ end_time: null });
              return true;
            }
            const t = parseLooseTime(text);
            if (!t) return false;
            patch({ end_time: t });
            return true;
          }}
        />
        <button
          type="button"
          tabIndex={-1}
          onClick={() => patch({ cancelled: !row.cancelled })}
          title={row.cancelled ? "Cancelled; click or press x to undo" : "Mark cancelled (x)"}
          data-testid="cancelled-toggle"
          className={`rounded border px-1.5 py-0.5 text-xs font-semibold ${
            row.cancelled ? "border-red-600 bg-red-600 text-white" : "border-slate-300 bg-white text-slate-400 hover:bg-slate-100"
          }`}
        >
          X
        </button>
        <label className="flex items-center" title="PDF page">
          <CommitInput
            display={row.page_number ? String(row.page_number) : ""}
            placeholder="p."
            className="w-8 text-center"
            onCommit={(text) => {
              if (!text.trim()) {
                patch({ page_number: null });
                return true;
              }
              const n = Number(text);
              if (!Number.isInteger(n) || n < 1) return false;
              patch({ page_number: n });
              return true;
            }}
          />
        </label>
        <div className="flex items-center">
          {warnings.length > 0 && (
            <span className="cursor-help text-sm text-amber-600" title={warnings.join("\n")}>
              ⚠
            </span>
          )}
          <button type="button" tabIndex={-1} className="rounded px-1 text-slate-400 hover:bg-slate-200 hover:text-slate-700" title="Duplicate (Ctrl+D)" onClick={() => onDuplicate(row.id)}>
            ⧉
          </button>
          <button type="button" tabIndex={-1} className="rounded px-1 text-slate-400 hover:bg-red-100 hover:text-red-700" title="Delete (Delete)" onClick={() => onDelete(row.id)}>
            ✕
          </button>
        </div>
      </div>
      {!selected && summary && (
        <div className="truncate pl-5 text-xs text-slate-500" title={summary}>
          {summary}
        </div>
      )}
      {selected && (
        <div className="mt-1 flex flex-wrap items-center gap-1.5 pl-5">
          {weekly && (
            <>
              <WeeksPicker
                weeks={row.weeks_of_month}
                onChange={(w) => patch({ weeks_of_month: w })}
                onAllButLast={() =>
                  patch({
                    weeks_of_month: [],
                    note: row.note?.includes(ALL_BUT_LAST_NOTE)
                      ? row.note
                      : [row.note, ALL_BUT_LAST_NOTE].filter(Boolean).join("; "),
                  })
                }
              />
              <CommitInput
                display={row.season ? describeSeason(row.season) : ""}
                placeholder="All year (Sep-May)"
                title="Season: Sep-May, Jun 4 - Sep 10; empty for all year"
                className="w-32"
                missing={missing.has("season")}
                autoFocus={focusField === "season"}
                onFocused={onFocusDone}
                onCommit={(text) => {
                  const parsed = parseSeason(text);
                  if (!parsed) return false;
                  patch({ season: parsed.season });
                  return true;
                }}
              />
            </>
          )}
          <CommitInput
            display={row.note ?? ""}
            placeholder="note"
            className="min-w-24 flex-1"
            autoFocus={focusField === "note"}
            onFocused={onFocusDone}
            onCommit={(text) => {
              patch({ note: text.trim() ? text.trim() : null });
              return true;
            }}
          />
        </div>
      )}
    </div>
  );
});
