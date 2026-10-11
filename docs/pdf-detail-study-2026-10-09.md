# GPT-6 Luna PDF-detail study ? October 9, 2026

## Executive conclusion

High detail can fix a small-text scanned bulletin, but this cohort does **not**
establish a reliable statistical predictor of extraction improvement. Most
differences were native-text interpretation, recurrence, exception handling, or
label/source ambiguity. Several winners changed when identical settings were
rerun.

The practical deliverable is a conservative **scan-resolution risk rule**, not a
claim that high detail guarantees a better schedule. It selects **2/19 PDFs**:
Blessed Trinity Buffalo and Blessed Family 7 West Seneca. It catches the one
visually verified scan-related gain, with one extra escalation. A fitted rule
that looked excellent on the training data failed leave-one-out validation and
should not be deployed.

No production extraction defaults or existing labels were changed.

## Cohort and experimental controls

- Matched exactly the 19 `(parish_slug, content_hash)` pairs from the latest
  **Gemini-qualified eval**, run October 5, 2026 at 21:28:49 UTC:
  `data/runs/gemini-3-flash-preview-qualified/eval/prompt-0c3297072125-0ada6e8be280`.
- This is the latest Gemini **eval cohort**, not freshly fetched October 9
  bulletins. Its recorded issue dates are 15 September 27, two September 26,
  one September 20, and one October 4. It is not a clean single-week sample.
- There are now 22 done labels; the three outside that Gemini cohort were
  deliberately excluded. Copied labels freeze this study's scoring inputs:
  361 required events and 10 optional events.
- Both conditions use `gpt-6-luna`, **high reasoning**, **strict JSON schema**,
  native PDF input, and identical current prompt/schema. Only `input_file.detail`
  changes between `low` and `high`. No `--pdf-as-images` or text-verbosity change.
- Both settings were run fresh over all 19 PDFs, then independently repeated
  over all 19. A third targeted pair covered Blessed Trinity, Blessed Family,
  and Sacred Heart Auburn. **82 fresh API calls**, all served successfully with
  zero skips/errors and zero result-cache hits.
- Historical results were not overwritten. The current policy fingerprint is
  `409460690c58`; Gemini's historical fingerprint was `0c3297072125`. The
  October 8 final-source-check policy additions explain this difference.
  Therefore, the fresh low/high comparison is controlled, but a fresh run versus
  historical Gemini is not a model-only comparison.
- The runner uses historical fetch dates, not October 9, for its reference
  date. Reference dates/church context are read from the database at execution;
  the cohort and labels are frozen, but the database is not archived here.

All artifacts below are rooted at
`data/runs/pdf-detail-study/eval/2026-10-09/`.

## Eval results

?Strict F1? means the repository's exact event matching, **not** the API's
strict-schema switch. ?Loose F1? also tolerates weekly-versus-dated equivalence.
Scores use unchanged labels and can penalize valid, unlabeled source events.

| Run | Strict precision | Strict recall | Strict F1 | Loose F1 | Missed required events | Scored spurious predictions |
|---|---:|---:|---:|---:|---:|---:|
| Initial low | 96.31% | 93.91% | 95.09% | 96.77% | 15 | 6 |
| Initial high | 96.79% | 91.97% | 94.32% | 95.74% | 23 | 5 |
| Repeat low | 96.46% | 90.58% | 93.43% | 95.14% | 27 | 5 |
| Repeat high | 96.77% | 91.41% | 94.02% | 95.44% | 26 | 6 |

The initial pair differed on **9/19 substantive schedules**: high won strict F1
on five, lost on three, and tied on one. Including notes/order/page references,
15 raw event arrays differed. The repeat pair differed on seven schedules and
13 raw arrays. Across pairs, 11 distinct PDFs had substantive differences.

Identical-setting repeats changed schedules on **11/19 low-detail PDFs** and
**7/19 high-detail PDFs**. That variability is substantial relative to the
detail-level effect. Two samples per condition are not enough to estimate a
dependable per-PDF benefit rate.

