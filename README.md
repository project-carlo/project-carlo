# Bulletin Processing Pipeline

Fetch parish bulletin PDFs and extract schedule events (Mass, Confession, Adoration)
with Gemini into SQLite.

Curated inputs (the parish and church lists, the schema, the code) live in git.
Everything the pipeline observes (bulletin PDFs, extraction results, the
events database, and the snapshot the website serves) lives in Cloudflare R2
and is pulled on demand. See [How data is stored](#how-data-is-stored).

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for Python and dependency management.
- [pnpm](https://pnpm.io/installation) for the web workspace.

Install on Windows (PowerShell):

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal, then run `uv --version` to confirm.

## Setup

From the project root:

```bash
uv sync --group dev
pnpm install
```

`pnpm install` uses [`pnpm-workspace.yaml`](pnpm-workspace.yaml) and installs JavaScript dependencies for `apps/web` (package name `web`) into the workspace store. The root `package.json` has no Node dependencies of its own; `pnpm install:web` is the same command if you prefer an explicit name.

## Get the data

The database and the website's snapshot are not committed. Pull the published copy:

```bash
pnpm data:pull
```

That needs R2 credentials in your environment or in `.env` (read-only keys are
enough; see [docs/data-setup.md](docs/data-setup.md)). Without credentials, you
can still get the snapshot the live site serves, which is all the web app needs:

```bash
pnpm data:pull --snapshot-only --public-fallback
```

## Run the web app

Start the web app (after pulling the snapshot):

```bash
pnpm dev:web
```

To see your own local pipeline changes in the app, rebuild the snapshot from
your local database with `pnpm extract:web`.

## Label bulletins (ground truth)

A local tool for recording by hand what each bulletin really says, to measure
Gemini against later. It runs on localhost only, with no auth, and reads R2
with the read-only keys (`R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`,
`R2_SECRET_ACCESS_KEY`).

```bash
pnpm label           # build the UI and serve it with the API at http://localhost:8766/
pnpm label --demo    # the same on a generated dataset (data/labeler-demo/, untracked)
pnpm dev:labeler     # Vite dev server on :5174, proxying /api to a running `pnpm label`
```

The PDF shown is the stored compacted copy (the first 10 pages), so page
numbers match what Gemini saw. Gemini's output is shown read-only: the cached
result for the bulletin's content hash (the current classifier version first),
or else the database's post-processed events. Accept rows one at a time
(Enter) or all at once, then fix them. Press `?` in the app for the keyboard
shortcuts.

Labels are saved to `data/labels/<parish_slug>/<content_hash>.json` and are
committed to git. Each file (`schema_version` 1) holds:

- `parish_slug`, `content_hash`, `source_url`
- `status`: `in_progress`, `done` or `skipped`
- `flags`: `wrong_bulletin`, `unreadable`, `no_schedule`, `church_missing`
- `published_date`, `note`, `labeler`, `seconds_spent`, `updated_at`
- `events`: one per event, each with:
  - `church_slug`, `event_type` (`mass`/`confession`/`adoration`), `event_kind` (`weekly`/`specific_date`)
  - `day_of_week` or `date`, `start_time` and `end_time` (24-hour `HH:MM`), `cancelled`, `page_number`, `note`
  - `weeks_of_month` (`first`…`fifth`, `last`; empty means every week) and `season` (`{start_month, start_day, end_month, end_day}`, which may wrap past New Year). These two apply to weekly rows only.
  - `origin`: `human`, `gemini` or `gemini-edited`

The API validates every file (`src/pdf_extract/labeling/labels.py`) and
rejects any slug or hash that would put it outside `data/labels`.

### Run a classifier over the labeled bulletins

```bash
pnpm eval --classifier gpt-6-luna --limit 2   # smoke test on two bulletins
pnpm eval --classifier gpt-6-luna             # every label marked done
pnpm eval --classifier gpt-6-luna --status done --status in_progress --parish all-saints-albany
```

Any classifier in `src/pdf_extract/classifiers/__init__.py` can be run
(`gemini-flash`, `gpt-6-luna`, `gpt-6-luna-nonstrict`, ...). Each bulletin is
classified as of the day it was fetched, and results are cached by classifier
version (model, prompt, schema and settings), PDF and church list, so re-running
an unchanged classifier makes no API calls (`--refresh` forces them). Output
goes to `data/runs/<classifier>/eval/<version>/`:

- `predictions/<parish_slug>/<content_hash>.json`: the classifier's events in
  the label's row shape, next to `published_date`, `wrong_bulletin`, token usage
  and timing, so each file lines up with its label.
- `run.json`: cache hits, errors, skipped bulletins and summed token usage.

The `gpt-6-luna` classifiers (`classifiers/openai_responses.py`) use the
Responses API with the schema and prompt in `classifiers/qualified_schedule.py`:
the production schema plus `weeks_of_month` and `season` on weekly slots, and the
production Gemini prompt extended with the labeling rules (weekly vs dated,
chapels, Communion Services, times given relative to a Mass), its static part
sent first as an explicit prompt-cache breakpoint. They need `OPENAI_API_KEY`.

### Score an eval run against the labels

```bash
pnpm eval:report --classifier gpt-6-luna                  # its current version
pnpm eval:report --classifier gpt-6-luna --version <ver>  # an older version's output
```

Writes `report.md` and `report.json` next to the predictions
(`src/pdf_extract/evals/report.py`). Labels marked done are scored (`--status
in_progress` adds those); skipped labels never are. Within each bulletin every
label event is paired with at most one prediction, in tiers tried strictest
first:

| Tier | Agrees on | Counts as found |
|---|---|---|
| `exact` | church, type, weekly/dated, weekday or date, start, cancelled, end time, weeks of month, season | strict, core, loose, any_time |
| `core` | the same, but end time, weeks of month or season differ | core, loose, any_time |
| `weekly_vs_dated` | weekly on one side, dated on the other, same weekday; church, type, start, cancelled agree | loose, any_time |
| `wrong_church` | everything in `core` but the church | never |
| `wrong_type` | everything in `core` but the event type | never |
| `wrong_time` | church, type, kind, weekday or date, cancelled; the start time differs | any_time |

The report gives precision, recall and F1 (pooled and per-bulletin average) at
the strict, core, loose and any_time levels; the wrong-church, wrong-type, missed and
spurious rates; the same broken down by event type and by weekly/dated; how
often end time, weeks of month, season and the presence of a note agree on the
pairs found at the loose level; per-bulletin perfect rate, published-date accuracy, wrong-bulletin
agreement and event-count error; token usage and timing; and every bulletin's
differences, worst bulletin first.

## Weekly pipeline

One command runs a whole weekly pass:

`fetch -> process -> snapshot -> publishing checks -> change report`

```bash
pnpm weekly:run            # = python -m pdf_extract weekly
pnpm weekly:run -- --diocese buffalo
pnpm weekly:run -- --parish st-joseph-cathedral-buffalo
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

The run's status decides what happens next:

| Status | Exit code | Meaning |
| :-- | :-: | :-- |
| `passed` | 0 | Every publishing check passed; safe to publish. |
| `held` | 10 | A check failed: church count changed, total events moved more than 10%, less than 90% of weekly slots survived, a parish dropped to zero events, a parish or church was removed from the CSVs, or more than half of the parishes failed to fetch. A person decides. |
| `failed` | 1 | A stage crashed. |

A local run never publishes anything.

### GitHub Actions

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

The change report is always in the job summary, and kept as a workflow
artifact for 90 days.

The R2 bucket, its API tokens and the repository secrets are described in
[docs/data-setup.md](docs/data-setup.md).

### Local Docker run

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

## How data is stored

| What | Where | Written by |
| :-- | :-- | :-- |
| Parish and church lists | `data/parishes.csv`, `data/churches.csv` in git | people, in pull requests |
| Database schema | `data/migrations/*.sql` in git | people, in pull requests |
| Bulletin PDFs | R2 `bulletins/<parish>/<sha256>.pdf` | `fetch` |
| Gemini extraction results | R2 `runs/<classifier>/cache/<version>/<sha256>.json` | `process`, `extract` |
| Bulletins, events, recurrence history, run records | the SQLite database, published per run to R2 `pipeline/runs/<run_id>/` | the pipeline |
| Website snapshot (gzipped JSON) | R2 `pipeline/runs/<run_id>/frontend.json.gz` (`frontend.snapshot`, gzipped SQLite, in older runs) | `weekly` |
| Which run is live | R2 `pipeline/latest.json` | the weekly workflow |

Everything under `pipeline/runs/` is written once and never changed, and a
rollback is just moving the pointer. After each publish the weekly workflow
prunes old runs (`pnpm data:prune`), keeping the last 8 weeks and, for a
year, each month's last run that passed or was published; those are the runs
you can roll back to.

`fetch` stores a compacted copy of each bulletin: the first 10 pages (all the
classifiers read) with images downsampled to 150 dpi by Ghostscript, falling
back to the PDF as downloaded when that fails or saves nothing. The key's
hash is of the PDF as downloaded. Without `gs` installed, long bulletins are
only truncated.

Locally, `data/` doubles as a cache of the bucket: a PDF or cached extraction
is downloaded the first time a command needs it and kept. With no R2
credentials the pipeline runs purely on local files.

Writes to R2 are opt-in (`CARLO_REMOTE_WRITE=1`) and only the weekly workflow
has write keys. Anyone else pulling data uses read-only keys, so nothing run
outside the workflow can change shared data, even `fetch` or `process`.

### Working with the database

```bash
pnpm data:pull        # reset data/parish_events.db (and the snapshot) to the published run
pnpm data:status      # which run is published, and recent runs
pnpm data:prune       # which old runs pruning would delete (--apply deletes them)
pnpm db:create        # an empty database instead (schema + parishes/churches, no bulletins)
```

`pnpm data:pull --run-id <id>` pulls a specific run instead, e.g. a held one
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

## Usage

### Command line

Run each stage independently:

```bash
pnpm run fetch [-- --parish "..."]
pnpm fetch:check [-- --parish SLUG --provider other --record tests/fixtures/fetch]
pnpm process [-- --parish "..." --model gemini-3-flash-preview]
pnpm weekly:run [-- --parish SLUG --diocese SLUG]
pnpm detect [-- --dry-run --limit N --pause-seconds 0.5]
pnpm recurrence:apply
pnpm geocode [-- --dry-run --limit N --email "you@example.com"]
pnpm diocese <subcommand> ...
pnpm extract:web
pnpm verify:frontend-snapshot
pnpm data:pull [--run-id ID --snapshot-only --no-snapshot]
pnpm data:status
pnpm data:prune [--keep-recent N --keep-monthly N --apply]
pnpm db:create
pnpm db:drop
```

Every stage is a subcommand of `python -m pdf_extract`; the `pnpm` scripts above
are shorthands for it. All commands accept
`-- --log-level DEBUG|INFO|WARNING|ERROR` (default: `INFO`), and each prints its
result as JSON on success.

Stage idempotency:

- `fetch` skips URLs already recorded in `bulletin.source_url`
- `process` skips bulletins with `processed_at` already set, and serves
  bulletins it has extracted before (same PDF hash, same model) from the cache

### Checking the fetch stage

Most parishes publish through ParishesOnline, eCatholic or Discover Mass, but
the `other` provider has to find the bulletin on the parish's own website, and
every site is laid out differently. `pnpm fetch:check` runs the resolvers in the
browser without touching the database, downloads what each one picks, and
prints one row per parish (`ok`, `resolve_failed`, `download_failed`,
`not_pdf`, or `blocked` when Cloudflare challenged the browser instead).

To keep a resolver change from fixing one site and breaking another, the pages
each resolver read on every parish's real site are recorded in
`tests/fixtures/fetch/<slug>.json.gz`, and `tests/test_fetch_replay.py` replays
them offline against the bulletin in `expected.json`. After changing `fetch.py`:

1. Run `pnpm test`. A changed pick on any recorded site fails the replay test.
   A site that now opens a page the old resolver never did fails with "re-record
   this parish".
2. Re-record the sites whose result should change, then check them by hand:
   `pnpm fetch:check -- --parish SLUG --record tests/fixtures/fetch`.
3. Update their entries in `tests/fixtures/fetch/expected.json`. That diff is the
   coverage change.

Run `fetch:check` in a headed browser (under `xvfb-run` on a server); Cloudflare
turns headless browsers away. In a Claude Code cloud sandbox, set up Chrome first
with `.claude/skills/parish-site-access/scripts/setup_browser.sh` and set
`PLAYWRIGHT_BROWSER_CHANNEL=chrome`.

### From Python

```python
from pdf_extract import extract_events, fetch_bulletins, process_bulletins

fetch_result = fetch_bulletins(parish_name="Southeast Rochester Catholic Community")
process_result = process_bulletins(parish_name="Southeast Rochester Catholic Community")
```

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

## Exploring new dioceses

`data/dioceses/<diocese>/` is where a diocese the pipeline does not cover yet is worked out
before its rows are promoted into `data/parishes.csv` and `data/churches.csv`. It has one
Markdown file per parish (bulletin publisher), church (worship site), excluded place and open
question. Each file carries dated, quoted evidence and an explanation written for whoever
audits the row later, and the files stay as the provenance of the live rows after
promotion. `pnpm diocese` fetches rosters (GCatholic, WP Store Locator parish finders),
measures coverage against them, audits which rows might be one bulletin, probes parish sites,
ParishesOnline containers and bulletin PDFs, rechecks evidence, and promotes. See
[`data/dioceses/README.md`](data/dioceses/README.md); agents get the short version from the
`explore-diocese` skill in `.claude/skills/`.

## Environment Variables

Commands read a `.env` file in the repo root if there is one (without
overriding variables already set).

- `GEMINI_API_KEY`: automatically picked up by the Gemini client.
- `OPENAI_API_KEY`: for the OpenAI classifiers (`pnpm eval`, `pnpm extract`).
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`: Cloudflare R2
  access. Without them everything runs on local files only.
- `R2_BUCKET`: bucket name (default `project-carlo-data`).
- `R2_ENDPOINT_URL`: only for a bucket in a jurisdiction (e.g. `https://<account>.eu.r2.cloudflarestorage.com`); otherwise derived from `R2_ACCOUNT_ID`.
- `CARLO_REMOTE_WRITE=1`: let commands write to R2. Set only by the weekly workflow.

### Web app (`apps/web`)

- `VITE_GEOAPIFY_API_KEY`: place search on the map (see `apps/web/.env.production`).
- `VITE_TALLY_FORM_ID`: Tally form ID for user feedback (e.g. `Me65rA` from `https://tally.so/r/Me65rA`). Set in `apps/web/.env.development` (dev) and `apps/web/.env.production` (build). When unset, feedback links are hidden.

## User feedback

Comments and corrections are collected with [Tally](https://tally.so). The form should include hidden fields named `page_path`, `full_url`, `church_slug`, and `church_name` (the app prefills these when someone opens the popup).

Review submissions in the Tally dashboard for your form → **Submissions**. Export CSV when batching data fixes.

## Project layout

- `pyproject.toml` - project metadata and dependencies
- `package.json` and `pnpm-workspace.yaml` - JS workspace for frontend
- `uv.lock` - locked dependency versions
- `data/migrations/` - SQLite schema, as numbered migrations
- `data/parishes.csv`, `data/churches.csv` - curated parish and church lists
- `data/dioceses/` - parishes and churches of dioceses still being explored
- `data/` (untracked) - the local database, bulletin PDF cache and run outputs
- `docs/data-setup.md` - R2 bucket, API tokens, GitHub secrets, and running the published data
- `apps/web/` - React + TypeScript + Vite frontend
- `apps/labeler/` - the local bulletin labeling UI (never deployed)
- `data/labels/` - ground-truth labels, one JSON file per bulletin (committed)
- `src/pdf_extract/extract_frontend_db.py` - builds the frontend snapshot (gzipped JSON; the format is in its docstring)
- `src/pdf_extract/` - Python CLI package
  - `__main__.py` - CLI entry point
  - `fetch.py` - bulletin fetching and provider link resolution
  - `fetch_check.py` - `fetch:check`, and recording/replaying the pages resolvers read
  - `process.py` - bulletin processing with Gemini AI
  - `schedule_extraction.py` - Gemini schedule extraction
  - `storage.py` - SQLite helpers and data paths
  - `db.py` - migrations and CSV seeding
  - `blobstore.py` - local/R2 storage for PDFs and cached extractions
  - `datasync.py` - pull, upload and publish runs
  - `weekly.py` - the weekly run; `report.py` its change report; `runs.py` run records
  - `detect.py` - bulletin provider detection (Playwright)
  - `recurrence.py` - promotes repeatedly-dated events to weekly ones
  - `timeparse.py` - shared parsing of the loose time/date strings the LLM returns
  - `geocode.py` - address geocoding (Nominatim)
  - `dioceses/` - diocese exploration: records, rosters and coverage, web probes, the `diocese` command
  - `labeling/` - the labeler's API (`pnpm label`): label files, bulletin queue, Gemini sources, demo data
  - `classifiers/` - pluggable bulletin → events classifiers (Gemini, OpenAI) and their registry
  - `evals/` - running classifiers over the labeled bulletins (`pnpm eval`)

## Dependencies

- [google-genai](https://github.com/googleapis/python-genai) - Gemini API client for PDF processing and structured JSON output.
- [playwright](https://playwright.dev/python/) - bulletin provider detection and link resolution.
- [pydantic](https://docs.pydantic.dev/) - data validation and Gemini response parsing.
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Cloudflare R2 access (S3 API).

To add more dependencies:

```bash
uv add package-name
```

## Development

Run linting:

```bash
pnpm lint
```

Run tests:

```bash
pnpm test
```
