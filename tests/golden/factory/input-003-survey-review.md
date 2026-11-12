# Factory job testd-map-1/003-survey-review: survey-review

You are a worker in the onboarding factory: one fresh session that runs one job and ends.
Code scheduled you, and no person is watching.

- Diocese: `testd`. This directory holds the Run's files, from branch `factory/testd-map-1`.
- Your scratch folder is `scratch/testd-map-1/003-survey-review/`; the Run's shared tools
  folder is `scratch/testd-map-1/tools/` (read its README.md before writing a script).
- You may change only `data/dioceses/testd/**`, `scratch/testd-map-1/003-survey-review/**`. Any other change is reverted and the job sent back.
- You can't commit, push, use `gh` or start agents. When you finish, the dispatcher runs
  its gates (`pnpm --silent diocese check testd`), then commits your work.
- Nobody answers questions during the job. A decision you can't make becomes a flag in
  your handoff, which is all the dispatcher reads.
- Keep your context small: everything you read is read again on every later step. Send
  long output to a file in your scratch folder and read only the part you need (`jq`,
  `grep`, `head`); grep a long document before reading it.

## Read first

Read these in full before you start; they are the rules this job is held to.

- `scratch/testd-map-1/003-survey-review/reads/data/dioceses/README.md`: *Fields*, *Traps* from `data/dioceses/README.md`
- `.claude/skills/s/rules.md`

## Handoff

Before you end, write `scratch/testd-map-1/003-survey-review/handoff.json`, about 300 tokens:

```json
{
 "status": "done | partial | blocked",
 "summary": "one or two sentences",
 "flags": [{"severity": "blocking | advisory", "scope": "parish | run", "subject": "roster:id or parish slug", "question": "what needs deciding", "evidence": ["path#section or URL with date"], "suggestion": "what you would do"}],
 "leads": [{"touches": "batch id or roster:id", "note": "..."}],
 "lessons": ["reusable publisher or rule lesson"],
 "verdict": "approve | send_back",
 "problems": ["..."],
 "rules": ["each proposed rule you accept, as written"]
}
```

- `status`: `done` when the job is finished; `partial` if you ran out of room and should be
  continued; `blocked` when nothing more can be done without a decision.
- `flags`: a `blocking` flag (`scope: run`) stops the Run until the owner answers an
  issue; this stage can't set a single parish aside. An `advisory` flag is listed in the
  PR. Give evidence and what you would do.
- `leads`: something outside your input that later work should know, naming the batch id
  or `roster:id` it touches.
- `lessons`: only what is reusable beyond one parish, one line each.

## Your job: review the survey of `testd`

The survey was job 1. Read `data/dioceses/testd/diocese.md`,
`data/dioceses/testd/batches.json` and `scratch/testd-map-1/survey.json`.
`pnpm --silent diocese batches validate testd` passed.

An earlier review sent the survey back for these; check they are fixed:
- Split b1 by town.
- Give b2 a reason.
