import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { onLocalDayChange } from "./dayRollover";

// Just the slice of `document` the watcher uses; the unit tests run in Node.
class FakeDocument extends EventTarget {
  visibilityState: DocumentVisibilityState = "visible";
}

describe("onLocalDayChange", () => {
  let doc: FakeDocument;
  let stop: (() => void) | undefined;

  beforeEach(() => {
    vi.useFakeTimers();
    // Wednesday 2026-06-10, half an hour before midnight.
    vi.setSystemTime(new Date(2026, 5, 10, 23, 30));
    doc = new FakeDocument();
    vi.stubGlobal("document", doc);
  });

  afterEach(() => {
    stop?.();
    stop = undefined;
    vi.unstubAllGlobals();
    vi.useRealTimers();
  });

  it("fires at each local midnight while the page stays open", () => {
    const onChange = vi.fn();
    stop = onLocalDayChange(onChange);

    vi.advanceTimersByTime(29 * 60 * 1000);
    expect(onChange).not.toHaveBeenCalled();

    vi.advanceTimersByTime(60 * 1000);
    expect(onChange).toHaveBeenCalledTimes(1);

    vi.advanceTimersByTime(24 * 60 * 60 * 1000);
    expect(onChange).toHaveBeenCalledTimes(2);
  });

  it("re-arms rather than firing when its timer runs early", () => {
    const onChange = vi.fn();
    stop = onLocalDayChange(onChange);

    // The wall clock falls a second behind the timer's, so the midnight timer
    // fires at what is still 23:59:59.
    vi.setSystemTime(new Date(2026, 5, 10, 23, 29, 59));
    vi.advanceTimersByTime(30 * 60 * 1000);
    expect(onChange).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1000);
    expect(onChange).toHaveBeenCalledTimes(1);
  });

  it("catches up when a suspended tab becomes visible again", () => {
    const onChange = vi.fn();
    stop = onLocalDayChange(onChange);

    // Suspended overnight: the clock moves on but no timer gets to run.
    doc.visibilityState = "hidden";
    vi.setSystemTime(new Date(2026, 5, 11, 7, 0));
    doc.visibilityState = "visible";
    doc.dispatchEvent(new Event("visibilitychange"));
    expect(onChange).toHaveBeenCalledTimes(1);

    // Neither another resume the same day nor the old midnight timer fires it
    // again.
    doc.dispatchEvent(new Event("visibilitychange"));
    vi.advanceTimersByTime(60 * 60 * 1000);
    expect(onChange).toHaveBeenCalledTimes(1);
  });

  it("stops watching once disposed", () => {
    const onChange = vi.fn();
    onLocalDayChange(onChange)();

    vi.advanceTimersByTime(24 * 60 * 60 * 1000);
    doc.dispatchEvent(new Event("visibilitychange"));
    expect(onChange).not.toHaveBeenCalled();
  });
});
