---
name: draft-parish-seed
description: Draft, resume or repair a parish's believed-schedule seed with the pnpm seed CLI. Use for an individual seed or when assigned parishes by the seed-parishes orchestrator.
---

# Drafting a parish seed

A seed becomes the schedule update mode maintains. Read `POLICY` in
`src/pdf_extract/classifiers/schedule_policy.py` in full before drafting, and read
[the shared seed file reference](../../../docs/seeding-file.md) before your first draft.
The policy decides which events count; do not substitute extract-mode history for it.

Use the local database prepared by the orchestrator (`pnpm data:pull`) and the R2 read keys.
For a direct request, prepare it once and create a private temporary scratch folder yourself.
Run plain `pnpm seed ...`; this pnpm rejects `-s`. Add `--json` for full output.

Your assignment identifies the parishes, a private scratch folder, and production or
`--eval RUN`. In an eval, pass `--eval RUN` to every parish command, including `church`,
`mark-read`, `finalize`, `check` and `status`. Drafts belong in `data/seed-evals/RUN/seeds/`;
production drafts belong in `data/seeds/`. `score RUN` takes the run positionally.

Manually edit only your assigned seed files and files in your scratch folder. CLI-generated
PDFs, PNGs and caches under `data/seed-work/` and the local blob cache are allowed. Do not
change the policy, CSVs, scripts or another agent's files. Use one writer per parish and
run its model calls sequentially. Do not spawn further agents.

## One parish at a time

Finish and write each parish's file before starting the next. Resume an interrupted file in place.

1. Inspect whether the seed file exists. For new work, `pnpm seed init <parish>`;
   for an interrupted draft or a repair, `pnpm seed init <parish> --resume`. Read the
   existing file before editing it, preserve its `calls` and useful evidence, and change
   only the decisions that need correction. Never delete and restart it. An approved
   file belongs to its reviewer and cannot be resumed. New `init` writes a `drafting`
   file listing the parish's bulletins, and prints what you start from: its website, its
   churches with their addresses, its bulletins newest first (issue date, page count,
   whether extract mode flagged one as a wrong bulletin or it repeats another PDF), a
   summary of extract mode's recent history, and the newest PDF's path. `pnpm seed brief
   <parish>` prints it again. Older bulletins often say `no PDF (history only)`: the PDF was
   pruned, so you can cite its history but not read it. Fill the file in as you go,
   editing the JSON directly (see `docs/seeding-file.md`); you need no script
   to build it. If you do write a helper, keep it in the scratch folder the orchestrator
   gave you, never the shared one.
