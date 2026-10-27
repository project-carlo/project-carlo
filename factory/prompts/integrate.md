<!-- The prompt for factory/stages/integrate.yaml. -->

You fold what the map jobs have learned into the diocese's playbook, so the next batch
reads a short, current guide instead of a growing log. The dispatcher appends each map
job's lessons, as written, one bullet each, to the `## New lessons` section of
`data/dioceses/<d>/diocese.md`; your job input says how many there are.

## Your job

1. Read `diocese.md`'s `### Bulletin publishers here`, `## Rules settled for this
   diocese` and `## New lessons`. Skim the README's *Traps* so you don't copy what every
   diocese already knows.
2. For each new lesson, decide where it belongs:
   - **A publisher's method** (how to read its sites, where its issues are when a site
     blocks the sandbox, an id pattern, a download cap): merge it into *Bulletin
     publishers here*, into the existing bullet for that publisher when there is one.
   - **A decision for more than one record** (how this diocese's campus chapels, shrines
     or family bulletins are treated): add it to *Rules settled*, saying who decided it
     and when, as the section asks ("map batch `dover-north`, 2026-11-02").
   - **One parish's detail** (its URL, its masthead, its closure): drop it. It is already
     in that parish's records; check with `pnpm diocese search` or a grep if in doubt, and
     if it isn't, keep its gist in your `summary` instead.
   - **Already said**, in the playbook or the README: drop it, or sharpen the existing
     line if the lesson adds something.
3. Keep each section a guide, not a log: one bullet per publisher or rule, the method
   first, an example parish only where it helps. Rewrite a bullet that two lessons now
   contradict, keeping what the newer evidence supports; if you can't tell which is right,
   keep both claims in that bullet and say they conflict.
4. Empty *New lessons*: leave its heading and remove every bullet under it.
5. `pnpm --silent diocese validate <d>` must still pass.

Don't change any other section of `diocese.md`, the records or the rosters. A
*Rules settled* line already there stays unless a lesson shows it is wrong; then flag it
rather than editing it.

## Handoff

- `summary`: how many lessons you merged, how many you dropped as parish detail or
  duplicates, and what the playbook gained ("8 lessons: 3 merged into ParishesOnline, 1 new
  rule on campus Masses, 4 dropped").
- `flags`: advisory, scope `run`, when lessons conflict and the evidence doesn't settle
  it, or a lesson contradicts a settled rule. Blocking only if the playbook can't be left
  in a state a map job can follow.
- `lessons` and `leads`: leave empty. A lesson that would help in any diocese stays in
  the playbook when it helps here too; `reconcile` lists those for the PR.
