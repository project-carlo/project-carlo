# Project Carlo: believed schedules updated by proposed changes

Status: implemented, with every parish still in extract mode until it is
seeded. Where the implementation had to decide something this plan left open,
or departs from it, see [Implementation decisions](#implementation-decisions).

Today every bulletin is extracted from scratch, and the site shows whatever the
parish's latest bulletin produced. Anything the extractor misses one week
disappears, a weekly slot filed as a dated one shows up as a removal plus an
addition, and the weekly change report is mostly that noise
(issue #77: 189 of 263 parishes "changed", +452 / −554 events).

This plan keeps a **believed schedule** per parish and changes it only through
recorded changes. The LLM is shown the believed schedule together with the
bulletin and answers with the **changes** it thinks the bulletin calls for. Every
call is stored with its model, prompt, schema and settings and the exact
schedule it was shown. Every change records the proposal and decision behind it.

Initial population of the schedules is out of scope: it happens by another
method (existing schedules, agent runs, manual review). This design only needs
it to write the first revision of each parish (`source_kind = 'seed'`), with
the date the seed is current as of.

The new tables arrive as an ordinary migration next to today's. Each parish
is in one of two modes: `extract` (today's from-scratch extraction) or
`update` (this plan). **Seeding a parish switches it**: a parish with a seed
revision is in update mode, and every other parish stays in extract mode. So
parishes move over one at a time or in batches, the easy ones first, and a
weekly run handles both kinds side by side. The old tables are dropped once
every parish has been seeded (see [Rollout](#rollout)).

## How a bulletin is processed (update mode)

```
believed schedule (parish @ revision N) ─┐
bulletin PDF                             ├─► llm_call ─► proposed_change ─► schedule_change ─► revision N+1
policy, schema, settings, date           ┘   (stored)    (stored, with       (the log)
                                                          its decision)
```

1. Fetch stores the bulletin, as today.
2. Render the parish's believed schedule into a canonical JSON **view**, and
   hash it.
3. Call the model with the policy prompt, the church list, the date, the view
   and the PDF. Store the call, whether or not it succeeds.
4. Store each proposed change, and where the bulletin prints each entry
   (its **sightings**).
5. The decision policy (code) decides each proposal at once: apply it or
   reject it. Nothing waits for a later bulletin.
6. Applied changes are appended to the change log as one new revision, and
   that revision is folded into the current schedule.

Steps 4 to 6 are one transaction: the proposals with their decisions, the
sightings, the revision, its log rows and the fold into `current_schedule`
are committed together or not at all. A crash before the commit leaves only
the stored call (step 3), which the next run reuses from the cache and
decides again; a crash after it leaves nothing to redo.

The change log is the source of truth. `current_schedule` is a materialized
view of it: the log replayed in order. Applying a revision appends to the log
and then folds that revision in; nothing else writes `current_schedule`, and a
full rebuild from the log must give the same table.

## Schema

The new `data/migrations/0004_schedule_state.sql`, in full. It adds tables
and one column, `church.retired_at` (see
[Churches leaving the CSV](#churches-leaving-the-csv)): `parish`, `bulletin`,
`event`, `event_occurrence` and the run tables are untouched, and nothing
writes the new tables for a parish in extract mode. The cleanup migration that
later drops the extract-mode tables is in [Rollout](#rollout).

```sql
-- Believed schedules: each parish's schedule kept as a log of changes, and the
-- LLM calls that propose them. Written only when the pipeline runs in update
-- mode (docs/schedule-state-plan.md).

-- A church that leaves churches.csv once it has schedule entries is retired,
-- not deleted: the log keeps pointing at its entries. Retired churches are
-- left out of the snapshot, the church list sent to the model, and the
-- churches a proposal may name.
ALTER TABLE church ADD COLUMN retired_at TEXT;

-- ── LLM calls ──

-- Text that shapes a call (the policy prompt, the response schema, the
-- context template), stored once by hash.
CREATE TABLE prompt_blob (
    hash TEXT PRIMARY KEY,            -- sha256 of text
    kind TEXT NOT NULL CHECK (kind IN ('policy', 'schema', 'context_template')),
    text TEXT NOT NULL
);

-- A believed schedule exactly as rendered for a call, stored once by hash: a
-- parish whose schedule did not change sends the same view again.
CREATE TABLE schedule_view (
    hash TEXT PRIMARY KEY,            -- sha256 of the canonical JSON
    json TEXT NOT NULL
);

CREATE TABLE llm_call (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT REFERENCES pipeline_run(id),
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    bulletin_id INTEGER NOT NULL REFERENCES bulletin(id) ON DELETE CASCADE,
    task TEXT NOT NULL CHECK (task IN ('schedule_update')),
    -- what was asked
    provider TEXT NOT NULL,           -- gemini | openai
    model TEXT NOT NULL,              -- as requested
    served_model TEXT,                -- as the API reported running it
    policy_hash TEXT NOT NULL REFERENCES prompt_blob(hash),
    schema_hash TEXT NOT NULL REFERENCES prompt_blob(hash),
    context_template_hash TEXT NOT NULL REFERENCES prompt_blob(hash),
    params_json TEXT NOT NULL,        -- reasoning effort, image detail, pdf_as_images, page limit, temperature...
    version TEXT NOT NULL,            -- digest of provider, model, the three hashes and params
    base_revision INTEGER NOT NULL,   -- the parish revision the view was rendered from
    view_hash TEXT NOT NULL REFERENCES schedule_view(hash),
    call_date TEXT NOT NULL,          -- the bulletin's fetch date, given to the model as "today"
    church_list_hash TEXT NOT NULL,   -- the parish's churches as sent
    request_key TEXT NOT NULL,        -- sha256(version, content_hash, view_hash, call_date, church_list_hash)
    -- what came back
    status TEXT NOT NULL CHECK (status IN ('ok', 'lenient', 'parse_failed', 'api_error')),
    error TEXT,
    response_key TEXT,                -- R2 key of the raw request and response
    published_date TEXT,              -- issue date the model read off the bulletin
    wrong_bulletin INTEGER CHECK (wrong_bulletin IN (0, 1)),
    church_list_needs_review INTEGER CHECK (church_list_needs_review IN (0, 1)),
    input_tokens INTEGER,
    cached_input_tokens INTEGER,
    output_tokens INTEGER,
    thinking_tokens INTEGER,
    cost_usd REAL,
    latency_ms INTEGER,
    started_at TEXT NOT NULL,
    finished_at TEXT
);
CREATE INDEX idx_llm_call_bulletin ON llm_call(bulletin_id);
CREATE INDEX idx_llm_call_parish ON llm_call(parish_id, id);
-- One answer per question: failed calls are kept, and a retry of one is a new row.
CREATE UNIQUE INDEX idx_llm_call_request ON llm_call(request_key)
    WHERE status IN ('ok', 'lenient');

-- ── The believed schedule ──

-- One schedule entry's content, written once and never changed. Identical
-- content is stored once (`hash`), so an entry's id names its content. The
-- log, the proposals and the current schedule all point at these rows, so the
-- columns and their checks are defined once.
CREATE TABLE schedule_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,        -- sha256 of every column below
    identity_key TEXT NOT NULL,       -- what makes two entries the same slot (below)
    -- Cascades only when the church's whole parish is removed: a church on its
    -- own is retired instead (church.retired_at).
    church_id INTEGER NOT NULL REFERENCES church(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL CHECK (event_type IN ('mass', 'confession', 'adoration')),
    event_kind TEXT NOT NULL CHECK (event_kind IN ('weekly', 'specific_date')),
    day_of_week TEXT CHECK (day_of_week IN
        ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    date TEXT,                        -- ISO date, specific_date only
    start_time INTEGER NOT NULL CHECK (start_time BETWEEN 0 AND 1439),
    end_time INTEGER CHECK (end_time IS NULL OR end_time BETWEEN 0 AND 1439),
    cancelled INTEGER NOT NULL DEFAULT 0 CHECK (cancelled IN (0, 1)),
    -- weeks of the month, as the labels' list: bit 0 first, 1 second, 2 third,
    -- 3 fourth, 4 fifth, 5 last. 0 = every week. Bit 6 (migration 0005, the
    -- labels' `exclude_weeks`): the listed weeks are the ones skipped.
    weeks_of_month INTEGER NOT NULL DEFAULT 0 CHECK (
        weeks_of_month BETWEEN 0 AND 127 AND weeks_of_month <> 64
    ),
    -- season, as the labels' object: months 1-12, days null or a day of that month
    season_start_month INTEGER CHECK (season_start_month BETWEEN 1 AND 12),
    season_start_day INTEGER CHECK (season_start_day BETWEEN 1 AND 31),
    season_end_month INTEGER CHECK (season_end_month BETWEEN 1 AND 12),
    season_end_day INTEGER CHECK (season_end_day BETWEEN 1 AND 31),
    note TEXT,
    CHECK ((event_kind = 'weekly' AND day_of_week IS NOT NULL AND date IS NULL)
        OR (event_kind = 'specific_date' AND date IS NOT NULL AND day_of_week IS NULL)),
    CHECK (event_kind = 'weekly' OR (weeks_of_month = 0 AND season_start_month IS NULL)),
    CHECK (event_kind = 'specific_date' OR cancelled = 0),
    CHECK ((season_start_month IS NULL) = (season_end_month IS NULL)),
    CHECK (season_start_day IS NULL OR season_start_month IS NOT NULL),
    CHECK (season_end_day IS NULL OR season_end_month IS NOT NULL)
);

-- Each parish's revisions. One revision per applied batch: a seed, one
-- llm_call's applied proposals, a person's edit, or the entries of a church
-- that left churches.csv or moved parish (`reference`).
CREATE TABLE schedule_revision (
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    revision INTEGER NOT NULL,        -- 1, 2, 3... per parish
    source_kind TEXT NOT NULL CHECK (source_kind IN ('seed', 'llm', 'human', 'reference')),
    llm_call_id INTEGER UNIQUE REFERENCES llm_call(id),   -- llm revisions
    run_id TEXT REFERENCES pipeline_run(id),
    actor TEXT,                       -- a person, or the seeding method
    note TEXT,
    -- seed revisions: the schedule reflects the bulletins fetched up to this
    -- time. Defaults to created_at. See "Which bulletins a parish processes".
    as_of TEXT,
    created_at TEXT NOT NULL,
    PRIMARY KEY (parish_id, revision),
    CHECK ((source_kind = 'seed') = (as_of IS NOT NULL))
);

-- What the model proposed, and what the policy did with it. Every proposal is
-- decided when its call is processed, so the decision lives on its own row.
CREATE TABLE proposed_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    llm_call_id INTEGER NOT NULL REFERENCES llm_call(id) ON DELETE CASCADE,
    seq INTEGER NOT NULL,             -- position in the model's answer; decided in this order
    op TEXT NOT NULL CHECK (op IN ('add', 'modify', 'delete')),
    raw_json TEXT NOT NULL,           -- the proposal as the model wrote it
    -- modify, delete: the entry id as the model gave it. Not a foreign key: it
    -- may name no entry, and is then rejected as unknown_item.
    target_entry_id INTEGER,
    -- add, modify: the whole new entry. Null when it could not be stored
    -- (unknown_church, invalid_entry).
    entry_id INTEGER REFERENCES schedule_entry(id),
    page_number INTEGER,
    rationale TEXT,
    decision TEXT NOT NULL CHECK (decision IN ('applied', 'rejected')),
    reason TEXT NOT NULL,             -- a code from the policy: 'auto', 'stale_bulletin', 'mass_delete', ...
    decided_by TEXT NOT NULL,         -- 'policy@<version>'
    UNIQUE (llm_call_id, seq),
    CHECK (decision = 'rejected'
        OR (op = 'add' AND target_entry_id IS NULL AND entry_id IS NOT NULL)
        OR (op = 'modify' AND target_entry_id IS NOT NULL AND entry_id IS NOT NULL)
        OR (op = 'delete' AND target_entry_id IS NOT NULL AND entry_id IS NULL))
);

-- The log. current_schedule is this replayed in order. Rows are only ever
-- appended.
CREATE TABLE schedule_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL,
    revision INTEGER NOT NULL,
    op TEXT NOT NULL CHECK (op IN ('add', 'modify', 'delete')),
    before_entry_id INTEGER REFERENCES schedule_entry(id),     -- null for add
    after_entry_id INTEGER REFERENCES schedule_entry(id),      -- null for delete
    -- The proposal this row carries out: an llm revision's applied one, or a
    -- rejected one a person applied by hand. Null otherwise.
    proposed_change_id INTEGER REFERENCES proposed_change(id),
    FOREIGN KEY (parish_id, revision) REFERENCES schedule_revision(parish_id, revision)
        ON DELETE CASCADE,
    CHECK ((op = 'add' AND before_entry_id IS NULL AND after_entry_id IS NOT NULL)
        OR (op = 'modify' AND before_entry_id IS NOT NULL AND after_entry_id IS NOT NULL)
        OR (op = 'delete' AND before_entry_id IS NOT NULL AND after_entry_id IS NULL))
);
CREATE INDEX idx_schedule_change_revision ON schedule_change(parish_id, revision);

-- The believed schedule now: schedule_change folded in order. Derived: written
-- only by folding a new revision in, and rebuildable from the log.
CREATE TABLE current_schedule (
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    entry_id INTEGER NOT NULL REFERENCES schedule_entry(id),
    identity_key TEXT NOT NULL,       -- copied from the entry, for the constraint below
    since_revision INTEGER NOT NULL,
    PRIMARY KEY (parish_id, entry_id),
    UNIQUE (parish_id, identity_key)  -- no two believed entries are the same slot
);

-- ── Where bulletins print entries ──

-- One row per entry per bulletin that prints it. Evidence, not schedule
-- content: sightings make no revisions, and no decision reads them. Written
-- for the entries a call lists in `seen`, for the new entry of each applied
-- add or modify, and by the seed method where it knows the bulletin.
CREATE TABLE entry_sighting (
    bulletin_id INTEGER NOT NULL REFERENCES bulletin(id) ON DELETE CASCADE,
    entry_id INTEGER NOT NULL REFERENCES schedule_entry(id),
    page_number INTEGER,              -- null when the source gave no page
    llm_call_id INTEGER REFERENCES llm_call(id) ON DELETE CASCADE,   -- null for seed sightings
    PRIMARY KEY (bulletin_id, entry_id)
);
CREATE INDEX idx_entry_sighting_entry ON entry_sighting(entry_id);
```

### Notes on the schema

**Entries are immutable.** A `schedule_entry` is one entry's content and is
never edited. A modify is a log row from the old entry to a new one, and the
current schedule swaps one for the other. Nothing points at an entry except
the log, the proposals, the sightings and `current_schedule`, so nothing can
be left pointing at a slot that has since changed. The price is that a slot has no single id
for its whole life: a modify gives it a new entry id. Nothing needs one (the
web app uses event ids as React list keys, in its map cache's change
signatures and as the last tie-break when sorting a schedule, all of which
only need them unique within a snapshot), and a slot's history is the chain
of its modify rows.

**Identity.** `identity_key` is computed in code from the entry:

- weekly: church, event type, weekday, start time
- specific_date: church, event type, date, start time

End time, weeks of month, season, cancelled and note are not part of identity,
so a change to any of them is a modify of the existing entry, and "every
Saturday 3 PM" and "first Saturday 3 PM" can't both be believed at once. The
`UNIQUE (parish_id, identity_key)` on `current_schedule` refuses a second live
entry for a slot, and the policy rejects a proposal that would create one as
`duplicate`.

A modify may change the start time, weekday or date as well, and so move the
entry to another slot ("the 5 PM vigil moves to 4:30" is one modify). It may
not change the church, event type or kind: the policy rejects that as
`invalid_modify`. A weekly entry turned into a dated one would otherwise
remove the weekly slot without counting as a delete.

**Weeks of the month and season** are structured as in the labels
(`labeling/labels.py`). The database stores `weeks_of_month` as a 6-bit mask,
plus a seventh bit for `exclude_weeks` ("every Sunday except the last" is
`["last"]` excluded, which no list of remaining weeks can say), always in
`labels.canonical_weeks`' form, and the season as four integer columns. The
view, the model's output and the snapshot use the labels' forms:
`["first", "third"]` with `exclude_weeks` false, and
`{"start_month": 5, "start_day": null, "end_month": 10, "end_day": null}`.
One converter, in one module, does the translation and is shared with the
labels code. The columns' checks only bound the days at 31; the entry checks
in code also hold each day to its month (`labels.DAYS_IN_MONTH`), and an entry
that fails them is rejected as `invalid_entry`.

**Cancellations** are specific_date entries with `cancelled = 1`, as in the
labels. Nothing stores which weekly slot one cancels: the snapshot builder
works it out each time (see [The snapshot](#the-snapshot-format-version-2)).
A cancelled one-off dated entry (a Christmas Mass called off) is that entry
modified to `cancelled = 1`, since `cancelled` is not part of identity.

**Dated entries expire on their own.** A specific_date entry dated before the
call date is left out of the view, and one dated before the snapshot's build
date is left out of the snapshot, with no revision. It is never deleted. That
keeps past dates out of the change log, which is where most of today's report
noise comes from.

**Page references are sightings.** A page number belongs to one bulletin,
not to an entry: an unchanged entry can move to another page, or not be
printed at all one week. So pages live on `entry_sighting`, keyed by bulletin
and entry, and never on `schedule_entry`.

- A call writes sightings when it succeeded and wasn't a wrong bulletin or
  stale, whatever the policy did with its proposals: one for each entry in its
  `seen` list that is live in its view (others are ignored), and one for the
  new entry of each applied add or modify, on the proposal's page. A second
  call on the same bulletin replaces the first's sightings.
- An entry with no sighting in a bulletin is still believed. Silence is not a
  change.
- A seeded or hand-edited entry has no sighting until a call lists it, unless
  the seed method knows its bulletin and page. A hand edit does not inherit the
  page of the entry it replaced: the edit may be because the bulletin changed.

**Changes take effect immediately.** There is no `valid_from`/`valid_until`.
The policy prompt says which changes to propose when (see
[Prompt rules](#prompt-rules)). Effective dates can be added later as columns
on `schedule_entry`.

### Churches leaving the CSV

`parish` and `church` are still seeded from the CSVs before every command
(`db.seed_reference_data`), and a parish removed from `parishes.csv` is still
deleted with everything under it, its schedule log included. A church is
different: its entries are referenced by its parish's log, which is never
rewritten, so it can't simply be deleted. When a church leaves
`churches.csv`, or names another parish:

1. If it has live entries, the seeding appends one `reference` revision to its
   (old) parish deleting them, with `actor = 'churches.csv'`. A moved church's
   entries are not carried to its new parish: they are seeded there like any
   other parish's.
2. A church that leaves the CSV and has ever had a `schedule_entry` gets
   `retired_at` set instead of being deleted. One without entries is deleted,
   as today. A retired church that comes back to the CSV (matched by slug, as
   now) has `retired_at` cleared and keeps its id; its schedule starts empty
   and is seeded.

Both happen in the same transaction as the rest of the seeding. Retired
churches are left out wherever churches are listed: the snapshot, the church
list sent to the model (`church_list_for_prompt`), and the churches a proposal
may name (`unknown_church`).

## The model's input and output

### Input: the view

The canonical JSON of the parish's current schedule, with dated entries before
the call date left out. Keys are sorted, entries ordered by church, kind,
weekday or date, then time, and there is no whitespace, so the same schedule
always hashes the same. `id` is the entry id:

```json
{"churches":[{"slug":"st-mary-albany","entries":[
  {"id":118,"event_type":"mass","event_kind":"weekly","day_of_week":"Sunday",
   "start_time":"9:00 AM","end_time":null,"weeks_of_month":[],"season":null,"note":null},
  {"id":131,"event_type":"confession","event_kind":"weekly","day_of_week":"Saturday",
   "start_time":"3:00 PM","end_time":"3:45 PM","weeks_of_month":["first"],"season":null,"note":null},
  {"id":140,"event_type":"mass","event_kind":"specific_date","date":"2026-10-14",
   "start_time":"7:00 AM","end_time":null,"cancelled":true,"note":null}
]}]}
```

The church list (slugs, names, addresses) goes in as context, as today, and
`church_list_hash` records which list was sent. The call date is the
bulletin's fetch date, so a replay of the same bulletin asks exactly the same
question and is served from the cache.

### Output

```json
{
  "published_date": "2026-10-11",
  "wrong_bulletin": false,
  "church_list_needs_review": false,
  "seen": [{"entry_id": 118, "page_number": 2}],
  "changes": [
    {"op": "modify", "entry_id": 131,
     "entry": {"event_type":"confession","event_kind":"weekly","church_slug":"st-mary-albany",
               "day_of_week":"Saturday","start_time":"3:00 PM","end_time":"4:00 PM",
               "weeks_of_month":["first"],"season":null,"note":null},
     "page_number": 2, "rationale": "End time changed from 3:45 to 4:00."},
    {"op": "add", "entry": {...}, "page_number": 3, "rationale": "..."},
    {"op": "delete", "entry_id": 140, "page_number": 1, "rationale": "..."}
  ]
}
```

- **add** and **modify** carry the whole new entry, not a patch. The model does
  not have to express "clear the end time", and code works out which fields
  changed.
- **`entry_id`** is an `id` from the view. It is stored as the proposal's
  `target_entry_id`.
- **`seen`** lists the entries from the view that the bulletin prints and the
  call does not change, each with its page. They become sightings.

### Prompt rules

The policy prompt tells the model:

- **Silence is not a change.** An entry the bulletin doesn't mention stays.
  Propose a delete only when the bulletin says the entry is discontinued, or
  prints what is clearly the full schedule for that church and event type
  without it.
- **Weekly changes wait until they are in effect.** Propose a change to a
  weekly entry only when it is already in effect in the bulletin's week. An
  announced future change ("from November 1 the vigil moves to 5 PM") waits
  for a bulletin from a week where it is in effect.
- **Dated entries don't wait.** Propose dated entries (holy days, Christmas,
  Holy Week, one-off events) and cancellations for any date from today on.
- **Cancelling a weekly slot** is an add of a dated entry with
  `cancelled: true` for the same church, event type and start time on that
  date. Cancelling a dated entry is a modify of it.
- **Seasons.** Put a season on both sets of entries only when the bulletin
  gives both schedules with their date ranges ("Summer, June–August: …;
  September–May: …"). Otherwise replace the weekly entries outright, and
  replace them back when the regular schedule returns.
- **Modify, not delete + add,** for a change to an existing entry (time, end
  time, weeks, season, note). Delete + add only when one entry is replaced by
  a different one. Nothing breaks if the model gets this wrong; it only makes
  the report read better. A modify never changes an entry's church, event
  type or kind: cancel a weekly slot with a dated add, as above.
- **List in `seen`** every entry from the view that the bulletin prints and
  you don't change, with the page it is printed on. An entry you change
  carries its page on the change instead.
- Refer to existing entries only by the ids in the view.

## Decision policy (v1)

The policy is code. Its version is recorded in every proposal's `decided_by`.
Every proposal is decided when its call is processed: applied or rejected.
Nothing is held for a later bulletin or a person; a person can still apply a
rejected proposal afterwards (see [Hand edits](#hand-edits)). A call that
fails (`parse_failed`, `api_error`) stores no proposals.

**The whole call** is rejected, every proposal with the same reason, when:

| Condition | Reason |
|---|---|
| the call says `wrong_bulletin` | `wrong_bulletin` |
| the bulletin's week is older than the parish's high-water mark (below) | `stale_bulletin` |
| it deletes at least 3 weekly entries, and more than half the parish's live weekly entries | `mass_delete` |

Otherwise each proposal is decided in `seq` order, against the schedule as the
proposals before it left it, and is **rejected** when:

| Condition | Reason |
|---|---|
| its entry names a church outside the parish | `unknown_church` |
| its entry fails the entry checks (a weekly entry with a date, say) | `invalid_entry` |
| it is a modify that changes its target's church, event type or kind | `invalid_modify` |
| it is an add or modify of a dated entry before the call date | `past_date` |
| its target isn't a live entry of the parish (including one an earlier proposal in the call already changed) | `unknown_item` |
| it would create a second live entry for a slot | `duplicate` |

Every other proposal is **applied** (`auto`): adds, modifies and deletes,
weekly or dated. A call with no applied proposals writes no revision.

### Which week a bulletin is for

A call's week is `bulletin_week` of the `published_date` it read, with the
existing cap on dates implausibly far past the fetch. A bulletin is **undated**
when the model read no date or an implausible one.

- The parish's **high-water mark** is the newest week among its earlier calls
  that succeeded, weren't a wrong bulletin or stale, and were dated, whether or
  not they applied anything. A bulletin that confirms the schedule is as
  current as one that changes it. The seed counts too: the mark is never
  older than the week of the parish's newest dated bulletin (not a wrong
  bulletin) fetched on or before its latest seed's `as_of`, since the seed is
  as current as that. So an old issue a site falls back to in the parish's
  first update-mode week is stale.
- **Older than the mark:** the call is rejected as `stale_bulletin`.
- **Same week as the mark:** applied. The 2nd bulletin for a week is noted in
  the report as a correction, and a 3rd or later is flagged, as today
  (`bulletin_week.place_bulletin`).
- **Undated:** applied, flagged in the report, and it doesn't move the mark:
  its week would only be a guess from the fetch date, and a wrong guess would
  make the next dated bulletin look stale. The cost is that an old issue with
  no readable date is applied like a current one; the flag is how it is
  seen, and a hand edit undoes it.

### Base revision

A call is shown the parish's current schedule and its proposals are applied
straight after, so before applying, the schedule must still render to the
call's `view_hash`. A mismatch is a bug, not a disagreement between bulletins:
the parish fails with an error in `run_parish_result` and nothing is applied.

### Hand edits

A small command writes `human` revisions, so a person can act on what the
policy rejected or the report flagged:

- **apply** a rejected call's proposals, all of them or chosen `seq`s. Each
  is checked against the current schedule with the per-proposal rules above
  (the whole-call rules are what the person is overriding), and any that fail
  are reported and skipped. The log rows carry the `proposed_change_id` they
  apply; the proposals' own decisions stay as the policy made them.
- **add**, **modify** or **delete** entries directly, with the same checks.

`actor` is the person, `note` says why. The command runs against the local
database, which is published as it is today. An editing interface is out of
scope.

## The report

The report has a section for each mode. Extract-mode parishes are reported as
today. For update-mode parishes, `report.py` reports from the run's
`proposed_change` rows, per parish:

- **Applied changes**, each with its page number and rationale. A modify shows
  before → after. A delete and an add of the same church, event type and
  weekday in one call are shown side by side.
- **Flags**, which don't block anything:
  - a parish whose schedule changed in each of its last 3 calls;
  - an undated bulletin;
  - a 3rd or later bulletin for one week (a 2nd is noted as a correction);
  - a live weekly entry that none of the parish's last 4 bulletins since it
    became live has printed (no sighting): still believed, but possibly gone.
    This leans on the model listing everything it sees in `seen`, so a model
    that skimps on the list makes the flag noisy, not the schedule wrong;
  - `church_list_needs_review`, as today.
- **Rejections:** counts by reason in the summary, and the proposals of every
  `mass_delete` and `stale_bulletin` call listed in full.

An update-mode parish no longer holds the run for its schedule changes: the
per-parish checks (a parish dropping to zero events, say) apply only to
extract-mode parishes, and `mass_delete` takes their place. The run-level
checks stay: more than half the parishes failed to fetch, a stage crashed, or
`verify_frontend_snapshot` fails, with its thresholds as today (church count,
±10% events, 90% of weekly slots kept). They compare the whole snapshot, so a
run right after a large batch of parishes was seeded compares the seeded
schedules with those parishes' last extracted ones and may be held; it is
approved by hand, or the batch is made smaller.

## Processing order

The process stage splits the run's parishes by mode. Extract-mode parishes go
through today's extraction, unchanged. Update-mode parishes go through the
steps above.

### Which bulletins a parish processes

An update-mode parish's bulletins are called when they were **fetched after
its latest seed's `as_of`** and have **no successful call yet**. Everything
fetched on or before `as_of` is taken to be in the seed, and is never called,
so switching a parish does not work through its past bulletins:

- A seed written from the current state leaves `as_of` at its creation time.
  The parish's first update-mode run calls only the bulletins fetched in that
  run, usually one.
- A seed built from an older bulletin sets `as_of` to that bulletin's fetch
  time, and the parish's first run catches up on the few issues fetched since,
  once.

Update mode goes by its own calls, not `bulletin.processed_at`, so what extract
mode did with a parish's bulletins before its seed doesn't matter. It still
writes `published_date`, `wrong_bulletin` and `processed_at` on the bulletins
it calls, which fetch and the snapshot read.

- **Sequential within a parish, parallel across parishes.** Each call reads the
  schedule the previous call left. Run concurrency stays per parish, as now.
- **In fetch order.** Today only each parish's newest fetched bulletin is
  extracted (`runner.latest_per_parish`), and an issue superseded before its
  run is skipped. Update mode calls each qualifying bulletin in fetch order,
  since any of them may change the schedule; in a normal week that is one per
  parish, sometimes two. A site's fallback to an old issue is still called
  (the date is only known after the model reads it), but its changes are
  rejected as `stale_bulletin`.
- **A failed call** (`parse_failed`, `api_error`) leaves its bulletin with no
  successful call, so the next run tries it again. Newer bulletins don't wait
  for it: once one of them has succeeded, the retry is usually older than the
  mark and rejected as stale, which is right, since the newer bulletin
  already spoke for that week. A bulletin whose call has failed in 3 runs is
  no longer retried, and the report says so.
- **No parish is bootstrapped** by showing the model an empty schedule: a
  parish without a seed is in extract mode.
- **Caching:** `request_key` is unique among successful calls; a failed call
  is kept, and its retry is a new row. Re-running the same bulletin against the
  same view, version, date and church list reuses the stored call instead of
  calling the API, both after a crash and in replays. A call whose proposals
  are already decided is not applied again. The raw response is in R2 under
  `llm/calls/<request_key>.json`, so a fresh database can reuse it too.

## The snapshot (format version 2)

Version 2 ships first, written while every parish is still in extract mode,
so seeding parishes changes no frontend code. It is version 2 because a weekly row with
`weeks_of_month = ["first"]` would otherwise be read as every week.

- **Kept columns:** `id`, `church_id`, `event_type`, `event_kind`,
  `day_of_week`, `date`, `start_time`, `end_time`, `cancelled`, `note`,
  `page_number`.
- **New:** `weeks_of_month`, `season_start_month`, `season_start_day`,
  `season_end_month`, `season_end_day`, `cancels_event_id`.
- **Dated entries** before the build date are left out.
- **`cancels_event_id`:** a cancelled dated entry cancels the live weekly entry
  with the same church, event type and start time on its date's weekday. The
  builder matches them on every build and writes that entry's id. After the
  identity rules there is at most one match. A cancellation that matches
  nothing is left out of the snapshot, as cancelled events are hidden today.
- **Reading version 1:** `read_snapshot` also reads a version 1 snapshot, as
  every week, no season and no cancellations, so the first v2 run's
  `verify_frontend_snapshot` can compare against the v1 snapshot before it.
  The app reads only version 2.

Each parish's rows and its churches' bulletin columns come from its own mode,
so one snapshot holds both kinds:

| | extract mode | update mode |
|---|---|---|
| rows | each parish's current bulletin's `event` rows, as today | `current_schedule` joined to `schedule_entry` |
| `id` | event id | minus the entry id |
| `weeks_of_month`, season | every week, no season | from the entry |
| `page_number` | from the event | the entry's sighting in the church's current bulletin (the one `bulletin_url` opens); null when that bulletin doesn't print it |
| `bulletin_url`, `bulletin_week` per church | as today | the newest bulletin whose call succeeded and wasn't a wrong bulletin or stale |

Event ids and entry ids are counted separately and would collide in one
snapshot, so entry ids are written negated (entry 118 is `-118`, in `id` and
in `cancels_event_id`). The app only needs ids unique within a snapshot, and
the sign says where a row came from when debugging. The id column's delta
encoding still works, since rows stay sorted by id.

A page link always opens the current bulletin, so a page from an older
bulletin is never shown: parish sites often serve a new PDF at the same
address, so an old issue's address can't be trusted to open that issue. An
entry with no page simply shows no link, and the section's "Found on bulletin
page N" is worked out from the entries that have one, as today. The frontend
needs no change for this.

`computeNextOccurrence` needs:

- the weeks-of-month and season rules;
- skipping a weekly entry's date when a cancellation names it.

## What changes in the code

| Area | Change |
|---|---|
| `data/migrations/` | `0004_schedule_state.sql` adds the tables above and `church.retired_at`. The cleanup migration comes later (see [Rollout](#rollout)) |
| `db.py`, `storage.py` | seeding retires a church with entries instead of deleting it, and writes the `reference` revision (see [Churches leaving the CSV](#churches-leaving-the-csv)); church lists leave retired churches out |
| `weekly.py`, `__main__.py` | the run passes each parish to its mode's process stage, report section and snapshot source. `__main__.py` also gains the hand-edit command. No setting or workflow variable: a parish's mode is whether it has a seed |
| `process.py` | splits parishes by mode. Update mode: each bulletin fetched after the seed's `as_of` with no successful call, in fetch order; render the view, call, store the call, then decide, apply and store sightings in one transaction. Extract mode as today, for the parishes without a seed |
| new `schedule/` package | the view renderer, entry hashing and identity, the policy, apply and fold (and a full rebuild from the log), hand edits, the converters for weeks of month and season |
| `classifiers/` | a `schedule_update` task: new policy prompt and response schema; version digest covers both; returns token usage and served model |
| `schedule_extraction.py` | unchanged: the from-scratch extraction serves extract mode and the evals |
| `bulletin_week.py`, `fetch.py` | unchanged while both modes exist: update mode also writes the bulletin's `published_date`, `wrong_bulletin` and `processed_at`, as extract mode does |
| `report.py`, `verify_frontend_snapshot.py` | a section per mode; update-mode parishes are reported from `proposed_change`, as in [The report](#the-report); the remaining run-level checks; verification reads a v1 previous snapshot |
| `extract_frontend_db.py`, `apps/web` | snapshot v2 with each parish's rows from its own mode, entry ids negated, and the cancellation matching; `computeNextOccurrence` rules |
| `labeling/bulletins.py` | for an update-mode parish, the read-only "model's answer" becomes the call's view with its applied proposals |

## Rollout

The work merges in small pieces. Until a parish is seeded, nothing about it
changes, so everything up to the first seed ships with every parish in
extract mode.

1. **Migration 0004 and the `schedule/` package** land. No parish has a seed,
   so nothing writes the new tables yet.
2. **Snapshot v2 and the frontend** ship, built from `event` with every
   parish in extract mode, and with the update-mode rows ready for when the
   first parish is seeded.
3. **Seed parishes in batches**, the easy ones first. Each parish's first
   `seed` revision is loaded into the published database by the out-of-scope
   method, with its `as_of` and with sightings where it knows the bulletin and
   page an entry came from. That parish is in update mode from the next weekly
   run. The harder parishes stay in extract mode for as long as they need. A
   later seed for a parish that already has one is a new `seed` revision of
   adds, modifies and deletes, like any other, with its own `as_of`.
4. **There is no switching a parish back** to extract mode. Removing its
   seed would mean rewriting the log, and extract mode's snapshot reads the
   `event` rows of the parish's newest processed bulletin, which a bulletin
   update mode processed doesn't have, so the parish would show nothing until
   its next new bulletin. A problem after seeding is fixed forward, with hand
   edits or a new `seed` revision.
5. **Cleanup,** once every parish is seeded and update mode has settled: a
   migration drops `event`, `event_occurrence`, `idx_bulletin_parish_processed`
   and the bulletin's `published_date`, `wrong_bulletin` and `processed_at`,
   and adds the view below for the readers of those columns. Extract mode and `recurrence.py`
   go; the from-scratch extraction stays for the evals.

```sql
-- What fetch and bulletin_week.py read in place of the dropped bulletin
-- columns: each bulletin with its latest successful read.
CREATE VIEW bulletin_reading AS
SELECT b.*,
       c.id AS llm_call_id,
       c.published_date,
       COALESCE(c.wrong_bulletin, 0) AS wrong_bulletin,
       c.finished_at AS processed_at
FROM bulletin b
LEFT JOIN llm_call c ON c.id = (
    SELECT id FROM llm_call
    WHERE bulletin_id = b.id AND status IN ('ok', 'lenient')
    ORDER BY id DESC LIMIT 1
);
```

## Out of scope

- Initial population of schedules (the `seed` revisions).
- Running a parish in both modes, or in update mode in shadow.
- Validating the update calls (eval cases, replays of past bulletins). That
  is separate work.
- Changes effective from a future date (`valid_from` / `valid_until`).
- Holding doubtful changes for corroboration by a later bulletin or for a
  person's review. Everything applies or is rejected at once in v1.
- Showing on the site that an entry isn't in this week's bulletin, or when it
  was last printed. Sightings hold the data for it.
- An interface for editing schedules beyond the hand-edit command.
- Periodic from-scratch audit calls to catch errors the update calls anchor on.
  This is a second `llm_call.task` when it comes.
- Tally corrections as `human` revisions.

## Implementation decisions

Decisions made while implementing this plan, where it was silent or where the
code departs from it.

### Storing calls

- **A successful call's row is written with its decisions.** Step 3 stores the
  raw request and reply in the blob store (`llm/calls/<request_key>.json`) as
  soon as the reply arrives, and a failed call's `llm_call` row at once. A
  successful call's `llm_call` row is inserted in the step 4 to 6 transaction.
  Otherwise a crash between the two would leave a successful call that was
  never decided, and "no successful call yet" would never pick its bulletin
  again. The stored reply is what the next run reuses: it finds it by request
  key and decides it without calling the API.
- **A reply that couldn't be read isn't reused.** It is kept in the blob store
  for debugging, but a retry calls the model again.
- **The same PDF is called once per parish.** A bulletin is not called when
  another bulletin of the parish with the same `content_hash` already has a
  successful call: there is nothing new in it, and with an unchanged view its
  request key would collide with the first call's.
- **One provider: gpt-6-luna.** `OpenAIScheduleUpdater` (in
  `classifiers/schedule_update.py`) runs every update call on `gpt-6-luna`
  through the OpenAI Responses API, set up as the eval module's `gpt-6-luna`
  classifier is: high reasoning effort, the PDF at low detail, and strict
  decoding of the response schema, so `params_json` is
  `{"file_detail":"low","reasoning_effort":"high","strict":true}`. The process
  stage's `--model` picks only the extract-mode Gemini model. The policy is a
  developer message marked as an explicit prompt-cache breakpoint, then the
  church list, the date and the view, then the PDF. It carries every rule of
  the eval policy (`classifiers/schedule_policy.py`: chapels and adoration
  chapels, weekly vs dated, dates, exclusions as the weeks that remain, times,
  notes and the final source checks), worded for changes, and the response
  schema's qualifier and note descriptions are the eval schema's.
- **Update calls run at the flex tier.** Each call asks for
  `service_tier: "flex"`, half the standard price. The trade-off is slower
  replies (the client timeout is 15 minutes) and, at times, no flex capacity.
  That shows up as a 429, a 5xx, or a response that was accepted and then
  ends `failed` with a `server_error` and no output. Once the client's
  retries are spent, such a call is asked again at the standard tier, so a
  busy week costs more instead of failing.
  The tier isn't in `params_json`: it changes neither the request's content
  nor the reply, so leaving it out keeps request keys, and with them stored
  replies, unchanged. The stored call record has the tier the response
  reports in `service_tier`, and `cost_usd` uses that tier's price.

### Deciding

- **`no_change`** is an extra per-proposal rejection reason: a modify whose new
  entry is exactly its target. It would otherwise write a revision that changes
  nothing.
- **Staleness is worked out, not stored.** `schedule/history.py` replays a
  parish's successful calls in order and places each against the mark as it
  stood then. Each call is placed against the seed it was made under (the
  latest seed at or before its `base_revision`), so a later seed doesn't make
  an earlier call look stale. A call is undated when it read no date, or one
  more than 21 days after the fetch (the existing cap). Mass deletes count the
  distinct live weekly entries a call's deletes name; modifies don't count.
- **The seed's bulletin counts as its week's first.** A seed's newest dated
  bulletin counts as the first bulletin for its week. The first update call
  for that week is therefore noted as a correction.
- **A call can only change what it was shown.** A modify or delete naming a
  live entry that wasn't in the call's view is `unknown_item`. That covers a
  dated entry already past, which stays out of the log as the plan says. Hand
  edits may name any live entry.
- **`seq` is the position in the model's answer.** It counts any change that
  was dropped because it had no known `op`. A lenient reply's `seen` or
  `changes` that isn't a list reads as empty. Its flags are true only for
  `true` or `"true"`.
- **A dated entry may repeat its own weekday.** Models often give
  `day_of_week` alongside `date`. When it agrees with the date it is dropped;
  when it disagrees the entry is `invalid_entry`.
- **Hand edits re-read the proposal.** `schedule apply` checks each proposal's
  entry as the model wrote it, so one rejected as `unknown_church` can be
  applied once the church is in `churches.csv`.
- **Hand edits need an update-mode parish.** `schedule add`, `modify`, `delete`
  and `apply` refuse a parish without a seed, so the new tables stay empty
  for extract-mode parishes. `schedule seed` is how a parish gets one.
- **One failed parish doesn't stop the stage.** An error while deciding a
  call rolls back that call's transaction. The parish is recorded as `failed`
  for the run, and the other parishes go on.

### Seeds and churches

- **`as_of` is normalised.** It is stored in the same form as `fetched_at`
  (`YYYY-MM-DDTHH:MM:SSZ`), because the two are compared as text. A date with
  no time means the end of that day, so everything fetched that day is in the
  seed.
- **A parish can still be deleted after a church moved into it.** If a church
  moved from parish A to parish B, A's log, proposals and sightings still name
  its entries. Deleting B would delete those entries by cascade, from under
  A's rows. So before B is deleted, any of its churches another parish still
  names are moved back to that parish and retired. That counts as a retirement
  in the run's CSV check.
- **The qualifier converters are shared through their constants.** The labels
  only validate the list and object forms and never convert them, so
  `schedule/qualifiers.py` is the one converter. It is built on the labels'
  `WEEKS_OF_MONTH`, `SEASON_KEYS` and `DAYS_IN_MONTH`.

### Runs and the report

- **One run result per parish.** `run_parish_result` holds one row per parish
  and stage, so when a parish has several bulletins in a run its row has the
  most notable outcome and every call's detail. The new outcomes are
  `updated`, `no_change`, `stale_bulletin`, `mass_delete`, `undated` and
  `gave_up`. Its `event_count` is the number of live entries.
- **The change diff leaves out update-mode parishes.** Any parish in update
  mode in either database is left out of the extract-mode diff, so it can't be
  counted as dropping to zero. A church retired from the CSV holds the run the
  same way a deleted one does.
- **The "not printed" flag** counts only the calls that were shown the entry
  (base revision at or after the entry's `since_revision`) and weren't a wrong
  bulletin or stale.

### Snapshot and site

- **Current bulletin.** An update-mode parish's `bulletin_url` and
  `bulletin_week` use the same ordering as extract mode over its processed
  bulletins, since update mode writes `processed_at`, `published_date` and
  `wrong_bulletin` on the bulletins it calls. That is the newest bulletin whose
  call succeeded and wasn't a wrong bulletin or stale (a stale one is older
  than the mark by definition). A parish seeded but not yet called keeps
  showing its last extract-mode bulletin rather than none.
- **One snapshot rule for both modes.** Dated rows before the build date are
  left out, and cancellations are matched to weekly rows, for extract-mode
  rows too. A cancellation matching nothing is left out in both modes; where an
  extract-mode bulletin repeats a weekly slot, the lowest id is named.
- **`weeks_of_month`** is a plain list column in the snapshot, and
  **`exclude_weeks`** a boolean one, added later to version 2 (a snapshot
  without it reads as false).
- **The site shows the qualifiers as PR 22 did.** The web app follows PR 22
  (lyonsl2/project-carlo#22, and the PRD on its branch) for how the
  qualifiers are shown, in `apps/web/src/lib/schedulePattern.ts`:
  - The copy is long form, at the grain the bulletin gave: "First Friday of
    the month", "Second and fourth Saturdays of the month", "October through
    June", "June 4 through September 10", joined with a comma when a slot has
    both. `schedule/qualifiers.describe_schedule_pattern` words the report's
    entries the same way.
  - The church page lists every weekly slot, in season or not, with the
    qualifier beside the time in the same italic annotation as the note
    ("First Friday of the month · Benediction").
  - The map and its filters hide a weekly slot that is out of season today.
    Monthly slots stay, since they do run at this time of year.
  - The map popup and the city summary give a slot that isn't every week its
    own row, with the qualifier as a line under it, so a first-Friday devotion
    is never folded into an every-Friday Mass. Popup dedup keys include the
    pattern. The city summary folds a run of days only when they keep the same
    pattern and it has no weeks of the month.
  - The next occurrence is looked for up to seven years ahead, so a slot whose
    weeks and season rarely meet is still found.

### Commands

- `pnpm schedule show|apply|add|modify|delete|seed|rebuild` is the hand-edit
  command. `seed` loads a JSON list of entries as a seed revision. It is a thin
  loader for whatever method builds the seeds, which is still out of scope.
  `rebuild` replays the log into `current_schedule` and reports any rows that
  differed.
- The labeler shows an update-mode bulletin's answer as the call's view with
  its applied proposals made, marked `update`.

### Rollout

Rollout steps 1 and 2 land together: the migration, the `schedule/` package,
update mode, and snapshot v2 with the frontend. No parish has a seed yet, so
the pipeline behaves as before, except that the snapshot is version 2. Version
2 leaves out past dated rows and cancellations that match no weekly row, which
the site was hiding anyway.

### Follow-ups

- `dioceses/records._referenced_by_events` still only looks at `event` rows
  when warning that a promotion would drop data. It doesn't yet look at
  believed-schedule entries.
