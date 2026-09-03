/** Wires the API, session state, rendering and keyboard into one screen. */

import { api } from "./api.js";
import { bindKeys } from "./keys.js";
import {
  addManualEvent,
  adoptTask,
  buildLabel,
  pickVariant,
  removeManualEvent,
  setConflictAll,
  setVerdict,
  state,
  undecidedIds,
} from "./state.js";
import {
  bindActions,
  renderAll,
  renderCards,
  renderFinishHint,
  renderPdf,
  renderProgress,
  renderQueue,
} from "./render.js";

const AUTOSAVE_DELAY_MS = 900;
let autosaveTimer = null;

// ── notifications ─────────────────────────────────────────────────────────
let toastTimer = null;
function toast(message, isError = false) {
  const node = document.getElementById("toast");
  node.textContent = message;
  node.classList.toggle("toast--error", isError);
  node.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    node.hidden = true;
  }, isError ? 6000 : 2200);
}

async function guard(work, failureMessage) {
  try {
    return await work();
  } catch (error) {
    toast(`${failureMessage}: ${error.message}`, true);
    return null;
  }
}

// ── saving ────────────────────────────────────────────────────────────────
/** Persist without finishing, so a browser crash never costs a session. */
function scheduleAutosave() {
  clearTimeout(autosaveTimer);
  autosaveTimer = setTimeout(() => {
    if (state.dirty) save(currentStatus(), { quiet: true });
  }, AUTOSAVE_DELAY_MS);
}

function currentStatus() {
  if (state.label?.status === "complete" && !undecidedIds().length) return "complete";
  return "in_progress";
}

async function save(status, { quiet = false } = {}) {
  if (!state.task) return null;
  clearTimeout(autosaveTimer);
  const response = await guard(
    () => api.saveLabel(buildLabel(status)),
    "Could not save",
  );
  if (!response) return null;
  state.label = response.label;
  state.dirty = false;
  renderProgress(response.progress);
  await refreshQueue();
  if (!quiet) toast(status === "complete" ? "Saved as ground truth" : "Progress saved");
  return response;
}

// ── loading ───────────────────────────────────────────────────────────────
async function refreshQueue() {
  const response = await guard(() => api.queue(state.params), "Could not load the queue");
  if (!response) return;
  state.queue = response.items;
  renderProgress(response.progress);
  renderQueue();
}

async function openTask(url) {
  if (state.dirty) await save(currentStatus(), { quiet: true });
  const response = await guard(() => api.task(url, state.params), "Could not load bulletin");
  if (!response) return;
  if (!response.task) {
    state.task = null;
    renderAll();
    toast("Nothing left in this queue");
    return;
  }
  adoptTask(response);
  state.task.parish_name = response.parish_name;
  state.task.parish_churches = response.parish_churches;
  focusFirstUndecided();
  renderProgress(response.progress);
  renderAll();
}

/** Land on the first thing that still needs a decision, not the top of the list. */
function focusFirstUndecided() {
  state.focus = 0;
  state.page = 1;
}

// ── focus & paging ────────────────────────────────────────────────────────
function moveFocus(delta) {
  if (!state.cards.length) return;
  state.focus = Math.min(Math.max(state.focus + delta, 0), state.cards.length - 1);
  const page = state.cards[state.focus]?.page;
  if (page && page !== state.page) {
    state.page = page;
    renderPdf();
  }
  renderCards();
}

function setPage(page) {
  const next = Math.max(1, page);
  if (next === state.page) return;
  state.page = next;
  renderPdf();
}

function focusedCard() {
  return state.cards[state.focus] || null;
}

/** After a verdict: repaint, autosave, and move on to the next open decision. */
function afterVerdict({ advance = true } = {}) {
  renderCards();
  renderFinishHint();
  scheduleAutosave();
  if (advance) advanceToNextUndecided();
}

