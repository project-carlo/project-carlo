/** DOM rendering for the review pane, PDF viewer, queue and progress line. */

import { state, candidateIndex, disputedIds, undecidedIds } from "./state.js";

export const actions = {};

/** Register the callbacks main.js owns, so rendering stays free of app logic. */
export function bindActions(handlers) {
  Object.assign(actions, handlers);
}

// ── tiny DOM helper ───────────────────────────────────────────────────────
function el(tag, props = {}, children = []) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(props)) {
    if (value === null || value === undefined || value === false) continue;
    if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (key === "html") node.innerHTML = value;
    else if (key.startsWith("on")) node.addEventListener(key.slice(2).toLowerCase(), value);
    else node.setAttribute(key, value === true ? "" : String(value));
  }
  for (const child of [].concat(children)) {
    if (child) node.append(child);
  }
  return node;
}

const churchName = (slug) => state.config?.church_names?.[slug] || slug;

// ── event display ─────────────────────────────────────────────────────────
/** Render an event as labelled segments, highlighting the fields under dispute.
 *
 *  Segments map onto the logical fields the server diffs by, so the one thing
 *  the models actually disagree about is the one thing that lights up.
 */
function eventLine(event, highlight = []) {
  const lit = new Set(highlight);
  const when =
    event.event_kind === "weekly"
      ? `Weekly ${event.day_of_week || "?"}`
      : event.date || "undated";
  const segments = [
    ["church", churchName(event.church_slug)],
    ["type", event.event_type],
    ["when", when],
    ["start", event.start_time],
    ["end", event.end_time ? `– ${event.end_time}` : null],
    ["cancelled", event.cancelled ? "CANCELLED" : null],
  ];

  return el(
    "div",
    { class: "option__event" },
    segments
      .filter(([, value]) => value)
      .flatMap(([field, value], index) => [
        index ? document.createTextNode(" · ") : null,
        el("span", { class: lit.has(field) ? "option__diff" : null, text: value }),
      ]),
  );
}

function sourceChips(candidate) {
  const chips = candidate.sources.map((name) =>
    el("span", { class: "chip chip--run", text: name }),
  );
  if (candidate.page_number) {
    chips.push(el("span", { class: "chip", text: `p. ${candidate.page_number}` }));
  }
  // Runs that filed this same slot under a single date instead of weekly. Shown
  // rather than asked about: the recurrence pass settles that from history
  // across bulletins, and one bulletin usually cannot.
  for (const reading of candidate.also_read_as || []) {
    chips.push(
      el("span", {
        class: "chip chip--muted",
        title:
          `${reading.sources.join(", ")} read this slot as ${reading.when}. ` +
          "Weekly vs. a single date is settled from history across bulletins, " +
          "so it is not a question here.",
        text: `also read as ${reading.when}`,
      }),
    );
  }
  for (const note of candidate.notes || []) {
    chips.push(el("span", { class: "chip", title: `${note.run}: ${note.note}`, text: note.note }));
  }
  return el("div", { class: "option__meta" }, chips);
}

// ── cards ─────────────────────────────────────────────────────────────────
/** Agreed events sitting one field from this decision — usually the duplicate
 *  that makes the answer obvious. */
function contextBlock(context) {
  if (!context?.length) return null;
  return el("div", { class: "context" }, [
    el("div", { text: "Every model already agreed on:" }),
    ...context.map((candidate) => el("code", { text: candidate.summary })),
  ]);
}

