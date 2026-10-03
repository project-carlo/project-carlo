# Eval report: gpt-6-luna

- Version: `gpt-6-luna+strict+reasoning-medium+detail-original+pages-200dpi+prompt-ebbd3108f0f8`
- Generated: 2026-10-03T17:32:36Z
- Bulletins scored: 19 (labels: done)
- Label events: 371; predicted events: 356

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 332 | 93.3% | 89.5% | 91.3% | 90.4% |
| core | 336 | 94.4% | 90.6% | 92.4% | 91.8% |
| loose | 339 | 95.2% | 91.4% | 93.3% | 92.9% |
| any_time | 340 | 95.5% | 91.6% | 93.5% | 93.2% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday; any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 0 | 0.0% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 31 | 8.4% |
| Spurious (of predicted events) | 16 | 4.5% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 332 | 89.5% |
| core | 4 | 1.1% |
| weekly_vs_dated | 3 | 0.8% |
| wrong_time | 1 | 0.3% |
| wrong_church | 0 | 0.0% |
| wrong_type | 0 | 0.0% |
| missed | 31 | 8.4% |

## By event type

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| adoration | 43 | 29 | 66.7% | 72.2% | 62.8% | 93.1% | 75.0% | 75.0% | 0.0% | 0.0% |
| confession | 66 | 69 | 90.4% | 91.9% | 95.5% | 91.3% | 93.3% | 94.8% | 0.0% | 0.0% |
| mass | 262 | 258 | 95.0% | 95.4% | 95.0% | 96.5% | 95.8% | 95.8% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 80 | 75 | 78.7% | 80.0% | 81.2% | 82.7% | 81.9% | 81.9% | 0.0% | 0.0% |
| weekly | 291 | 281 | 94.8% | 95.8% | 94.2% | 98.6% | 96.3% | 96.7% | 0.0% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 339 | 99.1% | 273 | 63 | 0 | 2 | 1 |
| weeks_of_month | 274 | 99.6% | 252 | 21 | 0 | 1 | 0 |
| season | 274 | 100.0% | 272 | 2 | 0 | 0 | 0 |
| note | 339 | 96.2% | 257 | 69 | 0 | 9 | 4 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 3 (15.8%) |
| Perfect (core) | 5 (26.3%) |
| Perfect (loose) | 5 (26.3%) |
| Perfect (any_time) | 6 (31.6%) |
| Published date correct | 9/12 (75.0%); 1 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 19 |
| Event count: mean abs error | 1.74 |
| Event count: over / under / exact | 5 / 6 / 8 |

## Cost

|  | Value |
|---|---|
| cache_write_tokens | 3,088 |
| cached_tokens | 55,584 |
| input_tokens | 653,411 |
| output_tokens | 51,090 |
| reasoning_tokens | 22,685 |
| Served from cache | 19 |
| Seconds (total / mean / median) | 597.261 / 31.435 / 27.701 |

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious |
|---|---|---|---|---|---|---|---|---|---|
| all-saints-corning/6630e7ed | 8 | 11 | 73.7% | 73.7% | 73.7% | 0 | 0 | 1 | 4 |
| our-lady-of-the-valley/afd5959b | 18 | 11 | 75.9% | 75.9% | 75.9% | 0 | 0 | 7 | 0 |
| our-lady-of-the-lakes/4151a2a3 | 16 | 19 | 85.7% | 85.7% | 85.7% | 0 | 0 | 1 | 4 |
| catholic-community-buffalo-north/8ce24228 | 34 | 28 | 87.1% | 87.1% | 87.1% | 0 | 0 | 7 | 1 |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 25 | 87.7% | 87.7% | 87.7% | 0 | 0 | 7 | 0 |
| all-saints-albany/b2e40cfa | 14 | 12 | 76.9% | 92.3% | 92.3% | 0 | 0 | 2 | 0 |
| blessed-trinity-buffalo/70221b6b | 8 | 7 | 93.3% | 93.3% | 93.3% | 0 | 0 | 1 | 0 |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 39 | 40 | 93.7% | 93.7% | 93.7% | 0 | 0 | 2 | 3 |
| assumption-resurrection/7850d6ec | 20 | 20 | 90.0% | 95.0% | 100.0% | 0 | 0 | 0 | 0 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 20 | 90.0% | 95.0% | 95.0% | 0 | 0 | 1 | 1 |
| all-saints-syracuse/62b6fa5f | 11 | 12 | 95.7% | 95.7% | 95.7% | 0 | 0 | 0 | 1 |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 12 | 11 | 95.7% | 95.7% | 95.7% | 0 | 0 | 1 | 0 |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 24 | 95.8% | 95.8% | 95.8% | 0 | 0 | 1 | 1 |
| beloved-disciples-lancaster/06de9de8 | 42 | 43 | 98.8% | 98.8% | 98.8% | 0 | 0 | 0 | 1 |
| blessed-sacrament-albany/673e93e2 | 13 | 13 | 84.6% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 16 | 93.8% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 |

## Differences

### all-saints-corning/6630e7ed

- **missed**: `mass 2026-10-01 08:30 @ st-marys-corning; note: In the gym`
- **spurious**: `adoration 2026-10-03 12:00–13:00 @ st-marys-corning; note: In the gym; Holy Hour and Rosary for Life`
- **spurious**: `mass 2026-09-28 08:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-09-30 18:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-10-02 12:15 @ st-marys-corning; CANCELLED`

### our-lady-of-the-valley/afd5959b

