# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-medium+detail-low+prompt-bae3517e4884`
- Generated: 2026-10-03T17:33:21Z
- Bulletins scored: 18 (labels: done)
- Label events: 337; predicted events: 325
- **1 labeled bulletin(s) have no prediction** and are not scored: catholic-community-buffalo-north/8ce24228

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 279 | 85.8% | 82.8% | 84.3% | 85.8% |
| core | 284 | 87.4% | 84.3% | 85.8% | 87.5% |
| loose | 313 | 96.3% | 92.9% | 94.6% | 93.1% |
| any_time | 317 | 97.5% | 94.1% | 95.8% | 94.1% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday; any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 0 | 0.0% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 20 | 5.9% |
| Spurious (of predicted events) | 8 | 2.5% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 279 | 82.8% |
| core | 5 | 1.5% |
| weekly_vs_dated | 29 | 8.6% |
| wrong_time | 4 | 1.2% |
| wrong_church | 0 | 0.0% |
| wrong_type | 0 | 0.0% |
| missed | 20 | 5.9% |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 42 | 40 | 78.0% | 85.4% | 85.7% | 90.0% | 87.8% | 95.1% | 0.0% | 0.0% |
| confession | 63 | 64 | 89.8% | 91.3% | 93.7% | 92.2% | 92.9% | 94.5% | 0.0% | 0.0% |
| mass | 232 | 221 | 83.9% | 84.3% | 94.0% | 98.6% | 96.2% | 96.2% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 62 | 29 | 48.4% | 50.5% | 80.6% | 86.2% | 82.4% | 82.4% | 0.0% | 0.0% |
| weekly | 275 | 296 | 90.0% | 91.4% | 95.6% | 97.3% | 96.5% | 97.9% | 0.0% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 313 | 98.7% | 240 | 69 | 1 | 2 | 1 |
| weeks_of_month | 261 | 99.6% | 244 | 16 | 0 | 1 | 0 |
| season | 261 | 100.0% | 259 | 2 | 0 | 0 | 0 |
| note | 313 | 92.0% | 238 | 50 | 0 | 24 | 1 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 3 (16.7%) |
| Perfect (core) | 5 (27.8%) |
| Perfect (loose) | 5 (27.8%) |
| Perfect (any_time) | 7 (38.9%) |
| Published date correct | 8/11 (72.7%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 18 |
| Event count: mean abs error | 1.00 |
| Event count: over / under / exact | 3 / 7 / 8 |

## Cost

|  | Value |
|---|---|
| cache_write_tokens | 2,142 |
| cached_tokens | 36,414 |
| input_tokens | 206,793 |
| output_tokens | 43,848 |
| reasoning_tokens | 18,295 |
| Served from cache | 2 |
| Seconds (total / mean / median) | 406.399 / 22.578 / 20.759 |

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious |
|---|---|---|---|---|---|---|---|---|---|
| all-saints-syracuse/62b6fa5f | 11 | 4 | 53.3% | 53.3% | 53.3% | 0 | 0 | 7 | 0 |
| our-lady-of-the-lakes/4151a2a3 | 16 | 17 | 84.8% | 84.8% | 84.8% | 0 | 0 | 2 | 3 |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 14 | 86.7% | 86.7% | 93.3% | 0 | 0 | 2 | 0 |
| all-saints-albany/b2e40cfa | 14 | 12 | 76.9% | 92.3% | 92.3% | 0 | 0 | 2 | 0 |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 23 | 85.1% | 93.6% | 93.6% | 0 | 0 | 2 | 1 |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 32 | 90.6% | 93.8% | 100.0% | 0 | 0 | 0 | 0 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 20 | 60.0% | 95.0% | 95.0% | 0 | 0 | 1 | 1 |
| assumption-resurrection/7850d6ec | 20 | 20 | 90.0% | 95.0% | 100.0% | 0 | 0 | 0 | 0 |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 12 | 11 | 95.7% | 95.7% | 95.7% | 0 | 0 | 1 | 0 |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 39 | 38 | 96.1% | 96.1% | 96.1% | 0 | 0 | 2 | 1 |
| our-lady-of-the-valley/afd5959b | 18 | 19 | 97.3% | 97.3% | 97.3% | 0 | 0 | 0 | 1 |
| beloved-disciples-lancaster/06de9de8 | 42 | 43 | 56.5% | 98.8% | 98.8% | 0 | 0 | 0 | 1 |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 84.6% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 93.8% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| all-saints-corning/6630e7ed | 8 | 8 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |

## Differences

### all-saints-syracuse/62b6fa5f

- **missed**: `mass Monday 11:30 @ all-saints-syracuse`
- **missed**: `mass Tuesday 11:30 @ all-saints-syracuse`
- **missed**: `mass Wednesday 11:30 @ all-saints-syracuse`
- **missed**: `mass Thursday 11:30 @ all-saints-syracuse`
- **missed**: `mass Friday 11:30 @ all-saints-syracuse`
- **missed**: `mass 2026-10-01 11:30 @ all-saints-syracuse; CANCELLED; note: Replaced by Liturgy of the Word with Communion`
- **missed**: `mass 2026-10-02 11:30 @ all-saints-syracuse; CANCELLED; note: Replaced by Liturgy of the Word with Communion`

### our-lady-of-the-lakes/4151a2a3

- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`
- **missed**: `confession 2026-10-04 14:45–15:15 @ st-patricks; note: In the sacristy`
- **spurious**: `confession 2026-11-07 14:45–15:15 @ st-patricks; note: Sacristy`
- **spurious**: `confession 2026-11-07 07:45–08:15 @ st-januarius; note: Chapel`
- **spurious**: `confession 2026-11-08 07:45–08:15 @ st-januarius; note: Chapel`

### basilica-sacred-heart-syracuse/a0d84f1f

- **wrong_time**: label `adoration Friday 12:40–15:00 @ basilica-sacred-heart-syracuse; weeks first` → predicted `adoration Friday 12:10–15:00 @ basilica-sacred-heart-syracuse; weeks first; note: Begins after the 12:10 PM Mass`
- **missed**: `mass 2026-09-29 07:00 @ basilica-sacred-heart-syracuse; CANCELLED; note: Replaced by Communion Service`
- **missed**: `mass 2026-09-30 12:10 @ basilica-sacred-heart-syracuse; CANCELLED; note: Replaced by Communion Service`

### all-saints-albany/b2e40cfa

- **weekly_vs_dated**: label `confession 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `confession Sunday 18:00–19:00 @ all-saints-albany`
- **weekly_vs_dated**: label `adoration 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `adoration Sunday 18:00–19:00 @ all-saints-albany`
- **missed**: `confession 2026-10-04 18:00–19:00 @ all-saints-albany`
- **missed**: `adoration 2026-10-04 18:00–19:00 @ all-saints-albany`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### our-lady-of-the-snow-saints-mary-and-martha/ee854149

- **weekly_vs_dated**: label `mass Saturday 09:00 @ st-francis-of-assisi; weeks first` → predicted `mass 2026-10-03 09:00 @ st-francis-of-assisi; note: First Saturday Mass for the Blessed Virgin Mary`
- **weekly_vs_dated**: label `mass Friday 09:00 @ st-hyacinth; weeks first; note: First Friday` → predicted `mass 2026-10-02 09:00 @ st-hyacinth; note: First Friday Mass and Sacred Heart Devotions`
- **missed**: `mass 2026-10-03 09:00 @ st-patrick-cato`
- **missed**: `adoration Friday 15:00 @ st-hyacinth; weeks first; note: Divine Mercy Chaplet and Benediction`
- **spurious**: `mass 2026-09-30 09:00 @ st-patrick-cato`

### blessed-family-7-west-seneca/eb8eb694

- **core**: label `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday` → predicted `adoration Friday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Adoration Chapel, 839 Mill Rd; weekend exposition continues through Sunday at 11:00 PM`
- **wrong_time**: label `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition` → predicted `adoration Saturday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Adoration Chapel, 839 Mill Rd; weekend exposition runs from Friday at 6:00 AM through Sunday at 11:00 PM`
- **wrong_time**: label `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday` → predicted `adoration Sunday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Adoration Chapel, 839 Mill Rd`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass 2026-09-28 08:30 @ sacred-heart` → predicted `mass Monday 08:30 @ sacred-heart`
- **weekly_vs_dated**: label `mass 2026-09-29 08:30 @ sacred-heart` → predicted `mass Tuesday 08:30 @ sacred-heart`
- **weekly_vs_dated**: label `mass 2026-10-02 08:30 @ sacred-heart` → predicted `mass Friday 08:30 @ sacred-heart`
- **weekly_vs_dated**: label `mass 2026-09-28 12:15 @ st-alphonsus` → predicted `mass Monday 12:15 @ st-alphonsus`
- **weekly_vs_dated**: label `mass 2026-09-29 12:15 @ st-alphonsus` → predicted `mass Tuesday 12:15 @ st-alphonsus`
- **weekly_vs_dated**: label `mass 2026-09-30 12:15 @ st-alphonsus` → predicted `mass Wednesday 12:15 @ st-alphonsus`
- **weekly_vs_dated**: label `mass 2026-10-01 17:15 @ st-alphonsus` → predicted `mass Thursday 17:15 @ st-alphonsus`
- **missed**: `mass 2026-09-25 07:30 @ st-alphonsus; CANCELLED; note: Regular 7:30 AM Mass discontinued`
- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Children's Adoration`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration; continues through October 7`
- **wrong_time**: label `confession Saturday 17:00 @ assumption; note: after 4:00 PM Mass` → predicted `confession Saturday 16:00 @ assumption; note: After 4:00 PM Mass`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **missed**: `confession Saturday 15:30–16:00 @ st-thomas-more`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **missed**: `mass 2026-10-03 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Polish Mass`
- **missed**: `adoration Sunday 15:00 @ our-lady-of-fatima-shrine-lewiston; note: Rosary & Benediction`
- **spurious**: `confession Sunday 13:15–13:30 @ our-lady-of-fatima-shrine-lewiston; weeks fourth; note: Before Tagalog Mass`

### our-lady-of-the-valley/afd5959b

- **spurious**: `mass Sunday 14:00 @ st-anns; note: Televised Mass for shut-ins; channel 1301 - Hornell`

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
- **weekly_vs_dated**: label `mass 2026-09-28 12:00 @ st-mary-assumption-lancaster` → predicted `mass Monday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-29 12:00 @ st-mary-assumption-lancaster` → predicted `mass Tuesday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-30 12:00 @ st-mary-assumption-lancaster` → predicted `mass Wednesday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-01 12:00 @ st-mary-assumption-lancaster` → predicted `mass Thursday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-10-02 12:00 @ st-mary-assumption-lancaster` → predicted `mass Friday 12:00 @ st-mary-assumption-lancaster`
- **weekly_vs_dated**: label `mass 2026-09-28 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Monday 09:00 @ st-philip-the-apostle-cheektowaga`
- **weekly_vs_dated**: label `mass 2026-09-29 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Tuesday 09:00 @ st-philip-the-apostle-cheektowaga`
- **weekly_vs_dated**: label `mass 2026-09-30 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Wednesday 09:00 @ st-philip-the-apostle-cheektowaga`
- **weekly_vs_dated**: label `mass 2026-10-01 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Thursday 09:00 @ st-philip-the-apostle-cheektowaga`
- **spurious**: `mass Friday 09:00 @ st-philip-the-apostle-cheektowaga`

### blessed-sacrament-albany/673e93e2

- **core**: label `confession Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: With Adoration` → predicted `confession Saturday 07:30 @ blessed-sacrament-albany; weeks first`
- **core**: label `adoration Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: Reconciliation available` → predicted `adoration Saturday 07:30 @ blessed-sacrament-albany; weeks first`

### our-mother-of-sorrows-holy-cross/f3f6ac9f

- **core**: label `mass Saturday 08:00 @ our-mother-of-sorrows; weeks second,third,fourth,fifth; note: 1st Saturday at St. John's on the Ridge at 8:15am` → predicted `mass Saturday 08:00 @ our-mother-of-sorrows; note: Except first Saturday; Mass is at St. John's on the Ridge`
