---
name: map-diocese
description: Map a whole new diocese from start to pull request as a lean orchestrator. Set up its rosters and structure, hand small batches of parishes to parish-scout agents one at a time, keep a playbook between batches, then cross-check, promote and open the PR. Use when asked to map, add or explore a whole diocese; use explore-diocese for single records, audits and fixes.
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

## 1. Set up

1. `pnpm diocese init <d> ...` and `pnpm diocese roster fetch <d> gcatholic`. If the
   diocese's directory runs WP Store Locator, `roster fetch <d> wpsl <URL>`. If scraping it
   takes more than reading one page, give it to a scout as a task (section 4).
2. Run `.claude/skills/parish-site-access/scripts/setup_browser.sh` once, so scouts don't
   each install Chrome.
3. Make the scratch folders (`scratch/` is ignored by git):
   `mkdir -p scratch/map-<d>/tools scratch/map-<d>/scouts` and start
   `scratch/map-<d>/tools/README.md` with one line saying what the folder is for.
4. Read the structure: the diocese's family or cluster list, its closed-parishes page, its
   pastoral plan. Write what you find in `diocese.md` *Sources*. This is the one place you
   read source pages yourself, because the batches depend on it.
5. Copy the playbook from the dioceses already mapped: in `diocese.md`, fill in the
   *Bulletin publishers here* section that `init` put under *Sources* with what earlier
   dioceses in the same region found about the publishers likely to appear (e.g. Discover
   Mass's daily download cap, eCatholic sites behind Cloudflare). Keep it to the lines a
   scout needs.

## 2. Plan the batches

List the roster in one line per entry rather than reading the JSON:
`jq -r '.entries[] | [.id, .name, .city, .group] | @tsv' data/dioceses/<d>/rosters/<r>.json`.

Group the entries into batches of about four parishes that belong together: one town, one
family or cluster, or one shared pastor. Entries that might share a bulletin go in the same
batch, so one scout settles them. Use fewer parishes for a family with many churches or a
city centre full of closures. Write the batches to `scratch/map-<d>/batches.md`, with each
batch's roster ids, and tick them off there as they finish.

Start with a typical batch, not the hardest one, so the playbook fills up before the
difficult ones.

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

- scraping the diocese's parish finder or Mass-times pages into a roster (`roster import`);
  report the entry count and anything odd;
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