- **missed**: `adoration Monday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Tuesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Wednesday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Thursday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Friday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Saturday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`
- **missed**: `adoration Sunday 06:00–19:00 @ st-anns; note: Eucharistic Adoration Chapel (Formerly St. Ann’s Convent Chapel)`

### our-lady-of-the-lakes/4151a2a3

- **missed**: `mass 2026-09-29 11:00 @ st-michaels-penn-yan; note: School Mass`
- **spurious**: `confession 2026-11-07 14:45–15:15 @ st-patricks; note: In the sacristy`
- **spurious**: `confession 2026-11-07 07:45–08:15 @ st-januarius; note: In the chapel`
- **spurious**: `confession 2026-11-08 14:45–15:15 @ st-patricks; note: In the sacristy`
- **spurious**: `confession 2026-11-08 07:45–08:15 @ st-januarius; note: In the chapel`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-09-27 11:00 @ holy-spirit-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-10-04 09:30 @ st-margaret-buffalo; note: Padre Pio Mass followed by procession`
- **missed**: `mass 2026-09-27 08:00 @ st-mark-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:30 @ st-rose-of-lima-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **missed**: `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **missed**: `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **spurious**: `mass Wednesday 08:00 @ st-mark-buffalo; note: During the school year when school is in session; closed to the public`

### blessed-family-7-west-seneca/eb8eb694

- **missed**: `adoration Monday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Tuesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Wednesday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Thursday 06:00–23:00 @ queen-of-heaven-west-seneca; note: Eucharistic Exposition`
- **missed**: `adoration Friday 06:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition starts at 6:00 AM Friday`
- **missed**: `adoration Saturday 00:00–23:59 @ queen-of-heaven-west-seneca; note: Continuous exposition`
- **missed**: `adoration Sunday 00:00–23:00 @ queen-of-heaven-west-seneca; note: Continuous exposition ends at 11:00 PM Sunday`

### all-saints-albany/b2e40cfa

- **weekly_vs_dated**: label `confession 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `confession Sunday 18:00–19:00 @ all-saints-albany`
- **weekly_vs_dated**: label `adoration 2026-09-27 18:00–19:00 @ all-saints-albany` → predicted `adoration Sunday 18:00–19:00 @ all-saints-albany`
- **missed**: `confession 2026-10-04 18:00–19:00 @ all-saints-albany`
- **missed**: `adoration 2026-10-04 18:00–19:00 @ all-saints-albany`

### blessed-trinity-buffalo/70221b6b

- **missed**: `mass 2026-10-28 19:00 @ blessed-trinity-buffalo; note: Healing Mass`

### our-lady-of-fatima-shrine-lewiston/0336b2ad

- **missed**: `mass 2026-10-03 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Polish Mass`
- **missed**: `adoration Sunday 15:00 @ our-lady-of-fatima-shrine-lewiston; note: Rosary & Benediction`
- **spurious**: `confession Sunday 13:15–13:30 @ our-lady-of-fatima-shrine-lewiston; weeks fourth; note: Before the 1:30 PM Tagalog Mass`
- **spurious**: `mass 2026-09-26 20:00 @ our-lady-of-fatima-shrine-lewiston`
- **spurious**: `mass 2026-10-12 16:00 @ our-lady-of-fatima-shrine-lewiston; note: Mass at the Shrine`

### assumption-resurrection/7850d6ec

- **core**: label `adoration 2026-10-06 00:00 @ resurrection; note: 40 Hours Adoration; continues until Oct 7 at 5:00 PM` → predicted `adoration 2026-10-06 00:00–17:00 @ resurrection; note: 40 Hours Adoration; continues until Wednesday, October 7`
- **wrong_time**: label `confession Wednesday 12:00 @ assumption; note: after 11:15 AM Mass` → predicted `confession Wednesday 11:45 @ assumption; note: After the 11:15 AM Mass`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass 2026-10-02 08:30 @ sacred-heart` → predicted `mass Friday 08:30 @ sacred-heart`
- **missed**: `mass 2026-09-25 07:30 @ st-alphonsus; CANCELLED; note: Regular 7:30 AM Mass discontinued`
- **spurious**: `adoration Friday 09:30–09:45 @ sacred-heart; weeks third; note: Children's Adoration`

### all-saints-syracuse/62b6fa5f

- **spurious**: `mass 2026-09-28 11:30 @ all-saints-syracuse; CANCELLED; note: Liturgy of the Word with Communion replaces Mass`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **missed**: `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### our-lady-of-the-snow-saints-mary-and-martha/ee854149

- **missed**: `mass 2026-10-03 09:00 @ st-patrick-cato`
- **spurious**: `mass 2026-09-30 09:00 @ st-patrick-cato`

### beloved-disciples-lancaster/06de9de8

- **spurious**: `mass 2026-10-02 12:00 @ st-philip-the-apostle-cheektowaga; note: All Souls`

### blessed-sacrament-albany/673e93e2

- **core**: label `confession Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: With Adoration` → predicted `confession Saturday 07:30 @ blessed-sacrament-albany; weeks first`
- **core**: label `adoration Saturday 07:30–08:45 @ blessed-sacrament-albany; weeks first; note: Reconciliation available` → predicted `adoration Saturday 07:30 @ blessed-sacrament-albany; weeks first`

### our-mother-of-sorrows-holy-cross/f3f6ac9f

- **core**: label `mass Saturday 08:00 @ our-mother-of-sorrows; weeks second,third,fourth,fifth; note: 1st Saturday at St. John's on the Ridge at 8:15am` → predicted `mass Saturday 08:00 @ our-mother-of-sorrows; note: Except first Saturdays; Mass is at St. John's on the Ridge`
