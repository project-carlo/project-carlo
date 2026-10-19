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

The PDF shown is the stored compacted copy (the first 10 pages, or the parish's
limit in `data/bulletin_page_limits.csv`), so page
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
  - `weeks_of_month` (`first`…`fifth`, `last`; empty means every week), `exclude_weeks` (true when the listed weeks are the ones skipped: "every Sunday except the last" is `["last"]` excluded; an exclusion the remaining weeks can say, such as "every week except the first", is written as those weeks instead; files saved before this field existed lack it, which reads as false) and `season` (`{start_month, start_day, end_month, end_day}`, which may wrap past New Year). These apply to weekly rows only.
  - `origin`: `human`, `gemini` or `gemini-edited`
  - `optional`: `null` for a required event; `include` or `exclude` for one where it is a judgment call whether it belongs at all, naming the preferred answer (press `o` on a row to cycle). Files saved before this field existed lack it, which reads as `null`.

The API validates every file (`src/pdf_extract/labeling/labels.py`) and
rejects any slug or hash that would put it outside `data/labels`.

### Run a classifier over the labeled bulletins

```bash
pnpm eval --classifier gpt-6-luna --limit 2   # smoke test on two bulletins
pnpm eval --classifier gpt-6-luna             # every label marked done
pnpm eval --classifier gpt-6-luna --status done --status in_progress --parish all-saints-albany
pnpm eval --classifier gemini-flash-qualified
```

Any classifier in `src/pdf_extract/classifiers/__init__.py` can be run
(`gemini-flash`, `gemini-flash-qualified`, `gpt-6-luna`, `gpt-6-luna-nonstrict`,
...). Each bulletin is classified as of the day it was fetched, and results are
cached by classifier version (model, prompt, schema and settings), PDF and
church list, so re-running
an unchanged classifier makes no API calls (`--refresh` forces them). Output
goes to `data/runs/<classifier>/eval/<version>/`, which is committed (the rest of
`data/runs/`, including the result cache, stays gitignored). `<version>` is
the settings and a digest (`strict_reasoning-medium_detail-low-d469c0cc103e`),
and prediction files are named by the first 12 characters of the content hash,
so paths stay inside Windows' 260-character limit:

- `predictions/<parish_slug>/<content_hash[:12]>.json`: the classifier's events
  in the label's row shape, next to the full `content_hash`, `published_date`,
  `wrong_bulletin`, token usage and timing, so each file lines up with its label.
- `run.json`: cache hits, errors, skipped bulletins and summed token usage.

The classifiers built for scoring against the labels share one prompt and one
schema:

- the policy in `classifiers/schedule_policy.py` (`POLICY`): the production
  Gemini prompt extended with the rules the labels follow (weekly vs dated,
  chapels and parish adoration chapels, Communion Services, Benediction, Masses
  closed to the public, special occasions in a regular slot, positive weeks of
  the month only, stated clock times over times worked out from a Mass, only
  dates the bulletin prints or pins to one clear day such as "this Saturday"),
  sent first and unchanged so it can be
  served from the prompt cache, then the parish's churches and today's date,
  then the PDF;
- the schema in `classifiers/qualified_schedule.py`: the production schema plus
  `weeks_of_month`, `exclude_weeks` and `season` on weekly slots.

Editing either changes the version of every classifier that uses them.

- `gpt-6-luna` and `gpt-6-luna-nonstrict` (`classifiers/openai_responses.py`)
  run them on the OpenAI Responses API, the policy as an explicit prompt-cache
  breakpoint. They need `OPENAI_API_KEY`.
- `gemini-flash-qualified` (`classifiers/gemini_qualified.py`) runs them through
  the production Gemini call (same model, client, timeout, backoff and lenient
  parse as `gemini-flash`). It needs `GEMINI_API_KEY`, and takes only `--model`
  (another Gemini model, written under `data/runs/<model>-qualified/`).

The `gpt-6-luna` model settings can be changed per run:

