# Measuring the factory's quota

Quota points, not API-price dollars, are what limit the factory, so each attempt's
five-hour and weekly points are measured from readings of the usage endpoint. The code
is `src/pdf_extract/factory/metrics/`; nothing in it picks, gates or blocks a job, and a
failure there is logged, never raised into a job. How accounts are chosen against the
caps is in [factory.md](factory.md#usage-and-accounts).

## Readings

Every reading is a `usage` row with its `source`, the attempt and job it is for, and the
whole response (`raw`: model-specific and extra windows too), with anything that looks
like a credential removed.

| Source | When |
|---|---|
| `select` | Each usage check, every account. |
| `before` | The chosen account's `select` reading, relabelled when its attempt starts. |
| `after` | Started in the background as soon as the worker returns. The gates wait for it at most 10 seconds; a late or failed one is logged and dropped. |
| `settled` | Once per attempt, when its account has been idle `quota_settle_seconds` (default 150) after it, since the meter lags a minute or two. |
| `periodic` | Every account each `quota_sample_minutes` (default 15). |

None of these run without accounts (stub Runs), or during a usage-check cooldown. Each
SDK rate-limit event is kept in full in `rate_limit_event` (type, status, utilization,
reset time, overage, raw), besides its `rate_limit` step.

**Calibration gap.** `calibration_gap_seconds` (default 0: nothing waits) holds the next
job on an account until that long after its last attempt finished, so every attempt gets
a settled reading. Set it at or above `quota_settle_seconds`, for calibration runs only.
A job waiting on every account waits until the soonest of one coming under its caps and
one's gap ending.

## Attribution

Computed when a report asks, never stored (`metrics/quota.py`). The meter shows whole
percents, so every answer is a range with a label, never a bare number:

| Label | When | Points |
|---|---|---|
| `settled` | An idle reading before, a settled one after, no other attempt on the account in between | the delta ±1 (a displayed 0 is `<1`) |
| `immediate` | Only a reading sooner than `quota_settle_seconds` after it | a minimum |
| `shared` | Another attempt on the account started less than `quota_settle_seconds` after this one ended | the group's total over its combined interval; no exact share (the first attempt's early reading still gives it a minimum) |
| `reset` | The window's reset time moved by more than 3 minutes (they jitter by a second), or passed | a minimum |
| `missing` | No usable reading before or after | none |
| `inconsistent` | The meter fell without a reset | none |

A job's points are the sum of its attempts' ranges; attempts in one `shared` group count
the group's upper bound once, and its label is its worst attempt's. The meter rising
between two readings while the account was idle is outside use, and attempts within an
hour of it are flagged.

**Window totals** (`factory quota --windows`): per account and window instance (keyed by
its reset time), the points used, the factory's settled, shared and uncertain portions,
and what's unexplained (outside use, usage lagging past an early reading, use before the
first reading). They stay useful when per-attempt attribution isn't.

## Attempt metadata

One `attempt_meta` row per attempt (`metrics/attempt_meta.py`):

- the requested model and effort (the stage spec's), the models it used (side calls
  included), SDK and CLI versions, entrypoint, the account's plan (from the login's
  `.credentials.json`, else `plan:` in `local.yaml`);
- `config_hash`: a fingerprint of the stage spec, prompt file and skill names, plus
  hashes of the code that builds the first message, the skills' contents, the `reads:`
  and the dispatcher's commit, so before/after comparisons see any change to what the
  worker was given;
- the attempt whose session it resumed;
- tokens, in total and per model: input; output, of which thinking is a part; cache
  reads; cache writes by 5-minute and 1-hour TTL; web searches; distinct messages and
  repeated transcript records (`metrics/tokens.py`);
- work units: a map job's batch entries, a seed or seed-review job's parishes, 1 for any
  other stage;
- gaps (what couldn't be recorded), and its `source`: `live` (the ResultMessage) or
  `transcript` (a crash or timeout, parsed from its transcript, counting messages once by
  id from the attempt's start to its finish, so a resumed session's other attempts stay
  out).

Rows with source `backfill` and `approximate = 1` are attempts from before quota tracking
(October 2026), filled in once from their transcripts by a command since removed. Their
quota is a minimum at best, never settled.

## Reports

- `pnpm factory quota`: points per unit of completed work, by stage, or within stages
  `--by model|effort|mode|account|plan|date|hour` (`--tz` for the last two): the median
  and range over settled samples, uncertain jobs apart, with sample counts, coverage,
  first-try gate passes, retries, send-backs, crashes and partials, unresolved and parked
  work, and dollars last as a diagnostic. It fits no model and assumes no peak hours or
  quota multipliers; those are questions for its data.
- `pnpm factory quota --windows`: the window totals above.
- `pnpm factory inspect <job>`: each attempt's metadata, tokens, rate-limit events and
  quota ranges with the readings used. `inspect --stage S --last N`: a stage's recent
  jobs with theirs.
- `pnpm factory cost [--stage]`: API-price dollars by Run or stage, a diagnostic only.
