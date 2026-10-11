/**
 * Reviewing a seed file: what each review action does to a slot, and the
 * parish's status after it. See docs/seeding-plan.md ("The seed file",
 * "Review in the labeler") and src/pdf_extract/seeding/files.py, which the
 * server validates every save against.
 */
import type { EditorRow, SeedAnswer, SeedEntry, SeedFile, SeedSlot, SeedStatus } from "../types";
import { formatDate } from "./dates";
import { describeSeason, describeWeeks } from "./pattern";
import { newId } from "./rows";
import { formatTime } from "./time";

function answer(choice: SeedAnswer["choice"], by: string): SeedAnswer {
  return { choice, by, at: new Date().toISOString().replace(/\.\d{3}Z$/, "Z") };
}

export function isOpen(slot: SeedSlot): boolean {
  return slot.status === "needs_human";
}

export function openCount(seed: SeedFile): number {
  return seed.slots.filter(isOpen).length;
}

/** The entry an excluded slot keeps for review: its own, or one its options name, or none. */
function keptEntry(slot: SeedSlot): SeedEntry | null {
  if (slot.entry) return slot.entry;
  const options = slot.options ?? [];
  return options.find((o) => o.leaning && o.entry)?.entry ?? options.find((o) => o.entry)?.entry ?? null;
}

/** Settle an open question with one of its options. Null when that can't be done. */
export function chooseOption(slot: SeedSlot, index: number, by: string): SeedSlot | null {
  const option = slot.options?.[index];
  if (!option) return null;
  if (option.entry) {
    return { ...slot, status: "settled", decision: "include", entry: option.entry, answer: answer(index, by) };
  }
  return { ...slot, status: "settled", decision: "exclude", entry: keptEntry(slot), answer: answer(index, by) };
}

/** Leave a slot out, whatever it was. */
export function dropSlot(slot: SeedSlot, by: string): SeedSlot {
  return { ...slot, status: "settled", decision: "exclude", entry: keptEntry(slot), answer: answer("dropped", by) };
}

/** Settle a slot as the reviewer edited it. */
export function editSlot(slot: SeedSlot, entry: SeedEntry, page: number | null, by: string): SeedSlot {
  return { ...slot, status: "settled", decision: "include", entry, page, answer: answer("edited", by) };
}

/**
 * Open a settled slot again as a question, its current decision as the leaning
 * answer. Null for a slot left out with no entry: there is nothing to include.
 */
export function reopenSlot(slot: SeedSlot): SeedSlot | null {
  if (isOpen(slot)) return slot;
  if (!slot.entry && !slot.options?.some((o) => o.leaning)) return null;
  const included = slot.decision === "include";
  const options =
    slot.options && slot.options.some((o) => o.leaning)
      ? slot.options
      : [
          { label: "Include", entry: slot.entry, leaning: included },
          { label: "Leave out", entry: null, leaning: !included },
        ];
  return {
    ...slot,
    status: "needs_human",
    question: slot.question ?? `Reopened by the reviewer: ${describeEntry(slot.entry)}`,
    options,
    answer: null,
  };
}

/**
 * The parish's status once a slot changed: needs_review while a question is
 * open, otherwise ready. Any change takes back an approval; blocked stays.
 */
export function statusAfterChange(seed: SeedFile): SeedStatus {
  if (seed.status === "blocked" || seed.status === "drafting") return seed.status;
  return openCount(seed) ? "needs_review" : "ready";
}

export function replaceSlot(seed: SeedFile, next: SeedSlot): SeedFile {
  const changed = { ...seed, slots: seed.slots.map((s) => (s.id === next.id ? next : s)) };
  return { ...changed, status: statusAfterChange(changed), approved_at: null };
}

export function approve(seed: SeedFile, reviewer: string): SeedFile | null {
  if (openCount(seed) || !reviewer.trim()) return null;
  return { ...seed, status: "approved", reviewer: reviewer.trim() };
}

/** Slots in the order the page lists them: open questions, settled, left out. */
export function slotGroups(seed: SeedFile): { open: SeedSlot[]; settled: SeedSlot[]; excluded: SeedSlot[] } {
  return {
    open: seed.slots.filter(isOpen),
    settled: seed.slots.filter((s) => !isOpen(s) && s.decision === "include"),
    excluded: seed.slots.filter((s) => !isOpen(s) && s.decision !== "include"),
  };
}

/** "Mass · Sun 9:00 AM · first, third · Sep–May · note" */
export function describeEntry(entry: SeedEntry | null): string {
  if (!entry) return "Leave out";
  const when = entry.event_kind === "weekly" ? (entry.day_of_week ?? "?") : formatDate(entry.date);
  const end = entry.end_time ? `–${formatTime(entry.end_time)}` : "";
  const parts = [
    `${entry.event_type[0].toUpperCase()}${entry.event_type.slice(1)}`,
    `${when} ${formatTime(entry.start_time)}${end}`,
  ];
  if (entry.cancelled) parts.push("cancelled");
  if (entry.weeks_of_month.length) parts.push(describeWeeks(entry.weeks_of_month));
  if (entry.season) parts.push(describeSeason(entry.season));
  if (entry.note) parts.push(entry.note);
  return parts.join(" · ");
}

/**
 * The newest bulletin the agent read: the one `as_of` names and a slot's page
 * refers to (as `newest_read_bulletin` on the server; times compared parsed).
 */
export function newestReadBulletin(seed: SeedFile): SeedFile["bulletins"][number] | null {
  let newest: SeedFile["bulletins"][number] | null = null;
  for (const b of seed.bulletins) {
    if (!b.read) continue;
    if (!newest || Date.parse(b.fetched_at) > Date.parse(newest.fetched_at)) newest = b;
  }
  return newest;
}

/** The full content hash a source or call's `bulletin` names (a hash or a prefix of one). */
export function resolveBulletin(seed: SeedFile, ref: string | null | undefined): string | null {
  if (!ref || ref.length < 8) return null;
  const prefix = ref.replace(/…$/, "").toLowerCase();
  const matches = seed.bulletins.filter((b) => b.content_hash.startsWith(prefix));
  return matches.length === 1 ? matches[0].content_hash : null;
}

/** A slot's entry as an editor row, so RowEditor can edit it. */
export function toEditorRow(entry: SeedEntry, page: number | null): EditorRow {
  return { ...entry, id: newId(), page_number: page, origin: "human", optional: null };
}

export function fromEditorRow(row: EditorRow): { entry: SeedEntry; page: number | null } {
  const weekly = row.event_kind === "weekly";
  return {
    entry: {
      church_slug: row.church_slug,
      event_type: row.event_type,
      event_kind: row.event_kind,
      day_of_week: weekly ? row.day_of_week : null,
      date: weekly ? null : row.date,
      start_time: row.start_time,
      end_time: row.end_time || null,
      cancelled: weekly ? false : row.cancelled,
      weeks_of_month: weekly ? row.weeks_of_month : [],
      season: weekly ? row.season : null,
      note: row.note?.trim() ? row.note.trim() : null,
    },
    page: row.page_number,
  };
}
