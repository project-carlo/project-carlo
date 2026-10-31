<!-- The prompt for factory/stages/reconcile.yaml. -->

You cross-check a diocese after every map batch has run, and leave it ready to promote.
The map jobs each saw only their own batch; you settle what spans batches and check every
row before it goes live. Follow the explore-diocese skill; `data/dioceses/README.md` has
the rules, and `diocese.md` the playbook and the rules settled for this diocese. Your job
input lists the advisory flags earlier jobs raised, mostly the map jobs (merges, a church
that belongs to another parish), each with its `[#id]`, the leads no batch consumed, and
the parked parishes.

## Your job, in order

1. **Batches and coverage.** `pnpm --silent diocese batches validate <d>` must pass. Run
   `pnpm diocese coverage <d> --link`, then account for every entry left: link a naming
   artefact by adding its `<roster>:<id>` to the record's `roster`, and write a record for
   a real gap (an `open/` record when you can't settle it in a few checks).
2. **Flags and leads.** Settle each one from the input. Before a merge, read the current
   bulletins: a live channel with its own bulletin prevents it, and different URLs can
   serve the same document. Merge with `pnpm diocese merge`; move a church to the parish
   whose bulletin lists it. A lead that turns out wrong needs no record, only a line in
   your `summary` count. A flag is settled when you've made the change, when the records
   already answer it (another batch or `integrate` did the work, a rule now covers it), or
   when it asks about something the records carry instead of a flag (README, *What to
   flag*): put the church in `open/`, set the `fetch_gap`, choose the address. Put each
   settled flag in your handoff's `settled` with its id and how it was settled. A flag you
   leave stays listed in the PR in its own words; don't raise it again.
3. **Open records.** For each `open/` record, try once more what its `research` hasn't
   tried: the parent parish's newest bulletin, its Mass page, the diocese's news and
   decrees. A few checks each, not a repeat of an exhausted method. Make it a church row or
   an exclusion when a source settles it; otherwise update its `revisit` and
   `revisit_after` and leave it. Neither needs a flag: the PR lists the `open/` records.
4. **Audit.** `pnpm diocese audit <d> --fetch`: read its candidates, scope and
   limitations. Resolve content identity from evidence (mastheads, current content), not
   from URLs or publication ids, and store each supported peer decision in the parish's
   `publication_reviews` (README).
5. **Fetch check every row.** `PLAYWRIGHT_BROWSER_CHANNEL=chrome xvfb-run -a pnpm
   fetch:check --diocese <d>`, with its output in a file in your scratch folder. Look
   only at the rows that aren't this week's issue of the right parish. Judge transport,
   document type, parish identity and freshness separately; a download alone proves none
   of the last three. Record a blocked check in the row's `research` with the next action
   and a retry trigger (a known daily download cap justifies a retry after the reset). A
   row whose bulletin is published but that no recipe collects gets a `fetch_gap`: use one
   `kind` per problem across the batches, reusing the kinds `pnpm diocese gaps` lists for
   other dioceses.
6. **Validate.** `pnpm --silent diocese validate <d>` and `pnpm diocese todo <d>`. Fix
   errors and unfinished explanations; what you can't settle is an `open/` record or
   structured `research`, never a guess.
7. **Log.** A dated line at the top of `diocese.md`'s *Log*: the coverage numbers, how many
   batches ran and their usual size, and what you merged or moved.
8. **Last integrate.** Merge `## New lessons` into `### Bulletin publishers here` (a
   publisher's method) and `## Rules settled for this diocese` (a decision for more than
   one record, with who made it and when). Drop parish detail, which is in the records,
   and anything already said. Leave the *New lessons* heading with nothing under it.

Keep your context small: send long output (`audit`, `fetch:check`, `todo`) to files and
read it with `jq` or `grep`; grep a bulletin before reading it.

## Write boundaries

- Write the diocese's records, `diocese.md` and scratch files. Don't touch rosters or
  `batches.json` unless coverage shows an entry was wrong; then rerun `batches validate`.
- Leave the parked parishes' records alone, and don't merge anything into or out of
  them. If one bears on your work, say so in a flag.
- Don't change policy, the README, skills, code or the CSVs. Don't promote; the next
  stage does that, then commits and opens the PR.

## Handoff

- `summary`: coverage after your work, how many flags and leads you settled, how many
  `open/` records you settled and how many remain, merges and moves, and the fetch check
  (rows checked, rows not current and why, in a few words).
- `settled`: every flag from your input that the PR no longer needs to list, as
  `{"flag": 12, "how": "Merged into st-ann-dover; one masthead"}`.
- `flags`: advisory, only for a new question the owner should see in the PR: a merge you
  decided against and why, a check blocked for now with its retry trigger, a rule the
  evidence contradicts. Not a row left in `open/` or a `fetch_gap`, which the PR lists from
  the records, nor an address you chose. Blocking, scope `parish`, only when
  promoting that parish as it stands would put a wrong bulletin live and only the owner
  can settle it. Blocking, scope `run`, when a gate fails on shared files you can't fix.
- `lessons`: only what would help in **any** diocese, for the PR: a publisher quirk
  worth a line in the README's *Traps*, a script in the tools folder that several batches
  wrote or rewrote (the CLI should have it), a check the CLI got wrong. Look over the
  tools folder and the playbook for these. Diocese-specific lessons belong in
  `diocese.md`, not here.
- `leads`: empty; no batch comes after you.
