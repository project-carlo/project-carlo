# Project Carlo: believed schedules updated by proposed changes

Status: proposal, for review. Nothing here is implemented.

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
it to write the first revision of each parish (`source_kind = 'seed'`).

The new tables arrive as an ordinary migration next to today's, and the
pipeline gains a mode: `extract` (today's from-scratch extraction) or `update`
(this plan). A weekly run uses one mode or the other, never both. The old
tables are dropped once update mode has settled (see [Rollout](#rollout)).

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
4. Store each proposed change.
5. The decision policy (code) decides each proposal at once: apply it or
   reject it. Nothing waits for a later bulletin.
6. Applied changes are appended to the change log as one new revision, and
   that revision is folded into the current schedule.

The change log is the source of truth. `current_schedule` is a materialized
view of it: the log replayed in order. Applying a revision appends to the log
and then folds that revision in; nothing else writes `current_schedule`, and a
full rebuild from the log must give the same table.

## Schema

The new `data/migrations/0004_schedule_state.sql`, in full. It only adds
tables: `parish`, `church`, `bulletin`, `event`, `event_occurrence` and the run
tables are untouched, and nothing writes the new tables in extract mode. The
cleanup migration that later drops the extract-mode tables is in
[Rollout](#rollout).

```sql
-- Believed schedules: each parish's schedule kept as a log of changes, and the
-- LLM calls that propose them. Written only when the pipeline runs in update
-- mode (docs/schedule-state-plan.md).

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
    request_key TEXT NOT NULL UNIQUE, -- sha256(version, content_hash, view_hash, call_date, church_list_hash)
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

-- ── The believed schedule ──

-- One schedule entry's content, written once and never changed. Identical
-- content is stored once (`hash`), so an entry's id names its content. The
-- log, the proposals and the current schedule all point at these rows, so the
-- columns and their checks are defined once.
CREATE TABLE schedule_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash TEXT NOT NULL UNIQUE,        -- sha256 of every column below
    identity_key TEXT NOT NULL,       -- what makes two entries the same slot (below)
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
    -- 3 fourth, 4 fifth, 5 last. 0 = every week.
    weeks_of_month INTEGER NOT NULL DEFAULT 0 CHECK (weeks_of_month BETWEEN 0 AND 63),
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
-- llm_call's applied proposals, or a person's edit.
CREATE TABLE schedule_revision (
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    revision INTEGER NOT NULL,        -- 1, 2, 3... per parish
    source_kind TEXT NOT NULL CHECK (source_kind IN ('seed', 'llm', 'human')),
    llm_call_id INTEGER REFERENCES llm_call(id),   -- llm revisions
    run_id TEXT REFERENCES pipeline_run(id),
    actor TEXT,                       -- a person, or the seeding method
    note TEXT,
    created_at TEXT NOT NULL,
    PRIMARY KEY (parish_id, revision)
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
    proposed_change_id INTEGER REFERENCES proposed_change(id), -- null for seed and human
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
```

### Notes on the schema

**Entries are immutable.** A `schedule_entry` is one entry's content and is
never edited. A modify is a log row from the old entry to a new one, and the
current schedule swaps one for the other. Nothing points at an entry except
the log, the proposals and `current_schedule`, so nothing can be left pointing
at a slot that has since changed. The price is that a slot has no single id
for its whole life: a modify gives it a new entry id. Nothing needs one (the
web app uses event ids only as React list keys), and a slot's history is the
chain of its modify rows.

**Identity.** `identity_key` is computed in code from the entry:

- weekly: church, event type, weekday, start time
- specific_date: church, event type, date, start time

End time, weeks of month, season, cancelled and note are not part of identity,
so a change to any of them is a modify of the existing entry, and "every
Saturday 3 PM" and "first Saturday 3 PM" can't both be believed at once. The
`UNIQUE (parish_id, identity_key)` on `current_schedule` refuses a second live
entry for a slot, and the policy rejects a proposal that would create one as
`duplicate`.

**Weeks of the month and season** are structured as in the labels
(`labeling/labels.py`). The database stores `weeks_of_month` as a 6-bit mask
and the season as four integer columns. The view, the model's output and the
snapshot use the labels' forms: `["first", "third"]` and
`{"start_month": 5, "start_day": null, "end_month": 10, "end_day": null}`.
One converter, in one module, does the translation and is shared with the
labels code.

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

**Changes take effect immediately.** There is no `valid_from`/`valid_until`.
The policy prompt says which changes to propose when (see
[Prompt rules](#prompt-rules)). Effective dates can be added later as columns
on `schedule_entry`.

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
  the report read better.
- Refer to existing entries only by the ids in the view.

## Decision policy (v1)

The policy is code. Its version is recorded in every proposal's `decided_by`.
Every proposal is decided when its call is processed: applied or rejected.
Nothing is held for a later bulletin or a person. A call that fails
(`parse_failed`, `api_error`) stores no proposals.

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
  current as one that changes it.
- **Older than the mark:** the call is rejected as `stale_bulletin`.
- **Same week as the mark:** applied. The 2nd bulletin for a week is noted in
  the report as a correction, and a 3rd or later is flagged, as today
  (`bulletin_week.place_bulletin`).
- **Undated:** applied, flagged in the report, and it doesn't move the mark:
  its week would only be a guess from the fetch date, and a wrong guess would
  make the next dated bulletin look stale.

### Base revision

A call is shown the parish's current schedule and its proposals are applied
straight after, so before applying, the schedule must still render to the
call's `view_hash`. A mismatch is a bug, not a disagreement between bulletins:
the parish fails with an error in `run_parish_result` and nothing is applied.

## The report (update mode)

`report.py` reports from the run's `proposed_change` rows, per parish:

- **Applied changes**, each with its page number and rationale. A modify shows
  before → after. A delete and an add of the same church, event type and
  weekday in one call are shown side by side.
- **Flags**, which don't block anything:
  - a parish whose schedule changed in each of its last 3 calls;
  - an undated bulletin;
  - a 3rd or later bulletin for one week (a 2nd is noted as a correction);
  - `church_list_needs_review`, as today.
- **Rejections:** counts by reason in the summary, and the proposals of every
  `mass_delete` and `stale_bulletin` call listed in full.

A run is no longer held for schedule changes. The run-level checks that remain
concern the run itself: more than half the parishes failed to fetch, a stage
crashed, or the snapshot fails to verify.

## Processing order

- **Sequential within a parish, parallel across parishes.** Each call reads the
  schedule the previous call left. Run concurrency stays per parish, as now.
- **New bulletins for one parish** are processed in order of fetch time. A
  site's fallback to an old issue is still called (the date is only known
  after the model reads it), but its changes are rejected as `stale_bulletin`.
- **A parish with no revision yet is skipped**, reported as `unseeded`. It
  is never bootstrapped by showing the model an empty schedule.
- **Caching:** `request_key` is unique. Re-running the same bulletin against the
  same view, version, date and church list reuses the stored call instead of
  calling the API, both after a crash and in replays. A call whose proposals
  are already decided is not applied again. The raw response is in R2 under
  `llm/calls/<request_key>.json`, so a fresh database can reuse it too.

## The snapshot (format version 2)

Version 2 ships first, written by extract mode, so the cutover to update mode
changes no frontend code. It is version 2 because a weekly row with
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

In each mode:

| | extract mode | update mode |
|---|---|---|
| rows | each parish's current bulletin's `event` rows, as today | `current_schedule` joined to `schedule_entry` |
| `id` | event id | entry id |
| `weeks_of_month`, season | every week, no season | from the entry |
| `page_number` | from the event | from the proposal that made the entry live; null for seeded entries |
| `bulletin_url`, `bulletin_week` per church | as today | the newest bulletin whose call succeeded and wasn't a wrong bulletin or stale |

`computeNextOccurrence` needs:

- the weeks-of-month and season rules;
- skipping a weekly entry's date when a cancellation names it.

## What changes in the code

| Area | Change |
|---|---|
| `data/migrations/` | `0004_schedule_state.sql` adds the tables above. The cleanup migration comes later (see [Rollout](#rollout)) |
| `weekly.py`, `__main__.py`, `weekly-docker.yml` | `SCHEDULE_MODE` (`extract` or `update`, default `extract`) picks the process stage, the report and the snapshot's source. The workflow reads it from a repository variable |
| `process.py` | update mode: render the view, call, store the call and its proposals, decide, apply. Extract mode as today |
| new `schedule/` package | the view renderer, entry hashing and identity, the policy, apply and fold (and a full rebuild from the log), the converters for weeks of month and season |
| `classifiers/` | a `schedule_update` task: new policy prompt and response schema; version digest covers both; returns token usage and served model |
| `schedule_extraction.py` | unchanged: the from-scratch extraction serves extract mode and the evals |
| `bulletin_week.py`, `fetch.py`, `storage.py` | unchanged while both modes exist: update mode also writes the bulletin's `published_date`, `wrong_bulletin` and `processed_at`, as extract mode does |
| `report.py`, `verify_frontend_snapshot.py` | update mode reports from `proposed_change`, as in [The report](#the-report-update-mode); the remaining run-level checks |
| `extract_frontend_db.py`, `apps/web` | snapshot v2 from either mode, with the cancellation matching; `computeNextOccurrence` rules |
| `labeling/bulletins.py` | in update mode, the read-only "model's answer" becomes the call's view with its applied proposals |

## Rollout

The work merges in small pieces behind `SCHEDULE_MODE`, and the weekly run
keeps publishing in extract mode until the switch.

1. **Migration 0004 and the `schedule/` package** land with the mode at
   `extract`. Nothing writes the new tables yet.
2. **Snapshot v2 and the frontend** ship, built from `event` in extract mode.
3. **Seed.** Each parish's first `seed` revision is loaded into the published
   database by the out-of-scope method. A later seed for a parish that already
   has one is a new `seed` revision of adds, modifies and deletes, like any
   other.
4. **Switch** the repository variable to `update`. The next weekly run
   processes its new bulletins against the seeded schedules.
5. **Rolling back** is setting it back to `extract`. `event` still holds what
   the last extract-mode run left, and bulletins update mode already processed
   are marked processed, so extract mode carries on from the next new
   bulletin. Switching forward again continues the believed schedule where it
   was, and the high-water mark keeps older bulletins out.
6. **Cleanup,** once update mode has settled: a migration drops `event`,
   `event_occurrence`, `idx_bulletin_parish_processed` and the bulletin's
   `published_date`, `wrong_bulletin` and `processed_at`, and adds the view
   below for the readers of those columns. Extract mode and `recurrence.py`
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
- Running both modes in one weekly run, or update mode in shadow.
- New eval cases for update calls. Testing is by hand.
- Changes effective from a future date (`valid_from` / `valid_until`).
- Holding doubtful changes for corroboration by a later bulletin or for a
  person's review. Everything applies or is rejected at once in v1.
- Recording which believed entries a bulletin showed unchanged (when each entry
  was last seen in print).
- Tooling for people to edit schedules (the tables record `human` revisions
  already).
- Periodic from-scratch audit calls to catch errors the update calls anchor on.
  This is a second `llm_call.task` when it comes.
- Tally corrections as `human` revisions.
