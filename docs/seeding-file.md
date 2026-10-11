# Seed file reference

Both seeding skills use this reference. Read it before drafting or repairing a seed.
The extraction policy remains `src/pdf_extract/classifiers/schedule_policy.py` (`POLICY`).

`seed init` creates the complete top-level object. Keep its `schema_version`, `parish_slug`,
`drafted_by`, `drafted_at`, `bulletins` and `calls`; add your `summary` and `slots`.
Never delete call records during repair: they are the audit trail and paid-call counter.
`seed init --resume` preserves the file, including prior decisions, sources and calls.

Mark every bulletin you read with `seed mark-read <parish> <hash>`, including one with no
schedule or one you reject. Slot citations also mark their bulletins read during `finalize`,
but citations alone cannot record everything you consulted. The newest listed bulletin must
be read before a nonblocked draft passes `check`; `as_of` is the newest read bulletin's fetch
time. Reading a newer bulletin requires reconsidering the draft against that bulletin.

A settled inclusion without a reviewer answer must have an `agent` source citing the newest
read bulletin at the slot's `page`. An older or website-only candidate is `needs_human`,
with `page: null` when the newest bulletin does not print it. A reviewer can explicitly
include such a candidate by answering the question. Historical evals reject website sources.
New approvals run these checks; loading already-approved seeds trusts their reviewer
without retroactively imposing new drafting evidence requirements.

## Parish status

| Status | Meaning |
| :-- | :-- |
| `drafting` | Work in progress, including an interrupted draft |
| `needs_review` | At least one open question |
| `ready` | No open questions; waiting for a person to approve |
| `approved` | A person approved it; agents must not resume or edit it |
| `blocked` | Cannot be seeded now; `blocked_reason` explains why |

`seed status` reads whether a file is loaded from the database; this is not a file field.
An answer is `{"choice": <option index, "edited", or "dropped">, "by": "<reviewer>",
"at": "<ISO time>"}`. The labeler sets it and updates the slot's entry, decision and status.

## Slots and sources

Write only what says something; `finalize` fills in the rest. A weekly slot, a seasonal
one, a dated cancellation, and an open question:

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
    "rationale": "Printed in the Mass schedule box of all four bulletins read; history agrees."
  },
  {
    "decision": "include", "status": "settled", "page": 2,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "adoration",
              "day_of_week": "Thursday", "start_time": "09:00", "end_time": "19:00",
              "season": {"start_month": 9, "start_day": null, "end_month": 5, "end_day": null}},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "Thursdays 9 AM - 7 PM, September through May"}],
    "rationale": "The schedule box gives the months; the policy keeps them as the season."
  },
  {
    "decision": "include", "status": "settled", "page": 3,
    "entry": {"church_slug": "st-marys-oswego", "event_type": "mass",
              "event_kind": "specific_date", "date": "2026-10-12", "start_time": "08:00",
              "cancelled": true, "note": "Columbus Day"},
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 3,
                 "said": "No 8 AM Mass on Monday, October 12"}],
    "rationale": "The newest bulletin cancels one date of the weekly Monday Mass."
  },
  {
    "status": "needs_human", "page": 2,
    "sources": [{"source": "agent", "bulletin": "9f2c41d0", "page": 2,
                 "said": "First Friday Holy Hour 9:45 AM"}],
    "rationale": "Printed once, with no place given; no other bulletin's calendar covers a first Friday.",
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
  a season may run across the new year. A half-stated season ("from October") is no season.
- `page` is where the **newest** bulletin prints the slot (null when it doesn't). It becomes
  the entry's sighting when the seed is loaded.
- `sources[].source` is `agent` (your reading), `history`, `website` (with its `url`), or a
  call's id. `bulletin` is a hash or a prefix of at least 8 characters. `said` is what that
  source says, in its words. When several bulletins print the same words, one `agent`
  source may list them as `bulletins`; `finalize` splits it into one source per bulletin.
  `finalize` adds the `history` sources that match; write one yourself only to say what it
  can't ("no weekday Masses stored").
- A seed holds weekly slots, plus dated entries and cancellations **on or after `as_of`'s
  date** (next Saturday's vigil called off). Update mode never reads a bulletin fetched on or
  before `as_of`, so a cancellation left out here never reaches the site.
- One slot per day and time: "Mon–Fri 8:00 AM" is five slots. Record each excluded
  history event as its own slot too: `seed diff` matches entries and options, not events
  mentioned only in a rationale. Reuse a rationale for a group excluded for the same reason.
- In new drafts, leave `reviewer`, `approved_at` and every `answer` null: the reviewer
  sets them. During repair, preserve existing reviewer answers and leave changes to
  answered decisions to the reviewer in the labeler.

