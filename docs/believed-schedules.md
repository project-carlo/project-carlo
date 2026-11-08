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

`pnpm schedule` looks at and hand-edits believed schedules:

```bash
pnpm schedule show --parish st-mary-albany          # the schedule as the model sees it
pnpm schedule apply --call 123 --actor you --note "checked the bulletin"   # a rejected call's proposals
pnpm schedule modify --parish st-mary-albany --entry-id 118 --entry '{...}' --actor you
pnpm schedule seed --parish st-mary-albany --file entries.json --actor you
```
