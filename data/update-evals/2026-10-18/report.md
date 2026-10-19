# October 18 weekly-update prompt regression and repair

The [published run](https://github.com/project-carlo/project-carlo/actions/runs/39127931592)
(`20261018T123547Z-gh39127931592`) reversed reviewed exclusions and deleted
monthly services from silence in generic schedule panels.

The fix supplies resolved seed decisions, their evidence and reviewer answers
alongside the live schedule. It excludes stale draft summaries and ordinary
included entries. Only the latest imported, approved seed supplies context;
a changed, unimported schedule or a newer manual seed cannot inject old notes.
Context is included in the stored view and its hash, so editing a rationale
changes request identity without re-seeding. Historical context does not
replace the current schedule or prevent explicit new evidence from changing it.

Prompt rules now require evidence addressing an occasional service before
deleting it, honor intentional exclusions, and cross-check generic panels
against explicit venue notices. A separate dated-calendar pass preserves new
one-off events while retaining monthly services.

## Real model replays

**All 12 targeted parish trials passed**, comprising **18 real API requests**.
Each parish was replayed three times independently, starting from the historical
schedule shown to its first call and applying new answers in bulletin order.
The same stored PDFs, original fetch dates and production model/settings were
used: `gpt-6-luna`, high reasoning, low PDF detail, strict schema. Replays used
the standard service tier instead of production's flex routing. No source
run database or remote data was changed.

| Parish | Original calls | Expected result | Trials |
| --- | --- | --- | --- |
| Holy Trinity Webster | 20, 29 | Keep First Saturday 6:30 PM Spanish Mass; still add Oct 25 6:30 PM Youth Mass | 3/3 |
| Mary, Mother of Our Savior | 34, 39 | Keep First Saturday 8:15 AM Mass and 8:45 AM Confession through both bulletins | 3/3 |
| St. Edward the Confessor | 81 | Do not restore Friday 9 AM Mass at the wrong church | 3/3 |
| All Saints Corning | 19 | Honor reviewed Saturday 4 PM exclusion; still add Oct 22 8:30 AM Mass | 3/3 |

None of the targeted erroneous proposals occurred, including at intermediate
steps of the two-bulletin trials. These repeated observations support the fix;
they do not guarantee deterministic model behavior on future bulletins.

An earlier prompt-only version protected the targeted slots but missed Webster's
Youth Mass in one of three trials. The final version adds reviewed context and
the separate dated-calendar pass; the Youth Mass was present in all final trials.
The earlier outcomes are retained in [prompt-only-summary.json](prompt-only-summary.json).

### Exploratory Corpus Christi control: a remaining ambiguity

Three additional real calls replayed Corpus Christi #21. Two removed the Thursday
weekly Mass/Confession, matching the original run. One kept the weekly entries
and instead cancelled October 22 Mass; it did not cancel the dependent Confession.
Thus the strict exploratory deletion expectation passed **2/3**, and
`all_expectations_passed` is false in the summary. Corpus is explicitly marked
non-gating in the spec because the user's targeted regressions concern the other
four parishes; this variation is retained for the next policy decision.

The delegated investigation found the Corpus deletions defensible: the standing
weekday panel actually changed in consecutive issues. This differs from the
First Saturday cases, whose routine panels already omitted the monthly services
when those services were established. The current repair leaves Corpus unchanged.
The redundant cancellation and treatment of dependent Confession when a Mass
is cancelled remain follow-up work.

## Correcting the published run's errors

Migration `0008_repair_reviewed_weekly_slots.sql` appends four `human` revisions
with five inverse changes:

- Remove All Saints Corning Saturday 4 PM Mass (entry 487 in this run).
- Remove St. Edward's Friday 9 AM Mass (entry 505).
- Restore Holy Trinity Webster First Saturday 6:30 PM Spanish Mass (entry 155).
- Restore Mary Mother's First Saturday 8:15 AM Mass and 8:45 AM Confession
  (entries 195 and 190).

The migration matches the exact source run and slot contents rather than fixed
entry IDs. It reverses a proposal only while the current schedule still reflects
it and no later change touched that identity. Existing corrections and subsequent
human/LLM decisions are preserved, as are all original calls and proposal decisions.
This is a correction to the reviewed decision, not a claim that the unresolved
Corning 4 PM service does not exist.

On a local copy of the published run the migration made exactly these five
changes; a full log replay matched `current_schedule` with zero differences.
A second migration pass made no changes. Tests also cover later human edits that
return to the same entry contents, and an unrelated subsequent schedule change.

The patch takes effect when the new code migrates the database: deploy snapshots
apply migrations, and the next weekly run persists the repaired history in its
published database. This PR does not mutate the immutable October 18 run or
publish directly from a local machine.

## Delegated investigation

[The subagent's full report](other-weekly-changes-review.md) identifies Corning
as the same lost-reviewed-exclusion issue and recommends retaining Corpus's
changes. It gives source-backed context wording and distinguishes facts from
hypotheses. Existing resolved seed decisions provide immediate context; a
separately maintained parish context field remains a useful future option for
knowledge that evolves after seeding. No new parish database field is required
for this fix.

## Reproduction and validation

Pull this specific run's database into a separate path, then:

```sh
uv run python scripts/replay-schedule-updates.py \
  --db /path/to/october-18-run.db \
  --spec data/update-evals/2026-10-18/spec.json \
  --out data/out/update-replay --trials 3
```

The command makes paid model calls and writes only local replay results.
[Source call metadata](source-calls.json) records original PDF hashes and
call dates. [Predictions](predictions/) retain each answer's changes, sightings,
usage and request-context hash. [Summary](summary.json) keeps every targeted and
exploratory expectation, including the Corpus discrepancy.

Validation: `uv run ruff check .`; `uv run pytest -q` — **1185 passed**.
