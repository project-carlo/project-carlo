# Project Carlo: showing where each time came from

Status: proposal, for discussion. Nothing here is built.

The church page says "Found on bulletin page 3" and links the current bulletin.
That is the only provenance a visitor sees today. The copy audit names it as
"a strong trust feature that few listing sites have", and also says the site
"never says how fresh the times are". The believed-schedule design
([schedule-state-plan.md](schedule-state-plan.md)) already stores much more
than the site shows: how each slot entered the schedule, every bulletin that
has printed it since, every change and the reason for it, and for seeded
parishes, the words each bulletin used and the person who approved the seed
([seeding-plan.md](seeding-plan.md)).

This plan proposes showing that history for each time slot. It stays out of
the way by default, with a short line or marker at most, and opens into a
full history in a popover (or a sheet on mobile). It starts from the data the
database and seed files already hold, then lists schema changes that would
make the history richer.

- [What a visitor would see](#what-a-visitor-would-see)
- [What the data supports today](#what-the-data-supports-today)
- [Gaps, and schema changes that close them](#gaps-and-schema-changes-that-close-them)
- [Getting it to the browser](#getting-it-to-the-browser)
- [Phases](#phases)
- [Decisions for you](#decisions-for-you)

## What a visitor would see

### Three levels of detail

1. **Nothing extra (the default).** The schedule looks as it does now, with
   one change: each time can be clicked or tapped. A dotted underline or a
   small mark on hover shows this, and the page shows no new text.
2. **A status marker, only when something is worth knowing.** A small glyph or
   italic note beside the time, used sparingly:
   - *Changed Oct 11* (a modify in the last 4 weeks)
   - *New Oct 11* (an add in the last 4 weeks, after the seed)
   - *Not in the last 2 bulletins* (still believed, but no sighting; the
     report already computes this flag)

   A slot that every recent bulletin printed gets no marker. That is the
   normal case, and marking it would add noise.
3. **The full history,** in a popover on desktop and a bottom sheet on mobile
   (both are already in `components/ui`). Opened from the time itself.

### The popover

A summary line, then a timeline with the newest entry first. Long runs of
unchanged weeks are folded into one line that can be expanded.

```
Saturday 4:00 p.m. Vigil Mass
Printed in every bulletin since we began tracking St. Mary's (7 of 7).

  Oct 11 bulletin · page 2                                   printed
  Sep 6 – Oct 4 · 5 bulletins · page 2                       printed   ▸
  Sep 6   Added to our schedule from the Sep 6 bulletin, page 2:
          “Sat 4:00 PM Vigil”
          Reviewed by a person before publishing.
  ──────── before tracking ────────
  Jun 14 – Aug 30 · 11 bulletins                    read by our earlier reader

  [Open this week’s bulletin at page 2]   [Suggest an edit]
```

A slot that has changed shows each change as a step, with the old value
struck through and the bulletin's reason:

```
Saturday 4:30 p.m. Vigil Mass
Changed Oct 11 (was 5:00 p.m.).

  Oct 11 bulletin · page 2       changed 5:00 → 4:30 p.m.
                                 “Beginning October 11, the Saturday Vigil
                                  will be celebrated at 4:30 PM.”
  Sep 6 – Oct 4 · 5 bulletins    printed as 5:00 p.m.                     ▸
  Sep 6   Added from the Sep 6 bulletin (5:00 p.m.), reviewed by a person.
```

And one that has gone quiet:

```
Wednesday 7:00 p.m. Confession
Last printed Sep 27. Not in the Oct 4 or Oct 11 bulletins.
We still list it because no bulletin has said it ended. Check with the parish.
```

### Wording

- Times in the history use the site's own style (`4:00 p.m.`). Quotes from
  bulletins are reproduced exactly as printed, in quotation marks.
- Bulletins are named by their week, as `BulletinLabel` already does
  ("Oct 11 bulletin"), never by fetch time.
- "Our automated reader" for the model, "a person" for a reviewer or a hand
  edit. Naming models, policies or reviewers' handles is for the internal view
  (below).
- Avoid "verified". A bulletin printing a time shows the parish still
  advertises it, not that it happens. "Printed in" is accurate.

### A church-level history

Besides the per-slot popover, a "Schedule changes" link (near "Latest parish
bulletin") opens the parish's changes in order, newest first:

```
Oct 11   Saturday Vigil Mass moves from 5:00 to 4:30 p.m.        page 2
Oct 11   Confession on Saturday now ends at 4:00 p.m. (was 3:45)  page 2
Sep 27   No 8:00 a.m. Mass on Monday, October 12 (Columbus Day)   page 3
Sep 6    Schedule first recorded, from the Sep 6 bulletin. Reviewed by a person.
```

This is the parish's `schedule_change` log, read one revision at a time. A
visitor who sees one marker can find out what else changed. It could be a
section on the church page or its own route (`/church/<slug>/history`).

### An internal view

The same popover with `?debug` (or in the labeler) adds what only a
maintainer needs: entry and revision ids, the `llm_call` (model, status,
cost), each proposal's `decision` and `reason`, and the **rejected** proposals
that touched the slot ("Oct 18: a bulletin proposed deleting this; rejected as
`stale_bulletin`"). Visitors never see rejected proposals. Maintainers find
them useful when a visitor reports a wrong time.

### Extract-mode parishes

Parishes not yet seeded have no tracked history: their times are whatever the
latest bulletin produced. Their popover says so plainly: "Read from the Oct 11
bulletin, page 2, by our automated reader. We aren't tracking this parish's
schedule week to week yet." This also shows the difference between seeded and
unseeded parishes, which the site doesn't show today.

## What the data supports today

Everything in the mock-ups above except the bulletin quotes after the seed,
and the "before tracking" line, can be built from tables that exist now.

| What to show | Where it comes from |
| :-- | :-- |
| When the slot entered the schedule, and how | The `add` row in `schedule_change` at the start of the slot's chain, and its `schedule_revision` (`source_kind`, `as_of` for a seed, `actor`, `created_at`) |
| The bulletin that added or changed it | `schedule_revision.llm_call_id` → `llm_call.bulletin_id` → `bulletin.published_date` / `bulletin_week` |
| Each change, with before and after | The `modify` rows in the chain, `before_entry_id` → `after_entry_id`; diff the two `schedule_entry` rows field by field |
| Why it changed | `proposed_change.rationale` and `page_number`, through `schedule_change.proposed_change_id` |
| Every bulletin that printed it, with page | `entry_sighting` for each entry in the chain (sightings of an earlier entry are "printed as 5:00 p.m.") |
| Bulletins that didn't print it | Successful, non-stale, non-wrong calls with `base_revision >= since_revision` and no sighting: the report's "not printed" flag (`schedule/report.py`) |
| Seed evidence: quotes, pages, reviewer | The approved seed file's slot: `sources[].said`, `page`, `bulletin`, `rationale`, `answer`, plus the file's `reviewer` and `approved_at` |
| Hand edits | `human` revisions: `actor`, `note` |
| Cancellations of one date | `specific_date` entries with `cancelled = 1`, matched to their weekly slot as the snapshot builder already does (`cancels_event_id`) |

**A slot's chain.** Entries are immutable and a modify swaps one entry for
another, so a slot has no single id. Its history is found by walking
`schedule_change` backwards from the live entry: find the row whose
`after_entry_id` is this entry, take its `before_entry_id`, and repeat until
reaching the `add`. That is a recursive CTE over a small table. Note that a
modify may move the start time or weekday, so the chain must be followed
through the log, not grouped by `identity_key`.

**Seed slot ↔ entry.** The database doesn't record which seed-file slot
produced which entry. They can be matched at build time by recomputing the
slot's entry hash with the loader's own conversion (`schedule/entries.py`)
and finding it in the seed revision's `add` rows. That needs the seed file
as it was when loaded, not as it is now (see gap 2).

**Before tracking.** Seed files already hold `history` sources for each
slot: the older bulletins in which extract mode found a matching event. The
earlier reader saw this time in N bulletins since some date. Shown dimmed and
labelled as the earlier reader's, it fills in the timeline for a parish
seeded last week.

## Gaps, and schema changes that close them

In order of value for the cost.

### 1. Quotes for every sighting (high value, small change)

Seed sources carry the bulletin's own words (`said`). Update calls don't: the
`seen` list is just `entry_id` and `page_number`. A short quote per sighting
is the most convincing thing the popover can show ("“Sat 4:00 PM Vigil”, page
2"), and it makes a wrong reading easy to spot.

- Add `quote` to `seen[]` and to each change in the response schema ("the
  words the bulletin prints for this entry, verbatim, at most ~80
  characters").
- `ALTER TABLE entry_sighting ADD COLUMN quote TEXT;` and write it there.
- Cost: a few output tokens per entry per call. This changes the classifier
  version, so request keys change and cached calls aren't reused. Land it
  between weekly runs.
- The seed loader writes the slot's `said` as the quote of the sightings it
  writes.

### 2. Keep the seed's evidence in the database (medium value, small change)

Today the loader reads an approved seed file, writes entries and one set of
sightings, and records only the file's digest in the revision's `note`. The
quotes, the older bulletins it cites, the rationale and the reviewer's answer
stay in git, and a later edit to the file changes them.

```sql
-- The approved seed file each seed revision was loaded from, as loaded.
CREATE TABLE seed_file (
    parish_id INTEGER NOT NULL,
    revision INTEGER NOT NULL,
    digest TEXT NOT NULL,
    json TEXT NOT NULL,
    PRIMARY KEY (parish_id, revision),
    FOREIGN KEY (parish_id, revision) REFERENCES schedule_revision(parish_id, revision)
        ON DELETE CASCADE
);
```

Also write a `seed_slot` reference on each of the seed revision's change rows
(`ALTER TABLE schedule_change ADD COLUMN seed_slot TEXT;`, holding the slot id
`s3`). The build then needs no hash matching to find the slot.

### 3. Sightings for every bulletin the seed read (medium value, no schema change)

The loader writes sightings only for the newest bulletin. A slot's `agent`
sources cite each bulletin the drafter read, with its page. Writing a
sighting for each (they are all in the database by content hash) lets the
timeline start with "printed in the 3 bulletins we read to seed this
parish", not just one. `entry_sighting.llm_call_id` is already null for seed
sightings.

### 4. Where a sighting came from (low cost, needed if 3 or 5 is done)

Once sightings come from seeds, from calls, and possibly from extract history,
the timeline needs to say which:

```sql
ALTER TABLE entry_sighting ADD COLUMN source TEXT NOT NULL DEFAULT 'call'
    CHECK (source IN ('call', 'seed', 'extract'));
```

### 5. Pre-seed history as sightings (optional)

Instead of reading `history` sources out of seed files, the loader could
match each seeded entry against the parish's older extract-mode `event` rows
(`seeding/coverage.py` already does this matching) and write `extract`
sightings. Then "before tracking" is ordinary data and parishes with long
extract histories get it for free. Extract mode was noisy, which is why the
timeline should label these and dim them.

### 6. A stable lineage id per slot (optional, convenience)

Walking the chain works, but a stored lineage id makes it a plain lookup and
gives each slot an id that survives modifies. That id is useful for deep
links (`/church/st-marys#slot-41`), for analytics on which histories get
opened, and for feedback ("Suggest an edit" for this slot).

```sql
ALTER TABLE schedule_change ADD COLUMN lineage_id INTEGER;  -- id of the add row that began the slot
ALTER TABLE current_schedule ADD COLUMN lineage_id INTEGER;
```

Apply sets it: an add uses its own row id, and a modify copies it from the
row that added its `before_entry_id`. `schedule rebuild` must reproduce it
from the log, so it stays derived data. Deleting a slot and adding it back
starts a new lineage. That is correct: the bulletin dropped it and later
printed it again.

### Not proposed

- **`valid_from` / effective dates.** The schedule-state plan leaves them out.
  For "announced but not yet in effect" changes, the history can show the
  rationale of the proposal that eventually applied it, which usually quotes
  the announcement.
- **Bounding boxes or crops of the bulletin.** Showing the printed line as an
  image would be very convincing, but model-reported boxes are unreliable,
  and it raises the question of republishing bulletin content. Quotes come
  first.

## Getting it to the browser

The site loads one gzipped snapshot for every page. The full history must not
go into it: it would grow with every week, and the scaling plan is already
working to keep that file small.

**Two small snapshot columns for the markers.** They let level 2 render with
no extra request. They go in `ADDED_COLUMNS`, so no version bump is needed:

- `last_seen_week`: the week of the newest bulletin that printed the entry,
  or null (coded column; few distinct values). The app compares it with the
  church's `bulletin_week` to say "not in the last N bulletins".
- `changed_week`: the week of the slot's last add or modify after the seed,
  or null. That gives "Changed Oct 11" or "New Oct 11".

**History files, fetched when a popover first opens.** `extract_frontend_db`
(or a sibling step) writes the full history per parish, keyed by the same
negated entry ids the snapshot uses. Both are built from the same database
in the same run, so the ids match. Stamp both with the build's id. If a cached
snapshot and a newer history file disagree, look up by (church, type, day,
time) instead, or show only the summary.

Where the files live depends on scale:

- **Now (~140 seeded parishes, ~540 churches):** one static file per parish
  in `public/history/<parish>.json`. Small, cached, and free to serve.
- **Nationally:** per-parish files would push the Workers Free limit of
  20,000 static files (the scaling plan's concern). Either shard them like the
  regional snapshot shards (one file per region or diocese), or serve them
  from R2 through a Worker route. The format doesn't change.

A rough size: a slot with 20 sightings, a couple of changes and its seed
quotes is about 1–2 KB of JSON before gzip. A parish with 30 slots is under
50 KB, and much less gzipped.

**Prerendering.** Church pages are prerendered for SEO. The markers can be
prerendered as text (from the snapshot columns); the popover stays
client-only.

## Phases

1. **Read-only, from today's data.** A `provenance.py` builder that walks
   chains, sightings, misses and seed files (from git) and writes the history
   files; `pnpm schedule history <parish>` prints the same thing in the
   terminal. The same output is useful when a visitor reports a wrong time.
   Then the popover on the church page, behind a flag. No schema change.
2. **Markers.** The two snapshot columns, and the markers, after reviewing
   their frequency on real data (if most slots get a marker, the threshold is
   wrong).
3. **Richer evidence.** Gaps 1–4: quotes on sightings, the seed file in the
   database, seed sightings for every read bulletin, and the sighting's
   source. One migration, a classifier version bump, and a loader change.
   Once loaded, re-loading the existing approved seeds isn't needed: the
   build can backfill `seed_file` from git for revisions already loaded,
   matching each one by the digest in its `note`.
4. **The church-level change log**, and pre-seed history (gap 5) if the
   popovers are getting used.
5. **Lineage ids** (gap 6), when deep links or per-slot feedback are wanted.

Measure along the way: popover opens per church page view (an analytics
event, as `data-track` does today), and whether "Suggest an edit" reports
drop or become more specific.

## Decisions for you

1. **Who is it for?** Visitors (trust), maintainers (debugging), or both. The
   plan assumes both, with rejected proposals and model details kept to the
   internal view.
2. **Linking old bulletins.** The site links only the current bulletin,
   because parish sites reuse a URL for each new issue. The pipeline has every
   past PDF in R2 (`bulletins/<parish>/<hash>.pdf`). Serving those would make
   each timeline row clickable, but it means republishing parish bulletins.
   The plan assumes no for now: old bulletins are shown by date and page, with
   quotes.
3. **Naming reviewers.** Seed files record a reviewer's handle. The plan says
   "reviewed by a person" publicly.
4. **Markers or no markers.** Level 2 changes the look of the schedule; levels
   1 and 3 don't. They can ship separately.
5. **How far back.** All tracked history, or a window (the last 6 months) with
   "earlier history" folded away. All history is cheap at current scale.