```bash
pnpm eval --classifier gpt-6-luna --reasoning high --image-detail high
pnpm eval --classifier gpt-6-luna --pdf-as-images --image-detail original
pnpm eval --classifier gpt-6-luna --model gpt-6.1-sol --reasoning high
```

- `--model`: any OpenAI model with the Responses API, in place of `gpt-6-luna`
  (same prompt and schema). Its results go under `data/runs/<model>/`
  (`<model>-nonstrict/` with `gpt-6-luna-nonstrict`).

- `--reasoning`: `none`, `minimal`, `low`, `medium` (default), `high`, `xhigh`, `max`.
- `--image-detail`: `auto`, `low` (default), `high`, or `original`, which only
  page images take.
- `--pdf-as-images`: render every page to a 200 dpi JPEG (pypdfium2) and send
  those, each after a "Page N of M" line, in place of the PDF.

Each setting is part of the classifier version, so every combination is cached
and written under its own `eval/<version>/` directory. `pnpm eval:report` takes
the same flags to find that run.

### Score an eval run against the labels

```bash
pnpm eval:report --classifier gpt-6-luna                  # its current version
pnpm eval:report --classifier gpt-6-luna --pdf-as-images  # the run made with those flags
pnpm eval:report --classifier gpt-6-luna --model gpt-6.1-sol
pnpm eval:report --classifier gemini-flash-qualified
pnpm eval:report --classifier gpt-6-luna --version <ver>  # an older version's output
```

Writes `report.md` and `report.json` next to the predictions
(`src/pdf_extract/evals/report.py`). Labels marked done are scored (`--status
in_progress` adds those); skipped labels never are. Within each bulletin every
label event is paired with at most one prediction, in tiers tried strictest
first. Pairing is one-to-one except in `weekly_vs_dated`, where one weekly
prediction covers every dated label event of its slot (church, type, start,
cancelled and weekday, on a date its weeks of month and season include); recall
counts each of those label events and precision counts the prediction once.

| Tier | Agrees on | Counts as found |
|---|---|---|
| `exact` | church, type, weekly/dated, weekday or date, start, cancelled, end time, weeks of month, season | strict, core, loose, any_time |
| `core` | the same, but end time, weeks of month or season differ | core, loose, any_time |
| `weekly_vs_dated` | weekly on one side, dated on the other, same weekday, the date in the weekly side's weeks of month and season; church, type, start, cancelled agree | loose, any_time |
| `wrong_church` | everything in `core` but the church | never |
| `wrong_type` | everything in `core` but the event type | never |
| `wrong_time` | church, type, kind, weekday or date, cancelled; the start time differs | any_time |

The report gives precision, recall and F1 (pooled and per-bulletin average) at
the strict, core, loose and any_time levels; the wrong-church, wrong-type, missed and
spurious rates; the same broken down by event type and by weekly/dated; how
often end time, weeks of month, season and the presence of a note agree on the
pairs found at the loose level (a covering weekly prediction is one pair); per-bulletin perfect rate, published-date accuracy, wrong-bulletin
agreement and event-count error; token usage, its cost at standard-tier list
prices and timing; and every bulletin's differences, worst bulletin first.
Prices are kept for `gpt-6-luna` and `gemini-3-flash-preview` only
(`src/pdf_extract/evals/pricing.py`); other models' runs are reported unpriced.
Gemini predictions made before thinking tokens were recorded are flagged, as
their cost leaves out that billed output.

Optional label events are left out of all of those numbers. They are paired
after the required events, against the predictions still unpaired, in the tiers
that count as found at any_time and in the same order; in `weekly_vs_dated` a
weekly prediction already covering a slot's required dated events covers its
optional ones too. A dated `exclude` event is never paired with a weekly
prediction. A prediction paired only with optional events is neither found nor
spurious. The report's "Optional events" section counts how often the
classifier made the preferred choice: predicted an `include` event, or left out
an `exclude` one.

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

