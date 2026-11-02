# The weekly pipeline

One command runs a whole weekly pass:

`fetch -> process -> snapshot -> publishing checks -> change report`

```bash
pnpm weekly:run            # = python -m pdf_extract weekly
pnpm weekly:run --diocese buffalo
pnpm weekly:run --parish st-joseph-cathedral-buffalo
```

`--parish` takes a slug or the name from `data/parishes.csv` (repeat it, or
pass several slugs separated by commas). `--diocese` takes a folder under
`data/dioceses/` and refreshes every live parish recorded there. The two
combine. Parishes outside the limit keep the bulletins they already had, and
the snapshot still contains every parish. Omit both to refresh everything.

Every run has an id. Each stage records what it did for each parish under that
id (`pipeline_run` and `run_parish_result` tables), and the run ends with a
report comparing the database before and after it, written to
`data/out/<run_id>/`:

- `report.md` / `report.json`: the publishing checks, per-parish failures (with
  how many runs in a row they have failed), stale parishes, and every Mass,
  Confession and Adoration that appeared or disappeared, church by church.
- `frontend.json.gz`: the snapshot the website would serve.
- `before.db`: the database as the run found it.

A parish's current bulletin is the one for the latest week, by the issue date
the extractor read off it (else the fetch date), and the most recently fetched
of that week's (`src/pdf_extract/bulletin_week.py`). So a second bulletin for a
week (a correction) replaces the first, and an old issue a site falls back to
is stored but never shown. The report lists the old issues, and flags a third
bulletin for one week for a person to look at. A parish is stale when its
newest bulletin is two weeks old, however recently the site served it.

`fetch` is described in [fetching.md](fetching.md). `process` skips bulletins with
`processed_at` already set, and takes bulletins it has extracted before (same PDF
hash, same classifier version) from the result cache instead of calling the model.

The run's status decides what happens next:

| Status | Exit code | Meaning |
| :-- | :-: | :-- |
| `passed` | 0 | Every publishing check passed; safe to publish. |
| `held` | 10 | A check failed: church count changed, total events moved more than 10%, less than 90% of weekly slots survived, a parish dropped to zero events, a parish or church was removed from the CSVs, or more than half of the parishes failed to fetch. A person decides. |
| `failed` | 1 | A stage crashed. |

A local run never publishes anything.

## Fetch-only parishes

A parish with `fetch_only` set to `true` in `data/parishes.csv` has its
bulletins fetched and stored every week, but `process` makes no model call for
it (Gemini or OpenAI), and the snapshot leaves out its churches, so the site
doesn't show them yet. Its fetch results get their own section of the run
report, and its failures don't count toward the publishing checks.
`pnpm diocese promote` marks every parish row it adds this way, so a new
diocese's bulletins can be checked before any money goes on extracting them.

To switch parishes on, clear the flag (leave the cell empty). The next run
processes each one's latest bulletin, not the weeks it was fetch-only.
Expect that run to be held if many parishes go live at once: their events
move the total past the 10% check. `pnpm process --include-fetch-only`
processes fetch-only parishes anyway, e.g. to try a few with `--parish`.

## Weekly recurrence detection

Bulletins are frequently unclear about whether a listing is a one-off or a
standing weekly slot, so the extractor sometimes files a recurring Mass,
Confession, or Adoration under a single calendar date. The frontend then shows
it as a dated event that vanishes once the date passes.

`src/pdf_extract/recurrence.py` catches those. Every occurrence the pipeline
extracts is recorded in the `event_occurrence` table, and when a dated event
turns up on the same weekday, at the same time, for the same church and event
type as each of the **two weeks immediately before it**, `process` rewrites it
as a weekly event (`event_kind` `weekly`, `day_of_week` filled in, `date`
cleared) before storing the bulletin's events.

Weekly extractions count towards that chain as much as dated ones. The
extractor is not consistent from week to week — on the current corpus, 173 of
1488 slots have been filed both ways at some point — so a slot that alternates
would otherwise never accumulate two consecutive dated sightings, even after
the bulletin had listed it in its weekly schedule for two months. A weekly row
carries no date, so it is credited to the week its bulletin covers: the first
matching weekday on or after the bulletin's published date. When the extractor
could not read an issue date off the bulletin, the fetch date stands in,
snapped to the nearest Sunday — it lands anywhere from the Saturday before
publication to the Wednesday after, and used raw it would credit a Sunday slot
to the wrong week roughly half the time.

The chain has to be unbroken: a slot seen two and four weeks ago but not last
week is fortnightly, not weekly, and is left as a dated event. Cancellations
are never promoted, and a promotion that would duplicate a weekly slot the same
bulletin already lists is dropped instead — including one that duplicates a
weekly slot the bulletin has *cancelled*. A bulletin's own dated rows never
count as evidence for that same bulletin, so a six-week series printed on three
consecutive dates stays a set of dated events instead of promoting itself to a
standing weekly one. Thresholds live at the top of `recurrence.py`
(`MIN_PRIOR_WEEKS`, `LOOKBACK_WEEKS`, `HISTORY_RETENTION_WEEKS`).

The occurrence table is the detector's memory of what bulletins announced:
the event table stores each bulletin's rows after promotion, and a promoted row
has lost the date it was sighted on.

