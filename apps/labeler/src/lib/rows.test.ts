import { describe, expect, it } from "vitest";
import type { EditorRow, GeminiRow } from "../types";
import { initHistory, pushHistory, redo, undo } from "./history";
import {
  blankRow,
  duplicateRow,
  editRow,
  fromGemini,
  handledGeminiIds,
  labelWarnings,
  rowProblems,
  sortRows,
  splitDates,
  splitDays,
  toLabelEvent,
} from "./rows";

const HF = "holy-family";
const SJ = "st-joseph";

function row(overrides: Partial<EditorRow> = {}): EditorRow {
  return {
    ...blankRow(undefined, { churches: [HF], viewedPage: 2 }),
    day_of_week: "Sunday",
    start_time: "10:30",
    ...overrides,
  };
}

function gemini(overrides: Partial<GeminiRow> = {}): GeminiRow {
  return {
    id: "g0",
    church_slug: HF,
    event_type: "mass",
    event_kind: "weekly",
    day_of_week: "Sunday",
    date: null,
    start_time: "10:30",
    end_time: null,
    cancelled: false,
    weeks_of_month: [],
    season: null,
    page_number: 2,
    note: null,
    raw: {},
    problems: [],
    ...overrides,
  };
}

describe("new rows", () => {
  it("pre-selects a parish's only church", () => {
    expect(blankRow(undefined, { churches: [HF], viewedPage: null }).church_slug).toBe(HF);
    expect(blankRow(undefined, { churches: [HF, SJ], viewedPage: null }).church_slug).toBe("");
  });

  it("keeps the previous row's church, type and kind, and takes the viewed page", () => {
    const prev = row({ church_slug: SJ, event_type: "confession", event_kind: "specific_date", page_number: 3 });
    const next = blankRow(prev, { churches: [HF, SJ], viewedPage: 4 });
    expect(next).toMatchObject({
      church_slug: SJ,
      event_type: "confession",
      event_kind: "specific_date",
      page_number: 4,
      start_time: "",
      origin: "human",
    });
    expect(blankRow(prev, { churches: [HF, SJ], viewedPage: null }).page_number).toBe(3);
  });
});

describe("splitting multi-day rows", () => {
  it("makes one row per day, the first keeping its identity", () => {
    const r = row({ day_of_week: null, start_time: "08:00" });
    const rows = splitDays(r, ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]);
    expect(rows.map((x) => x.day_of_week)).toEqual([
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
    ]);
    expect(rows[0].id).toBe(r.id);
    expect(new Set(rows.map((x) => x.id)).size).toBe(5);
    expect(rows.every((x) => x.start_time === "08:00" && x.church_slug === HF)).toBe(true);
  });

  it("marks split Gemini rows as edited", () => {
    const r = fromGemini(gemini({ day_of_week: "Monday" }));
    const rows = splitDays(r, ["Monday", "Tuesday"]);
    expect(rows.map((x) => x.origin)).toEqual(["gemini", "gemini-edited"]);
  });

  it("splits dates the same way", () => {
    const r = row({ event_kind: "specific_date", day_of_week: null });
    const rows = splitDates(r, ["2026-10-02", "2026-10-09"]);
    expect(rows.map((x) => [x.event_kind, x.date, x.day_of_week])).toEqual([
      ["specific_date", "2026-10-02", null],
      ["specific_date", "2026-10-09", null],
    ]);
  });
});

describe("origins", () => {
  it("records accepted Gemini rows as gemini, and edits as gemini-edited", () => {
    const accepted = fromGemini(gemini());
    expect(accepted.origin).toBe("gemini");
    expect(accepted.gemini_id).toBe("g0");
    expect(editRow(accepted, { start_time: "10:30" })).toBe(accepted);
    expect(editRow(accepted, { start_time: "11:00" }).origin).toBe("gemini-edited");
    expect(editRow(row(), { start_time: "11:00" }).origin).toBe("human");
  });

  it("duplicates as a new row derived from the original", () => {
    const accepted = fromGemini(gemini());
    const copy = duplicateRow(accepted);
    expect(copy.id).not.toBe(accepted.id);
    expect(copy.origin).toBe("gemini-edited");
    expect(copy.gemini_id).toBeUndefined();
    expect(duplicateRow(row()).origin).toBe("human");
  });

  it("clears what the other kind carries when switching kind", () => {
    const weekly = row({ weeks_of_month: ["first"], season: { start_month: 9, start_day: null, end_month: 5, end_day: null } });
    const dated = editRow(weekly, { event_kind: "specific_date", date: "2026-10-05" });
    expect(dated).toMatchObject({ day_of_week: null, weeks_of_month: [], season: null, date: "2026-10-05" });
    expect(editRow(dated, { event_kind: "weekly" }).date).toBeNull();
  });

  it("leaves unreadable Gemini fields empty to fill in", () => {
    const accepted = fromGemini(gemini({ start_time: null, problems: ["unreadable start time"] }));
    expect(rowProblems(accepted)).toEqual(["start time"]);
  });
});

