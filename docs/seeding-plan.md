# Project Carlo: seeding believed schedules with an agent

Status: implemented, with no parish seeded yet. Builds on [the schedule-state
plan](schedule-state-plan.md) (implemented in lyonsl2/project-carlo#105), whose
rollout step 3 is "seed parishes in batches" and leaves the seeding method out
of scope. This is that method. Where the implementation had to decide
something this plan left open, see
[Implementation decisions](#implementation-decisions).

A parish moves from extract mode to update mode when it gets its first `seed`
revision: the schedule the weekly run then keeps up to date, one bulletin at a
time. So the seed has to be right. A wrong slot in a seed stays until a
bulletin makes the model propose changing it, and a slot the seed misses is
only added when a bulletin makes the model notice it is missing.

Seeds are drafted by a Claude Code agent, which reads the parish's bulletins
itself against the extraction policy (`classifiers/schedule_policy.POLICY`).
It writes down, for every slot, what each source said, what it decided and
why. Where it can't decide, it writes a question for a person. A person
settles those questions in the labeler and approves the parish. The approved
seed file is committed, and the pipeline loads it.

## Decisions

- **The agent reads every bulletin it relies on.** It does not take a slot on
  trust because two other sources agree. Agent usage is cheap here; API usage
  is what to keep down.
- **External models are optional second opinions.** The agent's own reading
  and the extract-mode history already in the database come first. It calls
  `gpt-6.1-sol` or `gemini-3-flash-preview` only when those leave something in
  doubt, and every call is recorded in the seed file.
- **More than one bulletin when it helps.** The agent can see how many
  bulletins each parish has and reads further back (the second newest, the
  third...) when a question needs it: weekly or one-off, a time that differs
  between weeks, a seasonal note.
- **Seed scope:** weekly slots, plus dated entries and cancellations on or
  after the seed's `as_of` date. Update mode never calls a bulletin fetched on
  or before `as_of`, so a cancellation left out of the seed (next Saturday's
  vigil called off in the newest bulletin) would never reach the site.
- **Runs locally**, in Claude Code on the maintainer's machine, with the R2
  read keys, `OPENAI_API_KEY` and `GEMINI_API_KEY`.
- **Seed files are committed**, like the labels, and the pipeline loads the
  approved ones. Nothing is written to the published database by hand.
- **Subagents take 3–8 parishes each.** The number is the orchestrator's
  choice per batch, and nothing else depends on it.

## How a parish is seeded

```
pnpm seed pick ─► subagent per 3–8 parishes ─► data/seeds/<parish>.json ─► labeler review ─► approved, committed ─► next pipeline command loads it
                  (reads bulletins, history,      (every slot, its sources,    (open questions,
                   asks models when needed)        decision, rationale)         approve)
```

1. The orchestrating agent picks a batch (`pnpm seed pick`) and hands the
   parishes to subagents, a few each.
2. Each subagent drafts one parish at a time and writes its seed file before
   starting the next, so an interrupted subagent loses at most the parish it
   was on.
3. A person opens the labeler's Seeds view, answers the open questions,
   checks whatever else they want to, and approves the parish.
4. The approved files are committed and merged. Every pipeline command loads
   the approved seeds not yet in its database (see
   [Loading seeds](#loading-seeds)), so the parish is in update mode from the
   next weekly run.

## The agent

A skill, `.claude/skills/seed-parishes/SKILL.md`, next to `explore-diocese`.
It covers the orchestrator's job and the subagent's, the tools, the file
format, and the judgment calls below. The policy itself stays in
`schedule_policy.POLICY`: the skill tells the agent to read it, and does not
restate it.

### What a subagent does for each parish

1. **Look at what's available.** `pnpm seed bulletins <parish>` lists the
   parish's stored bulletins, newest first.
2. **Read the newest bulletin in full** (`pnpm seed pdf`), and draft every
   Mass, Confession and Adoration slot the policy asks for, with its page.
   Write down what it leaves out on purpose too (a Communion Service, a
   chapel at another address, a school Mass), since those are the policy
   calls a reviewer will want to see.
3. **Compare with history.** `pnpm seed history <parish>` shows what extract
   mode stored for the parish's past bulletins. It costs nothing. It came from
   the older production prompt, so a difference is a reason to look closer,
   not a vote.
4. **Read further back when a question needs it**, one bulletin at a time:
   - a slot printed in only one bulletin (weekly, or a one-off?)
   - a time or day that differs from history or between bulletins
   - a seasonal hint ("summer schedule", "beginning in Advent")
   - a newest bulletin that looks like an old issue, or a different parish's
5. **Ask a model when its own reading and history still leave doubt.** A
   targeted question (`pnpm seed ask`) is preferred to a full extraction
   (`pnpm seed extract`): it's cheaper, and its answer is about exactly the
   thing in doubt. The agent need not call any model for a parish whose
   bulletins are clear.
6. **Decide each slot**, and mark it:
   - `settled`: printed clearly, the policy is clear about it, and nothing
     the agent read contradicts it.
   - `needs_human`: the sources conflict and the bulletins don't settle it;
     the policy leaves it a judgment call; the print is unreadable; or the
     church or chapel it belongs to is unclear. The agent writes a short
     question and the answers it's choosing between, and says which it leans
     to and why.
7. **Run `pnpm seed check <parish>`** and fix anything it reports.

A parish that can't be seeded now (no usable bulletin, no schedule in its
bulletins, a church missing from `churches.csv`) is marked `blocked` with the
reason, and the subagent moves on.

### What the orchestrator does

- Picks the batch, splits it among subagents, and gives each the skill and
  its parish list.
- When the subagents finish, runs `pnpm seed check` over the batch and lists
  the parishes by status, with the number of open questions each.
- Never edits a subagent's decisions. A file that looks wrong is re-drafted by
  a subagent or left to the reviewer.

## Tools

`pnpm seed`, a new subcommand of the pipeline CLI. Every command reads the
local database (`pnpm data:pull`) and the blob store as the labeler does, and
prints compact text by default, `--json` on request.

| Command | What it does |
| :-- | :-- |
| `seed pick [--limit N] [--diocese D] [--labeled]` | Parishes with no seed and no seed file, easiest first: one church, a recent bulletin, extract-mode output stable from week to week. `--labeled` picks the parishes with labels instead, for the [test run](#testing-it-first). |
| `seed bulletins <parish>` | The parish's bulletins, newest first: short hash, fetch date, issue date if known, page count, whether extract mode flagged it as a wrong bulletin, and whether it's a duplicate of another. |
| `seed pdf <parish> <bulletin>` | Writes the stored compacted PDF (the first 10 pages, or the parish's limit) to a local path and prints it, so page numbers match the pipeline's and the labeler's. |
| `seed pages <parish> <bulletin> [--page N] [--dpi D]` | Renders pages as PNGs, for bulletins that are only images or a dense table to zoom into. |
| `seed history <parish> [--bulletins N]` | Extract mode's stored events for the parish's last N bulletins, one table per bulletin, with pages. |
| `seed extract <parish> <bulletin> --model M` | A full extraction with `POLICY`, through the existing classifiers (`gpt-6-luna --model gpt-6.1-sol`, `gemini-flash-qualified`) and the runner's result cache, so asking twice costs one call. The result is appended to the seed file's `calls`. |
| `seed ask <parish> <bulletin> --model M "question"` | One question about one bulletin, answered with an answer, the page and the words it read there. Appended to `calls`. |
| `seed check <parish>... [--all]` | The file is well formed, every entry parses as `pnpm schedule seed` would (`schedule.entries.parse_entry`), churches belong to the parish, no two included entries share a slot, every slot has a source and a rationale, every open question has options, and `as_of` is the newest bulletin consulted. |
| `seed status` | Every seed file's status and open questions, and whether the local database has loaded it. |

`M` is `gpt-6.1-sol` or `gemini-3-flash-preview`. `extract` and `ask` refuse
once a parish has used its call limit (`CARLO_SEED_CALL_LIMIT`, default 4),
so a confused subagent can't run up the bill. A cache hit doesn't count.

`ask` needs a new small prompt: `POLICY`, the parish's churches, the date,
then the question, with a schema of `answer`, `page` and `quote`. It is
versioned and cached like the classifiers.

There is no `seed load`: loading is what the pipeline does with approved files.
`pnpm schedule seed` stays as the low-level loader for one-off fixes.

## The seed file

`data/seeds/<parish_slug>.json`, committed. One file per parish.

```json
{
  "schema_version": 1,
  "parish_slug": "st-marys-oswego",
  "status": "needs_review",
  "as_of": "2026-10-04T06:12:31Z",
  "drafted_by": "claude-code/seed-parishes",
  "drafted_at": "2026-10-11T15:02:00Z",
  "reviewer": null,
  "approved_at": null,
  "summary": "Two churches. Weekend and daily Masses agree across three bulletins. Saturday confessions differ between weeks.",
  "blocked_reason": null,
  "bulletins": [
    {"content_hash": "9f2c…", "fetched_at": "2026-10-04T06:12:31Z", "published_date": "2026-10-04", "read": true},
    {"content_hash": "1ab3…", "fetched_at": "2026-09-27T06:10:02Z", "published_date": "2026-09-27", "read": true}
  ],
  "calls": [
    {"id": "c1", "kind": "ask", "model": "gemini-3-flash-preview", "bulletin": "9f2c…",
     "question": "Page 2: when are Saturday confessions at St. Mary's?",
     "answer": "3:00–3:45 PM", "page": 2, "quote": "Confessions Sat 3:00-3:45pm",
     "cached": false, "cost_usd": 0.004}
  ],
  "slots": [
    {
      "id": "s1",
      "decision": "include",
      "status": "settled",
      "entry": {"church_slug": "st-marys-oswego", "event_type": "mass", "event_kind": "weekly",
                "day_of_week": "Saturday", "date": null, "start_time": "16:00", "end_time": null,
                "cancelled": false, "weeks_of_month": [], "season": null, "note": "Vigil"},
      "page": 2,
      "sources": [
        {"source": "agent", "bulletin": "9f2c…", "page": 2, "said": "Sat 4:00 PM Vigil"},
        {"source": "agent", "bulletin": "1ab3…", "page": 2, "said": "Sat 4:00 PM Vigil"},
        {"source": "history", "bulletin": "1ab3…", "said": "weekly Saturday 16:00"}
      ],
      "rationale": "Printed in the Mass schedule box of both bulletins read; history agrees.",
      "question": null,
      "options": null,
      "answer": null
    },
    {
      "id": "s2",
      "decision": null,
      "status": "needs_human",
      "entry": null,
      "page": 2,
      "sources": [
        {"source": "agent", "bulletin": "9f2c…", "page": 2, "said": "Confessions Sat 3:00-3:45pm"},
        {"source": "agent", "bulletin": "1ab3…", "page": 2, "said": "Confessions Sat 3:30-3:50pm"},
        {"source": "c1", "bulletin": "9f2c…", "page": 2, "said": "3:00–3:45 PM"}
      ],
      "rationale": "The two newest bulletins print different times in the same box. The newest is more likely current, but the older time also appears in history for four weeks before.",
      "question": "Saturday confessions at St. Mary's: 3:00–3:45 or 3:30–3:50?",
      "options": [
        {"label": "3:00–3:45 (newest bulletin)", "entry": {"…": "…"}, "leaning": true},
        {"label": "3:30–3:50 (older bulletins)", "entry": {"…": "…"}},
        {"label": "Leave out", "entry": null}
      ],
      "answer": null
    }
  ]
}
```

- **`entry`** is in the labels' event shape without `page_number`, `origin`
  and `optional`: the shape `pnpm schedule seed` reads.
- **`page`** is where the newest bulletin prints the slot. It becomes the
  entry's sighting in that bulletin when the seed is loaded; null when the
  newest bulletin doesn't print it.
- **`sources[].source`** is `agent` (the agent's own reading), `history`
  (extract mode's stored events), or the id of a `calls` item.
- **`decision`** is `include` or `exclude`. Excluded slots keep their entry
  and rationale, for review, and are never loaded.
- **An answered question** has `answer` set to the chosen option's index, or
  to an entry the reviewer edited, and the reviewer's name. `decision`,
  `entry` and `status` (`settled`) follow from it.
- **`as_of`** is the fetch time of the newest bulletin consulted. Update mode
  calls every bulletin fetched after it, so bulletins that arrive while a seed
  waits for review are caught up on, not skipped.
- **`status`** of the parish:

  | Status | Meaning |
  | :-- | :-- |
  | `drafting` | a subagent is on it, or stopped part way |
  | `needs_review` | at least one open question |
  | `ready` | no open questions, waiting for approval |
  | `approved` | a person approved it; the pipeline loads it |
  | `blocked` | can't be seeded now; `blocked_reason` says why |

  Whether a file is loaded isn't stored in it: `seed status` reads it from
  the database.

## Review in the labeler

A Seeds mode in the labeler (`pnpm label`), next to the bulletin queue.

- **Queue:** parishes by status, `needs_review` first, with the number of
  open questions each.
- **Parish page:**
  - The existing `PdfViewer`, with a tab for each bulletin the agent read.
  - The agent's summary, then the open questions, then the settled slots
    (collapsed by default), then the excluded ones.
  - Each slot shows its sources side by side and the agent's rationale.
    Clicking a source opens its bulletin at its page.
- **Keys:** `1`/`2`/`3` choose an option; `e` edits the entry with
  `RowEditor`; `x` drops a slot; `r` reopens a settled slot as a question.
- **Approve** is enabled once nothing is open. It sets `status`, `reviewer`
  and `approved_at`, and runs the same checks as `seed check`.

New API routes beside the labels': `GET /api/seeds`, `GET
/api/seeds/<parish>`, `PUT /api/seeds/<parish>`. The PDF route the labeler
already has (`/api/bulletins/<parish>/<hash>/pdf`) serves the bulletins. The
server validates every write and confines paths to `data/seeds`, as for the
labels.

## Loading seeds

The published database is only written by the pipeline, so seeds reach it the
way `parishes.csv` does: every pipeline command, after re-seeding `parish` and
`church` from the CSVs, loads the approved seed files.

- For each `approved` file, the loader computes a digest of its included
  entries, pages and `as_of`. If the parish's latest `seed` revision doesn't
  carry that digest (in its `note`), it calls `schedule.store.write_seed` with
  the entries, `as_of`, `actor` set to the reviewer, and sightings for the
  newest bulletin (its content hash resolved to the parish's bulletin id).
- **A first seed switches the parish to update mode.** A later approved
  version of the file is a new `seed` revision, as the schedule-state plan
  allows, but only if its `as_of` is later than the parish's latest seed's.
  Otherwise re-loading it would undo the changes update mode has applied
  since, so the loader skips it and the run's report says so.
- A file that fails the checks is skipped and reported; the rest load.
- The local database loads approved seeds the same way, on the next local
  command, so `pnpm extract:web` shows the seeded schedules before merging.

**Batches and the run's change gate.** The run holds its snapshot when too
much changes at once, and a batch of newly seeded parishes is compared with
their last extracted schedules. Merge seeds in batches small enough to pass,
or approve the held run by hand.

## Testing it first

Before seeding for real, run the agent on the parishes behind the labeled
bulletins (`pnpm seed pick --labeled`). For these, `as_of` is fixed at the
labeled bulletin's fetch time, and `seed bulletins`, `history` and `pdf` hide
anything newer, so the agent sees what it would have seen then. The drafts go
to `data/seed-evals/<run>/`, not `data/seeds/`, so they are never loaded.

`pnpm seed score <run>` compares each draft with its label, using the eval
report's matching (`evals/report.py`). It compares only what a seed holds:
weekly rows, and dated rows and cancellations on or after `as_of`. It reports:

- the accuracy of the agent's `settled` slots, the number that matters most,
  since a reviewer may approve them without reading each one
- how often its leaning answer to an open question matched the label
- open questions per parish, and external calls and their cost per parish

Running it with 3 parishes per subagent and then with 8 shows whether batch
size costs accuracy.

## What changes in the code

| Where | Change |
| :-- | :-- |
| new `src/pdf_extract/seeding/` | the file format and its checks, the bulletin and history queries, `ask`, the loader, `score`, and the `seed` CLI |
| `classifiers/` | the `ask` prompt and schema, versioned like the others |
| `db.py` (or wherever pipeline commands bring the database up to date) | load approved seed files after the CSVs |
| `report.py` | list seeds loaded and seeds skipped in the run report |
| `labeling/server.py`, `apps/labeler/` | the Seeds routes and views |
| `.claude/skills/seed-parishes/` | the skill |
| `package.json`, `README.md` | `pnpm seed`, and a section on seeding |

## Out of scope

- Seeding from anything but stored bulletins: parish websites, phone calls,
  the diocesan directory.
- Running the agent unattended (in CI or on a schedule).
- Using approved seeds as labels. Their weekly slots are close to a label for
  the newest bulletin, so this could come later.

## Open questions

- **Approving parishes with no open questions.** Every parish is approved by a
  person in this plan. If the test run shows `settled` slots are reliable
  enough, `ready` parishes could be approved in bulk.
- **Subagent batch size**, settled by the test run.

## Implementation decisions

Decisions made while implementing this plan, where it was silent or where the
code departs from it. The code is `src/pdf_extract/seeding/`, the `ask` prompt
`classifiers/seed_ask.py`, the skill `.claude/skills/seed-parishes/SKILL.md`,
and the labeler's `views/SeedPage.tsx` and `lib/seeds.ts`.

### Commands

- **`seed init <parish>`** starts a parish's file: a `drafting` draft listing
  its bulletins, none read yet. `extract` and `ask` start one the same way when
  the parish has none, so a call always has a file to be recorded in.
- **Naming bulletins.** Commands take `latest` or at least 6 hex characters of
  a content hash. Inside a file, `content_hash` in `bulletins` is the full hash,
  and a source's or call's `bulletin` may be any prefix of at least 8
  characters that names one of the file's bulletins.
- **`seed bulletins`** counts the pages of the newest 8 bulletins (`--limit`),
  which downloads those PDFs, as the agent will read them anyway. A bulletin
  whose PDF is another row's (stored before fetch compared downloads by their
  bytes) is listed as a duplicate, and the other commands skip it.
- **`seed pick`'s "easiest"**, in order: one church, a newest bulletin fetched
  in the last 14 days, and extract mode's weekly slots alike in the two newest
  processed bulletins (their Jaccard similarity).
- **`seed pdf` and `seed pages`** write to `data/seed-work/<parish>/`
  (gitignored): the PDF the pipeline reads, and PNGs at `--dpi` (150).
- **Calls.** Both ask the bulletin as of its fetch date, as the evals do, so a
  replay is served from the cache. `extract` runs the eval classifiers
  (`gpt-6-luna --model gpt-6.1-sol`, `gemini-flash-qualified`) and shares their
  result cache. `ask` is cached under `runs/seed-ask/cache/`, by model and
  prompt version, PDF, church list, date and question; on OpenAI it reads the
  PDF at high detail with medium reasoning, since a question is about small
  print. `gpt-6.1-sol` has no price in `evals/pricing.py`, so its calls record
  `cost_usd` as null.
- **Output** is compact text, `--json` the full result: `__main__` prints a
  command's `render` when it sets one.

### The file

- **Every key is present** in the file, slot and option, as in the labels.
  Entries have 24-hour `HH:MM` times (what the labels and the scorer use).
- **An answer** is `{"choice", "by", "at"}`: `choice` is the option's index,
  `edited` (the reviewer's own entry), or `dropped` (the slot left out). An
  excluded slot keeps an entry for review: its own, or else the option the
  agent leaned to.
- **`seed check`** also reports a file still `drafting`, since it is a draft's
  last step, a dated included entry before `as_of`'s date (outside a seed's
  scope), and status that the file contradicts (`needs_review` with no open
  question, `ready` with one, `approved` without a reviewer).

### Review

- **What a review may change.** The server takes `slots`, `status`,
  `reviewer` and `blocked_reason` from the labeler and keeps the rest as the
  agent wrote it. It refuses a file still `drafting`, stamps `approved_at`
  itself, and runs `seed check` before saving an approval.
- **Any change takes back an approval**: the file goes back to `ready` or
  `needs_review`, and must be approved again.
- **Reopening** (`r`) turns a settled slot into a question with its current
  decision as the leaning answer, or its earlier options if it had them.

### Loading

- **The weekly run loads seeds after taking its before-copy**, so its
  snapshot checks compare a newly seeded parish with its last extracted
  schedule, as [Batches and the run's change gate](#loading-seeds) says. Every
  other command loads them in `db.ensure_db`, after the CSVs. A deploy
  (`data snapshot`) never loads them: like a CSV removal, a seed goes live
  through a weekly run.
- **Loaded once per digest.** The revision's note is `seed file <parish>
  <digest>`, and a file is loaded when no seed revision of its parish carries
  that note. A changed file whose `as_of` is not later than the parish's latest
  seed is skipped and reported, on every command, until it is.
- **The loader's checks** are `seed check`'s without the comparison of the
  file's bulletins with the database's: it needs only the entries, and writes a
  sighting only when the newest bulletin read is in the database.
- **The run report** has a Seeds section: what loaded and what was skipped.

### Test runs

- **`seed pick --labeled --eval RUN`** writes `data/seed-evals/RUN/run.json`:
  each labeled parish (a label marked done) with the fetch time of its newest
  labeled bulletin, the cutoff. A run keeps its manifest once written. Every
  command takes `--eval RUN`, reading and writing drafts in
  `data/seed-evals/RUN/seeds/` and hiding bulletins fetched after the cutoff,
  and `seed check` requires `as_of` to be the cutoff.
- **`seed score RUN`** writes `report.md` and `report.json` beside the drafts.
  Settled precision is reported at the eval report's strict and core levels.
  A leaning answer matches when its entry pairs with a row the label wants
  (required, or optional and preferably included), or, when it leans to
  leaving the slot out, when no option pairs with a required row. It also
  counts settled slots left out that a required label row the settled slots
  miss matches.

