# Believed schedules (update mode)

Every live parish keeps a **believed schedule**, changed only through recorded
changes: each new bulletin is shown to the model together with the schedule we
believe, the model proposes changes, and a code policy applies or rejects each
one. A parish goes live once its approved seed is loaded (see
[seeding-plan.md](seeding-plan.md)); until then its bulletins are fetched but
not processed or shown. (Parishes used to be extracted from scratch each week by
Gemini, "extract mode"; that path is gone.) The design is [schedule-state-plan.md](schedule-state-plan.md); this page describes
how update mode behaves now.

Update calls run on `gpt-6-luna` (OpenAI Responses API, high reasoning, the PDF
at low detail, strict decoding), set up like the eval module's `gpt-6-luna`
classifier, and need `OPENAI_API_KEY`. Their prompt
(`classifiers/schedule_update.py`) carries every rule of the eval policy
(`classifiers/schedule_policy.py`), worded for changes to the believed
schedule.

The update view also carries `reviewed_seed_context` from the parish's latest
imported, approved seed: excluded slots, answered questions, and monthly or
seasonal entries with their evidence. These explain intentional omissions and
unusual services; ordinary included slots are already in the live schedule.
The updater honors the resolved decision until new evidence addresses its
reason, and does not treat routine panel omissions as discontinuing a monthly
service. Draft summaries are left out. Context is stored and hashed with the
view, so editing a reviewed rationale changes the request/cache key without
re-seeding or replacing the current schedule.

Announced weekly changes are retained immediately with inclusive absolute
`valid_from` / `valid_until` dates. The old entry ends the day before the new
entry starts. These bounds apply to times, weekdays and location notes, and
do not repeat annually like a season. The snapshot and website honor them
without another bulletin or pipeline run. Snapshot format 3 carries the bounds.
A weekly entry whose end date has passed is deleted at the start of the
parish's next revision.

When a cancellation's duration is unclear, update mode keeps the weekly slot
and cancels only the dated occurrences the bulletin establishes. Repeated
omissions or cancellations do not establish permanent discontinuation on their
own. An explicit ongoing change can still replace or remove a weekly slot.
History-based promotion of repeated cancellations is tracked in
[issue #141](https://github.com/project-carlo/project-carlo/issues/141).

The [October 18 replay report](../data/update-evals/2026-10-18/report.md) records
the source cases, real model reruns, remaining ambiguity, and the guarded data
repair in migration 0008. Replays can be repeated with
`uv run python scripts/replay-schedule-updates.py --help`.
The [October 25 audit](../data/update-evals/2026-10-25/verification.md) records
the source evidence behind the guarded repairs in migration 0012.

Those two repairs, and the ones in migrations 0010 and 0013, stay as they
shipped. New corrections are correction files (below), not migrations.

`pnpm schedule` looks at and hand-edits believed schedules:

```bash
pnpm schedule show --parish st-mary-albany          # the schedule as the model sees it
pnpm schedule apply --call 123 --actor you --note "checked the bulletin"   # a rejected call's proposals
pnpm schedule modify --parish st-mary-albany --entry-id 118 --entry '{...}' --actor you
pnpm schedule seed --parish st-mary-albany --file entries.json --actor you
```

These change only your local database, which is never published.

## Corrections

A correction to a live schedule reaches the published database as a committed
file, reviewed in a pull request:

```
data/corrections/<parish-slug>/<YYYY-MM-DD>-<short-name>.json
```

Write one with the edit command and `--write-correction NAME` (a `--note` is
required). The command writes the file, with every entry, call and bulletin
named by its content rather than by database ids, and loads it into your local
database, so `pnpm schedule show` shows the result. If it doesn't load there,
no file is written. Commit the file.

```bash
pnpm schedule modify --parish st-mary-albany --entry-id 118 --entry '{...}' \
  --actor you --note "p. 2 moved the 11:00 Mass to 11:30" --write-correction late-mass
pnpm schedule apply --call 123 --seq 2 --actor you --note "the Mass is still printed" \
  --write-correction keep-first-friday
pnpm schedule wrong-bulletin --parish st-mary-albany --content-hash 1afe... \
  --actor you --note "a flyer, not a bulletin" --write-correction flyer
pnpm schedule corrections      # load any not loaded yet; list the ones skipped and why
```

A file names the parish, the actor, a note, `as_of` (the schedule it was made
against: when the parish's newest revision was written) and its operations:

| `op` | Fields | What it does |
|---|---|---|
| `add` | `after` | adds an entry |
| `modify` | `before`, `after` | replaces an entry |
| `delete` | `before` | deletes an entry |
| `apply` | `run_id`, `content_hash`, optional `seq` | applies the rejected proposals of the run's call for that bulletin |
| `wrong_bulletin` | `content_hash` | marks the parish's bulletin as not its own |

Entries are in the labels' form, as `--entry` takes them. A `wrong_bulletin`
mark changes which bulletin ranks as the parish's; it doesn't undo what the
call for it applied, which takes schedule operations in the same file.

**Loading.** Every pipeline command loads the files not loaded yet, after the
seeds (`schedule/corrections.py`). A file is one `human` revision whose note
carries a digest of its parish, `as_of` and operations, so loading it again
does nothing, and rewording its note doesn't load it again. A file of only
`wrong_bulletin` marks makes an empty revision, so it is recorded the same way.

**Guards.** A file applies whole or not at all. Its schedule operations are
checked in order with the hand edits' checks, and it is skipped, not forced,
when a `before` is no longer in the schedule, an operation fails a check (a
`duplicate`, say), a revision written after `as_of` changed one of its slots
(for `apply`, any revision after the call), or the call, proposal or bulletin
it names isn't in the database. A skipped file is tried again by every command,
and reported, until it loads or is removed.

**Going live.** A deploy builds the site's snapshot from the published database
with the files loaded, so a correction is on the site once its pull request
merges, as a migration's repair was. The deploy doesn't publish that database:
the next weekly run loads the files into the published one, after its
before-copy, so its checks see them, and its report lists each correction
applied and each skipped, with the reason. Both loads start from the same
published database, so they make the same revision; a file the database
already has a revision for is never loaded again.

A skipped correction doesn't fail CI. It shows in the preview deploy's data
snapshot summary (`seeded.corrections.skipped`) and in every weekly report,
and CI checks each committed file's shape, parish and churches.
