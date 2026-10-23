---
name: explore-diocese
description: Research a diocese the pipeline does not cover yet, or audit or extend one already explored, in data/dioceses/<diocese>/, using the `pnpm diocese` CLI. Covers finding each parish's bulletin, deciding which parishes share one, recording churches, closures and other exclusions with dated evidence, measuring coverage against diocesan lists, and promoting the result into data/parishes.csv and data/churches.csv. Use when asked to explore, add, research, audit or fix a diocese, a parish, a church or an exclusion.
---

# Exploring a diocese

Read `data/dioceses/README.md` before your first write. It has the rules, the file format,
the explanation standard, which sources to trust, and the traps. This page is the short
version.

To map a whole new diocese, follow the `map-diocese` skill: a `diocese-surveyor` agent sets
it up and plans small batches for `parish-scout` agents. This page is the method each of
them follows.

## The three rules

1. **One parish row = one bulletin.** Families, clusters, canonical mergers and decrees
   don't decide rows: the bulletin does. Several canonical parishes sharing one bulletin are
   one row; family members that each publish their own are separate rows.
2. **One church row = one place with public Mass now.** Oratories, chapels, shrines and
   campus chapels count. A closed building goes in `excluded/` with `reason: closed`; an
   open place that publishes nothing goes in with `reason: no-bulletin`, never `closed`.
3. **Every call is written down for an auditor.** A record's explanation and `evidence` let
   someone a year from now re-check it in minutes: a URL, the date you read it, the exact
   words, and what you inferred rather than read. Disagreements between sources are recorded,
   not smoothed over.

## Working loop

```bash
pnpm diocese list                                     # what exists
pnpm diocese todo <d>                                 # start here if the diocese exists
pnpm diocese init <d> --name "..." --state XX --gcatholic <key>   # new diocese
pnpm diocese roster fetch <d> gcatholic               # + the diocese's own directory:
pnpm diocese roster fetch <d> wpsl <finder URL>       #   or scrape it and `roster import`
                                                      #   (eCatholic finder map: parish-site-access finder.py)
```

Then, cheapest first:

1. **Structure before parishes.** Find the diocese's family/cluster list and its bulletins
   first. Settle "one bulletin or several" per group before creating rows.
2. **Find each bulletin:** `probe url <site>` (alive? redirected? squatted? which ids does
   it embed?), `probe po <org slug | LPi id>` (a ParishesOnline org's address, ids and
   latest issues), `probe container <a/b> --pages 3` (latest masthead; `--all --step 4` for
   a monthly changelog), `probe pdf <url> --grep <name>` (any bulletin's text; date closures
   this way). When `probe url` says HTTP4XX or NO-PARISH-WORDS, or finds no ids, the
   `parish-site-access` skill opens the site in a real browser, and it reads eCatholic and
   Discover Mass issues the way `probe container` reads ParishesOnline ones.
3. **Create records:** `pnpm diocese new parish|church|excluded|open <d> ...`. For churches,
   use `--from gcatholic:<id>` to prefill the address, Plus Code coordinates and evidence.
   **Then edit the file**: replace every TODO with the explanation, add dated `evidence` with
   verbatim `quote`s, and record `publication` ids on every parish.
4. **Before any parish row, run `pnpm diocese search <words>`.** It covers every diocese,
   the exclusions and the live CSVs.
5. **Merge rows that turn out to share a bulletin** with `pnpm diocese merge <d> <rows> --into
   <row>`. Only do it when the shared bulletin is current and each member's own old channel
   is silent. One live member channel means no merge.
6. **Account for every roster entry:** `pnpm diocese coverage <d> [--link]`. Link naming
   artefacts by adding `<roster>:<id>` to the record's `roster`, and create records for real
   gaps.
7. **Audit structure every session:** `pnpm diocese audit <d> [--fetch]`. Coverage can't see
   two rows that are really one bulletin.
8. **Check the fetch:** `pnpm fetch:check --diocese <d> --parish <slug>` resolves and
   downloads a row's bulletin before it is promoted (headed: `PLAYWRIGHT_BROWSER_CHANNEL=chrome
   xvfb-run -a` in the cloud sandbox).
9. **Finish:** `pnpm diocese validate <d>` (and `uv run pytest tests/test_dioceses.py`), a
   dated line in `diocese.md`'s *Log* with the coverage numbers, commit.

A closure after the fact: `pnpm diocese exclude <d> <church> --reason closed --last-mass
<date>`, then write why in the new `excluded/` file. Something you can't settle yet goes in
`open/` (or in `revisit` / `revisit_after` on a record), with the next step and a date. A
promoted church with no current Mass found and no source saying it closed: `pnpm diocese
question <d> <church> --revisit "..."`, which takes it off the site until it is settled.
A `no_bulletin` parish is kept in the records but left off the site.

## Don't

- Don't close, merge or delete anything on the strength of a plan, a decree, an old
  directory, an account name or an absence from a list. Read the current bulletin.
- Don't set `name_verified` / `address_verified` true without two independent sources.
- Don't quote from a summarizing fetch tool. Read the page itself (`probe pdf`, `curl`); the
  quote has to be findable by `pnpm diocese recheck`.
- Don't delete a promoted record: exclude or merge it, so `promote` removes its live row.
