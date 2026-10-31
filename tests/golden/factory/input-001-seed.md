# Factory job testd-seed-1/001-seed: seed

You are a worker in the onboarding factory (docs/factory-spec.md): one fresh session that
runs one job and ends. Code scheduled you, and no person is watching.

- Diocese: `testd`. This directory is the Run's worktree, on branch `factory/testd-seed-1`.
- Your scratch folder is `scratch/testd-seed-1/001-seed/`; the Run's shared tools folder
  is `scratch/testd-seed-1/tools/` (read its README.md before writing a script).
- You may change only `data/dioceses/testd/**`, `scratch/testd-seed-1/001-seed/**`. Any other change is reverted and the job sent back.
- You can't commit, push, use `gh` or start agents. When you finish, the dispatcher runs
  its gates (`pnpm --silent diocese check testd`), then commits your work.
- Nobody answers questions during the job. A decision you can't make becomes a flag in
  your handoff, which is all the dispatcher reads.

## Handoff

Before you end, write `scratch/testd-seed-1/001-seed/handoff.json`, about 300 tokens:

```json
{
 "status": "done | partial | blocked",
 "summary": "one or two sentences",
 "flags": [
  {
   "severity": "blocking | advisory",
   "scope": "parish | run",
   "subject": "roster:id or parish slug",
   "question": "what needs deciding",
   "evidence": [
    "path#section or URL with date"
   ],
   "suggestion": "what you would do"
  }
 ],
 "leads": [
  {
   "touches": "batch id or roster:id",
   "note": "..."
  }
 ],
 "lessons": [
  "reusable publisher or rule lesson"
 ]
}
```

- `status`: `done` when the job is finished; `partial` if you ran out of room and should be
  continued; `blocked` when nothing more can be done without a decision.
- `flags`: `blocking` sets a parish aside (`scope: parish`, subject `roster:id` or the
  parish slug) until the owner answers an issue, while the rest of the Run carries on; a
  blocking flag with `scope: run` stops the Run. `advisory` is listed in the PR: leave
  that parish open or excluded with a reason. Give evidence and what you would do. Don't
  flag what the records already carry (README, *What to flag*): a church left in `open/`,
  a bulletin `fetch` can't collect (`fetch_gap`), a check blocked for now (`research`
  with a retry trigger), or an address you chose between sources.
- `leads`: something outside your input that later work should know, naming the batch id
  or `roster:id` it touches.
- `lessons`: only what is reusable beyond one parish, one line each.

## Your job: seed `st-ann`

Draft `data/seeds/st-ann.json`, with `scratch/testd-seed-1/001-seed/` as
your scratch folder.
