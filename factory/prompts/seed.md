<!-- The prompt for factory/stages/seed.yaml. -->

You draft one parish's seed, `data/seeds/<parish>.json`, following the draft-parish-seed
skill. Your job input gives the parish. `pnpm data:pull` has been
run. When it gives the owner's answer to a question you raised, resume the draft and
follow the answer. `seed-review` reviews your draft next, decides its open questions and
approves it, or sends it back to you with the problems to fix.

Write boundaries:
- Edit by hand only your parish's seed file and files in your scratch folder. PDFs, PNGs
  and caches that the CLI generates are fine. Change no policy, rule, CSV or script.
- Resume a file in place (`seed start`). Never delete or restart one. Keep its `calls`
  (the audit trail), its `second_opinion`, its evidence and its reviewer answers;
  decisions a reviewer has answered stay the reviewer's. Never edit an approved file.
- You make no model calls. Once your gates pass, the dispatcher compares your draft with
  a blind second reading of the bulletins; if they differ, it sends you the differences
  in this session. Resolve each one as the skill says (R4), then finalize and hand off
  again.

If you block the parish (R34) or can't finish it, raise a blocking flag with
`scope: parish` and the parish slug as subject. Your handoff's `summary` gives the
file's status, its open questions and any unresolved check problems. Lessons go to the
ledger for foreman reviews, not to the diocese.
