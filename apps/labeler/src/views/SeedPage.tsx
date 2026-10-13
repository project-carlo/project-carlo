import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api, pdfUrl } from "../api";
import { PdfViewer, type ScrollRequest } from "../components/PdfViewer";
import { RowEditor } from "../components/RowEditor";
import { formatDate } from "../lib/dates";
import { navigate, seedHref, SEEDS_HREF } from "../lib/route";
import { asDated, editRow, rowProblems } from "../lib/rows";
import {
  approve,
  chooseForGroup,
  describeEntry,
  dropSlot,
  editSlot,
  expiredQuestions,
  fromEditorRow,
  groupOf,
  isOpen,
  newestReadBulletin,
  nextSeedToReview,
  openCount,
  reopenSlot,
  replaceSlot,
  replaceSlots,
  resolveBulletin,
  slotGroups,
  toEditorRow,
} from "../lib/seeds";
import type { Church, Config, EditorRow, SeedDetail, SeedFile, SeedSlot } from "../types";
import { SEED_STATUS_LABEL, SEED_STATUS_STYLE } from "../lib/seedStatus";

interface Props {
  parish: string;
  config: Config | null;
  labeler: string;
  onLabelerChange: (name: string) => void;
}

function isTyping(el: Element | null): boolean {
  return !!el?.matches('input:not([type="checkbox"]), textarea, select, [contenteditable="true"]');
}

function hostOf(url: string): string {
  try {
    return new URL(url).host;
  } catch {
    return url;
  }
}

export function SeedPage(props: Props) {
  const { parish } = props;
  const [detail, setDetail] = useState<SeedDetail | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setDetail(null);
    setError(null);
    api
      .seed(parish)
      .then((d) => !cancelled && setDetail(d))
      .catch((e: Error) => !cancelled && setError(e.message));
    return () => {
      cancelled = true;
    };
  }, [parish]);

  if (error) {
    return (
      <div className="p-8">
        <p className="mb-4 text-red-700">Could not open this seed: {error}</p>
        <a className="btn" href={SEEDS_HREF}>
          Back to the seeds
        </a>
      </div>
    );
  }
  if (!detail) return <div className="p-8 text-slate-500">Loading seed…</div>;
  if (!detail.seed) {
    return (
      <div className="p-8">
        <p className="mb-2 text-red-700">This seed file can't be reviewed until it is fixed:</p>
        <ul className="mb-4 list-disc pl-5 text-sm text-red-700" data-testid="seed-problems">
          {detail.problems.map((p) => (
            <li key={p}>{p}</li>
          ))}
        </ul>
        <a className="btn" href={SEEDS_HREF}>
          Back to the seeds
        </a>
      </div>
    );
  }
  return <SeedReview key={parish} initial={{ ...detail, seed: detail.seed }} {...props} />;
}

