---
name: map-diocese
description: Map a whole new diocese from start to pull request as a lean orchestrator. Have a diocese-surveyor agent set up its rosters, structure and batch plan, then hand small batches of parishes to parish-scout agents one at a time, keep a playbook between batches, then cross-check, promote and open the PR. Use when asked to map, add or explore a whole diocese; use explore-diocese for single records, audits and fixes.
---

# Mapping a whole diocese

You own the diocese until its PR is open. The rules are in `explore-diocese` and
`data/dioceses/README.md`; read both before you start. This page covers how to split the
work so it uses as little of the usage limit as it can.

## Why the work is split this way

An agent reads its whole context again on every step, so the cost of running one grows
with the square of how long it runs. Scranton, Allentown and Harrisburg each ran as six or
seven region agents of 10 to 17 parishes, all at once and all on Opus. Each cost $60 to $100,
about two-thirds of it spent re-reading contexts that had grown past 400k tokens of bulletin
text, probe output and screenshots. In Allentown, four of the six agents hit the usage
limit, and each resume rebuilt a large context.

So:

- **Setup is done once, by one careful agent.** A `diocese-surveyor` agent
  (`.claude/agents/diocese-surveyor.md`, on Opus) creates the diocese, scrapes its rosters,
  reads its structure into `diocese.md`, seeds the playbook and plans the batches. Every
  batch is built on that work, so it gets the stronger model; it runs once, so the cost is
  small next to the scouts.
- **Bulky reading happens in short-lived contexts.** A `parish-scout` agent
  (`.claude/agents/parish-scout.md`, on Sonnet) researches about four parishes, writes their
  records and ends. The records, with their quoted evidence, are the result, so its report
  to you is a few lines.
- **Your context stays small.** Don't read bulletins, PDFs, probe output, rosters or whole
  records yourself. Work from command summaries (`todo`, `coverage`, `audit`, `validate`,
  `search`) and scout reports, filtered with `jq`. Read a record only to settle a question
  that spans batches.
- **One scout at a time.** Each scout starts from what the earlier ones learned, and the
  run never stalls at the usage limit with several half-finished agents. Run two at once
  only if the user asks for speed.
- **What scouts learn goes into files, not into your context.** The playbook is the
  diocese's `diocese.md`; reusable scripts go in the tools folder. After the diocese, lessons
  that apply everywhere go into the README, a skill or the CLI, where the next diocese gets
  them for free.

## 1. Survey

Before any scout starts, start one `diocese-surveyor` with `Agent` (`subagent_type:
diocese-surveyor`, in the foreground, since nothing else can happen until it's done). Give
it the diocese's name, its slug if you've chosen one, and anything the user said about it.
It runs `init`, sets up the browser and the scratch folders, fetches and scrapes the
rosters, writes `diocese.md`'s intro, *Sources* and *Bulletin publishers here*, and plans
the batches in `scratch/map-<d>/batches.md`. Its definition says how; don't repeat it.

If it runs out of turns or hits the usage limit, resume it with `SendMessage`; don't start
the scouts on a half-finished survey.

## 2. Review the survey

This is the one place you read files the survey wrote, because every batch depends on them.

1. Read its report, `diocese.md` and `batches.md`. Check the roster counts without reading
   the JSON: `jq '.entries | length' data/dioceses/<d>/rosters/*.json`, and list a roster in
   one line per entry if a batch looks wrong:
   `jq -r '.entries[] | [.id, .name, .city, .group] | @tsv' data/dioceses/<d>/rosters/<r>.json`.
2. Check that every roster entry is in one batch, that entries that might share a bulletin
   (one family, one pastor, one town) are together, and that the first batch is a typical
   one. Send anything missing or wrong back to the surveyor with `SendMessage`; its
   context still holds the diocese.
3. Decide its proposed rules and write them in `diocese.md` *Rules settled*.
4. `pnpm diocese validate <d>`, then commit: `<Diocese>: rosters, sources and batches`.
   `batches.md` stays in `scratch/`; tick batches off there as they finish.

## 3. Run the scouts, one at a time

Start each scout with `Agent` (`subagent_type: parish-scout`), and give it:

- the diocese slug and the batch's roster entries as `<roster>:<id>`, with name and town;
- its scratch folder `scratch/map-<d>/scouts/<n>/` and the tools folder
  `scratch/map-<d>/tools/`;
- any leads from earlier batches that touch these entries.

Don't repeat what the agent definition or the skills already say.

When it finishes:

1. Check its records: `pnpm --silent diocese validate <d> | jq '.dioceses[] | {errors,
   incomplete}'`. Send any problem back to the same scout with `SendMessage`; its context
   still holds the parish.
2. Add its learnings to *Bulletin publishers here* (or *Rules settled*, for a decision),
   merged into what is there, not appended as a log.
3. Put each lead next to the batch it touches in `batches.md`, or settle it now if it
   spans batches (a merge, a church that belongs to another row).
4. Commit: `<Diocese>: batch <n> (<area>)`.

When a scout runs out of turns or hits the usage limit, resume it with `SendMessage` after
the reset instead of starting a new one. Its records are on disk either way.

## 4. Other tasks for a scout

Give a scout any job whose reading is large and whose answer is short. Say in the message
what it may write and what to report. For example:

- scraping a roster the survey couldn't get, or refreshing one with the surveyor's script
  in the tools folder (`roster import`); report the entry count and anything odd;
- dating a closure by grepping a bulletin archive; report the date and the quote;
- linking the `coverage` entries left unmatched at the end, when there are more than a
  handful;
- the full fetch check (section 5); report only the rows that are not this week's issue.

Keep for yourself whatever spans batches or sets policy: merges across batches, rules for
the whole diocese, `diocese.md`, promotion and the PR.

## 5. Finish

1. `pnpm diocese coverage <d> --link`, then account for what is left.
2. `pnpm diocese audit <d> --fetch`: the only check that catches two rows publishing one
   bulletin. Settle each group it lists.
3. A fetch check of every row, as a scout task:
   `PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm fetch:check --diocese <d>`.
   Discover Mass limits downloads per IP per day; if it refuses some rows, check those
   again once the limit resets.
4. `pnpm diocese validate <d>` and `todo <d>`. Write a dated line in `diocese.md`'s *Log*
   with the coverage numbers, how many scouts ran and the batch size.
5. `pnpm diocese promote <d> --dry-run`, read it, then `promote`, `uv run pytest` and the
   lint the repo runs. Commit, push and open the PR.
6. **Lessons for every diocese.** List in the PR description what a scout had to work out
   that would help in any diocese: a publisher's quirk worth a line in the README's
   *Traps*, a script every batch rewrote that belongs in the CLI. These make the next
   diocese cheaper.
