# Plan: a blind second opinion on every seed

Status: Phases 0–3 built (2026-11-18); the first small seed Run, reviewed with foreman, is
next. Phase 0's results and the prompt tuning are below and in
`data/runs/seed-opinion/eval/`. The decisions are recorded under "Decided" at the end, and
what the build settled under "Built" after them.

## Why

The drafter (Opus, `seed` stage) can ask for a second opinion today with `seed ask` or
`seed extract` (gpt-6.1-sol or gemini-3-flash-preview), limited to 4 paid calls per parish.
It never does: **0 of the 270 seed files in `data/seeds/` record a call.** R4 says model calls
are "a last resort" and "a clear parish needs no call", and the drafter takes that literally.
In practice, every seed gets one model's reading, checked by a reviewer from the same family.

The proposal: before the drafter submits, a model from another family reads the same
bulletins on its own and builds its own schedule, which the drafter doesn't see. When the
drafter submits, the dispatcher compares the two. The drafter must resolve every difference,
either by changing the seed or by showing from the bulletin why it is right. This happens on
every parish, so the drafter never has to choose to spend money.

Why gpt-6-luna:

- **Another model family.** Its mistakes should be mostly independent of Opus's, which is
  the point of a second reviewer.
- **It's the model that maintains the schedule.** Update mode (`schedule_update.UPDATE_MODEL`)
  runs on gpt-6-luna. Where luna reads a parish differently from the seed, update mode is
  likely to churn there later, so the comparison also flags trouble ahead.
- **It's cheap.** $0.10/M input tokens and $0.50/M output, half that on flex
  (`classifiers/pricing.py`). Measured in Phase 0: about $0.0025 a parish on flex, with
  the cached policy prefix, so well under $1 for a whole diocese.

## The flow

```
seed Run starts ─▶ dispatcher fires one blind luna call per parish (background, cached)
                     │
seed job (Opus) drafts as today ─▶ gates pass (`seed check`)
                     │
                     ▼
         reveal: write luna's schedule into the seed file, compare
           ├─ no differences ─▶ record agreement ─▶ commit, as today
           └─ differences ─▶ "opinion" prompt to the same session (not a send-back)
                               drafter changes slots, or keeps them with cited evidence
                               ─▶ gates again (every difference resolved) ─▶ commit
                     │
seed-review sees the seed, luna's schedule and every resolution, and checks each "kept"
                     │
pr: the summary lists differences per parish: changed / kept / asked
```

### 1. The blind call

A new task, `classifiers/seed_opinion.py`, modelled on `schedule_update.py` (Responses API,
strict schema, the stored raw reply, a request key) but taking several PDFs and no believed
schedule:

- **Prompt:** `POLICY` first and unchanged, so the prompt cache serves it as it does for the
  classifiers. Then a short seeding section, which says what a seed holds (weekly slots, plus
  dated entries and cancellations on or after the newest bulletin's date; R16) and how to
  read across bulletins (R35 recurrence across issues, R36 one omission, R12 a monthly
  service the newest issue's week can't show). Then the parish's churches, "today" (the
  newest bulletin's fetch date, as in `seed_ask._today`) and the PDFs, labelled B1…Bn
  newest first, each with its published date.
- **Kept out, so the reading stays independent:** extract-mode history, the website,
  diocese precedents, and the full `rules.md`. Luna reads only what the drafter's bulletins
  say.
- **Bulletins:** the newest 2–4 bulletins that have PDFs, one per issue week (no
  `duplicate_of`, and no repeat fetches of one issue). This is the set `seed start` lists
  first. `seed_ready_bulletins: 2` already guarantees at least two.
- **Output:** `entries[]` in the seed's entry shape (church_slug, event_type, day or date,
  start and end times, weeks_of_month, exclude_weeks, season, cancelled, note). Each entry
  has `evidence[]` (`bulletin` B-index, `page`, and `quote` exactly as printed), plus
  `church_list_needs_review` and a `wrong_bulletin` flag for each bulletin. The quotes
  matter most: they let the drafter check a claim against the PDF in seconds.
