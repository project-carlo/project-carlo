# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-low+detail-low+prompt-0c3297072125`
- Generated: 2026-10-05T21:55:57Z
- Bulletins scored: 19 (labels: done)
- Label events: 361; predicted events: 340
- Optional label events, not scored: 10 (the preferred choice made for 4/10 (40.0%))

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 318 | 93.5% | 88.1% | 90.7% | 92.6% |
| core | 319 | 93.8% | 88.4% | 91.0% | 92.8% |
| loose | 333 | 97.9% | 92.2% | 95.0% | 94.8% |
| any_time | 333 | 97.9% | 92.2% | 95.0% | 94.8% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday (a weekly prediction covers every dated label event of its slot); any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 1 | 0.3% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 27 | 7.5% |
| Spurious (of predicted events) | 6 | 1.8% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 318 | 88.1% |
| core | 1 | 0.3% |
| weekly_vs_dated | 14 | 3.9% |
| wrong_time | 0 | 0.0% |
| wrong_church | 1 | 0.3% |
| wrong_type | 0 | 0.0% |
| missed | 27 | 7.5% |

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
| adoration | 42 | 31 | 76.7% | 79.5% | 69.0% | 93.5% | 79.5% | 79.5% | 0.0% | 0.0% |
| confession | 62 | 64 | 96.8% | 96.8% | 98.4% | 95.3% | 96.8% | 96.8% | 1.6% | 0.0% |
| mass | 257 | 245 | 91.2% | 91.2% | 94.6% | 99.2% | 96.8% | 96.8% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 63 | 41 | 71.2% | 73.1% | 79.4% | 97.6% | 86.5% | 86.5% | 0.0% | 0.0% |
| weekly | 298 | 299 | 94.1% | 94.1% | 95.0% | 98.0% | 96.5% | 96.5% | 0.3% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 333 | 99.7% | 271 | 61 | 0 | 0 | 1 |
| weeks_of_month | 281 | 100.0% | 261 | 20 | 0 | 0 | 0 |
| season | 281 | 100.0% | 279 | 2 | 0 | 0 | 0 |
| note | 333 | 91.0% | 255 | 48 | 0 | 27 | 3 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 7 (36.8%) |
| Perfect (core) | 8 (42.1%) |
| Perfect (loose) | 8 (42.1%) |
| Perfect (any_time) | 8 (42.1%) |
| Published date correct | 8/12 (66.7%); 2 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 19 |
| Event count: mean abs error | 1.21 |
| Event count: over / under / exact | 1 / 7 / 11 |

## Cost

|  | Value |
|---|---|
| Cost (USD, list price) | $0.0369 |
| Cost per bulletin (mean) | $0.0019 |
| Cost per 1,000 bulletins | $1.94 |
| cache_write_tokens | 3,786 |
| cached_tokens | 68,148 |
| input_tokens | 255,799 |
| output_tokens | 34,645 |
| reasoning_tokens | 7,222 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 294.624 / 15.507 / 13.246 |

