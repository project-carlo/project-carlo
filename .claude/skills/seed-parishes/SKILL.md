---
name: seed-parishes
description: Draft believed-schedule seeds for parishes with the `pnpm seed` CLI, as an orchestrator handing parishes to subagents or as a subagent drafting them. Covers reading each parish's bulletins against the extraction policy, comparing with extract mode's history, asking an external model only when in doubt, writing data/seeds/<parish>.json with every slot's sources, decision and rationale, leaving questions for a reviewer, and test runs on the labeled parishes. Use when asked to seed parishes, draft or fix a seed, or run or score a seeding test run.
---

# Seeding parishes

A parish moves from extract mode to update mode when its first seed is loaded: from then on
the weekly run only proposes changes to the schedule the seed set. A wrong slot stays until a
bulletin makes the model change it, and a missed one is only added when a bulletin makes the
model notice it. So the seed has to be right. The design is `docs/seeding-plan.md`; read its
"The seed file" section before your first draft.

**The policy is `src/pdf_extract/classifiers/schedule_policy.py` (`POLICY`). Read it in full
before drafting.** It decides what counts: chapels, adoration chapels, Communion Services,
Benediction, Masses closed to the public, weekly vs dated, weeks of the month, seasons, which
times to give. This page does not restate it.

Every command reads the local database (`pnpm data:pull` first) and the blob store (the R2
read keys). Output is compact text; add `--json` for the full result. Run them as plain
`pnpm seed ...`: this pnpm rejects `-s`.

## If you are the orchestrator

1. `pnpm seed pick [--limit N] [--diocese D]`: parishes with no seed and no seed file,
   easiest first (one church, a recent bulletin, extract mode stable week to week).
2. Split them among `seed-drafter` subagents (`.claude/agents/seed-drafter.md`: this skill
   preloaded, Sonnet 5.5, no subagents of its own), **3 parishes each** unless asked
   otherwise, fewer when a parish has several churches. Every page a subagent reads stays in
   its context and is paid for again on each later request, so its third parish already
   costs about twice its first. Give each its parish list, the test run's `--eval RUN` if
   there is one, and **its own scratch folder** (`<scratchpad>/seed-a/`, `seed-b/`, ...):
   subagents share one scratchpad, and two writing the same file name overwrite each other's
   work. **Create each folder before spawning its subagent** (`mkdir -p`): a subagent's
   first write into a folder that isn't there fails. Tell it to write each parish's file
   before starting the next, and that WebFetch may be a deferred tool it has to load
   (ToolSearch) before its first use; `seed init` prints each parish's website. Override
   its model only to compare models on a test run.
3. When they finish: `pnpm seed check --all` and `pnpm seed status`. For a file that fails,
   run `pnpm seed finalize <parish>...` rather than fixing it by hand: it does only the
   bookkeeping (defaulted keys, sources split per bulletin, history sources, bulletins read,
   `as_of`, status) and changes no decision. What it still reports is a drafting problem:
   hand that parish back to a subagent (step 4).
   Report the parishes by status with their open questions.
4. **Never edit a subagent's decisions.** A file that looks wrong is re-drafted by a
   subagent (delete it and hand the parish out again), or left to the reviewer.

## If you are a subagent: one parish at a time

Finish and write each parish's file before starting the next, so an interrupted run loses at
most the parish it was on.

