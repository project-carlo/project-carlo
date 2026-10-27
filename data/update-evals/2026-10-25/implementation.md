# October 25 repairs and update safeguards

The [source audit](verification.md) distinguishes incorrect output from deferred
changes and faithfully copied unusual source times. This change implements the
verified repairs without rewriting model calls or replacing approved seeds.
No remote database or published snapshot was changed during implementation.

## Data repairs

Migration 0012 reads [repairs.json](repairs.json), matches the original weekly
run, parish and bulletin content hash, and appends eight human revisions:

- Vestal: remove the false October 31, 4 PM cancellation.
- Holy Spirit: end Friday Adoration at 8 PM, retaining the 7–8 PM closing Holy Hour note.
- Transfiguration: add October 28, 6:30 AM Mass and 6:10–6:25 AM Confession.
- St. Michael, South Glens Falls: add November 2, 7 PM Mass of Remembrance.
- Cicero: remove the disputed November 15, 2 AM First Penance pending confirmation,
  without inventing a 2 PM replacement.
- St. Stephen, Marathon: retain summer Mass/Confession through October 30 and
  winter Mass 4 PM / Confession 3–3:45 PM from October 31. Remove the now redundant
  October 31 dated exceptions atomically with each corresponding weekly transition.
- Lake George: retain Chapel notes through October 31 and clear them from
  November 1, preserving all service times. Do not infer a June return schedule.
- St. Bartholomew: retain Tuesday 9 AM through November 1; add Monday 9 AM from November 2.

St. Jerome's supported October 31, 3 AM service is unchanged. Transfiguration's
October 29/30, 6:30 AM Masses remain. The historical October 21 omission and
uncertain October 22/23 timetable discrepancies are not backfilled as future changes.
The other Norwich cluster churches are not assigned to St. Bartholomew. A
cross-parish read check found St. Malachy's Friday 9 AM and St. Paul's Wednesday
and Friday 9 AM slots; reconciling their own source bulletins remains separate
from these eight source-specific repairs. No St. Theresa venue was guessed.

Each repair requires the exact expected current content and skips slots touched
by any later decision, even a removal followed by restoration of identical
content. Missing additions likewise respect later additions/removals. Unrelated
edits survive. A repeated application is a no-op. On a private copy of the real
run, 29 log changes were appended across eight revisions; a repeat made zero
changes, foreign keys passed, and rebuilding all 170 believed schedules found
zero differing current rows. Database-specific entry/call IDs are not used to
select repair targets.

Python migrations use the same transaction, version bump and foreign-key checks
as SQL migrations. A failure rolls back the data and schema version together.

## Effective dates and source guidance

Migration 0011 adds inclusive absolute `valid_from` / `valid_until` dates to
weekly entries. Announced transitions end the old entry the day before the
change and add a replacement starting on the effective date. Unlike a season,
these dates do not repeat annually. The model sees future versions and their
bounds; expired versions disappear from its view but remain in the audit log.
Existing unbounded entries retain their hashes and identities.

Bounds participate in recurrence identity and overlap checks, cancellation
matching, snapshot export, browser occurrence calculation, map filtering,
schedule grouping and date descriptions. Thus a snapshot built before October
31 can show the winter schedule on November 7 without another bulletin or run.

The shared prompt distinguishes parallel sister-church services from relocation,
weekly-interpretation exclusions from dated-service exclusions, and a closing
Holy Hour from an ordinary embedded one. It explicitly avoids deriving services'
return from a building's reopening. Vestal's reviewed exclusion rationale also
explains its recurring mixed intentions list, with a link to the October 25 PDF.
The seed validates and its imported schedule digest is unchanged: this context
edit does not re-seed the parish.

Decision policy 2 holds newly proposed services before 5 AM as
`unusual_time_review`, exposed in the usual rejection report. It does not flip
AM/PM, block dated cancellations, or require another approval for unchanged
existing night services or date-bounded versions of an established weekly night
slot. Humans can use the existing `schedule apply` or `schedule add` commands
after verification. For Cicero's historical proposal, already applied before the
repair, use `schedule add` if subsequently confirmed; do not attempt to reapply
the historical applied proposal.

## Real model replays and limits

[spec.json](spec.json) reconstructs each original call's historical schedule.
Replays use the stored PDFs, original call dates, production model `gpt-6-luna`,
high reasoning and low PDF detail, with standard service tier for turnaround.
They run on in-memory copies; migrations and proposed changes never write the
source database. [predictions.json](predictions.json) records final responses,
decisions and token usage; [summary.json](summary.json) records the final policy
hash, classifier version and checks. [policy.txt](policy.txt) is the tested prompt.

All **16 targeted trials** passed: two independent calls each for Vestal, Holy
Spirit, Transfiguration, St. Stephen, Lake George, St. Bartholomew, Cicero and
St. Jerome. This includes retaining the supported morning/night services and
holding Cicero's printed time rather than guessing PM.

**South Glens Falls remains a recall limitation.** The Mass was absent in both
final trials. It is explicitly an exploratory control, not counted among the 16
targeted passes. The verified data repair adds the service independently. Two
additional high-PDF-detail trials also missed it, so production detail was not
changed. [high-detail-summary.json](high-detail-summary.json) records that negative
experiment. This PR does not claim to eliminate calendar recall misses generally.

The [initial summary](initial-summary.json) retains 14/18 passes before the
explicit reopening clarification: the two Lake George trials inferred June
returns, and the two calendar recall controls missed the Mass. The final Lake
George trials preserve open-ended main-church services and infer no June return.
These small replay samples support the targeted changes, not deterministic
guarantees on later bulletins.

Repeat the final cases with a database containing the original calls:

```sh
uv run python scripts/replay-schedule-updates.py --db data/audit-source.db \
  --spec data/update-evals/2026-10-25/spec.json \
  --out data/out/oct25-replay --trials 2
```

`--file-detail high` is available for controlled detail comparisons. Calls are
billable; they do not publish or modify the source database.

## Deployment and validation

Snapshot format **3** carries the bounds. The new web reader accepts formats 2
and 3, so it can deploy while the published data is still format 2. **Deploy the
new reader before publishing a format 3 snapshot.** Older readers reject format
3 instead of silently ignoring date bounds. The exporter also reads a pre-0011
database, treating its entries as unbounded.

Validation covers source-specific repairs and later-review guards for every
case, migration rollback/idempotence, unchanged legacy hashes, date validation,
split-order handling, cancellation target selection, no-new-bulletin transitions,
human approval of night services, old snapshots, and browser occurrence/map
behavior across the transition dates. Full Python and web/labeler checks and
builds are recorded in the PR.
