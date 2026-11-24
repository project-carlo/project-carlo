---
name: draft-parish-seed
description: Draft, resume or repair a parish's believed-schedule seed with the pnpm seed CLI. The method the onboarding factory's seed jobs follow.
---

# Drafting a parish seed

A seed becomes the schedule that update mode maintains. Before your first draft, read three
things: `POLICY` in `src/pdf_extract/classifiers/schedule_policy.py`, in full, which says
what one bulletin shows; [rules.md](rules.md), which holds every seeding decision; and
[file-format.md](file-format.md), which describes the JSON.

Use the local database (`pnpm data:pull` has been run before you start) and the R2 read
keys. Run plain `pnpm seed ...`, since this pnpm rejects `-s`. `pnpm seed --help` lists every
command, and `--json` gives a command's full output.

Do one parish at a time. Finish and finalize each before starting the next.

**A parish with no bulletin** (`bulletin_provider: website_schedule`) gets a source seed
instead, and steps 2–6 don't apply. `seed start` says so. Capture each page of the
parish's own website or Facebook page you rely on with `seed capture <parish> [path or
address]` (run it under `xvfb-run -a`, like `seed site`); it prints the page's text and
the paths of its screenshot tiles, which you Read for what only a picture shows. Cite
captures as `cap <capture>: <its words>` (rules.md R42–R45; file-format.md, "Source
seeds"), say why the schedule looks current with `seed current <parish> "…"`, and commit
`data/seeds/captures/<parish>/` with the file (its texts, and the screenshots `finalize`
puts there for quotes read from a picture). Then steps 7 and 8 as for any parish.

1. **Start.** `pnpm seed start <parish>` creates the draft, or resumes it if it exists, and
   prints the brief: the website, the churches, the bulletins newest first, a summary of
   history, and the newest PDF's path. `seed brief <parish>` prints the brief again. If
   the command says it resumed a draft, read the file before editing and change only
   what needs correcting. A bulletin marked `no PDF (history only)` was pruned: you can
   cite its history but can't read it. Write the file with `seed slot` and the other write
   commands (step 7), not by editing the JSON or writing scripts. `seed slot list <parish>`
   shows the draft's slots and their ids.
2. **Read the newest bulletin in full** (R2). `seed text <parish> <hash>` is the cheapest
   read, and it marks each page that is only an image. It lacks the print of images on
   text pages that have no text layer (a schedule can be set as a picture): `seed pages
   <parish> <hash> --images` packs those into one image, so look at it once. Render a page
   that is only an image, or whose layout matters (a schedule box, a table, a calendar,
   where the text can detach a time from its heading), with `seed pages <parish> <hash>
   --page N`: 100 dpi, which reads ordinary schedule boxes and intentions as well as 150.
   **Zoom when print is small or you are unsure of any digit** of a time you cite: `seed
   pages <parish> <hash> --page N --region bottom-right` (halves, quarters, or
   `x0,y0,x1,y1` fractions from the top left) renders that part sharp, and one zoom can
   take a whole schedule box. Each render prints its token cost; Read shrinks anything
   over 2000 px, so a whole page above about 180 dpi buys nothing. `seed pdf <parish>
   <hash>` writes a bulletin's PDF, with the pipeline's page numbers. Draft its slots,
   then run `seed mark-read <parish> <hash>`.
3. **Compare with history.** `seed history <parish> [--bulletins N]` prints one table per
   bulletin, and it is free. Apply R7–R9. Use your own readings across bulletins to
   establish recurrence (R35); one silent issue does not erase a repeated schedule
   (R36). For the latter, record `--weekly-omission "why only an omission" --page -`
   and the older bulletin readings. History's extracted rows are hints, not
   substitutes for those readings.
4. **Read further back** when R3 or R11 calls for it. Start with `seed grep <parish>
   [pattern]`, which searches every stored bulletin at once (with no pattern, it searches
   for schedule words). Then read one bulletin at a time with `seed text <parish> <hash>
   [--page N]`, which usually costs less context than images. Use `seed pages` only for a
   page that is an image or whose layout matters. For an issue of more than a few pages
   that is only images, `seed pages <parish> <hash> --sheet [--page 2-10]` tiles its pages
   into labelled sheets (one image for up to about 12 pages, each sharp enough to tell
   what it holds) to find the pages you need; render just those, and zoom (`--region`)
   where the print is small. For two or three pages a sheet saves nothing: render them. Run `seed mark-read` on each
   bulletin you read. To look up a church, use `seed church <name and town>` (R21).
5. **Website (when R5 calls for it).** `seed site <parish>` prints the
   homepage's text and the links that look like schedules. `seed site <parish>
   /mass-times` (or a full address) prints one of those pages, and each page is kept for
   a day. Under R6 a real, current parish schedule that fits the bulletin may supply a
   missing time. Quote it and record why it appears current and fits the newest read
   bulletin using `--website-current` and `--website-context`. Keep its slot page null.
6. **No model calls.** Decide from your own reading of the bulletins, history and the
   website. The one model call a seed gets is the dispatcher's second opinion, after
   you finish (step 9, R4).
7. **Decide each slot** by [rules.md](rules.md). Apply active rules and POLICY exceptions
   first, cite the rule in the rationale, then ask about what remains unclear. Do not
   offer a false weekly pattern when the format cannot express the real one (R33).
   Preserve reviewer answers and group only questions that truly share one answer
   (R27). `seed slot include`, `slot
   exclude` and `slot ask` add slots (one per day and time), and `seed slot batch
   <parish> plan.txt` writes a whole parish at once; the syntax and an example are in
   [file-format.md](file-format.md), "Writing slots", and `pnpm seed slot --help`. Each
   write is checked before it is saved. Then `seed summary <parish> "..."`, and `seed
   church-issue` (R23) or `seed block` (R34) where they apply.
8. **Finalize.** `pnpm seed finalize <parish>` does the bookkeeping and then checks the
   file. It fills in defaults, splits `bulletins` sources, adds `history` sources, marks
   the bulletins you cited as read, and sets `as_of` and `status`. Fix what it reports
   with `seed slot edit <parish> <id> ...` (or `slot rm` for a slot you added) and run it
   again until it says OK; `slot show <parish> <id>` prints a slot in full. Deal with
   every `!` warning (R9). `seed diff <parish>` lists those warnings, history events that
   read a slot at another time (R8), and included slots that history never had. If a
   problem can't be resolved, block the parish (R34).
9. **The second opinion (R4).** In the factory, once your draft passes its gates, the
   dispatcher compares it with gpt-6-luna's blind reading of the newest bulletins and
   writes that reading into the file as `second_opinion`. If they differ, it sends you
   the differences, with luna's quotes and pages, in the same session. `seed opinion show
   <parish>` lists them and where each stands. For each, re-read the page it quotes, then
   change the slot (`slot edit`...; the difference goes away), ask (a question with
   luna's reading as an option), or keep the draft: `seed opinion keep <parish> d3 --src
   "1ab3e7c2 p2: Sat 4:00 PM Vigil" --why "R1: printed in the schedule box of all three
   issues"`. Then finalize again; `seed check` fails while any difference is open, or if
   `second_opinion` was edited. A parish you block still answers it.