1. `pnpm seed init <parish>`: writes `data/seeds/<parish>.json`, a `drafting` file listing
   the parish's bulletins, and prints what you start from: the parish's website, its
   churches with their addresses, its bulletins newest first (issue date, page count,
   whether extract mode flagged one as a wrong bulletin or it repeats another PDF), a
   summary of extract mode's recent history, and the newest PDF's path. `pnpm seed brief
   <parish>` prints it again. Older bulletins often say `no PDF (history only)`: the PDF was
   pruned, so you can cite its history but not read it. Fill the file in as you go,
   editing the JSON directly (see [the file](#the-file-slot-by-slot)); you need no script
   to build it. If you do write a helper, keep it in the scratch folder the orchestrator
   gave you, never the shared one.
2. **Read the newest bulletin in full**: the PDF `init` wrote (`pnpm seed pdf <parish>
   <hash>` writes any other; page numbers match the pipeline's). For a page that is only an
   image or a dense table, `pnpm seed pages <parish> <hash> --page N [--dpi 200]` renders a
   PNG to look at. Draft every Mass, Confession and Adoration slot the policy asks for,
   with its page. Write down what you leave out on purpose too (a Communion Service, a
   chapel at another address, a school Mass): those are the calls a reviewer wants to see.
3. **Compare with history.** `init`'s summary shows each recent history event and how many
   bulletins it is in; `pnpm seed history <parish> [--bulletins N]` gives one table per
   bulletin. Free. It came from an older prompt, so a difference is a reason to look
   closer, not a vote.
4. **Read further back** when a question needs it. `pnpm seed grep <parish> [pattern]`
   searches the text of every stored bulletin at once, newest first (with no pattern, for
   schedule words): use it to see which bulletins print a slot before reading any. Then
   read one bulletin at a time by its text: `pnpm seed text <parish> <hash> [--page N]`
   costs a tenth of the PDF. Read a page as an image (`seed pages --page N`) only when
   `seed text` or `seed grep` says it is only an image, or its layout matters (a schedule
   grid whose text comes out scrambled). Look further back for:
   - a slot printed in only one bulletin (weekly, or a one-off?)
   - a time or day that differs from history or between bulletins
   - a seasonal hint ("summer schedule", "beginning in Advent")
   - a newest bulletin that looks like an old issue, or another parish's

   Cite every bulletin you read in an `agent` source; `finalize` marks those read. Before
   calling a weeks-of-the-month slot (First Friday Holy Hour) "seen once", check whether the
   other bulletins' calendars even cover a week it falls in. For a church or chapel the
   bulletin names, `pnpm seed church <name, town or street>` says whether it is in
   `data/churches.csv` and whose it is.
5. **The parish website is an extra source, not a step.** Look at it (WebFetch, at the
   address `init` printed; load the tool first if it is deferred) only when a question
   needs it: the bulletins and history disagree, or a slot's location or regularity is
   unclear. Cite what it says as `{"source": "website", "url": "<the page read>", "said":
   "..."}`. Websites go stale: one can back a reading up or raise a question, but it doesn't
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
   - `needs_human`: the sources conflict and the bulletins don't settle it; the policy leaves
     it a judgment call; the print is unreadable; or which church or chapel it belongs to is
     unclear. Write a short `question`, the `options` you are choosing between (an option's
     `entry` is null for "leave it out"), mark exactly one `"leaning": true`, and say why in
     the rationale.

   Three cases are always `needs_human`, leaning as you judge:
   - **Anything you would flag to the reviewer.** The reviewer works in the labeler and
     never sees your report: a doubt that is only in your report is lost, and the slot is
     approved as settled.
   - **A slot the newest bulletin doesn't print**, backed only by the website or older
     bulletins.
   - **A schedule the file can't express**, such as "every other Wednesday": offer weekly
     with a note saying so, the next dated occurrence (on or after `as_of`), and leaving it
     out. Don't invent a field for it.
8. Write the `summary`: two or three sentences a reviewer reads first.
9. `pnpm seed finalize <parish>` does the bookkeeping, then checks the file: it fills in
   every key a slot or entry leaves at its default, splits a source citing `bulletins` into
   one per bulletin, adds a `history` source for each matching event of recent history (so
   you need not write those), marks read the bulletins your `agent` sources cite, sets
   `as_of` to the newest one's `fetched_at` and `status` to `needs_review` if a question is
   open, else `ready`. Fix everything it reports and run it again until it says OK. It
   also warns (`!`) of each history event no slot or option covers: an omission is what
   update mode is worst at recovering from, so give each one a slot, included or left out
   with the reason. `pnpm seed diff <parish>` lists the same, plus the included slots
   history never had.

A parish that can't be seeded now (no usable bulletin, no schedule in its bulletins, a church
missing from `data/churches.csv`) gets `"status": "blocked"` with `blocked_reason`, and you
move on (`finalize` leaves a blocked status alone).

## The file, slot by slot

Write only what says something; `finalize` fills in the rest. A weekly slot, a seasonal
one, a dated cancellation, and an open question:

```json
"slots": [
  {
    "decision": "include", "status": "settled", "page": 2,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "mass",
              "day_of_week": "Saturday", "start_time": "16:00"},
    "sources": [
      {"source": "agent", "bulletins": ["9f2c41d0", "1ab3e7c2", "77d0be19"], "page": 2,
       "said": "Sat 4:00 PM Vigil"},
      {"source": "agent", "bulletin": "5e60aa31", "page": 3, "said": "Saturday 4 PM"}
    ],
    "rationale": "Printed in the Mass schedule box of all four bulletins read; history agrees."
  },
  {
    "decision": "include", "status": "settled", "page": 2,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "adoration",
              "day_of_week": "Thursday", "start_time": "09:00", "end_time": "19:00",
              "season": {"start_month": 9, "start_day": null, "end_month": 5, "end_day": null}},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "Thursdays 9 AM - 7 PM, September through May"}],
    "rationale": "The schedule box gives the months; the policy keeps them as the season."
  },
  {
    "decision": "include", "status": "settled", "page": 3,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "mass",
              "event_kind": "specific_date", "date": "2026-10-12", "start_time": "08:00",
              "cancelled": true, "note": "Columbus Day"},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 3,
                 "said": "No 8 AM Mass on Monday, October 12"}],
    "rationale": "The newest bulletin cancels one date of the weekly Monday Mass."
  },
  {
    "status": "needs_human", "page": 2,
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "First Friday Holy Hour 9:45 AM"}],
    "rationale": "Printed once, with no place given; no other bulletin's calendar covers a first Friday.",
    "question": "Add a first-Friday 9:45 AM Holy Hour at St. Mary's?",
    "options": [
      {"label": "First Fridays 9:45 AM", "leaning": true,
       "entry": {"church_slug": "st-marys-oswego", "event_type": "adoration",
                 "day_of_week": "Friday", "start_time": "09:45", "weeks_of_month": ["first"]}},
      {"label": "Leave out", "entry": null}
    ]
  }
]
```

- `entry` is a label event without `page_number`, `origin` and `optional`, times 24-hour
  `HH:MM`. `event_kind` is `weekly` or `specific_date` (never "dated"; `finalize` sets it from
  whether the entry has a `date`). A weekly entry has `day_of_week`, and may have
  `weeks_of_month` and `season`, and `exclude_weeks` true when the listed weeks are the
  ones it skips ("every Sunday except the last" is `["last"]` with `exclude_weeks` true;
  "except the first" is still the weeks that remain); a dated one has `date`, and
  `cancelled` true when the bulletin calls it off. `finalize` fills `church_slug` when the
  parish has one church.
- `season` has all four keys: months 1–12, and a day of the month or null when the
  bulletin gives only the month. September through May is `start_month` 9, `end_month` 5:
  a season may run across the new year. A half-stated season ("from October") is no season.
- `page` is where the **newest** bulletin prints the slot (null when it doesn't). It becomes
  the entry's sighting when the seed is loaded.
- `sources[].source` is `agent` (your reading), `history`, `website` (with its `url`), or a
  call's id. `bulletin` is a hash or a prefix of at least 8 characters. `said` is what that
  source says, in its words. When several bulletins print the same words, one `agent`
  source may list them as `bulletins`; `finalize` splits it into one source per bulletin.
  `finalize` adds the `history` sources that match; write one yourself only to say what it
  can't ("no weekday Masses stored").
- A seed holds weekly slots, plus dated entries and cancellations **on or after `as_of`'s
  date** (next Saturday's vigil called off). Update mode never reads a bulletin fetched on or
  before `as_of`, so a cancellation left out here never reaches the site.
- One slot per day and time: "Mon–Fri 8:00 AM" is five slots. An excluded slot may stand
  for a group left out for one reason (a sister parish's whole column): give one entry from
  it and list the rest in the rationale.
- Leave `reviewer`, `approved_at` and every `answer` null: the reviewer sets them.

## Test runs on the labeled parishes

Before seeding for real, and to compare batch sizes:

```bash
pnpm seed pick --labeled --eval RUN    # the labeled parishes; writes data/seed-evals/RUN/run.json
# every command then takes --eval RUN: drafts go to data/seed-evals/RUN/seeds/, never loaded,
# and each parish's bulletins newer than its labeled one are hidden.
pnpm seed score RUN                    # data/seed-evals/RUN/report.md
```

In a test run `as_of` is the labeled bulletin's fetch time. The score's headline is the
precision of your **settled** slots, since a reviewer may approve them without reading each
one: settle only what you would bet on.

## After you

A person opens the labeler's Seeds mode (`pnpm label`, then Seeds), answers the open
questions, and approves the parish. Approved files are committed, and every pipeline command
loads the approved seeds not yet in its database; the weekly run does so after taking its
before-copy, so a large batch can hold the run's change checks. Merge seeds in batches.
