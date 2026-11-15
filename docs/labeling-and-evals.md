# Labeling bulletins and evaluating classifiers

Labels record by hand what each bulletin really says (the ground truth).
`pnpm eval` runs a classifier over the labeled bulletins and `pnpm eval:report`
scores its output against the labels.

## The labeler

A local tool for writing labels, to measure the classifiers against. It runs on localhost only, with no auth, and reads R2
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

The API validates every file (`src/pdf_extract/labeling/labels.py`, with the
vocabulary and entry checks in `src/pdf_extract/model.py`) and
rejects any slug or hash that would put it outside `data/labels`.

## Run a classifier over the labeled bulletins

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

## Score an eval run against the labels

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
(`src/pdf_extract/classifiers/pricing.py`); other models' runs are reported unpriced.
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
