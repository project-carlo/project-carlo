# Eval report: gemini-3-flash-preview-qualified

- Version: `gemini-3-flash-preview+prompt-0c3297072125`
- Generated: 2026-10-05T21:29:00Z
- Bulletins scored: 19 (labels: done)
- Label events: 361; predicted events: 377
- Optional label events, not scored: 10 (the preferred choice made for 5/10 (50.0%))

## Headline

| Level | Found | Precision | Recall | F1 (micro) | F1 (macro) |
|---|---|---|---|---|---|
| strict | 330 | 87.5% | 91.4% | 89.4% | 90.7% |
| core | 331 | 87.8% | 91.7% | 89.7% | 91.1% |
| loose | 352 | 93.4% | 97.5% | 95.4% | 94.9% |
| any_time | 352 | 93.4% | 97.5% | 95.4% | 94.9% |

Strict = everything agrees; core = end time / weeks / season may differ; loose = also weekly-vs-dated on the same weekday (a weekly prediction covers every dated label event of its slot); any_time = also a wrong start time (same church, type and day). Micro pools every event; macro averages per-bulletin F1.

## Errors

|  | Count | Share |
|---|---|---|
| Wrong church (of label events) | 1 | 0.3% |
| Wrong type (of label events) | 0 | 0.0% |
| Missed (of label events) | 8 | 2.2% |
| Spurious (of predicted events) | 24 | 6.4% |

### Where each label event ended up

| Outcome | Count | Share |
|---|---|---|
| exact | 330 | 91.4% |
| core | 1 | 0.3% |
| weekly_vs_dated | 21 | 5.8% |
| wrong_time | 0 | 0.0% |
| wrong_church | 1 | 0.3% |
| wrong_type | 0 | 0.0% |
| missed | 8 | 2.2% |

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
| adoration | 42 | 49 | 92.3% | 92.3% | 100.0% | 85.7% | 92.3% | 92.3% | 0.0% | 0.0% |
| confession | 62 | 64 | 93.7% | 93.7% | 98.4% | 95.3% | 96.8% | 96.8% | 1.6% | 0.0% |
| mass | 257 | 264 | 87.9% | 88.3% | 96.9% | 94.3% | 95.6% | 95.6% | 0.0% | 0.0% |

## By event kind

|  | Label | Pred | Strict F1 | Core F1 | Loose R | Loose P | Loose F1 | Any-time F1 | Wrong church | Wrong type |
|---|---|---|---|---|---|---|---|---|---|---|
| specific_date | 63 | 54 | 58.1% | 58.1% | 87.3% | 63.0% | 76.1% | 76.1% | 0.0% | 0.0% |
| weekly | 298 | 323 | 95.3% | 95.7% | 99.7% | 98.5% | 99.0% | 99.0% | 0.3% | 0.0% |

## Field accuracy (pairs found at the loose level)

Missing = the label has it, the prediction does not; extra = the reverse. Weeks and season are over weekly–weekly pairs; notes by presence only.

| Field | Pairs | Accuracy | Both empty | Match | Different | Missing | Extra |
|---|---|---|---|---|---|---|---|
| end_time | 352 | 100.0% | 278 | 74 | 0 | 0 | 0 |
| weeks_of_month | 297 | 99.7% | 275 | 21 | 1 | 0 | 0 |
| season | 297 | 100.0% | 295 | 2 | 0 | 0 | 0 |
| note | 352 | 89.5% | 251 | 64 | 0 | 27 | 10 |

## Bulletins

|  | Value |
|---|---|
| Perfect (strict) | 11 (57.9%) |
| Perfect (core) | 11 (57.9%) |
| Perfect (loose) | 12 (63.2%) |
| Perfect (any_time) | 12 (63.2%) |
| Published date correct | 10/12 (83.3%); 0 not given |
| Wrong bulletin (tp / fp / fn / tn) | 0 / 0 / 0 / 19 |
| Event count: mean abs error | 0.84 |
| Event count: over / under / exact | 5 / 0 / 14 |

## Cost

|  | Value |
|---|---|
| Cost (USD, list price) | $0.4784 |
| Cost per bulletin (mean) | $0.0252 |
| Cost per 1,000 bulletins | $25.18 |
| cached_tokens | 43,310 |
| output_tokens | 37,730 |
| prompt_tokens | 105,460 |
| thinking_tokens | 110,644 |
| Served from cache | 0 |
| Seconds (total / mean / median) | 801.681 / 42.194 / 37.98 |