A parish's current bulletin is the one for the latest week, by the issue date
the extractor read off it (else the fetch date), and the most recently fetched
of that week's (`src/pdf_extract/bulletin_week.py`). So a second bulletin for a
week (a correction) replaces the first, and an old issue a site falls back to
is stored but never shown. The report lists the old issues, and flags a third
bulletin for one week for a person to look at. A parish is stale when its
newest bulletin is two weeks old, however recently the site served it.

`fetch` works on several parishes at once (`pnpm fetch -- --workers N`,
default 6, each with its own browser), but never has two workers fetching
from one site: all ParishesOnline parishes count as one site, as do all
eCatholic and all Discover Mass parishes, and any other site counts by its
domain (so `parishes.rcda.org` and `www.rcda.org` are one). A worker holds one
site at a time: its parish's while its browser finds the bulletin, then the
PDF's while it downloads it, and lets go before compacting the PDF, so the
next parish on a site starts then. Requests a page makes to other sites, and
redirects, are not held back; with only a few workers, no site gets more than
a few at once. A worker whose browser will not launch, or stops answering,
gets a new one; the fetch fails only when no worker can.

The run's status decides what happens next:

| Status | Exit code | Meaning |
| :-- | :-: | :-- |
| `passed` | 0 | Every publishing check passed; safe to publish. |
| `held` | 10 | A check failed: church count changed, total events moved more than 10%, less than 90% of weekly slots survived, a parish dropped to zero events, a parish or church was removed from the CSVs, or more than half of the parishes failed to fetch. A person decides. |
| `failed` | 1 | A stage crashed. |

A local run never publishes anything.

### Fetch-only parishes

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
move the total past the 10% check. `pnpm process -- --include-fetch-only`
processes fetch-only parishes anyway, e.g. to try a few with `--parish`.

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

Pushes to `main` deploy the site. Every pull request that touches the site gets
a preview: **Deploy Web** uploads each push to it and comments the link.

CI (`.github/workflows/ci.yml`) runs on pull requests in two jobs, `python`
(ruff, pytest) and `node` (web lint, type check and unit tests; the labeler's
checks and build). A job whose files the pull request doesn't touch skips its
checks and passes.

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
classifiers read; `data/bulletin_page_limits.csv` raises the limit for a parish whose
schedule runs past page 10, with the reason) with images downsampled to 150 dpi by Ghostscript, falling
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

- `fetch` skips a parish whose newest bulletin is already this weekend's, by
  the issue date the extractor read off it (and only when that bulletin was
  fetched within a few days of the date). Otherwise it downloads the bulletin,
  asking the server first whether the copy it has from that address is still
  current (`ETag` / `Last-Modified`), and keeps it only if it is new: not the
  same bytes as any of the parish's bulletins (`src/pdf_extract/duplicates.py`).
  A bulletin
  seen again is recorded on its row (`last_seen_at`), not stored twice. The
  address is never taken to mean the bulletin is unchanged: Discover Mass
  serves the same PDF from a new address each time, and some sites put each
  week's bulletin at the same one.
- `process` skips bulletins with `processed_at` already set, and serves
  bulletins it has extracted before (same PDF hash, same model) from the cache

### Checking the fetch stage

Most parishes publish through ParishesOnline, eCatholic or Discover Mass, but
the `other` provider has to find the bulletin on the parish's own website, and
every site is laid out differently. `pnpm fetch:check` runs the resolvers in the
browser without touching the database, downloads what each one picks, and
prints one row per parish (`ok`, `resolve_failed`, `download_failed`,
`not_pdf`, or `blocked` when Cloudflare challenged the browser instead).

#### How the `other` resolver reads a site

`src/pdf_extract/parish_sites/` reads a parish's own site in three stages:

1. **Locate** the bulletin page by following the homepage's "bulletin" links
   (`locate.py`).
