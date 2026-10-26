# Onboarding factory: specification (draft)

Status: draft. The [MVP](#13-mvp) is what gets the first diocese through end to end;
everything else is in [Future enhancements](#future-enhancements).

## 1. Goal

Agents take a diocese from nothing to fully seeded parishes without a person in the loop,
apart from merging PRs and answering issues. Each piece of work is a job, small enough for
one agent, run by a fresh worker. Code decides what runs next. A person works only through
GitHub issues, foreman reviews and the PRs.

Each diocese goes through two Runs. A **map Run** finds every parish's bulletin and
promotes the diocese, so its parishes go live in extract mode like every parish so far. A
**seed Run** starts once those parishes have bulletins in the database, and seeds them with
today's seeding tools.

## 2. Vocabulary

| Term | Meaning |
|---|---|
| **Run** | One pass of one diocese through the pipeline, either a map Run or a seed Run: one branch, one worktree, one PR. |
| **Stage** | A kind of work (`survey`, `map`, `seed`, ...), defined by a stage spec. |
| **Stage spec** | A stage's prompt, skills, model, tools, write boundaries, gates and limits. |
| **Job** | One run of a stage on one input, such as "map batch 3 of Wilmington" or "seed St. Paul". Agent jobs have a worker; code jobs don't. |
| **Worker** | A fresh Agent SDK session that runs one job and ends. It can't start other agents. |
| **Gate** | A code check the dispatcher runs after a job. The worker's own report is never enough. |
| **Handoff** | The JSON a worker writes at the end of its job. |
| **Flag** | A structured request for a decision, either **blocking** or **advisory**. |
| **Parked** | A parish set aside by a blocking flag. The rest of its Run carries on. |
| **Reviewer** | A stage that judges another stage's work (`survey-review`, `seed-review`). |
| **Foreman** | A skill you run by hand to review a job or a stage and suggest improvements (§9). |
| **Dispatcher** | Code, not an agent. It picks the next job, checks usage, starts workers, runs gates, retries. |
| **Ledger** | SQLite state: Runs, jobs, attempts, sessions, worker steps, costs, flags. |
| **Queue** | `factory/queue.json`, the ordered list of dioceses waiting for a map Run. |

## 3. The pipeline

**Map Run**

```
survey ─▶ survey-review ─▶ map × each batch ─▶ reconcile ─▶ promote ─▶ PR ─▶ (you merge)
                           integrate whenever New lessons passes 8 entries
```

**Seed Run**, once enough parishes have 2 bulletins (§11)

```
for each batch: seed × each parish ─▶ seed-review ──▶ PR ─▶ (you merge)
```

- **One Run at a time**, and one job at a time within it (`max_workers: 1`). Batches run
  in order, so each map batch starts from the playbook the earlier ones built.
- A seed Run that is ready goes before a new map Run, so dioceses are finished before new
  ones start. A Run waiting for your merge, or blocked on an issue, steps aside and the
  next Run starts.
- In a map Run, a parish the map job excluded or left open gets no seed later.
- A seed Run uses the map Run's batches from `batches.json`, leaving out parishes that
  aren't ready.
- The stage order is code in the dispatcher.
- Jobs pass work to each other **only through files and git**: records, seeds,
  `diocese.md`, `batches.json` and handoffs. Never through messages.

### Stages

| Stage | Run | Kind | Model | Does | Gates |
|---|---|---|---|---|---|
| survey | map | agent | Opus, high | `init`, rosters, `diocese.md` intro and sources, `batches.json` (today's `diocese-surveyor`) | `batches validate`, `diocese validate` |
| survey-review | map | reviewer | Opus | Checks grouping, exclusion reasons and proposed rules | none |
| map | map | agent | Sonnet, high | Maps about 4 parishes: bulletin source, churches, exclusions and open records (today's `parish-scout`) | `diocese validate` |
| integrate | map | agent | Opus | Merges *New lessons* into the playbook in `diocese.md` | `diocese validate` |
| reconcile | map | agent | Opus | `coverage --link`, `audit --fetch`, peer `publication_reviews`, merges across batches, `fetch:check --diocese`, a last integrate | `batches validate`, `diocese validate` |
| promote | map | code | none | `promote --dry-run`, `promote`, `uv run pytest`, lint, commit | its own exit codes |
| seed | seed | agent | Sonnet, high | Drafts one parish's seed (today's `seed-drafter`) | `seed check` |
| seed-review | seed | reviewer | Opus | Approves each seed in the batch or sends it back, answering questions by `rules.md` | `seed check` on approved files |
| pr | both | code | none | Pushes, opens the PR and writes its summary (§10) | none |

### Integrating what batches learn

What a map job learns reaches later batches in three ways:

- **Leads** go through code. A handoff lead names the batch or roster entry it touches,
  and the dispatcher adds it to that batch's job input.
- **Lessons** are appended by the dispatcher, as written, to *New lessons* in
  `diocese.md`, which every later map job reads. When the list passes 8 entries, the next
  job is `integrate`, which merges them into *Bulletin publishers here* and *Rules
  settled*, keeps only what's reusable, and empties the list.
- **Fixes across batches** (a merge, a church that belongs to another parish) are raised
  as advisory flags and handled by `reconcile`.

Lessons from `seed` jobs don't go into `diocese.md`. They stay in the ledger for foreman
reviews.

## 4. Stage spec

One file per stage, `factory/stages/<stage>.yaml`, holding what a foreman review might
change. The dispatcher builds each job's input in code.

```yaml
stage: map
kind: agent                    # agent | reviewer | code
model: claude-sonnet-5-5
effort: high
prompt: .claude/agents/parish-scout.md
skills: [explore-diocese, parish-site-access]
tools: [Bash, Read, Edit, Write]
writes:                        # globs, checked by the diff-scope gate
  - data/dioceses/{diocese}/**
  - scratch/{run}/{job}/**
gates:
  - pnpm --silent diocese validate {diocese}
limits: { max_turns: 300, max_minutes: 90 }
```

Every job records the commit it ran at. That identifies the stage spec, skills, prompts
and CLI it ran with.

### Gates every agent job gets

- **Handoff gate.** The handoff exists and matches the schema.
- **Diff-scope gate.** Every changed path matches `writes`. On a failure the dispatcher
  reverts the out-of-scope changes and sends the job back with the paths.

Reviewers write nothing but their handoff (`writes` is only their scratch folder). The
dispatcher acts on their verdicts (§8).

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

Reviewers add their verdicts:

- `survey-review`: `"verdict": "approve | send_back"`, `"problems": [...]`, and
  `"rules": [...]`, the proposed rules it accepts, as written.
- `seed-review`: `"seeds": [{ "parish", "verdict": "approve | send_back", "answers":
  { "<question id>": "..." }, "problems": [...] }]`.

`reconcile` puts lessons that would help in any diocese (a publisher's quirk worth a line
in the README's *Traps*, a script every batch rewrote) in its `lessons`, for the PR.

## 5. Dispatcher

A long-running Python process on the Claude Agent SDK, on this machine. Python, because
everything it calls is Python: the `diocese` and `seed` CLIs, the blob store, `pytest`.
Each tick:

1. **Usage.** For each of the two accounts, it reads
   `GET https://api.anthropic.com/api/oauth/usage` with that account's Claude Code login
   token, the call T3 Code makes. An account can take a new job only while it's under both
   of its limits:
   - **5-hour:** below `five_hour_cap` (default 75%);
   - **weekly, paced:** below `weekly_cap × (days into the week + 1) ÷ 7` (default cap
     70%), so the factory can't use up the week early but can still work on its first day.

   A rate-limit error from the SDK is the backstop: that job becomes `waiting_usage`
   whatever the endpoint said. If no account is eligible, it waits for the earliest reset.
   `pnpm factory pause` and `resume` override this.

   **Accounts.** Each account has its own config directory (`CLAUDE_CONFIG_DIR`), which
   holds its login and session transcripts. A new job goes to the eligible account with the
   most headroom, and **stays on that account** for its whole life, because it can only be
   resumed from where its transcript is stored.
2. **Pick the next job.** With no job running, it takes the next job of the active Run.
   With no active Run, it starts one: a ready seed Run first (§11), otherwise a map Run for
   the first diocese in the queue that has none.
3. **Start a job.** It merges `origin/main` into the Run branch so the worker gets the
   latest specs and data (§10), then runs `query()` with the stage spec in the Run's
   worktree. It stores the session id, the transcript, the cost and each step the worker
   takes.
4. **Finish a job.** It runs the gates, then:
   - all pass → commit with a `Factory-Job: <id>` trailer, push the branch, act on the
     handoff (leads, lessons, verdicts, flags), queue the next job;
   - a gate fails or a reviewer sends the work back → resume the same session with the
     exact problems, up to 2 send-backs per job, then raise a blocking flag;
   - usage limit hit → `waiting_usage`, and the same session resumes after the reset;
   - crash → resume the session; `partial` → resume once with "continue", then a blocking
     flag;
   - over `max_minutes` → stop the session and treat it as `partial`.

   If a session can't be resumed, a fresh worker of the same stage gets the problems and
   the files already on disk.
5. **Flags.** Advisory flags are stored for the PR. A blocking flag about a parish
   **parks** that parish and opens an issue (§7); the Run carries on with the next job. A
   blocking flag about the Run (a bad survey, a merge conflict, a gate the worker can't pass
   on shared files) opens an issue and blocks the Run.

Job states: `queued → running → (gating) → done`, plus `waiting_usage`, `sent_back`,
`blocked` and `failed`. A Run is `active`, `blocked`, `in_review` or `merged`. A parish's
state comes from its files (`diocese todo`, `seed status`), not the ledger.

CLI: `pnpm factory status | queue | run | pause | resume | retry <job> | inspect <job> |
cost [--stage]`.

### Worker setup

- **Worktree.** The dispatcher works in its own worktree, one branch per Run, with its own
  copy of the database and its own `node_modules`, so it never touches your checkout.
- **Permissions.** Workers run in auto mode (`permission_mode="auto"`), where a classifier
  checks each action instead of a person. Only the dispatcher commits, pushes and opens
  PRs.

## 6. Ledger and storage

- `data/factory/factory.db` (SQLite, gitignored, on the Linux filesystem, not under `/mnt/c`).
- Transcripts and handoffs go in `data/factory/runs/<run>/<job>/`, also gitignored.
- **Nightly backup** with SQLite `.backup`, uploaded to R2.
- Work lives in git, and every job pushes its branch. Losing the database loses only
  history, costs and transcripts, which only foreman reviews need.
- `factory/queue.json` is committed: an ordered list of `{ diocese, notes }`. A one-off
  agent session edits it.

## 7. Flags and issues

- Flags are either **blocking** or **advisory**. An advisory flag lets the Run continue;
  the parish is left open or excluded with a reason, and the flag is listed in the PR.
- A blocking flag becomes a **GitHub issue** with labels `factory`, `run:<diocese>` and
  `stage:<stage>`, holding the question, the evidence and the suggestion.
- You answer by commenting and closing the issue. The dispatcher sees it closed and
  resumes the blocked job with your answer:
  - your last comment is the answer;
  - a comment of `/accept` takes the issue's suggestion;
  - closing with no comment from you changes nothing: the dispatcher reopens the issue
    and says so;
  - only comments from your GitHub login count, since the answer becomes part of an
    agent's prompt.
- A parked parish whose issue is answered gets its job queued again. If the Run has
  already passed that stage, the job runs before `reconcile`, or before `promote` if
  `reconcile` is done.

## 8. Reviewers

A reviewer **never edits the work it reviews**, and writes nothing but its handoff. The
dispatcher acts on its verdicts:

1. **Approve.** For `survey-review`, the dispatcher appends its accepted rules to *Rules
   settled* in `diocese.md` and the Run moves on. For `seed-review`, it runs
   `pnpm seed approve <parish> --reviewer agent:seed-review@<commit>` with the reviewer's
   answers (§11).
2. **Send back** to the worker's session with specific problems, which counts against the
   job's 2 send-backs. For `seed-review`, each seed sent back goes to the session that
   drafted it.
3. **Flag**, which becomes an issue when it's blocking.

When `seed-review` answers a question against the drafter's lean, that is recorded for
foreman reviews.

## 9. Foreman

A foreman is a **skill you run by hand**, not a standing agent. You ask it to review a job,
a stage's recent jobs, or a Run, and it tells you what went wrong and how to improve it.

- **Context.** `pnpm factory inspect <job>` prints everything about a job in one place:
  its stage and commit, its input and handoff, its gate results, every attempt and
  send-back, what later stages said about its output (reviewer verdicts, your issue
  answers), its cost and the path to its transcript. The skill starts from that and reads
  the transcript selectively.
- **What it looks for.** Where the job went wrong in the transcript, and why: the skill
  text, the agent prompt, the CLI, the model, the job's input, or the source itself (a
  publisher no instructions could have handled). Repeated work, wasted turns and
  instructions the worker ignored or misread are as useful as outright errors.
- **What it gives you.** What went wrong, the evidence, and concrete changes to the stage
  spec (skill, agent prompt, CLI or model), most useful first. It changes nothing unless
  you ask; when you do, it opens a PR against the spec, and you merge it.
- **Reasons, not scores.** There is no trusted way yet to show a spec change helped. The
  commit each job ran at shows which version of the spec it used.

## 10. Git and PRs

- One branch per Run (`factory/<diocese>-map`, `factory/<diocese>-seed`). Each job ends
  in a commit with a `Factory-Job` trailer, then a push.
- Before each job, the dispatcher merges `origin/main` into the Run branch. This keeps
  specs current and the PR mergeable. A merge conflict raises a Run-level blocking flag,
  except in `parishes.csv` and `churches.csv`: there a code job takes main's version and
  runs `promote` again.
- The `pr` code step writes the PR summary from the ledger and the CLIs:
  - **map Run:** coverage numbers, advisory flags, parked parishes, and `reconcile`'s
    lessons for every diocese;
  - **seed Run:** seeds by status, advisory flags, parked parishes, and a random sample
    of agent approvals for you to spot-check.
- **You merge.** Seeds load as they do today once the seed PR is merged.

## 11. Seed Runs

A seed Run uses today's seeding tools against the database, so the parishes need bulletin
rows first.

- **When a parish is ready.** A parish from a merged map Run is ready once the database has
  at least 2 of its bulletins. Once a day the dispatcher refreshes its database copy
  (`pnpm data:pull`) and counts them.
- **First seed Run.** Starts once 80% of the diocese's mapped parishes are ready, and
  seeds those.
- **Follow-up seed Run.** Seeds the rest. It starts when they are all ready, or 6 weeks
  after the map Run merged, whichever comes first. Each parish still not ready then gets an
  issue, since its bulletin source is probably broken.
- **Agent approval.** One new command: `pnpm seed approve <parish> --reviewer agent:...
  [--answers <file>]`. It does what Seeds mode does for a person and writes only
  `reviewer`, `approved_at` and the reviewer's answers.

## 12. What carries over

- `explore-diocese`, `draft-parish-seed` and `parish-site-access` become stage skills.
- `diocese-surveyor`, `parish-scout` and `seed-drafter` become the prompts for the
  `survey`, `map` and `seed` stage specs.
- `map-diocese` and `seed-parishes` are the orchestrators the factory replaces. Keep
  them for manual sessions until the factory has proven itself, then retire them.
- New: a `foreman` skill (§9).

## 13. MVP

Get one diocese through end to end, then improve it.

- `pnpm seed approve`.
- The dispatcher: usage check with the two accounts, job picking, resume, gates, the
  daily seed-readiness check.
- The ledger and its nightly backup.
- Stage specs for every stage.
- Issues for blocking flags, and reading your answers back.
- The `pr` step.
- `pnpm factory` CLI, including `inspect`, and the foreman skill.

**First Run: Diocese of Wilmington** (Delaware and Maryland's Eastern Shore, roughly 56
parishes; the survey will confirm the number). It's small, settled and next to territory
you've already mapped. You review its PRs closely; they are the test of the factory.

## Future enhancements

- **Dashboard.** A local page showing usage against caps, Runs, the running worker and
  anything waiting on you. Until then, `pnpm factory status`.
- **Triage.** An agent that tries to settle blocking flags itself (an existing rule, a
  retry later) before opening an issue. Worth adding if there are too many issues.
- **Sandbox.** Run workers in the SDK's Bash sandbox with permissions bypassed, instead of
  auto mode, to save the classifier's usage and its false blocks. First check that
  `parish-site-access`'s headed Chrome works inside it.
- **More at once.** Several Runs, or several workers, in parallel.
- **Overrules and auto-merge.** Record your corrections against reviewer decisions, drop
  spot-checks once the record supports it, and merge automatically when gates pass.
- **Measuring spec changes.** Foremen that run on their own, and replay evals to show a
  change helped.
- **Other intakes.** Leads from eCatholic dumps or pasted lists feeding or ranking the
  queue.
- **An outside model's opinion** in `seed-review`.
