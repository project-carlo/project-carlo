# Onboarding factory: specification (draft)

Status: draft, being worked through section by section. Decisions settled in the design
session are stated plainly; proposals not yet agreed are marked **Proposed**; open
decisions are in [Open questions](#open-questions).

## 1. Goal

Agents take a diocese from nothing to fully seeded parishes, ready to go live, without a
person in the loop. Each piece of work is a job, small enough for one agent, run by a fresh
worker. Code decides what runs next. A person works only through the dashboard, GitHub
issues, foreman reviews and the final PR.

Out of scope for now: leads from other sources (an eCatholic site dump, for example).
The diocese is the unit of work because its roster is what coverage, exclusions and
batching depend on. See [Deferred](#deferred).

## 2. Vocabulary

| Term | Meaning |
|---|---|
| **Run** | One diocese moving through the pipeline: one branch, one worktree, one PR. |
| **Stage** | A kind of work (`survey`, `map`, `seed`, ...), defined by a versioned stage spec. |
| **Stage spec** | A stage's contract: input, model, skills, tools, write boundaries, gates, handoff, retry policy. |
| **Job** | One run of a stage on one input, such as "map batch 3 of Wilmington" or "seed St. Paul". Agent jobs have a worker; code jobs don't. |
| **Worker** | A fresh Agent SDK session that runs one job and ends. It can't start other agents. |
| **Gate** | A code check the dispatcher runs after a job. The worker's own report is never enough. |
| **Handoff** | The JSON a worker writes at the end of its job. |
| **Flag** | A structured request for a decision, either **blocking** or **advisory**. |
| **Parked** | A parish set aside by a blocking flag. The rest of its Run carries on. |
| **Triage** | The agent that resolves flags, turns them into follow-up jobs, or escalates them to a GitHub issue. |
| **Reviewer** | A stage that judges another stage's work (`survey-review`, `seed-review`, `pr-review`). |
| **Foreman** | A skill you run by hand to review a job or a stage and suggest improvements (§9). |
| **Dispatcher** | Code, not an agent. It picks ready jobs, checks usage, starts workers, runs gates, retries. |
| **Ledger** | SQLite state: Runs, jobs, attempts, sessions, worker steps, costs, spec versions, flags. |
| **Queue** | `factory/queue.json`, the ordered list of dioceses waiting for a Run. |

## 3. The pipeline

```
survey ─▶ survey-review ─▶ ┌ map ─▶ seed × each parish ─▶ seed-review ┐ × one per batch
                           │  integrate after batches 3, 8, 18, then every 10 │
                           └──────────────────────────────────────────────────┘
       ─▶ reconcile ─▶ fetch-check ─▶ promote ─▶ open PR ─▶ pr-review ─▶ (you merge)
```

- A Run has **at most one active job**. Batches inside a diocese run one at a time, so
  each map batch starts from the playbook the earlier ones built. To scale, run more Runs
  at once.
- Within a batch, the `map` job comes first, then one `seed` job for each parish it
  mapped, then one `seed-review` job for the batch's seeds. A parish the map job excluded
  or left open gets no seed job.
- `integrate` runs less often as the diocese goes on: after batches 3, 8 and 18, then
  every 10, and its work is done once more in `reconcile`. Early batches teach the most.
- `factory/pipeline.yaml` sets the stage order, the batch loop and the integrate schedule.
  Stage specs don't refer to each other.
- Jobs pass work to each other **only through files and git**: records, seeds,
  `diocese.md`, `batches.json` and handoffs. Never through messages.

### Stages

| Stage | Kind | Model | Does | Gates |
|---|---|---|---|---|
| survey | agent | Opus, high | `init`, rosters, `diocese.md` intro and sources, `batches.json` (today's `diocese-surveyor`) | `batches validate`, `diocese validate` |
| survey-review | reviewer | Opus | Checks grouping, exclusion reasons and proposed rules | none |
| map | agent | Sonnet, high | Maps about 4 parishes: bulletin source, churches, exclusions and open records (today's `parish-scout`) | `diocese validate` |
| seed | agent | Sonnet, high | Drafts one parish's seed from its bulletins (§12) (today's `seed-drafter`) | `seed check` |
| seed-review | reviewer | Opus | Approves the batch's seeds or sends them back, answering questions by `rules.md` | `seed check` on approved files |
| integrate | agent | Opus | Merges *New lessons* into the playbook in `diocese.md` (§3, Integrating) | `diocese validate` |
| reconcile | agent | Opus | `coverage --link`, `audit --fetch`, peer `publication_reviews`, merges across batches, a last integrate | `batches validate`, `diocese validate` |
| fetch-check | agent | Sonnet | `fetch:check --diocese`, reports rows that aren't this week's issue | none |
| promote | code | none | `promote --dry-run`, `promote`, `uv run pytest`, lint, commit | its own exit codes |
| pr-review | reviewer | Opus | Reviews the PR, writes the summary and a spot-check sample | none |
| triage | agent | Opus | Sorts flags (§7) | none |

The model is a field in the stage spec. A foreman review can suggest changing it, like any
other field.

### Integrating what batches learn

What a map job learns reaches later batches in three ways:

- **Leads** go through code. A handoff lead names the batch or roster entry it touches,
  and the dispatcher adds it to that batch's job input.
- **Lessons** are appended by the dispatcher, as written, to *New lessons* in
  `diocese.md`, which every later map job reads. `integrate` merges them into *Bulletin
  publishers here* and *Rules settled*, keeps only what's reusable, and empties the list.
- **Fixes across batches** (a merge, a church that belongs to another parish) are raised
  as advisory flags and handled by `reconcile`. If a merge touches a parish that already
  has a seed, that seed goes back to the `seed` stage.

Lessons from `seed` jobs don't go into `diocese.md`. They stay in the ledger for foreman
reviews.

## 4. Stage spec

One file per stage, `factory/stages/<stage>.yaml`:

```yaml
stage: map
kind: agent                    # agent | reviewer | code
model: claude-sonnet-5-5
effort: high
input:                         # JSON schema of the job input
  run: string
  diocese: string
  batch_id: string
  parishes: [{ ref: "<roster>:<id>", name: string, town: string }]
  leads: [string]
skills: [explore-diocese, parish-site-access]
tools: [Bash, Read, Edit, Write]
writes:                        # globs; enforced by hooks and the diff-scope gate
  - data/dioceses/{diocese}/**
  - scratch/{run}/{job}/**
gates:
  - pnpm --silent diocese validate {diocese}
limits: { max_turns: 300, max_minutes: 90 }
retry: { usage_limit: resume, crash: resume, partial: resume_once, gate_fail: send_back }
send_back_limit: 2             # shared by gate failures and reviewer send-backs
```

**Spec version** = a hash of the stage file plus every skill file and agent prompt it loads.
Every job records the version it ran on and the commit it ran at, since the CLI and its
checks change results as much as the skill text does.

### Gates every agent job gets

- **Handoff gate.** The handoff exists and matches the schema.
- **Diff-scope gate.** Every changed path matches `writes`. PreToolUse hooks block
  out-of-scope `Edit` and `Write` calls as they happen, and this gate catches what slips
  through `Bash`.
- **Reviewer-scope gate** (reviewers only). In a seed file, a reviewer changes only what
  `seed approve` writes: `reviewer`, `approved_at` and its answers to open questions.

### Handoff

`scratch/{run}/{job}/handoff.json`, about 300 tokens:

```json
{
  "status": "done | partial | blocked",
  "summary": "one or two sentences",
  "changed": ["paths"],
  "flags": [{
    "severity": "blocking | advisory",
    "scope": "parish | run",
    "subject": "roster:id or parish slug",
    "question": "what needs deciding",
    "evidence": ["path#section or URL with date"],
    "suggestion": "what the worker would do"
  }],
  "leads": [{ "touches": "batch id or roster:id", "note": "..." }],
  "lessons": ["reusable publisher or rule lesson"]
}
```

Reviewers add `"verdict": "approve | send_back"` and, for a send-back, `"problems": [...]`.

## 5. Dispatcher

A long-running Python process on the Claude Agent SDK, on this machine. Python, because
everything it calls is Python: the `diocese` and `seed` CLIs, the blob store, `pytest`.
Each tick:

1. **Usage.** For each account in the pool, it reads
   `GET https://api.anthropic.com/api/oauth/usage` with that account's Claude Code login
   token, the call T3 Code makes. This endpoint isn't documented, so the response shape
   needs checking and could change. An account can take a new job only while it's under
   both of its limits:
   - **5-hour:** below `five_hour_cap` (default 75%);
   - **weekly, paced:** below `weekly_cap × (days into the week + 1) ÷ 7` (default cap
     70%), so the factory can't use up the week early but can still work on its first day.

   **Failing safe.** If the endpoint fails or returns a shape the dispatcher doesn't
   recognise, it starts no new jobs until the endpoint works again. Running jobs carry on.
   A rate-limit error from the SDK is the backstop: that job becomes `waiting_usage`
   whatever the endpoint said.

   Both accounts currently share with your own sessions, so both use the defaults.
   If no account is eligible, it waits for the earliest reset. `pnpm factory pause` and
   `resume` override this.

   **Account pool.** Each account has its own config directory (`CLAUDE_CONFIG_DIR`),
   which holds its login and session transcripts, and its own caps. A new job goes to the
   eligible account with the most headroom, and **stays on that account** for its whole
   life, because it can only be resumed from where its transcript is stored.
2. **Concurrency.** It starts jobs until `max_workers` (1–2 for now) are running. A free
   slot goes to a ready job in an active Run first; it starts a new Run from the queue only
   when no active Run has a job ready. Finishing dioceses comes before starting new ones.
3. **Start a job.** It merges `origin/main` into the Run branch so the worker gets the
   latest specs and data (§10), then runs `query()` with the stage spec in the Run's
   worktree (Worker setup, below). It stores the session id, the transcript, the cost and
   each step the worker takes.
4. **Finish a job.** It runs the gates, then:
   - all pass → commit with a `Factory-Job: <id>` trailer, push the branch, route the
     handoff's leads and lessons (§3), queue the next job;
   - a gate fails → resume the same session with the exact errors, up to `send_back_limit`,
     then raise a blocking flag;
   - usage limit hit → job becomes `waiting_usage`, and the same session resumes after the reset;
   - crash → resume the session; `partial` → resume once with "continue", then a blocking flag;
   - over `max_minutes` → stop the session and treat it as `partial`.
5. **Flags.** Advisory flags are stored for the PR. A blocking flag about a parish
   **parks** that parish: its open record stays, the flag goes to triage, and the Run
   carries on with the next job. A blocking flag about the Run (a bad survey, a merge
   conflict, a gate the worker can't pass on shared files) pauses the Run.
6. **Promote lock.** Only one `promote` runs at a time across all Runs, because it writes
   the shared `parishes.csv` and `churches.csv`.
7. **Budget.** Each Run has a usage budget, counted in percentage points of the weekly
   limit. A Run that reaches it pauses with a Run-level flag.

Job states: `queued → running → (gating) → done`, plus `waiting_usage`, `sent_back`,
`blocked` and `failed`. A Run is `active`, `blocked`, `in_review` or `merged`. A parish in
a Run is `waiting`, `mapped`, `seeded`, `approved`, `excluded`, `open` or `parked`.

CLI: `pnpm factory status | queue | run | pause | resume | retry <job> | inspect <job> |
cost [--stage] | rebuild | dashboard`.

### Worker setup

- **Worktree.** Each Run's worktree has its own copy of the database, its own
  `node_modules`, and its own Chrome profile and xvfb display for `parish-site-access`, so
  two workers never share a browser.
- **Isolation.** Workers read untrusted parish websites and have `Bash`, so a worker
  starts with an environment that holds no R2 write keys and no GitHub token. Only the
  dispatcher commits, pushes, opens PRs and writes to R2. The diff-scope gate catches
  stray files, and these limits cover what it can't: pushing, calling `gh`, or reading
  keys.

### Dashboard

`pnpm factory dashboard` serves a local page from the dispatcher, separate from the
labeler. It reads the ledger and refreshes every few seconds:

- **Accounts:** each account's 5-hour and weekly use against its caps and the weekly pace.
- **Waiting on you:** escalated issues, PRs ready to merge with their spot-checks, and
  anything paused.
- **Runs:** each Run's stage, batches done, and its parishes by state.
- **Workers:** each running job, its account and model, how long it has run, and its
  latest step.
- **Recent:** gate failures, send-backs, flags and finished jobs.

It is read-only apart from Pause and Resume.

## 6. Ledger and storage

- `data/factory/factory.db` (SQLite, gitignored, on the Linux filesystem, not under `/mnt/c`).
- Transcripts and handoffs go in `data/factory/runs/<run>/<job>/`, also gitignored.
- **Nightly backup** with SQLite `.backup`, uploaded to R2.
- **Durability.** Work exists in git, and every job pushes its branch. Run and job state can be
  rebuilt from the `Factory-Job` commit trailers (`factory rebuild`). Losing the database
  loses only history, costs and transcripts, which only foreman reviews need.
- `factory/queue.json` is committed: an ordered list of `{ diocese, notes }`. A one-off
  agent session edits it. The dispatcher starts the first diocese that has no Run.

## 7. Flags, triage and the inbox

- Flags are either **blocking** or **advisory**. A blocking flag parks its parish, or
  pauses the Run when it's about the Run (§5). An advisory flag lets the Run continue; the
  parish is left open or excluded with a reason, and the flag is listed in the PR.
- **Triage** picks up each flag and does one of three things:
  1. **Resolves** it with an existing rule or a playbook entry, by resuming the job or
     queueing a follow-up.
  2. **Turns it into a follow-up job**: a retry after a reset, or another method.
  3. **Escalates** it as a **GitHub issue** with labels `factory`, `run:<diocese>` and
     `stage:<stage>`, holding the question, the evidence and the suggestion.
- You answer by commenting and closing the issue. The dispatcher sees it closed and
  resumes the blocked job with your answer:
  - your last comment is the answer;
  - closing with no comment accepts the issue's suggestion;
  - only comments from your GitHub login count, since the answer becomes part of an
    agent's prompt. The same applies to `/overrule` comments (§11).
- A parked parish whose issue is answered gets its job queued again. If the Run has
  already passed that stage, the job runs before `reconcile`, or before `promote` if
  `reconcile` is done.

## 8. Reviewers

A reviewer **never edits the work it reviews**. It can:

1. **Approve**, writing only its verdict and its answers to open questions;
2. **Send back** to the worker's session with specific problems, which counts against
   `send_back_limit`. The dispatcher resumes that session on the account it ran on. If it
   can't be resumed, a fresh worker of the same stage gets the problems and the files
   already on disk;
3. **Flag**, which goes to triage.

`seed-review` approves with `pnpm seed approve` (§12), which records
`agent:seed-review@<spec version>` in the seed's `reviewer` field, plus `approved_at`.
When it answers a question against the drafter's lean, that is recorded for foreman
reviews.

## 9. Foreman

A foreman is a **skill you run by hand**, not a standing agent. You ask it to review a job,
a stage's recent jobs, or a Run, and it tells you what went wrong and how to improve it.

- **Context.** `pnpm factory inspect <job>` prints everything about a job in one place:
  its stage, spec version and commit, its input and handoff, its gate results, every
  attempt and send-back, what later stages said about its output (reviewer verdicts,
  triage resolutions, your issue answers and overrules), its cost and the path to its
  transcript. The skill starts from that and reads the transcript selectively.
- **What it looks for.** Where the job went wrong in the transcript, and why: the skill
  text, the agent prompt, the CLI, the model, the job's input, or the source itself (a
  publisher no instructions could have handled). Repeated work, wasted turns and
  instructions the worker ignored or misread are as useful as outright errors.
- **What it gives you.** What went wrong, the evidence, and concrete changes to the stage
  spec (skill, agent prompt, CLI or model), most useful first. It changes nothing unless
  you ask; when you do, it opens a PR against the spec, and you merge it.
- **No measuring for now.** There is no trusted way yet to show a spec change helped, so
  a foreman review gives reasons, not scores. Spec versions are still recorded, so you
  can see which version each job ran on.

## 10. Git and PRs

- One branch per Run (`factory/<diocese>`) in its own worktree. Each job ends in a
  commit with a `Factory-Job` trailer, then a push.
- Before each job, the dispatcher merges `origin/main` into the Run branch. This keeps
  specs current and the PR mergeable. A merge conflict raises a Run-level blocking flag,
  except in `parishes.csv` and `churches.csv`: there a code job takes main's version and
  runs `promote` again.
- At the end: one PR per diocese. `pr-review` writes the summary: coverage numbers,
  advisory flags, parked parishes, lessons for every diocese, and a random sample of agent
  approvals to spot-check.
- **You merge.** Auto-merge comes later (§11).

## 11. Autonomy ladder

Every decision a reviewer or triage makes is recorded. You spot-check a sample until
its record supports letting it decide alone. Then the check is removed.

**Recording an overrule.** You comment on the PR with
`/overrule <parish> <slot id>: <reason>` (or `/overrule survey: <reason>`). The dispatcher
reads these comments, records each one against the reviewer's decision, and sends the
fix back to the worker that wrote it. The reason also appears in foreman reviews of that
stage.

| Step | Now | Later |
|---|---|---|
| Merge | You merge after `pr-review` | Auto-merge when gates and `pr-review` pass |
| Seed approval | `seed-review` approves; you spot-check from the PR | No spot-check |
| Survey | `survey-review`; you spot-check the first few | No spot-check |

## 12. Seeding changes

New parishes have no rows in the database until after merge. Instead of giving every
`seed` command a second source, **a seed carries its own bulletins**, and the database
learns about them when the seed loads.

- **The seed's bulletin list.** Each entry in a seed's `bulletins` has the content hash,
  source URL, issue date, `fetched_at`, how it was obtained (`fetch`, `backfill` or
  `by hand`) and `read`. The PDFs are stored by hash, under the blob store's usual keys
  (`bulletins/<parish>/<hash>.pdf`).
- **`seed start` builds the list.** It's the only command that works differently for a
  new parish:
  - a parish in the database: from its bulletin rows, as today;
  - a new parish: from `pnpm fetch --parish X --backfill 4`, which downloads up to 4
    recent issues into the Run bulletin folder through the fetcher's publisher adapters
    and writes nothing to the database or R2; and from `pnpm seed add-bulletin <parish>
    <url|file>`, for an issue the worker found by hand. Its name, website and churches
    come from the diocese records.

  Every other command (`pdf`, `text`, `pages`, `grep`, `mark-read`, `slot`, `finalize`,
  `check`) works from the list and the PDFs. `history` and `diff` show extracted history
  when the parish has some, and say there is none otherwise.
- **Run bulletin folder.** `data/factory/runs/<run>/bulletins/<parish>/<hash>.pdf`
  (gitignored). Blob reads look there first.
- **How many bulletins.** At least one. The worker reads the newest issue in full and reads
  older ones only when it's unsure. A missed first-Friday service is acceptable: weekly
  update mode will find it. Rewrite the rules to match: R7–R9 apply only when there is
  extracted history, and R35 and R36 become tools the drafter may use, not requirements.
- **`as_of` and the seed's week.** `as_of` stays the time the newest read bulletin was
  fetched (for a new parish, when the Run downloaded it). `finalize` also records the
  seed's `week`, the Sunday of the newest read issue.
- **Update mode** changes in two places:
  - a bulletin is read when it was fetched after `as_of`, has no successful call, **and
    isn't in the seed's list**. Today the first weekly fetch reads the seed's own newest
    issue again;
  - the parish's starting mark is the seed's `week`, stored on its seed revision, instead
    of a search for rows fetched on or before `as_of` (`seed_mark`).
- **Loading happens in one place.** Approved seeds load in the weekly run (after its
  before-copy, as now) and with `pnpm seed load`, not as a side effect of every pipeline
  command. Loading adds a `bulletin` row, marked as coming from a seed, for each listed
  bulletin the database lacks, so sightings and evidence links resolve. Check that the
  weekly run's change gate doesn't hold the snapshot when a whole diocese of new seeds
  loads at once.
- **Checks** compare a seed with its own list and PDFs. For a parish in the database, they
  also confirm the listed bulletins are that parish's.
- **Agent approval command**: `pnpm seed approve <parish> --reviewer agent:...`, which
  does what Seeds mode does for a person and writes only `reviewer`, `approved_at` and the
  reviewer's answers.
- **After merge**, the dispatcher uploads the PDFs that approved seeds list to R2 under
  their usual keys, so the evidence can still be read later. This code step is the only
  place this machine uses R2 write keys. Agents never do.
- **Existing seeds.** A one-off migration fills in the new list fields and `week` for the
  seeds in `data/seeds/` from the database.

## 13. What carries over

- `explore-diocese`, `draft-parish-seed` and `parish-site-access` become stage skills.
- `diocese-surveyor`, `parish-scout` and `seed-drafter` become the prompts for the
  `survey`, `map` and `seed` stage specs.
- `map-diocese` and `seed-parishes` are the orchestrators the factory replaces. Keep
  them for manual sessions until the factory has proven itself, then retire them.
- New: a `foreman` skill (§9).

## 14. Build order and pilot

The plan is a thin version of everything first: get one Run through end to end, then
improve it.

- **Phase 0, seeding and CLI:** the seed's own bulletin list, `--backfill` into the Run
  folder, `add-bulletin`, `seed approve`, `seed load`, the update-mode changes, the
  migration of existing seeds, and the rules rewrite (§12).
- **Phase 1, thin pipeline:** dispatcher, ledger, stage specs for every stage, gates,
  usage check, resume, worker setup, the dashboard, `factory inspect` and the foreman
  skill. Triage off: flags go straight to issues.
- **Phase 2:** triage on, after the first Run merges.

**Shadow pilot: Diocese of Erie** (61 parishes, mapped with today's batch method). A code
step makes a throwaway branch from main with Erie removed: its diocese folder, its seeds
and its rows in `parishes.csv` and `churches.csv`. The factory runs on that branch with
PR creation and R2 uploads switched off. A compare script then reports where the result
differs from main: coverage, exclusions, bulletin sources, and seed slots where main has
approved seeds. Each difference is either a factory mistake or a fix to main.

**First real Run: Diocese of Wilmington** (Delaware and Maryland's Eastern Shore, roughly
56 parishes; the survey will confirm the number). It's small, settled and next to territory
you've already mapped.

## Open questions

None right now.

## Deferred

- Leads and other intakes (eCatholic dumps, pasted lists) feeding the pipeline or ranking the queue.
- Foremen that run on their own, and a trusted way to measure a spec change (replay evals).
- An outside model's opinion in `seed-review`.
- Auto-merge.
