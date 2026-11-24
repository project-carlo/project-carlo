# Seed second opinion: prompt tuning (2026-11-17)

Continues Phase 0 (`phase0-2026-11-16/`, `docs/seed-second-opinion-plan.md`). The work had two
steps: fix the comparison's artefacts, then tune the seed-opinion task (`TASK` and field
descriptions in `classifiers/seed_opinion.py`; `POLICY` and `schedule_update.py` untouched),
all on the same 258 approved seeds. **Chosen: prompt v2** (fingerprint `a926f746480c`),
which is the current state of `seed_opinion.py`.

## 1. The comparison (`src/pdf_extract/seeding/opinion.py`)

Each fix has a test in `tests/test_seed_opinion.py` (14 tests in all). Things count as equal
only where a visitor would see the same schedule.

| artefact | fix |
|---|---|
| 24-hour Adoration written 12:00 AM-12:00 AM, 12:00 AM-11:59 PM or 12:00 AM with no end | all three are all day; this applies to excluded slots too (St. Daniel, Eternal Flame, St. Ann) |
| a period past midnight written as one entry (`Fri 8:00 PM-6:00 AM`) or as two days' entries | compared as its two parts, which group as one item; an end of 12:00 AM after a later start is midnight of the same day |
| same slot, one side with no end or another end, reported as missing + extra | paired as `differs` |
| several slots on one day (Sunday 9/10/11, Friday weeks 2-5 + first) blocking pairing | paired by the same start first, then the nearest start within 120 min (any start when only one of each is left) |
| a dated entry on a day an included weekly slot covers (same church, type, weekday, start; date inside the slot's weeks and season) | dropped (`covered-by-weekly`), on either side, when not matched exactly |
| a cancellation that cancels nothing on either side (no included weekly slot or dated entry at that church/type/day/time) | dropped (`cancels-nothing`) |
| an excluded slot with another season, weeks or end | `excluded` (not `missing`) when the start matches |
| a church slug that plainly means a listed one (`st-mary-honeoye` for `st-marys-honeoye`) | mapped (difflib, cutoff 0.85, one candidate) and flagged as a problem |
| a slot resting only on bulletins luna wasn't given (its agent sources, or history's when it has none) | `resolved: unseen-bulletins` |
| a website-backed slot: a `website` source with R6 (or C9, its old ID) cited, or website-only | `resolved: website` |
| a settled exclusion citing R22-R26 | `resolved: policy-exclusion` |

