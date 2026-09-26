import type { EditorRow, Flags, Label, Status } from "../types";
import { fromLabelEvent, rowProblems, toLabelEvent } from "./rows";

/** The undoable part of a label. */
export interface Draft {
  status: Status;
  flags: Flags;
  published_date: string | null;
  note: string;
  rows: EditorRow[];
}

export const NO_FLAGS: Flags = {
  wrong_bulletin: false,
  unreadable: false,
  no_schedule: false,
  church_missing: false,
};

export function draftFromLabel(label: Label | null): Draft {
  return {
    status: label?.status ?? "in_progress",
    flags: { ...NO_FLAGS, ...label?.flags },
    published_date: label?.published_date ?? null,
    note: label?.note ?? "",
    rows: (label?.events ?? []).map(fromLabelEvent),
  };
}

/** Everything a save would write (row ids and editor links left out). */
export function draftKey(d: Draft): string {
  return JSON.stringify([d.status, d.flags, d.published_date, d.note, d.rows.map(toLabelEvent)]);
}

export function buildLabel(
  d: Draft,
  ctx: { parish: string; hash: string; sourceUrl: string; labeler: string; seconds: number },
): Label {
  return {
    schema_version: 1,
    parish_slug: ctx.parish,
    content_hash: ctx.hash,
    source_url: ctx.sourceUrl,
    status: d.status,
    flags: d.flags,
    published_date: d.published_date,
    note: d.note,
    labeler: ctx.labeler,
    seconds_spent: Math.max(0, Math.round(ctx.seconds)),
    updated_at: "",
    events: d.rows.map(toLabelEvent),
  };
}

/** Why the draft cannot be saved yet (a row missing a required field), or null. */
export function blockingMessage(rows: EditorRow[]): string | null {
  for (const [i, row] of rows.entries()) {
    const problems = rowProblems(row);
    if (problems.length) return `row ${i + 1} needs ${problems.join(", ")}`;
  }
  return null;
}
