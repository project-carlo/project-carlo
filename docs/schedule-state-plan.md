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

There is no migration. The new schema is a fresh baseline and the pipeline cuts
over to it (see [Cutover](#cutover)).

## How a bulletin is processed

```
believed schedule (parish @ revision N) ─┐
bulletin PDF                             ├─► llm_call ─► proposed_change ─► schedule_change ─► revision N+1
policy, schema, settings, date           ┘   (stored)    (stored, with       (the log)
                                                          its decision)
```

1. Fetch stores the bulletin, as today.
2. Render the parish's believed schedule at its current revision into a
   canonical JSON **view**, and hash it.
3. Call the model with the policy prompt, the church list, the date, the view
   and the PDF. Store the call, whether or not it succeeds.
4. Store each proposed change.
5. The decision policy (code) decides each proposal at once: apply it or
   reject it. Nothing waits for a later bulletin.
6. Applied changes are written to the change log as one new revision, and the
   current schedule is updated from them.

The change log is the source of truth. `schedule_item` (the current schedule)
is what the log folds to and can be rebuilt from it.

## Schema

The new `data/migrations/0001_initial.sql`, in full. `parish`, `church`,
`pipeline_run` and `run_parish_result` are unchanged. `bulletin` loses the
columns that came from the extractor. `event` and `event_occurrence` are gone.

```sql
-- Project Carlo database schema: the believed-schedule baseline.
-- Marks the database as this format, so code refuses a pre-cutover database
-- instead of mistaking its user_version for this baseline's.
PRAGMA application_id = 0x43524C32;   -- 'CRL2'
PRAGMA foreign_keys = ON;

-- ── Curated (unchanged): seeded from data/parishes.csv and data/churches.csv ──

CREATE TABLE parish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    homepage_url TEXT NOT NULL,
    bulletin_provider TEXT,
    provider_id TEXT,
    created_at TEXT
);

CREATE TABLE church (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    slug TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    address_line1 TEXT, address_line2 TEXT,
    city TEXT, state TEXT, postal_code TEXT,
    latitude REAL, longitude REAL,
    name_verified INTEGER NOT NULL DEFAULT 0,
    address_verified INTEGER NOT NULL DEFAULT 0,
    created_at TEXT
);
CREATE INDEX idx_church_parish_name ON church(parish_id, name);
CREATE INDEX idx_church_lat_lng ON church(latitude, longitude);

-- ── Fetched bulletins: only what fetch knows. What the model read off a
--    bulletin (its date, whether it is this parish's) is on its llm_call. ──

CREATE TABLE bulletin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    source_url TEXT NOT NULL,
    content_hash TEXT NOT NULL,       -- sha256 of the PDF as downloaded
    fetched_at TEXT NOT NULL,
    last_seen_at TEXT,
    etag TEXT,
    last_modified TEXT,
    UNIQUE (parish_id, source_url, content_hash)
);

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
    call_date TEXT NOT NULL,          -- the "today" the prompt gave
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
    finished_at TEXT                  -- replaces bulletin.processed_at
);
CREATE INDEX idx_llm_call_bulletin ON llm_call(bulletin_id);
CREATE INDEX idx_llm_call_parish ON llm_call(parish_id, id);

-- What fetch and bulletin_week.py read in place of the removed bulletin
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

-- ── The believed schedule ──

-- An immutable schedule entry value. Items, proposals and the change log all
-- point at these rows, so the columns and their checks are defined once.
-- Identical values are stored once (`hash`).
CREATE TABLE schedule_value (
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
    -- the weekly slot a cancelled specific_date entry cancels, when it is one
    cancels_item_id INTEGER REFERENCES schedule_item(id),
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
    CHECK ((season_start_month IS NULL) = (season_end_month IS NULL)),
    CHECK (season_start_day IS NULL OR season_start_month IS NOT NULL),
    CHECK (season_end_day IS NULL OR season_end_month IS NOT NULL),
    CHECK (cancels_item_id IS NULL OR (event_kind = 'specific_date' AND cancelled = 1))
);

-- One row per entry the parish's schedule has ever had. Its id is stable for
-- its whole life, and is how the model refers to it.
CREATE TABLE schedule_item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL REFERENCES parish(id) ON DELETE CASCADE,
    value_id INTEGER NOT NULL REFERENCES schedule_value(id),   -- current value
    identity_key TEXT NOT NULL,       -- copied from the value, for the index below
    created_revision INTEGER NOT NULL,
    deleted_revision INTEGER          -- null while believed
);
-- No two believed entries are the same slot.
CREATE UNIQUE INDEX idx_schedule_item_live
    ON schedule_item(parish_id, identity_key) WHERE deleted_revision IS NULL;

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

-- The log. schedule_item is this folded in order.
CREATE TABLE schedule_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parish_id INTEGER NOT NULL,
    revision INTEGER NOT NULL,
    op TEXT NOT NULL CHECK (op IN ('add', 'modify', 'delete')),
    item_id INTEGER NOT NULL REFERENCES schedule_item(id) ON DELETE CASCADE,
    before_value_id INTEGER REFERENCES schedule_value(id),     -- null for add
    after_value_id INTEGER REFERENCES schedule_value(id),      -- null for delete
    proposed_change_id INTEGER REFERENCES proposed_change(id), -- null for seed and human
    FOREIGN KEY (parish_id, revision) REFERENCES schedule_revision(parish_id, revision)
        ON DELETE CASCADE,
    CHECK ((op = 'add' AND before_value_id IS NULL AND after_value_id IS NOT NULL)
        OR (op = 'modify' AND before_value_id IS NOT NULL AND after_value_id IS NOT NULL)
        OR (op = 'delete' AND before_value_id IS NOT NULL AND after_value_id IS NULL))
);
CREATE INDEX idx_schedule_change_item ON schedule_change(item_id);

-- ── What the model proposed, and what the policy did with it ──

-- Every proposal is decided when its call is processed, applied or rejected,
-- so the decision lives on the proposal's own row.
CREATE TABLE proposed_change (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    llm_call_id INTEGER NOT NULL REFERENCES llm_call(id) ON DELETE CASCADE,
    op TEXT NOT NULL CHECK (op IN ('add', 'modify', 'delete')),
    target_item_id INTEGER REFERENCES schedule_item(id),   -- modify, delete
    value_id INTEGER REFERENCES schedule_value(id),        -- add, modify: the whole new value
    page_number INTEGER,
    quote TEXT,                       -- the bulletin's words that call for the change
    rationale TEXT,
    decision TEXT NOT NULL CHECK (decision IN ('applied', 'rejected')),
    reason TEXT NOT NULL,             -- a code from the policy: 'auto', 'stale_bulletin', 'conflict', ...
    decided_by TEXT NOT NULL,         -- 'policy@<version>'
    CHECK ((op = 'add' AND target_item_id IS NULL AND value_id IS NOT NULL)
        OR (op = 'modify' AND target_item_id IS NOT NULL AND value_id IS NOT NULL)
        OR (op = 'delete' AND target_item_id IS NOT NULL AND value_id IS NULL))
);
CREATE INDEX idx_proposed_change_call ON proposed_change(llm_call_id);

-- ── Run bookkeeping (unchanged) ──

CREATE TABLE pipeline_run (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    git_sha TEXT,
    trigger TEXT,
    summary_json TEXT
);

CREATE TABLE run_parish_result (
    run_id TEXT NOT NULL REFERENCES pipeline_run(id) ON DELETE CASCADE,
    parish_slug TEXT NOT NULL,
    stage TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    source_url TEXT,
    content_hash TEXT,
    event_count INTEGER,
    PRIMARY KEY (run_id, parish_slug, stage)
);
```

### Notes on the schema

**Values, items and changes.** A `schedule_value` is one entry's content, never
edited. A `schedule_item` is one entry over its lifetime, pointing at its
current value. A modify writes a new value and moves the pointer, and the log
keeps both. With this split, the item columns and their checks exist only
once: proposals, the log and the current schedule all reference value rows,
and nothing holds an item as JSON.

**Identity.** `identity_key` is computed in code from the value:

- weekly: church, event type, weekday, start time, weeks of month, season
- specific_date: church, event type, date, start time, cancelled

End time and note are not part of identity. Two live entries with the same
identity are refused by the index, and the policy rejects an add that would
duplicate one as `duplicate`.

**Weeks of the month and season** are structured as in the labels
(`labeling/labels.py`). The database stores `weeks_of_month` as a 6-bit mask
and the season as four integer columns. The view, the model's output and the
snapshot use the labels' forms: `["first", "third"]` and
`{"start_month": 5, "start_day": null, "end_month": 10, "end_day": null}`.
One converter, in one module, does the translation and is shared with the
labels code.

**Cancellations** are specific_date entries with `cancelled = 1`, as in the
labels. When one cancels a believed weekly slot, `cancels_item_id` names it, so
the site can skip that slot on that date.

**Dated entries expire on their own.** A specific_date entry whose date has
passed is left out of the view and out of the snapshot, with no revision. It is
never deleted. That keeps past dates out of the change log, which is where most
of today's report noise comes from.

**Changes take effect immediately.** There is no `valid_from`/`valid_until`.
The policy prompt tells the model to propose only changes that are already in
effect in the bulletin's week, and to leave an announced future change ("from
November 1 the vigil moves to 5 PM") until a bulletin from a week where it is in
effect. Effective dates can be added later as columns on `schedule_value`.

**Bulletin columns.** `published_date`, `wrong_bulletin` and `processed_at`
move to `llm_call`. The `bulletin_reading` view lets `bulletin_week.py`,
`fetch.py` and `storage.py` keep reading the same fields from it rather than
from `bulletin`.

## The model's input and output

### Input: the view

The canonical JSON of the parish's live entries, with expired dated entries
left out. Keys are sorted, entries ordered by church, kind, weekday or date,
then time, and there is no whitespace, so the same schedule always hashes the
same:

```json
{"churches":[{"slug":"st-mary-albany","entries":[
  {"id":118,"event_type":"mass","event_kind":"weekly","day_of_week":"Sunday",
   "start_time":"9:00 AM","end_time":null,"weeks_of_month":[],"season":null,"note":null},
  {"id":131,"event_type":"confession","event_kind":"weekly","day_of_week":"Saturday",
   "start_time":"3:00 PM","end_time":"3:45 PM","weeks_of_month":["first"],"season":null,"note":null},
  {"id":140,"event_type":"mass","event_kind":"specific_date","date":"2026-10-14",
   "start_time":"7:00 AM","cancelled":true,"cancels_item_id":119,"note":null}
]}]}
```

The church list (slugs, names, addresses) goes in as context, as today, and
`church_list_hash` records which list was sent.

### Output

```json
{
  "published_date": "2026-10-11",
  "wrong_bulletin": false,
  "church_list_needs_review": false,
  "changes": [
    {"op": "modify", "item_id": 131,
     "entry": {"event_type":"confession","event_kind":"weekly","church_slug":"st-mary-albany",
               "day_of_week":"Saturday","start_time":"3:00 PM","end_time":"4:00 PM",
               "weeks_of_month":["first"],"season":null,"note":null},
     "page_number": 2, "quote": "Confessions 1st Saturday 3:00–4:00 PM",
     "rationale": "End time changed from 3:45 to 4:00."},
    {"op": "add", "entry": {...}, "page_number": 3, "quote": "...", "rationale": "..."},
    {"op": "delete", "item_id": 140, "page_number": 1, "quote": "...", "rationale": "..."}
  ]
}
```

- **add** and **modify** carry the whole new entry, not a patch. The model does
  not have to express "clear the end time", and code works out which fields
  changed.
- **modify vs. delete + add.** The model may use either, and the policy treats
  them the same way. The report can still show an add and a delete of the same
  identity in one call as a modify.
- **`quote`** is required on every change. The report checks it against the
  PDF's text layer where there is one.

## Decision policy (v1)

The policy is code. Its version is recorded in every proposal's `decided_by`.
Every proposal is decided when its call is processed: applied or rejected.
Nothing is held for a later bulletin or a person.

A proposal is **rejected** when:

| Condition | Reason |
|---|---|
| the call says `wrong_bulletin` | `wrong_bulletin` |
| the bulletin's week is older than the week of the parish's last applied call | `stale_bulletin` |
| its target item changed since the call's `base_revision` | `conflict` |
| it targets an item that isn't live in the parish | `unknown_item` |
| it is an add, or a modify, that would duplicate a live identity | `duplicate` |
| its entry names a church outside the parish | `unknown_church` |

Every other proposal is **applied** (`auto`): adds, modifies and deletes,
weekly or dated. A call that fails (`parse_failed`, `api_error`) stores no
proposals.

The report flags applied changes worth a look, without blocking them:

- a quote not found in the PDF's text layer;
- a call that deletes more than half the parish's live entries;
- a parish whose schedule changed in each of its last few calls.

A run is no longer held for schedule changes. The run-level checks that remain
concern the run itself: more than half the parishes failed to fetch, a stage
crashed, or the snapshot fails to verify.

## Processing order

- **Sequential within a parish, parallel across parishes.** Each call reads the
  revision the previous call left. Run concurrency stays per parish, as now.
- **New bulletins for one parish** are processed in order of fetch time. A
  site's fallback to an old issue is still called (the date is only known
  after the model reads it), but its changes are rejected as `stale_bulletin`.
- **A parish with no revision yet is skipped**, reported as `unseeded`. It
  is never bootstrapped by showing the model an empty schedule.
- **Caching:** `request_key` is unique. Re-running the same bulletin against the
  same view, version, date and church list reuses the stored call instead of
  calling the API, both after a crash and in replays. The raw response is in R2
  under `llm/calls/<request_key>.json`, so a fresh database can reuse it too.

## The snapshot (format version 2)

`extract_frontend_db.py` builds events from live `schedule_item`s joined to
their values. It leaves out specific_date entries whose date has passed.

- **Kept columns:** `id` (the item id), `church_id`, `event_type`,
  `event_kind`, `day_of_week`, `date`, `start_time`, `end_time`, `cancelled`,
  `note`.
- **`page_number`:** from the proposal behind the item's current value. Null
  for seeded entries.
- **New:** `weeks_of_month`, `season_start_month`, `season_start_day`,
  `season_end_month`, `season_end_day`, `cancels_event_id`.
- **Per church:** `bulletin_url` and `bulletin_week` come from the parish's
  latest bulletin with an applied call.

It is version 2 because a weekly row with `weeks_of_month = ["first"]` would
otherwise be read as every week. `computeNextOccurrence` needs:

- the weeks-of-month and season rules (the feature you're adding with this);
- skipping a weekly slot's date when a live cancellation names it.

## What changes in the code

| Area | Change |
|---|---|
| `data/migrations/` | the three migrations replaced by the new `0001_initial.sql` |
| `db.py` | `ensure_db` refuses a database without the new `application_id` |
| `process.py` | rewritten: render view, call, store the call and its proposals, decide, apply |
| new `schedule/` package | the view renderer, value hashing and identity, the policy, apply/fold, the converters for weeks of month and season |
| `classifiers/` | a `schedule_update` task: new policy prompt and response schema; version digest covers both; returns token usage and served model |
| `schedule_extraction.py` | the production schema and prompt move to the new task; the from-scratch extraction stays for evals |
| `recurrence.py`, `event_occurrence` | removed: the model sees the believed weekly slot, so a dated sighting of it is no change |
| `bulletin_week.py`, `fetch.py`, `storage.py` | read `bulletin_reading` instead of the dropped bulletin columns |
| `report.py`, `weekly.py`, `verify_frontend_snapshot.py` | report from `proposed_change` per parish, with the flags above; the remaining run-level checks |
| `extract_frontend_db.py`, `apps/web` | snapshot v2; `computeNextOccurrence` rules |
| `labeling/bulletins.py` | the read-only "model's answer" becomes the call's view with its proposals applied |
| `evals/` | the new eval cases below |

## Evals

The labels stay as they are, one full schedule per bulletin. What changes is
how a case is built, because a call now needs a believed schedule as input:

- **Identity.** Use the label as the view. The right answer is no changes. This
  measures the **false-change rate**, the
  number that matters most here.
- **Perturbation.** Use the label with known edits: an entry removed, a time
  shifted, a fake entry added, an end time dropped, a qualifier lost. The right
  answer is exactly the inverse edits. This scores recall of real changes.
- **Sequential.** Use the previous week's label as the view and score the
  result against this week's label, with the existing tiers in
  `evals/report.py`. Today there is one label per parish, so this needs the
  following week's bulletin labeled for some parishes.

Scoring applies the proposals with the v1 policy, so the eval measures what
would reach the site, not only what the model said.

## Cutover

1. **Merge the code** with the weekly workflow and deploys paused. The deploy
   builds its snapshot from the published database, and the published database
   stays in the old format until step 3.
2. **Build the new database**, seeded by the out-of-scope method: parish and
   church tables from the CSVs, one `seed` revision per parish. `bulletin` starts
   empty. The first run fetches each parish's current bulletin as new. PDFs are
   content-addressed in R2, so nothing is stored twice.
3. **Run the weekly pipeline on it and publish it** through the usual
   candidate → publish path.
4. **Resume deploys.** The first deploy builds a v2 snapshot from it. Old pages
   reload on the snapshot version change (`staleDeploy.ts`).

What the cutover gives up:

- **Rollback can't cross it.** A pre-cutover run can't be published by the new
  code, and `data:pull` of one refuses. Those runs stay in R2 until pruning ages
  them out.
- **The old `event` history isn't carried over.** It stays readable in the
  pre-cutover runs if the seeding method wants it.
- **Prediction caches start fresh.** The old caches in R2 under
  `runs/<classifier>/cache/` still serve the evals' from-scratch classifiers.

## Out of scope

- Initial population of schedules (the `seed` revisions).
- Changes effective from a future date (`valid_from` / `valid_until`).
- Holding doubtful changes for corroboration by a later bulletin or for a
  person's review. Everything applies at once in v1.
- Recording which believed entries a bulletin showed unchanged (when each entry
  was last seen in print).
- Tooling for people to edit schedules (the tables record `human` revisions
  already).
- Periodic from-scratch audit calls to catch errors the update calls anchor on.
  This is a second `llm_call.task` when it comes.
- Tally corrections as `human` revisions.

## Open questions

1. **`weeks_of_month` storage:** a 6-bit mask (proposed), or six boolean
   columns? Either way it converts to the labels' list at the edges.
2. **The view's date cutoff:** leave out specific_date entries dated before the
   call date (proposed), or before the start of the bulletin's week?
