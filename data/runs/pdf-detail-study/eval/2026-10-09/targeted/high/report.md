# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-high+detail-high+prompt-409460690c58`
- Generated: 2026-10-09T14:40:42Z
- Bulletins scored: 3 (labels: done)
- Label events: 60; predicted events: 53

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 52 | 98.1% | 86.7% | 92.0% | 92.9% |
| core | 52 | 98.1% | 86.7% | 92.0% | 92.9% |
| loose | 52 | 98.1% | 86.7% | 92.0% | 92.9% |
| any_time | 52 | 98.1% | 86.7% | 92.0% | 92.9% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday (a weekly prediction covers every dated label event of its slot); any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 0 | 0.0% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 8 | 13.3% |
| Spurious (of predicted events) | 1 | 1.9% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 52 | 86.7% |
| core | 0 | 0.0% |
| weekly_vs_dated | 0 | 0.0% |
| wrong_time | 0 | 0.0% |
| wrong_church | 0 | 0.0% |
| wrong_type | 0 | 0.0% |
| missed | 8 | 13.3% |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 9 | 3 | 33.3% | 33.3% | 22.2% | 66.7% | 33.3% | 33.3% | 0.0% | 0.0% |
| confession | 6 | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 0.0% | 0.0% |
| mass | 45 | 44 | 98.9% | 98.9% | 97.8% | 100.0% | 98.9% | 98.9% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 9 | 8 | 94.1% | 94.1% | 88.9% | 100.0% | 94.1% | 94.1% | 0.0% | 0.0% |
| weekly | 51 | 45 | 91.7% | 91.7% | 86.3% | 97.8% | 91.7% | 91.7% | 0.0% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 52 | 100.0% | 48 | 4 | 0 | 0 | 0 |
| weeks_of_month | 44 | 100.0% | 40 | 4 | 0 | 0 | 0 |
| season | 44 | 100.0% | 44 | 0 | 0 | 0 | 0 |
| note | 52 | 94.2% | 45 | 4 | 0 | 3 | 0 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 0 (0.0%) |
| Perfect (core) | 0 (0.0%) |
| Perfect (loose) | 0 (0.0%) |
| Perfect (any_time) | 0 (0.0%) |
| Published date correct | 2/2 (100.0%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 3 |
| Event count: mean abs error | 3.00 |
| Event count: over / under / exact | 1 / 2 / 0 |

## Cost

|  | Value |
|---|---|
| Cost (USD, list price) | $0.0122 |
| Cost per bulletin (mean) | $0.0041 |
| Cost per 1,000 bulletins | $4.06 |
| cache_write_tokens | 0 |
| cached_tokens | 12,021 |
| input_tokens | 72,426 |
| output_tokens | 12,020 |
| reasoning_tokens | 7,818 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 161.566 / 53.855 / 45.875 |

- `gpt-6-luna` priced per 1M tokens at $0.10 input, $0.01 cached input, $0.125 cache write, $0.50 output; over 272,000 input tokens $0.20 input, $0.75 output (https://developers.openai.com/api/docs/pricing).
- Standard-tier list prices as of 2026-10-05, for the calls behind 3 scored prediction(s), including those served from the cache.

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious | Optional preferred |
|---|---|---|---|---|---|---|---|---|---|---|
| blessed-family-7-west-seneca/eb8eb694 | 32 | 25 | 87.7% | 87.7% | 87.7% | 0 | 0 | 7 | 0 | – |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 21 | 97.6% | 97.6% | 97.6% | 0 | 0 | 0 | 1 | – |

## Differences

### blessed-family-7-west-seneca/eb8eb694

- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### sacred-heart-auburn-cluster/79b41c2c

- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Children's Adoration`
