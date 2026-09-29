import { useState, type KeyboardEvent } from "react";
import type { BulletinDetail, Church, EventType, GeminiRow } from "../types";
import { dateForWeekday, formatDate, shortDay } from "../lib/dates";
import { describeSeason, describeWeeks } from "../lib/pattern";
import { weekdayOf } from "../lib/rows";
import { formatTime } from "../lib/time";

interface Props {
  gemini: BulletinDetail["gemini"];
  churches: Church[];
  handled: Set<string>;
  dismissed: Set<string>;
  onAccept: (ids: string[], select?: boolean) => void;
  /** Accept a weekly row as that weekday of the bulletin's week. False when it could not be placed. */
  onAcceptDated: (id: string) => boolean;
  /** Accept as weekly on that weekday, first week of the month, with the note cleared. */
  onAcceptFirst: (id: string) => boolean;
  onDismiss: (id: string, dismissed: boolean) => void;
  onEdit: (id: string) => void;
  onShowPage: (page: number) => void;
  bulletinDate: string | null;
}

const TYPE_LABEL: Record<EventType, string> = {
  mass: "Masses",
  confession: "Confessions",
  adoration: "Adoration",
};

function SourceLine({ source }: { source: BulletinDetail["gemini"]["source"] }) {
  if (source.kind === "cache") {
    return (
      <span>
        Cached result · <b>{source.model ?? "unknown model"}</b> · prompt{" "}
        <code className="text-xs">{source.prompt_version ?? "?"}</code>
        {source.is_current_version ? (
          <span className="ml-1 rounded bg-emerald-100 px-1 text-xs text-emerald-800">current version</span>
        ) : (
          <span className="ml-1 rounded bg-amber-100 px-1 text-xs text-amber-800">older version</span>
        )}
        {source.church_list_matches === false && (
          <span className="ml-1 rounded bg-amber-100 px-1 text-xs text-amber-800" title="Extracted against an older church list">
            older church list
          </span>
        )}
      </span>
    );
  }
  if (source.kind === "post-processing") {
    return (
      <span title="No cached result for this PDF: these are the bulletin's rows in the event table, after storage and weekly promotion. The model and prompt are not recorded there.">
        <span className="rounded bg-orange-100 px-1 text-xs font-semibold text-orange-800">post-processing</span>{" "}
        event table rows · model and prompt not recorded
      </span>
    );
  }
  return <span>No Gemini output for this bulletin</span>;
}

function describe(g: GeminiRow): string {
  const when =
    g.event_kind === "weekly"
      ? (g.day_of_week ?? g.raw.day_of_week ?? "?")
      : g.date
        ? formatDate(g.date)
        : (g.raw.date ?? "?");
  const start = g.start_time ? formatTime(g.start_time) : (g.raw.start_time ?? "?");
  const end = g.end_time ? `–${formatTime(g.end_time)}` : g.raw.end_time ? `–${g.raw.end_time}` : "";
  return `${when} ${start}${end}`;
}

