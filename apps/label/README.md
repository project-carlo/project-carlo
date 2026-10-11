# Bulletin labeling app

A local tool for collecting human ground truth on bulletin event extraction, so
classifier runs can be scored on whether they are *right* rather than only on
whether they agree with each other.

It is a side app: stdlib Python and plain ES modules, no build step and no
dependencies beyond what the pipeline already installs. It reads the classifier
runs under `data/runs/`, serves the bulletin PDFs, and writes labels to
`data/labels.json`.

```bash
pnpm label            # label bulletins in a browser
pnpm label:score      # score every run against the labels collected so far
pnpm label:export     # dump ground truth as flat event rows
```

## Before you start

The app reviews classifier runs, so produce at least one first — two or more is
where it earns its keep:

```bash
pnpm extract -- --classifier gemini-flash
pnpm extract -- --classifier gpt-5.4-mini
```

`pnpm label` then reviews every run in `data/runs/`. Narrow it with
`uv run python apps/label/cli.py serve --classifier gemini-flash --classifier gpt-5.4-mini`.

The server binds to loopback and has no authentication. It reads and writes
files in the repository, so do not expose it to a network.

## How a bulletin is put together

Labeling a bulletin from a blank page is slow, and most of a bulletin is not in
doubt. So the app starts from what the models produced and only asks about the
parts that are actually uncertain. Every event any run proposed becomes a
*candidate*, and candidates are sorted into three buckets:

**Agreed** — proposed by every run that saw the bulletin. These are pre-accepted
and collapsed. Press `g` to review them; they are usually right, and confirming
each one by hand is the single biggest waste of a labeler's time.

**Disagreements** — two runs reading the same slot differently, shown as one
card with the field in dispute called out in the heading and highlighted in each
reading. Press `1` or `2` to say which one is right. Two candidates are treated
as readings of one slot only when they differ in exactly one *logical* field and
no single run proposed both — a run that listed Tuesday and Thursday Masses
separately plainly means two events, and there is no right answer to pick
between them.

The logical fields are deliberately coarser than the columns. `event_kind`,
`day_of_week` and `date` collapse into one field, `when`, because the extractor
filing a standing Sunday slot under a single calendar date moves all three at
once, and the labeler is answering one question, not three.

**Found by one model** — an event nothing else came near. Keep it or drop it.
When it sits one field from something every model agreed on, that neighbour is
shown underneath, which usually turns the decision into a glance.

Below those is a form for adding events **no** model found. Those are what make
recall measurable, which is why marking a bulletin complete means "the accepted
set is exhaustive", not just "I answered the questions".

### Weekly vs. dated is not one of the questions

One split never becomes a decision. When a run files a slot as weekly and
another files it under a single date on that same weekday, the two are the same
slot, and the app merges them into one candidate carrying the weekly reading.
The dated reading shows up as a dashed `also read as 2026-03-08 (Sun)` chip so
the split is visible, but nothing is asked about it and the card is agreed if
every run proposed one reading or the other.

That is not a shortcut. "Adoration Wednesday at 7:00 PM" printed under this
week's calendar genuinely reads both ways, and a labeler staring at one bulletin
is guessing as much as the model was. The pipeline already answers it from
somewhere the bulletin cannot: `pdf_extract.recurrence` promotes a dated event
to weekly once the same slot turns up in each of the preceding weeks in
`data/event_history.json` — the same evidence that makes 173 of 1488 slots in
the current corpus show up filed both ways at some point. Paying a keystroke per
bulletin for a worse answer than `pnpm recurrence:backfill` already gives is not
a good trade.

The consequences run through the rest of the app: an accepted event whose
readings were merged is stored with `when_undetermined: true`, and scoring
counts a prediction that differs from ground truth only on that axis as a hit
(see below). A date on a *different* weekday, or two runs naming two different
dates, is a genuinely wrong reading and is still put in front of you.

## Working through the queue

The queue leads with the bulletins where the models disagree most, because a
bulletin they read identically teaches you very little per minute spent. Other
orderings are available in the header, along with a filter for what to show.

Everything is keyboard-driven; `?` lists the shortcuts.

