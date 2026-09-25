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

## Weekly pipeline

One command runs a whole weekly pass:

`fetch -> process -> snapshot -> publishing checks -> change report`

```bash
pnpm weekly:run            # = python -m pdf_extract weekly
```

Every run has an id. Each stage records what it did for each parish under that
id (`pipeline_run` and `run_parish_result` tables), and the run ends with a
report comparing the database before and after it, written to
`data/out/<run_id>/`:

- `report.md` / `report.json`: the publishing checks, per-parish failures (with
  how many runs in a row they have failed), stale parishes, and every Mass,
  Confession and Adoration that appeared or disappeared, church by church.
- `frontend.snapshot`: what the website would serve.
- `before.db`: the database as the run found it.

The run's status decides what happens next:

| Status | Exit code | Meaning |
| :-- | :-: | :-- |
| `passed` | 0 | Every publishing check passed; safe to publish. |
| `held` | 10 | A check failed (church count changed, total events moved more than 10%, less than 90% of weekly slots survived, or a parish dropped to zero events). A person decides. |
| `failed` | 1 | A stage crashed. |

A local run never publishes anything.

### GitHub Actions

`.github/workflows/weekly-docker.yml` runs Sundays at 08:17 UTC (and on
demand). It pulls the published database, runs the pipeline in the Docker
image, uploads the result to R2 as a candidate, and then:

- **passed**: publishes it (moves `pipeline/latest.json` to the new run) and
  deploys the site.
- **held** or **failed**: leaves the site on the previous run, opens or updates
  an issue labelled `data-refresh` with the change report, and fails the job.
  To publish a held run anyway, run the **Publish Data Run** workflow with its
  run id. The same workflow rolls back: publish an earlier run id.

The change report is always in the job summary, and kept as a workflow
artifact for 90 days. Nothing is committed to the repository.

Repository secrets and the one-time setup are in
[docs/data-setup.md](docs/data-setup.md).

### Local Docker run

```bash
docker compose build weekly-job
export GEMINI_API_KEY=... R2_ACCOUNT_ID=... R2_ACCESS_KEY_ID=... R2_SECRET_ACCESS_KEY=...
docker compose run --rm weekly-job
```

The Docker image runs Playwright in headed mode under `xvfb` when no display is
available. For debugging, set `PLAYWRIGHT_HEADLESS=1` to force headless mode or
`PLAYWRIGHT_BROWSER_CHANNEL=chrome` to use a locally installed Chrome channel.

## How data is stored

| What | Where | Written by |
| :-- | :-- | :-- |
| Parish and church lists | `data/parishes.csv`, `data/churches.csv` in git | people, in pull requests |
| Database schema | `data/migrations/*.sql` in git | people, in pull requests |
| Bulletin PDFs | R2 `bulletins/<parish>/<sha256>.pdf` | `fetch` |
| Gemini extraction results | R2 `runs/<classifier>/cache/<version>/<sha256>.json` | `process`, `extract` |
| Bulletins, events, recurrence history, run records | the SQLite database, published per run to R2 `pipeline/runs/<run_id>/` | the pipeline |
| Website snapshot | R2 `pipeline/runs/<run_id>/frontend.snapshot` | `weekly` |
| Which run is live | R2 `pipeline/latest.json` | the weekly workflow |

Everything under `pipeline/runs/` is written once and never changed, so every
week's database stays available and a rollback is just moving the pointer.

Locally, `data/` doubles as a cache of the bucket: a PDF or cached extraction
is downloaded the first time a command needs it and kept. With no R2
credentials the pipeline runs purely on local files.

Writes to R2 are opt-in (`CARLO_REMOTE_WRITE=1`) and only the weekly workflow
has write keys. Laptops and agent sessions get read-only keys, so nothing run
outside the workflow can change shared data, even `fetch` or `process`.

### Working with the database

```bash
pnpm data:pull        # reset data/parish_events.db (and the snapshot) to the published run
pnpm data:status      # which run is published, and recent runs
pnpm db:create        # an empty database instead (schema + parishes/churches, no bulletins)
```

`pnpm data:pull --run-id <id>` pulls a specific run instead, e.g. a held one
you want to inspect. The database you replace is kept as
`data/parish_events.db.bak`.

Every pipeline command first brings the local database up to date: it applies
new migrations and re-seeds the `parish` and `church` tables from the CSVs,
matching rows by slug. An edited CSV takes effect on the next command, as
before. A parish or church removed from its CSV is deleted along with its
bulletins and events.

To change the schema, add the next numbered file to `data/migrations/`; never
edit one that has shipped. `PRAGMA user_version` records which migrations a
database has.

## Usage

### Command line

Run each stage independently:

```bash
pnpm run fetch [-- --parish "..."]
pnpm process [-- --parish "..." --model gemini-3-flash-preview]
pnpm weekly:run
pnpm detect [-- --dry-run --limit N --pause-seconds 0.5]
pnpm recurrence:apply
pnpm geocode [-- --dry-run --limit N --email "you@example.com"]
pnpm extract:web
pnpm verify:frontend-snapshot
pnpm data:pull [--run-id ID --snapshot-only --no-snapshot]
pnpm data:status
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

## Environment Variables

Commands read a `.env` file in the repo root if there is one (without
overriding variables already set).

- `GEMINI_API_KEY`: automatically picked up by the Gemini client.
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`: Cloudflare R2
  access. Without them everything runs on local files only.
- `R2_BUCKET`: bucket name (default `project-carlo-data`).
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
- `data/` (untracked) - the local database, bulletin PDF cache and run outputs
- `docs/data-setup.md` - one-time R2 and GitHub setup
- `apps/web/` - React + TypeScript + Vite frontend
- `src/pdf_extract/extract_frontend_db.py` - builds the frontend SQLite snapshot
- `src/pdf_extract/` - Python CLI package
  - `__main__.py` - CLI entry point
  - `fetch.py` - bulletin fetching and provider link resolution
  - `process.py` - bulletin processing with Gemini AI
  - `schedule_extraction.py` - Gemini schedule extraction
  - `storage.py` - SQLite helpers and data paths
  - `db.py` - migrations, CSV seeding, legacy JSON import
  - `blobstore.py` - local/R2 storage for PDFs and cached extractions
  - `datasync.py` - pull, upload and publish runs
  - `weekly.py` - the weekly run; `report.py` its change report; `runs.py` run records
  - `detect.py` - bulletin provider detection (Playwright)
  - `recurrence.py` - promotes repeatedly-dated events to weekly ones
  - `timeparse.py` - shared parsing of the loose time/date strings the LLM returns
  - `geocode.py` - address geocoding (Nominatim)

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