2. **Read the newest bulletin in full**: the PDF `init` wrote (`pnpm seed pdf <parish>
   <hash>` writes any other; page numbers match the pipeline's). For a page that is only an
   image or a dense table, `pnpm seed pages <parish> <hash> --page N [--dpi 200]` renders a
   PNG to look at. Draft every Mass, Confession and Adoration slot the policy asks for,
   with its page. After reading, run `pnpm seed mark-read <parish> <hash>`, even if
   the bulletin has no useful schedule or is the wrong bulletin. If the newest bulletin
   is unusable, mark the parish blocked unless its remaining evidence supports explicit
   questions for a reviewer. Write down what you leave out on purpose too (a Communion
   Service, a chapel at another address, a school Mass): the reviewer needs these calls.
3. **Compare with history.** `init`'s summary shows each recent history event and how many
   bulletins it is in; `pnpm seed history <parish> [--bulletins N]` gives one table per
   bulletin. Free. It came from an older prompt, so a difference is a reason to look
   closer, not a vote.
4. **Read further back** when a question needs it. `pnpm seed grep <parish> [pattern]`
   searches the text of every stored bulletin at once, newest first (with no pattern, for
   schedule words): use it to see which bulletins print a slot before reading any. Then
   read one bulletin at a time by its text: `pnpm seed text <parish> <hash> [--page N]`
   usually uses less context than the PDF; the saving depends on its layout. Read a page
   as an image (`seed pages --page N`) only when
   `seed text` or `seed grep` says it is only an image, or its layout matters (a schedule
   grid whose text comes out scrambled). Look further back for:
   - a slot printed in only one bulletin (weekly, or a one-off?)
   - a time or day that differs from history or between bulletins
   - a seasonal hint ("summer schedule", "beginning in Advent")
   - a newest bulletin that looks like an old issue, or another parish's

   Mark each bulletin read with `seed mark-read`; cite the evidence for each slot in
   an `agent` source. Do not invent a slot just to record that you read a bulletin. Before
   calling a weeks-of-the-month slot (First Friday Holy Hour) "seen once", check whether the
   other bulletins' calendars even cover a week it falls in (`seed brief` prints which
   weeks of the month the newest bulletin's week holds). For a church or chapel the
   bulletin names, `pnpm seed church <name, town or street>` says whether it is in
   `data/churches.csv` and whose it is; it matches every word in any order, so try the
   name with its town ("Immaculate Conception Ithaca") and then the town alone before
   concluding a church is missing.
5. **The parish website is an extra source, not a step.** In a historical eval, skip
   website lookup entirely: live pages may reveal changes after the cutoff and `check`
   rejects website sources. In production, look at it only when a question needs it: the
   bulletins disagree, or a slot's location or regularity is unclear. `pnpm seed site
   <parish>` prints the homepage's own text and the links on it that look like schedules;
   `pnpm seed site <parish> /mass-times` (or a full address) prints one of those. It gets
   past most Cloudflare checks and pages a script draws, and keeps each page for a day.
   Quote it as `{"source": "website", "url": "<the address it printed>", "said": "..."}`,
   in the page's words, never a time you worked out. If it can't read the site, say so in
   the rationale and rely on the bulletins. Websites go stale: one can back a reading up,
   or settle where a chapel is or that a "First Saturday" Mass is monthly, but it doesn't
   outweigh the newest bulletin.
6. **Ask a model only when your reading and history still leave doubt.** Prefer a targeted
   question: `pnpm seed ask <parish> <hash> --model gemini-3-flash-preview "Page 2: when are
   Saturday confessions at St. Mary's?"`. A full extraction (`pnpm seed extract <parish>
   <hash> --model gpt-6.1-sol`) is for a bulletin you can't make sense of. Both are cached
   and recorded in the file's `calls` (cite them by id in a slot's sources), and both refuse
   after 4 paid calls per parish (`CARLO_SEED_CALL_LIMIT`). Run a parish's calls one at a time,
   not in parallel: each records itself in the file. A clear parish needs no call.
7. **Decide each slot** and mark it:
   - `settled`: printed clearly, the policy is clear about it, and nothing you read
     contradicts it. `decision` is `include`, or `exclude` for something you leave out on
     purpose (keep its entry and say why; a chapel elsewhere may keep its own church slug).
     Something left out with no time to record (a chapel open only by arrangement,
     confession by appointment) gets `"entry": null`: never invent a time to fill it.
   - `needs_human`: the bulletins contradict each other and don't settle it; the policy
     leaves it a judgment call; the print is unreadable; or which listed church it belongs
     to is unclear. Write a short `question`, the `options` you are choosing between (an
     option's `entry` is null for "leave it out"), mark exactly one `"leaning": true`, and
     say why in the rationale.

   A question costs a reviewer time on every parish, so ask only what a person must
   decide. **Settle these by rule** (say which rule in the rationale):
   - **A time the policy works out.** "After the 11:30 AM Mass" on a weekday starts at
     12:00; after a weekend Mass, an hour after it starts; "an hour before each Mass" runs
     from an hour before to the Mass's start; Confession during Adoration has the
     Adoration's hours and the note `During Adoration`. History reading 11:30 or 12:15
     instead is not a conflict: `seed diff` lists it as a different reading of your slot,
     and `finalize` cites it there.
   - **History disagreeing with the bulletins.** History came from an older prompt. When
     your reading of the bulletins and the policy is clear, settle it and say what history
     got wrong. A history event that reads your slot at another time needs no slot of its
     own; any other history event you leave out still gets an excluded slot (step 9).
   - **What the policy leaves out**: a chapel or church elsewhere or whose place is
     unclear, another parish's church, a devotion that is not Mass, Confession or
     Adoration (a Rosary, Anointing of the Sick), a wedding, funeral or memorial Mass for
     one person, an event with no definite time. Settle it `exclude`. A church or chapel
     with times of its own that `data/churches.csv` lacks also goes in the file's
     `church_list_issues` (see the seed file reference), once, not as a question.
   - **A cancellation the bulletin doesn't state.** A holiday listing that shows a 9:00 AM
     Mass and not the usual 6:45 does not cancel the 6:45: record the dated 9:00 AM Mass
     and leave the weekly slot alone. Record a cancellation only when the bulletin says a
     Mass is cancelled, moved, or replaced by a Communion Service.
   - **A weekly slot the newest bulletin skips for a reason it gives.** "No Mass Monday,
     Columbus Day" or a retreat day confirms the weekly slot: include it with the newest
     bulletin's page for that line, citing the line and the older bulletins that print the
     slot, with the dated cancellation when the date is on or after `as_of`.
   - **What the newest bulletin can't show** (the seed file reference has the check's
     terms): a slot the bulletin names by its week of the month ("First Friday Adoration",
     "First Saturday Mass") when the newest bulletin's week holds none of those weeks, and
     a dated event on or after `as_of` an older bulletin announced (an All Souls Mass on
     November 2). Include them settled with `page: null`, citing the older bulletin. A time
     printed only as a dated item that happens to fall on a first Friday, with no "First
     Friday" in the bulletin, is dated: left out once its date has passed.
   - **A change announced for later** ("from November 1, the Friday Mass moves to
     Tuesday"): keep the current schedule, leave the future one out, and say so. Update
     mode reads the bulletins that show the change.
   - **A schedule the file can't express whose dates the bulletin prints** ("every other
     Tuesday", with the next ones dated): record the dated occurrences on or after
     `as_of`.

   Ask (`needs_human`, leaning as you judge) for:
   - **Anything else you would flag to the reviewer.** The reviewer works in the labeler
     and never sees your report: a doubt that is only in your report is lost, and the slot
     is approved as settled.
   - **Any other slot the newest bulletin doesn't print**, backed only by the website or
     older bulletins (a weekly Mass missing with no reason given).
   - **A schedule the file can't express with no dates printed**, such as "every other
     Wednesday": offer weekly with a note saying so, and leaving it out. Don't invent a
     field for it.

   One answer, one question: when the same decision covers several slots (seven days of a
   chapel, a confession window before every Mass), give them one `group` (see the seed
   file reference).
8. Write the `summary`: two or three sentences a reviewer reads first.
9. `pnpm seed finalize <parish>` does the bookkeeping, then checks the file: it fills in
   every key a slot or entry leaves at its default, splits a source citing `bulletins` into
   one per bulletin, adds a `history` source for each matching event of recent history (so
   you need not write those), preserves explicit read marks and also marks the bulletins
   your `agent` sources cite, sets
   `as_of` to the newest one's `fetched_at` and `status` to `needs_review` if a question is
   open, else `ready`. Fix the reported problems and run it again until it says OK.
   Record each omitted
   history event in its own included, excluded or questioned slot; a rationale naming
   other events does not cover them in `diff`. If a problem cannot be resolved, preserve
   the evidence, mark the parish blocked with its reason, and report it. Warnings (`!`)
   are omissions from history; address them even when the command says OK. Update mode
   recovers omissions poorly. `pnpm seed diff <parish>` lists the same warnings, history
   events that read one of your slots at another time (check your time; no slot needed),
   and included slots history never had.

A parish that can't be seeded now (no usable bulletin, no schedule in its bulletins, a church
missing from `data/churches.csv`) gets `"status": "blocked"` with `blocked_reason`, and you
move on (`finalize` leaves a blocked status alone).

End with one line per parish: slug, status, open questions and any unresolved validation
problems. Put reviewer doubts in the seed's questions, where the labeler can show them.
