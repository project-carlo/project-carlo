---
name: seed-evals
description: Run a historical eval of parish seeding on the labeled parishes - select them, assign seed-drafter agents, resume or verify the run, and score it against the labels - to measure a change to the drafting skill, its rules, a model or the batch size. Production seeds are drafted only by the onboarding factory's seed Runs.
---

# Seed evals

An eval drafts seeds for the labeled parishes, as of a past date, and scores them against
the labels. Its drafts go to `data/seed-evals/RUN/seeds/` and are never loaded or
approved. Production seeds come only from the onboarding factory's seed Runs
(`docs/factory-spec.md`). The design is in `docs/seeding-plan.md`. Drafters follow
`.claude/skills/draft-parish-seed/`, whose [rules.md](../draft-parish-seed/rules.md)
holds every slot decision. Your job is to prepare, assign, verify and score the run.
Don't make slot decisions yourself.

## Prepare and select

Run `pnpm data:pull` once before assigning work. Commands use the local database and the
R2 read keys; only model second opinions need API keys. Run plain `pnpm seed ...` (this
pnpm rejects `-s`). `pnpm seed --help` lists the commands by phase.

`pnpm seed pick --labeled --eval RUN [--limit N] [--resume]` creates the run's manifest or
reuses it. Pass `--eval RUN` to every command after that, including `check`, `finalize`
and `status`. Use a new run name for each batch-size or model comparison; reusing a run
keeps its manifest and its existing drafts.

Look at `pnpm seed status --eval RUN` for interrupted, blocked or invalid files. Assign
requested repairs explicitly: `pick --resume` offers unfinished drafts, not finished ones.

## Assign

Split the selected parishes into separate assignments for `seed-drafter`
(`.claude/agents/seed-drafter.md`), which preloads only `draft-parish-seed`. Give each agent
3 parishes by default, fewer for complex parishes, or the batch size the eval compares.
The agent definition sets the default model; override it only for a model comparison.

Make a private scratch folder for each agent before you start it (`mkdir -p`). Its message
gives:

- its parish slugs and the exact `--eval RUN`;
- its private scratch folder;
- which files already exist, and the exact problems to repair, if any.

Never give one parish to two active writers. The skill and the agent definition cover
everything else; don't repeat their instructions in assignments.

Parallel drafters share one usage limit. Ten at once used up a session's limit three
minutes in, and six failed mid-parish. Start about five, and add more as they finish.
When an agent fails on a usage limit, its files are safe. After the limit resets, resume
that same agent (`SendMessage` to it) instead of starting a new one. Paste its parishes'
lines from `pnpm seed status --eval RUN` as they are, not counts restated from memory.

## Verify and recover

When the agents finish, run `pnpm seed check <parish>... --eval RUN` on the assigned
slugs, and look at `pnpm seed status --eval RUN`. `pnpm seed check --all --eval RUN`
audits the whole run and reports malformed files one by one.

For bookkeeping problems, run `pnpm seed finalize <parish>... --eval RUN`. It doesn't
change decisions. Send any remaining problems back to a drafter with their exact messages.
Recovery follows the drafter's write boundaries: never edit a draft's decisions, and never
delete a seed file.

## Score and report

`pnpm seed score RUN` writes `data/seed-evals/RUN/report.md` and `report.json`. Compare
settled precision with recall, wrongly excluded slots, questions, calls and cost, against
the earlier runs the eval is measured against. Report what changed and by how much, with
the parishes and slots behind any difference that matters.