Recorded input tokens were approximately **262,574 low versus 474,887 high** in
the initial pair: 1.81 times as much input for high. Repository-price estimates
were $0.056885 low and $0.075926 high, about a 33% total-cost increase. All 82
calls together are estimated at **$0.286109**. These use the repository's
October 5 price table and recorded prompt-cache usage; they are not a billing
statement or a freshly verified provider price quote.

## Manual verification and PDFs set aside

Original rendered pages/crops were visually inspected by the main agent and a
review subagent. Judgments were checked against printed source, not merely
whether labels awarded a higher score. Notes for every cohort member are in
`manual_review.json`; schedule changes are in `comparison.json` and
`repeat/comparison.json`.

Four PDFs have at least one unambiguous, source-supported high-over-low
correction in the observed pairs. They are copied locally under
`data/out/pdf-detail-study/2026-10-09/`, with identities and explanations in
`benefit_manifest.json`:

| PDF | Verified correction | Source | Classification |
|---|---|---|---|
| Blessed Trinity Buffalo | Removes invented Thursday 11:00 Mass; restores October 28 healing Mass at 19:00 | Cover's Mon/Tue/Wed/Fri schedule, and page 4 announcement | **Observed raster-text gain** |
| All Saints Corning | Adds three explicitly timed ?No Mass? cancellations | Page 2: September 28 08:00, September 30 18:00, October 2 12:15 | Native-text gain; labels omit these cancellations |
| Beloved Disciples Lancaster | Restores October 2 08:30 Our Lady of Pompeii Mass | Page 3 OLP row; page 9 resolves abbreviation | Native-text row-coverage gain |
| Sacred Heart Auburn | Restores September 25 St. Alphonsus cancellation; correctly makes 11:30 First Friday Mass recurring | Pages 2 and 3 | Native-text exception/recurrence gain |

The **raster-only candidate folder contains Blessed Trinity alone**. The other
three are kept separately as native-semantic observed gains so that training
does not conflate optical resolution with interpretation.

Important qualification: these are **observed advantages, not proven causal or
repeatable benefits**. In Blessed Trinity's second and third pairs, both detail
levels omitted the healing Mass. Low was correct on the weekday schedule in
those later pairs. Beloved's missing row was recovered by repeat low too.
Sacred Heart's initial cancellation omission disappeared on repeat low.

### Other differing cases and label concerns

| PDF | Visual review finding |
|---|---|
| Blessed Family 7 West Seneca | Nine of ten pages scanned. Initial and third pairs tie; repeat high drops clearly printed first/third Tuesday confession 17:00?17:45. High detail was not consistently beneficial. |
| Assumption?Resurrection | Weekly Wednesday confession prints ?after 11:15 Mass?; noon is explicit only on the dated September 23 calendar. High's weekly-noon consolidation improves label F1 but requires adjudication. |
| Fatima Shrine Lewiston | Low reads a small raster October 12 16:00 Mass flyer in both pairs. The dated event duplicates a weekly slot. Printed September 26 ?8 pm? conflicts with regular 8 am. Repeat high's calculated healing-Mass confession also exposes a plausible label omission. |
| Catholic Community Buffalo North | Moved-Mass cancellation handling and combined mission/reconciliation component timing differ. Native-text policy interpretation, not an optical recovery. |
| Our Lady of the Lakes | ?First full weekend? plus explicit October/November dates cannot be represented reliably by a fixed Sunday ordinal. Repeat low uses the printed dates and beats high. |
| Our Lady of the Valley | Page 7 advertisement prints chapel open daily 06:00?19:00; text is native-extractable. Whether opening hours establish an adoration schedule is a policy issue. Initial low includes seven daily events; other runs omit them. |
| All Saints Syracuse | ?Daily Liturgy? standing schedule conflicts with dated Communion Services. Repeat high's better score loses a printed Monday exception. |
| Queen of Peace / St. Thomas More | Heading versus appointment-phone venue attribution is ambiguous. Labels require the entire combined Stations/Rosary/Adoration block as adoration, while current policy warns against inventing component hours. |

Sacred Heart's raster Children's Adoration flyer also visibly states third
Friday at 09:30; deleting it can improve F1 because labels omit it. This is not
clean evidence that high detail improved extraction. Existing labels were left
unchanged to keep the experiment auditable.

## Statistical PDF features

