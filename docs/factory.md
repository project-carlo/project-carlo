# The onboarding factory

Agents take a diocese from nothing to seeded parishes, with a person in the loop only to
merge PRs and answer GitHub issues. Each piece of work is a **job**, small enough for one
agent and run by a fresh worker. Code decides what runs next.

Each diocese goes through two Runs. A **map Run** finds every parish's bulletin and
promotes the diocese, so its parishes go live in extract mode. A **seed Run** starts once
those parishes have bulletins in the database, and seeds them. An agent reviewer answers
every open seed question and approves the seeds; the PR lists each decision so you can
change any before merging.

The code is `src/pdf_extract/factory/` (its `__init__.py` lists the modules); stage specs,
prompts, the queue and settings are in `factory/`. How quota is measured is in
[factory-quota.md](factory-quota.md).

## Vocabulary

| Term | Meaning |
|---|---|
| **Run** | One pass of one diocese through the pipeline, map or seed: one branch, one worktree, one PR. |
| **Stage** | A kind of work (`survey`, `map`, `seed`...), defined by its stage spec `factory/stages/<stage>.yaml` and prompt `factory/prompts/<stage>.md`. |
| **Job** | One run of a stage on one input ("map batch 3", "seed St. Paul"), named `<seq>-<stage>` in its Run (`wilmington-map-1/004-map`). |
| **Attempt** | One worker session on a job: the first, or a send-back, resume, continue or answer. |
| **Worker** | A fresh Agent SDK session that runs one attempt and ends. It can't start other agents, commit or push. |
| **Gate** | A check the dispatcher runs after an attempt. The worker's own report is never enough. |
| **Handoff** | The JSON a worker writes at the end of its job (`handoff.py` has the schema). |
| **Flag** | A request for a decision, **blocking** (becomes an issue) or **advisory** (listed in the PR). |
| **Parked** | A parish set aside by a blocking flag while the rest of its Run carries on. |
| **Reviewer** | A stage that judges another's work without editing it (`survey-review`, `seed-review`). |
| **Playbook** | The sections of `diocese.md` later map jobs read: publishers, rules settled, new lessons. |
| **Precedent** | A seed question `seed-review` settled by judgment, kept in `diocese.md` so the rest of the diocese is decided alike. |
| **Dispatcher** | The long-running Python process that picks jobs, starts workers, runs gates and records everything in the ledger. |
| **Ledger** | `data/factory/factory.db` (SQLite): Runs, jobs, attempts, steps, gates, flags, readings. |
| **Foreman** | The `foreman` skill you run by hand to review a job, a stage or a Run. |

## The pipeline

```
map Run   survey ─▶ survey-review ─▶ map × each batch ─▶ reconcile ─▶ promote ─▶ pr ─▶ you merge
                                    integrate when New lessons passes lessons_before_integrate,
                                    and once more before reconcile if any wait
seed Run  for each batch: seed × each parish ─▶ seed-review ─▶ pr ─▶ you merge
```

- **One job at a time.** When nothing runs, the dispatcher picks the active Run's next
  job; else a blocked Run whose issues are all answered; else a ready seed Run; else a
  map Run for the next diocese in `factory/queue.json`. Dioceses finish before new ones
  start. The stage order is code (`plan.py`), computed from the ledger and the Run's
  files, not queued ahead.
- **Jobs share work only through files and git**: records, seeds, `diocese.md`,
  `batches.json`, handoffs. A lead in a handoff goes to the job input of the batch it
  names. A lesson is appended to *New lessons* in `diocese.md`; `integrate` folds them
  into the playbook, keeps it near its target sizes, and lists each rule it merged or
  reworded, which the PR shows. Fixes across batches are advisory flags for `reconcile`.
- **Promote and pr are code**: promote runs `factory/stages/promote.yaml`'s commands;
  pr pushes, opens the PR and writes its summary from the ledger.
- **Seed Runs** use the map Run's batches. A parish is ready once the database has
  `seed_ready_bulletins` of its bulletins (counted daily after `pnpm data:pull`). The
  first seed Run starts at `seed_first_run_share` of the diocese ready, a follow-up seeds
  the rest, and after `seed_follow_up_weeks` each parish still not ready gets an issue.