- `gpt-6-luna` priced per 1M tokens at $0.10 input, $0.01 cached input, $0.125 cache write, $0.50 output; over 272,000 input tokens $0.20 input, $0.75 output (https://developers.openai.com/api/docs/pricing).
- Standard-tier list prices as of 2026-10-05, for the calls behind 19 scored prediction(s), including those served from the cache.

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious | Optional preferred |
|---|---|---|---|---|---|---|---|---|---|---|
| our-lady-of-the-valley/afd5959b | 18 | 13 | 77.4% | 77.4% | 77.4% | 0 | 0 | 6 | 1 | – |
| catholic-community-buffalo-north/8ce24228 | 30 | 24 | 85.2% | 85.2% | 85.2% | 0 | 0 | 7 | 1 | 0/3 |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 25 | 84.2% | 87.7% | 87.7% | 0 | 0 | 7 | 0 | – |
| our-lady-of-the-lakes/4151a2a3 | 14 | 15 | 89.7% | 89.7% | 89.7% | 0 | 0 | 1 | 2 | 2/2 |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 11 | 11 | 90.9% | 90.9% | 90.9% | 1 | 0 | 0 | 0 | 0/1 |
| all-saints-albany/b2e40cfa | 12 | 12 | 91.7% | 91.7% | 91.7% | 0 | 0 | 1 | 1 | – |
| all-saints-corning/6630e7ed | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 | – |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 20 | 90.0% | 95.0% | 95.0% | 0 | 0 | 1 | 1 | – |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 23 | 97.9% | 97.9% | 97.9% | 0 | 0 | 1 | 0 | – |
| beloved-disciples-lancaster/06de9de8 | 42 | 41 | 69.9% | 98.8% | 98.8% | 0 | 0 | 1 | 0 | – |
| assumption-resurrection/7850d6ec | 20 | 20 | 95.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-syracuse/62b6fa5f | 11 | 11 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | 0/1 |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 38 | 38 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | 2/3 |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |

## Differences

### our-lady-of-the-valley/afd5959b

- **missed**: `adoration Monday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Tuesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Wednesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Thursday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Friday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Saturday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **spurious**: `mass 2026-10-13 19:00 @ st-marys-rexville; note: Blessed Fulton Sheen relic tour`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-09-26 16:30 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:00 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-30 18:30 @ holy-spirit-buffalo; note: Mission Mass`
- **missed**: `mass 2026-09-27 11:00 @ holy-spirit-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 09:30 @ st-margaret-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 08:00 @ st-mark-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:30 @ st-rose-of-lima-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **spurious**: `adoration Monday 18:30 @ assumption-buffalo; season 10/5–10/26; note: Benediction`
- **optional, prefer include**: left out `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`

### blessed-family-7-west-seneca/eb8eb694

- **weekly_vs_dated**: label `mass Saturday 08:00 @ queen-of-heaven-west-seneca; weeks first; note: In honor of the Blessed Virgin Mary` → predicted `mass 2026-10-03 08:00 @ queen-of-heaven-west-seneca; note: First Saturday`
- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`

### our-lady-of-the-lakes/4151a2a3

- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`
- **spurious**: `confession Saturday 14:45–15:15 @ st-patricks; note: Sacristy`
- **spurious**: `confession Sunday 07:45–08:15 @ st-januarius; note: Chapel`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **wrong_church**: label `confession Saturday 15:30–16:00 @ st-thomas-more` → predicted `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`
- **optional, prefer include**: left out `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### all-saints-albany/b2e40cfa

- **missed**: `mass Thursday 17:30 @ all-saints-albany`
- **spurious**: `mass ? 17:30 @ all-saints-albany`

### all-saints-corning/6630e7ed

- **missed**: `mass 2026-10-01 08:30 @ st-marys-corning; note: In the gym`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass Friday 11:30 @ sacred-heart; weeks first; note: Held in Sacred Heart Parish Hall` → predicted `mass 2026-10-02 11:30 @ sacred-heart; note: First Friday Mass in the Parish Hall`
- **missed**: `mass 2026-09-25 07:30 @ st-alphonsus; CANCELLED; note: Regular 7:30 AM Mass discontinued`
- **spurious**: `adoration Friday 09:30–09:45 @ sacred-heart; weeks third; note: Children's Adoration`

### our-lady-of-the-snow-saints-mary-and-martha/ee854149

- **missed**: `mass 2026-10-02 07:00 @ st-marys-auburn`

### beloved-disciples-lancaster/06de9de8

- **weekly_vs_dated**: label `mass 2026-09-28 08:30 @ our-lady-of-pompeii-lancaster` → predicted `mass Monday 08:30 @ our-lady-of-pompeii-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-29 08:30 @ our-lady-of-pompeii-lancaster` → predicted `mass Tuesday 08:30 @ our-lady-of-pompeii-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-01 08:30 @ our-lady-of-pompeii-lancaster` → predicted `mass Thursday 08:30 @ our-lady-of-pompeii-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-02 08:30 @ our-lady-of-pompeii-lancaster` → predicted `mass Friday 08:30 @ our-lady-of-pompeii-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-28 08:15 @ st-martha-depew` → predicted `mass Monday 08:15 @ st-martha-depew`
- **weekly_vs_dated**: label `mass 2026-09-29 08:15 @ st-martha-depew` → predicted `mass Tuesday 08:15 @ st-martha-depew`
- **weekly_vs_dated**: label `mass 2026-09-30 08:15 @ st-martha-depew` → predicted `mass Wednesday 08:15 @ st-martha-depew`
- **weekly_vs_dated**: label `mass 2026-10-01 08:15 @ st-martha-depew` → predicted `mass Thursday 08:15 @ st-martha-depew`
- **weekly_vs_dated**: label `mass 2026-10-02 08:15 @ st-martha-depew` → predicted `mass Friday 08:15 @ st-martha-depew`
- **weekly_vs_dated**: label `mass 2026-09-28 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Monday 09:00 @ st-philip-the-apostle-cheektowaga`
- **weekly_vs_dated**: label `mass 2026-09-29 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Tuesday 09:00 @ st-philip-the-apostle-cheektowaga`
- **weekly_vs_dated**: label `mass 2026-09-30 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Wednesday 09:00 @ st-philip-the-apostle-cheektowaga`
- **missed**: `mass 2026-10-01 09:00 @ st-philip-the-apostle-cheektowaga`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration through October 7`

### all-saints-syracuse/62b6fa5f

- **optional, prefer include**: left out `mass 2026-09-28 11:30 @ all-saints-syracuse; CANCELLED; note: Replaced by Liturgy of the Word with Communion`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **optional, prefer include**: left out `confession Sunday 13:15–13:30 @ our-lady-of-fatima-shrine-lewiston; weeks fourth; note: Before Tagalog mass`
