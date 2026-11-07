<!-- The prompt for factory/stages/map.yaml. -->

You map one batch of a diocese's parishes, following the explore-diocese skill. Your job
input gives your roster entries, any leads from earlier jobs that touch them, and the
diocese's playbook: the *Bulletin publishers here*, *Rules settled* and *New lessons*
sections of its `diocese.md`, which earlier jobs left (which publishers print here, how to
read each, which sites block the browser and where their bulletins are instead). When it
gives an owner's answer instead, you map only the entries it names, following the answer.

## Reading bulletins and sites

- Grep a bulletin before reading it (`probe pdf <url> --grep <name> --grep Mass`, `--pages`,
  `--chars`). You need the masthead, the Mass schedule and the lines that settle a question,
  not the whole issue.
- Take a screenshot or render a page only when the text can't answer the question.
- Open `.claude/skills/parish-site-access/SKILL.md` only when `probe url` can't read a
  site. The browser is already set up.
- Reread a record only for the part a new question needs.

## Write boundaries

- Write records only for your batch's roster entries and the places you find through them
  (a mission or chapel in the bulletin's Mass schedule). Run `pnpm diocese search <words>`
  before creating one.
- Merge only rows inside your batch. Don't edit records outside it, `diocese.md`, rosters,
  CSVs, policy or code. Something a later batch should check (a possible shared bulletin,
  a wrong roster entry) is a lead, with `touches` set to its batch id or `roster:id`. A fix
  across batches (a merge, a church that belongs to another batch's row) is an advisory
  flag; `reconcile` settles those once every batch is mapped.
- A lesson is for the batches after yours: a publisher's method (how to recognise its
  sites, read its issues or record them; an id pattern; a download cap) or a decision
  that applies to several records. Never one parish's detail (its URL, masthead, address,
  closure, or which publisher prints it): that is in its records, and no later batch maps
  that parish. Nor what the playbook or the README already says. Most batches have one
  or two lessons, or none. They go in your handoff's `lessons`, not in `diocese.md`: the
  dispatcher adds them to *New lessons*, and `integrate` folds those into the playbook.
- A script the next map job could use goes in the tools folder, with one line in its
  `README.md`: what it does and how to run it.

## Each parish

Finish each parish (its records written, evidence quoted, its fetch check run) before
starting the next. Check a row with `PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm
fetch:check --diocese <d> --parish <slug>`, and record the `recipe` it prints for `other`
rows once its pick is the correct current bulletin. What you can't settle is structured
`research` with a retry trigger, never a guess. At the end, run `pnpm --silent diocese
validate <d>` and fix errors and unfinished explanations in your own records.

A parish you can't settle without the owner's decision gets a blocking flag with
`scope: parish`, and the rest of the batch carries on. Don't flag what the records carry
instead (README, *What to flag*): a church no source settles, a bulletin `fetch` can't
collect, a check blocked for now, sources that disagree on an address.

## Manifest and handoff

Write a small `manifest.json` in your scratch folder: changed paths, counts by kind,
checks run and their results and scope, decisions made or unresolved. Reference records
for full evidence; don't copy their bodies or probe output into it.

Your handoff's `summary` gives the counts and the validation result (say whether it
covers your batch or the diocese). Leads, flags and lessons go in their own fields; empty
lists are fine. If you run out of room, leave completed records and a manifest showing
what remains, and hand off with status `partial`.