- **After the PR opens** the Run doesn't change. A parked parish answered later goes to a
  small follow-up Run of the same kind (`map → promote → pr` or `seed → seed-review →
  pr`) once the PR is merged.

## A job

1. **Merge main.** At the start of each stage, if `origin/main` has moved, the dispatcher
   merges it into the Run branch, then loads the stage spec, so a job always runs with
   the spec and prompt of one commit. A conflict blocks the Run, except in
   `parishes.csv` and `churches.csv`, where main's side wins and promote runs again.
2. **Choose an account** under its caps (below).
3. **Start the worker** in the Run's worktree. The stage prompt is appended to Claude
   Code's system prompt; the first message is built in code (`render.py`): the folders,
   write boundaries, gates, the files in `reads:`, the handoff path and schema, then the
   stage's input. `pnpm factory prompt <stage>` previews it with sizes.
4. **Gate it**: the handoff exists and parses; every changed path matches the spec's
   `writes` (out-of-scope changes are reverted); HEAD didn't move; then the spec's gates.
5. **Then:**
   - all pass: commit with a `Factory-Job` trailer, push, act on the handoff (leads,
     lessons, verdicts, flags), and the next job follows;
   - a gate fails or a reviewer sends it back: the same session gets the problems, up to
     `max_send_backs`; then a seed parks its parish and anything else blocks the Run;
   - a usage limit: the job waits for the reset and resumes its session;
   - a crash: it resumes, or a fresh worker gets the files and what it was told; the
     Run blocks after `max_crashes`;
   - a session ending early (turns, minutes): "continue" `max_continues` times, then the
     Run blocks.

   Each step after the gates is recorded as it completes, so a restarted dispatcher
   doesn't commit or append twice. A job still `running` at startup counts as a crash.

Reviewers write only their handoff; the dispatcher acts on it. `survey-review`'s accepted
rules go into *Rules settled*. `seed-review` answers every open question by a rule, a
precedent or its own judgment, and the dispatcher runs `pnpm seed approve` with those
answers; judgment answers become precedents. It sends a seed back only for an error an
answer can't fix.

## What needs you

- **Issues.** A blocking flag becomes an issue labelled `factory`, `run:<diocese>` and
  `stage:<stage>`. Answer by commenting and closing it: your last comment is the answer,
  `/accept` takes the issue's suggestion (text after it is added), and closing without a
  comment reopens it. Only your login's comments count. Issues are polled every
  `issue_poll_minutes`.
- **PRs.** A map Run's PR lists coverage, open records, fetch gaps, advisory and settled
  flags, parked parishes, the playbook's sizes and every rule `integrate` changed. A seed
  Run's lists every decision `seed-review` made, answers against the drafter's lean
  first. Fix what's wrong, then **merge with a merge commit** so main keeps the Run's
  history. Merged Runs are noticed after the next fetch, and their worktrees removed.
- **Rules stay yours.** The factory never edits `rules.md`; turning a precedent or a
  decision into a rule is your own PR.
- **Reviews.** The `foreman` skill starts from `pnpm factory inspect <job>` and suggests
  changes to the stage spec; it changes nothing unless you ask.

## Usage and accounts

Each account is a Claude Code config directory signed in with `claude /login`; workers
use that subscription, not an API key. Before each attempt the dispatcher reads every
account's usage from the endpoint Claude Code uses. An account can take a job only if its
usage plus what the job is expected to use stays below `five_hour_cap` and below the paced
weekly cap, `weekly_cap × (days into the week + 1) ÷ 7`.

What a job is expected to use is its stage's `job_usage` in `factory/config.yaml`, points
of each window set from past jobs, so a survey needs much more room than a map batch.
Jobs already running on the account add their own `job_usage`, so jobs in parallel don't
count the same room twice. A job expected to use the whole cap or more starts only from
an unused window. The estimate only decides when a job starts: one that runs past the
cap is not stopped.

