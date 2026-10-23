---
name: seed-parishes
description: Orchestrate batches of parish believed-schedule seeds, including historical eval runs. Use to select parishes, assign seed-drafter agents, resume a batch, verify results or score an eval; use draft-parish-seed for individual drafting and repairs.
---

# Seeding parish batches

A person reviews and approves every seed before the pipeline loads it. The design is in
`docs/seeding-plan.md`. Drafters follow `.claude/skills/draft-parish-seed/`, whose
[rules.md](../draft-parish-seed/rules.md) holds every slot decision. Your job is to
prepare, assign, verify and report the batch, and to propose new rules from the reviews.
Don't make slot decisions yourself.

## Prepare and select

Run `pnpm data:pull` once before assigning work. Commands use the local database and the
R2 read keys; only model second opinions need API keys. Run plain `pnpm seed ...` (this
pnpm rejects `-s`). `pnpm seed --help` lists the commands by phase.

Choose the context first, and keep it on every command that follows:

- Production: `pnpm seed pick [--limit N] [--diocese D] [--resume]` selects unseeded
  parishes, easiest first. `--resume` also offers files still `drafting`.
- Historical eval: `pnpm seed pick --labeled --eval RUN [--limit N] [--resume]` creates the
  run's manifest or reuses it. Pass `--eval RUN` to every command after that, including
  `check`, `finalize` and `status`. Eval drafts are never loaded.

Look at `pnpm seed status [--eval RUN]` for interrupted, blocked or invalid files. Assign
requested repairs explicitly: `pick --resume` offers unfinished drafts, not finished ones.

## Assign

Split the selected parishes into separate assignments for `seed-drafter`
(`.claude/agents/seed-drafter.md`), which preloads only `draft-parish-seed`. Give each agent
3 parishes by default, fewer for complex parishes. Change this when the user asks, or when
an eval gives evidence for another batch size. Larger assignments keep more PDF context,
but their cost depends on the runtime and on prompt caching. The agent definition sets the
default model; override it only for a requested model comparison in an eval.

Make a private scratch folder for each agent before you start it (`mkdir -p`). Its message
gives:

- its parish slugs, production or the exact `--eval RUN`, and its output directory;
- its private scratch folder;
- which files already exist, and the exact problems to repair, if any.

Never give one parish to two active writers. The skill and the agent definition cover
everything else; don't repeat their instructions in assignments.

Parallel drafters share one usage limit. Ten at once used up a session's limit three
minutes in, and six failed mid-parish. Start about five, and add more as they finish.
When an agent fails on a usage limit, its files are safe. After the limit resets, resume
that same agent (`SendMessage` to it) instead of starting a new one. Paste its parishes'
lines from `pnpm seed status` as they are, not counts restated from memory.

## Verify and recover

When the agents finish, run `pnpm seed check <parish>... [--eval RUN]` on the assigned
slugs, and look at `pnpm seed status [--eval RUN]`. `pnpm seed check --all [--eval RUN]`
audits the whole directory and reports malformed files one by one.

For bookkeeping problems, run `pnpm seed finalize <parish>... [--eval RUN]`. It doesn't
change decisions. Send any remaining problems back to a drafter with their exact messages.
Recovery follows the drafter's write boundaries: never edit a draft's decisions, and never
delete a seed file. Approved files belong to their reviewer.

Report the assigned parishes by status, with their open questions and unresolved checks,
and the churches the files list in `church_list_issues` (for whoever maintains
`data/churches.csv`). A ready file whose rationale holds a doubt it never asked about goes
back to its drafter, to become a question (rules.md asks by default).

Before returning a question to the reviewer, check whether an active rule already
settles it. In particular, R6 allows an assessed parish website schedule, R12 and R19
allow the specified older evidence, R35 establishes recurrence across bulletins, and
R36 retains a repeated schedule after one omission. Keep questions about unresolved
public access, hedged availability and unknown venues open; those still need a decision.

## Learn from reviews

After a batch has been reviewed, run `pnpm seed questions --answered [--eval RUN]`. Look
for answers that repeat a situation, and above all answers that go against the leaning.
In your report, propose each as a candidate for rules.md, in the same form as its
Candidates section: a When, a Lean, and the parishes and slots as evidence. Don't edit
rules.md yourself: the owner adds the candidates and promotes them.

## Eval and handoff

`pnpm seed score RUN` writes `data/seed-evals/RUN/report.md` and `report.json`. Compare
settled precision with recall, wrongly excluded slots, questions, calls and cost. Use a
new run name for each batch-size or model comparison; reusing a run keeps its manifest
and its existing drafts.

A person opens Seeds mode (`pnpm label`), answers the questions and approves. Approved
files are committed and merged in batches. The weekly run's before-copy compares newly
seeded schedules with the previous extracted ones, so a large batch can hold its change
gate.
