---
name: foreman
description: Review an onboarding-factory job, a stage's recent jobs, or a whole Run, to find what went wrong and why, and suggest concrete changes to the stage spec (prompt, skill, CLI or model). Use when the owner asks to inspect, review or debug a factory job, stage or Run, or asks why a worker was sent back, blocked, slow or expensive.
---

# Reviewing factory work

The factory (`docs/factory-spec.md`) runs each job as a fresh worker on one stage spec:
`factory/stages/<stage>.yaml`, the prompt and skills it names, and the CLIs they call. You
find where a job went wrong and which part of that spec, or something else, caused it.
You change nothing unless the owner asks.

## Gather

- **One job:** `pnpm factory inspect <job>`. It prints the job's stage and the commit it
  ran at, its input and handoff, the gate results, every attempt and send-back, what later
  stages said about its output (reviewer verdicts, the owner's issue answers), its cost,
  and the path to its transcript.
- **A stage:** `pnpm factory inspect --stage <stage> --last N` lists its recent jobs, and
  `pnpm factory cost --stage` shows where usage goes. Pick the jobs worth reading: sent
  back, blocked, flagged, or far over the stage's usual cost or turns.
- **A Run:** `pnpm factory status`, then inspect the jobs that were sent back or raised
  flags, and the PR's list of seed-review's decisions.

Start from what later stages said: a reviewer's send-back problems, a gate's failure or
the owner's issue answer usually point straight at the mistake. Then read the spec as the
job saw it: `git show <commit>:factory/stages/<stage>.yaml`, and the prompt and skills at
that commit. `git log --oneline <commit>..origin/main -- factory .claude src/pdf_extract`
shows whether it has changed since; don't propose what is already fixed.

## Read the transcript selectively

The transcript is a Claude Code JSONL file, one event per line. Never read it whole.
With `T` its path:

```bash
# every tool call, with its line number
jq -rn 'foreach inputs as $e (0; .+1; . as $n | $e | select(.type=="assistant")
  | .message.content[]? | select(.type=="tool_use")
  | "\($n) \(.name) \(.input|tostring|.[0:200])")' T
# tool errors
jq -rn 'foreach inputs as $e (0; .+1; . as $n | $e | select(.type=="user")
  | .message.content[]? | select(.type=="tool_result" and .is_error==true)
  | "\($n) \(.content|tostring|.[0:300])")' T
# repeated commands
jq -r 'select(.type=="assistant") | .message.content[]? | select(.name=="Bash")
  | .input.command' T | sort | uniq -c | sort -rn | head -20
# the largest tool results (what filled the context)
jq -rn 'foreach inputs as $e (0; .+1; . as $n | $e | select(.type=="user")
  | .message.content[]? | select(.type=="tool_result")
  | "\(.content|tostring|length) \($n)")' T | sort -rn | head
```

Then read the lines around each place that matters with `sed -n 'A,Bp' T | jq ...`. If
`jq` isn't installed, the same filters are a few lines of `python3 -c`.

## What to look for

- **Where it went wrong**, and the first point it could have been avoided.
- **Why**, as one of: the skill text, the agent prompt, the CLI (a missing command, a
  misleading message, output too large), the model or effort, the job's input (a wrong
  lead, a missing path), or the source itself (a publisher no instructions could have
  handled). Only the first four are spec changes.
- **Waste:** repeated work, the same command run again with small changes, a scraper
  rewritten that the tools folder already had, large reads that a grep would have
  answered, turns spent on questions the handoff should have flagged.
- **Instructions ignored or misread:** quote the instruction and the step that broke it.
  Two workers misreading the same line means the line is wrong, not the workers.

## Candidate seeding rules

When reviewing seed Runs, run `pnpm seed questions --answered --by person`: the answers
the owner changed in seed-review's decisions before merging. Look for answers that repeat
a situation, and above all answers that go against the leaning. Propose each as a
candidate for rules.md, in the same form as its Candidates section: a When, a Lean, and
the parishes and slots as evidence. seed-review's own answers (`--by agent`) aren't by
themselves evidence for a candidate.

## Report

1. **What went wrong**, in a few sentences per problem, most costly first.
2. **Evidence:** transcript line numbers and short quotes, gate output, reviewer problems.
3. **Changes**, most useful first: the file (stage spec, prompt, skill, CLI or model),
   the exact edit or a precise description of it, and the reason. Say which jobs it would
   have helped.

Give reasons, not scores. There is no trusted way yet to show a spec change helped; the
commit each later job ran at shows which version of the spec it used, so the next review
can compare.

## Making changes

Only when the owner asks. Branch from `origin/main` (`foreman/<stage>-<topic>`), make the
change, run the tests the change touches, and open a PR against the spec with the
evidence. Never edit `.claude/skills/draft-parish-seed/rules.md`: policy is the owner's;
propose a rule in your report instead. Don't fix a Run's data (records, seeds) as part
of a spec change; name what needs fixing and leave it to the owner.
