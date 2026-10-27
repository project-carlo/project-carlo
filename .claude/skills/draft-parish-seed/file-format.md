# Seed file format

`data/seeds/<parish>.json`. This is the file's shape; what to decide for each slot is in [rules.md](rules.md).

`seed start` creates the complete top-level object. Keep its `schema_version`,
`parish_slug`, `drafted_by`, `drafted_at`, `bulletins` and `calls`, and add your `summary`
(two or three sentences a reviewer reads first) and `slots` with the write commands
("Writing slots", below). `calls` is the audit trail and
the paid-call counter. Each entry of `bulletins` has `read`, which `seed mark-read` and
`finalize` set. `as_of` is the newest read bulletin's fetch time, and `finalize` sets it.

## Parish status

| Status | Meaning |
| :-- | :-- |
| `drafting` | Work in progress, including an interrupted draft |
| `needs_review` | At least one open question |
| `ready` | No open questions; waiting for `seed-review` to approve |
| `approved` | `seed-review` approved it; it is the reviewer's |
| `blocked` | Cannot be seeded now; `blocked_reason` explains why |

`seed status` reads whether a file is loaded from the database; this is not a file field.
An answer is `{"choice": <option index, "edited", or "dropped">, "by": "<reviewer>",
"at": "<ISO time>"}`. `seed approve` sets it from `seed-review`'s answers and updates the
slot's entry, decision and status, as the labeler does.

## Slots and sources

Write only what says something; `finalize` fills in the rest. A weekly slot, a seasonal
one, a dated cancellation, and an open question, each rationale citing its rule:

```json
"slots": [
  {
    "decision": "include", "status": "settled", "page": 2,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "mass",
              "day_of_week": "Saturday", "start_time": "16:00"},
    "sources": [
      {"source": "agent", "bulletins": ["9f2c41d0", "1ab3e7c2", "77d0be19"], "page": 2,
       "said": "Sat 4:00 PM Vigil"},
      {"source": "agent", "bulletin": "5e60aa31", "page": 3, "said": "Saturday 4 PM"}
    ],
    "rationale": "R1: printed in the Mass schedule box of all four bulletins read."
  },
  {
    "decision": "include", "status": "settled", "page": 2,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "adoration",
              "day_of_week": "Thursday", "start_time": "09:00", "end_time": "19:00",
              "season": {"start_month": 9, "start_day": null, "end_month": 5, "end_day": null}},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "Thursdays 9 AM - 7 PM, September through May"}],
    "rationale": "R1: the schedule box gives the months; POLICY keeps them as the season."
  },
  {
    "decision": "include", "status": "settled", "page": 3,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "mass",
              "event_kind": "specific_date", "date": "2026-10-12", "start_time": "08:00",
              "cancelled": true, "note": "Columbus Day"},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 3,
                 "said": "No 8 AM Mass on Monday, October 12"}],
    "rationale": "R1, R16: the newest bulletin cancels one date of the weekly Monday Mass."
  },
  {
    "decision": "exclude", "status": "settled", "page": 2,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "mass",
              "day_of_week": "Monday", "start_time": "12:15",
              "note": "At the Franciscan Place, Destiny USA"},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "Franciscan Place: Mon-Thu 12:15 Mass"}],
    "rationale": "R23: the chapel at Destiny USA is not on the church list."
  },
  {
    "status": "needs_human", "page": 2,
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "First Friday Holy Hour 9:45 AM"}],
    "rationale": "R32: no place given. Printed once; no other week read holds a first Friday.",
    "question": "Add a first-Friday 9:45 AM Holy Hour at St. Mary's?",
    "options": [
      {"label": "First Fridays 9:45 AM", "leaning": true,
       "entry": {"church_slug": "st-marys-oswego", "event_type": "adoration",
                 "day_of_week": "Friday", "start_time": "09:45", "weeks_of_month": ["first"]}},
      {"label": "Leave out", "entry": null}
    ]
  }
]
```

- `entry` is a label event without `page_number`, `origin` and `optional`, times 24-hour
  `HH:MM`. `event_kind` is `weekly` or `specific_date` (never "dated"; `finalize` sets it from
  whether the entry has a `date`). A weekly entry has `day_of_week`, and may have
  `weeks_of_month` and `season`, and `exclude_weeks: true` when the listed weeks are
  the ones it skips. "Every Sunday except the last" is `weeks_of_month: ["last"]`
  with `exclude_weeks: true`; "except the first" uses the weeks that remain. A dated
  entry has `date`, and `cancelled: true` when called off. `finalize` defaults
  `exclude_weeks` to false and fills `church_slug` for a one-church parish.
