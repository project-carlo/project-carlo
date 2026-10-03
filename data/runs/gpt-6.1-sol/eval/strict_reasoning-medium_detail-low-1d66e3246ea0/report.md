# Eval report: gpt-6.1-sol

- Version: `gpt-6.1-sol+strict+reasoning-medium+detail-low+prompt-ebbd3108f0f8`
- Generated: 2026-10-03T17:32:40Z
- Bulletins scored: 19 (labels: done)
- Label events: 371; predicted events: 358

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 326 | 91.1% | 87.9% | 89.4% | 87.6% |
| core | 335 | 93.6% | 90.3% | 91.9% | 90.5% |
| loose | 348 | 97.2% | 93.8% | 95.5% | 94.2% |
| any_time | 348 | 97.2% | 93.8% | 95.5% | 94.2% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday; any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 0 | 0.0% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 23 | 6.2% |
| Spurious (of predicted events) | 10 | 2.8% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 326 | 87.9% |
| core | 9 | 2.4% |
| weekly_vs_dated | 13 | 3.5% |
| wrong_time | 0 | 0.0% |
| wrong_church | 0 | 0.0% |
| wrong_type | 0 | 0.0% |
| missed | 23 | 6.2% |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 43 | 36 | 70.9% | 86.1% | 81.4% | 97.2% | 88.6% | 88.6% | 0.0% | 0.0% |
| confession | 66 | 65 | 85.5% | 88.5% | 93.9% | 95.4% | 94.7% | 94.7% | 0.0% | 0.0% |
| mass | 262 | 257 | 93.3% | 93.6% | 95.8% | 97.7% | 96.7% | 96.7% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 80 | 67 | 77.6% | 78.9% | 85.0% | 91.0% | 87.8% | 87.8% | 0.0% | 0.0% |
| weekly | 291 | 291 | 92.4% | 95.2% | 96.2% | 98.6% | 97.4% | 97.4% | 0.0% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 348 | 97.7% | 276 | 64 | 2 | 4 | 2 |
| weeks_of_month | 277 | 99.6% | 255 | 21 | 0 | 1 | 0 |
| season | 277 | 100.0% | 275 | 2 | 0 | 0 | 0 |
| note | 348 | 96.0% | 253 | 81 | 0 | 9 | 5 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 4 (21.1%) |
| Perfect (core) | 7 (36.8%) |
| Perfect (loose) | 8 (42.1%) |
| Perfect (any_time) | 8 (42.1%) |
| Published date correct | 12/12 (100.0%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 19 |
| Event count: mean abs error | 1.21 |
| Event count: over / under / exact | 4 / 6 / 9 |

## Cost

|  | Value |
|---|---|
| cache_write_tokens | 3,088 |
| cached_tokens | 55,584 |
| input_tokens | 242,570 |
| output_tokens | 28,719 |
| reasoning_tokens | 3,375 |
| Served from cache | 19 |
| Seconds (total / mean / median) | 509.755 / 26.829 / 23.846 |

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious |
|---|---|---|---|---|---|---|---|---|---|
| our-lady-of-the-valley/afd5959b | 18 | 11 | 75.9% | 75.9% | 75.9% | 0 | 0 | 7 | 0 |
| all-saints-corning/6630e7ed | 8 | 10 | 77.8% | 77.8% | 77.8% | 0 | 0 | 1 | 3 |
| all-saints-syracuse/62b6fa5f | 11 | 9 | 60.0% | 80.0% | 80.0% | 0 | 0 | 3 | 1 |
| our-lady-of-the-lakes/4151a2a3 | 16 | 13 | 69.0% | 89.7% | 89.7% | 0 | 0 | 3 | 0 |
| all-saints-albany/b2e40cfa | 14 | 12 | 61.5% | 92.3% | 92.3% | 0 | 0 | 2 | 0 |
| catholic-community-buffalo-north/8ce24228 | 34 | 31 | 92.3% | 92.3% | 92.3% | 0 | 0 | 4 | 1 |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 12 | 11 | 95.7% | 95.7% | 95.7% | 0 | 0 | 1 | 0 |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 24 | 95.8% | 95.8% | 95.8% | 0 | 0 | 1 | 1 |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 39 | 40 | 96.2% | 96.2% | 96.2% | 0 | 0 | 1 | 2 |
| assumption-resurrection/7850d6ec | 20 | 21 | 87.8% | 97.6% | 97.6% | 0 | 0 | 0 | 1 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 21 | 92.7% | 97.6% | 97.6% | 0 | 0 | 0 | 1 |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 84.6% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| beloved-disciples-lancaster/06de9de8 | 42 | 42 | 88.1% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 32 | 93.8% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 93.8% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| blessed-trinity-buffalo/70221b6b | 8 | 8 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |

## Differences

### our-lady-of-the-valley/afd5959b

- **missed**: `adoration Monday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Tuesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Wednesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Thursday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Friday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Saturday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Sunday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`

### all-saints-corning/6630e7ed

- **missed**: `mass 2026-10-01 08:30 @ st-marys-corning; note: In the gym`
- **spurious**: `mass 2026-09-28 08:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-09-30 18:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-10-02 12:15 @ st-marys-corning; CANCELLED`

### all-saints-syracuse/62b6fa5f

- **weekly_vs_dated**: label `mass Tuesday 11:30 @ all-saints-syracuse` → predicted `mass 2026-09-29 11:30 @ all-saints-syracuse`
- **weekly_vs_dated**: label `mass Wednesday 11:30 @ all-saints-syracuse` → predicted `mass 2026-09-30 11:30 @ all-saints-syracuse`
- **missed**: `mass Monday 11:30 @ all-saints-syracuse`
- **missed**: `mass Thursday 11:30 @ all-saints-syracuse`
- **missed**: `mass Friday 11:30 @ all-saints-syracuse`
- **spurious**: `mass 2026-09-28 11:30 @ all-saints-syracuse; CANCELLED; note: Calendar lists Communion service; Mass intentions conflict.`

### our-lady-of-the-lakes/4151a2a3

- **core**: label `adoration Thursday 08:30 @ st-michaels-penn-yan; note: Holy Hour in Chapel` → predicted `adoration Thursday 08:30–09:30 @ st-michaels-penn-yan; note: Holy Hour in the chapel.`
- **weekly_vs_dated**: label `confession 2026-10-04 07:45–08:15 @ st-januarius; note: In the chapel` → predicted `confession Sunday 07:45–08:15 @ st-januarius; weeks first; note: In the chapel; Sunday of the first full Saturday–Sunday weekend, which may be the second Sunday. December: see Advent schedule.`
- **weekly_vs_dated**: label `confession 2026-10-03 14:45–15:15 @ st-patricks; note: In the sacristy` → predicted `confession Saturday 14:45–15:15 @ st-patricks; weeks first; note: In the sacristy; first full weekend of the month. December: see Advent schedule.`
- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`
- **missed**: `confession 2026-10-03 07:45–08:15 @ st-januarius; note: In the chapel`
- **missed**: `confession 2026-10-04 14:45–15:15 @ st-patricks; note: In the sacristy`

### all-saints-albany/b2e40cfa

- **core**: label `confession Thursday 16:30–17:30 @ all-saints-albany` → predicted `confession Thursday 16:30 @ all-saints-albany`
- **core**: label `adoration Thursday 16:30–17:30 @ all-saints-albany` → predicted `adoration Thursday 16:30 @ all-saints-albany`
- **weekly_vs_dated**: label `confession 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `confession Sunday 18:00–19:00 @ all-saints-albany`
- **weekly_vs_dated**: label `adoration 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `adoration Sunday 18:00–19:00 @ all-saints-albany`
- **missed**: `confession 2026-10-04 18:00–19:00 @ all-saints-albany`
- **missed**: `adoration 2026-10-04 18:00–19:00 @ all-saints-albany`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-10-04 09:30 @ st-margaret-buffalo; note: Padre Pio Mass followed by procession`
- **missed**: `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **missed**: `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **missed**: `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **spurious**: `mass Wednesday 08:00 @ st-mark-buffalo; note: When school is in session; closed to the public`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **missed**: `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### our-lady-of-the-snow-saints-mary-and-martha/ee854149

- **missed**: `mass 2026-10-03 09:00 @ st-patrick-cato`
- **spurious**: `mass 2026-09-30 09:00 @ st-patrick-cato`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **missed**: `mass 2026-10-03 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Polish Mass`
- **spurious**: `confession Sunday 13:15–13:30 @ our-lady-of-fatima-shrine-lewiston; weeks fourth; note: 15 minutes before Tagalog Mass`
- **spurious**: `confession 2026-10-04 18:15–18:30 @ our-lady-of-fatima-shrine-lewiston; note: 15 minutes before Healing Mass`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration; ends October 7 at 5:00 PM`
- **weekly_vs_dated**: label `confession Wednesday 12:00 @ assumption; note: after 11:15 AM Mass` → predicted `confession 2026-09-23 12:00 @ assumption; note: Explicit calendar time after the 11:15 AM Mass`
- **spurious**: `confession Wednesday 11:45 @ assumption; note: After the 11:15 AM Mass`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass 2026-10-02 08:30 @ sacred-heart` → predicted `mass Friday 08:30 @ sacred-heart; note: Beginning September 25, 2026`
- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Children's Adoration`

### blessed-sacrament-albany/673e93e2

- **core**: label `confession Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: With Adoration` → predicted `confession Saturday 07:30 @ blessed-sacrament-albany; weeks first`
- **core**: label `adoration Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: Reconciliation available` → predicted `adoration Saturday 07:30 @ blessed-sacrament-albany; weeks first`

### beloved-disciples-lancaster/06de9de8

- **weekly_vs_dated**: label `mass 2026-09-28 12:00 @ st-mary-assumption-lancaster` → predicted `mass Monday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-29 12:00 @ st-mary-assumption-lancaster` → predicted `mass Tuesday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-30 12:00 @ st-mary-assumption-lancaster` → predicted `mass Wednesday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-01 12:00 @ st-mary-assumption-lancaster` → predicted `mass Thursday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-02 12:00 @ st-mary-assumption-lancaster` → predicted `mass Friday 12:00 @ st-mary-assumption-lancaster`

### blessed-family-7-west-seneca/eb8eb694

- **core**: label `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday` → predicted `adoration Friday 06:00–00:00 @ queen-of-heaven-west-seneca; note: Chapel; exposition continues through Sunday at 11:00 PM`
- **core**: label `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition` → predicted `adoration Saturday 00:00–00:00 @ queen-of-heaven-west-seneca; note: Chapel; continuous exposition all day and overnight`

### our-mother-of-sorrows-holy-cross/f3f6ac9f

- **core**: label `mass Saturday 08:00 @ our-mother-of-sorrows; weeks second,third,fourth,fifth; note: 1st Saturday at St. John's on the Ridge at 8:15am` → predicted `mass Saturday 08:00 @ our-mother-of-sorrows; note: Except the first Saturday of the month.`
