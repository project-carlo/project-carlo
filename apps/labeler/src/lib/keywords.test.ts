import { describe, expect, it } from "vitest";
import { splitKeywords } from "./keywords";

describe("splitKeywords", () => {
  it("finds schedule words and cancellations", () => {
    const found = (text: string) =>
      splitKeywords(text)
        .filter((s) => s.keyword)
        .map((s) => [s.text, s.keyword]);
    expect(found("Saturday Vigil Mass 4:00 PM")).toEqual([["Mass", "schedule"]]);
    expect(found("Masses and Confessions")).toEqual([
      ["Masses", "schedule"],
      ["Confessions", "schedule"],
    ]);
    expect(found("Sacrament of Reconciliation; Holy Hour; ADORATION")).toEqual([
      ["Reconciliation", "schedule"],
      ["Holy Hour", "schedule"],
      ["ADORATION", "schedule"],
    ]);
    expect(found("Mass is cancelled; cancellations; canceled")).toEqual([
      ["Mass", "schedule"],
      ["cancelled", "cancel"],
      ["cancellations", "cancel"],
      ["canceled", "cancel"],
    ]);
  });

  it("leaves words that only contain a keyword alone", () => {
    expect(splitKeywords("Christmas in Massachusetts").every((s) => !s.keyword)).toBe(true);
  });

  it("keeps all the text", () => {
    const text = "The 8:00 AM Mass on Monday is cancelled.";
    expect(splitKeywords(text).map((s) => s.text).join("")).toBe(text);
  });
});