describe("saving", () => {
  it("lists what stops a row from being saved", () => {
    expect(rowProblems(row())).toEqual([]);
    expect(rowProblems(row({ church_slug: "", day_of_week: null, start_time: "" }))).toEqual([
      "church",
      "day",
      "start time",
    ]);
    expect(rowProblems(row({ event_kind: "specific_date", day_of_week: null }))).toEqual(["date"]);
  });

  it("writes label events without editor-only fields", () => {
    const event = toLabelEvent({ ...fromGemini(gemini()), note: "  ", end_time: "" });
    expect(event).toEqual({
      church_slug: HF,
      event_type: "mass",
      event_kind: "weekly",
      day_of_week: "Sunday",
      date: null,
      start_time: "10:30",
      end_time: null,
      cancelled: false,
      weeks_of_month: [],
      season: null,
      page_number: 2,
      note: null,
      origin: "gemini",
    });
  });
});

describe("warnings", () => {
  const opts = { gemini: [], dismissed: new Set<string>(), bulletinDate: "2026-09-27", churches: [HF, SJ] };

  it("flags an end before the start", () => {
    const w = labelWarnings([row({ start_time: "15:00", end_time: "14:45" })], opts);
    expect(w[0].message).toMatch(/ends \(2:45 PM\) before it starts \(3:00 PM\)/);
  });

  it("flags dated events far from the bulletin date", () => {
    const near = row({ event_kind: "specific_date", day_of_week: null, date: "2026-10-30" });
    const far = row({ event_kind: "specific_date", day_of_week: null, date: "2026-11-15" });
    const w = labelWarnings([near, far], opts);
    expect(w).toHaveLength(1);
    expect(w[0]).toMatchObject({ rowId: far.id });
    expect(w[0].message).toMatch(/49 days after/);
  });

  it("flags duplicates", () => {
    const a = row();
    const w = labelWarnings([a, { ...a, id: "other" }], opts);
    expect(w).toEqual([{ rowId: "other", message: "Row 2 duplicates row 1" }]);
  });

  it("counts Gemini rows not yet accepted or dismissed", () => {
    const g = [gemini({ id: "g0" }), gemini({ id: "g1", start_time: "08:00" }), gemini({ id: "g2", start_time: "12:00" })];
    const rows = [row(), editRow(fromGemini(g[1]), { start_time: "08:15" })];
    expect([...handledGeminiIds(rows, g)].sort()).toEqual(["g0", "g1"]);
    const w = labelWarnings(rows, { ...opts, gemini: g });
    expect(w).toEqual([{ geminiId: "g2", message: "1 Gemini row not yet accepted or dismissed" }]);
    expect(labelWarnings(rows, { ...opts, gemini: g, dismissed: new Set(["g2"]) })).toEqual([]);
  });
});

describe("sorting and history", () => {
  it("sorts by church, type, kind, day and time", () => {
    const rows = [
      row({ church_slug: SJ, start_time: "09:00" }),
      row({ event_type: "confession", day_of_week: "Saturday", start_time: "15:00" }),
      row({ day_of_week: "Saturday", start_time: "16:00" }),
      row({ start_time: "08:00" }),
      row({ event_kind: "specific_date", day_of_week: null, date: "2026-10-05", start_time: "08:00" }),
    ];
    const sorted = sortRows(rows, [HF, SJ]);
    expect(sorted.map((r) => rows.indexOf(r))).toEqual([3, 2, 4, 1, 0]);
  });

  it("undoes and redoes", () => {
    let h = initHistory(1);
    h = pushHistory(h, 2);
    h = pushHistory(h, 3);
    h = undo(h);
    expect(h.present).toBe(2);
    h = redo(h);
    expect(h.present).toBe(3);
    h = undo(undo(h));
    h = pushHistory(h, 4);
    expect(h).toEqual({ past: [1], present: 4, future: [] });
    expect(undo(initHistory(1)).present).toBe(1);
  });
});