| Key | Action |
|---|---|
| `j` / `k` | Next / previous decision |
| `1` … `9` | Pick that reading, or accept (`1`) / reject (`2`) a single candidate |
| `a` / `x` | Accept / reject everything on the focused card |
| `u` | Undo the focused card's verdict |
| `n` | Add an event the models missed |
| `[` / `]` | Previous / next PDF page |
| `p` | Jump the PDF to the focused card's page |
| `g` | Show or hide the agreed candidates |
| `s` | Save progress without finishing |
| `enter` | Mark complete and open the next bulletin |
| `shift`+`S` | Skip this bulletin |
| `q` | Queue |

Moving between cards jumps the PDF to the page the models reported the event on,
so the evidence is on screen without hunting for it. The PDF is served truncated
to the same page limit the classifiers were given, so those page numbers line
up. Clicking inside the PDF hands the keyboard to the viewer; the shortcuts come
back as soon as the mouse returns to the decisions column.

Work is saved automatically as you go, so a closed tab costs nothing. A bulletin
stays `in_progress` until every disagreement has a verdict and you press enter.

## What gets written

`data/labels.json`, keyed by bulletin source URL. It is committed: it is the one
artifact in this repo that cannot be regenerated. Writes are atomic, so an
interrupted save cannot truncate it.

Each entry records both what was accepted and what was rejected. The rejections
matter as much as the acceptances — a candidate a human confirmed is wrong is a
scored false positive for whichever run proposed it.

An accepted event carries `when_undetermined: true` when the runs split over
weekly vs. a single date and the app took the weekly reading without asking, so
nobody reading this file later mistakes those three columns for a human's answer.

```json
{
  "https://example.org/bulletin.pdf": {
    "parish_slug": "st-mary-parish",
    "status": "complete",
    "events":   [{ "church_slug": "st-mary", "event_type": "mass", "origin": "model", "sources": ["gemini-flash"], "...": "..." }],
    "rejected": [{ "church_slug": "st-mary", "event_type": "mass", "...": "..." }],
    "labeled_at": "2026-09-03T02:31:00Z"
  }
}
```

Events are identified by `pdf_extract.compare.event_key`, the same tuple the
classifier comparison uses, so a label written here scores directly against a
run. Ids are recomputed on save rather than trusted from the browser.

## Scoring

```
$ pnpm label:score

Ground truth: 12 complete of 14 labeled bulletins

| Classifier   | Bulletins | TP | FP | FN | Precision | Recall | F1    |
|--------------|----------:|---:|---:|---:|----------:|-------:|------:|
| gemini-flash |        12 | 96 |  9 | 11 |     0.914 |  0.897 | 0.905 |
| gpt-5.4-mini |        12 | 99 | 14 |  8 |     0.876 |  0.925 | 0.900 |

### gemini-flash errors
Near misses (right slot, one field wrong):
  - end time: 3
  - start time: 2
Invented events: 1
Missed events: 6
Weekly vs. dated, not scored either way (pnpm recurrence:backfill settles it): 5
```

Only bulletins marked complete count towards precision and recall: a partly
labeled bulletin cannot tell you what a model *missed*. Partial work is not
wasted, though — it still scores precision over the candidates that were ruled
on, reported separately.

The error breakdown is the part worth acting on. A false positive sitting one
field from a false negative is the model reading a real event slightly wrong,
which is a prompt problem; an invented event is a different problem entirely,
and the two are counted separately rather than lumped into one F1.

The last line is neither. A run that read the right slot but filed it weekly
where ground truth has a date — or the reverse — scores as a hit, because that
axis is not labeled and `pdf_extract.recurrence` decides it downstream from
history. The count is still printed: it measures how often the extractor
equivocates, which is worth watching even though it costs no precision here.

## Layout

```
apps/label/
  cli.py               serve / score / export
  labelapp/
    events.py          event identity, logical fields, diffing
    corpus.py          reads runs, bulletins and the parish/church CSVs
    candidates.py      candidates, conflict pairing, per-bulletin review
    store.py           reads and writes data/labels.json
    workspace.py       queue, ordering and progress
    score.py           precision / recall / error attribution
    server.py          stdlib HTTP server: JSON API, PDFs, static files
  static/              the UI (no build step)
```

Tests live with the rest of the suite in `tests/test_label_*.py` and run under
`pnpm test`.
