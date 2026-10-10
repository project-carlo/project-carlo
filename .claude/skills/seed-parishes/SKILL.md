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
read keys). Output is compact text; add `--json` for the full result.

## If you are the orchestrator

1. `pnpm seed pick [--limit N] [--diocese D]`: parishes with no seed and no seed file,
   easiest first (one church, a recent bulletin, extract mode stable week to week).
2. Split them among subagents, **3 to 8 parishes each** (your choice per batch). Give each
   subagent this skill's path, its parish list, and the test run's `--eval RUN` if there is
   one. Tell it to write each parish's file before starting the next.
3. When they finish: `pnpm seed check --all` and `pnpm seed status`. Report the parishes by
   status with their open questions.
4. **Never edit a subagent's decisions.** A file that looks wrong is re-drafted by a
   subagent (delete it and hand the parish out again), or left to the reviewer.

## If you are a subagent: one parish at a time

Finish and write each parish's file before starting the next, so an interrupted run loses at
most the parish it was on.

1. `pnpm seed init <parish>`: writes `data/seeds/<parish>.json`, a `drafting` file listing
   the parish's bulletins. Fill it in as you go.
2. `pnpm seed bulletins <parish>`: bulletins newest first, with issue date, page count, and
   whether extract mode flagged one as a wrong bulletin or it repeats another PDF.
3. **Read the newest bulletin in full**: `pnpm seed pdf <parish> latest` writes the stored PDF
   (the pages the pipeline reads, so page numbers match) and prints its path; read that file.
   For a page that is only an image or a dense table, `pnpm seed pages <parish> <hash>
   --page N [--dpi 200]` renders a PNG to look at. Draft every Mass, Confession and Adoration
   slot the policy asks for, with its page. Write down what you leave out on purpose too
   (a Communion Service, a chapel at another address, a school Mass): those are the calls a
   reviewer wants to see.
4. `pnpm seed history <parish> [--bulletins N]`: what extract mode stored for recent
   bulletins. Free. It came from an older prompt, so a difference is a reason to look closer,
   not a vote.
5. **Read further back, one bulletin at a time,** when a question needs it:
   - a slot printed in only one bulletin (weekly, or a one-off?)
   - a time or day that differs from history or between bulletins
   - a seasonal hint ("summer schedule", "beginning in Advent")
   - a newest bulletin that looks like an old issue, or another parish's
   Mark every bulletin you read `"read": true`.
6. **Ask a model only when your reading and history still leave doubt.** Prefer a targeted
   question: `pnpm seed ask <parish> <hash> --model gemini-3-flash-preview "Page 2: when are
   Saturday confessions at St. Mary's?"`. A full extraction (`pnpm seed extract <parish>
   <hash> --model gpt-6.1-sol`) is for a bulletin you can't make sense of. Both are cached
   and recorded in the file's `calls` (cite them by id in a slot's sources), and both refuse
   after 4 paid calls per parish (`CARLO_SEED_CALL_LIMIT`). A clear parish needs no call.
7. **Decide each slot** and mark it:
   - `settled`: printed clearly, the policy is clear about it, and nothing you read
     contradicts it. `decision` is `include`, or `exclude` for something you leave out on
     purpose (keep its entry and say why).
   - `needs_human`: the sources conflict and the bulletins don't settle it; the policy leaves
     it a judgment call; the print is unreadable; or which church or chapel it belongs to is
     unclear. Write a short `question`, the `options` you are choosing between (an option's
     `entry` is null for "leave it out"), mark exactly one `"leaning": true`, and say why in
     the rationale.
8. Fill in the parish: `as_of` is the newest bulletin you read's `fetched_at` (as the file
   lists it), `summary` is two or three sentences a reviewer reads first, and `status` is
   `needs_review` if any question is open, else `ready`.
9. `pnpm seed check <parish>` and fix everything it reports.

A parish that can't be seeded now (no usable bulletin, no schedule in its bulletins, a church
missing from `data/churches.csv`) gets `"status": "blocked"` with `blocked_reason`, and you
move on.

## The file, slot by slot

```json
{
  "id": "s1",
  "decision": "include",
  "status": "settled",
  "entry": {"church_slug": "st-marys-oswego", "event_type": "mass", "event_kind": "weekly",
            "day_of_week": "Saturday", "date": null, "start_time": "16:00", "end_time": null,
            "cancelled": false, "weeks_of_month": [], "season": null, "note": "Vigil"},
  "page": 2,
  "sources": [
    {"source": "agent", "bulletin": "9f2c41d0", "page": 2, "said": "Sat 4:00 PM Vigil"},
    {"source": "history", "bulletin": "1ab3e7c2", "said": "weekly Saturday 16:00"}
  ],
  "rationale": "Printed in the Mass schedule box of both bulletins read; history agrees.",
  "question": null, "options": null, "answer": null
}
```

- `entry` is a label event without `page_number`, `origin` and `optional`: every key present,
  times 24-hour `HH:MM`, `weeks_of_month` and `season` only on weekly entries, `cancelled`
  only on dated ones.
- `page` is where the **newest** bulletin prints the slot (null when it doesn't). It becomes
  the entry's sighting when the seed is loaded.
- `sources[].source` is `agent` (your reading), `history`, or a call's id. `bulletin` is a
  hash or a prefix of at least 8 characters. `said` is what that source says, in its words.
- A seed holds weekly slots, plus dated entries and cancellations **on or after `as_of`'s
  date** (next Saturday's vigil called off). Update mode never reads a bulletin fetched on or
  before `as_of`, so a cancellation left out here never reaches the site.
- One slot per day and time: "Mon–Fri 8:00 AM" is five slots.
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