- **Settings:** update mode's: reasoning `high`, PDFs at low detail, flex first. If a bulletin set would go
  over `long_context_over` (272k tokens), drop the oldest bulletin rather than pay
  long-context prices.

### 2. Firing it, and keeping it hidden

- When a seed Run starts, the dispatcher sends calls for all of its parishes from a small
  thread pool, as `process_update_mode` does across parishes. It's one call per parish, and
  only the dispatcher makes these calls, so the drafter needs no model keys.
- The reply goes in a new ledger table, `seed_opinion` (run_id, parish, bulletins,
  request_key, model/version, status, reply, cost_usd, created_at, revealed_at). The
  request key covers the model, prompt version, bulletin hashes, churches and today, so a
  retry or a restarted dispatcher doesn't pay twice. The ledger lives in
  `~/carlo-factory/data/factory/`, outside the Run's checkout, and the reply isn't written
  to R2, which workers can read, until it's revealed.
- **How hidden it is:** the live factory runs workers in the sandbox
  (`worker_backend: sandbox`), which can't see the ledger. Even without the sandbox,
  nothing would point a worker to it, and a worker that went looking would show in review.
- If, at reveal, the drafter's newest read bulletin is newer than the opinion's (a
  `data:pull` arrived mid-Run), the dispatcher reruns the call on the drafter's set before
  comparing, waiting for the reply. If the call is still in flight at reveal, the
  dispatcher waits for it, up to a timeout. If luna can't be reached, the job goes ahead
  without an opinion and the PR says so. A seed is never blocked on luna.

### 3. Reveal and compare

This is a new step in `engine.py`, after `_stage_gates` passes for a `seed` job and before
`_finish`:

1. **Write the opinion into the seed file** as a top-level `second_opinion`: model,
   version, call id (also appended to `calls`, so a slot source can cite it as `c1`),
   bulletins, cost, luna's entries, and `differences[]`. Keep a hash of the entries in the
   ledger. A gate checks that the drafter hasn't edited luna's entries; the drafter writes
   only the resolutions.
2. **Compare** with `schedule_diff`'s fingerprints, not `seeding/coverage.py`'s matching.
   Coverage deliberately ignores weeks of the month, seasons and end times because
   history's are unreliable. Luna reads the PDFs, so those fields count, and
   `recurrence_mask` already treats "except the last Sunday" and "first to fourth Sunday"
   as the same thing. Kinds of difference:
   - `missing`: luna has an entry that no slot or option covers;
   - `excluded`: luna has an entry that the seed leaves out, or that a question leans
     against;
   - `extra`: the seed includes, as settled, an entry luna doesn't have;
   - `differs`: same church, type and day, but a different time, weeks, season or end
     time (one of each, as `schedule_diff` pairs them);
   - `question`: the seed asks, and luna's entry matches an option other than the
     leaning one.

   Group a difference that covers several days ("Mon–Fri 8:00 vs 8:30") into one item, the
   way a question group works. Notes aren't compared.