Implemented in `src/pdf_extract/pdf_detail.py`, using existing dependencies
only. The primary extraction covered **all 127 pages of all 19 PDFs**, with no
feature errors/truncation, in **89.69 seconds**: approximately 4.72 seconds/PDF.

Measurements include:

- Native text character count per page, using pypdf extraction.
- Image draw count, maximum displayed image area, and estimated union coverage;
  transformations and nested forms are handled. Rotation/clipping/transparency
  can still make axis-aligned area estimates imperfect.
- Page dimensions and native glyph-height quantiles from PDFium.
- Raster ink density, row-projection line pitch, connected-component counts,
  and text-like component height/width statistics.
- Estimated glyph/component sizes after a **hypothetical maximum-side 512 px
  resize**. This is a feature normalization assumption, not a provider rendering
  contract or evidence of the exact pixels seen by the API.

Primary raster settings: 100 dpi, 2,000,000 pixels/page cap, grayscale ink
threshold 200. Connected components are geometry, **not OCR**. Native glyph
measurements can include invisible OCR layers.

Examples from schedule-bearing pages:

| PDF/page | Native chars | Image coverage | Text-like components | Median component height at 512 px | Projection pitch at 512 px |
|---|---:|---:|---:|---:|---:|
| Blessed Family, page 2 | 0 | ~100% | 2,325 | 3.72 px | 4.89 px |
| Blessed Trinity, page 2 | 0 | 100% | 2,522 | 4.65 px | 8.84 px |

Blessed Trinity's photo-heavy cover has a misleading 52.95 px projection pitch
and 40% ink density. This illustrates why one whole-page projection statistic
alone is inadequate.

## Classification experiments

Two separate manual targets were evaluated:

1. **Any observed source-supported advantage:** the four set-aside PDFs.
2. **Observed raster-text advantage:** Blessed Trinity only.

?False positive? here means escalation without a confirmed observed gain; it
does not prove that the PDF can never benefit. Ambiguous/mixed cases were not
promoted to positive training labels. These labels are deliberately conservative
and the sample is small.

Decision stumps were searched over nine document features, both inequality
directions, and all between-observation thresholds. Loss is **5 ? false
negatives + false positives**. Leave-one-out refits the threshold using only
the other 18 PDFs; there is no held-out publication-week dataset.

| Method / target | True positives | False negatives | Extra escalations | Recall | Precision |
|---|---:|---:|---:|---:|---:|
| Scan-risk rule / four observed gains | 1 | 3 | 1 | 25% | 50% |
| Fitted stump, training / four gains | 4 | 0 | 1 | 100% | 80% |
| Fitted stump, leave-one-out / four gains | 1 | 3 | 1 | 25% | 50% |
| Scan-risk rule / one raster gain | 1 | 0 | 1 | 100% | 50% |
| Fitted stump, training / raster gain | 1 | 0 | 0 | 100% | 100% |
| Fitted stump, leave-one-out / raster gain | 0 | 1 | 2 | 0% | 0% |

The broader fitted stump chose **minimum native glyph height >= 2.934 px**?a
counterintuitive direction if tiny text were causing the errors. It selects
Corning, Beloved, Trinity, Sacred Heart, and Blessed Sacrament Albany. Its
leave-one-out collapse indicates coincidental separation, not a defensible
benefit model.

The raster-only stump chose mean image coverage >= 0.958, separating a single
positive perfectly in training. Holding out that sole positive removes any
positive training example. Its 100% training score has no generalization value.

The initial broad native/raster-size heuristic escalated **17/19** PDFs and
still missed Sacred Heart. Native small glyphs and advertising images are too
common to be useful standalone benefit indicators in native-PDF input.

### Conservative scan-risk rule

`route_scan_risk` requires positive evidence of small raster text:

1. A scan page has **<80 native characters** and **>=70% image coverage**.
2. Small-text evidence additionally requires **>=100 text-like components**,
   **1.5?35% ink density**, **median component height <=6 px** and
   **line pitch <=12 px** in 512-px-normalized units.
3. Escalate if that evidence occurs in any of the first three pages, **or** if
   at least half the document is scanned and any page has that evidence.