export function GeminiPanel({
  gemini,
  churches,
  handled,
  dismissed,
  onAccept,
  onAcceptDated,
  onAcceptFirst,
  onDismiss,
  onEdit,
  onShowPage,
  bulletinDate,
}: Props) {
  const [open, setOpen] = useState(true);
  const rows = gemini.events;
  const pending = rows.filter((g) => !handled.has(g.id) && !dismissed.has(g.id));
  const known = new Set(churches.map((c) => c.slug));
  const groups: { church: string; name: string; type: EventType | null; rows: GeminiRow[] }[] = [];
  const churchOrder = [...churches.map((c) => c.slug), ...new Set(rows.map((r) => r.church_slug).filter((s) => !known.has(s)))];
  for (const slug of churchOrder) {
    for (const type of ["mass", "confession", "adoration", null] as const) {
      const members = rows.filter((r) => r.church_slug === slug && r.event_type === type);
      if (members.length) {
        groups.push({
          church: slug,
          name: churches.find((c) => c.slug === slug)?.name ?? slug,
          type,
          rows: members,
        });
      }
    }
  }

  const onRowKey = (e: KeyboardEvent<HTMLDivElement>, g: GeminiRow) => {
    // Ctrl+Enter and the other page shortcuts pass through.
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const key = e.key.length === 1 ? e.key.toLowerCase() : e.key;
    const items = () => [...document.querySelectorAll<HTMLElement>("[data-gemini-row]")];
    // Accepting re-renders the list and can drop focus, so land again after paint.
    const land = (el: HTMLElement | undefined) => {
      if (!el) return;
      const page = Number(el.dataset.page);
      if (page) onShowPage(page);
      const id = el.dataset.geminiRow ?? "";
      const focusIt = () => document.querySelector<HTMLElement>(`[data-gemini-row="${CSS.escape(id)}"]`)?.focus();
      focusIt();
      requestAnimationFrame(focusIt);
    };
    const neighbor = (delta: number) => {
      const rows = items();
      return rows[rows.indexOf(e.currentTarget) + delta];
    };
    // The next row still waiting for a decision, skipping ones already accepted or dismissed.
    const nextCandidate = () => {
      const rows = items();
      const start = rows.indexOf(e.currentTarget);
      return rows.slice(start + 1).find((el) => el.dataset.pending === "true");
    };
    if (key === "e") {
      e.preventDefault();
      e.stopPropagation();
      onEdit(g.id);
      return;
    }
    if (key === "d") {
      e.preventDefault();
      e.stopPropagation();
      if (onAcceptDated(g.id)) land(nextCandidate() ?? e.currentTarget);
      return;
    }
    if (key === "f") {
      e.preventDefault();
      e.stopPropagation();
      if (onAcceptFirst(g.id)) land(nextCandidate() ?? e.currentTarget);
      return;
    }
    if (e.key === "Enter" || e.key === " " || key === "y") {
      e.preventDefault();
      e.stopPropagation();
      if (!handled.has(g.id)) onAccept([g.id], false);
      land(nextCandidate() ?? e.currentTarget);
    } else if (e.key === "Delete" || e.key === "Backspace" || key === "n") {
      e.preventDefault();
      e.stopPropagation();
      onDismiss(g.id, !dismissed.has(g.id));
      land(neighbor(1) ?? e.currentTarget);
    } else if (e.key === "ArrowDown" || key === "j") {
      e.preventDefault();
      land(neighbor(1));
    } else if (e.key === "ArrowUp" || key === "k") {
      e.preventDefault();
      land(neighbor(-1));
    }
  };

  return (
    <section className="rounded-lg border border-violet-200 bg-white" data-gemini-panel>
      <header className="flex flex-wrap items-center gap-2 border-b border-violet-100 bg-violet-50 px-3 py-1.5">
        <button type="button" className="text-sm font-semibold text-violet-900" onClick={() => setOpen(!open)}>
          {open ? "▾" : "▸"} Gemini ({rows.length})
        </button>
        <span className="text-xs text-slate-600">
          <SourceLine source={gemini.source} />
        </span>
        <span className="ml-auto text-xs text-slate-500">
          {pending.length} to review
        </span>
        <button
          type="button"
          className="btn py-0.5 text-xs"
          disabled={pending.length === 0}
          onClick={() => onAccept(pending.map((g) => g.id))}
          title="Accept every Gemini row not yet accepted or dismissed"
        >
          Accept all
        </button>
      </header>
      {open && (
        <div className="max-h-[34vh] space-y-2 overflow-y-auto p-2">
          {(gemini.wrong_bulletin || gemini.church_list_needs_review) && (
            <div className="rounded bg-amber-50 px-2 py-1 text-xs text-amber-900">
              {gemini.wrong_bulletin && "Gemini flagged this as the wrong bulletin. "}
              {gemini.church_list_needs_review && "Gemini thinks the church list needs review."}
            </div>
          )}
          {rows.length === 0 && <p className="px-1 text-sm text-slate-500">Nothing to show.</p>}
          {groups.map((group) => (
            <div key={`${group.church}-${group.type}`}>
              <div className="px-1 text-xs font-semibold tracking-wide text-slate-500 uppercase">
                {group.name} · {group.type ? TYPE_LABEL[group.type] : "Unknown type"}
                {!known.has(group.church) && <span className="ml-1 text-red-600 normal-case">(church not in parish)</span>}
              </div>
              {group.rows.map((g) => {
                const isHandled = handled.has(g.id);
                const isDismissed = dismissed.has(g.id);
                const weekDate =
                  g.event_kind === "weekly" && g.day_of_week && bulletinDate
                    ? dateForWeekday(bulletinDate, g.day_of_week)
                    : null;
                const firstDay = weekdayOf(g);
                const alreadyFirst =
                  g.event_kind === "weekly" &&
                  g.weeks_of_month.length === 1 &&
                  g.weeks_of_month[0] === "first" &&
                  !g.note?.trim();
                return (
                  <div
                    key={g.id}
                    data-gemini-row={g.id}
                    data-page={g.page_number ?? undefined}
                    data-pending={!isHandled && !isDismissed ? "true" : undefined}
                    tabIndex={0}
                    onKeyDown={(e) => onRowKey(e, g)}
                    onClick={() => g.page_number && onShowPage(g.page_number)}
                    className={`group flex items-center gap-2 rounded px-1.5 py-0.5 text-sm outline-none focus:bg-violet-100 focus:ring-1 focus:ring-violet-400 ${
                      isDismissed ? "text-slate-400 line-through" : isHandled ? "text-slate-500" : "text-slate-900"
                    }`}
                  >
                    <span className="w-4 text-center" title={isHandled ? "Accepted or matched" : isDismissed ? "Dismissed" : "Not reviewed"}>
                      {isHandled ? <span className="text-emerald-600">✓</span> : isDismissed ? "–" : <span className="text-violet-500">•</span>}
                    </span>
                    <span className="tabular-nums">{describe(g)}</span>
                    {g.cancelled && <span className="rounded bg-red-100 px-1 text-xs text-red-700 no-underline">cancelled</span>}
                    {g.weeks_of_month.length > 0 && <span className="text-xs text-sky-700">{describeWeeks(g.weeks_of_month)}</span>}
                    {g.season && <span className="text-xs text-sky-700">{describeSeason(g.season)}</span>}
                    {g.note && <span className="truncate text-xs text-slate-500 italic">{g.note}</span>}
                    {g.problems.length > 0 && (
                      <span className="cursor-help text-xs text-red-600" title={g.problems.join("\n")}>
                        ⚠ {g.problems.length}
                      </span>
                    )}
                    <span className="ml-auto flex shrink-0 items-center gap-1">
                      {g.page_number && <span className="text-xs text-slate-400">p.{g.page_number}</span>}
                      {firstDay && !alreadyFirst && !isHandled && !isDismissed && (
                        <button
                          type="button"
                          tabIndex={-1}
                          className="rounded border border-sky-300 bg-white px-1.5 text-xs font-semibold text-sky-800 hover:bg-sky-50"
                          title={`Accept as the first ${firstDay} of the month and clear the note (f)`}
                          onClick={(e) => {
                            e.stopPropagation();
                            onAcceptFirst(g.id);
                          }}
                        >
                          1st {shortDay(firstDay)}
                        </button>
                      )}
                      {weekDate && !isHandled && !isDismissed && (
                        <button
                          type="button"
                          tabIndex={-1}
                          className="rounded border border-violet-300 bg-white px-1.5 text-xs font-semibold text-violet-800 hover:bg-violet-50"
                          title={`Accept as ${formatDate(weekDate)} instead of every ${g.day_of_week} (d)`}
                          onClick={(e) => {
                            e.stopPropagation();
                            onAcceptDated(g.id);
                          }}
                        >
                          {formatDate(weekDate)}
                        </button>
                      )}
                      {!isHandled && (
                        <button
                          type="button"
                          tabIndex={-1}
                          className="rounded bg-violet-600 px-1.5 text-xs font-semibold text-white hover:bg-violet-700"
                          title={[
                            "Accept into the ground truth (Enter).",
                            weekDate ? `d accepts it as ${formatDate(weekDate)}.` : "e edits this row.",
                            firstDay && !alreadyFirst ? `f accepts it as the first ${firstDay} of the month.` : "",
                          ]
                            .filter(Boolean)
                            .join(" ")}
                          onClick={(e) => {
                            e.stopPropagation();
                            onAccept([g.id]);
                          }}
                        >
                          Accept
                        </button>
                      )}
                      {!isHandled && (
                        <button
                          type="button"
                          tabIndex={-1}
                          className="rounded px-1 text-xs text-slate-400 hover:bg-slate-200 hover:text-slate-700"
                          title={isDismissed ? "Restore" : "Dismiss: Gemini is wrong here (Delete)"}
                          onClick={(e) => {
                            e.stopPropagation();
                            onDismiss(g.id, !isDismissed);
                          }}
                        >
                          {isDismissed ? "Restore" : "Dismiss"}
                        </button>
                      )}
                    </span>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
