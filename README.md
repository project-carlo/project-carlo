# Bulletin Processing Pipeline

Fetch parish bulletin PDFs and extract schedule events (Mass, Confession, Adoration)
with Gemini into SQLite.

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

## Run the web app

Refresh the frontend SQLite snapshot:

```bash
pnpm extract:web
```

Start the web app:

```bash
pnpm dev:web
```

## Weekly Docker workflow

Use the included Docker setup to run the weekly pipeline in one repeatable environment:

`fetch -> process -> extract:web -> verify:frontend-snapshot -> build:web`

The pipeline updates `data/metadata.json`, `data/events.json`, `data/event_history.json`, and
`apps/web/public/frontend.snapshot`. Downloaded PDFs and local SQLite/build artifacts stay untracked.

### First-time setup

1. Make sure you have `GEMINI_API_KEY` available in your shell.
2. Build the image:

```bash
docker compose build weekly-job
```

### Local weekly run

```bash
export GEMINI_API_KEY=...
docker compose run --rm -e GEMINI_API_KEY weekly-job
```

This runs `pnpm weekly:run`. It does not create commits; GitHub Actions owns the
scheduled commit step. Compose does not pass your repo `.env` file into the
container; pass only the specific variables you want with `-e`.

The Docker image runs Playwright in headed mode under `xvfb` when no display is
available. This avoids true headless mode while still working on GitHub-hosted
runners. For debugging, set `PLAYWRIGHT_HEADLESS=1` to force headless mode or
`PLAYWRIGHT_BROWSER_CHANNEL=chrome` to use a locally installed Chrome channel.

### GitHub Actions weekly run

The scheduled workflow lives at `.github/workflows/weekly-docker.yml`.

Required repository secrets:

- `GEMINI_API_KEY`

The workflow:

- runs on `workflow_dispatch` and Sundays at `08:17` UTC;
- builds the Docker image with Buildx and GitHub Actions layer cache;
- runs the weekly pipeline inside the container;
- copies back only `data/metadata.json`, `data/events.json`, `data/event_history.json`, and `apps/web/public/frontend.snapshot`;
- commits and pushes generated changes with the GitHub Actions bot when there is a diff.

GitHub scheduled workflows run on the default branch and use UTC. The `17` minute offset avoids the highest-load top-of-hour window.

### Scheduler examples

Linux cron (every Sunday at 03:00):

```cron
0 3 * * 0 cd /path/to/project-carlo && docker compose run --rm -e GEMINI_API_KEY weekly-job
```

Windows Task Scheduler action:

- Program/script: `docker`
- Arguments: `compose run --rm -e GEMINI_API_KEY weekly-job`
- Start in: path to the repository root

### Troubleshooting

- **Missing API keys**: pass `GEMINI_API_KEY` with `docker compose run -e`, or set it as a repository secret for GitHub Actions.
- **No commit created in GitHub Actions**: expected when the generated outputs did not change.
- **Verification failed**: `verify:frontend-snapshot` exits non-zero and stops build/commit by design.
- **Dependency changes not reflected locally**: rebuild the image with `docker compose build weekly-job`.
- **Browser behavior differs**: Docker defaults to headed Chromium under `xvfb`; set `PLAYWRIGHT_HEADLESS=1` only when you specifically want true headless mode.

## Usage

### Command line

Run each stage independently:

```bash
pnpm run fetch [-- --parish "..."]
pnpm process [-- --parish "..." --model gemini-3-flash-preview]
pnpm detect [-- --dry-run --limit N --pause-seconds 0.5]
pnpm recurrence:backfill [-- --limit N]
pnpm recurrence:apply
pnpm pattern:backfill [-- --dry-run]
pnpm geocode [-- --dry-run --limit N --email "you@example.com"]
pnpm db:create
pnpm db:drop
```

All commands accept `-- --log-level DEBUG|INFO|WARNING|ERROR` (default: `INFO`).

Stage idempotency:

- `fetch` skips URLs already recorded in `bulletin.source_url`
- `process` skips rows with `processed_at` already set

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
extracts is recorded in `data/event_history.json`, and when a dated event turns
up on the same weekday, at the same time, for the same church and event type as
each of the **two weeks immediately before it**, `process` rewrites it as a
weekly event (`event_kind` `weekly`, `day_of_week` filled in, `date` cleared)
before writing `data/events.json`.

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

Occurrences are grouped by slot on disk rather than stored one per row, which
keeps the file in the hundreds of KB rather than the low MB now that it covers
every event every week.

`data/event_history.json` is the pipeline's only memory of past bulletins —
`data/events.json` is compacted down to the latest bulletin per parish on every
run — so it is committed along with the other generated data files.

Two commands support it:

- `pnpm recurrence:backfill` seeds `data/event_history.json` from past committed
  revisions of `data/events.json`, so the detector does not have to wait weeks
  for evidence to accumulate. Run it locally: it shells out to `git log` and
  `git show`, and `.dockerignore` keeps `.git` out of the weekly image, so it
  cannot run inside the container.
- `pnpm recurrence:apply` re-runs promotion over the current `data/events.json`.
  `process` already promotes each bulletin as it merges it; this is for applying
  a backfilled history, or a changed threshold, to events processed earlier. Run
  it after `recurrence:backfill`, not before: promotion clears a row's date, so
  apply records every sighting to the history first and then promotes.
  Backfilling afterwards would be reading from an `events.json` that has already
  lost those dates.

## Partial-year and monthly schedules

Not every recurring slot happens every week, all year. Confessions at Holy
Trinity in Webster run Tuesdays at 4:30 — October through June. First Friday
devotions are a Friday slot that comes round once a month. The extractor used to
have nowhere to put either fact except `note`, free text nothing downstream
reads, so the map offered the confession slot in September and listed the
devotions as though they happened every Friday.