3. **When luna agrees,** add a `c1` source to each matching slot automatically ("gpt-6-luna
   read the same: B1 p2 'Sat 4:00 PM Vigil'"). The reviewer then sees which slots two
   families agree on.
4. **No differences:** mark it revealed and go on to `_finish`.
5. **Differences:** set `pending_prompt=pending("opinion", render.opinion_prompt(diffs))`
   and requeue the same session. This is its own kind of attempt and doesn't count against
   `max_send_backs`. A session that can't be resumed gets a fresh worker with the files,
   as a crash does.

### 4. What the drafter does with differences

For each difference, it re-reads the cited page and either:

- **changes the seed** (`slot edit`, `slot include`…). The next comparison no longer shows
  the difference, so it is resolved by the change, with nothing more to record;
- **asks:** turns it into a `needs_human` question with luna's reading as one of the
  options. This also resolves it automatically;
- **keeps its slot:** `pnpm seed opinion keep <parish> d3 --src "B1 p2: …" --why "R…"`. A
  kept difference must cite a bulletin page (the CLI's usual source syntax) and give a
  rule-based reason ("R17: the 9:00 is the Thanksgiving listing; the weekly 6:45 is in the
  schedule box of all three issues").

`seed opinion show <parish>` lists the differences and their state. It refuses to run until
the opinion has been revealed, since the file has nothing to show before then. `seed check`
gains a problem: "difference d3 unresolved". Every submission re-runs the comparison against
the stored opinion. That way, a slot changed after a seed-review send-back that creates a new
difference has to be resolved too, and resolutions whose difference is gone are dropped.

The opinion prompt tells the drafter to treat luna as a second reader, not as an authority.
Luna has no history, no website and no precedents, so it will often be wrong on exactly the
cases rules.md exists for (R6 website times, R23 unlisted chapels, R33 patterns the format
can't express). Those should be quick "keep" resolutions. The prompt also warns against the
opposite failure: changing a slot only because luna said so, without re-reading the page.

### 5. Seed-review and the PR

- **seed-review** gets one more duty: check every `kept` resolution against the cited page.
  A kept resolution that the page doesn't support is a send-back. A parish where both models
  agree on every slot can get a lighter review. This aims the reviewer's high effort at the
  disputed slots.
- **The PR summary** gets a per-Run table (parishes, differences, changed, asked, kept,
  cost), then the kept differences listed one by one. Those are where two models disagreed
  and the drafter overruled luna: the decisions most worth the owner's eyes.
- **Foreman** gets the difference counts and the share kept versus changed, per job and
  per stage, to track noise over time.

### 6. What goes away

- `seed ask` and `seed extract` leave the skill, R4 is rewritten ("the dispatcher's
  second opinion; model calls are not yours to make"), and `GEMINI_API_KEY` and
  `OPENAI_API_KEY` leave `seed.yaml`'s secrets. That's a security gain too: seed workers
  no longer hold API keys.
- `CARLO_SEED_CALL_LIMIT` and the paid-call counter go with them, unless the commands are
  kept for interactive use (question 2).

## Phases

**Phase 0: measure on the 270 approved seeds (do this first).** A script runs the blind call
on every approved seed's bulletin set, using the bulletins each seed cites, with "today" at
its `as_of`. It compares the result with the approved slots and reports differences per
parish. Then classify a sample by hand, or with a Claude pass checked by you: luna right (a
real seed error), seed right (luna noise), or ambiguous. This settles whether the idea pays:

- the cost per parish, for real;
- how much noise the drafter will face: a few differences per parish is fine, twenty is a
  tax that teaches the drafter to wave them through;
- how many real errors are sitting in approved seeds. Those errors are fixed by a repair
  Run, which is a win on its own;
- prompt fixes, made before any drafter sees a difference.

Suggested go/no-go: a median of 3 or fewer differences per parish, and at least one in five
differences pointing at a real seed error or a question worth asking.

**Phase 0 results (2026-11-16),** in `data/runs/seed-opinion/eval/phase0-2026-11-16/`
(`analysis.md`):

- 258 seeds compared for about $0.84 in all. Counting website-backed slots and R22–R26
  exclusions as resolved, there were 244 differences: a median of 0 a parish, 60% of
  parishes with none, 92% with 3 or fewer. The noise threshold is met.
- In a sample of 24, the seed was right on 14, luna on 1, 5 were judgment calls and 4 were
  structural. That is 25% worth a look, but only one real error: an event time printed
  only in an image.
- Luna's typical mistakes are R33 patterns written as weekly, missed lines in schedule
  boxes, misread small print and ignored same-bulletin exceptions. Prompt work in Phase 1
  should target those.
- Phase 1 must also fix six comparison artefacts listed in `analysis.md` (24-hour
  encodings, unpaired end-time differences, and others), and treat website-backed slots as
  resolved.

**Phase 1: task and CLI.** `classifiers/seed_opinion.py`, request keys and stored replies,
the `second_opinion` file section and its validation, the comparison (built on
`schedule_diff`), `seed opinion show/keep`, the new `seed check` problems, and tests with
recorded replies.

**Phase 2: dispatcher.** The `seed_opinion` ledger table, firing calls at Run start, the
reveal step and the `opinion` attempt kind in `engine.py`, `render.opinion_prompt`, rerun on
a changed bulletin set, and the timeout and no-luna fallback.

**Phase 3: stage spec.** Skill and rules changes (R4, the opinion step in SKILL.md), drop
`ask`/`extract` and the model keys from `seed.yaml`, seed-review's new duty, the PR summary
table, and foreman metrics. Then run a small seed Run and review it with foreman.

## Risks

- **Deferring to luna.** An agent shown another answer tends to adopt it. Requiring a
  re-read and a cited page for both "change" and "keep", plus the reviewer checking every
  keep, is the guard. Phase 0 and foreman show which way the drafter leans.
- **Noise wearing it down.** If luna is wrong often, the drafter learns to dismiss it.
  Phase 0's go/no-go and prompt tuning come first. Comparing at the fingerprint level and
  ignoring notes removes most false differences.
- **Multi-PDF quality is unmeasured.** The luna evals so far read one bulletin per call.
  Phase 0 is that eval.
- **Context per job.** The opinion prompt adds tokens to the drafter's session. Grouping
  differences and sending luna's quotes, not its whole schedule, keeps it small.

## Decided (2026-11-16)

1. A drafter-blocked parish (R34) still gets the comparison.
2. `seed ask`, `seed extract` and the call limit are deleted.
3. Hiding: the sandbox is enough, and so is review.
4. `excluded` differences count, but a settled exclusion that cites R22–R26 is resolved by
   its own rationale.
5. Phase 0: capped at $2 for all approved seeds. The count of differences matters more
   than who is right, so a sample is classified by Claude, not by the owner.
6. Luna's readings go no further for now: not to update mode, and not to the labeler.

## Built (2026-11-18)

- **The file** (`seeding/second_opinion.py`, validated in `files.py`; file-format.md, "The
  second opinion"): `second_opinion` holds the model, version, call id (also in `calls`,
  kind `opinion`), request key, today, the bulletins as B1…Bn, cost, luna's entries with
  their evidence and their hash, and `differences`, each with an id, its kind, the
  entries and slots it involves, both readings in words, and a `resolution`: `changed`,
  `asked`, `kept` (a bulletin page and a rule), `answered` (a reviewer answered its
  slot) or `auto` (website, R22–R26 exclusion, unseen bulletins).
- **Re-comparing** on every `seed check`, `finalize` and `seed opinion keep`. A
  difference keeps its id while its kind, entries, slots, fields and the seed's reading
  stay the same, so a kept one reopens as a new difference when its slot changes, and a
  vanished one becomes `changed` (or `asked`, if its slot became a question).
- **Checks.** `seed check` reports each open difference, and fails if the entries no
  longer hash to the file's `entries_sha256`, or to the dispatcher's, which it passes to
  the seed gate as `CARLO_SEED_OPINION_SHA256`. Approved seeds aren't held to it.
- **The dispatcher** (`factory/opinions.py`, the reveal step in `engine.py`): the
  `seed_opinion` ledger table; calls fired when a seed Run is active, on a thread pool,
  each reply stored under its request key and reused by any later request with the same
  key; a call cut off by a restart asked once more. At reveal the job waits in `gating`
  (gates not rerun) up to `opinion_timeout_minutes`; it asks again on the drafter's own
  bulletins when the request's newest bulletin isn't the drafter's newest read, and once
  when the Run's first request failed. The `opinion` attempt clears the gates action and
  requeues the session; `send_backs` is untouched. A Run whose checkout lacks
  `second_opinion.py` (started before this, not yet merged main) gets no opinion.
- **Hiding.** Replies live only in the ledger until revealed; the nightly R2 backup drops
  unrevealed replies and vacuums. Seed workers no longer hold model keys.
- **Removed:** `seed ask`, `seed extract`, `CARLO_SEED_CALL_LIMIT`, `classifiers/seed_ask.py`
  and `seeding/calls.py`. Older files' `ask`/`extract` calls stay valid.
- **Not done:** dropping the oldest bulletin to stay under `long_context_over` (the token
  count is only known after the call; v2's 258 calls used at most 129k input tokens, median
34k).