function optionRow({ candidate, keyHint, pressed, rejected, onPick, onToggle, highlight }) {
  // Three states, not two: an untouched variant and a rejected one must not look
  // the same, or a half-finished conflict is indistinguishable from a decided one.
  const verdictClass = pressed ? " option--accepted" : rejected ? " option--rejected" : "";
  return el(
    "div",
    {
      class: `option${verdictClass}`,
      "aria-pressed": pressed ? "true" : "false",
      role: "button",
      tabindex: "-1",
      onClick: onPick,
    },
    [
      el("span", { class: "option__key", text: keyHint }),
      el("span", { class: "option__body" }, [
        eventLine(candidate.event, highlight),
        sourceChips(candidate),
      ]),
      onToggle
        ? el("button", {
            class: "btn btn--icon btn--accept",
            "aria-pressed": pressed ? "true" : "false",
            title: "Accept this one as well as any other pick",
            text: "✓",
            onClick: (occasion) => {
              occasion.stopPropagation();
              onToggle();
            },
          })
        : null,
    ],
  );
}

function conflictCard(conflict, index, focused) {
  const verdictFor = (id) => state.verdicts.get(id);
  const decided = conflict.variants.every((variant) => verdictFor(variant.key_id));
  const anyAccepted = conflict.variants.some((v) => verdictFor(v.key_id) === "accept");

  const classes = ["card"];
  if (focused) classes.push("card--focused");
  if (!decided) classes.push("card--undecided");
  else classes.push(anyAccepted ? "card--decided" : "card--rejected");

  return el("article", { class: classes.join(" "), "data-card": index }, [
    el("header", { class: "card__head" }, [
      el("span", { class: "card__title" }, [
        document.createTextNode("Models disagree on "),
        el("em", { text: conflict.field_labels.join(" + ") }),
      ]),
      el("span", { class: "card__hint", text: `${conflict.variants.length} readings` }),
    ]),

    ...conflict.variants.map((variant, position) =>
      optionRow({
        candidate: variant,
        keyHint: String(position + 1),
        pressed: verdictFor(variant.key_id) === "accept",
        rejected: verdictFor(variant.key_id) === "reject",
        highlight: conflict.fields,
        onPick: () => actions.pick(conflict, variant.key_id),
        onToggle: () =>
          actions.toggle(
            variant.key_id,
            verdictFor(variant.key_id) === "accept" ? null : "accept",
          ),
      }),
    ),

    contextBlock(conflict.context),

    el("div", { class: "card__actions" }, [
      el("button", {
        class: "btn",
        type: "button",
        text: "Keep all",
        title: "All of these are real events (a)",
        onClick: () => actions.setAll(conflict, "accept"),
      }),
      el("button", {
        class: "btn btn--reject",
        type: "button",
        "aria-pressed": decided && !anyAccepted ? "true" : "false",
        text: "None are right",
        title: "Reject every reading (x)",
        onClick: () => actions.setAll(conflict, "reject"),
      }),
    ]),
  ]);
}

function singleCard(candidate, index, focused, { agreed = false } = {}) {
  const verdict = state.verdicts.get(candidate.key_id);
  const classes = ["card"];
  if (focused) classes.push("card--focused");
  if (!verdict) classes.push("card--undecided");
  else classes.push(verdict === "accept" ? "card--decided" : "card--rejected");

  const missingFrom = (state.task.runs || []).filter(
    (name) => !candidate.sources.includes(name),
  );

  return el("article", { class: classes.join(" "), "data-card": index }, [
    agreed
      ? null
      : el("header", { class: "card__head" }, [
          el("span", { class: "card__title" }, [
            document.createTextNode("Only "),
            el("em", { text: candidate.sources.join(", ") }),
            document.createTextNode(
              missingFrom.length ? ` found this — ${missingFrom.join(", ")} did not` : " found this",
            ),
          ]),
        ]),
    el("div", { class: "option", "aria-pressed": verdict === "accept" ? "true" : "false" }, [
      el("span", { class: "option__key", text: agreed ? "✓" : "1" }),
      el("span", { class: "option__body" }, [
        eventLine(candidate.event),
        sourceChips(candidate),
      ]),
    ]),
    agreed ? null : contextBlock(candidate.context),
    el("div", { class: "card__actions" }, [
      el("button", {
        class: "btn btn--accept",
        type: "button",
        "aria-pressed": verdict === "accept" ? "true" : "false",
        text: "Correct",
        onClick: () => actions.toggle(candidate.key_id, "accept"),
      }),
      el("button", {
        class: "btn btn--reject",
        type: "button",
        "aria-pressed": verdict === "reject" ? "true" : "false",
        text: "Not in the bulletin",
        onClick: () => actions.toggle(candidate.key_id, "reject"),
      }),
    ]),
  ]);
}

