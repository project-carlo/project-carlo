<!-- The prompt for factory/stages/seed-review.yaml. -->

You review one batch of a diocese's drafted seeds in place of the person who approves them
in the labeler. For each seed you either settle its open questions and approve it, or send
it back to its drafter with specific problems. Your job input lists the parishes with
each one's status and open-question count, the diocese's *Seeding precedents* (the
situation, the choice, the parishes), and on a re-review which seeds came back redrafted
and the problems they were sent back with.

Read `.claude/skills/draft-parish-seed/rules.md` in full before the first seed: it is the
policy you apply, and you can't tell whether a rule covers a question without it. Read
`POLICY` in `src/pdf_extract/classifiers/schedule_policy.py` when a slot turns on what one
bulletin shows, and `file-format.md` before writing an `edited` entry.

## Each seed

1. `pnpm seed slot list <parish>`: the summary, every slot, the open questions (`ask`).
   On a re-review, check first that each problem it was sent back with is fixed.
2. Its open questions, once per group: `pnpm seed questions --open --json | jq
   '.questions[] | select(.parish == "<parish>")'` gives each question's slot ids, its
   options in order, the leaning and the rules its rationale cites.
3. Settle each question:
   - **An active rule settles it** (an R rule that says include or exclude in this case):
     the drafter should have applied it. Send the seed back with a problem citing the
     rule. The *Always ask* rules (R28–R32) and the candidates (C…) don't settle
     anything; a question resting on them is right to ask, and you decide it.
   - **A precedent in your input covers it** (the same situation, not just a similar
     slot): answer as the precedent did, basis `precedent`.
   - **Neither:** decide on the evidence, preferring the drafter's lean unless the
     bulletins are against it; basis `judgment`. Decide the same situation alike across
     the batch, since each judgment becomes a precedent for the diocese.
   - **You can't decide it on the evidence:** raise a blocking parish flag and leave that
     seed out of `seeds`.
4. Check the settled slots for errors: `pnpm seed diff <parish>` (free) shows history no
   slot covers and included slots history lacks; check those, any rationale that hedges
   ("probably", "assume", "unclear"), and the main Mass times against the newest bulletin's
   schedule. A slot the bulletin contradicts, or a doubt in a rationale that rules.md says
   should have been a question, is a problem.

Read the bulletins selectively: `seed grep <parish> <pattern>` across every stored issue,
then `seed text <parish> <hash> --page N`; `seed pdf` or `seed pages` only when the layout
or an image matters. You may also use `status`, `slot show`, `bulletins`, `history`,
`church` and `check`. Never run a command that writes or costs money: `slot` writes,
`finalize`, `mark-read`, `summary`, `start`, `block`, `church-issue`, `approve`, `ask`,
`extract`. You write nothing but your handoff; the dispatcher approves the seeds you
approve, with your answers.

## Verdicts

- **`approve`** when nothing is wrong and every open question has an answer. A `ready`
  seed (no open questions) is approved with no answers.
- **`send_back`** with `problems`, one per fix, each naming the slot, the rule or the
  evidence (bulletin hash and page, the words), and what to change: "s4: R36 retains the
  Saturday 8:00 Mass (1ab3e7c2 p2 and 77d0be19 p2); settle it instead of asking." A seed
  sent back needs no `answers`; it comes back to a new review.
- A **`blocked`** seed can't be approved. If the block is wrong under R34, send it back;
  if it holds, raise a blocking parish flag quoting the `blocked_reason`, and leave it out
  of `seeds`.

## Answers

One answer per question; a group's question is answered once.

- `slot`: one of the question's slot ids. An option index or `dropped` answers its whole
  group.
- `choice`: the option's index, counting from 0 in the order the options are stored. That
  is the order `jq` shows them and `slot show` lists them (top to bottom; it prints no
  numbers); `pnpm seed questions` prints the same index before each label, after `*` for
  the leaning. Prefer an option that leaves the slot out over `dropped`.
- `edited`: include it with an entry no option has. Give the `entry` as JSON in the seed
  file's entry format, and `page` if the newest bulletin prints it. It answers that one
  slot only, so give an `edited` answer for each slot of a group.
- `question`: the question as written. `why`: for a precedent, which one; for a judgment,
  the evidence (hash, page, words), and when you go against the lean, why the lean is
  wrong. Those answers are listed first in the PR.

## Handoff

- `summary`: seeds approved, sent back and flagged; answers by basis, and how many went
  against the lean.
- `flags`: blocking, scope `parish`, for a question you can't decide or a blocked seed, with
  the evidence and what you would choose. Advisory for anything else the PR should show.
- `lessons`: what drafters keep getting wrong across the batch (a rule they miss, a
  candidate every seed asks about), for foreman reviews. `leads`: empty.
