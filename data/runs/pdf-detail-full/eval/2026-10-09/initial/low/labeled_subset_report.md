# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-high+detail-low+prompt-409460690c58`
- Generated: 2026-10-09T16:21:33Z
- Bulletins scored: 21 (labels: done)
- Label events: 380; predicted events: 360
- Optional label events, not scored: 10 (the preferred choice made for 4/10 (40.0%))
- **1 labeled bulletin(s) have no prediction** and are not scored: assumption-resurrection/7850d6ec

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 348 | 96.7% | 91.6% | 94.1% | 93.4% |
| core | 351 | 97.5% | 92.4% | 94.9% | 94.5% |
| loose | 353 | 98.1% | 92.9% | 95.4% | 95.2% |
| any_time | 353 | 98.1% | 92.9% | 95.4% | 95.2% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday (a weekly prediction covers every dated label event of its slot); any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 0 | 0.0% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 27 | 7.1% |
| Spurious (of predicted events) | 7 | 1.9% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 348 | 91.6% |
| core | 3 | 0.8% |
| weekly_vs_dated | 2 | 0.5% |
| wrong_time | 0 | 0.0% |
| wrong_church | 0 | 0.0% |
| wrong_type | 0 | 0.0% |
| missed | 27 | 7.1% |

## Optional events

Label events marked optional are left out of every other number in this report, and so are the predictions paired with them. Preferred = an `include` event was predicted (at the any_time level), or an `exclude` event was not.

| Preference | Events | Preferred choice made |
|---|---|---|
| include | 8 | 2/8 (25.0%) |
| exclude | 2 | 2/2 (100.0%) |
| all | 10 | 4/10 (40.0%) |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 43 | 30 | 68.5% | 74.0% | 62.8% | 90.0% | 74.0% | 74.0% | 0.0% | 0.0% |
| confession | 61 | 61 | 93.4% | 95.1% | 98.4% | 98.4% | 98.4% | 98.4% | 0.0% | 0.0% |
| mass | 276 | 269 | 97.6% | 97.6% | 96.4% | 98.9% | 97.6% | 97.6% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 68 | 60 | 84.4% | 84.4% | 82.4% | 90.0% | 85.9% | 85.9% | 0.0% | 0.0% |
| weekly | 312 | 300 | 96.1% | 97.1% | 95.2% | 99.7% | 97.4% | 97.4% | 0.0% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 353 | 99.2% | 289 | 61 | 0 | 2 | 1 |
| weeks_of_month | 297 | 100.0% | 275 | 22 | 0 | 0 | 0 |
| season | 297 | 100.0% | 295 | 2 | 0 | 0 | 0 |
| note | 353 | 94.3% | 274 | 59 | 0 | 18 | 2 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 8 (38.1%) |
| Perfect (core) | 9 (42.9%) |
| Perfect (loose) | 9 (42.9%) |
| Perfect (any_time) | 9 (42.9%) |
| Published date correct | 8/11 (72.7%); 1 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 21 |
| Event count: mean abs error | 1.52 |
| Event count: over / under / exact | 3 / 9 / 9 |

## Cost

|  | Value |
|---|---|
| Cost (USD, list price) | $0.0585 |
| Cost per bulletin (mean) | $0.0028 |
| Cost per 1,000 bulletins | $2.78 |
| cache_write_tokens | 0 |
| cached_tokens | 84,147 |
| input_tokens | 291,350 |
| output_tokens | 73,794 |
| reasoning_tokens | 45,112 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 879.408 / 41.877 / 39.818 |