function advanceToNextUndecided() {
  const pending = new Set(undecidedIds());
  for (let index = state.focus + 1; index < state.cards.length; index += 1) {
    const card = state.cards[index];
    const ids =
      card.kind === "conflict"
        ? card.conflict.variants.map((variant) => variant.key_id)
        : card.candidate
          ? [card.candidate.key_id]
          : [];
    if (ids.some((id) => pending.has(id))) {
      state.focus = index;
      const page = card.page;
      if (page && page !== state.page) {
        state.page = page;
        renderPdf();
      }
      renderCards();
      return;
    }
  }
  renderCards();
}

// ── actions used by the rendered controls ─────────────────────────────────
bindActions({
  pick(conflict, keyId) {
    pickVariant(conflict, keyId);
    afterVerdict();
  },
  setAll(conflict, verdict) {
    setConflictAll(conflict, verdict);
    afterVerdict();
  },
  toggle(keyId, verdict) {
    setVerdict(keyId, state.verdicts.get(keyId) === verdict ? null : verdict);
    afterVerdict({ advance: verdict !== null });
  },
  toggleAgreed() {
    state.showAgreed = !state.showAgreed;
    renderCards();
  },
  addManual(formData) {
    const kind = formData.get("event_kind");
    const event = {
      church_slug: formData.get("church_slug") || "",
      event_type: formData.get("event_type") || "mass",
      event_kind: kind,
      day_of_week: kind === "weekly" ? formData.get("day_of_week") : null,
      date: kind === "weekly" ? null : formData.get("date") || null,
      start_time: (formData.get("start_time") || "").trim(),
      end_time: (formData.get("end_time") || "").trim() || null,
      cancelled: formData.get("cancelled") === "on",
      note: (formData.get("note") || "").trim() || null,
      page_number: state.page,
      origin: "human",
      sources: [],
    };
    if (!event.church_slug || !event.start_time) {
      toast("A church and a start time are required", true);
      return;
    }
    if (event.event_kind === "specific_date" && !event.date) {
      toast("Pick a date, or switch the event to weekly", true);
      return;
    }
    // A local id is enough to dedupe and delete; the server recomputes the real
    // one from the event's own fields when the label is saved.
    event.key_id = `human:${[
      event.church_slug,
      event.event_type,
      event.event_kind,
      event.day_of_week,
      event.date,
      event.start_time,
      event.end_time,
      event.cancelled,
    ].join("|")}`;

    if (!addManualEvent(event)) {
      toast("That event is already in the list");
      return;
    }
    renderCards();
    renderFinishHint();
    scheduleAutosave();
    toast("Event added");
  },
  removeManual(keyId) {
    removeManualEvent(keyId);
    renderCards();
    renderFinishHint();
    scheduleAutosave();
  },
  setWrongBulletin(value) {
    state.wrongBulletin = value;
    state.dirty = true;
    scheduleAutosave();
  },
  openTask,
});

// ── verdict shortcuts on the focused card ─────────────────────────────────
function applyToFocused(verdict) {
  const card = focusedCard();
  if (!card) return;
  if (card.kind === "conflict") setConflictAll(card.conflict, verdict);
  else if (card.candidate) setVerdict(card.candidate.key_id, verdict);
  else return;
  afterVerdict();
}

function clearFocused() {
  const card = focusedCard();
  if (!card) return;
  if (card.kind === "conflict") {
    for (const variant of card.conflict.variants) setVerdict(variant.key_id, null);
  } else if (card.candidate) {
    setVerdict(card.candidate.key_id, null);
  } else {
    return;
  }
  afterVerdict({ advance: false });
}

function chooseByDigit(digit) {
  const card = focusedCard();
  if (!card) return;
  if (card.kind === "conflict") {
    const variant = card.conflict.variants[digit - 1];
    if (!variant) return;
    pickVariant(card.conflict, variant.key_id);
    afterVerdict();
    return;
  }
  if (card.candidate && digit <= 2) {
    setVerdict(card.candidate.key_id, digit === 1 ? "accept" : "reject");
    afterVerdict();
  }
}

// ── completion ────────────────────────────────────────────────────────────
async function completeAndAdvance() {
  const remaining = undecidedIds().length;
  if (remaining) {
    toast(`${remaining} disagreement${remaining === 1 ? "" : "s"} still undecided`, true);
    return;
  }
  const next = state.nextUrl;
  const response = await save("complete");
  if (!response) return;
  if (next && next !== state.task.bulletin_source_url) await openTask(next);
  else await openTask(undefined);
}

