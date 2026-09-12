# PRD: Monthly and Partial-Year Schedules

**Status:** Implemented on `claude/event-seasonal-monthly-ranges-sq2awv` (PR #22)
**Date:** 2026-09-12
**Product:** Project Carlo

## Summary

Parish bulletins routinely qualify a weekly time with more than weekday and clock: a slot that runs only part of the year, or only on certain weeks of the month. Project Carlo used to store those facts as unread free-text notes, so the map advertised them as if they happened every week, all year.

This work gives weekly events two structured qualifiers — **weeks of the month** and an **inclusive season range dated to the day** — and uses them everywhere a schedule is extracted, stored, filtered, or shown. After a one-time correction of existing rows, the extractor is the only writer; getting its prompt right is the performance-critical part of the change.

## Problem

A weekly slot is not always every week, all year.

- Holy Trinity (Webster) prints "Confessions Tuesdays 4:30, October through June."
- First Friday devotions are a Friday slot that comes round once a month.
- St. Theodore's prints a summer Mass schedule as "June 4 through September 10," not the whole of June and September.

Until these had fields of their own, the extractor could only put them in `note`. Nothing downstream reads `note` as a schedule rule. The map therefore offered the Webster confession slot in September, and listed First Friday devotions as if they happened every Friday.

A season bounded only to the month is still too coarse for what parishes actually print. "June 4 through September 10" is not June through September: the first week of June is out of season.

## Goals

1. Store month-of-year and week-of-month facts as data, not as unread notes.
2. Hide out-of-season weekly slots from the map and its filters. The map answers "where can I go this week."
3. Keep the full parish schedule on the church page, with the qualifier beside the time, so a reader can see why a slot they found on the church page is not on the map today.
4. Describe a season at the grain the bulletin stated it. "January to April" reads back as "January through April," not "January 1 through April 30." "June 4 through September 10" keeps the days.
5. Stop recurrence promotion from treating a monthly or out-of-season row as evidence of a standing weekly slot.
6. Treat the extraction prompt as a first-class control surface. Whether the model fills these fields correctly is what determines overall system performance; prompt wording must be reviewable, isolated, and iterable without touching the rest of the stack.

## Non-goals

- Modeling exclusions ("every Saturday except the first"). The fields cannot say that; those cases stay in `note` until a later design.
- A committed backfill tool or ongoing note-to-field pipeline. Existing rows can be corrected once (a local script is fine). After that, new bulletins fill the fields through extraction. Do not keep a `pattern:backfill` command in the product.
- Qualifiers on dated (one-off) events. A dated event already names the day it happens.
- A separate display-string column for the season (`season_note` was tried and dropped). A null day already encodes "this boundary was stated as a whole month."
- Changing how language, location, benediction, or other special context is stored. That remains `note`, beside the qualifier.

## Users and jobs

| Who | Job | What this changes |
| --- | --- | --- |
| Someone looking for Mass, Confession, or Adoration this week | Find a church that is actually offering it now | Map and filters hide out-of-season slots |
| Someone looking up a specific parish | See that parish's whole standing schedule | Church page lists every weekly slot, with when it runs |
| The person tuning extraction | Get the model to fill these fields correctly, every week | Prompt and schema descriptions are the lever; they must be easy to read, change, and judge |
| Recurrence promotion | Decide whether a dated sighting is a weekly slot | Monthly and out-of-season rows are not counted as weekly evidence |

## Requirements

### Data model

A weekly event may carry:

| Field | Meaning | Empty / null means |
| --- | --- | --- |
| `weeks_of_month` | Which occurrences of `day_of_week` within the month the slot falls on. Canonical ordinals: `first`, `second`, `third`, `fourth`, `fifth`, `last`. Stored as a comma-joined string (`first`, `first,third`, `last`). | Every week |
| `season_start_month` / `season_end_month` | Inclusive 1–12 range of the year the slot runs. A start later in the calendar than the end wraps the new year (October through June). Both must be set, or neither. | All year |
| `season_start_day` / `season_end_day` | Inclusive day of that month. Set only when the bulletin dated the boundary. An impossible day (February 30) is dropped, leaving the whole-month reading. February is given 29 days: a season boundary is a recurring calendar position, not a date in one year. | That end sits at the edge of its month (1st, or last day of the month) |

Rules:

- `last` is distinct from `fourth`. A five-Friday month has a fourth Friday and a different last one; a bulletin that says "last" means the later date.
- A half-stated season ("runs from October," no end month) is no season at all. Do not invent a December cutoff.
- Dated events cannot carry these fields.
- `note` is not displaced. Special context stays in `note` and renders beside the qualifier.

Python (`src/pdf_extract/schedule_pattern.py`) is the single place that decides what the qualifiers mean on the way into the database. TypeScript (`apps/web/src/lib/schedulePattern.ts`) mirrors the same rules in the browser. Both are pure functions, so the SPA and the prerenderer agree.

### Extraction prompt (the quality lever)

Going forward, every weekly slot gets these fields from the model. Downstream display and filtering can only be as correct as this step. Prompt changes therefore need tighter control than the rest of this work.

The control surface is two places that the model actually reads:

1. **The events system prompt** — the instructions that say when a weekly slot is monthly or seasonal, how to fill the fields, and what not to put in `note`.
2. **The extraction schema field descriptions** — `weeks_of_month`, the four season fields, and `note` on `WeeklySlot`. These travel with the structured-output schema and steer the model as much as the prompt does.

Requirements for how those change:

- **Isolated and reviewable.** Qualifier policy lives in its own prompt block (and matching field descriptions), not three bullets mixed into the existing wall of instructions. A reviewer should be able to read the qualifier rules without reading the rest of the extractor.
- **Iterable without a stack change.** Wording, examples, and named-season mappings can be revised without touching schema columns, frontend filtering, or display copy. A prompt-only change still bumps the extraction schema version so cached results are not reused.
- **Judged, not assumed.** A prompt change is accepted only when it is checked against a small set of real bulletins that cover the hard cases: First Friday, 1st-and-3rd, October-through-June wrapping the new year, a day-accurate range ("June 4 through September 10"), a whole-month range that must not invent days, a named season ("summer Mass"), an exclusion that names off months, and a note that must stay a note (language, benediction). Wrong fills, invented days, and restated notes are regressions.
- **Policy is explicit.** The prompt, not implicit model judgment, decides:
  - A monthly or seasonal slot still belongs in `weekly_schedule`.
  - Empty `weeks_of_month` means every week; both season months or neither.
  - Days are filled only when the bulletin dated the boundary. Do not invent the 1st or the 30th.
  - When the bulletin names a season instead of months, which months that season means (today: summer as June–August, school year as September–June). This mapping is prompt text and is expected to be tuned.
  - An exclusion that names the off months is read as the complementary season (does not run in July or August → September through June).
  - `note` must not restate what the qualifier fields already carry.

The current branch already added the fields and some of this wording. That wording is a first draft of the policy, not the finished prompt.

### One-time corpus correction

Existing `events.json` rows still have the old notes. Correct them once so the shipped data matches the new fields, then stop.

A local script is fine if it helps find and rewrite the obvious cases. Do not commit the script, a `pattern:backfill` command, or any ongoing note-parsing path. After the corrected rows are reviewed and look right, new bulletins go through extraction only.

### Map and filters

The map answers "where can I go this week."

- Hide a weekly slot that is out of season today.
- Keep monthly slots: they do run at this time of year. The pin popup carries a line saying which week of the month.
- Do not collapse a first-Friday devotion with a Friday slot that runs every week. Dedup keys include the pattern, not just weekday and start time.

### Church page

Someone looking up a parish wants its whole schedule.

- List every weekly slot, in or out of season.
- Put the derived qualifier beside the time: "Tuesdays 4:30 p.m. — October through June", "First Friday of the month", "June 4 through September 10".
- A slot that cannot resolve to any occurrence in the next seven years is dropped. The lookahead exists because a last-Thursday Holy Hour that only runs June 4–20 offers very few candidate dates.

Display copy is derived from the fields at the grain they were filled in at. Whole-month seasons stay in months; dated seasons keep the days.

### Recurrence detection

Do not credit these rows as evidence of a standing weekly slot:

- A monthly row credited to its bulletin's week invents sightings on weeks it never happens.
- A seasonal row credited out of season does the same.

A few of those in a row are exactly what promotion reads as a weekly slot.

## Display copy

| Stored pattern | Shown as |
| --- | --- |
| `weeks_of_month: ["first"]`, Friday | First Friday of the month |
| `weeks_of_month: ["second", "fourth"]`, Saturday | Second and fourth Saturdays of the month |
| `season: October–June`, no days | October through June |
| `season: June 4–September 10` | June 4 through September 10 |
| `season: January–April`, no days | January through April |
| both, e.g. first Friday, October–June | First Friday of the month, October through June |
| plain weekly | nothing extra |

## Success criteria

- Out-of-season weekly slots do not appear on the map or in map filters.
- The church page still lists them, with a qualifier that matches the bulletin's grain.
- First Friday (and similar) slots are not listed as every-week Fridays, and are not deduped against every-week Fridays.
- Recurrence promotion does not invent weekly slots from monthly or out-of-season rows.
- Qualifier prompt text and schema field descriptions can be reviewed and changed on their own, and a wording-only change invalidates cached extractions.
- Prompt changes are checked against the hard-case bulletin set before they ship.
- The one-time `events.json` corrections look right on review; no backfill tool ships with the product.
- Python and TypeScript agree on whether a date matches a pattern, and on how the pattern is described.
- Tests cover normalization, date matching, display copy, snapshot columns, map filtering, and next-occurrence search.

## Known corpus examples

- Holy Trinity, Webster: Confessions Tuesdays 4:30, October through June.
- St. Theodore's: summer Masses, June 4 through September 10.
- First Friday (and similar ordinal) devotions across the corpus.

## Open questions

These are not decided by the current branch; they are the natural next product questions.

1. Should the map hide a monthly slot on weeks it does not fall on (e.g. hide First Friday on the 3rd of the month), or is "this time of year" enough?
2. What named-season mapping should the prompt actually teach (summer → June–August, school year → September–June, and any others), and against which bulletins is that mapping judged?
3. Is there a later need for exclusions ("every Saturday except the first"), or is leaving those as notes acceptable indefinitely?
4. When a church has both a school-year slot and a summer slot for the same weekday and time, is the current listing (two rows, each with its season) the right church-page shape?
5. Where should the qualifier prompt block live so it stays easy to edit — a dedicated string next to the schema, a separate prompt file, or something else — and what is the smallest eval set that makes a prompt tweak safe to land?