- `gpt-6-luna` priced per 1M tokens at $0.10 input, $0.01 cached input, $0.125 cache write, $0.50 output; over 272,000 input tokens $0.20 input, $0.75 output (https://developers.openai.com/api/docs/pricing).
- Standard-tier list prices as of 2026-10-05, for the calls behind 21 scored prediction(s), including those served from the cache.

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious | Optional preferred |
|---|---|---|---|---|---|---|---|---|---|---|
| our-lady-of-the-valley/afd5959b | 18 | 11 | 75.9% | 75.9% | 75.9% | 0 | 0 | 7 | 0 | – |
| st-henry-averill-park/532c7691 | 15 | 19 | 82.4% | 82.4% | 82.4% | 0 | 0 | 1 | 5 | – |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 25 | 87.7% | 87.7% | 87.7% | 0 | 0 | 7 | 0 | – |
| catholic-community-buffalo-north/8ce24228 | 30 | 24 | 88.9% | 88.9% | 88.9% | 0 | 0 | 6 | 0 | 0/3 |
| all-saints-corning/6630e7ed | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| ccncc-valatie/21eee451 | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 11 | 10 | 95.2% | 95.2% | 95.2% | 0 | 0 | 1 | 0 | 0/1 |
| our-lady-of-the-lakes/4151a2a3 | 14 | 13 | 74.1% | 96.3% | 96.3% | 0 | 0 | 1 | 0 | 1/2 |
| blessed-sacrament-st-vincent-de-paul-syracuse/a43633ed | 16 | 15 | 96.8% | 96.8% | 96.8% | 0 | 0 | 1 | 0 | – |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 21 | 97.6% | 97.6% | 97.6% | 0 | 0 | 0 | 1 | – |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 38 | 39 | 98.7% | 98.7% | 98.7% | 0 | 0 | 0 | 1 | 3/3 |
| all-saints-albany/b2e40cfa | 12 | 12 | 83.3% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-syracuse/62b6fa5f | 11 | 11 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | 0/1 |
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

### st-henry-averill-park/532c7691

- **missed**: `mass 2026-09-27 17:00 @ st-henry-averill-park; note: Faith Formation Mass`
- **spurious**: `mass 2026-09-11 18:00 @ st-henry-averill-park; note: September 11th Memorial Mass`
- **spurious**: `confession 2026-09-11 17:00 @ st-henry-averill-park`
- **spurious**: `adoration 2026-09-11 17:00 @ st-henry-averill-park`
- **spurious**: `mass 2026-09-04 08:30 @ st-henry-averill-park; CANCELLED`
- **spurious**: `adoration 2026-09-04 09:00–11:00 @ st-henry-averill-park; CANCELLED`

### blessed-family-7-west-seneca/eb8eb694

- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-09-26 16:30 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:00 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 11:00 @ holy-spirit-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 09:30 @ st-margaret-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 08:00 @ st-mark-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:30 @ st-rose-of-lima-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **optional, prefer include**: left out `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`

### all-saints-corning/6630e7ed

- **missed**: `confession 2026-10-01 17:00–17:45 @ st-marys-corning; note: In the gym`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### ccncc-valatie/21eee451

- **missed**: `adoration Wednesday 10:35 @ st-joseph-stuyvesant; note: After 10:05am mass`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **missed**: `adoration 2026-10-02 10:00–14:00 @ our-lady-queen-of-peace; note: Includes Stations of the Cross and Rosary`
- **optional, prefer include**: left out `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### our-lady-of-the-lakes/4151a2a3

- **core**: label `adoration Thursday 08:30 @ st-michaels-penn-yan; note: Holy Hour in Chapel` → predicted `adoration Thursday 08:30–09:30 @ st-michaels-penn-yan; note: St. Michael's Chapel`
- **weekly_vs_dated**: label `confession 2026-10-04 07:45–08:15 @ st-januarius; note: In the chapel` → predicted `confession Sunday 07:45–08:15 @ st-januarius; weeks first; note: Chapel`
- **weekly_vs_dated**: label `confession 2026-10-03 14:45–15:15 @ st-patricks; note: In the sacristy` → predicted `confession Saturday 14:45–15:15 @ st-patricks; weeks first; note: Sacristy`
- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`
- **optional, prefer include**: left out `confession 2026-11-08 07:45–08:15 @ st-januarius; note: In the chapel`

### blessed-sacrament-st-vincent-de-paul-syracuse/a43633ed

- **missed**: `mass 2026-10-02 09:00 @ blessed-sacrament-syracuse; note: School Mass`

### sacred-heart-auburn-cluster/79b41c2c

- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Children's Adoration`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **spurious**: `mass 2026-09-26 20:00 @ our-lady-of-fatima-shrine-lewiston`

### all-saints-albany/b2e40cfa

- **core**: label `confession Thursday 16:30–17:30 @ all-saints-albany` → predicted `confession Thursday 16:30 @ all-saints-albany`
- **core**: label `adoration Thursday 16:30–17:30 @ all-saints-albany` → predicted `adoration Thursday 16:30 @ all-saints-albany`

### all-saints-syracuse/62b6fa5f

- **optional, prefer include**: left out `mass 2026-09-28 11:30 @ all-saints-syracuse; CANCELLED; note: Replaced by Liturgy of the Word with Communion`
