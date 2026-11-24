# Phase 0 analysis

What `report.md` measures, read by hand. The plan is in docs/seed-second-opinion-plan.md.

## Run

- 266 approved seeds. 258 were compared; 8 had only one bulletin with a stored PDF.
- gpt-6-luna, reasoning high, PDFs at low detail, flex. One call fell back to the standard
  tier when flex had no capacity.
- Cost: about $0.84 in all ($0.0029 median a parish), counting about 2¢ lost when the first
  run (8 workers) was restarted with 24. The policy prefix was served from the prompt cache.
- Flex latency: median about 145 s a call, up to 7 minutes. Run as many calls at once as
  flex allows; 24 at a time worked.

## Counts

`report.md` counts every grouped difference: 319 across 258 parishes. Two kinds are
structural, since luna can't see what settled them, so production should treat them as
resolved:

- a settled exclusion that cites R22–R26 (2);
- an included slot backed by a website source (R6) (73 groups; 95 of the 212 ungrouped
  "extra" slots).

Without those:

| | |
|---|---|
| differences | 244 (mean 0.95, median 0 a parish) |
| parishes with none | 154 of 258 (60%) |
| parishes with 3 or fewer | 237 (92%) |
| most in one parish | 10 |
| by kind | extra 109, missing 62, differs 49, excluded 24 |

The plan's noise threshold, a median of 3 or fewer, is met easily.

## Who was right: a sample of 24

Stratified by kind, one per parish; checked against the PDFs by a Claude subagent
(`sample.json`, `verdicts.json`).

| kind | seed right | luna right | judgment | structural |
|---|---:|---:|---:|---:|
| extra (8) | 5 | 0 | 2 | 1 |
| missing (7) | 4 | 1 | 1 | 1 |
| differs (6) | 2 | 0 | 2 | 2 |
| excluded (3) | 3 | 0 | 0 | 0 |
| **all (24)** | **14** | **1** | **5** | **4** |

- **Luna right, one item:** st-mary-our-mother s12. It excludes the October 29 Sheen relic
  event because "no start time is printed in any stored bulletin". The October 11
  bulletin's page 3 graphic prints "St. Mary Our Mother, Horseheads, Thursday, Oct. 29,
  2026, 7:00pm" (checked by hand). The time is only in the image, so text search misses it.
- **Judgment (5):** Masses with no church named, decided in opposite directions by
  different reviewers (#2, #13); whether "Holy Hour" implies a one-hour end (#17); whether
  Benediction ends Adoration (#21); confession before a monthly Tagalog Mass (#7). Each
  would be a reasonable question for a person.
- The plan's value threshold was one in five pointing at a real error or a question worth
  asking. The sample gives 6 in 24 (25%), but only one real error. Most differences are
  luna's mistakes, which the drafter would dismiss.

## Luna's mistakes

- Writes non-weekly patterns as weekly: every other Wednesday, alternating weeks, "first
  full weekend" as first Sunday, and a Memorial Day to Columbus Day season as months 5–10.
  These are R33 cases.
- Misses lines in schedule boxes or calendars: a "last 2 Mondays" line, a Spanish
  cancellation, a relocated second Mass.
- Misreads small print: two churches' confession times blended into one, adorer sign-up
  gaps taken as Adoration, 24-hour Adoration recorded as two hours.
- Ignores exceptions printed in the same bulletin: a Wednesday Mass at another church,
  Communion Service days against an intentions template.

## Comparison artefacts to fix in Phase 1

Each makes a difference that isn't one:

- 24-hour Adoration written as 00:00–00:00 and as 00:00–23:59.
- The same slot where one side has no end time: reported as missing plus extra, not paired.
- A same-slot end-time difference reported as extra, not differs.
- A dated entry on a day an included weekly slot already covers (POLICY says not to
  duplicate it).
- An excluded slot whose season differs: reported as missing, not paired with the
  exclusion.
- A reviewer-excluded slot with no entry, which can never match.
