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
