import { describe, expect, it } from "vitest";
import {
  continuousAccessLine,
  continuousRow,
  continuousTimes,
  currentContinuous,
} from "./continuous";
import type { ContinuousAdoration } from "./types";

function chapel(overrides: Partial<ContinuousAdoration> = {}): ContinuousAdoration {
  return {
    id: -1,
    church_id: 1,
    access: "not_stated",
    open_from: null,
    open_until: null,
    note: null,
    page_number: null,
    valid_from: null,
    valid_until: null,
    ...overrides,
  };
}

describe("continuous chapel wording", () => {
  it("says open 24 hours, and only the church page says the source is silent", () => {
    const c = chapel();
    expect(continuousTimes(c)).toBe("Open 24 hours");
    expect(continuousAccessLine(c, { compact: true })).toBeNull();
    expect(continuousAccessLine(c)).toBe("The bulletin gives no access details.");
    expect(continuousAccessLine(c, { source: "The parish website" })).toBe(
      "The parish website gives no access details.",
    );
  });

  it("gives a code-after-hours chapel's locked hours, or says after hours", () => {
    const c = chapel({ access: "code_after_hours", open_from: 360, open_until: 1260 });
    expect(continuousTimes(c)).toBe("Open 24 hours");
    expect(continuousAccessLine(c, { compact: true })).toBe(
      "Door code needed 9 p.m. – 6 a.m. Contact the parish office for details.",
    );
    expect(continuousAccessLine(c)).toBe(
      "Unlocked 6 a.m. – 9 p.m. Door code needed at other hours. " +
        "Contact the parish office for details.",
    );
    expect(
      continuousAccessLine(chapel({ access: "code_after_hours" }), { compact: true }),
    ).toBe("Door code needed after hours. Contact the parish office for details.");
  });

  it("words a code at every hour and access by arrangement", () => {
    expect(continuousTimes(chapel({ access: "code" }))).toBe("24 hours with code");
    expect(continuousTimes(chapel({ access: "arrangement" }))).toBe("By arrangement");
    expect(continuousAccessLine(chapel({ access: "arrangement" }))).toBe(
      "Contact the parish office for details.",
    );
  });

  it("is one Every day row in the popup's shape", () => {
    expect(continuousRow(chapel({ id: 5, access: "code" }), { compact: true })).toEqual({
      key: "continuous:5",
      label: "Every day",
      times: ["24 hours with code"],
      note: "Contact the parish office for details.",
    });
  });
});

describe("currentContinuous", () => {
  it("picks the record open today, so a closure hides the chapel", () => {
    const today = new Date(2026, 10, 17);
    const closed = chapel({ id: 1, valid_until: "2026-11-01" });
    const reopened = chapel({ id: 2, valid_from: "2026-12-01" });
    expect(currentContinuous([closed, reopened], today)).toBeNull();
    expect(currentContinuous([closed, reopened], new Date(2026, 11, 1))?.id).toBe(2);
    expect(currentContinuous([chapel({ id: 3 })], today)?.id).toBe(3);
  });
});
