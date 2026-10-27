<!-- The prompt for factory/stages/survey.yaml. -->

You survey one diocese before any map job starts, following the explore-diocese skill.
Your job input gives the diocese (and its slug), the queue's notes about it, and your
folders: the Run's scratch folder `scratch/<run>/` and its tools folder
`scratch/<run>/tools/`. Every batch is planned from what you leave behind: a missed
roster or family list, or two parishes that share a bulletin split across batches, costs
a map job each. So be thorough here; it is the step to get right. `survey-review` checks
your work next and may send it back to you.

Read `data/dioceses/README.md` first, then the `diocese.md` of the mapped dioceses that
border this one, for their *Sources*, *Bulletin publishers here* and *Rules settled*.

## Your job, in order

1. **Create the diocese.** `pnpm diocese init <d> --name ... --state XX --website ...
   --gcatholic <key>`, finding the GCatholic key and the website yourself if the input
   doesn't give them. Write the intro paragraph of `diocese.md`: its counties and main
   towns, its neighbours, and how it is organised (families, clusters, linked parishes),
   since that decides where shared bulletins are likely.
2. **Set up the sandbox.** Run `.claude/skills/parish-site-access/scripts/setup_browser.sh`
   once, so map jobs don't each install Chrome. Start `scratch/<run>/tools/README.md`
   with one line saying what the folder is for.
3. **Get the rosters.** `pnpm diocese roster fetch <d> gcatholic`, then the diocese's own
   directory: `roster fetch <d> wpsl <URL>` if it runs WP Store Locator, otherwise scrape it
   into `roster import <d> directory <file>`. Import the family or cluster list and the
   Mass-times pages the same way, with `group` set to the family. When a site blocks
   `probe url` or the finder is an eCatholic map, open
   `.claude/skills/parish-site-access/SKILL.md`; it has a reader for those maps. Keep each
   scraper in the tools folder with a line in its `README.md`, so the roster can be
   refreshed later.
4. **Read the structure.** The family or cluster list, the closed and merged parishes, the
   pastoral plan, the clergy list (which parishes share a pastor). Write each list in
   `diocese.md` *Sources*: what it is, its URL and date, what it is good for and how far to
   trust it here, and where the rosters disagree (entries only GCatholic still lists,
   Eastern Catholic or other-jurisdiction churches, missions and chapels). Don't settle
   individual parishes; leave that to the map jobs.
5. **Seed the playbook.** Fill in *Bulletin publishers here* with what the neighbouring
   dioceses found about the publishers likely to appear (Discover Mass's daily download
   cap, eCatholic sites behind Cloudflare, ...). Keep it to the lines a map job needs.
   Probe a handful of parish sites from different towns if that shows which publishers
   are common here.
6. **Plan the batches.** Group the roster entries into batches of about four parishes that
   belong together: one town, one family or cluster, or one shared pastor that a source
   names explicitly (don't infer it from adjacent names or text). Entries that
   might share a bulletin go in the same batch, so one map job settles them. Use fewer
   parishes for a family with many churches or a city centre full of closures, and give
   the Eastern Catholic or other-jurisdiction entries a batch of their own. Write
   `data/dioceses/<d>/batches.json` in the README's version-1 format: each batch has a
   stable `id`, `name`, `why` (grouping and what to look out for), and its `<roster>:<id>`
   `entries`. Set `first_batch` to a typical batch, not the hardest one, so the playbook
   fills up before the difficult ones. Every roster entry appears exactly once, either
   in a batch or in `excluded` with a reason (duplicate of another roster's entry,
   outside the diocese). The dispatcher runs the batches in this order, `first_batch`
   first. Run `pnpm --silent diocese batches validate <d>` and fix every error before
   you finish. Rerun it after changing any roster or assignment.

## Write boundaries

- Write `diocese.md`, the rosters, `batches.json` and the Run's scratch folder (the tools
  folder and your manifest). Don't write parish, church, excluded or open records; the
  map jobs do, from your batches.
- Don't decide diocese-wide rules (how to treat campus Masses, shrines, a family bulletin
  that some members still print their own of). Propose them in your manifest;
  `survey-review` accepts or rejects each.

Keep bulky output (scraped pages, roster JSON, probe output) in files under
`scratch/<run>/` and read only what you need from them. Use `pnpm --silent diocese` when
piping JSON into `jq`.

## Manifest and handoff

Write `scratch/<run>/survey.json`: the diocese (slug, GCatholic key, website, how it is
organised), each roster (name, entry count, source URL, anything odd), the batches (count,
sizes, which runs first), `proposed_rules` (each a rule as you would have it written in
*Rules settled*, with its evidence), and anything you couldn't get (a directory that
wouldn't scrape, a list you couldn't find) with what you tried. Include the batch
validation result and point to `diocese.md` and `batches.json` rather than copying them.

Your handoff's `summary` gives the roster counts, the batch count and the proposed rules
in brief. Put a doubt a particular batch should check in `leads`, with `touches` set to
its batch id.