Three fields on a weekly event carry it now:

- `weeks_of_month` — which occurrences of the weekday within the month the slot
  falls on, as canonical ordinals (`first`, `first,third`, `last`). Empty means
  every week. `last` stays distinct from `fourth`: a month with five Fridays has
  a fourth Friday and a different last one.
- `season_start_month` / `season_start_day` / `season_end_month` /
  `season_end_day` — the inclusive range of the year the slot runs in. Both
  months null means all year, and a start later in the calendar than the end
  wraps the new year, which is the shape a schedule tied to the school year
  takes. A day is set only when the bulletin dated the boundary ("June 4
  through September 10"); a null day leaves that end at the edge of its month,
  which is what "January to April" means.
- `season_note` — how the bulletin itself worded that range. The days are what
  filtering reads; the note is what a reader is shown, so a parish that printed
  "January to April" is quoted rather than corrected to "January 1 through
  April 30". Weeks of the month get no such field: "First Friday of the month"
  derives from `weeks_of_month` and reads back the same. Anything further about
  a monthly slot — a Healing Mass, a benediction — belongs in the ordinary
  `note`, as it always did.

Only weekly events can carry them; a dated event already names the day it
happens. `src/pdf_extract/schedule_pattern.py` normalises whatever wording the
model returns and decides what the fields mean, and
`apps/web/src/lib/schedulePattern.ts` mirrors the same rules in the browser.

What the frontend does with them:

- **Map and filters** hide a weekly slot that is out of season. The map answers
  "where can I go this week", so a slot that does not resume until October is
  not an answer in September. Monthly slots stay — they do run at this time of
  year — and the pin popup carries a note saying which week of the month.
- **The church page** lists every slot either way, with the qualifier beside the
  time: "Tuesdays 4:30 p.m. — October through June". Someone looking up a parish
  wants its whole schedule, and the note is also what explains why the map did
  not show it. The phrase comes from `season_note` when there is one, and is
  derived from the fields otherwise.
- **Recurrence detection** stops counting these slots as evidence of a weekly
  one. A monthly row credited to its bulletin's week, or a seasonal row credited
  out of season, would invent sightings on weeks the slot never happens — and a
  few of those in a row are exactly what promotion reads as a standing weekly
  slot.

`pnpm pattern:backfill` recovers the qualifiers from notes already on file, so
the corpus does not have to wait for every parish's next bulletin. It reads only
notes that state the pattern outright ("First Friday of the month", "October
through June", "Sept. 8 to May 30") and refuses anything with an exclusion in it
("Except 1st Saturday of the month"), where reading the ordinal would invert the
meaning, or a named season ("Summer Mass"), where the months the parish means
are not on the page. A season it reads keeps the matched phrase verbatim as its
`season_note`. It skips a row the extractor has already qualified. Notes it
cannot read are left exactly as they are.

## Environment Variables

- `GEMINI_API_KEY`: automatically picked up by the Gemini client.

### Web app (`apps/web`)

- `VITE_GEOAPIFY_API_KEY`: place search on the map (see `apps/web/.env.production`).
- `VITE_TALLY_FORM_ID`: Tally form ID for user feedback (e.g. `Me65rA` from `https://tally.so/r/Me65rA`). Set in `apps/web/.env.development` (dev) and `apps/web/.env.production` (build). When unset, feedback links are hidden.

## User feedback

Comments and corrections are collected with [Tally](https://tally.so). The form should include hidden fields named `page_path`, `full_url`, `church_slug`, and `church_name` (the app prefills these when someone opens the popup).

Review submissions in the Tally dashboard for your form → **Submissions**. Export CSV when batching data fixes.

## Database workflow

The database is rebuilt from flat files (`data/schema.sql`, CSVs, and JSONs):

```bash
pnpm db:create   # drop and recreate from schema + data files
pnpm db:drop     # delete the SQLite file
```

`schema.sql` is the source of truth for the database schema. Pipeline commands
(`fetch`, `process`) automatically rebuild the DB before running.

## Project layout

- `pyproject.toml` - project metadata and dependencies
- `package.json` and `pnpm-workspace.yaml` - JS workspace for frontend
- `uv.lock` - locked dependency versions
- `data/schema.sql` - SQLite schema (source of truth)
- `data/` - CSV, JSON data files and downloaded bulletin PDFs
- `data/event_history.json` - occurrences seen in past bulletins (weekly recurrence detection)
- `apps/web/` - React + TypeScript + Vite frontend
- `src/pdf_extract/extract_frontend_db.py` - builds the frontend SQLite snapshot
- `src/pdf_extract/` - Python CLI package
  - `__main__.py` - CLI entry point
  - `fetch.py` - bulletin fetching and provider link resolution
  - `process.py` - bulletin processing with Gemini AI
  - `schedule_extraction.py` - Gemini schedule extraction
  - `storage.py` - SQLite helpers and data paths
  - `db.py` - database creation from data files
  - `detect.py` - bulletin provider detection (Playwright)
  - `recurrence.py` - promotes repeatedly-dated events to weekly ones
  - `schedule_pattern.py` - weeks-of-month and partial-year season qualifiers
  - `pattern_backfill.py` - recovers those qualifiers from older events' notes
  - `timeparse.py` - shared parsing of the loose time/date strings the LLM returns
  - `geocode.py` - address geocoding (Nominatim)

## Dependencies

- [google-genai](https://github.com/googleapis/python-genai) - Gemini API client for PDF processing and structured JSON output.
- [playwright](https://playwright.dev/python/) - bulletin provider detection and link resolution.
- [pydantic](https://docs.pydantic.dev/) - data validation and Gemini response parsing.

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