A website source that only corroborates a slot printed in a bulletin luna read ("R1 ... the
website agrees") is **not** resolved: that is luna missing a printed slot, and it is what
prompt work should reduce. (Phase 0's analysis counted every slot with any website source
as resolved, 95 extras; this counts 52 groups.)

The runner (`scripts/seed-opinion-phase0.py`) now reports counted differences (resolved
excluded): total, median, parishes with none and with 3 or fewer, per kind, agreements,
resolved and dropped counts, output tokens and cost a parish. `--name` writes to
`eval/<name>/`, and `--replay VERSION` re-compares the cached replies of an earlier prompt
version without calls (how the baseline was made).

The baseline is the unchanged Phase 0 prompt (`15a8e58cb64e`) under this matcher, replayed
from the cache for $0 (`baseline-matcher-v2/`). Under the old matcher's report the same
replies had 317 differences (R22-R26 resolved) and 3548 agreements. Under this one they
have 204 and 3581.

## 2. The prompt

All the changes are in `TASK`, which stays static and in the cached developer message after
`POLICY`. Every rule is general, and most restate what POLICY or rules.md already intend
(rule 4, rules 6-7, Times, R14/R15/R33, R36). The rules, grouped by section:

- **v1** (`96cf6b07b25d`), from `failure-modes.md`:
  - *Weekly or dated:* check the weeks in between before calling a slot weekly. A slot
    that alternates with weeks lacking it, dates printed two weeks apart, or a rotation
    table is dated; one shown week without it is an omission.
  - *Seasons:* a season needs a printed start and end. Holiday-bounded or one-ended
    periods and "first full weekend" are dated entries.
  - *Read every page:* services in calendars, sidebars, flyers, the pastor's column and
    images; look for dated services and cancellations on or after today; a day heading
    applies to every line under it.
  - *Exceptions:* qualifiers set the weeks; a one-day exception overrides a range; a
    monthly service that replaces the regular ones; a dated listing beats a reused
    template; "the only Mass is X" cancels the rest.
  - *Times:* "N minutes before" ends at the Mass; a clock start followed by a Mass has no
    end; Benediction closes Adoration; a period past midnight is split; 24-hour or
    perpetual Adoration with no hours is 12:00 AM-11:59 PM; an end time printed in
    another passage is used; never join times across blocks; volunteer sign-up hours are
    not Adoration; garbled times are not completed.
  - *Before you answer:* delete dated duplicates of weekly slots; recheck alternation;
    notes hold no schedule; quote the whole clause and each bulletin's own page.
  - Also fixed the stale section name: "Entries: weekly or dated" is now "Weekly or dated".
- **v2** (`a926f746480c`) fixes v1's own failure modes:
  - an exception limits a slot only when it names that slot. A notice about a separately
    named service ("First Saturday Masses discontinued") doesn't, and neither does an
    exception that a shown week's dated listing contradicts;
  - a start worked out from "N minutes before" always ends at the Mass. The no-end rule
    is only for a printed clock time followed by a *Mass*; another service at a stated
    time ends the period;
  - a feast at a regular slot's time (All Saints at the Sunday Masses) is the weekly
    slot, not a dated entry;
  - only weeks a bulletin shows count as weeks without a slot;
  - a final check that every time in a schedule box, or printed in two weeks' listings,
    is in the answer.
- **v3** (`b9001dbf5431`) = v2 plus:
  - a chapel's own hours printed with an adorer appeal still count (v2 dropped Eternal
    Flame's "24-hour Adoration chapels ... looking for adorers");
  - a church whose name only partly matches a listed one is another church (v1 and v2
    put St. John XXIII's weekend Masses at the listed St. John Vianney);
  - the slug field description says to copy the slug exactly.

No per-request schema change was made. A `church_slug` enum of the parish's slugs would
end the 1-parish-a-run bad slug (`st-mary-honeoye`, `basilica-st-mary-of-the-angels-olean`),
but the response schema is part of the request's prompt. A per-parish schema would likely
cost the cached prefix (about 6k tokens, roughly +$0.0003 a parish, +10%) and add a
schema-compile on every call. The matcher's slug mapping handles it for nothing.

## 3. Results (258 parishes; counted = grouped, resolved excluded)

| | baseline | v1 | v2 | v3 |
|---|---:|---:|---:|---:|
| counted differences | 204 | 199 | **179** | 185 |
| median a parish | 0 | 0 | 0 | 0 |
| parishes with none | 156 | 172 | 162 | 167 |
| parishes with 3 or fewer | 244 | 245 | **248** | 247 |
| missing | 26 | 24 | 25 | 32 |
| extra | 96 | 103 | 87 | 89 |
| differs | 52 | 44 | 39 | 40 |
| excluded | 30 | 28 | 28 | 24 |
| agreements (luna entries matching a slot) | 3581 | 3590 | **3623** | 3622 |
| luna entries | 3739 | 3760 | 3771 | 3778 |
| groups new vs baseline / gone | - | 105 / 110 | 80 / 105 | 91 / 110 |
| hand-checked seed_right errors still flagged (of 35) | 31 | 9 | 13 | 12 |
| luna_right still flagged (of 3) | 3 | 2 | **3** | 2 |
| output tokens a parish, median / mean | 5174 / 6037 | 5490 / 6763 | 5908 / 6760 | 5674 / 6622 |
| cost a parish, median / mean | $0.0029 / 0.0032 | $0.0029 / 0.0032 | $0.0030 / 0.0032 | $0.0032 / 0.0038* |
| this run's spend | $0 | $0.838 | $0.789 | $0.944 |

\* v3's flex had no room for 42 calls (v1 and v2: none), which went to the standard tier at twice the
price. The prompt's own cost is v2's. That also made the budget holds skip 82 parishes
in the first pass, and a second pass (cap $0.52) finished them, keeping the run under
$1.20. v1 likewise needed a second pass for 8 parishes.

Run-to-run noise is large. Between any two runs about 80-110 groups appear and as many
go, so a difference of a few counted items between runs means little. v2 against the
baseline (-25 counted, +42 agreements, every luna_right kept) is the clearest signal.

### The 64 hand-checked items (seed_right items still present, by failure mode)

| failure mode | items | baseline | v1 | v2 | v3 |
|---|---:|---:|---:|---:|---:|
| missed-line | 8 | 7 | 4 | 5 | 5 |
| nonweekly-as-weekly | 7 | 7 | 1 | 1 | 0 |
| ignored-same-bulletin-exception | 4 | 4 | 0 | 1 | 0 |
| dated-duplicate-of-weekly | 2 | 0 | 0 | 0 | 0 |
| signup-as-service | 2 | 2 | 0 | 1 | 1 |
| relative-to-mass-not-derived | 2 | 2 | 1 | 0 | 0 |
| regular-slot-recorded-as-dated | 1 | 1 | 1 | 1 | 1 |
| blended-adjacent-entries | 1 | 1 | 0 | 1 | 1 |
| overnight-span-collapsed | 1 | 1 | 1 | 1 | 1 |
| shared-heading-applied-to-one-line | 1 | 1 | 0 | 0 | 1 |
| implied-cancellation-not-recorded | 1 | 1 | 0 | 0 | 0 |
| invalid-church-slug | 1 | 0 | 0 | 0 | 0 |
| benediction-time-as-start | 1 | 1 | 0 | 0 | 1 |
| silently-repaired-misprint | 1 | 1 | 1 | 1 | 1 |
| ended-at-following-mass | 1 | 1 | 0 | 1 | 0 |
| missed-end-time-elsewhere | 1 | 1 | 0 | 0 | 0 |
| all | 35 | 31 | 9 | 13 | 12 |

The four the baseline already lost (dated duplicates, the bad slug) went with the matcher.

**luna_right:**
- st-mary-our-mother s12 (the 7:00 PM relic Mass, only in an image) and transfiguration-troy
  s4/s5 (confession after the weekend Masses, an image-only box) are flagged in every run.
- chautauqua-family-catholic s19 is flagged in the baseline and v2 but **lost in v1 and
  v3**. Luna applied "11/7 FIRST SATURDAY - NO MASS" and "discontinue First Saturday Masses"
  to the 4:00 PM vigil and so agreed with the seed's wrong "except the first". v2's rule
  (an exception must name the slot, and a shown week's listing beats it; B4's Oct 3 lists
  the vigil) fixed it in v2's run but not v3's, so the reading is unstable.

## 4. Failure modes

**Went down** (hand-checked items and the sweep):
- nonweekly-as-weekly: 7 to 0-1 (Holy Name's Oct 13 & 27, St. Rose's alternate weeks,
  the confession rotation, Bolton Landing).
- ignored-same-bulletin-exception: 4 to 0-1 (St. Luke's "other than First Fridays",
  SS. Columba-Brigid's last Sunday, Boonville's Wednesday, St. Leo's Communion Service).
- signup-as-service: Whitehall and Oneida fixed.
- relative-to-mass times: Owego "1/2 hour before", Benediction as end (St. Peter's), end
  times from another passage (Marcellus) and "followed by Mass" (Franklinville) fixed in
  most runs.
- dated duplicates: mostly gone (also matched away).
- missed-line: about half. Mater Christi's four Mondays, Ithaca's Mass of Remembrance and
  Wheat's First Friday are now read. Holy Rosary's flyer, West Winfield's "last 2
  Mondays" and Stamford's Monday are still missed.

**Didn't go down:**
- overnight spans (Transfiguration Syracuse's First Friday-to-Saturday);
- the silently repaired misprint (Kateri's "3:4pm");
- the regular slot recorded as dated (Assumption Syracuse's 8:30);
- blended adjacent blocks (Niagara Falls, back in v2 and v3);
- the judgment items (Benediction as an end, Holy Hour length, venue calls), which stay
  as differences, as they should.

**New failure modes found by spot checks** (about 20 new differences read across v1-v3):
- v1 only, all fixed in v2:
  - derived "15 minutes before every Mass" confessions lost their end (Fatima, 6 groups);
  - "followed by Evening Prayer at 6:00" lost its end (Sacred Heart Troy);
  - "an hour before the Mass" lost its end (Hudson Valley);
  - All Saints weekend Masses were recorded as dated (Ballston Spa);
  - Tue/Thu/Fri 6:30 Masses were made dated because the week between two bulletins
    wasn't shown (Transfiguration Syracuse);
  - box lines were dropped (Holy Trinity Hudson's Saturday confession, Twelve Apostles'
    Sunday noon);
- v1 and v2: Eternal Flame's two 24-hour chapels were dropped (the sign-up rule
  overreached; fixed in v3);
- v1 and v2, not fixed in v3: St. John XXIII's weekend Masses given to the listed
  St. John Vianney;
- v2: a literal "4:00am" vigil from an intentions misprint (St. Martin de Porres).
- **Judged to be luna applying POLICY where the seed didn't** (not luna errors):
  - "Confessions available after all Masses" turned into after-Mass windows (St. Louis
    Pittsford);
  - Lakeshore's and Sacred Heart Troy's perpetual chapels as all day;
  - Oneida's and St. Daniel's 24-hour chapels, now matched to the seed's venue exclusions.

## 5. Spend

| | sanity | full run | total |
|---|---:|---:|---:|
| v1 (first sanity check at `f067cc16`, superseded) | $0.046 | $0.838 | $0.884 |
| v2 | $0.049 | $0.789 | $0.838 |
| v3 | $0.039 | $0.944 | $0.983 |
| **all** | | | **$2.70** of $3.60 |

No run went over $1.20. The baseline and every re-comparison were cache replays ($0).

## 6. Chosen version and what next

v2 is the final state of `seed_opinion.py`. It has the fewest counted differences, the most
agreements, the most parishes with 3 or fewer, and is the only run that keeps all three
real seed errors flagged. v3's two fixes (chapel hours with an adorer appeal, the
similar-name church) are sound, but its run came out no better overall and lost
chautauqua again. They are worth re-testing together with a second v2 run to measure the
noise.

Worth considering next:
- `seed_opinion` has run-to-run variance of about ±10% in counted differences. Production
  can't rerun, but evaluation should compare two runs of the same prompt before believing
  a small gain.
- The chautauqua case shows that luna still reads a separately named service's
  cancellation as a qualifier of the regular slot. That is a POLICY-level rule for the
  eval classifiers too.
- Outputs: `baseline-matcher-v2/`, `prompt-v1-2026-11-17/`, `prompt-v2-2026-11-17/`,
  `prompt-v3-2026-11-17/` (each has its `report.md`; the script's `results.json` stays local). Replies are cached
  by prompt version in `cache/`.
