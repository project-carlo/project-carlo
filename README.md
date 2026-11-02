# Project Carlo

Project Carlo finds Mass, Confession and Adoration times at Catholic churches and
shows them on a map at [projectcarlo.com](https://projectcarlo.com). Most parishes
publish their schedule only in a weekly bulletin PDF, so each week this pipeline
fetches every parish's bulletin, reads the schedule out of it with a language
model, checks the result and publishes it to the site.

The repository holds:

- **The pipeline** (`src/pdf_extract/`, a Python CLI): fetching bulletins,
  extracting schedules and publishing a snapshot for the site.
- **The website** (`apps/web/`): a React app on Cloudflare that reads the snapshot.
- **The labeler** (`apps/labeler/`): a local tool for checking extractions by hand
  and seeding parishes' schedules.
- **The onboarding factory** (`factory/`): agent jobs that add new dioceses and
  their parishes.
- **The curated data** (`data/`): the parish and church lists, the database schema,
  diocese research, labels and seeds.

## How it works

Each Sunday a GitHub Actions workflow runs the weekly pass:

1. **Fetch** finds each parish's current bulletin, through its publisher
   (ParishesOnline, eCatholic, Discover Mass) or its own website, and stores the PDF.
2. **Process** reads each new bulletin. Most parishes are extracted from scratch by
   Gemini. A parish with a reviewed **believed schedule** (update mode) instead
   has an OpenAI model propose changes to that schedule, which code accepts or
   rejects.
3. **Snapshot** builds the JSON file the website serves.
4. **Publishing checks** compare the run with the last one. If nothing moved too
   far, the run is published and the site deployed. If something did, the run is
   held and a GitHub issue is opened for a person to review.

New dioceses are researched in `data/dioceses/` and promoted into
`data/parishes.csv` and `data/churches.csv`. Each new parish is then given a
reviewed first schedule (its seed). The onboarding factory runs both steps with
agents.

## Quick start

These steps work on macOS and Linux (including WSL).

### 1. Install the tools

You need [uv](https://docs.astral.sh/uv/) (it installs the right Python, 3.13,
for you), [Node.js](https://nodejs.org/) 22 with pnpm, and Ghostscript, which
shrinks bulletin PDFs. Fetches open a headed browser, which Cloudflare blocks less
often than a headless one. On Linux without a display, run them under
`xvfb-run -a` (from `xvfb`), or set `PLAYWRIGHT_HEADLESS=1`.

macOS ([Homebrew](https://brew.sh)):

```bash
brew install uv node@22 ghostscript
echo 'export PATH="$(brew --prefix node@22)/bin:$PATH"' >> ~/.zshrc && exec zsh
corepack enable    # provides the pnpm version pinned in package.json
```

Linux (Debian or Ubuntu):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo apt-get update && sudo apt-get install -y ghostscript xvfb
```

Then install Node 22 ([nodejs.org](https://nodejs.org/en/download) has commands
for nvm and other installers) and run `corepack enable`, with `sudo` if Node is
installed system-wide.

### 2. Install the dependencies

From the project root:

```bash
uv sync --group dev
pnpm install
uv run playwright install chromium   # on Linux: add --with-deps
```

`pnpm install` installs the web app and labeler (see `pnpm-workspace.yaml`). The
Playwright browser is needed to fetch bulletins.

### 3. Get the data

The database and the website's snapshot are not committed. Pull the published
copy:

```bash
pnpm data:pull
```

That needs R2 credentials in your environment or in `.env` (read-only keys are
enough; see [docs/data-setup.md](docs/data-setup.md)). Without credentials, you
can still get the snapshot the live site serves, which is all the web app needs:

```bash
pnpm data:pull --snapshot-only --public-fallback
```

### 4. Run the web app

```bash
pnpm dev:web
```

To see your own local pipeline changes in the app, rebuild the snapshot from your
local database with `pnpm extract:web`.

## Commands

Every pipeline command is a subcommand of `python -m pdf_extract`, and the `pnpm`
scripts in `package.json` are shortcuts for them. Pass flags straight after the
script name, without a `--` (`pnpm weekly:run --diocese buffalo`). Each command
takes `--help` and `--log-level DEBUG|INFO|WARNING|ERROR` (default `INFO`), and
prints its result as JSON on success.

`pnpm fetch` is pnpm's own command, so the fetch script is run as `pnpm run fetch`.

| Command | What it does |
| :-- | :-- |
| **Weekly pipeline** | |
| `pnpm weekly:run [--parish SLUG] [--diocese SLUG]` | The whole weekly pass, locally (never publishes) |
| `pnpm run fetch [--parish NAME] [--workers N]` | Fetch new bulletins |
| `pnpm process [--parish NAME] [--model M] [--include-fetch-only]` | Extract or update schedules from new bulletins |
| `pnpm recurrence:apply` | Re-run weekly-recurrence promotion over current events |
| `pnpm extract:web` | Rebuild the web app's snapshot from the local database |
| `pnpm verify:frontend-snapshot` | Check a new snapshot hasn't drifted too far from the previous one |
| **Data** | |
| `pnpm data:pull [--run-id ID] [--snapshot-only] [--no-snapshot]` | Replace the local database (and snapshot) with a published run |
| `pnpm data:status` | Which run is published, and recent runs |
| `pnpm data:prune [--apply]` | Which old runs pruning would delete |
| `pnpm db:create` / `pnpm db:drop` | An empty database (schema and CSVs, no bulletins) / delete it |
| **Fetching and parish data** | |
| `pnpm fetch:check [--parish SLUG] [--provider P] [--record DIR]` | Dry-run the bulletin resolvers ([docs/fetching.md](docs/fetching.md)) |
| `pnpm detect` / `pnpm detect:apply` | Detect each parish's bulletin provider / write it to the CSV |
| `pnpm verify` / `pnpm verify:apply` | Check church data against the latest bulletins / write fixes to the CSV |
| `pnpm geocode` / `pnpm geocode:apply` | Look up church coordinates from addresses / write them to the CSV |
| `pnpm diocese <subcommand>` | Research a new diocese ([data/dioceses/README.md](data/dioceses/README.md)) |
| **Schedules and seeding** | |
| `pnpm schedule <subcommand>` | Inspect and hand-edit believed schedules |
| `pnpm seed <subcommand>` | Draft, check and approve parish seeds |
| `pnpm factory <subcommand>` | The onboarding factory |
| **Labels and evals** | |
| `pnpm label [--demo]` | The labeler, at http://localhost:8766/ |
| `pnpm eval --classifier C` / `pnpm eval:report --classifier C` | Run a classifier over the labeled bulletins / score it |
| `pnpm extract --classifier C` / `pnpm compare C1 C2 ...` | Run an experimental classifier over fetched bulletins / compare runs |
| `uv run python -m pdf_extract replay-gates` | Replay the publishing checks over archived runs (no pnpm script) |
| **Web app and labeler** | |
| `pnpm dev:web` / `pnpm build:web` / `pnpm preview:web` | Run the web app's dev server / build it / build and serve it with wrangler |
| `pnpm perf:web` | Benchmark the web app's UI |
| `pnpm geocode:cities` | Look up the centre of each city page's city |
| `pnpm dev:labeler` | The labeler's Vite dev server ([docs/labeling-and-evals.md](docs/labeling-and-evals.md)) |
| `pnpm check:core` / `pnpm lint:core` / `pnpm test:core` | Type check, lint and test the shared `@carlo/core` package |
| `pnpm install:web` | Same as `pnpm install` |
| **Other** | |
| `pnpm analytics` | Report on site visits ([docs/analytics.md](docs/analytics.md)) |

The pipeline can also be called from Python:

```python
from pdf_extract import fetch_bulletins, process_bulletins

fetch_bulletins(parish_name="Southeast Rochester Catholic Community")
process_bulletins(parish_name="Southeast Rochester Catholic Community")
```

## Weekly pipeline

```bash
pnpm weekly:run                                    # every parish
pnpm weekly:run --diocese buffalo                  # one diocese
pnpm weekly:run --parish st-joseph-cathedral-buffalo
```

A run writes its change report, the snapshot it built and the database it started
from to `data/out/<run_id>/`. It ends `passed` (exit code 0), `held` (10: a
publishing check failed and a person decides) or `failed` (1: a stage crashed).
On GitHub, a passed run is published and deployed. A held run opens a
`data-refresh` issue and can be published by hand with the **Publish Data Run**
workflow, which also rolls back.

Parishes marked `fetch_only` in `data/parishes.csv` have their bulletins fetched
but not extracted or shown, so a new diocese can be checked before money is spent
on it.

Details, including the publishing checks, fetch-only parishes, recurrence
detection, the workflows, deploys and a local Docker run, are in
[docs/weekly-pipeline.md](docs/weekly-pipeline.md). How fetching works, and how to
change it safely, is in [docs/fetching.md](docs/fetching.md).

## How data is stored

Curated inputs (the parish and church lists, the schema, the code) live in git.
Everything the pipeline observes lives in Cloudflare R2 and is pulled on demand:

| What | Where | Written by |
| :-- | :-- | :-- |
| Parish and church lists | `data/parishes.csv`, `data/churches.csv` in git | people, in pull requests |
| Database schema | `data/migrations/*.sql` in git | people, in pull requests |
| Bulletin PDFs | R2 `bulletins/<parish>/<sha256>.pdf` | `fetch` |
| Extraction results | R2 `runs/<classifier>/cache/<version>/<sha256>.json` | `process`, `extract` |
| Bulletins, events, recurrence history, run records | the SQLite database, published per run to R2 `pipeline/runs/<run_id>/` | the pipeline |
| Website snapshot (gzipped JSON) | R2 `pipeline/runs/<run_id>/frontend.json.gz` | `weekly` |
| Which run is live | R2 `pipeline/latest.json` | the weekly and Publish Data Run workflows |

Published runs are never changed, so a rollback only moves the pointer. Locally,
`data/` doubles as a cache of the bucket, and with no R2 credentials the pipeline
runs on local files only. Only the weekly and Publish Data Run workflows can write
to R2.

Every pipeline command first brings the local database up to date: it applies new
migrations and re-seeds the `parish` and `church` tables from the CSVs. A parish
or church removed from its CSV is deleted along with its bulletins and events.

More in [docs/weekly-pipeline.md](docs/weekly-pipeline.md#data-and-the-database).
The bucket, its keys and the repository secrets are set up in
[docs/data-setup.md](docs/data-setup.md).

## Adding parishes

### Exploring new dioceses

`data/dioceses/<diocese>/` is where a diocese the pipeline does not cover yet is
worked out before its rows are promoted into `data/parishes.csv` and
`data/churches.csv`. It has one Markdown file per parish (bulletin publisher),
church (worship site), excluded place and open question. Each file carries dated,
quoted evidence and an explanation for whoever audits the row later, and the files
stay as the provenance of the live rows after promotion. `pnpm diocese` fetches
rosters, measures coverage against them, probes parish sites and bulletins,
rechecks evidence, and promotes. See
[`data/dioceses/README.md`](data/dioceses/README.md); agents get the short version
from the `explore-diocese` skill in `.claude/skills/`.

### Seeding parishes

A parish's first seed (`data/seeds/<parish>.json`) is drafted from its bulletins
and approved by the onboarding factory's seed Runs
([docs/seeding-plan.md](docs/seeding-plan.md)). Its drafters follow the
`draft-parish-seed` skill, whose [rules.md](.claude/skills/draft-parish-seed/rules.md)
holds every seeding decision (a slot no rule covers becomes a question), and
[file-format.md](.claude/skills/draft-parish-seed/file-format.md) holds the file
format. `seed-review` answers the questions and approves. The factory's PR lists
each answer, and the owner can change one in the labeler's **Seeds** mode
(`pnpm label`) before merging. Pipeline commands load newly approved files as
`seed` revisions, which puts those parishes in update mode (a deploy never loads
them).

```bash
pnpm seed --help                        # every command, by phase
pnpm seed start st-mary-albany          # start or resume a draft; prints where it starts from
pnpm seed finalize st-mary-albany       # the drafter's last step: bookkeeping, then check
pnpm seed check --all                   # check every file; `status` lists them
pnpm seed questions --answered --by person   # the owner's changed answers, to find new rules
```

How update mode then keeps each schedule current is in
[docs/believed-schedules.md](docs/believed-schedules.md).

### Onboarding factory

The factory takes a diocese from nothing to seeded parishes without a person in the
loop, apart from merging its PRs and answering its GitHub issues
([docs/factory.md](docs/factory.md)). A dispatcher runs small agent jobs
one at a time: a map Run (survey, batches of parishes, reconcile, promote, PR) for
each diocese in `factory/queue.json`, then seed Runs once the mapped parishes have
bulletins. Stage specs and prompts are in `factory/`. The ledger, transcripts and
Run worktrees are in `data/factory/` of the dispatcher's own checkout; the live
dispatcher runs from `~/carlo-factory`.

```bash
uv sync --group dev --group factory            # the Agent SDK
pnpm factory run --stub scenario.json          # canned workers: no usage, no GitHub
pnpm factory run                               # the dispatcher (or factory/carlo-factory.service)
pnpm factory status                            # Runs, the running job, usage, open issues
pnpm factory inspect wilmington-map-1/004-map  # one job in full; the `foreman` skill starts here
pnpm seed approve <parish> --reviewer agent:seed-review@<commit> --answers answers.json
```

## Labels and evals

`pnpm label` opens a local tool for recording by hand what each bulletin really
says. The labels are committed under `data/labels/`, and `pnpm eval` and
`pnpm eval:report` score any classifier against them. The label format, the
classifiers and how scoring works are in
[docs/labeling-and-evals.md](docs/labeling-and-evals.md).

## Environment variables

Commands read a `.env` file in the repo root if there is one (without overriding
variables already set).

- `GEMINI_API_KEY`: for extract-mode `pnpm process` and the Gemini classifiers.
- `OPENAI_API_KEY`: for the OpenAI classifiers (`pnpm eval`, `pnpm extract`),
  the update-mode calls of `pnpm process` and `pnpm weekly:run`, and
  `pnpm seed ask|extract`.
- `CARLO_SEED_CALL_LIMIT`: external calls `pnpm seed ask|extract` may make per
  parish (default 4).
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`: Cloudflare R2
  access. Without them everything runs on local files only.
- `R2_BUCKET`: bucket name (default `project-carlo-data`).
- `R2_ENDPOINT_URL`: only for a bucket in a jurisdiction (e.g.
  `https://<account>.eu.r2.cloudflarestorage.com`); otherwise derived from
  `R2_ACCOUNT_ID`.
- `CARLO_REMOTE_WRITE=1`: let commands write to R2. Set only by the weekly and
  Publish Data Run workflows.
- `PLAYWRIGHT_HEADLESS=1`: force a headless browser. `PLAYWRIGHT_BROWSER_CHANNEL=chrome`:
  use the installed Chrome instead of Playwright's Chromium.

### Web app (`apps/web`)

- `VITE_GEOAPIFY_API_KEY`: place search on the map (see `apps/web/.env.production`).
- `VITE_TALLY_FORM_ID`: Tally form ID for user feedback (e.g. `Me65rA` from
  `https://tally.so/r/Me65rA`). Set in `apps/web/.env.development` (dev) and
  `apps/web/.env.production` (build). When unset, feedback links are hidden.

## The website

**Feedback.** Comments and corrections are collected with
[Tally](https://tally.so). The form should include hidden fields named
`page_path`, `full_url`, `church_slug` and `church_name`, which the app prefills
when someone opens the popup. Review submissions in the Tally dashboard under
**Submissions**, and export a CSV when batching data fixes.

**Analytics.** The site records pageviews and a few actions (search picks,
filters, bulletin clicks) itself, in Cloudflare Workers Analytics Engine: no
cookies, no third party. `pnpm analytics` prints a report, and `/admin/analytics`
shows the same reports behind Cloudflare Access. See
[docs/analytics.md](docs/analytics.md).

**Deploys.** Pushes to `main` deploy the site, and every pull request that touches
it gets a preview link. Deploys build the snapshot from the published database, so
CSV edits show up in previews and go live on merge.

## Project layout

- `src/pdf_extract/` - the pipeline's Python package
  - `__main__.py` - the CLI
  - `weekly.py` - the weekly run; `report.py` its change report; `runs.py` run records
  - `fetch.py` - bulletin fetching; `parish_sites/` reading parishes' own websites;
    `fetch_check.py` checking and recording what fetch picks; `browser.py` the shared
    Playwright launcher
  - `pdf_compact.py`, `pdf_truncate.py` - shrinking bulletins before they are stored
  - `duplicates.py`, `bulletin_week.py` - is a bulletin new, and which one is current
  - `process.py` - the process stage, in extract mode or update mode
  - `schedule_extraction.py` - the production Gemini extraction
  - `classifiers/` - pluggable bulletin → events classifiers (Gemini, OpenAI) and their registry
  - `schedule/` - believed schedules: the change log, decision policy, update stage and hand edits
  - `seeding/` - seed files: format and checks, the agent's tools, loading approved ones
  - `recurrence.py` - promotes repeatedly-dated events to weekly ones
  - `extract_frontend_db.py` - builds the website snapshot (the format is in its docstring)
  - `db.py`, `storage.py` - migrations, CSV seeding and SQLite helpers
  - `blobstore.py`, `datasync.py` - local/R2 storage; pulling, uploading and publishing runs
  - `detect.py`, `verify.py`, `geocode.py`, `apply.py` - finding providers, checking
    church data and geocoding, and writing the results back to the CSVs
  - `dioceses/` - diocese research and the `diocese` command
  - `factory/` - the onboarding factory's dispatcher
  - `labeling/` - the labeler's API
  - `evals/`, `extract_run.py`, `compare.py`, `replay_gates.py` - scoring and comparing classifiers, replaying checks
- `apps/web/` - the website (React, TypeScript, Vite, Cloudflare Workers)
- `apps/labeler/` - the local labeling UI (never deployed)
- `packages/core/` - `@carlo/core`: snapshot decoding, schedules and their formatting,
  shared by the website and the planned mobile app ([docs/mobile-port-plan.md](docs/mobile-port-plan.md))
- `factory/` - the factory's settings, stage specs, prompts and diocese queue
- `data/` - committed: `parishes.csv`, `churches.csv`, `migrations/`, `dioceses/`,
  `labels/`, `seeds/`, eval results under `runs/<classifier>/eval/`. Untracked: the
  local database, the bulletin cache and run outputs
- `docs/` - guides (`weekly-pipeline.md`, `fetching.md`, `believed-schedules.md`,
  `labeling-and-evals.md`, `factory.md`, `factory-quota.md`, `data-setup.md`,
  `analytics.md`) and design plans (`*-plan.md`)
- `tests/` - pytest suite, with recorded parish sites under `tests/fixtures/fetch/`
- `.github/workflows/` - CI, the weekly run, publishing and deploys
- `.claude/skills/` - skills for agents working on dioceses, seeds and the factory

## Development

```bash
pnpm test && pnpm lint                                   # Python: pytest and ruff
pnpm lint:core && pnpm check:core && pnpm test:core      # @carlo/core: lint, types, unit tests
pnpm lint:web && pnpm check:web && pnpm --filter web test   # web app: lint, types, unit tests
pnpm lint:labeler && pnpm check:labeler && pnpm test:labeler && pnpm build:labeler
```

CI (`.github/workflows/ci.yml`) runs the same checks on pull requests, in a
`python` job and a `node` job. A job whose files the pull request doesn't touch
skips its checks and passes.

- **Schema changes:** add the next numbered file to `data/migrations/`. Never edit
  one that has shipped.
- **Fetch changes:** the tests replay recorded parish sites, so a change that fixes
  one site and breaks another fails. See
  [docs/fetching.md](docs/fetching.md#recorded-sites) for re-recording.
- **Dependencies:** `uv add <package>` for Python (listed in `pyproject.toml`),
  `pnpm --filter web add <package>` for the web app.

## License

The code is licensed under the [GNU Affero General Public License v3.0](LICENSE).
If you run a modified version as a website, you must offer its source to the
people who use it.

The curated data in `data/` and the schedule data the site publishes (the
database and snapshot `pnpm data:pull` fetches) are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse them for any
purpose with credit to Project Carlo. The bulletins themselves belong to their
parishes and are not covered.

Two exceptions in that data:

- Church coordinates taken from OpenStreetMap are © OpenStreetMap contributors
  and available under the
  [Open Database License (ODbL)](https://opendatacommons.org/licenses/odbl/),
  not CC BY. These are the churches whose record in
  `data/dioceses/<diocese>/churches/` says `coordinates_from: osm-node` or
  `nominatim`, or `geocode-stage` (the `pnpm geocode` stage looks addresses up
  in OpenStreetMap's Nominatim). Their latitude and longitude carry the same
  terms in `data/churches.csv` and the published database.
- Other coordinates come from the sources their record names, most from
  [GCatholic](https://gcatholic.org)'s Plus Codes (`gcatholic-plus-code`);
  credit those sources too when you reuse them.

The fonts, map tiles and other third-party material the site uses are listed,
with their licenses, in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
