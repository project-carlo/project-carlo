# Project Carlo: seeding believed schedules with an agent

Status: implemented and in use, with 50 parishes seeded and approved (October 2026).
Builds on [the schedule-state
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
seed file is committed, and the pipeline loads it. In the onboarding factory
([factory-spec.md](factory-spec.md)), an agent reviewer may answer and approve
instead (see [Approval by an agent](#approval-by-an-agent)).

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
  third...) when a slot needs it (rules.md R3).
- **Seed scope:** weekly slots, plus dated entries and cancellations from the
  seed's `as_of` date on, since update mode starts after `as_of` (rules.md
  R16).
- **Runs locally**, in Claude Code on the maintainer's machine, with the R2
  read keys, `OPENAI_API_KEY` and `GEMINI_API_KEY`.
- **Seed files are committed**, like the labels, and the pipeline loads the
  approved ones. Nothing is written to the published database by hand.
- **Subagents default to 3 parishes each**, fewer for complex parishes. Other
  batch sizes can be compared in evals; the default is not a measured cost ratio.

## How a parish is seeded

```
pnpm seed pick ─► subagent per 3 parishes ─► data/seeds/<parish>.json ─► labeler review ─► approved, committed ─► next pipeline command loads it
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

Two skills split the work. `.claude/skills/seed-parishes/SKILL.md` selects, assigns and
verifies batches, and proposes new rules from reviewers' answers.
`.claude/skills/draft-parish-seed/SKILL.md` is the drafting procedure for one parish. The
`seed-drafter` agent (`.claude/agents/seed-drafter.md`) preloads only the drafting skill,
and holds the drafter's write boundaries. The drafting skill keeps its references beside
it:

- [rules.md](../.claude/skills/draft-parish-seed/rules.md) holds every seeding decision
  rule, with stable IDs that rationales cite. Its default is to ask: a slot no rule covers
  becomes a question for the reviewer. It also holds candidate rules taken from reviewers'
  answers, which the owner promotes. `pnpm seed questions` lists the answered questions
  that new candidates come from.
- [file-format.md](../.claude/skills/draft-parish-seed/file-format.md) is the seed file's
  format.
- The policy stays in `schedule_policy.POLICY`, which the drafter reads in full. It rules
  on one bulletin at a time; rules.md decides across bulletins, history and the website.

## Tools

`pnpm seed`, a subcommand of the pipeline CLI. Every command reads the local database
(`pnpm data:pull`) and the blob store as the labeler does, and prints compact text by
default, or `--json` on request. `pnpm seed --help`, which prints the docstring of
`src/pdf_extract/seeding/cli.py`, is the command reference. It lists the commands by phase:
batch, draft, read, compare and paid calls.

`M` is `gpt-6.1-sol` or `gemini-3-flash-preview`. `extract` and `ask` refuse
once a parish has used its call limit (`CARLO_SEED_CALL_LIMIT`, default 4),
so a confused subagent can't run up the bill. A cache hit doesn't count.

`ask` needs a new small prompt: `POLICY`, the parish's churches, the date,
then the question, with a schema of `answer`, `page` and `quote`. It is
versioned and cached like the classifiers.

There is no `seed load`: loading is what the pipeline does with approved files.
`pnpm schedule seed` stays as the low-level loader for one-off fixes.

## The seed file

One file per parish, `data/seeds/<parish_slug>.json`. Its format, statuses and slot
examples are in [file-format.md](../.claude/skills/draft-parish-seed/file-format.md).
`as_of` is the newest read bulletin's fetch time, and update mode catches up with the
bulletins fetched after it. What a draft must show to settle a slot (its evidence) is in
[rules.md](../.claude/skills/draft-parish-seed/rules.md), and `seed check` enforces the
parts noted there.

## Review in the labeler

A Seeds mode in the labeler (`pnpm label`), next to the bulletin queue.

- **Queue:** parishes by status, `needs_review` first, with the number of
  open questions each (a group counts once) and any church-list issues.
  **Approve all ready (N)** approves every `ready` file using the reviewer name,
  regardless of the status filter. Each file passes the usual approval checks;
  failures stay unapproved and are listed with links to their parish pages.
- **Parish page:**
  - The existing `PdfViewer`, with a tab for each bulletin the agent read.
  - The agent's summary and church-list issues, then the open questions (a
    group's once: one answer settles all its slots), then the settled slots
    (collapsed by default), then the excluded ones.
  - Questions whose every proposed entry is dated before today are marked,
    and one button leaves them all out.
  - Each slot shows its sources side by side and the agent's rationale.
    Clicking a source opens its bulletin at its page.
- **Keys:** `1`-`9` choose an option; `e` edits the entry with
  `RowEditor`; `x` drops a slot; `r` reopens a settled slot as a question.
- **Approve** is enabled once nothing is open. It sets `status`, `reviewer`
  and `approved_at`, and runs the same checks as `seed check`.

New API routes beside the labels': `GET /api/seeds`, `GET
/api/seeds/<parish>`, `PUT /api/seeds/<parish>`, and `POST /api/seeds/approve-ready`
(body: `{ "reviewer": "Your name" }`; returns approved slugs, per-file failures,
and the updated queue). The PDF route the labeler
already has (`/api/bulletins/<parish>/<hash>/pdf`) serves the bulletins. The
server validates every write and confines paths to `data/seeds`, as for the
labels.

## Approval by an agent

The onboarding factory ([factory-spec.md](factory-spec.md), §8 and §11) has a
`seed-review` agent review the seeds of a seed Run. When it approves one, the
factory runs `pnpm seed approve <parish> --reviewer agent:seed-review@<commit>
--answers <file>`. That does what Seeds mode does for a person: each answer
changes its slot as the labeler would, with `by: agent:seed-review@<commit>`,
and the file is approved with that `reviewer`. The checks and `approved_at`
are a person's approval's.

- **Agent answers are kept apart.** `seed questions --answered` lists them
  after people's, by their `by`. Candidate rules come from people's decisions,
  or from a borderline case the owner agrees with.
- **Rules stay the owner's.** The factory never edits rules.md; the owner adds
  a rule in a separate PR.
- **People still approve in the labeler.** `seed approve` refuses a reviewer
  not starting `agent:`. The factory's PR lists every question `seed-review`
  settled by judgment, for the owner to read.

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
bulletins (`pnpm seed pick --labeled --eval RUN`). For these, `as_of` is fixed at the
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
| `.claude/skills/seed-parishes/`, `.claude/skills/draft-parish-seed/` | orchestrator and drafting skills; the drafting skill's `rules.md` (decision rules) and `file-format.md` (the file) |
| `package.json`, `README.md` | `pnpm seed`, and a section on seeding |

## Out of scope

- Using websites as the primary seed source, or consulting live websites in
  historical evals (rules.md says how far a website counts in production).
  Phone calls and the diocesan directory remain out of scope.
- Running the agent unattended (in CI or on a schedule), except as the
  onboarding factory's seed Runs ([factory-spec.md](factory-spec.md)).
- Using approved seeds as labels. Their weekly slots are close to a label for
  the newest bulletin, so this could come later.

## Open questions

- **Approving parishes with no open questions.** People approve `ready`
  parishes in bulk (**Approve all ready**). In the factory, `seed-review`
  approves them with `seed approve` and no answers. Whether an agent's approval
  is reliable enough is for the factory's PRs to show.
- **Subagent batch size**, settled by the test run.

## Implementation decisions

Decisions made while implementing this plan, where it was silent or where the
code departs from it. The code is `src/pdf_extract/seeding/`, the `ask` prompt
`classifiers/seed_ask.py`, the skill `.claude/skills/seed-parishes/SKILL.md`,
the drafting skill `.claude/skills/draft-parish-seed/` (with its `rules.md` and
`file-format.md`), and the labeler's `views/SeedPage.tsx` and `lib/seeds.ts`.

### Commands

- **`seed start <parish>`** starts a parish's file: a `drafting` draft listing
  its bulletins, none read yet. `extract` and `ask` start one the same way when
  the parish has none, so a call always has a file to be recorded in. `init`
  is its old name, kept as an unlisted alias that ignores `--resume`.
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
- **`seed start` prints `seed brief`**, so a draft starts from one command.
  On a parish that has a file already it resumes it, leaving its bytes
  unchanged, and says so; approved files cannot be resumed. `pick --resume`
  includes unfinished drafts. The brief's history leaves out dated events before the
  newest bulletin's fetch date (outside a seed's scope), and folds an event
  that recurs with different notes or pages into one row.
- **Matching history to slots** (`seeding/coverage.py`), for `finalize`'s
  history sources and `seed diff`: the same event type, start time and
  church (when the entry names one); a weekly event the same weekday of a
  weekly entry; a dated event the same date, or the weekday of a weekly entry
  unless it is a cancellation. Season, weeks of the month and end times are
  not compared. History of a bulletin extract mode flagged as wrong is left
  out. `seed diff` also leaves out dated events before the seed's `as_of`
  date, and a cancellation of a weekly slot the file leaves out.
- **History sources** come from the bulletins with a stored PDF (the newest
  4 when the blob store can't be listed), one per matching event, and never
  for a bulletin the slot already cites in a history source, so `finalize`
  can run again. Their `said` is the event as `seed history` prints it.
- **`bulletins` in a source** is shorthand for drafting only: `finalize`
  expands it, and `seed check` rejects a file that still has it, so the
  stored format, the loader and the labeler never see it.
- **A forgotten `--eval`.** A command that needs a parish's file (`mark-read`,
  `diff`, `finalize`, `check` of named parishes), run without `--eval` when only
  a test run has a draft of the parish, names that run ("did you mean --eval
  RUN?"). `start` warns instead, since a test run's parish may be seeded for
  real.
- **`seed questions`** lists every question in the seed files (a group once),
  with its options, the leaning, the answer and how it relates to the leaning
  (`leaning`, `other`, `dropped`, `edited`; a drop counts as matching a
  leave-out leaning), and the rule and candidate IDs (`R12`, `C3`) its
  rationale cites. Each answered question says whether a person or an agent
  answered it (`answered_by`, from a `by` starting `agent:`); the text lists
  agents' answers last, under their own heading, and `--by agent|person`
  picks one kind.
- **`seed approve <parish> --reviewer agent:NAME@COMMIT [--answers FILE]`**
  is an agent reviewer's approval (`review.approve_seed`). The answers are a
  JSON list of `{"slot", "choice", "entry", "page"}`, `-` for stdin; other
  keys are ignored, so the factory passes `seed-review`'s answers on as they
  are. An option's index or `dropped` answers the slot's whole open group, as
  in the labeler; `edited` (with `entry`, and `page` if it changes) answers
  the slot alone. It then saves through the labeler's save, under its lock.
  It refuses a reviewer not starting `agent:`, a file missing, `drafting`,
  `approved` or `blocked`, an answer to a slot that isn't an open question,
  an option that can't settle every slot of its group, and questions still
  open after the answers (naming their slots). It has no `--eval`: test runs
  are scored, not approved.

### The file

- **Explicit reading.** `seed mark-read <parish> <bulletin>` records reading
  without requiring a slot citation. `finalize` preserves these marks and
  also marks cited bulletins; merely downloading a PDF does not mark it read.
- **Evidence checks.** `seed check` enforces rules.md's R1 and its explicit
  exceptions: an assessed parish website schedule (R6), older read bulletin
  evidence for monthly or future dated entries (R12/R19), and an established
  weekly schedule retained after one omission (R36). These exceptions have a
  null slot page rather than a manufactured newest-bulletin sighting. R2 still
  requires the newest listed bulletin to be marked read; historical evals
  reject website sources (R5). A reviewer's answer may include an older candidate.
- **Batch failures.** `check --all` and multi-parish `finalize` report malformed
  files individually and continue with the other parishes.

- **Every key is present** in the file, slot and option, as in the labels.
  Entries have 24-hour `HH:MM` times (what the labels and the scorer use).
- **An answer** is `{"choice", "by", "at"}`: `choice` is the option's index,
  `edited` (the reviewer's own entry), or `dropped` (the slot left out). An
  excluded slot keeps an entry for review: its own, or else the option the
  agent leaned to, or none when neither has one. Only an included slot must
  have an entry.
- **Only included entries must be the parish's churches.** A slot left out,
  or an option, may name a chapel elsewhere, so the agent can record what it
  left out as it is.
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
- **Reopening** (`r`) turns a settled slot into a question, Include or Leave
  out, with its current decision as the leaning answer, or its earlier options
  if it had them.
- **One save at a time.** Each save sends the whole file, so the page waits
  for one to finish before taking the next action, and the server saves one
  review at a time. A file too malformed to show comes back as its problems
  only.

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
- **The loader's checks** omit the comparison of the file's bulletins with
  the database's and trust already-approved evidence. Current drafting checks
  still apply before new approvals, but must not prevent older approved seeds
  loading. Entry validity, duplicate slots, scope and file shape remain checked.
  A sighting is written only when the newest read bulletin is in the database.
- **The run report** has a Seeds section: what loaded and what was skipped.

### Test runs

- **`seed pick --labeled --eval RUN`** writes `data/seed-evals/RUN/run.json`:
  each labeled parish (a label marked done) with the fetch time of its newest
  labeled bulletin, the cutoff. A run keeps its manifest once written;
  `--resume` also offers unfinished drafts. Every parish command, including
  `church`, takes `--eval RUN`, reading and writing drafts in
  `data/seed-evals/RUN/seeds/` and hiding bulletins fetched after the cutoff.
  Live website sources are forbidden, and `seed check` requires `as_of` to
  be the cutoff.
- **`seed score RUN`** writes `report.md` and `report.json` beside the drafts.
  Settled precision is reported at the eval report's strict and core levels.
  A leaning answer matches when its entry pairs with a row the label wants
  (required, or optional and preferably included), or, when it leans to
  leaving the slot out, when no option pairs with a required row. It also
  counts settled slots left out that a required label row the settled slots
  miss matches.