- `gemini-3-flash-preview` priced per 1M tokens at $0.50 input, $0.05 cached input, $3.00 output (https://ai.google.dev/gemini-api/docs/pricing).
- Standard-tier list prices as of 2026-10-05, for the calls behind 19 scored prediction(s), including those served from the cache.

## Per bulletin (worst first)

| Bulletin | Label | Pred | Strict F1 | Loose F1 | Any-time F1 | Wrong church | Wrong type | Missed | Spurious | Optional preferred |
|---|---|---|---|---|---|---|---|---|---|---|
| all-saints-corning/6630e7ed | 8 | 13 | 66.7% | 66.7% | 66.7% | 0 | 0 | 1 | 6 | – |
| our-lady-of-the-lakes/4151a2a3 | 14 | 22 | 66.7% | 77.8% | 77.8% | 0 | 0 | 0 | 8 | 1/2 |
| catholic-community-buffalo-north/8ce24228 | 30 | 31 | 78.7% | 78.7% | 78.7% | 0 | 0 | 6 | 7 | 0/3 |
| our-lady-queen-of-peace-st-thomas-more/a705ed3f | 11 | 11 | 90.9% | 90.9% | 90.9% | 1 | 0 | 0 | 0 | 0/1 |
| sacred-heart-auburn-cluster/79b41c2c | 20 | 20 | 65.0% | 95.0% | 95.0% | 0 | 0 | 1 | 1 | – |
| blessed-sacrament-albany/673e93e2 | 13 | 14 | 96.3% | 96.3% | 96.3% | 0 | 0 | 0 | 1 | – |
| our-mother-of-sorrows-holy-cross/f3f6ac9f | 16 | 17 | 90.9% | 97.0% | 97.0% | 0 | 0 | 0 | 1 | – |
| beloved-disciples-lancaster/06de9de8 | 42 | 42 | 69.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-albany/b2e40cfa | 12 | 12 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-on-the-hudson-mechanicville/bd99469d | 10 | 10 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| all-saints-syracuse/62b6fa5f | 11 | 11 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | 1/1 |
| assumption-resurrection/7850d6ec | 20 | 20 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| basilica-sacred-heart-syracuse/a0d84f1f | 16 | 16 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| blessed-family-7-west-seneca/eb8eb694 | 32 | 32 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| blessed-trinity-buffalo/70221b6b | 8 | 8 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| cathedral-immaculate-conception-syracuse/e61ecc12 | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-lady-of-fatima-shrine-lewiston/0336b2ad | 38 | 38 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | 3/3 |
| our-lady-of-the-snow-saints-mary-and-martha/ee854149 | 24 | 24 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |
| our-lady-of-the-valley/afd5959b | 18 | 18 | 100.0% | 100.0% | 100.0% | 0 | 0 | 0 | 0 | – |

## Differences

### all-saints-corning/6630e7ed

- **missed**: `mass 2026-10-01 08:30 @ st-marys-corning; note: In the gym`
- **spurious**: `mass Wednesday 18:00 @ st-marys-corning; note: In the gym`
- **spurious**: `adoration 2026-10-03 12:00–13:00 @ st-marys-corning; note: Holy Hour and Rosary for Life; in the gym`
- **spurious**: `mass 2026-09-28 08:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-09-30 18:00 @ st-marys-corning; CANCELLED`
- **spurious**: `mass 2026-10-01 08:30 @ st-marys-corning; CANCELLED; note: Moved to 6:00 PM`
- **spurious**: `mass 2026-10-02 12:15 @ st-marys-corning; CANCELLED`

### our-lady-of-the-lakes/4151a2a3

- **weekly_vs_dated**: label `confession 2026-10-04 07:45–08:15 @ st-januarius; note: In the chapel` → predicted `confession Sunday 07:45–08:15 @ st-januarius; weeks first; note: In the Chapel`
- **weekly_vs_dated**: label `confession 2026-10-03 14:45–15:15 @ st-patricks; note: In the sacristy` → predicted `confession Saturday 14:45–15:15 @ st-patricks; weeks first; note: In the Sacristy`
- **spurious**: `confession Saturday 07:45–08:15 @ st-januarius; weeks first; note: In the Chapel`
- **spurious**: `confession Sunday 14:45–15:15 @ st-patricks; weeks first; note: In the Sacristy`
- **spurious**: `mass 2026-09-28 08:00 @ st-januarius; CANCELLED; note: Replaced by Communion Service`
- **spurious**: `mass 2026-09-29 08:00 @ st-michaels-penn-yan; CANCELLED; note: Replaced by Communion Service`
- **spurious**: `mass 2026-09-30 08:00 @ st-januarius; CANCELLED; note: Replaced by Communion Service`
- **spurious**: `mass 2026-10-01 08:00 @ st-michaels-penn-yan; CANCELLED; note: Replaced by Communion Service`
- **spurious**: `mass 2026-10-02 08:00 @ st-januarius; CANCELLED; note: Replaced by Communion Service`
- **spurious**: `mass 2026-10-02 08:00 @ st-michaels-penn-yan; CANCELLED; note: Replaced by Communion Service`
- **optional, prefer include**: left out `confession 2026-11-08 07:45–08:15 @ st-januarius; note: In the chapel`

### catholic-community-buffalo-north/8ce24228

- **missed**: `mass 2026-09-26 16:30 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:00 @ assumption-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 11:00 @ holy-spirit-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 09:30 @ st-margaret-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 08:00 @ st-mark-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **missed**: `mass 2026-09-27 10:30 @ st-rose-of-lima-buffalo; CANCELLED; note: Replaced by Mission Mass schedule`
- **spurious**: `mass 2026-09-26 16:00 @ st-rose-of-lima-buffalo; note: CCBN Family Mission`
- **spurious**: `mass 2026-10-03 00:00 @ st-rose-of-lima-buffalo; note: First Saturday Mass`
- **spurious**: `mass 2026-10-04 11:00 @ holy-spirit-buffalo; note: Children's Liturgy Mass`
- **spurious**: `adoration 2026-10-05 18:30 @ assumption-buffalo; note: Adoration with Rosary and Benediction`
- **spurious**: `adoration 2026-10-12 18:30 @ assumption-buffalo; note: Adoration with Rosary and Benediction`
- **spurious**: `adoration 2026-10-19 18:30 @ assumption-buffalo; note: Adoration with Rosary and Benediction`
- **spurious**: `adoration 2026-10-26 18:30 @ assumption-buffalo; note: Adoration with Rosary and Benediction`
- **optional, prefer include**: left out `mass 2026-09-28 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-29 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`
- **optional, prefer include**: left out `mass 2026-09-30 07:00 @ st-rose-of-lima-buffalo; CANCELLED; note: Not listed during Mission week`

### our-lady-queen-of-peace-st-thomas-more/a705ed3f

- **wrong_church**: label `confession Saturday 15:30–16:00 @ st-thomas-more` → predicted `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`
- **optional, prefer include**: left out `confession Saturday 15:30–16:00 @ our-lady-queen-of-peace`

### sacred-heart-auburn-cluster/79b41c2c

- **weekly_vs_dated**: label `mass 2026-09-28 08:30 @ sacred-heart` → predicted `mass Monday 08:30 @ sacred-heart`
- **weekly_vs_dated**: label `mass 2026-09-29 08:30 @ sacred-heart` → predicted `mass Tuesday 08:30 @ sacred-heart`
- **weekly_vs_dated**: label `mass 2026-09-28 12:15 @ st-alphonsus` → predicted `mass Monday 12:15 @ st-alphonsus`
- **weekly_vs_dated**: label `mass 2026-09-29 12:15 @ st-alphonsus` → predicted `mass Tuesday 12:15 @ st-alphonsus`
- **weekly_vs_dated**: label `mass 2026-09-30 12:15 @ st-alphonsus` → predicted `mass Wednesday 12:15 @ st-alphonsus`
- **weekly_vs_dated**: label `mass 2026-10-01 17:15 @ st-alphonsus` → predicted `mass Thursday 17:15 @ st-alphonsus`
- **missed**: `mass 2026-09-25 07:30 @ st-alphonsus; CANCELLED; note: Regular 7:30 AM Mass discontinued`
- **spurious**: `adoration Friday 09:30 @ sacred-heart; weeks third; note: Childrens Adoration`

### blessed-sacrament-albany/673e93e2

- **spurious**: `mass 2026-10-02 07:00 @ blessed-sacrament-albany; CANCELLED`

### our-mother-of-sorrows-holy-cross/f3f6ac9f

- **core**: label `mass Saturday 08:00 @ our-mother-of-sorrows; weeks second,third,fourth,fifth; note: 1st Saturday at St. John's on the Ridge at 8:15am` → predicted `mass Saturday 08:00 @ our-mother-of-sorrows; weeks second,third,fourth,fifth,last`
- **spurious**: `adoration 2026-10-03 13:00–15:00 @ our-mother-of-sorrows; note: In chapel`

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
- **weekly_vs_dated**: label `mass 2026-10-01 09:00 @ st-philip-the-apostle-cheektowaga` → predicted `mass Thursday 09:00 @ st-philip-the-apostle-cheektowaga`
