<!-- The prompt for factory/stages/map.yaml. -->

You map one batch of a diocese's parishes, following the explore-diocese skill. Your job
input gives the diocese, your roster entries, your scratch folder, the Run's shared tools
folder, and any leads from earlier jobs that touch your entries. When it gives an owner's
answer instead, you map only the entries it names, following the answer.

Before your first write, read `data/dioceses/README.md`, then the diocese's `diocese.md`.
Its *Sources*, *Bulletin publishers here* and *Rules settled* sections are the playbook the
earlier map jobs left: which publishers print here, how to read each, which sites block the
sandbox and where their bulletins are instead. Read the tools folder's `README.md` before
writing a script; one may already do what you need.

## Keep your context small

Everything you read stays in your context and is read again on every later step, so a
large read early on is paid for many times over.

- Grep a bulletin before reading it (`probe pdf <url> --grep <name> --grep Mass`, `--pages`,
  `--chars`). You need the masthead, the Mass schedule and the lines that settle a question,
  not the whole issue.
- Send long command output to a file in your scratch folder and read only the part you
  need (`jq`, `grep`, `head`).
- Take a screenshot or render a page only when the text can't answer the question.
- Open `.claude/skills/parish-site-access/SKILL.md` only when `probe url` can't read a
  site. The browser is already set up.
- Keep full evidence and parish-specific findings in the records; reread only the parts
  needed to settle a new question. Shared playbook lessons must be reusable across parishes.

## Write boundaries

- Write records only for your batch's roster entries and the places you find through them
  (a mission or chapel in the bulletin's Mass schedule). Run `pnpm diocese search <words>`
  before creating one.
- Merge only rows inside your batch. Don't edit records outside it, `diocese.md`, rosters,
  CSVs, policy or code. Something a later batch should check (a possible shared bulletin,
  a wrong roster entry) is a lead, with `touches` set to its batch id or `roster:id`. A fix
  across batches (a merge, a church that belongs to another batch's row) is an advisory
  flag; `reconcile` settles those once every batch is mapped.
- A reusable lesson goes in your handoff's `lessons`, not in `diocese.md`: the dispatcher
  adds it to *New lessons*, and `integrate` merges those into the playbook.
- A script the next map job could use goes in the tools folder, with one line in its
  `README.md`: what it does and how to run it.

Write structured updates with `uv run python -m pdf_extract diocese write <d> <kind>
<slug> --file record.json`; use `--create` only for explicit new records. See the README's
payload example and list-replacement rules. Don't build scratch `fill_record` writers.

Finish each parish (its records written, evidence quoted, its fetch check run) before
starting the next. Check a row with `PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm
fetch:check --diocese <d> --parish <slug>`, and record the `recipe` it prints for `other`
rows once its pick is the correct current bulletin. Distinguish transport, document type,
parish identity and freshness; a successful download alone doesn't settle them. Use the
README's bounded-research rules for blocked or exhausted checks; preserve uncertainty and
retry triggers instead of repeating the same search. At the end, run
`pnpm --silent diocese validate <d>` and fix errors and unfinished explanations in your own
records. Unresolved research belongs in structured `research`, not fabricated certainty;
a parish you can't settle without the owner's decision gets a blocking flag with
`scope: parish`, and the rest of the batch carries on.

## Record it, don't flag it

Three things go in the records, not in a flag (README, *What to flag*):

- **A church you can't settle.** No source shows Mass there now and none says it closed:
  an `open/` record, with the next check in `revisit` and a date in `revisit_after`. The
  PR lists every `open/` record.
- **A bulletin `fetch` can't collect.** The parish publishes one, but no recipe reads it
  (a host that answers 403, links that aren't PDFs, an HTML-only bulletin, an embedded
  viewer): set the row's `fetch_gap`, reusing a `kind` that `pnpm diocese gaps` lists for
  the same problem.
- **Sources that disagree on an address or a name.** Choose, preferring the parish's and
  the diocese's own sources unless you have a reason not to, and say why in *Name and
  address*.

## Manifest and handoff

Write a small `manifest.json` in your scratch folder: changed paths, counts by kind,
checks run and their results and scope, decisions made or unresolved. Reference records
for full evidence; don't copy their bodies or probe output into it.

Your handoff's `summary` gives the counts and the validation result (say whether it
covers your batch or the diocese). Leads, flags and lessons go in their own fields; empty
lists are fine. If you run out of room, leave completed records and a manifest showing
what remains, and hand off with status `partial`.
