# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-high+detail-low+prompt-409460690c58`
- Generated: 2026-10-09T14:32:15Z
- Bulletins scored: 19 (labels: done)
- Label events: 361; predicted events: 352
- Optional label events, not scored: 10 (the preferred choice made for 5/10 (50.0%))

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 339 | 96.3% | 93.9% | 95.1% | 94.6% |
| core | 342 | 97.2% | 94.7% | 95.9% | 95.8% |
| loose | 345 | 98.0% | 95.6% | 96.8% | 96.8% |
| any_time | 345 | 98.0% | 95.6% | 96.8% | 96.8% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday (a weekly prediction covers every dated label event of its slot); any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 1 | 0.3% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 15 | 4.2% |
| Spurious (of predicted events) | 6 | 1.7% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 339 | 93.9% |
| core | 3 | 0.8% |
| weekly_vs_dated | 3 | 0.8% |
| wrong_time | 0 | 0.0% |
| wrong_church | 1 | 0.3% |
| wrong_type | 0 | 0.0% |
| missed | 15 | 4.2% |

## Optional events

Label events marked optional are left out of every other number in this report, and so are the predictions paired with them. Preferred = an `include` event was predicted (at the any_time level), or an `exclude` event was not.

| Preference | Events | Preferred choice made |
|---|---|---|
| include | 8 | 3/8 (37.5%) |
| exclude | 2 | 2/2 (100.0%) |
| all | 10 | 5/10 (50.0%) |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 42 | 35 | 83.1% | 88.3% | 81.0% | 97.1% | 88.3% | 88.3% | 0.0% | 0.0% |
| confession | 62 | 64 | 90.5% | 92.1% | 98.4% | 95.3% | 96.8% | 96.8% | 1.6% | 0.0% |
| mass | 257 | 253 | 98.0% | 98.0% | 97.3% | 98.8% | 98.0% | 98.0% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 63 | 57 | 86.7% | 88.3% | 87.3% | 94.7% | 90.8% | 90.8% | 0.0% | 0.0% |
| weekly | 298 | 295 | 96.8% | 97.5% | 97.3% | 98.6% | 98.0% | 98.0% | 0.3% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 345 | 99.1% | 278 | 64 | 0 | 2 | 1 |
| weeks_of_month | 289 | 100.0% | 267 | 22 | 0 | 0 | 0 |
| season | 289 | 100.0% | 287 | 2 | 0 | 0 | 0 |
| note | 345 | 95.9% | 258 | 73 | 0 | 12 | 2 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 9 (47.4%) |
| Perfect (core) | 10 (52.6%) |
| Perfect (loose) | 10 (52.6%) |
| Perfect (any_time) | 10 (52.6%) |
| Published date correct | 9/12 (75.0%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 19 |
| Event count: mean abs error | 0.89 |
| Event count: over / under / exact | 2 / 5 / 12 |

## Cost

|  | Value |
|---|---|
| Cost (USD, list price) | $0.0569 |
| Cost per bulletin (mean) | $0.0030 |
| Cost per 1,000 bulletins | $2.99 |
| cache_write_tokens | 4,007 |
| cached_tokens | 72,126 |
| input_tokens | 262,574 |
| output_tokens | 74,037 |
| reasoning_tokens | 45,639 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 862.768 / 45.409 / 46.078 |

- `gpt-6-luna` priced per 1M tokens at $0.10 input, $0.01 cached input, $0.125 cache write, $0.50 output; over 272,000 input tokens $0.20 input, $0.75 output (https://developers.openai.com/api/docs/pricing).
- Standard-tier list prices as of 2026-10-05, for the calls behind 19 scored prediction(s), including those served from the cache.

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious | Optional preferred |
|---|---|---|---|---|---|---|---|---|---|---|
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 11 | 10 | 85.7% | 85.7% | 85.7% | 1 | 0 | 1 | 0 | 0/1 |
| blessed-trinity-buffalo/70221b6b | 8 | 8 | 87.5% | 87.5% | 87.5% | 0 | 0 | 1 | 1 | – |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 25 | 87.7% | 87.7% | 87.7% | 0 | 0 | 7 | 0 | – |
| catholic-community-buffalo-north/8ce24228 | 30 | 27 | 94.7% | 94.7% | 94.7% | 0 | 0 | 3 | 0 | 0/3 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 20 | 95.0% | 95.0% | 95.0% | 0 | 0 | 1 | 1 | – |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 38 | 41 | 96.2% | 96.2% | 96.2% | 0 | 0 | 0 | 3 | 3/3 |
| our-lady-of-the-lakes/4151a2a3 | 14 | 13 | 81.5% | 96.3% | 96.3% | 0 | 0 | 1 | 0 | 2/2 |
| assumption-resurrection/7850d6ec | 20 | 21 | 87.8% | 97.6% | 97.6% | 0 | 0 | 0 | 1 | – |
| beloved-disciples-lancaster/06de9de8 | 42 | 41 | 98.8% | 98.8% | 98.8% | 0 | 0 | 1 | 0 | – |
| all-saints-albany/b2e40cfa | 12 | 12 | 83.3% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-corning/6630e7ed | 8 | 8 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-syracuse/62b6fa5f | 11 | 11 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | 0/1 |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 24 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-lady-of-the-valley/afd5959b | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |

## Differences

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **wrong_church**: label `confession Saturday 15:30–16:00 @ st-thomas-more` → predicted `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`
- **missed**: `adoration 2026-10-02 10:00–14:00 @ our-lady-queen-of-peace; note: Includes Stations of the Cross and Rosary`
- **optional, prefer include**: left out `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`
- **spurious**: `mass Thursday 11:00 @ blessed-trinity-buffalo`

### blessed-family-7-west-seneca/eb8eb694

- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-09-27 11:00 @ holy-spirit-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 08:00 @ st-mark-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:30 @ st-rose-of-lima-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **optional, prefer include**: left out `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`

### sacred-heart-auburn-cluster/79b41c2c

- **missed**: `mass 2026-09-25 07:30 @ st-alphonsus; CANCELLED; note: Regular 7:30 AM Mass discontinued`
- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Children's Adoration`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **spurious**: `mass 2026-09-26 20:00 @ our-lady-of-fatima-shrine-lewiston`
- **spurious**: `mass 2026-10-12 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Walking pilgrimage`
- **spurious**: `confession 2026-09-26 19:45–20:00 @ our-lady-of-fatima-shrine-lewiston; note: 15 minutes before the 8:00 PM Mass`

### our-lady-of-the-lakes/4151a2a3

- **weekly_vs_dated**: label `confession 2026-10-04 07:45–08:15 @ st-januarius; note: In the chapel` → predicted `confession Sunday 07:45–08:15 @ st-januarius; weeks first,second; note: First full weekend of the month; Chapel`
- **weekly_vs_dated**: label `confession 2026-10-03 14:45–15:15 @ st-patricks; note: In the sacristy` → predicted `confession Saturday 14:45–15:15 @ st-patricks; weeks first,second; note: First full weekend of the month; Sacristy`
- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration, through October 7`
- **weekly_vs_dated**: label `confession Wednesday 12:00 @ assumption; note: after 11:15 AM Mass` → predicted `confession 2026-09-23 12:00 @ assumption`
- **spurious**: `confession Wednesday 11:45 @ assumption; note: After the 11:15 AM Mass`

### beloved-disciples-lancaster/06de9de8

- **missed**: `mass 2026-10-02 08:30 @ our-lady-of-pompeii-lancaster`

### all-saints-albany/b2e40cfa

- **core**: label `confession Thursday 16:30–17:30 @ all-saints-albany` → predicted `confession Thursday 16:30 @ all-saints-albany`
- **core**: label `adoration Thursday 16:30–17:30 @ all-saints-albany` → predicted `adoration Thursday 16:30 @ all-saints-albany`

### all-saints-syracuse/62b6fa5f

- **optional, prefer include**: left out `mass 2026-09-28 11:30 @ all-saints-syracuse; CANCELLED; note: Replaced by Liturgy of the Word with Communion`