The job goes to the eligible account whose weekly window resets soonest, and stays on
it, since its session can only be resumed there. With none eligible, it waits for the
soonest one. A failing usage check pauses the factory; a 429 waits
`usage_cooldown_minutes` and tries again. `pnpm factory resume --override-caps` ignores
the caps until the next pause or resume; a worker's rate-limit error still makes its job
wait.

## Where a change goes, and when it takes effect

| You want to change… | It goes in | Takes effect |
|---|---|---|
| What one stage is told to do | `factory/prompts/<s>.md` | next stage start after merge to main |
| Model, effort, tools, limits, write scope, required reads, denied commands | `factory/stages/<s>.yaml` | same |
| How to research a diocese or seed a parish (shared with your sessions) | the skill | same |
| Record formats and field rules | `data/dioceses/README.md` | same |
| The queue | `factory/queue.json` | next fetch after merge |
| A number: caps, retries, send-backs, lesson threshold, cooldowns | `factory/config.yaml` | pull `~/carlo-factory`, restart |
| What a stage's first message or resume prompts say | `render.py` | pull, restart |
| What happens to a stage's output | `engine.py` (or the stage's module, once it has one) | pull, restart |
| The stage order, or a new stage | `plan.py` (+ spec, prompt) | pull, restart |
| Retry, crash, gate or resume mechanics | `engine.py`, `attempts.py` | pull, restart |
| How quota and tokens are measured | `metrics/` | pull, restart |

The first five reach a Run when it merges main; the rest when the dispatcher restarts.
Every change lands mid-Run, so:

- **Deploying Python:** `pnpm factory pause`, wait for the running job, merge, pull
  `~/carlo-factory`, restart the service, `pnpm factory resume`. Pausing first matters
  when a PR changes both Python and `factory/` files.
- **A new stage spec key** is added to `StageSpec` (defaulting to today's behaviour) in
  an earlier PR, deployed, than the first spec that uses it: a Run merges main before
  the dispatcher restarts, and an unknown key stops its stages loading.
- **No `factory/` file moves**: a Run worktree that hasn't merged the move would fail.

## Running it

1. Make the dispatcher its own checkout: `git worktree add ~/carlo-factory origin/main
   --detach`, and run `pnpm factory` from there. Its ledger, transcripts and Run
   worktrees live in its `data/factory/` (gitignored, on the Linux filesystem).
2. `uv sync --group dev --group factory`, `pnpm data:pull`, and R2 keys that can write in
   `.env` for the nightly ledger backup.
3. Sign each account in: `CLAUDE_CONFIG_DIR=<dir> claude /login`. List them, your GitHub
   login and any paths in `data/factory/local.yaml` (`factory/local.example.yaml`). `gh`
   must be signed in.
4. Try it without usage: `pnpm factory run --stub scenario.json` plays canned workers
   with its own ledger, worktrees, issues and PRs under `data/factory/stub/`, branches
   `factory-stub/<run>`, and no pushes. `--stub` on the other commands reads that ledger.
5. Start it: `pnpm factory run`, or the systemd unit `factory/carlo-factory.service`.

```
pnpm factory status                      Runs, the running job, usage, what waits on you
pnpm factory queue                       dioceses waiting for a map Run
pnpm factory pause [REASON] | resume     stop or start taking jobs
pnpm factory retry <job>                 run a blocked or failed job again
pnpm factory inspect <job> [--prompt]    everything about a job, for a foreman review
pnpm factory inspect --stage S --last N  a stage's recent jobs with their quota
pnpm factory prompt <stage> [--run R]    what the stage's next job would be given
pnpm factory quota [--by K] [--windows]  quota points per unit of work (factory-quota.md)
pnpm factory cost [--stage]              API-price dollars by Run or stage: a diagnostic
pnpm factory backup                      back the ledger up to R2 now
```

## Not built yet

- A dashboard; until then, `pnpm factory status`.
- Sandboxed workers instead of auto mode (#168).
- Several Runs or workers at once.
- An agent that tries to settle a blocking flag before it becomes an issue.
- Recording your corrections to reviewer decisions, and auto-merge once they're rare.
- Replay evals, to show a spec change helped.
