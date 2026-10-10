import { describe, expect, it } from "vitest";
import type { SeedEntry, SeedFile, SeedSlot } from "../types";
import { parseRoute } from "./route";
import {
  approve,
  chooseOption,
  describeEntry,
  dropSlot,
  editSlot,
  fromEditorRow,
  openCount,
  reopenSlot,
  replaceSlot,
  resolveBulletin,
  slotGroups,
  toEditorRow,
} from "./seeds";

const entry = (overrides: Partial<SeedEntry> = {}): SeedEntry => ({
  church_slug: "st-mary",
  event_type: "confession",
  event_kind: "weekly",
  day_of_week: "Saturday",
  date: null,
  start_time: "15:00",
  end_time: "15:45",
  cancelled: false,
  weeks_of_month: [],
  season: null,
  note: null,
  ...overrides,
});

const question: SeedSlot = {
  id: "s2",
  decision: null,
  status: "needs_human",
  entry: null,
  page: 2,
  sources: [{ source: "agent", bulletin: "9f2c41d0", page: 2, said: "Sat 3:00-3:45" }],
  rationale: "Two bulletins disagree.",
  question: "Saturday confessions: 3:00 or 3:30?",
  options: [
    { label: "3:00-3:45", entry: entry(), leaning: true },
    { label: "3:30-3:50", entry: entry({ start_time: "15:30", end_time: "15:50" }) },
    { label: "Leave out", entry: null },
  ],
  answer: null,
};

const settled: SeedSlot = {
  ...question,
  id: "s1",
  status: "settled",
  decision: "include",
  entry: entry({ event_type: "mass", start_time: "16:00", end_time: null }),
  question: null,
  options: null,
};

const seed = (slots: SeedSlot[], status: SeedFile["status"] = "needs_review"): SeedFile => ({
  schema_version: 1,
  parish_slug: "st-mary",
  status,
  as_of: "2026-10-04T06:12:31Z",
  drafted_by: "test",
  drafted_at: null,
  reviewer: null,
  approved_at: null,
  summary: "",
  blocked_reason: null,
  bulletins: [
    { content_hash: `9f2c41d0${"0".repeat(56)}`, fetched_at: "2026-10-04T06:12:31Z", published_date: "2026-10-04", read: true },
    { content_hash: `1ab3e7c2${"0".repeat(56)}`, fetched_at: "2026-09-27T06:10:02Z", published_date: null, read: true },
  ],
  calls: [],
  slots,
});

describe("answering a question", () => {
  it("settles it with the chosen option's entry", () => {
    const answered = chooseOption(question, 1, "Ann")!;
    expect(answered).toMatchObject({ status: "settled", decision: "include", entry: { start_time: "15:30" } });
    expect(answered.answer).toMatchObject({ choice: 1, by: "Ann" });
  });

  it("leaves it out while keeping the entry the agent leaned to", () => {
    const answered = chooseOption(question, 2, "Ann")!;
    expect(answered).toMatchObject({ decision: "exclude", entry: { start_time: "15:00" }, answer: { choice: 2 } });
  });

  it("refuses an option that doesn't exist", () => {
    expect(chooseOption(question, 7, "Ann")).toBeNull();
  });
});

describe("other review actions", () => {
  it("drops, edits and reopens a slot", () => {
    expect(dropSlot(settled, "Ann")).toMatchObject({ decision: "exclude", answer: { choice: "dropped" } });
    const edited = editSlot(question, entry({ start_time: "14:30" }), 3, "Ann");
    expect(edited).toMatchObject({ status: "settled", decision: "include", page: 3, answer: { choice: "edited" } });
    const reopened = reopenSlot(settled);
    expect(reopened.status).toBe("needs_human");
    expect(reopened.options?.map((o) => [o.label, o.leaning])).toEqual([
      ["Keep as drafted", true],
      ["Leave out", false],
    ]);
    expect(reopenSlot(dropSlot(settled, "Ann")!).options?.[1].leaning).toBe(true);
  });

  it("keeps a question's own options when it is reopened after an answer", () => {
    const reopened = reopenSlot(chooseOption(question, 0, "Ann")!);
    expect(reopened.options).toBe(question.options);
    expect(reopened.answer).toBeNull();
  });
});

describe("the parish's status", () => {
  it("is needs_review while questions are open, then ready, then approved", () => {
    let file = seed([settled, question]);
    expect(openCount(file)).toBe(1);
    expect(approve(file, "Ann")).toBeNull();
    file = replaceSlot(file, chooseOption(question, 0, "Ann")!);
    expect(file.status).toBe("ready");
    expect(approve(file, " ")).toBeNull();
    const approved = approve(file, "Ann")!;
    expect(approved).toMatchObject({ status: "approved", reviewer: "Ann" });
    expect(replaceSlot(approved, dropSlot(settled, "Ann")!).status).toBe("ready");
  });

  it("groups slots as open, settled and left out", () => {
    const groups = slotGroups(seed([settled, question, dropSlot(settled, "Ann")!]));
    expect([groups.open.length, groups.settled.length, groups.excluded.length]).toEqual([1, 1, 1]);
  });
});

describe("helpers", () => {
  it("describes entries and resolves hash prefixes", () => {
    expect(describeEntry(entry({ weeks_of_month: ["first"], note: "Benediction" }))).toBe(
      "Confession · Saturday 3:00 PM–3:45 PM · 1st · Benediction",
    );
    expect(describeEntry(null)).toBe("Leave out");
    const file = seed([]);
    expect(resolveBulletin(file, "9f2c41d0")).toBe(file.bulletins[0].content_hash);
    expect(resolveBulletin(file, "9f2c")).toBeNull();
  });

  it("round-trips an entry through the row editor", () => {
    const dated = entry({ event_kind: "specific_date", day_of_week: null, date: "2026-10-10", cancelled: true });
    expect(fromEditorRow(toEditorRow(dated, 4))).toEqual({ entry: dated, page: 4 });
  });

  it("routes the seeds pages", () => {
    expect(parseRoute("#/seeds")).toEqual({ page: "seeds" });
    expect(parseRoute("#/s/st-mary")).toEqual({ page: "seed", parish: "st-mary" });
  });
});
