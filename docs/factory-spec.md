# Onboarding factory: specification

Status: the [MVP](#13-mvp) is implemented (`src/pdf_extract/factory/`, `factory/`) and
tested with stub workers; it has not yet run a real diocese. Everything else is in
[Future enhancements](#future-enhancements). How to run it, and what the implementation
decided where this spec was silent, are in [Running it](#running-it) and
[Implementation decisions](#implementation-decisions).

## 1. Goal

Agents take a diocese from nothing to fully seeded parishes without a person in the loop,
apart from merging PRs and answering issues. Each piece of work is a job, small enough for
one agent, run by a fresh worker. Code decides what runs next. A person works only through
GitHub issues, foreman reviews and the PRs.

Each diocese goes through two Runs. A **map Run** finds every parish's bulletin and
promotes the diocese, so its parishes go live in extract mode like every parish so far. A
**seed Run** starts once those parishes have bulletins in the database, and seeds them with
today's seeding tools.

An agent reviewer decides every open question and approves the seeds, which replaces
`seeding-plan.md`'s rule that a person approves every seed. You stay involved through the
PR: it lists every decision the reviewer made and why (§10), and you change any that's
wrong before merging. If one shows a gap in the policy, you change it (`rules.md`, a
skill) in a separate PR. The factory never changes `rules.md`.

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
| **Precedent** | A seed question `seed-review` settled that no rule covered, kept in `diocese.md` so the rest of the diocese is decided alike. |

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
- When no job is running, the dispatcher picks, in order: the active Run's next job; a
  blocked Run whose issues are all answered; a ready seed Run; a map Run for the next
  diocese in the queue. So dioceses are finished before new ones start. A Run waiting for
  your merge, or blocked on an issue, steps aside.
- Once a Run's PR is open, the Run doesn't change. A parked parish answered after that
  goes into a small follow-up Run of the same kind, which starts after the PR is merged:
  `map → promote → pr` or `seed → seed-review → pr`, for those parishes only.
- In a map Run, a parish the map job excluded or left open gets no seed later.
- A seed Run uses the map Run's batches from `batches.json`, leaving out parishes that
  aren't ready.
- The stage order is code in the dispatcher.
- Jobs pass work to each other **only through files and git**: records, seeds,
  `diocese.md`, `batches.json` and handoffs. Never through messages.

### Stages

| Stage | Run | Kind | Model | Does | Gates |
|---|---|---|---|---|---|
| survey | map | agent | Opus, high | `init`, rosters, `diocese.md` intro and sources, `batches.json` | `batches validate`, `diocese validate` |
| survey-review | map | reviewer | Opus | Checks grouping, exclusion reasons and proposed rules | none |
| map | map | agent | Sonnet, high | Maps about 4 parishes: bulletin source, churches, exclusions and open records | `diocese validate` |
| integrate | map | agent | Opus | Merges *New lessons* into the playbook in `diocese.md` | `diocese validate` |
| reconcile | map | agent | Opus | `coverage --link`, `audit --fetch`, peer `publication_reviews`, merges across batches, `fetch:check --diocese`, a last integrate | `batches validate`, `diocese validate` |
| promote | map | code | none | `promote --dry-run`, `promote`, `uv run pytest`, lint, commit | its own exit codes |
| seed | seed | agent | Sonnet, high | Drafts one parish's seed | `seed check` |
| seed-review | seed | reviewer | Opus | Answers every open question in the batch (by a rule, the diocese's precedents or its own judgment) and approves each seed; sends a seed back only for an error an answer can't fix (§8) | `seed check` on approved files |
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
  as advisory flags and handled by `reconcile`, which names each flag it settles so the PR
  stops listing it as open (§7).

Lessons from `seed` jobs don't go into `diocese.md`. They stay in the ledger for foreman
reviews. What a seed Run carries forward is `seed-review`'s decisions that no rule
covered: the dispatcher appends each to *Seeding precedents* in `diocese.md` (the
situation, the choice and the parishes), and later `seed-review` jobs in that diocese
follow them. Precedents stay in their diocese; only you turn one into a rule.

## 4. Stage spec

One file per stage, `factory/stages/<stage>.yaml`, holding what a foreman review might
change. The dispatcher builds each job's input in code.

```yaml
stage: map
kind: agent                    # agent | reviewer | code
model: claude-sonnet-5-5
effort: high
prompt: factory/prompts/map.md
skills: [explore-diocese, parish-site-access]
tools: [Bash, Read, Edit, Write]
writes:                        # globs, checked by the diff-scope gate
  - data/dioceses/{diocese}/**
  - scratch/{run}/{job}/**
gates:
  - pnpm --silent diocese validate {diocese}
secrets: []                    # .env entries its workers get (seed: R2_*, model keys)
gate_secrets: []               # .env entries its gate commands get
limits: { max_turns: 300, max_minutes: 90 }
```

Every job records the commit it ran at. That identifies the stage spec, skills, prompts
and CLI it ran with.

### Gates every agent job gets

- **Handoff gate.** The handoff exists and matches the schema.
- **Diff-scope gate.** Every changed path matches `writes`. On a failure the dispatcher
  reverts the out-of-scope changes and sends the job back with the paths. A sandboxed
  worker's changes that were never brought back into the Run (out of scope, a link, too
  big) fail it the same way.

Reviewers write nothing but their handoff (`writes` is only their scratch folder). The
dispatcher acts on their verdicts (§8).

### Handoff

`scratch/{run}/{job}/handoff.json`, about 300 tokens:

```json
{
  "status": "done | partial | blocked",
  "summary": "one or two sentences",
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
- `reconcile` (not a reviewer) adds `"settled": [{ "flag": 12, "how": "..." }]`: the
  earlier advisory flags it settled, by the ids its job input shows. The dispatcher sends
  it back for an id that isn't an advisory flag of its Run.
- `seed-review`: `"seeds": [{ "parish", "verdict": "approve | send_back", "answers":
  [{ "question", "choice", "basis": "rule | precedent | judgment", "why" }], "problems":
  [...] }]`, a verdict for every parish. It never raises a blocking parish flag: it
  decides the question instead.

The dispatcher takes the changed paths from `git`, not from the handoff.

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
     100%): 1/7 of the weekly allowance on day 1, 2/7 on day 2, up to 7/7 on day 7.
     Days start at the account's weekly reset time, so the factory can use the full weekly
     allowance without using it all early.

   A rate-limit error from the SDK is the backstop: that job becomes `waiting_usage`
   whatever the endpoint said. If no account is eligible, it waits for the earliest reset.
   If the endpoint errors or its response doesn't parse, the dispatcher pauses and says
   why; `pnpm factory resume` starts it again. A 429 Too Many Requests doesn't pause it:
   it waits 30 minutes, reading nothing, then the next usage check tries again (another
   429 waits another 30 minutes). `pnpm factory status` shows the cooldown's reason and
   next retry, and `resume` retries at once. `pnpm factory pause` and `resume` also
   override the caps.

   **Accounts.** Each account has its own config directory (`CLAUDE_CONFIG_DIR`), which
   holds its login and session transcripts. A new job goes to the eligible account whose
   weekly window resets soonest, so an account's allowance is used before its reset rather
   than lost (between accounts resetting together, the one with the most headroom). It
   **stays on that account** for its whole life, because it can only be resumed from where
   its transcript is stored.

   Each account is signed in once with `claude /login` under its config directory. The
   Agent SDK runs the Claude Code binary, so jobs use that subscription login, not an API
   key. Anthropic's terms allow this for your own use: Pro and Max limits "assume
   ordinary, individual usage of Claude Code and the Agent SDK". What they forbid is
   offering Claude login in a product for other people. A factory running around the
   clock stretches "ordinary", which is one more reason for the caps above.
2. **Pick the next job** in the order in §3.
3. **Start a job.** At the start of a stage, if `origin/main` has moved, it merges it into
   the Run branch so the worker gets the latest specs and data (§10). It then runs
   `query()` with the stage spec in the Run's worktree, and stores the session id, the
   transcript, the cost and each step the worker takes.
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

   Each step after the gates is recorded in the ledger as it completes, so a dispatcher
   restarted partway through skips what's done instead of committing or appending lessons
   twice.
5. **Flags.** Advisory flags are stored for the PR; those `reconcile` lists in `settled`
   are marked settled, with its `how` and its job. A blocking flag about a parish, from a
   map or seed job (other stages are sent back for one), **parks** that parish and opens
   an issue (§7); the Run carries on with the next job. A
   blocking flag about the Run (a bad survey, a merge conflict, a gate the worker can't pass
   on shared files) opens an issue and blocks the Run.

Job states: `queued → running → (gating) → done`, plus `waiting_usage`, `sent_back`,
`blocked` and `failed`. A Run is `active`, `blocked`, `in_review` or `merged`. A parish's
state comes from its files (`diocese todo`, `seed status`), not the ledger.

A Run in review becomes `merged` when its last commit is in `origin/main`, which the
dispatcher checks after each `git fetch`, or, for a PR squashed or rebased, when GitHub
says its PR is merged. Merge factory PRs with a merge commit where you can, so main keeps
the Run's history. You handle review comments in your
own session.

CLI: `pnpm factory status | queue | run | pause | resume | retry <job> | inspect <job> |
quota [--by ...] [--windows] [backfill] | cost [--stage] | backup | clones [--apply]`.

### Worker setup

See `docs/factory-sandbox-plan.md` for the design and what is still to verify live.

- **Checkout.** The dispatcher works in its own clone, one standalone clone per Run on
  the Run's branch, each with its own copy of the database and its own `.venv`. None
  shares git metadata with your checkout or with each other.
- **Sandbox.** `worker_backend: sandbox` runs each attempt's Claude CLI, and everything
  it starts (Bash, `uv`, Chrome, Xvfb), in a fresh rootless Podman container: no
  capabilities, a read-only root, memory, CPU and process limits, and an internal
  network whose only way out is an egress proxy that refuses private, host and metadata
  addresses. The worker edits a private copy of the Run's files with no `.git`, its
  tools (`src/`, `.claude/`, `factory/`) read-only. After the attempt the dispatcher
  copies back only ordinary files inside `writes`. If Podman, the image or the proxy
  fails, the attempt ends as `sandbox` and the job waits; it never runs on the host
  instead. `worker_backend: host` (the default until the live checks pass) runs the CLI
  on the host.
- **Environment.** Either way, a worker starts through `factory/sandbox/claude-in-box`
  with only what the dispatcher names: no `.env` keys but its stage's `secrets:`, no
  GitHub, Cloudflare or SSH, and its own Xvfb, not the host's display. `pnpm factory`
  reads `.env` into a dict instead of its own environment, and gate commands get its
  environment without secrets, plus their stage's `gate_secrets:`.
- **Claude login.** Host workers use the account's config folder. Sandboxed workers get
  the account's `claude setup-token` token (`worker_token_file:`), which never refreshes,
  so a worker can't rotate the login the dispatcher reads usage with.
- **Permissions.** Workers run in auto mode, where a classifier checks each action
  instead of a person. The SDK starts in `default` mode, so the dispatcher sets
  `permission_mode="auto"` explicitly.
- **Only the dispatcher commits, pushes and opens PRs.** Workers start without
  `GH_TOKEN` or git credentials in their environment, and with deny rules for `git
  commit`, `git push` and `gh`. The diff-scope gate checks files git tracks or would
  track; gitignored files (the database copy, `scratch/`) are left to the worker. The
  dispatcher's own git calls run without hooks or fsmonitor.
- **Supervision.** The dispatcher runs as a systemd user service with `Restart=always`.
  On startup it removes any worker container left behind, then treats a job still
  marked `running` as a crash and resumes it.

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
  the parish is left open or excluded with a reason, and the flag is listed in the PR
  unless `reconcile` settles it. The PR lists settled flags apart, collapsed, with how
  each was settled.
- Some things need no flag, because the records carry them (`data/dioceses/README.md`,
  *What to flag*): a church no source settles (an `open/` record, which `reconcile` tries
  once more and the PR lists), a bulletin `fetch` can't collect (the parish's `fetch_gap`,
  which the PR lists by kind and `pnpm diocese gaps` lists across dioceses), a check
  blocked for now (the row's `research`, with a retry trigger), and an address or name
  the sources disagree on (the worker chooses, preferring the parish's and the diocese's
  own, and says why in the record).
- A blocking flag becomes a **GitHub issue** with labels `factory`, `run:<diocese>` and
  `stage:<stage>`, holding the question, the evidence and the suggestion.
- You answer by commenting and closing the issue. The dispatcher checks open factory
  issues every 10 minutes, and when one is closed it resumes the blocked job with your
  answer:
  - your last comment is the answer;
  - a comment of `/accept` takes the issue's suggestion;
  - closing with no comment from you changes nothing: the dispatcher reopens the issue
    and says so;
  - only comments from your GitHub login count, since the answer becomes part of an
    agent's prompt.
- A parked parish whose issue is answered gets its job queued again. If the Run has
  already passed that stage, the job runs before `reconcile`, or before `promote` if
  `reconcile` is done. Once the PR is open, the parish goes to a follow-up Run (§3).

## 8. Reviewers

A reviewer **never edits the work it reviews**, and writes nothing but its handoff. The
dispatcher acts on its verdicts:

1. **Approve.** For `survey-review`, the dispatcher appends its accepted rules to *Rules
   settled* in `diocese.md` and the Run moves on. For `seed-review`, it runs
   `pnpm seed approve <parish> --reviewer agent:seed-review@<commit>` with the reviewer's
   answers (§11), and appends those settled by judgment to *Seeding precedents* (§3).
2. **Send back** to the worker's session with specific problems, which counts against the
   job's 2 send-backs. For `seed-review`, each seed sent back goes to the session that
   drafted it, and counts against that seed job. When the redrafts pass their gates, a
   new `seed-review` job reviews only those seeds. A seed past its 2 send-backs gets a
   blocking flag, and its parish is parked.
3. **Flag**, which becomes an issue when it's blocking. `survey-review` may raise one;
   `seed-review` raises only advisory flags.

`seed-review` answers every open question and approves the seed. It sends a seed back
only for an error an answer can't fix (a settled slot the newest bulletin contradicts,
broken evidence), never for an open question. How it answers one:

- **A rule in `rules.md` covers it.** Answer as the rule says (basis `rule`). The drafter
  should have applied it, which is a lesson for foreman reviews.
- **A precedent in this diocese covers it.** Follow the precedent (basis `precedent`).
- **Neither covers it.** Decide, preferring the drafter's lean unless the evidence is
  against it, and say why (basis `judgment`). It decides even when the evidence is thin,
  choosing what the evidence best supports and saying what was missing.

Every answer is listed in the PR, and recorded in the ledger for foreman reviews.

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

- One branch per Run, numbered because a diocese can have several Runs of a kind
  (`factory/<diocese>-map-1`, `factory/<diocese>-seed-1`, `factory/<diocese>-seed-2`).
  Each job ends in a commit with a `Factory-Job` trailer, then a push.
- At the start of each stage, if `origin/main` has moved, the dispatcher merges it into
  the Run branch. This keeps specs current and the PR mergeable without a merge commit per
  job, and no stage changes spec partway through. A merge conflict raises a Run-level
  blocking flag,
  except in `parishes.csv` and `churches.csv`: there a code job takes main's version and
  runs `promote` again.
- The `pr` code step writes the PR summary from the ledger and the CLIs:
  - **map Run:** coverage numbers, the `open/` records with what would settle each, the
    fetch gaps by kind, advisory flags still open, the flags settled during the Run
    (collapsed), parked parishes, and `reconcile`'s lessons for every diocese;
  - **seed Run:** seeds by status, advisory flags, parked parishes, and **every decision
    `seed-review` made**, by judgment, by precedent and by a rule, each with the parish
    and slot, the drafter's lean, the choice and why. Answers against the lean come first.
    You change any that's wrong before merging; a wrong judgment may be a reason to change
    the policy.
  - Only approved seeds go to main: a parked parish's draft is left out of the PR, and its
    follow-up Run drafts it again with your answer.
- **You merge**, with a merge commit. Seeds load as they do today once the seed PR is
  merged.

## 11. Seed Runs

A seed Run uses today's seeding tools against the database, so the parishes need bulletin
rows first.

- **When a parish is ready.** A parish from a merged map Run is ready once the database has
  at least 2 of its bulletins. Only parishes the map Run promoted with a bulletin source
  count, for readiness and for the 80% below; excluded and open ones never do, and one
  with a `fetch_gap` counts only once its collector lands and the gap is cleared on main
  (the seed Run's notes say how many wait). Once a day the dispatcher refreshes its database copy
  (`pnpm data:pull`) and counts them.
- **First seed Run.** Starts once 80% of the diocese's mapped parishes are ready, and
  seeds those. If that hasn't happened 6 weeks after the map Run merged, it starts then
  with whatever is ready, and each parish still not ready gets an issue, as below.
- **Follow-up seed Run.** Seeds the rest. It starts when they are all ready, or 6 weeks
  after the map Run merged, whichever comes first. Each parish still not ready then gets an
  issue, since its bulletin source is probably broken.
- **Agent approval.** One new command: `pnpm seed approve <parish> --reviewer agent:...
  [--answers <file>]`. It does what Seeds mode does for a person: it writes each answer
  into its slot as `{"choice", "by": "agent:seed-review@<commit>", "at"}`, then
  `reviewer` and `approved_at`, and changes nothing else.
- **Rules stay yours.** The factory never edits `rules.md`. `pnpm seed questions
  --answered` shows agent answers apart from people's, by their `by`, so candidate rules
  come from your own decisions or from a borderline case you agree with. Either way, you
  add the rule in a separate PR.

## 12. What carries over

- `explore-diocese`, `draft-parish-seed` and `parish-site-access` become stage skills.
- The `diocese-surveyor`, `parish-scout` and `seed-drafter` agents become the prompts
  `factory/prompts/survey.md`, `map.md` and `seed.md`.
- The `map-diocese` and `seed-parishes` orchestrators are retired: mapping and seeding
  run only through the factory. Seeding's historical evals (`seed pick --labeled`,
  `seed score`) are removed with them, and proposing candidate rules from the owner's
  answers moves to the foreman.
- New: a `foreman` skill (§9).

## 13. MVP

Get one diocese through end to end, then improve it.

- `pnpm seed approve`, `seed questions` showing agent answers separately, and
  `seeding-plan.md` updated for agent approval.
- A stub-worker mode: fake workers write canned handoffs and diffs, so send-backs,
  parking, follow-up Runs, merge conflicts and resuming after a kill can be tested without
  spending usage.
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

## Running it

1. Make the dispatcher its own clone of `main`, apart from yours:
   `git clone <origin url> ~/carlo-factory`. Run `pnpm factory` from there; its ledger,
   transcripts and Run checkouts live in its `data/factory/`. (A checkout made earlier
   as a linked worktree: stop the dispatcher, then `pnpm factory clones --apply` turns it
   and its Run worktrees into standalone clones in place.)
2. `uv sync --group dev --group factory` (the `factory` group holds the Agent SDK),
   `pnpm data:pull`, and R2 keys that can write in `.env` for the nightly backup.
3. Sign each account in once: `CLAUDE_CONFIG_DIR=~/.claude claude /login`, and the
   same for the second. List them, your GitHub login and any paths in
   `data/factory/local.yaml` (`factory/local.example.yaml`). `gh` must be signed in.
4. Try it without spending usage: `pnpm factory run --stub scenario.json` plays canned
   workers (`workers.scenario_script`). A stub run has its own ledger, worktrees, issues
   and PRs under `data/factory/stub/` and branches `factory-stub/<run>`, and pushes
   nothing, so it never touches the real Runs; `pnpm factory status --stub` (and
   `inspect`, `cost`... `--stub`) reads it.
5. To sandbox workers: `sudo apt install podman` (rootless; check `podman info` as
   yourself). For each account, `CLAUDE_CONFIG_DIR=~/.claude_2 claude setup-token`, save
   the token to a file only you can read (`chmod 600`) and name it as that account's
   `worker_token_file:`. Then set `worker_backend: sandbox`. The first attempt builds the
   worker image (`factory/sandbox/Containerfile`, from `origin/main`) and starts the
   egress proxy; `pnpm factory status` says when workers run on the host.
6. Start it: `pnpm factory run`, or the systemd unit `factory/carlo-factory.service`.
   `pnpm factory status` shows what it is doing and what waits on you.

## Implementation decisions

Where the implementation had to decide something this spec left open.

### Runs and jobs

- **A checkout per Run**, under `data/factory/worktrees/<run>` (`worktrees_dir` in
  `local.yaml`): a standalone clone of the remote on the Run's branch from `origin/main`,
  with a copy of the dispatcher's database and `uv sync --group dev` (`setup`). Workers
  resume a session only in the Run that made it, so a follow-up Run's jobs start fresh
  workers with your answer in their input.
- **A merged Run's checkout is deleted**, with its sandbox workspace, once the dispatcher
  sees the merge: nothing needs it after that, since answers go to a follow-up Run and
  seed readiness reads the parish records from `origin/main`. Its `scratch/<run>/`
  (handoffs, manifests, tools) is copied to `data/factory/runs/<run>/scratch/` first.
- **The next job is computed, not queued ahead** (`plan.py`): a queued job (a send-back,
  an answer) first, then the stage order. A seed Run's batches are the map Run's
  `batches.json`, each parish placed by the roster refs in its record; parishes in no
  batch come last.
- **Jobs are named `<seq>-<stage>`** within their Run (`wilmington-map-1/004-map`); their
  scratch folder is `scratch/<run>/<job>/`, and the Run's shared tools folder
  `scratch/<run>/tools/`.
- **Job input.** The stage's prompt file, frontmatter stripped, is appended to Claude
  Code's system prompt. The first message is built in code (`inputs.py`): a header with the
  write boundaries, the gates, the handoff path and schema, then the stage's input.
  Resumed attempts get only the problems, your answer, or "continue".
- **Stage prompts** are `factory/prompts/<stage>.md`, one per agent and reviewer stage.
- **Crashes.** A crashed attempt resumes its session; one that couldn't resume (no turns)
  gets a fresh worker, with the whole job input and whatever that attempt was told (the
  problems to fix, an answer). The third crash since the owner last unblocked the job
  (an answer or `factory retry`) blocks the Run. `max_turns` and `max_minutes` end an
  attempt as `partial`.
- **Workers can't move HEAD.** Besides `git commit`, `git push` and `gh`, the deny rules
  cover `git reset`, `checkout`, `switch`, `rebase`, `merge` and `stash`. If HEAD moved
  anyway, the gate resets it softly and sends the job back.
- **A handoff with status `blocked`** must carry a blocking flag. A blocking flag with
  `scope: run` blocks the Run without running the stage gates; parish flags don't stop
  the job finishing. When a job raised several Run-level flags, it resumes once all are
  answered, with every answer.
- **seed-review must cover its batch**: a verdict for every parish, and no blocking
  parish flag, or it is sent back. Only `judgment` answers become precedents.
- **A parked seed's draft is committed** as it stands (`seed <parish>, parked`), so the
  next job's diff-scope gate sees only its own changes and a job answered within the Run
  finds the draft. The `pr` step then takes every seed that isn't approved back out. A
  seed job whose handoff parks its own parish isn't held to `seed check`.
- **`seed approve` failing** on a reviewer's answers sends the seed back to its drafter
  with the error, like any send-back. The stage gate `pnpm seed check {approved}` runs
  after the approvals.
- **Promote and pr are code.** A failing promote command blocks the Run with its output.
  The PR is opened with `gh pr create`; an open PR for the branch is reused.

### Workers and the sandbox

- **The boundary is the CLI, not the SDK.** The Agent SDK stays in the dispatcher and
  starts `factory/sandbox/claude-in-box` as its CLI (`cli_path`), which starts the real
  CLI on the host or in the container. The SDK only reads its messages, so steps, costs
  and rate-limit events are unchanged. That holds only while the dispatcher's
  `ClaudeAgentOptions` set no `hooks`, `can_use_tool` or in-process MCP servers, which
  would run tools in the dispatcher; a test checks it.
- **The launcher** keeps only the environment names the dispatcher lists in `CARLO_BOX`,
  drops the rest of what the SDK passes down (the dispatcher's whole environment), and
  on SIGTERM (a timeout) removes the container or kills the worker's process group, so
  no Chrome survives an attempt.
- **The image** is built on the dispatcher's machine from `origin/main`'s Containerfile,
  `pyproject.toml` and `uv.lock`, tagged by their hash: a Run can't change what its
  workers run in. The project's dependencies are in a read-only `/opt/venv`; the Run's
  `src/` is on `PYTHONPATH`.
- **The workspace** is `data/factory/sandbox/<run>/work`, refreshed from the Run's
  checkout before each attempt (rsync, without `.git`, `.venv` or `node_modules`; the
  worker's database copy and caches are kept). It sits at its own path in the container,
  so the CLI's working directory and session keys match the host's. After each attempt
  the container is removed first, then changed files matching `writes` are copied back
  by content. Links, hard links, devices, `..` and `.git` paths, files over 50 MB and
  more than 2,000 files are refused and recorded on the attempt (`attempt.refused`).
- **Sessions** are in `data/factory/sessions/<run>/`, mounted as the container's
  `~/.claude/projects`: per Run, since an answer job resumes the session of the job it
  answers.
- **The egress proxy** is Stripe's smokescreen, built locally from
  `factory/sandbox/Proxy.Containerfile` using the checksum-pinned v0.1.0 release binary
  (pulling its GHCR image returns 403 here and in CI). Like the worker image, its build file
  comes from `origin/main`, never a Run. It runs as one long-lived container (`carlo-egress`)
  on the workers' internal network (`carlo-workers`) and the normal one. It refuses
  loopback, private, CGNAT, link-local and metadata, multicast and the host's own
  addresses, and resolves names itself, so DNS rebinding doesn't get past it. Workers
  get `HTTP(S)_PROXY`; Chrome gets `proxy=` from it at both Playwright launches.
  The worker image disables pnpm's automatic pre-script dependency install, since its
  scripts use the preinstalled Python environment without `node_modules`. Both browser
  launch sites enable Chromium's own sandbox in the image. The checked-in seccomp
  profile allows its nested-namespace `chroot` without adding container capabilities;
  see `factory/sandbox/seccomp.README.md`. `factory/sandbox/smoke-worker.py` tests the
  full image without credentials, including headed Chromium/Chrome and PDF rendering.
  The proxy uses the first DNS resolver discovered in an external-only container,
  because the internal network's DNS refuses public lookups.
  Claude's web search runs on Anthropic's side and doesn't pass through it.
- **`sandbox` outcome.** Podman missing, the image failing to build, the network or
  proxy failing, an account without a `worker_token_file`, or a container that can't be
  removed: the job waits 10 minutes and tries again, without counting a crash. The third
  in a row blocks the Run.

### Usage

- The endpoint is read with each account's `.credentials.json` token and
  `anthropic-beta: oauth-2025-04-20`. An expired login is refreshed by running
  `claude auth status` under that account; if it is still expired, the dispatcher pauses.
- **Days into the week** are counted from `seven_day.resets_at` minus 7 days. An account
  over the paced weekly cap waits for the next day's cap, or for the reset once it is past
  the full cap or on the last day.
- `pnpm factory resume --override-caps` starts jobs whatever the caps say until the next
  `pause` or `resume`. A worker's rate-limit error still makes its job wait.

**Measuring quota per job.** Quota points, not API-price dollars, are what limit the
factory, so each attempt's five-hour and weekly points are measured from readings of the
usage endpoint (`quota.py`):

- **Readings.** The reading taken to choose an account is the chosen account's `before`
  reading for the attempt; an `after` reading starts as soon as the worker returns and is
  taken in the background while the attempt is recorded. The gates wait for it at most
  10 seconds; if it fails or comes later, that is logged and the job carries on. Once an account has been idle
  `quota_settle_seconds` (default 150) after its last attempt, the dispatcher takes one
  `settled` reading of it, since the meter lags a minute or two; and every
  `quota_sample_minutes` (default 15) a `periodic` reading of every account. Each reading
  keeps the whole response (`raw`: model-specific and extra windows too), with anything
  that looks like a credential removed. None of this runs without accounts (stub Runs).
- **Calibration gap.** `calibration_gap_seconds` (default 0: nothing waits) holds the
  next job on an account until that long after its last attempt finished, so every
  attempt gets a settled reading. Set it at or above `quota_settle_seconds`, for
  calibration runs only; it is a setting, with no CLI flag. A job that waits on every
  account waits until the soonest of one coming under its caps and one's gap ending.
- **Attribution** is computed when a report asks, never stored, as a range with a label.
  `settled`: an idle reading before, a settled one after, no other attempt on the account
  in between: the delta ±1 for whole-percent rounding (a displayed 0 is `<1`).
  `immediate`: only an early reading after: a minimum. `shared`: another attempt on the
  account started less than `quota_settle_seconds` after this one ended: the group's
  total over its combined interval, with its attempts, and no exact share (the first
  attempt's early reading still gives it a minimum). A job with several attempts in one
  group counts the group's upper bound once. `reset`: the window's reset time
  moved by more than 3 minutes (reset times jitter by a second between readings), or
  passed: a minimum. `missing`, or `inconsistent` (the meter fell without a reset): no
  number. The meter rising between two readings while the account was idle is outside
  use, and attempts within an hour of it are flagged.
- **Window totals** (`factory quota --windows`): per account and window instance (keyed
  by its reset time), the points used, the factory's settled, shared and uncertain
  portions, and what's unexplained (outside use, usage lagging past an early reading, use
  before the first reading). They stay useful when per-attempt attribution isn't.
- **Work units**: a map job's batch entries, a seed or seed-review job's parishes, 1
  for any other stage. `factory quota` reports points per unit of completed work by
  stage, or within each stage by model, effort, mode (entrypoint), account, plan, date or
  hour (`--tz`): the median and range over settled samples, uncertain jobs apart, with
  sample counts, coverage, first-try gate passes, retries, send-backs, crashes and
  partials, unresolved and parked work, and dollars last as a diagnostic. It fits no
  model and assumes no peak hours or quota multipliers; those are questions for its data.
- **Plans** come from each login's `.credentials.json` (`subscriptionType`,
  `rateLimitTier`), else `plan:` on the account in `local.yaml`.

### Issues and answers

- The dispatcher's own comments carry `<!-- factory -->` and are never read as answers,
  since it comments with your `gh` login. `/accept` may be followed by more text, which is
  added to the suggestion.
- Labels `factory`, `run:<diocese>` and `stage:<stage>` are created when first needed.
- A parish still not ready 6 weeks after its map Run merged gets one issue
  (`stage:seed`), not a flag; it is seeded when it becomes ready.

### Ledger

- `data/factory/factory.db` holds Runs, jobs, attempts, steps (every tool call and text
  block, truncated), gate results, actions done after the gates, flags, leads, lessons,
  reviewer verdicts, seed-review's decisions and usage readings. Transcripts are copied to
  `data/factory/runs/<run>/<job>/<session>.jsonl` after each attempt.
- **Quota tables.** `usage` rows carry their `source` (`select`, `before`, `after`,
  `settled`, `periodic`), the attempt and job a reading is for, and the scrubbed `raw`
  response. `rate_limit_event` keeps every SDK rate-limit event in full (type, status,
  utilization, reset time, overage, raw, without credentials), besides its `rate_limit`
  step; failing to record one never stops the attempt. `attempt_meta`,
  one row per attempt: requested model and effort (the stage spec's), the models it
  actually used (side calls included), SDK and CLI versions, entrypoint, the account's
  plan, a hash of the stage spec, prompt file and skill names at its commit, the attempt
  whose session it resumed, tokens (input; output, of which thinking is a part; cache
  reads; cache writes kept apart by 5-minute and 1-hour TTL; web searches) in total and
  per model, distinct messages and repeated transcript records, work units, gaps, and its
  `source`: `live` (the ResultMessage), `transcript` (a crash or timeout, parsed from its
  transcript: messages counted once by id, from the attempt's start to its finish, so a
  resumed session's other attempts aren't counted in it) or `backfill`.
- An older ledger gains the new columns when the dispatcher opens it.
- **Backfill.** `pnpm factory quota backfill` fills `attempt_meta` for attempts without
  it, from their copied transcripts and the stage spec at their commit (`git show`), and
  links the selection readings around them by time. Its quota is `approximate`: a
  minimum at best, never settled. Each attempt lists what couldn't be recovered (the SDK
  version, utilization dropped from old rate-limit steps, no settled reading, the plan
  then). Running it again changes nothing.
- The nightly backup goes to R2 under `factory/backups/` when the local hour passes
  `backup_hour`; without keys that can write it stays in `data/factory/backups/`.

## Future enhancements

- **Dashboard.** A local page showing usage against caps, Runs, the running worker and
  anything waiting on you. Until then, `pnpm factory status`.
- **Triage.** An agent that tries to settle blocking flags itself (an existing rule, a
  retry later) before opening an issue. Worth adding if there are too many issues.
- **Sandbox, next steps.** Once the live checks pass and `sandbox` is the default: refuse
  `host` for real Runs unless `allow_host_workers: true`. Then bypass permissions inside
  the container instead of auto mode, to save the classifier's usage and its false
  blocks, now that the container is the boundary. Scoped keys for seed stages (a
  read-only R2 token, model keys with spend caps). gVisor or a microVM if host-kernel
  exploits become a concern.
- **More at once.** Several Runs, or several workers, in parallel.
- **Overrules and auto-merge.** Record your corrections against reviewer decisions,
  shorten the PR's list of seed-review's decisions once the record supports it, and
  merge automatically when gates pass.
- **Measuring spec changes.** Foremen that run on their own, and replay evals to show a
  change helped.
- **Other intakes.** Leads from eCatholic dumps or pasted lists feeding or ranking the
  queue.
- **An outside model's opinion** in `seed-review`.
