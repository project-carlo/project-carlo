---
name: explore-diocese
description: The method for researching a diocese in data/dioceses/<diocese>/ with the `pnpm diocese` CLI, followed by the onboarding factory's survey, map, reconcile and integrate stages, and used directly to audit or fix a diocese already mapped. Covers finding each parish's bulletin, deciding which parishes share one, recording churches, closures and other exclusions with dated evidence, measuring coverage against diocesan lists, and promoting the result into data/parishes.csv and data/churches.csv. Use when asked to research, audit or fix a mapped diocese, a parish, a church or an exclusion. A new diocese is mapped by the factory: add it to factory/queue.json.
---

# Exploring a diocese

Read `data/dioceses/README.md` before your first write. It has the rules, the file format,
the explanation standard, which sources to trust, and the traps. This page is the short
version.

A whole new diocese is mapped by the onboarding factory (`docs/factory-spec.md`): add it to
`factory/queue.json`. Its survey, map, reconcile and integrate jobs follow this page.

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
3. **Write records:** `uv run python -m pdf_extract diocese write <d> <kind> <slug>
   --file record.json` patches flat fields plus `body`; lists replace existing lists.
   Add `--create` only for explicit new records; `--file -` reads stdin. It validates and
   writes atomically, returning slug, path and validation counts. See the README's payload
   example. Existing `new` and `merge` remain supported; `new church --from gcatholic:<id>`
   can prefill address, coordinates and evidence before a structured update. Replace TODOs
   with explanations, dated evidence and parish publication ids; don't use scratch
   `fill_record` scripts. For JSON pipelines use `pnpm --silent diocese` or direct `uv`;
   diagnostics stay on stderr, never `2>&1` into `jq`.
4. **Before any parish row, run `pnpm diocese search <words>`.** It covers every diocese,
   the exclusions and the live CSVs.
5. **Merge rows that turn out to share a bulletin** with `pnpm diocese merge <d> <rows> --into
   <row>`. Read current content: a live channel with a distinct bulletin prevents a merge;
   different URLs can serve the same document. Preserve supported `separate` / `shared`
   peer decisions in `publication_reviews`, apart from publication ids.
6. **Account for every roster entry:** `pnpm diocese coverage <d> [--link]`. Link naming
   artefacts by adding `<roster>:<id>` to the record's `roster`, and create records for real
   gaps.
7. **Audit structure every session:** `pnpm diocese audit <d> [--fetch]`. Read its candidate
   scope and limitations; coverage and distinct URLs can't establish separate documents.
8. **Check the fetch:** `pnpm fetch:check --diocese <d> --parish <slug>` resolves and
   downloads a row's bulletin before it is promoted (headed: `PLAYWRIGHT_BROWSER_CHANNEL=chrome
   xvfb-run -a` in the cloud sandbox). Review transport, document type, parish identity and
   freshness separately; successful transport alone isn't a verified current bulletin.
9. **Finish:** `pnpm diocese validate <d>` (and `uv run pytest tests/test_dioceses.py`).
   A change to a mapped diocese also gets a dated line in `diocese.md`'s *Log*.

A closure after the fact: `pnpm diocese exclude <d> <church> --reason closed --last-mass
<date>`, then write why in the new `excluded/` file. Something you can't settle yet goes in
`open/` (or in `revisit` / `revisit_after` on a record), with the next step and a date. A
promoted church with no current Mass found and no source saying it closed: `pnpm diocese
question <d> <church> --revisit "..."`, which takes it off the site until it is settled.
A `no_bulletin` parish is kept in the records but left off the site. Optional
`bulletin_status` records availability independently; it doesn't control promotion.

## Bounded research

Follow the README's structured `research` rules: save the method, URL when applicable,
checked date, outcome, next action and retry trigger with the affected record. Distinguish
not found, access blocked, unsupported format and not published. `todo <d>` exposes
unresolved research alongside revisits; inspect the record before retrying. An exhausted
check needs no repeat until the method/source changes or its retry trigger fires. Use
`retry_when` for dependencies and add `revisit_after` for scheduled checks. Don't impose a
fixed request budget that sacrifices evidence or turn a blocked search into certainty.

## Don't

- Don't close, merge or delete anything on the strength of a plan, a decree, an old
  directory, an account name or an absence from a list. Read the current bulletin.
- Don't set `name_verified` / `address_verified` true without two independent sources.
- Don't quote from a summarizing fetch tool. Read the page itself (`probe pdf`, `probe get`);
  the quote has to be findable by `pnpm diocese recheck`.
- Don't fetch with curl and a browser user agent (`-A "Mozilla/5.0 ..."`) or `-k`. The
  sandbox's safety check refuses them, as bot-check circumvention and TLS weakening, though
  not every time: in Wilmington it let about 70 through and stopped 4. Use `pnpm diocese
  probe get <url>` (`--out <file>` to save a PDF or page): the probes' own client, which
  verifies TLS. It handles pages, PDFs and JSON APIs such as WordPress's `/wp-json/`. When it
  reports a bot check or a 403, open the page with parish-site-access's `visit.py`; when the
  certificate doesn't verify, try `http://`. Don't retry with other headers.
- Don't delete a promoted record: exclude or merge it, so `promote` removes its live row.
- Don't infer shared-pastor associations from adjacent names or text. Preserve explicit
  parish/pastor links from the source; leave ambiguous associations unresolved.