4. Feature errors, truncation, or no analyzed pages conservatively escalate.
   A top-level PDF parse/render exception still needs caller-level fallback.

Early-page evidence reduces false positives from image-only advertising at the
end of otherwise native-text bulletins. The predominantly-scanned fallback
reduces false negatives from unstable projection profiles on individual pages.

This selects Blessed Family and Blessed Trinity: **10.5%** of the cohort.
It has zero observed raster-target false negatives, but that means **one
positive captured**, not a validated population recall estimate. It misses the
three native-semantic gain cases, which these optical features are not intended
to solve.

Using the recorded predictions as a counterfactual hybrid:

| Policy | Initial strict F1 | Repeat strict F1 |
|---|---:|---:|
| All low | 95.09% | 93.43% |
| All high | 94.32% | 94.02% |
| Scan-risk-selected high, otherwise low | 95.37% | 93.28% |

The hybrid helps the initial trial and slightly hurts the repeat. This is
another reason not to claim demonstrated production accuracy gains.

### Lower-cost feature extraction experiment

At 60 dpi with a 250,000-pixel cap, all features took **33.26 seconds**. The
first stricter rule required at least half the pages individually to pass every
small-text measurement; it **missed Blessed Trinity** because raster geometry
changed with sampling resolution.

The revised predominantly-scanned fallback above selects **the same two PDFs
at both feature resolutions**, without new API calls. Both the previous and
revised results are retained. This is an explicit recall-oriented refinement
on the observed cohort, not an independent validation set. The CLI defaults
remain the primary 100-dpi settings.

## Recommendation

Do **not** deploy the fitted threshold or call this a validated benefit model.
The scan-risk rule is a reasonable conservative escalation candidate, but
high detail alone does not prevent wrong schedules. Keep semantic/source
validation, and treat ambiguous source/label cases separately.

To validate automatic routing, collect multiple additional publication weeks,
more scanned and mixed-content schedules, and repeated paired calls. Correct
policy/label inconsistencies through an explicit labeling review, not by
silently changing this experiment's ground truth. Evaluate by held-out
parish/week and report low-detail error recovery and high-detail regressions,
not just one overall F1 number.

## Reproduction and artifacts

Validation: **924 tests passed** in the full repository suite. Focused Ruff
lint and formatting checks also pass for the new source, scripts, and tests.

Run from the repository root. Fresh API runs incur provider charges. Use a new
output directory to preserve this experiment:

```powershell
uv run python scripts/pdf_detail_study.py prepare --output data/runs/pdf-detail-study/eval/new-study
uv run python scripts/pdf_detail_study.py run --output data/runs/pdf-detail-study/eval/new-study --detail low --refresh
uv run python scripts/pdf_detail_study.py run --output data/runs/pdf-detail-study/eval/new-study --detail high --refresh
uv run python scripts/pdf_detail_study.py analyze --output data/runs/pdf-detail-study/eval/new-study
uv run python scripts/pdf_detail_study.py features --output data/runs/pdf-detail-study/eval/new-study
```

Manual source review must create `manual_review.json` before fitting or copying
benefit candidates. For the already-reviewed saved study:

```powershell
uv run python scripts/pdf_detail_fit.py
uv run python scripts/pdf_detail_study.py set-aside
uv run pytest
```

- `cohort.json`, `labels/`: matched identities and frozen ground truth.
- `low/`, `high/`, `repeat/`, `targeted/`: predictions, usage, run summaries,
  and scored reports.
- `comparison.json`, `repeat/comparison.json`, `targeted/comparison.json`:
  substantive schedule differences, separate from raw note/order differences.
- `manual_review.json`, `benefit_manifest.json`: visual judgments and copied
  PDF identities/locations.
- `features.json`: primary measurements plus the reduced-resolution experiment;
  its saved historical rule outputs precede the final recall-oriented refinement.
- `classification_experiments.json`: fitted rules, leave-one-out results,
  current-rule counterfactuals, and revised lower-resolution decisions.
- `evidence/`: local rendered pages/contact sheets/crops, ignored in git.

PDF copies and visual evidence stay local; prediction/measurement/review JSON
and this report are available as repository changes. Production defaults and
existing source labels are unchanged.