- `season` has all four keys: months 1–12, and a day of the month or null when the
  bulletin gives only the month. September through May is `start_month` 9, `end_month` 5:
  a season may run across the new year (R15 says when there is none).
- `page` is where the **newest** bulletin prints the slot, or null when it doesn't. It
  becomes the entry's sighting when the seed is loaded.
- `sources[].source` is `agent` (your reading), `history`, `website` (with the `url` that
  `seed site` printed), or a call's id. `bulletin` is a hash or a prefix of at least 8
  characters. `said` is what that source says, in its own words. When several bulletins
  print the same words, one `agent` source may list them as `bulletins`, and `finalize`
  splits it into one source per bulletin. `finalize` adds the `history` sources that
  match. Write one yourself only to say what it can't ("no weekday Masses stored").
- A website source may carry `schedule_check`: `checked_at` (ISO time of the agent's
  assessment), `current_because` (why the schedule appears current after considering
  stale-page clues), `bulletin` (the newest read bulletin's hash or prefix), and
  `fits_because` (why the quoted schedule makes sense in that bulletin's context).
  For an agent-settled website-backed inclusion, keep the website's actual schedule
  quote in `said`, its URL in `url`, and the slot's `page` null. The exact time need
  not appear in a bulletin. Validation requires the assessment's shape and newest
  bulletin reference; the agent judges credibility and freshness. It imposes no
  fixed age or frequency threshold. `finalize` preserves assessments and never creates one.
- An every-week slot retained after one omission may carry `weekly_omission`:
  `{"bulletin": "9f2c41d0", "reason": "..."}`. The reference must name the newest
  read issue; `reason` explicitly assesses why that issue merely omits the established
  service rather than cancelling it or changing its schedule. Keep `page` null and
  cite paged `agent` quotes for this same church, service type, weekday and time from
  at least two older read issue weeks. One must be the immediately preceding read
  issue, dated exactly one issue week before newest. Duplicate citations, different
  PDFs for the same week, and repeat fetches do not supply another week. Only valid,
  plausible `published_date` values count; fetch dates cannot substitute for missing
  issue dates. Validation checks this provenance; the agent must judge what the
  quotes establish and whether newest contradicts them. Named monthly patterns
  (`weeks_of_month` or `exclude_weeks`) use their existing targeted evidence rules,
  never this fallback. `finalize` preserves the assessment and never creates one.
- One slot per day and time: "Mon–Fri 8:00 AM" is five slots.
- A question has a short `question`, `options` (an option's `entry` is null for "leave it
  out"), exactly one `"leaning": true`, and its reasons in `rationale`. Slots that share a
  `"group"` name have the same `question`, and options with the same labels, in the same
  order, with the same leaning. Each slot keeps its own entries. The labeler shows the
  group once, and its answer settles them all.
- `church_list_issues` (top level) lists each church or chapel once:
  `{"church": "The Franciscan Place, Destiny USA", "said": "Mon-Thu 12:15 Mass;
  Confession Wed 11-12", "bulletin": "9f2c41d0", "page": 2}`.
- `blocked_reason` says why a `blocked` file can't be seeded now.
- `reviewer`, `approved_at` and every `answer` are the reviewer's: null in a new draft,
  and left as they are in a repair.

## Writing slots

Write slots with `pnpm seed slot ...`, never by editing the JSON or with a script. Each
command checks what it wrote against the file's validation and the parish's churches, and
writes nothing if a check fails. `pnpm seed slot --help` has the full syntax.

- An **entry** is words in any order: type (`mass`, `confession`, `adoration`); days
  (`Sat`, `Mon-Fri`, `Tue,Thu`) or a date (`2026-10-12`); times (`16:00`, `15:00-15:45`,
  `08:00,10:30`, or `4pm`); `@church` (a slug, or a unique part of one of the parish's;
  needed when it has several); weeks (`first`, `2nd,4th`, `last`, or `except=last` for
  the weeks it skips); `season=9-5` or `season=9/15-5/31`; `cancelled`; and last,
  `note=` with the rest of the text. Several days or times make one slot each.
- A **source** is `"HEAD: what it said"`. The head is `latest p2` (the newest listed
  bulletin), hash prefixes `9f2c41d0,1ab3e7c2 p2` (one source each), `web URL`,
  `history`, or a call's id (`c1 p3`). A slot's `page` defaults to its source's page on
  the newest bulletin.
- With a `web URL: quote` source, the paired flags `--website-current "why it appears
  current" --website-context "why it fits the newest bulletin" add a `schedule_check`
  to each website source added by that command. The CLI records the check time and
  newest listed bulletin reference. Read and mark that bulletin before finalizing;
  use `--page -` when editing a slot that previously had a bulletin page. Without
  those flags, website sources remain ordinary supporting evidence. For different
  assessments, add website sources in separate commands.
- `slot include` and `slot edit` accept `--weekly-omission "why newest merely omits
  this established service"` to record that judgment against the newest listed
  bulletin. Supply the matching older quotes with `--src` and use `--page -`.
  For example: `--src "1ab3e7c2,77d0be19 p2: Holy Family: Saturday Vigil Mass 4 PM"`.
  Read and mark newest before finalizing; the evidence requirements above still
  apply. `slot edit ... --weekly-omission -` removes the assessment.
- An **option** is `--option "LABEL" "ENTRY"`, or just `--option "LABEL"` for leaving it
  out. `*` before one label marks the leaning. An entry `+ ...` is the first option's
  entry with those changes (`+ except=first`).

The slots above, plus a grouped question, as one batch (`pnpm seed slot batch <parish>
plan.txt`; each line is a `seed slot` command without `slot` and the parish):

```
include "mass Sat 16:00" --src "latest,1ab3e7c2,77d0be19 p2: Sat 4:00 PM Vigil" \
    --src "5e60aa31 p3: Saturday 4 PM" --why "R1: printed in the Mass schedule box of all four bulletins read."
include "adoration Thu 09:00-19:00 season=9-5" \
    --src "latest p2: Thursdays 9 AM - 7 PM, September through May" \
    --why "R1: the schedule box gives the months; POLICY keeps them as the season."
include "mass 2026-10-12 08:00 cancelled note=Columbus Day" \
    --src "latest p3: No 8 AM Mass on Monday, October 12" \
    --why "R1, R16: the newest bulletin cancels one date of the weekly Monday Mass."
exclude "mass Mon-Thu 12:15 note=At the Franciscan Place, Destiny USA" \
    --src "latest p2: Franciscan Place: Mon-Thu 12:15 Mass" \
    --why "R23: the chapel at Destiny USA is not on the church list."
exclude - --src "latest p3: Confession by appointment" --why "R26: by appointment has no time."
ask "Add a first-Friday 9:45 AM Holy Hour at St. Mary's?" \
    --option "*First Fridays 9:45 AM" "adoration Fri 09:45 first" --option "Leave out" \
    --src "latest p2: First Friday Holy Hour 9:45 AM" \
    --why "R32: no place given. Printed once; no other week read holds a first Friday."
ask "Add the convent chapel's 7 AM weekday Mass?" --group convent \
    --option "*Weekdays 7 AM" "mass Mon-Fri 07:00 note=Convent chapel" --option "Leave out" \
    --src "latest p4: Convent chapel, weekdays 7 AM" --why "R32: the chapel may be St. Mary's."
church-issue "The Franciscan Place, Destiny USA" "latest p2: Mon-Thu 12:15 Mass; Confession Wed 11-12"
summary "One church. Weekend, weekday and Adoration times agree in all four bulletins. Open: a first-Friday Holy Hour and the convent chapel's weekday Mass."
```

The last `ask` makes five slots, Monday to Friday, in group `convent`: one answer settles
them all. Then:

- `seed slot list <parish>` lists every slot with its id; `slot show <parish> s3` prints
  one in full, its sources numbered.
- `seed slot edit <parish> s3 [s4 ...]` changes slots and keeps their ids: `--entry
  "16:30 note="` (only what it names), `--include`, `--exclude` or `--ask "Q" --option
  ...` (a question settled by `--include` takes its leaning option's entry), `--page`,
  `--src` (adds), `--drop-src N`, `--why`, `--group`.
- `seed slot rm <parish> s3` removes a slot you added. A slot a reviewer answered keeps
  its decision, and a call's evidence stays.
- `seed summary`, `seed church-issue <parish> "church" "HEAD: said"` (`--rm` takes one
  off) and `seed block <parish> "reason"` (`--clear` undoes it) set the file's fields.