2. **Collect** the PDFs it offers (`collectors.py`). Each collector handles one
   way a site offers them: `drive-folder`, `redirected-pdf` (the bulletin link
   is the PDF), `page-pdfs` (links, or addresses in the page's markup),
   `linked-issue-page` (an embedded flipbook or a publisher's listing) and
   `dated-post` (a weekly post that wraps the PDF). They run in that order
   until one finds a convincing set. `page-pdfs` also reads PDF addresses a
   viewer plugin keeps in base64 JSON (PDF Embedder's `pdfemb-data`, 3D
   FlipBook's `FB3D_CLIENT_DATA`), and takes Google Drive files, Google Docs
   (exported as PDF), Concrete CMS and DotNetNuke (`LinkClick.aspx`) downloads
   as PDFs. One more collector runs only when a recipe names it:
   `page-images`, for a parish that posts each issue as an image (a JPEG per
   weekend); `fetch` stores the image as a one-page PDF.
3. **Choose** this week's issue among them (`choose.py`), and say why:
   `current` (dated this week), or a fallback (`newest-recent`, `titled`,
   `first-listed`). `newest-recent` is the newest issue dated in the last 45
   days, taken when the first listed is plainly old, or when it is neither
   dated nor labelled "bulletin" and the page lists a dated series.

Each fetch result records how its bulletin was found ("page-pdfs on
https://…/bulletins: current"), and the run report lists any new bulletin the
site dated, but not this week.

A parish can pin the first two stages with a **recipe** in its `provider_id`:
a collector, a bulletin page, or both (`page-pdfs https://example.org/bulletins`;
a collector alone reads `website` as the bulletin page). A pinned parish skips
the homepage and runs only its collector, so it fails loudly when its site
changes rather than guessing, and no change made for another site can change
what it picks. `fetch:check` prints the recipe that reproduces each pick it
guessed; pin it once the pick is right.

When a site needs something new, add a collector rather than a branch inside
an existing one, and record the site (below).

#### Recorded sites

To keep a resolver change from fixing one site and breaking another, the pages
each resolver read on every parish's real site are recorded in
`tests/fixtures/fetch/<slug>.json.gz`, and `tests/test_fetch_replay.py` replays
them offline against the bulletin in `expected.json`, using each parish's
recipe in `data/parishes.csv` as it is now. After changing `fetch.py` or
`parish_sites/`, or pinning a recipe:

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
- `OPENAI_API_KEY`: for the OpenAI classifiers (`pnpm eval`, `pnpm extract`),
  the update-mode calls of `pnpm process` and `pnpm weekly:run`, and `pnpm seed ask|extract`.
- `CARLO_SEED_CALL_LIMIT`: external calls `pnpm seed ask|extract` may make per parish (default 4).
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

## Visitor analytics

The site records pageviews and a few actions (search picks, filters, bulletin
clicks) itself, in Cloudflare Workers Analytics Engine: no cookies, no third
party. `pnpm analytics` prints a report, and `/admin/analytics` shows the same
reports as a page you can open on a phone, behind Cloudflare Access. See
[docs/analytics.md](docs/analytics.md) for what's recorded, the tokens and
Access setup they need, and how to add an event.

## Believed schedules (update mode)

A parish can instead keep a **believed schedule**, changed only through
recorded changes: each new bulletin is shown to the model together with the
schedule we believe, the model proposes changes, and a code policy applies or
rejects each one. The design is
[docs/schedule-state-plan.md](docs/schedule-state-plan.md). A parish is in this
mode once it has a seed revision; every other parish is extracted from scratch
as above, and a weekly run handles both.

Update calls run on `gpt-6-luna` (OpenAI Responses API, high reasoning, the PDF
at low detail, strict decoding), set up like the eval module's `gpt-6-luna`
classifier, and need `OPENAI_API_KEY`. Their prompt
(`classifiers/schedule_update.py`) carries every rule of the eval policy
(`classifiers/schedule_policy.py`), worded for changes to the believed
schedule. `--model` on `pnpm process` only picks the Gemini model for
extract-mode parishes.

The update view also carries `reviewed_seed_context` from the parish's latest
imported, approved seed: excluded slots, answered questions, and monthly or
seasonal entries with their evidence. These explain intentional omissions and
unusual services; ordinary included slots are already in the live schedule.
The updater honors the resolved decision until new evidence addresses its
reason, and does not treat routine panel omissions as discontinuing a monthly
service. Draft summaries are left out. Context is stored and hashed with the
view, so editing a reviewed rationale changes the request/cache key without
re-seeding or replacing the current schedule.

The [October 18 replay report](data/update-evals/2026-10-18/report.md) records
the source cases, real model reruns, remaining ambiguity, and the guarded data
repair in migration 0008. Replays can be repeated with
`uv run python scripts/replay-schedule-updates.py --help`.

`pnpm schedule` looks at and hand-edits believed schedules:

```bash
pnpm schedule show --parish st-mary-albany          # the schedule as the model sees it
pnpm schedule apply --call 123 --actor you --note "checked the bulletin"   # a rejected call's proposals
pnpm schedule modify --parish st-mary-albany --entry-id 118 --entry '{...}' --actor you
pnpm schedule seed --parish st-mary-albany --file entries.json --actor you
```

## Seeding parishes

A parish's first seed (`data/seeds/<parish>.json`) is drafted by Claude Code agents from its
bulletins and approved by a person ([docs/seeding-plan.md](docs/seeding-plan.md)). The
`seed-parishes` skill runs batches through `seed-drafter` agents, which follow the
`draft-parish-seed` skill. Its [rules.md](.claude/skills/draft-parish-seed/rules.md) holds
every seeding decision (a slot no rule covers becomes a question for the reviewer), and
[file-format.md](.claude/skills/draft-parish-seed/file-format.md) holds the file format.
`pnpm seed --help` lists every command by phase.

```bash
pnpm seed pick                          # parishes to seed next, easiest first
pnpm seed start st-mary-albany          # start or resume a draft; prints where it starts from
pnpm seed finalize st-mary-albany       # the drafter's last step: bookkeeping, then check
pnpm seed check --all                   # the orchestrator's check; `status` lists every file
pnpm seed questions --answered          # reviewers' answers against the leanings, to find new rules
pnpm seed pick --labeled --eval try-1   # start a test run on the labeled parishes
pnpm seed score try-1                   # score its drafts against the labels
```

Reviewers answer the questions and approve in the labeler's **Seeds** mode (`pnpm label`).
Enter your reviewer name and click **Approve all ready (N)** in the Seeds queue to
approve every **Ready to approve** seed, regardless of the status filter. Each file
runs the usual approval checks; failures stay unapproved and appear with their problems.
Pipeline commands load newly approved files as `seed` revisions, which puts those parishes
in update mode (a deploy never loads them).

## Project layout

- `pyproject.toml` - project metadata and dependencies
- `package.json` and `pnpm-workspace.yaml` - JS workspace for frontend
- `uv.lock` - locked dependency versions
- `data/migrations/` - SQLite schema, as numbered migrations
- `data/parishes.csv`, `data/churches.csv` - curated parish and church lists
- `data/dioceses/` - parishes and churches of dioceses still being explored
- `data/` (untracked) - the local database, bulletin PDF cache and run outputs
- `docs/data-setup.md` - R2 bucket, API tokens, GitHub secrets, and running the published data
- `docs/analytics.md` - visitor analytics: what's recorded and how to query it
- `apps/web/` - React + TypeScript + Vite frontend
- `apps/labeler/` - the local bulletin labeling UI (never deployed)
- `data/labels/` - ground-truth labels, one JSON file per bulletin (committed)
- `data/seeds/` - parish seed files, drafted by an agent and approved in the labeler (committed); `data/seed-evals/` holds test runs on the labeled parishes
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
  - `schedule/` - believed schedules for update-mode parishes: the change log, the decision policy, the update stage, hand edits (`pnpm schedule`)
  - `seeding/` - seed files: their format and checks, the agent's tools (`pnpm seed`), loading approved ones, scoring test runs, the labeler's review
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
