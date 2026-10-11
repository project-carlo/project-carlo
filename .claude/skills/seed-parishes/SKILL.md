---
name: seed-parishes
description: Orchestrate batches of parish believed-schedule seeds, including historical eval runs. Use to select parishes, assign seed-drafter agents, resume a batch, verify results or score an eval; use draft-parish-seed for individual drafting and repairs.
---

# Seeding parish batches

A person reviews and approves every seed before the pipeline loads it. The design is
`docs/seeding-plan.md`; the shared file contract is
[docs/seeding-file.md](../../../docs/seeding-file.md). The drafter reads `POLICY` and makes
slot decisions. Your job is to prepare, assign, verify and report the batch.

## Prepare and select

Run `pnpm data:pull` once before assigning work. Commands use the local database and R2
read keys. Only model second opinions need their API keys. Run plain `pnpm seed ...`;
this pnpm rejects `-s`. Use `--json` when you need the full result.

Choose the context first and keep it on every subsequent command:

- Production: `pnpm seed pick [--limit N] [--diocese D] [--resume]` selects unseeded
  parishes, easiest first. `--resume` also offers files still `drafting`.
- Historical eval: `pnpm seed pick --labeled --eval RUN [--limit N] [--resume]` creates
  the run manifest or reuses it. Every parish command then needs `--eval RUN`, including
  batch `check`, `finalize` and `status`. Drafts are never loaded. Live website lookup is
  forbidden because it can reveal information after the cutoff.

Inspect `pnpm seed status [--eval RUN]` for interrupted, blocked or invalid files. Assign
requested repairs explicitly; `pick --resume` offers unfinished drafts, not completed ones.

## Assign

Split the selected parishes into disjoint assignments for `seed-drafter`
(`.claude/agents/seed-drafter.md`), which preloads only `draft-parish-seed`. Default to
3 parishes per agent, fewer for complex parishes; change this when the user requests it
or an eval supplies evidence for another batch size. Larger assignments retain more PDF
context, but their cost depends on the runtime and prompt caching. The agent definition
owns the default model; override it only for a requested model comparison in an eval.

Create a private scratch folder for each agent before spawning it (`mkdir -p`). Include:

- Its parish slugs, production or the exact `--eval RUN`, and its output directory.
- Its private scratch folder.
- Which files already exist and the concrete problems to repair, if any.
- The instruction to resume existing files in place, preserve calls and evidence, and
  finish and write each parish before starting the next.

Do not assign the same parish to two active writers. The drafter's instructions cover
policy reading, evidence, websites, model calls and writing boundaries; do not duplicate
those instructions in every assignment.

## Verify and recover

After the agents finish, verify the assigned slugs with
`pnpm seed check <parish>... [--eval RUN]`, and inspect
`pnpm seed status [--eval RUN]`. To audit the whole selected directory, use
`pnpm seed check --all [--eval RUN]`; malformed files are reported individually.

For bookkeeping problems, run `pnpm seed finalize <parish>... [--eval RUN]`. Its defaults,
source expansion, read marks, history sources, `as_of` and status do not change decisions.
Return remaining problems to a drafter with their exact messages. Never edit its substantive
decisions or delete its seed file: deletion loses evidence and resets the paid-call counter.
If the drafter cannot resolve a problem, preserve the draft and report its blocked reason
or leave the decision to the reviewer. Approved files belong to their reviewer.

Report the assigned parishes by status, with open questions and unresolved checks. The
reviewer sees the seed in the labeler, so substantive doubts must also be in its questions.

## Eval and handoff

`pnpm seed score RUN` writes `data/seed-evals/RUN/report.md` and `report.json`. Compare settled
precision alongside recall, wrongly excluded slots, questions, calls and cost. Use a new
run name for each batch-size or model comparison; reusing a run preserves its manifest
and existing drafts. Historical evals use only cutoff-visible bulletins and history.

A person opens Seeds mode (`pnpm label`), answers questions and approves. Approved files
are committed and merged in batches: the weekly run's before-copy compares newly seeded
schedules with the previous extracted schedules, so a large batch can hold its change gate.
