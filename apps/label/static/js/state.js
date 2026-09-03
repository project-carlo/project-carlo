/** Session state, and the rules turning clicks into a saveable label.
 *
 *  A verdict is recorded per candidate `key_id`: `accept` puts the event into
 *  ground truth, `reject` records it as a confirmed extraction error. Candidates
 *  every classifier agreed on start accepted, so a labeler only has to touch the
 *  ones the models actually split on.
 */

export const state = {
  config: null,
  params: { sort: "disagreement", which: "todo", parish: null },
  queue: [],
  progress: null,

  task: null,
  label: null,
  nextUrl: null,

  /** key_id -> "accept" | "reject" */
  verdicts: new Map(),
  /** events a human added because no model proposed them */
  manual: [],
  notes: "",
  wrongBulletin: false,

  /** flattened focusable cards, rebuilt on every render */
  cards: [],
  focus: 0,
  showAgreed: false,
  page: 1,
  dirty: false,
  startedAt: 0,
};

/** Every candidate on the current task, keyed by key_id. */
export function candidateIndex() {
  const index = new Map();
  if (!state.task) return index;
  for (const candidate of state.task.agreed) index.set(candidate.key_id, candidate);
  for (const candidate of state.task.singletons) index.set(candidate.key_id, candidate);
  for (const conflict of state.task.conflicts) {
    for (const candidate of conflict.variants) index.set(candidate.key_id, candidate);
  }
  return index;
}

/** key_ids the labeler is expected to rule on: everything the models split over. */
export function disputedIds() {
  if (!state.task) return [];
  return [
    ...state.task.singletons.map((candidate) => candidate.key_id),
    ...state.task.conflicts.flatMap((conflict) =>
      conflict.variants.map((candidate) => candidate.key_id),
    ),
  ];
}

export function undecidedIds() {
  return disputedIds().filter((id) => !state.verdicts.has(id));
}

/** Load a task, seeding verdicts from a saved label or from model agreement. */
export function adoptTask(payload) {
  state.task = payload.task;
  state.label = payload.label || null;
  state.nextUrl = payload.next_url || null;
  state.verdicts = new Map();
  state.manual = [];
  state.notes = state.label?.notes || "";
  state.wrongBulletin = Boolean(state.label?.wrong_bulletin);
  state.focus = 0;
  state.dirty = false;
  state.startedAt = Date.now();
  state.page = 1;

  if (state.label) {
    for (const event of state.label.events || []) {
      if (event.origin === "human") state.manual.push(event);
      else state.verdicts.set(event.key_id, "accept");
    }
    for (const event of state.label.rejected || []) {
      state.verdicts.set(event.key_id, "reject");
    }
  }

  // Candidates every run proposed are pre-accepted. They are the cheap majority
  // of any bulletin, and re-confirming each one by hand is the single biggest
  // waste of a labeler's time.
  for (const candidate of state.task.agreed) {
    if (!state.verdicts.has(candidate.key_id)) {
      state.verdicts.set(candidate.key_id, "accept");
    }
  }
}

export function setVerdict(keyId, verdict) {
  if (verdict === null) state.verdicts.delete(keyId);
  else state.verdicts.set(keyId, verdict);
  state.dirty = true;
}

/** Accept one variant of a conflict and reject its siblings. */
export function pickVariant(conflict, keyId) {
  for (const variant of conflict.variants) {
    setVerdict(variant.key_id, variant.key_id === keyId ? "accept" : "reject");
  }
}

export function setConflictAll(conflict, verdict) {
  for (const variant of conflict.variants) setVerdict(variant.key_id, verdict);
}

export function addManualEvent(event) {
  if (state.manual.some((existing) => existing.key_id === event.key_id)) return false;
  state.manual.push(event);
  state.dirty = true;
  return true;
}

export function removeManualEvent(keyId) {
  state.manual = state.manual.filter((event) => event.key_id !== keyId);
  state.dirty = true;
}

/** Build the label document to POST. */
export function buildLabel(status) {
  const index = candidateIndex();
  const events = [];
  const rejected = [];

  for (const [keyId, verdict] of state.verdicts) {
    const candidate = index.get(keyId);
    if (!candidate) continue;
    const row = {
      ...candidate.event,
      key_id: keyId,
      origin: "model",
      sources: candidate.sources,
      page_number: candidate.page_number,
    };
    (verdict === "accept" ? events : rejected).push(row);
  }
  for (const event of state.manual) {
    events.push({ ...event, origin: "human" });
  }

  return {
    bulletin_source_url: state.task.bulletin_source_url,
    parish_slug: state.task.parish_slug,
    content_hash: state.task.content_hash,
    published_date: state.task.published_date,
    status,
    wrong_bulletin: state.wrongBulletin,
    notes: state.notes,
    events,
    rejected,
    seconds_spent: Math.round((Date.now() - state.startedAt) / 1000),
  };
}
