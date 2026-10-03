# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-medium+detail-low+prompt-a46d78b44585`
- Generated: 2026-10-03T17:33:18Z
- Bulletins scored: 18 (labels: done)
- Label events: 337; predicted events: 309
- **1 labeled bulletin(s) have no prediction** and are not scored: catholic-community-buffalo-north/8ce24228

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 285 | 92.2% | 84.6% | 88.2% | 88.5% |
| core | 289 | 93.5% | 85.8% | 89.5% | 89.9% |
| loose | 303 | 98.1% | 89.9% | 93.8% | 93.9% |
| any_time | 304 | 98.4% | 90.2% | 94.1% | 94.2% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday; any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 0 | 0.0% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 33 | 9.8% |
| Spurious (of predicted events) | 5 | 1.6% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 285 | 84.6% |
| core | 4 | 1.2% |
| weekly_vs_dated | 14 | 4.2% |
| wrong_time | 1 | 0.3% |
| wrong_church | 0 | 0.0% |
| wrong_type | 0 | 0.0% |
| missed | 33 | 9.8% |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 42 | 25 | 65.7% | 71.6% | 59.5% | 100.0% | 74.6% | 74.6% | 0.0% | 0.0% |
| confession | 63 | 62 | 86.4% | 88.0% | 92.1% | 93.5% | 92.8% | 94.4% | 0.0% | 0.0% |
| mass | 232 | 222 | 92.1% | 92.5% | 94.8% | 99.1% | 96.9% | 96.9% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 62 | 43 | 66.7% | 68.6% | 74.2% | 93.0% | 81.9% | 81.9% | 0.0% | 0.0% |
| weekly | 275 | 266 | 92.4% | 93.5% | 93.5% | 98.9% | 96.1% | 96.5% | 0.0% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 303 | 99.0% | 242 | 58 | 0 | 2 | 1 |
| weeks_of_month | 253 | 99.6% | 235 | 17 | 0 | 1 | 0 |
| season | 253 | 100.0% | 251 | 2 | 0 | 0 | 0 |
| note | 303 | 95.4% | 232 | 57 | 0 | 8 | 6 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 4 (22.2%) |
| Perfect (core) | 6 (33.3%) |
| Perfect (loose) | 6 (33.3%) |
| Perfect (any_time) | 7 (38.9%) |
| Published date correct | 8/11 (72.7%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 18 |
| Event count: mean abs error | 1.56 |
| Event count: over / under / exact | 0 / 9 / 9 |

## Cost

|  | Value |
|---|---|
| cache_write_tokens | 2,973 |
| cached_tokens | 50,541 |
| input_tokens | 221,751 |
| output_tokens | 45,364 |
| reasoning_tokens | 21,274 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 462.028 / 25.668 / 24.075 |

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious |
|---|---|---|---|---|---|---|---|---|---|
| our-lady-of-the-valley/afd5959b | 18 | 11 | 62.1% | 75.9% | 75.9% | 0 | 0 | 7 | 0 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 14 | 70.6% | 82.4% | 82.4% | 0 | 0 | 6 | 0 |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 26 | 86.2% | 86.2% | 86.2% | 0 | 0 | 7 | 1 |
| our-lady-of-the-lakes/4151a2a3 | 16 | 13 | 75.9% | 89.7% | 89.7% | 0 | 0 | 3 | 0 |
| all-saints-albany/b2e40cfa | 14 | 12 | 76.9% | 92.3% | 92.3% | 0 | 0 | 2 | 0 |
| all-saints-corning/6630e7ed | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 23 | 89.4% | 93.6% | 93.6% | 0 | 0 | 2 | 1 |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 39 | 39 | 94.9% | 94.9% | 94.9% | 0 | 0 | 2 | 2 |
| assumption-resurrection/7850d6ec | 20 | 20 | 90.0% | 95.0% | 100.0% | 0 | 0 | 0 | 0 |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 12 | 11 | 95.7% | 95.7% | 95.7% | 0 | 0 | 1 | 0 |
| beloved-disciples-lancaster/06de9de8 | 42 | 42 | 85.7% | 97.6% | 97.6% | 0 | 0 | 1 | 1 |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 84.6% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 93.8% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| all-saints-syracuse/62b6fa5f | 11 | 11 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |

## Differences

### our-lady-of-the-valley/afd5959b

- **weekly_vs_dated**: label `mass Thursday 12:10 @ st-anns` → predicted `mass 2026-10-01 12:10 @ st-anns`
- **weekly_vs_dated**: label `mass Friday 12:10 @ st-anns` → predicted `mass 2026-10-02 12:10 @ st-anns`
- **missed**: `adoration Monday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Tuesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Wednesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Thursday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Friday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Saturday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Sunday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass Friday 11:30 @ sacred-heart; weeks first; note: Held in Sacred Heart Parish Hall` → predicted `mass 2026-10-02 11:30 @ sacred-heart; note: First Friday Mass in the Parish Hall`
- **weekly_vs_dated**: label `mass 2026-10-02 08:30 @ sacred-heart` → predicted `mass Friday 08:30 @ sacred-heart`
- **missed**: `mass 2026-09-28 08:30 @ sacred-heart`
- **missed**: `mass 2026-09-29 08:30 @ sacred-heart`
- **missed**: `mass 2026-09-28 12:15 @ st-alphonsus`
- **missed**: `mass 2026-09-29 12:15 @ st-alphonsus`
- **missed**: `mass 2026-09-30 12:15 @ st-alphonsus`
- **missed**: `mass 2026-10-01 17:15 @ st-alphonsus`

### blessed-family-7-west-seneca/eb8eb694

- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`
- **spurious**: `confession Saturday 15:00 @ st-john-vianney-orchard-park`

### our-lady-of-the-lakes/4151a2a3

- **weekly_vs_dated**: label `confession 2026-10-04 07:45–08:15 @ st-januarius; note: In the chapel` → predicted `confession Sunday 07:45–08:15 @ st-januarius; weeks first; note: In the chapel; December schedule to be announced`
- **weekly_vs_dated**: label `confession 2026-10-03 14:45–15:15 @ st-patricks; note: In the sacristy` → predicted `confession Saturday 14:45–15:15 @ st-patricks; weeks first; note: In the sacristy; December schedule to be announced`
- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`
- **missed**: `confession 2026-10-03 07:45–08:15 @ st-januarius; note: In the chapel`
- **missed**: `confession 2026-10-04 14:45–15:15 @ st-patricks; note: In the sacristy`

### all-saints-albany/b2e40cfa

- **weekly_vs_dated**: label `confession 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `confession Sunday 18:00–19:00 @ all-saints-albany`
- **weekly_vs_dated**: label `adoration 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `adoration Sunday 18:00–19:00 @ all-saints-albany`
- **missed**: `confession 2026-10-04 18:00–19:00 @ all-saints-albany`
- **missed**: `adoration 2026-10-04 18:00–19:00 @ all-saints-albany`

### all-saints-corning/6630e7ed

- **missed**: `mass 2026-10-01 08:30 @ st-marys-corning; note: In the gym`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### our-lady-of-the-snow-saints-mary-and-martha/ee854149

- **weekly_vs_dated**: label `mass Friday 09:00 @ st-hyacinth; weeks first; note: First Friday` → predicted `mass 2026-10-02 09:00 @ st-hyacinth; note: First Friday devotions`
- **missed**: `mass 2026-10-03 09:00 @ st-patrick-cato`
- **missed**: `adoration Friday 15:00 @ st-hyacinth; weeks first; note: Divine Mercy Chaplet and Benediction`
- **spurious**: `mass 2026-09-30 09:00 @ st-patrick-cato`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **missed**: `mass 2026-10-03 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Polish Mass`
- **missed**: `adoration Sunday 15:00 @ our-lady-of-fatima-shrine-lewiston; note: Rosary & Benediction`
- **spurious**: `confession Sunday 13:15–13:30 @ our-lady-of-fatima-shrine-lewiston; weeks fourth; note: 15 minutes before Tagalog Mass`
- **spurious**: `confession 2026-10-04 18:15–18:30 @ our-lady-of-fatima-shrine-lewiston; note: 15 minutes before the Healing Mass`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration; ends October 7`
- **wrong_time**: label `confession Wednesday 12:00 @ assumption; note: after 11:15 AM Mass` → predicted `confession Wednesday 11:45 @ assumption; note: After 11:15 AM Mass`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **missed**: `confession Saturday 15:30–16:00 @ st-thomas-more`

### beloved-disciples-lancaster/06de9de8

- **weekly_vs_dated**: label `mass 2026-09-28 12:00 @ st-mary-assumption-lancaster` → predicted `mass Monday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-29 12:00 @ st-mary-assumption-lancaster` → predicted `mass Tuesday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-30 12:00 @ st-mary-assumption-lancaster` → predicted `mass Wednesday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-01 12:00 @ st-mary-assumption-lancaster` → predicted `mass Thursday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-02 12:00 @ st-mary-assumption-lancaster` → predicted `mass Friday 12:00 @ st-mary-assumption-lancaster`
- **missed**: `mass 2026-10-01 09:00 @ st-philip-the-apostle-cheektowaga`
- **spurious**: `mass 2026-10-02 09:00 @ st-philip-the-apostle-cheektowaga`

### blessed-sacrament-albany/673e93e2

- **core**: label `confession Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: With Adoration` → predicted `confession Saturday 07:30 @ blessed-sacrament-albany; weeks first`
- **core**: label `adoration Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: Reconciliation available` → predicted `adoration Saturday 07:30 @ blessed-sacrament-albany; weeks first`

### our-mother-of-sorrows-holy-cross/f3f6ac9f

- **core**: label `mass Saturday 08:00 @ our-mother-of-sorrows; weeks second,third,fourth,fifth; note: 1st Saturday at St. John's on the Ridge at 8:15am` → predicted `mass Saturday 08:00 @ our-mother-of-sorrows; note: Except first Saturday`
