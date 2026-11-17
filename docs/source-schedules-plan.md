# Project Carlo: schedules for parishes with no bulletin

Status: implemented (November 2026): the capability, with no parish moved over
yet. Where the code had to decide something this plan left open, or departs
from it, see [Implementation decisions](#implementation-decisions).

Some parishes publish no bulletin the pipeline can read, but post their Mass,
Confession and Adoration times on their own website or Facebook page. This plan
lets such a parish go live with a **source schedule**: a seed drafted from that
page instead of from bulletins, kept as it is until someone checks the page
again. The weekly run never updates it.

This plan builds the capability only. It doesn't move any existing record over,
decide which parishes qualify or set how source seeds are reviewed (see
[Out of scope](#out-of-scope)).

## Decisions

- **Sources are the parish's own website or its own Facebook page.** Not the
  diocese's directory, Google, MassTimes or any other listing. Whether to allow
  more depends on how many parishes these two cover.
- **Only parishes with no bulletin.** A parish whose bulletin is published but
  can't be fetched yet (`unsupported`, or a `fetch_gap`) never uses this. It
  waits for a collector.
- **No freshness cutoff in code.** The drafting agent judges whether a page is
  current, and the seed records why it thinks so. A schedule past its recheck
  date stays on the site, and the weekly report lists it.
- **These churches look the same as the rest** on the map, in lists and in
  search. Only the church page's source line and the wording that names a
  bulletin differ.
- **One main source link per parish.** The seed file keeps every page it
  quotes, and the site links the main one.
- **Refreshing is re-seeding.** A later approved version of the seed file, with
  a later `as_of`, is loaded as a new `seed` revision, as the loader already
  allows ([seeding-plan.md](seeding-plan.md#loading-seeds)). The future
  quarterly agent writes that version, so this plan needs no update path of its
  own.

## How it fits the current model

The schedule store needs no change. A believed schedule is a series of
revisions, and a `seed` revision is entries plus an `as_of` time. Nothing
requires a bulletin behind it. The parts that assume a bulletin are the
records' provider values and promotion, the seed tooling and checks, the
snapshot's church columns and the site's wording.

## The parish row

A new `bulletin_provider` value, `website_schedule` (it covers Facebook too):

- **Records** (`dioceses/records.py`): a valid provider. Its `website` is the
  main source page. It needs no `publication` ids and can't have a
  `fetch_gap`. `validate` warns about a `website_schedule` row with no approved
  seed file, since it would be on the site with nothing to show.
- **Promotion:** `website_schedule` rows are promoted like any other. Settled
  policy 4 in [data/dioceses/README.md](../data/dioceses/README.md) becomes:
  "the site shows only places it can give a schedule for, from a bulletin or a
  source schedule". `no_bulletin` and `unsupported` stay off the site.
- **Fetch and process skip it.** `fetch._resolve_fetch_source` already returns
  nothing for a provider it doesn't know, which keeps such a parish out of the
  stale-bulletin report. A test should pin that. `fetch:check` refuses it, as it
  refuses `no_bulletin`: there is nothing to fetch. `process` finds no bulletins
  after the seed's `as_of` and makes no call.
- **When a bulletin turns up**, set the real provider. The weekly run then
  updates the schedule from bulletins fetched after the source seed's `as_of`,
  the same way it carries on from a bulletin seed. Whether to re-seed from the
  first bulletin instead is left to the person who switches it.

## Keeping the source

A bulletin is stored as a PDF, so a reviewer can always see what the agent
read. A web page or Facebook post can change or disappear, so the drafting
tools store what was read:

- `pnpm seed capture <parish> [path or address]` renders the page and keeps its
  visible text and a full-page screenshot. The text is committed beside the
  seeds, `data/seeds/captures/<parish>/<sha256 of the text>.txt`, so its quotes
  can be checked anywhere and a reviewer reads it in the pull request. The
  screenshot (PNG) goes in the blob store, `captures/<parish>/<sha256>.png`,
  with tiles that fit Read in `data/seed-work/<parish>/captures/`. It prints the
  capture's id, its text and the tiles' paths.
- It uses the parish-site-access skill's headed Chrome, which gets past most
  Cloudflare checks and renders JavaScript sites. Facebook pages need that
  browser too, and may show only a login wall: the capture then reports it
  rather than storing an empty page.
- Captures are named by content, like bulletins, so capturing an unchanged page
  again adds nothing, and the future updater can see whether a page changed
  since the last seed.

## The seed file

A source seed is a seed file (`data/seeds/<parish>.json`) with a `kind`:

| Field | Bulletin seed (today) | Source seed |
| :-- | :-- | :-- |
| `kind` | `bulletin` (the default, so existing files don't change) | `source` |
| `bulletins` | the parish's bulletins, each marked `read` | empty |
| `captures` | absent | each page read: `url`, `final_url`, `platform` (`website` or `facebook`), `captured_at`, the text's hash (`content_hash`) and the screenshot's, and `primary` on exactly one |
| `as_of` | the newest read bulletin's fetch time | the newest capture's time |
| slot `page` | where the newest bulletin prints it | always null |
| slot sources | `agent`, `history`, `website`, call ids | `website` or `facebook`, each naming its capture and quoting it in `said` |
| `recheck_after` | absent | a date, three months after `as_of` by default |

A source seed also records, once for the file, why the agent believes the
schedule is current (`current_because`). Clues include a dated post, the
current pastor's name, this year's dates or a seasonal heading. This replaces
R6's per-slot `schedule_check`, which compares a website with a bulletin.

**Checks** (`seeding/checks.py`), for `kind: source`:

- No bulletins and no calls. Every source cites a capture in the file, and its
  `said` appears in that capture's committed text (case, whitespace and
  typographic quotes and dashes folded), so a quote can't be made up. A quote
  read from the screenshot is marked `from_image` and can't be matched.
- The committed text is there, with the hash the file gives. The parish is
  `website_schedule`. Website captures are on the parish's own website (same
  registrable domain as its `website`). One is primary, and `as_of` is the
  newest capture's time.
- `current_because` and `recheck_after` (after `as_of`) are present.
- The checks that don't depend on bulletins still apply: entry validity,
  churches, duplicate slots, dated entries on or after `as_of`'s date, and
  status.
- R1, R2 and the bulletin exceptions (R12/R19, R36) don't apply.

**Commands:** `seed start` starts a source seed for a `website_schedule`
parish, with no bulletins, and its brief says so. `seed capture` adds to
`captures`, `seed capture-text` prints one, and `seed current` sets
`current_because` (and `--recheck-after`). The slot-writing commands take
`cap <capture>: said` (or `cap primary`, and `cap <capture> image: said`) as a
source. `extract` and `ask` refuse a source seed, since they read PDFs.
`finalize` adds no history sources, because such a parish has no extract-mode
history.

## Drafting rules

The drafting skill gets a source section in `rules.md`, R42–R45:

- Read the parish's site for its schedule pages (Mass times, Confession,
  Adoration) and its Facebook page for recent schedule posts. Capture every
  page a slot relies on.
- Judge currency and record it in `current_because`. Watch for an old pastor,
  last year's dates, a "summer schedule" out of season, and a website that
  disagrees with recent Facebook posts. A real conflict between sources becomes
  a question.
- A pinned or recent Facebook post that states a regular schedule can settle
  slots. A single event post settles only that dated entry.
- Expect dated one-off events and holy days to be missing. That is normal, not
  something to ask about. A dated entry goes in only when a capture states it
  and it falls on or after `as_of`.

## Loading

`seeding/loader.py` loads an approved source seed as it does a bulletin seed:
one `seed` revision, reloaded only for a new digest with a later `as_of`. It
writes no sightings. It records the primary capture's platform and URL with
the revision, in a migration (0014) that adds `schedule_source` and
`schedule_source_url` to `schedule_revision` (null for every other revision;
`source_kind` was taken). The capture time is the revision's `as_of`. The
snapshot reads the parish's latest seed revision for these.

## Snapshot

Columns added to `churches`, listed in `ADDED_COLUMNS` (null in older
snapshots, read as a bulletin church), so `SNAPSHOT_VERSION` stays 3:

- `schedule_source`: null for a bulletin parish, else `website` or `facebook`.
- `source_url`: the primary capture's URL.
- `checked_on`: the date of the seed's `as_of`.

`bulletin_url` and `bulletin_week` stay null for these churches. The churches'
query takes them from the parish's latest seed revision when the parish is
`website_schedule`.

## The website

- **Source line** (`ChurchPageContent.tsx`): in place of "Bulletin for the
  week of…", show "From the parish website" or "From the parish's Facebook
  page", then "· checked November 16, 2026", linking to `source_url`. It is
  marked `data-lastmod-exempt` like the bulletin line, though it changes only
  when the parish is re-seeded.
- **Page links** need nothing: "Found on bulletin page N" already hides when an
  entry has no page.
- **Wording that names a bulletin** gets a variant for these churches:
  - the AI disclaimer in `copy.ts` ("Times are read from each parish's
    bulletin…");
  - the church description in `seo.ts` ("…from the parish's weekly bulletin");
  - the empty-schedule note ("The parish bulletin may not include them…").
- **Site-wide wording:** `SOURCE_PHRASE` ("from each parish's weekly bulletin")
  becomes "from each parish's bulletin or website".
- **JSON-LD and sitemap dates** follow the page's content hash as now, so they
  move only when a re-seed changes the page.
- `packages/core` (`types.ts`, `snapshot.ts`) reads the new columns. The mobile
  app shows no bulletin links yet and needs no change.

## Labeler

The Seeds view shows a source seed's captures where it shows bulletin tabs:
the screenshot, the stored text and a link to the live page. Clicking a
source opens its capture. A new route,
`GET /api/seeds/<parish>/captures/<hash>/<text|png>`, serves the committed text
and the screenshot from the blob store, only for a capture the parish's seed
file lists. The rest of the review is the same.

## Weekly run and report

- The report's Seeds section names a loaded source seed as one.
- A new **Source schedules due** section lists `website_schedule` parishes
  whose latest seed's `recheck_after` has passed, with the date it was last
  checked. It is a warning only: the times stay on the site, the run isn't
  held, and this is the list the future updater works from.
- A batch of source seeds going live at once can trip the run's change gate,
  as a seed batch can. Merge them in batches it passes, or approve the held run.

## What changes in the code

| Where | Change |
| :-- | :-- |
| `dioceses/records.py`, `data/dioceses/README.md` | `website_schedule`: validation, promotion, Settled policy 4 |
| `fetch.py`, `__main__.py` (`fetch:check`) | skip and refuse `website_schedule`, with tests |
| new `seeding/captures.py`, `seeding/cli.py` | `seed capture`, storing text and screenshots |
| `seeding/files.py`, `checks.py`, `slots.py`, `finalize.py`, `calls.py` | `kind: source`: format, checks, writing slots, no history, no paid calls |
| `seeding/loader.py`, migration 0014 | load source seeds, store `schedule_source` and `schedule_source_url` with the revision |
| `dioceses/audit.py`, `factory/plan.py` | a `website_schedule` row shares no bulletin, and is never waited on by a seed Run |
| `extract_frontend_db.py`, `packages/core` | the snapshot's `schedule_source`, `source_url` and `checked_on` |
| `apps/web` | source line, wording variants |
| `labeling/server.py`, `apps/labeler` | capture route and viewer |
| `report.py` | source seeds loaded, Source schedules due |
| `.claude/skills/draft-parish-seed/` | source rules in `rules.md`, `kind: source` in `file-format.md`, the procedure in `SKILL.md` |

## Out of scope

- **Moving existing parishes over:** the 109 `no_bulletin` parish rows, and
  the 73 churches in `excluded/` with `reason: no-bulletin`, which need parish
  rows of their own first. Each move is a records change once the capability
  exists.
- **The factory:** a map stage that sets `website_schedule`, and seed jobs for
  these parishes (they need no bulletins, so they wouldn't wait for any).
- **How source seeds are reviewed and approved**, and how much evidence a
  parish needs to qualify. For now the agent's judgement, recorded in
  `current_because`.
- **The quarterly updater.** It re-seeds from new captures, and should only
  need the pieces above.
- **Other sources** (the diocese's directory, Google, MassTimes), and
  **falling back** to a source schedule when a bulletin parish's bulletin
  stops coming.
- **`unsupported` parishes and parishes with a `fetch_gap`**, which never use
  this.

## Implementation decisions

Decisions made while building this, where the plan was silent or the code
departs from it.

- **Capture text is committed, not only stored.** Drafters run with R2 read
  keys only (writes are `CARLO_REMOTE_WRITE`), so a capture kept only in the
  blob store would never leave the drafter's machine. The text is small, so it
  is committed in `data/seeds/captures/`, with `eol=lf` in `.gitattributes`
  so a checkout can't change its hash. The screenshot stays in the blob store:
  it reaches R2 only from a machine that writes there, and the labeler says so
  when it is missing.
- **A capture is its text.** Capturing a page whose text is unchanged keeps the
  capture, moves its `captured_at` to now and replaces its screenshot, since a
  picture on the page (a Facebook schedule) can change under the same text.
- **Quotes are matched** case-, whitespace- and punctuation-insensitively
  (typographic quotes, dashes and ellipses made plain).
- **`recheck_after`** is set by `finalize` to three months after `as_of`
  unless the drafter set a later date; a newer capture that overtakes it
  resets it.
- **Evidence checks run at drafting and approval only**, like a bulletin
  seed's: the loader trusts an approved file, so a parish that has since
  found a bulletin doesn't make its old source seed fail on every command.
- **A later bulletin seed hides the source.** The snapshot shows a church's
  source only while its parish is `website_schedule` and its latest seed
  revision is a source seed's.
- **A source seed's digest** also covers its primary page's URL (a bulletin
  seed's is unchanged), since the revision records it.
- **The bulletin church's disclaimer is unchanged**, byte for byte, so no
  existing church page changes; only city, index and landing pages change
  once, with `SOURCE_PHRASE` and the city disclaimer ("…bulletin or
  website…"), and their sitemap dates move once with them.
- **The source line** links `source_url`, unless it is the parish's homepage,
  which "Visit the parish website" already links; then it is plain text. Its
  link is tracked as `outbound` with `schedule_source` (docs/analytics.md).
- **The factory** leaves `website_schedule` parishes out of seed Runs'
  readiness (they have no bulletins to wait for). Drafting them in the factory
  is out of scope; the explore-diocese method still files a parish with no
  bulletin as `no_bulletin`.