`pnpm recurrence:apply` re-runs promotion over each parish's current events.
`process` already promotes each bulletin as it stores it; this is for applying
a changed threshold to events processed earlier. It records every sighting to
the history before promoting, since promotion clears a row's date.

## GitHub Actions

`.github/workflows/weekly-docker.yml` runs Sundays at 08:17 UTC (and on
demand). A manual run can be limited with its **Parishes** and **Dioceses**
inputs (slugs, comma-separated); leave them empty to refresh everything. A
limited run is published the same way when it passes: the snapshot still has
every parish, with fresh bulletins for the ones the run refreshed. The workflow
pulls the published database, runs the pipeline on the GitHub runner, uploads
the result to R2 as a candidate, and then:

- **passed**: publishes it (moves `pipeline/latest.json` to the new run),
  deploys the site, and closes any open `data-refresh` issues it supersedes.
- **held** or **failed**: leaves the site on the previous run, opens or updates
  an issue labelled `data-refresh` with the change report, and fails the job.
  To publish a held run anyway, run the **Publish Data Run** workflow with its
  run id. The same workflow rolls back: publish an earlier run id with
  **rollback** ticked. Without it, publishing a run older than the live one is
  refused, since that would drop the newer run's data.

Only the default branch writes to R2 or publishes. Dispatching the workflow on
another branch runs that branch's code against the published data and shows
its report, but nothing it fetches or extracts leaves the job.

Deploys build the snapshot themselves, from the published database with the
code being deployed, so the snapshot's format always matches the web app, and
edits to the CSVs show up in previews and go live on merge. The exception is a
CSV change that removes a parish or church: that deletes events, so deploys
build the snapshot from the published database as it stands, without the CSV
edits, until a reviewed weekly run publishes the removal.

Pushes to `main` deploy the site. Every pull request that touches the site gets
a preview: **Deploy Web** uploads each push to it and comments the link.

A deploy replaces the site's files, so a page opened before one would 404 on the
hashed chunks (`/assets/*`) its scripts still load. The production deploy
therefore runs `apps/web/scripts/carry-assets.ts` first: it downloads the files
the live site's `asset-manifest.json` lists that the new build no longer has,
for 14 days after they left it, into the build. Storage is free and wrangler
uploads only files Cloudflare doesn't already have; if the deploy would pass
15,000 files (the Free plan allows 20,000) the earliest retired go first. A
failed download or an unreachable site only means fewer files are carried; it
never fails the deploy.

A page whose chunk is gone anyway (open longer than that, or a file that wasn't
carried) reloads once into the new version (`apps/web/src/lib/staleDeploy.ts`),
as does one that fetches a snapshot in a format its code can't read.

The change report is always in the job summary, and kept as a workflow
artifact for 90 days.

The R2 bucket, its API tokens and the repository secrets are described in
[data-setup.md](data-setup.md).

## Local Docker run

```bash
docker compose build weekly-job
export GEMINI_API_KEY=... R2_ACCOUNT_ID=... R2_ACCESS_KEY_ID=... R2_SECRET_ACCESS_KEY=...
docker compose run --rm weekly-job
DIOCESES=buffalo docker compose run --rm weekly-job
PARISHES=st-joseph-cathedral-buffalo docker compose run --rm weekly-job
```

That image is for this local run. The weekly workflow installs the same Python
toolchain on the runner and does not build it. The image runs Playwright in
headed mode under `xvfb` when no display is available. For debugging, set
`PLAYWRIGHT_HEADLESS=1` to force headless mode or `PLAYWRIGHT_BROWSER_CHANNEL=chrome`
to use a locally installed Chrome channel.

## Data and the database

Where each kind of data lives is in the README's
[How data is stored](../README.md#how-data-is-stored).

Everything under `pipeline/runs/` is written once and never changed, and a
rollback is just moving the pointer. After each publish the weekly workflow
prunes old runs (`pnpm data:prune`), keeping the last 8 weeks and, for a
year, each month's last run that passed or was published; those are the runs
you can roll back to.

Locally, `data/` doubles as a cache of the bucket: a PDF or cached extraction
is downloaded the first time a command needs it and kept. With no R2
credentials the pipeline runs purely on local files.

Writes to R2 are opt-in (`CARLO_REMOTE_WRITE=1`) and only the weekly workflow
has write keys. Anyone else pulling data uses read-only keys, so nothing run
outside the workflow can change shared data, even `fetch` or `process`.

`pnpm data:pull --run-id <id>` pulls a specific run instead of the published one, e.g. a held one
you want to inspect. The database you replace is kept as
`data/parish_events.db.bak`. Runs from before the snapshot became JSON hold a
gzipped SQLite snapshot this code can't read: pulling one rebuilds its
snapshot from its database, and a `--snapshot-only` pull of one fails.

Every pipeline command first brings the local database up to date: it applies
new migrations and re-seeds the `parish` and `church` tables from the CSVs,
matching rows by slug. An edited CSV takes effect on the next command. A
parish or church removed from its CSV is deleted along with its bulletins and
events.

To change the schema, add the next numbered file to `data/migrations/`; never
edit one that has shipped. `PRAGMA user_version` records which migrations a
database has.