async function skipBulletin() {
  const reason = window.prompt("Why skip this bulletin?", state.label?.skip_reason || "");
  if (reason === null) return;
  const next = state.nextUrl;
  const payload = { ...buildLabel("skipped"), skip_reason: reason };
  const response = await guard(() => api.saveLabel(payload), "Could not save");
  if (!response) return;
  state.dirty = false;
  renderProgress(response.progress);
  toast("Skipped");
  await openTask(next || undefined);
}

// ── panels ────────────────────────────────────────────────────────────────
const togglePanel = (id, force) => {
  const node = document.getElementById(id);
  node.hidden = force !== undefined ? !force : !node.hidden;
};

// ── boot ──────────────────────────────────────────────────────────────────
function wireChrome() {
  document.getElementById("sort-select").addEventListener("change", async (event) => {
    state.params.sort = event.target.value;
    await refreshQueue();
  });
  document.getElementById("filter-select").addEventListener("change", async (event) => {
    state.params.which = event.target.value;
    await refreshQueue();
  });
  document.getElementById("queue-toggle").addEventListener("click", () => togglePanel("queue-panel"));
  document.getElementById("queue-close").addEventListener("click", () => togglePanel("queue-panel", false));
  document.getElementById("help-toggle").addEventListener("click", () => togglePanel("help-panel"));
  document.getElementById("help-close").addEventListener("click", () => togglePanel("help-panel", false));

  document.getElementById("page-prev").addEventListener("click", () => setPage(state.page - 1));
  document.getElementById("page-next").addEventListener("click", () => setPage(state.page + 1));

  document.getElementById("save-partial").addEventListener("click", () => save("in_progress"));
  document.getElementById("save-complete").addEventListener("click", completeAndAdvance);
  document.getElementById("skip-bulletin").addEventListener("click", skipBulletin);

  document.getElementById("bulletin-notes").addEventListener("input", (event) => {
    state.notes = event.target.value;
    state.dirty = true;
    scheduleAutosave();
  });

  // Clicking into the PDF hands the keyboard to the viewer's own document, where
  // none of the shortcuts below can be heard. Take it back as soon as the mouse
  // returns to the decisions column, so `1`/`a`/`x` keep working after a scroll.
  document.querySelector(".pane--work").addEventListener("mouseenter", () => {
    if (document.activeElement?.tagName === "IFRAME") {
      document.activeElement.blur();
      window.focus();
    }
  });

  // A refresh or a closed tab should never lose a verdict.
  window.addEventListener("beforeunload", (event) => {
    if (!state.dirty) return;
    event.preventDefault();
    event.returnValue = "";
  });

  bindKeys({
    j: () => moveFocus(1),
    k: () => moveFocus(-1),
    a: () => applyToFocused("accept"),
    x: () => applyToFocused("reject"),
    u: clearFocused,
    digit: chooseByDigit,
    "[": () => setPage(state.page - 1),
    "]": () => setPage(state.page + 1),
    p: () => {
      const page = focusedCard()?.page;
      if (page) setPage(page);
      else toast("No model reported a page for this one");
    },
    g: () => {
      state.showAgreed = !state.showAgreed;
      renderCards();
    },
    n: () => {
      const form = document.getElementById("add-form");
      form?.scrollIntoView({ block: "center" });
      form?.elements.church_slug?.focus();
    },
    s: () => save("in_progress"),
    S: skipBulletin,
    Enter: completeAndAdvance,
    q: () => togglePanel("queue-panel"),
    "?": () => togglePanel("help-panel"),
    Escape: () => {
      togglePanel("queue-panel", false);
      togglePanel("help-panel", false);
    },
  });
}

async function boot() {
  wireChrome();
  state.config = await guard(() => api.config(), "Could not reach the server");
  if (!state.config) return;

  document.getElementById("sort-select").value = state.params.sort;
  document.getElementById("filter-select").value = state.params.which;

  await refreshQueue();
  await openTask(undefined);
  if (!state.queue.length) toast("No bulletins to label with the current filter");
}

boot();
