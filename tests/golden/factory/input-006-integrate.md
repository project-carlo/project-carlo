# Factory job testd-map-1/006-integrate: integrate

You are a worker in the onboarding factory: one fresh session that runs one job and ends.
Code scheduled you, and no person is watching.

- Diocese: `testd`. This directory holds the Run's files, from branch `factory/testd-map-1`.
- Your scratch folder is `scratch/testd-map-1/006-integrate/`; the Run's shared tools
  folder is `scratch/testd-map-1/tools/` (read its README.md before writing a script).
- You may change only `data/dioceses/testd/**`, `scratch/testd-map-1/006-integrate/**`. Any other change is reverted and the job sent back.
- You can't commit, push, use `gh` or start agents. When you finish, the dispatcher runs
  its gates (`pnpm --silent diocese check testd`), then commits your work.
- Nobody answers questions during the job. A decision you can't make becomes a flag in
  your handoff, which is all the dispatcher reads.
- Keep your context small: everything you read is read again on every later step. Send
  long output to a file in your scratch folder and read only the part you need (`jq`,
  `grep`, `head`); grep a long document before reading it.

## Read first

Read these in full before you start; they are the rules this job is held to.

- `scratch/testd-map-1/006-integrate/reads/data/dioceses/README.md`: *Fields*, *Traps* from `data/dioceses/README.md`
- `.claude/skills/s/rules.md`

## Handoff

Before you end, write `scratch/testd-map-1/006-integrate/handoff.json`, about 300 tokens:

```json
{
 "status": "done | partial | blocked",
 "summary": "one or two sentences",
 "flags": [{"severity": "blocking | advisory", "scope": "parish | run", "subject": "roster:id or parish slug", "question": "what needs deciding", "evidence": ["path#section or URL with date"], "suggestion": "what you would do"}],
 "leads": [{"touches": "batch id or roster:id", "note": "..."}],
 "lessons": ["reusable publisher or rule lesson"],
 "rules_changed": [{"was": ["each rule it replaces, word for word"], "now": "the rule that replaces them"}]
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

## Your job: integrate 2 new lessons

The playbook in `data/dioceses/testd/diocese.md` now, by section (bytes of the text
under each heading, as `wc -c` counts them), and the size to keep each near:

- *Bulletin publishers here*: 0.0 KB (target 8.0 KB)
- *Rules settled for this diocese*: 0.0 KB (target 6.0 KB)
- *New lessons*: 2 entries, 0.1 KB, all to fold in or drop
