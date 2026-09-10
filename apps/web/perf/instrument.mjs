// In-page measurement kit, injected before any app code runs.
//
// Everything that needs sub-frame accuracy lives here rather than in the driver:
// a Playwright round-trip costs a millisecond or two, which is the same order as
// the interactions we are trying to measure. The driver only asks the page to
// run a scripted burst and hands back the numbers.

/** Source of the init script. Kept as one self-contained function for addInitScript. */
export function instrumentationSource() {
  return `(${pageAgent.toString()})();`;
}

function pageAgent() {
  const state = {
    longTasks: [],
    paint: {},
    lcp: 0,
    /** Wall-clock (performance.now) of the last DOM mutation anywhere in <body>. */
    lastMutation: 0,
    mutationCount: 0,
  };

  const observe = (type, handler) => {
    try {
      new PerformanceObserver(handler).observe({ type, buffered: true });
    } catch {
      /* entry type unsupported in this browser build */
    }
  };

  observe("longtask", (list) => {
    for (const entry of list.getEntries()) {
      state.longTasks.push({ start: entry.startTime, duration: entry.duration });
    }
  });
  observe("paint", (list) => {
    for (const entry of list.getEntries()) state.paint[entry.name] = entry.startTime;
  });
  observe("largest-contentful-paint", (list) => {
    const entries = list.getEntries();
    if (entries.length > 0) state.lcp = entries[entries.length - 1].startTime;
  });

  const startMutationWatch = () => {
    const observer = new MutationObserver((records) => {
      state.mutationCount += records.length;
      state.lastMutation = performance.now();
    });
    observer.observe(document.documentElement, {
      subtree: true,
      childList: true,
      attributes: true,
      characterData: true,
    });
  };
  if (document.documentElement) startMutationWatch();
  else document.addEventListener("readystatechange", startMutationWatch, { once: true });

  /** Resolves just after the browser has painted the next frame. */
  const afterPaint = () =>
    new Promise((resolve) => {
      requestAnimationFrame(() => {
        // A message-channel task runs after the frame's paint has been
        // committed, so this timestamp includes style, layout and paint —
        // not just the React commit.
        const channel = new MessageChannel();
        channel.port1.onmessage = () => resolve(performance.now());
        channel.port2.postMessage(0);
      });
    });

  /**
   * Total blocking time contribution of a long task, per the web-vitals
   * definition — computed on the portion of the task inside the window, so a
   * task that merely overlaps the start of a measurement isn't charged in
   * full to it.
   */
  const blockingPortion = (durationInWindow) => Math.max(0, durationInWindow - 50);

  const bench = {
    now: () => performance.now(),

    /**
     * Long tasks / mutation counters observed since `since` (default: page
     * start). A task that started before `since` and ran past it is counted
     * only for its overlap: the tail of startup work routinely straddles the
     * boundary of an interaction scenario, and charging its whole duration to
     * the interaction inflated blocking and long-task totals.
     */
    tasksSince(since = 0) {
      const clipped = [];
      for (const task of state.longTasks) {
        const end = task.start + task.duration;
        if (end < since) continue;
        clipped.push(end - Math.max(task.start, since));
      }
      return {
        count: clipped.length,
        totalMs: clipped.reduce((sum, d) => sum + d, 0),
        blockingMs: clipped.reduce((sum, d) => sum + blockingPortion(d), 0),
        longestMs: clipped.reduce((max, d) => Math.max(max, d), 0),
      };
    },

    loadMetrics() {
      const nav = performance.getEntriesByType("navigation")[0];
      return {
        fcpMs: state.paint["first-contentful-paint"] ?? null,
        lcpMs: state.lcp || null,
        domContentLoadedMs: nav ? nav.domContentLoadedEventEnd : null,
        loadEventMs: nav ? nav.loadEventEnd : null,
        transferredKb: performance
          .getEntriesByType("resource")
          .reduce((sum, r) => sum + (r.transferSize || 0), 0) / 1024,
      };
    },

    /**
     * Dispatch one interaction and time it.
     * `sync` is the blocking work the event handler did before yielding;
     * `paint` is input → next painted frame, i.e. what the user feels.
     */
    async measure(action) {
      const start = performance.now();
      action();
      const afterHandler = performance.now();
      const painted = await afterPaint();
      return {
        syncMs: afterHandler - start,
        paintMs: painted - start,
      };
    },

    /**
     * Wait until the main thread and the DOM have been quiet for `quietMs`.
     * Returns how long the work actually took (0 when it was already idle),
     * which is the "did the deferred/transition work finish?" number that
     * paint latency alone can miss.
     */
    async settle(quietMs = 250, timeoutMs = 8000) {
      const start = performance.now();
      let lastActivity = start;
      while (performance.now() - start < timeoutMs) {
        await new Promise((resolve) => setTimeout(resolve, 50));
        const now = performance.now();
        const recentTask = state.longTasks[state.longTasks.length - 1];
        const taskEnd = recentTask ? recentTask.start + recentTask.duration : 0;
        lastActivity = Math.max(lastActivity, taskEnd, state.lastMutation);
        if (now - lastActivity >= quietMs) break;
      }
      return Math.max(0, lastActivity - start);
    },

    /** Set a React-controlled input's value the way a real user's keystroke would. */
    setInputValue(element, value, eventType = "input") {
      const prototype =
        element instanceof HTMLTextAreaElement
          ? HTMLTextAreaElement.prototype
          : HTMLInputElement.prototype;
      const setter = Object.getOwnPropertyDescriptor(prototype, "value").set;
      setter.call(element, String(value));
      element.dispatchEvent(new Event(eventType, { bubbles: true }));
    },

    /** Number of Leaflet markers currently in the DOM — the map's render fan-out. */
    markerCount: () => document.querySelectorAll(".leaflet-marker-icon").length,
  };

  Object.defineProperty(window, "__bench", { value: bench, writable: false });
}
