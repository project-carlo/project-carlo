# Plan: refactoring the onboarding factory

Status: plan only, written 2026-10-31 from the code at `40ae1478` (main) and the live
factory in `~/carlo-factory` (Wilmington, Philadelphia, Camden and Trenton in review;
Metuchen active, 6 of 29 batches mapped; six more dioceses queued). Reviewed once by an
agent against the code and the ledger; its corrections are folded in.

## 1. Goals and decisions

Goals:

1. **Structure.** Each kind of change has one obvious home (§3.3).
2. **Interpretability.** For any stage or past job you can see what the worker was given
   and what it was told to read, and a change to code-built prompt text shows up as a diff.
3. **Simplicity.** Less instruction text per worker, one statement of each rule, a smaller
   dispatcher core.

Non-goals: changing the stage order, models, Run semantics or the ledger's meaning;
parallel workers.

Decided (owner, 2026-10-31):

- **Playbook:** keep `integrate`, rewrite its brief, run it less often, and report section
  sizes; add a hard size budget only after one Run's data (Phase 3).
- **Rules settled:** `integrate` may condense it (merge duplicates, tighten wording),
  keeping each rule's decision and attribution; it never changes what a rule decides and
  flags apparent contradictions.
- **Order:** this refactor's Phases 1–4 land before the sandbox plan
  (`docs/factory-sandbox-plan.md`, #168) changes the dispatcher, so the sandbox code goes
  into the new `attempts.py`. One docs rewrite covers both (Phase 5).

Taken on the reviewer's advice (say if you disagree):

- **Prompt text stays in Python**, all of it in one module (`render.py`), not in
  `input.md` templates: the inputs are conditional, and templates in the Run's worktree
  would add a version-skew problem (§4).
- **No move of `factory/` files.** `factory/stages/<s>.yaml` and `factory/prompts/<s>.md`
  stay where they are, for the same reason.
- **Measurement code moves into `metrics/`; `backfill.py` is deleted.** The calibration
  gap stays (it is off by default).

## 2. What is wrong today

### 2.1 A stage is defined in about seven places

To understand or change `seed-review` you read `factory/stages/seed-review.yaml`,
`factory/prompts/seed-review.md`, `inputs.py` (`_seed_review_input`), `handoff.py`
(`SeedReview`, `read_handoff`, `schema_text`), `dispatcher.py` (`_seed_verdicts`,
`_decisions`, special cases in `_gate` and `_finish`), `plan.py` (`_next_seed`),
`workers.py` (`default_handoff`) and `quota.py` (`work_units`). Stage names appear as
string literals in 11 of the 20 modules.

### 2.2 `dispatcher.py` (1,218 lines) mixes six concerns

The tick loop and picking; account choice, quota readings and calibration; the attempt
lifecycle and resume prompts; gates, send-backs and blocking; reviewer verdicts, lessons
and precedents; issues, answers, follow-up Runs, merges, readiness and backups.

### 2.3 Settings and their effect are hard to trace

- Crash and failure limits, the retry wait and the 429 cooldown are constants in
  `dispatcher.py:96-100`; "continue once after a partial" is `continues < 1` (`:666`).
- `QUOTA_SETTLE_SECONDS` is in both `config.py` and `config.yaml`; `max_workers` in
  `config.yaml` is read by nothing.
- Three kinds of change take effect at different times, and nothing says so (§3.3).
- **Version skew.** Stage specs and prompts are read from the Run's worktree; the Python
  comes from `~/carlo-factory`. `load_stage` runs *before* `_merge_main`
  (`dispatcher.py:333` vs `:337`), so the first job of each stage runs with the
  pre-merge stage spec (model, tools, writes) but the post-merge prompt file.

### 2.4 What a worker is given is spread over many layers

The first message is built in code and stored per attempt (`pnpm factory inspect <job>
--prompt` prints it). Everything else the worker fetches because prose tells it to. For a
map job (148 attempts in the ledger):

| Layer | Source | Size | Used |
|---|---|---|---|
| Appended system prompt | `factory/prompts/map.md` | 4.4 KB | always |
| First message | `inputs.py` header, handoff schema, input | ~3 KB | always |
| Skill | `explore-diocese` | 8 KB | loaded in 101 |
| Skill | `parish-site-access` `SKILL.md` | 15 KB | read in 71; its scripts ran in 124 |
| "Read first" | `data/dioceses/README.md` | 34 KB | in 139, mostly `cat` of the whole file |
| "Read first" | the diocese's `diocese.md` | 13–61 KB | `cat` in full in ~130 |
| "Read first" | the Run's `tools/README.md` | 1–2 KB | most |

Instructions are roughly 17–28k of the ~95k tokens an average map turn carries; the rest
is working material. So a perfect prompt diet saves at most ~15–20% per turn, and the real
levers are the README (~9k tokens) and the playbook's publishers section (3–10k tokens).
Nothing shows the whole picture for a stage, or for a job that hasn't run yet.

### 2.5 The same rule is said in several layers

| Rule | Files |
|---|---|
| Judge transport, document type, identity, freshness separately | map.md, reconcile.md, explore-diocese, README |
| `--silent` when piping JSON | survey.md, explore-diocese, README |
| Don't infer shared pastors | survey.md, survey-review.md, explore-diocese |
| No `fill_record` writers | map.md, explore-diocese, README |
| Keep your context small | map.md, reconcile.md, survey-review.md |
| Scratch and tools folder paths | header, stage input, stage prompt (3× per job) |

The README's *Method* (6 KB) repeats explore-diocese. Map's header says the scratch folder
is `scratch/<run>/<job>/` while its `writes` allow `scratch/<run>/**`.

Text written for the Claude Code cloud sandbox reaches host workers: survey step 2 runs
`setup_browser.sh` (Chrome via `apt-get`, the agent proxy's CA), and `parish-site-access`
explains that setup.

### 2.6 The playbook isn't staying short

`integrate` exists so map jobs read "a short, current guide instead of a growing log".
470 lessons came from 138 map jobs (3.4 each), so with a threshold of 8 it ran 42 times
(about $0.58 a job, 11% of spend). The cost isn't the problem; the result is:

| Run | *Bulletin publishers here* | *Rules settled* |
|---|---|---|
| Philadelphia | 38 KB | 10 KB |
| Trenton | 24.5 KB | 11.2 KB |
| Camden | 19.6 KB | 9.0 KB |
| Wilmington | 13.5 KB | 5.2 KB |

Most lessons are about one parish ("Bon Venture also serves Spotswood…"), and integrate
folds them in rather than dropping them. Its brief forbids touching an existing *Rules
settled* line, so that section only grows. `reconcile` step 7 repeats integrate.

### 2.7 Also

- Measurement (`quota.py`, `tokens.py`, `backfill.py`, the quota half of `report.py`, the
  reading code in the dispatcher) is ~1,300 of ~5,000 lines, interleaved with operation.
- `docs/factory-spec.md` still says the factory "has not yet run a real diocese"; the
  worker header points every worker at it.

## 3. Target design

### 3.1 Layout

```
factory/                       # unchanged places; read from the Run's worktree
  config.yaml                  # dispatcher policy (read from ~/carlo-factory at start)
  queue.json
  stages/<stage>.yaml          # + reads:, deny:
  prompts/<stage>.md

src/pdf_extract/factory/
  engine.py                    # tick, pick, attempt, gates, send-back, block; no stage names
  attempts.py                  # pending prompts: start, fresh, send-back, continue, resume, answer
  accounts.py                  # choosing an account against the caps, cooldowns
  answers.py                   # issues → answers → requeue, follow-up Runs
  housekeeping.py              # merged Runs, retire, readiness, backups
  render.py                    # every piece of worker-facing text code builds
  spec.py                      # stage spec loading (today's stages.py)
  stages/                      # behaviour of the stages that have any (§3.2)
    map.py  seed.py  survey_review.py  seed_review.py  code.py
  plan.py  ledger.py  git.py  forge.py  playbook.py  config.py  cli.py
  metrics/                     # quota, tokens, readings, attempt_meta, quota reports
```

`render.py` holds the header, each stage's input, the handoff schema text, and the
send-back, continue, resume and answer prompts, plus the texts of gate and handoff
problems that go back to workers. Rendering is pure: it reads the ledger and the files and
writes nothing.

### 3.2 Stage behaviour

Only five stages have behaviour beyond "run the agent, run the gates, commit": map,
seed, survey-review, seed-review, and the code stages (promote, pr). Each gets a module of
plain functions; a stage without a module gets the defaults. The hooks, from today's
branches in `dispatcher.py`:

| Hook | Default | Who overrides it (today's code) |
|---|---|---|
| `handoff` model | `Handoff` | survey-review, seed-review (`handoff.py:80`) |
| `can_park` | false | map, seed (`PARKING_STAGES`) |
| `check(handoff)` | none | seed-review coverage (`_coverage_problems`) |
| `skip_gates(handoff)` | false | seed parking itself (`:704`); seed-review (`:707`) |
| `on_done(handoff, services)` | none | map lessons → playbook (`:879`); survey-review verdict and rules (`:914`); seed-review approvals, decisions, precedents (`:942`) |
| `gates_after_done` | false | seed-review: gates run after approvals; a failure commits them and blocks (`:830`) |
| `on_exhausted` | block the Run | seed parks its parish (`:771`) |
| `answer_input(flag)` | n/a | map and seed requeue shapes (`:1125`) |
| `merges_main` | true | pr skips; map re-promotes after a merge (`:349`, `:360`) |
| `run_code` | n/a | promote, pr (`:1015`, `:1030`) |
| `work_units`, `stub_handoff` | 1, `done` | map, seed, seed-review |

`on_done` gets an engine services object (send back or exhaust another job, run a command,
commit), because reviewers act on the job they reviewed. Seed stages have never run live
(no seed Runs in the ledger): their part of the refactor rests on the stub tests.

### 3.3 Where a change goes, and when it takes effect

| You want to change… | It goes in | Takes effect |
|---|---|---|
| What one stage is told to do | `factory/prompts/<s>.md` | next stage start after merge to main |
| Model, effort, tools, limits, write scope, required reads, denied commands | `factory/stages/<s>.yaml` | same |
| How to research a diocese or seed a parish (shared with your sessions) | the skill | same |
| Record formats and field rules | `data/dioceses/README.md` (reference, not method) | same |
| The queue | `factory/queue.json` | next fetch after merge |
| A number: caps, retries, send-backs, lesson threshold, cooldowns | `factory/config.yaml` | pull `~/carlo-factory`, restart |
| What a stage's first message or resume prompts say | `render.py` | pull, restart |
| What happens to a stage's output | `stages/<s>.py` | pull, restart |
| The stage order, or a new stage | `plan.py` (+ spec, prompt, module) | pull, restart |
| Retry, crash, gate or resume mechanics | `engine.py`, `attempts.py` | pull, restart |
| How quota and tokens are measured | `metrics/` | pull, restart |

This table moves into `docs/factory.md` (Phase 5).

### 3.4 Seeing what a worker gets

- `stages/<s>.yaml` gets `reads:`, the files the worker must read first, replacing
  "read X first" prose. Entries may name a section:
  `data/dioceses/README.md#Fields`. The header renders the list.
- Small, computed context (playbook sections, precedents, leads) is inlined by code.
  Large or bulky context (the README sections, reconcile's flags and leads list) is a
  read or a file in the job's scratch folder.
- `pnpm factory prompt <stage> --run R` previews a job that hasn't run: the appended
  system prompt, the first message, the skills, and each read with its size in tokens.
  It opens the ledger read-only.
- `pnpm factory inspect <job> --prompt` adds the same breakdown for a past attempt
  (stage files from its `commit_sha`).
- Golden tests cover the text code renders (header, each stage's input from a fixture
  Run, the schema, the resume prompts), not `prompts/*.md`, so a prompt edit isn't shown
  twice in its PR.

### 3.5 One home per rule

- `data/dioceses/README.md`: the data model and file format. *Method* moves out.
- Skills: the method, shared by workers and your own sessions. Cloud-sandbox setup moves
  out of what workers read.
- Stage prompts: only the stage's scope, what it may write, what it hands off, and how it
  differs from the skill.
- Header (code): what every job shares, said once.

## 4. Compatibility: every change lands mid-Run

Six dioceses are queued behind Metuchen, so some Run is always active, and a Run merges
main at every stage start (each integrate counts), so a change reaches it within about
3–4 map jobs. Every phase follows these rules:

- The dispatcher's Python works with the stage specs and prompts of a Run worktree that
  hasn't merged the change yet. New spec keys default to today's behaviour.
- No `factory/` file moves or renames. (`_record_meta` hardcodes the spec path,
  `dispatcher.py:648`; `load_stage` would fail in an old worktree, which counts as a
  transient failure and blocks the Run after three.)
- Phase 1 moves the merge before `load_stage`, so a job always runs with the spec and
  prompt of the same commit.
- Python changes: `pnpm factory pause`, wait for the running job, pull `~/carlo-factory`,
  restart the service, `pnpm factory resume`.

## 5. Phases

Each phase is one PR (Phase 4 is two), passes `uv run pytest` and a stub Run
(`pnpm factory run --stub`), and follows §4.

### Phase 1: render, compatibility, settings (no worker-visible change)

- `render.py`: move the header, inputs and resume prompts out of `inputs.py` and
  `dispatcher.py` unchanged. Move lead claiming (`inputs.py:163-167`) into the engine,
  before rendering, keeping a fresh worker's leads stable.
- `prompt` command and the `inspect --prompt` breakdown (§3.4); golden tests.
- The config fingerprint adds a hash of the rendered header and input template, the
  skills' contents, `reads:` and the dispatcher's commit, so before/after comparisons see
  code-built text too (today it covers only the spec, prompt file and skill names,
  `quota.py:448`).
- Merge main before loading the stage spec.
- `config.yaml`: `max_crashes`, `max_failures`, `failure_retry_minutes`,
  `usage_cooldown_minutes`, `max_continues`, defaults as today. Remove
  `QUOTA_SETTLE_SECONDS`'s duplicate and the unused `max_workers`.
- Done when `pnpm factory prompt map --run metuchen-map-1` prints the next map job's
  input and leaves the ledger unchanged, and golden tests pass on unchanged output.

### Phase 2: prompt diet (changes what workers read)

- Add `reads:` (default empty) and `deny:` (default empty, passed to `disallowed_tools`
  alongside `DENIED`).
- Map reads only the README's *Fields*, *Structured writes and bounded research*, *Traps*
  and *The explanation* (~14 KB instead of 34 KB); the playbook sections it needs
  (*Bulletin publishers here*, *Rules settled*, *New lessons*) are inlined, and it stops
  reading all of `diocese.md`. Other stages get `reads:` for what their prompts tell them
  to read today.
- Remove restated method from the stage prompts (§3.5); say the folders once; print the
  handoff schema compactly; drop the pointer to `factory-spec.md`; fix map's scratch
  `writes`.
- Remove survey step 2 (`setup_browser.sh`) and move the cloud-only setup in
  `parish-site-access` out of the part workers read (confirm on the host that the
  browser scripts still run without it).
- Reconcile's advisory flags and leads (13 KB on average in its first message today) go
  to a file in its scratch folder.
- `deny:` only for paid or irreversible commands: seed-review's `pnpm seed extract`, `ask`,
  `approve`. Writes outside a reviewer's scratch folder are already reverted by the
  diff-scope gate, and prefix denies on writes are easy to sidestep.
- Expected: map instructions from ~17–28k tokens to ~10–14k; ~10% less context per turn.
  Measure the instruction tokens from the `prompt` command's sizes; guard against
  regressions with the send-back rate and gate failures on the next batches (cost per
  batch varies too much between dioceses to compare).

### Phase 3: keep the playbook short (changes integrate and map)

- Rewrite integrate's brief: the playbook is a guide, not a log; one parish's detail is
  dropped (it is in the records); it may condense *Rules settled* as decided in §1.
- Integrate's input gives each section's current size and a target (publishers ~8 KB,
  rules ~6 KB). Reconcile's summary and the PR report the final sizes.
- Tighten map's lesson guidance: a publisher's method or a decision for several records,
  never one parish's detail.
- Raise `lessons_before_integrate` from 8 to 15.
- Remove reconcile's step 7; the plan schedules a last `integrate` before `reconcile`
  when *New lessons* is non-empty.
- After the next full Run: decide on a hard budget gate from its sizes.

### Phase 4: stage modules and the engine split (no worker-visible change)

- Commit 1, mechanical moves: split `dispatcher.py` into `engine.py`, `attempts.py`,
  `accounts.py`, `answers.py` and `housekeeping.py`; rename `stages.py` to `spec.py`.
  `Dispatcher` stays as a thin facade so `cli.py` changes little.
- Commit 2: the stage modules and hooks (§3.2); `PARKING_STAGES`, `MODELS`,
  `default_handoff` and `work_units` move into them.
- Ledger keys (`approved:<job>`, `failures:<job>`, `set_up:<run>`, action names) keep
  their names, so a ledger written before the refactor resumes after it.
- Tests that reach into the dispatcher (`test_factory.py:874` `_seed_verdicts`;
  `:1623`, `:1829` `USAGE_COOLDOWN`, `AFTER_READING_WAIT`) are updated; add a stub
  scenario for a whole seed Run if the suite lacks one.
- Done when no stage name appears in `engine.py`.

Then the sandbox plan's dispatcher phases (#168), with their code in `attempts.py` and
their per-stage `secrets:` key in the stage specs.

### Phase 5: metrics package and docs

- Move `quota.py`, `tokens.py`, the usage readings, `_record_meta`, `sample_quota` and the
  quota reports into `metrics/`. Delete `backfill.py` and its CLI command.
- One docs rewrite, together with the sandbox plan's docs phase: replace
  `docs/factory-spec.md` with `docs/factory.md` (~150 lines: goal, pipeline, vocabulary,
  §3.3's table, how to run it) and `docs/factory-quota.md` (the measurement design).
  Update the pointers in the foreman and explore-diocese skills.