function manualCard(event, index, focused) {
  const classes = ["card", "card--decided"];
  if (focused) classes.push("card--focused");
  return el("article", { class: classes.join(" "), "data-card": index }, [
    el("header", { class: "card__head" }, [
      el("span", { class: "card__title" }, [
        document.createTextNode("Added by hand — "),
        el("em", { text: "no model found this" }),
      ]),
      el("button", {
        class: "btn btn--icon",
        type: "button",
        text: "Remove",
        onClick: () => actions.removeManual(event.key_id),
      }),
    ]),
    el("div", { class: "option", "aria-pressed": "true" }, [
      el("span", { class: "option__key", text: "+" }),
      el("span", { class: "option__body" }, [eventLine(event)]),
    ]),
  ]);
}

// ── manual add form ───────────────────────────────────────────────────────
function addForm() {
  const churches = state.task.parish_churches?.length
    ? state.task.parish_churches
    : state.config?.churches_by_parish?.[state.task.parish_slug] || [];

  const form = el("form", { class: "card", id: "add-form" }, [
    el("header", { class: "card__head" }, [
      el("span", { class: "card__title", text: "Add an event the models missed" }),
      el("span", { class: "card__hint", text: "n" }),
    ]),
    el("div", { class: "addform" }, [
      el("label", {}, [
        el("span", { text: "Church" }),
        el(
          "select",
          { name: "church_slug", required: true },
          churches.map((church) =>
            el("option", { value: church.slug, text: church.name }),
          ),
        ),
      ]),
      el("label", {}, [
        el("span", { text: "Type" }),
        el(
          "select",
          { name: "event_type" },
          ["mass", "confession", "adoration"].map((value) =>
            el("option", { value, text: value }),
          ),
        ),
      ]),
      el("label", {}, [
        el("span", { text: "Recurrence" }),
        el(
          "select",
          { name: "event_kind", onChange: (occasion) => syncKind(occasion.target.form) },
          [
            el("option", { value: "weekly", text: "Weekly" }),
            el("option", { value: "specific_date", text: "One date" }),
          ],
        ),
      ]),
      el("label", { id: "add-when" }, [
        el("span", { text: "Day" }),
        el(
          "select",
          { name: "day_of_week" },
          ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].map(
            (value) => el("option", { value, text: value }),
          ),
        ),
      ]),
      el("label", { id: "add-date", hidden: true }, [
        el("span", { text: "Date" }),
        el("input", { type: "date", name: "date" }),
      ]),
      el("label", {}, [
        el("span", { text: "Start" }),
        el("input", { name: "start_time", placeholder: "9:00 AM", required: true }),
      ]),
      el("label", {}, [
        el("span", { text: "End (optional)" }),
        el("input", { name: "end_time", placeholder: "9:45 AM" }),
      ]),
      el("label", { class: "addform__check" }, [
        el("input", { type: "checkbox", name: "cancelled" }),
        el("span", { text: "Cancelled" }),
      ]),
      el("label", { class: "addform__wide" }, [
        el("span", { text: "Note (optional)" }),
        el("input", { name: "note", placeholder: "Latin, Spanish, first Friday…" }),
      ]),
      el("div", { class: "addform__actions" }, [
        el("button", { class: "btn btn--primary", type: "submit", text: "Add event" }),
        el("span", { class: "card__hint", text: "Times as 9:00 AM · dates as YYYY-MM-DD" }),
      ]),
    ]),
  ]);

  form.addEventListener("submit", (occasion) => {
    occasion.preventDefault();
    actions.addManual(new FormData(form));
    form.reset();
    syncKind(form);
  });
  return form;
}

