# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-high+detail-low+prompt-409460690c58`
- Generated: 2026-10-09T14:35:39Z
- Bulletins scored: 19 (labels: done)
- Label events: 361; predicted events: 339
- Optional label events, not scored: 10 (the preferred choice made for 6/10 (60.0%))

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 327 | 96.5% | 90.6% | 93.4% | 91.9% |
| core | 330 | 97.3% | 91.4% | 94.3% | 93.0% |
| loose | 333 | 98.2% | 92.2% | 95.1% | 94.4% |
| any_time | 333 | 98.2% | 92.2% | 95.1% | 94.4% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday (a weekly prediction covers every dated label event of its slot); any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 1 | 0.3% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 27 | 7.5% |
| Spurious (of predicted events) | 5 | 1.5% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 327 | 90.6% |
| core | 3 | 0.8% |
| weekly_vs_dated | 3 | 0.8% |
| wrong_time | 0 | 0.0% |
| wrong_church | 1 | 0.3% |
| wrong_type | 0 | 0.0% |
| missed | 27 | 7.5% |

## Optional events

Label events marked optional are left out of every other number in this report, and so are the predictions paired with them. Preferred = an `include` event was predicted (at the any_time level), or an `exclude` event was not.

| Preference | Events | Preferred choice made |
|---|---|---|
| include | 8 | 4/8 (50.0%) |
| exclude | 2 | 2/2 (100.0%) |
| all | 10 | 6/10 (60.0%) |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 42 | 29 | 73.2% | 78.9% | 66.7% | 96.6% | 78.9% | 78.9% | 0.0% | 0.0% |
| confession | 62 | 61 | 95.9% | 97.6% | 96.8% | 98.4% | 97.6% | 97.6% | 1.6% | 0.0% |
| mass | 257 | 249 | 95.7% | 95.7% | 95.3% | 98.4% | 96.8% | 96.8% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 63 | 60 | 84.6% | 86.2% | 84.1% | 93.3% | 88.6% | 88.6% | 0.0% | 0.0% |
| weekly | 298 | 279 | 95.3% | 96.0% | 94.0% | 99.3% | 96.5% | 96.5% | 0.3% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 333 | 99.1% | 272 | 58 | 0 | 2 | 1 |
| weeks_of_month | 277 | 100.0% | 256 | 21 | 0 | 0 | 0 |
| season | 277 | 100.0% | 275 | 2 | 0 | 0 | 0 |
| note | 333 | 94.9% | 255 | 61 | 0 | 14 | 3 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 7 (36.8%) |
| Perfect (core) | 9 (47.4%) |
| Perfect (loose) | 9 (47.4%) |
| Perfect (any_time) | 9 (47.4%) |
| Published date correct | 10/12 (83.3%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 19 |
| Event count: mean abs error | 1.68 |
| Event count: over / under / exact | 3 / 6 / 10 |

## Cost

|  | Value |
|---|---|
| Cost (USD, list price) | $0.0559 |
| Cost per bulletin (mean) | $0.0029 |
| Cost per 1,000 bulletins | $2.94 |
| cache_write_tokens | 0 |
| cached_tokens | 76,133 |
| input_tokens | 262,574 |
| output_tokens | 72,900 |
| reasoning_tokens | 45,466 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 743.672 / 39.141 / 36.196 |

- `gpt-6-luna` priced per 1M tokens at $0.10 input, $0.01 cached input, $0.125 cache write, $0.50 output; over 272,000 input tokens $0.20 input, $0.75 output (https://developers.openai.com/api/docs/pricing).
- Standard-tier list prices as of 2026-10-05, for the calls behind 19 scored prediction(s), including those served from the cache.

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious | Optional preferred |
|---|---|---|---|---|---|---|---|---|---|---|
| our-lady-of-the-valley/afd5959b | 18 | 11 | 75.9% | 75.9% | 75.9% | 0 | 0 | 7 | 0 | – |
| all-saints-syracuse/62b6fa5f | 11 | 8 | 63.2% | 84.2% | 84.2% | 0 | 0 | 3 | 0 | 1/1 |
| all-saints-corning/6630e7ed | 8 | 11 | 84.2% | 84.2% | 84.2% | 0 | 0 | 0 | 3 | – |
| catholic-community-buffalo-north/8ce24228 | 30 | 22 | 84.6% | 84.6% | 84.6% | 0 | 0 | 8 | 0 | 0/3 |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 25 | 87.7% | 87.7% | 87.7% | 0 | 0 | 7 | 0 | – |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 11 | 11 | 90.9% | 90.9% | 90.9% | 1 | 0 | 0 | 0 | 0/1 |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| our-lady-of-the-lakes/4151a2a3 | 14 | 13 | 96.3% | 96.3% | 96.3% | 0 | 0 | 1 | 0 | 2/2 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 21 | 92.7% | 97.6% | 97.6% | 0 | 0 | 0 | 1 | – |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 38 | 39 | 98.7% | 98.7% | 98.7% | 0 | 0 | 0 | 1 | 3/3 |
| all-saints-albany/b2e40cfa | 12 | 12 | 83.3% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| assumption-resurrection/7850d6ec | 20 | 20 | 95.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| beloved-disciples-lancaster/06de9de8 | 42 | 42 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 24 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |

## Differences

### our-lady-of-the-valley/afd5959b

- **missed**: `adoration Monday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Tuesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Wednesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Thursday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Friday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Saturday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Sunday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`

### all-saints-syracuse/62b6fa5f

- **weekly_vs_dated**: label `mass Tuesday 11:30 @ all-saints-syracuse` → predicted `mass 2026-09-29 11:30 @ all-saints-syracuse`
- **weekly_vs_dated**: label `mass Wednesday 11:30 @ all-saints-syracuse` → predicted `mass 2026-09-30 11:30 @ all-saints-syracuse`
- **missed**: `mass Monday 11:30 @ all-saints-syracuse`
- **missed**: `mass Thursday 11:30 @ all-saints-syracuse`
- **missed**: `mass Friday 11:30 @ all-saints-syracuse`

### all-saints-corning/6630e7ed

- **spurious**: `mass 2026-09-28 08:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-09-30 18:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-10-02 12:15 @ st-marys-corning; CANCELLED`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-09-26 16:30 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:00 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `confession 2026-09-29 18:30 @ assumption-buffalo; note: Mission Talk/Reconciliation Service`
- **missed**: `mass 2026-09-30 18:30 @ holy-spirit-buffalo; note: Mission Mass`
- **missed**: `mass 2026-09-27 11:00 @ holy-spirit-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 09:30 @ st-margaret-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 08:00 @ st-mark-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:30 @ st-rose-of-lima-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **optional, prefer include**: left out `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`

### blessed-family-7-west-seneca/eb8eb694

- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **wrong_church**: label `confession Saturday 15:30–16:00 @ st-thomas-more` → predicted `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`
- **optional, prefer include**: left out `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### our-lady-of-the-lakes/4151a2a3

- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass Friday 11:30 @ sacred-heart; weeks first; note: Held in Sacred Heart Parish Hall` → predicted `mass 2026-10-02 11:30 @ sacred-heart; note: First Friday; Parish Hall`
- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Children's Adoration`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **spurious**: `mass 2026-10-12 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Walking pilgrimage`

### all-saints-albany/b2e40cfa

- **core**: label `confession Thursday 16:30–17:30 @ all-saints-albany` → predicted `confession Thursday 16:30 @ all-saints-albany`
- **core**: label `adoration Thursday 16:30–17:30 @ all-saints-albany` → predicted `adoration Thursday 16:30 @ all-saints-albany`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration; ends October 7`
