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
one-off events while retaining monthly services. Ambiguous interruptions now keep
the weekly slot and add cancellations only for dates established by the bulletin.
Only explicit discontinuation or an explicit ongoing replacement removes a weekly
service; repeated omissions and cancellations do not establish permanence.
Explicitly dependent Confession/Adoration is cancelled for the affected date too,
while independently scheduled services are preserved.

Context selection is automatic for every eligible update-mode parish, not a
handpicked parish exception. It includes settled exclusions, answered questions,
and monthly/seasonal slots, with their rationale, sources and reviewer answers.
On this run’s database, 45 of 50 seeded parishes have selected context. No new
handwritten parish context or draft summaries were injected.

## Real model replays

**All 15 targeted parish trials passed**, comprising **21 real API requests**.
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
| Corpus Christi Round Lake | 21 | Keep Thursday Mass and dependent Confession; cancel both Oct 22 occurrences | 3/3 |

None of the targeted erroneous proposals occurred, including at intermediate
steps of the two-bulletin trials. These repeated observations support the fix;
they do not guarantee deterministic model behavior on future bulletins.

An earlier prompt-only version protected the targeted slots but missed Webster's
Youth Mass in one of three trials. The final version adds reviewed context and
the separate dated-calendar pass; the Youth Mass was present in all final trials.
The earlier outcomes are retained in [prompt-only-summary.json](prompt-only-summary.json).

### Cancellation preference and earlier trials

The earlier prompt produced two recurring removals and one dated Mass cancellation
in three Corpus trials; the cancellation-only answer missed dependent Confession.
Those original outcomes remain in [the archived summary](before-cancellation-preference/summary.json)
and the three Corpus predictions beside it. The delegated investigation supported
the removals as one possible interpretation of the changed standing panel. The
follow-up policy decision is more conservative: preserve the weekly service until
there is explicit ongoing evidence, and accumulate dated cancellations instead.

An initial cancellation-preference run passed all three Corpus cases but restored
Corning’s excluded Mass in one trial. The prompt was clarified: an excluded entry
is a rejected candidate, not a venue fact; a generic venue statement plus repeated
intentions cannot establish a reviewed service’s public venue. Reversal requires
service-specific clarification and a rationale identifying the new evidence.
Those intermediate outcomes remain in [cancellation-preference-initial-summary.json](cancellation-preference-initial-summary.json).
The current predictions and summary were rerun with that clarification; all five
parishes passed three independent trials each.

Promotion of repeated cancellations is future work, tracked in
[GitHub issue #141](https://github.com/project-carlo/project-carlo/issues/141).
The issue covers thresholds, independent evidence, duplicate/corrected bulletins,
known bounded closures, resumption, qualifiers, dependencies and auditable retirement.
No promotion code is implemented in this change. The new prompt affects subsequent
model calls; the existing five-entry data repair below remains unchanged and does
not retrospectively restore Corpus’s deleted entries.

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
as the same lost-reviewed-exclusion issue and documents why Corpus's
removals were defensible before the cancellation preference was chosen. It gives source-backed context wording and distinguishes facts from
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
expectation. Earlier Corpus ambiguity is preserved in the archived results.

Validation: `uv run ruff check .`; `uv run pytest -q` — **1185 passed**.