/** Show the day picker for weekly events and the date picker for one-offs. */
function syncKind(form) {
  if (!form) return;
  const weekly = form.elements.event_kind.value === "weekly";
  form.querySelector("#add-when").hidden = !weekly;
  form.querySelector("#add-date").hidden = weekly;
}

// ── panes ─────────────────────────────────────────────────────────────────
export function renderCards() {
  const host = document.getElementById("cards");
  host.replaceChildren();
  state.cards = [];
  if (!state.task) {
    host.append(el("p", { class: "empty", text: "Nothing left in this queue." }));
    return;
  }

  const push = (card) => {
    state.cards.push(card);
    return state.cards.length - 1;
  };
  const focusedAt = (index) => index === state.focus;

  if (state.task.conflicts.length) {
    host.append(sectionHead(`Disagreements (${state.task.conflicts.length})`));
    for (const conflict of state.task.conflicts) {
      const index = push({ kind: "conflict", conflict, page: conflict.variants[0].page_number });
      host.append(conflictCard(conflict, index, focusedAt(index)));
    }
  }

  if (state.task.singletons.length) {
    host.append(sectionHead(`Found by one model (${state.task.singletons.length})`));
    for (const candidate of state.task.singletons) {
      const index = push({ kind: "single", candidate, page: candidate.page_number });
      host.append(singleCard(candidate, index, focusedAt(index)));
    }
  }

  if (state.manual.length) {
    host.append(sectionHead(`Added by hand (${state.manual.length})`));
    for (const event of state.manual) {
      const index = push({ kind: "manual", event, page: event.page_number });
      host.append(manualCard(event, index, focusedAt(index)));
    }
  }

  host.append(
    sectionHead(
      `Agreed by every model (${state.task.agreed.length})`,
      state.showAgreed ? "hide" : "review",
      () => actions.toggleAgreed(),
    ),
  );
  if (state.showAgreed) {
    for (const candidate of state.task.agreed) {
      const index = push({ kind: "single", candidate, page: candidate.page_number });
      host.append(singleCard(candidate, index, focusedAt(index), { agreed: true }));
    }
  }

  host.append(sectionHead("Missing events"));
  host.append(addForm());
  syncKind(document.getElementById("add-form"));

  const focused = host.querySelector(".card--focused");
  if (focused) focused.scrollIntoView({ block: "nearest" });
}

function sectionHead(title, actionLabel, onAction) {
  return el("div", { class: "section-head" }, [
    el("span", { text: title }),
    actionLabel ? el("button", { type: "button", text: actionLabel, onClick: onAction }) : null,
  ]);
}

export function renderBanner() {
  const host = document.getElementById("banner-slot");
  host.replaceChildren();
  if (!state.task) return;

  const flagged = state.task.wrong_bulletin_runs || [];
  const counts = Object.entries(state.task.run_event_counts || {})
    .map(([name, count]) => `${name}: ${count}`)
    .join(" · ");

  host.append(
    el("div", { class: "banner" }, [
      el("label", {}, [
        el("input", {
          type: "checkbox",
          checked: state.wrongBulletin,
          onChange: (occasion) => actions.setWrongBulletin(occasion.target.checked),
        }),
        el("span", {
          text: flagged.length
            ? `Wrong bulletin? ${flagged.join(", ")} flagged this PDF as the wrong document.`
            : "This PDF is not a usable bulletin for this parish",
        }),
      ]),
      el("div", { class: "option__meta" }, [
        el("span", { class: "chip", text: `${state.task.candidate_count} candidates` }),
        el("span", { class: "chip", text: `${state.task.agreed_count} agreed` }),
        el("span", {
          class: state.task.disputed_count ? "chip chip--warn" : "chip",
          text: `${state.task.disputed_count} disputed`,
        }),
        ...(counts ? [el("span", { class: "chip", text: counts })] : []),
      ]),
    ]),
  );
}