function SeedReview({ initial, parish, labeler, onLabelerChange }: Props & { initial: SeedDetail & { seed: SeedFile } }) {
  const [detail, setDetail] = useState<SeedDetail>(initial);
  const [seed, setSeed] = useState<SeedFile>(initial.seed);
  const [message, setMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [advancing, setAdvancing] = useState(false);
  const advancingRef = useRef(false);
  // Saves go one at a time: each sends the whole file, so two in flight could
  // land out of order. A ref, so keys pressed before a re-render see it too.
  const savingRef = useRef(false);
  const [showSettled, setShowSettled] = useState(false);
  const [editing, setEditing] = useState<{ slotId: string; row: EditorRow } | null>(null);
  const tabs = useMemo(() => {
    const read = seed.bulletins.filter((b) => b.read);
    return read.length ? read : seed.bulletins;
  }, [seed.bulletins]);
  const [activeHash, setActiveHash] = useState<string | null>(tabs[0]?.content_hash ?? null);
  const [scrollTo, setScrollTo] = useState<ScrollRequest | null>(null);
  const groups = useMemo(() => slotGroups(seed), [seed]);
  const ordered = useMemo(
    () => [...groups.open, ...(showSettled ? groups.settled : []), ...groups.excluded],
    [groups, showSettled],
  );
  const [selectedId, setSelectedId] = useState<string | null>(ordered[0]?.id ?? null);
  const selected = seed.slots.find((s) => s.id === selectedId) ?? null;
  const drafting = seed.status === "drafting";
  const reviewer = labeler.trim();

  const save = useCallback(
    (next: SeedFile) => {
      const previous = seed;
      setSeed(next);
      savingRef.current = true;
      setSaving(true);
      setMessage(null);
      api
        .saveSeed(next)
        .then((d) => {
          setDetail(d);
          // A save is validated, so the file comes back whole.
          if (d.seed) setSeed(d.seed);
        })
        .catch((e: Error) => {
          setSeed(previous);
          setMessage(`Not saved: ${e.message}`);
        })
        .finally(() => {
          savingRef.current = false;
          setSaving(false);
        });
    },
    [seed],
  );

  /** Whether a review action may run now; says why not when it can't. */
  const canAct = (): boolean => {
    let why: string | null = null;
    if (savingRef.current) why = "Still saving the last change; try again in a moment.";
    else if (advancingRef.current) why = "Still finding the next seed; try again in a moment.";
    else if (drafting) why = "A subagent is still drafting this parish.";
    else if (!reviewer) why = "Type your name as the reviewer first.";
    if (why) setMessage(why);
    return !why;
  };

  const act = (slot: SeedSlot | null, change: (slot: SeedSlot) => SeedSlot | null, failure: string) => {
    if (!slot || !canAct()) return;
    const next = change(slot);
    if (!next) return setMessage(failure);
    save(replaceSlot(seed, next));
  };

  const choose = (slot: SeedSlot, index: number) => {
    if (!canAct()) return;
    const next = isOpen(slot) ? chooseForGroup(seed, slot, index, reviewer) : null;
    if (!next) return setMessage("That option can't settle this slot.");
    save(next);
  };
  /** Leave a slot out: an open question's whole group with it. */
  const drop = (slot: SeedSlot) => {
    if (!canAct()) return;
    const slots = isOpen(slot) ? groupOf(seed, slot) : [slot];
    save(replaceSlots(seed, slots.map((s) => dropSlot(s, reviewer))));
  };
  const dropExpired = () => {
    if (!canAct() || !expired.length) return;
    save(replaceSlots(seed, expired.map((s) => dropSlot(s, reviewer))));
  };
  const reopen = (slot: SeedSlot) => act(slot, (s) => reopenSlot(s), "This slot was left out with no entry to include.");
  const startEdit = (slot: SeedSlot) => {
    if (advancingRef.current) return;
    const entry = slot.entry ?? slot.options?.find((o) => o.leaning && o.entry)?.entry ?? slot.options?.find((o) => o.entry)?.entry;
    if (!entry) return setMessage("This slot has no entry to edit.");
    setEditing({ slotId: slot.id, row: toEditorRow(entry, slot.page) });
  };
  const saveEdit = () => {
    if (!editing) return;
    const slot = seed.slots.find((s) => s.id === editing.slotId);
    const problems = rowProblems(editing.row);
    if (problems.length) return setMessage(`Fill in: ${problems.join(", ")}`);
    if (editing.row.pending_split) return setMessage("A slot is one day or date; add the others as their own slots in the file.");
    if (!slot || !canAct()) return;
    const { entry, page } = fromEditorRow(editing.row);
    setEditing(null);
    act(slot, (s) => editSlot(s, entry, page, reviewer), "");
  };
  const doApprove = () => {
    if (!canAct()) return;
    const next = approve(seed, reviewer);
    if (!next) return setMessage("Answer every open question first.");
    save(next);
  };

  const goNext = async () => {
    if (savingRef.current || advancingRef.current || editing) return;
    advancingRef.current = true;
    setAdvancing(true);
    setMessage(null);
    try {
      const { seeds } = await api.seeds();
      const next = nextSeedToReview(seeds, parish);
      if (next) navigate(seedHref(next.parish_slug));
      else setMessage("No other seeds are ready to approve or need review.");
    } catch (e) {
      setMessage(`Could not find the next seed: ${(e as Error).message}`);
    } finally {
      advancingRef.current = false;
      setAdvancing(false);
    }
  };

  const showSource = (hash: string | null, page: number | null | undefined) => {
    if (!hash) return;
    setActiveHash(hash);
    if (page) setScrollTo({ page, nonce: Date.now() });
  };

  // ── keyboard ──
  const onKey = (e: KeyboardEvent) => {
    if (e.key === "Escape" && editing) {
      setEditing(null);
      return;
    }
    if (isTyping(e.target as HTMLElement) || e.ctrlKey || e.metaKey || e.altKey || editing) return;
    const index = selected ? ordered.findIndex((s) => s.id === selected.id) : -1;
    const handled = () => e.preventDefault();
    if (e.key === "j" || e.key === "ArrowDown") {
      const next = ordered[Math.min(ordered.length - 1, index + 1)];
      if (next) setSelectedId(next.id);
      return handled();
    }
    if (e.key === "k" || e.key === "ArrowUp") {
      const next = ordered[Math.max(0, index - 1)];
      if (next) setSelectedId(next.id);
      return handled();
    }
    if (!selected) return;
    if (/^[1-9]$/.test(e.key) && isOpen(selected)) {
      choose(selected, Number(e.key) - 1);
      return handled();
    }
    if (e.key === "e") {
      startEdit(selected);
      return handled();
    }
    if (e.key === "x") {
      drop(selected);
      return handled();
    }
    if (e.key === "r" && !isOpen(selected)) {
      reopen(selected);
      return handled();
    }
  };
  const onKeyRef = useRef(onKey);
  onKeyRef.current = onKey;
  useEffect(() => {
    const listener = (e: KeyboardEvent) => onKeyRef.current(e);
    window.addEventListener("keydown", listener);
    return () => window.removeEventListener("keydown", listener);
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    document.querySelector(`[data-slot-id="${selectedId}"]`)?.scrollIntoView({ block: "nearest" });
  }, [selectedId]);

  // A settled slot selected by a source link or an answer stays visible.
  useEffect(() => {
    if (selected && !isOpen(selected) && selected.decision === "include") setShowSettled(true);
  }, [selected]);

  const activeBulletin = seed.bulletins.find((b) => b.content_hash === activeHash) ?? null;
  const asOfHash = newestReadBulletin(seed)?.content_hash ?? null;
  const n_open = openCount(seed);
  const today = new Date().toLocaleDateString("en-CA");
  const expired = expiredQuestions(seed, today);
  const expiredIds = new Set(expired.map((s) => s.id));
  const churchIssues = seed.church_list_issues ?? [];
  const missing = new Set(seed.bulletins.map((b) => b.content_hash).filter((h) => !detail.bulletins_in_db.includes(h)));

  return (
    <div className="grid h-full grid-cols-[minmax(0,3fr)_minmax(0,2fr)] grid-rows-[minmax(0,1fr)] overflow-hidden">
      <div className="flex min-h-0 flex-col">
        <div className="flex shrink-0 gap-1 overflow-x-auto border-b border-slate-700 bg-slate-900 px-2 pt-1.5" data-testid="bulletin-tabs">
          {tabs.map((b) => (
            <button
              key={b.content_hash}
              onClick={() => setActiveHash(b.content_hash)}
              className={`rounded-t px-2.5 py-1 text-xs whitespace-nowrap ${
                b.content_hash === activeHash ? "bg-slate-800 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
              title={`${b.content_hash}\nfetched ${b.fetched_at}${missing.has(b.content_hash) ? "\nnot in the local database" : ""}`}
            >
              {b.published_date ? `Issue ${formatDate(b.published_date)}` : `Fetched ${b.fetched_at.slice(0, 10)}`}
              {b.content_hash === asOfHash && " · as of"}
              {!b.read && " · unread"}
            </button>
          ))}
        </div>
        <div className="min-h-0 flex-1">
          {activeHash ? (
            <PdfViewer key={activeHash} url={pdfUrl(parish, activeHash)} scrollTo={scrollTo} onPageChange={() => {}} />
          ) : (
            <div className="p-4 text-slate-500">The seed lists no bulletin.</div>
          )}
        </div>
      </div>

      <div className="flex min-w-0 flex-col border-l border-slate-300 bg-slate-50">
        <header className="shrink-0 space-y-1.5 border-b border-slate-200 bg-white px-3 py-2">
          <div className="flex flex-wrap items-center gap-2">
            <a href={SEEDS_HREF} className="text-sm text-sky-700 hover:underline">
              ← Seeds
            </a>
            <h1 className="truncate text-base font-semibold" title={parish}>
              {detail.parish.name}
            </h1>
            <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${SEED_STATUS_STYLE[seed.status]}`} data-testid="seed-status">
              {SEED_STATUS_LABEL[seed.status]}
            </span>
            {detail.loaded && <span className="text-xs text-emerald-700">loaded in the local database</span>}
            {saving && <span className="text-xs text-slate-500">saving…</span>}
            <label className="ml-auto flex items-center gap-1 text-xs text-slate-600">
              Reviewer
              <input
                value={labeler}
                onChange={(e) => onLabelerChange(e.target.value)}
                className="w-28 rounded border border-slate-300 bg-white px-1.5 py-0.5 text-xs"
                placeholder="Your name"
              />
            </label>
            <button
              className="btn-primary"
              disabled={n_open > 0 || drafting || seed.status === "approved" || seed.status === "blocked" || saving || advancing}
              onClick={doApprove}
              title={n_open ? `${n_open} questions still open` : "Approve: the next pipeline command loads it once merged"}
              data-testid="approve"
            >
              {seed.status === "approved" ? "Approved" : "Approve"}
            </button>
            <button
              className="btn"
              disabled={saving || advancing || !!editing}
              onClick={goNext}
              title="Open the next ready-to-approve seed, then seeds needing review"
              data-testid="next-seed"
            >
              {advancing ? "Finding next…" : "Next to review →"}
            </button>
          </div>
          {seed.summary && <p className="text-sm text-slate-700">{seed.summary}</p>}
          <p className="text-xs text-slate-500">
            As of {seed.as_of ?? "—"} · {seed.calls.length} external calls
            {seed.calls.length > 0 && ` ($${seed.calls.reduce((t, c) => t + (c.cost_usd ?? 0), 0).toFixed(3)})`}
            {seed.reviewer && ` · reviewer ${seed.reviewer}`}
            {seed.approved_at && ` · approved ${seed.approved_at.slice(0, 10)}`}
          </p>
          {seed.status === "blocked" && <p className="text-sm text-zinc-700">Blocked: {seed.blocked_reason}</p>}
          {drafting && <p className="text-sm text-amber-800">A subagent is still drafting this parish; it can't be reviewed yet.</p>}
          {detail.problems.length > 0 && (
            <ul className="list-disc pl-5 text-xs text-red-700" data-testid="seed-problems">
              {detail.problems.map((p) => (
                <li key={p}>{p}</li>
              ))}
            </ul>
          )}
          {churchIssues.length > 0 && (
            <div className="text-xs text-slate-700" data-testid="church-list-issues">
              <p className="font-medium">For the church list (not seeded):</p>
              <ul className="list-disc pl-5">
                {churchIssues.map((issue, i) => {
                  const hash = resolveBulletin(seed, issue.bulletin);
                  return (
                    <li key={i}>
                      <span className="font-medium">{issue.church}</span>: {issue.said}
                      {hash && (
                        <button className="ml-1 text-sky-700 hover:underline" onClick={() => showSource(hash, issue.page)}>
                          {issue.page ? `p. ${issue.page}` : "bulletin"}
                        </button>
                      )}
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
          {expired.length > 0 && !drafting && (
            <p className="flex items-center gap-2 text-xs text-amber-800">
              {expired.length} {expired.length === 1 ? "question asks" : "questions ask"} about dates that have passed.
              <button className="btn px-1.5 py-0 text-xs" onClick={dropExpired} disabled={saving} data-testid="drop-expired">
                Leave them out
              </button>
            </p>
          )}
          {message && <p className="text-sm text-red-700" data-testid="seed-message">{message}</p>}
        </header>

        <div className="min-h-0 flex-1 space-y-4 overflow-y-auto p-3">
          <Section title={`Open questions (${groups.open.length})`}>
            {groups.open.length === 0 && <p className="text-sm text-slate-500">None: approve when the rest looks right.</p>}
            {groups.open.map((slot) => (
              <SlotCard key={slot.id} {...cardProps(slot)} />
            ))}
          </Section>
          <Section
            title={`Settled (${groups.settled.length})`}
            collapsed={!showSettled}
            onToggle={() => setShowSettled((v) => !v)}
          >
            {groups.settled.map((slot) => (
              <SlotCard key={slot.id} {...cardProps(slot)} />
            ))}
          </Section>
          <Section title={`Left out (${groups.excluded.length})`}>
            {groups.excluded.map((slot) => (
              <SlotCard key={slot.id} {...cardProps(slot)} />
            ))}
          </Section>
        </div>
        <footer className="shrink-0 border-t border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-500">
          <kbd>j</kbd>/<kbd>k</kbd> move · <kbd>1</kbd>–<kbd>9</kbd> choose an option · <kbd>e</kbd> edit · <kbd>x</kbd> leave out ·{" "}
          <kbd>r</kbd> reopen · <kbd>Esc</kbd> cancel an edit
        </footer>
      </div>
    </div>
  );

  function cardProps(slot: SeedSlot): SlotCardProps {
    return {
      slot,
      seed,
      churches: detail.churches,
      selected: slot.id === selectedId,
      groupmates: isOpen(slot) ? groupOf(seed, slot) : [slot],
      expired: expiredIds.has(slot.id),
      editing: editing?.slotId === slot.id ? editing.row : null,
      refDate: activeBulletin?.published_date ?? null,
      onSelect: () => setSelectedId(slot.id),
      onChoose: (i) => choose(slot, i),
      onDrop: () => drop(slot),
      onReopen: () => reopen(slot),
      onEdit: () => startEdit(slot),
      onEditChange: (row) => setEditing({ slotId: slot.id, row }),
      onEditSave: saveEdit,
      onEditCancel: () => setEditing(null),
      onSource: showSource,
    };
  }
}

function Section({
  title,
  children,
  collapsed,
  onToggle,
}: {
  title: string;
  children: React.ReactNode;
  collapsed?: boolean;
  onToggle?: () => void;
}) {
  return (
    <section>
      <h2 className="mb-1.5 text-xs font-semibold tracking-wide text-slate-500 uppercase">
        {onToggle ? (
          <button onClick={onToggle} className="hover:text-slate-800">
            {collapsed ? "▸" : "▾"} {title}
          </button>
        ) : (
          title
        )}
      </h2>
      {!collapsed && <div className="space-y-2">{children}</div>}
    </section>
  );
}

interface SlotCardProps {
  slot: SeedSlot;
  /** The slots an answer to this one settles: its open group, or itself. */
  groupmates: SeedSlot[];
  expired: boolean;
  seed: SeedFile;
  churches: Church[];
  selected: boolean;
  editing: EditorRow | null;
  refDate: string | null;
  onSelect: () => void;
  onChoose: (index: number) => void;
  onDrop: () => void;
  onReopen: () => void;
  onEdit: () => void;
  onEditChange: (row: EditorRow) => void;
  onEditSave: () => void;
  onEditCancel: () => void;
  onSource: (hash: string | null, page: number | null | undefined) => void;
}

function SlotCard(props: SlotCardProps) {
  const { slot, seed, churches, selected, editing, groupmates } = props;
  const church = (slug: string | undefined) => churches.find((c) => c.slug === slug)?.name ?? slug ?? "";
  const open = isOpen(slot);
  const calls = new Map(seed.calls.map((c) => [c.id, c]));
  const newest = newestReadBulletin(seed)?.content_hash ?? null;
  return (
    <div
      data-slot-id={slot.id}
      data-testid={`slot-${slot.id}`}
      onMouseDown={props.onSelect}
      className={`rounded border bg-white p-2 text-sm ${selected ? "border-sky-500 ring-1 ring-sky-500" : "border-slate-200"} ${
        slot.decision === "exclude" && !open ? "opacity-80" : ""
      }`}
    >
      <div className="flex flex-wrap items-baseline gap-2">
        <span className="text-xs text-slate-400">{slot.id}</span>
        {slot.entry ? (
          <span className="font-medium">
            {describeEntry(slot.entry)} <span className="font-normal text-slate-500">· {church(slot.entry.church_slug)}</span>
          </span>
        ) : (
          <span className="font-medium text-slate-500">{open ? "No entry yet" : "No time (left out)"}</span>
        )}
        {slot.page && (
          <button className="text-xs text-sky-700 hover:underline" onClick={() => props.onSource(newest, slot.page)}>
            p. {slot.page}
          </button>
        )}
        {props.expired && <span className="text-xs text-amber-800">date passed</span>}
        {!open && (
          <span className={`text-xs ${slot.decision === "include" ? "text-emerald-700" : "text-zinc-500"}`}>
            {slot.decision === "include" ? "included" : "left out"}
            {slot.answer && ` by ${slot.answer.by} (${typeof slot.answer.choice === "number" ? `option ${slot.answer.choice + 1}` : slot.answer.choice})`}
          </span>
        )}
        <span className="ml-auto flex gap-1">
          <button className="btn px-1.5 py-0 text-xs" onClick={props.onEdit} title="Edit the entry (e)">
            Edit
          </button>
          <button className="btn px-1.5 py-0 text-xs" onClick={props.onDrop} title="Leave this slot out (x)">
            Leave out
          </button>
          {!open && (
            <button className="btn px-1.5 py-0 text-xs" onClick={props.onReopen} title="Reopen as a question (r)">
              Reopen
            </button>
          )}
        </span>
      </div>

      {open && (
        <div className="mt-1.5 rounded bg-amber-50 p-2">
          <p className="font-medium text-amber-900">{slot.question}</p>
          {groupmates.length > 1 && (
            <p className="text-xs text-amber-800" data-testid={`group-${slot.id}`}>
              One answer for {groupmates.length} slots: {groupmates.map((s) => s.id).join(", ")}
            </p>
          )}
          <div className="mt-1 flex flex-col gap-1">
            {(slot.options ?? []).map((option, i) => (
              <button
                key={i}
                onClick={() => props.onChoose(i)}
                className={`flex items-baseline gap-2 rounded border px-2 py-1 text-left text-sm hover:bg-white ${
                  option.leaning ? "border-amber-500 bg-amber-100" : "border-amber-200"
                }`}
                data-testid={`option-${slot.id}-${i}`}
              >
                <kbd>{i + 1}</kbd>
                <span>
                  {option.label}
                  {groupmates.length > 1
                    ? groupmates.map((g) => {
                        const entry = g.options?.[i]?.entry;
                        return entry ? (
                          <span key={g.id} className="block text-xs text-slate-600">
                            {describeEntry(entry)} · {church(entry.church_slug)}
                          </span>
                        ) : null;
                      })
                    : option.entry && (
                        <span className="block text-xs text-slate-600">
                          {describeEntry(option.entry)} · {church(option.entry.church_slug)}
                        </span>
                      )}
                </span>
                {option.leaning && <span className="ml-auto text-xs text-amber-800">agent leans to this</span>}
              </button>
            ))}
          </div>
        </div>
      )}

      {editing && (
        <div className="mt-1.5 space-y-1 rounded bg-sky-50 p-2">
          <RowEditor
            row={editing}
            index={0}
            churches={churches}
            selected
            warnings={[]}
            refDate={props.refDate}
            focusField={null}
            onFocusDone={() => {}}
            onSelect={() => {}}
            onPatch={(_, patch) => props.onEditChange(editRow(editing, patch))}
            onTransform={(_, fn) => props.onEditChange(fn(editing))}
            onLeave={() => {}}
            onDelete={props.onEditCancel}
            onDuplicate={() => {}}
            onMakeDated={() => props.onEditChange(asDated(editing, props.refDate))}
          />
          <div className="flex gap-2">
            <button className="btn-primary" onClick={props.onEditSave} data-testid="save-edit">
              Save as edited
            </button>
            <button className="btn" onClick={props.onEditCancel}>
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="mt-1.5 grid grid-cols-[repeat(auto-fill,minmax(10rem,1fr))] gap-1.5">
        {slot.sources.map((source, i) => {
          if (source.url && /^https?:\/\//.test(source.url)) {
            return (
              <a
                key={i}
                href={source.url}
                target="_blank"
                rel="noreferrer"
                className="rounded border border-slate-200 bg-slate-50 px-1.5 py-1 text-left text-xs hover:border-sky-400"
              >
                <span className="font-semibold text-slate-600">{source.source}</span>
                <span className="text-slate-400"> · {hostOf(source.url)}</span>
                <span className="block text-slate-800">{source.said}</span>
              </a>
            );
          }
          const call = calls.get(source.source);
          const hash = resolveBulletin(seed, source.bulletin ?? call?.bulletin);
          const bulletin = seed.bulletins.find((b) => b.content_hash === hash);
          const page = source.page ?? call?.page ?? null;
          return (
            <button
              key={i}
              onClick={() => props.onSource(hash, page)}
              disabled={!hash}
              className="rounded border border-slate-200 bg-slate-50 px-1.5 py-1 text-left text-xs hover:border-sky-400 disabled:hover:border-slate-200"
              title={call?.kind === "ask" ? `Asked: ${call.question}\nQuote: ${call.quote ?? ""}` : undefined}
            >
              <span className="font-semibold text-slate-600">
                {call ? `${call.id} ${call.kind} · ${call.model}` : source.source}
              </span>
              {bulletin && (
                <span className="text-slate-400">
                  {" "}
                  · {bulletin.published_date ? formatDate(bulletin.published_date) : bulletin.fetched_at.slice(0, 10)}
                  {page ? ` p.${page}` : ""}
                </span>
              )}
              <span className="block text-slate-800">{source.said}</span>
            </button>
          );
        })}
      </div>
      <p className="mt-1 text-xs text-slate-600">{slot.rationale}</p>
    </div>
  );
}