export function renderPdf() {
  const holder = document.getElementById("pdf-holder");
  const openLink = document.getElementById("pdf-open");
  if (!state.task) {
    holder.replaceChildren(el("p", { class: "empty", text: "No bulletin loaded." }));
    return;
  }

  document.getElementById("bulletin-parish").textContent =
    state.task.parish_name || state.task.parish_slug;
  document.getElementById("bulletin-date").textContent =
    state.task.published_date || state.task.fetched_at?.slice(0, 10) || "date unknown";
  document.getElementById("page-label").textContent = `p. ${state.page}`;

  const base = `/api/pdf?url=${encodeURIComponent(state.task.bulletin_source_url)}`;
  openLink.href = base;

  if (!state.task.has_pdf) {
    holder.replaceChildren(
      el("p", {
        class: "empty",
        text: "This bulletin's PDF is not on disk. Run `pnpm fetch` to download it, then reload.",
      }),
    );
    return;
  }

  // The viewer only honours the fragment when the src actually changes, so the
  // frame is replaced rather than mutated. `pagemode` collapses the thumbnail
  // rail where the viewer supports it, and is ignored where it does not.
  const src = `${base}#page=${state.page}&view=FitH&pagemode=none`;
  const existing = holder.querySelector("iframe");
  if (!existing || existing.dataset.src !== src) {
    holder.replaceChildren(el("iframe", { src, "data-src": src, title: "Bulletin PDF" }));
  }
}

export function renderProgress(progress) {
  if (progress) state.progress = progress;
  const summary = state.progress;
  if (!summary) return;
  document.getElementById("progress-line").textContent =
    `${summary.complete}/${summary.bulletins} bulletins complete · ` +
    `${summary.disputed_undecided} disagreements left · ` +
    `${summary.labeled_events} ground-truth events`;
}

export function renderQueue() {
  const list = document.getElementById("queue-list");
  list.replaceChildren();
  const current = state.task?.bulletin_source_url;

  for (const item of state.queue) {
    const done = item.status === "complete";
    list.append(
      el("li", {}, [
        el(
          "button",
          {
            type: "button",
            "aria-current": item.bulletin_source_url === current ? "true" : "false",
            onClick: () => actions.openTask(item.bulletin_source_url),
          },
          [
            el("span", { class: "queue__row" }, [
              el("span", { class: "queue__name", text: item.parish_name }),
              el("span", {
                class: "chip" + (item.undecided_count ? " chip--warn" : ""),
                text: done ? "done" : `${item.undecided_count} left`,
              }),
            ]),
            el("span", {
              class: "queue__meta",
              text:
                `${item.published_date || "undated"} · ${item.candidate_count} candidates · ` +
                `${item.disputed_count} disputed`,
            }),
          ],
        ),
      ]),
    );
  }
  if (!state.queue.length) {
    list.append(el("li", {}, el("p", { class: "empty", text: "Queue is empty." })));
  }
}

export function renderFinishHint() {
  const hint = document.getElementById("finish-hint");
  const remaining = undecidedIds().length;
  const button = document.getElementById("save-complete");
  const accepted =
    [...state.verdicts.values()].filter((verdict) => verdict === "accept").length +
    state.manual.length;

  button.disabled = remaining > 0;
  hint.classList.toggle("finish__hint--blocked", remaining > 0);
  hint.textContent = remaining
    ? `${remaining} disagreement${remaining === 1 ? "" : "s"} still undecided.`
    : `${accepted} events will be saved as ground truth ` +
      `(${state.task?.agreed_count || 0} of them agreed by every model — press g to review).`;
}

export function renderNotes() {
  const field = document.getElementById("bulletin-notes");
  if (field.value !== state.notes) field.value = state.notes;
}

export function renderAll() {
  renderBanner();
  renderCards();
  renderPdf();
  renderFinishHint();
  renderNotes();
  renderQueue();
}

export { disputedIds, candidateIndex };
